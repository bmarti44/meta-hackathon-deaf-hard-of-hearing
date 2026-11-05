# Gen 30 pre-registration: one eighth of Gen 27's room dose, the final dose-only step (T0)

> Claude Opus 5.5, 2026-11-05 ~01:10 EST. Written before any Gen 30
> training.
> Source: Astra's Gen 29 review, choice (a), adopted in the disposition
> in [../gen29/astra-review-gen29.md](../gen29/astra-review-gen29.md).
> Muse chose (c) instead; that is queued as Gen 31.
> T0 only. `promoted FALSE`.
> Gen 27–29 records are unchanged. This authorizes no earlier seeds.

## The one change (vs Gen 29)

| | Gen 27 | Gen 28 | Gen 29 | **Gen 30** |
|---|---|---|---|---|
| P(reverberant \| noisy) | 0.5 | 0.25 | 0.125 | **0.0625** |
| Dry noisy / reverberant noisy / dry quiet | 45 / 45 / 10 | 67.5 / 22.5 / 10 | 78.75 / 11.25 / 10 | **84.375 / 5.625 / 10** |

`research/gen30/train17.py --room aug0625`.

**Frozen:** everything else is as in Gen 27–29.
- Seed 20261117, scratch, 24,000 updates, final checkpoint only. P is
  fixed before training: no parameter search, no checkpoint selection.
- The same 602,510-parameter architecture, batch 8 × 2 s, SI-SDR,
  Adam 1e-3 cosine to 1e-4, clipping 5.
- Gen 19's speakers, SNR and noise recipe.
- The corrected RIR manifest `f306700d…` and its splits, per-talker
  RIRs, the direct-plus-50 ms target and taper, alignment, and
  augmentation RNG `[seed, 27]`.
- The room mode is recorded in the checkpoint and resume identity.

**Tests:** `test_train17.py`, 3/3 passing.
- train17 `aug125` is bit-identical to Gen 29's train16.
- `aug0625` has the 84.375 / 5.625 / 10 shares, and its dry items equal
  the dry stream.
- Resume refuses a room-mode change.

## Judgment (unchanged)

- Gen 27's `judge_v3.py` (cleared at 2b548df), against **same-seed
  Gen 19**, on the same registered materials. Its printed "GEN27
  SCREEN" label is a hard-coded string.
- ADVANCE needs R1a ≥ +0.30 dB, R1b CI lo > 0, R1c ≥ 10/16, and C, T,
  D, S2, S3, SP all true. No tolerance or rounding forgiveness; D needs
  non-negative means and lower bounds > −0.15 dB / > −0.003 at both
  SNRs.
- Gen 30 − Gen 29 deltas for the primary and dry scores are reported
  descriptively.
- ADVANCE authorizes seeds 18/19 only, followed by fresh-material
  confirmation.

## Campaign boundary (new, registered here)

**Any Gen 30 failure ends the dose-only campaign, even if R1a passes**
(Astra, Gen 29 review). No further dose values are tried. The next
approach is Gen 31 (Muse's choice: fine-tune Gen 19 on the room mix, then
blend weights back toward Gen 19 with the blend fixed on a separate
validation split). Gen 31 gets its own registration and Astra pre-launch
review.

**Expectation, stated in advance:** R1a may fall below +0.30 (Muse);
passing cannot be predicted (Astra).
Gen 29 trained in 36.7 min; never substitute an interim checkpoint.

Run: `research/gen30/pipeline.sh`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen30/train17.py` | `3966507a07ec470d505668a5575ff05efb278bd75f79cd079d9e9d6e96eacbfa` |
| `research/gen30/test_train17.py` | `88c71abb1cd1e221192d1e23f8b9682bbbf1dfa79a4775cd8c1e2cf8e5ae0de4` |
| `research/gen30/pipeline.sh` | `5c65687fb3474516cae28d62c78a86a54a1e11819901029c83ea84397d795232` |
| `research/gen29/train16.py` | `175bf1aec6cac34f0d90a104696db061d04b04e41619e1e20ab6c2874c7d072a` |
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
