# Gen 35 pre-registration: frozen output-path repair audit (T0)

> Claude Opus 5.5, 2026-11-05 ~04:25 EST. Written before any repaired
> output was scored.
> Source: Astra's Gen 34 review, choice (c), adopted in
> [../gen34/astra-review-gen34.md](../gen34/astra-review-gen34.md).
> **No training, selection or gate change.** A pass authorises an inference
> repair only. `promoted FALSE`. Gen 34 stays unchanged and is reported
> separately.

## Why

Gen 34 found that the frozen models' output is **sign-flipped** for Gen 19
seeds 17 and 19, and that it carries a **DC offset** equal to the decoder
bias:
- seed 17: +0.110;
- seed 18: −0.165;
- seed 19: −0.146.

Every registered gate metric is blind to both; Gen 34's added waveform
error is not (Astra). The published Hugging Face `enhance.py` inherits
both; it then rescales the output to the input RMS
with the DC still in the signal.

## The one change: three predefined output arms (`repair.py`)

For each frozen Gen 19 checkpoint (seeds 17 / 18 / 19):
- **A0 existing:** the Gen 34 v1 research path, `undelay(model(x))`. Its
  last 63 samples are zero padding.
- **A1 sign:** `polarity × flushed(model(x))`. The model runs on x plus 63
  zeros, and `out[63 : 63 + n]` is kept, exactly as in the published
  `enhance.py`.
- **A2 repair:** `polarity × (flushed(model(x)) − decoder_bias)`.

**Polarity** is a registered constant per checkpoint, bound to its sha256,
from `research/gen34/polarity_check.json`: −1 / +1 / −1. It is never
estimated per utterance or per ear. The bias is read from the checkpoint.
Nothing is fitted.

**Exported entry point:** `export_enhance` reproduces the published
`enhance.py` (snapshot in `published/`, tested to within 1e-6). It is
audited as published and with the same repair inserted before its RMS
restore. This is reported, not gated; the entry point is mono and cannot
speak to direction.

## Panels (`run_repair.py`)

- **P1:** the Gen 34 BRUDEX asset, 240 items (192 noisy, 48 target-only),
  per ear.
- **P2:** the screen-v2 dry development panel, 512 items.
- **P3:** its 64 clean crops alone (quiet).
- **P4:** the 16 crossed spatial scenes.
- **P5:** the 48 BRUDEX target-only items at three fixed input levels,
  RMS 0.035 / 0.14 / 0.56.
- **P6:** 2 s of silence, and speech-to-silence transitions (3 s of speech
  then 2 s of silence, scoring the last 1.5 s).
- **P7:** the exported entry point on target-only items at the three
  levels, and on silence.

## Decision (`judge_repair.py`, Astra's rule; engineering tolerances, not clinical margins)

**REPAIR ACCEPTED (inference only)** requires all of the following for A2,
in every seed:
- **V0:** rows are complete, and **A0 seed 17 reproduces Gen 34's audited
  Gen 19 rows exactly**.
- **R1:** the signed projection α > 0 on every target-only clip and ear
  (P1, P3, and P5 at all three levels).
- **R2:** mean target-only waveform error is below A1's for every seed ×
  setting × ear.
- **R3:** no P1 noisy item-ear and no P2 item loses more than 0.01 dB
  SI-SDR or 0.001 STOI vs A0.
- **R4:** no P1 item or P4 scene has ILD error up by more than 0.05 dB, or
  any ITD error increase, vs A0.
- **R5:** clipping does not rise on any P1 or P5 row-ear; the alignment lag
  is 0 on every P1 target-only ear; RMS on silence and on every transition
  tail is ≤ A0's.

Otherwise: **INVESTIGATE**, with no threshold rescue. P7 is reported
descriptively.

**Expectation, stated in advance:**
- Sign and DC do not affect SI-SDR, STOI or ILD, so R3 and R4 should hold,
  apart from the flushed last 63 samples.
- R1, R2 and R5 test whether the repair does what it claims.

**If accepted:** the owner is asked about publishing a config-level
polarity and bias patch to Hugging Face, with a version bump, bound to the
checkpoint hashes and with the weights unchanged. Nothing is published
without the owner's go-ahead.

**Tests:** `test_gen35.py`, 5/5 passing. They cover:
- the registered polarity;
- A0 being exactly the v1 path for all three seeds;
- A1 vs A2 differing by the bias;
- A2 positively signed with lower DC;
- the v1 padding;
- the export matching the published file, with its repair fixing sign
  and DC.

Run: `research/gen35/pipeline.sh`.

## Pre-launch amendment 1 (2026-11-05 ~04:45, before any repaired output was scored)

Astra's first pre-launch review was **NOT CLEARED**, with four blocking items
([astra-prelaunch-review.md](./astra-prelaunch-review.md)). Fixes:

1. **V0 completeness.**
   - Each panel × seed × arm must hold **exactly** the registered key set, with unique keys matched across arms.
   - Every required metric must be present, numeric (not boolean) and finite.
   - Malformed input gives INVESTIGATE, never a pass.
2. **Full rule coverage.**
   - R2 adds P3 and every P5 level × setting × ear.
   - R3 adds P4 per-ear SI-SDR/STOI (now computed).
   - R5 checks clipping on every row-ear in P1–P6, and the lag on every target-only ear or clip in P1, P3 and P5.
3. **The exported entry point is now gated, separately.**
   - Arms: E0 published / **E1 sign-only** / E2 repaired.
   - Panels: X1 BRUDEX noisy, X2 dry, X3 target-only at three levels plus X3q quiet crops, X4 silence and speech-to-silence transitions.
   - Checks E1 / E2 / E3 / E5 mirror R1 / R2 / R3 / R5.
   - The waveform error is **unadjusted**: the export restores output to the input's RMS, and for target-only input the input is the reference.
4. **Polarity binding.**
   - All three sha256 → polarity entries are frozen in `repair.POLARITY`. Any other checkpoint is refused, and the table is cross-checked against the Gen 34 evidence.
   - V0 validates provenance.
5. The wording "every registered metric is blind to both" is corrected (above).

**Tests:** `test_gen35.py`, 7/7 passing. They now:
- confirm that a complete, rule-satisfying synthetic run is accepted;
- reproduce Astra's attacks (a missing P2 item; the P5 high level replaced by duplicates; X4 silence replaced by a duplicate), plus a missing metric, a boolean metric, a wrong checkpoint hash, whole-panel waveform-error worsening in P3 / P5 / X3 / X3q, a P4 per-ear loss, P2 clipping, a P3 lag, an X1 STOI loss and X4 silence RMS. Each must give INVESTIGATE;
- check that an unregistered checkpoint is refused.

The hash table is updated below.

## Pre-launch amendment 2 (2026-11-05 ~04:55, before any repaired output was scored)

Astra's verification of amendment 1 was **NOT CLEARED**, with two blocking
items. Fixes:
1. **Gate applicability comes from the registered key.** A P1 item is
   target-only exactly when its SNR is null. The `cond` label must match it,
   and a mismatch is INVALID, so relabelling a target-only row as noisy can
   no longer skip R1, R2 or R5.
2. **Unregistered seed or arm groups are rejected** before completeness is
   evaluated.

Tested by her two attacks (a relabelled row with negative α, +100 dB error
and an 80-sample lag; an extra seed; an extra arm with null metrics), and by
the same bad values without relabelling. `test_gen35.py` is 7/7. The hash
table is updated below.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen35/repair.py` | `9b822da5635fdec44aa6bfb5622d937623148d52592e45656b7ce32b53c16ebb` |
| `research/gen35/run_repair.py` | `62b29c39ffc58299279909cf5492d7a48d66bc8792506d8b75d1421724e8d6a9` |
| `research/gen35/judge_repair.py` | `faa85583a46c4a9566f356d87387c49b3b76b8c29ed64ed57910fde67f3be70f` |
| `research/gen35/test_gen35.py` | `041187d552cdf4767ffebf7370ac4105a46cc799be9510826c50ab4501fa8ab9` |
| `research/gen35/pipeline.sh` | `c2da453df248cacc5c6c82a6f4d26e9043fcc80be7bdb1d9f4cbc3ce714cad9a` |
| `research/gen35/published/enhance.py` | `59b65cdaead7aca31d54fb73f1b1d2a7fcf6b3c1bb7feb07dcd42588d79611b5` |
| `research/gen35/published/model_causal.py` | `e09ca1e0e8b761ed7116d5291e08c196e97243f5a111faca0fe68a15a5f8e1da` |
| `research/gen34/polarity_check.json` | `53782c4aafe6669107e48946ffdb322a79988174b7185ff9069a6f774cb7df74` |
| `research/gen34/recorded_panel.py` | `6aef539828ed399f77933fc61ef6f57c54de43400bfca40a7f5a7b5b012d312d` |
| `research/gen34/audit_s17.json` | `bbbfe5340597b285d8f460bacc9242a570da1d51fd197f3710d7eb2872b7ae32` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/gen15/model_causal.py` | `c357bc178448631c0349d80876636ae7d1e0b46d90abf057115c44799507a674` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen19/weights/causal_seed20261118.pt` | `ef098dfd429f20dcf7c199b6a534795c232a372a66af65e473fb5b6325a30916` |
| `research/gen19/weights/causal_seed20261119.pt` | `89837737be430645441d577c44f277e2fee6b76ffb6865f613e8d72ae6fdcb32` |
