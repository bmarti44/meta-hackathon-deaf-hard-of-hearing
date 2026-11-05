#!/bin/bash
# Gen26 screen (screen v2) for one seed: build midpoint -> artifact check -> panel v2 (control vs cand) -> bench v2 (safeguards)
# -> judge_v2. PIPELINE DONE means "evaluated"; read screen_v2_s<S>.json verdict before any replication.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=${1:-17}; SEED=$((20261100 + S)); L=/tmp/gen26_s${S}_pipeline.log; G=research/gen26; CK=$G/weights/mid50_seed$SEED.pt
[ -e $G/panel_v2_s$S.json ] && { echo "REFUSED: outputs exist" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/interp.py --seed $S >> $L 2>&1 || { echo "BUILD FAILED $(date)" >> $L; exit 1; }
$PY $G/verify_g26.py --seed $S >> $L 2>&1 || { echo "ARTIFACT FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/panel_v2.py --system control=research/gen19/weights/causal_seed$SEED.pt --system mid50=$CK --out $G/panel_v2_s$S.json >> $L 2>&1 || { echo "PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g26mid50s$S --out research/bench-n6/benchv2_g26mid50s$S.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/judge_v2.py --panel $G/panel_v2_s$S.json --bench research/bench-n6/benchv2_g26mid50s$S.json --cand mid50 --cand-sha $(shasum -a 256 $CK | cut -d' ' -f1) --seed $S --out $G/screen_v2_s$S.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
