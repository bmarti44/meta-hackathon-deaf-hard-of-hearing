# Muse (Meta) independent review of the Gen 25 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API through the `beforetheimplant-muse` Lambda's direct-invoke `review` mode, 2026-11-04 ~20:53. The prompt was identical to Astra's.

## Verbatim answer

1. FAIL is correct. Arithmetic checks:
`0.7346-0.5641=0.1705~+0.1706; 1.0900-1.0604=+0.0296; dev mean 0.80/8=+0.100, 7/8>0` - all match within rounding.
Gates: `+0.30dB BOTH VAL+bench at -5dB` fails `+0.1706/+0.0296`; `STOI non-worsening BOTH` fails on bench `-0.0010` despite VAL `+0.0005`. Checks 1=False, 2=False therefore SCREEN FAIL is correct. Provenance PASS + VAL parity 6.5e-6dB / 3.2e-8 + hash match `0899593386e1` support reproducibility only.

May: report as training-free exploratory null with descriptive small positives.
May not: claim efficacy, generalizability, or clinical benefit. `dev +0.100 7/8, 0dB +0.092/+0.054, quiet 39.2dB/-0.0030, white +0.29, SSN +6.45` are all below primary magnitude, single seed-17, STOI bench worsened, and do not address seed-mean KPI gap `1.187654 vs 1.5, need +0.312346`.

No retention, no promotion. Do not use average as parent. Baseline/control stays Gen19-final `80000b64c413`. Gen26 parentage stays as planned `Gen19<->Gen21-R48`, unchanged.

2. Yes: build + register larger dev panel FIRST, then run Gen26.
That order prevents tuning-to-dev leakage and moving goalposts. Keep Gen19 scorecard frozen unchanged for comparability.

Spec hardening for Gen26 prereg:
- list 16 training-disjoint IDs x4 crops x4 mixtures + disjointness proof vs train/tuning/VAL/bench; separate tuning material IDs for exponent calibration, no peeking.
- freeze Gen22 gates: +0.30dB BOTH, STOI >=0 BOTH strict, 0dB safeguard, quiet, CI-lo>0, dev >0 and >=5/8 - now >=?/16.
- define Gen26 exactly: checkpoints, alpha=0.5, per-seed then seed-mean, bit-exact recompute + parity guard.
- isolate concurrent Gen24 narrow-SNR training; separate provenance.
Separate prereg for mask-exponent calibration before any mask-head continuation / subpools / distillation.

3. For SUBMISSION.md:
Gen25 tested a training-free uniform average of nine Gen19 checkpoints against Gen19-final on seed 17 and failed pre-registered gates with +0.17 dB VAL and +0.03 dB bench at -5 dB versus +0.30 dB required plus bench STOI -0.0010. The averaged weights are not retained and Gen19-final remains the baseline.
