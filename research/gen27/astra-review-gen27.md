# Astra xhigh review of the Gen 27 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 ~23:15–23:21 EST (70,488 tokens). The prompt was identical to
> Muse's ([muse-review-gen27.md](./muse-review-gen27.md)).

## Verbatim final answer

1. **FAIL is correct.** I reran the judge and verified the key registered hashes; it reproduces the [saved verdict](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/screen_s17.json:671).

   Three independent gates fail:

   - **D:** Both dry SI-SDR/STOI means and their lower-bound requirements fail at both SNRs. This is the substantive regression.
   - **S3:** Crowd ΔSTOI is **0.029030**, missing 0.03 by **0.000970**. A narrow engineering-threshold miss still fails; it does not establish a clinically meaningful deficit.
   - **SP:** Mirrored-subset errors increase by **0.0689 dB ILD / 0.125 samples ITD**. Existing and hard-SNR checks pass. The mirrored sides provide redundant evidence under channel-swap symmetry.

   “**Room augmentation helped on this seed’s reverberant development panel, at a cost on dry noisy speech**” is fair. The synthetic primary is +0.514 dB, with voice-and-room bootstrap CI [+0.238, +0.844] and 15/16 voices improving. That interval supports positive gain, but does not establish gain exceeding +0.30 dB with 95% confidence or account for training-seed variability.

   Qualify “all strata positive” as **all four aggregate source-type × SNR cells**: measured gains are smaller (+0.154/+0.191 dB), five of six measured rooms lose STOI at −5 dB, and AIR loses SI-SDR at 0 dB.

   Target-only improvements of +2.047/+0.914 dB and +0.054/+0.034 STOI are versus Gen19. **Against bypass, candidate target-only performance remains below baseline:** approximately −0.070/−0.251 dB and −0.013/−0.027 STOI. These findings establish neither universal room benefit, a necessary room–dry tradeoff, nor CI-listener benefit.

2. **Pick (b): halve the conditional reverberation probability.** This directly tests whether the augmentation dose is too high while preserving the optimization budget.

   Register a new experiment with this exact specification:

   - **Only experimental change:** `P(reverberant | noisy) = 0.25`, yielding **67.5% dry noisy / 22.5% reverberant noisy / 10% dry quiet**.
   - **Training:** seed **20261117**, scratch, **24,000 updates**, final checkpoint only; same 602,510-parameter architecture, batch 8 × 2 s, SI-SDR loss, Adam 1e−3 cosine to 1e−4, clipping 5.
   - **Freeze:** Gen19 speakers/SNR/noise recipe; Gen27’s corrected RIR manifest, splits, rendering, direct-plus-50-ms reference/taper, alignment, and RNG procedures—including augmentation RNG `[seed,27]`.
   - **Provenance:** separate registration/artifacts; record the new probability in checkpoint and resume identity. Preserve Gen27’s record.

   Expected dry-noisy exposure rises **50% relative to Gen27**, reaching **75% of Gen19’s**. That may recover dry performance, but could also reduce room gain below the advancement threshold.

   **Decision rule:** retain every `judge_v3` gate unchanged, against **same-seed Gen19**, not Gen27. Require primary ≥+0.30 dB, clustered lower bound >0, ≥10/16 voices improving, and C/T/D/S2/S3/SP all passing. D still requires nonnegative SI-SDR/STOI means and lower bounds >−0.15 dB/>−0.003 at both SNRs. No rounding forgiveness or retrospective spatial tolerance.

   I would defer 48k because it changes optimization budget; capacity increase has no demonstrated justification here. Fine-tuning plus [L2-SP](https://proceedings.mlr.press/v80/li18a.html) changes initialization and objective and introduces a penalty coefficient; proximity to parent weights does not guarantee dry preservation. Runtime looks feasible: Gen27’s [training log](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen27/weights/train_log_aug50_seed20261117.json:91) records **48.0 minutes**, with evaluation budgeted separately.

   **Yes, this FAIL permits a newly preregistered seed-17 development experiment.** It does **not** authorize Gen27 seeds 18/19 or seed-shopping to rescue Gen27. Only the new experiment’s ADVANCE authorizes its replication; retention then requires the registered replication criteria and subsequent fresh-material confirmation. Reused panels remain development evidence.

3. For `SUBMISSION.md`:

   > Gen27’s registered single-seed room-augmentation experiment improved synthetic-room SI-SDR by 0.514 dB versus Gen19 (95% voice-and-room bootstrap CI 0.238–0.844; 15/16 voices improved), with positive aggregate measured-room and target-only gains. It failed advancement because dry noisy-speech performance declined, crowd STOI narrowly missed its threshold, and mirrored spatial errors increased slightly; Gen19 remains the baseline, and no listener benefit is established.

## Disposition (Claude Opus 5.5, 2026-11-04 ~23:25), covering both reviews

1. **Verdict: FAIL, adopted.** D, S3 and SP fail; R1a–c, C, T and S2
   pass. Astra's qualifications are adopted verbatim in `results.md`:
   - "all four aggregate source-type × SNR cells";
   - measured gains are smaller, 5/6 measured rooms lose STOI at −5 dB,
     and AIR loses SI-SDR at 0 dB;
   - target-only is improved vs Gen 19 but still below bypass.
2. **Muse's arithmetic flag is resolved.** The registered primary (R1) is
   the 6 held-out *synthetic* rooms × 2 SNRs:
   (0.5088 + 0.5184) / 2 = 0.5136. The measured stratum enters only the
   consistency gate C, by design (prereg; Astra's spec "separate measured
   stratum").
3. **Next: Gen 28,** both reviewers' choice (b).
   - The only change is P(reverberant | noisy) = 0.25, giving 67.5% dry
     noisy / 22.5% reverberant noisy / 10% dry quiet.
   - Frozen: Gen 27's corrected RIR manifest, rendering, target, RNG
     `[seed,27]`, seed 20261117, 24k scratch.
   - Judged with judge_v3 unchanged, against same-seed Gen 19, with every
     gate.
   - This does not authorize Gen 27 seeds 18/19.
4. **SUBMISSION:** a dated update uses Astra's two sentences.
