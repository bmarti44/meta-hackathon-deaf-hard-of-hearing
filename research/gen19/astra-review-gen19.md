# Astra xhigh review of Gen 19 (complete) — verbatim + disposition

> Reviewer: Codex `gpt-6-astra`, reasoning xhigh, read-only, 2026-11-04
> (Codex session 01a1a545-a87f-7180-8b63-d22fd9c7c68c; full session log
> incl. her tool calls: /tmp/astra_gen19_review.txt at review time).
> Prompt: verify seed-mean computations from the 3 bench JSONs; rank
> k-distribution paired continuations vs a 48k run; Stage C evidence
> defensibility + fresh-material requirements; first concrete change.
> Standing holder rule: Astra review between generations.

## Verbatim final answer

**Run the k-distribution pair first, after repairing its RNG setup.** The Gen19 arithmetic is correct. The late validation gains justify keeping 48k on the agenda, but they do not establish that 48k should take priority. Gen19 has not earned a Stage C **evidence** test.

1. **Verification: no material arithmetic error; several interpretation limits.**

I recomputed deltas from each bench’s raw rows, checked the checkpoint hashes against the actual weights, and reran the scorecard.

| Metric | Recomputed seed mean |
|---|---:|
| Crowd ΔSI-SDR | +3.51437 dB |
| Crowd ΔSTOI | +0.035408 |
| Crowd ΔACE-electro | +0.072187 |
| Crowd ΔSI-SDR, −5 dB | **+1.18765 dB — FAIL** |
| Crowd ΔSI-SDR, 0 dB | +4.64615 dB |
| Crowd ΔSTOI, −5 dB | +0.005480 |
| SSN / white ΔSI-SDR | +6.45356 / +0.72889 dB |
| Quiet absolute SI-SDR / ΔSTOI | 36.32094 dB / −0.004769 |

The −5 dB SI-SDR values are **1.06039 / 1.35558 / 1.14699**: every seed misses +1.5. The result is correctly **13 PASS / 1 FAIL**, with complete evidence under the scorecard’s implemented checks.

The validation movement also checks out, using the precision stored in `val_log`:

| VAL seed mean | 12k | 18k | 24k | 18k→24k |
|---|---:|---:|---:|---:|
| −5 dB ΔSI-SDR | 0.3233 | 0.3767 | 0.7800 | **+0.4033** |
| −5 dB ΔSTOI | −0.00433 | −0.00033 | 0.00833 | **+0.00867** |
| 0 dB ΔSI-SDR | 3.7500 | 4.0600 | 4.2367 | +0.1767 |
| 0 dB ΔSTOI | 0.07167 | 0.08200 | 0.08533 | +0.00333 |

All three seeds improve both metrics at both SNRs between those endpoints. However:

- **This supports further optimization, not a linear extrapolation.** LR falls from approximately `2.32e-4` at 18k to `1e-4` at 24k. The benefit belongs to the combined training-budget/schedule intervention. Individual trajectories fluctuate; the logs do not retain per-speaker results needed to verify the interim review’s “both target speakers” condition.
- **The spatial result is seed 1 only**, on four scenes: target-ILD 5.46945 versus 5.96419; ITD 4.0 versus 5.75 samples. The aggregate passes, but its −5 dB scene worsens: **11.22 versus 10.29 dB target-ILD error**.
- Each seed bench contains **24 crowd mixtures, six per SNR**. Repeating those mixtures across training seeds does not increase material diversity. The merged CI bounds are an envelope of per-seed crop-bootstrap intervals, not a population CI.
- “Crowd k8–12” currently means draws with replacement from six interferer voices—approximately **4.6–5.3 distinct voices**, not 8–12 distinct speakers.
- White-noise SI-SDR passes, but white **vocoded ESTOI decreases in all three seeds**, mean −0.0594. That is a diagnostic concern, not an additional registered FAIL.
- “Complete evidence” is narrower than promotion readiness: the scorecard still omits quiet PESQ and streaming RTF, as already recorded in the [previous disposition](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen18/astra-review-disposition.md:30).

2. **Precise experiment order and acceptance criteria.**

The −5 dB movement meets the rationale for *considering* 48k. It does not compel running it first. The paired experiment costs 24k additional steps across both arms and directly tests the proposed recipe change while controlling the optimizer restart and schedule.

| Rank | Experiment | Decision rule |
|---|---|---|
| **1** | Corrected **A/B 12k continuations** from the same Gen19 seed-1 parent, keeping the registered optimizer protocol | Retain the registered final-checkpoint criterion: **B−A ≥+0.30 dB at −5 dB**, with **non-worsening −5 dB STOI**. Before launch, add explicit safeguards against material 0 dB or quiet regression. Acceptance advances B to scratch replication; it earns no KPI claim. |
| **2, if B passes** | **24k from scratch with crowd80**, then complete all three registered seeds | Compare against Gen19 at the same budget. Require a reproducible −5 dB improvement, non-worsening −5 dB STOI, and preservation of currently passing required rows. A claim of clearing the milestone requires the full scorecard to pass, including −5 dB ≥+1.5. If B fails rank 1, skip this experiment and retain legacy k. |
| **3** | **48k from scratch on the retained recipe**, with the cosine schedule preregistered over 48k | Screen against that recipe’s 24k final: **≥+0.30 dB additional −5 dB SI-SDR**, non-worsening −5 dB STOI, and no material 0 dB/quiet regression. Replicate across three seeds before a recipe or KPI claim. Describe it as a budget-and-schedule comparison. |
| **4 onward** | Compressed spectral auxiliary → SNR concentration → STOI auxiliary | One change at a time. Advance STOI earlier only if waveform improvements again coexist with intelligibility harm. |

For the proposed “material regression” safeguards, I would preregister **0.15 dB SI-SDR / 0.003 STOI at 0 dB**, plus quiet absolute SI-SDR ≥25 dB and quiet ΔSTOI ≥−0.02. These are proposed operational thresholds, not statistical significance tests.

Also report **A−parent and B−parent**. If both improve similarly, that supports additional optimization under the restart protocol; it supplies no evidence that changing k helped. If B wins mainly because A deteriorates, do not describe that as an absolute improvement.

The existing [Gen20 preregistration](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/prereg.md:14) correctly separates continuation screening from scratch replication. Note that `train9.py` requires `--init-from`; merely setting `--steps 24000` would still produce a continuation.

3. **Stage C evidence waits; methods shakedown can happen now.**

Under the current [KPI contract](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/KPI.md:8), all required rows must pass before Stage C evidence listening. The explicit exception is a father-only **“METHODS SHAKEDOWN — NOT EVIDENCE”** pilot, with clean-vocoded and oracle-vocoded controls. It can debug audibility, artifacts, task difficulty and headroom now.

This is a prospective project rule, not a scientific law that objective thresholds must always precede listening. I would preserve it rather than relax it after observing a near miss.

Before promotion, I would require the following confirmation package, frozen before evaluation:

- **Fresh objective material:** at least **12 new target speakers**, with four utterances each, evaluated at −5/0/+5/+10 dB—48 crowd mixtures per SNR. Use fresh interferer recordings and mixture seeds, with speaker and utterance disjointness from training, VAL, development benches and listening pilots. Preserve a replication stratum matching the existing six-voice sampling recipe; separately test genuinely distinct 8–12-voice crowds. Include competing speech, SSN, white and quiet controls.
- **Independent pass:** all three final checkpoints must meet the existing seed-mean thresholds on that fresh set alone. Do not pool development and confirmation results to rescue a failure. Report paired uncertainty clustered by speaker/utterance, alongside individual seeds and SNRs.
- **Fresh spatial confirmation:** evaluate all three checkpoint hashes on multiple contents with geometry crossed with SNR, including mirrored directions. Require the aggregate ILD/ITD gates and preregister hard-SNR no-harm checks so easy scenes cannot conceal the observed −5 dB deterioration.
- **Fresh listening material:** separate, untouched sentences; blinded system identities; balanced randomized lists; fixed familiarization; candidate, unprocessed-vocoded and classical-gate-vocoded comparisons; clean/oracle headroom controls. Avoid presenting the same sentence under several systems to the same listener. Preregister transcription scoring, sample size, meaningful improvement, quiet non-inferiority and stopping rules; treat clarity ratings as secondary.
- **Outstanding engineering checks:** quiet PESQ, final-weight causality, latency, measured CPU streaming RTF and limited listening exports.

The current [listening-pack builder](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/listening_pack.py:43) checks the older `bench_results.json` gate and regenerates fixed legacy crops. It needs candidate-hash binding, the current complete scorecard and a fresh-material manifest before producing evidence packs.

Even successful Stage C results establish a result for that listener and vocoder setup; they do not establish your son’s benefit. Vocoder studies explicitly identify differences between normal-hearing simulations and CI perception. [Sinha and Azadpour, 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11479273/)

4. **First concrete change: repair Gen20’s continuation RNG design before launching.**

At [train9.py:237](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/train9.py:237), the default seed restarts the parent’s mixture RNG. With the unchanged pool, legacy A consequently replays the parent’s initial training mixtures. I verified **four consecutive batches were bit-identical**. Crowd80 changes RNG consumption; only **one of its 32 clean targets** matched A in that check.

Use a **new, explicitly registered continuation-data seed shared by both arms**, then isolate randomness by example and purpose so target crop, SNR, quiet/SSN selection and shared interferer draws remain aligned when k changes. Verify that alignment before training.

In the same preparation, record parent hash, continuation seed, branch, actual k recipe and optimizer schedule; use branch-specific output paths. [The checkpoint writer currently records `gen19` and uniform k for both arms.](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/train9.py:208)

No files were edited.


## Disposition (muse-wonder-full-1.0, 2026-11-04)

Accepted in full:

1. **Arithmetic confirmed** by her independent recomputation from raw
   rows + checkpoint hashes. Interpretation limits recorded in
   results.md caveats: spatial is seed-1/4-scene with the -5 dB scene
   worsening (11.22 vs 10.29); "crowd k8-12" is ~4.6-5.3 distinct
   voices; white vocoded ESTOI falls in all seeds (-0.0594,
   diagnostic); quiet PESQ + streaming RTF still outstanding.
2. **Order: corrected Gen20 A/B pair first** (not 48k). 48k is rank 3,
   on whatever recipe Gen20 retains, judged as budget+schedule.
3. **Safeguards added to the Gen20 preregistration before launch:**
   B-A at 0 dB no worse than -0.15 dB SI-SDR / -0.003 STOI (VAL);
   quiet read on bench v2 finals (abs >=25, dSTOI >=-0.02); report
   A-parent and B-parent; a B win caused by A deteriorating is not
   an absolute improvement.
4. **RNG flaw fixed before any launch** (her finding #4, verified by
   her bit-identical-batch check): new registered continuation seed
   20261120 shared by both arms; per-example purpose-isolated
   substreams so clean target, SNR, quiet/SSN choice and interferer
   prefix are identical across arms - only k differs. Checkpoint
   metadata now records gen20, branch, parent hash, continuation
   seed and schedule (previously misrecorded gen19/uniform-k).
   Alignment covered by tests in research/gen20/test_train9.py.
5. **Stage C evidence: not yet.** Only the labelled METHODS
   SHAKEDOWN pilot is permitted now. Her fresh-material confirmation
   package (12 new target speakers, genuinely distinct 8-12-voice
   stratum, all-3-checkpoint spatial, fresh listening lists,
   PESQ/RTF, hash-bound listening pack) is adopted as the promotion
   gate and will be preregistered when a candidate passes all
   required rows. `promoted FALSE` stands.
