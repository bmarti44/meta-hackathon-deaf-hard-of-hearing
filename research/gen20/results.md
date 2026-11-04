# Gen 20 — k-distribution: NULL, legacy k retained (T0)

> Model: requested Sol 6.1 / actual `muse-wonder-full-1.0`. 2026-11-04.
> Pre-registered: [prereg.md](./prereg.md) (incl. Astra amendment).
> Continuations make no KPI claim by design. `promoted FALSE`.

## Design executed

Paired 12k continuations from Gen19 seed-1 parent
(`80000b64…f367`), shared continuation seed 20261120,
per-example purpose-isolated RNG substreams (arms share targets,
SNRs, noise-kind choices, interferer prefix; only k differs),
fresh Adam warm-up 3e-5→3e-4 cosine→3e-5. A: legacy k~U{2..12}
(`6856d911…e7c4`, 2245 s). B: crowd80 80% k8–12/20% k4–7
(`d5a934a0…44e`, 2643 s). Final checkpoints only.

## Registered acceptance — FAILS (H2 rejected)

| VAL final | −5 dB ΔSI-SDR | −5 dB ΔSTOI | 0 dB ΔSI-SDR | 0 dB ΔSTOI |
|---|---|---|---|---|
| Parent (step 0) | 0.56 | 0.009 | 4.10 | 0.080 |
| A legacy | 0.81 | 0.016 | 4.36 | 0.086 |
| B crowd80 | 0.83 | 0.014 | 4.35 | 0.086 |
| **B−A** | **+0.02** (req ≥+0.30 ✗) | **−0.002** (req ≥0 ✗) | −0.01 ✓ | 0.000 ✓ |

A−parent +0.25, B−parent +0.27 at −5 dB: both arms gained
equally from the optimizer restart/anneal; the k change itself
contributed nothing measurable. 0 dB safeguards pass trivially.

Bench v2 on finals (n=6/cell) agrees: crowd ΔSI-SDR A +3.59 vs
B +3.64 (parent seed-1 +3.45); crowd @−5 dB A +1.12 vs B +1.17
(parent +1.06), ΔSTOI −0.002 B−A; quiet safeguard passes both
(abs 40.0/40.7 ≥25, ΔSTOI −0.003/−0.004 ≥−0.02). Competing
talkers: B is worse (+1.10 vs A +1.70) — expected direction for
dropping low-k training, and a further reason not to adopt B.

## Decision

Legacy k retained; no from-scratch crowd80 (Astra rank-2 skipped
per its own condition). Next per Astra ranking: Gen 21 = 48k
steps from scratch on the retained Gen19 recipe (budget+schedule
comparison), after Astra's between-generation review of this null.
