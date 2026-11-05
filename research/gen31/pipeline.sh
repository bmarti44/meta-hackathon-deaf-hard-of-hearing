#!/bin/bash
# Gen31 seed-17 (WiSE-FT): fine-tune Gen19 on the aug50 room mix (8k, lr 1e-4 -> 1e-5, Gen19's own data stream from
# the 24k handoff) -> 10 weight blends a=0.1..1.0 -> test-clean VAL picks alpha* (largest a whose whole prefix shows no
# dry loss vs Gen19) -> if a candidate exists: reverberant panel -> dry screen-v2 panel -> bench v2 -> spatial -> judge_v3.
# Exit 3 from the VAL step = NO CANDIDATE: Gen31 is filed as FAIL and no screen material is touched.
# PIPELINE DONE means "evaluated", not "advanced". Never substitute an interim checkpoint (registration).
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=17; SEED=20261117; L=/tmp/gen31_s17_pipeline.log; G=research/gen31; G27=research/gen27
C19=research/gen19/weights/causal_seed$SEED.pt; HO=research/gen21/weights/rng_handoff_seed$SEED.pt
FT=$G/weights/ft_aug50_seed$SEED.pt; ST=$G/weights/ft_aug50_seed${SEED}_state_latest.pt; CK=$G/weights/wiseft_seed$SEED.pt
# Registered prerequisite (Astra pre-launch note): Gen31 runs only after Gen30's seed-17 screen returned FAIL.
G30V=$($PY -c "import json;print(json.load(open('research/gen30/screen_s17.json'))['verdict'])" 2>/dev/null)
[ "$G30V" = "FAIL" ] || { echo "REFUSED: Gen30 verdict is '$G30V', not FAIL $(date)" >> $L; exit 1; }
[ -e $G/screen_s17.json ] && { echo "REFUSED: screen exists" >> $L; exit 1; }
[ -e $G/val_selection_s17.json ] && { echo "REFUSED: VAL selection exists" >> $L; exit 1; }
echo "finetune start $(date)" >> $L
if [ ! -f "$FT" ]; then
  if [ -f "$ST" ]; then RES="--resume $ST"; else RES=""; fi
  $PY $G/train18.py --loss sisdr --snr legacy --room aug50 --mode finetune --init-from $C19 --rng-handoff $HO --steps 8000 \
    --seed $SEED --out $FT --log $G/weights/train_log_ft_aug50_seed$SEED.json $RES >> /tmp/gen31_ft_s17.log 2>&1 || { echo "FINETUNE FAILED $(date)" >> $L; exit 1; }
fi
echo "finetune DONE $(date)" >> $L
$PY $G/blend.py --base $C19 --ft $FT --outdir $G/weights/blends >> $L 2>&1 || { echo "BLEND FAILED $(date)" >> $L; exit 1; }
$PY $G/val_testclean.py --base $C19 --index $G/weights/blends/index.json --candidate $CK --out $G/val_selection_s17.json >> $L 2>&1
rc=$?
if [ $rc -eq 3 ]; then echo "NO CANDIDATE: Gen31 FAIL (no screen run) $(date)" >> $L; echo "PIPELINE DONE $(date)" >> $L; exit 0; fi
[ $rc -ne 0 ] && { echo "VAL FAILED $(date)" >> $L; exit 1; }
$PY $G27/panel_rev.py --system control=$C19 --system wiseft=$CK --out $G/panel_rev_s17.json >> $L 2>&1 || { echo "REV PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/panel_v2.py --system control=$C19 --system wiseft=$CK --out $G/panel_v2_s17.json >> $L 2>&1 || { echo "DRY PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g31wisefts17 --out research/bench-n6/benchv2_g31wisefts17.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --run-spatial $CK --name wiseft --out $G/spatial_wiseft_s17.json >> $L 2>&1 || { echo "SPATIAL FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --rev $G/panel_rev_s17.json --panel $G/panel_v2_s17.json --bench research/bench-n6/benchv2_g31wisefts17.json \
  --spatial-cand $G/spatial_wiseft_s17.json --spatial-ctrl $G27/selftest/spatial_gen19_s17.json \
  --cand wiseft --cand-sha $(shasum -a 256 $CK | cut -d' ' -f1) --seed $S --out $G/screen_s17.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
