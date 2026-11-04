# Gen 18 — data scale at matched compute is neutral (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-03.
> Sole change vs Gen 17: training pool = LibriSpeech
> train-clean-100 (251 speakers, 28,539 files, CC BY 4.0;
> archive SHA-256 d4ddd1d5…bf6e2, 6,387,309,499 bytes; verified
> disjoint from all v2 TEST/VAL/interferer speakers). Frozen:
> architecture, neg-SI-SDR loss, mixtures, 6000 steps, 3 seeds
> (20261117/18/19), final-checkpoint rule, MPS (~25 min/seed).
> T0 only, no listener claim. `promoted FALSE`.

## Seed-mean KPI verdict (bench v2 crowd) — FAIL, tied with Gen 17

| Crowd (seed-mean) | Gen 18 (251 spk) | Gen 17 (26 spk) | KPI |
|---|---|---|---|
| ΔSI-SDR | +2.73 [2.68/2.77/2.74] | +2.73 | ≥+3.0 FAIL |
| ΔSTOI | +0.015 | +0.016 | ≥+0.03 FAIL |
| ΔACE electro-corr | +0.053 | +0.056 | ≥+0.05 PASS |
| ΔSI-SDR @ −5 dB | +0.63 | +0.80 | ≥+1.5 FAIL |
| Δvocoded ESTOI | +0.037 | +0.036 | supporting |

9 PASS / 3 FAIL on the scorecard (complete evidence: 3 seed
benches + hash-matched spatial). White seed-mean +0.60 (better
than Gen 17's +0.25; control was −0.74) — pool diversity still
protects unseen-noise generalization. Competing talkers +0.78
mean, proxies flat, unchanged.

**Reading:** at a fixed 6000-step budget the model consumes
≈26.7 h of target crops regardless of pool size, so 10× voices
cannot express themselves. Data scale *alone, at matched
compute* is neutral on the headline KPIs. The binding failures
(crowd magnitude, STOI, −5 dB) now point at training length /
capacity or the objective — ranked by Astra review next,
before Gen 19.
