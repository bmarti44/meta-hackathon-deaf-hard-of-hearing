"""Gen19: Gen18 recipe at 24,000 steps + fixed VAL panel (T0 only).

Pre-registered per Astra training-strategy review step 1:
from scratch, train-clean-100, architecture/loss/mixtures frozen,
Adam 1e-3 cosine->1e-4 stretched over 24k steps, batch 8x2 s,
clip 5, final-checkpoint rule. VAL panel (targets 5536/5694,
dev-clean interferers, crowd k8-12) every 2000 steps diagnoses
convergence; inspect 6k/12k/18k/24k. Seeds replicate before
any KPI claim.

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

Run: /tmp/gen9env/bin/python research/gen19/train8.py --steps 24000
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
                panel.append({"snr": snr, "clean": clean, "mix": (clean + noise).astype(np.float32)})
        for _ in range(4):
            clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), SEG4)
            clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
            panel.append({"snr": 999.0, "clean": clean, "mix": clean.copy()})
    return panel


def _si_sdr_np(ref, est):
    ref = ref.astype(np.float64) - ref.mean(); est = est.astype(np.float64) - est.mean()
    a = np.dot(est, ref) / (np.dot(ref, ref) + 1e-12)
    p = a * ref
    return float(10 * np.log10((np.dot(p, p) + 1e-12) / (np.dot(est - p, est - p) + 1e-12)))


def eval_val(model, panel, device):
    from pystoi import stoi
    from model_causal import undelay
    was_training = model.training
    model.eval()
    agg = {}
    with torch.no_grad():
        for item in panel:
            est = undelay(model(torch.from_numpy(item["mix"][None]).to(device))[0].cpu().numpy())
            tr = slice(256, -256)
            d = _si_sdr_np(item["clean"][tr], est[tr]) - _si_sdr_np(item["clean"][tr], item["mix"][tr])
            ds = float(stoi(item["clean"][tr].astype(np.float64), est[tr].astype(np.float64), FS) -
                       stoi(item["clean"][tr].astype(np.float64), item["mix"][tr].astype(np.float64), FS))
            agg.setdefault(item["snr"], []).append((d, ds))
    if was_training:
        model.train()
    return {str(k): {"d_sisdr": round(float(np.mean([v[0] for v in vs])), 2),
                     "d_stoi": round(float(np.mean([v[1] for v in vs])), 3)}
            for k, vs in sorted(agg.items())}


def save_ckpt(model, out, steps, seed, speakers=None):
    torch.save({"state_dict": model.state_dict(), "steps": steps, "seed": seed,
                "train_speakers": speakers or TRAIN_SPK,
                "data": "LibriSpeech train-clean-100 OpenSLR12 CC-BY-4.0 (archive sha256 d4ddd1d5...bf6e2)",
                "gen": "gen19", "arch": "causal Conv-TasNet-style (gen15/model_causal.py)",
                "loss": "negative waveform SI-SDR vs DELAY-shifted clean (Gen15 recipe)",
                "babble_k": "uniform {2..12}", "snr_mix": "60% U(-5,5) + 40% U(-5,10)",
                "noise_mix": "70% babble / 30% SSN, 10% quiet"}, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=24000)
    ap.add_argument("--seed", type=int, default=20261117)
    ap.add_argument("--device", default="mps" if torch.backends.mps.is_available() else "cpu")
    ap.add_argument("--data-root", default="/tmp/gen17dl/LibriSpeech/train-clean-100")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    out = Path(a.out) if a.out else HERE / "weights" / f"causal_seed{a.seed}.pt"
    logp = Path(a.log) if a.log else HERE / "weights" / f"train_log_seed{a.seed}.json"
    if out.exists() and not a.force:
        raise SystemExit(f"REFUSED: {out} exists (pass --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK + VAL_SPK)), "speaker holdout violated"
    print(f"device={a.device}", flush=True)
    model = CausalTasNetEnh()
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
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.steps, eta_min=1e-4)
    val_panel = build_val_panel()
    val_log = [{"step": 0, "val": eval_val(model, val_panel, a.device)}]
    print(f"VAL step0 {val_log[0]['val']}", flush=True)
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
        if (step + 1) % 500 == 0 and step + 1 < a.steps:
            ck = out.with_name(f"{out.stem}_step{step+1}.pt")
            save_ckpt(model, ck, step + 1, a.seed, train_spk)
            print(f"interim ckpt {ck}", flush=True)
        if (step + 1) % 2000 == 0:
            v = eval_val(model, val_panel, a.device)
            val_log.append({"step": step + 1, "val": v})
            print(f"VAL step{step+1} {v}", flush=True)
    wall = time.time() - t0
    model = model.to("cpu").eval()
    caus_post = suffix_invariance_test(model, seed=1)
    for r in caus_post:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated post-train: {r}"
    sha = save_ckpt(model, out, a.steps, a.seed, train_spk)
    meta = {"steps": a.steps, "wall_s": round(wall, 1), "batch": 8, "seg_s": 2.0,
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
