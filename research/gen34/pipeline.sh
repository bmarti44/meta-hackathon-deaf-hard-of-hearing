#!/bin/bash
# Gen34 frozen real-recording audit (evaluation asset; no training, no selection, no model advancement).
# Requires the BRUDEX subset fetched by research/gen34/fetch_brudex.py into /tmp/brudex_dl/data (48 speech files:
# SPK1-4 x low/medium/high x DOA -60/-30/30/60, eMicRun 1; 3 babble files, eMicRun 1) and /tmp/brudex_dl/LICENSE.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; L=/tmp/gen34_pipeline.log; G=research/gen34
[ -e $G/asset_verdict_v1.json ] && { echo "REFUSED: verdict exists" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/run_audit.py --out $G/audit_s17.json >> $L 2>&1 || { echo "AUDIT FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_recorded_v1.py --audit $G/audit_s17.json --out $G/asset_verdict_v1.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
