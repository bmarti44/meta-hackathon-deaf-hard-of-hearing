"""Gen14: training REDESIGN screen for J4-A1 (architecture EXACTLY unchanged).

Requested: Sol 6.1. Actual: muse-wonder-full-1.0. Date: 2026-11-03.
T0 in-silico screen only. NEVER a listener-benefit claim.

Why: Gen13 (3000 steps x 3 seeds, same recipe) gave a seed-stable babble null
(dSI-SDR -0.12 dB [-0.34,+0.12], identical point estimate to Gen12's 750-step
run). Same-recipe more-steps is a closed lever. Gen14 changes levers:

  (a) LOSS   : mask-MSE + envelope SI-SDR-style loss. The envelope term is
               -SI-SDR (dB) between the masked mel envelope (applied mask x
               mixture envelope) and the clean mel envelope, flattened per
               item over (frames x bands), scaled by ENV_W/20 so its
               magnitude is comparable to mask-MSE (checked at smoke).
  (b) POOL   : babble k ~ U{2..8} talkers (Gen13: U{2,3,4}) + SNR curriculum
               widening to -5..+15 dB over training: progress<1/3 U[0,15],
               <2/3 U[-2.5,15], else U[-5,15] (Gen13: U[-5,10] fixed).
               Retained: 10% quiet, noisy items 70% babble / 30% SSN,
               interferers only from train speakers, target excluded.
  (c) TARGET : cIRM-style COMPRESSED magnitude mask IRM**0.5 vs plain IRM.
               A true complex IRM is impossible here (envelope-only sigmoid
               output, no phase) -- this is the compressed-magnitude part
               only. Trained compressed => DECOMPRESSED at inference
               (applied mask = predicted**2), including inside the envelope
               loss and in all eval paths for cIRM configs.
  (d) LR     : Adam 2e-3 cosine to 2e-5 final (Gen13: 2e-4). Bundled with (b)
               in every non-control config; NOT isolated (declared limit).

Screen design (ONE screen, 4 configs x 1 seed, then best-2 x 2nd seed):
  C0 control      : Gen13 recipe (IRM, mask-MSE, k2-4, SNR-5..10, LR->2e-4)
  C1 a+b+d / IRM  : new loss + new pool + new LR, plain IRM
  C2 a+b+d / cIRM : as C1 but compressed target   (C2 vs C1 isolates (c))
  C3 b+d / IRM    : new pool + new LR, mask-MSE only (C1 vs C3 isolates (a);
                                                    C3 vs C0 tests (b)+(d))
Steps: 700/config (Gen12's 750-step screen point already showed the same
babble null as Gen13's 3000, so ~700 is the comparable screen scale; a null
here closes this recipe family AT SCREEN SCALE -- see results.md caveat).
Selection (pre-registered): rank configs by mean babble dSI-SDR on the exact
Gen13 eval2 babble crops (quick eval, IRM-independent waveform readout);
guardrail: SSN dSI-SDR must stay > 0. Top-2 get seed 2.
Gate (final, full Gen13 eval2 protocol, babble primary): per config,
seed-mean babble dSI-SDR bootstrap 95% CI excluding 0 (positive) = signal;
else this recipe family is closed.
Budget: 6 train runs x 700 steps x ~0.37 s/step ~= 26 sequential CPU-min
(single-process Gen13 rate) + eval; run in parallel (4-6 procs) for wall time.

Architecture: gen11/j4_model.py imported unchanged; 238,656 params asserted.
Causality is by construction there (right-aligned frames, unidirectional
LSTM, per-frame norm); cIRM decompression is pointwise per frame.
Data/holdout: identical to Gen13 train2.py (imported, asserted).

Run:
  /tmp/gen9env/bin/python research/gen14/train3.py screen          # 4 cfgs, seed1, parallel
  /tmp/gen9env/bin/python research/gen14/train3.py quickeval --weights research/gen14/weights/C*_seed*.pt
  /tmp/gen9env/bin/python research/gen14/train3.py train --config C1 --seed 20261114 --steps 700
  /tmp/gen9env/bin/python research/gen14/train3.py fulleval        # best-2 x 2 seeds, parallel, + combine
"""
from __future__ import annotations
import argparse, glob, hashlib, json, os, subprocess, sys, time
from pathlib import Path
import numpy as np, torch, torch.nn.functional as F

HERE = Path(__file__).resolve().parent
GEN13 = HERE.parent / "gen13"
sys.path.insert(0, str(HERE.parent / "gen11")); sys.path.insert(0, str(GEN13))
from j4_model import EPS, FS, J4A1  # noqa: E402
from train2 import TRAIN_SPK, TEST_BABBLE_SPK, TEST_SPK, babble, crop, load_pool, make_ssn_fast, rms  # noqa: E402

SEG = 2 * FS
ENV_W = 0.2          # envelope-loss weight: loss += ENV_W * (-envSI-SDR_dB)/20 = 0.01*(-dB)
                     # (smoke at init: envSI-SDR ~+12 dB, mask-MSE ~0.15 -> terms comparable)
BETA = 0.5           # cIRM-style compression exponent (target = IRM**BETA)
SEED1, SEED2 = 20261113, 20261114

CONFIGS = {
    "C0": dict(env_loss=False, new_pool=False, cirm=False, lr_min=2e-4),
    "C1": dict(env_loss=True,  new_pool=True,  cirm=False, lr_min=2e-5),
    "C2": dict(env_loss=True,  new_pool=True,  cirm=True,  lr_min=2e-5),
    "C3": dict(env_loss=False, new_pool=True,  cirm=False, lr_min=2e-5),
}


# --------------------------------------------------------------------------
# Batch construction (Gen13 make_batch with lever (b) switches + curriculum)
# --------------------------------------------------------------------------
def snr_draw(rng, cfg, progress):
    if not cfg["new_pool"]:
        return float(rng.uniform(-5, 10))
    lo = 0.0 if progress < 1 / 3 else (-2.5 if progress < 2 / 3 else -5.0)
    return float(rng.uniform(lo, 15.0))


def make_batch(rng, pool, cfg, progress, batch=8, quiet_p=0.10):
    cleans, noises, mixs, kinds = [], [], [], []
    for _ in range(batch):
        spk = TRAIN_SPK[rng.integers(0, len(TRAIN_SPK))]
        clean = crop(rng, pool[spk][rng.integers(0, len(pool[spk]))])
        clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
        if rng.random() < quiet_p:
            noise = np.zeros_like(clean); kind = "quiet"
        else:
            snr = snr_draw(rng, cfg, progress)
            if rng.random() < 0.70:
                others = [s for s in TRAIN_SPK if s != spk]
                k = int(rng.integers(2, 9)) if cfg["new_pool"] else int(rng.integers(2, 5))
                noise = babble(rng, pool, others, k=k); kind = f"babble{k}"
            else:
                noise = make_ssn_fast(rng); kind = "ssn"
            noise = (noise / (rms(noise) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
        cleans.append(clean); noises.append(noise); mixs.append(clean + noise); kinds.append(kind)
    to = lambda a: torch.from_numpy(np.stack(a))  # noqa: E731
    return to(cleans), to(noises), to(mixs), kinds


def env_sisdr_db(est, ref):
    """Per-item scale-invariant SDR (dB) between envelopes, (B,T,Bands)->(B,)."""
    e = est.flatten(1).double(); r = ref.flatten(1).double()
    alpha = (e * r).sum(1, keepdim=True) / ((r * r).sum(1, keepdim=True) + 1e-12)
    proj = alpha * r
    return 10 * torch.log10(((proj * proj).sum(1) + 1e-12) / (((e - proj) ** 2).sum(1) + 1e-12))


def applied_mask(pred, cfg):
    return pred ** (1.0 / BETA) if cfg["cirm"] else pred


def compute_loss(model, clean, noise, mix, cfg):
    with torch.no_grad():
        _, ec = model.extract_features(clean); _, en = model.extract_features(noise)
        irm = torch.sqrt(ec ** 2 / (ec ** 2 + en ** 2 + EPS))
    target = irm ** BETA if cfg["cirm"] else irm
    feats, mix_env = model.extract_features(mix)
    pred = model.forward_features(feats)
    mask_mse = F.mse_loss(pred, target)
    parts = {"mask_mse": float(mask_mse.detach()), "env_sisdr": None, "env_term": 0.0}
    loss = mask_mse
    if cfg["env_loss"]:
        sdr = env_sisdr_db(applied_mask(pred, cfg) * mix_env, ec)
        term = ENV_W * (-sdr.mean()) / 20.0
        loss = loss + term.float()
        parts["env_sisdr"] = float(sdr.mean().detach()); parts["env_term"] = float(term.detach())
    return loss, parts


# --------------------------------------------------------------------------
# Training (one config x one seed)
# --------------------------------------------------------------------------
def cmd_train(a):
    cfg = CONFIGS[a.config]
    if a.threads:
        torch.set_num_threads(a.threads)
    out = Path(a.out) if a.out else HERE / "weights" / f"{a.config}_seed{a.seed}.pt"
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.manual_seed(a.seed); rng = np.random.default_rng(a.seed)
    pool = load_pool(TRAIN_SPK)
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK)), "speaker holdout violated"
    model = J4A1(); assert model.count_parameters() == 238656  # arch EXACT
    opt = torch.optim.Adam(model.parameters(), lr=2e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.steps, eta_min=cfg["lr_min"])
    log = []; t0 = time.time()
    for step in range(a.steps):
        clean, noise, mix, _ = make_batch(rng, pool, cfg, progress=step / max(a.steps - 1, 1))
        loss, parts = compute_loss(model, clean, noise, mix, cfg)
        opt.zero_grad(); loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step(); sched.step()
        if step % 50 == 0 or step == a.steps - 1:
            rec = {"step": step, "loss": float(loss), **parts, "grad_norm": float(gn),
                   "lr": float(opt.param_groups[0]["lr"]), "elapsed_s": round(time.time() - t0, 1)}
            log.append(rec); print(f"[{a.config} s{a.seed}] {rec}", flush=True)
    wall = time.time() - t0
    torch.save({"state_dict": model.state_dict(), "steps": a.steps, "seed": a.seed,
                "config": a.config, "config_dict": cfg, "beta": BETA, "env_w": ENV_W,
                "train_speakers": TRAIN_SPK, "gen": "gen14", "arch": "gen11 J4A1 unchanged"}, out)
    sha = hashlib.sha256(out.read_bytes()).hexdigest()
    meta = {"config": a.config, "config_dict": cfg, "seed": a.seed, "steps": a.steps,
            "wall_s": round(wall, 1), "threads": torch.get_num_threads(),
            "weights_sha256": sha, "params": model.count_parameters(),
            "loss_first3_logged_mean": float(np.mean([r["loss"] for r in log[:3]])),
            "loss_last3_logged_mean": float(np.mean([r["loss"] for r in log[-3:]])), "log": log}
    (out.parent / f"train_log_{a.config}_seed{a.seed}.json").write_text(json.dumps(meta, indent=1))
    print(f"DONE {a.config} seed{a.seed} wall={wall:.0f}s -> {out} sha256={sha}", flush=True)


# --------------------------------------------------------------------------
# Model loading: cIRM decompression wrapper (pointwise, still frame-causal)
# --------------------------------------------------------------------------
class Decompress:
    """Wraps J4A1 so model(mix) returns decompressed masks for cIRM configs."""
    def __init__(self, base):
        self.base = base
        self.window = base.window; self.filterbank = base.filterbank
        self.extract_features = base.extract_features
    def __call__(self, waveform):
        pred, _ = self.base(waveform)
        dec = pred ** (1.0 / BETA)
        _, env = self.base.extract_features(waveform)
        return dec, dec * env


def load_for_eval(wp):
    ckpt = torch.load(wp, map_location="cpu", weights_only=False)
    m = J4A1(); m.load_state_dict(ckpt["state_dict"]); m.eval()
    wrap = Decompress(m) if ckpt.get("config_dict", {}).get("cirm") else m
    return wrap, ckpt


# --------------------------------------------------------------------------
# Quick eval: exact Gen13 eval2 crops, babble+SSN, waveform SI-SDR + logMAE
# --------------------------------------------------------------------------
def cmd_quickeval(a):
    sys.path.insert(0, str(GEN13))
    from eval2 import build_eval_crops, reconstruct, si_sdr  # noqa: E402
    pool = load_pool(TEST_SPK + TEST_BABBLE_SPK)
    crops = [c for c in build_eval_crops(pool, 8) if c["kind"] in ("babble-heldout-spk", "ssn", "quiet")]
    results = {}
    for w in a.weights:
        wp = Path(w); model, ckpt = load_for_eval(wp)
        rows = []
        with torch.no_grad():
            for c in crops:
                mt = torch.from_numpy(c["mix"][None]); ct = torch.from_numpy(c["clean"][None])
                _, ec = model.extract_features(ct) if not isinstance(model, Decompress) else model.base.extract_features(ct)
                feats_env = model.base.extract_features(mt)[1] if isinstance(model, Decompress) else model.extract_features(mt)[1]
                masks, masked = model(mt)
                base = model.base if isinstance(model, Decompress) else model
                wav = reconstruct(base, c["mix"], masks[0])
                wav_un = reconstruct(base, c["mix"], torch.ones_like(masks[0]))
                tr = lambda v: v[256:-256]  # noqa: E731
                logmae = lambda e: float(torch.mean(torch.abs(torch.log(e + 1e-6) - torch.log(ec + 1e-6))))  # noqa: E731
                rows.append({"kind": c["kind"], "d_sisdr": si_sdr(tr(c["clean"]), tr(wav)) - si_sdr(tr(c["clean"]), tr(wav_un)),
                             "imp_logMAE": logmae(feats_env) - logmae(masked)})
        agg = {}
        for kind in ("babble-heldout-spk", "ssn", "quiet"):
            sel = [r for r in rows if r["kind"] == kind]
            if sel:
                agg[kind] = {"n": len(sel), "d_sisdr_mean": float(np.mean([r["d_sisdr"] for r in sel])),
                             "imp_logMAE_mean": float(np.mean([r["imp_logMAE"] for r in sel]))}
        tag = f"{ckpt.get('config')}_seed{ckpt.get('seed')}"
        results[tag] = agg
        print(f"{tag}: {json.dumps(agg)}", flush=True)
    out = HERE / "weights" / "quickeval.json"
    prev = json.loads(out.read_text()) if out.exists() else {}
    prev.update(results); out.write_text(json.dumps(prev, indent=1))
    print(f"QUICKEVAL -> {out}")


# --------------------------------------------------------------------------
# Full eval: Gen13 eval2 protocol verbatim (eval_one_model), one ckpt/proc
# --------------------------------------------------------------------------
def cmd_evalone(a):
    sys.path.insert(0, str(GEN13))
    from eval2 import build_eval_crops, eval_one_model  # noqa: E402
    from ace_sim import mel_to_ace_matrix  # noqa: E402
    wp = Path(a.weights)
    pool = load_pool(TEST_SPK + TEST_BABBLE_SPK)
    crops = build_eval_crops(pool, a.n_per_cell)
    proto = J4A1(); w_ace = mel_to_ace_matrix(proto.filterbank)
    model, ckpt = load_for_eval(wp)
    tag = f"{ckpt.get('config')}_seed{ckpt.get('seed')}"
    # eval_one_model calls model.extract_features / model(waveform); Decompress provides both.
    rows = eval_one_model(model, tag, crops, w_ace)
    out = HERE / "weights" / f"fulleval_rows_{tag}.json"
    out.write_text(json.dumps({"tag": tag, "config": ckpt.get("config"), "seed": ckpt.get("seed"),
                                "weights": str(wp), "sha256": hashlib.sha256(wp.read_bytes()).hexdigest(),
                                "rows": rows}, indent=1))
    print(f"EVALONE DONE {tag} -> {out}", flush=True)


def cmd_combine(a):
    sys.path.insert(0, str(GEN13))
    from eval2 import DIFFS, bootstrap_ci  # noqa: E402
    files = sorted(glob.glob(str(HERE / "weights" / "fulleval_rows_*.json")))
    bycfg = {}
    for f in files:
        d = json.loads(Path(f).read_text()); bycfg.setdefault(d["config"], []).append(d)
    rng = np.random.default_rng(13)  # same bootstrap seed/reps as Gen13 summarise
    summary = {}
    for cfgname, ds in sorted(bycfg.items()):
        ds.sort(key=lambda d: d["seed"])
        # seed-mean per crop (Gen13 convention), then paired bootstrap over crops
        base = ds[0]["rows"]; numkeys = [k for k in base[0] if k not in ("system", "kind", "spk", "snr_db")]
        mean_rows = []
        for i, r0 in enumerate(base):
            mr = {"kind": r0["kind"], "snr_db": r0["snr_db"], "spk": r0["spk"]}
            for k in numkeys:
                mr[k] = float(np.nanmean([d["rows"][i][k] for d in ds]))
            mean_rows.append(mr)
        entry = {"seeds": [d["seed"] for d in ds], "per_seed": {}, "seed_mean": {}}
        for d in ds:
            entry["per_seed"][str(d["seed"])] = _summ(d["rows"], DIFFS, bootstrap_ci, rng)
        entry["seed_mean"] = _summ(mean_rows, DIFFS, bootstrap_ci, rng)
        summary[cfgname] = entry
    out = HERE / "weights" / "fulleval_summary.json"
    out.write_text(json.dumps(summary, indent=1))
    for cfgname, e in summary.items():
        b = e["seed_mean"]["babble-heldout-spk"]["d_sisdr"]
        print(f"{cfgname} seed-mean babble dSI-SDR {b['mean']:+.3f} [{b['ci_lo']:+.3f},{b['ci_hi']:+.3f}] n={b['n']}")
    print(f"COMBINE -> {out}")


def _summ(rows, DIFFS, bootstrap_ci, rng):
    out = {}
    for kind in sorted(set(r["kind"] for r in rows)):
        sel = [r for r in rows if r["kind"] == kind]
        e = {"n_crops": len(sel)}
        for name, (x, y) in DIFFS.items():
            e[name] = bootstrap_ci([r[x] - r[y] for r in sel], rng)
        for k in ["mask_mse", "sisdr_unprocOLA", "sisdr_j4", "sisdr_oracleIRM",
                  "env_logMAE_unproc", "env_logMAE_j4"]:
            e[k] = float(np.nanmean([r[k] for r in sel]))
        out[kind] = e
    return out


# --------------------------------------------------------------------------
# Parallel drivers (subprocesses of this file; one managed foreground call)
# --------------------------------------------------------------------------
def _run_parallel(cmds, label):
    procs = [subprocess.Popen(c) for c in cmds]
    rc = [p.wait() for p in procs]
    print(f"{label} return codes: {rc}", flush=True)
    if any(rc):
        raise SystemExit(f"{label}: a subprocess failed {rc}")


def cmd_screen(a):
    threads = max(1, (os.cpu_count() or 8) // len(CONFIGS))
    cmds = [[sys.executable, str(Path(__file__).resolve()), "train", "--config", c,
             "--seed", str(SEED1), "--steps", str(a.steps), "--threads", str(threads)]
            for c in CONFIGS]
    t0 = time.time(); _run_parallel(cmds, "SCREEN")
    print(f"SCREEN wall={time.time()-t0:.0f}s (4 configs parallel)")


def cmd_fulleval(a):
    wps = a.weights or sorted(glob.glob(str(HERE / "weights" / "C*_seed*.pt")))
    # only best-2 configs (those having BOTH seeds) unless weights given explicitly
    if not a.weights:
        from collections import Counter
        cnt = Counter(Path(w).stem.split("_")[0] for w in wps)
        best = {c for c, n in cnt.items() if n >= 2}
        wps = [w for w in wps if Path(w).stem.split("_")[0] in best]
    print(f"fulleval weights: {wps}", flush=True)
    cmds = [[sys.executable, str(Path(__file__).resolve()), "evalone", "--weights", w] for w in wps]
    t0 = time.time(); _run_parallel(cmds, "FULLEVAL")
    cmd_combine(a)
    print(f"FULLEVAL wall={time.time()-t0:.0f}s")


def cmd_causality(a):
    """Prefix test per checkpoint: shared prefix, differing suffix -> dmask=0."""
    out_lines = []
    for w in a.weights:
        model, ckpt = load_for_eval(Path(w))
        g = torch.Generator().manual_seed(7)
        prefix = torch.randn(1, FS // 2, generator=g) * 0.1
        x1 = torch.cat([prefix, torch.randn(1, FS // 2, generator=g) * 0.1], 1)
        x2 = torch.cat([prefix, torch.randn(1, FS // 2, generator=g) * 0.5], 1)
        with torch.no_grad():
            m1, _ = model(x1); m2, _ = model(x2)
        npre = (FS // 2 - 128) // 64  # frames fully inside shared prefix (conservative)
        d = float((m1[0, :npre] - m2[0, :npre]).abs().max())
        line = f"{Path(w).name}: prefix frames={npre} max|dmask|={d}"
        out_lines.append(line); print(line, flush=True)
        assert d == 0.0, "CAUSALITY VIOLATED"
    print("CAUSALITY OK for all checkpoints")


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("train"); p.add_argument("--config", required=True, choices=sorted(CONFIGS))
    p.add_argument("--seed", type=int, default=SEED1); p.add_argument("--steps", type=int, default=700)
    p.add_argument("--threads", type=int, default=0); p.add_argument("--out", default=None); p.set_defaults(fn=cmd_train)
    p = sub.add_parser("screen"); p.add_argument("--steps", type=int, default=700); p.set_defaults(fn=cmd_screen)
    p = sub.add_parser("quickeval"); p.add_argument("--weights", nargs="+", required=True); p.set_defaults(fn=cmd_quickeval)
    p = sub.add_parser("evalone"); p.add_argument("--weights", required=True)
    p.add_argument("--n-per-cell", type=int, default=8); p.set_defaults(fn=cmd_evalone)
    p = sub.add_parser("fulleval"); p.add_argument("--weights", nargs="*", default=None); p.set_defaults(fn=cmd_fulleval)
    p = sub.add_parser("combine"); p.set_defaults(fn=cmd_combine)
    p = sub.add_parser("causality"); p.add_argument("--weights", nargs="+", required=True); p.set_defaults(fn=cmd_causality)
    a = ap.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
