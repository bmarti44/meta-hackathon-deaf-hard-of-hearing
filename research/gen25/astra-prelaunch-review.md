# Astra xhigh pre-launch review of Gen 25 (+ research roadmap) — verbatim + disposition

> `codex exec -m gpt-6-astra -c model_reasoning_effort="xhigh" -s read-only`,
> 2026-11-04 20:31–20:39 EST (104,066 tokens). Prompt:
> `/tmp/astra_g25_prompt.txt`. It asked for a pre-launch review of commit
> 61c40ff plus a ranked roadmap answering the holder's question about
> weight editing, small models and other routes.

## Verbatim final answer

**Hold the launch package for the fixes below. The averaging recipe itself is valid.**

I reviewed `61c40ff` and the subsequent manifest commit `1929453`. Read-only checks passed: all 27 checkpoint hashes, seed/step metadata, matching tensor schemas, finite weights, and all eight Gen25 registered source hashes. Seed-17 parent VAL parity also passed: maximum differences **6.54×10⁻⁶ dB SI-SDR** and **3.16×10⁻⁸ STOI**. I did not build or evaluate Gen25.

**Blocking defects to fix before launch:**

1. **Enforce the registered input identities.** At `61c40ff`, the untracked inputs had no committed hashes. `1929453` fixes that registration gap, but [swa.py:67](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen25/swa.py:67) merely records whatever files it loads; [the verifier:65](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen23/verify_provenance.py:65) never checks the input manifest or averaging recipe. Reference/hash the manifest in the prereg, reject mismatches before construction, and verify the saved tensors equal the prescribed nine-input average. The binaries need durable archival storage, not necessarily Git tracking.

2. **Complete the promised VAL parity guard.** [swa.py:60](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen25/swa.py:60) collects both metrics but checks only SI-SDR. Check both metrics, finite values, unique item keys and exact panel membership, using explicit exceptions. Current seed-17 values are sound; the executable guard remains incomplete.

3. **Resolve the shared-verifier collision with running Gen24.** Adding Gen25 changed `verify_provenance.py` from Gen24’s registered `1b1bf42…` to `eba3c53…`. Consequently, [Gen24’s frozen source check](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen24/prereg.md:85) will fail. Isolate Gen25 support and preserve Gen24’s frozen checker; explicitly file/dispose this code-only deviation. Do not silently replace Gen24’s preregistered hash. This is a provenance failure, not evidence that Gen24’s trained weights are defective.

Commit the corrections and updated Gen25 source hashes before constructing its candidate.

The following are **non-blocking for the default CPU screen**:

- `--device mps` is broken: inputs move to MPS, models remain on CPU. Either support device movement properly or restrict this averaging/evaluation script to CPU.
- [The pipeline](/tmp/gen25_pipeline.sh:6) correctly stops on execution failures. However, a scientific `FAIL` exits zero, so `PIPELINE DONE` means evaluation completed—not advancement. Any replication automation must read `verdict == "ADVANCE"` and require provenance PASS.
- Commit the pipeline, add overwrite protection, and pin imported dependencies/environment/data manifests. The current source table omits transitive dependencies; the verifier also checks CI consistency without recomputing bootstrap bounds.
- Confirmation is specified but lacks a Gen25 aggregation command. Implement that before retention. Recipe acceptance does not substitute for hash-matched spatial evidence and the complete KPI scorecard.

**The final-candidate interpretation is legitimate:** Gen25 is a new, prospectively specified *derived final artifact*, not Gen19’s terminal optimizer checkpoint. Using intermediate weights as fixed arithmetic inputs does not constitute judging or selecting intermediate checkpoints. Keep the window, coefficients and seeds fixed; do not try alternate windows after seeing the result. Disclose that the hypothesis arose after observing Gen19’s trajectory. The wrapper correctly applies Gen22’s six numerical screen rules.

For the roadmap, finish Gen24 unchanged. These are ranked by value per laptop hour; budgets are estimates for an otherwise unshared machine. Each trained candidate uses a fixed terminal step. Gen25 retains its existing rules; later generations should use the prospectively registered larger-panel rule described below.

| Rank | Single intervention | Why it could help; realistic expectation | Cost and decision |
|---|---|---|---|
| **1** | **Gen25’s fixed nine-checkpoint average.** | Reduces late-trajectory variation without extra inference cost. These checkpoints come from a decaying Adam schedule, so this is SWA-style averaging—not the original constant/cyclical-LR procedure. Expect a small effect; **+0.30 is an ambitious outcome**, not a forecast. [SWA](https://arxiv.org/abs/1803.05407) | **5–15 min**, mostly evaluation. Apply Gen22 screen and confirmation exactly; no window search after failure. |
| **2** | **One fixed midpoint:** `0.5·Gen19 + 0.5·Gen21-R48`, within each seed. | Shared ancestry makes weight coordinates compatible; interpolation could recover hard-SNR behavior while retaining useful continuation updates. R48’s negative three-seed bench gain makes the upside uncertain. This is a WiSE-FT-style hypothesis, not evidence that vision results transfer. [WiSE-FT](https://arxiv.org/abs/2109.01903) | **5–15 min.** Register α=0.5 before evaluation, then apply the full gate. Do not sweep α against bench. |
| **3** | **One-parameter mask calibration:** replace `m` with `m^γ`, selecting from `{0.8, 1, 1.25}` on tuning material only. | Tests whether masks leave excessive residual crowd noise or suppress useful speech. A uniform waveform gain cannot materially improve SI-SDR because it is scale-invariant. Mask calibration can, but may damage STOI/quiet. | **15–30 min.** Register the grid and tie-break toward γ=1; freeze one result before independent screening. Expect mostly small effects, often below +0.30. |
| **4** | **Restrict a short hard-SNR continuation to the 12,960-parameter mask head.** | Tests whether useful frozen features need a different decision boundary. Use 4k steps, hard60, and fixed L2-SP toward the parent; compare with a matched full-model continuation using the same schedule/data/penalty. The experimental factor is the trainable parameter set. [L2-SP](https://proceedings.mlr.press/v80/li18a.html) | **30–60 min including the matched control.** Require the parent-relative gate and report the full-model comparison. Plausibly more than a calibration gain, but capacity restrictions can also prevent improvement. Low-rank adapters are a separate follow-up. |
| **5** | **Change babble identity reuse:** draw each mixture’s interferers from a randomly selected six-speaker training subpool, preserving legacy k/SNR/noise proportions. | Evaluation repeatedly samples six identities; training samples from roughly 250 eligible identities. Gen20 changed k, not this repeated-voice structure. This tests a concrete distribution mismatch without using evaluation voices. | **75–110 min**, 24k scratch. Require the registered gain and safeguards, including broad development support. A +0.30 effect is plausible but unestablished; narrow recipe overfitting is possible. |
| **6** | **Add one teacher-distillation term to an otherwise matched short continuation.** | A demonstrably stronger non-causal/look-ahead teacher may provide useful training targets while the deployed student remains causal. It cannot give the student unavailable future information. [Speech-enhancement precedent](https://www.isca-archive.org/interspeech_2024/liu24n_interspeech.html) | **60–120 min only with a ready teacher and bounded/cached inference.** First require clean data lineage and clear development headroom—e.g. ≥1 dB over parent. Freeze teacher/coefficient, compare with no-distillation continuation, then apply the gate and suffix-invariance test. Otherwise defer; teacher construction is additional work. |

Inspecting weights is useful for finding nonfinite values, abnormal layer updates, saturation and gradient allocation. Individual weight values do not identify “bad speech features” that can reliably be edited manually.

EMA is worth registering during a future continuation; sparse saved checkpoints cannot reconstruct exact per-update EMA. Same-parent model soups may eventually help, but independently initialized seeds should not be averaged naively. Re-basin requires architecture-aware alignment through this encoder/decoder, depthwise, residual and skip structure; it has poor immediate value here. [Model soups](https://arxiv.org/abs/2203.05482), [re-basin](https://arxiv.org/abs/2209.04836).

A tiny replacement model mainly buys speed. A small **causal estimated-SNR helper** becomes more attractive if scalar calibration reveals consistent condition-dependent gains; evaluation must use estimated—not oracle—SNR. Binaural input supplies genuinely additional spatial information, but needs a separately registered task, training scenes and spatial safeguards. It cannot inherit the mono scorecard.

**Change future screening, while preserving the historical scorecard.** Gen22’s +0.149 and Gen23’s −0.337 VAL changes are real deterministic differences on fixed examples. They do not establish a numerical “noise floor.” The uncertainty concerns generalization: eight VAL items contain only two target speakers, and six bench mixtures confound speaker, content and mixture effects.

Before the next generation:

- Register a larger development panel—for example, **16 training-disjoint targets × four crops × four mixtures = 256 items/SNR**, at −5 and 0 dB, plus safeguards. Hash the material.
- Separate calibration/tuning material from the advancement panel. Register a paired ≥+0.30 dB advancement criterion, non-worsening STOI, safeguards, speaker-clustered uncertainty and three-seed confirmation. Additional crops do not become independent speakers.
- Keep Gen19’s original panels, thresholds and **13/14** result unchanged. Report the new protocol separately; do not retroactively turn Gen20–25 failures into passes. Reserve untouched speakers/material for final confirmation.

Finally, Gen19’s exact seed-mean −5 dB score is **1.187654**. Clearing +1.5 requires **+0.312346 dB**; merely passing a +0.30 improvement gate does not necessarily clear that KPI.

## Disposition (Claude Opus 5.5, 2026-11-04 ~20:50)

**Blocking 1 (input identities): fixed.**
- `swa.py` now refuses any input whose sha256 differs from the committed
  `input_manifest.json`, before any averaging.
- The prereg lists the manifest's hash.
- The new `verify_provenance_g25.py` re-checks every input and requires
  the saved weights to equal the uniform average of the 9 inputs,
  bit-exact.
- Binaries: the inputs stay local, with hashes committed. Durable
  archival is open; Hugging Face is the planned home.

**Blocking 2 (parity guard): fixed.** It checks both metrics, finite
values, unique keys and exact membership, and raises explicit errors.

**Blocking 3 (shared-verifier collision): fixed.**
- `research/gen23/verify_provenance.py` is restored byte-for-byte to the
  Gen 24-registered version (sha `1b1bf42…`, from commit edbf7e8).
- Gen 25 uses its own `research/gen25/verify_provenance_g25.py`.
- The deviation (the shared file was modified in 61c40ff, then restored)
  is filed in Gen 24's prereg run log. Gen 24's running pipeline calls the
  restored file, whose hash matches its registration.

**Non-blocking items:**
- **Device:** the script is CPU-only now; `--device` is removed.
- **Pipeline:** committed as `research/gen25/pipeline.sh`, with overwrite
  protection. It is documented that PIPELINE DONE means "evaluated"; any
  replication reads `verdict == "ADVANCE"` and the provenance PASS.
- **Not done yet:**
  - the confirmation aggregation command (it will be written before any
    retention if the screen advances);
  - pinning transitive dependencies;
  - recomputing the bootstrap CIs.
  These are noted as open.

**Validity:** adopted as a derived final artifact. The window,
coefficients and seeds are fixed, and no alternate windows will be tried
after the result. The prereg now discloses that the hypothesis arose
after observing Gen 19's trajectory and the holder's question.

**KPI note:** Gen 19's exact seed-mean −5 dB score is 1.187654, so
clearing +1.5 needs +0.312346 dB. Passing the +0.30 gate does not by
itself clear the KPI.

**Roadmap adopted, in order:**
1. Gen 25 (this run).
2. Gen 26: a fixed α=0.5 midpoint of Gen 19 and Gen 21-R48, per seed.
3. Mask-exponent calibration with a separate tuning panel.
4. Mask-head-only hard-SNR continuation versus a matched full-model
   control.
5. Babble identity reuse via six-speaker training subpools.
6. Distillation, only with a ready teacher.

**Future screening:** before Gen 26 or 27, a larger registered development
panel (16 training-disjoint targets × 4 crops × 4 mixtures) with separate
tuning material. Gen 19's original panels, thresholds and 13/14 stay
unchanged.
