# Gen 11 J4-A1 build report — causality by construction + test

> **Model routing.** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> Source spec: [candidate-J4-causal.md §2](../gen10/candidate-J4-causal.md).
> **What this is:** a runnable PyTorch implementation of J4-A1 plus
> machine-checked causality evidence (T0, in-silico).
> **What this is not:** efficacy evidence of any kind. No listener,
> SRT, power, or on-processor latency claim is made or implied.
> The training run below is a labelled **T0 smoke test only**.

## Files

| File | Contents |
|---|---|
| [j4_model.py](./j4_model.py) | `J4A1` model: causal framing, 64-band log filterbank features, per-frame norm, 2×128 unidirectional LSTM, sigmoid mask, envelope-mask output |
| [test_j4.py](./test_j4.py) | 7 tests (pytest or plain `python test_j4.py`): suffix-invariance ×3, static graph audit, streaming==sequence, params/MACs, latency |
| [train_smoke.py](./train_smoke.py) | 200-step synthetic training smoke (T0 only) |
| This file | Build report with measured outputs |

Environment: reused `/tmp/gen9env` (Python 3.11.17, torch 2.15.0 CPU,
6 threads) + `pytest 9.2.0` installed into it via `uv`.
Hardware: **Apple M5 Max** (`sysctl machdep.cpu.brand_string`),
macOS 26.6 arm64. All numbers below are this machine, this run.

Run commands:

```bash
/tmp/gen9env/bin/python research/gen11/j4_model.py
/tmp/gen9env/bin/python -m pytest research/gen11/test_j4.py -q
/tmp/gen9env/bin/python research/gen11/test_j4.py
/tmp/gen9env/bin/python research/gen11/train_smoke.py
```

## Architecture as built (spec §2 mapping)

| Spec row | Built | Where |
|---|---|---|
| `fs` 16,000 Hz | 16,000 | `FS` |
| `W`=128 (8 ms), right-aligned, **no centre padding** | Frame *j* = samples `[jH, jH+W−1]` via `unfold`; **no waveform padding anywhere** — input shorter than 128 samples yields 0 frames | `frame_signal`, `num_frames` |
| `H`=64 (4 ms, 250 fps) | 64; 1 s → 249 frames | `H` |
| Future frames `L`=0 | No operation reads frame > *j* (tested, §Tests) | whole graph |
| Context `K`=5 (*j−4…j*) | Mask *j* computed after stepping frames *j−4…j* through the LSTM; carried state also summarises earlier frames (still ≤ *j*). Frames *j*<4 run from zero state (spec §3.2 priming) | `step`, `forward_features` |
| Bands `B`=64 (PROPOSED) | 64 triangular mel bands (50 Hz–8 kHz) over the 128-pt rFFT of the Hann-windowed frame; fixed buffer, 0 parameters | `mel_filterbank` |
| Features `F_j` = log band energies of frame *j* only; no deltas | `log(band_energy + 1e-8)`; no delta features at all | `extract_features` |
| 2×128 **unidirectional** LSTM | Two forward-only `UniLSTMCell` layers, state carried forward only | `UniLSTMCell`, `cells` |
| FC + sigmoid → mask `M_j` for frame *j* | `Linear(128→64)` + sigmoid, applied to frame *j* in the same hop; no mask smoothing | `fc`, `step` |
| Normalisation: causal only | **Per-frame layer norm over the band axis of `F_j` alone**, no affine parameters (`F.layer_norm`, statistic set = {`F_j`}). No batch/segment statistic exists in the graph | `causal_norm` |
| Convolutions: none in core path | None | — |
| Attention/pooling: none | None | — |
| Envelope-mask output, **no waveform OLA** | Outputs are `(masks, masked_envelopes)`, both `(batch, T, 64)`; `masked = M_j · env_j`. There is no synthesis path to call | `forward` |

### One deliberate deviation in mechanism, none in accounting

Spec §3.4 counts each LSTM layer as `4h·(in+h+1)` — **one** bias vector.
`torch.nn.LSTM` carries two (`bias_ih`, `bias_hh`), which would build
239,680 parameters (+1,024) against the filed 238,656. The LSTM cell is
therefore implemented directly with a single fused bias, so the **built
graph** matches the filed count exactly (verified from tensor shapes
below, not from the formula).

### Note on spec §3.2 finite span vs persistent state

§3.2 files a 384-sample (24 ms) total span per mask, which holds if the
LSTM is re-run windowed over exactly *j−4…j* from zero state. A
persistent-state unidirectional LSTM (this build; also the reading under
which §3.4's 237,568 MACs/**frame** is one step per frame, not five)
depends on all frames ≤ *j*. Both readings are strictly frame-causal and
both give suffix Δ=0. They differ in memory span and in MACs per output
mask (windowed re-run ≈ 5× the recurrent term). HP-J4-1 should pin which
reading is ratified; the causality claims in this report hold either way,
the §3.2 "24 ms span" sentence holds only under the windowed reading.

## Tests — outputs (this run)

`pytest`: **`7 passed in 1.55s`.** Plain-script run, verbatim:

```text
PASS (1a) suffix-invariance waveform: prefix Delta exactly 0
PASS (1b) suffix-invariance truncation: Delta exactly 0
PASS (1c) impulse probe: no frame ending before impulse changes
PASS (2) static frame-causality: index/norm/barred-module audits
PASS (2b) streaming step == sequence forward, bitwise
PASS (3) params = 238,656 and MACs/frame = 237,568 (spec S3.4)
PASS (4) CPU latency per frame: ... (below)
```

### (1) Suffix-invariance — Δ = 0 exactly (spec §2.5 item 3)

Identical 0.5 s prefix + three suffixes (noise ×0.1, noise ×3.0, silence).
On all 124 frames fully inside the shared prefix, masks **and** masked
envelopes are `torch.equal` — bitwise identical, max |Δ| = 0.0 — for both
alternative suffixes. Truncation variant: outputs from a stream cut at
⅓ s are bitwise equal to the head of the full-stream outputs.
Impulse probe: an impulse at sample 4,000 changes no frame ending before
sample 4,000, and does change later frames (probe is live, test not
vacuous); suffixes likewise change post-prefix outputs (asserted).

Negative control (probe script, `/tmp/gen11_probe.py`): replacing the
per-frame norm with a barred whole-segment statistic makes the same
prefix comparison fail loudly — max prefix feature difference **4.118**
— vs **0.0** for the built causal norm. The test can detect the Gen 9
failure mode; the build does not have it.

Exactness scope, stated plainly: Δ=0 is bitwise for a fixed stream/batch
configuration (the §2.5 replay protocol). The same waveform run at a
different **batch size** differs by ≤ 6×10⁻⁸ (float GEMM blocking) — a
numeric artefact, not information flow: no operation in the graph mixes
batch rows. Deployment is a single stream.

### (2) Static frame-causality check (spec §2.5 items 1–2)

- **Index audit:** `frame_bounds(j) = (j·64, j·64+127)`; max input sample
  for output *j* is `jH+W−1`, as required. K=5 entry span:
  `(K−1)H + W = 384` samples.
- **Norm audit:** no `LayerNorm`/`GroupNorm`/`BatchNorm` module exists in
  the tree; the only normalisation is parameter-free per-frame
  `F.layer_norm` over the band axis (statistic set {`F_j`} ⊆ frames ≤ *j*),
  read from source in `causal_norm`.
- **Barred-module audit:** asserted absent — `nn.LSTM/GRU/RNN` (hence no
  bidirectional path), any `Conv*`/transposed conv, batch norm,
  `MultiheadAttention`/`Transformer`, any temporal pooling.
- **Framing audit:** `num_frames(127)=0`, `num_frames(128)=1`,
  `num_frames(16000)=249` — the no-padding formula.
- **Streaming audit:** frame-by-frame `step()` from zero state reproduces
  sequence `forward()` **bitwise** — the deployed streaming unit and the
  audited sequence graph are the same computation.

### (3) Parameters and MACs vs spec §3.4

Recounted from built tensor shapes (independent of the closed form):

```text
L1 = 98,816   L2 = 131,584   FC = 8,256   total = 238,656  (spec 238,656) ✓
MACs/frame = 237,568  (spec 237,568) ✓   -> 59.4 MMAC/s at 250 fps
j4_model.py main: params=238656 spec=238656 | MACs/frame=237568 spec=237568
                  1 s in -> masks (2, 249, 64), masked env (2, 249, 64)
```

### (4) CPU latency per frame — measured (Apple M5 Max, torch 2.15.0, 6 threads)

Frame deadline (hop) = **4.0 ms**. Two measurement passes in the test run:

| Quantity | Pass 1 | Pass 2 |
|---|---|---|
| `step()` median (feature frame → mask) | 0.042 ms | 0.047 ms |
| `step()` mean | 0.044 ms | 0.053 ms |
| `step()` p99 | 0.048 ms | 0.142 ms |
| `step()` max (249 frames) | 0.104 ms | 0.331 ms |
| End-to-end per frame (waveform → masks, incl. FFT/filterbank) | 0.060 ms | 0.059 ms |

Every figure is >10× under the 4.0 ms hop deadline **on this laptop CPU**.
This is a desktop-class ARM core, not a Nucleus-class processor: it shows
the graph is cheap, it does **not** fill HP-J2-1, predict bench p99, or
say anything about power (spec §3.4: no mW figure is derivable, none is
offered). Algorithmic latency is unchanged from spec §3.1: T_window
8.0 ms + lookahead 0 + synthesis 0.

## Training smoke — T0 only, NOT efficacy

Synthetic speech-like signals: harmonic stacks (f0 90–250 Hz with wander,
1/h tilt, two formant bumps, ~4 Hz syllabic AM with voicing gaps) + white
noise at random −5…+10 dB SNR. Target: ideal ratio mask in the model's
own filterbank from the clean/noise components (offline target, spec §4
admissible). Adam, lr 3e-3, batch 8 × 0.5 s, mask-MSE, 200 steps:

```text
step   0  mask-MSE 0.18510
step  50  mask-MSE 0.01718
step 100  mask-MSE 0.01586
step 150  mask-MSE 0.01650
step 199  mask-MSE 0.01506
first10 mean 0.10902 -> last10 mean 0.01713 (DECREASED) in 19.7s
```

Loss decreases ~6× and gradients flow through the causal graph. That is
all this shows. It is not evidence about speech, listeners, SRT, or
benefit; the signals are synthetic, the target is an oracle mask, and no
held-out or human measurement exists. **Label: T0 smoke only.**

## Unresolved / not done here

- HP-J4-1 ratification items remain human-owned: exact filterbank pin
  (this build's mel choice is an implementation default), windowed vs
  persistent-state reading of K=5 (see note above), state-reset behaviour
  after dropout, dual-mic stratum.
- No real-speech training, no weights of record, no bench (Stage 0),
  no power figure, no on-device latency. J4 status per Gen 10 is
  unchanged by this build: `promoted FALSE`, validation set 0.
- Exact Δ=0 is bitwise at fixed batch/stream shape (see §Tests (1)).
