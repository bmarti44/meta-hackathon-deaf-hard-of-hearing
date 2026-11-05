"""Screen v2 advancement panel (registered for Gen 26 onward; Astra Gen25 pre-launch review).

Built so that later experiments are judged on many more voices than the old
8-item VAL panel and 6-mixture bench, while Gen 19's original scorecard stays
unchanged.

- 16 training-disjoint target voices from LibriSpeech dev-clean that no
  earlier panel used as a target or crowd voice: 8 female, 8 male.
- 4 further unused voices are reserved, untouched, for a later fresh
  confirmation: 5338 F, 3000 M, 3170 M, 3752 M.
- Per target: 4 clean 4-second crops x 4 independently drawn crowds
  (k ~ U{8..12} talkers drawn from the OTHER 15 panel voices) x SNR
  {-5, 0} dB, giving 512 paired items (256 per SNR).
- Fixed RNG seed 20261204, and the material is hashed. Tuning or
  calibration experiments must NOT use this panel; the Gen21 8-voice dev
  panel is the designated tuning material.

Usage:
  python research/screen_v2/panel_v2.py --hash
  python research/screen_v2/panel_v2.py --system control=<ckpt> --system cand=<ckpt> --out <json>
"""
from __future__ import annotations
import argparse, collections, hashlib, json, sys, time
from pathlib import Path
import numpy as np, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE.parent / "gen21"))
from train10 import load_pool, pool_get, crop, rms, babble, _si_sdr_np, FS  # noqa: E402
from model_causal import CausalTasNetEnh, undelay  # noqa: E402

FEMALE = ["84", "1462", "1673", "1919", "3081", "3536", "3576", "3853"]
MALE = ["174", "251", "422", "652", "777", "1272", "2803", "2902"]
TARGETS = FEMALE + MALE
RESERVED = ["5338", "3000", "3170", "3752"]
ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
SEED = 20261204


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
                for snr in (-5.0, 0.0):
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


def load_model(path):
    m = CausalTasNetEnh()
    ck = torch.load(path, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["state_dict"] if "state_dict" in ck else ck)
    return m.eval(), hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hash", action="store_true")
    ap.add_argument("--system", action="append", default=[], metavar="NAME=PATH")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    t0 = time.time()
    items = build_items()
    mh = material_hash(items)
    print(f"items={len(items)} material_sha256={mh} build {time.time()-t0:.0f}s", flush=True)
    if a.hash or not a.system:
        return
    from pystoi import stoi
    tr = slice(256, -256)
    base = {id(it): (_si_sdr_np(it["clean"][tr], it["mix_wav"][tr]),
                     float(stoi(it["clean"][tr].astype(np.float64), it["mix_wav"][tr].astype(np.float64), FS))) for it in items}
    rows = []
    for spec in a.system:
        name, path = spec.split("=", 1)
        model, sha = load_model(path)
        t1 = time.time()
        with torch.no_grad():
            for it in items:
                est = undelay(model(torch.from_numpy(it["mix_wav"][None]))[0].numpy())
                b_s, b_t = base[id(it)]
                rows.append({"system": name, "sha256": sha, "spk": it["spk"], "crop": it["crop"], "mix": it["mix"], "snr": it["snr"],
                             "d_sisdr": float(_si_sdr_np(it["clean"][tr], est[tr]) - b_s),
                             "d_stoi": float(stoi(it["clean"][tr].astype(np.float64), est[tr].astype(np.float64), FS) - b_t)})
        print(f"{name} done {time.time()-t1:.0f}s", flush=True)
    agg = collections.defaultdict(dict)
    for name in {r["system"] for r in rows}:
        for snr in (-5.0, 0.0):
            rs = [r for r in rows if r["system"] == name and r["snr"] == snr]
            agg[name][str(snr)] = {"d_sisdr": float(np.mean([r["d_sisdr"] for r in rs])), "d_stoi": float(np.mean([r["d_stoi"] for r in rs]))}
    Path(a.out).write_text(json.dumps({"panel": "screen_v2", "seed": SEED, "material_sha256": mh, "targets": TARGETS,
                                       "reserved": RESERVED, "n_items": len(items), "summary": agg, "rows": rows}, indent=1))
    for name, v in agg.items():
        print(name, {k: (round(x["d_sisdr"], 3), round(x["d_stoi"], 4)) for k, x in v.items()})
    print(f"WROTE {a.out}")


if __name__ == "__main__":
    main()
