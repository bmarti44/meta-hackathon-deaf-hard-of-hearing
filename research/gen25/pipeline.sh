#!/bin/bash
# Gen25 screen for one seed: build swa9 (+VAL) -> bench -> dev -> judge -> Gen25 provenance.
# Each step is gated on its exit status. NOTE (Astra): a scientific FAIL exits 0, so PIPELINE DONE
# means "evaluated", not "advanced"; read screen_s<S>.json verdict before any replication.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=${1:-17}; SEED=$((20261100 + S)); L=/tmp/gen25_s${S}_pipeline.log; G=research/gen25; CK=$G/weights/swa9_seed$SEED.pt
[ -e research/bench-n6/benchv2_g25swa9s$S.json ] && { echo "REFUSED: bench output exists" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/swa.py --seed $S >> $L 2>&1 || { echo "SWA FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g25swa9s$S --out research/bench-n6/benchv2_g25swa9s$S.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY research/gen21/dev_audit.py --system control=research/gen19/weights/causal_seed$SEED.pt --system swa9=$CK --out $G/dev_audit_s$S.json >> $L 2>&1 || { echo "DEV FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_screen.py --seed $S --out $G/screen_s$S.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
$PY $G/verify_provenance_g25.py --gen 25 --seed $S >> $L 2>&1 || { echo "PROVENANCE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
