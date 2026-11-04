"""Re-check Gen23 pre-launch smoke evidence from the retained logs (MPS, 2026-11-04 ~17:25-17:35).
Commands (each killed after step 200):
  train12.py --loss sisdr     --mode scratch --seed 20261117 --diag-every 50 --state-every 100000   -> sisdr_parity.log
  train12.py --loss sisdr_cs5 --mode scratch --seed 20261117 --diag-every 50 --state-every 100000   -> cs5_a.log, cs5_b.log
  train12.py --loss sisdr_cs5 --mode scratch --seed 20261117 --diag-every 0  --state-every 100000   -> cs5_nodiag.log"""
import ast, json
from pathlib import Path

H = Path(__file__).resolve().parent
rec = lambda n: [ast.literal_eval(l) for l in (H / n).read_text().splitlines() if l.startswith("{'step'")]  # noqa: E731
strip = lambda r, drop=("elapsed_s",): {k: v for k, v in r.items() if k not in drop}  # noqa: E731
g19 = {r["step"]: r for r in json.loads((H.parents[1] / "gen19/weights/train_log_seed20261117.json").read_text())["log"]}
p = rec("sisdr_parity.log")
print("sisdr vs Gen19 mismatches:", [r["step"] for r in p if (r["neg_sisdr_loss_db"], r["grad_norm"]) != (g19[r["step"]]["neg_sisdr_loss_db"], g19[r["step"]]["grad_norm"])], f"(steps {p[0]['step']}-{p[-1]['step']})")
a, b, c = rec("cs5_a.log"), rec("cs5_b.log"), rec("cs5_nodiag.log")
print("cs5 repeat bit-identical:", [strip(x) for x in a] == [strip(x) for x in b[:len(a)]])
print("cs5 diag-on vs off identical updates:", [strip(x, ("elapsed_s", "grad_diag")) for x in a] == [strip(x, ("elapsed_s", "grad_diag")) for x in c[:len(a)]])
print("gn_cs5 > 0 at every diag step:", all(r["grad_diag"]["gn_cs5"] > 0 for r in a if "grad_diag" in r))
