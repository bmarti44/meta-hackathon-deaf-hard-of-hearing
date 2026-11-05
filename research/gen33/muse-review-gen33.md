# Muse (Meta) independent review of the Gen 33 result and agenda — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~03:04.
> Disposition: see [astra-review-gen33.md](./astra-review-gen33.md#disposition-claude-opus-55-2026-11-05-0320-covering-both-reviews).

## Verbatim answer

REVIEW: Gen33 REJECTED stands. In-silico only, no clinical inference.

1. Decision and measures:

REJECTED is correct on the text given. L1 fail: +0.096 dB ILD, +0.125 ITD vs Gen19 independent. L2 fail: 5.523 vs 5.492 dB mean target-ILD err = +0.031 dB worse. L4 fail: 18/40 =45% per-ear negative. No arithmetic error found.

Characterisation is correct *if* results.md keeps the two ILD metrics separate:
- ILD distortion (output vs mixture): 0.39 linked vs 1.04 Gen32 = -0.65 dB, better preservation.
- target-ILD err (output vs clean target): 5.60 vs 5.52 = +0.08 dB worse on existing bench; +0.85/+1.02 dB worse at +5/+10 dB crossed scenes.

Do not merge them. The low 0.39 does not overturn L1/L2. Copying mixture gives 0 distortion by definition.

What can be concluded, narrowly:
Only this linkage failed: frozen Gen32 alpha=0.7 weights + post-hoc averaged-encoder shared mask m=mask_net((encL+encR)/2), tested on assumed head model, 16 crossed +4 scenes, seed 17. Pattern is SNR-dependent tradeoff, not general win: target-ILD -0.74/-0.75 dB at -5/0 dB but +0.85/+1.02 at +5/+10 dB; per-ear SI-SDR >=0 / -0.05 / -0.18 / -1.04 dB by SNR; ITD +0.5 samples at 0 dB. Descriptive Gen19-linked +0.12 SI-SDR/+0.004 STOI at -5dB is exploratory only.
Do not claim "linking fails" or "linking helps low SNR." No joint training, no measured HRTF/BRIR, n small.

Which metric primary: keep target-ILD err as primary for directional hearing. Literature: bilateral CI users get little usable ITD via current envelope processing and rely dominantly on ILDs for lateralization; binaural noise-reduction literature evaluates preservation of target cues / localization error, e.g. Baumgaertel et al., Hassager et al., Best et al. Mixture-distortion rewards doing nothing and confounds residual noise with cue preservation. It belongs as secondary safety guardrail, not primary. Do not reclassify retrospectively to turn a fail into pass. Any change must be prospective with new prereg and rationale.

2. After 7 straight room-line FAILs, stop tuning synthetic gates. Build the eval asset first.

Ranked:
1. Freeze REAL-EVAL-v1 - real measured rooms/voices, evaluation-only.
2. Frozen Gen19 generalization probe on REAL-EVAL-v1, no training.
3. Only then: trainable two-input linked gain end-to-end, or ACE-envelope auxiliary - one change at a time.

Spec for #1, single change:
Change: add one frozen evaluation asset, zero weight changes. Assemble from open measured data, e.g. 3 real rooms RT60 ~0.3-0.8s Aachen/Surrey BRIRs + 2 unseen Libri speakers + real cafeteria babble recording, fixed 24 scenes: -5/0/+5 dB x target +/-30/60deg, interferer mirrored, 16kHz, locked file hashes, seed 17 separate from training seeds. Compute mixture, Gen19 independent only.
Decision rule: asset accepted iff a) mixture SI-SDR spread >6 dB across scenes, b) clean-target ILD computable in all scenes, c) Gen19 runs without code change and shows variance, not ceiling/floor. No promotion on this Gen.
Judge: independent hash-check + metric script; PASS = asset locked and logged; FAIL = rebuild, no model claims. Explicitly forbid training on REAL-EVAL-v1 in prereg. Ideal extension later: same geometry re-recorded with two BTE mics / Nucleus 6 USB accessory in owner's actual living room/kitchen, same frozen list.

Rationale: Gen27-33 loop is overfitting to one synthetic head/RIR. Further 1-hr dose/WiSE tweaks will not resolve ecological validity.

3. SUBMISSION.md Gen33 bullet:

Gen33 tested frozen-weight averaged-encoder shared mask; REJECTED - no spatial or quality win, worse target-ILD and up to -1.04 dB SI-SDR at +10 dB with 18/40 per-ear losses vs independent. Lower mixture-ILD distortion did not improve target localization; Gen19 remains baseline, no user benefit implied.
