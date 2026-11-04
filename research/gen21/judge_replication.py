"""Gen 21 replication judgment (prereg.md decision rules), 48k finals only.

VAL panel: unrounded per-item means from train-log val_log
(parent = R48 log at lifetime 24000, i.e. the Gen19 parent before
any restart update). Bench panel: crowd rows of bench v2 JSONs,
paired against `unproc` per (kind, crop, spk, snr). Gains are vs
each seed's own Gen19 parent. Prints a table and writes JSON.

Usage: python research/gen21/judge_replication.py [--seeds 17 18 19] [--out f.json]
"""
import argparse, collections, json, statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = ROOT / "research/gen21/weights"
B = ROOT / "research/bench-n6"
PARENT_BENCH = {17: "bench_v2_gen19.json", 18: "benchv2_gen19s2.json", 19: "benchv2_gen19s3.json"}
SFX = {17: "", 18: "s18", 19: "s19"}


def val(log, lifetime):
    d = json.loads(Path(log).read_text())
    e = [x for x in d["val_log"] if x["lifetime_step"] == lifetime]
    assert len(e) == 1, (log, lifetime)
    by = collections.defaultdict(list)
    for it in e[0]["items"]:
        by[it["snr"]].append((it["d_sisdr"], it["d_stoi"]))
    return {snr: (statistics.fmean(v[0] for v in vs), statistics.fmean(v[1] for v in vs))
            for snr, vs in by.items()}, d.get("weights_sha256")


def bench(path):
    d = json.loads(Path(path).read_text())
    cand = d["meta"]["candidate"]
    base = {(r["kind"], r["crop"], r["spk"], r["snr_db"]): r for r in d["rows"] if r["system"] == "unproc"}
    out = {}
    for snr in (-5.0, 0.0):
        rs = [r for r in d["rows"] if r["system"] == cand and r["kind"] == "crowd" and r["snr_db"] == snr]
        assert len(rs) == 6, (path, snr, len(rs))
        k = lambda r: base[(r["kind"], r["crop"], r["spk"], r["snr_db"])]
        out[snr] = (statistics.fmean(r["sisdr"] - k(r)["sisdr"] for r in rs),
                    statistics.fmean(r["stoi"] - k(r)["stoi"] for r in rs))
    q = d["summary"][cand]["quiet"]
    out["quiet"] = (q["sisdr"], q["d_stoi"]["mean"])
    return out, d["meta"]["checkpoint_sha256"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[17, 18, 19])
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    res = {"seeds": a.seeds, "per_seed": {}, "arms": {}}
    for s in a.seeds:
        seed = 20261100 + s
        P, _ = val(W / f"train_log_r48_seed{seed}.json", 24000)
        PB, psha = bench(B / PARENT_BENCH[s])
        r48_parent = json.loads((W / f"train_log_r48_seed{seed}.json").read_text())["parent_sha256"]
        assert r48_parent == psha, f"seed {s}: R48 parent {r48_parent} != parent bench {psha}"
        row = {"parent_val": P[-5.0], "parent_bench": PB[-5.0], "parent_sha": psha}
        for arm in ("s48", "r48"):
            V, vsha = val(W / f"train_log_{arm}_seed{seed}.json", 48000)
            Bn, bsha = bench(B / f"benchv2_g21{arm}{SFX[s]}_48k.json")
            assert vsha == bsha, f"hash mismatch {arm} seed {s}: VAL {vsha} vs bench {bsha}"
            row[arm] = {
                "sha": bsha,
                "val_m5": V[-5.0], "bench_m5": Bn[-5.0],
                "val_gain_m5": [V[-5.0][i] - P[-5.0][i] for i in (0, 1)],
                "bench_gain_m5": [Bn[-5.0][i] - PB[-5.0][i] for i in (0, 1)],
                "val_gain_0": [V[0.0][i] - P[0.0][i] for i in (0, 1)],
                "bench_gain_0": [Bn[0.0][i] - PB[0.0][i] for i in (0, 1)],
                "bench_quiet": Bn["quiet"],
            }
        res["per_seed"][s] = row
    n = len(a.seeds)
    for arm in ("s48", "r48"):
        rows = [res["per_seed"][s][arm] for s in a.seeds]
        m = lambda key, i: statistics.fmean(r[key][i] for r in rows)
        g = {k: [m(k, 0), m(k, 1)] for k in ("val_gain_m5", "bench_gain_m5", "val_gain_0", "bench_gain_0")}
        pos = {p: sum(r[f"{p}_gain_m5"][0] > 0 for r in rows) for p in ("val", "bench")}
        checks = {
            "mean_gain_m5_ge_0.30_both": g["val_gain_m5"][0] >= 0.30 and g["bench_gain_m5"][0] >= 0.30,
            "mean_stoi_m5_nonworsening_both": g["val_gain_m5"][1] >= 0 and g["bench_gain_m5"][1] >= 0,
            "positive_ge_2of3_both": pos["val"] >= 2 and pos["bench"] >= 2,
            "zero_db_safeguard": all(g[k][0] >= -0.15 and g[k][1] >= -0.003 for k in ("val_gain_0", "bench_gain_0")),
            "quiet_safeguard": all(r["bench_quiet"][0] >= 25 and r["bench_quiet"][1] >= -0.02 for r in rows),
        }
        res["arms"][arm] = {"mean_gains": g, "positive_seeds": pos, "checks": checks,
                            "qualifies": n == 3 and all(checks.values())}
    sr = {p: statistics.fmean(res["per_seed"][s]["s48"][f"{p}_m5"][0] - res["per_seed"][s]["r48"][f"{p}_m5"][0]
                              for s in a.seeds) for p in ("val", "bench")}
    res["s48_minus_r48_m5"] = sr

    for s in a.seeds:
        r = res["per_seed"][s]
        print(f"seed {s}: parent VAL -5 {r['parent_val'][0]:.4f} bench -5 {r['parent_bench'][0]:.4f}")
        for arm in ("s48", "r48"):
            x = r[arm]
            print(f"  {arm} {x['sha'][:12]} VAL-5 {x['val_m5'][0]:.4f} gain {x['val_gain_m5'][0]:+.4f}/{x['val_gain_m5'][1]:+.4f} | "
                  f"bench-5 {x['bench_m5'][0]:.4f} gain {x['bench_gain_m5'][0]:+.4f}/{x['bench_gain_m5'][1]:+.4f} | "
                  f"0dB VAL {x['val_gain_0'][0]:+.3f} bench {x['bench_gain_0'][0]:+.3f} | quiet {x['bench_quiet'][0]:.1f}/{x['bench_quiet'][1]:+.4f}")
    for arm, v in res["arms"].items():
        g = v["mean_gains"]
        print(f"{arm.upper()} mean gain -5: VAL {g['val_gain_m5'][0]:+.4f} (STOI {g['val_gain_m5'][1]:+.4f}) "
              f"bench {g['bench_gain_m5'][0]:+.4f} (STOI {g['bench_gain_m5'][1]:+.4f}); positive VAL {v['positive_seeds']['val']}/{n} "
              f"bench {v['positive_seeds']['bench']}/{n}; checks {v['checks']}; QUALIFIES={v['qualifies']}")
    print(f"S48-R48 @-5 seed-mean: VAL {sr['val']:+.4f} bench {sr['bench']:+.4f} (scratch preferred only if both >= 0.15)")
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
