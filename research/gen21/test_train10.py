"""Gen21 pairing guarantees (Astra Gen20 review): the S48->R48 RNG handoff
must make R48's first batch identical to S48's next batch, and train10's
batch generator must replay Gen19's (train8) stream batch-for-batch."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "bench-n6"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t10 = load("train10", HERE / "train10.py")
t8 = load("train8", HERE.parent / "gen19" / "train8.py")


def fake(mod, monkeypatch):
    speakers = [f"s{i}" for i in range(14)]
    pool = {s: [0, 1] for s in speakers}

    def get(_p, spk, idx):
        t = np.arange(mod.SEG + 4000, dtype=np.float64)
        f = 100.0 + 37.0 * speakers.index(spk) + 11.0 * idx
        return np.sin(2 * np.pi * f * t / mod.FS).astype(np.float32)

    monkeypatch.setattr(mod, "pool_get", get)
    return pool, speakers


def same_batch(a, b):
    return all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) \
        and a[3] == b[3] and a[4] == b[4]


def test_replays_gen19_stream(monkeypatch):
    pool, spk = fake(t10, monkeypatch)
    fake(t8, monkeypatch)
    r1, r2 = np.random.default_rng(20261117), np.random.default_rng(20261117)
    for _ in range(4):
        assert same_batch(t10.make_batch(r1, pool, spk), t8.make_batch(r2, pool, spk))


def test_handoff_next_batch_identical(monkeypatch):
    pool, spk = fake(t10, monkeypatch)
    rng = np.random.default_rng(20261117)
    for _ in range(3):
        t10.make_batch(rng, pool, spk)
    state = rng.bit_generator.state          # S48 @24k snapshot point
    expect = t10.make_batch(rng, pool, spk)  # S48's next batch
    r48 = t10.rng_from_state(state, seed=20261117)
    assert same_batch(expect, t10.make_batch(r48, pool, spk))
