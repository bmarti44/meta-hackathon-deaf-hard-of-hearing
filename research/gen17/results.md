# Gen 17 — data scale works: crowd babble +2.82 dB, ACE KPI first pass (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-03.
> Gen 15 architecture + loss unchanged. Changes vs Gen 15: 26 train
> speakers (bench-v2 prereg), babble k~U{2..12}, SNR weighted to
> −5..+5 dB, 6000 steps, MPS (726 s wall). Seed 20261117 (1 of 3;
> seeds 2–3 + matched 10-speaker control complete the design).
> Final checkpoint scored (frozen rule); interims diagnostic.
> T0 only, no listener claim. `promoted FALSE`.

## KPI scorecard (bench v2, crowd, n=24/kind) — 9 PASS / 3 FAIL

| KPI | Actual | Required | Verdict |
|---|---|---|---|
| Crowd ΔSI-SDR | +2.82 dB | ≥ +3.0 | FAIL (near) |
| Crowd ΔSTOI | +0.017 | ≥ +0.03 | FAIL |
| Crowd ΔACE electro-corr | +0.058 | ≥ +0.05, CI>0 | **PASS (first ever)** |
| Crowd ΔSI-SDR @ −5 dB | +0.99 | ≥ +1.5 | FAIL |
| Crowd ΔSI-SDR @ 0 dB | +4.08 | ≥ +1.5 | PASS (stretch) |
| SSN ΔSI-SDR | +5.31 | ≥ +3.0 | PASS (stretch) |
| Quiet abs SI-SDR / ΔSTOI | 31.0 / −0.006 | ≥25 / ≥−0.02 | PASS (stretch) |
| Target-ILD err / ITD err | 5.54 < 5.96 / 4.2 ≤ 5.8 | beat unproc | PASS |

Vocoded ESTOI (crowd) +0.038, band-env Pearson +0.039 — the
intelligibility proxies finally move with SI-SDR on crowd.
Competing talkers unchanged (+0.81 dB, proxies flat), and legacy
bench babble +1.03 dB ≈ Gen 15's +1.07 — as the target-ambiguity
diagnosis predicted, data scale does not fix competing talkers.

## Trajectory (crowd ΔSI-SDR, v2)

Gen 15 final +1.75 → Gen 17 step2000 +1.96 (n=8 interim) →
Gen 17 final +2.82. Data scale + steps is the first lever that
moved every crowd proxy together.

## Matched control (10 speakers, same seed/settings/steps)

Crowd ΔSI-SDR **+2.54 dB** (ΔSTOI +0.013, ΔACEel +0.056,
ΔvocESTOI +0.026) vs 26-speaker **+2.82 dB**. At this one seed,
speaker count 10→26 accounts for ≈ +0.28 dB of the gain over
Gen 15 (+1.75); the larger share came from the changed training
recipe (6000 steps, crowd-size k, hard-SNR weighting) — those
were changed together, so their individual shares are not
identified. Competing: control +0.64 ≈ 26-spk +0.81.

## Seed-mean verdict (3 seeds × {26spk, 10spk control}, bench v2)

Seed variance is small (crowd ΔSI-SDR spread ≤0.18 dB).

| Crowd (seed-mean) | 26 speakers | 10-spk control | KPI |
|---|---|---|---|
| ΔSI-SDR | +2.73 [2.82/2.64/2.72] | +2.47 [2.54/2.41/2.46] | ≥+3.0 FAIL |
| ΔSTOI | +0.016 | +0.010 | ≥+0.03 FAIL |
| ΔACE electro-corr | +0.056 | +0.053 | ≥+0.05 PASS |
| Δvocoded ESTOI | +0.036 | +0.023 | (supporting) |
| White ΔSI-SDR | +0.25 | **−0.74** | ≥0 |

Speaker diversity 10→26 is worth +0.26 dB crowd and +0.99 dB on
held-out white noise (control *fails* white no-harm) — small on
the headline, real on generalization. The bigger Gen15→Gen17
gain came from steps/recipe (changed together, shares not
identified). Competing talkers: 26spk +0.85 vs control +0.59,
proxies flat in both — still a cue problem, not a data problem
at this scale. Overall KPI verdict remains **FAIL** (crowd
magnitude, STOI, −5 dB row), closest any generation has come.

## Next

Astra xhigh review (standing rule), then Gen 18: train-clean-100
(251 speakers, downloading) and/or CI-domain loss per review.
