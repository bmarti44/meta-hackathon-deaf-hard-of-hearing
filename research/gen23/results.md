# Gen 23 — plain SI-SDR + 5 × compressed spectral loss, seed-17 screen: FAIL (T0)

> Claude Opus 5.5, 2026-11-04. Pre-registered: [prereg.md](./prereg.md).
> Concurrent code audit: [astra-code-audit.md](./astra-code-audit.md).
> Judge: [judge_screen.py](./judge_screen.py) → [screen_s17.json](./screen_s17.json).
> Provenance: [verify_provenance.py](./verify_provenance.py) `--gen 23` → **PASS** on every check:
> - file rehashes, and the 6 registered source hashes;
> - VAL item set (40) and bench grid (102 rows) complete and duplicate-free;
> - all summary means recomputed from raw pairs.
>
> Reviews (filed separately): Astra and Muse. Final checkpoint only. `promoted FALSE`.

**Verdict:** the single-seed (20261117), 24k-scratch screen failed. The
spectral term is **not retained** and Gen 19 stays the baseline.

**Run.**
- Launched 17:31:38; trained 65.5 min with no interruption.
- Final `sisdr_cs5_scratch_seed20261117.pt` sha `3e027fad…`.
- Control: Gen 19 seed-17 `80000b64…`.

## Registered rules (candidate − same-seed Gen 19)

| # | Rule | Value | Pass |
|---|---|---|---|
| 1 | −5 dB ΔSI-SDR ≥ +0.30 on BOTH panels | VAL **−0.338**, bench **−0.027** | **✗** |
| 2 | −5 dB ΔSTOI non-worsening, both panels | −0.0120 / −0.0028 | **✗** |
| 3 | 0 dB loss ≤ 0.15 dB / 0.003 STOI | VAL −0.025 / −0.0006; bench +0.071 / +0.0005 | ✓ |
| 4 | Quiet abs ≥ 25 dB, ΔSTOI ≥ −0.02 | 35.3 dB / −0.0027 | ✓ |
| 5 | Other required mono rows | crowd +3.43 / +0.034 / +0.070 (CI lo all > 0); SSN +6.42; **white −0.01** (needs ≥ 0) | **✗** |
| 6 | Dev panel: gain > 0, ≥ 5/8 targets improve | +0.003 dB, 5/8 | ✓ (barely) |

## Descriptive readouts (no decision role)

- **The spectral term barely steered training.**
  - The median gradient-norm ratio 5·L_CS / SI-SDR was **0.008** over all
    48 diagnostic batches, and 0.012 in the late half.
  - The raw L_CS fell from 0.057 to 0.043.
  - This was disclosed before launch (pre-launch smoke: `gn_cs5`
    0.13–0.48 vs `gn_sisdr` 1.6–170). At weight 5 the term is about 1% of
    the update.
- **VAL −5 dB, same seed:**

  | Step | Gen 23 | Gen 22 | Gen 19 |
  |---|---|---|---|
  | 12k | 0.567 | 0.555 | 0.60 |
  | 16k | 0.208 | 0.513 | 0.41 |
  | 20k | 0.411 | 0.763 | 0.69 |
  | 24k | 0.227 | 0.713 | 0.56 |

  Gen 22's and Gen 23's changes were both small perturbations of the same
  Gen 19 trajectory. Their finals landed +0.15 and −0.34 dB from Gen 19 on
  the 8-item VAL panel. That spread is about as large as the +0.30 screen
  bar.

**Reading.** This screen rejects compressed spectral supervision *at the
registered weight* as a fix for the −5 dB wall. It does not test the
idea at a weight large enough to matter, which would be a separate,
re-registered experiment.

Gen 22 and Gen 23 together suggest that single-seed screens of small
loss perturbations sit close to panel and trajectory noise at the
+0.30 bar. That is a design lesson for the next registration
(descriptive only), not a change to these verdicts.

Per the registered order, next is narrower noisy-SNR sampling
([../gen24/prereg.md](../gen24/prereg.md)). It is a data-distribution
change of about 2.3× hard-region exposure, not a ~1% gradient
perturbation.
