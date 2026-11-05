# Muse (Meta) independent review of the Gen 30 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~01:48.
> - Same prompt as Astra's, plus the Gen 31 registration text inline (Muse has no file access).
> - The answer ends mid-sentence at the output limit; it is filed as returned.
> - Disposition: see [astra-review-gen30.md](./astra-review-gen30.md#disposition-claude-opus-55-2026-11-05-0200-covering-both-reviews).

## Verbatim answer

1. Gen30 FAIL is correct, characterisation is correct.

* Verdict: `D=False, S3=False` -> FAIL under no-tolerance rule. Label `GEN27 SCREEN FAIL` is a copy typo; checks/material are Gen30.
* D: means `-0.0315` at -5dB and `-0.0629` at 0dB, both <0, so fails `means >=0`. Lower bounds `-0.1007/-0.0017` and `-0.0917/-0.0026` are all inside `>-0.15 / >-0.003`. Fails on means, not on bounds. Correctly stated.
* S3: crowd +3.438 / competing +1.483 / SSN +6.441 pass, white-heldout `-0.048` fails `mean>=0`. CI `-1.178..+0.872` spans zero and Gen29 was `+0.105`; this is a noisy single-mean failure, but failure under registered rule.
* Arithmetic checks: synthetic -5: (0.193+0.088+0.216+0.079+0.381+0.581)/6=0.256, synthetic 0: 2.162/6=0.360, measured -5: 0.334/6=0.056, measured 0: 0.476/6=0.079. Mean synthetic (0.2562+0.3603)/2=0.3082 matches R1a. R1a 0.3082>=0.30, R1b lo 0.101>0, R1c 14/16 pass. SP: cand ILD 5.438<5.964, ITD 4.0<5.75; hard 8.423<8.793, 12=12; mirrored 5.390<5.427, 3.0=3.0 -> non-worsening PASS. No material swap: dry replay hash matches.

Dose line P=0.5/0.25/0.125/0.0625, seed-17 only, n=1:

* R1: 0.514/0.459/0.370/0.308, lo 0.238/0.230/0.163/0.101. Lower dose = less in-silico rev gain. Measured -5/0 collapses at last step: 0.154/0.191, 0.157/0.171, 0.140/0.164 -> 0.056/0.079.
* Dry 0dB: -0.492/-0.317/-0.126/-0.063 improves toward zero but never >=0. Dry -5dB: -0.228/-0.115/-0.018/-0.032 non-monotonic at end; Gen30 CI -0.101..+0.042 includes both zero and prior point.
* S3 fail/pass/pass/fail, SP fail/fail/fail/pass. Seesaw, not convergence.

Conclude only: dose reduces dry harm and rev gain together, does not solve dry-negative-means, white-negative-mean, or joint S3+SP. Single seed, no trend CIs. Ending dose-only is justified. No clinical claim.

2. Gen31 is the right next step. Let running pipeline finish; do not start variants.

Why: respects registered boundary - new mechanism, not another dose; pre-cleared; cheap ~13+3+5 min; alpha chosen on fresh test-clean VAL, not screen; prefix rule `largest alpha with all <=alpha passing`, 4x d>=0 strict; endpoints bit-tested; same judge_v3 vs same-seed Gen19 applied once; NO CANDIDATE explicitly allowed; expectation states R1a>=0.30 uncertain.

If Gen31 FAIL / NO CANDIDATE, ranked next, laptop ~1h:

  1. Anchor-regularized fine-tune + WiSE blend - attacks forgetting directly, same cost.
  2. Late-layer-only fine-tune + WiSE blend - less forgetting surface.
  3. Freeze room line, lock Gen19 baseline on reserved voices + white/spatial - safety, no new benefit.

Top pick spec - Gen32 L2-SP + WiSE-FT, T0, single seed-17:

* Parent: Gen19 seed-17 final `80000b64..f367` only; continue from `research/gen21/weights/rng_handoff_seed20261117.pt`; aug50 45/45/10, manifest `f306700d..`, direct+50ms target, RNG `[seed,27]`, batch 8x2s, SI-SDR, clip 5, fresh Adam 1e-4 cosine to 1e-5, 8000 updates, final checkpoint only.
* Change vs Gen31: loss = SI-SDR + lambda*mean((theta-theta_Gen19)^2), single pre-fixed lambda=1e-3, all 181 params. No lambda sweep.
* Blend theta(a)=(1-a)Gen19+aFT, a in 0.1..1.0. Same VAL panel as Gen31: 16 test-clean speakers, 512 dry items, seed 20261131, hash `c2c4f89a..638`; same rule: d=mean(blend-Gen19) paired, pass(a)=all 4 d>=0 for SI-SDR/STOI x -5/0dB, a*=largest grid a with all a'<=a passing, else NO CANDIDATE, no screen touch. Keep 24 reserved speakers untouched.
* Judge once on a* with judge_v3 vs same-seed Gen19, same ADVANCE: R1a>=0.30, R1b lo>0, R1c>=10/16, C/T/D/S2/S3/SP all true, D means>=0 and lo
