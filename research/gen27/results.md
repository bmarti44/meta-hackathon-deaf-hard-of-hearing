# Gen 27 — room augmentation, seed-17 screen: FAIL (helped in rooms, cost on dry speech) (T0)

> Claude Opus 5.5, 2026-11-04 ~23:25.
> - Registration: [prereg.md](./prereg.md) (S1–S10).
> - Reviews: [pre-launch](./astra-prelaunch-review.md),
>   [verification](./astra-verification-reviews.md),
>   [Astra result](./astra-review-gen27.md), [Muse result](./muse-review-gen27.md).
> - Judge: `judge_v3.py` → [screen_s17.json](./screen_s17.json).
> - Final checkpoint `weights/aug50_seed20261117.pt`, 24k steps; training
>   took 48 min.
> - `promoted FALSE`.

**Verdict:** FAIL. R1a–c, C, T and S2 pass; **D, S3 and SP fail**. Gen 19
remains the baseline.

| Gate | Result | Pass |
|---|---|---|
| R1a primary: reverberant gain vs Gen 19 (6 held-out synthetic rooms × −5/0 dB) | **+0.514 dB** | ✓ |
| R1b voice + room bootstrap 95% CI lower bound > 0 | [+0.238, +0.844] | ✓ |
| R1c ≥ 10/16 voices improve | 15/16 | ✓ |
| C every source-type × SNR cell ≥ 0 | synthetic −5/0: +0.509/+0.518 dB; measured −5/0: +0.154/+0.191 dB (STOI ≥ 0 in each aggregate cell) | ✓ |
| T target-only non-worsening vs Gen 19 | synthetic +2.047 dB / +0.054; measured +0.914 dB / +0.034 | ✓ |
| D dry screen-v2 non-worsening | −5 dB: −0.228 dB / −0.010; 0 dB: −0.492 dB / −0.010 | **✗** |
| S2 quiet | 37.4 dB / −0.0017 | ✓ |
| S3 other dry bench rows | crowd ΔSTOI 0.02903 vs ≥ 0.03 (missed by 0.00097); the other rows pass | **✗** |
| SP spatial | existing and hard-SNR pass; mirrored subsets +0.069 dB ILD / +0.125 samples ITD worse | **✗** |

**Reading** (Astra's qualifications adopted):
- Room augmentation helped on this seed's reverberant development panel,
  at a cost on dry noisy speech.
- "All strata positive" means all four aggregate source-type × SNR cells.
  Measured-room gains are smaller, 5 of 6 measured rooms lose a little
  STOI at −5 dB, and the AIR room loses SI-SDR at 0 dB.
- Target-only performance improves vs Gen 19 (which degraded reverberant
  clean speech), but stays slightly below bypass (about −0.07 / −0.25 dB).
- The CI supports a positive gain. It does not establish a gain above
  +0.30 dB with 95% confidence, nor seed-to-seed robustness.
- No universal room benefit, no necessary room–dry trade-off, and no
  listener benefit is established.

**Descriptive:** on the original dry bench, crowd at −5 dB scored +1.150
(Gen 19 seed 17: +1.060).

**Next: Gen 28**, both reviewers' choice. Halve the reverberant share
(P = 0.25 → 67.5 / 22.5 / 10) with everything else frozen and the same
gates.
