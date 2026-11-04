# Astra xhigh review of Gen 21 screen + training evaluation — verbatim + disposition

> Reviewer: Codex `gpt-6-astra`, reasoning xhigh, read-only, 2026-11-04
> (between-generation standing rule + holder request for training
> recommendations). Full log: /tmp/astra_gen21_review.txt.

## Verbatim final answer

**Both arms correctly ADVANCE under the registered screen. I recommend completing both arms’ seeds 18/19 without changing Gen21.** However, the evidence does change my next training recommendation: **test softly capped SI-SDR first, then compressed spectral → SNR concentration → STOI auxiliary.** A supplementary gradient diagnostic found a concrete problem with the current loss.

I read the requested files, recomputed the item/row comparisons, and verified all six bench checkpoint hashes against the actual weights. No files were edited or optimizer updates performed.

**The VAL–bench divergence is partly concentration and partly a genuine decline on the sampled material. Its population causes cannot be separated with these panels.**

The final arithmetic is:

| Arm | VAL −5 dB ΔSI-SDR / ΔSTOI | SI-SDR gain over parent | Bench −5 dB ΔSI-SDR / ΔSTOI | SI-SDR gain over parent |
|---|---:|---:|---:|---:|
| S48 | 1.004963 / 0.018360 | +0.440885 | 0.933703 / 0.005500 | −0.126689 |
| R48 | 0.880019 / 0.014586 | +0.315940 | 1.198350 / 0.011193 | +0.137958 |

Both clear even the stricter interpretation of the screen: raw parent VAL +0.30, with genuinely non-worsening STOI—not merely the rounded 0.86/0.009 cutoffs. The supplied mono safeguards pass: 0 dB improves, quiet reaches 42.78/42.63 dB, and the other required mono thresholds remain satisfied. This does not establish Gen21 spatial or full KPI clearance. [Registered rules](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/prereg.md:29)

There is an important correction to the concentration interpretation: **R48’s absolute performance is concentrated in 5536, but its improvement over the parent is reasonably balanced.**

| VAL target | Parent | S48 36k | S48 48k | R48 36k | R48 48k |
|---|---:|---:|---:|---:|---:|
| 5536 | 1.134 | 1.499 | 1.903 | 1.437 | 1.479 |
| 5694 | −0.005 | 0.223 | 0.107 | 0.421 | 0.281 |

These are −5 dB ΔSI-SDR means over four items per speaker.

- **S48 versus parent:** gains +0.770 for 5536 and +0.112 for 5694. Thus 5536 supplies **87.3%** of the aggregate gain. STOI changes are +0.01867 and −0.00023.
- **R48 versus parent:** gains +0.345 and +0.286; 5536 supplies **54.7%**. STOI improves for both speakers, although 5694 remains negative relative to unprocessed speech.
- **S48 36k→48k:** 5536 improves +0.405 dB/+0.01737 STOI, while 5694 declines −0.117 dB/−0.00725 STOI. Their average conceals that split.

Moreover, 5694’s negative mean STOI is driven by **one particularly bad item, index 20**: S48 ends at −2.314 dB/−0.1435 STOI. Its other three items have positive ΔSTOI. These observations identify problematic mixtures; they do not establish a speaker-wide failure. Sources: [S48 items](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_s48_seed20261117.json), [R48 items and raw parent](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/weights/train_log_r48_seed20261117.json).

On bench, S48’s late decline is broader:

| Bench target, one −5 dB mixture each | S48 36k→48k SI-SDR change | STOI change |
|---|---:|---:|
| 1988 | −0.309 | −0.00199 |
| 1993 | −0.871 | −0.01820 |
| 5895 | +0.337 | −0.00334 |
| 6241 | −0.717 | −0.01177 |
| 6295 | −0.080 | +0.00090 |
| 6313 | +0.079 | +0.00484 |
| **Mean** | **−0.260** | **−0.00493** |

Four of six mixtures worsen on each metric. Removing any one mixture leaves the SI-SDR decline between **−0.380 and −0.138 dB**. The decline also appears in post-selection ACE correlation and vocoded ESTOI. R48’s corresponding SI-SDR decline is much smaller, −0.0455 dB, with essentially unchanged mean STOI. [36k rows](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/benchv2_g21s48_36k.json), [48k rows](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/benchv2_g21s48_48k.json)

**This is not noise caused by drawing different evaluation mixtures at different checkpoints.** The panels are fixed, and bench unprocessed SI-SDR/STOI values match exactly across all six files. The checkpoint changes really produce these changes on those mixtures.

What remains uncertain is generalization. Descriptive paired-bootstrap 95% intervals over the six bench mixtures are:

- S48 final minus parent: **[−0.562, +0.270] dB**.
- R48 final minus parent: **[−0.039, +0.323] dB**.
- S48 48k minus 36k: **[−0.594, +0.074] dB**.

These tiny-panel intervals are not population evidence. Bench has one mixture per target at each SNR, so speaker, utterance and mixture effects are confounded. Its absolute performance is concentrated too: removing the 5895 mixture reduces parent/S48/R48 means to **0.479/0.241/0.565 dB**.

Before or alongside replication, I recommend a **separate development audit**: the existing eight VAL/bench targets × four target crops × four independently sampled interferer mixtures, at −5 and 0 dB. Evaluate parent, both 36k checkpoints and both finals on the identical crossed material. This can estimate mixture variability within target content. Preserve the registered panel and keep the eventual fresh confirmation speakers untouched.

**Replication still has a useful, narrower question to answer.**

I would keep both arms because neither three-seed acceptance criterion is mathematically settled, and dropping S48 would abandon the registered paired policy comparison. The remaining work is approximately **8.9 hours** at the observed runtimes.

To attain +0.30 seed-mean improvement, seeds 18/19 must average:

| Arm | Required remaining mean VAL gain over corresponding parents | Required remaining mean bench gain |
|---|---:|---:|
| S48 | +0.230 dB | **+0.513 dB** |
| R48 | +0.292 dB | **+0.381 dB** |

S48 is clearly the less promising hard-SNR candidate. Its seed-1 bench STOI also declines versus parent, so subsequent seeds must compensate for that.

For scratch preference, the remaining two seeds must average **S48−R48 ≥+0.163 dB on VAL and ≥+0.357 dB on bench**, plus the registered STOI and sign conditions. Seed 1 supplies no material scratch advantage.

Seed 1 already settles these narrower points:

- Neither final demonstrates the required joint +0.30 VAL-and-bench improvement for this seed.
- S48 final regresses on this bench’s hard-SNR mean.
- No benched interim checkpoint rescues the +0.30 bench criterion either: the largest gain is R48@36k, approximately +0.183 dB.
- Selecting 36k or a VAL peak retrospectively is unjustified.

Replication can decide reproducibility across training histories and the registered seed-mean policy choice. **It cannot turn six repeated mixtures into a broader material sample**, isolate optimizer reset from LR shape, or establish listener benefit. If neither arm qualifies, retain Gen19 as the accepted baseline; “otherwise prefer continuation” should not become automatic acceptance of a failed R48.

**For training, the strongest new evidence concerns gradient allocation.**

The current objective averages per-example logarithmic SI-SDR losses. Equal averaging does not imply equal gradient contributions. As an example becomes nearly perfectly reconstructed, the residual-energy denominator becomes small and its gradients can become large.

The logs show clipping at norm 5 on **69% of logged S48 batches and 78% of R48 batches during the last 12k updates**. I then ran a frozen-weight diagnostic on **16 newly generated training batches**, using data seed **20261122**, batch 8×2 s, on CPU. Ten batches contained quiet examples. I differentiated the quiet and noisy contributions separately, each retaining the actual `/8` batch weighting.

| Final model | Median quiet/noisy gradient-norm ratio in quiet-containing batches | Median full gradient norm | With proposed 30 dB soft cap |
|---|---:|---:|---:|
| S48 | **53.2×** | 242.2 | 11.8 |
| R48 | **36.6×** | 174.1 | 8.6 |

These are parameter gradients, not just loss magnitudes. The cap still leaves clipping; it substantially changes the imbalance. The parent shows the same problem, though less severely than S48.

This supplies a specific mechanism worth testing: **excellent quiet reconstruction can dominate a mixed batch and cause global clipping to attenuate its noisy-example contribution.** Quiet occurs in about 57% of batch-8 draws despite being only 10% of examples. This diagnostic establishes local gradient behavior, not that the cap will improve trained performance.

Other likely contributors, with weaker causal evidence, are:

- **Hard-SNR allocation:** only 17.3% of noisy examples lie in [−5,−3] dB. Including quiet/noise-kind probabilities, only **10.92% of all examples** are babble in that interval: 0.874 per batch, with **39.6% of batches containing none**. Requiring k≥8 raises the empty-batch probability to 66.5%. Thus “60% hard-SNR sampling” overstates exposure near −5.
- **Objective geometry:** waveform SI-SDR gives no explicit frequency-band balance or temporal-envelope objective. Compressed spectral supervision remains plausible, but its benefit to the specific SI-SDR wall is unproven.
- **Crop/context mismatch:** training resets on 2 s crops; evaluation uses 4 s. The TCN’s nominal convolutional context is approximately 1.02 s, so startup occupies a substantial training fraction. Cumulative normalization also carries past statistics; the entire model is not strictly limited to a 1.02 s dependency. [Architecture](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen15/model_causal.py:34)
- **Babble structure:** evaluation’s 8–12 draws from six voices produce approximately 4.6–5.3 distinct identities. Training has 250 eligible interferer identities per target, so its high-k mixtures have far fewer repeated identities. Gen20 tested k allocation, not this identity-repetition difference. Its null and competing-speech deterioration argue against another immediate k increase.
- **Capacity:** 602,510 parameters and the existing context may constrain separation, but the present evidence does not identify capacity as the binding limit. A larger batch likewise does not fix systematic gradient imbalance.

**My ranked experimental plan is below.** Each change is tested separately and retained only after passing its own comparison.

For the nonarchitectural screens, freeze the budget/policy selected by Gen21:

- R48 selected: **24k continuation** from the corresponding Gen19 parent, using the registered restart schedule.
- S48 selected: **48k scratch** with its registered schedule.
- Neither qualifies: **24k scratch**, against Gen19’s recipe and schedule.

Screen seed **20261117**, then replicate promising candidates on **18/19**. Reuse existing controls only when initialization, data stream and policy match exactly. Judge registered finals; 2k evaluations are diagnostics, not checkpoint selection.

Except for the explicitly intelligibility-focused fourth experiment, require **candidate−control ≥+0.30 dB at −5 on both VAL and bench**, non-worsening −5 STOI, and the existing 0 dB/quiet/other-required-row safeguards. Confirmation requires the same seed-mean bars and positive changes in at least two seeds. For these future experiments, also preregister positive mean improvement on the expanded development panel, supported by at least five of its eight targets.

1. **Softly cap training SI-SDR at 30 dB.**

   Change only the loss denominator as shown below. Keep quiet probability, clipping, batch, sampler and schedule fixed. This directly tests the observed excessive gradient contribution from already well-reconstructed examples.

   Use the shared one-seed final-budget screen and subsequent two-seed replication. Log ordinary SI-SDR alongside capped loss and occasional quiet/noisy gradient contributions. Evaluation metrics remain uncapped.

   Soft thresholds have been used to prevent easy examples dominating SDR-family training; applying the threshold to this scale-invariant projection formulation is the proposed experiment here. [Wisdom et al., NeurIPS 2020](https://papers.nips.cc/paper/2020/file/28538c394c36e4d5ea8ff5ad60562a93-Paper.pdf)

2. **Add compressed spectral supervision.**

   To the retained objective, add **5·L_CS**: average across Hann STFTs of **256/512/1024 samples**, hops **64/128/256**, `center=False`, normalized transforms; compression exponent **0.3**; **0.7 magnitude MSE + 0.3 compressed-complex MSE**, with mean reductions and a fixed numerical floor. Compare output against the same delayed clean target.

   This addresses spectral-detail errors that waveform fitting may underweight. Use the same screen, seeds and +0.30 acceptance bar. Log the two losses and their gradient contributions separately.

   Gen16 does **not** establish a general auxiliary-loss null: it combined two different terms, used a pre-selection log-envelope objective, and trained one seed for only 2k updates. It does caution against adding several objectives together. Published compressed-loss results support testing this approach, but their quality gains do not guarantee better SI-SDR. [Braun and Tashev](https://arxiv.org/pdf/2009.12286)

3. **Concentrate noisy SNRs more narrowly.**

   Replace the noisy-example distribution with **60% U(−5,−2) + 40% U(−2,10)**. Preserve quiet 10%, babble/SSN 70/30 and legacy k. Map the same random draws to the new intervals so targets and underlying noise waveforms remain paired.

   This raises [−5,−3] exposure from 17.3% to **40% of noisy examples**, approximately 2.3×. It tests insufficient hard-region exposure independently of k or loss changes.

   Use the shared fixed-budget screen and acceptance bar; the 0 dB safeguards are particularly important. Gen20’s k-null gives no reason to skip this experiment.

4. **Add a differentiable STOI auxiliary only after those tests, unless intelligibility harm becomes reproducible.**

   Add **10·(1−STOI_diff)** to the retained objective, using aligned signals and a validated differentiable implementation. Retain the waveform objective.

   Use the same steps and seeds. For acceptance as an *intelligibility repair*, require **≥+0.005 STOI at −5 on both panels**, non-worsening SI-SDR, and the existing safeguards. This does not substitute for the SI-SDR milestone.

   I would not move this ahead of spectral/SNR work yet: aggregate hard-SNR STOI passes, and S48’s late bench SI-SDR and STOI deteriorate together. Direct STOI optimization is also not assured to outperform spectral objectives. [Kolbæk et al.](https://arxiv.org/abs/1802.00604)

5. **Then test longer crops before enlarging the model.**

   Change **2 s→4 s**, retaining batch 8, architecture, objective and update schedule. Use the same seed screen and +0.30 bar. This tests startup/normalization mismatch and longer examples; it also doubles audio exposure and approximately doubles training work, so describe the effect accordingly.

   Increasing batch size or receptive field should be a separate later experiment. Neither currently has evidence strong enough to precede the cheaper objective and sampling tests.

**The first concrete training change is therefore this proposed replacement inside the next candidate trainer’s SI-SDR loss:**

```python
power = (proj * proj).sum(-1)
error = (noise * noise).sum(-1)
ratio = power / (error + 1e-3 * power + eps)
return -10.0 * torch.log10(ratio + eps)
```

This smoothly limits the training score near 30 dB while barely changing the loss at poor reconstruction levels. It adds no inference cost.

Run the expanded diagnostic evaluation before or alongside Gen21 replication. **Finish Gen21’s original training arms before launching these recipe changes.** The gradient diagnostic above is already complete; the proposed capped-loss training experiment has not been run.


## Disposition (muse-wonder-full-1.0, 2026-11-04)

1. **Replication launched unchanged**: seeds 18/19, both arms,
   sequential (~8.9 h). Registered acceptance unchanged (seed-mean
   >=+0.30 on BOTH VAL and bench @-5 dB, safeguards, >=2/3 seeds
   positive; scratch preference >=0.15 both panels). If neither
   arm qualifies, Gen19 stays the accepted baseline - a failed R48
   is NOT auto-accepted.
2. Correction adopted: R48's VAL improvement over parent is
   balanced across speakers (54.7% from 5536); only S48's gain is
   concentrated (87.3%). results.md amended.
3. **Expanded development diagnostic** (8 targets x 4 crops x 4
   mixtures @-5/0 dB; parent + both 36k + both finals) built as
   research/gen21/dev_audit.py and run alongside replication;
   registered panels untouched, confirmation speakers unused.
4. **Training plan after Gen21 replication** (her ranking, each
   one change, seed-17 screen then 18/19, +0.30 both-panels bar):
   (1) 30 dB soft-capped SI-SDR loss - her gradient diagnostic
   (quiet/noisy grad-norm ratio 53x/37x; clipping 69-78% of late
   batches) is the strongest mechanistic lead in the programme;
   (2) compressed spectral 5*L_CS (256/512/1024, exp 0.3,
   0.7 mag/0.3 complex); (3) SNR concentration 60% U(-5,-2) +
   40% U(-2,10), paired draws; (4) STOI auxiliary 10*(1-STOI)
   only as intelligibility repair; (5) 4 s crops. Budget/policy
   for screens = whichever Gen21 selects (R48->24k continuation,
   S48->48k scratch, neither->24k scratch).
