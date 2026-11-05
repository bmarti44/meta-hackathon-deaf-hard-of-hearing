# Gen 28 — half the room dose, seed-17 screen: FAIL (closest yet) (T0)

> Claude Opus 5.5, 2026-11-05 ~00:15.
> - Registration: [prereg.md](./prereg.md); Astra cleared it pre-launch.
> - Judge: Gen 27's `judge_v3.py`, unchanged → [screen_s17.json](./screen_s17.json).
> - Reviews: [Astra](./astra-review-gen28.md) and [Muse](./muse-review-gen28.md).
> - Training took 37.2 min. `promoted FALSE`.

**Verdict:** FAIL. R1a–c, C, T, S2 and **S3** pass; **D and SP fail**.

| | Gen 27 (P = 0.5) | Gen 28 (P = 0.25) |
|---|---|---|
| R1 room gain vs Gen 19 (6 held-out synthetic rooms) | +0.514 [+0.238, +0.844] | **+0.459 [+0.230, +0.736]**, 15/16 voices |
| C: measured rooms −5 / 0 dB | +0.154 / +0.191 | +0.157 / +0.171 |
| T: target-only vs Gen 19, synthetic / measured | +2.05 / +0.91 dB | +1.81 / +0.73 dB |
| D: dry −5 dB | −0.228 dB / −0.010 | **−0.115 dB / −0.006** ✗ |
| D: dry 0 dB | −0.492 dB / −0.010 | **−0.317 dB / −0.008** ✗ |
| S3: crowd ΔSTOI (≥ 0.03) | 0.0290 ✗ | **0.0315 ✓** |
| SP | ILD + ITD worse in mirrored subsets ✗ | **ITD only:** a one-bin ITD-error increase (crop 1, 0 dB, ±30°: 0 → 1 sample), producing +0.125 samples in the subset mean; perceptual significance undetermined ✗ |

**Reading** (this seed and panel only):
- Halving the dose kept 89.4% of the room gain and cut the dry SI-SDR
  penalties by about 50% / 36%. That supports one more dose step.
- It establishes no general dose-response curve and no zero-cost dose.
- Target-only performance remains below bypass.
- No listener benefit is established.

**Next: Gen 29,** P = 0.125 (78.75 / 11.25 / 10), with the same gates. If
the room gain falls below +0.30, the dose taper stops and the approach
changes.
