# Gen 22 — 30 dB soft-capped SI-SDR, seed-17 screen: FAIL (T0)

> Claude Opus 5.5, 2026-11-04. Pre-registered: [prereg.md](./prereg.md).
> Pre-launch review: [astra-prelaunch-review.md](./astra-prelaunch-review.md).
> Screen review: [astra-review-gen22-screen.md](./astra-review-gen22-screen.md).
> Judge: [judge_screen.py](./judge_screen.py) → [screen_s17.json](./screen_s17.json).
> Final checkpoint only. `promoted FALSE`.

**Verdict:** the single-seed (20261117), 24k-scratch screen failed the
benefit criterion, so the cap is **not retained** and Gen 19 stays the
baseline. This is the registered non-advancement label ("NULL for this
policy"). It does not establish equivalence, zero effect across seeds,
or anything about other cap thresholds or budgets.

**Run and provenance.**

- Launched 15:45:55; ran 90.9 min with no interruption.
- Final `cap30_scratch_seed20261117.pt` sha `227f00a0…a9e5`.
- The same hash appears in the train log, the bench and the dev rows.
- Control: Gen 19 seed-17 final `80000b64…`.
- Exact causality was re-verified after training.

## Registered rules (candidate − same-seed Gen 19)

| # | Rule | Value | Pass |
|---|---|---|---|
| 1 | −5 dB ΔSI-SDR ≥ +0.30 on BOTH panels | VAL **+0.149**, bench **−0.010** | **✗** |
| 2 | −5 dB ΔSTOI non-worsening, both panels | +0.0001 / +0.0008 | ✓ |
| 3 | 0 dB loss ≤ 0.15 dB / 0.003 STOI | VAL +0.063 / +0.0014; bench +0.055 / +0.0039 | ✓ |
| 4 | Quiet abs SI-SDR ≥ 25 dB, ΔSTOI ≥ −0.02 | 35.8 dB / −0.0028 | ✓ |
| 5 | Other required mono rows still pass | crowd +3.48 / +0.037 / +0.070 (CI lo 2.71 / 0.025 / 0.049); SSN +6.50; white +0.06 | ✓ |
| 6 | Dev panel: mean gain > 0, ≥ 5/8 targets improve | +0.076 dB, 6/8 | ✓ |

Absolute −5 dB levels:

| Panel | cap30 | Gen 19 |
|---|---|---|
| VAL | 0.7131 | 0.5641 |
| Bench | 1.0507 | 1.0604 |

Overall crowd on this seed: +3.48 vs +3.45 for Gen 19. White
SI-SDR: +0.06 vs +0.20.

## What the trajectory and diagnostics show (descriptive, no decision role)

The VAL −5 dB trajectory tracks Gen 19's same-seed trajectory closely
at every 2k checkpoint. Examples:

| Step | cap30 (dB) | Gen 19 (dB) |
|---|---|---|
| 12k | 0.555 | 0.60 |
| 20k | 0.763 | 0.69 |
| 24k | 0.713 | 0.56 |

The cap changed little about where training went.

From [diag_summary.py](./diag_summary.py) and Astra's recomputation:

- **Clipping frequency** in the late half was similar: 66.7% (Gen 19)
  vs 67.3% (cap30) of 480 logged steps.
- **Clipping severity** fell: the median pre-clip norm went
  34.28 → 14.92, and the median clip multiplier 0.146 → 0.335.
- **The in-training quiet/noisy gradient-norm ratio** was 4.9× / 4.8× /
  6.4× over 0–8k / 8k–16k / 16k–24k. That is from only 11 / 9 / 9
  quiet-containing diagnostic batches, and Gen 19 has no matching
  in-training baseline.
- **The earlier 37–53× frozen-weight figures** came from different
  checkpoints and batches. They are not a paired baseline.

**Reading.** The result weakens the claim that *this* cap fixes the
hard-SNR failure. It neither falsifies the gradient-imbalance
hypothesis nor establishes it as the bottleneck.

Per the prereg, Gen 23 tests rank 2: plain SI-SDR + 5 × compressed
spectral loss, under the same rules
([../gen23/prereg.md](../gen23/prereg.md)).
