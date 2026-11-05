#!/bin/bash
# Gen33 linkage feasibility (no training): frozen Gen32 alpha=0.7 weights processed with ONE shared mask for both ears
# (research/gen33/linked.py), on the registered spatial scenes plus per-ear and target-only measures; decision by
# research/gen33/judge_link.py (Astra's rule). Success = "linkage feasibility passed", never ADVANCE; Gen32 stays FAIL.
set -u
cd "$(dirname "$0")/../.."
PY=/tmp/gen9env/bin/python; L=/tmp/gen33_s17_pipeline.log; G=research/gen33
C19=research/gen19/weights/causal_seed20261117.pt; C32=research/gen32/weights/wiseftpd_seed20261117.pt
[ -e $G/link_s17.json ] && { echo "REFUSED: decision exists" >> $L; exit 1; }
echo "start $(date)" >> $L
$PY $G/spatial_linked.py --ckpt $C19 --mode independent --name gen19 --out $G/spatial_gen19_indep_s17.json >> $L 2>&1 || { echo "G19 FAILED" >> $L; exit 1; }
$PY $G/spatial_linked.py --ckpt $C32 --mode independent --name wiseftpd --out $G/spatial_gen32_indep_s17.json >> $L 2>&1 || { echo "G32 FAILED" >> $L; exit 1; }
$PY $G/spatial_linked.py --ckpt $C32 --mode linked --name wiseftpd_linked --out $G/spatial_gen32_linked_s17.json >> $L 2>&1 || { echo "LINKED FAILED" >> $L; exit 1; }
$PY $G/spatial_linked.py --ckpt $C19 --mode linked --name gen19_linked --out $G/spatial_gen19_linked_s17.json >> $L 2>&1 || { echo "G19 LINKED FAILED" >> $L; exit 1; }
$PY $G/judge_link.py --linked $G/spatial_gen32_linked_s17.json --gen32 $G/spatial_gen32_indep_s17.json \
  --gen19 $G/spatial_gen19_indep_s17.json --gen19-ctrl research/gen27/selftest/spatial_gen19_s17.json \
  --gen19-linked $G/spatial_gen19_linked_s17.json --out $G/link_s17.json >> $L 2>&1 || { echo "JUDGE FAILED $(date)" >> $L; exit 1; }
echo "PIPELINE DONE $(date)" >> $L
