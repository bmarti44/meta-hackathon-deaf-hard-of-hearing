# Gen 19 — 24k steps: 13/14 KPIs pass seed-mean, one row left (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Pre-registered: [prereg.md](./prereg.md). Three seeds complete
> (20261117/18/19), final-checkpoint rule, hash-matched spatial.
> T0 only, no listener claim. `promoted FALSE` pending Astra
> review + Stage C protocol gates (fresh-material rule).

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

## Seed-mean verdict (3 seeds, complete evidence)

Crowd ΔSI-SDR **+3.51** [3.45/3.57/3.53], ΔSTOI **+0.035**,
ΔACE electro **+0.072**, @0 dB +4.65 (stretch), @−5 dB STOI
guard +0.005 ✓, SSN +6.45, white +0.73, quiet 36.3 abs,
spatial target-ILD 5.47 < 5.96 ✓. **Sole FAIL: crowd
ΔSI-SDR @ −5 dB +1.19 vs required +1.5.** Scorecard verdict:
FAIL (complete evidence — first non-INCOMPLETE verdict).
Competing talkers +1.45 mean SI-SDR, STOI ≈ 0 (not gated).

## Remaining

Astra xhigh review (standing rule), then Gen 20 per plan
(k-distribution 80% k8–12 via paired continuations) aimed at
the −5 dB row. Stage C listening requires ALL required rows
plus fresh-material replication — not earned yet.
