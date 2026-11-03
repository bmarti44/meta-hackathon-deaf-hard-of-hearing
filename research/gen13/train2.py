"""Gen13: Retrain J4-A1 (gen11 architecture UNCHANGED) with babble IN training.

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
NEVER a listener-benefit claim. Objective in-silico (T0) re-screen only.

Why (Gen12 next-step gate, research/gen12/Gen12-summary.md): Gen12's 750-step
single-seed screen found a gain only on trained SSN, a null on unseen-talker
babble, and failure on held-out white noise. Gen13 re-screens at >=3000 steps
with 3 seeds and bootstrap CIs (eval2.py), architecture and IRM target
identical to Gen12 so the comparison isolates training budget/seeds.

Holdout design (whole noise class + speakers held out):
  * Target speakers: train 84 174 251 422 652 777 1272 1462 1673 1919;
    held-out eval targets 1988 1993 (never in any training pool).
  * Babble interferers in training: multi-talker mixtures (k ~ U{2,3,4}
    talkers) drawn ONLY from train speakers (target speaker excluded per
    item). Eval babble uses interferer-only speakers 8842 8297 -- babble is
    a SEEN class with HELD-OUT speakers (same split as Gen12).
  * White noise: NEVER in training -- held-out noise CLASS (eval only).
  * SSN (generated, 1-pole tilted white noise; not a recording): trained
    class, identical generator to Gen12.

Mixtures (on-the-fly, seeded): 2 s target crops RMS-normalised to 0.1 +
interferer at SNR -5..+10 dB. 10% quiet (IRM=1, quiet-identity term);
of noisy items 70% babble / 30% SSN (Gen12 proportions retained; the one
deliberate change vs Gen12 is k in {2,3,4} instead of fixed k=3, a broader
babble pool -- recorded here so the comparison is not overstated).
Target: mel-envelope IRM sqrt(Eclean/(Eclean+Enoise+eps)), loss mask-MSE,
Adam 2e-3 cosine to 2e-4, grad-clip 5, batch 8 x 2.0 s (all as Gen12).

Data: LibriSpeech dev-clean (OpenSLR 12), CC BY 4.0,
  https://www.openslr.org/resources/12/dev-clean.tar.gz
  archive SHA-256 (Gen12 download) 76f87d09...728ab3 (see gen12/results.md).
Subset under /tmp/gen12dl (not committed); this script refuses to run if it
is absent rather than silently substituting other data.

Run (3 seeds, as filed for Gen13):
  /tmp/gen9env/bin/python research/gen13/train2.py --seed 20261103 --steps 3000
  /tmp/gen9env/bin/python research/gen13/train2.py --seed 20261104 --steps 3000
  /tmp/gen9env/bin/python research/gen13/train2.py --seed 20261105 --steps 3000
"""
from __future__ import annotations
import argparse, hashlib, json, sys, time
from pathlib import Path
import numpy as np, soundfile as sf, torch, torch.nn.functional as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen11"))
from j4_model import EPS, FS, J4A1  # noqa: E402

DATA_ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
TRAIN_SPK = ["84", "174", "251", "422", "652", "777", "1272", "1462", "1673", "1919"]
TEST_SPK = ["1988", "1993"]
TEST_BABBLE_SPK = ["8842", "8297"]
SEG = 2 * FS


def load_pool(speakers):
    pool = {}
    for spk in speakers:
        files = sorted((DATA_ROOT / spk).rglob("*.flac"))
        if not files:
            raise FileNotFoundError(f"no FLAC for speaker {spk} under {DATA_ROOT}; "
                                    "re-download per docstring / gen12/results.md")
        arrs = []
        for f in files:
            x, sr = sf.read(f, dtype="float32", always_2d=False)
            assert sr == FS, (f, sr)
            if x.ndim > 1:
                x = x[:, 0]
            if len(x) >= FS:
                arrs.append(np.ascontiguousarray(x))
        pool[spk] = arrs
    return pool


def crop(rng, arr, n=SEG):
    if len(arr) <= n:
        out = np.zeros(n, dtype=np.float32); out[:len(arr)] = arr; return out
    s = rng.integers(0, len(arr) - n + 1); return arr[s:s + n].copy()


def rms(x):
    return float(np.sqrt(np.mean(x.astype(np.float64) ** 2) + 1e-12))


def make_ssn_fast(rng, n=SEG):
    # Identical generator to Gen12 (generated SSN proxy, not a recording).
    from scipy.signal import lfilter
    w = rng.standard_normal(n)
    y = lfilter([0.15], [1, -0.85], w); y = lfilter([1.0], [1, -0.4], y)
    return y.astype(np.float32)


def babble(rng, pool, speakers, k=3, n=SEG):
    out = np.zeros(n, dtype=np.float64)
    for _ in range(k):
        spk = speakers[rng.integers(0, len(speakers))]
        arr = pool[spk][rng.integers(0, len(pool[spk]))]
        c = crop(rng, arr, n).astype(np.float64); out += c / (rms(c) + 1e-9)
    return (out / k).astype(np.float32)


def make_batch(rng, pool, speakers, batch=8, quiet_p=0.10):
    cleans, noises, mixs, snrs, kinds = [], [], [], [], []
    for _ in range(batch):
        spk = speakers[rng.integers(0, len(speakers))]
        clean = crop(rng, pool[spk][rng.integers(0, len(pool[spk]))])
        clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
        if rng.random() < quiet_p:
            noise = np.zeros_like(clean); snr = 999.0; kind = "quiet"
        else:
            snr = float(rng.uniform(-5, 10))
            if rng.random() < 0.70:
                others = [s for s in speakers if s != spk]
                k = int(rng.integers(2, 5))  # multi-talker: 2, 3 or 4 talkers
                noise = babble(rng, pool, others, k=k); kind = f"babble{k}"
            else:
                noise = make_ssn_fast(rng); kind = "ssn"
            noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
        cleans.append(clean); noises.append(noise); mixs.append(clean + noise)
        snrs.append(snr); kinds.append(kind)
    to = lambda a: torch.from_numpy(np.stack(a))  # noqa: E731
    return to(cleans), to(noises), to(mixs), snrs, kinds


def irm_target(model, clean, noise):
    with torch.no_grad():
        _, ec = model.extract_features(clean); _, en = model.extract_features(noise)
        return torch.sqrt((ec ** 2) / (ec ** 2 + en ** 2 + EPS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=20261103)
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    out = Path(a.out) if a.out else HERE / "weights" / f"j4_seed{a.seed}.pt"
    logp = Path(a.log) if a.log else HERE / "weights" / f"train_log_seed{a.seed}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    print(f"loading pool from {DATA_ROOT}", flush=True); tload = time.time()
    pool = load_pool(TRAIN_SPK)
    counts = {k: len(v) for k, v in pool.items()}
    total_s = sum(len(x) for v in pool.values() for x in v) / FS
    print(f"pool files={counts} total_s={total_s:.0f} load_s={time.time()-tload:.1f}", flush=True)
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK)), "speaker holdout violated"
    model = J4A1()
    assert model.count_parameters() == 238656, model.count_parameters()  # gen11 arch unchanged
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.steps, eta_min=2e-4)
    log = []; t0 = time.time()
    for step in range(a.steps):
        clean, noise, mix, snrs, kinds = make_batch(rng, pool, TRAIN_SPK, batch=8)
        irm = irm_target(model, clean, noise)
        masks, _ = model(mix); loss = F.mse_loss(masks, irm)
        opt.zero_grad(); loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step(); sched.step()
        if step % 25 == 0 or step == a.steps - 1:
            rec = {"step": step, "loss": float(loss), "grad_norm": float(gn),
                   "lr": float(opt.param_groups[0]["lr"]), "elapsed_s": round(time.time() - t0, 1)}
            log.append(rec); print(rec, flush=True)
    wall = time.time() - t0
    torch.save({"state_dict": model.state_dict(), "steps": a.steps, "seed": a.seed,
                "train_speakers": TRAIN_SPK,
                "data": "LibriSpeech dev-clean subset OpenSLR12 CC-BY-4.0",
                "gen": "gen13", "arch": "gen11 J4A1 unchanged",
                "babble_k": "uniform {2,3,4}", "noise_mix": "70% babble / 30% SSN, 10% quiet"}, out)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    meta = {"steps": a.steps, "wall_s": round(wall, 1), "batch": 8, "seg_s": 2.0,
            "seed": a.seed, "weights": str(out), "weights_sha256": sha,
            "params": model.count_parameters(), "pool_files": counts,
            "pool_total_s": round(total_s, 1),
            "loss_first5_logged_mean": float(np.mean([r["loss"] for r in log[:5]])),
            "loss_last5_logged_mean": float(np.mean([r["loss"] for r in log[-5:]])),
            "log": log}
    logp.write_text(json.dumps(meta, indent=1))
    print(f"DONE wall={wall:.0f}s weights={out} sha256={sha}", flush=True)


if __name__ == "__main__":
    main()
