# Causal / low-latency DNN speech enhancement with CI listeners — search

**Header:** Sol 6.1 requested; actual agent `muse-wonder-full-1.0`;
2026-11-03. GOAL v2.3. Inspected sources only (PubMed abstracts
via NCBI E-utilities, PMC/Europe PMC full texts, arXiv HTML,
Hugging Face API/cards/configs); no invented data. Context:
Gen 8 proved the Schulz/Keles checkpoint NONCAUSAL as serialized
(`causal=False`, `gLN`, 765 ms masker future context —
[Gen8-summary.md](../gen08/Gen8-summary.md),
[attack-checkpoint-identity.md](../gen08/attack-checkpoint-identity.md)).
Question: does any *genuinely causal* model have human CI data?

## Verdict

**YES — but only from one lineage, and not ConvTasNet-class.**
Two frame-causal models (no future frames, by inspected
architecture) have human CI **SRT** (adaptive SNR-50) data:
Goehring et al. 2017 NNSE (N=14 CI) and Goehring et al. 2019
RNN-LSTM (N=10 CI). A third, Gaultier & Goehring 2024, has
human CI SRT data for *low-latency bounded-lookahead* models
(~15 ms / 4 ms future), which are not strictly causal.
**No causal ConvTasNet variant, DeepFilterNet, DPCRN, or CRN
was found with any human CI listener evaluation** — those
lineages are objective-metric only (or HI/NH listeners).
All causal CI SRT effects below are vs **unprocessed**, in
adults, under noise-specific or two-noise training — none is
vs a current commercial front-end.

Definitions used: *strict/frame-causal* = output for frame/step
uses current+past input only (bounded algorithmic delay from
the analysis window is reported separately); *low-latency
noncausal* = explicit future context with a small stated bound;
*noncausal* = bidirectional/transformer/global-norm/full-segment.

## Ranked table (causality evidence × human CI evidence)

| Rank | Model / study | Causality evidence (inspected) | CI listeners | Effect vs comparator |
|---|---|---|---|---|
| 1 | **NNSE** — Goehring et al. 2017, *Hear Res* 344:183-194, PMID 27913315, PMC5256482 | **Strict frame-causal.** Feed-forward NN estimates Wiener gain from feature vector `[F_n, F_{n-1}]` only: "using information related to the current and past frames only"; "using only the past and the current frames". Stated algorithmic delay **10 ms**; ACE front end 8-ms FFT blocks, 7-ms overlap. Full text explicitly contrasts itself with Healy/Chen future-frame (>20 ms) designs | **N=14 CI users**, adaptive SRT, 3 noises (SWN, ICRA, 20-talker babble), blinded | SRT improvement vs unprocessed (ACE): speaker-independent NNSE-MT **1.4 dB (SWN), 5.4 dB (ICRA), 0.4 dB NS (babble)**; speaker-dependent NNSE-ST **2.3 / 6.4 / 2.0 dB**. Noise-specific networks (trained per noise type) — key generalisation limit |
| 2 | **RNN-LSTM ERM** — Goehring, Keshavarzi, Carlyon & Moore 2019, *JASA* 146:705-718, PMID 31370586, PMC6773603 | **Strict frame-causal.** 2 hidden LSTM layers (128 units) + FC sigmoid output; "steps 1-5 corresponded to successive frames j-4, j-3, j-2, j-1, j" to estimate the ratio mask for frame j — no `j+1` input anywhere in inspected methods. 20-ms frames / 10-ms hop at 16 kHz; no separate ms algorithmic-delay figure stated in inspected text | **N=10 CI users** (Exp. 2) + N=10 NH with CI simulations (Exp. 1, not counted here), adaptive SRT in babble + traffic | SRT improvement vs unprocessed: **+3.4 dB babble (significant; all 10 CI better), +2.0 dB traffic (NS; 4/10 worse)**. Trained many-talker, tested unseen talker, same noise classes |
| 3 | **DP-RNN TasNet (1 mic) / FaSNet-TAC (2, 6 mics)** — Gaultier & Goehring 2024, *JASA* 155:3833-3847, PMID 38884525; OSF preprint full text inspected | **Low-latency, NOT strict-causal.** 1M: dual-path RNN TasNet modified to unidirectional global RNN + channel-wise norm "to align … with causal processing requirements", stated minimal latency **~15 ms** (chunk structure retained). 2M/6M FaSNet: explicitly "only requires **4 ms of future information**" (1-ms frame, 6-ms contextual window) | **N=12 CI listeners** (+15 NH CI-simulation), adaptive SRT, noisy-reverberant | SRT improvement vs noisy-reverberant unprocessed (CI group): **2.3 dB (1M), 7.4 dB abstract / 7.6 dB discussion (multi-mic), 10.3 dB (6-mic)** — abstract/discussion discrepancy noted, not resolved. Ideal-mask reference +24.8 dB. Multi-mic gains need mic configurations beyond a standard single processor |
| 4 | **Deep ACE / Fused Deep ACE** — Gajecki et al. 2023, *IEEE TBME* 70:2700-2709, PMID 37030808 (N=8 CI); Gajecki & Nogueira 2024, PMID 38376983 + arXiv:2310.01122v1 (N=5 BiCI) | **UNVERIFIED — do not rank as causal.** Abstracts claim denoised electrodograms "without sacrificing processing latency" / "same 2 ms latency as ACE", but inspected arXiv full text gives only ConvTasNet-style separator hyperparameters (F=64, L=32, P=3, X=8, R=3) with **no causal flag, padding, or norm type**; the 2 ms figure equals the L=32-sample encoder length at 16 kHz — the same encoder-window ≠ full-receptive-field error Gen 8 documented for Schulz. Until code/config shows causal padding + cumulative norm, causality is unproven | N=8 CI (2023); N=5 bilateral CI (fused) | **Fixed-SNR word scores, not SRT.** 2023: "highest speech intelligibility scores" (no extractable effect in inspected abstract). Fused v1: HSM word-recognition at subject-specific fixed SNRs vs bilateral ACE without NR (Gen 8 ledger: qualitative; up to 22.8% WRS cited in its intro for prior work) |
| 5 | **LSTM front-end, biased loss** — Kang, Zheng & Meng 2021, *Front Med* 8:740123, PMID 34820392 | **UNVERIFIED.** Inspected abstract/full-text snippets: "A long-short term memory (LSTM) network was trained to estimate T-F masking gains"; directionality (uni- vs bi-), frame context, and latency not stated in inspected passages | CI recipients (subjective experiments incl. SRT-in-noise tests; **N and effect magnitude absent from inspected abstract**) | Abstract qualitative only: SRT tests show intelligibility "significantly improved" with noise-suppression-biased loss vs balanced loss. Not extractable as a causal-SRT datum without full-text architecture + N extraction |
| 6 | **CNN (Wiener-/SS-/vanilla), causal variants** — Mamun, Khorram & Hansen 2019, Interspeech, PMID 34307643, PMC8296973 | **Causal variants exist by design** (causal convolutions replacing past+future CNN; "causal Wiener-CNN outperforms other networks" on envelope-correlation metric) | **N=0 human.** Objective ECM only, in CI filter-bank feature space | No listener effect. Proof that a causal CI-targeted CNN was built and objectively benchmarked — and never, in inspected record, taken to CI listeners |
| 7 | **Effectively-causal GCRN** — Healy et al. 2021, *JASA* 149:3943, PMID 34241481 (+ 2021 causal-conversion-cost companion, PMC8612765) | "Effectively causal": gated convolutional recurrent network, complex spectral mapping, future-frame use only within stated speech-perception delay tolerance (authors' framing, abstract) | **Hearing-impaired listeners — not CI** | Significant intelligibility benefit in untrained noises (HI). Included as the nearest causal-with-listeners evidence *outside* CI; its own introduction cites Goehring 2017 as the CI causal precedent |
| 8 | **RNN (BiLSTM) + SepFormer** — Borjigin et al. 2024, *Sci Rep* 14:13241, PMID 38853168, PMC11163011 | **Explicitly NONCAUSAL** (full text ×3): "both RNN (bi-directional LSTM) and SepFormer used non-causal processing with access to future frames"; causal conversion named as future work. SepFormer processing ≈5× real time on CPU | N=13 CI listeners | Fixed-SNR word scores vs unprocessed (Gen 8 ledger: +11.94 pp RNN, +20.91 pp SepFormer at 5 dB CCITT) — **not SRT, not causal** |
| 9 | **DCCTN** — Mamun & Hansen 2024, *IEEE/ACM TASLP* 32:2616-2629, PMID 39831177 | **NONCAUSAL by construction** (abstract): complex U-Net with transformer bottleneck over the T-F spectrogram + frequency-transformation block; no causal/streaming claim. Compared objectively vs CRN/DCCRN/GCRN | N=4 CI recipients (formal listener evaluation) | "Significant improvement in speech intelligibility" (abstract; no SRT dB in inspected abstract). Human CI data, wrong causality class |
| 10 | **ConvTasNet (Schulz/Keles checkpoint)** — Schulz et al. 2026, DOI 10.3389/fauot.2025.1746635 | **Proven NONCAUSAL** (Gen 8 direct pickle inspection: `causal=False`, `gLN`, kernel/stride 32/16, 765 ms future context) despite "1 ms ultra-low latency" claim | N=12 CI enrolled, 10 complete pairs | Offline SRT benefit 5.9 dB vs unprocessed (Gen 8 ledger). External offline evidence only; excluded from causal ranking |
| 11 | **Causal ConvTasNet lineage** — Luo & Mesgarani 2019 causal config (cLN replaces gLN); "On TasNet for Low-Latency…" arXiv:2103.14882 (3 configs: noncausal+gLN / noncausal+cLN / **causal+cLN**); Bokaei et al. causal ConvTasNet "latency of 3 ms" | Genuinely causal configurations are well-defined in inspected abstracts/full-text snippets (causal convs + cumulative LN) | **N=0 CI listeners in every inspected record** — objective metrics (SI-SDR/STOI-class) on speech corpora only | No human CI effect exists to report. This is the direct answer for "causal ConvTasNet with CI listeners": **none found** |
| 12 | **DeepFilterNet / DPCRN / CRN (HF + arXiv)** — HF `fal/DeepFilterNet3` card+`config.ini` inspected; DeepFilterNet repo README; PubMed `(DeepFilterNet OR DPCRN OR "convolutional recurrent") AND (cochlear OR hearing)` | DeepFilterNet3 config: `conv_lookahead=2`, `df_lookahead=2`, FFT 960 / hop 480 @48 kHz (20/10 ms) → **bounded-lookahead low-latency, not strict-causal**. HF card itself carries license only — no listener evaluation. CRN appears in CI literature only as an *objective baseline* inside DCCTN (rank 9) | **N=0 CI listeners found** for DeepFilterNet, DPCRN, or CRN as the evaluated intervention | No human CI effect exists to report |

## Notes on the two strict-causal positives

- Both are **mask/gain-estimation in an auditory filterbank**,
  not waveform TasNet-style models. Their causality is cheap
  to achieve precisely because the architecture is a per-frame
  gain regression / 5-step LSTM — there is no dilated-TCN
  receptive field to audit. A causal-ConvTasNet retrain (Gen 8
  push 2) would be a *third*, currently unmeasured, causal
  lineage; ranks 1-2 do not predict its SRT cost.
- Comparators are unprocessed/ACE-without-NR throughout.
  Neither study supports a claim vs a current commercial
  front-end, a pediatric claim, or a quiet non-inferiority
  claim. Noise-specific training (2017) and two noise classes
  (2019, traffic NS) bound generalisation.
- Gaultier 2024 (rank 3) is the strongest *magnitude* with CI
  SRT (up to 10.3 dB) but its multi-mic conditions are
  4-ms-future systems requiring 2-6 microphones; only the
  1-mic ~15 ms condition (2.3 dB, CI group only) is near a
  conventional processor form factor.

## Search record (2026-11-03, inspected)

- PubMed E-utilities: `Goehring cochlear implant neural network
  speech enhancement`; `causal speech enhancement cochlear
  implant`; `cochlear implant deep learning speech enhancement
  listeners`; `(cochlear implant) AND (causal OR real-time OR
  low-latency) AND (neural OR deep learning)`;
  `(DeepFilterNet OR DPCRN OR "convolutional recurrent") AND
  (cochlear OR hearing)`; targeted fetches for PMIDs 27913315,
  31370586, 38884525, 34307643, 37030808, 38376983, 38853168,
  39831177, 34820392, 34241481.
- Full texts inspected for causality language: PMC5256482
  (Goehring 2017), PMC6773603 (Goehring 2019), PMC11163011
  (Borjigin 2024), PMC8296973 (Mamun 2019), OSF preprint of
  Gaultier & Goehring 2024 (publisher PDF via OpenAlex OA
  record), arXiv:2310.01122v1 HTML (Fused Deep ACE).
- HF/arXiv: HF API model search `ConvTasNet` (20 repos incl.
  `cankeles/…`, `JorisCos/…` — none inspected carries a causal
  config or CI evaluation), `DeepFilterNet` (`fal/DeepFilterNet3`
  `config.ini` read in full), `DPCRN` (no HF models returned),
  arXiv API `Deep ACE` (no record), arXiv:2103.14882 and
  Luo & Mesgarani causal-cLN descriptions.
- Simulation-only studies (NH vocoder, e.g. FCN/EAS PMID
  33275585) were excluded from the ranking per brief, as were
  HI-only listener studies except rank 7 as a labelled
  boundary case.

## Unresolved (named, not settled)

- Deep ACE / Fused Deep ACE (rank 4): separator padding/norm
  in the *journal* versions and any released code were not
  inspected (IEEE full text not retrieved); causality stays
  UNVERIFIED, neither proven causal nor proven noncausal.
- Kang 2021 (rank 5): LSTM directionality/context, CI N, and
  SRT magnitudes need full-text extraction (PMC8606413)
  before any ranking change.
- Goehring 2019: end-to-end algorithmic delay in ms (frame +
  overlap-add) not numerically stated in inspected text;
  frame-causality (j-4…j) is stated.
- Gaultier 2024: 7.4 (abstract) vs 7.6 dB (discussion) for the
  same multi-mic condition; intra-chunk directionality of the
  DP-RNN not fully specified in inspected preprint passages.
- No search can prove a universal negative: "no causal
  ConvTasNet/DeepFilterNet/DPCRN/CRN with CI listeners" means
  none surfaced in the PubMed/HF/arXiv records inspected
  above on 2026-11-03.

*End. Scores nothing; external evidence only. No candidate,
manifest, or cell is changed by this file.*
