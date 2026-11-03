# Attack replay — Schulz/Keles checkpoint prefix/suffix future-dependence (EXECUTED)

> **Header:** Sol 6.1 requested; actual `muse-wonder-full-1.0`; **2026-11-03**.
> GOAL **v2.3**. Gen8 inputs: [Gen8-summary.md](../gen08/Gen8-summary.md),
> [attack-checkpoint-identity.md](../gen08/attack-checkpoint-identity.md)
> (serialized `causal=False`, `gLN`, kernel/stride 32/16 → **NONCAUSAL**, no execution).
> This file is the Gen8 §4 push-1 replay: **T0 quantification only**. It was
> **actually executed** as logged below (env, download, load, forward passes).
> Nothing not run is claimed. Script: [gen9_replay.py](./gen9_replay.py);
> raw stdout: [replay-output.txt](./replay-output.txt). Local logs: `/tmp/gen9logs/01–09`.
> No candidate/manifest/scoring: `promoted FALSE`, FROZEN retained, G3b BLOCKED,
> validation set 0. No SI-SDR/STOI/SRT, no listening claim, no clinical PASS.

## Verdict (executed)

**Future suffix rewrites the common past, everywhere, including sample 0.**
With a byte-identical 1.0 s prefix and only the following 1.0 s suffix changed,
the checkpoint's output inside the shared prefix changed at **every sample**
(16,000/16,000), first differing sample **0**, while the identical-input
control differed by exactly **0**. Prefix perturbation (zero vs loud-noise
suffix): relative RMS difference **0.59**, prefix SNR **4.53 dB**. In the
earliest window **0–235 ms** — more than the Gen8-recomputed 765 ms
convolutional future reach before the suffix begins — relative RMS difference
was **0.78** (2.13 dB). A causal/streaming system must give 0 in the common
past; this empirically quantifies (in a modern-version reconstruction, §2)
what Gen8 already proved from the serialized args. Identity does not depend
on this replay; the replay only prices the perturbation magnitude.

## 1. Environment — commands and observed output

Host: macOS 26.6 (25G72), arm64. Scratch only under `/tmp/gen9env` (repo env untouched).

```sh
uv python install 3.11
uv venv --python 3.11 /tmp/gen9env
VIRTUAL_ENV=/tmp/gen9env uv pip install --python /tmp/gen9env/bin/python torch asteroid numpy scipy
```

Observed (`/tmp/gen9logs/01-env.txt`, `02-pip.txt`): `Python 3.11 is already
installed`; venv `Using CPython 3.11.17 … Creating virtual environment at:
/tmp/gen9env`; install `Resolved 55 packages … Installed 55 packages`,
including `torch==2.15.0`, `asteroid==0.7.0`, `numpy==2.4.6`, `scipy==1.17.1`,
`torchaudio==2.11.1`, `pytorch-lightning==2.6.6`, `asteroid-filterbanks==0.4.0`.
Exit 0.

**Failure encountered and fixed (exact):** first
`import torch, asteroid` failed with `ModuleNotFoundError: No module named
'requests'` (asteroid 0.7.0 `utils/hub_utils.py` imports it; not pulled in).
Remedy run: `uv pip install … requests` → `requests==2.34.2` (+ certifi,
charset-normalizer, urllib3); re-import then printed `torch 2.15.0 /
asteroid 0.7.0 / numpy 2.4.6 / scipy 1.17.1` (`03-download.txt`, `04-requests-fix.txt`).

**Version caveat (material).** This is the *modern* route Gen8 §4 allowed,
**not** the checkpoint's recorded `torch 1.10.0+cu111 / asteroid 0.5.2 /
pytorch_lightning 1.4.9` (that pinned route was **not** attempted after the
modern route loaded; it is not claimed to install or fail on this host).
Therefore numbers below are the modern reconstruction's, gated by the §2
checks — not bit-identical 0.5.2 numerics.

## 2. Checkpoint re-download, hash, reconstruction checks

```sh
curl -L --fail -o /tmp/gen9_pytorch_model.bin \
  "https://huggingface.co/cankeles/ConvTasNet_WHAMR_enhsingle_16k/resolve/f47048acf872880e504bd92f4252f996d73c3024/pytorch_model.bin"
shasum -a 256 /tmp/gen9_pytorch_model.bin
```

Observed: `curl_exit:0`, 20,122,511 B,
`a96014fc1ddf9bf45bb43f2143799d9941907b8bbbbd833f69b27406d3b9026a` — **exact
match** to the HF LFS oid / Gen8 expected SHA (also re-verified inside the
replay script before loading: `sha_match=True`).

Load path (explicit, per Gen8 §4): `torch.load(..., map_location="cpu",
weights_only=False)` on the hash-verified file only — pickle deserialization
of a third-party checkpoint is code-trust; scope here was this one pinned
binary. Reconstruction: `ConvTasNet(**model_args)`, then
`load_state_dict(strict=True)`.

Observed (`05-signature.txt`, `06-construct.txt`, `07-replay.txt`):

- `model_args` from the loaded dict **exactly match Gen8 §2 table**:
  `fb_name='FreeFB', n_filters=512, kernel_size=32, stride=16,
  sample_rate=16000.0, in_chan=512, out_chan=512, bn_chan=128, hid_chan=512,
  skip_chan=128, conv_kernel_size=3, n_blocks=8, n_repeats=3, n_src=1,
  norm_type='gLN', mask_act='relu', causal=False, encoder_activation=None`.
  Constructed **as-is** (`FreeFB` accepted by asteroid 0.7.0; no remapping).
- `load_state_dict strict: <All keys matched successfully>` (345 tensors;
  first `encoder.filterbank._filters (512, 1, 32)`); 5,000,881 params.
- Smoke: zeros `(1,16000)` → output `(1,1,16000)`, RMS 0.
- Semantics in the version actually run (`09-semantics-versions.txt`):
  asteroid 0.7.0 `norms.py:_glob_norm` → `dims = arange(1, len(x.shape))`
  (channel + whole time segment); `convolutional.py` → `if not causal:
  padding = (conv_kernel_size - 1) * 2**x // 2` (symmetric), chop only if
  causal. Same semantics Gen8 inspected in 0.5.2. This is the filed
  model-args/semantics check Gen8 required before trusting modern-route numbers.

**Output-scale note.** Absolute output RMS is ~10³ for unit-scale inputs
(e.g. noise in RMS 0.01/0.1/1.0 → out RMS 37/396/5666, corr −0.71/−0.71/−0.83;
`08-scale-probe.txt`). Read as the model's arbitrary output units (Conv-TasNet
training is scale-invariant; filter RMS ≈0.31/0.39 over 512 channels) —
**inferred, not proven** against a 0.5.2 run. Consequently only *relative*
within-model metrics (relative RMS difference, output-vs-output prefix SNR)
are interpreted below; absolute RMS is reported uninterpreted.

## 3. Test design (synthetic only)

Script `gen9_replay.py` (deterministic: `np.random.default_rng(1234)`,
`torch.manual_seed(0)`, CPU, `eval()`, `no_grad`). Sample rate 16 kHz.
One **1.0 s prefix** (180/360/720 Hz harmonic complex, 4 Hz AM, + 0.05 RMS
Gaussian noise) concatenated with one of four **1.0 s suffixes**: zeros;
loud Gaussian noise (×0.6); 1 kHz tone (×0.4); natural continuation of the
prefix generator. Whole 2.0 s supplied in **one forward pass** per condition
(so `gLN` sees the full 2 s segment — chunk-length variation was **not** run).
Output differences measured **only inside the shared prefix** in windows
[0,1), [0,0.2), [0,0.5), [0.5,1), [0.9,1), [0,0.235) s. The last window ends
>765 ms before suffix onset. Control: identical input run twice.

## 4. Results (observed stdout, `07-replay.txt` / replay-output.txt)

Forward times 0.45–0.72 s per 2 s input (this CPU, 6 torch threads — offline
whole-segment time, **not** a streaming-latency measurement).
`input_prefix_identical=True`.

| Comparison (prefix window) | max abs Δ | RMS Δ | RMS ref | rel. RMS Δ | prefix SNR | samples ≠0 |
|---|---|---|---|---|---|---|
| CONTROL identical input, [0,1) s | 0 | 0 | 3421.29 | 0 | ∞ dB | 0/16000 |
| zero vs LOUD, [0,1) s | 6109.65 | 2030.11 | 3421.29 | **0.593** | **4.53 dB** | 16000/16000 |
| zero vs LOUD, [0,0.235) s | 5263.85 | 2441.64 | 3119.17 | **0.783** | **2.13 dB** | 3760/3760 |
| zero vs LOUD, [0.5,1) s | 4960.55 | 1480.16 | 3517.80 | 0.421 | 7.52 dB | 8000/8000 |
| zero vs LOUD, [0.9,1) s | 3046.24 | 972.15 | 2823.35 | 0.344 | 9.26 dB | 1600/1600 |
| zero vs TONE, [0,1) s | 1412.47 | 408.49 | 3421.29 | 0.119 | 18.46 dB | 16000/16000 |
| zero vs TONE, [0,0.235) s | 1137.39 | 353.28 | 3119.17 | 0.113 | 18.92 dB | 3760/3760 |
| continuation vs LOUD, [0,1) s | 5349.01 | 1842.66 | 3254.62 | 0.566 | 4.94 dB | 16000/16000 |
| continuation vs LOUD, [0,0.235) s | 4856.46 | 2291.36 | 2986.57 | 0.767 | 2.30 dB | 3760/3760 |

Full per-window table (all 24 rows) in [replay-output.txt](./replay-output.txt).
First nonzero output difference (zero vs loud): **sample 0 (0.0000 s)**; first
difference >1e-4 also sample 0. Every control window: RMS Δ = 0 exactly,
so the perturbation is not run-to-run nondeterminism on this setup.

Interpretation, bounded: (i) nonzero Δ anywhere in the common past refutes
causality for this reconstruction — consistent with, and redundant to, Gen8's
serialized-args proof; (ii) large Δ in [0,0.235) s, beyond the 765 ms
convolutional reach, is the signature expected from segment-wide `gLN`
(the only inspected mechanism in this architecture reaching that far) —
attribution is architectural inference on top of the empirical Δ, not a
separate ablation (no gLN-ablated variant was run); (iii) magnitudes are
suffix-dependent (loud ≫ tone), as expected for a global-stat mechanism, but
no dose-response law is claimed from three suffixes.

## 5. What was NOT run / does not follow

- No pinned 0.5.2/torch 1.10 reproduction; no cross-version numeric equality.
- No chunked/streaming-mode forwards, no chunk-length sweep (Gen8 §4's
  multi-chunk `gLN` exposure remains open; this run used one 2 s segment).
- No real speech/noise corpora, no held-out speakers, no SI-SDR/STOI/PESQ,
  no SRT or human listening, no on-processor latency/power (J3 B1/B2/B5/B7).
- No causal rebuild, no flag-flip experiment — a causal rebuild stays a new,
  unmeasured model (Gen8 §4 push 2). Nothing here prices its SRT cost.
- No change to Gen8 verdicts: checkpoint admissible only as J3 **A2 offline
  oracle/ceiling reference**; B3 cannot be met by it; Schulz 5.9 dB remains
  offline-processing external evidence (ledger-only, unscoreable). Schulz's
  actual runtime/chunking/overrides remain unreported and unsettled.

## 6. Reproduction

```sh
uv python install 3.11
uv venv --python 3.11 /tmp/gen9env
VIRTUAL_ENV=/tmp/gen9env uv pip install --python /tmp/gen9env/bin/python torch asteroid numpy scipy requests
curl -L --fail -o /tmp/gen9_pytorch_model.bin \
  "https://huggingface.co/cankeles/ConvTasNet_WHAMR_enhsingle_16k/resolve/f47048acf872880e504bd92f4252f996d73c3024/pytorch_model.bin"
shasum -a 256 /tmp/gen9_pytorch_model.bin   # expect a96014fc…3b9026a (full §2)
/tmp/gen9env/bin/python research/gen09/gen9_replay.py
# note: script expects the checkpoint at /tmp/gen9_pytorch_model.bin and asserts its SHA
```

*End. Executed T0 replay under GOAL v2.3: future dependence quantified in a
modern-version, args- and strict-load-verified reconstruction; identity was
already settled in Gen8. Scores nothing.*
