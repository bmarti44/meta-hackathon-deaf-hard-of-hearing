# Attack — external DNN checkpoint causal identity (Astra Rank 1, codex-unstick-2)

**Header:** Sol 6.1 requested; actual agent muse-wonder-full-1.0; 2026-11-03. Inspected sources only; no invented data. The checkpoint binary was downloaded and its pickle header *disassembled* (see §2); the model was **not instantiated, loaded with torch, or executed** — no inference, prefix test, or audio result is claimed.

## Verdict

**NONCAUSAL — resolved from the serialized checkpoint itself.**

The cited checkpoint `cankeles/ConvTasNet_WHAMR_enhsingle_16k` serializes `causal: False` and `norm_type: 'gLN'` in its own `model_args`. Under the Asteroid version recorded inside that same checkpoint (0.5.2), `causal=False` gives symmetric (future-looking) padding in every dilated depthwise convolution, and `gLN` normalizes over channel **and the whole supplied time segment**. Either property alone defeats a streaming/causal identity; this checkpoint has both. As serialized it is an **offline reference model**, not a causal front-end. This upgrades the codex-unstick-2 conditional finding ("if defaults, then noncausal") to a direct inspection of the actual serialized arguments — and corrects two of its inputs (kernel/stride are 32/16, not the 16/8 printed on the model card and in Schulz et al.).

Narrow residual: whether Schulz et al.'s *runtime* overrode `model_args`, chunked the input, or used a different local copy cannot be settled from the paper (no code, chunk length, or compute-software version is reported). That does not change the identity of the checkpoint they cite as used "without further modification."

## 1. Claim-by-claim evidence

| # | Claim | Inspected evidence | Status |
|---|---|---|---|
| 1 | Schulz et al. used this exact public model | Schulz et al. 2026, *Front. Audiol. Otol.* 3:1746635, DOI 10.3389/fauot.2025.1746635, §2.4: "a pre-trained open-source Conv-TasNet model was used without further modification (Keles, 2022)"; ref. 17 gives the HuggingFace URL `cankeles/ConvTasNet_WHAMR_enhsingle_16k` (accessed November 3, 2025) | Inspected (full text fetched 2026-11-03) |
| 2 | Schulz reports 1 ms latency from a 16-sample kernel/stride 8 | §2.4: encoder "512 filters with a kernel size of 16 samples … stride of 8 samples"; "Our analysis of the algorithm's impulse response confirmed 16-sample (1 ms) look-ahead, i.e. an algorithmic delay of 1 ms." Abstract/§4 repeat "ultra-low latency (1 ms)" | Inspected; contradicted by #5/#6 below |
| 3 | The Hub repo contains no separate config that could specify `causal`/`norm_type` | HF API `GET /api/models/cankeles/ConvTasNet_WHAMR_enhsingle_16k`: `config: {}`, siblings = `.gitattributes`, `README.md`, `pytorch_model.bin`; `sha f47048acf872880e504bd92f4252f996d73c3024`, `lastModified 2022-02-17` | Inspected 2026-11-03 |
| 4 | Weights file identity/size | HF tree API: `pytorch_model.bin` 20,122,511 bytes, LFS oid `a96014fc1ddf9bf45bb43f2143799d9941907b8bbbbd833f69b27406d3b9026a`; `README.md` 1,497 bytes. Downloaded copy SHA-256 = the same oid (exact match). Commits API: `pytorch_model.bin` uploaded 2022-02-15T20:02:52Z (`3cdbbe53…`); every later commit touches only `README.md`/`.gitattributes` — the binary at HEAD is the 2022 upload | Inspected; hash-verified |
| 5 | Serialized `model_args`: **`causal=False`, `norm_type='gLN'`** | Pickle-opcode disassembly of `archive/data.pkl` inside the downloaded zip (§2): at byte offsets 52799/52815 `'causal'` → `NEWFALSE`; at 52735/52754 `'norm_type'` → `'gLN'`. Full args in §2 table | **Directly inspected — decisive** |
| 6 | Serialized kernel/stride are **32/16**, not 16/8 | Same disassembly: `'kernel_size'` → `32`, `'stride'` → `16`, `'sample_rate'` → `16000.0`. Independently corroborated by the first `state_dict` tensor `encoder.filterbank._filters` with size tuple (512, 1, 32) in the same pickle | Directly inspected, dual-route |
| 7 | The model card's printed training config disagrees with its own checkpoint | `README.md` (raw, fetched) "Training config": `filterbank: kernel_size 16, stride 8; masknet: bn_chan 128, hid_chan 512, mask_act relu, n_blocks 8, n_repeats 3, skip_chan 128` and **no `causal`/`norm_type` keys at all**. Serialized args match the card on n_blocks/n_repeats/channels/mask_act but not on kernel/stride | Inspected; card is not a faithful record of the binary |
| 8 | 32/16 is inherited from the parent checkpoint | Card: "fine tuned… The initial model was taken from `JorisCos/ConvTasNet_Libri1Mix_enhsingle_16k`." Parent README (raw, fetched) config: `kernel_size 32, stride 16`, otherwise same masknet sizes; parent card likewise omits `causal`/`norm_type` | Inspected (consistent explanation, not independently proven) |
| 9 | Software versions that produced the checkpoint are serialized in it | Same pickle, `infos.software_versions`: `torch_version 1.10.0+cu111`, `pytorch_lightning_version 1.4.9`, **`asteroid_version 0.5.2`**; `dataset 'WHAM'`, `task 'enh_single'` | Directly inspected |
| 10 | In Asteroid 0.5.2, `causal=False` ⇒ symmetric future padding; `causal=True` ⇒ full left padding + chop | `asteroid/masknn/convolutional.py` @ tag `v0.5.2`, `TDConvNet.__init__`: `if not causal: padding = (conv_kernel_size - 1) * 2**x // 2` else `(conv_kernel_size - 1) * 2**x`, `dilation=2**x`; `Conv1DBlock` wraps the depthwise conv in `_Chop1d(padding)` **only** `if causal` | Inspected (raw source @ v0.5.2) |
| 11 | In Asteroid 0.5.2, `gLN` ⇒ dependence on the entire supplied segment | `asteroid/masknn/norms.py` @ `v0.5.2`: `GlobLN.forward` → `_glob_norm`, `dims = arange(1, len(x.shape))` (channel + time), `z_norm` over those dims. `norms.get('gLN')` is used in the bottleneck and twice per `Conv1DBlock` | Inspected |
| 12 | Asteroid itself forbids this combination for causal use | `asteroid/models/conv_tasnet.py` @ `v0.5.2` (= master, also fetched): defaults `norm_type="gLN"`, `causal=False`; `if causal and norm_type not in ["cgLN","cLN"]: norm_type="cLN"` with warning. The checkpoint never triggered this — it was serialized noncausal | Inspected |
| 13 | Schulz gives no compute-software version, code, or chunking for the DNN processing | Full-text search: the only software versions are "R (Version 4.3.1)… RStudio (Version 23.06.2)" for statistics (§2.6) and MATLAB (unnamed version) for test delivery (§2.3). No Python/PyTorch/Asteroid version, no checkpoint hash/revision, no segment/chunk length, no impulse-method detail beyond the §2.4 sentence | Inspected (absence in fetched full text) |

## 2. Checkpoint inspection (method and full serialized args)

Method, 2026-11-03: `curl` download of `…/resolve/main/pytorch_model.bin` to `/tmp` (19 MB on disk; 20,122,511 bytes); SHA-256 verified against the Hub LFS oid (claim #4). The file is a PyTorch zip archive (347 members: `archive/data.pkl` 53,832 bytes, `archive/version` = `3`, 345 tensor storages `archive/data/0…344`). `data.pkl` was walked with Python stdlib `pickletools.genops` (12,732 opcodes) — an opcode listing that **does not unpickle, import torch, instantiate, or run anything**. Local scratch: `/tmp/inspect_cankeles.py`, `/tmp/inspect2.py`, `/tmp/inspect3.py`, outputs `/tmp/cankeles_ops2.txt`; checkpoint copy `/tmp/cankeles_pytorch_model.bin`.

Top-level serialized dict keys, in order: `model_name='ConvTasNet'`, `state_dict` (OrderedDict), `model_args`, `infos`. This is Asteroid's `serialize()` format (`from_pretrained` requires `model_args` + `state_dict`), so `model_args` below is exactly what `BaseModel.from_pretrained("cankeles/ConvTasNet_WHAMR_enhsingle_16k")` would reconstruct the network from.

| `model_args` key | Serialized value (pickle offset) |
|---|---|
| `fb_name` | `'FreeFB'` (52421) |
| `n_filters` | 512 |
| `kernel_size` | **32** (52476) |
| `stride` | **16** (52499) |
| `sample_rate` | 16000.0 |
| `in_chan` / `out_chan` | 512 / 512 |
| `bn_chan` / `hid_chan` / `skip_chan` | 128 / 512 / 128 |
| `conv_kernel_size` | 3 |
| `n_blocks` / `n_repeats` / `n_src` | 8 / 3 / 1 |
| `norm_type` | **`'gLN'`** (52735) |
| `mask_act` | `'relu'` |
| `causal` | **`False`** (`NEWFALSE` at 52815) |
| `encoder_activation` | `None` |

## 3. Derived future-context (recomputed from serialized values, not card values)

With `conv_kernel_size=3` and noncausal padding `2^x` per block (claim #10), each depthwise convolution reaches `dilation = 2^x` latent frames into the future. Rightward reach summed over one repeat: `1+2+…+128 = 255` latent frames; × 3 repeats = **765 latent frames**. At the serialized stride of 16 samples/frame and 16 kHz that is 12,240 samples = **765 ms of convolutional future context** from the masker alone — before encoder (32-sample window) and decoder support. This *supersedes* the 382.5 ms figure in codex-unstick-2, which used the card's stride 8; the true serialized stride doubles it.

Independently, `gLN` (claims #5, #11) makes every normalized activation a function of the **entire time segment supplied in that forward pass**, so with whole-sentence offline processing the dependence is segment-wide, not bounded by 765 ms at all. The convolutional number is therefore a floor for a hypothetical gLN-free rebuild with these weights' geometry, not a bound on the checkpoint as-is.

Consequence for the Schulz latency claim: a 16-sample (1 ms) impulse look-ahead is not reconcilable with the cited checkpoint's serialized identity — not only because impulse onset cannot prove causality for a globally-normalized nonlinear masker (codex-unstick-2 counterexample), but because the checkpoint's own kernel is 32 samples and its stride (latent hop) is 16 samples. The paper's "16 samples" matches neither the kernel (32) nor any full-network quantity; it coincides with the card's erroneous kernel entry, and numerically with the true stride. On inspected evidence, Schulz (and the card) describe a different configuration from the binary both point to.

## 4. What this does and does not settle

Settled:
- The named checkpoint is **noncausal as serialized** (`causal=False`, `gLN`), under its own recorded Asteroid 0.5.2 semantics. J3 criterion B3 (verified full-network causal implementation) **cannot** be met by this checkpoint; it can serve only as an offline reference. Flipping the flag is not a repair: the weights were trained with symmetric context and global normalization, so a causal rebuild is a new model whose listening benefit is unmeasured.
- The Schulz et al. 5.9 dB adult CI benefit, if produced by this checkpoint used "without further modification" as stated, is an **offline-processing** benefit, and their 1 ms algorithmic-delay claim does not describe the cited binary. The result remains real external evidence of offline DNN efficacy; it is not evidence that a ≤1 ms (or any streaming) implementation preserves it.

Not settled / not done here:
- No execution: no `torch.load`, instantiation, forward pass, prefix/suffix test, or audio metric was run in this attack. The empirical prefix test is still worth running to *quantify* common-prefix perturbation, but it is no longer needed to decide the causal identity — the serialized args decide it.
- Schulz's actual runtime (library versions, chunk length fed to `gLN`, any kwargs override of `model_args`) is unreported in the paper and unresolved; an override would contradict their "without further modification" statement and is not evidenced.
- A causal retrain's SRT cost, on-processor latency/power (B1/B2/B5/B7), and any project scoring cell are untouched by this file. No PASS is implied anywhere.
