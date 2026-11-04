# Astra xhigh interim review of Gen 21 (holder-requested) — verbatim + disposition

> Reviewer: Codex `gpt-6-astra`, reasoning xhigh, read-only, 2026-11-04,
> while S48 was at ~42.6k/48k. Full log: /tmp/astra_gen21_interim.txt.

## Verbatim final answer

**Let S48 finish, then finish R48. Nothing in the interim results justifies changing the registered schedules, endpoints, or advancement rule.** The core implementation is faithful; I found one checkpoint-retention omission and several workflow details worth fixing before R48 launches. No files were edited.

For the implementation audit:

- **S48 LR is correct.** The actual 24k state contains `T_max=48000`, scheduler epoch 24,000, Adam count 24,000, and LR **0.0005499999999998973**—the registered **5.5e−4**. The 36k state also has matching optimizer/scheduler counts and weights identical to its inference checkpoint. S48 retains Adam state throughout.
- **Handoff timing is correct.** Update 24,000 finishes, the scheduler advances, the checkpoint/state/handoff are saved, and only then does VAL run. Batch 24,001 is drawn on the next loop iteration. The handoff’s NumPy and Torch states exactly match the saved 24k state. [Save ordering](< /Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:319>)
- **Restart warm-up is correct under the completed-update convention.** LR is 3e−5 at initialization, 2.9892e−4 after 249 updates, 3e−4 after 250, then cosine-decays to 3e−5 after continuation update 24,000. Thus update 251 uses the peak LR. [Schedule]( /Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:299)
- **Checkpoint lifetime labels are correct.** Inference checkpoint `steps` and full-state `step` mean lifetime updates. JSON `steps` means updates in this invocation; `lifetime_steps` includes the parent. VAL records contain both. Training-loss stdout uses a zero-based loop index and reports the *post-update* LR: its `step: 24000` is already after update 24,001. That explains its slightly-below-0.00055 LR.
- **I found no current sampler divergence.** Gen19’s batch-generation code is unchanged. Speaker names and file lists are sorted. Cache hits, eviction and decoding consume no RNG; crops do not mutate cached audio. VAL owns a separate NumPy generator. The causality probe uses a private Torch generator, and the model has no stochastic forward operations. Restart does not restore the saved Torch RNG, but this does not affect this recipe’s data stream.

Both supplied tests passed. I additionally compared **three actual-corpus batches starting from the saved handoff** between train10 and train8: tensors, labels and resulting RNG states matched exactly despite cache differences and intervening Torch random draws. The current pool matches the parent’s speaker list and per-speaker file counts: **251 speakers, 28,539 files**. This is strong implementation evidence, although not a replay audit of all 24,000 historical batches.

Two qualifications prevent an unconditional “everything implemented” verdict:

1. **R48 never saves its initial lifetime-24k full state.** The save condition is inside the training loop, whose first restart lifetime count is 24,001. Its first full state will therefore be at 36k. The Gen19 parent supplies the 24k *weights*, but lacks the newly initialized Adam/scheduler state and restored continuation RNG. [Save condition](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:337)
2. Pairing still assumes unchanged corpus contents. The handoff asserts seed/step, but neither pins the ordered file-content manifest nor validates the parent’s seed/24k metadata. The inspected parent is correct, including hash `80000b64…f367`; preserve that provenance for the real restart launch.

The subsequent live VAL results are encouraging but variable. These are the **rounded stdout values**, with each pair showing ΔSI-SDR / ΔSTOI:

| S48 lifetime updates | −5 dB | 0 dB |
|---:|---:|---:|
| 24k | 0.74 / 0.007 | 4.19 / 0.085 |
| 26k | 0.33 / 0.005 | 4.44 / 0.087 |
| 28k | −0.17 / −0.003 | 4.41 / 0.088 |
| 30k | 0.80 / 0.016 | 4.28 / 0.089 |
| 32k | 1.12 / 0.013 | 4.67 / 0.098 |
| 34k | 0.98 / 0.013 | 4.66 / 0.090 |
| 36k | 0.86 / 0.013 | 4.53 / 0.091 |
| 38k | 0.84 / 0.017 | 4.58 / 0.095 |
| 40k | 1.22 / 0.028 | 4.79 / 0.100 |
| **42k** | **0.91 / 0.017** | **4.74 / 0.097** |

Source: [live training log](/tmp/gen21_s48.log:996). The latest training record I inspected was around 42.6k.

The 42k result clears the numerical screen cutoffs provisionally, and later 0 dB results comfortably preserve the parent’s performance. **Neither establishes final advancement.** Finish both endpoints; advance both arms to seeds 18/19 only if either **48k final** qualifies with safeguards. Quiet absolute SI-SDR and other bench safeguards remain unestablished by these VAL lines. The large negative quiet VAL *delta* is not the quiet *absolute* SI-SDR gate.

For the queued bench/judging workflow, use this explicit mapping. Filenames below share the seed suffix `20261117`.

| Lifetime | S48 weights | R48 weights |
|---:|---|---|
| 24k | `s48_seed20261117_step24000.pt` | Gen19 `causal_seed20261117.pt` |
| 36k | `s48_seed20261117_step36000.pt` | `r48_seed20261117_step36000.pt` |
| 48k | `s48_seed20261117.pt` | `r48_seed20261117.pt` |

In particular:

- R48’s lifetime-36k full state is **`r48_seed20261117_state_step36000.pt`**, created after **12k continuation updates**. Its stdout says `VAL step12000`. Its final stdout says `VAL step24000`, meaning lifetime 48k.
- Bench the registered **24k/36k/48k** checkpoints, retaining separate outputs. R48’s 24k parent bench can reuse the existing hash-matched result. Use **bench_v2**, the same **six crops per cell** as the parent, and `--babble-kind crowd` for the scorecard. Changing crop count changes the generated evaluation material.
- **Never submit the three checkpoints from one seed as three seeds.** The current scorecard checks three distinct checkpoint hashes, not distinct training seeds; it could incorrectly accept that input arrangement as complete evidence. Aggregate only one arm’s three **48k finals from seeds 17/18/19**. [Evidence check](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/bench-n6/kpi_scorecard.py:138)
- Judge unrounded final means, not printed values. There is a small preregistration precision ambiguity: the smoke’s raw parent is **0.5640785 / 0.0091386**, while the explicit registered screen is **0.86 / 0.009**. I would retain those explicit operational cutoffs and disclose exact parent differences, especially for a boundary result.
- Per-example VAL records currently remain in memory until the final JSON write. A crash—or failed post-training causality assertion—would lose those records despite surviving checkpoints. Incremental persistence would improve R48’s evidence retention. Also, saved full states do **not** imply an implemented resume command; `--init-from` performs a fresh restart. [Final log write](/Users/bmarti44/bufferright/research-deaf-hard-of-hearing/research/gen21/train10.py:353)

**First concrete change:** before R48 starts, save its initialized **lifetime-24k full state**, after restoring the handoff RNG and constructing fresh Adam/scheduler, before drawing its first batch. That closes the checkpoint-retention omission without changing the experiment. Keep S48 running and leave the registered training and acceptance plan intact.


## Disposition (muse-wonder-full-1.0, 2026-11-04, applied before R48 start)

1. **Plan unchanged**: S48 finishes, then R48; judgment on 48k finals
   only, explicit cutoffs 0.86 / 0.009 retained (raw parent
   0.5640785 / 0.0091386 disclosed at judging).
2. **First concrete change applied**: restart mode now saves its
   initialized lifetime-24k full state (fresh Adam/scheduler +
   restored handoff RNG) before the first batch. Smoke-verified;
   edit landed while S48 (already-loaded code) was unaffected.
3. Parent metadata now asserted (steps 24000, seed match).
4. Per-example VAL records persist incrementally
   (`*_val_partial.json` at every VAL eval) so a crash cannot lose them.
5. Judging workflow adopts her checkpoint map; bench_v2 n=6/cell,
   separate outputs per lifetime checkpoint; scorecard will only
   ever aggregate one arm's three 48k finals across seeds 17/18/19
   (never three checkpoints of one seed).
