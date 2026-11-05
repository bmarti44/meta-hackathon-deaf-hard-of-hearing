# Muse (Meta) independent review of the Gen 24 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-04 ~22:00. The prompt was identical to Astra's.

## Verbatim answer

As T0 in-silico reviewer, on papers as given:

**1. FAIL is correct. Arithmetic checks out.**

* VAL -5: 0.3518-0.5641 = -0.2123, STOI -0.0085. Bench -5: 1.0411-1.0604 = -0.0193, STOI -0.0014. Both < +0.30 target, both STOI worsening. Checks 1=False, 2=False correct.
* 0-dB safeguard: VAL -0.296 / -0.0107, bench -0.045 / -0.0043. Both negative SI-SDR + STOI worsening. Check 3=False correct and material, not borderline. VAL shows degradation at the easier condition, not just a miss at -5 dB.
* Dev -5: values sum to +0.515/8 = +0.064 mean, 4/8 >0. Check 6=False correct. Mean is misleading: heterogeneous, with 5536 -0.832 vs 5895 +0.586.
* Quiet/others pass does not rescue screen. Overall FAIL correctly characterised as primary miss + STOI worsening + 0-dB safeguard failure.

May conclude: this specific variant — 0.6*U(-5,-2)+0.4*U(-2,10) by affine remap of same draws, 40% at -5 to -3 dB vs 17.3%, plain SI-SDR, 24k scratch, seed 17 vs Gen19 final 80000b64c413 — did not help and worsened 0-dB VAL.

May NOT conclude: hard-SNR exposure in general fails; other mix, budget, curriculum, loss, seeds would fail; Gen19 13/14 invalidated; anything about intelligibility or CI-user benefit. n=1 seed, run 1 stopped ~100 and filed, in-silico SI-SDR/STOI only.

**2. No plan change.**

Gen24 tests SNR-distribution, Gen27 tests rooms/reverb — orthogonal. One null plus Gen20-23,25 nulls supports holder's pivot away from simple retrains, but gives no positive/negative evidence for Gen27. Proceed Gen27 as pre-launch reviewed, then real recordings, two-input, ACE aux in order. Do not promote Gen19: crowd -5 seed-mean 1.188 vs 1.5, plus provisional reverb degradation.

Provenance PASS conditional on logs: hash match reported, deviation filed.

**3. SUBMISSION.md Gen24 bullet — two sentences:**

Gen24 tested harder SNR exposure with 40% of noisy items at -5 to -3 dB versus 17.3% before over 24k steps at seed 17 and failed screen against the Gen19 final model with -5 dB gains of -0.21 dB on VAL and -0.02 dB on bench and worse 0 dB performance. This is a single-seed in-silico null with no test of real-world hearing and does not change the next room-augmentation and real-recording tests.
