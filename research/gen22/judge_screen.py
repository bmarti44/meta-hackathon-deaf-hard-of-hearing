"""Gen22 screen judgment (prereg.md rules 1-7), 24k-scratch policy ONLY.

Candidate: gen22/weights/train_log_cap30_scratch_seed<S>.json (FINAL
entry only), bench `benchv2_g22cap30s<s>.json`, dev panel
`gen22/dev_audit_s<s>.json` (systems `control`, `cap30`). Control:
Gen19 final of the same seed (VAL = its step-0 record in the Gen21 R48
log, whose parent_sha256 must equal the Gen19 bench hash).
Provenance is enforced (Astra pre-launch review item 4): candidate
hash identical across VAL log / bench / dev rows, control hash
identical across R48 parent / Gen19 bench / dev rows, exact 8-target
dev panel with 16 paired items per target per SNR.

Usage: python research/gen22/judge_screen.py --seed 17 [--out f.json]
"""
import argparse, collections, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen21"))
from judge_replication import B, PARENT_BENCH, W, bench  # noqa: E402

DEV_TARGETS = {"5536", "5694", "1988", "1993", "5895", "6241", "6295", "6313"}
DEV_GRID = {(t, c, m, s) for t in DEV_TARGETS for c in range(4) for m in range(4) for s in (-5.0, 0.0)}
POLICY = {"mode": "scratch", "loss": "cap30", "steps": 24000}


class Invalid(Exception):
    pass


def _need(cond, msg):
    if not cond:
        raise Invalid(msg)


def _val_entry(log, lifetime):
    e = [x for x in log["val_log"] if x["lifetime_step"] == lifetime]
    _need(len(e) == 1, f"no unique VAL entry at lifetime {lifetime}")
    by = collections.defaultdict(list)
    for it in e[0]["items"]:
        by[it["snr"]].append((it["d_sisdr"], it["d_stoi"]))
    return {snr: (statistics.fmean(v[0] for v in vs), statistics.fmean(v[1] for v in vs)) for snr, vs in by.items()}


def _dev(rows, ctrl_sha, cand_sha):
    sys_rows = {"control": [r for r in rows if r["system"] == "control"],
                "cap30": [r for r in rows if r["system"] == "cap30"]}
    for name, sha in (("control", ctrl_sha), ("cap30", cand_sha)):
        shas = {r["sha256"] for r in sys_rows[name]}
        _need(shas == {sha}, f"dev {name} hash {shas} != {sha}")
    key = lambda r: (r["spk"], r["crop"], r["mix"], r["snr"])  # noqa: E731
    for name, rs in sys_rows.items():  # full registered grid, duplicate-free (Astra Gen21-final review)
        keys = [key(r) for r in rs]
        _need(len(keys) == len(set(keys)), f"dev {name} has duplicate items")
        _need(set(keys) == DEV_GRID, f"dev {name} grid != 8 targets x 4 crops x 4 mixtures x 2 SNRs "
                                     f"(missing {len(DEV_GRID - set(keys))}, extra {len(set(keys) - DEV_GRID)})")
    c = {key(r): r for r in sys_rows["control"] if r["snr"] == -5.0}
    x = {key(r): r for r in sys_rows["cap30"] if r["snr"] == -5.0}
    tgt = {t: statistics.fmean(x[k]["d_sisdr"] - c[k]["d_sisdr"] for k in c if k[0] == t) for t in sorted(DEV_TARGETS)}
    return statistics.fmean(x[k]["d_sisdr"] - c[k]["d_sisdr"] for k in c), tgt


def judge(ctrl_log_p, cand_log_p, ctrl_bench_p, cand_bench_p, dev_p, seed):
    ctrl_log = json.loads(Path(ctrl_log_p).read_text())
    cand_log = json.loads(Path(cand_log_p).read_text())
    _need(cand_log.get("seed") == seed and ctrl_log.get("seed") == seed,
          f"seed identity: candidate {cand_log.get('seed')}, control {ctrl_log.get('seed')}, registered {seed}")
    for k, v in POLICY.items():
        _need(cand_log.get(k) == v, f"candidate log {k}={cand_log.get(k)} != registered {v}")
    _need(cand_log.get("lifetime_steps") == POLICY["steps"], "candidate log is not a 24k final")
    CB, csha = bench(ctrl_bench_p)
    XB, bsha = bench(cand_bench_p)
    _need(ctrl_log.get("parent_sha256") == csha, f"control VAL parent {ctrl_log.get('parent_sha256')} != control bench {csha}")
    _need(cand_log.get("weights_sha256") == bsha, f"candidate final {cand_log.get('weights_sha256')} != bench {bsha}")
    CV = _val_entry(ctrl_log, 24000)  # R48 step 0 = Gen19 parent before any update
    XV = _val_entry(cand_log, cand_log["lifetime_steps"])
    bd = json.loads(Path(cand_bench_p).read_text())
    s = bd["summary"][bd["meta"]["candidate"]]
    dev_gain, tgt = _dev(json.loads(Path(dev_p).read_text())["rows"], csha, bsha)

    g = lambda X, C, snr, i: X[snr][i] - C[snr][i]  # noqa: E731
    cr = s["crowd"]
    rows = {
        "val_gain_m5": (g(XV, CV, -5.0, 0), g(XV, CV, -5.0, 1)),
        "bench_gain_m5": (g(XB, CB, -5.0, 0), g(XB, CB, -5.0, 1)),
        "val_gain_0": (g(XV, CV, 0.0, 0), g(XV, CV, 0.0, 1)),
        "bench_gain_0": (g(XB, CB, 0.0, 0), g(XB, CB, 0.0, 1)),
        "cand_val_m5": XV[-5.0], "ctrl_val_m5": CV[-5.0], "cand_bench_m5": XB[-5.0], "ctrl_bench_m5": CB[-5.0],
        "quiet_abs_dstoi": XB["quiet"],
        "crowd_mean": (cr["d_sisdr"]["mean"], cr["d_stoi"]["mean"], cr["d_ace_electro_corr"]["mean"]),
        "crowd_ci_lo": (cr["d_sisdr"]["ci_lo"], cr["d_stoi"]["ci_lo"], cr["d_ace_electro_corr"]["ci_lo"]),
        "ssn": s["ssn"]["d_sisdr"]["mean"], "white": s["white-heldout"]["d_sisdr"]["mean"],
        "dev_gain_m5": dev_gain, "dev_targets_improved": sum(v > 0 for v in tgt.values()), "dev_per_target": tgt,
        "cand_sha": bsha, "ctrl_sha": csha,
    }
    m, lo = rows["crowd_mean"], rows["crowd_ci_lo"]
    checks = {
        "1_m5_gain_ge_0.30_both": rows["val_gain_m5"][0] >= 0.30 and rows["bench_gain_m5"][0] >= 0.30,
        "2_m5_stoi_nonworsening_both": rows["val_gain_m5"][1] >= 0 and rows["bench_gain_m5"][1] >= 0,
        "3_zero_db_safeguard": all(rows[k][0] >= -0.15 and rows[k][1] >= -0.003 for k in ("val_gain_0", "bench_gain_0")),
        "4_quiet": rows["quiet_abs_dstoi"][0] >= 25 and rows["quiet_abs_dstoi"][1] >= -0.02,
        "5_other_required_rows": m[0] >= 3.0 and m[1] >= 0.03 and m[2] >= 0.05 and all(x > 0 for x in lo)
                                 and rows["ssn"] >= 3.0 and rows["white"] >= 0,
        "6_dev_panel": dev_gain > 0 and rows["dev_targets_improved"] >= 5,
    }
    return rows, checks, ("ADVANCE" if all(checks.values()) else "FAIL")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    seed = 20261100 + a.seed
    rows, checks, verdict = judge(W / f"train_log_r48_seed{seed}.json",
                                  HERE / "weights" / f"train_log_cap30_scratch_seed{seed}.json",
                                  B / PARENT_BENCH[a.seed], B / f"benchv2_g22cap30s{a.seed}.json",
                                  HERE / f"dev_audit_s{a.seed}.json", seed)
    r = rows
    print(f"seed {a.seed} candidate {r['cand_sha'][:12]} control {r['ctrl_sha'][:12]}")
    print(f"  VAL  -5: cand {r['cand_val_m5'][0]:.4f} ctrl {r['ctrl_val_m5'][0]:.4f} gain {r['val_gain_m5'][0]:+.4f} / STOI {r['val_gain_m5'][1]:+.4f}")
    print(f"  bench-5: cand {r['cand_bench_m5'][0]:.4f} ctrl {r['ctrl_bench_m5'][0]:.4f} gain {r['bench_gain_m5'][0]:+.4f} / STOI {r['bench_gain_m5'][1]:+.4f}")
    print(f"  0 dB gains VAL {r['val_gain_0'][0]:+.3f}/{r['val_gain_0'][1]:+.4f} bench {r['bench_gain_0'][0]:+.3f}/{r['bench_gain_0'][1]:+.4f}")
    print(f"  quiet {r['quiet_abs_dstoi'][0]:.1f} dB / {r['quiet_abs_dstoi'][1]:+.4f}; crowd {r['crowd_mean']} CI-lo {r['crowd_ci_lo']}; SSN {r['ssn']:+.2f}; white {r['white']:+.2f}")
    print(f"  dev -5 gain {r['dev_gain_m5']:+.3f}, targets improved {r['dev_targets_improved']}/8 {({k: round(v, 3) for k, v in r['dev_per_target'].items()})}")
    print(f"  checks {checks}\n  SCREEN {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "rows": rows, "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
