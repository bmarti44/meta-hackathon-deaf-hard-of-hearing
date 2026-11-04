"""Gen20 k-sampler: distribution matches the preregistration (80/20, support)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "bench-n6"))
spec = importlib.util.spec_from_file_location("train9", HERE / "train9.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_crowd80_support_and_mix():
    rng = np.random.default_rng(7)
    ks = [mod.sample_k(rng, "crowd80") for _ in range(4000)]
    assert min(ks) >= 4 and max(ks) <= 12
    frac_hi = np.mean([8 <= k <= 12 for k in ks])
    assert 0.76 < frac_hi < 0.84, frac_hi


def test_legacy_support():
    rng = np.random.default_rng(7)
    ks = [mod.sample_k(rng, "legacy") for _ in range(4000)]
    assert min(ks) == 2 and max(ks) == 12


def _fake_pool(monkeypatch):
    speakers = [f"s{i}" for i in range(14)]
    pool = {s: [0, 1] for s in speakers}

    def fake_get(pool_, spk, idx):
        t = np.arange(mod.SEG + 4000, dtype=np.float64)
        f = 100.0 + 37.0 * speakers.index(spk) + 11.0 * idx
        return np.sin(2 * np.pi * f * t / mod.FS).astype(np.float32)

    monkeypatch.setattr(mod, "pool_get", fake_get)
    return pool, speakers


def test_arms_share_everything_except_k(monkeypatch):
    """Astra Gen19 review #4: same continuation seed, arms differ only in k."""
    pool, speakers = _fake_pool(monkeypatch)
    a = mod.make_batch(np.random.default_rng(20261120), pool, speakers,
                       batch=16, k_mode="legacy")
    b = mod.make_batch(np.random.default_rng(20261120), pool, speakers,
                       batch=16, k_mode="crowd80")
    # identical clean targets, SNRs, and noise-kind family per item
    assert (a[0].numpy() == b[0].numpy()).all()
    assert a[3] == b[3]
    fam = lambda ks: ["babble" if k.startswith("babble") else k for k in ks]  # noqa: E731
    assert fam(a[4]) == fam(b[4])
    # quiet and SSN items bit-identical; babble items may differ only via k
    for i, kind in enumerate(fam(a[4])):
        if kind in ("quiet", "ssn"):
            assert (a[1][i].numpy() == b[1][i].numpy()).all(), i
    ka = [int(k[6:]) for k in a[4] if k.startswith("babble")]
    kb = [int(k[6:]) for k in b[4] if k.startswith("babble")]
    assert all(2 <= k <= 12 for k in ka) and all(4 <= k <= 12 for k in kb)


def test_continuation_seed_changes_stream(monkeypatch):
    pool, speakers = _fake_pool(monkeypatch)
    a = mod.make_batch(np.random.default_rng(20261120), pool, speakers,
                       batch=8, k_mode="legacy")
    b = mod.make_batch(np.random.default_rng(20261117), pool, speakers,
                       batch=8, k_mode="legacy")
    assert not (a[0].numpy() == b[0].numpy()).all()
