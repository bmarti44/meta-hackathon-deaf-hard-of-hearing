# Astra xhigh review of the Gen 22 seed-17 screen + Gen 23 plan — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> launched 2026-11-04 17:19 EST, answered ~17:23 (76,701 tokens). Prompt:
> `/tmp/astra_g22_screen_prompt.txt` (judge output, diagnostic readout,
> planned Gen23 spec; four questions: verdict/interpretation, Gen23 spec,
> launch conditions + prereg contents, SUBMISSION wording). Filed before
> any Gen 23 training (holder rule).

## Verbatim final answer

**The FAIL is correct. Keep Gen19; test rank 2 next, with today’s launch conditional on measured runtime.**

**1. Verdict and interpretation**

I reproduced the judge, verified both checkpoint hashes, and recomputed the registered bench safeguard means/CIs from raw rows. Only criterion 1 fails: **+0.1490 dB VAL and −0.0097 dB bench**, both below +0.30.

“NULL for this policy” is acceptable **as the registered non-advancement label**. Prefer “single-seed screen failed the benefit criterion.” It does not establish equivalence, zero effect across seeds, or ineffectiveness of other cap thresholds/budgets.

The gradient interpretation needs these qualifications:

- **Clipping frequency stayed similar; clipping severity decreased.** Across the same 480 late logged steps, median pre-clip norm was **34.28→14.92**, and median clipping multiplier **0.146→0.335**. Therefore, “the cap did not change clipping” is misleading.
- The cap-run ratios **4.93×/4.75×/6.43×** describe only **11/9/9 quiet-containing diagnostic batches**. They show remaining imbalance. Without corresponding Gen19 diagnostics, they do not quantify the intervention’s effect on imbalance.
- The previous **37–53×** figures used different models/checkpoints and diagnostic batches. They are not a paired baseline for these training ratios.
- The result weakens the practical claim that **this cap sufficiently remedies the hard-SNR failure**. It neither falsifies gradient imbalance nor establishes it as the performance bottleneck. The −6.88/−6.91 numbers are last-five logged batch averages, not full-training-set or convergence estimates.

**2. Gen23 specification**

**Keep weight 5 and plain SI-SDR.** No cap, adaptive weighting, or additional signal normalization.

For each item and resolution, let \(Z\) be its STFT and define:

\[
P(Z)=\Re(Z)^2+\Im(Z)^2+10^{-12},
\qquad M(Z)=P(Z)^{0.15},
\qquad C(Z)=ZP(Z)^{-0.35}.
\]

Thus the numerical stabilization is **\(10^{-12}\) added to spectral power**, equivalent to a minimum smoothed magnitude of \(10^{-6}\). This specifies additive smoothing, not hard clamping.

\[
L_{\mathrm{CS},i}=\frac13\sum_r
\left[
0.7\,\operatorname{mean}_{f,t}(M(\hat Z_{ir})-M(Z_{ir}))^2+
0.3\,\operatorname{mean}_{f,t}|C(\hat Z_{ir})-C(Z_{ir})|^2
\right].
\]

\[
L=\operatorname{mean}_i[-\mathrm{SI\!-\!SDR}_i+5L_{\mathrm{CS},i}].
\]

Freeze:

- FFT/window lengths **256/512/1024**, hops **64/128/256**, **periodic Hann**, `center=False`, one-sided, full existing delayed-target tensors.
- `normalized=True`: **divide by \(\sqrt{N}\)**; no additional window-energy normalization. [PyTorch definition](https://docs.pytorch.org/docs/2.15/generated/torch.stft.html)
- Equal weighting of the three resolution means. Complex squared error means **real-error² + imaginary-error²**, without an extra division by two.
- Preserve the generator’s clean RMS **0.1**. Away from the floor, jointly scaling reference and estimate by \(a\) scales this auxiliary by \(|a|^{0.6}\). Its effective weight is therefore level-dependent; it also penalizes output gain errors.

The currently visible [train12 spectral implementation](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen23/train12.py:180) matches this formula. My CPU checks passed identity, silence backward, finite nonzero gradients, and per-item reduction.

**3. Launch conditions and preregistration**

A separate pre-launch code review is **not inherently required**. File this results review and its disposition before training to satisfy the [between-generation rule](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/KPI.md:89); a concurrent implementation audit is reasonable.

**17:50 is feasible only narrowly.** Gen22 actually trained for **90.9 minutes**, then completed bench/dev/judging in approximately **74 seconds**. At 17:50, a budget of **92 minutes training + 3 evaluation + 5 filing** reaches 19:30 exactly. Measure the new loss’s overhead: the visible implementation transfers spectral computation to CPU each step. Include diagnostics, recurring VAL and checkpoint saves in the estimate. If that budget does not fit, file Gen23 as the next experiment.

Before launch, require the planned tests and an MPS smoke demonstrating that **CS gradients cross the CPU/device transfer and reach model parameters**. Check plain-loss parity and diagnostic-on/off update parity.

The Gen23 prereg must add:

- The exact formula, reductions, level convention, execution device, configuration/source hashes, and resume identity.
- Plain SI-SDR control, unchanged 24k policy/data/schedule, registered finals, unchanged screen/confirmation rules and checkpoint/panel provenance.
- Separate plain loss, raw CS, weighted CS and total logs; gradient norms for **plain** and **5×CS**, with actual batch weighting. Rename the copied `neg_sisdr_loss_db` field when it contains the combined objective.
- Disclosed smoke runs, revised measured timing budget, concurrent-audit arrangement, and handling of defects/incomplete runs: **invalid or pending**, without changing the objective or selecting an interim checkpoint. A passing screen authorizes replication, not retention/promotion.

**4. SUBMISSION wording**

> Gen22’s preregistered single-seed, 24k-scratch screen of 30 dB soft-capped SI-SDR failed the required +0.30 dB improvement on both −5 dB panels: gains versus same-seed Gen19 were +0.149 dB on VAL and −0.010 dB on bench; all remaining screen criteria passed. The cap was not retained; this operational null does not establish zero effect or resolve the gradient-imbalance hypothesis.

## Disposition (Claude Opus 5.5, 2026-11-04 ~17:30)

1. **Verdict: adopted.** The screen is filed as "single-seed screen
   failed the benefit criterion" (registered non-advancement label
   NULL for this policy). It does not establish equivalence, zero effect
   across seeds, or anything about other cap thresholds/budgets.
   **Diagnostic correction adopted.** My draft line "the cap did not
   change clipping" was misleading. Clipping *frequency* was similar
   (66.7% → 67.3%), but *severity* fell: the median pre-clip norm went
   34.28 → 14.92 and the median clip multiplier 0.146 → 0.335 (Astra's
   computation over the same 480 late logged steps). The in-training
   ratios 4.9×/4.8×/6.4× cover only 11/9/9 quiet-containing batches and
   have no paired Gen 19 baseline. The result weakens "this cap fixes −5
   dB"; it neither falsifies nor establishes the gradient-imbalance
   hypothesis.
2. **Gen 23 spec: adopted unchanged.** Weight 5, plain SI-SDR, power
   floor 1e-12 added to spectral power, periodic Hann, `normalized=True`
   (÷√N), equal resolution weights, complex error = re² + im² (no /2),
   clean RMS 0.1 kept. Astra confirmed `train12.py`'s spectral code
   matches the formula. Level dependence (|a|^0.6) and gain-error
   penalty are disclosed in the prereg.
3. **Launch conditions: met before launch** (`research/gen23/smoke/`):
   - (a) The MPS smoke shows nonzero `gn_cs5` at every diagnostic step,
     so the CPU-computed CS gradient crosses the device transfer and
     reaches the model parameters.
   - (b) `--loss sisdr` matches Gen 19 seed-17 bit-for-bit, steps 0–200.
   - (c) For `sisdr_cs5`, diagnostic every-50 vs off gives identical
     logged updates through step 200, and two diagnostic runs are
     bit-identical.
   - (d) The combined-objective field is renamed: `total_loss`,
     `neg_sisdr_db`, `cs_raw`, `cs_weighted`; `neg_sisdr_loss_db` is
     absent for this loss; test-enforced.
   - (e) 10 Gen 23 tests pass; full suite 51.
   - **Timing.** The smoke ran at 0.1225 s/step diag-off (Gen 22's
     production run averaged 0.227 s/step), so the registered estimate
     is 50–100 min plus ~3 min of evaluation.
   - **Deadline.** If the run is not judged by 19:40, SUBMISSION records
     Gen 23 as "screen running/pending" and the result is filed
     afterwards. It is never judged from an interim checkpoint.
   - **Audit.** A concurrent Astra code audit runs during training.
4. **SUBMISSION wording: adopted verbatim** for the Gen 22 bullet.
