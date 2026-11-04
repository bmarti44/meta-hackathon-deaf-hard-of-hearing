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
