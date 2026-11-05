# Muse (Meta) independent review of the Gen 32 result — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~02:38.
> Disposition: see [astra-review-gen32.md](./astra-review-gen32.md#disposition-claude-opus-55-2026-11-05-0255-covering-both-reviews).

## Verbatim answer

FAIL stands on all three cited gates. Do not upgrade or reinterpret.

1. Gate check:

- R1a: +0.283 < 0.30 bar, so FAIL even though CI [+0.125,+0.465] excludes 0 and 14/16 voices positive. R1b/R1c passing does not rescue it.
- D: -5 dB +0.032 / +0.0002, 0 dB -0.0012 / +0.0016. One of four means <0, so FAIL by the pre-registered all-means >=0 rule. -0.0012 dB [-0.019,+0.016] is in-silico tie, not a regression proven, but it is not a pass.
- SP: +0.066 dB mirrored ILD vs Gen19 = FAIL. Split by SNR makes it worse: better only at -5 dB, +0.05..+0.15 worse at 0/5/10 dB. ITD tied.
- VAL alpha*=0.7 follows the stated prefix rule.

What can be concluded, no more:
Gen32 with preserve-dry 100 + WiSE-FT 0.7 got dry to ~parity and got first all-6-measured-rooms positive at -5/0 dB (+0.067/+0.103) plus synthetic +0.283. That is progress on the tradeoff, not a deployable result. No evidence of intelligibility or real-CI benefit. Selection used the test-clean dry panel, so D is best-case and still failed. The repeating pattern across Gen27-29 and Gen32 - room training with independent per-ear inference worsens ILD at easy SNRs - points to architecture, not dose.

2. Next: do (c), linked two-ear inference. Do not do (a) longer FT or (b) aug75: both increase room dose that has already failed D 5 times and worsened ILD 4 times, for a needed +0.017 dB to reach 0.30.

Exact Gen33 spec, ~15 min compute, no retraining:
Take frozen Gen32 alpha=0.7 weights unchanged. Change only bilateral inference: compute per-ear gains gL,gR per T-F bin as now, then apply common gain gC=(gL+gR)/2 to both ears: yL=gC*xL, yR=gC*xR. This preserves input ILD by construction and is deployable as one linked processor.

Judge with zero gate changes: run identical judge_v3 vs same-seed Gen19 on same seeds/panels. CANDIDATE only if all Gen32 gates pass unchanged: R1a >=0.30, R1b/R1c pass, D 4/4 means >=0, T/S2/S3 pass, SP pass vs Gen19. Pre-register diagnostic only: linked ILD < unlinked Gen32 ILD. If SP still fails, stop room line and move agenda; do not tune linking on test.

3. SUBMISSION.md bullet:

Gen32 tried to learn reverberant rooms while keeping dry speech unchanged, leaving dry speech about the same and improving room scores a little. It missed our preset bars for rooms, dry speech at 0 dB, and direction preservation, so it was rejected as a candidate.
