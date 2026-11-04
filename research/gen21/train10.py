"""Gen21: S48 vs R48 — budget/schedule policy at 48k lifetime (T0 only).

Pre-registered per Astra Gen20 review. Two modes, one frozen
recipe (Gen19: model, neg-SI-SDR loss, legacy k, SNR mix,
train-clean-100, batch 8x2 s, clip 5, ORIGINAL Gen19 batch
generator - no substreams - so scratch replays the parent data
stream under seed 20261117/18/19):
- scratch (S48): 48k from scratch, Adam 1e-3 cosine->1e-4 over
  48k. At step 24000 writes an RNG handoff + full training state.
- restart (R48): Gen19 parent + 24k, fresh Adam (250-step warmup
  3e-5->3e-4, cosine->3e-5), data RNG cloned from the S48
  handoff so lifetime batches 24k-48k are identical across arms.
VAL every 2000 with unrounded per-example records; acceptance on
48k finals only (see prereg.md for the decision rules).

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
NEVER a listener-benefit claim. Objective in-silico (T0) screen only.

Protocol is Gen13's verbatim (research/gen13/train2.py): same
LibriSpeech dev-clean subset under /tmp/gen12dl, same speaker split
(train 84 174 251 422 652 777 1272 1462 1673 1919; held-out targets
1988 1993; eval interferers 8842 8297), same mixture recipe (2 s crops
RMS 0.1, SNR -5..+10 dB, 10% quiet, noisy items 70% multi-talker babble
k~U{2,3,4} from train speakers only / 30% generated SSN, white noise
NEVER trained = held-out class), batch 8. The data functions below are
copied from gen13/train2.py so RNG consumption and mixtures match.

What changes (the Gen15 axis): architecture (model_causal.py, strictly
causal waveform TasNet instead of mel-envelope mask regression) and
objective (negative waveform SI-SDR vs delayed clean target; see
model_causal docstring for the DELAY=63-sample content delay).

Stated CPU budget: 2000 steps x batch 8 x 2 s on CPU (/tmp/gen9env,
torch 2.15.0). Adam lr 1e-3 cosine to 1e-4, grad-clip 5. One seed
(20261115) -- a screen, not a seed study. Checkpoints every 500 steps.

Run: /tmp/gen9env/bin/python research/gen21/train10.py --mode scratch --seed 20261117
then: ... --mode restart --seed 20261117 --init-from research/gen19/weights/causal_seed20261117.pt
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np, soundfile as sf, torch, torch.nn.functional as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
from model_causal import (CausalTasNetEnh, audit_causality, delay_target,  # noqa: E402
                          receptive_field, suffix_invariance_test)

DATA_ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
FS = 16000
TRAIN_SPK = ["84", "174", "251", "422", "652", "777", "1272", "1462", "1673", "1919",
             "2035", "2078", "2086", "2277", "2412", "2428", "2803", "2902", "3000",
             "3081", "3170", "3536", "3576", "3752", "3853", "5338"]  # bench-v2 prereg
TEST_SPK = ["1988", "1993", "5895", "6241", "6295", "6313"]
TEST_BABBLE_SPK = ["8297", "8842", "6319", "6345", "7850", "7976"]
VAL_SPK = ["5536", "5694"]
SEG = 2 * FS


_FILE_CACHE: dict = {}


def _read_cached(path):
    if path not in _FILE_CACHE:
        if len(_FILE_CACHE) >= 256:
            _FILE_CACHE.clear()
        x, sr = sf.read(path, dtype="float32", always_2d=False)
        assert sr == FS, (path, sr)
        if x.ndim > 1:
            x = x[:, 0]
        _FILE_CACHE[path] = np.ascontiguousarray(x)
    return _FILE_CACHE[path]


def load_pool(speakers, root=None):
    """On-demand pool: speaker -> list of FLAC paths (decoded lazily
    by crop_from_pool). Crop/babble helpers take path-lists via the
    pool_get shim below so mixture code is unchanged in structure."""
    root = Path(root) if root else DATA_ROOT
    pool = {}
    for spk in speakers:
        files = sorted((root / spk).rglob("*.flac"))
        if not files:
            raise FileNotFoundError(f"no FLAC for speaker {spk} under {root}")
        pool[spk] = files
    return pool


def pool_get(pool, spk, idx):
    return _read_cached(pool[spk][idx])


def crop(rng, arr, n=SEG):
    if len(arr) <= n:
        out = np.zeros(n, dtype=np.float32); out[:len(arr)] = arr; return out
    s = rng.integers(0, len(arr) - n + 1); return arr[s:s + n].copy()


def rms(x):
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2) + 1e-12))


def make_ssn_fast(rng, n=SEG):
    # Identical generator to Gen12/Gen13 (generated SSN proxy).
    from scipy.signal import lfilter
    w = rng.standard_normal(n)
    y = lfilter([0.15], [1, -0.85], w); y = lfilter([1.0], [1, -0.4], y)
    return y.astype(np.float32)


def babble(rng, pool, speakers, k=3, n=SEG):
    out = np.zeros(n, dtype=np.float64)
    for _ in range(k):
        spk = speakers[rng.integers(0, len(speakers))]
        arr = pool_get(pool, spk, int(rng.integers(0, len(pool[spk]))))
        c = crop(rng, arr, n).astype(np.float64); out += c / (rms(c) + 1e-9)
    return (out / k).astype(np.float32)


def make_batch(rng, pool, speakers, batch=8, quiet_p=0.10):
    cleans, noises, mixs, snrs, kinds = [], [], [], [], []
    for _ in range(batch):
        spk = speakers[rng.integers(0, len(speakers))]
        clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))))
        clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
        if rng.random() < quiet_p:
            noise = np.zeros_like(clean); snr = 999.0; kind = "quiet"
        else:
            snr = float(rng.uniform(-5, 5)) if rng.random() < 0.6 else float(rng.uniform(-5, 10))
            if rng.random() < 0.70:
                others = [s for s in speakers if s != spk]
                k = int(rng.integers(2, 13))
                noise = babble(rng, pool, others, k=k); kind = f"babble{k}"
            else:
                noise = make_ssn_fast(rng); kind = "ssn"
            noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
        cleans.append(clean); noises.append(noise); mixs.append(clean + noise)
        snrs.append(snr); kinds.append(kind)
    to = lambda a: torch.from_numpy(np.stack(a))  # noqa: E731
    return to(cleans), to(noises), to(mixs), snrs, kinds


def neg_si_sdr(ref, est, eps=1e-8):
    """Negative SI-SDR (dB), mean over batch. ref/est: (B,T)."""
    ref = ref - ref.mean(dim=-1, keepdim=True)
    est = est - est.mean(dim=-1, keepdim=True)
    alpha = (est * ref).sum(-1, keepdim=True) / ((ref * ref).sum(-1, keepdim=True) + eps)
    proj = alpha * ref
    noise = est - proj
    ratio = (proj * proj).sum(-1) / ((noise * noise).sum(-1) + eps)
    return -10.0 * torch.log10(ratio + eps)


VAL_ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
VAL_INTERFERERS = ["2035", "2078", "2086", "2277", "2412", "2428"]


def build_val_panel():
    """Fixed VAL mixtures (Astra step 1): targets 5536/5694, crowd
    k8-12 from 6 dev-clean interferers, 4 crops/target/SNR + quiet."""
    pool = load_pool(VAL_SPK + VAL_INTERFERERS, root=VAL_ROOT)
    rng = np.random.default_rng(777123)
    SEG4 = 4 * FS
    panel = []
    for spk in VAL_SPK:
        for snr in [-5.0, 0.0, 5.0, 10.0]:
            for _ in range(4):
                clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), SEG4)
                clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
                noise = babble(rng, pool, VAL_INTERFERERS, k=int(rng.integers(8, 13)), n=SEG4)
                noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                panel.append({"snr": snr, "spk": spk, "clean": clean, "mix": (clean + noise).astype(np.float32)})
        for _ in range(4):
            clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), SEG4)
            clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
            panel.append({"snr": 999.0, "spk": spk, "clean": clean, "mix": clean.copy()})
    return panel


def _si_sdr_np(ref, est):
    ref = ref.astype(np.float64) - ref.mean(); est = est.astype(np.float64) - est.mean()
    a = np.dot(est, ref) / (np.dot(ref, ref) + 1e-12)
    p = a * ref
    return float(10 * np.log10((np.dot(p, p) + 1e-12) / (np.dot(est - p, est - p) + 1e-12)))


def eval_val(model, panel, device):
    """Returns (rounded summary, unrounded per-example records)."""
    from pystoi import stoi
    from model_causal import undelay
    was_training = model.training
    model.eval()
    agg = {}
    items = []
    with torch.no_grad():
        for i, item in enumerate(panel):
            est = undelay(model(torch.from_numpy(item["mix"][None]).to(device))[0].cpu().numpy())
            tr = slice(256, -256)
            d = _si_sdr_np(item["clean"][tr], est[tr]) - _si_sdr_np(item["clean"][tr], item["mix"][tr])
            ds = float(stoi(item["clean"][tr].astype(np.float64), est[tr].astype(np.float64), FS) -
                       stoi(item["clean"][tr].astype(np.float64), item["mix"][tr].astype(np.float64), FS))
            agg.setdefault(item["snr"], []).append((d, ds))
            items.append({"idx": i, "spk": item.get("spk"), "snr": item["snr"],
                          "d_sisdr": float(d), "d_stoi": float(ds)})
    if was_training:
        model.train()
    summary = {str(k): {"d_sisdr": round(float(np.mean([v[0] for v in vs])), 2),
                        "d_stoi": round(float(np.mean([v[1] for v in vs])), 3)}
               for k, vs in sorted(agg.items())}
    return summary, items


def save_ckpt(model, out, steps, seed, speakers=None, mode="scratch",
              init_from=None, parent_sha256=None):
    torch.save({"state_dict": model.state_dict(), "steps": steps, "seed": seed,
                "mode": mode, "init_from": init_from, "parent_sha256": parent_sha256,
                "train_speakers": speakers or TRAIN_SPK,
                "data": "LibriSpeech train-clean-100 OpenSLR12 CC-BY-4.0 (archive sha256 d4ddd1d5...bf6e2)",
                "gen": "gen21", "arch": "causal Conv-TasNet-style (gen15/model_causal.py)",
                "loss": "negative waveform SI-SDR vs DELAY-shifted clean (Gen15 recipe)",
                "babble_k": "uniform {2..12}", "snr_mix": "60% U(-5,5) + 40% U(-5,10)",
                "noise_mix": "70% babble / 30% SSN, 10% quiet"}, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def save_state(model, opt, sched, rng, out, step, seed, mode):
    """Full resumable training state (optimizer/scheduler/RNG included)."""
    torch.save({"state_dict": model.state_dict(), "opt": opt.state_dict(),
                "sched": sched.state_dict(), "np_rng_state": rng.bit_generator.state,
                "torch_rng_state": torch.get_rng_state(), "step": step,
                "seed": seed, "mode": mode, "gen": "gen21"}, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def rng_from_state(state, seed=0):
    rng = np.random.default_rng(seed)
    rng.bit_generator.state = state
    return rng


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["scratch", "restart"], required=True)
    ap.add_argument("--steps", type=int, default=None,
                    help="default: scratch 48000, restart 24000")
    ap.add_argument("--seed", type=int, default=20261117)
    ap.add_argument("--init-from", default=None, help="restart: Gen19 parent checkpoint")
    ap.add_argument("--rng-handoff", default=None,
                    help="restart: S48 step-24000 RNG state file (default: weights/rng_handoff_seed<seed>.pt)")
    ap.add_argument("--device", default="mps" if torch.backends.mps.is_available() else "cpu")
    ap.add_argument("--data-root", default="/tmp/gen17dl/LibriSpeech/train-clean-100")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    if a.steps is None:
        a.steps = 48000 if a.mode == "scratch" else 24000
    tag = "s48" if a.mode == "scratch" else "r48"
    out = Path(a.out) if a.out else HERE / "weights" / f"{tag}_seed{a.seed}.pt"
    logp = Path(a.log) if a.log else HERE / "weights" / f"train_log_{tag}_seed{a.seed}.json"
    if out.exists() and not a.force:
        raise SystemExit(f"REFUSED: {out} exists (pass --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    parent_sha = None
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK + VAL_SPK)), "speaker holdout violated"
    print(f"device={a.device} mode={a.mode} steps={a.steps} seed={a.seed}", flush=True)
    model = CausalTasNetEnh()
    if a.mode == "restart":
        assert a.init_from, "restart requires --init-from"
        _ck = torch.load(a.init_from, map_location="cpu", weights_only=False)
        model.load_state_dict(_ck["state_dict"] if "state_dict" in _ck else _ck)
        parent_sha = hashlib.sha256(Path(a.init_from).read_bytes()).hexdigest()
        _hf = Path(a.rng_handoff) if a.rng_handoff else HERE / "weights" / f"rng_handoff_seed{a.seed}.pt"
        _h = torch.load(_hf, map_location="cpu", weights_only=False)
        assert _h["seed"] == a.seed and _h["step"] == 24000, f"bad handoff {_hf}: {_h.get('seed')}/{_h.get('step')}"
        rng = rng_from_state(_h["np_rng_state"], seed=a.seed)
        print(f"restart parent={a.init_from} parent_sha256={parent_sha} handoff={_hf}", flush=True)
    bad = audit_causality(model)
    assert not bad, bad
    caus = suffix_invariance_test(model)
    for r in caus:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated: {r}"
    print(f"params={model.count_parameters()} rf={receptive_field()}", flush=True)
    print(f"causality pre-train: {caus}", flush=True)
    model = model.to(a.device)
    print(f"loading pool from {DATA_ROOT}", flush=True); tload = time.time()
    root = Path(a.data_root)
    train_spk = sorted(d.name for d in root.iterdir() if d.is_dir())
    assert train_spk, f"no speaker dirs under {root}"
    assert not (set(train_spk) & set(TEST_SPK + TEST_BABBLE_SPK + VAL_SPK)), "holdout leak in data root"
    print(f"data_root={root} speakers={len(train_spk)}", flush=True)
    pool = load_pool(train_spk, root=root)
    counts = {k: len(v) for k, v in pool.items()}
    total_s = float(sum(counts.values()))  # file count; audio decoded on demand
    print(f"pool n_speakers={len(counts)} n_files={int(total_s)} index_s={time.time()-tload:.1f}", flush=True)
    life0 = 0 if a.mode == "scratch" else 24000  # lifetime updates already done
    if a.mode == "scratch":
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.steps, eta_min=1e-4)
    else:
        opt = torch.optim.Adam(model.parameters(), lr=3e-5)

        def _lr_lambda(step):
            import math
            if step < 250:
                return 1.0 + 9.0 * step / 250.0
            t = (step - 250) / max(1, a.steps - 250)
            return 1.0 + 4.5 * (1.0 + math.cos(math.pi * t))

        sched = torch.optim.lr_scheduler.LambdaLR(opt, _lr_lambda)
    val_panel = build_val_panel()
    _v0, _items0 = eval_val(model, val_panel, a.device)
    val_log = [{"step": 0, "lifetime_step": life0, "val": _v0, "items": _items0}]
    print(f"VAL step0 {_v0}", flush=True)
    log = []; t0 = time.time()
    for step in range(a.steps):
        clean, noise, mix, snrs, kinds = make_batch(rng, pool, train_spk, batch=8)
        clean, mix = clean.to(a.device), mix.to(a.device)
        est = model(mix)
        losses = neg_si_sdr(delay_target(clean), est)
        loss = losses.mean()
        opt.zero_grad(); loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step(); sched.step()
        if step % 25 == 0 or step == a.steps - 1:
            rec = {"step": step, "neg_sisdr_loss_db": float(loss),
                   "grad_norm": float(gn), "lr": float(opt.param_groups[0]["lr"]),
                   "elapsed_s": round(time.time() - t0, 1)}
            log.append(rec); print(rec, flush=True)
        if (step + 1) % 2000 == 0 and step + 1 < a.steps:
            ck = out.with_name(f"{out.stem}_step{life0 + step + 1}.pt")
            save_ckpt(model, ck, life0 + step + 1, a.seed, train_spk, a.mode, a.init_from, parent_sha)
            print(f"interim ckpt {ck}", flush=True)
        if life0 + step + 1 in (24000, 36000, 48000):
            st = out.with_name(f"{out.stem}_state_step{life0 + step + 1}.pt")
            _sha = save_state(model, opt, sched, rng, st, life0 + step + 1, a.seed, a.mode)
            print(f"full state {st} sha256={_sha}", flush=True)
            if a.mode == "scratch" and step + 1 == 24000:
                _hf = HERE / "weights" / f"rng_handoff_seed{a.seed}.pt"
                torch.save({"np_rng_state": rng.bit_generator.state,
                            "torch_rng_state": torch.get_rng_state(),
                            "seed": a.seed, "step": 24000, "gen": "gen21"}, _hf)
                print(f"RNG HANDOFF -> {_hf}", flush=True)
        if (step + 1) % 2000 == 0:
            v, vitems = eval_val(model, val_panel, a.device)
            val_log.append({"step": step + 1, "lifetime_step": life0 + step + 1,
                            "val": v, "items": vitems})
            print(f"VAL step{step+1} {v}", flush=True)
    wall = time.time() - t0
    model = model.to("cpu").eval()
    caus_post = suffix_invariance_test(model, seed=1)
    for r in caus_post:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated post-train: {r}"
    sha = save_ckpt(model, out, life0 + a.steps, a.seed, train_spk, a.mode, a.init_from, parent_sha)
    meta = {"steps": a.steps, "lifetime_steps": life0 + a.steps, "mode": a.mode,
            "init_from": a.init_from, "parent_sha256": parent_sha,
            "wall_s": round(wall, 1), "batch": 8, "seg_s": 2.0,
            "seed": a.seed, "weights": str(out), "weights_sha256": sha,
            "params": model.count_parameters(), "pool_files": counts,
            "pool_n_files": int(total_s), "receptive_field": receptive_field(),
            "causality_pre": caus, "causality_post": caus_post,
            "loss_first5_logged_mean": float(np.mean([r["neg_sisdr_loss_db"] for r in log[:5]])),
            "loss_last5_logged_mean": float(np.mean([r["neg_sisdr_loss_db"] for r in log[-5:]])),
            "log": log, "val_log": val_log}
    logp.write_text(json.dumps(meta, indent=1))
    print(f"DONE wall={wall:.0f}s weights={out} sha256={sha}", flush=True)


if __name__ == "__main__":
    main()
