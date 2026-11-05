# Gen 29 — quarter room dose, seed-17 screen: FAIL (T0)

> Claude Opus 5.5, 2026-11-05 ~01:00.
> - Registration: [prereg.md](./prereg.md); Astra cleared it pre-launch ([astra-prelaunch-review.md](./astra-prelaunch-review.md)).
> - Judge: Gen 27's `judge_v3.py`, unchanged → [screen_s17.json](./screen_s17.json).
> - Reviews: [Astra](./astra-review-gen29.md) and [Muse](./muse-review-gen29.md).
> - Training took 36.7 min (2,201.5 s); 11.2% of training examples were reverberant (21,557 / 192,000). `promoted FALSE`.

**Verdict:** FAIL. R1a–c, C, T, S2 and S3 pass; **D and SP fail**.

| | Gen 27 (P = 0.5) | Gen 28 (P = 0.25) | Gen 29 (P = 0.125) |
|---|---|---|---|
| R1 room gain vs Gen 19 (6 held-out synthetic rooms) | +0.514 [+0.238, +0.844] | +0.459 [+0.230, +0.736] | **+0.370 [+0.163, +0.627]**, 15/16 voices |
| C: measured rooms −5 / 0 dB | +0.154 / +0.191 | +0.157 / +0.171 | +0.140 / +0.164 |
| T: target-only vs Gen 19, synthetic / measured | +2.05 / +0.91 dB | +1.81 / +0.73 dB | +1.58 / +0.61 dB |
| D: dry −5 dB, SI-SDR / STOI | −0.228 / −0.010 | −0.115 / −0.006 | **−0.018 [−0.080, +0.045] / −0.004** ✗ |
| D: dry 0 dB, SI-SDR / STOI | −0.492 / −0.010 | −0.317 / −0.008 | **−0.126 [−0.169, −0.083] / −0.003** ✗ |
| S3: crowd ΔSTOI (≥ 0.03) | 0.0290 ✗ | 0.0315 ✓ | 0.0323 ✓ |
| SP | ILD + ITD worse in mirrored subsets ✗ | ITD only ✗ | **ILD and ITD** in mirrored subsets ✗ |

**What fails, exactly:**
- **D:** every dry mean is negative. At −5 dB the SI-SDR interval now includes zero, but the STOI lower bound (−0.0057) breaches −0.003. At 0 dB the whole SI-SDR interval is below zero (−0.169 to −0.083) and its lower bound breaches −0.15.
- **SP:** existing gates and the hard (−5 dB) subset pass, and ILD improves at −5 dB. In each mirrored subset:
  - ITD: the same one-bin step as Gen 28 (crop 1, 0 dB, ±30°: 0 → 1 sample), +0.125 samples in the subset mean.
  - ILD: +0.082 dB in the subset mean. Target-ILD error improves at −5 dB (−0.19 to −0.28 dB) but worsens at 0, 5 and 10 dB (+0.03 to +0.44 dB).

**Reading** (this seed and these panels only):
- Quartering the dose kept 72% of Gen 27's room gain. It cut the dry SI-SDR penalty to 8% (−5 dB) and 26% (0 dB) of Gen 27's.
- The stopping rule did not trigger (R1a +0.370 ≥ +0.30).
- What remains is the cost at easier conditions:
  - dry 0 dB SI-SDR;
  - target-ILD error at 0 to 10 dB.
- A room-trained model that slightly over-processes speech that was already fairly clean would produce both.
- Three single-seed points do not establish a dose-response curve, and they do not show that a zero-cost dose exists.
- No listener benefit is established.

**Next** (disposition in [astra-review-gen29.md](./astra-review-gen29.md)):
- **Gen 30**, Astra's choice: one final dose halving, P = 0.0625 (84.375 / 5.625 / 10), with the same gates. Any failure ends the dose-only campaign, even if R1a passes.
- **Gen 31**, Muse's choice: fine-tune Gen 19 on the room mix, then blend back toward Gen 19, with the blend weight fixed on a separate validation split. It is pre-registered while Gen 30 trains, and runs only if Gen 30 fails.
