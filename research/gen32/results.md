# Gen 32 — room fine-tune with dry-output preservation, blended back: FAIL (closest yet) (T0)

> Claude Opus 5.5, 2026-11-05 ~02:45.
> - Registration: [prereg.md](./prereg.md); Astra and Muse cleared it.
> - Selection: [val_selection_s17.json](./val_selection_s17.json), with per-item scores.
> - Judge: unchanged `judge_v3.py` → [screen_s17.json](./screen_s17.json).
> - Reviews: [Astra](./astra-review-gen32.md) and [Muse](./muse-review-gen32.md).
> - `promoted FALSE`.

**Verdict:** FAIL. A candidate was selected (α\* = 0.7) and screened once.
- R1b, R1c, C, T, S2 and S3 pass.
- **R1a fails:** +0.283 < +0.30.
- **D fails** on one mean: 0 dB SI-SDR −0.0012 dB.
- **SP fails** on mirrored ILD: +0.066 dB.

**Step 1, fine-tune with preservation:**
- 8,000 updates from Gen 19 seed 17 on aug50, `--preserve-dry 100`.
- 14.8 min (886.8 s).
- The logged penalty stayed small: 0.0004–0.0014, versus 0.0061 drift for Gen 31's unpenalised fine-tune on training batches.

**Steps 2–3, blends on the test-clean dry VAL panel** (mean of blend − Gen 19):

| α | −5 dB SI-SDR | −5 dB STOI | 0 dB SI-SDR | 0 dB STOI | pass |
|---|---|---|---|---|---|
| 0.1 | +0.0067 | +0.00001 | +0.0020 | +0.00015 | ✓ |
| 0.5 | +0.0283 | +0.00005 | +0.0040 | +0.00067 | ✓ |
| **0.7** | +0.0360 | +0.00007 | +0.0014 | +0.00090 | ✓ (α\*) |
| 0.8 | +0.0392 | +0.00009 | −0.0009 | +0.00101 | ✗ |
| 1.0 | +0.0441 | +0.00012 | −0.0074 | +0.00122 | ✗ |

Compare Gen 31, where every α failed and α = 1 reached −0.101 dB at 0 dB. With
preservation, the whole dry curve moved up.

**Screen of the α = 0.7 blend vs same-seed Gen 19:**

| | Gen 30 (scratch, P = 0.0625) | **Gen 32** |
|---|---|---|
| R1 synthetic-room gain | +0.308 [+0.101, +0.554] | **+0.283 [+0.125, +0.465]** ✗ (< 0.30), 14/16 voices |
| Measured rooms −5 / 0 dB | +0.056 / +0.079 | **+0.067 / +0.103**; all six measured rooms positive in SI-SDR at both SNRs |
| D dry −5 dB, SI-SDR / STOI | −0.032 / +0.0002 | **+0.032 [+0.016, +0.048] / +0.0002** |
| D dry 0 dB, SI-SDR / STOI | −0.063 / −0.0008 | **−0.0012 [−0.019, +0.016] / +0.0016** ✗ (mean < 0) |
| S3: crowd / white | +3.44 / −0.048 | +3.50 (ΔSTOI +0.037) / +0.121 ✓ |
| Quiet (S2) | 37.5 dB | 41.0 dB ✓ |
| SP | pass | ✗ mirrored ILD +0.066 dB (ITD tied 3.0 vs 3.0); better at −5 dB, worse at 0–10 dB (+0.05 to +0.15 dB) |

**Reading** (this seed and these development panels only):
- **Dry preservation worked.**
  - On the screen's dry panel, −5 dB SI-SDR is now significantly better than Gen 19, and both STOI means are positive.
  - The only negative mean is 0 dB SI-SDR, at −0.0012 dB, with an interval spanning zero.
  - It fails D because D requires every mean ≥ 0, and that requirement is kept.
- **The room gain shrank below the bar:**
  - +0.283 against +0.30, though its interval excludes zero and 14/16 voices improve.
  - Measured-room transfer is the best of the room line: every measured room is positive.
- **The direction-cue cost at easier SNRs persists:**
  - small ILD increases at 0–10 dB;
  - ITD unchanged.
- No listener benefit is established.

**Artifacts committed:**
- the fine-tune final weights and train log;
- the candidate blend (`wiseftpd_seed20261117.pt`);
- the blend index and the selection JSON;
- the screen, panel, spatial and bench JSONs.
