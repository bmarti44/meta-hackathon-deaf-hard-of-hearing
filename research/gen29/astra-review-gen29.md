# Astra xhigh review of the Gen 29 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~00:57–01:00 EST (58,026 tokens). The prompt was identical to
> Muse's ([muse-review-gen29.md](./muse-review-gen29.md)).

## Verbatim final answer

1. **FAIL is correct.** I reran `judge_v3`: the saved verdict and checks reproduce, and trainer, judge, and checkpoint hashes match. “GEN27 SCREEN” is a hard-coded label in the reused judge.

- **D fails at both SNRs.** All four means are negative. At −5 dB, the SI-SDR lower bound passes its margin, but STOI’s does not; at 0 dB, both lower bounds fail.
- **SP fails on mirrored ILD and ITD.** Existing and hard-SNR checks pass. The ITD difference is one scene changing from 0 to 1 sample error per eight-scene directional subset; the mirrored sides duplicate the same evidence. Small magnitude does not override the registered rule, and perceptual significance is undetermined.
- **R1/C/T/S2/S3 pass.** The +0.370 dB primary is **synthetic-room** gain. Measured-room aggregate gains are smaller, and four measured rooms have negative STOI changes at −5 dB. Target-only improvement is relative to Gen19; aggregate target-only SI-SDR and STOI remain below unprocessed.

The **0 dB dry SI-SDR loss is the clearest persistent constraint**, with CI [−0.169, −0.083] dB, but it is not the sole blocker: −5 dB STOI and mirrored spatial preservation also need fixing.

The three points show a descriptive tradeoff on this seed and reused development material: less augmentation accompanies smaller synthetic-room gains and smaller dry SI-SDR penalties. They establish neither a general dose-response curve nor an unavoidable tradeoff; measured-room gains are relatively flat and SP is not monotonic. The bootstrap excludes training-seed variability, and these are not three independent replications. **The registered taper-stopping condition has not triggered: 0.3695 ≥ 0.30.**

2. **Pick (a): P=0.0625, as one final, prospectively bounded dose-only experiment.**

The last halving recovered approximately 0.191 dB at dry 0 dB while losing 0.090 dB of primary room gain. That warrants one more isolated test, although the remaining 0.070 dB room headroom is narrow and passing cannot be predicted.

Exact specification:

- **84.375% dry noisy / 5.625% reverberant noisy / 10% dry quiet.**
- Seed **20261117**, scratch, **24,000 updates**, final checkpoint only.
- Freeze Gen29’s architecture, SI-SDR loss, batch 8×2 s, Adam 1e−3 cosine→1e−4, clipping 5, speakers/SNR/noise recipe, corrected RIR manifest and splits, per-source rendering, early target/taper/alignment, and RNG streams.
- Fix P before training; no parameter search or checkpoint selection. Gen29’s 36.7-minute training makes approximately one hour including evaluation plausible.

Use **unchanged judge_v3 against same-seed Gen19**: R1a ≥0.30, R1b lower bound >0, R1c ≥10/16, and every C/T/D/S2/S3/SP gate true. No tolerance or rounding forgiveness. ADVANCE authorizes seeds 18/19, followed by fresh-material confirmation.

I would additionally preregister: **any failure ends this dose-only campaign**, even if R1a passes. That is a proposed new boundary, not the existing stopping rule.

L2-SP and WiSE-FT remain reasonable subsequent hypotheses, but the proposed versions combine initialization with anchoring or interpolation. Their published evidence concerns vision models, not CI enhancement. ([L2-SP](https://arxiv.org/abs/1802.01483), [WiSE-FT](https://arxiv.org/abs/2109.01903)) Preserving today’s performance remains a measured requirement; none of these methods guarantees it.

3. Suggested two sentences:

> Gen29 reduced room augmentation to one quarter of Gen27’s dose and improved synthetic-room SI-SDR by 0.370 dB versus Gen19 in one training seed (95% voice-and-room bootstrap CI 0.163–0.627), while reducing but not eliminating dry-speech losses. It failed the registered dry-preservation and mirrored ILD/ITD gates despite passing the other checks; Gen19 remains the baseline, and no listener benefit is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~01:05), covering both reviews

1. **FAIL adopted.** Both reviewers reproduce it:
   - D fails at both SNRs (all four means negative; at 0 dB the whole SI-SDR interval is below zero).
   - SP fails on mirrored ILD and ITD. The ITD miss is the same bin as Gen 28 (crop 1, 0 dB, ±30°, 0 → 1 sample). The two mirrored subsets duplicate the same evidence. Perceptual significance is undetermined; SP stays FAIL with no tolerance.
   - Astra's addition is adopted: the +0.370 dB is synthetic-room gain. Measured-room gains are smaller, and four measured rooms have small negative STOI changes at −5 dB.
2. **The "GEN27 SCREEN" label** is a hard-coded string in the reused judge, not an error in the run.
3. **The two reviewers split on what to do next:**
   - Astra: (a) one final dose halving, P = 0.0625.
   - Muse: (c) fine-tune Gen 19 on the room mix, then blend weights back toward Gen 19 (WiSE-FT).
4. **Resolution: both, in order.**
   - **Gen 30 = Astra's (a)**, exactly as she specified: 84.375 / 5.625 / 10, seed 20261117, scratch, 24k, everything else frozen, unchanged judge_v3 vs same-seed Gen 19.
     - Astra's new boundary is adopted and registered: **any Gen 30 failure ends the dose-only campaign**, even if R1a passes.
     - Reason: the registered stopping rule has not triggered, and this is the cheapest single-factor test. It closes the taper with a prospective bound instead of leaving it open.
   - **Gen 31 = Muse's (c)**, built and pre-registered while Gen 30 trains.
     - The blend weight is fixed by a rule on a validation split disjoint from every screen voice and room.
     - Astra's pre-launch review is required.
     - It runs only if Gen 30 fails, which ends the dose campaign.
     - Astra's caution is recorded: the published evidence for WiSE-FT and L2-SP is from vision models, and neither guarantees preservation; that remains a measured requirement.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
