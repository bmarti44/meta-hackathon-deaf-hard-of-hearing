# Muse (Meta) independent review of the Gen 27 seed-17 screen — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `high`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-04 ~23:16. The prompt was identical to Astra's. Its arithmetic flag about +0.514 vs 0.343 is resolved in the disposition of [astra-review-gen27.md](./astra-review-gen27.md): the primary uses the synthetic rooms only, by registration.

## Verbatim answer

1. FAIL is correct, characterisation needs one fix.

* Gates from `judge_v3`: PASS `R1a,R1b,R1c,C,T,S2`; FAIL `D,S3,SP`. Under all-must-pass, `GEN27 SCREEN FAIL` follows.
* `D`: dry `SISDR gain -0.2282 dB @-5, -0.4922 dB @0`, `STOI -0.0102/-0.0104`. Both SNRs negative. Clear fail.
* `S3`: crowd dry vs unproc `+3.142 dB / +0.0290 STOI / +0.0634 ACE`. `0.030-0.0290=0.001` miss is real under prereg. Do not round to pass. CI-lo `0.0179` is also <0.03.
* `SP`: existing scenes pass `ILD 5.487 vs 5.964, ITD 4.25 vs 5.75` lower=better, crossed hard no worse `8.453 vs 8.793, 12 vs 12`, but mirrored `+0.069 dB, +0.125 samp` worse than Gen19 triggers `no-worsening` fail. Small, but fail is fail.
* Arithmetic flag: per-room incremental gains listed average to ~0.343 dB:
synthetic `-5:0.5088, 0.0:0.5184`, measured `-5:0.1538, 0.0:0.1906` reproduced exactly. Mean `(0.5088+0.5184+0.1538+0.1906)/4=0.343`. This does **not** equal reported `rev primary +0.5136 dB`. Clarify baseline/weighting for `+0.5136` vs `voice+room CI +0.238..+0.844` before record. Do not publish both without reconciliation. Dry replay hash match `557ad44f3f87` is good.
* Heterogeneity: 23/24 roomxSNR cells >0, 1 negative `air 0.0 -0.036 dB`. Measured-short rooms `e2a,jr1,jr2,ofc,air ~0.00-0.15 dB`; synthetic + large measured drive mean. `15/16 voices` is not universal.
* `target-only synthetic +2.0471/measured +0.9137 dB, STOI up`, `ctrl` negative, supports non-trivial effect, not metric gaming.

May conclude: in-silico trade-off signal - reverberant-noisy up on this 12-room/2-SNR screen, dry-noisy down, target-only not worsened.

May not conclude: net benefit, intelligibility/clinical benefit, generalisation beyond these RIRs/talkers/SNRs/3s cuts, or that `0.001 STOI` / `0.069 dB` misses are negligible - prereg thresholds are binding.

"Helped in rooms at a cost on dry" is fair as shorthand only with: mean effect heterogeneous and small in 5/6 measured rooms, dry cost larger at 0 dB, and primary-number inconsistency unresolved.

2. Best next: (b) lower reverberant fraction. Same compute, tests dose-response directly.

Why not others: (a) 48k steps doubles ~1.5-2h MPS budget and confounds exposure with steps; (c) L2-SP adds lambda + two-stage, not single-change; (d) capacity breaks 602k/5.88ms envelope and does not fix shift.

GEN28 spec, single change vs GEN27:
`same model/code/optimizer/LR/schedule/batch, 24k scratch, seed 20261117, same RIR split-by-room, per-talker RIRs, same target direct+50ms early/5ms taper, same Gen19 SNR recipe. Only mixture 45/45/10 -> 65% dry-noisy / 25% rev-noisy / 10% dry-quiet.`

Decision rule: same `judge_v3.py` on same `screen_s17` material, same thresholds. PASS iff all `R1a,R1b,R1c,C,T,D,S2,S3,SP=True`. Retaining `R1` and fixing `D` required. Any post-hoc threshold relaxation, subgroup claim, or multi-recipe cherry-pick = invalid.

Seed-17 FAIL here permits a new preregistered GEN28, forbids promoting GEN27 or re-labelling this run as pass.

3. SUBMISSION.md Gen27 bullet:

> Gen27 added room reverberation to training and failed its pre-registered screen: reverberant test scores rose on average but dry-speech scores fell, with additional narrow misses on bench and spatial gates, so the model was not advanced. A follow-up will test a lower reverberation fraction to try to keep room gains without lowering dry-speech scores.
