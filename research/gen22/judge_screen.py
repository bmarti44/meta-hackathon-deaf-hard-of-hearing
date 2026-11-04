"""Gen22 screen judgment (prereg.md rules 1-6), 24k-scratch policy.

Candidate: gen22/weights/train_log_cap30_scratch_seed<S>.json (final),
bench `benchv2_g22cap30s<s>.json`, dev panel `gen22/dev_audit_s<s>.json`
(systems `control`, `cap30`). Control: Gen19 final of the same seed
(VAL = its step-0 record in the Gen21 R48 log; bench = Gen19 bench).

Usage: python research/gen22/judge_screen.py --seed 17 [--out f.json]
"""
import argparse, json, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen21"))
from judge_replication import B, PARENT_BENCH, W, bench, val  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--steps", type=int, default=24000)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    seed = 20261100 + a.seed
    CV, _ = val(W / f"train_log_r48_seed{seed}.json", 24000)
    XV, vsha = val(HERE / "weights" / f"train_log_cap30_scratch_seed{seed}.json", a.steps)
    CB, csha = bench(B / PARENT_BENCH[a.seed])
    bpath = B / f"benchv2_g22cap30s{a.seed}.json"
    XB, bsha = bench(bpath)
    assert vsha == bsha, f"VAL/bench hash mismatch {vsha} vs {bsha}"
    bd = json.loads(bpath.read_text())
    s = bd["summary"][bd["meta"]["candidate"]]
    dev = json.loads((HERE / f"dev_audit_s{a.seed}.json").read_text())["summary"]
    dc, dx = dev["control@-5.0"], dev["cap30@-5.0"]
    dev_gain = dx["d_sisdr"] - dc["d_sisdr"]
    tgt = {t: dx["per_target_sisdr"][t] - dc["per_target_sisdr"][t] for t in dc["per_target_sisdr"]}

    g = lambda X, C, snr, i: X[snr][i] - C[snr][i]  # noqa: E731
    rows = {
        "val_gain_m5": (g(XV, CV, -5.0, 0), g(XV, CV, -5.0, 1)),
        "bench_gain_m5": (g(XB, CB, -5.0, 0), g(XB, CB, -5.0, 1)),
        "val_gain_0": (g(XV, CV, 0.0, 0), g(XV, CV, 0.0, 1)),
        "bench_gain_0": (g(XB, CB, 0.0, 0), g(XB, CB, 0.0, 1)),
        "quiet_abs_dstoi": XB["quiet"],
        "crowd": (s["crowd"]["d_sisdr"]["mean"], s["crowd"]["d_stoi"]["mean"], s["crowd"]["d_ace_electro_corr"]["mean"]),
        "ssn": s["ssn"]["d_sisdr"]["mean"], "white": s["white-heldout"]["d_sisdr"]["mean"],
        "dev_gain_m5": dev_gain, "dev_targets_improved": sum(v > 0 for v in tgt.values()),
        "dev_per_target": tgt,
    }
    checks = {
        "1_m5_gain_ge_0.30_both": rows["val_gain_m5"][0] >= 0.30 and rows["bench_gain_m5"][0] >= 0.30,
        "2_m5_stoi_nonworsening_both": rows["val_gain_m5"][1] >= 0 and rows["bench_gain_m5"][1] >= 0,
        "3_zero_db_safeguard": all(rows[k][0] >= -0.15 and rows[k][1] >= -0.003 for k in ("val_gain_0", "bench_gain_0")),
        "4_quiet": rows["quiet_abs_dstoi"][0] >= 25 and rows["quiet_abs_dstoi"][1] >= -0.02,
        "5_other_required_rows": rows["crowd"][0] >= 3.0 and rows["crowd"][1] >= 0.03 and rows["crowd"][2] >= 0.05
                                 and rows["ssn"] >= 3.0 and rows["white"] >= 0,
        "6_dev_panel": dev_gain > 0 and rows["dev_targets_improved"] >= 5,
    }
    verdict = "ADVANCE" if all(checks.values()) else "FAIL"
    print(f"seed {a.seed} candidate {bsha[:12]} control {csha[:12]}")
    print(f"  VAL  -5: cand {XV[-5.0][0]:.4f} ctrl {CV[-5.0][0]:.4f} gain {rows['val_gain_m5'][0]:+.4f} / STOI {rows['val_gain_m5'][1]:+.4f}")
    print(f"  bench-5: cand {XB[-5.0][0]:.4f} ctrl {CB[-5.0][0]:.4f} gain {rows['bench_gain_m5'][0]:+.4f} / STOI {rows['bench_gain_m5'][1]:+.4f}")
    print(f"  0 dB gains VAL {rows['val_gain_0'][0]:+.3f}/{rows['val_gain_0'][1]:+.4f} bench {rows['bench_gain_0'][0]:+.3f}/{rows['bench_gain_0'][1]:+.4f}")
    print(f"  quiet {rows['quiet_abs_dstoi'][0]:.1f} dB / {rows['quiet_abs_dstoi'][1]:+.4f}; crowd {rows['crowd'][0]:+.2f}/{rows['crowd'][1]:+.3f}/{rows['crowd'][2]:+.3f}; SSN {rows['ssn']:+.2f}; white {rows['white']:+.2f}")
    print(f"  dev -5 gain {dev_gain:+.3f}, targets improved {rows['dev_targets_improved']}/8 {({k: round(v, 3) for k, v in tgt.items()})}")
    print(f"  checks {checks}\n  SCREEN {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "rows": rows, "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
