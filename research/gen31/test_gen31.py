"""Gen31 guarantees.
- blend: a=0 is Gen19 bit-for-bit, a=1 is the fine-tune bit-for-bit, a=0.5 is the float64 midpoint.
- select_alpha: largest alpha whose whole prefix passes; NaN fails; first-point failure -> None.
- VAL panel: 8 F + 8 M test-clean targets, 24 reserved, disjoint from every earlier speaker list.
- train18: scratch batches identical to Gen30's train17; finetune refuses a wrong parent, a missing handoff,
  and a mode change on resume; a finetune smoke starts from Gen19's trained weights and records provenance.
"""
import importlib.util, subprocess, sys
from pathlib import Path
import numpy as np, pytest, torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "gen15")); sys.path.insert(0, str(HERE.parent / "gen27"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


blend = load("blend_g31", HERE / "blend.py")
G19 = REPO / "research/gen19/weights/causal_seed20261117.pt"
HANDOFF = REPO / "research/gen21/weights/rng_handoff_seed20261117.pt"


def test_blend_endpoints_and_midpoint(tmp_path):
    sd0 = blend.load_sd(G19)
    sd1 = {k: v + torch.randn_like(v) * 0.01 for k, v in sd0.items()}
    b0, b1, bh = blend.blend_sd(sd0, sd1, 0.0), blend.blend_sd(sd0, sd1, 1.0), blend.blend_sd(sd0, sd1, 0.5)
    assert all(torch.equal(b0[k], sd0[k]) for k in sd0)
    assert all(torch.equal(b1[k], sd1[k]) for k in sd0)
    assert all(torch.equal(bh[k], (0.5 * sd0[k].double() + 0.5 * sd1[k].double()).float()) for k in sd0)
    assert blend.GRID == (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)


def test_select_alpha_prefix_rule():
    v = load("val_g31", HERE / "val_testclean.py")
    grid = list(blend.GRID)

    def summ(fail_at=(), nan_at=()):
        out = {}
        for al in grid:
            x = -0.01 if al in fail_at else 0.01
            if al in nan_at:
                x = float("nan")
            out[f"{al:.1f}"] = {"-5.0": {"d_sisdr": x, "d_stoi": 0.0}, "0.0": {"d_sisdr": 0.0, "d_stoi": 0.0}}
        return out
    assert v.select_alpha(summ(), grid)[0] == 1.0
    assert v.select_alpha(summ(fail_at=(0.3,)), grid)[0] == 0.2          # a later pass does not rescue the gap
    assert v.select_alpha(summ(fail_at=(0.1,)), grid)[0] is None
    assert v.select_alpha(summ(nan_at=(0.6,)), grid)[0] == 0.5
    s = summ(); s["0.4"]["0.0"]["d_stoi"] = -1e-6
    assert v.select_alpha(s, grid)[0] == 0.3                              # every metric, both SNRs


def test_val_panel_voices():
    v = load("val_g31b", HERE / "val_testclean.py")
    assert len(v.FEMALE) == len(v.MALE) == 8 and len(v.RESERVED) == 24
    assert not (set(v.TARGETS) & set(v.RESERVED))
    assert not ((set(v.TARGETS) | set(v.RESERVED)) & v.used_elsewhere())
    if v.ROOT.exists():
        assert {d.name for d in v.ROOT.iterdir() if d.is_dir()} == set(v.TARGETS) | set(v.RESERVED)


T27 = load("test_train14_g31", HERE.parent / "gen27" / "test_train14.py")
t17 = load("train17_g31", HERE.parent / "gen30" / "train17.py")
t18 = load("train18_g31", HERE / "train18.py")


def test_scratch_batches_identical_to_gen30(monkeypatch):
    for room in ("aug50", "aug0625"):
        pool, spk = T27._fake(t17.t13, monkeypatch)
        A, B = [], []
        for mod, acc in ((t17, A), (t18, B)):
            rng, ra = np.random.default_rng(5), np.random.default_rng([5, 27])
            acc += [mod.make_batch(rng, pool, spk, room=room, aug_rng=ra, bank=T27.BANK) for _ in range(4)]
        for a, b in zip(A, B):
            assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:5] == b[3:5] and a[5] == b[5]


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_RIR = Path("/tmp/rirs/RIRS_NOISES")


def _run(tmp_path, name, *x):
    return subprocess.run([sys.executable, str(HERE / "train18.py"), "--loss", "sisdr", "--snr", "legacy", "--room", "aug50",
                           "--steps", "4", "--state-every", "2", "--diag-every", "0", "--val-every", "0", "--device", "cpu",
                           "--out", str(tmp_path / f"{name}.pt"), "--log", str(tmp_path / f"{name}.json"), *x],
                          capture_output=True, text=True)


@pytest.mark.skipif(not (_DATA.exists() and _RIR.exists()), reason="data missing")
def test_finetune_provenance_and_refusals(tmp_path):
    bad_parent = tmp_path / "fake.pt"
    torch.save({**torch.load(G19, weights_only=False), "note": "x"}, bad_parent)
    r = _run(tmp_path, "w", "--mode", "finetune", "--init-from", str(bad_parent), "--rng-handoff", str(HANDOFF))
    assert r.returncode != 0 and "not the registered Gen19" in (r.stdout + r.stderr)
    r = _run(tmp_path, "h", "--mode", "finetune", "--init-from", str(G19))
    assert r.returncode != 0 and "requires --init-from and --rng-handoff" in (r.stdout + r.stderr)
    r = _run(tmp_path, "s", "--mode", "scratch", "--init-from", str(G19))
    assert r.returncode != 0 and "finetune-only" in (r.stdout + r.stderr)
    ok = _run(tmp_path, "f", "--mode", "finetune", "--init-from", str(G19), "--rng-handoff", str(HANDOFF))
    assert ok.returncode == 0, ok.stderr[-1500:]
    ck = torch.load(tmp_path / "f.pt", weights_only=False)
    assert ck["mode"] == "finetune" and ck["parent_sha256"] == t18.GEN19_SHA[20261117] and ck["room_mode"] == "aug50"
    import json
    log = json.loads((tmp_path / "f.json").read_text())
    assert log["lifetime_steps"] == 24004 and log["lr"] == [1e-4, 1e-5] and log["rng_handoff"] == str(HANDOFF)
    assert log["log"][0]["neg_sisdr_loss_db"] < -3.0, "first loss should reflect Gen19's trained weights"
    import math   # lr is logged after sched.step(): cosine 1e-4 -> 1e-5 over 4 steps, after 1 step
    assert abs(log["log"][0]["lr"] - (1e-5 + 9e-5 * (1 + math.cos(math.pi / 4)) / 2)) < 1e-12
    sd0 = blend.load_sd(G19)
    drift = max(float((ck["state_dict"][k] - sd0[k]).abs().max()) for k in sd0)
    assert 0 < drift < 0.01, drift                                          # 4 small Adam steps away from Gen19
    st = tmp_path / "f_state_latest.pt"; assert st.exists()
    r = _run(tmp_path, "g", "--mode", "scratch", "--resume", str(st))
    assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr)
