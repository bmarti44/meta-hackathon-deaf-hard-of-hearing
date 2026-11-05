"""Gen34 runner: build the recorded panel once, run bypass, Gen19 (twice, for the duplicate-baseline check) and Gen32,
and write every row plus a descriptive summary. judge_recorded_v1.py then decides VALID ASSET / INVALID from integrity
checks only; model scores never decide whether the asset is accepted.

Usage: python research/gen34/run_audit.py --out research/gen34/audit_s17.json
"""
from __future__ import annotations
import argparse, hashlib, json, statistics, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recorded_panel as P  # noqa: E402

REPO = HERE.parent.parent
CK = {"gen19": REPO / "research/gen19/weights/causal_seed20261117.pt",
      "gen32": REPO / "research/gen32/weights/wiseftpd_seed20261117.pt"}


def summarize(rows):
    by = {}
    for r in rows:
        by.setdefault(r["system"], {})[(r["talker"], r["setting"], r["az"], r["snr"])] = r
    out = {}
    def m(xs): return statistics.fmean(xs)
    for cand, ref in (("gen19", "bypass"), ("gen32", "bypass"), ("gen32", "gen19")):
        for s in P.SETTINGS:
            for snr in P.SNRS + (None,):
                ks = [k for k in by[cand] if k[1] == s and k[3] == snr]
                d = {}
                for met in ("sisdr", "stoi", "wave_err"):
                    dl = [by[cand][k][f"{met}_L"] - by[ref][k][f"{met}_L"] for k in ks]
                    dr = [by[cand][k][f"{met}_R"] - by[ref][k][f"{met}_R"] for k in ks]
                    worse = max if met == "wave_err" else min   # waveform error: higher is worse
                    d[met] = m(dl + dr); d[f"{met}_left_ear"] = m(dl); d[f"{met}_right_ear"] = m(dr)
                    d[f"{met}_worst_ear"] = m(worse(a, b) for a, b in zip(dl, dr))
                for met in ("ild_target_err_db", "ild_mixture_dist_db", "itd_err_samples"):
                    d[met] = m(by[cand][k][met] - by[ref][k][met] for k in ks)
                out[f"{cand}-{ref}|{s}|{'target_only' if snr is None else f'{snr:+.0f}'}"] = d
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    t0 = time.time()
    items, mh, meta = P.build()
    print(f"items={len(items)} material_sha256={mh} {time.time()-t0:.0f}s", flush=True)
    rows = P.run_system(items, "bypass")
    for name in ("gen19", "gen19_repeat", "gen32"):
        ck = CK["gen32" if name == "gen32" else "gen19"]
        rows += P.run_system(items, name, ck)
        print(f"{name} done {time.time()-t0:.0f}s", flush=True)
    doc = {"panel": "gen34_brudex_recorded_v1", "material_sha256": mh, "n_items": len(items), "meta": meta,
           "checkpoints": {k: {"path": str(v.relative_to(REPO)), "sha256": hashlib.sha256(v.read_bytes()).hexdigest()} for k, v in CK.items()},
           "rows": rows, "summary_descriptive": summarize([r for r in rows if r["system"] != "gen19_repeat"])}
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(f"WROTE {a.out} {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
