# Gen 21 screen (seed 20261117) — both arms advance on VAL; bench −5 dB diverges (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Pre-registered: [prereg.md](./prereg.md); interim audit:
> [astra-interim-review.md](./astra-interim-review.md). Screen only —
> no KPI claim until 3-seed replication. `promoted FALSE`.

## Unrounded VAL finals (48k lifetime; cutoffs 0.86 / 0.009)

Parent raw (R48 step 0): −5 dB 0.5641/0.0091, 0 dB 4.1004/0.0798.

| Arm | −5 dB ΔSI-SDR/ΔSTOI | Δparent | 0 dB | Screen |
|---|---|---|---|---|
| S48 `33c15254…eaa7` | 1.0050/0.0184 | +0.4409/+0.0092 | 4.7726/0.0988 | ADVANCE |
| R48 `32c6898b…41d` | 0.8800/0.0146 | +0.3159/+0.0054 | 4.4620/0.0881 | ADVANCE |

0 dB safeguards pass both. S48−R48 at −5 dB: +0.1249 dB
(below the 0.15 scratch-preference margin; seed-mean rule
applies after replication). **Per-speaker caveat (corrected per
Astra review):** absolute −5 dB VAL levels are higher on target
5536 (S48 1.903, R48 1.479) than 5694 (0.107/0.281), but the
*gain over parent* is concentrated only for S48 (87.3% from
5536); R48's gain is balanced (+0.345/+0.286, 54.7%). 5694's
negative mean ΔSTOI is driven by one bad item (idx 20).

## Bench v2 (n=6/cell, seed-1 vs Gen19 seed-1 parent)

| Ckpt | Crowd ΔSI-SDR/ΔSTOI | Crowd @−5 dB | @0 dB | Quiet abs/ΔSTOI | Comp |
|---|---|---|---|---|---|
| Gen19 parent | +3.45/+0.035 | +1.06/+0.007 | +4.58 | 37.3/−0.004 | +1.54 |
| S48 @24k | +3.54/+0.039 | +1.18/+0.011 | +4.64 | 32.1/−0.006 | +1.60 |
| S48 @36k | +3.74/+0.042 | +1.19/+0.010 | +4.96 | 37.1/−0.004 | +1.84 |
| **S48 final** | **+3.75/+0.043** | **+0.93/+0.005** | +4.99 | 42.8/−0.003 | +1.97 |
| R48 @36k | +3.60/+0.038 | +1.24/+0.011 | +4.79 | 33.5/−0.006 | +1.70 |
| **R48 final** | **+3.68/+0.041** | **+1.20/+0.011** | +4.89 | 42.6/−0.002 | +1.81 |

## Reading

VAL says both policies buy real −5 dB improvement; bench −5 dB
(6 target speakers, different mixtures) says S48 final actually
regressed vs parent seed-1 (0.93 vs 1.06) and R48 gained +0.14.
Overall crowd, @0 dB, SSN, white and quiet all improved in both
arms. Replication acceptance needs ≥+0.30 seed-mean on BOTH
VAL and bench at −5 dB — seed-1 bench evidence puts that in
doubt, especially for S48. Astra's review
([astra-review-gen21.md](./astra-review-gen21.md)): complete
both arms' seeds 18/19 unchanged (launched), run an expanded
development diagnostic alongside, and afterwards test a 30 dB
soft-capped SI-SDR loss first — her frozen-weight diagnostic
found quiet examples contributing ~37–53× the gradient norm of
noisy ones (clipping on 69–78% of late batches), a concrete
mechanism starving hard-SNR learning.

## Expanded development diagnostic (same day, alongside replication)

[dev_audit.py](./dev_audit.py): 8 targets × 4 crops × 4 mixtures
@−5/0 dB (128 items/SNR, seed 20261123), paired vs parent.
@−5 dB paired ΔSI-SDR: S48@36k +0.353 (93/128 items positive),
**S48 final +0.453 (96/128)**, R48@36k +0.329 (111/128),
**R48 final +0.322 (104/128)**; per-target means improve for
all 8 targets in both finals, and S48's bench 36k→48k dip does
NOT reproduce (final > 36k here). Absolute levels differ from
the registered panels (parent @−5 +2.05 here vs +1.06 bench /
+0.56 VAL) — single-mixture and 4-mixture panels are simply
noisy draws (e.g. parent on 5536: −0.49 here vs +1.13 on VAL's
fixed items). Development evidence only; registered panels and
acceptance rules unchanged.

## 3-seed replication verdict (2026-11-04 15:35) — NEITHER ARM QUALIFIES

> Claude Opus 5.5 (took over from muse-wonder-full-1.0 at ~13:00).
> Judge: [judge_replication.py](./judge_replication.py) →
> [replication_judgment.json](./replication_judgment.json) (reproduces
> the filed seed-17/18 numbers exactly; asserts each R48 parent hash
> equals its parent bench hash and each final's VAL-log hash equals
> its bench hash). 48k finals only. `promoted FALSE`.

**Seed-19 provenance.** S48s19 was killed at step 12,500 (12:57)
when the previous agent session ended — no process left and no
full state before 24k. It was relaunched from scratch, same seed,
at 13:00; rerun losses (steps 100–225) and per-item VAL records
(steps 0 and 2000) are bit-identical to the killed run, so the
rerun is a faithful replay. Killed-run artifacts are kept untracked
in `weights/aborted_s48s19_run1/`. R48s19 ran concurrently with
S48s19's second half, launched on the 24k RNG handoff (scheduling
only; parent sha `89837737…` = `benchv2_gen19s3.json`).

Gains vs each seed's own Gen19 parent at −5 dB (ΔSI-SDR dB / ΔSTOI):

| Seed | Parent VAL / bench | S48 VAL gain | S48 bench gain | R48 VAL gain | R48 bench gain |
|---|---|---|---|---|---|
| 17 | 0.5641 / 1.0604 | +0.4409/+0.0092 | −0.1267/−0.0018 | +0.3159/+0.0054 | +0.1380/+0.0039 |
| 18 | 1.0061 / 1.3556 | −0.1580/−0.0000 | −0.4351/−0.0000 | −0.0416/−0.0043 | −0.2654/+0.0032 |
| 19 | 0.7723 / 1.1470 | +0.1483/+0.0149 | −0.1474/+0.0083 | +0.0790/+0.0088 | −0.1736/+0.0062 |
| **Mean** | 0.7808 / 1.1877 | **+0.1437**/+0.0080 | **−0.2364**/+0.0022 | **+0.1178**/+0.0033 | **−0.1004**/+0.0044 |

| Rule (prereg) | S48 | R48 |
|---|---|---|
| Mean gain ≥ +0.30 on BOTH VAL and bench | FAIL | FAIL |
| Non-worsening mean −5 STOI (both panels) | pass | pass |
| Positive in ≥ 2/3 seeds (both panels) | FAIL (VAL 2/3, bench 0/3) | FAIL (VAL 2/3, bench 1/3) |
| 0 dB safeguard (≤0.15 dB / 0.003 STOI) | pass | pass |
| Quiet abs ≥ 25 dB, ΔSTOI ≥ −0.02 | pass | pass |
| **Qualifies** | **NO** | **NO** |

Scratch preference (S48−R48 ≥ 0.15 on both): VAL +0.026, bench
−0.136 → not preferred. Per the prereg, a failed R48 is NOT
accepted by default: **Gen 19 remains the accepted baseline**
(13/14 required KPIs; crowd @−5 dB +1.19 vs +1.5). No spatial run
or KPI scorecard for Gen 21 (gated on qualification).

Seed-19 bench detail (n=6/cell):

| Ckpt | Crowd ΔSI-SDR/ΔSTOI | Crowd @−5 dB | @0 dB | Quiet abs/ΔSTOI | Comp |
|---|---|---|---|---|---|
| Gen19 s19 parent | +3.53/+0.034 | +1.15/+0.001 | +4.68 | 36.7/−0.004 | +1.32 |
| S48 @24k | +3.62/+0.039 | +1.10/+0.005 | +4.65 | 33.8/−0.005 | +1.53 |
| S48 @36k | +3.62/+0.044 | +0.92/+0.010 | +4.78 | 38.6/−0.003 | +1.71 |
| **S48 final** | **+3.88/+0.045** | **+1.00/+0.009** | +5.23 | 38.6/−0.004 | +2.03 |
| R48 @36k | +3.50/+0.040 | +0.95/+0.004 | +4.53 | 37.1/−0.005 | +1.47 |
| **R48 final** | **+3.70/+0.042** | **+0.97/+0.007** | +4.93 | 42.4/−0.004 | +1.78 |

**Reading.** Doubling optimization reliably buys the *easy*
conditions — seed-mean overall crowd ΔSI-SDR rises from +3.51
(Gen19) to +3.79 (S48) / +3.67 (R48), and 0 dB, competing-talker
and quiet improve in every seed — but not the −5 dB wall: bench
−5 dB falls in 3/3 seeds for S48 and 2/3 for R48, and VAL gains
(+0.14/+0.12) are below half the bar. This is the pattern Astra's
gradient diagnostic predicts (near-perfect examples dominating the
clipped gradient), so the next generation changes the objective,
not the budget: **Gen 22 = 30 dB soft-capped SI-SDR under the
"neither selected" policy (24k scratch, Gen19 controls)**,
[../gen22/prereg.md](../gen22/prereg.md). Effects remain
confounded as registered (optimizer reset vs LR shape not
separated); 6-mixture bench and 8-item VAL panels are small.
