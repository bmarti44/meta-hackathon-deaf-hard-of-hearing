# Muse (Meta) independent review of the Gen 31 result — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`) via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~02:02.
> - The first call, at effort `high`, returned an empty answer.
> - It was re-run once at effort `medium` with the identical prompt; that answer is below.
> - Disposition: see [astra-review-gen31.md](./astra-review-gen31.md#disposition-claude-opus-55-2026-11-05-0220-covering-both-reviews).

## Verbatim answer (effort medium)

1. Handling: Yes. NO CANDIDATE is correct per registered rule.

Rule was: largest a with all 4 mean paired dry deltas >=0 over whole prefix. a=0.1 has -5dB dSTOI=-0.00003 <0, so prefix fails at first step. No cherry-pick, no screen touched, FAIL is correct.

What curve shows: systematic trade, not uniform win. -5dB dSISDR +0.02 to +0.08, 0dB dSTOI +0.0004 to +0.0014 improve with a; -5dB dSTOI -0.00003 to -0.00075 and 0dB dSISDR +0.0008 to -0.1011 degrade with a. Magnitudes at a=0.1 are negligible: hundredths dB, STOI 3e-05 to 4e-04.

What it does not show: not evidence of meaningful dry harm at a=0.1; 512-item mean -0.00003 STOI is test noise. Not evidence FT has no room value; VAL here is dry-only. Not evidence about real CI users; in-silico LibriSpeech dry metric only. Gen27-30 context matters: dry 0dB costs -0.49 to -0.06 dB with room gains +0.51 to +0.31 dB were real trade, D FAIL each time. Gen31 failure is different: noise-level failure.

2. Yes, adopt pre-specified non-inferiority margin prospectively. Zero-margin on 4 point-estimates makes true-zero preservation fail with P~1-(~0.5^4)=~94% if independent; correlated still >>50%.

For new generations only, suggest:

VAL selection and judge primary: mean paired delta >= -0.10 dB SI-SDR AND >= -0.005 STOI, on each of the 4 dry conditions.

A priori basis, not from Gen27-31: -0.10 dB is below run-to-run enhancement noise ~0.2-0.3 dB and well below ~0.5-1.0 dB usually needed for audible level/quality shift; -0.005 STOI is 1/2 to 1/4 of commonly cited 0.01-0.02 intelligibility-relevant STOI change, and ~3-5x SE on n~500. That kills coin-flip without permitting meaningful regression.

Anti-moving-goalposts: do not re-score Gen27-31 as passes; keep zero-margin judge_v3 D computed and reported as secondary safety; version as judge_v4 with NI primary; preregister margins with this justification before seeing new VAL; require same margins to also hold on held-out screen.

If you insist on zero-margin, only design that can pass reliably is dry-bypass: leave dry path bit-identical to Gen19 by architecture/gating, learn only wet-gated residual. Fine-tuning + linear blend cannot.

3. Not (a) as drafted. Single COEF=100 is uncalibrated: loss is relative MSE, scale unknown, x100 likely dominates or is irrelevant vs enhancement loss. And Gen31 VAL is dry-only with zero-margin, so even a good trade will again select a~0 with no room gain.

Next ~1h: calibrated anchor sweep + joint dry-room selection.

Train: same Gen19 seed-17, same aug50 45/45/10, same 8k updates Adam 1e-4->1e-5. First 5 min: forward 50 dry clips, measure main loss L0 vs preserve term P0, pick 3 COEFs spanning P0*COEF ~0.1x,1x,3x L0, e.g. log-spaced. Train 3x ~12 min.

VAL: fresh seeds, 16-voice 512-item dry panel (-5,0 dB) + matched synthetic-room panel same utterances with fixed RIR/noise (-5,0 dB). Selection preregistered: among COEF x alpha in {0.1..1.0}, maximize mean wet dSISDR subject to all 4 dry means meeting NI margins above; require wet gain lower 95% CI >0. If tie, smallest dry cost.

Judge: unchanged judge_v3 screen plus report NI pass/fail and wet gains; no promotion on dry alone; in-silico only.

4. SUBMISSION.md sentences: Gen31 interpolated the reverberant-tuned model back toward Gen19 but no blend preserved all four dry noisy scores exactly, so no candidate advanced. The shortfall at the closest blend was 0.00003 STOI points, i.e. test noise, showing no dry-preserving win in this direction and no evidence about real implant hearing.
