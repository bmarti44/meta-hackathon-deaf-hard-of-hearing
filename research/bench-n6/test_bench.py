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
from kpi_scorecard import score_kpis  # noqa: E402
from bench_v2 import TEST_INTERFERERS, TEST_SPK_V2, TRAIN_SPK_V2, VAL_SPK, ncm_simple, vocoded_estoi  # noqa: E402


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


def _kpi_summary(babble_d, stoi_d, ace_d):
    e = lambda d, lo: {"mean": d, "ci_lo": lo, "ci_hi": d + 0.1}  # noqa: E731
    cand = {"babble-heldout-spk": {"sisdr": 6.0, "d_sisdr": e(babble_d, babble_d - 0.5),
                                   "d_stoi": e(stoi_d, stoi_d - 0.01),
                                   "d_ace_electro_corr": e(ace_d, ace_d - 0.02)},
            "ssn": {"d_sisdr": e(4.0, 3.5)}, "white-heldout": {"d_sisdr": e(1.0, 0.5)},
            "quiet": {"sisdr": 27.0, "d_stoi": e(-0.005, -0.01)}}
    return {"cand": cand, "causal_gate": {"babble-heldout-spk": {"sisdr": 2.6}}}


def test_kpi_scorecard_pass_and_fail():
    per_snr = {-5.0: 2.0, 0.0: 2.5, 5.0: 4.0, 10.0: 5.0}
    spatial = {"cand": {"ild_distortion_db": 0.15, "ild_target_err_db": 3.0, "itd_err_samples": 3.0},
               "gate_linked": {"ild_distortion_db": 0.19},
               "unproc": {"ild_target_err_db": 6.0, "itd_err_samples": 5.0}}
    card = score_kpis(_kpi_summary(3.5, 0.04, 0.06), per_snr, spatial, "cand", spatial_candidate="cand")
    assert card["all_required_pass"] is True
    weak = score_kpis(_kpi_summary(1.07, -0.016, 0.011), per_snr, spatial, "cand", spatial_candidate="cand")
    assert weak["all_required_pass"] is False
    failed = {r["kpi"] for r in weak["rows"] if not r["pass"]}
    assert {"babble dSI-SDR", "babble dSTOI", "babble dACE-electro"} <= failed


def test_v2_splits_disjoint_and_complete():
    allv2 = TRAIN_SPK_V2 + VAL_SPK + TEST_SPK_V2 + TEST_INTERFERERS
    assert len(allv2) == len(set(allv2)) == 40
    assert "1988" in TEST_SPK_V2 and "8842" in TEST_INTERFERERS  # legacy continuity


def test_vocoded_estoi_and_ncm_identity():
    x = _speech_like()
    assert vocoded_estoi(x, x) > 0.95
    assert ncm_simple(x, x) > 0.99


def test_holdout_speakers_disjoint_from_train():
    assert not (set(TEST_SPK) & set(TRAIN_SPK))
    assert not (set(TEST_BABBLE_SPK) & set(TRAIN_SPK))
    assert not (set(TEST_BABBLE_SPK) & set(TEST_SPK))
