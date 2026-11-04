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


# --- Resume guarantees (Astra pre-launch review item 6): uninterrupted vs
# resumed run with the SAME schedule horizon, diagnostics straddling the
# resume point; changed budget/loss must be refused. CPU, ~40 s, needs data.
import subprocess  # noqa: E402

import pytest  # noqa: E402

_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_VAL = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
_need_data = pytest.mark.skipif(not (_DATA.exists() and _VAL.exists()), reason="LibriSpeech not present")


def _run(tmp, name, *extra):
    cmd = [sys.executable, str(HERE / "train11.py"), "--loss", "cap30", "--mode", "scratch",
           "--steps", "6", "--state-every", "3", "--diag-every", "2", "--device", "cpu",
           "--out", str(tmp / f"{name}.pt"), "--log", str(tmp / f"{name}.json"), *extra]
    return subprocess.run(cmd, capture_output=True, text=True)


@_need_data
def test_resume_is_bit_identical_and_guards_identity(tmp_path):
    import json
    a = _run(tmp_path, "a")
    assert a.returncode == 0, a.stderr[-2000:]
    state = tmp_path / "a_state_latest.pt"  # rolling state at step 3 of 6
    assert torch.load(state, weights_only=False)["step"] == 3
    b = _run(tmp_path, "b", "--resume", str(state))
    assert b.returncode == 0, b.stderr[-2000:]
    sa = torch.load(tmp_path / "a.pt", weights_only=False)["state_dict"]
    sb = torch.load(tmp_path / "b.pt", weights_only=False)["state_dict"]
    assert all(torch.equal(sa[k], sb[k]) for k in sa)
    strip = lambda log: [{k: v for k, v in r.items() if k != "elapsed_s"} for r in log]  # noqa: E731
    la, lb = (json.loads((tmp_path / f"{n}.json").read_text()) for n in "ab")
    assert strip(la["log"]) == strip(lb["log"]) and la["val_log"] == lb["val_log"]
    assert any("grad_diag" in r and r["step"] == 4 for r in lb["log"])  # diag after resume
    assert la["weights_sha256"] != "" and lb["resumed"] is True
    for extra in (["--steps", "8"], ["--loss", "sisdr"]):
        r = _run(tmp_path, "c", "--resume", str(state), *extra)
        assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr)
