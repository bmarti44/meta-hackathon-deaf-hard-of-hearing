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
  - Material sha256 `4271a2d6…` (superseded by amendment 1).
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

## Pre-launch amendment 1 (2026-11-05 ~06:20, before any candidate output was scored)

Astra's first pre-launch review was **NOT CLEARED**, with five blocking items
([astra-prelaunch-review.md](./astra-prelaunch-review.md)). Fixes:

1. **The contract is now implemented as declared.**
   - The polarity / bias correction comes right after delay removal.
   - The final resampling happens next, then **explicit removal of the output's whole-file mean**.
   - Last, **one final linear gain**: `g = min(DC-free input RMS / output RMS, −1 dBFS / output peak)`.
   - Both levels are DC-free.
   - The model class is loaded **from the published `model_causal.py` by file path**. Before, the name resolved to Gen 15's module. The published `enhance.py` (E0) is made to bind that same module, and this is asserted.
2. **The rule is restored to its full coverage.**
   - G2 now uses X3 cells per level × setting.
   - Every export target-only row, **overload included**, must not worsen in waveform error or |AC-gain error|.
   - Research P1 target-only preservation is added: per setting × ear means, and per item-ear.
   - G1 now covers A2 on P1 target-only ears.
   - G3 adds per-ear SI-SDR and STOI_DC for A2 vs A1 on every P1 noisy item and P4 scene.
   - G4 gates export lag(C) = 0.
3. **Strict schema.**
   - Every key field must be present with its registered type: no booleans, and no missing field read as null.
   - Every metric must be numeric, finite and inside its domain (peaks, RMS, ILD, ITD and |gain| ≥ 0; saturation in [0, 1]; lags are integers).
   - Unregistered seeds and arms are rejected.
4. **Complete binding.**
   - Each seed's fresh material hash must equal the seal.
   - With `rebuild`, the manifest is rebuilt from the audio and must reproduce the seal.
   - Release safetensors, `config.json` (`0eb99ef2…`), `enhance.py` and `model_causal.py` are all bound, the last both as the snapshot and as the Hugging Face file (`e09ca1e0…`, verified identical).
   - The contract table must equal `contract.build_table()`.
5. **No unlabelled overload.**
   - Each F1 mixture and its clean target are scaled by one gain to a −6 dBFS mixture peak, so all 64 × 3 F1 item-rates are representable.
   - Representability is sealed **per item and rate** for F1 and F2: 87 of 144 F2 item-rates exceed full scale, and they are labelled.
   - New material sha256: `006258a8e7eef74dc83989981fcc24079cb2289ac77d3e7dbbc06a30bbaf692f`.

**Expectation, stated in advance:** G2's no-worsening check on |AC-gain
error| for overload and capped items may fail. That is the level-vs-headroom
trade-off, made visible on purpose.

**Tests:** `test_gen36.py`, 5/5 passing. The judge test now covers 30
attacks, including every one from Astra's review: a missing P1 `snr` key,
boolean identities, a negative peak or gain, an incomplete per-seed hash,
config and module rebinding, a whole X3 setting with no improvement, an
overload item that worsens, and export lag.

The hash table is updated below.

## Pre-launch amendment 2 (2026-11-05 ~06:45, before any candidate output was scored)

Astra's verification of amendment 1 was **NOT CLEARED**, with three items.
Fixes:

1. **Manifest binding.**
   - The judge pins `manifest.json`'s bytes (`MANIFEST_SHA`) and refuses any other content.
   - With `rebuild`, it rebuilds the manifest from the audio. The hash, the target and crowd lists, and every F1 / F2 item identity and per-rate representability must all equal the seal.
   - A refusal is caught by `judge_safe`, which now also catches `SystemExit`, and becomes INVESTIGATE rather than a crash.
2. **Research target preservation.** Per-ear |AC-gain error| is now recorded on P1 target-only items, and gated by item-ear non-worsening of A2 vs A1.
3. **Metric domains.** STOI and STOI_DC, including per-ear fields, must lie in [−1, 1].

**Tests:** `test_gen36.py`, 6/6 passing. They now include Astra's attacks:
- A2 AC-gain errors worsening to 9 dB;
- STOI_DC = 2 on F1 and on P4 per ear;
- STOI = −1.5;
- the manifest tampered in memory, with 63 of 64 F1 items removed and the claimed hash kept, with `rebuild=True`.

The hash table is updated below.

## Source hashes (sha256)

| File | sha256 |
|---|---|
| `research/gen36/enhance_v2.py` | `2045914cbea9590209d2ec7d37452b31758138ec12618e9cd910d220e259ff16` |
| `research/gen36/contract.py` | `9e11fea5ea2c8a6f36fedf544f4c51820cd3359f2a7fffa6b0beffcd20a3057c` |
| `research/gen36/manifest.py` | `95514afc1cb7a0c97abc2781355341977bf363516be576c7cf5a748c97d69925` |
| `research/gen36/manifest.json` | `41dc19934a8ee955b60d596bb793dc65eea94734d9e687143c57345710793550` |
| `research/gen36/run_contract.py` | `b3e765785e01c941754a60f5180c56170c24dde9284b0dde3f4f01dd37c3a5da` |
| `research/gen36/judge_contract.py` | `61553de9191f7a42ebe2b3928cc773f9a2f21d7a94ef431ea03b4eb8a5058478` |
| `research/gen36/test_gen36.py` | `d619787ef19ee6c1453eec41c3d55b48ab216d2e69d36fffa6051506a1e62d4b` |
| `research/gen36/pipeline.sh` | `ad893db7df797cfdd4d67613c08b4a0cfc1ca007edf7ad665018e854181a9c84` |
| `research/gen35/repair.py` | `9b822da5635fdec44aa6bfb5622d937623148d52592e45656b7ce32b53c16ebb` |
| `research/gen35/published/enhance.py` | `59b65cdaead7aca31d54fb73f1b1d2a7fcf6b3c1bb7feb07dcd42588d79611b5` |
| `research/gen35/published/model_causal.py` | `e09ca1e0e8b761ed7116d5291e08c196e97243f5a111faca0fe68a15a5f8e1da` |
| `research/gen34/recorded_panel.py` | `6aef539828ed399f77933fc61ef6f57c54de43400bfca40a7f5a7b5b012d312d` |
| `research/screen_v2/panel_v2.py` | `d4c83a33bd2d88b5301dfcb218a8dc43e34559248ee9b6df6600102c4a5e408e` |
| `research/gen19/weights/causal_seed20261117.pt` | `80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367` |
| `research/gen19/weights/causal_seed20261118.pt` | `ef098dfd429f20dcf7c199b6a534795c232a372a66af65e473fb5b6325a30916` |
| `research/gen19/weights/causal_seed20261119.pt` | `89837737be430645441d577c44f277e2fee6b76ffb6865f613e8d72ae6fdcb32` |
