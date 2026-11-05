#!/bin/bash
# Gen27 seed-17 screen: train aug50 (24k scratch) -> reverberant panel -> dry screen-v2 panel -> bench v2 ->
# spatial (candidate; control = registered self-test file) -> judge_v3. Each step gated on its exit status.
# PIPELINE DONE means "evaluated", not "advanced": read screen_s17.json's verdict before any replication.
# Never substitute an interim checkpoint (registration).
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=17; SEED=20261117; L=/tmp/gen27_s17_pipeline.log; G=research/gen27
CK=$G/weights/aug50_seed$SEED.pt; ST=$G/weights/aug50_seed${SEED}_state_latest.pt; C19=research/gen19/weights/causal_seed$SEED.pt
[ -e $G/screen_s17.json ] && { echo "REFUSED: screen exists" >> $L; exit 1; }
echo "train start $(date)" >> $L
if [ -f "$ST" ]; then RES="--resume $ST"; else RES=""; fi
$PY $G/train14.py --loss sisdr --snr legacy --room aug50 --mode scratch --seed $SEED --out $CK --log $G/weights/train_log_aug50_seed$SEED.json $RES >> /tmp/gen27_aug50_s17.log 2>&1 || { echo "TRAIN FAILED $(date)" >> $L; exit 1; }
echo "train DONE $(date)" >> $L
$PY $G/panel_rev.py --system control=$C19 --system aug50=$CK --out $G/panel_rev_s17.json >> $L 2>&1 || { echo "REV PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/panel_v2.py --system control=$C19 --system aug50=$CK --out $G/panel_v2_s17.json >> $L 2>&1 || { echo "DRY PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g27aug50s17 --out research/bench-n6/benchv2_g27aug50s17.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_v3.py --run-spatial $CK --name aug50 --out $G/spatial_aug50_s17.json >> $L 2>&1 || { echo "SPATIAL FAILED $(date)" >> $L; exit 1; }
$PY $G/judge_v3.py --rev $G/panel_rev_s17.json --panel $G/panel_v2_s17.json --bench research/bench-n6/benchv2_g27aug50s17.json \
  --spatial-cand $G/spatial_aug50_s17.json --spatial-ctrl $G/selftest/spatial_gen19_s17.json \
  --cand aug50 --cand-sha $(shasum -a 256 $CK | cut -d' ' -f1) --seed $S --out $G/screen_s17.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
