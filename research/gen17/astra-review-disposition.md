# Astra xhigh review of Gen 17 — disposition (2026-11-03)

Standing between-generation rule. Reviewer recomputed all six
runs from crop rows (bootstrap intervals reproduced exactly,
checkpoint hashes match train logs). Headline: arithmetic sound,
interpretation too confident, scorecard cannot yet certify the
full KPI contract. NO-GO stands.

Accepted and applied:
- Wording: matched experiment identifies **pool expansion**
  (1.35→3.50 h, target+interferer diversity), not speaker count
  alone; white "no-harm" is SI-SDR-gate-narrow (white ACE −0.030,
  vocESTOI −0.083); competing = "no demonstrated solution at
  this scale"; seed-mean −5 dB crowd row is +0.80 (seed1's +0.99
  was flattering); STOI at −5 dB still negative.
- Scorecard: multi-seed manifest (hashes must match across
  bench/spatial files; <3 seed benches or missing/mismatched
  evidence → INCOMPLETE, never PASS); bench outputs now record
  checkpoint SHA-256.
- KPI.md Gen 15 baseline column corrected to balanced-v2 values
  (+1.75/+0.002/+0.037), legacy kept in results.md.
- Gen 18 ranking adopted: (a) train-clean-100 sole change,
  matched compute (6000 steps ≈ 26.7 h target crops/seed —
  a scale experiment, not convergence), judged on STOI/−5 dB
  rows; (b) CI-domain loss next, one term at a time, VAL-chosen
  weights; (c) binaural after spatial bench v2 (§2.4) exists.

Deferred with reason: full spatial bench v2 (measured HRIRs,
AGC/ADRO back-end) — scheduled before any binaural ranking;
fresh untouched confirmation set — required before promotion,
not before Gen 18 screening.
