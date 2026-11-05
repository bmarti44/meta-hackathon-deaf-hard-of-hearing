# Gen 36 pre-registration: output-contract repair for the published model (T0)

> Claude Opus 5.5, 2026-11-05 ~05:45 EST. Written before any candidate
> output was scored.
> Source: both reviewers' Gen 35 choice (b), with Astra's single
> conjunctive rule, adopted in
> [../gen35/astra-review-gen35.md](../gen35/astra-review-gen35.md).
> **No training, no selection.** A pass permits only an **owner-approved**
> inference release, with unchanged weights and `promoted FALSE`. Nothing
> is published by this registration.

## The one change: a frozen output contract (`enhance_v2.py`)

Versus the published `enhance.py` (snapshot at
`research/gen35/published/`, sha `59b65cda…`, identical to the file on
Hugging Face), and nothing else:

1. **Contract bound to the weights file.** The published safetensors are
   downloaded fresh from Hugging Face and verified **tensor-for-tensor
   equal** to the audited Gen 19 checkpoints (`contract.py`). Each
   file's sha256 maps to:

   | file | seed | polarity | decoder bias |
   |---|---|---|---|
   | `model.safetensors` (`3780d9f5…`) | 17 | −1 | +0.110101 |
   | `seed18.safetensors` (`36d56df8…`) | 18 | +1 | −0.164652 |
   | `seed19.safetensors` (`9cf2c8fa…`) | 19 | −1 | −0.145688 |

   - An unregistered file is refused, as is a bias that does not match.
   - The correction `polarity × (y − bias)` is applied right after delay
     removal, before any level step.
2. **DC handling:** level restoration uses the corrected, DC-free output,
   so the level budget is no longer spent on DC.
3. **Headroom:** one linear gain, capped after the final resampling:
   `out × min(1, 10^(−1/20) / max|out|)`, a −1 dBFS ceiling. The candidate
   is never hard-clipped.

Everything else is as published: mono mix-down, resampling to 16 kHz,
whole-file RMS 0.14 input gain (offline), and the delay flush. The public
interface is mono, so it makes no claim about two-ear direction.

## Comparators and panels (`run_contract.py`)

**Export arms:**
- **E0:** the published core followed by its CLI writer's `np.clip`.
- **E1:** E0 with the registered polarity (sign-only), also clipped.
- **C:** the candidate.

**Fresh, sealed panels** (`manifest.py` → `manifest.json`):
- **Source:** LibriSpeech **test-other**, never used in this repo.
  - Archive md5 `fb5a50374b501bb3bac4815ee91d3135` (OpenSLR); sha256 `d09c181b…`.
  - 8 targets (the 4 lowest-numbered F and M speakers) and 12 crowd voices (the next 6 F and 6 M).
  - The speaker lists are disjoint from every earlier list (asserted).
  - Material sha256 `4271a2d627063a2cb2ddadf9d625a65f26cd10367777a833df0417445715aed0`.
- **Encoding:** every output is **written and decoded** at 16 / 44.1 / 48 kHz, in WAV PCM_16, WAV FLOAT and FLAC PCM_16, and **scored as decoded**.
- **F1, noisy:** 8 targets × 2 utterances × SNR −5 / 0 / +5 / +10 = 64 items.
- **F2, target-only:** the 16 crops at input RMS 0.035 and 0.14, plus a labelled **overload** level (peak 1.5 × full scale).
  - 29 of the 48 items exceed full scale: all 16 overload items and 13 natural RMS-0.14 peaks.
  - Representability is sealed in `manifest.json` and never read from rows.

**Regression panels** (16 kHz, in memory, with the writer's clip emulated
for E0 / E1):
- X1: BRUDEX noisy, mono (192);
- X2: the screen-v2 dry panel (512);
- X3: BRUDEX target-only at RMS 0.035 / 0.14 / 0.56 (144); representability recomputed from the audio;
- X3q: the 64 quiet crops;
- X4: silence and 48 speech-to-silence transitions.

**Research path** (Gen 35 `Arms`), comparing **A2 vs the equally flushed
A1**:
- P1: BRUDEX, 240 items per ear;
- P4: 16 crossed spatial scenes;
- P6: silence and transitions.

## Decision (`judge_contract.py`, Astra's conjunctive rule)

**REPAIR ACCEPTED (inference only)** requires all of the following, for
every seed:
- **G0, well-formed and bound:**
  - exact key sets with unique keys, and only registered seed / arm groups;
  - every required metric numeric and finite;
  - release tensors and the contract table verified;
  - the fresh material hash equal to the seal.
- **G1:** α > 0 on every candidate target-only row (F2, X3, X3q).
- **G2, waveform and gain:**
  - mean `wave_err(C) < wave_err(E1)` in every target-only cell (F2 level × rate × format; X3 level; X3q);
  - on every **representable** target-only row, `wave_err(C) ≤ wave_err(E1)` and `|AC-gain error|(C) ≤ (E1)`. Peak attenuation therefore stays visible.
- **G3, noisy:** on every F1, X1 and X2 row, ΔSI-SDR ≥ −0.01 dB and **ΔSTOI_DC ≥ −0.001**, vs E1. STOI_DC is STOI on mean-removed signals; ordinary STOI is reported only.
- **G4, research path vs the equally flushed A1:**
  - ILD error +≤ 0.05 dB, and no ITD-error increase, on every P1 item and P4 scene;
  - lag 0 on every P1 target-only ear;
  - P6 RMS(A2) ≤ A1.
- **G5, headroom:**
  - candidate pre-write peak ≤ −1 dBFS;
  - decoded peaks ≤ −1 dBFS plus the codec's quantisation step;
  - no sample at full scale;
  - X4 silence / tail RMS(C) ≤ E0.

Otherwise: **INVESTIGATE**, with no fallback candidate and no threshold
rescue.

**Expectation, stated in advance:** G2's per-item gain check may fail
where the headroom cap binds on a representable item. That is the
level-vs-headroom trade-off made visible on purpose.

**Tests** (`test_gen36.py`, 5/5 passing):
- the candidate contract for all three release files (sign, DC, level when the cap does not bind, −1 dBFS when it does);
- refusal of an unregistered file;
- the judge accepts a complete, rule-satisfying synthetic run;
- the judge returns INVESTIGATE for each of 18 attacks: missing, duplicate, unregistered seed or arm, unsealed material, unbound contract, each gate violated, a boolean metric. A `representable` label in a row is ignored.

Run: `research/gen36/pipeline.sh`.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen36/enhance_v2.py` | `fdc64219588a034d5d027c855d565a3aeda5b2cc15d193a3fe952e0550b4c8a4` |
| `research/gen36/contract.py` | `89823ab6d0f0d7f066056ae5ed8cf93d1bc360b0b782093c2ad5391d296935ed` |
| `research/gen36/manifest.py` | `1726961f31e07ef89c685276029dedfe761c5301dea61d63eaba2de24fca58d5` |
| `research/gen36/manifest.json` | `727919ce414595cae8a575cf2677af6f469a9d13aa609b97302cbfce00e236d3` |
| `research/gen36/run_contract.py` | `4d3f6603ef5100aeabdd0700dff869baf0a2b8b956cf914bcc13599abaf7e5a6` |
| `research/gen36/judge_contract.py` | `77a375748b8d7a4890b062da7c99c22bd59fb9f243074ebc0bd3344581c2a754` |
| `research/gen36/test_gen36.py` | `0f466a01d10280c3299898cb1f19582bb905b2983a207b27d816c3e1db8e3400` |
| `research/gen36/pipeline.sh` | `ad893db7df797cfdd4d67613c08b4a0cfc1ca007edf7ad665018e854181a9c84` |
| `research/gen35/repair.py` | `9b822da5635fdec44aa6bfb5622d937623148d52592e45656b7ce32b53c16ebb` |
| `research/gen35/published/enhance.py` | `59b65cdaead7aca31d54fb73f1b1d2a7fcf6b3c1bb7feb07dcd42588d79611b5` |
| `research/gen35/published/model_causal.py` | `e09ca1e0e8b761ed7116d5291e08c196e97243f5a111faca0fe68a15a5f8e1da` |
| `research/gen34/recorded_panel.py` | `6aef539828ed399f77933fc61ef6f57c54de43400bfca40a7f5a7b5b012d312d` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen19/weights/causal_seed20261118.pt` | `ef098dfd429f20dcf7c199b6a534795c232a372a66af65e473fb5b6325a30916` |
| `research/gen19/weights/causal_seed20261119.pt` | `89837737be430645441d577c44f277e2fee6b76ffb6865f613e8d72ae6fdcb32` |
