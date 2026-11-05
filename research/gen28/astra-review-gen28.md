# Astra xhigh review of the Gen 28 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~00:07–00:12 EST (60,066 tokens). The prompt was identical to
> Muse's ([muse-review-gen28.md](./muse-review-gen28.md)).

## Verbatim final answer

1. **FAIL is correct.** I reran `judge_v3`; the report and checks match the saved result. The “GEN27 SCREEN” text is a hard-coded label in the reused judge.

   - **D fails independently:** both SI-SDR and STOI means are negative at both SNRs, and all four lower bounds breach their registered margins. This is more than an inconclusive safeguard.
   - **SP fails only on mirrored ITD:** existing and hard-SNR checks pass; mirrored ILD improves.
   - R1/C/T/S2/S3 pass. Target-only improvement is relative to Gen19; aggregate target-only SI-SDR and STOI remain below bypass.

   Halving the dose retained **89.4% of the synthetic-room gain**, while reducing dry SI-SDR penalties by **49.6%/35.6%** at −5/0 dB. That supports further dose exploration on this seed and development panel. It does not establish a general dose-response curve, an unavoidable tradeoff, or a dose with zero dry cost; the voice-and-room bootstrap does not capture training-seed variability.

   I verified the ITD change: **crop 1, 0 dB, target ±30°, error 0→1 sample**, once per eight-scene directional subset. The [estimator](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/spatial.py:57) selects integer correlation lags; one sample is 62.5 μs at 16 kHz. The two mirrored failures duplicate the same evidence. Report **“a one-bin ITD-error increase, producing +0.125 samples in the subset mean; perceptual significance undetermined.”** Discretisation can amplify a small peak shift, but these results cannot establish that the change is purely an artefact. Keep SP=FAIL; any fractional-lag diagnostic should be explicitly exploratory.

2. **Pick (a): P(reverberant | noisy)=0.125.** The first halving preserved substantial room gain while improving dry scores, making another halving the clearest next single-factor experiment—not a prediction of passing.

   Exact specification: **78.75% dry noisy / 11.25% reverberant noisy / 10% dry quiet**, seed **20261117**, scratch, **24,000 updates**, final checkpoint only. Freeze the 602,510-parameter architecture, batch 8×2 s, SI-SDR loss, Adam 1e−3 cosine to 1e−4, clipping 5, speakers/SNR/noise recipe, corrected RIR manifest and splits, early target/taper/alignment, and augmentation RNG `[seed,27]`. Register the new mode and its checkpoint/resume identity before training. Gen28’s logged training time was **37.2 minutes**, so this is plausible within the budget including evaluation.

   Retain **every judge_v3 gate against same-seed Gen19**: primary ≥0.30 dB, voice+room lower bound >0, ≥10/16 improved voices, and C/T/D/S2/S3/SP all true. D still requires nonnegative means and lower bounds >−0.15 dB/>−0.003 at both SNRs; SP gets no tolerance. Only ADVANCE authorizes seeds 18/19; subsequent confirmation needs fresh material.

   Defer short fine-tuning because it changes initialization and update budget; adding [L2-SP](https://proceedings.mlr.press/v80/li18a.html) also changes the objective. A 48k run tests training duration rather than completing this dose comparison.

3. Suggested two sentences:

   > Gen28 halved the room-augmentation probability and improved synthetic-room SI-SDR by 0.459 dB versus Gen19 in one training seed, while reducing but not eliminating the dry-speech losses seen in Gen27. It failed the registered dry-preservation and spatial ITD gates despite passing the other checks; Gen19 remains the baseline, and no listener benefit is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~00:15), covering both reviews

1. **FAIL adopted.** D fails independently, and SP fails only on mirrored
   ITD. The ITD miss is reported in Astra's wording: "a one-bin ITD-error
   increase, producing +0.125 samples in the subset mean; perceptual
   significance undetermined". The cause is crop 1, 0 dB, target ±30°,
   error 0 → 1 sample. SP stays FAIL, with no tolerance.
2. **The "GEN27 SCREEN" label** in the judge output is a hard-coded string
   in the reused judge_v3, not an error in the run.
3. **Dose result, this seed and panel only:**
   - halving the dose kept 89.4% of the room gain and cut the dry SI-SDR
     penalties by 49.6% / 35.6%;
   - this establishes no general curve and no zero-cost dose.
4. **Next: Gen 29,** both reviewers' choice (a), P(reverberant | noisy) =
   0.125 → 78.75 / 11.25 / 10, with everything else frozen and the same
   gates vs Gen 19.
   - Muse's stopping rule is adopted: if the room gain falls below
     +0.30, stop cutting the dose and change the approach.
5. **SUBMISSION:** a dated update uses Astra's two sentences.
