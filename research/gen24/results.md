# Gen 24 — narrower noisy-SNR sampling, seed-17 screen: FAIL (T0)

> Claude Opus 5.5, 2026-11-04 ~22:05.
> - Registration: [prereg.md](./prereg.md). Run 1 was stopped by the
>   holder at step ~100 (filed in `aborted_run1/`). Run 2 ran 20:20–21:57
>   under the same registration.
> - Judge: [judge_screen.py](./judge_screen.py) → [screen_s17.json](./screen_s17.json).
> - Provenance: the registered shared verifier (`1b1bf42…`) **PASS**.
> - Reviews: Muse ([muse-review-gen24.md](./muse-review-gen24.md)) and
>   Astra ([astra-review-gen24.md](./astra-review-gen24.md)).
> - Final checkpoint only. `promoted FALSE`.

**Verdict:** the screen fails. The SNR change is **not retained**, and
Gen 19 stays the baseline.

| # | Rule (candidate − same-seed Gen 19) | Value | Pass |
|---|---|---|---|
| 1 | −5 dB ΔSI-SDR ≥ +0.30 on BOTH panels | VAL **−0.212**, bench **−0.019** | ✗ |
| 2 | −5 dB ΔSTOI non-worsening | −0.0085 / −0.0014 | ✗ |
| 3 | 0 dB safeguard (≥ −0.15 dB / −0.003) | VAL **−0.296 / −0.0107**, bench −0.045 / −0.0043 | ✗ |
| 4 | Quiet | 36.4 dB / −0.0036 | ✓ |
| 5 | Other required rows | crowd +3.39 / +0.032 / +0.071 (CI lo > 0); SSN +6.29; white +0.27 | ✓ |
| 6 | Dev panel > 0 with ≥ 5/8 | +0.064, **4/8** | ✗ |

**Reading.**
- This variant did not help: 40% of noisy training items at −5 to
  −3 dB (vs 17.3%), same draws, plain SI-SDR, 24k scratch, seed 17.
- It made the easier 0 dB condition worse on VAL.
- The dev panel was mixed (5536 −0.83 vs 5895 +0.59).
- It does not show that hard-SNR exposure fails in general (other mixes,
  budgets, curricula or seeds), and it says nothing about listeners.

With Gen 20–23 and 25, this supports the holder's redirection: changes
that only reshuffle the same dry training data have not moved the wall.
The next experiment changes what the program hears (rooms, Gen 27).
