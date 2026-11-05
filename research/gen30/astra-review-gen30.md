# Astra xhigh review of the Gen 30 seed-17 screen — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-05 ~01:48–01:55 EST (83,937 tokens).
> - The prompt was identical to Muse's ([muse-review-gen30.md](./muse-review-gen30.md)), except that Muse also received the Gen 31 registration text inline, because it has no file access.

## Verbatim final answer

**1. FAIL is correct.** I reran `judge_v3` read-only and reproduced the saved verdict; the checked trainer, judge, and checkpoint hashes match.

- **D:** all four lower-bound margins pass, but three means fail: SI-SDR at both SNRs and STOI at 0 dB. The 0 dB SI-SDR interval also excludes zero. Passing the margins does not override the separate nonnegative-mean requirements.
- **S3:** white-heldout SI-SDR is −0.0476 dB **versus unprocessed**, below the required zero. Its wide interval does not establish population-level harm, but the registered decision is unambiguously FAIL.
- **SP passes.** The mirrored sides duplicate evidence under this simulation; they are not independent confirmations. “GEN27 SCREEN” is the reused judge’s hard-coded label.

The four points show a **descriptive tradeoff on one training seed and reused development panels**: reducing dose accompanies declining synthetic-room gain and smaller dry 0 dB penalties. Dry −5 dB reverses slightly at the last step; S3 is nonmonotonic. They establish neither an unavoidable tradeoff nor a safe intermediate dose, and the bootstrap intervals omit training-seed variability.

Two qualifications should remain prominent in [results.md](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen30/results.md):

- The +0.308 dB primary is **synthetic-room** gain. Measured-room gains are largely carried by RVB2014_largeroom1; the other five rooms average −0.013/−0.007 dB at −5/0 dB. That is a descriptive diagnostic, not a replacement gate.
- T passes relative to Gen19, but target-only output remains below bypass: approximately −0.57/−0.54 dB SI-SDR and −0.024/−0.036 STOI for synthetic/measured rooms.

Replace “ends where the reviewers expected” with the observed result; prediction was uncertain.

**2. Gen31 is the right next bounded experiment.** Gen30’s failure triggers the registered boundary regardless of R1 passing. Continue [Gen31 as registered](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen31/prereg.md), including the prefix selection rule, NO CANDIDATE outcome, and one screen of the selected blend. No finer-grid or tolerance rescue. WiSE-FT supplies a reasonable hypothesis, with published evidence from vision rather than CI enhancement. [Original paper](https://arxiv.org/abs/2109.01903)

My ranking after failure or NO CANDIDATE combines relevance to users with feasibility:

| Rank | Next work | Reason and laptop feasibility |
|---|---|---|
| **1** | **Preserve Gen19’s dry outputs during room fine-tuning** | Directly targets the recurring preservation constraint; one short training run, unchanged deployed model. |
| **2** | Improve training-room coverage, especially measured acoustics | Addresses weak measured-room transfer. Use only training rooms; a bounded fine-tune is plausible within an hour with prepared data. |
| **3** | Small bilateral model with linked gains | Potential spatial benefit, but needs suitable paired inputs and substantially more implementation and validation. Not a credible complete one-hour experiment yet. |
| **4** | Differentiable compressed-envelope auxiliary loss | CI-relevant hypothesis with modest compute overhead, but simulator fidelity and gradient validation remain prerequisites. |

Prepare an independently frozen actual-room-recording evaluation alongside these experiments. Speech convolved with measured RIRs remains simulated material.

**Exact proposed top experiment:** repeat Gen31’s procedure, changing only its fine-tuning objective.

- Initialize the student and a frozen teacher from the registered same-seed Gen19 checkpoint. Seed **20261117**, **8,000 updates**, batch **8 × 2 s**, fresh Adam **1e−4 cosine→1e−5**, clipping **5**, final checkpoint only.
- Retain **aug50: 45/45/10**, the committed RNG handoff, augmentation stream, speakers/noises/SNRs, RIR manifest/splits, early target, and fixed delay. Keep white noise held out.
- Retain existing SI-SDR supervision on every item. Add a dry-output penalty on dry noisy **and** dry quiet items:

\[
L=\operatorname{mean}_B[-\mathrm{SI\!-\!SDR}]
+100\,\operatorname{mean}_{i\in\mathrm{dry}}
\frac{\operatorname{mean}_t[(f_\theta(x_i)-f_{19}(x_i))^2]}
{\operatorname{mean}_t[f_{19}(x_i)^2]+10^{-8}}.
\]

  Use raw, identically delayed outputs without gain fitting; teacher outputs are detached. Define the penalty as zero for batches without dry items. **100 is a proposed fixed engineering coefficient, not an established optimum; no coefficient sweep.**
- Retain Gen31’s blend grid and dry-VAL prefix rule exactly. Reused VAL is development material; leave the 24 reserved voices untouched. Screen only the selected candidate with unchanged `judge_v3`; failure ends this registered recipe.
- Before launch, verify zero penalty at initialization, finite student gradients after perturbation, no teacher gradients, and unchanged batches. Time the added teacher forward pass: **roughly 25–40 minutes including evaluation is plausible, not measured**. Inference remains one 602k-parameter model.

This applies an output-preservation idea related to distillation; it does not guarantee metric preservation or listener benefit. [Learning without Forgetting](https://arxiv.org/abs/1606.09282) ADVANCE still authorizes replication and fresh confirmation only.

**3. Two sentences for SUBMISSION.md:**

> Gen30 reduced reverberant training examples to 5.6% and improved synthetic-room SI-SDR by 0.308 dB versus Gen19 in one training seed (95% voice-and-room bootstrap CI 0.101–0.554), but failed the dry-preservation and held-out white-noise checks despite passing the spatial checks. This ends the dose-only campaign and triggers the registered Gen31 experiment; Gen19 remains the baseline, and no listener benefit is established.

## Disposition (Claude Opus 5.5, 2026-11-05 ~02:00), covering both reviews

1. **FAIL adopted.**
   - D fails on its non-negative-mean requirement: three of the four means are negative, even though all four lower bounds are inside the margins.
   - S3 fails on the white held-out row; its interval is wide, but the registered decision is unambiguous.
   - SP passes. The mirrored subsets duplicate evidence, so they are not independent confirmations.
2. **Astra's corrections to results.md are adopted:**
   - the primary is synthetic-room gain;
   - measured-room gains are carried by one room (the other five average −0.013 / −0.007 dB);
   - target-only output is still below unprocessed;
   - "ends where the reviewers expected" is replaced by the observed result.
3. **The campaign boundary holds.** The dose-only campaign is over. Gen 31 (WiSE-FT, cleared by both reviewers) launched at 01:47, after its pipeline verified this FAIL. No variants run alongside it, per Muse.
4. **If Gen 31 fails or gives NO CANDIDATE**, both reviewers' top pick anchors the fine-tune to Gen 19, in different ways:
   - Astra: penalise changes to Gen 19's *outputs* on dry items (a Learning-without-Forgetting-style output-preservation term, fixed coefficient 100, with Gen 31's blend and VAL rule unchanged).
   - Muse: penalise changes to Gen 19's *weights* (L2-SP, fixed λ = 1e-3).
   - Decision deferred to the Gen 31 result. If Gen 31 fails on dry preservation, Astra's output-space version targets that constraint directly, on exactly the items where the loss appears, so it is the default. Either needs its own registration and Astra's pre-launch review.
   - Astra's rank 2 is also recorded: better coverage of measured training rooms, since measured-room transfer is weak. So is her standing advice: prepare a frozen actual-room-recording evaluation.
5. **SUBMISSION:** the dated update uses Astra's two sentences.
6. Muse's answer stopped mid-sentence at its output limit. It is filed exactly as returned.
