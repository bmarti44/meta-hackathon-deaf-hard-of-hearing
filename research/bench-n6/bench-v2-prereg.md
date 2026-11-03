# Bench v2 pre-registration (2026-11-03, before any v2 scoring)

Per REVIEW.md §2 (holder-delegated KPI split, §7). Legacy bench
(`bench.py`) stays byte-identical and keeps being reported.

## Speaker splits (LibriSpeech dev-clean, all 40; disjoint, asserted)

- TRAIN (Gen 17+, 26): 84 174 251 422 652 777 1272 1462 1673 1919
  (legacy 10) + 2035 2078 2086 2277 2412 2428 2803 2902 3000 3081
  3170 3536 3576 3752 3853 5338
- VAL targets (checkpoint decisions only, 2): 5536 5694
- TEST targets (6): 1988 1993 (legacy continuity) + 5895 6241 6295 6313
- TEST interferers (eval babble only, 6): 8297 8842 + 6319 6345 7850 7976

## Conditions (4 s crops, SNR −5/0/+5/+10 dB, RNG 20261117)

- `crowd`: babble k~U{8..12} draws from TEST interferers. KPI babble
  rows apply here for single-mic models.
- `competing`: babble k=2 from TEST interferers. Reported; KPI rows
  apply only to binaural/personalized models.
- `ssn`, `white-heldout`, `quiet`: as legacy bench.

## Metrics (per crop, paired vs unprocessed)

Legacy SI-SDR / STOI / ACE env + post-selection correlations, plus
on 8-of-22 vocoded output (same vocoder seed clean vs estimate):
**vocoded ESTOI** (pystoi extended) and **simplified NCM**
(per-ACE-band normalized envelope covariance, uniform weights —
labeled simplified, not the full Chen & Loizou weighting).
Proxies are supporting evidence only (REVIEW §2.3).

## Amendments (2026-11-03, Astra xhigh review — recorded, not silent)

1. "Simplified NCM" renamed **band-env Pearson**: it is mean
   per-band envelope correlation on raw waveforms, not NCM and
   not on vocoded output; it inherits no published validation.
   Vocoded ESTOI remains as registered.
2. Speaker cycling fixed to a global counter (per-cell restart
   meant the first filed v2 run at n=2 tested only speakers
   1988/1993). Balanced runs use n-per-cell a multiple of 6.
   The first v2 baseline is superseded by the balanced re-run.
3. Spatial gate corrected (PROTOCOL Stage B2): ILD *distortion
   vs the mixture* is diagnostic only — perfect target recovery
   would "fail" it. The gate is target-ILD error vs clean.

## Rules

- No model is selected or tuned on TEST; VAL targets exist for
  checkpoint decisions when needed. Fixed budgets preferred.
- KPI.md Required thresholds are unchanged; they are read against
  `crowd` for single-mic candidates. Legacy bench results remain
  in every report next to v2.
