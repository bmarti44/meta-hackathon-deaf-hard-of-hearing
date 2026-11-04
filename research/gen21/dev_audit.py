"""Gen21 expanded development diagnostic (Astra Gen21 review) — T0 only.

Estimates mixture variability WITHIN target content, which the
registered panels cannot: 8 existing development targets
(VAL 5536/5694 + bench-v2 1988/1993/5895/6241/6295/6313) x
4 clean crops x 4 independently sampled crowd mixtures
(k8-12, same 6-voice recipes as VAL/bench) x SNR {-5, 0} dB.
Systems: parent + both 36k + both 48k finals, identical material.
Development evidence ONLY: registered panels and metrics are
untouched; no confirmation speakers are used; nothing here can
select checkpoints or support a KPI claim.

Run: /tmp/gen9env/bin/python research/gen21/dev_audit.py --device cpu
"""
from __future__ import annotations
import argparse, collections, hashlib, json, sys, time
from pathlib import Path
import numpy as np, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen15"))
sys.path.insert(0, str(HERE))
from train10 import load_pool, pool_get, crop, rms, babble, _si_sdr_np, FS  # noqa: E402
from model_causal import CausalTasNetEnh, undelay  # noqa: E402

VAL_T = ["5536", "5694"]
VAL_I = ["2035", "2078", "2086", "2277", "2412", "2428"]
BENCH_T = ["1988", "1993", "5895", "6241", "6295", "6313"]
BENCH_I = ["8297", "8842", "6319", "6345", "7850", "7976"]
ROOT = Path("/tmp/gen12dl/LibriSpeech/dev-clean")
SYSTEMS = [
    ("parent", "research/gen19/weights/causal_seed20261117.pt"),
    ("s48_36k", "research/gen21/weights/s48_seed20261117_step36000.pt"),
    ("s48_48k", "research/gen21/weights/s48_seed20261117.pt"),
    ("r48_36k", "research/gen21/weights/r48_seed20261117_step36000.pt"),
    ("r48_48k", "research/gen21/weights/r48_seed20261117.pt"),
]


def build_items():
    pool = load_pool(VAL_T + VAL_I + BENCH_T + BENCH_I, root=ROOT)
    rng = np.random.default_rng(20261123)
    SEG4 = 4 * FS
    items = []
    for spk, interf in [(s, VAL_I) for s in VAL_T] + [(s, BENCH_I) for s in BENCH_T]:
        for c in range(4):
            clean = crop(rng, pool_get(pool, spk, int(rng.integers(0, len(pool[spk])))), SEG4)
            clean = (clean / (rms(clean) + 1e-9) * 0.1).astype(np.float32)
            for mix_ix in range(4):
                noise0 = babble(rng, pool, interf, k=int(rng.integers(8, 13)), n=SEG4)
                for snr in (-5.0, 0.0):
                    noise = (noise0 / (rms(noise0) + 1e-9) * rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                    items.append({"spk": spk, "crop": c, "mix": mix_ix, "snr": snr,
                                  "clean": clean, "mix_wav": (clean + noise).astype(np.float32)})
    return items


def load_model(path, device):
    m = CausalTasNetEnh()
    ck = torch.load(path, map_location="cpu", weights_only=False)
    m.load_state_dict(ck["state_dict"] if "state_dict" in ck else ck)
    return m.to(device).eval(), hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    from pystoi import stoi
    ap = argparse.ArgumentParser()
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--out", default=str(HERE / "dev_audit.json"))
    a = ap.parse_args()
    items = build_items()
    print(f"items={len(items)} device={a.device}", flush=True)
    rows = []
    tr = slice(256, -256)
    base = {}
    for it in items:
        base[id(it)] = (_si_sdr_np(it["clean"][tr], it["mix_wav"][tr]),
                        float(stoi(it["clean"][tr].astype(np.float64), it["mix_wav"][tr].astype(np.float64), FS)))
    for name, path in SYSTEMS:
        model, sha = load_model(path, a.device)
        t0 = time.time()
        with torch.no_grad():
            for it in items:
                est = undelay(model(torch.from_numpy(it["mix_wav"][None]).to(a.device))[0].cpu().numpy())
                b_s, b_t = base[id(it)]
                rows.append({"system": name, "sha256": sha, "spk": it["spk"], "crop": it["crop"],
                             "mix": it["mix"], "snr": it["snr"],
                             "d_sisdr": float(_si_sdr_np(it["clean"][tr], est[tr]) - b_s),
                             "d_stoi": float(stoi(it["clean"][tr].astype(np.float64), est[tr].astype(np.float64), FS) - b_t)})
        print(f"{name} done {time.time()-t0:.0f}s", flush=True)
        del model
    agg = {}
    for (sysn, snr), rs in collections.defaultdict(list, {}).items():
        pass
    groups = collections.defaultdict(list)
    for r in rows:
        groups[(r["system"], r["snr"])].append(r)
    for (sysn, snr), rs in sorted(groups.items()):
        agg[f"{sysn}@{snr}"] = {
            "d_sisdr": float(np.mean([r["d_sisdr"] for r in rs])),
            "d_stoi": float(np.mean([r["d_stoi"] for r in rs])),
            "per_target_sisdr": {s: float(np.mean([r["d_sisdr"] for r in rs if r["spk"] == s]))
                                 for s in sorted({r["spk"] for r in rs})}}
    Path(a.out).write_text(json.dumps({"seed": 20261123, "n_items": len(items),
                                        "summary": agg, "rows": rows}, indent=1))
    for k, v in agg.items():
        print(k, f"dSI-SDR {v['d_sisdr']:+.3f} dSTOI {v['d_stoi']:+.3f}")
    print(f"WROTE {a.out}")


if __name__ == "__main__":
    main()
