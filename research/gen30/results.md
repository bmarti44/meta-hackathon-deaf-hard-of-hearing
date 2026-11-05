# Gen 30 — one eighth of the room dose, seed-17 screen: FAIL; dose-only campaign ends (T0)

> Claude Opus 5.5, 2026-11-05 ~01:55.
> - Registration: [prereg.md](./prereg.md); Astra cleared it pre-launch ([astra-prelaunch-review.md](./astra-prelaunch-review.md)).
> - Judge: Gen 27's `judge_v3.py`, unchanged → [screen_s17.json](./screen_s17.json).
> - Reviews: [Astra](./astra-review-gen30.md) and [Muse](./muse-review-gen30.md).
> - Training took 36.4 min (2,181.1 s); 5.6% of training examples were reverberant (10,806 / 192,000). `promoted FALSE`.

**Verdict:** FAIL. R1a–c, C, T, S2 and **SP** pass; **D and S3 fail**.

By the registered campaign boundary, any Gen 30 failure ends the dose-only
campaign. Gen 31 (WiSE-FT) was launched at 01:47, as registered, after
its pipeline confirmed this FAIL verdict.

| | Gen 27 (P = 0.5) | Gen 28 (0.25) | Gen 29 (0.125) | **Gen 30 (0.0625)** |
|---|---|---|---|---|
| R1 room gain vs Gen 19 (6 held-out synthetic rooms) | +0.514 | +0.459 | +0.370 | **+0.308 [+0.101, +0.554]**, 14/16 voices |
| C: measured rooms −5 / 0 dB | +0.154 / +0.191 | +0.157 / +0.171 | +0.140 / +0.164 | +0.056 / +0.079 |
| T: target-only vs Gen 19, synthetic / measured | +2.05 / +0.91 | +1.81 / +0.73 | +1.58 / +0.61 | +1.55 / +0.62 dB |
| D: dry −5 dB, SI-SDR / STOI | −0.228 / −0.010 | −0.115 / −0.006 | −0.018 / −0.004 | **−0.032 [−0.101, +0.042] / +0.0002** ✗ |
| D: dry 0 dB, SI-SDR / STOI | −0.492 / −0.010 | −0.317 / −0.008 | −0.126 / −0.003 | **−0.063 [−0.092, −0.032] / −0.0008** ✗ |
| S3 | fail | pass | pass | **fail** (white held-out SI-SDR −0.048 < 0) |
| SP | fail | fail | fail | **pass** |

**What fails, exactly:**
- **D:**
  - All four lower bounds are now inside their margins (> −0.15 dB / > −0.003).
  - D also requires non-negative means. Three of the four means are negative: SI-SDR at both SNRs, and STOI at 0 dB.
  - At 0 dB the whole SI-SDR interval is below zero.
- **S3:** held-out white noise is −0.048 dB, against a required ≥ 0.
  - Its interval is wide (−1.18 to +0.87); Gen 29 had +0.105.
  - The crowd row passes: +3.44 dB, ΔSTOI +0.037, ΔACE +0.068, all lower bounds > 0.

**What passes for the first time:** SP. Existing gates pass. The hard
−5 dB subset improves target-ILD error by 0.37 dB with ITD tied. Both
mirrored subsets improve ILD by 0.04 dB with ITD tied (3.0 vs 3.0
samples).

**Reading** (this seed and these panels only):
- The dose line ends where the reviewers expected:
  - room gain is just above its bar (+0.308 vs +0.30, lower bound +0.101);
  - measured-room gains have nearly vanished (+0.06 / +0.08), and four of six measured rooms are slightly negative in SI-SDR at −5 dB;
  - the dry cost at 0 dB is about half of Gen 29's, but its interval still excludes zero.
- Four single-seed points are descriptive. They do not establish a curve.
- No listener benefit is established.

**Next:** Gen 31, already running (registered; Astra and Muse cleared it):
fine-tune Gen 19 on rooms, then blend the weights back toward Gen 19, with
the blend chosen on fresh test-clean voices.
