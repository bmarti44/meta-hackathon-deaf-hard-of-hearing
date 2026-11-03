# REVIEW — handoff: next directions for the causal CI front-end (speech + direction)

> Written 2026-11-03 by a research-only session (Claude Opus 5.5) for the agent
> continuing the Gen 15/16 → bench-n6 line. This review **changed no code and
> no data**. It combines a read of the repo (gen10–gen16, bench-n6) with three
> literature/documentation sweeps. Citations marked **UNVERIFIED** were not
> confirmed against a primary source and must not be relied on as stated.
> Everything here is T0 / in-silico guidance. Nothing in it authorizes Stage D
> (implant) work. PROTOCOL.md, KPI.md, the safety limiter, and the "no
> listener-benefit claim" rule all still bind.

---

## 0. Your mission (the handoff prompt)

You are continuing the causal noise-reduction + direction-cue front-end for
the holder's son (bilateral Nucleus 6, ACE 8-of-22). Holder direction: speech
understanding and directional hearing are **co-equal**. Push as far as
laptop-scale training allows. Prove everything on the bench (Stages A–C)
before any implant involvement.

Execute the plan in §3 **in order**. Run one generation per change, bench
every interim checkpoint, and file results the same way Gen 13–16 did
(summary + results + independent re-run). Before you start:

1. Read `research/bench-n6/PROTOCOL.md`, `research/bench-n6/KPI.md`,
   `research/gen15/Gen15-summary.md` and `research/bench-n6/results.md`.
2. Let the in-flight Gen 16 run (`research/gen16/train5.py`, seed 20261116)
   finish. Bench all its checkpoints under the unchanged protocol and file
   them. Do not kill it and do not cherry-pick. (Note: the in-flight process
   started before the overwrite guard existed; its final save will overwrite
   the 10-step smoke `causal_seed20261116.pt` and its log JSON. That is
   expected.)
3. Then start §3 Phase 0.

Do not re-litigate holder decisions. The holder's 2026-11-03 answers are in
§7: the KPI split and personalization with the parents' voices are approved;
the processor model is still unconfirmed. Keep legacy readouts beside any new
ones. Never silently move a goalpost.

---

## 1. Diagnosis — why babble is stuck (repo evidence + literature)

### 1.1 The eval "babble" is mostly a target-ambiguity problem, not a noise problem

- `bench.py::build_crops` and `gen13/train2.py::babble` build the held-out
  babble as **k=3 crops drawn from only 2 interferer voices** (8842/8297,
  repeats allowed). Each crop is RMS-normalized, summed, then scaled to the
  target SNR.
- Arithmetic: each interferer sits ≈ SNR + 4.8 dB relative to the target. At
  −5 dB SNR every interfering voice is about as loud as the target (≈ −0.2 dB).
  A single-mic model has **no cue for which voice to keep**. At +10 dB the
  target is simply the loudest voice.
- That matches Gen 15 exactly: per-SNR babble ΔSI-SDR was −0.08 / +0.69 /
  +2.03 / +1.91 dB at −5/0/+5/+10. The gain appears only where "keep the
  loudest talker" is the right rule.
- Literature agrees:
  - Masking changes most as babble goes from 1 to 2–4 talkers, which is where
    a competing voice is most target-like (Rosen et al. 2013, JASA 133:2431).
  - The large competing-talker DNN wins for hearing-impaired listeners were
    talker-dependent: +59 points (Healy et al. 2017, JASA 141:4230) and +26
    points in babble (Healy et al. 2021, JASA 149:3943, trained on one target
    talker).
  - Talker-independent causal systems needed much larger training sets
    (Healy et al. 2021 JASA 150:3976; Healy et al. 2023 JASA 153:2751).
- **Consequence:** the KPI "babble ΔSI-SDR ≥ +3 dB, including ≥ +1.5 dB at
  −5 dB" on this eval is probably unreachable for *any* single-mic causal
  model without a target cue. The fix is to give the model a cue (spatial or
  speaker) and to separate crowd babble from competing talkers in the bench.

### 1.2 Training data is at least an order of magnitude too small

- Training uses 10 speakers, ≈ 81 min of speech
  (`gen16/weights/train_log*.json`: pool_total_s 4869).
- `/tmp/gen12dl/dev-clean.tar.gz` contains 40 speakers; only 14 are
  extracted. Download sizes: LibriSpeech train-clean-100 = 251 speakers,
  6.3 GB; train-clean-360 = 921 speakers, 23 GB.
- Every system that generalized to unseen talkers used far more data:

  | System | Training data |
  |---|---|
  | Deep ACE (Gajecki 2023, IEEE TBME 70:2700) | 30 speakers |
  | Borjigin et al. 2024 (Sci Rep 14:13241; 13 CI users, +20–26 points in 2-talker babble, *non-causal*) | ≈ 250 speakers, 100 h + WHAM! |
  | Schulz et al. 2026 (Front Audiol Otol 3:1746635) | 921 speakers, 364 h |
  | Diehl et al. 2023 (Front Med Eng) | ≈ 10,000 h |
  | Chen et al. 2016 (JASA 139:2604); Healy 2021 | 10,000 noises |

- Generalization needs many speakers and many noises (Kolbæk, Tan & Jensen
  2017, IEEE/ACM TASLP 25:153).

### 1.3 Causality is not the bottleneck

Healy et al. 2021 (JASA 149:3943) found that a fully causal network and the
same network with 20 ms look-ahead differed by only ≈ 2 STOI points (81.7 vs
83.4). Keep strict causality and ≤ 10 ms latency. They cost little.

### 1.4 The objective and the CI readout are misaligned (partly addressed by Gen 16)

- Neg-SI-SDR alone buys waveform fit, not STOI or electrodogram fidelity
  (Gen 15). Kolbæk et al. 2020 (IEEE/ACM TASLP, arXiv:1909.01019) show
  waveform-matching losses can fail.
- Gen 16's ACE term is `log10(env + 1e-6)`, MAE, **pre-selection**. The
  1e-6 floor gives large weight to near-silent bands that a real processor
  never stimulates (below the T-level / base level).
- Deep ACE 1.0/2.0 (Nogueira lab, github.com/APGDHZ/DeepACE2.0) instead use:
  - MSE on the **LGF-compressed electrodogram**;
  - a ×10–15 penalty on wrongly selected bands;
  - **BCE on the 8-of-22 selection mask**.

  A TasNet + ACE baseline trained on SI-SNR did slightly worse than that.
- A noise-removal-biased loss (α ≈ 0.3–0.4) beat plain MSE for CI users by
  3.3 dB SRT (SSN) and 1.2 dB (babble) (Kang, Zheng & Meng 2021, Front Med,
  doi:10.3389/fmed.2021.740123).

### 1.5 Direction — the per-ear model is the wrong topology, and the screen misses the real distortion

- **Cues used:** bilateral CI users localize mostly from broadband and
  high-frequency ILDs; envelope ITD is weak and fine-structure ITD is lost
  under ACE (Aronoff et al. 2010, JASA 127:EL87; Laback et al. 2015,
  Hear Res 322:138).
- **Typical error:** bilateral CI users are at 20–30° RMS vs ≈ 6° for normal
  hearing (Dorman et al. 2016, Audiol Neurotol 21:127). Children range
  19–56° (Grieco-Calub & Litovsky 2010, Ear Hear 31:645).
- **The clinical chain itself distorts ILD by several dB.**
  - The clinical AGC is unlinked per ear: attack 5 ms, release 65 ms, ∞:1
    (Archer-Boyd & Carlyon 2021, JASA 150:506, citing Vaerenberg 2014).
  - During head turns, max ILD deviation is 1.45 dB linked vs 3.56 dB
    unlinked, and ADRO deviation peaks at 19.6 dB at 2.14 kHz (same paper).
  - N6 AGC linking needed custom firmware plus a cable in Potts et al. 2019
    (Trends Hear 23). That gave ≈ 8° RMS improvement and 2.5 dB SRT in
    Nucleus users. So clinical N6 is **unlinked**, inferred, with no explicit
    Cochlear statement found.
- **Current screen weakness:** `spatial.py` uses Woodworth ITD + smooth head
  shadow. It misses the non-monotonic ILD-vs-azimuth behaviour that drives CI
  localization errors (Kelvasa & Dietz 2015, Trends Hear 19). It also measures
  ILD before any N6-like AGC/ADRO.
- **Binaural DNN topology works.** A causal multi-input/multi-output TasNet
  (Han, Luo & Mesgarani 2020, ICASSP, arXiv:2002.06637; 1.67M params,
  < 5 ms) gave:
  - ILD error 0.19 dB vs 0.46 dB for a per-ear TasNet;
  - ITD error 1.8 µs vs 5.8 µs.
- **Binaural input also solves §1.1.** Interaural cues let a model pick the
  frontal target out of lateral babble. Multi-mic CI DNN gains: +7.4 /
  +10.3 dB SRT vs +2.3 dB single-mic (Gaultier & Goehring 2024, JASA
  155:3833; 12 CI users; not strictly causal, ≈ 4 ms look-ahead).

---

## 2. Bench / KPI changes (do these first — Phase 0)

Keep the legacy bench byte-identical and keep reporting it, for continuity.
Add a **v2 bench** alongside it. Pre-register v2 in a committed file before
any model is scored on it.

### 2.1 Split babble into two problems

- **crowd babble:** ≥ 8 talkers drawn from **many held-out speakers**. This
  is noise-like and solvable single-mic.
- **competing talkers:** 1–3 talkers. This needs a target cue, so it is
  scored for single-mic models but expected to stay near-null.

Report both at −5/0/+5/+10 dB. The "≥ +3 dB babble" KPI applies to crowd
babble for single-mic models, and to competing talkers only for binaural or
personalized models. **The holder approved this split on 2026-11-03 (§7).**
Keep the legacy rows reported.

### 2.2 Widen the held-out speakers

Use the other 26 dev-clean speakers and/or test-clean (40 speakers) for
targets and interferers. Two target voices is not a population. Keep a
separate validation split for checkpoint decisions so the test set is never
used for selection.

### 2.3 Add CI-relevant intelligibility proxies

- Compute these on the **8-of-22 vocoded output** (`vocoder.py`):
  - **ESTOI** (Jensen & Taal 2016, IEEE/ACM TASLP 24:2009). It is designed
    for modulated maskers like babble; `pystoi` has `extended=True`.
  - **NCM** (Chen & Loizou 2011, Ear Hear 32:331). It correlates r = 0.90–0.96
    with vocoded intelligibility in SSN and 2-talker babble.
- Keep STOI and post-selection ACE correlation.
- Schulz 2026 found STOI over-predicts benefit by 2–3 dB, so treat every proxy
  as supporting, not truth.

### 2.4 Spatial bench v2 (Stage B2)

- **Rendering:** measured BTE HRIRs/BRIRs.
  - **Kayser et al. 2009** (EURASIP JASP 2009:298605): 3 BTE mics per ear
    plus in-ear on a HATS; anechoic, office and cafeteria rooms. Research use
    only, request form at medi.uni-oldenburg.de/hrir.
  - **OlHeaD-HRTF / Denk 2018** (Trends Hear 22; CC BY-NC-SA) for head
    variability.
  - Hold out rooms and heads for test.
- **Downstream model:** add a per-ear N6-like back-end after the front-end:
  AGC with attack 5 ms, release 65 ms, high ratio, plus a crude ADRO-like slow
  per-channel gain. Measure ILD **after ACE**, per band, in the electrodogram.
- **KPI:** replace raw ILD dB with **predicted azimuth RMS error**. Build a
  per-band ILD → angle lookup from clean BTE HRIRs through the same chain. Run
  a sanity check against the Hu/Dietz modular CI binaural model (Hu et al.
  2023, Acta Acustica 7:42) if it is available.
- **Report cue error separately for target and noise.** MWF-style processing
  can move the noise image (Van den Bogaert et al. 2008, JASA 124:484).
- **Add MBSTOI** (Andersen et al. 2018, Speech Commun 102:1; implemented in
  pyclarity, MIT) as a relative binaural speech gate.

### 2.5 Engineering

- **Train on Apple MPS.** `torch.backends.mps.is_available()` is True on this
  M5 Max (128 GB, 18 cores), but Gen 12–16 trained on CPU. Measure the
  speed-up first, then use it to buy data and steps.
- **Generate data on the fly**, with multiprocessing workers doing HRIR/RIR
  convolution.
- **Stream it.** Build a frame-by-frame streaming implementation of the chosen
  model, measure RTF and latency, and keep the exact suffix-invariance test.

---

## 3. Ranked plan (one generation per change; bench everything)

### Phase 1 — Gen 17: data scale, same Gen 15 architecture (isolates the data effect)

- **Speech:** LibriSpeech train-clean-100 (251 speakers, CC BY 4.0). Go to
  train-clean-360 if MPS throughput allows.
- **Noise:**
  - real recorded noise: WHAM! (binaural cafés/restaurants, CC BY-NC 4.0),
    DEMAND, MUSAN (CC BY 4.0);
  - babble built from **many** speakers with k up to 8–20;
  - synthetic SSN kept.
- **Reverb:** OpenSLR 26/28 RIRs (Apache 2.0) or pyroomacoustics (MIT).
  gpuRIR needs CUDA, so it will not work here.
- **SNR distribution:** weight training toward −5…+5 dB.
- **Seeds:** 3, judged on the seed-mean, per KPI.md.
- **Expected:** crowd-babble gains and better held-out generalization;
  competing talkers still near-null (§1.1).

### Phase 2 — Gen 18: CI-domain loss

- Keep a compressed complex / multi-resolution STFT term:
  - compressed complex spectral loss: Braun & Tashev, arXiv:2009.12286;
  - MR-STFT: Yamamoto et al. 2020, ICASSP, arXiv:1910.11480.
- Replace Gen 16's log-envelope MAE with a **Deep-ACE-style electrodogram
  loss**:
  - a loudness-growth-function (LGF) compression between base and saturation
    levels, so sub-threshold errors cost nothing;
  - MSE on the result;
  - a penalty or BCE on the 8-of-22 selection. A soft top-k or
    straight-through estimator is fine, but no published differentiable n-of-m
    loss was found, so log it as a design choice.
- Add a quiet-identity term to fix the quiet PESQ regression (3.11).
- Optionally add a Kang-2021-style asymmetric weight toward noise removal.

### Phase 3 — Gen 19: low-latency STFT-domain architecture (≤ 10 ms, ≤ 1M params)

- **Front-end:** dual-window STFT — long analysis window, short synthesis
  window (Wang, Wichern, Watanabe & Le Roux 2022, IEEE/ACM TASLP 31:397).
  Strong down to 2 ms algorithmic latency, beating Conv-TasNet at similar
  compute.
- **Backbone candidates:**

  | Model | Params | Notes |
  |---|---|---|
  | GTCRN (Rong et al. ICASSP 2024, github.com/Xiaobin-Rong/gtcrn) | ≈ 24–48K | Small enough to scale |
  | FSPEN (ICASSP 2024) | ≈ 79K | Small enough to scale |
  | GCFSnet (Westhausen & Meyer 2023, WASPAA, arXiv:2307.08858) | ≈ 164K | Causal, 2 ms latency, BTE front+rear mics, binaural link; best match to this budget, and the bridge into Phase 4 |

- Use complex masks or deep filtering over past frames only.
- **Rejected:** DeepFilterNet2/3. It has 40 ms latency and 2.3M params.

### Phase 4 — Gen 20+: binaural, linked, front-target model (the co-equal direction goal)

Can start in parallel once §2.4 exists.

- **Input:** 4 channels (BTE front + rear per ear) rendered with Kayser /
  OlHeaD HRIRs. Target = the frontal talker (0 ± 30°); interferers = lateral
  babble or talkers.
  - Stretch: a direction-conditioned target (Tesch & Gerkmann, ICASSP 2023,
    arXiv:2211.02420; TASLP 2024, arXiv:2304.12023).
- **Output, simplest and cue-safe:** one **common real-valued gain per T-F
  bin**, applied to both ears' reference mics. ILD/ITD of every source are
  preserved by construction (see `LinkedSpectralGate`, which already proves
  0.19 dB).
- **Output, alternative:** per-ear complex filters trained with
  Tokala-style terms (BCCTN, ICASSP 2024, arXiv:2403.05393):
  SNR : STOI : ILD : IPD = 1 : 10 : 1 : 10, with ILD/IPD over speech-active
  bins only, plus an MWF-N-style partial-noise mix-back (η) so the babble
  keeps its position.
- **Pre-AGC linking:** apply a common level/gain across ears in the front-end,
  and optionally keep levels below the N6 AGC knee. This is the laptop
  equivalent of Potts 2019's linked AGC (≈ 8° RMS, 2.5 dB SRT).
- **Optional ILD enhancement, as a fitting parameter, not trained in:**
  - linear angle → ILD expansion (Williges et al. 2018, Trends Hear 22; the
    only variant that discriminated all directions in noise);
  - Francart et al. 2011 (JASA 130:2817): −4 to −10° in bimodal listeners;
  - MOC-style contralateral gain (Lopez-Poveda 2016–2020): 1.6–5 dB SRT and
    25.3 → 22.7° in bilateral CI users.
- **Low priority:** envelope-ITD sharpening (Monaghan & Seeber 2016). It is
  weak under ACE and intelligibility-neutral or worse.

### Phase 5 — personalization (enrollment), as a separate track

- Condition on the child's main talkers (parents, teacher, siblings) via an
  enrollment embedding, or fine-tune.
- **Evidence:** personalized PercepNet PESQ 1.75 → 2.36 (Giri et al. 2021,
  arXiv:2106.04129). pDCATTUNET STOI 79.9 → 85.6 in interfering-talker tests
  (Eskimez et al. 2021, arXiv:2110.09625).
- **Watch target over-suppression.** It rose from ≈ 9% to 15–17% in Eskimez
  2021. Add an asymmetric over-suppression loss (VoiceFilter-Lite,
  arXiv:2009.04323) and a "speaker not enrolled → behave as generic model"
  test.
- Approved by the holder for his own and his wife's voices (§7). Recordings
  stay local and out of the repo.

---

## 4. Delivery path facts (for planning only — Stage D stays unauthorized)

- **Confirm CP910 vs CP920 first.** The CP920 has **no accessory socket**: no
  cable input and no monitor earphones. The monitor earphones being on hand
  implies CP910 but does not prove it. (Source: CP910/CP920 User Guide
  390443 ISS12.)
- **Stereo, independent L/R delivery is possible.**
  - **Cable (CP910 only):** Bilateral Personal Audio Cable. The guide says
    "Bilateral recipients can listen in stereo". The exact L/R pin mapping is
    UNVERIFIED.
  - **Wireless (any CP900):** the **Wireless TV Streamer on its Stereo
    setting** ("For bilateral fittings, the switch should preferably be set to
    the Stereo position"; analog mini-jack input).
  - The Mini Mic 2+ and Phone Clip are probably mono (UNVERIFIED). Do not use
    them for spatial work.
- **Safety:** Cochlear requires the **mains isolation cable** whenever a
  personal audio cable connects to a mains-powered device, *including a
  charging laptop*. Otherwise run on battery.
- **Mixing:**
  - The pediatric default mic:accessory ratio is 1:1 (Nucleus 7 source; the
    N6 ratio set is UNVERIFIED).
  - With mixing, the processor's own mic signal arrives earlier and sums with
    the delayed front-end output. That gives comb/echo artifacts and dilutes
    both the noise reduction and the cues.
  - Any eventual session needs an **accessory-only program** set by the
    audiologist.
  - Whether SmartSound iQ (SCAN/ADRO/AGC) still processes accessory input is
    UNVERIFIED. Model the AGC per §2.4 regardless.
- **Latency:** the wireless streaming latency figure ("< 18 ms") is
  UNVERIFIED. Measure end-to-end latency on the actual path before any session
  design.

---

## 5. Realistic expectations (so effort goes where the evidence is)

- **Single-mic, causal, crowd babble:** the CI precedent is ≈ +2–3.4 dB SRT:
  - Goehring 2019 (JASA 146:705): +3.4 dB babble, 10 CI users, many-talker
    training;
  - Kang 2021: +2.2 dB babble;
  - Gaultier & Goehring 2024: +2.3 dB single-mic.

  Gains concentrate from ≈ 0 dB SNR upward.
- **Competing talkers** need a spatial or speaker cue (§1.1). Binaural
  multi-mic is where large gains live (+7–10 dB SRT, Gaultier & Goehring
  2024).
- **Direction:** a credible target is no added cue error through the N6
  chain, plus a predicted-azimuth improvement over independent-AGC processing
  (literature effects ≈ 3–8°). Do not aim for normal-hearing localization.

## 6. Data / tool licenses (personal, non-commercial use)

- **CC BY / Apache / MIT (usable freely):** LibriSpeech, MUSAN,
  OpenSLR 26/28, BUT ReverbDB, ACE corpus, pyroomacoustics, pyclarity,
  Clarity CEC3 data.
- **Non-commercial only:** WHAM!, EARS, Kayser 2009, OlHeaD, MyST (child
  speech, via LDC), Cochlear Nucleus Toolbox (github.com/Cochlear-Research/
  nucleus-toolbox, CC BY-NC-SA, MATLAB + python — check whether it gives a
  reference ACE/LGF to validate `ace_sim.py` against).
- **GPL-3.0:** AB Generic Python Toolbox.

Record a license column in any new data manifest. Keep the downloads in
`/tmp` or another location outside the repo, as the gen12 convention does.

## 7. Holder decisions (2026-11-03) and remaining open questions

**Decided:**

1. **KPI split (§2.1): APPROVED.** The holder delegated the call ("do what
   you think is best").
   - Single-mic models: the babble KPIs apply to **crowd babble**.
   - Competing talkers: the babble KPIs apply only to binaural or
     personalized models.
   - Legacy-bench rows stay reported side by side. Record the change in
     KPI.md with this date and the holder-delegation note.
2. **Personalization (Phase 5): APPROVED** for the holder's and his wife's
   voices. Both are consenting adults. The son's voice is not needed, since
   enrollment targets are the talkers he listens to.
   - Recordings stay local and out of git (`.gitignore` them).
   - Hash recordings in manifests; do not commit the audio.
   - Never use them in any public artifact.
   - Ask the holder for a short enrollment set per speaker (e.g. 2–5 min of
     read speech in a quiet room) plus some conversational speech for
     held-out testing. Keep enrollment and test utterances disjoint.
   - Bench the personalized model on both enrolled voices **and**
     non-enrolled voices (the no-harm check).

**Still open:**

3. **CP910 vs CP920.** "Nucleus 6" alone does not settle it: both were sold
   for the whole N6 lifetime. To tell them apart:
   - read the model printed on each processor;
   - check whether it has an accessory socket (CP910 has one, CP920 does not
     and is smaller);
   - or check whether the on-hand monitor earphones plug in and work (they
     do on the CP910 only).

   Until confirmed, plan both delivery routes. The TV Streamer route works on
   either model.
4. **Audiologist questions for later:** accessory-only program, streaming
   level limits, and whether SmartSound processing applies to accessory
   input.
