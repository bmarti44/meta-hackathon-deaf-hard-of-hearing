"""Descriptive gradient readout for a Gen22 run (no decision role).
Clipping rate = share of logged steps with pre-clip grad norm > 5 in
the last half of training, vs Gen19's same-seed log; quiet/noisy
gradient-norm ratio from `grad_diag` records (quiet-containing batches).

Usage: python research/gen22/diag_summary.py --seed 17
"""
import argparse, json, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=17); a = ap.parse_args()
seed = 20261100 + a.seed
g22 = json.loads((HERE / "weights" / f"train_log_cap30_scratch_seed{seed}.json").read_text())
g19 = json.loads((HERE.parent / "gen19/weights" / f"train_log_seed{seed}.json").read_text())


def clip_rate(log, steps):
    late = [r for r in log if r["step"] >= steps // 2 and r["step"] % 25 == 0]
    return sum(r["grad_norm"] > 5.0 for r in late) / len(late), len(late)


for name, d in (("gen19 (plain SI-SDR)", g19), ("gen22 cap30", g22)):
    cr, n = clip_rate(d["log"], d["steps"])
    key = "neg_sisdr_uncapped_db" if "neg_sisdr_uncapped_db" in d["log"][-1] else "neg_sisdr_loss_db"
    last = statistics.fmean(r[key] for r in d["log"][-5:])
    print(f"{name}: late-half clipping {cr:.1%} of {n} logged steps; last-5 logged UNCAPPED neg-SI-SDR {last:.2f} dB")
dg = [r for r in g22["log"] if "grad_diag" in r]
for lo, hi in ((0, 8000), (8000, 16000), (16000, 24000)):
    q = [r["grad_diag"]["gn_quiet"] / r["grad_diag"]["gn_noisy"] for r in dg
         if lo <= r["step"] < hi and r["grad_diag"].get("n_quiet", 0) > 0 and r["grad_diag"].get("gn_noisy")]
    print(f"steps {lo}-{hi}: quiet/noisy grad-norm ratio median {statistics.median(q):.2f}x over {len(q)} quiet-containing diag batches" if q else f"steps {lo}-{hi}: no quiet-containing diag batches")
