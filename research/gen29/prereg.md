# Gen 29 pre-registration: a quarter of Gen 27's room dose (T0)

> Claude Opus 5.5, 2026-11-05 ~00:20 EST. Written before any Gen 29
> training.
> Source: Astra's and Muse's Gen 28 reviews, both of which chose option
> (a): [../gen28/astra-review-gen28.md](../gen28/astra-review-gen28.md),
> [../gen28/muse-review-gen28.md](../gen28/muse-review-gen28.md).
> T0 only. `promoted FALSE`.
> Gen 27 and Gen 28 records are unchanged. This authorizes no earlier
> seeds.

## The one change (vs Gen 28)

| | Gen 27 | Gen 28 | **Gen 29** |
|---|---|---|---|
| P(reverberant \| noisy) | 0.5 | 0.25 | **0.125** |
| Dry noisy / reverberant noisy / dry quiet | 45 / 45 / 10 | 67.5 / 22.5 / 10 | **78.75 / 11.25 / 10** |

`research/gen29/train16.py --room aug125`.

**Frozen:** everything else is as in Gen 27 and Gen 28.
- Seed 20261117, scratch, 24,000 updates, final checkpoint only.
- The same 602,510-parameter architecture, batch 8 × 2 s, SI-SDR,
  Adam 1e-3 cosine to 1e-4, clipping 5.
- Gen 19's speakers, SNR and noise recipe.
- The corrected RIR manifest `f306700d…` and its splits, per-talker
  RIRs, the direct-plus-50 ms target and taper, alignment, and
  augmentation RNG `[seed, 27]`.
- The room mode is recorded in the checkpoint and resume identity.

**Tests:** `test_train16.py`, 3/3 passing.
- train16 `aug25` is bit-identical to Gen 28's train15.
- `aug125` has the 78.75 / 11.25 / 10 shares, and its dry items equal the
  dry stream.
- Resume refuses a room-mode change.

## Judgment (unchanged)

- Gen 27's `judge_v3.py` (cleared at 2b548df), against **same-seed
  Gen 19**, on the same registered materials.
- ADVANCE needs R1a ≥ +0.30 dB, R1b CI lo > 0, R1c ≥ 10/16, and C, T,
  D, S2, S3, SP all true. No tolerance; D needs non-negative means and
  lower bounds > −0.15 dB / > −0.003 at both SNRs.
- Gen 29 − Gen 28 deltas for the primary and dry scores are reported
  descriptively.
- ADVANCE authorizes seeds 18/19 only.

**Stopping rule** (Muse, adopted in the Gen 28 disposition): if R1a falls
below +0.30, the dose taper stops and the next generation changes the
approach rather than cutting the dose further.

**Expectation, stated in advance:** D may still fail (both reviewers).
Gen 28 trained in 37.2 min; never substitute an interim checkpoint.

Run: `research/gen29/pipeline.sh`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen29/train16.py` | `175bf1aec6cac34f0d90a104696db061d04b04e41619e1e20ab6c2874c7d072a` |
| `research/gen29/test_train16.py` | `34d01295073f06e1d8763fe50f57038d1303126974af9b83718abe9c030cd1f7` |
| `research/gen29/pipeline.sh` | `3e5e75d3c3d3c3dcdfef2ffa930afa4a72d39499b9cb21302692fc70714ab971` |
| `research/gen28/train15.py` | `11ef7caced5ed60cff7b6628fa763586d8bbe049a1677f0afee3c5662886165f` |
| `research/gen27/train14.py` | `9d39741c2e63aaa7773bd6e88165676a33ff207c034b215664a805b5c01567e7` |
| `research/gen27/rirbank.py` | `14376aafb87c73eaed6482d07b3958834b86b51b96100b7698d8e7ea7cc0e7f1` |
| `research/gen27/rir_manifest.json` | `f306700d0dce5aded749a5f48e6da6d6bc66a6bdce3d0e27677081a41b7c1711` |
| `research/gen27/panel_rev.py` | `875cd1eed0b869f0fee4631d9adcf0e91e0b90e25e88769a3718cdcd07efebf6` |
| `research/gen27/judge_v3.py` | `faa38995052d38de526fbc868baed6dab577bc0598c1c045dcb956023ba4beb7` |
| `research/gen27/registered_hashes.json` | `49fb96fd28ca1b4545fca5e2b8fda24390c914a7f1e818e5a56773f58a97b7d4` |
| `research/screen_v2/judge_v2.py` | `f35c88d3d08cc4a7bea2f38cf95918ff11f28eed22b394cae3c25c84acf0dcac` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
