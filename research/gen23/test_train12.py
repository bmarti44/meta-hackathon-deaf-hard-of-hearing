"""Gen23 guarantees: `sisdr_cs5` is exactly neg SI-SDR + 5*L_CS (the one
registered change), L_CS is zero at a perfect output, positive otherwise,
finite-gradient at silence (fixed floor), bit-deterministic (CPU STFT),
`--loss sisdr` is still the Gen19 objective, the batch stream is still
Gen19's, and resume stays bit-identical with the new logging."""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t12 = load("train12", HERE / "train12.py")
t8 = load("train8", HERE.parent / "gen19" / "train8.py")


def _sig(n=4, T=16000, seed=0):
    g = torch.Generator().manual_seed(seed)
    return 0.1 * torch.randn(n, T, generator=g)


def test_sisdr_key_is_gen19_objective():
    assert t12.LOSSES["sisdr"] is t12.neg_si_sdr
    ref, est = _sig(), _sig(seed=1)
    assert torch.equal(t12.neg_si_sdr(ref, est), t8.neg_si_sdr(ref, est))


def test_cs5_is_sisdr_plus_five_cs():
    ref, est = _sig(), _sig(seed=1)
    want = t12.neg_si_sdr(ref, est) + 5.0 * t12.compressed_spectral(ref, est)
    assert torch.equal(t12.LOSSES["sisdr_cs5"](ref, est), want)
    assert t12.compressed_spectral(ref, est).shape == (4,)
    assert t12.CS_FFTS == ((256, 64), (512, 128), (1024, 256)) and t12.CS_EXP == 0.3 and t12.CS_WEIGHT == 5.0


def test_cs_zero_at_perfect_positive_otherwise():
    ref = _sig()
    assert float(t12.compressed_spectral(ref, ref.clone()).abs().max()) == 0.0
    assert bool((t12.compressed_spectral(ref, ref + 0.01 * _sig(seed=2)) > 0).all())
    # not scale-invariant (unlike SI-SDR): a level error is penalised
    assert bool((t12.compressed_spectral(ref, 0.5 * ref) > 0).all())


def test_cs_gradient_finite_at_silence():
    ref = _sig()
    est = torch.zeros_like(ref, requires_grad=True)
    t12.compressed_spectral(ref, est).sum().backward()
    assert torch.isfinite(est.grad).all() and float(est.grad.abs().sum()) > 0


@pytest.mark.skipif(not torch.backends.mps.is_available(), reason="no MPS")
def test_cs_gradient_bit_deterministic_from_mps():
    ref = _sig(8, 32000).to("mps")
    gs = []
    for _ in range(3):
        est = _sig(8, 32000, seed=3).to("mps").requires_grad_(True)
        g, = torch.autograd.grad(t12.LOSSES["sisdr_cs5"](ref, est).mean(), est)
        gs.append(g.cpu())
    assert all(torch.equal(gs[0], g) for g in gs[1:])


def _fake(mod, monkeypatch):
    speakers = [f"s{i}" for i in range(14)]
    pool = {s: [0, 1] for s in speakers}

    def get(_p, spk, idx):
        t = np.arange(mod.SEG + 4000, dtype=np.float64)
        f = 100.0 + 37.0 * speakers.index(spk) + 11.0 * idx
        return np.sin(2 * np.pi * f * t / mod.FS).astype(np.float32)

    monkeypatch.setattr(mod, "pool_get", get)
    return pool, speakers


def test_replays_gen19_stream(monkeypatch):
    pool, spk = _fake(t12, monkeypatch)
    _fake(t8, monkeypatch)
    r1, r2 = np.random.default_rng(20261117), np.random.default_rng(20261117)
    for _ in range(4):
        a, b = t12.make_batch(r1, pool, spk), t8.make_batch(r2, pool, spk)
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:] == b[3:]


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_VAL = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
_need_data = pytest.mark.skipif(not (_DATA.exists() and _VAL.exists()), reason="LibriSpeech not present")


def _run(tmp, name, *extra):
    cmd = [sys.executable, str(HERE / "train12.py"), "--loss", "sisdr_cs5", "--mode", "scratch",
           "--steps", "6", "--state-every", "3", "--diag-every", "2", "--device", "cpu",
           "--out", str(tmp / f"{name}.pt"), "--log", str(tmp / f"{name}.json"), *extra]
    return subprocess.run(cmd, capture_output=True, text=True)


@_need_data
def test_resume_is_bit_identical_and_logs_terms(tmp_path):
    a = _run(tmp_path, "a")
    assert a.returncode == 0, a.stderr[-2000:]
    state = tmp_path / "a_state_latest.pt"
    assert torch.load(state, weights_only=False)["step"] == 3
    b = _run(tmp_path, "b", "--resume", str(state))
    assert b.returncode == 0, b.stderr[-2000:]
    sa = torch.load(tmp_path / "a.pt", weights_only=False)["state_dict"]
    sb = torch.load(tmp_path / "b.pt", weights_only=False)["state_dict"]
    assert all(torch.equal(sa[k], sb[k]) for k in sa)
    strip = lambda log: [{k: v for k, v in r.items() if k != "elapsed_s"} for r in log]  # noqa: E731
    la, lb = (json.loads((tmp_path / f"{n}.json").read_text()) for n in "ab")
    assert strip(la["log"]) == strip(lb["log"]) and la["val_log"] == lb["val_log"]
    assert la["loss"] == "sisdr_cs5" and all({"total_loss", "neg_sisdr_db", "cs_raw", "cs_weighted"} <= set(r) for r in la["log"])
    assert all(abs(r["total_loss"] - (r["neg_sisdr_db"] + 5.0 * r["cs_raw"])) < 1e-4 for r in la["log"])
    assert not any("neg_sisdr_loss_db" in r for r in la["log"])
    d = [r["grad_diag"] for r in la["log"] if "grad_diag" in r]
    assert d and all("gn_sisdr" in x and "gn_cs5" in x for x in d)
    r = _run(tmp_path, "c", "--resume", str(state), "--loss", "sisdr")
    assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr)
