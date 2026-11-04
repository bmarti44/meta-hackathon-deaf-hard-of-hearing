# Gen 19 pre-registration (2026-11-03, before training)

Per Astra training-strategy review step 1 (disposition:
../gen18/astra-review-disposition.md).

- Sole change vs Gen 18: **24,000 steps** from scratch, Adam
  1e-3 cosine→1e-4 stretched over the full budget. Frozen:
  model, neg-SI-SDR loss, mixture recipe (70% babble k~U{2..12},
  SNR 60% U(−5,5)+40% U(−5,10), 10% quiet), batch 8×2 s,
  clip 5, train-clean-100 pool, seeds 20261117/18/19,
  final-checkpoint rule.
- VAL panel (diagnostic only, never selection): targets
  5536/5694, interferers 2035/2078/2086/2277/2412/2428, crowd
  k8–12, 4 crops/target/SNR + quiet, fixed RNG 777123, every
  2000 steps. Inspect 6k/12k/18k/24k trajectory.
- Success readout: crowd ΔSI-SDR ≥0.3 dB or ΔSTOI ≥0.005 over
  Gen 18 seed-mean on VAL/test with hard rows improving and no
  guard regression. 48k considered only if 18k→24k improves
  both SI-SDR and STOI on VAL.
- Screen seed 20261117 first; replicate other seeds before
  any KPI claim. Scorecard requires 3 distinct-hash seed
  benches + hash-matched spatial (INCOMPLETE otherwise).
