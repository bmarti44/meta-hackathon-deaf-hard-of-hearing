"""Gen27 trainer guarantees (research/gen27/astra-agenda-review.md spec):
- `--room dry` is the Gen19 batch stream bit-for-bit, and a short dry run
  gives the same weights as train13 `--loss sisdr --snr legacy`;
- `aug50` makes the same main-RNG draws as Gen19 (paired speech/noise),
  ~45/45/10 dry-noisy/reverberant-noisy/dry-quiet, dry examples identical;
- the reverberant reference is the target through direct + 50 ms with a
  5 ms taper; each source has its own RIR from one room, convolved before
  summation, with real history; SNR is full reverberant target vs summed
  reverberant interferers;
- the frozen manifest splits by room (train/eval disjoint; measured rooms
  eval-only);
- resume is refused when --room changes, and bit-identical otherwise.
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

import numpy as np
import pytest
import torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


t14 = load("train14", HERE / "train14.py")
t8 = load("train8_g27", HERE.parent / "gen19" / "train8.py")
rb = t14.rirbank
FS, SEG, CTX = t14.FS, t14.SEG, t14.CTX


def _fake(mod, monkeypatch):
    speakers = [f"s{i}" for i in range(14)]
    pool = {s: [0, 1] for s in speakers}

    def get(_p, spk, idx):
        t = np.arange(SEG + 4000 + 9000 * idx, dtype=np.float64)
        f = 100.0 + 37.0 * speakers.index(spk) + 11.0 * idx
        return (np.sin(2 * np.pi * f * t / FS) * (1 + 0.3 * np.sin(t / 900.0))).astype(np.float32)

    monkeypatch.setattr(mod, "pool_get", get)
    return pool, speakers


class FakeBank:
    """Synthetic exponentially decaying RIRs, 3 rooms per stratum, 4 positions."""

    def __init__(self):
        r = np.random.default_rng(5)
        self.nfft, self.ctx = t14.NFFT, CTX
        self.rooms = {"short": [], "medium": [], "long": []}
        for si, (st, rt) in enumerate((("short", 0.3), ("medium", 0.5), ("long", 0.7))):
            for j in range(3):
                hs, hes, H, HE, meta = [], [], [], [], []
                for p in range(4):
                    n = int(0.9 * FS); d = 40 + 30 * p + 7 * j
                    h = np.zeros(n); tt = np.arange(n - d) / FS
                    h[d:] = r.standard_normal(n - d) * np.exp(-6.91 * tt / rt) * 0.05
                    h[d] = 1.0 / (1 + p)
                    he = h * rb.early_window(n, d)
                    hs.append(h); hes.append(he)
                    H.append(np.fft.rfft(h, self.nfft)); HE.append(np.fft.rfft(he, self.nfft))
                    meta.append({"direct_idx": d, "drr_db": 0.0, "c50_db": 0.0, "rt60_s": rt})
                self.rooms[st].append({"room_id": f"{st}{j}", "stratum": st, "h": hs, "he": hes,
                                       "H": H, "HE": HE, "meta": meta})


BANK = FakeBank()


def test_dry_is_gen19_stream(monkeypatch):
    pool, spk = _fake(t14.t13, monkeypatch)
    _fake(t8, monkeypatch)
    r1, r2 = np.random.default_rng(20261117), np.random.default_rng(20261117)
    for _ in range(8):
        a = t14.make_batch(r1, pool, spk, room="dry")
        b = t8.make_batch(r2, pool, spk)
        assert all((x.numpy() == y.numpy()).all() for x, y in zip(a[:3], b[:3])) and a[3:] == b[3:]
    assert r1.random() == r2.random()


def test_babble_stems_sum_is_babble(monkeypatch):
    pool, spk = _fake(t14.t13, monkeypatch)
    r1, r2 = np.random.default_rng(3), np.random.default_rng(3)
    for k in (2, 5, 12):
        stems, _ = t14.babble_stems(r1, pool, spk, k=k)
        assert np.array_equal(t14.sum_stems(stems, k), t14.t13.babble(r2, pool, spk, k=k))
    assert r1.random() == r2.random()


def _batches(monkeypatch, n, seed=20261117):
    pool, spk = _fake(t14.t13, monkeypatch)
    _fake(t8, monkeypatch)
    r1, r2, ra = np.random.default_rng(seed), np.random.default_rng(seed), np.random.default_rng([seed, 27])
    out = []
    for _ in range(n):
        A = t14.make_batch(r1, pool, spk, room="aug50", aug_rng=ra, bank=BANK)
        D = t8.make_batch(r2, pool, spk)
        out.append((A, D))
    return out, r1, r2


def test_aug50_pairs_draws_and_keeps_dry_examples(monkeypatch):
    bs, r1, r2 = _batches(monkeypatch, 12)
    n_rev = 0
    for A, D in bs:
        assert A[3] == D[3] and A[4] == D[4]  # same SNR draws and noise kinds
        for i, m in enumerate(A[5]):
            if m["cond"] == "rev_noisy":
                n_rev += 1
                continue
            for j in range(3):  # dry examples: reference, noise and mixture identical to Gen19
                assert torch.equal(A[j][i], D[j][i])
    assert n_rev > 0
    assert r1.random() == r2.random()  # identical main-RNG consumption


def test_aug50_fractions(monkeypatch):
    bs, _, _ = _batches(monkeypatch, 250, seed=11)
    conds = [m["cond"] for A, _ in bs for m in A[5]]
    f = {c: conds.count(c) / len(conds) for c in ("dry_noisy", "rev_noisy", "dry_quiet")}
    assert abs(f["dry_noisy"] - 0.45) < 0.04 and abs(f["rev_noisy"] - 0.45) < 0.04 and abs(f["dry_quiet"] - 0.10) < 0.025, f
    strata = [m["stratum"] for A, _ in bs for m in A[5] if m["cond"] == "rev_noisy"]
    for s in ("short", "medium", "long"):
        assert abs(strata.count(s) / len(strata) - 1 / 3) < 0.06


def test_early_window_50ms_with_5ms_taper():
    d = 123
    w = rb.early_window(4000, d)
    e45, e50 = d + int(0.045 * FS), d + int(0.050 * FS)
    assert (w[:e45 + 1] == 1.0).all() and (w[e50:] == 0.0).all()
    tap = w[e45 + 1:e50]
    assert len(tap) == int(0.005 * FS) - 1 and (np.diff(tap) < 0).all() and 0 < tap.min() and tap.max() < 1
    assert abs(w[e45 + 40] - 0.5) < 1e-12  # half-cosine midpoint


def _independent_render(clean, pre, h):
    """Direct-form linear convolution with history (no FFT), window [CTX, CTX+SEG)."""
    x = np.concatenate([pre.astype(np.float64), clean.astype(np.float64)])
    return np.convolve(x, h)[CTX:CTX + SEG]


def test_reverberant_target_noise_and_snr(monkeypatch):
    pool, spk = _fake(t14.t13, monkeypatch)
    rng, ra = np.random.default_rng(99), np.random.default_rng([99, 27])
    checked = 0
    for _ in range(10):
        r_copy = np.random.default_rng(); r_copy.bit_generator.state = rng.bit_generator.state
        A = t14.make_batch(rng, pool, spk, room="aug50", aug_rng=ra, bank=BANK)
        for i, m in enumerate(A[5]):
            if m["cond"] != "rev_noisy":
                continue
            room = next(r for r in BANK.rooms[m["stratum"]] if r["room_id"] == m["room_id"])
            t = m["target_pos"]
            # per-source RIRs: one per interferer source, all from this room, none at the target position
            k = int(A[4][i][6:]) if A[4][i].startswith("babble") else 1
            assert len(m["src_pos"]) == k and t not in m["src_pos"]
            assert all(0 <= j < len(room["h"]) for j in m["src_pos"])
            rev_t = A[2][i].double() - A[1][i].double()
            snr = 10 * np.log10(float((rev_t ** 2).mean()) / float((A[1][i].double() ** 2).mean()))
            assert abs(snr - A[3][i]) < 1e-3  # full reverberant target vs summed interferers
            checked += 1
    assert checked > 5


def test_reference_is_direct_plus_early_and_sources_convolved_before_sum(monkeypatch):
    """Rebuild one reverberant example by direct convolution from the same draws."""
    pool, spk = _fake(t14.t13, monkeypatch)
    found = False
    for seed in range(40):
        rng, ra = np.random.default_rng(seed), np.random.default_rng([seed, 27])
        r_main = np.random.default_rng(seed)
        ra2 = np.random.default_rng([seed, 27])
        A = t14.make_batch(rng, pool, spk, batch=1, room="aug50", aug_rng=ra, bank=BANK)
        m = A[5][0]
        if m["cond"] != "rev_noisy" or not A[4][0].startswith("babble"):
            continue
        # replay the draws by hand
        sp = spk[r_main.integers(0, len(spk))]
        clean, pre = t14.crop_ctx(r_main, t14.t13.pool_get(pool, sp, int(r_main.integers(0, 2))))
        g = t14.t13.rms(clean) + 1e-9
        clean = (clean / g * 0.1).astype(np.float32); pre = (pre / g * 0.1).astype(np.float32)
        ra2.random(); r_main.random(); low = r_main.random() < 0.6
        snr = float(r_main.uniform(-5, 5)) if low else float(r_main.uniform(-5, 10))
        r_main.random(); others = [s for s in spk if s != sp]; k = int(r_main.integers(2, 13))
        stems, pres = t14.babble_stems(r_main, pool, others, k=k)
        room = next(r for r in BANK.rooms[m["stratum"]] if r["room_id"] == m["room_id"])
        early = _independent_render(clean, pre, room["he"][m["target_pos"]])
        rev_t = _independent_render(clean, pre, room["h"][m["target_pos"]])
        rev_n = sum(np.convolve(np.concatenate([p, s]), room["h"][j])[CTX:CTX + SEG]
                    for s, p, j in zip(stems, pres, m["src_pos"])) / k
        noise = rev_n / (t14.t13.rms(rev_n) + 1e-9) * t14.t13.rms(rev_t) * 10 ** (-snr / 20)
        assert np.allclose(A[0][0].numpy(), early, atol=1e-6)        # reference = direct + 50 ms
        assert np.allclose(A[1][0].numpy(), noise, atol=1e-6)        # per-source conv before summation
        assert np.allclose(A[2][0].numpy(), rev_t + noise, atol=1e-6)
        # history matters: rendering without the preceding samples differs at the window start
        no_hist = _independent_render(clean, np.zeros_like(pre), room["he"][m["target_pos"]])
        assert np.abs(no_hist[:200] - early[:200]).max() > 0 or np.abs(pre).max() == 0
        found = True
        break
    assert found


MAN = HERE / "rir_manifest.json"
_need_man = pytest.mark.skipif(not MAN.exists(), reason="manifest not built")


@_need_man
def test_manifest_room_split_disjoint_and_balanced():
    man = json.loads(MAN.read_text())
    by_split = {}
    for r in man["rooms"]:
        by_split.setdefault(r["split"], []).append(r)
    train = {r["room_id"] for r in by_split["train"]}
    evals = {r["room_id"] for s in ("eval_synth", "eval_measured") for r in by_split.get(s, [])}
    assert train and evals and not (train & evals)
    files = lambda rs: {f["file"] for r in rs for f in r["rirs"]}  # noqa: E731
    assert not (files(by_split["train"]) & files(by_split["eval_synth"] + by_split.get("eval_measured", [])))
    assert all(r["family"].startswith("simulated") for r in by_split["train"] + by_split["eval_synth"])
    assert all(not r["family"].startswith("simulated") for r in by_split.get("eval_measured", []))
    st = [r["stratum"] for r in by_split["train"]]
    assert st.count("short") == st.count("medium") == st.count("long") > 0
    es = [r["stratum"] for r in by_split["eval_synth"]]
    assert es.count("short") == es.count("medium") == es.count("long") == 2
    for r in by_split["train"] + by_split["eval_synth"]:
        assert 0.2 <= r["rt60_s"] <= 0.8 and len(r["rirs"]) >= 2


_DATA = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
_VAL = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
_need_data = pytest.mark.skipif(not (_DATA.exists() and _VAL.exists()), reason="LibriSpeech not present")


def _run(script, tmp, name, *extra):
    cmd = [sys.executable, str(script), "--loss", "sisdr", "--snr", "legacy", "--mode", "scratch",
           "--steps", "6", "--state-every", "3", "--diag-every", "2", "--device", "cpu",
           "--out", str(tmp / f"{name}.pt"), "--log", str(tmp / f"{name}.json"), *extra]
    return subprocess.run(cmd, capture_output=True, text=True)


@_need_data
def test_dry_run_weights_equal_train13(tmp_path):
    a = _run(HERE / "train14.py", tmp_path, "dry", "--room", "dry")
    assert a.returncode == 0, a.stderr[-2000:]
    b = _run(HERE.parent / "gen24" / "train13.py", tmp_path, "t13")
    assert b.returncode == 0, b.stderr[-2000:]
    sa = torch.load(tmp_path / "dry.pt", weights_only=False)
    sb = torch.load(tmp_path / "t13.pt", weights_only=False)["state_dict"]
    assert all(torch.equal(sa["state_dict"][k], sb[k]) for k in sb)
    assert sa["room_mode"] == "dry" and sa["rir_manifest_sha256"] is None
    la, lb = (json.loads((tmp_path / f"{n}.json").read_text()) for n in ("dry", "t13"))
    keep = ("step", "neg_sisdr_loss_db", "neg_sisdr_uncapped_db", "grad_norm", "lr", "grad_diag")
    strip = lambda log: [{k: r[k] for k in keep if k in r} for r in log]  # noqa: E731
    assert strip(la["log"]) == strip(lb["log"]) and la["val_log"] == lb["val_log"]


@_need_data
@_need_man
def test_aug50_resume_bit_identical_and_room_change_refused(tmp_path):
    a = _run(HERE / "train14.py", tmp_path, "a", "--room", "aug50")
    assert a.returncode == 0, a.stderr[-2000:]
    state = tmp_path / "a_state_latest.pt"
    b = _run(HERE / "train14.py", tmp_path, "b", "--room", "aug50", "--resume", str(state))
    assert b.returncode == 0, b.stderr[-2000:]
    sa = torch.load(tmp_path / "a.pt", weights_only=False)
    sb = torch.load(tmp_path / "b.pt", weights_only=False)
    assert all(torch.equal(sa["state_dict"][k], sb["state_dict"][k]) for k in sa["state_dict"])
    assert sa["room_mode"] == "aug50" and sa["rir_manifest_sha256"] == t14.rirbank.sha256_file(MAN)
    la, lb = (json.loads((tmp_path / f"{n}.json").read_text()) for n in "ab")
    assert la["room_counts"] == lb["room_counts"] and sum(la["room_counts"]["cond"].values()) == 48
    r = _run(HERE / "train14.py", tmp_path, "c", "--room", "dry", "--resume", str(state))
    assert r.returncode != 0 and "REFUSED resume" in (r.stdout + r.stderr) and "room" in (r.stdout + r.stderr)
