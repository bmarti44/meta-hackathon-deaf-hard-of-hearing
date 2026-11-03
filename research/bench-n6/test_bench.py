"""Durable tests for the no-implant bench (bench-n6).

Run: /tmp/gen9env/bin/python -m pytest research/bench-n6/test_bench.py -q
These assert the PROTOCOL.md contract, not current model quality:
silence stays silent, output is peak-limited, the classical baseline
is exactly causal on a shared prefix, and eval speakers are disjoint
from training speakers.
"""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from baselines import CausalSpectralGate, oracle_irm_waveform  # noqa: E402
from common import FS, limit_signal, rms, si_sdr  # noqa: E402
from vocoder import extract_envelopes, vocode  # noqa: E402
from bench import TEST_BABBLE_SPK, TEST_SPK, TRAIN_SPK, evaluate_go_nogo  # noqa: E402


def _speech_like(seed=0, n=FS):
    rng = np.random.default_rng(seed)
    t = np.arange(n) / FS
    x = 0.1 * np.sin(2 * np.pi * 220 * t) + 0.05 * np.sin(2 * np.pi * 440 * t)
    return (x * (0.5 + 0.5 * np.sin(2 * np.pi * 3 * t)) + 0.01 * rng.standard_normal(n)).astype(np.float32)


def test_vocoder_silence_length_peak_determinism():
    z = np.zeros(FS, dtype=np.float32)
    assert float(np.max(np.abs(vocode(z)))) < 1e-4
    x = _speech_like()
    a, b = vocode(x, seed=7), vocode(x, seed=7)
    assert a.shape == x.shape and np.array_equal(a, b)
    assert float(np.max(np.abs(a))) <= 0.89 + 1e-6
    assert rms(a) > 0.01, "vocoded speech-like input must not be muted"


def test_limiter_caps_peak_and_never_invents_signal():
    loud = (5.0 * _speech_like()).astype(np.float32)
    y = limit_signal(loud)
    assert float(np.max(np.abs(y))) <= 0.89 + 1e-6
    assert float(np.max(np.abs(limit_signal(np.zeros(FS, dtype=np.float32))))) == 0.0


def test_causal_gate_suffix_invariance_exact():
    rng = np.random.default_rng(3)
    prefix = _speech_like(n=FS // 2)
    a = np.concatenate([prefix, _speech_like(seed=1, n=FS // 2)])
    b = np.concatenate([prefix, (3 * rng.standard_normal(FS // 2)).astype(np.float32)])
    ya, yb = CausalSpectralGate().process(a), CausalSpectralGate().process(b)
    # Output blocks ENDING inside the shared prefix must be bit-identical.
    # The straddling block (ends after the prefix, writes the last <128
    # prefix samples) legitimately sees suffix samples, so the exact
    # boundary is the last hop multiple <= len(prefix).
    bound = (FS // 2 // 128) * 128
    assert np.array_equal(ya[:bound], yb[:bound])
    assert not np.array_equal(ya[FS // 2:], yb[FS // 2:]), "test has no power if suffixes agree"


def test_causal_gate_does_not_mute_clean_input():
    x = _speech_like()
    y = CausalSpectralGate().process(x)
    assert rms(y) > 0.25 * rms(x)


def test_envelope_identity_and_si_sdr():
    x = _speech_like()
    e = extract_envelopes(x)
    assert e.shape[1] == 22 and e.shape[0] > 10
    assert si_sdr(x, x) > 60


def test_oracle_output_is_bounded():
    # Regression: bench run 1 oracle peaks exceeded 100 at OLA edges.
    clean = _speech_like()
    noise = (0.05 * np.random.default_rng(0).standard_normal(len(clean))).astype(np.float32)
    y = oracle_irm_waveform(clean, noise, clean + noise)
    assert float(np.max(np.abs(y))) < 5.0 * float(np.max(np.abs(clean + noise))) + 0.5


def test_go_nogo_quiet_is_absolute_not_delta():
    good = {"cand": {
        "babble-heldout-spk": {"sisdr": 3.0, "d_sisdr": {"ci_lo": 0.1}, "d_ace_electro_corr": {"ci_lo": 0.01}},
        "quiet": {"sisdr": 20.0, "d_stoi": {"mean": -0.01}, "d_sisdr": {"mean": -127.0}},
        "white-heldout": {"d_sisdr": {"mean": 0.5}}},
        "causal_gate": {"babble-heldout-spk": {"sisdr": 2.5}}}
    assert evaluate_go_nogo(good)["cand"]["earns_vocoder_listening"] is True
    bad = {"cand": {
        "babble-heldout-spk": {"sisdr": 3.0, "d_sisdr": {"ci_lo": 0.1}, "d_ace_electro_corr": {"ci_lo": -0.01}},
        "quiet": {"sisdr": 20.0, "d_stoi": {"mean": -0.01}},
        "white-heldout": {"d_sisdr": {"mean": 0.5}}}}
    assert evaluate_go_nogo(bad)["cand"]["earns_vocoder_listening"] is False
    assert evaluate_go_nogo(good)["cand"]["earns_implant_consideration"] is False


def test_holdout_speakers_disjoint_from_train():
    assert not (set(TEST_SPK) & set(TRAIN_SPK))
    assert not (set(TEST_BABBLE_SPK) & set(TRAIN_SPK))
    assert not (set(TEST_BABBLE_SPK) & set(TEST_SPK))
