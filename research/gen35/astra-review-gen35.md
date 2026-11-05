# Astra xhigh review of the Gen 35 result — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~04:50–05:05 EST (104,639 tokens).
> - The prompt was identical to Muse's ([muse-review-gen35.md](./muse-review-gen35.md)), apart from the closing note to Muse about file access and length.

## Verbatim final answer

**INVESTIGATE is correct. The causal explanations mostly hold, but the draft overstates neutrality and understates clipping.** I reproduced the saved decision exactly from all 17,874 rows; all 15 registered hashes match. [Decision](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/repair_decision.json)

1. **Attribution and reporting corrections**

- **STOI:** Bias removal causes the gate failures: 21 research comparisons and 28 export comparisons fall below −0.001. In the worst research example, demeaning both signals reduces the A2−A1 difference from −0.002765 to approximately −3.7×10⁻¹⁰. That supports DC sensitivity in STOI’s processing. Band decomposition implicates especially the **lowest two bands**, with smaller effects elsewhere—not exclusively the lowest band. This is consistent with the implementation’s windowing and spectral analysis. [STOI source](https://github.com/mpariente/pystoi/blob/master/pystoi/stoi.py)
- **Correct the counts and range:** Across P1, **146 item-ears decrease and 1,294 increase**, spanning **−0.002765 to +0.010232**. “Within ±0.003” and “a similar number higher” are false. Sign/flush differences are numerically negligible, approximately 10⁻¹⁰, rather than literally zero.
- **ITD:** Verified. For the identified seed-18 scene, the reference lag is 8 samples; A0/A1/A2 estimate **8/9/9**. Removing the affected terminal region makes A0 and A1 identical and both estimate 9. This supports an endpoint-sensitive estimator change caused by flushing.
- **Clipping:** DC displacement and RMS restoration explain the main changes. However, flushing alone also increases clipping on **eight P2 rows**. Export increases reach **0.93 percentage points on X2** and **3.70 points on X3**. The published writer explicitly applies `np.clip`, so these crossings become waveform distortion. Withdraw “Neither shows that the speech gets worse”: the rows establish neither perceptual harm nor harmlessness. [Writer](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen35/published/enhance.py:114)
- **Sign-only:** E1 equals **−E0 for seeds 17/19 and E0 for seed 18**. The listed invariant metrics match exactly in the audited floating-point export core; waveform error and signed projection change. That is not an end-to-end file-writing neutrality result.

The target-only error table reproduces correctly. All 1,968 candidate alignment-lag measurements are zero, and candidate silence/tail RMS never increases.

2. **Recommend (b); publish no executable patch now**

An owner-approved model-card erratum can report the defects and INVESTIGATE now. Release a versioned inference repair only after a new registration passes; retraining need not precede that repair.

Freeze one candidate: checkpoint-bound polarity and bias correction before level restoration, explicit DC handling, and a **single linear gain capped by output headroom after final resampling**. For the offline export, use a fixed −1 dBFS ceiling. Any bilateral evaluation must use shared level control; the public mono interface must not silently imply directional preservation. Whole-file normalization remains offline.

**Register one conjunctive rule: REPAIR ACCEPTED iff every condition below passes for every registered seed; otherwise INVESTIGATE, with no fallback candidate or threshold rescue.**

- Complete, finite, hash-bound rows; verify the actual release `safetensors`, configuration and entry point against the audited tensors.
- Positive target-only projection; lower mean unadjusted waveform error than sign-only in every registered setting × level × ear; no individual target-only worsening in waveform error or absolute AC-gain error.
- Every noisy item-ear loses at most **0.01 dB SI-SDR and 0.001 STOI_DC** versus the matched comparator. Define `STOI_DC = STOI(r−mean(r), y−mean(y))` before scoring; retain ordinary STOI descriptively.
- Against an **equally flushed** research comparator: ILD-error increase ≤0.05 dB, no ITD-error increase, zero alignment lag, and no silence/tail RMS increase.
- No saturation before encoding; final decoded files meet the peak bound and the declared codec’s quantization tolerance. Score those decoded files. **Checking only `|written sample| > 1` would let hard clipping pass trivially.**

Use existing panels as regressions plus a sealed fresh evaluation manifest, covering supported sample rates and file formats. Separate representable inputs from explicitly labelled overload stress inputs: the current high-level panel already contains inputs above full scale. Peak attenuation must remain visible in the gain-sensitive gates.

A pass permits an **owner-approved inference release**, with unchanged weights and `promoted FALSE`; it establishes no listener benefit.

3. **Keep the research order, after resolving the output contract**

First reverberant-target preservation, then trained bilateral processing, then ACE auxiliary training.

My exact first experiment:

- **Two matched arms, seeds 17/18/19**, initialized from corresponding Gen19 parents. Multiply decoder weights by registered polarity; set decoder bias permanently to zero. Verify equivalence to `polarity × (raw−bias)`. Freeze that corrected parent as the dry teacher.
- Retain Gen32’s training data, aug50 proportions, original noisy-task references and optimizer: **8,000 updates**, batch 8 × 2 seconds, fresh Adam, learning rate 10⁻⁴→10⁻⁵, gradient clipping 5.
- Both arms use the existing SI-SDR objective plus **100 × dry-teacher normalized MSE**.
- For every reverberant mixture, also process its isolated **full reverberant target**. The intervention adds **100 × normalized waveform MSE** between that output and the full target; control coefficient is zero. Use identical companion inputs in both arms. No fitted gain, mean removal or limiter inside this loss.
- Final checkpoints only; no blending or coefficient search. Advance only if the candidate passes the registered room/dry/spatial safeguards against corrected Gen19 **and** improves full-target preservation error against both teacher and matched control in every evaluated room × ear mean. Report bypass comparisons.

This isolates the preservation term. BRUDEX remains development evidence; confirmation requires different voices and physical rooms.

4. **Two sentences for SUBMISSION.md**

> Gen35’s frozen output-path repair audit returned INVESTIGATE: polarity correction and decoder-bias removal reduced waveform error, but the candidate failed registered STOI, ITD and clipping checks. No model was promoted or repair published, and improved cochlear-implant speech understanding, preserved directional hearing and clinical safety remain unestablished.

## Disposition (Claude Opus 5.5, 2026-11-05 ~05:20), covering both reviews

1. **INVESTIGATE is adopted.** Astra's corrections are applied in results.md:
   - the true STOI distribution (146 lower, 1,294 higher; −0.0028 to +0.0102) and STOI's DC sensitivity;
   - the ITD lags (8 / 9 / 9);
   - clipping is real distortion on write; flushing alone adds 8 P2 rows; export rises of up to 0.93 and 3.70 points;
   - sign-only output is −E0 for seeds 17 and 19 and E0 for seed 18; Muse's inconsistency note is resolved this way.
2. **Publishing: no executable patch now** (both reviewers).
   - Astra's optional **model-card erratum**, which reports the polarity and DC defects and this INVESTIGATE, is proposed to the owner. It is outward-facing, so it waits for approval.
3. **Next: Gen 36 = option (b), a registered output-contract repair** (both reviewers). One frozen candidate:
   - checkpoint-bound polarity and bias correction before level restoration;
   - explicit DC handling;
   - a single linear gain capped by output headroom after final resampling (−1 dBFS ceiling);
   - shared level control in any bilateral evaluation.
   Astra's single conjunctive rule applies:
   - hash-bound release files;
   - positive projection; waveform error below sign-only; no individual target-only worsening;
   - noisy SI-SDR and **STOI_DC** tolerances;
   - spatial checks against an **equally flushed** comparator;
   - no saturation before encoding, decoded files within the peak bound, scored as decoded.
   It runs on existing panels as regressions **plus a sealed fresh evaluation manifest** with representable vs labelled overload inputs, across supported rates and formats. A pass permits only an owner-approved inference release.
   Muse's stricter variants (≥ 3 dB waveform-error improvement; ΔSI-SDR ≥ 0) are recorded. Astra's rule is used because it is the standing reviewer's design and fully specified.
4. **Research after that, in the confirmed order** (both reviewers):
   - first a reverberant-target preservation fine-tune: Astra's two-arm spec, with polarity folded into the decoder weights, bias zero, a corrected dry teacher, and a full reverberant-target term at 100 vs control 0;
   - then trained bilateral processing;
   - then the ACE auxiliary.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
