#!/bin/bash
# Gen36 output-contract repair audit (no training). Needs /tmp/gen36_release (published HF files), /tmp/gen36dl (test-other),
# /tmp/brudex_dl/data (Gen34 asset) and the dev-clean data used by screen v2.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; L=/tmp/gen36_pipeline.log; G=research/gen36
[ -e $G/contract_decision.json ] && { echo "REFUSED: decision exists" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/run_contract.py --out $G/contract_rows.json >> $L 2>&1 || { echo "RUN FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_contract.py --rows $G/contract_rows.json --out $G/contract_decision.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
