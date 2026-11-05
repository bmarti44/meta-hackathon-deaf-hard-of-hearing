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

Every registered metric is blind to both. The published Hugging Face
`enhance.py` inherits both; it then rescales the output to the input RMS
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

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen35/repair.py` | `37165c117d69e7fb477d305d9ae7aaa929f303c5fe6b7703f787ddd24867e57b` |
| `research/gen35/run_repair.py` | `99e6dddaa70c23bce15fbb887f9b235213b0024dd76bda581eb7a04e05db2fe7` |
| `research/gen35/judge_repair.py` | `2e4b38b6fcc8e7d2f4e369f46b6fcea06d778f14ee79439803694668a17e714f` |
| `research/gen35/test_gen35.py` | `e47339078748dd89a2339d7cc813cff880a5ec0914db5e03fcda408b6e573d9b` |
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
