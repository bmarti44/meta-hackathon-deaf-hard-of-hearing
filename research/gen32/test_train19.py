"""Gen32 guarantees (Astra's Gen30 review pre-launch checks):
- the penalty is exactly zero when student == teacher, and zero for a batch with no dry items;
- after a perturbation the student gets finite gradients and the frozen teacher gets none;
- batches are unchanged vs Gen31's train18 (make_batch is untouched);
- --preserve-dry is finetune-only; a CPU smoke logs preserve_pen == 0 at step 0 and records the coefficient.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path
import numpy as np, pytest, torch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE.parent / "gen15")); sys.path.insert(0, str(HERE.parent / "gen27"))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


t18 = load("train18_g32", HERE.parent / "gen31" / "train18.py")
t19 = load("train19_g32", HERE / "train19.py")
T27 = load("test_train14_g32", HERE.parent / "gen27" / "test_train14.py")
G19 = REPO / "research/gen19/weights/causal_seed20261117.pt"
HANDOFF = REPO / "research/gen21/weights/rng_handoff_seed20261117.pt"


def _models():
    from model_causal import CausalTasNetEnh
    ck = torch.load(G19, map_location="cpu", weights_only=False)
    s, t = CausalTasNetEnh(), CausalTasNetEnh()
    s.load_state_dict(ck["state_dict"]); t.load_state_dict(ck["state_dict"]); t.eval()
    for p in t.parameters():
        p.requires_grad_(False)
    return s, t


def test_zero_at_init_and_no_dry_items():
    s, t = _models()
    mix = torch.randn(3, 16000) * 0.1
    est = s(mix)
    assert t19.preserve_penalty(est, t, mix, torch.tensor([True, False, True])).item() == 0.0
    assert t19.preserve_penalty(est, t, mix, torch.tensor([False, False, False])).item() == 0.0


def test_gradients_student_only():
    s, t = _models()
    with torch.no_grad():
        for p in s.parameters():
            p.add_(torch.randn_like(p) * 1e-3)
    mix = torch.randn(2, 16000) * 0.1
    pen = t19.preserve_penalty(s(mix), t, mix, torch.tensor([True, True]))
    assert float(pen) > 0
    pen.backward()
    unused = {n for n, p in s.named_parameters() if p.grad is None}
    assert unused == {"blocks.13.res.weight", "blocks.13.res.bias"}, unused   # last block's residual output is unused by design
    g = [p.grad for n, p in s.named_parameters() if n not in unused]
    assert all(torch.isfinite(x).all() for x in g) and any(float(x.abs().sum()) > 0 for x in g)
    assert all(p.grad is None for p in t.parameters())


def test_dry_mask():
    b = [None] * 5 + [[{"cond": "dry_noisy"}, {"cond": "rev_noisy"}, {"cond": "dry_quiet"}]]
    assert t19.dry_mask(b, ["babble", "babble", "quiet"], "aug50", "cpu").tolist() == [True, False, True]
    assert t19.dry_mask(b[:5], ["babble", "quiet"], "dry", "cpu").tolist() == [True, True]


def test_batches_identical_to_gen31(monkeypatch):
    pool, spk = T27._fake(t18.t13, monkeypatch)
    A, B = [], []
    for mod, acc in ((t18, A), (t19, B)):
        rng, ra = np.random.default_rng(9), np.random.default_rng([9, 27])
        acc += [mod.make_batch(rng, pool, spk, room="aug50", aug_rng=ra, bank=T27.BANK) for _ in range(4)]
    for a, b in zip(A, B):
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:5] == b[3:5] and a[5] == b[5]


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_RIR = Path("/tmp/rirs/RIRS_NOISES")


def _run(tmp_path, name, *x):
    return subprocess.run([sys.executable, str(HERE / "train19.py"), "--loss", "sisdr", "--snr", "legacy", "--room", "aug50",
                           "--steps", "3", "--state-every", "0", "--diag-every", "0", "--val-every", "0", "--device", "cpu",
                           "--out", str(tmp_path / f"{name}.pt"), "--log", str(tmp_path / f"{name}.json"), *x],
                          capture_output=True, text=True)


@pytest.mark.skipif(not (_DATA.exists() and _RIR.exists()), reason="data missing")
def test_smoke_and_refusal(tmp_path):
    r = _run(tmp_path, "s", "--mode", "scratch", "--preserve-dry", "100")
    assert r.returncode != 0 and "finetune-only" in (r.stdout + r.stderr)
    ok = _run(tmp_path, "f", "--mode", "finetune", "--init-from", str(G19), "--rng-handoff", str(HANDOFF), "--preserve-dry", "100")
    assert ok.returncode == 0, ok.stderr[-1500:]
    log = json.loads((tmp_path / "f.json").read_text())
    assert log["preserve_dry"] == 100.0 and log["log"][0]["preserve_pen"] == 0.0
    ck = torch.load(tmp_path / "f.pt", weights_only=False)
    assert ck["mode"] == "finetune" and ck["preserve_dry"] == 100.0


def test_val2_identical_panel_and_rule():
    v1 = load("val1_g32", HERE.parent / "gen31" / "val_testclean.py")
    v2 = load("val2_g32", HERE / "val_testclean2.py")
    assert v1.TARGETS == v2.TARGETS and v1.RESERVED == v2.RESERVED and v1.SEED == v2.SEED
    grid = [round(0.1 * i, 1) for i in range(1, 11)]
    rng = np.random.default_rng(0)
    for _ in range(50):
        s = {f"{a:.1f}": {snr: {"d_sisdr": float(rng.normal(0, 0.01)), "d_stoi": float(rng.normal(0, 0.001))} for snr in ("-5.0", "0.0")}
             for a in grid}
        assert v1.select_alpha(s, grid) == v2.select_alpha(s, grid)
    if v2.ROOT.exists():
        assert v2.material_hash(v2.build_items()) == "c2c4f89a59533601dc0a3f2b219fb6b65fe9a4d468349cd5a442709c9873b638"
