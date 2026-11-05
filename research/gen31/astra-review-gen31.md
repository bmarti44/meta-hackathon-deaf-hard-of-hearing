# Astra xhigh review of the Gen 31 result — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~02:02–02:10 EST (81,763 tokens).
> - The prompt was identical to Muse's ([muse-review-gen31.md](./muse-review-gen31.md)), apart from the closing note to Muse about file access and length.

## Verbatim final answer

1. **NO CANDIDATE → FAIL is correct.** The checked source hashes match the registration, the selection JSON records no candidate, and the pipeline log stops before screening. The exact −5 dB STOI delta at α=0.1 is −0.0000305446; rounding does not explain the failure.

The curve shows a small, metric-dependent dry tradeoff for this seed and panel. Every sampled nonzero blend fails at least one endpoint, so removing the prefix requirement would not rescue it. It establishes neither an unavoidable tradeoff nor population-level harm, equivalence, room benefit, or CI-user benefit. No room evaluation occurred.

Correct [results.md:41](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen31/results.md:41): replace “far below anything a listener could notice” with **“numerically small; its perceptual significance is unknown.”** Also distinguish **selection failure** from failure of judge_v3, which never ran.

2. **The statistical concern is valid, but I would not introduce positive margins for Gen32 under your requested evidence standard.**

For four independent, symmetric, nondegenerate estimates centered at zero, all four means pass with probability 1/16. Here the endpoints—and adjacent blends—are correlated, so that probability is illustrative only. Exact waveform preservation is different: paired deltas are identically zero and pass. Increasing sample size does not cure the sign requirement at an exactly zero population mean with nonzero sampling variance.

I cannot justify exact positive SI-SDR/STOI margins as CI perceptual non-inferiority limits:

- Fixed-waveform metrics are essentially deterministic. Sampling uncertainty belongs in confidence intervals; it does not itself establish an acceptable loss.
- Acoustic SNR JNDs cannot simply be transferred to SI-SDR, and ΔSTOI is not a percentage-point intelligibility change. Research on reverberant CI simulations documents distortion-dependent prediction errors, including misleading improvements from over-attenuation. [Shahidi et al., 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10959555/)
- The existing **0.15 dB / 0.003** bounds predate Gen27, but I found no independent perceptual or repeatability calibration supporting those particular values. They are engineering tolerances, not demonstrated inaudibility thresholds.

A future calibrated NI design should require each paired, voice-clustered lower confidence bound to exceed its independently justified negative margin. Align VAL selection with that objective; changing only one gate leaves the other bottleneck. Register the new version before new candidate results, retain old D as secondary, preserve all historical verdicts, and keep calibration material separate from fresh confirmation.

Under current D, reliable success needs **positive dry headroom**, or exact Gen19 outputs on protected inputs through a validated deployable mechanism. Soft distillation only encourages preservation. Gen32 can plausibly succeed because dry supervision can improve performance while anchoring limits drift; it cannot guarantee success.

3. **Choose (a): one Gen32 output-preservation experiment, with unchanged selection and judgment.** It directly tests the proposed mechanism within the available budget.

| Component | Exact specification |
|---|---|
| Initialization | Student and frozen teacher from registered Gen19 seed **20261117**; committed 24k RNG handoff. |
| Training | **8,000 updates**, batch **8 × 2 s**, fresh Adam **1e−4 cosine→1e−5**, clipping **5**, final checkpoint only. |
| Data | Unchanged aug50 **45/45/10**, training RIR split, augmentation RNG, speakers/noises/SNRs, early target and delay. |
| Objective | Existing SI-SDR loss on every item, plus the drafted normalized waveform penalty with **COEF=100**, averaged over dry noisy and dry quiet items. Detached teacher; raw identically delayed outputs; zero penalty when no dry items. |
| Selection | α ∈ **{0.1,…,1.0}**; largest whole prefix with all four paired dry means **≥0**. α=0.1 failure means **NO CANDIDATE → FAIL**, no screen. |
| Judgment | Screen the selected blend once with unchanged **judge_v3**: R1a ≥0.30 dB, R1b lower bound >0, R1c ≥10/16 voices, and C/T/D/S2/S3/SP all pass. |
| Stopping | No coefficient, checkpoint, or grid rescue. ADVANCE authorizes replication and fresh confirmation only. |

**100 is a fixed experimental coefficient, not a preservation guarantee.** Budget approximately 25–40 minutes including evaluation, pending timing of the teacher pass. Deployment remains one 602k-parameter model.

I reran the four tests that require no file writes: **4 passed**; I did not rerun the writing smoke test. Before registration, record `preserve_dry` in exported checkpoint metadata—it currently appears in logs/resume state—and retain per-item VAL scores for descriptive clustered intervals. Reused VAL is now development material; leave the 24 reserved voices untouched.

For the real-user objective, report measured-room results individually and quiet/target-only results against bypass. Preserving Gen19’s behavior does not establish preservation of what users hear well today.

4. Suggested two sentences:

> Gen31 fine-tuned Gen19 on room-augmented speech and tested ten weight blends, but selected no candidate because the first blend reduced mean −5 dB dry STOI by 0.00003, failing the registered zero-loss rule. Gen31 therefore failed before screening; Gen19 remains the baseline, and neither room benefit nor benefit for cochlear-implant users was established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~02:20), covering both reviews

1. **NO CANDIDATE → FAIL is adopted.** This was a selection failure: judge_v3 never ran. Astra's wording correction is adopted in results.md: the −0.00003 STOI miss is "numerically small; its perceptual significance is unknown."
2. **Margins (question 2): no change.** The reviewers split:
   - Muse proposed prospective non-inferiority margins (−0.10 dB SI-SDR, −0.005 STOI) as a new judge_v4.
   - Astra found no a-priori basis for any specific margin as a CI perceptual limit. ΔSTOI and SI-SDR deltas do not map to intelligibility JNDs, and the existing 0.15 dB / 0.003 bounds are engineering tolerances.
   - Adopted: the zero-margin D and the VAL rule stay. Changing them after five near-misses would look like goalpost-moving. It would also weaken the owner's standard of "without hurting anything they hear well today."
   - Muse's proposal is recorded as an open design question. Any future change must be registered before new results, keep the current D as a reported secondary, and never re-score Gen 27–31.
3. **Next (question 3): Gen 32 = Astra's (a)**, Gen 31's procedure plus `--preserve-dry 100`. Muse objected that 100 is uncalibrated. That is answered without touching VAL or screen material, by a scale check on training batches only (`research/gen32/calibrate_coef.py` → `coef_calibration.json`):
   - The unpenalised Gen 31 fine-tune drifts r = 0.0061 (median 0.0044) on dry training items.
   - At COEF 100 that drift would cost 0.61 loss units, roughly 0.6 dB of the SI-SDR objective (mean −SI-SDR -10.1 dB).
   - That is the same order as the main loss changes: neither negligible nor dominating. **COEF stays fixed at 100.**
   - Muse's 3-coefficient sweep with joint dry/room selection is not adopted. It needs three trainings and a new room VAL panel, and the manifest has no held-out rooms left outside the screen.
   - Astra's two pre-registration items are adopted: `preserve_dry` goes into checkpoint metadata, and per-item VAL scores are kept for descriptive clustered intervals. The Gen 31 VAL panel is now development material; the 24 reserved voices stay untouched.
4. **Muse's first answer was empty.** At effort high the reply came back empty (the output budget was presumably consumed). It was re-run once at effort medium with the identical prompt; both are filed.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
