"""Gen22 guarantees: the capped loss is the registered one-line change
(saturates at -30 dB, ~identical for poor reconstructions, never below
plain), `--loss sisdr` is the old objective, and the batch stream is
still Gen19's (so Gen19 seed-17 is an exact control)."""
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t11 = load("train11", HERE / "train11.py")
t8 = load("train8", HERE.parent / "gen19" / "train8.py")


def _sig(n=4, T=8000, seed=0):
    g = torch.Generator().manual_seed(seed)
    return torch.randn(n, T, generator=g, dtype=torch.float64)


def test_sisdr_key_is_gen19_objective():
    assert t11.LOSSES["sisdr"] is t11.neg_si_sdr
    ref, est = _sig(), _sig(seed=1)
    assert torch.equal(t11.neg_si_sdr(ref, est), t8.neg_si_sdr(ref, est))


def test_cap_saturates_at_minus_30db():
    ref = _sig()
    plain = t11.neg_si_sdr(ref, ref.clone())
    cap = t11.neg_si_sdr_cap(ref, ref.clone())
    assert (plain < -60).all()
    assert torch.allclose(cap, torch.full_like(cap, -10 * math.log10(1e3)), atol=1e-3)


def test_cap_barely_changes_poor_reconstructions():
    ref = _sig()
    est = ref + _sig(seed=2)  # ~0 dB
    d = t11.neg_si_sdr_cap(ref, est) - t11.neg_si_sdr(ref, est)
    assert (d >= 0).all() and (d < 0.01).all()


def test_cap_never_below_plain():
    ref = _sig(n=16)
    for s, scale in enumerate([1e-4, 1e-2, 0.3, 1.0, 3.0]):
        est = ref + scale * _sig(n=16, seed=10 + s)
        assert (t11.neg_si_sdr_cap(ref, est) >= t11.neg_si_sdr(ref, est) - 1e-9).all()


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
    pool, spk = _fake(t11, monkeypatch)
    _fake(t8, monkeypatch)
    r1, r2 = np.random.default_rng(20261117), np.random.default_rng(20261117)
    for _ in range(4):
        a, b = t11.make_batch(r1, pool, spk), t8.make_batch(r2, pool, spk)
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:] == b[3:]
