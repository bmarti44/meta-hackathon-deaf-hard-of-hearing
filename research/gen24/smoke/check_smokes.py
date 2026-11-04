"""Re-check Gen24 pre-registration smoke evidence (MPS, 2026-11-04 ~17:41-17:44, run while Gen23 trained).
Commands (each killed after step 200):
  train13.py --loss sisdr --snr legacy --mode scratch --seed 20261117 --diag-every 50 --state-every 100000 -> legacy_parity.log
  train13.py --loss sisdr --snr hard60 --mode scratch --seed 20261117 --diag-every 50 --state-every 100000 -> hard60_a.log, hard60_b.log"""
import ast, json
from pathlib import Path

H = Path(__file__).resolve().parent
rec = lambda n: [ast.literal_eval(l) for l in (H / n).read_text().splitlines() if l.startswith("{'step'")]  # noqa: E731
strip = lambda r: {k: v for k, v in r.items() if k != "elapsed_s"}  # noqa: E731
g19 = {r["step"]: r for r in json.loads((H.parents[1] / "gen19/weights/train_log_seed20261117.json").read_text())["log"]}
p = rec("legacy_parity.log")
print("legacy vs Gen19 mismatches:", [r["step"] for r in p if (r["neg_sisdr_loss_db"], r["grad_norm"]) != (g19[r["step"]]["neg_sisdr_loss_db"], g19[r["step"]]["grad_norm"])], f"(steps {p[0]['step']}-{p[-1]['step']})")
a, b = rec("hard60_a.log"), rec("hard60_b.log")
n = min(len(a), len(b))
print(f"hard60 repeat bit-identical over {n} logged steps:", [strip(x) for x in a[:n]] == [strip(x) for x in b[:n]])
print("hard60 differs from legacy (loss at step 25):", a[1]["neg_sisdr_loss_db"], "vs", p[1]["neg_sisdr_loss_db"])
