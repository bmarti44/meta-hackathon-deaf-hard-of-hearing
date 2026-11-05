#!/bin/bash
# Gen35 frozen output-path repair audit (no training, no selection). Requires the Gen34 BRUDEX subset in /tmp/brudex_dl/data.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; L=/tmp/gen35_pipeline.log; G=research/gen35
[ -e $G/repair_decision.json ] && { echo "REFUSED: decision exists" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/run_repair.py --out $G/repair_rows.json >> $L 2>&1 || { echo "RUN FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_repair.py --rows $G/repair_rows.json --out $G/repair_decision.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
