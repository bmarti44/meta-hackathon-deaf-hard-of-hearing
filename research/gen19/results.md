# Gen 19 — 24k steps: first KPI-passing rows across the board (seed 1, T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-03.
> Pre-registered: [prereg.md](./prereg.md). One seed so far
> (20261117); scorecard verdict INCOMPLETE until seeds replicate.
> T0 only, no listener claim. `promoted FALSE`.

## Seed-1 KPI scorecard (bench v2 crowd) — 13 PASS / 1 FAIL

| KPI | Gen 19 s1 | Gen 18 seed-mean | Required |
|---|---|---|---|
| Crowd ΔSI-SDR | **+3.45** | +2.73 | ≥+3.0 ✓ |
| Crowd ΔSTOI | **+0.035** | +0.015 | ≥+0.03 ✓ |
| Crowd ΔACE electro | +0.069 | +0.053 | ≥+0.05 ✓ |
| Crowd @ −5 dB SI-SDR | +1.06 | +0.63 | ≥+1.5 ✗ |
| Crowd @ −5 dB STOI guard | +0.007 | — | ≥0 ✓ (first pass) |
| Crowd @ 0 dB | +4.58 | +3.9 | stretch ✓ |
| SSN / quiet | +6.43 / 37.3 abs | +5.36 / 30.1 | stretch ✓ |
| Competing ΔSI-SDR | +1.54 | +0.78 | (not gated mono) |

VAL trajectory (fixed panel): 0 dB +1.14 (500) → +3.12 (8k) →
+3.75 (12k) → +4.10 (24k); −5 dB −0.67 → +0.56 with STOI
−0.010 → +0.009. The 6k→8k flat window was schedule phase,
not convergence (Astra interim thresholds: material learning
at 12k confirmed). Training length was a binding constraint
at 6k steps; whether 48k helps is judged by 18k→24k VAL
movement (both SI-SDR and STOI improved — recorded for Astra).

## Remaining

Seeds 20261118/19 replicating; seed-mean verdict + Astra xhigh
review before Gen 20 (k-distribution per plan). The −5 dB
SI-SDR row is now the sole failing required KPI.
