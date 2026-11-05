# Muse (Meta) independent review of the Gen 35 result — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~04:50.
> Disposition: see [astra-review-gen35.md](./astra-review-gen35.md#disposition-claude-opus-55-2026-11-05-0520-covering-both-reviews).

## Verbatim answer

No file access; from text only.

1. Is INVESTIGATE correct, attribution right?

INVESTIGATE is correct. 4/6 research, 3/5 export checks named as fail. Registered rule with no rescue = INVESTIGATE. No waiver allowed.

Attribution is plausible but has one inconsistency to resolve from rows:

- STOI: claimed A2 vs A1 / E2 vs E1 only, sign and flush delta exactly 0, worst -0.0028 / -0.0022, bidirectional, ~146 lower vs similar higher, SI-SDR unchanged to 0.0003 dB. That pattern is consistent with DC-leakage into STOI lowest band, not speech loss. SI-SDR is mean-removed so immune. Accept as descriptive, not as pass.
- ITD: 1 scene seed 18 talker1/low/+60deg/-5dB 0->1 sample, claimed A1 vs A0 only. Plausible: sign flips both ears, bias is common DC, neither moves whole-utterance XC peak; replacing 63 trailing zeros with signal can move peak 1 bin. Still a registered fail.
- Clip: DC +-0.11-0.16 vs fixed +-1 plus export RMS-restore-including-DC explanation is arithmetically plausible. Example: gain = Rin/sqrt(Rs^2+DC^2); removing DC raises speech ~0.5-1 dB, loud Rin=0.56 then clips more. But that is real clipping on write, not just measurement. Cannot waive.
- Table: 17: +5.3 to -2.9 to -13.3; 19: +5.1 to -2.1 to -14.2; 18: -1.2 to -1.2 to -12.8. 18 shows 0 dB from sign alone.
- Inconsistency: E1 claimed exactly -E0 everywhere with max diff 0, yet min alpha 17/18/19 goes -0.78/+0.52/-0.70 to +0.63/+0.52/+0.58. Seed 18 unchanged. If exact negation, +0.52 must flip to -0.52. Verify from rows whether alpha is abs, seed 18 was not flipped, or negation claim is wrong. Block any publish until cleared.

2. Publish to Hugging Face: nothing now.

Do not publish (a) sign-only now. Exactly neutral on SI-SDR/STOI/clip/RMS by construction means no in-silico evidence of better speech-in-noise, only polarity number fix; mono polarity is inaudible, bilateral common inversion preserves ITD. Churn with no benefit, leaves 0.11-0.16 DC in place.

Recommend (b) only: register new candidate E3 = sign fix + DC removed before RMS restore + peak-safe output stage, clip counted on final written file, STOI reported raw but gated on DC-invariant version. Judge on fresh frozen rows.

Single registered rule, pre-registered before rows, owner approval required, else nothing published:

PROMOTE E3 iff on fresh rows: polarity alpha>0 all clips/levels both paths; mean target-only err < E1 by >=3 dB; SI-SDR delta >=0 and DC-invariant STOI delta >=0 on all P1 item-ears; ITD delta =0 all scenes; final-file clip fraction <= published; lag=0; silence/tail RMS not increased. Any fail = INVESTIGATE, no rescue.

(c) retraining with signed gain-sensitive loss and no decoder bias follows only after (b) passes or fails on fresh data.

3. Next research: confirm order, spec #1 first.

Confirm: 1) reverberant-target preservation fine-tune vs corrected teacher, 2) trained bilateral, 3) ACE auxiliary. Do not skip to bilateral before mono preservation is clean.

Spec #1, pre-register: teacher = A2 research output with sign/bias/delay corrected, RMS restored DC-excluded + peak normalized to -1 dBFS; student = same 602k arch except decoder bias removed/forbidden, init from current; targets = reverberant clean, not anechoic; loss = signed gain-sensitive MSE on waveform + multi-res STFT, no SI-SDR-only term; data = same P1 + reverb held-out; freeze encoder 2k steps then unfreeze; success = same gates as E3 plus no anechoic-only overfit. Fresh rows, no reuse of Gen35 rows.

4. SUBMISSION.md Gen35 bullet:

Gen 35 frozen repair audit failed its registered gates so nothing was promoted or published. Sign fix alone is exactly neutral and DC removal explains the small STOI, 1-sample ITD, and clip-count flags, but clipping is real and needs a peak-safe candidate tested on fresh data.
