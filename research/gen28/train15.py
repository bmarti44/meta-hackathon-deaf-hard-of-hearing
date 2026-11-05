"""Gen28 (T0): research/gen27/train14.py with ONE change, a new `--room aug25`:
P(reverberant | noisy) = 0.25, i.e. 67.5% dry noisy / 22.5% reverberant noisy / 10% dry quiet
(Gen27 aug50 = 0.5). Everything else is train14 verbatim: Gen19 recipe and draws, Gen27's corrected
RIR manifest (research/gen27/rir_manifest.json), per-talker RIRs from one train room, direct + 50 ms
target with 5 ms taper, augmentation RNG [seed, 27], fixed 63-sample delay. `dry`/`aug50` behave
exactly as in train14. Gen28 edits: Claude Opus 5.5, 2026-11-04 (Astra + Muse Gen27 reviews, choice b).

--- Base: Gen27 train14 docstring follows ---
Gen27 (DRAFT, not launched): room augmentation, one intervention.

Spec: research/gen27/astra-agenda-review.md ("My concrete Gen27
specification"). Trainer = research/gen24/train13.py run as
`--loss sisdr --snr legacy` (the Gen19 recipe bit-for-bit) plus
`--room {dry,aug50}`:

- `dry`: make_batch is train13.make_batch itself, so the batch stream,
  weights and logs are Gen19's. The aug RNG is created but never drawn.
- `aug50`: the main RNG makes EXACTLY the Gen19 draws in the same order
  (speaker, file, crop start, quiet, SNR branch/value, babble/SSN, k,
  interferer speakers/files/crops, SSN white noise). A second RNG,
  np.random.default_rng([seed, 27]) ("aug RNG"), makes every augmentation
  draw, so each example's underlying speech/noise is paired with the Gen19
  stream. Per example the aug RNG draws u ~ U(0,1); quiet examples (10%)
  stay dry; noisy examples (90%) are reverberant when u < 0.5, giving
  45% dry noisy / 45% reverberant noisy / 10% dry quiet.
- Reverberant example: stratum ~ U{short, medium, long}, room ~ U(train
  rooms of that stratum), target position ~ U(room RIRs); every
  interferer source (each babble talker, or the single SSN source) gets
  its own RIR ~ U(the room's other RIRs), drawn with replacement. Each
  source is convolved (with real convolution history: the L_MAX samples
  preceding the crop in the same file, at the same gain) BEFORE
  summation. Training reference = target convolved with the direct +
  50 ms early RIR (rirbank.early_window), then delay_target (fixed
  DELAY=63). SNR = full reverberant target energy vs summed reverberant
  interferer energy (the Gen19 SNR draw). No reference normalization and
  no per-output alignment. Dry examples keep the original clean target.
- SSN history (no Gen19 draw exists for it): the L_MAX samples before the
  SSN segment are generated from the aug RNG with the same filters; the
  SSN segment itself is the Gen19 draw unchanged.

Resume identity includes --room and the RIR manifest sha256; checkpoints
record room_mode. Room metadata counts are logged every 25 steps.
Scratch only (Gen27 trains from scratch; restart mode is not carried over).

Edits: Claude Opus 5.5, 2026-11-04. NEVER a listener-benefit claim.

Run (NOT launched): /tmp/gen9env/bin/python research/gen27/train14.py --loss sisdr --snr legacy --room aug50 --mode scratch --seed 20261117
"""
from __future__ import annotations
import argparse, collections, hashlib, json, os, sys, time
from pathlib import Path
import numpy as np, torch
import scipy.fft as sfft
from scipy.signal import lfilter

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "gen24"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "gen27"))
import train13 as t13  # noqa: E402
import rirbank  # noqa: E402
from model_causal import (CausalTasNetEnh, audit_causality, delay_target,  # noqa: E402
                          receptive_field, suffix_invariance_test)

FS, SEG = t13.FS, t13.SEG
CTX = rirbank.L_MAX                      # convolution history (samples)
NFFT = sfft.next_fast_len(SEG + CTX)    # circular conv clean on [CTX, CTX+SEG)
ROOM_MODES = ("dry", "aug50", "aug25")
REV_P_BY = {"aug50": 0.5, "aug25": 0.25}  # share of noisy examples made reverberant (Gen28: aug25)
REV_P = 0.5                              # legacy name (aug50)
DEFAULT_MANIFEST = HERE.parent / "gen27" / "rir_manifest.json"


def crop_ctx(rng, arr, n=SEG, ctx=CTX):
    """train13.crop with the same single draw, also returning the ctx
    samples before the crop (zero-padded on the left at file start)."""
    pre = np.zeros(ctx, dtype=np.float32)
    if len(arr) <= n:
        out = np.zeros(n, dtype=np.float32); out[:len(arr)] = arr; return out, pre
    s = rng.integers(0, len(arr) - n + 1)
    p = arr[max(0, s - ctx):s]
    pre[ctx - len(p):] = p
    return arr[s:s + n].copy(), pre


def babble_stems(rng, pool, speakers, k=3, n=SEG, ctx=CTX):
    """train13.babble's draws, returning each RMS-normalized talker stem and
    its history at the same gain. sum(stems)/k reproduces babble() exactly
    (same float64 accumulation order); see test_train14."""
    stems, pres = [], []
    for _ in range(k):
        spk = speakers[rng.integers(0, len(speakers))]
        arr = t13.pool_get(pool, spk, int(rng.integers(0, len(pool[spk]))))
        c, p = crop_ctx(rng, arr, n, ctx)
        c = c.astype(np.float64); g = t13.rms(c) + 1e-9
        stems.append(c / g); pres.append(p.astype(np.float64) / g)
    return stems, pres


def sum_stems(stems, k):
    out = np.zeros(len(stems[0]), dtype=np.float64)
    for s in stems:
        out += s
    return (out / k).astype(np.float32)


def ssn_history(aug_rng, ctx=CTX):
    w = aug_rng.standard_normal(ctx)
    y = lfilter([0.15], [1, -0.85], w); y = lfilter([1.0], [1, -0.4], y)
    return y


def conv_window(x_full, H, nfft=NFFT, ctx=CTX, n=SEG):
    """Linear convolution of x_full (ctx + n samples) with the RIR whose
    rfft is H, keeping output samples [ctx, ctx + n)."""
    return sfft.irfft(sfft.rfft(x_full, nfft) * H, nfft)[ctx:ctx + n]


def render_reverberant(aug_rng, bank, clean, pre, src_stems, src_pres, k):
    """Returns (rev_target, early_target, rev_noise_unscaled, meta)."""
    strata = ("short", "medium", "long")
    stratum = strata[aug_rng.integers(0, 3)]
    rooms = bank.rooms[stratum]
    room = rooms[aug_rng.integers(0, len(rooms))]
    n_pos = len(room["H"])
    t = int(aug_rng.integers(0, n_pos))
    others = [i for i in range(n_pos) if i != t]
    x = np.concatenate([pre.astype(np.float64), clean.astype(np.float64)])
    X = sfft.rfft(x, bank.nfft)
    rev_t = sfft.irfft(X * room["H"][t], bank.nfft)[CTX:CTX + SEG]
    early = sfft.irfft(X * room["HE"][t], bank.nfft)[CTX:CTX + SEG]
    acc = np.zeros(bank.nfft // 2 + 1, dtype=np.complex128)
    src_pos = []
    for s, p in zip(src_stems, src_pres):
        j = others[aug_rng.integers(0, len(others))]
        src_pos.append(j)
        acc += sfft.rfft(np.concatenate([p, s]), bank.nfft) * room["H"][j]
    rev_n = sfft.irfft(acc, bank.nfft)[CTX:CTX + SEG] / k
    m = room["meta"][t]
    meta = {"room_id": room["room_id"], "stratum": stratum, "target_pos": t, "src_pos": src_pos,
            "drr_db": m["drr_db"], "c50_db": m["c50_db"], "rt60_s": m["rt60_s"]}
    return rev_t, early, rev_n, meta


def make_batch(rng, pool, speakers, batch=8, quiet_p=0.10, snr_mode="legacy",
               room="dry", aug_rng=None, bank=None):
    """room='dry' -> train13.make_batch verbatim (5-tuple). room='aug50' ->
    same main-RNG draws plus aug-RNG rendering; returns a 6-tuple whose
    first item is the training reference (early target if reverberant,
    original clean if dry) and whose last item is per-example metadata."""
    if room == "dry":
        return t13.make_batch(rng, pool, speakers, batch=batch, quiet_p=quiet_p, snr_mode=snr_mode)
    assert room in REV_P_BY and aug_rng is not None and bank is not None, room
    refs, noises, mixs, snrs, kinds, metas = [], [], [], [], [], []
    for _ in range(batch):
        spk = speakers[rng.integers(0, len(speakers))]
        clean, pre = crop_ctx(rng, t13.pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))))
        g = t13.rms(clean) + 1e-9
        clean = (clean / g * 0.1).astype(np.float32)
        pre = (pre / g * 0.1).astype(np.float32)
        u = aug_rng.random()  # drawn for every example: aug stream independent of content
        if rng.random() < quiet_p:
            noise = np.zeros_like(clean); snr = 999.0; kind = "quiet"
            refs.append(clean); noises.append(noise); mixs.append(clean.copy())
            snrs.append(snr); kinds.append(kind); metas.append({"cond": "dry_quiet"})
            continue
        low = rng.random() < 0.6
        x = float(rng.uniform(-5, 5)) if low else float(rng.uniform(-5, 10))
        snr = t13.map_snr(x, low, snr_mode)
        if rng.random() < 0.70:
            others = [s for s in speakers if s != spk]
            k = int(rng.integers(2, 13))
            stems, spres = babble_stems(rng, pool, others, k=k); kind = f"babble{k}"
            dry_noise = sum_stems(stems, k); kdiv = k
        else:
            ssn = t13.make_ssn_fast(rng); kind = "ssn"
            stems, spres = [ssn.astype(np.float64)], None
            dry_noise = ssn; kdiv = 1
        rev = u < REV_P_BY[room]
        if not rev:
            noise = (dry_noise / (t13.rms(dry_noise) + 1e-9) * t13.rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
            refs.append(clean); noises.append(noise); mixs.append(clean + noise)
            snrs.append(snr); kinds.append(kind); metas.append({"cond": "dry_noisy"})
            continue
        if spres is None:
            spres = [ssn_history(aug_rng)]
        rev_t, early, rev_n, meta = render_reverberant(aug_rng, bank, clean, pre, stems, spres, kdiv)
        noise = rev_n / (t13.rms(rev_n) + 1e-9) * t13.rms(rev_t) * 10 ** (-snr / 20)
        refs.append(early.astype(np.float32)); noises.append(noise.astype(np.float32))
        mixs.append((rev_t + noise).astype(np.float32))
        snrs.append(snr); kinds.append(kind); metas.append({"cond": "rev_noisy", **meta})
    to = lambda a: torch.from_numpy(np.stack(a))  # noqa: E731
    return to(refs), to(noises), to(mixs), snrs, kinds, metas


class RoomCounts:
    """Cumulative room-metadata counts for the log."""

    def __init__(self, d=None):
        d = d or {}
        self.cond = collections.Counter(d.get("cond", {}))
        self.stratum = collections.Counter(d.get("stratum", {}))
        self.room = collections.Counter(d.get("room", {}))
        self.sum_drr = d.get("sum_drr", 0.0); self.sum_c50 = d.get("sum_c50", 0.0)

    def add(self, metas):
        for m in metas:
            self.cond[m["cond"]] += 1
            if m["cond"] == "rev_noisy":
                self.stratum[m["stratum"]] += 1; self.room[m["room_id"]] += 1
                self.sum_drr += m["drr_db"]; self.sum_c50 += m["c50_db"]

    def as_dict(self):
        n = max(1, self.cond.get("rev_noisy", 0))
        return {"cond": dict(self.cond), "stratum": dict(self.stratum), "room": dict(self.room),
                "n_rooms_used": len(self.room), "sum_drr": self.sum_drr, "sum_c50": self.sum_c50,
                "mean_target_drr_db": self.sum_drr / n, "mean_target_c50_db": self.sum_c50 / n}

    def brief(self):
        d = self.as_dict()
        return {"cond": d["cond"], "stratum": d["stratum"], "n_rooms_used": d["n_rooms_used"],
                "mean_target_drr_db": round(d["mean_target_drr_db"], 2),
                "mean_target_c50_db": round(d["mean_target_c50_db"], 2)}


ROOM_DESC = {"dry": "no room augmentation (Gen19 stream)",
             "aug25": "67.5% dry noisy / 22.5% reverberant noisy / 10% dry quiet; per-source RIRs from one train room; else as aug50",
             "aug50": "45% dry noisy / 45% reverberant noisy / 10% dry quiet; per-source RIRs from one train room "
                      "(RT60 strata short/medium/long uniform); reference = direct + 50 ms (5 ms taper)"}


def save_ckpt(model, out, steps, seed, speakers, loss, snr, room, rir_sha):
    torch.save({"state_dict": model.state_dict(), "steps": steps, "seed": seed,
                "mode": "scratch", "init_from": None, "parent_sha256": None,
                "train_speakers": speakers,
                "data": "LibriSpeech train-clean-100 OpenSLR12 CC-BY-4.0 (archive sha256 d4ddd1d5...bf6e2)",
                "gen": "gen27", "arch": "causal Conv-TasNet-style (gen15/model_causal.py)",
                "loss": t13.LOSS_DESC[loss], "loss_key": loss,
                "babble_k": "uniform {2..12}", "snr_mode": snr, "snr_mix": t13.SNR_DESC[snr],
                "noise_mix": "70% babble / 30% SSN, 10% quiet",
                "room_mode": room, "room_desc": ROOM_DESC[room], "rir_manifest_sha256": rir_sha}, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def save_state(model, opt, sched, rng, aug_rng, out, step, seed, extra=None):
    tmp = Path(f"{out}.tmp")
    torch.save({"state_dict": model.state_dict(), "opt": opt.state_dict(),
                "sched": sched.state_dict(), "np_rng_state": rng.bit_generator.state,
                "aug_rng_state": aug_rng.bit_generator.state,
                "torch_rng_state": torch.get_rng_state(), "step": step,
                "seed": seed, "mode": "scratch", "gen": "gen27", **(extra or {})}, tmp)
    os.replace(tmp, out)
    return hashlib.sha256(Path(out).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--loss", choices=sorted(t13.LOSSES), required=True)
    ap.add_argument("--mode", choices=["scratch"], required=True)
    ap.add_argument("--snr", choices=t13.SNR_MODES, required=True)
    ap.add_argument("--room", choices=ROOM_MODES, required=True)
    ap.add_argument("--rir-manifest", default=str(DEFAULT_MANIFEST))
    ap.add_argument("--rir-root", default=str(rirbank.FILE_ROOT))
    ap.add_argument("--steps", type=int, default=24000)
    ap.add_argument("--resume", default=None)
    ap.add_argument("--state-every", type=int, default=2000)
    ap.add_argument("--diag-every", type=int, default=500)
    ap.add_argument("--val-every", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20261117)
    ap.add_argument("--device", default="mps" if torch.backends.mps.is_available() else "cpu")
    ap.add_argument("--data-root", default="/tmp/gen17dl/LibriSpeech/train-clean-100")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    tag = f"{a.loss}_{a.snr}_{a.room}_{a.mode}"
    out = Path(a.out) if a.out else HERE / "weights" / f"{tag}_seed{a.seed}.pt"
    logp = Path(a.log) if a.log else HERE / "weights" / f"train_log_{tag}_seed{a.seed}.json"
    if out.exists() and not a.force and not a.resume:
        raise SystemExit(f"REFUSED: {out} exists (pass --force to overwrite)")
    out.parent.mkdir(parents=True, exist_ok=True)
    rir_sha = rirbank.sha256_file(a.rir_manifest) if a.room != "dry" else None
    _r = None
    if a.resume:  # identity checked before touching any artifact
        _r = torch.load(a.resume, map_location="cpu", weights_only=False)
        want = {"seed": a.seed, "mode": a.mode, "loss": a.loss, "snr": a.snr, "room": a.room,
                "rir_manifest_sha256": rir_sha, "total_steps": a.steps, "data_root": str(a.data_root),
                "init_from": None}
        bad = {k: (_r.get(k), v) for k, v in want.items() if _r.get(k) != v}
        if bad:
            raise SystemExit(f"REFUSED resume: identity mismatch {bad}")
        if not (0 < _r["step"] < a.steps):
            raise SystemExit(f"REFUSED resume: saved step {_r['step']} outside (0, {a.steps})")
    torch.manual_seed(a.seed)
    rng = np.random.default_rng(a.seed)
    aug_rng = np.random.default_rng([a.seed, 27])  # never drawn in dry mode
    assert not (set(t13.TRAIN_SPK) & set(t13.TEST_SPK + t13.TEST_BABBLE_SPK + t13.VAL_SPK)), "speaker holdout violated"
    print(f"device={a.device} loss={a.loss} room={a.room} steps={a.steps} seed={a.seed}", flush=True)
    loss_fn = t13.LOSSES[a.loss]
    model = CausalTasNetEnh()
    bad = audit_causality(model)
    assert not bad, bad
    caus = suffix_invariance_test(model)
    for r in caus:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated: {r}"
    print(f"params={model.count_parameters()} rf={receptive_field()}", flush=True)
    print(f"causality pre-train: {caus}", flush=True)
    model = model.to(a.device)
    root = Path(a.data_root)
    train_spk = sorted(d.name for d in root.iterdir() if d.is_dir())
    assert train_spk, f"no speaker dirs under {root}"
    assert not (set(train_spk) & set(t13.TEST_SPK + t13.TEST_BABBLE_SPK + t13.VAL_SPK)), "holdout leak in data root"
    pool = t13.load_pool(train_spk, root=root)
    counts = {k: len(v) for k, v in pool.items()}
    total_s = float(sum(counts.values()))
    print(f"data_root={root} speakers={len(train_spk)} pool n_files={int(total_s)}", flush=True)
    bank, bank_s = None, 0.0
    if a.room != "dry":
        tb = time.time()
        bank = rirbank.Bank(a.rir_manifest, splits=("train",), nfft=NFFT, root=a.rir_root)
        bank_s = time.time() - tb
        man_rooms = {s: [r["room_id"] for r in v] for s, v in bank.rooms.items()}
        assert all(man_rooms.values()), f"empty stratum in train bank {man_rooms}"
        print(f"RIR bank manifest_sha256={rir_sha} train rooms={ {s: len(v) for s, v in man_rooms.items()} } "
              f"rirs={bank.n_rirs()} nfft={NFFT} cache_s={bank_s:.1f}", flush=True)
    ident = {"loss": a.loss, "snr": a.snr, "room": a.room, "rir_manifest_sha256": rir_sha,
             "total_steps": a.steps, "data_root": str(a.data_root),
             "init_from": None, "parent_sha256": None, "pool_n_files": int(total_s)}
    if _r is not None and _r.get("pool_n_files") != int(total_s):
        raise SystemExit(f"REFUSED resume: pool files {_r.get('pool_n_files')} != {int(total_s)}")
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=a.steps, eta_min=1e-4)
    val_panel = t13.build_val_panel()
    roll = out.with_name(f"{out.stem}_state_latest.pt")
    start, t_prev = 0, 0.0
    rc = RoomCounts()
    if _r is not None:
        model.load_state_dict(_r["state_dict"]); opt.load_state_dict(_r["opt"]); sched.load_state_dict(_r["sched"])
        rng = t13.rng_from_state(_r["np_rng_state"], seed=a.seed)
        aug_rng = t13.rng_from_state(_r["aug_rng_state"], seed=a.seed)
        torch.set_rng_state(_r["torch_rng_state"])
        start = _r["step"]; log, val_log, t_prev = _r["log"], _r["val_log"], _r["elapsed_s"]
        rc = RoomCounts(_r.get("room_counts"))
        print(f"RESUMED {a.resume} at step {_r['step']}", flush=True)
    else:
        _v0, _items0 = t13.eval_val(model, val_panel, a.device)
        val_log = [{"step": 0, "lifetime_step": 0, "val": _v0, "items": _items0}]
        print(f"VAL step0 {_v0}", flush=True)
        log = []
    t0 = time.time() - t_prev
    data_s = 0.0
    params = [p for p in model.parameters()]
    for step in range(start, a.steps):
        td = time.time()
        b = make_batch(rng, pool, train_spk, batch=8, snr_mode=a.snr, room=a.room, aug_rng=aug_rng, bank=bank)
        clean, noise, mix, snrs, kinds = b[:5]
        if a.room != "dry":
            rc.add(b[5])
        else:
            rc.add([{"cond": "dry_quiet" if k == "quiet" else "dry_noisy"} for k in kinds])
        data_s += time.time() - td
        clean, mix = clean.to(a.device), mix.to(a.device)
        est = model(mix)
        ref = delay_target(clean)
        losses = loss_fn(ref, est)
        loss = losses.mean()
        diag = None
        if a.diag_every and step % a.diag_every == 0:
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
                plain = float(t13.neg_si_sdr(ref, est.detach()).mean())
            rec = {"step": step, "neg_sisdr_loss_db": float(loss), "neg_sisdr_uncapped_db": plain,
                   "grad_norm": float(gn), "lr": float(opt.param_groups[0]["lr"]),
                   "elapsed_s": round(time.time() - t0, 1), "room_counts": rc.brief()}
            if diag:
                rec["grad_diag"] = diag
            log.append(rec); print(rec, flush=True)
        if (step + 1) % 2000 == 0 and step + 1 < a.steps:
            ck = out.with_name(f"{out.stem}_step{step + 1}.pt")
            save_ckpt(model, ck, step + 1, a.seed, train_spk, a.loss, a.snr, a.room, rir_sha)
            print(f"interim ckpt {ck} (never a substitute for the final)", flush=True)
        if a.val_every and (step + 1) % a.val_every == 0:
            v, vitems = t13.eval_val(model, val_panel, a.device)
            val_log.append({"step": step + 1, "lifetime_step": step + 1, "val": v, "items": vitems})
            print(f"VAL step{step+1} {v}", flush=True)
            out.with_name(f"{out.stem}_val_partial.json").write_text(
                json.dumps({"room": a.room, "seed": a.seed, "val_log": val_log}, indent=1))
        if step + 1 == 24000:
            st = out.with_name(f"{out.stem}_state_step24000.pt")
            _sha = save_state(model, opt, sched, rng, aug_rng, st, step + 1, a.seed,
                              {**ident, "log": log, "val_log": val_log, "elapsed_s": time.time() - t0,
                               "room_counts": rc.as_dict()})
            print(f"full state {st} sha256={_sha}", flush=True)
        if a.state_every and (step + 1) % a.state_every == 0 and step + 1 < a.steps:
            save_state(model, opt, sched, rng, aug_rng, roll, step + 1, a.seed,
                       {**ident, "log": log, "val_log": val_log, "elapsed_s": time.time() - t0,
                        "room_counts": rc.as_dict()})
    wall = time.time() - t0
    model = model.to("cpu").eval()
    caus_post = suffix_invariance_test(model, seed=1)
    for r in caus_post:
        assert r["max_diff_prefix_P"] == 0.0, f"causality violated post-train: {r}"
    sha = save_ckpt(model, out, a.steps, a.seed, train_spk, a.loss, a.snr, a.room, rir_sha)
    meta = {"steps": a.steps, "lifetime_steps": a.steps, "mode": a.mode, "loss": a.loss, "snr": a.snr,
            "room": a.room, "room_desc": ROOM_DESC[a.room], "rir_manifest_sha256": rir_sha,
            "rir_cache_s": round(bank_s, 2), "data_s_this_process": round(data_s, 1),
            "room_counts": rc.as_dict(), "resumed": bool(a.resume), "init_from": None, "parent_sha256": None,
            "wall_s": round(wall, 1), "batch": 8, "seg_s": 2.0,
            "seed": a.seed, "weights": str(out), "weights_sha256": sha,
            "params": model.count_parameters(), "pool_files": counts,
            "pool_n_files": int(total_s), "receptive_field": receptive_field(),
            "causality_pre": caus, "causality_post": caus_post,
            "loss_first5_logged_mean": float(np.mean([r[t13.LOSS_KEY[a.loss]] for r in log[:5]])),
            "loss_last5_logged_mean": float(np.mean([r[t13.LOSS_KEY[a.loss]] for r in log[-5:]])),
            "log": log, "val_log": val_log}
    logp.write_text(json.dumps(meta, indent=1))
    print(f"DONE wall={wall:.0f}s data_s={data_s:.1f} weights={out} sha256={sha}", flush=True)


if __name__ == "__main__":
    main()
