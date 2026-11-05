#!/bin/bash
# Gen29 seed-17 screen: train aug125 (P(rev|noisy)=0.125) (24k scratch) -> reverberant panel -> dry screen-v2 panel -> bench v2 ->
# spatial (candidate; control = registered self-test file) -> judge_v3. Each step gated on its exit status.
# PIPELINE DONE means "evaluated", not "advanced": read screen_s17.json's verdict before any replication.
# Never substitute an interim checkpoint (registration).
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=17; SEED=20261117; L=/tmp/gen29_s17_pipeline.log; G=research/gen29; G27=research/gen27
CK=$G/weights/aug125_seed$SEED.pt; ST=$G/weights/aug125_seed${SEED}_state_latest.pt; C19=research/gen19/weights/causal_seed$SEED.pt
[ -e $G/screen_s17.json ] && { echo "REFUSED: screen exists" >> $L; exit 1; }
echo "train start $(date)" >> $L
if [ -f "$ST" ]; then RES="--resume $ST"; else RES=""; fi
$PY $G/train16.py --loss sisdr --snr legacy --room aug125 --mode scratch --seed $SEED --out $CK --log $G/weights/train_log_aug125_seed$SEED.json $RES >> /tmp/gen29_aug125_s17.log 2>&1 || { echo "TRAIN FAILED $(date)" >> $L; exit 1; }
echo "train DONE $(date)" >> $L
$PY $G27/panel_rev.py --system control=$C19 --system aug125=$CK --out $G/panel_rev_s17.json >> $L 2>&1 || { echo "REV PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/panel_v2.py --system control=$C19 --system aug125=$CK --out $G/panel_v2_s17.json >> $L 2>&1 || { echo "DRY PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g29aug125s17 --out research/bench-n6/benchv2_g29aug125s17.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --run-spatial $CK --name aug125 --out $G/spatial_aug125_s17.json >> $L 2>&1 || { echo "SPATIAL FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --rev $G/panel_rev_s17.json --panel $G/panel_v2_s17.json --bench research/bench-n6/benchv2_g29aug125s17.json \
  --spatial-cand $G/spatial_aug125_s17.json --spatial-ctrl $G27/selftest/spatial_gen19_s17.json \
  --cand aug125 --cand-sha $(shasum -a 256 $CK | cut -d' ' -f1) --seed $S --out $G/screen_s17.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
