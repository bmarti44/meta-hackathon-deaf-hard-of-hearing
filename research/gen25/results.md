# Gen 25 — weight averaging of Gen 19's last 9 checkpoints, seed-17 screen: FAIL (T0)

> Claude Opus 5.5, 2026-11-04 ~20:55.
> - Pre-registered: [prereg.md](./prereg.md), revised after
>   [astra-prelaunch-review.md](./astra-prelaunch-review.md) and before
>   any candidate was built.
> - Judge: [judge_screen.py](./judge_screen.py) →
>   [screen_s17.json](./screen_s17.json).
> - Provenance: [verify_provenance_g25.py](./verify_provenance_g25.py)
>   **PASS**, including every input matching the committed manifest and
>   the saved weights equalling the 9-input average bit-exactly.
> - VAL parity guard: max diffs 6.5e-6 dB and 3.2e-8 STOI.
> - Reviews: Muse ([muse-review-gen25.md](./muse-review-gen25.md)) and
>   Astra ([astra-review-gen25.md](./astra-review-gen25.md)).
>
> No training, no selection. `promoted FALSE`.

**Verdict:** the screen fails. The averaged weights are **not retained**
and are not used as a parent; the Gen 19 final (`80000b64…`) stays the
baseline.

| # | Rule (candidate − same-seed Gen 19) | Value | Pass |
|---|---|---|---|
| 1 | −5 dB ΔSI-SDR ≥ +0.30 on BOTH panels | VAL **+0.171**, bench **+0.030** | ✗ |
| 2 | −5 dB ΔSTOI non-worsening, both panels | VAL +0.0005, bench **−0.0010** | ✗ |
| 3 | 0 dB safeguard | VAL +0.092 / +0.0029; bench +0.054 / +0.0005 | ✓ |
| 4 | Quiet abs ≥ 25 dB, ΔSTOI ≥ −0.02 | 39.2 dB / −0.0030 | ✓ |
| 5 | Other required rows | crowd +3.47 / +0.035 / +0.070 (CI lo > 0); SSN +6.45; white +0.29 | ✓ |
| 6 | Dev panel > 0, ≥ 5/8 targets | +0.100 dB, 7/8 | ✓ |

**Reading (descriptive only).**
- Averaging gave small, broad improvements on this seed: dev +0.100 with
  7 of 8 voices, positive 0 dB gains, quiet +1.91 dB over Gen 19
  (37.27 → 39.18 dB), and white +0.089 dB over Gen 19 (+0.196 → +0.286).
- Checkpoint averaging was expected to give a few tenths of a dB at most
  (prereg), and that is what it gave. It does not approach the +0.30 bar
  or the +0.312 needed for the −5 dB KPI.
- It is one seed. It is not efficacy evidence and not a reason to retain
  or reuse these weights. No alternative windows will be tried.

**Next (per both reviews):** register a larger development panel, with
separate tuning material and training-disjoint voices, before Gen 26 (a
fixed α=0.5 midpoint of Gen 19 and Gen 21-R48). Gen 19's original
scorecard stays unchanged.
