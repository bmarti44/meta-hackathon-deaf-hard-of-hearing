# Muse (Meta) pre-launch review of Gen 33 — verbatim

> Meta **Muse Spark** (`muse-spark-1.3`), effort `medium`, via the Meta Model API (Lambda direct-invoke `review` mode), 2026-11-05 ~02:51.
> - It received the registration text inline and was asked to judge the design only.
> - Its notes 1 (per-ear and worst-ear) and 4 (target-only cue subsets) are adopted as descriptive additions in pre-launch amendment 1.

## Verbatim answer

CLEARED FOR LAUNCH

Blocking items: none for T0 in-silico feasibility.
- Frozen weights, no training/tuning, no selection: `m=mask_net((zL+zR)/2)` only. Explicit no alternative pooling after result.
- Cannot rescue Gen 32: `promoted FALSE`, never ADVANCE, Gen 32 stays FAIL, identical-ear parity acknowledged. Mono R1a/D unchanged by construction.
- Leakage controls adequate: identical-ear bit-exact mono rebuild, ear-swap symmetry, causality (future unchanged), independent mode reproduces `spatial_wiseftpd_s17.json` + Gen 19 self-test, fake-linked rejection.
- Cue protection: L1 keeps original `judge_v3.spatial_gates` unchanged, L2 requires 16-scene mean ILD < independent Gen 32, L3 requires mean ILD and ITD <= independent Gen 19 in all 8 subsets (4 SNR x 2 mirror-pairs, 2 scenes each =16). L4 requires pooled per-ear SI-SDR/STOI >=0 vs both Gen 32-ind and Gen 19-ind in all noisy + target-only subsets.
- Hardware correctly caved: sync, Nucleus 6 I/O unverified, no clinical claim. Linked-AGC cited as rationale only.

Non-blocking notes:
1. L4 pools both ears. Mean >=0 can hide L-loss compensated by R-gain. For bilateral cue users, future confirmation should gate each ear separately, plus worst-ear.
2. n=2 scenes/subset means L3/L4 means (16 ILD/ITD + ~64 SI-SDR/STOI checks) are high-variance. All-must-pass is fail-safe for false pass, but a single pass is weak evidence; replication required as stated.
3. L2 is strict inequality with no margin; trivial epsilon wins. Only meaningful with L3+L4 jointly passing.
4. Target-only ILD/ITD subset definition not enumerated; lock to same 8 mirror subsets before run.
