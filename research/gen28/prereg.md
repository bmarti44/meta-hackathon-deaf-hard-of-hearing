# Gen 28 pre-registration: half the room dose (T0)

> Claude Opus 5.5, 2026-11-04 ~23:40 EST. Written before any Gen 28
> training.
> Source: Astra's and Muse's Gen 27 result reviews, both of which chose
> option (b): [../gen27/astra-review-gen27.md](../gen27/astra-review-gen27.md),
> [../gen27/muse-review-gen27.md](../gen27/muse-review-gen27.md).
> T0 in-silico only. `promoted FALSE`.
> Gen 27's record is unchanged, and this does not authorize Gen 27
> seeds 18/19.

## Question

Gen 27, with half of all noisy training examples in simulated rooms,
helped in held-out rooms (+0.514 dB) but cost dry noisy speech
(−0.23 / −0.49 dB). Does a smaller room dose keep a room gain of
≥ +0.30 dB without the dry cost?

## The one change (vs Gen 27)

| | Gen 27 (`aug50`) | Gen 28 (`aug25`) |
|---|---|---|
| P(reverberant \| noisy) | 0.5 | **0.25** |
| Dry noisy / reverberant noisy / dry quiet | 45 / 45 / 10% | **67.5 / 22.5 / 10%** |

`research/gen28/train15.py --room aug25`.

**Frozen from Gen 27:**
- seed 20261117, scratch, 24,000 updates, final checkpoint only;
- the same 602,510-parameter architecture, batch 8 × 2 s, SI-SDR loss,
  Adam 1e-3 cosine to 1e-4, clipping 5;
- Gen 19's speakers, SNR and noise recipe;
- Gen 27's corrected RIR manifest (`f306700d…`), split by room;
- per-talker RIRs from one train room;
- the direct-plus-50 ms target with 5 ms taper (audited onset rule);
- alignment, and augmentation RNG `[seed, 27]`.

The checkpoint and resume identity record `room_mode`. A changed mode is
refused on resume (test).

**Tests:** `test_train15.py`, 3/3 passing.
- `aug50` from train15 is bit-identical to Gen 27's train14 batches.
- `aug25` has the 67.5 / 22.5 / 10 shares, and its dry items equal the dry
  stream exactly (paired draws).
- Resume refuses a room-mode change.

## Judgment (unchanged from Gen 27)

- Gen 27's `judge_v3.py`, exactly as cleared at 2b548df (hash below),
  against **same-seed Gen 19** (not Gen 27).
- The same registered reverberant panel (material `5f7d268a…`), dry
  screen-v2 panel (`557ad44f…`), bench v2 and spatial bench.
- ADVANCE needs R1a ≥ +0.30 dB, R1b voice+room CI lo > 0, R1c ≥ 10/16
  voices, and C, T, D, S2, S3, SP all true. No rounding forgiveness and
  no retrospective tolerance.
- ADVANCE authorizes seeds 18/19 for this recipe only.

**Expectation, stated in advance:** dry exposure rises to 75% of Gen 19's,
which may recover dry performance but may push the room gain below
+0.30.

**Timing:** Gen 27 trained in 48.0 min, and the full pipeline took about
54 min. Never substitute an interim checkpoint.

Run: `research/gen28/pipeline.sh`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen28/train15.py` | `11ef7caced5ed60cff7b6628fa763586d8bbe049a1677f0afee3c5662886165f` |
| `research/gen28/test_train15.py` | `44d63116836833d80cb8165fc793a03b15201fbe57ae793671539e807cda7b6c` |
| `research/gen28/pipeline.sh` | `e9faa604a7d4f5e6c6c64daaaaeb59e6caf866bdc9b2822dc1f80b4d0dfa0a15` |
| `research/gen27/train14.py` | `9d39741c2e63aaa7773bd6e88165676a33ff207c034b215664a805b5c01567e7` |
| `research/gen27/rirbank.py` | `14376aafb87c73eaed6482d07b3958834b86b51b96100b7698d8e7ea7cc0e7f1` |
| `research/gen27/rir_manifest.json` | `f306700d0dce5aded749a5f48e6da6d6bc66a6bdce3d0e27677081a41b7c1711` |
| `research/gen27/panel_rev.py` | `875cd1eed0b869f0fee4631d9adcf0e91e0b90e25e88769a3718cdcd07efebf6` |
| `research/gen27/judge_v3.py` | `faa38995052d38de526fbc868baed6dab577bc0598c1c045dcb956023ba4beb7` |
| `research/gen27/registered_hashes.json` | `49fb96fd28ca1b4545fca5e2b8fda24390c914a7f1e818e5a56773f58a97b7d4` |
| `research/screen_v2/judge_v2.py` | `f35c88d3d08cc4a7bea2f38cf95918ff11f28eed22b394cae3c25c84acf0dcac` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/bench-n6/bench_v2.py` | `23d813395304b501d09a1b653a2bf6d5de1009b56dbace441e5b1daeed9bcb8d` |
| `research/gen24/train13.py` | `5ad336fc891dac7ceff79a63a78393a8d1a5166b88bee92c734f9841aafdce08` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
