# Muse (Meta) independent review of the Gen 34 result — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~03:57.
> Disposition: see [astra-review-gen34.md](./astra-review-gen34.md#disposition-claude-opus-55-2026-11-05-0415-covering-both-reviews).

## Verbatim answer

VALID ASSET is about integrity, not benefit. On text given, VALID ASSET is reasonable, readings mostly careful, with fixes.

1. VALID ASSET and readings:

Arithmetic checks: 3 T60 x 4 SNR =12 noisy cells +3 target-only =15. So "15 of 15" is consistent. Gen32 target-only STOI deltas: 0.973-0.971=+0.002, 0.959-0.955=+0.004, 0.950-0.941=+0.009, inside claimed +0.001 to +0.009. Worst cell quoted -2.00/-0.034 matches table high/+10dB. No mismatch.

VALID ASSET as development material: acceptable if A1-A7 as stated pass. A2 is the weak point: "overlap excluded by documented SQAM/VCTK provenance; speaker identity unresolved" means no file-level proof of talker independence from LibriSpeech training. That must stay as a limitation. It is development material only, not confirmation. Correctly `promoted FALSE`, no training/selection.

Readings are largely fair: means only, descriptive only, stresses one lab/4 talkers, one seed small Gen32 edge "not evidence of listener benefit." Good.

Overclaim to fix: "Gen 19 helps" / "In crowds...helps." Should be "improves SI-SDR/STOI on these recordings." No listening test, no CI simulation, no variance shown. Cannot claim help.

Missing that should have been reported:
- spread, not just each-ear means: range/SD across 4 talkers x 4 azimuths, worst-ear, per-azimuth.
- absolute noisy STOI/SI-SDR, not only deltas; input SNR calibration on recorded mixtures.
- directional metrics: ILD error and ITD/delay error in noisy cells, not only A4 direction on 16 low target-only items.
- level, clipping, sample-rate, latency/causality, bypass numbers.
- babble provenance, talker IDs, lag search for alpha.

2. Polarity:

Characterisation is correct in substance: SI-SDR is invariant to scaling by -1, STOI uses magnitude/energy envelopes and ILD uses energy, so all blind to global sign. Seed-dependent sign is plausible under symmetric init; table 2 negative /1 positive supports it. Alpha ~ -0.92 at zero lag with ~+6dB waveform error despite SI-SDR gain is the expected signature.

Recommendation, exact:
- Do not silently rewrite Hugging Face weights. Publish as config-only patch with version bump: add `"polarity": -1 for seed17/19, +1 for seed18,` measured by frozen `alpha on target-only LibriSpeech dev-clean` script, and `enhance.py: y_out = polarity * y_raw`, same checkpoint both ears. Weights unchanged. Document that all registered metrics unchanged.
- Future preregs: add non-gating safety check `A8: target-only alpha >0 after polarity correction, |alpha| reported, lag 0 +/-20 samples`, and assert bilateral polarity equal. Do not change loss to sign-anchored loss now: would perturb training for no CI-envelope gain. Fix in post-processing.

ACE likely unaffected, but mixing with acoustic residual/EAS/hearing-aid and opposite-sign bilateral seeds would be affected. That justifies fix.

3. Best next 1-h experiment:

Do (a) preservation fine-tune, not (b)/(c). Rationale: demonstrated regression is hurting what is heard well today: STOI 0.971/0.955/0.941 on clean reverberant and -2.0dB/-0.034 at high/+10dB. Shared-mask or ACE-envelope are architectural and >1h and do not fix quiet regression first.

Spec, pre-register:
- Start Gen19-seed17 frozen encoder; fine-tune mask decoder only, ~1h laptop, 1 seed, low LR e.g. 1e-4, few k steps.
- Synthetic mix only, never BRUDEX: e.g. 50% noisy RIR T60 0.3-1.3s SNR -5 to +10dB SI-SDR loss, 50% reverberant target-only with preservation loss L = waveform MSE + 0.5*(1-STOI), weight lambda tuned to halve clean gap.
- Judge primary: existing synthetic gates must pass with no regression; success = target-only synthetic STOI drop <0.015 and noisy synthetic SI-SDR within 0.3dB of Gen19. BRUDEX frozen descriptive only, run once at end, no selection, no training on BRUDEX talkers/room/BRIRs. Any iteration on BRUDEX = overfit, forfeit asset.
- Report same Table + worst-ear + alpha.

4. SUBMISSION.md sentences:

Gen 34 froze a 240-item real-recording audit as a VALID development-only asset; on those recordings Gen 19 improved metrics in babble but lowered them in quiet echoey speech. It also found a seed-dependent output sign inversion missed by all sign-blind metrics, with a config-level polarity fix proposed and no verdict change.
