"""Gen22: 30 dB soft-capped SI-SDR training loss (T0 only).

One change vs the Gen21 trainer (research/gen21/train10.py), per
Astra's Gen21 review rank 1: the training SI-SDR denominator gets
+1e-3*power, smoothly capping the per-example training score near
30 dB so near-perfect (mostly quiet) examples stop dominating the
clipped gradient. `--loss sisdr` reproduces the old objective
exactly (control / equivalence check). Evaluation is uncapped.
Everything else is train10 verbatim: Gen19 batch generator, model,
batch 8x2 s, clip 5, quiet 10%, schedules for both policies.
Additions that do not touch the update path: uncapped SI-SDR is
logged next to the capped loss, quiet/noisy gradient-norm
contributions every 500 steps (torch.autograd.grad on the same
graph, before the real backward), and a rolling full training
state every 2000 steps with --resume (Gen21 seed-19 was killed by
a session end at 12.5k with no resumable state).

Requested: Sol 6.1 (Gen21 base). Gen22 edits: Claude Opus 5.5, 2026-11-04.
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

Run: /tmp/gen9env/bin/python research/gen22/train11.py --loss cap30 --mode scratch --seed 20261117
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, time
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


def neg_si_sdr_cap(ref, est, eps=1e-8, tau=1e-3):
    """Gen22: soft-capped negative SI-SDR (Astra Gen21 review, verbatim
    denominator change). Approaches -10*log10(1/tau) = -30 dB as the
    residual vanishes; ~unchanged for poor reconstructions."""
    ref = ref - ref.mean(dim=-1, keepdim=True)
    est = est - est.mean(dim=-1, keepdim=True)
    alpha = (est * ref).sum(-1, keepdim=True) / ((ref * ref).sum(-1, keepdim=True) + eps)
    proj = alpha * ref
    noise = est - proj
    power = (proj * proj).sum(-1)
    error = (noise * noise).sum(-1)
    ratio = power / (error + tau * power + eps)
    return -10.0 * torch.log10(ratio + eps)


LOSSES = {"sisdr": neg_si_sdr, "cap30": neg_si_sdr_cap}
LOSS_DESC = {"sisdr": "negative waveform SI-SDR vs DELAY-shifted clean (Gen15 recipe)",
             "cap30": "negative waveform SI-SDR, 30 dB soft cap (denominator + 1e-3*power), DELAY-shifted clean"}


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
              init_from=None, parent_sha256=None, loss="cap30"):
    torch.save({"state_dict": model.state_dict(), "steps": steps, "seed": seed,
                "mode": mode, "init_from": init_from, "parent_sha256": parent_sha256,
                "train_speakers": speakers or TRAIN_SPK,
                "data": "LibriSpeech train-clean-100 OpenSLR12 CC-BY-4.0 (archive sha256 d4ddd1d5...bf6e2)",
                "gen": "gen22", "arch": "causal Conv-TasNet-style (gen15/model_causal.py)",
                "loss": LOSS_DESC[loss], "loss_key": loss,
                "babble_k": "uniform {2..12}", "snr_mix": "60% U(-5,5) + 40% U(-5,10)",
                "noise_mix": "70% babble / 30% SSN, 10% quiet"}, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def save_state(model, opt, sched, rng, out, step, seed, mode, extra=None):
    """Full resumable training state (optimizer/scheduler/RNG included)."""
    tmp = Path(f"{out}.tmp")
    torch.save({"state_dict": model.state_dict(), "opt": opt.state_dict(),
                "sched": sched.state_dict(), "np_rng_state": rng.bit_generator.state,
                "torch_rng_state": torch.get_rng_state(), "step": step,
                "seed": seed, "mode": mode, "gen": "gen22", **(extra or {})}, tmp)
    os.replace(tmp, out)  # atomic: a kill mid-write never corrupts the previous state
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def rng_from_state(state, seed=0):
    rng = np.random.default_rng(seed)
    rng.bit_generator.state = state
    return rng


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loss", choices=sorted(LOSSES), required=True)
    ap.add_argument("--mode", choices=["scratch", "restart"], required=True)
    ap.add_argument("--steps", type=int, default=24000,
                    help="total updates in this run (policy frozen by prereg.md; 24k scratch or 24k restart)")
    ap.add_argument("--resume", default=None, help="rolling *_state_latest.pt to resume from")
    ap.add_argument("--state-every", type=int, default=2000)
    ap.add_argument("--diag-every", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20261117)
    ap.add_argument("--init-from", default=None, help="restart: Gen19 parent checkpoint")
    ap.add_argument("--rng-handoff", default=None,
                    help="restart: S48 step-24000 RNG state file (default: gen21/weights/rng_handoff_seed<seed>.pt)")
    ap.add_argument("--device", default="mps" if torch.backends.mps.is_available() else "cpu")
    ap.add_argument("--data-root", default="/tmp/gen17dl/LibriSpeech/train-clean-100")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    tag = f"{a.loss}_{a.mode}"
    out = Path(a.out) if a.out else HERE / "weights" / f"{tag}_seed{a.seed}.pt"
    logp = Path(a.log) if a.log else HERE / "weights" / f"train_log_{tag}_seed{a.seed}.json"
    if out.exists() and not a.force and not a.resume:
        raise SystemExit(f"REFUSED: {out} exists (pass --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)
    life0 = 0 if a.mode == "scratch" else 24000  # lifetime updates already done
    _r = None
    if a.resume:  # validate run identity BEFORE touching any artifact (Astra pre-launch review)
        _r = torch.load(a.resume, map_location="cpu", weights_only=False)
        want = {"seed": a.seed, "mode": a.mode, "loss": a.loss, "total_steps": a.steps,
                "data_root": str(a.data_root), "init_from": a.init_from}
        bad = {k: (_r.get(k), v) for k, v in want.items() if _r.get(k) != v}
        if bad:
            raise SystemExit(f"REFUSED resume: identity mismatch {bad}")
        if not (life0 < _r["step"] < life0 + a.steps):
            raise SystemExit(f"REFUSED resume: saved step {_r['step']} outside ({life0}, {life0 + a.steps})")
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    parent_sha = None
    assert not (set(TRAIN_SPK) & set(TEST_SPK + TEST_BABBLE_SPK + VAL_SPK)), "speaker holdout violated"
    print(f"device={a.device} loss={a.loss} mode={a.mode} steps={a.steps} seed={a.seed}", flush=True)
    loss_fn = LOSSES[a.loss]
    model = CausalTasNetEnh()
    if a.mode == "restart":
        assert a.init_from, "restart requires --init-from"
        _ck = torch.load(a.init_from, map_location="cpu", weights_only=False)
        assert _ck.get("steps") == 24000 and _ck.get("seed") == a.seed, \
            f"parent metadata mismatch: steps={_ck.get('steps')} seed={_ck.get('seed')}"
        model.load_state_dict(_ck["state_dict"] if "state_dict" in _ck else _ck)
        parent_sha = hashlib.sha256(Path(a.init_from).read_bytes()).hexdigest()
        _hf = Path(a.rng_handoff) if a.rng_handoff else HERE.parent / "gen21" / "weights" / f"rng_handoff_seed{a.seed}.pt"
        _h = torch.load(_hf, map_location="cpu", weights_only=False)
        assert _h["seed"] == a.seed and _h["step"] == 24000, f"bad handoff {_hf}: {_h.get('seed')}/{_h.get('step')}"
        rng = rng_from_state(_h["np_rng_state"], seed=a.seed)
        if _r is not None and _r.get("parent_sha256") != parent_sha:
            raise SystemExit(f"REFUSED resume: parent sha {_r.get('parent_sha256')} != {parent_sha}")
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
    ident = {"loss": a.loss, "total_steps": a.steps, "data_root": str(a.data_root),
             "init_from": a.init_from, "parent_sha256": parent_sha, "pool_n_files": int(total_s)}
    if _r is not None and _r.get("pool_n_files") != int(total_s):
        raise SystemExit(f"REFUSED resume: pool files {_r.get('pool_n_files')} != {int(total_s)}")
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
        # Astra interim review: retain the initialized lifetime-24k state
        # (fresh Adam/scheduler + restored handoff RNG) before any batch.
        if _r is None:
            _st0 = out.with_name(f"{out.stem}_state_step24000.pt")
            print(f"initial full state {_st0} sha256={save_state(model, opt, sched, rng, _st0, 24000, a.seed, a.mode, ident)}", flush=True)
    val_panel = build_val_panel()
    roll = out.with_name(f"{out.stem}_state_latest.pt")
    start, t_prev = 0, 0.0
    if _r is not None:
        model.load_state_dict(_r["state_dict"]); opt.load_state_dict(_r["opt"]); sched.load_state_dict(_r["sched"])
        rng = rng_from_state(_r["np_rng_state"], seed=a.seed); torch.set_rng_state(_r["torch_rng_state"])
        start = _r["step"] - life0; log, val_log, t_prev = _r["log"], _r["val_log"], _r["elapsed_s"]
        print(f"RESUMED {a.resume} at lifetime step {_r['step']}", flush=True)
    else:
        _v0, _items0 = eval_val(model, val_panel, a.device)
        val_log = [{"step": 0, "lifetime_step": life0, "val": _v0, "items": _items0}]
        print(f"VAL step0 {_v0}", flush=True)
        log = []
    t0 = time.time() - t_prev
    params = [p for p in model.parameters()]
    for step in range(start, a.steps):
        clean, noise, mix, snrs, kinds = make_batch(rng, pool, train_spk, batch=8)
        clean, mix = clean.to(a.device), mix.to(a.device)
        est = model(mix)
        ref = delay_target(clean)
        losses = loss_fn(ref, est)
        loss = losses.mean()
        diag = None
        if a.diag_every and step % a.diag_every == 0:
            # Astra-requested diagnostic: quiet vs noisy parameter-gradient
            # contributions with the real /8 weighting. autograd.grad does not
            # touch .grad, so the update below is unchanged.
            q = torch.tensor([k == "quiet" for k in kinds], device=losses.device)
            diag = {"n_quiet": int(q.sum())}
            for name, m in (("quiet", q), ("noisy", ~q)):
                if bool(m.any()):
                    g = torch.autograd.grad((losses * m).sum() / len(kinds), params,
                                            retain_graph=True, allow_unused=True)
                    diag[f"gn_{name}"] = float(torch.sqrt(sum((x * x).sum() for x in g if x is not None)))
        opt.zero_grad(); loss.backward()
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step(); sched.step()
        if step % 25 == 0 or step == a.steps - 1 or diag:
            with torch.no_grad():
                plain = float(neg_si_sdr(ref, est.detach()).mean())
            rec = {"step": step, "neg_sisdr_loss_db": float(loss), "neg_sisdr_uncapped_db": plain,
                   "grad_norm": float(gn), "lr": float(opt.param_groups[0]["lr"]),
                   "elapsed_s": round(time.time() - t0, 1)}
            if diag:
                rec["grad_diag"] = diag
            log.append(rec); print(rec, flush=True)
        if (step + 1) % 2000 == 0 and step + 1 < a.steps:
            ck = out.with_name(f"{out.stem}_step{life0 + step + 1}.pt")
            save_ckpt(model, ck, life0 + step + 1, a.seed, train_spk, a.mode, a.init_from, parent_sha, a.loss)
            print(f"interim ckpt {ck}", flush=True)
        if (step + 1) % 2000 == 0:
            v, vitems = eval_val(model, val_panel, a.device)
            val_log.append({"step": step + 1, "lifetime_step": life0 + step + 1,
                            "val": v, "items": vitems})
            print(f"VAL step{step+1} {v}", flush=True)
            # Incremental persistence: a crash must not lose per-example VAL.
            _vp = out.with_name(f"{out.stem}_val_partial.json")
            _vp.write_text(json.dumps({"mode": a.mode, "seed": a.seed,
                                        "val_log": val_log}, indent=1))
        if life0 + step + 1 in (24000, 36000, 48000):
            st = out.with_name(f"{out.stem}_state_step{life0 + step + 1}.pt")
            _sha = save_state(model, opt, sched, rng, st, life0 + step + 1, a.seed, a.mode,
                              {**ident, "log": log, "val_log": val_log, "elapsed_s": time.time() - t0})
            print(f"full state {st} sha256={_sha}", flush=True)
        if a.state_every and (step + 1) % a.state_every == 0 and step + 1 < a.steps:
            save_state(model, opt, sched, rng, roll, life0 + step + 1, a.seed, a.mode,
                       {**ident, "log": log, "val_log": val_log, "elapsed_s": time.time() - t0})
    wall = time.time() - t0
    model = model.to("cpu").eval()
    caus_post = suffix_invariance_test(model, seed=1)
    for r in caus_post:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated post-train: {r}"
    sha = save_ckpt(model, out, life0 + a.steps, a.seed, train_spk, a.mode, a.init_from, parent_sha, a.loss)
    meta = {"steps": a.steps, "lifetime_steps": life0 + a.steps, "mode": a.mode, "loss": a.loss,
            "resumed": bool(a.resume),
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
