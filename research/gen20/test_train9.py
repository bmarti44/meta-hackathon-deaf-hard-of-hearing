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
