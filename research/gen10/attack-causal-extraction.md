# Attack — full causal extraction: Goehring 2017/2019, Kang 2021, Gaultier 2024, Deep ACE

**Header:** Sol 6.1 requested; actual agent `muse-wonder-full-1.0`;
2026-11-03. Gen 10. GOAL **v2.3** (no generation cap, no loop stop).
**Inspected only** — PMC efetch XML (`db=pmc`, `rettype=full`) for
PMC5256482 / PMC6773603 / PMC8606413 (fetched 2026-11-03, 138–154 kB
XML each); Gaultier 2024 has **no PMC record** (eSearch `38884525[UID]`
in `db=pmc` → count 0), so the inspected body is the OSF preprint PDF
(doi:10.31234/osf.io/5e2mu, dated 20 Dec 2023, 15 pp., the version
Gen 9 also used) cross-checked against the PubMed/Europe PMC abstract
(JASA 155:3833–3847, doi:10.1121/10.0026218); Deep ACE from
arXiv:2310.01122v1 full text (ar5iv render) + the author's code repo
`github.com/tomgajecki/DeepACE` @ main (2025-05-26). Prior:
[Gen9-summary.md](../gen09/Gen9-summary.md),
[causal-dnn-search.md](../gen09/causal-dnn-search.md).
**Authority:** agent extraction = triage only. Human dual
extraction/GRADE PENDING. Scores nothing; `promoted FALSE`,
FROZEN retained, G3b BLOCKED, validation set 0.

> **Headline.** Gen 9's four desk-closures are now closed at full
> text. Goehring 2017 + 2019 causality is **proven from methods
> text** (frame indices quoted below). Kang 2021 resolves to
> **N=7 CI for SRT** (not the N=19 headline) with causality
> **UNVERIFIED** (LSTM directionality never stated) and only
> "about"-grade SRT magnitudes. Gaultier 2024's 1-mic model is
> **bounded-lookahead, not causal** — its own Fig. 1 labels the
> intra-chunk path **Bi-LSTM**; the 7.4-vs-7.6 dB discrepancy
> resolves to **7.6 dB** from the reported group means. Deep ACE
> stays **UNVERIFIED for the evaluated model**: the paper never
> states padding/norm, and the released code is causal-*capable*
> (flag-gated) but ships no paper checkpoint/config and its
> encoder is symmetrically padded even in causal mode.
> **No study below reports a confidence interval for any SRT
> difference** — every CI in this file is agent-derived from a
> reported paired *t* and labelled as such.

## 0. Latency conventions (used throughout)

- *Frame-causal*: output for frame *j* is a function of input
  frames ≤ *j* only. The analysis window itself still imposes an
  algorithmic delay ≈ one hop (streaming, output emitted at frame
  end) to one window length (block-aligned).
- Derived figures show their arithmetic and are marked
  **[derived]**; figures quoted from the paper are **[stated]**.

## 1. Goehring et al. 2017 — NNSE (PMC5256482) — CAUSAL, proven

*Hear Res* 344:183–194. PMID 27913315.

| Item | Extracted (inspected) |
|---|---|
| N / design | **N=14 CI users** (native Dutch, Cochlear Nucleus, mean age 61 y, range 23–81; one ear tested; mean implant use 9.8 y). Repeated-measures, each subject own control; **subject + audiologist blind** to processing condition; 9 conditions = 3 maskers (SWN, ICRA, 20-talker BABBLE) × 3 processing (UN, NNSE-ST speaker-dependent, NNSE-MT speaker-independent), each tested **3×, counterbalanced**; final SRT = mean of 3 |
| SRT procedure | Adaptive 1-down/1-up, speech fixed 65 dB SPL, noise adjusted in 2 dB steps, 10-sentence lists, SRT = mean of last 6 SNRs incl. hypothetical 11th; all-keywords-correct scoring |
| Comparator | **Unprocessed research ACE (UN)** on NIC3/L34 — no commercial front-end, no NR comparator |
| Causality proof | Feature vector is `[F_n, F_{n-1}]` (140-dim): *"the NN estimated the Wiener gain using information related to the current and past frames only"*; *"satisfies this requirement by using only the past and the current frames"*; explicitly contrasted with Healy/Chen *"non-causal information (future frames)… (>20 ms)"*. No `n+1` input exists in the inspected methods. **Strictly frame-causal.** |
| Latency | **[stated] algorithmic delay 10 ms.** Structure check **[derived]**: NNSE analysis = 20 ms segments, 50% overlap → hop = 20 × 0.5 = **10 ms** = the stated delay. ACE path: 8 ms FFT blocks, 7 ms overlap → hop 1 ms; gain smoothed with 12 ms exponential time constant before application to ACE envelopes (a lag, not lookahead). No on-processor measured latency (MATLAB/NIC3 bench delivery) |
| Baseline SRT (UN) | SWN **2.8 dB**, ICRA **5.1 dB**, BABBLE **6.7 dB** (group means) |

**Exact SRT effects vs UN** (two-way RM-ANOVA processing
F(2,26)=31.83, p<0.001; interaction F(4,54)=13.73, p<0.001;
Bonferroni post-hocs):

| Noise | NNSE-MT (speaker-indep.) | NNSE-ST (speaker-dep.) | Omnibus |
|---|---|---|---|
| SWN | **+1.4 dB**, p=0.019 | **+2.3 dB**, p=0.003 | F(2,12)=8.165, p=0.006 |
| ICRA | **+5.4 dB**, p<0.001 | **+6.4 dB**, p<0.001 | F(2,12)=28.13, p<0.001 |
| BABBLE | **+0.4 dB, NS** (no p printed for MT-vs-UN; "significant improvement… only for NNSE-ST") | **+2.0 dB**, p<0.001 (MT-vs-ST p=0.035) | F(1.364,32.727)=7.45, p=0.009 (GG-corrected) |

Individuals: SWN 11/14 (MT) and 13/14 (ST) improved; ICRA 13/14
both (some >10 dB); BABBLE MT only 8/14 improved (1.5–3 dB), rest
same/worse. **CIs: NOT REPORTED** — figures show SEM bars only;
no paired *t*/SD-of-difference in text, so no CI is derivable
without digitising Fig. 4/5 (not done; would not be extraction).
Limits: **noise-specific networks** (one net per noise type,
tested on novel segments of the same type); unseen-noise
generalisation explicitly not assessed in listeners.

## 2. Goehring, Keshavarzi, Carlyon & Moore 2019 — RNN-LSTM ERM (PMC6773603) — CAUSAL, proven

*JASA* 146:705–718. PMID 31370586.

| Item | Extracted (inspected) |
|---|---|
| N / design | Exp. 2 (counted): **N=10 CI users** (post-/peri-lingually deafened, 6 female, mean 65 y, 49–74; unilateral AB HiRes 90K, ≥3 y experience, mean 5.5 y). Exp. 1 (not counted): N=10 NH, SPIRAL vocoder. Within-subject: 3 processing (UN, PR=RNN, IRM ideal mask) × 2 noises (20-talker babble, traffic), **3 runs/condition, block order counterbalanced, run order randomised**; stimuli via clinical AB Harmony processor, AUX input, mic disabled, adaptive preprocessing off |
| SRT procedure | 1-up/1-down adaptive, 2 dB steps, start −4 dB, all-3-keywords scoring; SRT = mean SNR of last 10 sentences (Exp. 1 wording; Exp. 2 "similar") |
| Comparator | **Unprocessed (UN)** speech-in-noise through the same clinical map; IRM = oracle upper bound, not a comparator product |
| Causality proof | *"steps 1, 2, 3, 4, and 5 corresponded to successive frames j-4, j-3, j-2, j-1, and j… The RNN estimated the IRM for frame j"* (2 hidden LSTM layers ×128 + FC sigmoid). No `j+1` term anywhere in inspected methods; intro: *"Other studies have used causal signal processing without future frames…"* citing this lineage. Feature normalisation uses **training-set** mean/SD (fixed constants at test time — no test-segment leakage). **Strictly frame-causal.** Caveat: stimuli were **re-synthesised offline** (mask × noisy phase, overlap-add) for presentation; causality is a property of the *algorithm as specified*, not of a streaming run — the paper itself notes processor integration would avoid re-synthesis |
| Latency | **[stated] none in ms** (only the generic "below about 10–20 ms" requirement). **[derived]** from stated params: 20 ms frames @16 kHz (320 samples), 10 ms overlap → hop = 20 − 10 = **10 ms**; mask for frame *j* available only after frame *j* is fully observed, so streaming algorithmic latency = **10 ms (hop-aligned) to 20 ms (window-aligned)** depending on OLA alignment — the paper does not pin the convention. Past context span = 4 hops × 10 ms + 20 ms window = **60 ms of history, 0 ms of future** |
| Baseline SRT (UN) | Babble **7.9 dB**, traffic **2.8 dB**; PR babble 4.5 dB (= 7.9 − 3.4 ✓); IRM −8.0 / −8.6 dB (floor −10 dB reached by all subjects ≥once) |

**Exact SRT effects vs UN** (3-condition RM-ANOVA processing
F(2,18)=273.2, p<0.001, UN-vs-PR p=0.006; focused UN-vs-PR
RM-ANOVA F(1,9)=72.5, p=0.002, interaction NS p=0.144):

| Noise | Effect (PR − UN) | Reported test | 95% CI **[derived by agent from reported paired t: SE = Δ/t, Δ ± t₀.₉₇₅,₉·SE]** |
|---|---|---|---|
| Babble | **+3.4 dB** (10/10 better) | t(9)=7.2, p<0.001 | SE 0.47 → **[+2.3, +4.5] dB** |
| Traffic | **+2.0 dB, NS** (6/10 better, worst −1.2 dB) | t(9)=1.9, p=0.077 | SE 1.05 → **[−0.4, +4.4] dB** (includes 0 ✓) |

Paper-reported CIs: **none** (box plots only). Training: many
talkers (VCTK), tested on novel talker + novel noise recordings
of the **same two classes**, single training SNR (5 dB).

## 3. Kang, Zheng & Meng 2021 — LSTM + weighting loss (PMC8606413) — causality UNVERIFIED

*Front Med* 8:740123. PMID 34820392. **Gen 9's "N unextracted"
resolves — and the SRT N is 7, not 19.**

| Item | Extracted (inspected) |
|---|---|
| N / design | **19 CI recipients recruited in total** (all unilateral Cochlear CI24M, Mandarin; built-in NR switched off), split across **two disjoint sub-tests**: **SRT test N=7 (C1–C7)**; fixed-SNR speech-recognition (WRR) test N=12 (C8–C19). Plus N=10 NH vocoder-simulation SRT (not CI data). CI SRT test: within-subject, 10 blocks = 5 front-ends (Noisy, WF, MSE-MASK, WL-MASK α=0.3, α=0.4) × 2 noises (SSN, babble); MHINT-M 20-utterance lists; loudspeaker presentation ~65 dB SPL; adaptive 1-down/1-up (init 12 dB, 4 dB → 2 dB steps, SRT = mean of last 6 reversals); each sentence replayable up to 3× on request |
| Comparator | **Noisy = unprocessed** (primary); also Wiener-filter (WF) and MSE-loss LSTM (MSE-MASK) — the only study in this file with a non-DL algorithm comparator, still not a commercial front-end |
| Causality proof | **NONE FOUND.** Full text says only: *"A long-short term memory (LSTM) network was trained to estimate the T-F masking gains"*; architecture = input layer 256 LSTM units + 2 FC layers (512) + 256-unit sigmoid output. The words causal / unidirectional / bidirectional / future / past-frame context **do not appear** in the inspected full text; no statement of whether the gain for frame *t* sees frames > *t* (offline whole-utterance LSTM evaluation is not excluded). Verdict: **UNVERIFIED** — a plain uni-LSTM *would* be frame-causal, but that is an assumption about an unstated implementation, not evidence |
| Latency | **[stated] none** (no ms delay figure anywhere). **[derived]** from stated STFT only: Hanning window **32 ms**, shift **16 ms**, 512-pt FFT @16 kHz (512/16000 = 32 ms ✓) → *if* run frame-causally, algorithmic latency = **16 ms (hop-aligned) to 32 ms (window-aligned)**, before any ISTFT/OLA cost. This already sits at/above the 10–20 ms hearing-device envelope the Goehring papers cite — and the paper's own conclusion flags real-time implementation as an unsolved drawback ("real-time noise estimation is required… might restrict implementation") |

**SRT effects (N=7 CI)** — the paper prints **no numeric SRT
table**; magnitudes exist only as Figure 8 + these discussion
sentences: WL-MASK vs Noisy *"about 6 dB in SSN and about 2.2 dB
in Babble"*; WL-MASK vs MSE-MASK *"about 3.3 dB in SSN and about
1.2 dB in Babble"* (α not pinned per figure in that sentence).
Two-way RM-ANOVA: SE-method F(1.825,10.97)=19.69, p<0.001;
noise F(1,6)=43.6, p<0.001; interaction F(1.56,9.361)=7.152,
p=0.02. Tukey: SSN — WL α=0.3/0.4 vs Noisy both p<0.0021, vs WF
≥p<0.0332, vs MSE-MASK significant at α=0.3 (p<0.0332) only;
Babble — WL α=0.3 vs Noisy p<0.0332 and vs MSE-MASK p<0.0021;
α=0.4 vs Noisy p<0.0332, vs WF/MSE-MASK NS.
**CIs: NOT REPORTED and not derivable** (no paired *t*, no SD of
differences; figure error bars are SDs of WL conditions only).
Grade this datum **figure/"about"-grade, N=7** — it cannot enter
any ledger as an exact effect without human figure extraction.
(NH vocoder arm, for the record: WL vs Noisy ≈8.6 dB SSN /
≈6.3 dB babble — simulation only, not CI evidence. N=12 WRR arm:
WL vs Noisy NS everywhere except 0 dB SSN, α=0.3/0.5 p=0.007/0.004.)

## 4. Gaultier & Goehring 2024 — DP-RNN TasNet / FaSNet-TAC — LOW-LATENCY NONCAUSAL (both paths)

*JASA* 155:3833–3847. PMID 38884525. **No PMC full text exists**
(efetch/eSearch verified 2026-11-03); inspected body = OSF
preprint doi:10.31234/osf.io/5e2mu (20 Dec 2023). Any
publisher-version wording difference is UNVERIFIED.

| Item | Extracted (inspected) |
|---|---|
| N / design | Exp. 2 (counted): **N=12 CI listeners** (7 female, mean 67.5 y, 51–79; unilateral AB, ≥1.5 y experience). Exp. 1: N=15 NH + SPIRAL vocoder. Within-subject, **double-blind**, 5 conditions (UN, 1M, 2M, 6M, IRM), order randomised then repeated in reverse (2 lists/condition, averaged); clinical AB Harmony via AUX, mic off, adaptive preprocessing disabled. Noisy-**reverberant** multi-talker babble, fully mismatched train/test |
| SRT procedure | 1-up/1-down, 15-sentence BKB lists, start 0 dB SNR, 2 dB steps, all-3-keywords; SRT = mean SNR of last 10 sentences |
| Comparator | **Noisy-reverberant unprocessed (UN)**; IRM oracle upper bound |
| Causality — 1M (DP-RNN TasNet) | **NOT strict-causal.** Text: global (inter-chunk) RNN switched to *"unidirectional mode"* + channel-wise norm (cLN, *"only uses inputs at the current time step"*). But **Fig. 1 labels the local (intra-chunk) path "Bi-LSTM"** — bidirectional *within* each chunk, so every output in a chunk can depend on later samples in that chunk. Authors' own wording is only *"align … more closely with the causal processing requirements"*. Class: **bounded-lookahead = one chunk** |
| Latency — 1M | **[stated] "minimal latency of about 15 ms"**; params: window 2 samples, chunk size 250 (encoder frames). **[derived]** consistency: encoder stride = window/2 = 1 sample → at 16 kHz one encoder frame = 1/16000 s = 0.0625 ms; 250 frames × 0.0625 ms = **15.6 ms ≈ the stated ~15 ms** ✓ (sampling rate itself is never printed in the preprint — 16 kHz is inferred from this identity plus lineage convention; mark fs INFERRED). The lookahead for the *first* sample of a chunk is the full chunk (Bi-LSTM), decaying to ~0 at chunk end |
| Causality/latency — 2M/6M (FaSNet-TAC) | **Explicitly noncausal, bounded:** symmetric contextual window *"encompassing past and future samples centered around the current frame"*, shrunk to 1 ms frame / 6 ms context → **[stated] "only requires 4 ms of future information"**. Arithmetic note **[derived]**: a symmetric 6 ms window around a 1 ms frame implies (6−1)/2 = 2.5 ms future, not 4 ms — the paper's 4 ms presumably counts the full post-frame context under its framing offset; the discrepancy is in the *paper's* bookkeeping, quoted here unresolved. Fig. 2 likewise shows a Bi-LSTM intra-chunk path |

**Exact SRT effects, CI group (N=12)** — group mean SRTs printed
in text: **[UN 10.5, 1M 8.2, 2M 2.9, 6M 0.2, IRM −14.3] dB**;
RM-ANOVA F(4,44)=245.6, p<0.001; Holm-Bonferroni post-hocs:

| Condition | Δ vs UN from printed means | Reported test (d = Cohen's d) | 95% CI **[derived: SE = Δ/t, Δ ± t₀.₉₇₅,₁₁·SE]** |
|---|---|---|---|
| 1M | 10.5 − 8.2 = **+2.3 dB** | t(11)=−2.693, d=−0.79, p=0.021 | SE 0.85 → **[+0.4, +4.2] dB** |
| 2M | 10.5 − 2.9 = **+7.6 dB** | t(11)=−7.936, d=−1.93, p<0.001 | SE 0.96 → **[+5.5, +9.7] dB** |
| 6M | 10.5 − 0.2 = **+10.3 dB** | t(11)=−11.519, d=−3.11, p<0.001 | SE 0.89 → **[+8.3, +12.3] dB** |
| IRM | **+24.8 dB** | t(11)=−42.317, d=−7.1, p<0.001 | SE 0.59 → **[+23.5, +26.1] dB** |

**7.4-vs-7.6 discrepancy RESOLVED:** abstract says "7.4 and
10.3 dB" for the multi-mic algorithms; discussion says "2.3 dB,
**7.6 dB** and 10.3 dB". The printed CI group means give
10.5 − 2.9 = **7.6 dB exactly** → the discussion figure is the
one consistent with the paper's own means; the abstract's 7.4 dB
is inconsistent with them (no second 2M mean pair in the text
reproduces 7.4). Individuals: 1M 9/12 better (range −0.8…+10.4 dB
benefit), 2M 11/12, 6M 12/12 (6.8–17.8 dB). Paper-reported CIs:
**none**. 2M needs 2 unilateral mics, 6M needs 6 bilateral mics —
beyond a standard single-processor form factor. (NH-sim arm:
1M +0.3 dB NS, t(14)=−0.365, p=0.721 — simulation only.)

## 5. Deep ACE / Fused Deep ACE — verdict UNVERIFIED (paper); code causal-capable but not the evaluated artifact

Gajecki & Nogueira, arXiv:2310.01122v1 (2023-10-02) + *IEEE TBME*
journal version (PMID 38376983; IEEE full text not retrieved —
abstract only, its padding/norm UNVERIFIED).

**Paper text audit (ar5iv full-text render, word counts):**
`causal` ×0, `padding` ×0, `normalization` ×0 (`norm` ×6, all
"normal hearing"/"normalized stimulation"/MBSTOI — never a norm
layer). Separator specified only by Table I hyperparameters
(F=64, **L=32**, B=64, H=128, S=32, **P=3, X=8, R=3**) + a pointer
to refs [32,33] "for a detailed description". Training on
**4-second segments**. The latency claim: ACE's 128-pt FFT
*"introduces a 2 ms algorithmic latency"* and Fused Deep ACE
*"introduces the same 2 ms latency as the bilateral ACE setup"*.
**[derived]** 2 ms = L/f_s = 32/16000 — i.e. the **encoder
kernel length**, exactly the encoder-window ≠ receptive-field
error Gen 8 documented for Schulz. With stride L/2 = 16 samples
= 1 ms per encoder frame, a TasNet TCN of P=3, dilations
2⁰…2⁷, X=8, R=3 has receptive field
1 + 3·Σ_x (P−1)·2ˣ = 1 + 3·2·255 = **1531 frames ≈ 1531 ms**;
under symmetric ("same") padding half of it, **≈765 ms**, is
*future*. The paper's 2 ms claim is therefore compatible only
with a causal-padded separator — which the paper never asserts.

**Code audit** (`github.com/tomgajecki/DeepACE`, author's repo;
TF code copyright 2021 MH Hannover, repo first pushed 2025-02-14,
main @ 2025-05-26; no checkpoint, no `params.json`, no release
tying it to the 2310.01122 runs):

- Causality is a **runtime flag**, and it gates exactly the right
  two things. TF `model.py`: `causal → padding="causal"` +
  `_ChannelNorm` (normalises over channels **per time step** —
  causal); `else → padding="same"` + `_GlobalNorm` (mean/var over
  **time × channels of the whole segment** — segment-wide
  noncausal, the gLN pattern). Torch `netblocks.py`: causal →
  left-only pad `(padding, 0)` + cumulative LN (`cLN`); else
  symmetric pad + `GroupNorm(1, ·)` over the segment.
- Shipped defaults point causal: TF `utils.py`
  `--causal default=True`; Torch `config.yaml` `causal: True`.
  **But** the Torch class default is `causal: bool = False`, and
  **both shipped configs contradict the paper's Table I**
  (code: P=128, X=2, R=2; paper: P=3, X=8, R=3 — note P even
  changes meaning between the TF and Torch trees), so these
  configs are demonstrably **not the paper's training configs**.
- **Encoder leak even in causal mode:** TF encoder is
  `Conv1D(kernel=L, stride=L//2, padding="same")` unconditionally;
  Torch encoder `padding=enc_stride` (symmetric). "Same" padding
  centres the 32-sample kernel → each encoder frame sees
  ≈L/2 = 16 samples = **1 ms of future** regardless of the TCN
  flag. As shipped, the code is at best **1 ms-lookahead**, not
  sample-strict-causal, even with `causal=True`.

**Verdict: UNVERIFIED** for the model evaluated in
arXiv:2310.01122 (N=5 BiCI, fixed subject-specific SNRs, HSM
WRS — not SRT: e.g. fused vs unprocessed CCITT 92.07% vs 54.52%,
p=0.008; ICRA7 89.81% vs 57.74%, p=0.008). The code proves a
causal configuration *exists* in the author's lineage and is the
shipped default — upgrade path is a serialized config/checkpoint
for the evaluated runs (or the journal version's separator
spec), **plus** an encoder-padding fix. Until then Deep ACE
cannot be ranked causal, and its "2 ms" must not be quoted as
end-to-end latency. This narrows, but does not close, Gen 9's
UNVERIFIED.

## 6. Synthesis — what changed vs Gen 9

| Gen 9 open item | Gen 10 state |
|---|---|
| Goehring 2019 ms delay unstated | Still unstated; **[derived] 10–20 ms** from 20 ms/10 ms framing, 0 ms future (§2) |
| Kang 2021 N / directionality / effects | **N=7 CI (SRT)**, ≈+6.0/+2.2 dB vs unprocessed ("about"-grade, figure-only); directionality/causality/latency **never stated → UNVERIFIED**; STFT alone implies 16–32 ms if causal (§3) |
| Gaultier 7.4 vs 7.6 dB | **7.6 dB** — from the paper's printed group means (10.5−2.9); abstract 7.4 is the outlier (§4) |
| Gaultier intra-chunk directionality | **Bi-LSTM (Figs. 1–2)** → 1M is chunk-bounded-lookahead (~15.6 ms), not causal; only the inter-chunk path + norm were causalised (§4) |
| Deep ACE padding/norm (code) | Code inspected: flag-gated causal TCN (causal pad + ChannelNorm/cLN) exists and defaults on, but no paper checkpoint/config, config ≠ Table I, encoder "same"-padded (+1 ms future) → **UNVERIFIED stands** (§5) |
| CIs for SRT effects | **Reported by none of the four.** Agent-derived from paired *t* where printed (2019, Gaultier); not derivable for 2017 (SEM figures only) or Kang (no *t*/SD-diff) |

Standing state unchanged: strictly-causal-with-CI-SRT evidence
remains exactly the two Goehring filterbank mask/gain models,
both vs **unprocessed**, adults, ≤3 noise classes. Nothing here
moves a scored cell, mints a candidate, or substitutes for
human dual extraction.

## Unresolved (named)

- Goehring 2017: numeric SEM/SD-of-difference (figure-only) —
  CI for its six effects needs figure digitisation or author data.
- Gaultier 2024: JASA publisher version vs OSF preprint wording
  (paywalled PDF not retrieved; abstract numbers match preprint);
  sampling rate inferred, not printed; FaSNet "4 ms future" vs
  symmetric-window arithmetic (2.5 ms) — paper's bookkeeping.
- Deep ACE: journal (TBME) separator spec; serialized config for
  the evaluated BiCI runs; whether refs [32,33] (2023 Deep ACE,
  N=8) state padding/norm — not inspected in this pass.
- Kang 2021: exact per-α mean SRTs are figure-only (Fig. 8);
  LSTM directionality may be answerable only from author code
  (none linked in inspected text).

*End. Gen 10 extraction under GOAL v2.3. Inspected sources only;
derived values labelled. Scores nothing.*
