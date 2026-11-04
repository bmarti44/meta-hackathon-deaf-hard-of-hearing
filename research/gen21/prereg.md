# Gen 21 pre-registration — S48 vs R48 at 48k lifetime updates

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Design + decision rules verbatim from Astra's Gen20 review
> ([../gen20/astra-review-gen20.md](../gen20/astra-review-gen20.md)).
> Written before any Gen21 training.

## Question

Does more optimization close the −5 dB crowd gap (Gen19 seed-mean
bench +1.19 vs required +1.5), and is 48k-from-scratch a better
use of compute than continuing the Gen19 parents for 24k?

## Arms (recipe frozen = Gen19; only the policy below varies)

| Arm | History | LR policy |
|---|---|---|
| S48 | 48k from scratch | Adam cosine 1e-3→1e-4 over 48k (LR@24k = 5.5e-4; its 24k ckpt ≠ Gen19) |
| R48 | Gen19 parent + 24k | Fresh Adam, 250-step warm-up 3e-5→3e-4, cosine→3e-5 at 24k |

Original Gen19 batch generator + seeds 20261117/18/19: S48's
first 24k batches replay the parent stream; at S48 step 24000
the data-RNG state is cloned into R48, so lifetime batches
24k–48k are identical across arms. Full optimizer/RNG state
saved at lifetime 24k/36k/48k. VAL every 2000, unrounded
per-example records retained. Bench 24k/36k/48k checkpoints;
**acceptance on 48k finals only** — no interim selection.

## Decision rules (Astra, verbatim numbers)

- **Screen seed 20261117 first**, both endpoints finished.
  Advance to seeds 18/19 if either arm's final VAL −5 dB SI-SDR
  improves ≥+0.30 over its parent (seed 1: ≥0.86) with −5 dB
  STOI ≥0.009 (non-worsening) and safeguards passing. If
  neither qualifies, stop without claiming a population null.
- **Replicate both arms** if the screen advances: require mean
  improvement over Gen19 ≥+0.30 dB on BOTH VAL and bench at
  −5 dB, non-worsening mean STOI, positive in ≥2/3 seeds.
- **Safeguards:** 0 dB degradation ≤0.15 dB / 0.003 STOI; quiet
  abs ≥25 dB and ΔSTOI ≥−0.02; currently-passing required rows
  preserved.
- **Prefer scratch only if** S48−R48 ≥0.15 dB at −5 dB on both
  VAL and bench seed means, non-worsening STOI, positive in
  ≥2 seeds; otherwise prefer continuation (reuses parents).
- Progress ≠ milestone: Gen19 −5 dB means are VAL 0.7800
  [annotated 2026-11-04 after the verdict: rounded; unrounded
  0.7808299135 — thresholds unchanged] /
  bench 1.187654; +0.30 still leaves bench at 1.488 < 1.5.
  Milestone needs the unchanged KPI contract (3 seeds +
  hash-matched spatial); promotion additionally needs the
  fresh-material + engineering gates. `promoted FALSE`.

Effects identified: S48−Gen19 (budget+schedule), R48−Gen19
(restart-policy extra optimization), S48−R48 (policy at matched
budget+examples). Optimizer-reset vs LR-shape is NOT separated.
Screen cost: 72k new updates (parent reused).
