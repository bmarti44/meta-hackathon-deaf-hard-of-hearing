# Gen 22 pre-registration — 30 dB soft-capped SI-SDR training loss

> Claude Opus 5.5, 2026-11-04 ~13:10 EST; revised ~13:25 per Astra's
> pre-launch review ([astra-prelaunch-review.md](./astra-prelaunch-review.md)).
> Written before any Gen 22 training. Source of the change and decision rules: Astra's Gen21
> review, rank 1 ([../gen21/astra-review-gen21.md](../gen21/astra-review-gen21.md)).
> T0 in-silico only. `promoted FALSE`.

## Question

Does capping each example's training SI-SDR near 30 dB, so that
near-perfect (mostly quiet) examples stop dominating the globally
clipped gradient, lift crowd −5 dB performance? Astra's
frozen-weight diagnostic: quiet/noisy gradient-norm ratio
53×/37× in quiet-containing batches; clipping at norm 5 on
69–78% of late batches.

## The one change

`research/gen22/train11.py --loss cap30`: denominator
`error + 1e-3·power` in the training SI-SDR (Astra's code,
verbatim). Everything else is the Gen21 trainer: Gen19 batch
generator, model (602,510 params), batch 8×2 s, quiet 10%,
clip 5, Adam, schedules. Evaluation metrics stay uncapped.
Logging-only additions (uncapped SI-SDR beside the loss,
quiet/noisy gradient contributions every 500 steps via
`autograd.grad` before the real backward, rolling resumable
state every 2000 steps) do not touch the update path.

**Control validity (verified before registration):** with
`--loss sisdr` the trainer reproduces Gen19 seed-17's logged
loss and grad-norm bit-for-bit at every logged step 0–325 on
MPS (diagnostic firing at step 0), and a kill → `--resume`
from the step-300 state stays bit-identical through 425; after
the review fixes, a fresh run is again bit-identical through
step 200. Logs + re-check script: `research/gen22/smoke/`
(`parity_check.py`). Prefix parity does not prove a bit-identical
24k final; it shows the update path and data stream are Gen19's.
Tests: `research/gen22/test_train11.py` (cap saturates at
−30 dB, <0.01 dB change at ~0 dB, never below plain, `sisdr`
is the Gen19 objective, Gen19 batch stream replayed; CPU
uninterrupted-vs-resumed run bit-identical in weights, logs, LR
and VAL across a diagnostic boundary; changed budget/loss
refused) and `test_judge_screen.py` (provenance violations —
missing dev target, wrong dev hash, interim checkpoint, bench
hash mismatch, wrong policy — raise; failed CI bound FAILs).

## Policy (frozen by the Gen21 SELECTED policy, per Astra's table)

| Gen21 selected policy | Gen22 screen | Exact control |
|---|---|---|
| Neither | 24k scratch, cosine 1e-3→1e-4 over 24k | Gen19 final of the same seed |
| R48 | 24k restart from Gen19 parent + Gen21 RNG handoff | Gen21 R48 final, same seed |
| S48 | 48k scratch (~174 min/seed — not launchable today) | Gen21 S48 final, same seed |

`judge_screen.py` implements ONLY the 24k-scratch row (it refuses
other policies). If Gen21 selects R48 or S48, a dated addendum
plus a matching judge (control files, filenames, timing) is
committed and reviewed before any launch.

## Panels and readouts (final checkpoint only)

- **VAL** (8 items @−5 dB, fixed panel): unrounded per-item
  means from the train log. Control VAL for 24k scratch = the
  Gen19 parent's step-0 record in the Gen21 R48 log of the same
  seed (seed 17: 0.5641 dB / 0.0091 STOI @−5; 0 dB 4.1004 / 0.0798).
- **Bench v2** `--n-per-cell 6`: crowd @−5 / @0 paired vs
  `unproc`, quiet absolute SI-SDR and ΔSTOI, plus overall crowd,
  SSN and white rows. Control bench seed 17 =
  `bench_v2_gen19.json` (@−5 1.0604).
- **Expanded dev panel** (`gen21/dev_audit.py --system`,
  128 items @−5 / 0 dB, 8 targets, candidate vs control).

## Decision rules (Astra, verbatim numbers)

Screen seed 20261117. **ADVANCE** to seeds 18/19 only if all:
1. candidate − control ≥ **+0.30 dB at −5 dB on BOTH VAL and bench**;
2. −5 dB ΔSTOI non-worsening vs control on both panels;
3. 0 dB degradation ≤ 0.15 dB and ≤ 0.003 STOI on both panels;
4. quiet absolute SI-SDR ≥ 25 dB and quiet ΔSTOI ≥ −0.02;
5. other currently-passing required mono rows still pass on
   this seed's bench (crowd ΔSI-SDR ≥ 3.0, ΔSTOI ≥ 0.03,
   ΔACE-electro ≥ 0.05, each with 95% CI lower bound > 0;
   SSN ≥ 3.0; white ≥ 0);
6. dev panel @−5 dB: positive mean improvement over control,
   with ≥ 5 of 8 targets improving (exact registered 8 targets,
   16 paired items each; hashes must match the VAL/bench
   checkpoints).

**Confirmation** (seeds 18/19, controls Gen19 s18/s19 under the
24k-scratch policy): rules 1–5 on 3-seed means; candidate −
control positive in ≥ 2 of 3 seeds **on each of VAL and bench
@−5 dB**; dev panel: 3-seed mean gain > 0 and ≥ 5 of 8 targets
improving on their 3-seed mean per-target gain. Only then is
the cap retained into the recipe. If the screen fails, the cap
is filed as a NULL for this policy and Gen 23 tests rank 2
(compressed spectral 5·L_CS) under the same rules.

Not identified: whether gains come from the quiet/noisy
rebalancing specifically or from generally lower clipping;
the gradient-diagnostic log is descriptive only.

## Cost / timing

24k steps ≈ 76–85 min on MPS (Gen19 seed 17 took 84.8 min),
plus ~25 min for bench, dev panel, judging and filing. Astra's
guidance: launch by ~17:30 at the latest. Launch only after the Gen21 verdict
is filed and Astra's review of it is filed with a disposition
(holder rule). Today's deadline rule: launch the screen only if
it can train, bench and be filed by 19:30; otherwise this
registration plus the smoke evidence above is the filed next step.

Run:
`/tmp/gen9env/bin/python research/gen22/train11.py --loss cap30 --mode scratch --seed 20261117 > /tmp/gen22_cap30_s17.log 2>&1`
Judge: `research/gen22/judge_screen.py --seed 17`.
