"""Gen24 draft guarantees: `--snr legacy` is the Gen19 batch stream bit-for-bit;
`hard60` consumes the same draws (same clean targets, same noise waveforms up
to level), maps SNRs into 0.6*U(-5,-2)+0.4*U(-2,10) ([-5,-3] share 40%), and
resume stays bit-identical with SNR mode in the run identity."""
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


t13 = load("train13", HERE / "train13.py")
t8 = load("train8_g24", HERE.parent / "gen19" / "train8.py")


def _fake(mod, monkeypatch):
    speakers = [f"s{i}" for i in range(14)]
    pool = {s: [0, 1] for s in speakers}

    def get(_p, spk, idx):
        t = np.arange(mod.SEG + 4000, dtype=np.float64)
        f = 100.0 + 37.0 * speakers.index(spk) + 11.0 * idx
        return np.sin(2 * np.pi * f * t / mod.FS).astype(np.float32)

    monkeypatch.setattr(mod, "pool_get", get)
    return pool, speakers


def test_legacy_replays_gen19_stream(monkeypatch):
    pool, spk = _fake(t13, monkeypatch)
    _fake(t8, monkeypatch)
    r1, r2 = np.random.default_rng(20261117), np.random.default_rng(20261117)
    for _ in range(6):
        a, b = t13.make_batch(r1, pool, spk, snr_mode="legacy"), t8.make_batch(r2, pool, spk)
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:] == b[3:]


def test_hard60_pairs_draws_and_rescales_noise_only(monkeypatch):
    pool, spk = _fake(t13, monkeypatch)
    r1, r2 = np.random.default_rng(7), np.random.default_rng(7)
    for _ in range(6):
        L = t13.make_batch(r1, pool, spk, snr_mode="legacy")
        H = t13.make_batch(r2, pool, spk, snr_mode="hard60")
        assert torch.equal(L[0], H[0]) and L[4] == H[4]  # same clean targets and noise kinds
        for i, (sl, sh) in enumerate(zip(L[3], H[3])):
            if sl == 999.0:
                assert sh == 999.0 and float(H[1][i].abs().max()) == 0.0
                continue
            assert -5.0 <= sh <= 10.0
            nz = L[1][i].abs() > 1e-4
            ratio = H[1][i].double()[nz] / L[1][i].double()[nz]
            assert torch.allclose(ratio, torch.full_like(ratio, 10 ** (-(sh - sl) / 20)), rtol=1e-3)
    assert r1.random() == r2.random()  # identical RNG consumption


def test_hard60_map_and_exposure():
    assert t13.map_snr(-5.0, True, "hard60") == -5.0 and t13.map_snr(5.0, True, "hard60") == -2.0
    assert t13.map_snr(-5.0, False, "hard60") == -2.0 and t13.map_snr(10.0, False, "hard60") == 10.0
    assert t13.map_snr(1.234, True, "legacy") == 1.234
    rng = np.random.default_rng(0)
    low = rng.random(200000) < 0.6
    x = np.where(low, rng.uniform(-5, 5, 200000), rng.uniform(-5, 10, 200000))
    old = np.mean((x >= -5) & (x <= -3))
    new = np.array([t13.map_snr(v, l, "hard60") for v, l in zip(x[:50000], low[:50000])])
    assert abs(old - 0.1733) < 0.005 and abs(np.mean(new <= -3) - 0.40) < 0.01


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_VAL = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
_need_data = pytest.mark.skipif(not (_DATA.exists() and _VAL.exists()), reason="LibriSpeech not present")


def _run(tmp, name, *extra):
    cmd = [sys.executable, str(HERE / "train13.py"), "--loss", "sisdr", "--snr", "hard60", "--mode", "scratch",
           "--steps", "6", "--state-every", "3", "--diag-every", "2", "--device", "cpu",
           "--out", str(tmp / f"{name}.pt"), "--log", str(tmp / f"{name}.json"), *extra]
    return subprocess.run(cmd, capture_output=True, text=True)


@_need_data
def test_resume_is_bit_identical_and_guards_snr(tmp_path):
    a = _run(tmp_path, "a")
    assert a.returncode == 0, a.stderr[-2000:]
    state = tmp_path / "a_state_latest.pt"
    b = _run(tmp_path, "b", "--resume", str(state))
    assert b.returncode == 0, b.stderr[-2000:]
    sa = torch.load(tmp_path / "a.pt", weights_only=False)["state_dict"]
    sb = torch.load(tmp_path / "b.pt", weights_only=False)["state_dict"]
    assert all(torch.equal(sa[k], sb[k]) for k in sa)
    ck = torch.load(tmp_path / "a.pt", weights_only=False)
    assert ck["snr_mode"] == "hard60" and ck["snr_mix"].startswith("60% U(-5,-2)")  # Astra Gen23 review: ckpt records the real mode
    la, lb = (json.loads((tmp_path / f"{n}.json").read_text()) for n in "ab")
    strip = lambda log: [{k: v for k, v in r.items() if k != "elapsed_s"} for r in log]  # noqa: E731
    assert strip(la["log"]) == strip(lb["log"]) and la["val_log"] == lb["val_log"] and la["snr"] == "hard60"
    cmd = [sys.executable, str(HERE / "train13.py"), "--loss", "sisdr", "--snr", "legacy", "--mode", "scratch",
           "--steps", "6", "--state-every", "3", "--diag-every", "2", "--device", "cpu",
           "--out", str(tmp_path / "c.pt"), "--log", str(tmp_path / "c.json"), "--resume", str(state)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr)
