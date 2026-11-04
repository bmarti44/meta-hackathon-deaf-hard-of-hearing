"""Gen23 screen judgment: Gen22's registered rules 1-6 verbatim
(research/gen22/judge_screen.py `judge`), candidate = `sisdr_cs5`
24k scratch, control = Gen19 final of the same seed.

Files: gen23/weights/train_log_sisdr_cs5_scratch_seed<S>.json (final
entry only), bench-n6/benchv2_g23cs5s<s>.json, gen23/dev_audit_s<s>.json
(dev systems `control`, `cs5`).

Usage: python research/gen23/judge_screen.py --seed 17 [--out f.json]
"""
import argparse, importlib.util, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("judge_screen_g22", HERE.parent / "gen22" / "judge_screen.py")
J22 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(J22)  # unique module name: gen22/gen23 both ship judge_screen.py
B, PARENT_BENCH, W, judge = J22.B, J22.PARENT_BENCH, J22.W, J22.judge

CAND = "cs5"
POLICY = {"mode": "scratch", "loss": "sisdr_cs5", "steps": 24000}


def run(s):
    seed = 20261100 + s
    return judge(W / f"train_log_r48_seed{seed}.json",
                 HERE / "weights" / f"train_log_sisdr_cs5_scratch_seed{seed}.json",
                 B / PARENT_BENCH[s], B / f"benchv2_g23cs5s{s}.json",
                 HERE / f"dev_audit_s{s}.json", seed, cand=CAND, policy=POLICY)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    r, checks, verdict = run(a.seed)
    print(f"seed {a.seed} candidate {r['cand_sha'][:12]} control {r['ctrl_sha'][:12]}")
    print(f"  VAL  -5: cand {r['cand_val_m5'][0]:.4f} ctrl {r['ctrl_val_m5'][0]:.4f} gain {r['val_gain_m5'][0]:+.4f} / STOI {r['val_gain_m5'][1]:+.4f}")
    print(f"  bench-5: cand {r['cand_bench_m5'][0]:.4f} ctrl {r['ctrl_bench_m5'][0]:.4f} gain {r['bench_gain_m5'][0]:+.4f} / STOI {r['bench_gain_m5'][1]:+.4f}")
    print(f"  0 dB gains VAL {r['val_gain_0'][0]:+.3f}/{r['val_gain_0'][1]:+.4f} bench {r['bench_gain_0'][0]:+.3f}/{r['bench_gain_0'][1]:+.4f}")
    print(f"  quiet {r['quiet_abs_dstoi'][0]:.1f} dB / {r['quiet_abs_dstoi'][1]:+.4f}; crowd {r['crowd_mean']} CI-lo {r['crowd_ci_lo']}; SSN {r['ssn']:+.2f}; white {r['white']:+.2f}")
    print(f"  dev -5 gain {r['dev_gain_m5']:+.3f}, targets improved {r['dev_targets_improved']}/8 {({k: round(v, 3) for k, v in r['dev_per_target'].items()})}")
    print(f"  checks {checks}\n  SCREEN {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "rows": r, "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
