"""Bench v2 (pre-registered in bench-v2-prereg.md). Legacy bench.py untouched.

Adds: crowd (>=8 talkers) vs competing (2 talkers) babble split,
6 test target speakers, vocoded ESTOI + simplified NCM.
Run: /tmp/gen9env/bin/python research/bench-n6/bench_v2.py --n-per-cell 2 \
       [--gen15 <causal checkpoint>]
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "gen13"))
sys.path.insert(0, str(HERE.parent / "gen15"))

from common import FS, bootstrap_ci, limit_signal  # noqa: E402
from baselines import CausalSpectralGate, oracle_irm_waveform  # noqa: E402
from bench import load_gen15, metrics_for  # noqa: E402
from vocoder import extract_envelopes, vocode  # noqa: E402

TRAIN_SPK_V2 = ["84", "174", "251", "422", "652", "777", "1272", "1462", "1673", "1919",
                "2035", "2078", "2086", "2277", "2412", "2428", "2803", "2902", "3000",
                "3081", "3170", "3536", "3576", "3752", "3853", "5338"]
VAL_SPK = ["5536", "5694"]
TEST_SPK_V2 = ["1988", "1993", "5895", "6241", "6295", "6313"]
TEST_INTERFERERS = ["8297", "8842", "6319", "6345", "7850", "7976"]
assert not (set(TRAIN_SPK_V2) & set(VAL_SPK + TEST_SPK_V2 + TEST_INTERFERERS))
assert not (set(TEST_SPK_V2) & set(TEST_INTERFERERS))
CROWD_K = (8, 12)


def build_crops_v2(n_per_cell):
    from train2 import babble, crop, load_pool, make_ssn_fast, rms as _rms
    pool = load_pool(TEST_SPK_V2 + TEST_INTERFERERS)
    rng = np.random.default_rng(20261117)
    SEG = 4 * FS
    crops = []
    for kind in ["crowd", "competing", "ssn", "white-heldout", "quiet"]:
        snrs = [999.0] if kind == "quiet" else [-5.0, 0.0, 5.0, 10.0]
        for snr in snrs:
            for i in range(n_per_cell):
                spk = TEST_SPK_V2[i % len(TEST_SPK_V2)]
                clean = crop(rng, pool[spk][rng.integers(0, len(pool[spk]))], SEG)
                clean = (clean / (_rms(clean) + 1e-9) * 0.1).astype(np.float32)
                if kind == "quiet":
                    noise = np.zeros_like(clean)
                elif kind == "crowd":
                    noise = babble(rng, pool, TEST_INTERFERERS, k=int(rng.integers(CROWD_K[0], CROWD_K[1] + 1)), n=SEG)
                elif kind == "competing":
                    noise = babble(rng, pool, TEST_INTERFERERS, k=2, n=SEG)
                elif kind == "ssn":
                    noise = np.concatenate([make_ssn_fast(rng, SEG // 2), make_ssn_fast(rng, SEG - SEG // 2)])
                else:
                    noise = rng.standard_normal(SEG).astype(np.float32)
                if kind != "quiet":
                    noise = (noise / (_rms(noise) + 1e-9) * _rms(clean) * 10 ** (-snr / 20)).astype(np.float32)
                crops.append({"kind": kind, "snr_db": float(snr), "spk": spk,
                              "clean": clean, "noise": noise, "mix": (clean + noise).astype(np.float32)})
    return crops


def vocoded_estoi(clean, est, seed=7):
    try:
        from pystoi import stoi
        vc = vocode(limit_signal(clean), seed=seed)
        ve = vocode(limit_signal(est), seed=seed)
        tr = slice(256, -256)
        return float(stoi(vc[tr].astype(np.float64), ve[tr].astype(np.float64), FS, extended=True))
    except Exception:
        return float("nan")


def ncm_simple(clean, est):
    """Simplified NCM: mean per-ACE-band normalized envelope covariance
    on vocoded signals is expensive; here on raw-waveform ACE envelopes
    (labeled simplified — not full Chen & Loizou)."""
    a = extract_envelopes(est); b = extract_envelopes(clean)
    T = min(len(a), len(b)); a, b = a[:T], b[:T]
    a = a - a.mean(axis=0, keepdims=True); b = b - b.mean(axis=0, keepdims=True)
    cov = (a * b).mean(axis=0)
    den = np.sqrt((a ** 2).mean(axis=0) * (b ** 2).mean(axis=0)) + 1e-12
    return float(np.clip(np.mean(cov / den), -1, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-cell", type=int, default=2)
    ap.add_argument("--gen15", default=None)
    ap.add_argument("--candidate-name", default="gen15_causal")
    ap.add_argument("--out", default=str(HERE / "bench_v2_results.json"))
    a = ap.parse_args()
    t0 = time.time()
    crops = build_crops_v2(a.n_per_cell)
    systems = {"unproc": lambda c: c["mix"],
               "causal_gate": lambda c: CausalSpectralGate().process(c["mix"]),
               "oracle_noncausal": lambda c: oracle_irm_waveform(c["clean"], c["noise"], c["mix"])}
    if a.gen15:
        systems[a.candidate_name] = lambda c, r=load_gen15(a.gen15): r(c["mix"])
    rows = []
    for ci, c in enumerate(crops):
        for name, fn in systems.items():
            est = fn(c)
            rows.append({"crop": ci, "kind": c["kind"], "snr_db": c["snr_db"], "spk": c["spk"],
                         "system": name, **metrics_for(c["clean"], est),
                         "voc_estoi": vocoded_estoi(c["clean"], est),
                         "ncm_simple": ncm_simple(c["clean"], est)})
        print(f"crop {ci+1}/{len(crops)} {c['kind']} elapsed={time.time()-t0:.0f}s", flush=True)
    base = {r["crop"]: r for r in rows if r["system"] == "unproc"}
    summary = {}
    for name in systems:
        summary[name] = {}
        for kind in sorted({r["kind"] for r in rows}):
            sel = [r for r in rows if r["system"] == name and r["kind"] == kind]
            e = {"n": len(sel)}
            for k in ["sisdr", "stoi", "ace_electro_corr", "voc_estoi", "ncm_simple"]:
                e[k] = float(np.nanmean([r[k] for r in sel]))
                e[f"d_{k}"] = bootstrap_ci([r[k] - base[r["crop"]][k] for r in sel])
            summary[name][kind] = e
    Path(a.out).write_text(json.dumps({"meta": {"bench": "v2", "n_per_cell": a.n_per_cell,
                                                 "gen15": a.gen15, "candidate": a.candidate_name},
                                        "summary": summary, "rows": rows}, indent=1))
    for name, byk in summary.items():
        for kind in ["crowd", "competing"]:
            if kind in byk:
                e = byk[kind]
                print(f"{name:18s} {kind:10s} dSI-SDR {e['d_sisdr']['mean']:+.2f} "
                      f"dSTOI {e['d_stoi']['mean']:+.3f} dACEel {e['d_ace_electro_corr']['mean']:+.3f} "
                      f"dVocESTOI {e['d_voc_estoi']['mean']:+.3f} dNCM {e['d_ncm_simple']['mean']:+.3f}")
    print(f"BENCH V2 DONE {time.time()-t0:.0f}s -> {a.out}")


if __name__ == "__main__":
    main()
