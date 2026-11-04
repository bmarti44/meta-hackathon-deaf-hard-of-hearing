"""Re-check the Gen22 pre-launch parity evidence from the retained logs:
`--loss sisdr` run (steps 0-325) and its `--resume` from the step-300
state (steps 300-425) vs Gen19 seed-17's logged loss and grad-norm.
Commands that produced the logs (MPS, 2026-11-04 ~13:03-13:07):
  train11.py --loss sisdr --mode scratch --seed 20261117 --state-every 100 --out <tmp>/a.pt  (killed after step 325)
  train11.py ... same ... --resume <tmp>/a_state_latest.pt                                     (killed after step 425)
  train11.py --loss cap30 --mode scratch --seed 20261117 --diag-every 50 --out <tmp>/c.pt     (killed after step 200)
(the pre-fix trainer revision 5a7b927; the later resume-identity fix does not touch the update path)."""
import ast, json
from pathlib import Path

H = Path(__file__).resolve().parent
g19 = {r["step"]: r for r in json.loads((H.parents[1] / "gen19/weights/train_log_seed20261117.json").read_text())["log"]}
for name in ("sisdr_parity_run.log", "sisdr_resume_from300.log", "sisdr_parity_postfix.log"):
    recs = [ast.literal_eval(l) for l in (H / name).read_text().splitlines() if l.startswith("{'step'")]
    bad = [r["step"] for r in recs if (r["neg_sisdr_loss_db"], r["grad_norm"]) != (g19[r["step"]]["neg_sisdr_loss_db"], g19[r["step"]]["grad_norm"])]
    print(f"{name}: steps {recs[0]['step']}-{recs[-1]['step']} ({len(recs)} logged) mismatches={bad}")
