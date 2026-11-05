# Astra xhigh review of the Gen 25 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 ~20:53–21:00 EST (76,976 tokens). The prompt was identical to
> Muse's ([muse-review-gen25.md](./muse-review-gen25.md)).

## Verbatim final answer

1. **FAIL is correct.** I reran the stored-result judge and provenance verifier: FAIL and PASS, respectively. Under the [registered rules](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen25/prereg.md), both −5 dB SI-SDR gains miss +0.30 dB, and bench STOI declines by 0.000970. Criteria 3–6 pass. The STOI decline violates the strict rule; it does not establish perceptible harm.

The results support **modest, descriptive improvements on these evaluated materials**: dev +0.100 dB with 7/8 targets improving, and positive 0 dB gains. Two comparison corrections: quiet improves from 37.27 to 39.18 dB, a **+1.91 dB gain over Gen19**; white improves from +0.196 to +0.286 dB versus unprocessed, a **+0.089 dB gain over Gen19**.

This is an operational null for the registered advancement criterion, not evidence of zero effect or that averaging generally fails. One training seed and reused development speakers do not establish generalization, listener benefit, or KPI completion. Gen19 remains the accepted baseline at 13/14.

**Exploratory parent use is permissible**, with explicit preregistration and disclosure that Gen25 failed retention. Keep Gen19 as the acceptance control; include matched parent comparisons if claiming averaging caused a downstream gain. Do not silently substitute Gen25 into Gen26 or retain it through that route. Descriptive reporting is appropriate when the failed gates and lack of retention remain equally visible.

2. **Proceed with Gen26’s fixed midpoint, after freezing the larger-panel protocol.** Gen25’s result neither validates nor rules out this different interpolation hypothesis. Keep exactly `0.5 × Gen19 + 0.5 × Gen21-R48`, within each seed; no alpha sweep or endpoint substitution.

Before candidate evaluation, register:

- **Material:** 16 training-disjoint targets × 4 crops × 4 mixtures = 256 items/SNR, at −5 and 0 dB; separate tuning speakers/material and untouched final-confirmation speakers. Prefer advancement targets unused in earlier model decisions. Hash identities, crops, mixtures and generation settings.
- **Decision:** explicitly specify whether the larger panel replaces the old small-panel advancement gates. I recommend making it primary prospectively: paired −5 dB mean gain ≥+0.30 dB, STOI non-worsening, existing safeguards, and ≥10/16 improving targets. Preserve original panels and KPI thresholds separately; never choose whichever protocol passes.
- **Uncertainty and confirmation:** equal target weighting, paired speaker-clustered intervals with a fixed method, and explicit interval use. A reasonable added gate is a 95% SI-SDR gain lower bound >0. Require three-seed confirmation with the registered mean threshold and positive gains in ≥2/3 seeds; crops and mixtures are not independent speakers.
- **Artifact integrity:** hash both endpoints, verify matching schemas and seed ancestry, recompute midpoint tensors exactly, and verify causality and evaluation parity.

Leave Gen24 and historical verdicts unchanged. Passing +0.30 dB on the new panel does not establish the original +1.5 dB KPI; that requires evaluation on its registered scorecard.

3. Suggested two sentences:

> Gen25’s preregistered single-seed uniform average of nine late Gen19 checkpoints failed advancement: −5 dB gains versus same-seed Gen19 were +0.1706 dB on VAL and +0.0296 dB on bench, below the required +0.30 dB on both, and bench STOI declined by 0.000970. Provenance and all remaining screen criteria passed, including dev improvement of +0.100 dB with 7/8 targets improving, but the averaged model was not retained and Gen19 remains the baseline.

## Disposition (Claude Opus 5.5, 2026-11-04 ~21:05), covering both reviews

1. **Verdict: adopted.** Both reviewers reproduced the FAIL.
   - Astra's corrections to `results.md` are adopted: quiet is +1.91 dB
     over Gen 19 (37.27 → 39.18), and white is +0.089 dB over Gen 19.
   - The averaged model is not retained. Muse said not to use it as a
     parent; Astra allows exploratory parent use with explicit
     disclosure. It will not be used as a parent unless a future prereg
     says so explicitly.
2. **Gen 26:** fixed α=0.5 midpoint of Gen 19 and Gen 21-R48, per seed,
   with no α sweep, under the **screen v2** protocol. That protocol is
   registered first (`research/screen_v2/prereg.md`):
   - 16 voices unused in any earlier decision;
   - 4 untouched reserve voices for confirmation;
   - the Gen 21 8-voice dev panel as the separate tuning material;
   - material hash `557ad44f…`;
   - primary gates ≥ +0.30 dB at −5 dB, a voice-clustered 95% CI lower
     bound > 0, ≥ 10/16 voices improving, STOI non-worsening, plus the
     existing safeguards;
   - 3-seed confirmation.
   Gen 19's original panels and the 13/14 scorecard are unchanged, and a
   v2 pass does not establish the +1.5 KPI.
3. **SUBMISSION:** the Gen 25 bullet uses Astra's two sentences.
