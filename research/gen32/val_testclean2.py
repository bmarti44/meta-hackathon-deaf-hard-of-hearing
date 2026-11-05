"""Gen32 copy of research/gen31/val_testclean.py: IDENTICAL panel, material and selection rule; ONE addition, the
per-item scores of every system are kept in the output (Astra's Gen31 review) for descriptive clustered intervals.
The panel is development material since Gen31; the 24 reserved test-clean voices stay untouched.

Gen31 WiSE-FT step 3 of 3: choose the blend weight on a fresh validation panel, never on screen material.

Panel (built exactly like research/screen_v2/panel_v2.py, different voices and seed):
- LibriSpeech test-clean (OpenSLR 12, CC-BY-4.0; archive md5 32fa31d27d2e1cad72775fee3f4849a9, sha256
  39fde525...6c23), never used anywhere in this repo before Gen31.
- 16 target voices: the 8 lowest-numbered female and 8 lowest-numbered male test-clean speakers.
  The other 24 test-clean speakers are RESERVED, untouched, for a later fresh confirmation.
- Per target: 4 clean 4 s crops x 4 crowds (k ~ U{8..12} talkers from the other 15 VAL voices) x SNR
  {-5, 0} dB = 512 dry items. Seed 20261131. Material is hashed.

Rule (registered in research/gen31/prereg.md):
- For each grid alpha, d = mean over items of (blend - Gen19) SI-SDR and STOI, per SNR (paired per item).
- pass(alpha) = all four of d_sisdr(-5), d_stoi(-5), d_sisdr(0), d_stoi(0) >= 0.
- alpha* = the largest grid alpha such that every grid alpha' <= alpha passes. If 0.1 fails: NO CANDIDATE.
- The chosen blend is copied byte-for-byte to the candidate path; nothing else is selected.

Usage:
  python research/gen31/val_testclean.py --hash
  python research/gen31/val_testclean.py --base <gen19.pt> --index research/gen31/weights/blends/index.json \
      --candidate research/gen31/weights/wiseft_seed20261117.pt --out research/gen31/val_selection_s17.json
Exit status 3 = NO CANDIDATE (pipeline stops; Gen31 is then filed as FAIL with no screen).
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, sys, time
from multiprocessing import get_context
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "gen21"))
sys.path.insert(0, str(HERE.parent / "gen24"))
from train10 import load_pool, pool_get, crop, rms, babble, _si_sdr_np, FS  # noqa: E402

ROOT = Path("/tmp/gen31dl/LibriSpeech/test-clean")
FEMALE = ["121", "237", "1221", "1284", "1580", "1995", "2094", "2961"]
MALE = ["61", "260", "672", "908", "1089", "1188", "1320", "2300"]
TARGETS = FEMALE + MALE
RESERVED = ["3570", "3575", "3729", "4446", "4507", "4970", "4992", "5142", "5683", "6829", "8463", "8555",
            "2830", "4077", "5105", "5639", "6930", "7021", "7127", "7176", "7729", "8224", "8230", "8455"]
SEED = 20261131
SNRS = (-5.0, 0.0)
TR = slice(256, -256)


def used_elsewhere():
    """Every speaker id any earlier panel, split or training root used."""
    import train13 as t13
    sys.path.insert(0, str(HERE.parent / "screen_v2"))
    import panel_v2
    ids = set(t13.TRAIN_SPK) | set(t13.TEST_SPK) | set(t13.TEST_BABBLE_SPK) | set(t13.VAL_SPK)
    ids |= set(getattr(t13, "VAL_INTERFERERS", [])) | set(panel_v2.TARGETS) | set(panel_v2.RESERVED)
    tc100 = Path("/tmp/gen17dl/LibriSpeech/train-clean-100")
    if tc100.exists():
        ids |= {d.name for d in tc100.iterdir() if d.is_dir()}
    return ids


def build_items():
    pool = load_pool(TARGETS, root=ROOT)
    rng = np.random.default_rng(SEED)
    seg = 4 * FS
    items = []
    for spk in TARGETS:
        others = [s for s in TARGETS if s != spk]
        for c in range(4):
            clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), seg)
            clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
            for mix_ix in range(4):
                noise0 = babble(rng, pool, others, k=int(rng.integers(8, 13)), n=seg)
                for snr in SNRS:
                    noise = (noise0 / (rms(noise0) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                    items.append({"spk": spk, "crop": c, "mix": mix_ix, "snr": snr,
                                  "clean": clean, "mix_wav": (clean + noise).astype(np.float32)})
    return items


def material_hash(items):
    h = hashlib.sha256()
    for it in items:
        h.update(f"{it['spk']}|{it['crop']}|{it['mix']}|{it['snr']}".encode())
        h.update(it["clean"].tobytes()); h.update(it["mix_wav"].tobytes())
    return h.hexdigest()


def select_alpha(summary, grid):
    """summary[alpha_str][snr_str] = {'d_sisdr','d_stoi'} (blend - Gen19). Returns (alpha* or None, passes)."""
    passes = {}
    for al in grid:
        s = summary[f"{al:.1f}"]
        passes[f"{al:.1f}"] = all(np.isfinite(s[str(snr)][m]) and s[str(snr)][m] >= 0
                                  for snr in SNRS for m in ("d_sisdr", "d_stoi"))
    best = None
    for al in sorted(grid):
        if not passes[f"{al:.1f}"]:
            break
        best = al
    return best, passes


def _eval(args):
    name, path, lo, hi = args
    import torch
    from pystoi import stoi
    from model_causal import CausalTasNetEnh, undelay
    torch.set_num_threads(1)
    items = build_items()[lo:hi]
    m = CausalTasNetEnh()
    ck = torch.load(path, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["state_dict"] if "state_dict" in ck else ck); m.eval()
    out = []
    with torch.no_grad():
        for it in items:
            est = undelay(m(torch.from_numpy(it["mix_wav"][None]))[0].numpy())
            out.append((float(_si_sdr_np(it["clean"][TR], est[TR])),
                        float(stoi(it["clean"][TR].astype(np.float64), est[TR].astype(np.float64), FS))))
    return name, lo, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--base", default=None)
    ap.add_argument("--index", default=None)
    ap.add_argument("--candidate", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    t0 = time.time()
    clash = (set(TARGETS) | set(RESERVED)) & used_elsewhere()
    assert not clash, f"VAL voices used elsewhere: {sorted(clash)}"
    assert len(set(TARGETS) | set(RESERVED)) == 40 and not set(TARGETS) & set(RESERVED)
    items = build_items()
    mh = material_hash(items)
    print(f"items={len(items)} material_sha256={mh} build {time.time()-t0:.0f}s", flush=True)
    if a.hash:
        return
    idx = json.loads(Path(a.index).read_text())
    base_sha = hashlib.sha256(Path(a.base).read_bytes()).hexdigest()
    assert base_sha == idx["base_sha256"], "base checkpoint differs from the blends' base"
    grid = [float(g) for g in idx["grid"]]
    systems = {"gen19": a.base, **{f"{al:.1f}": idx["blends"][f"{al:.1f}"]["path"] for al in grid}}
    for al in grid:
        b = idx["blends"][f"{al:.1f}"]
        assert hashlib.sha256(Path(b["path"]).read_bytes()).hexdigest() == b["sha256"], f"blend {al} hash mismatch"
    n = len(items)
    jobs = [(name, path, 0, n) for name, path in systems.items()]  # one job per system
    res = {name: [None] * n for name in systems}
    with get_context("spawn").Pool(a.workers) as p:
        for name, lo, out in p.imap_unordered(_eval, jobs):
            res[name][lo:lo + len(out)] = out
    assert all(None not in v for v in res.values())
    summary = {}
    for name in systems:
        if name == "gen19":
            continue
        summary[name] = {}
        for snr in SNRS:
            ix = [i for i, it in enumerate(items) if it["snr"] == snr]
            ds = [res[name][i][0] - res["gen19"][i][0] for i in ix]
            dt = [res[name][i][1] - res["gen19"][i][1] for i in ix]
            summary[name][str(snr)] = {"n": len(ix), "d_sisdr": float(np.mean(ds)), "d_stoi": float(np.mean(dt))}
    best, passes = select_alpha(summary, grid)
    per_item = [{"spk": it["spk"], "crop": it["crop"], "mix": it["mix"], "snr": it["snr"],
                 **{f"{name}_sisdr": res[name][i][0] for name in systems}, **{f"{name}_stoi": res[name][i][1] for name in systems}}
                for i, it in enumerate(items)]
    rec = {"panel": "gen31_val_testclean", "seed": SEED, "material_sha256": mh, "targets": TARGETS, "reserved": RESERVED,
           "n_items": n, "base": a.base, "base_sha256": base_sha, "ft_sha256": idx["ft_sha256"], "grid": grid,
           "summary_vs_gen19": summary, "passes": passes, "alpha_star": best, "candidate": None, "candidate_sha256": None,
           "rule": "largest grid alpha such that every alpha' <= alpha has mean (blend - Gen19) SI-SDR and STOI >= 0 at -5 and 0 dB",
           "per_item": per_item}
    for al in grid:
        s = summary[f"{al:.1f}"]
        print(f"alpha={al:.1f} " + " ".join(f"{snr:+.0f}dB d_sisdr={s[str(snr)]['d_sisdr']:+.4f} d_stoi={s[str(snr)]['d_stoi']:+.5f}" for snr in SNRS)
              + f" pass={passes[f'{al:.1f}']}", flush=True)
    if best is not None:
        src = idx["blends"][f"{best:.1f}"]["path"]
        assert not Path(a.candidate).exists(), f"REFUSED: {a.candidate} exists"
        shutil.copyfile(src, a.candidate)
        rec["candidate"] = a.candidate
        rec["candidate_sha256"] = hashlib.sha256(Path(a.candidate).read_bytes()).hexdigest()
        assert rec["candidate_sha256"] == idx["blends"][f"{best:.1f}"]["sha256"]
    Path(a.out).write_text(json.dumps(rec, indent=1))
    print(f"alpha*={best} candidate={rec['candidate']} sha256={rec['candidate_sha256']} {time.time()-t0:.0f}s", flush=True)
    if best is None:
        print("NO CANDIDATE", flush=True)
        sys.exit(3)


if __name__ == "__main__":
    main()
