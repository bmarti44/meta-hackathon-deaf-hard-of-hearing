# Astra xhigh review of Gen 20 — verbatim + disposition

> Reviewer: Codex `gpt-6-astra`, reasoning xhigh, read-only, 2026-11-04.
> Standing holder rule: Astra review between generations. Full session
> log: /tmp/astra_gen20_review.txt at review time.

## Verbatim final answer

**The Gen20 null stands: retain legacy k and skip scratch crowd80. I would revise Gen21 to compare 48k from scratch against Gen19 plus 24k of continuation.** The evidence supports testing more optimization; it does not establish that scratch training is the better use of compute.

I checked the requested files, recomputed the bench deltas, and verified the parent and final checkpoint hashes. Both step-0 VAL records equal the parent’s final record at the stored precision.

The final arithmetic is:

| −5 dB metric | Parent seed 1 | A: legacy | B: crowd80 |
|---|---:|---:|---:|
| VAL ΔSI-SDR | 0.56 | 0.81 | 0.83 |
| VAL ΔSTOI | 0.009 | 0.016 | 0.014 |
| Bench ΔSI-SDR | 1.060392 | 1.122203 | 1.164864 |
| Bench ΔSTOI | 0.007319 | 0.008214 | 0.005723 |

Thus B−A fails both registered primary conditions. The 0 dB safeguards pass, and both quiet safeguards pass. One small reporting correction: **B’s bench −5 dB value rounds to 1.16, rather than 1.17.** Sources: [A log](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/weights/train_log_legacy_seed20261120.json:3682), [B log](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/weights/train_log_crowd80_seed20261120.json:3682), [A bench](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/benchv2_gen20a.json), [B bench](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/benchv2_gen20b.json).

There is no interim rescue. B−A at −5 dB VAL across 2/4/6/8/10/12k was **−0.34, +0.15, +0.04, +0.09, −0.02, +0.02 dB**. No logged checkpoint reached +0.30. Both arms had higher SI-SDR at 4k—A 1.11, B 1.26—than at the registered final. That cautions against extrapolating gains with training length; it does not authorize selecting those checkpoints retrospectively.

The bench’s small crowd advantage also lacks concentration at the hard SNR:

| SNR | Crowd B−A SI-SDR | Crowd B−A STOI |
|---|---:|---:|
| −5 dB | +0.0427 | −0.00249 |
| 0 dB | −0.0169 | +0.00070 |
| +5 dB | +0.0266 | +0.00088 |
| +10 dB | +0.1406 | +0.00152 |

At −5 dB, B beats A on three of six crops. Competing speech deteriorates by **0.6034 dB overall**, including −0.7359 at −5 dB and −1.3345 at +10 dB. None of this changes the retention decision.

I would narrow the interpretation in [results.md](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen20/results.md:26): **additional training under this restart protocol improved both arms similarly; crowd80 failed to deliver the registered benefit.** “Gained from the optimizer restart” is not isolated causally, and “nothing measurable” overstates a single-seed null. Extra updates, fresh mixtures, optimizer reset, and LR schedule changed together. Nor does this establish that training of *any* kind helps. A’s actual bench −5 dB improvement was **+0.0618 dB**; B’s was +0.1045.

For Gen21, I recommend the following preregistration.

| Arm | Training history | Learning-rate policy |
|---|---|---|
| **S48** | 48,000 updates from scratch | Fresh Adam; cosine **1e−3 → 1e−4 over all 48k**, without a restart |
| **R48** | Corresponding Gen19 24k parent + 24,000 additional updates | Fresh Adam; **250-update linear warm-up 3e−5 → 3e−4**, then cosine → **3e−5 at continuation update 24k** |

Freeze architecture, negative SI-SDR loss, train-clean-100 pool, legacy k, SNR/noise distributions, batch 8×2 s, clipping, and evaluation material.

For S48, with \(t\) completed updates, register  
\[
\eta(t)=10^{-4}+\frac{9\times10^{-4}}{2}\left[1+\cos(\pi t/48000)\right].
\]
Its LR at 24k is **5.5e−4**. That checkpoint is not equivalent to Gen19’s completed 24k schedule.

**Pair the data as well as the initialization histories.** Use seeds **20261117/18/19** and the original Gen19 batch generator for this schedule comparison. S48’s first 24k batches should reproduce the corresponding parent’s training stream. At S48 step 24k, clone its actual data RNG state into R48, so both arms receive identical batches for lifetime updates 24k–48k. R48 must not restart the parent’s data seed from its beginning. With k identical across arms, this preserves alignment without introducing another sampler change.

Use these decision rules:

- **Screen seed 20261117 first.** Finish both registered endpoints. Advance to seeds 18/19 if either arm improves final −5 dB VAL SI-SDR by **≥0.30 dB over its parent**, with non-worsening −5 dB STOI and passing safeguards. For seed 1, that means VAL SI-SDR **≥0.86** and STOI **≥0.009**. If neither qualifies, stop this experiment without claiming a population null.
- **Replicate both arms when the screen advances**, so strategy comparisons have three paired initialization histories. Require mean improvement over Gen19 of **≥0.30 dB on both VAL and bench at −5 dB**, non-worsening mean STOI there, and positive SI-SDR improvements in at least two of three seeds.
- **Keep the safeguards:** 0 dB degradation no greater than **0.15 dB SI-SDR / 0.003 STOI**, quiet absolute SI-SDR ≥25 dB and ΔSTOI ≥−0.02, and preservation of currently passing required rows.
- **Among qualifying arms, prefer scratch only for a material advantage over R48.** I propose preregistering **S48−R48 ≥0.15 dB at −5 dB on both VAL and bench seed means**, non-worsening STOI, and positive SI-SDR differences in at least two seeds. This is a proposed operational margin, not a significance test. If both qualify without that advantage, prefer continuation because it reuses the existing parents.
- **Separate progress from milestone clearance.** Gen19’s −5 dB seed means are VAL **0.7800** and bench **1.187654**. A +0.30 gain gives bench **1.487654**, still short of **1.5**. Milestone clearance requires the unchanged KPI contract and complete seed/spatial evidence; promotion still requires the adopted fresh-material and engineering gates.
- Evaluate VAL every 2k and retain unrounded per-example results with speaker identities. Save and bench the registered 24k/36k/48k checkpoints; use **48k finals only** for acceptance. Do not stop or select on interim peaks.

The Gen20 A arm is an important **36k historical efficiency reference**, but its +0.25 VAL gain is not a universal correction to subtract from a three-seed result. A scratch seed-1 result of 0.86 would meet the old +0.30 screen while beating A by only **0.05 dB**. That is weak justification for scratch’s additional cost; the matched R48 comparison supplies the missing evidence.

This design distinguishes:

- **S48−Gen19:** the combined longer-budget/longer-schedule effect.
- **R48−Gen19:** additional optimization under a specified restart policy.
- **S48−R48:** optimization-policy differences at the same total update budget and matched training examples.

It does **not** separately identify optimizer reset versus LR shape. A pure uninterrupted-extension control would need preserved Adam state—for example, Gen19’s schedule followed by 24k at its terminal LR. Existing [Gen19 checkpoints](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen19/train8.py:203) lack that state. I would not add that third arm unless the policy comparison makes the mechanistic question worth its cost. The proposed seed-1 screen costs **72k new updates**, using the existing parent.

If 48k still misses the milestone, **retain compressed spectral → SNR concentration → STOI auxiliary**, testing one change at the selected fixed training budget.

Compressed spectral remains a useful alternate training signal even when STOI passes; it is not solely an intelligibility repair. The previously proposed starting recipe is −SI-SDR + 5·L_CS, with 256/512/1024 STFTs, exponent 0.3, and 0.7 magnitude/0.3 complex weighting. Published waveform-enhancement results support testing compressed spectral losses, although they do not establish benefit for this model. [Dai et al., 2022](https://aclanthology.org/2022.rocling-1.13/)

SNR concentration remains second: the k-null says nothing decisive about SNR allocation. STOI auxiliary stays third because the retained arm’s hard-SNR guard now passes. Move it earlier if further waveform gains reproducibly bring back intelligibility harm.

**First concrete change:** prepare a Gen21 trainer with explicit scratch and restart modes, fixed schedule horizons, full optimizer/scheduler/RNG checkpoint state, and the paired-data handoff at 24k. Before launch, verify that R48 starts at its parent’s VAL result and receives the same next batch as S48, while S48 retains its optimizer state. Simply setting `train9.py --steps 48000` would train a continuation to **72k lifetime updates**, not produce the intended scratch run.

No files were edited.


## Disposition (muse-wonder-full-1.0, 2026-11-04)

Accepted. (1) Gen20 null stands; results.md wording narrowed to her
formulation and the bench @-5 dB B value corrected 1.17 -> 1.16
(double-rounding on my side; raw 1.164864). (2) Gen21 redesigned as
S48 (48k scratch, cosine over 48k) vs R48 (Gen19 parent + 24k restart)
with paired data via RNG-state handoff at S48 step 24k, seed-17 screen
first, her acceptance/safeguard numbers verbatim in
../gen21/prereg.md. (3) Trainer gains full optimizer/RNG checkpoint
state and per-example unrounded VAL records. Post-48k order retained:
compressed spectral -> SNR concentration -> STOI auxiliary.
