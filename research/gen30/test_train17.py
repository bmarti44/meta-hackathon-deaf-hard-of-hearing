"""Gen30 guarantees (adapted from Gen29's test_train16): train17 differs from Gen29's train16 ONLY by the new `aug0625` mode.
Base Gen28 notes: train15 differs from Gen27's train14 ONLY by the new `aug25` mode.
- `aug50` batches from train15 are bit-identical to train14's (same draws, same augmentation);
- `aug25` makes the same main-RNG draws as `dry`/Gen19 (paired speech and noise) and puts
  ~22.5% of items in rooms (67.5% dry noisy / 22.5% reverberant noisy / 10% dry quiet);
- resume identity refuses a room-mode change (aug50 <-> aug25)."""
import importlib.util, subprocess, sys
from pathlib import Path
import numpy as np, pytest, torch

HERE = Path(__file__).resolve().parent
G27 = HERE.parent / "gen27"
sys.path.insert(0, str(HERE.parent / "gen15")); sys.path.insert(0, str(G27))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


t14 = load("train14_g30", G27 / "train14.py")
t15 = load("train15_g30", HERE.parent / "gen28" / "train15.py")
t16 = load("train16_g29", HERE.parent / "gen29" / "train16.py")
t17 = load("train17_g30", HERE / "train17.py")
T27 = load("test_train14_g30", G27 / "test_train14.py")   # reuse its fake pool and synthetic bank fixtures


def _fake(mod, monkeypatch):
    return T27._fake(mod, monkeypatch) if hasattr(T27, "_fake") else None


@pytest.fixture
def bank():
    return T27.BANK if hasattr(T27, "BANK") else None


def _batches(mod, room, monkeypatch, n=40, seed=20261117):
    pool, spk = T27._fake(mod.t13, monkeypatch) if hasattr(T27, "_fake") else (None, None)
    rng, ra = np.random.default_rng(seed), np.random.default_rng([seed, 27])
    return [mod.make_batch(rng, pool, spk, room=room, aug_rng=ra, bank=T27.BANK) for _ in range(n)]


def test_aug125_identical_to_gen29(monkeypatch):
    A = _batches(t16, "aug125", monkeypatch, n=6); B = _batches(t17, "aug125", monkeypatch, n=6)
    for a, b in zip(A, B):
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:5] == b[3:5] and a[5] == b[5]


def test_aug0625_fractions_and_pairing(monkeypatch):
    C = _batches(t17, "aug0625", monkeypatch, n=400)
    conds = [m["cond"] for b in C for m in b[5]]
    f = {k: conds.count(k) / len(conds) for k in ("dry_noisy", "rev_noisy", "dry_quiet")}
    assert abs(f["dry_noisy"] - 0.84375) < 0.035 and abs(f["rev_noisy"] - 0.05625) < 0.02 and abs(f["dry_quiet"] - 0.10) < 0.03, f
    # dry items of aug25 equal the dry stream exactly (same main-RNG draws)
    pool, spk = T27._fake(t17.t13, monkeypatch)
    r1, r2, ra = np.random.default_rng(7), np.random.default_rng(7), np.random.default_rng([7, 27])
    for _ in range(10):
        D = t17.make_batch(r1, pool, spk, room="dry")
        A = t17.make_batch(r2, pool, spk, room="aug0625", aug_rng=ra, bank=T27.BANK)
        assert D[4] == A[4] and D[3] == A[3]
        for i, m in enumerate(A[5]):
            if m["cond"] != "rev_noisy":
                assert torch.equal(D[0][i], A[0][i]) and torch.equal(D[2][i], A[2][i])
    assert r1.random() == r2.random()


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
@pytest.mark.skipif(not _DATA.exists(), reason="data missing")
def test_resume_refuses_room_change(tmp_path):
    run = lambda name, *x: subprocess.run([sys.executable, str(HERE / "train17.py"), "--loss", "sisdr", "--snr", "legacy", "--mode", "scratch",
                                            "--steps", "4", "--state-every", "2", "--diag-every", "0", "--val-every", "0", "--device", "cpu",
                                            "--out", str(tmp_path / f"{name}.pt"), "--log", str(tmp_path / f"{name}.json"), *x], capture_output=True, text=True)
    a = run("a", "--room", "aug0625"); assert a.returncode == 0, a.stderr[-1500:]
    st = tmp_path / "a_state_latest.pt"; assert st.exists()
    assert torch.load(tmp_path / "a.pt", weights_only=False)["room_mode"] == "aug0625"
    r = run("c", "--room", "aug125", "--resume", str(st)); assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr)
