# Muse (Meta) independent review of the Gen 29 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~00:57. The prompt was identical to Astra's.
> Disposition: see [astra-review-gen29.md](./astra-review-gen29.md#disposition-claude-opus-55-2026-11-05-0105-covering-both-reviews).

## Verbatim answer

1. FAIL is correct, typo aside:

* Registered `GEN27 SCREEN FAIL` should read GEN29. With `D=False` and `SP=False`, overall FAIL follows under AND gates.
* Arithmetic checks: ILD mirrored 5.509-5.427=+0.082 dB worse, ITD 3.125-3.000=+0.125 sample worse - correctly called small. Dry 0dB SI-SDR -0.126, lo -0.169, hi -0.083 stated: CI entirely <0. Dry STOI also negative both SNRs: -0.0039/lo -0.0057 and -0.0028/lo -0.0048.
* Characterisation nuance missing: `S3 PASS` is bench-v2 dry crowd +3.363/lo 2.597, STOI +0.0323/lo 0.0198. `D FAIL` is screen-v2 dry. Different panels. Do not conflate.
* SP nuance: existing vs unproc passes 5.539<5.964 ILD, 4.25<5.75 ITD; hard -5 vs Gen19 passes/ties 8.560<8.793, 12=12. Only mirrored fails by tiny margin - fragility/replication needed, but gate FAIL stands.

Three single-seed points, P=0.5/0.25/0.125, seed 17 only:

* Descriptive only: R1 +0.514/+0.459/+0.370, dry -5dB -0.228/-0.115/-0.018, dry 0dB -0.492/-0.317/-0.126. Consistent with tradeoff, not proof of one.
* No CIs on differences, no multi-seed variance, no linearity test. Cannot extrapolate. Measured C +0.154/+0.191, +0.157/+0.171, +0.140/+0.164 is essentially flat - persistence is hypothesis, not conclusion.
* Binding constraint is now dry 0dB: R1a +0.3695>0.30 still passes, R1b lo +0.163>0, R1c 15/16, C/T pass. D 0dB CI excludes 0. That alone blocks anything that must not hurt dry, where users hear well today.

2. Pick (c) WiSE-FT interpolation - one FT run + free scalar search off-screen. Rejects:

* (a) P=0.0625: extrapolation predicts R1 ~0.28-0.30 borderline FAIL with dry 0dB likely still <0. Trades away primary without fixing mechanism.
* (b) L2-SP: needs re-train per lambda, two changes at once.
* (d): new rooms / binaural-linked: scope/architecture change, does not address dry-cost mechanism.

Exact spec, laptop ~1h, pre-register before any screen:

* Init: Gen19 weights frozen as `theta0`. FT = same Gen29 aug125 pipeline 78.75/11.25/10, realised ~11% rev, all else frozen, same seed 17 family, but FT only ~12min, LR 0.1x Gen29, no other change. Produces `thetaFT`.
* Interpolate: `theta(a)=(1-a)*theta0+a*thetaFT`, a in 0.0,0.1,...,1.0. No retraining.
* VAL, never screen: separate seed e.g. 99, voices/rooms disjoint from 12 screen rooms listed + screen voices, 3s, SNR -5/0, dry + rev. Hash VAL IDs in prereg.
* Choose `a*`: on VAL only, among a with VAL dry SI-SDR gain >=0 and STOI gain >=0 at both SNRs, pick max VAL rev gain. If none, `a*=0`, stop, report no candidate. Lock `a*`, then run `judge_v3` once vs same-seed Gen19.
* Decision: same gates. Success = D both SNRs non-worsening AND R1a>=0.30 AND R1b lo>0, R1c>=10/16, C>0 each SNR/stratum, T>=0, S2/S3/SP no worsening. Any D regression = FAIL even if R1 larger.

3. SUBMISSION.md Gen29 bullet:

> Gen29 cut room exposure to ~11% of examples; reverberant gain fell to +0.37 dB while dry 0-dB quality still scored lower at -0.13 dB with confidence interval entirely below zero, so the screen failed. Dose reduction alone shrank but did not remove the dry cost, so tapering stops here.
