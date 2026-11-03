# KPI targets — "working really well" defined in numbers

> Holder direction 2026-11-03: get training cleaned up and shoot
> for concrete KPI targets. Holder-set ambition (same day): **no
> ceiling** — push as far as laptop-scale training (~1–2 h/run)
> allows, keep optimizing data and recipe generation over
> generation. **Speech understanding and directional hearing are
> co-equal goals**, not a trade-off. Required rows below are
> therefore *milestones that earn a listening test*, not stopping
> points; optimization continues past them toward the oracle.
> These are T0 bench targets on Gen 13-identical held-out crops
> (full size: 32/condition), not listener claims.
> Baselines: Gen 15 final (bench run 2 / its own full eval).

**KPI split (2026-11-03, per REVIEW.md §7 holder delegation):**
the legacy eval babble (k=3 from 2 interferer voices) is a
*competing-talker* test — at −5 dB each interferer is ≈ as loud
as the target, so single-mic models have no target cue. The
babble KPIs below apply to **crowd babble** (≥8 talkers, many
held-out voices; bench v2, Phase 0) for single-mic models, and
to competing talkers only for binaural/personalized models.
Legacy rows keep being reported side by side; nothing is
silently redefined. Verified Phase 0 facts: 40 dev-clean
speakers now extracted (was 14); MPS training verified
0.117 s/step synchronised vs 3.73 CPU in the same harness
(~32×; data generation becomes the bottleneck).

## Primary — crowd babble, held-out talkers (the hard problem)

| KPI | Required | Stretch | Gen 15 | Oracle ceiling |
|---|---|---|---|---|
| ΔSI-SDR (dB), 95% CI lo > 0 | ≥ +3.0 | ≥ +5.0 | +1.07 | +10.9 |
| ΔSTOI, CI lo > 0 | ≥ +0.03 | ≥ +0.06 | −0.016 | +0.28 |
| ΔACE electro-corr (post 8-of-22), CI lo > 0 | ≥ +0.05 | ≥ +0.10 | +0.011 | +0.34 |
| ΔSI-SDR at −5 dB and 0 dB SNR | ≥ +1.5 each | ≥ +3.0 each | ≈0 / +0.4 | — |
| Babble SI-SDR > classical gate | yes | yes | yes | — |

Rationale: +3 dB is roughly a third of the oracle headroom and
the lower end of improvements reported for lab DNN systems in CI
listeners (1.4–6.4 dB SRT, different metric — used for scale
only). The per-SNR row exists because Gen 15's gain sat only at
easy SNRs; help is needed most at −5/0 dB.

## No-harm — other conditions

| KPI | Required | Stretch | Gen 15 |
|---|---|---|---|
| SSN ΔSI-SDR | ≥ +3.0 | ≥ +5.0 | +4.3 |
| Held-out white ΔSI-SDR | ≥ 0 | ≥ +1.5 | +0.84 |
| Quiet absolute SI-SDR | ≥ 25 dB | ≥ 30 dB | 26.1 (bench) |
| Quiet ΔSTOI | ≥ −0.02 | ≥ −0.01 | −0.009 |
| Quiet PESQ (own-eval readout) | ≥ 4.0 | ≥ 4.3 | 3.11 ✗ |

## Spatial — direction cues (Stage B2, co-primary)

| KPI | Required | Stretch | Gen 15 |
|---|---|---|---|
| Target-ILD error vs clean target | < unprocessed on same scenes | ≥ 30% below unprocessed | 5.42 vs 5.96 |
| ITD error vs target | ≤ unprocessed on same scenes | < unprocessed | pass |
| ILD distortion vs mixture | diagnostic only (perfect recovery scores 5.96 — must not gate) | — | 0.95 |
| Architecture (binaural phase) | linked bilateral gains (common mask/gain both ears) | — | per-ear ✗ |

## Robustness and engineering

| KPI | Required |
|---|---|
| Seeds | 3; every seed babble ΔSI-SDR > 0; KPIs judged on seed-mean |
| Causality | exact suffix invariance (max prefix Δ = 0.0) on final weights |
| Algorithmic latency | ≤ 10 ms excluding compute (Gen 15: 5.88 ms) |
| Streaming RTF | measured < 1.0 on CPU (frame-by-frame), reported |
| Size | ≤ 1M parameters (Gen 15: 602,510) |
| Safety | all human-listenable files peak ≤ 0.889 via limiter |

## Training cleanup rules (from Gen 15/16 lessons)

1. One canonical trainer per generation; smoke runs write to a
   distinct `--out` (a 10-step smoke overwrote Gen 16's final
   filename once — now guarded).
2. Fixed step budget, all interim checkpoints benched and
   reported — no cherry-picking the best checkpoint after the fact.
3. Loss terms logged separately every 25 steps.
4. Eval is one command (`bench.py --n-per-cell 8`) + spatial bench;
   KPI verdict printed by `kpi_scorecard.py`, never eyeballed.
5. Speaker/noise holdouts asserted in code (existing tests).
6. **Astra review between generations** (holder standing rule,
   2026-11-03): Codex `gpt-6-astra` at xhigh reviews each
   generation's filed results + bench contract before the next
   generation trains; disposition filed beside this file.
7. Data optimization (holder direction, within laptop scale):
   expand training speakers beyond the current 10 from the same
   corpus (holdouts unchanged), weight training SNRs toward the
   hard −5/0 dB region where Gen 15 had no gain, vary babble
   talker counts. Each change one generation at a time, benched.

Scorecard: `/tmp/gen9env/bin/python research/bench-n6/kpi_scorecard.py
--bench <bench_results.json> --spatial <spatial_results.json>`.
