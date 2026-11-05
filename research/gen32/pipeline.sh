#!/bin/bash
# Gen32 seed-17: Gen31's WiSE-FT procedure with ONE change, a dry-output-preservation term in the fine-tune
# (--preserve-dry 100 vs a frozen Gen19 teacher). Fine-tune (8k, aug50, Gen19's 24k handoff) -> Gen31's blend.py
# (a=0.1..1.0, unchanged) -> the same test-clean VAL panel and prefix rule (val_testclean2.py keeps per-item scores)
# -> if a candidate exists: reverberant panel -> dry screen-v2 panel -> bench v2 -> spatial -> judge_v3 vs same-seed Gen19.
# Exit 3 from the VAL step = NO CANDIDATE: Gen32 is filed as FAIL and no screen material is touched.
# PIPELINE DONE means "evaluated", not "advanced". Never substitute an interim checkpoint (registration).
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; S=17; SEED=20261117; L=/tmp/gen32_s17_pipeline.log; G=research/gen32; G27=research/gen27
C19=research/gen19/weights/causal_seed$SEED.pt; HO=research/gen21/weights/rng_handoff_seed$SEED.pt
FT=$G/weights/ftpd100_aug50_seed$SEED.pt; ST=$G/weights/ftpd100_aug50_seed${SEED}_state_latest.pt; CK=$G/weights/wiseftpd_seed$SEED.pt
# Registered prerequisite: Gen32 runs only after Gen31 selected no candidate.
G31=$($PY -c "import json;d=json.load(open('research/gen31/val_selection_s17.json'));print('NONE' if d['alpha_star'] is None else d['alpha_star'])" 2>/dev/null)
[ "$G31" = "NONE" ] || { echo "REFUSED: Gen31 alpha* is '$G31', not NONE $(date)" >> $L; exit 1; }
[ -e $G/screen_s17.json ] && { echo "REFUSED: screen exists" >> $L; exit 1; }
[ -e $G/val_selection_s17.json ] && { echo "REFUSED: VAL selection exists" >> $L; exit 1; }
echo "finetune start $(date)" >> $L
if [ ! -f "$FT" ]; then
  if [ -f "$ST" ]; then RES="--resume $ST"; else RES=""; fi
  $PY $G/train19.py --loss sisdr --snr legacy --room aug50 --mode finetune --init-from $C19 --rng-handoff $HO --steps 8000 \
    --preserve-dry 100 --seed $SEED --out $FT --log $G/weights/train_log_ftpd100_aug50_seed$SEED.json $RES >> /tmp/gen32_ft_s17.log 2>&1 || { echo "FINETUNE FAILED $(date)" >> $L; exit 1; }
fi
echo "finetune DONE $(date)" >> $L
$PY research/gen31/blend.py --base $C19 --ft $FT --outdir $G/weights/blends >> $L 2>&1 || { echo "BLEND FAILED $(date)" >> $L; exit 1; }
$PY $G/val_testclean2.py --base $C19 --index $G/weights/blends/index.json --candidate $CK --out $G/val_selection_s17.json >> $L 2>&1
rc=$?
if [ $rc -eq 3 ]; then echo "NO CANDIDATE: Gen32 FAIL (no screen run) $(date)" >> $L; echo "PIPELINE DONE $(date)" >> $L; exit 0; fi
[ $rc -ne 0 ] && { echo "VAL FAILED $(date)" >> $L; exit 1; }
$PY $G27/panel_rev.py --system control=$C19 --system wiseftpd=$CK --out $G/panel_rev_s17.json >> $L 2>&1 || { echo "REV PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/screen_v2/panel_v2.py --system control=$C19 --system wiseftpd=$CK --out $G/panel_v2_s17.json >> $L 2>&1 || { echo "DRY PANEL FAILED $(date)" >> $L; exit 1; }
$PY research/bench-n6/bench_v2.py --n-per-cell 6 --gen15 $CK --candidate-name g32wiseftpds17 --out research/bench-n6/benchv2_g32wiseftpds17.json >> $L 2>&1 || { echo "BENCH FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --run-spatial $CK --name wiseftpd --out $G/spatial_wiseftpd_s17.json >> $L 2>&1 || { echo "SPATIAL FAILED $(date)" >> $L; exit 1; }
$PY $G27/judge_v3.py --rev $G/panel_rev_s17.json --panel $G/panel_v2_s17.json --bench research/bench-n6/benchv2_g32wiseftpds17.json \
  --spatial-cand $G/spatial_wiseftpd_s17.json --spatial-ctrl $G27/selftest/spatial_gen19_s17.json \
  --cand wiseftpd --cand-sha $(shasum -a 256 $CK | cut -d' ' -f1) --seed $S --out $G/screen_s17.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
