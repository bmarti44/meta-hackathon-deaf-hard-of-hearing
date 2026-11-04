# Astra xhigh interim review of Gen 19 — disposition (2026-11-03)

Holder requested review of interim results. Verdict: **continue
to 24k unchanged.** Real local plateau (6k→8k nearly flat), but
low-LR phase untested; stopping at 12k would be a truncated
screen, not the registered experiment. Diagnostic thresholds
(operational, not statistical): flat window = crowd mean change
<0.15 dB and <0.003 STOI with no SNR row ≥0.30 dB/0.005;
material learning = ≥0.30 dB or ≥0.005 STOI persisting across
two evals and both target speakers. 48k only if 18k→24k
improves both SI-SDR and STOI materially.

Step order kept: k-distribution → compressed spectral loss →
SNR schedule → STOI auxiliary (STOI earlier only if hard-row
SI-SDR gains arrive with STOI still negative).

Panel caveats recorded: 2 target speakers (8 mixtures/SNR);
k counts draws with replacement (~4.6–5.3 distinct voices);
SNR rows use different content (within-row checkpoint
comparisons are paired, across-row are confounded); VAL
interferers overlap Gen 17's train pool (asymmetric Gen 17
comparisons), disjoint from Gen 18/19.

## Gen 18 finals on this VAL panel (requested reference)

| VAL ΔSI-SDR | −5 dB | 0 dB | +5 dB |
|---|---|---|---|
| Gen 18 seeds 17/18/19 | +0.07/+0.05/+0.15 | +3.11/+3.25/+3.33 | +3.62/+3.78/+3.77 |
| Gen 19 @ step 8000 | −0.28 | +3.12 | +3.59 |

Gen 19 at one-third budget (LR still 7.75e-4) already matches
Gen 18 finals at 0/+5 dB; −5 dB is stuck near zero in both.
Whether LR decay adds anything is exactly what 12k/18k/24k
will show, judged by the thresholds above.
