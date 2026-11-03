# Gen 10 J4 — Goehring-class frame-causal DNN front-end as the A1 build (Appendix B)

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> **Gen 10 under GOAL v2.3** (no generation cap, no loop
> stop; PASS bar unchanged). **Inspected sources only**;
> no invented data. Inputs:
> [Gen9-summary.md](../gen09/Gen9-summary.md),
> [causal-dnn-search.md](../gen09/causal-dnn-search.md)
> (rank 1 Goehring 2017 NNSE, PMC5256482; rank 2
> Goehring 2019 RNN-LSTM ERM, PMC6773603 — both full-text
> inspected there), [candidate-J3-bench.md](../gen07/candidate-J3-bench.md)
> (Stage-0 bench, B1–B10, HP-J3-1/2),
> [candidate-J2-ai-pediatric.md](../gen06/candidate-J2-ai-pediatric.md)
> (comparator C-J2, stages, K1–K4, HP-J2-1…6),
> [candidate-J1-ai-frontend.md](../gen05/candidate-J1-ai-frontend.md)
> (HP-J1-1…4). **Authority: agent synthesis = triage
> only.** Human dual extraction, protocol/freeze/
> held-out, H-1…H-8, manifest/class ratification, every
> HOLDER-PIN: **PENDING**.
>
> **What J4 is.** The A1 build decision Gen 9 §4 push 2
> left open ("causal-ConvTasNet retrain *vs*
> Goehring-class design"), taken on paper for the
> Goehring class. J4 names one buildable architecture
> whose causality holds **by construction** — past +
> current frames only, causal normalisation, no segment
> statistic — so the J3 bench audits a finite 24 ms
> past span, not a 765 ms dilated future. **What J4 is
> not:** a scored result, a trained model, or evidence.
> No weights exist. No latency, power, or SRT number
> for J4 has been measured. §3's latency budget is
> **T0 in-silico arithmetic** from filed parameters —
> a lower bound the bench can falsify, never HP-J2-1.
> Goehring SRT effects are external ledger-class
> evidence vs unprocessed in adults; they mint no
> `delta_g2_db`, no PASS, and (§2.3) do not transfer to
> J4's retimed frames. **`promoted FALSE`, FROZEN
> retained, G3b BLOCKED, validation set 0.** J-lineage
> unfielded pending **HP-J1-4**; J4 widens that fence
> by nothing.

## 1. Why the Goehring class, and why not causal ConvTasNet

Gen 9's inspected verdict, carried without re-grading:

- Exactly two strict frame-causal models have human CI
  adaptive-SRT data, both Goehring filterbank mask/gain
  designs: 2017 NNSE (N=14; gain from current + past
  frames; 10 ms stated delay; speaker-independent SRT
  vs unprocessed ACE +1.4 dB SWN, +5.4 dB ICRA, +0.4 dB
  NS babble; noise-specific training) and 2019
  RNN-LSTM (N=10; mask for frame *j* from *j−4…j*;
  +3.4 dB babble significant, +2.0 dB traffic NS; no ms
  end-to-end delay stated).
- No causal ConvTasNet, DeepFilterNet, DPCRN, or CRN
  with any human CI evaluation surfaced (Gen 9 search,
  2026-11-03). Causal ConvTasNet configs exist
  (cLN for gLN) objective-only, N=0 CI. Choosing that
  branch would anchor A1 to a class with zero CI
  precedent *and* the exact audit failure Gen 8/9
  executed against (serialized `causal=False`, `gLN`;
  replay rel. RMS 0.593 in the shared prefix, first
  differing sample 0).
- Gaultier & Goehring 2024 (+2.3 dB 1-mic to +10.3 dB
  6-mic, N=12) is bounded-lookahead (~15 ms / 4 ms
  future), not causal: inadmissible as J4 architecture
  under J2's causal-only rule, admissible only as the
  standing price of lookahead J4 refuses to pay.
  Deep ACE/Fused causality stays UNVERIFIED (no
  padding/norm in inspected text); J4's design exists
  so that no J-build ever sits in that cell again:
  every padding and norm choice is filed below, in
  advance, in this document.

The class choice buys auditability, not effect size.
Per-frame gain/mask regression has no dilated-TCN
receptive field to misread (Gen 9 search, "Notes on
the two strict-causal positives"). It also inherits
the class's recorded weaknesses, which §5–§6 convert
into kills rather than caveats: 2017's babble null
under speaker-independent training, 2019's traffic
null, noise-specific / two-noise training throughout,
and every effect measured vs **unprocessed** — while
J4 must beat SCAN 2 (§6).

## 2. A1 architecture spec — `J4-A1` (causality by construction)

One build, not a family. Anything not listed here is
not part of J4-A1; any change to a filed row after
HP-J4-1 freeze is a new build (new weights hash,
HP-J2-3 re-filed, bench re-run). Values marked
PROPOSED are design budgets for human ratification at
HP-J4-1, in the J3 sense: ratified before training,
never loosened after seeing data.

### 2.1 Signal path

```text
mic (single, primary) → causal framing/filterbank (§2.2)
  → per-frame features F_j → unidirectional LSTM stack (§2.3)
  → mask M_j ∈ [0,1]^B → masked filterbank envelopes
  → ACE-class sound coding, MAP, charge/phase UNCHANGED
```

- **Domain:** filterbank-envelope masking inserted
  *before* sound coding (J2 mechanism carried). J4-A1
  emits **no resynthesised waveform**: there is no
  overlap-add synthesis stage and therefore no
  synthesis lookahead term (§3). A waveform-output
  variant is a different candidate, not a J4 option —
  its T0 budget already fails B1 (§3.3).
- **Microphones:** single-microphone primary. Dual-
  mic input (concatenated per-mic features, same
  frame grid, same causality rules) is a secondary
  stratum only if HP-J4-1 files it with its own
  weights hash; multi-mic beamforming / FaSNet-class
  spatial modules are out of scope (they import the
  4 ms-future construction Gen 9 excluded).
- **Target rule:** none beyond denoising — J4-A1
  estimates a speech-presence mask, it does not
  select a talker. The two-frontal-talker condition
  (J3 S8 / J2 stress) is therefore scored as
  interferer-speech leakage, not wrong-talker
  selection; a build that suppresses the frontal
  target as "noise" fails §6 quiet/music NI and the
  S8 attribution screen. Any future target-selection
  head reopens HP-J2-3 as a new build.

### 2.2 Framing and features (the latency-bearing rows)

| Parameter | J4-A1 value | Provenance |
|---|---|---|
| Sample rate `fs` | 16,000 Hz | Both Goehring records at 16 kHz class (2019: 20 ms/10 ms "at 16 kHz", inspected Gen 9) |
| Window `W` | **128 samples = 8.0 ms**, right-aligned: frame *j* = samples `[jH, jH+W−1]`, emitted only when sample `jH+W−1` exists. **No centre padding** | PROPOSED retiming (§2.4); 8 ms block length matches 2017's inspected 8-ms FFT blocks |
| Hop `H` | **64 samples = 4.0 ms** (50% overlap; 250 frames/s) | PROPOSED retiming (§2.4) |
| Future frames `L` | **0** | Causal-only rule (J2 §3; J3 B3) |
| Past context `K` | **5 frames** (*j−4…j*) | 2019 inspected: "steps 1-5 corresponded to successive frames j-4…j" |
| Bands `B` | PROPOSED 64 log-magnitude filterbank bands per frame; exact filterbank (type, spacing, floor) pinned HP-J4-1 | Causality/latency invariant to `B`; compute is not (§3.4 formula carries `B` symbolically) |
| Features `F_j` | log band energies of frame *j* only. No delta/delta-delta computed with a centred difference (a centred delta reads *j+1* and is a desk-kill, §7 K-J4-0); if deltas are filed at HP-J4-1 they are backward differences `F_j − F_{j−1}` | By construction |

### 2.3 Network (every row is a causality row)

| Component | J4-A1 | Barred alternatives (desk-kill if present) |
|---|---|---|
| Recurrence | 2 hidden **unidirectional** LSTM layers, 128 units (2019 inspected sizes), state carried forward only; state reset behaviour at stream start/dropout filed HP-J4-1 (zero-state, §3.2 priming) | BiLSTM (Borjigin-class), any backward pass over the utterance |
| Output | Fully-connected + sigmoid → mask `M_j` for frame *j* (2019 inspected head) applied to frame *j* envelopes in the same hop | Mask applied to any frame ≠ *j*; smoothing `M_j` with `M_{j+1}` (centred smoothing reads the future; trailing-only smoothing, if filed, uses `M_{j−1}` and adds no latency) |
| Normalisation | **Causal only:** per-frame layer norm over the feature axis of `F_j` alone, *or* cumulative layer norm (cLN/cgLN class) whose running mean/variance at frame *j* uses frames ≤ *j* only. One choice pinned HP-J4-1; statistics code inspected at audit (§2.5) | `gLN` / any whole-segment or whole-utterance statistic (the Gen 9 replay mechanism: one suffix rewrote the prefix from sample 0); batch norm with batch statistics at inference |
| Convolutions | None in the core path. If HP-J4-1 files a front-end conv, left-padding only (pad = kernel−1 past samples, 0 future), dilation into the past only | Symmetric/`same` padding (reads ⌊k/2⌋ future samples per layer), transposed convs |
| Attention/pooling | None | Transformer/self-attention over the segment, global pooling over time, dual-path chunking with intra-chunk bidirectionality (the Gaultier 1M unresolved row) |
| Gain stage | Masked envelopes feed ACE unchanged; no output gain make-up that can exceed the filed MAP. Any over-MAP sample = J3 B8 desk-kill | Level-creep / loudness re-normalisation over a window including future frames |

### 2.4 The retiming mutation — stated, not smuggled

J4-A1 keeps 2019's *topology* (5-frame context,
2×128 uni-LSTM, sigmoid mask) and changes its *clock*:
published 20 ms window / 10 ms hop → 8 ms / 4 ms.
Reason is arithmetic, §3.3: at 20 ms the T0 window
term alone equals the B2 hard ceiling (20 ms) before
one microsecond of compute, so the as-published
framing cannot pass J3 B1 (≤10 ms p99) on any
hardware. **Consequence, binding:** the published
+3.4 dB babble / +2.0 dB traffic effects were measured
at 20/10 framing and **do not transfer** to an 8/4
retrain. J4-A1 at 8/4 is an unmeasured model whose
only inherited assets are (a) proof that the class
can be frame-causal, (b) effect *signs* vs
unprocessed at other parameters. Its SRT is decided
in §6 Stage 1 or nowhere. The 2017 NNSE (feed-forward
gain from `[F_n, F_{n−1}]`, 8-ms blocks, 10 ms stated
delay) is filed as the **fallback topology** if
HP-J4-1 humans prefer the shallower network: same
§2.2 framing, `K=2`, no recurrence. Fallback ≠ second
chance: if both topologies are trained, both are
separate builds with separate hashes, and selection
between them on validation material is a held-out
breach (J3 §B.3.3 carried). HP-J4-1 names exactly one
primary topology before training starts.

### 2.5 Causality audit (static, pre-bench, pass/fail)

Before J3 sees the build, three desk checks on the
locked graph + weights hash (HP-J2-3):

1. **Index audit:** for output frame *j*, enumerate
   every input sample the graph can read. Required:
   max input sample index ≤ `jH+W−1`. One line of
   arithmetic from §2.2–2.3; a graph that cannot
   produce this bound (opaque padding, segment norm)
   fails uninspected = fails, cf. Deep ACE UNVERIFIED.
2. **Norm audit:** every normalisation node's
   statistic set ⊆ frames ≤ *j*, read from source,
   not from the config flag (Gen 8 lesson: the flag
   is the claim, the code is the evidence).
3. **Suffix-replay (Gen 9 method, inverted):**
   identical 1 s prefix, differing suffixes; a causal
   build must return prefix Δ = **exactly 0** (the
   bar Gen 9 set: "A causal system must give 0" —
   Schulz gave 16,000/16,000 differing samples).
   Any Δ > 0 = K-J4-0 desk-kill (§7), no bench slot.

J3 §B.4.4 shift test then re-audits the same property
acoustically on hardware; static/bench disagreement
voids the run (J3 carried).

## 3. In-silico latency budget (T0 — arithmetic, not measurement)

**Label: T0 (GOAL §5.3), mechanism plausibility
only.** Every term below is computed from §2.2
parameters. Nothing here fills HP-J2-1 (measured
latency/power/sync file), predicts bench p99, or
enters a G-cell. Convention = J3 §B.4.1 end-to-end
definition decomposed; T0 covers the *algorithmic*
terms only and prints compute/I-O as the unmeasured
residual the bench owns.

### 3.1 Terms

```text
T_alg  = T_window + T_lookahead + T_synthesis
T_e2e  = T_alg + T_compute + T_IO + T_ACE/RF      (bench-measured terms last)
```

| Term | Arithmetic | Value |
|---|---|---|
| `T_window` (collect frame *j*) | `W / fs = 128 / 16000 s` | **8.0 ms** |
| `T_lookahead` | `L × H / fs = 0 × 64 / 16000 s` | **0.0 ms** by construction |
| `T_synthesis` | no waveform resynthesis (§2.1); mask applies to frame *j* envelopes in-hop | **0.0 ms** |
| **`T_alg` (T0 subtotal)** | `8.0 + 0.0 + 0.0` | **8.0 ms** |
| `T_compute + T_IO + T_ACE/RF` | not computable from architecture parameters; J3 §B.4.2 impulse method on H-primary | **UNMEASURED** |
| Headroom to J3 B1 (p99 ≤ 10 ms) | `10.0 − 8.0` | **2.0 ms** for all unmeasured terms |
| Headroom to J3 B2 (max ≤ 20 ms) | `20.0 − 8.0` | **12.0 ms** |
| Frame deadline (sustained compute) | `H / fs = 64 / 16000 s` | **4.0 ms/frame**; overrun = J3 B4/B5 kill territory |

Reading the budget honestly: 8.0 ms is a *floor*.
J4-A1 passes B1 on paper only in the weak sense that
its floor leaves 2.0 ms of room; whether a Nucleus-
class processor executes 250 frames/s of LSTM inside
that room is exactly what Stage 0 measures (K1). A
T0 floor above B1 would have desk-killed the design
without hardware — that is the only job this section
can do, and §3.3 does it to two neighbouring designs.

### 3.2 What past context costs (and what it does not)

- Steady-state latency contribution of frames
  *j−4…j−1*: **0 ms** — already observed when frame
  *j* closes. Past context is memory, not delay.
- Total waveform span one mask can depend on:
  `(K−1)·H + W = 4×64 + 128 = 384 samples = 24.0 ms`,
  all of it ≤ current sample. Contrast filed for
  scale: the dead Schulz checkpoint's masker future
  context was **765 ms** (Gen 8/9) — J4's entire
  receptive field, past included, is ~3% of that
  lookahead alone.
- Priming: from stream start, first full-context
  mask at `(K−1)·H + W = 24.0 ms`. Before that,
  zero-state LSTM + causal zero-padding of missing
  past frames emits masks from the first frame
  (8.0 ms); priming behaviour after dropout/
  processor-off is filed HP-J4-1 and shown on the
  bench steady-state run (J3 §B.4.4.3), never
  assumed inaudible.
- 2017 fallback (`K=2`, 8 ms blocks): span
  `1×H + W`; at its inspected 1 ms hop (8-ms blocks,
  7-ms overlap) span = 9.0 ms, `T_window` = 8.0 ms —
  order-consistent with its stated 10 ms delay
  (inspected), which is *its* measured-system claim,
  not evidence about J4-A1.

### 3.3 Neighbouring designs priced by the same arithmetic

| Design | `T_window` | `T_lookahead` | `T_alg` floor | vs B1/B2 |
|---|---|---|---|---|
| **J4-A1 (8/4, envelope mask)** | 8.0 ms | 0 | **8.0 ms** | 2.0 ms under B1 — bench decides |
| Goehring 2019 as-published (20/10) | `320/16000` = 20.0 ms | 0 | 20.0 ms | = B2 ceiling before compute → B1 impossible; hence §2.4 retiming |
| J4 with waveform WOLA (`+1 hop`) | 8.0 ms | 0 + synthesis `64/16000` = 4.0 ms | 12.0 ms | > B1 on paper → why §2.1 bars waveform output |
| Gaultier FaSNet-class (for scale) | — | 4 ms future (inspected) | — | Not causal at any window; excluded, §1 |

### 3.4 Compute size (T0 formula; power stays blank)

Parameter count as a function of bands `B`
(`h = 128`; LSTM layer = `4h·(in + h + 1)`):

```text
L1 = 4·128·(B + 129)      L2 = 4·128·257 = 131,584
FC = 129·B                total = L1 + L2 + FC
```

At the PROPOSED `B = 64`: L1 = 98,816; FC = 8,256;
**total = 238,656 parameters**. Multiply-accumulates
per frame ≈ `4h(B+h) + 4h(2h) + hB` = 237,568 MAC at
`B=64`; at 250 frames/s ≈ **59.4 MMAC/s** sustained.
These are sizing numbers for HP-J4-1 hardware debate
only. **No mW, mA, battery-hour, or thermal figure
is derived from them** — no Nucleus-class current
draw or battery capacity exists in any inspected
record (J3 §B.2 item 5, carried verbatim); power is
a bench output (J3 §B.5), and any version of this
file containing a pre-filled power number is
fabricated.

## 4. Training data plan (design material only; partition before training)

Training choices are filed here because Gen 9 showed
training regime *is* the generalisation limit of this
class (2017 noise-specific networks; 2019 two noises,
traffic NS). The plan is written to make those exact
failures visible early, at T0, cheaply.

- **Target:** ideal ratio mask / Wiener-class gain in
  the §2.2 filterbank, computed from clean target
  speech per frame *j* (target definition, exponent,
  and flooring pinned HP-J4-2; the mask target is
  part of the intervention, HP-J2-3 carried).
- **Loss:** mask-domain regression loss named and
  version-pinned HP-J4-2. A quiet-identity term
  (target mask = 1 on clean/quiet frames) is
  mandatory by design: quiet NI (−5 pp, §6) is
  defended in training, not discovered in children.
  No loss term may read future frames (offline
  training with non-causal *targets* is admissible —
  the deployed graph is what §2.5 audits — but any
  non-causal teacher is named as A2-class design
  material, and tuning against A2 on validation
  material is a held-out breach, J3 carried).
- **Speakers:** many-talker training, **speaker-
  independent primary claim** (2019 trained
  many-talker / tested unseen talker, inspected).
  Speaker-dependent variants (2017 NNSE-ST) are
  barred as a primary claim — a per-child fine-tune
  is a different candidate with its own burden
  accounting. Talker-disjoint train/validation
  split by talker *and* corpus.
- **Noises (train broad, hold out whole classes):**
  training pool spans multi-talker babble (primary
  geometry class), stationary speech-shaped noise
  (specificity control), modulated/ICRA-class noise,
  and traffic/environmental recordings — i.e. the
  classes carrying the inspected Goehring records
  (babble +0.4 dB NS in 2017 and +3.4 dB in 2019;
  ICRA +5.4 dB, SWN +1.4 dB in 2017; traffic
  +2.0 dB NS in 2019), so the nulls are
  inside the training distribution and cannot be
  blamed on it. **At least one entire noise class
  and one corpus are held out of training** and used
  only at the sealed T0 screen (§5 Stage 0 objective
  metrics): a build whose objective gain exists only
  on trained noises replicates 2017's limit and is
  filed as such before any listener is recruited.
  Noise-specific per-class networks (2017 regime)
  are barred for J4-A1 primary.
- **Mixture grid:** SNR and level grid pinned
  HP-J4-2 spanning the §6 test grid (J3 proposed
  −10…+10 dB; 55/65/75 dB SPL targets), reverberation
  condition filed explicitly (anechoic-only training
  with reverberant claims = mislabelled build;
  Gaultier's noisy-reverberant condition is the
  standing reminder that the field tests there).
- **Held-out discipline (GOAL §5.2):** partition
  committed *before* training by talker, corpus,
  noise instance, and (for any listener stage) by
  child; bench-dev vs bench-validation split per
  J3 §B.3.3; seeds, corpus licenses, and file hashes
  into the run archive (J3 §B.8). Rebuild after
  opening validation = fresh validation set or
  exploratory-after-seen: Y. **Validation set for
  the J-lineage today: 0** — this plan creates the
  *slot*, not the set.
- **No child data in training/tuning** for any build
  whose Stage 1/2 children could overlap it; child
  speech corpora, if HP-J4-2 files them for
  robustness training, are design material with
  their own partition and consent/licence record,
  and confer no pediatric claim (T0 stays T0).

## 5. Stage 0 — bench with J4-A1 in the A1 slot

Unchanged J3 protocol, J4 supplies only the build:
A0 = C-J2 passthrough (Nucleus 8 / Kanso 3, SmartSound
iQ 2 + SCAN 2 feature state as filed, HP-J2-2);
**A1 = J4-A1** (locked hash post-§2.5 audit); A2 =
Schulz/Keles checkpoint or SepFormer-class offline
oracle, ceiling reference only, inadmissible for any
pass (Gen 9: checkpoint stays A2-only; its 5.9 dB
stays offline, ledger-only, unscoreable). Hardware
strata H-primary / H-dev / H-secondary, signals
S1–S10, diffuse-babble recipe, latency/power methods,
and thresholds **B1–B10 are inherited verbatim** —
J4 changes no bench number. For the record, the
rows J4's §3 arithmetic pre-registers against:
B1 p99 ≤10 ms (T0 floor 8.0 ms + UNMEASURED residual),
B2 max ≤20 ms, B3 look-ahead = 0 (§2.5 predicts pass;
the bench shift test decides), B8 over-MAP = kill.
B4/B6/B7/B9 blanks stay blank until HP-J3-2 humans
ratify them; the bench does not run bilaterally with
B6 empty (J3 carried). Bench output fills HP-J2-1
and decides K1 only; objective metrics on sealed
material (incl. the §4 held-out noise class) are an
engineering screen with no pass threshold (J3 §B.7
design), reported with A2 as ceiling to price what
causality at 8/4 framing cost against the offline
oracle. **Stage 0 moves no G-cell.**

## 6. Adult bridge vs SCAN 2, then gated pediatric descent

Stage order is J2's, inherited: each stage gates the
next, stages are study-readiness units, never
promotion steps. J4's contribution is naming what
sits in the ON arm.

### 6.1 Stage 1 — adult bridge (T3, provisional only; K-J4-2 lives here)

- **Population:** experienced adult Cochlear Nucleus 8
  / Kanso 3 users on their own processors/MAPs.
  Adult data file **no** pediatric claim; min tier
  for any G2 PASS stays T4.
- **Arms (within-subject):** ON = J4-A1 inserted
  before sound coding; OFF = **C-J2: SmartSound iQ 2
  with SCAN 2, feature state exactly as fitted/enabled
  for that adult** (per-user state filed, HP-J2-2;
  automated ForwardFocus state recorded, never
  assumed). Same implant, MAP, battery type.
- **Primary readout:** adaptive SRT (SNR-50) in
  diffuse/co-located multi-talker babble (J2 frozen
  primary geometry, speech S0). Secondaries:
  S0Nrearhalf / S0N3 spatial babble (where C-J2 is
  strongest — inspected pointer: SCAN 2 + automated
  ForwardFocus beat SCAN 2 alone by 4.2–4.3 dB there,
  PMID 41046328, adult T3, via J2/J3), stationary
  speech-shaped noise (specificity control),
  two-frontal-talker stress, quiet co-primary every
  session, music battery (named HP-J2-4). Procedure
  guards per J2: list randomisation, practice to
  plateau, blinded scoring, AB/BA order, matched
  acclimatisation.
- **The honest prior:** Goehring effects are vs
  *unprocessed*. In the primary geometry's noise
  class, the speaker-independent precedent is
  +0.4 dB NS (2017 babble) and +3.4 dB (2019 babble,
  at 20/10 framing J4 does not use, §2.4) — both
  against no front-end at all. Against SCAN 2 the
  available headroom is unknown and plausibly
  smaller. That is precisely what the kill is for:
- **Kill K-J4-2: primary-geometry SRT advantage
  (J4-A1 − C-J2) < 3 dB in adults ⇒ J4 dies; no
  child is recruited.** 3 dB = Appendix A G2 PASS
  delta, not a J4 invention. Precision rule (J2
  carried): the 95% CI must exclude both 0 and the
  <3 dB region to advance; a CI spanning 3 dB at
  locked N = INSUFFICIENT-precision = design-as-
  powered killed, no post-hoc re-powering. Quiet NI
  (−5 pp), spatial-secondary NI, and music NI
  breaches kill at this stage too (K-J4-4).
- **No N asserted** (J2 rule): no within-subject
  SRT-difference SD for this contrast exists in
  inspected records; pilot/run-in SD is obtained,
  then N locked before unblinded analysis (HP-J4-3).
  N=14/N=10 (Goehring) and N=20 (PMID 41046328) are
  feasibility pointers for design, barred as
  variance sources.

### 6.2 Stage 2 — pediatric descent (T4; the G2 decider, gated)

Exists **only if** HP-J1-4 signs, Stage 0 clears K1,
and Stage 1 clears K-J4-2 — in that order. Design =
J2 Stage 2 verbatim with J4-A1 as the ON build:
Bands A (6.0–7.0 y, primary open-set SRT, same
geometries and C-J2 comparator with age-labeled
SCAN 2 feature state) and B (4.0–<6.0 y, closed-set
word-in-noise + localisation, **no SRT PASS or kill
read from Band B**), AB/BA take-home crossover,
datalogged wear-time, alarm battery (HP-J2-5),
testability counts printed per §3.2 stratum,
treatment-policy denominators. **Kill K-J4-3:**
Band-A primary SRT < 3 dB vs C-J2 (point or
precision rule) ⇒ J-lineage front-end claim in this
form retired; no Band-B/C rescue narrative. Stage 3
(language-trajectory, G3a) only if separately frozen
after K-J4-3+K-J4-4 clear; the SRT→language
mediation assumption stays UNRESOLVED until measured
in linked children (GOAL §5.3). **No W0/W1 efficacy
claim of any kind**; infant windows remain
mechanism-chain only. Off-label enabling of
age-gated comparator features below labeled ages is
barred unless the human protocol/ethics route
explicitly authorises and labels it (J2 carried).

## 7. Appendix B — full specification (GOAL App. B, all fields)

- **ID / track:** `GEN10-J4`. Track P portfolio
  component *iff* HP-J1-4 signs (G1 = NA proposed);
  if HP-J1-4 denies NA, J4 withdraws with J1/J2/J3
  together. Manifest:
  [`manifest-GEN10-J4.csv`](./manifest-GEN10-J4.csv)
  (G1 not required by NA proposal; G2–G6 required;
  manifest/class ratification PENDING human).
- **Mechanism & target cells:** §2 — frame-causal
  filterbank mask estimation (uni-LSTM 2×128,
  *j−4…j*, causal norm) before ACE-class coding; MAP
  and charge/phase unchanged. No cells targeted, no
  biology touched, no surgery. Intervention = J4-A1
  ON vs C-J2 OFF on the same hardware.
- **Delivery route & dose/units:** software/firmware
  research build on the user's existing external
  processor (H-primary); body-worn front-end results
  labeled non-transferable (J2/J3 carried). Dose =
  locked weights hash (HP-J2-3) × datalogged
  wear-time h/day. Latency/power budgets are bench
  gates (§3 T0 floor 8.0 ms; B1 ≤10 ms p99, B2
  ≤20 ms max, measured) — no parameter of §2.2 may
  be changed to meet them after freeze without a
  new build.
- **Timing by window & decision origin:** deployable
  from first activation in principle; *tested* only
  bench → adult (T3) → W3 pediatric G2 (Bands A/B)
  → W2/W3 G3a trajectory slot. Decision origins
  9/12 mo inherited pathway facts; no W0/W1 claim.
  Reversible ≤1 fitting session (rollback bench-
  tested Stage 0, J3 B10).
- **Model system / comparator:** C-J2 primary
  (Nucleus 8/Kanso 3, SmartSound iQ 2 + SCAN 2 as
  fitted per age band, HP-J2-2); C-J2-M (MED-EL
  SONNET 3/RONDO 3, ASM 3.0) secondary stratum,
  reported separately, never pooled; AB excluded
  pending HP-J2-2 IFU inspection. Beating C-J2 is
  the kill/advance question; any C0 language also
  requires the frozen `frozen_bilateral_eCI_v1`
  contrast and its claim cap (implementation gap
  ≠ C0 win). Unprocessed mixtures are **not** a
  comparator anywhere in J4 (they are the Goehring
  literature's comparator, which is why that
  literature cannot pre-answer §6).
- **Eligibility by §3.2 stratum:** genotype/anatomy-
  agnostic in theory for C-J2/C-J2-M users;
  testability is the honest restriction, reported
  per stratum (Bands A/B/C per J2 §3 carried).
  ANSD/CND/malformation/syndromic/additional-
  disabilities: included-and-stratified, never
  dropped from denominators. Bilateral: same arm
  both ears, sync per HP-J1-3/B6 (bench must not run
  bilaterally with B6 blank). Bimodal CI+HA:
  separate stratum; HA-side DNN out of scope, no
  hearing-aid evidence imported. Adult Stage 1:
  experienced adult C-J2 users (stratification by
  the same §3.2 axes where recordable).
- **G1–G6 measurement plan (App. A cells):**
  - G1 = NA (proposed, HP-J1-4). No channel claim;
    bilateral timing handled as G5/G2-localisation
    safety measurement, never a G1 win.
  - G2 primary: SRT-in-noise (J4-A1 − C-J2), advance
    ≥3 dB primary geometry + quiet NI −5 pp +
    spatial NI; Band-A Stage 2 is the decider (T4);
    Stage 1 adult = provisional/kill only. Band-B
    word-in-noise ≥10 pp / localisation ≥10°
    (NI −5 pp / +5°), music ≥10 pp (NI −5 pp)
    secondary per J2/App. A.
  - G3a: Stage-3 slot only, modality-matched SS
    (+0.4 SD / NI −0.2 SD, W2/W3, T4);
    INSUFFICIENT until separately frozen and run.
  - G3b: BLOCKED. Preference/wear-time descriptive
    only; no instrument/MCID/autonomy inference.
  - G4: no biology touched (design fact, scored as
    a win nowhere); EAS/bimodal residual-hearing
    protection = MAP/output-limiting unchanged,
    bench-verified (B8).
  - G5: per-harm NI per §8 FMEA; dedicated alarm/
    environmental battery (HP-J2-5) and localisation
    NI; latency harm closed at bench (B1/B2) before
    any human exposure.
  - G6: wear-time NI (datalogged), battery-swap/
    charge events/day, fitting visits, exclusion-for-
    testability/hardware rates by stratum (single-
    manufacturer coverage stated, no % asserted —
    App. D numerators unpinned), zero-added
    caregiver program-management (fully automatic;
    a build needing per-environment parent program
    selection fails the burden test C-J2 passes).
- **Power/precision:** no N asserted anywhere (§6.1).
  Estimand = within-user mean SRT difference,
  treatment-policy; precision rule = 95% CI excludes
  0 and the <3 dB region to advance; variance inputs
  owed from run-in/pilot, N locked pre-unblinding
  (HP-J4-3). Objective-screen metrics carry no
  power claim (T0).
- **FMEA summary:** §8 (App. C rows; J2 rows
  inherited, J4-new rows marked ◆).
- **Burden:** C-J2 visits + filed acclimatisation
  sessions per arm (counted, not invented hours,
  until Stage 1 measures them); daily charge/swap
  from datalogs + Stage-0 battery projection (B7:
  ≥16 h reference day, relative-loss % still
  HP-J3-2 blank); travel per G6. Training a build
  is project burden, never family burden; no
  per-child fine-tune in primary (§4).
- **Regulatory class & staging (§10):** device
  software change on a marketed processor,
  investigational build; class/IDE-equivalent route
  named at human freeze; adult-bridge-before-
  pediatric-decider staging (§6); pediatric T4
  required for every child claim; no promotion
  language at any stage here.
- **FTO flag:** processor owners hold the deployment
  surface; Goehring-class methods are published
  academic designs (patent/FTO status **not**
  inspected in this generation — flagged, not
  cleared); corpus/model licenses filed HP-J4-2.
  Research-use only; no design-around advice.
- **Kill criterion:** §9 (K-J4-0…4, all
  unevaluated).
- **Parentage + single-mutation log:** parents =
  GEN6-J2 (design of record: comparator, stages,
  kills) + GEN7-J3 (bench) + Gen 9 causal-search
  ranks 1–2 (external architecture precedent).
  Single mutation **M-J4-1:** *name the A1 build* —
  J2/J3 left A1 abstract ("a causal DNN build");
  J4 fixes it to the Goehring-class spec of §2 with
  the §2.4 retiming (20/10 → 8/4) as an explicit,
  SRT-non-transferring sub-mutation. No comparator,
  geometry, threshold, gate, or stage is mutated.
- **Exploratory-after-seen:** Y — after Gen 9
  causal-dnn-search + executed noncausality replay
  (2026-11-03), Gen 8 checkpoint autopsy, and
  J2/J3's inspected records (PMIDs 38853168,
  37030808, 41046328; manufacturer battery
  conventions). Validation = J4's own sealed
  bench/Stage-1/Stage-2 material (partitions §4);
  none exists yet. Validation set: **0**.

## 8. FMEA (App. C; Sev 1–4, probability + source tier)

| Harm | Sev | Prob (tier) | Mitigation / G5 input | Stopping rule |
|---|---|---|---|---|
| Latency degrading AV synchrony / own voice | 2 | Bench-measurable (Stage 0); 10–20 ms disturbance bound (PMID 38853168 via J2/J3) | T0 floor 8.0 ms (§3); B1/B2 measured incl. in-babble | Bench over budget → desk-kill, no human exposure |
| ◆ False causality (hidden future path: centred delta, `same` padding, segment norm) | 2 | Design risk — the exact Gen 8/9 failure | §2.5 three-part audit; Gen 9 suffix-replay Δ=0 bar; J3 §B.4.4 shift test | Any Δ>0 / audit failure → K-J4-0, no bench slot |
| ◆ Trained-noise overfit (2017 regime) / traffic-class null (2019) | 2 | Named class risk (inspected records) | Broad training + held-out class/corpus screen (§4); traffic inside test battery | Objective gain only on trained noises → filed human-withdrawal decision pre-Stage 1 (J3 D10 language) |
| Masking artefacts / musical noise; target speech suppressed as noise | 2 | Unstated (T3 lab class) | Quiet-identity loss (§4); quiet + music NI; S8 leakage screen | Quiet/music NI breach → K-J4-4 |
| Suppression of alarms / environmental sounds | 3 | Unstated | Alarm battery HP-J2-5 both arms; bench alarm-band levels (J3 §B.6) | Any missed-alarm signal vs C-J2 → halt arm, DSMB-equivalent review |
| Wear-time loss (compute/battery/heat at 250 frames/s) | 2 | Bench + datalog | §3.4 sizing; B7 battery projection vs 16 h day; thermal logging (J3 §B.5.3) | Wear-time NI breach → K-J4-4 |
| Binaural timing corruption / localisation loss | 2 | Bench-measurable | HP-J1-3 sync spec; B6 (blank — HP-J3-2) gates bilateral bench | Localisation NI breach → halt bilateral arm |
| Adult-to-child transport failure | 2 | Named risk (maturation; HINT-C pointer via J2) | Stage gates; adult result files no child claim | Stage-2 <3 dB → K-J4-3 |
| Testability-exclusion bias | 2 | Named risk (J2 BKB-SIN pointer) | Run-in testability printed per stratum; ITT denominators | Below freeze floor → coverage FAIL filed, G6 INSUFFICIENT |
| Comparator mis-specification (SCAN 2 state ≠ labeled use) | 2 | Design risk (age gating, J2 §2.1) | Per-user feature-state file HP-J2-2, audited pre-analysis | Unfileable state → excluded from primary, counted |
| Output level-creep vs residual acoustic hearing | 3 | Bench-measurable | MAP unchanged; B8 on every condition | Any over-MAP sample → desk-kill |
| False reassurance / delayed standard care | 2 | Design risk | Standard care continues both arms; J4 never delays CI/mapping/EI | Attributable delay = process FAIL |
| Device failure/revision; MRI | 1 | = C-J2 hardware | Software rollback ≤1 session, bench pre-tested (B10) | Rollback failure → halt build |
| Anesthesia/meningitis/facial/CSF/vestibular/surgical RH loss; charge/thermal/phototoxic injury; AAV immunity/shedding; opsin; neurotrophin misrouting/tumor; reprogramming off-fate/tumor; nerve injury/migration; elution depletion; genomic mis-triage/VUS; binaural deprivation from delayed second ear | — | NA with reason: no surgery, no biology, no new charge regime, no sequencing, no ear-sequencing decision | Charge/phase = C-J2 MAP, bench-verified; bilateral same-arm rule (§6.2) | — |

## 9. Kill criteria (proposed; human-ratified pre-scoring — all unevaluated)

- **K-J4-0 (desk, new):** §2.5 audit fails — any
  future-frame path (padding, norm statistic,
  centred feature, bidirectional/attention module)
  or suffix-replay Δ > 0 ⇒ build desk-killed before
  the bench. Flag-flip repair (`causal=True` on
  noncausal weights) is not a repair (Gen 9).
- **K1 (inherited J2/J3):** Stage 0 cannot file
  J4-A1 meeting B1–B10 on H-primary from *measured*
  records (§3 T0 numbers are inadmissible here).
- **K-J4-2 (adult bridge):** Stage 1 primary SRT
  advantage vs SCAN 2 (C-J2) **< 3 dB**, or CI
  failing the §6.1 precision rule at locked N ⇒
  no pediatric stage exists.
- **K-J4-3 (pediatric):** Stage 2 Band A < 3 dB
  vs C-J2 under the same precision rule ⇒ J4 and
  the J-lineage front-end claim in this form
  retire (J2 K3 carried; re-powering after seeing
  the estimate barred).
- **K-J4-4 (NI bundle, any stage):** quiet −5 pp,
  music, localisation, alarm-battery, or wear-time
  NI breach ⇒ kill/halt per §8 row.
Advance means only: next stage may be *frozen by
humans*. Nothing here promotes: joint G2–G6 PASS at
≥Moderate human-verified GRADE incl. a qualified
G3b (BLOCKED) is still required, so J4's strongest
honest outcome this generation is a buildable A1
spec with a T0 latency floor and pre-filed kills.

## 10. HOLDER-PINs

Carried, unchanged: **HP-J1-4** (fielding gate for
the whole J-lineage) · HP-J1-3 · HP-J2-1 · HP-J2-2 ·
HP-J2-3 · HP-J2-4 · HP-J2-5 · HP-J2-6 · HP-J3-1 ·
HP-J3-2 · HP-J3-3. New: **HP-J4-1** architecture
freeze (topology = LSTM-primary or NNSE-fallback,
one named; filterbank/`B`; norm choice §2.3; state-
reset/priming behaviour; dual-mic stratum Y/N) ·
**HP-J4-2** training freeze (mask target, loss,
corpora + licenses, talker/corpus/noise partition
incl. held-out class, SNR/level/reverb grid, seeds,
weights hash process) · **HP-J4-3** Stage-1 pilot
variance → locked N + analysis plan (Stage-2 N
remains HP-J2-6; filed before unblinded data).
Named humans H-1…H-8 PENDING as throughout.
Unpinned ⇒ INSUFFICIENT + no scoring, as ever.

## 11. Unresolved (named, not settled)

- Goehring 2019 end-to-end ms delay never stated in
  inspected text; J4's 8/4 budget is a new design
  point, and no inspected record measures an 8/4
  LSTM masker in any listener (cost of the §2.4
  retiming on SRT is **unknown**, decided only in
  Stage 1).
- Filterbank particulars of the Goehring records
  beyond Gen 9's extraction (band count/spacing)
  were not re-inspected this generation; `B=64` is
  PROPOSED, not inherited, and §3.4 compute scales
  with whatever HP-J4-1 pins.
- Whether a Nucleus-class processor sustains
  250 frames/s × 237,568 MAC (at `B=64`) inside B1's
  2.0 ms T0 headroom is a hardware measurement
  (K1), not inferable from MAC counts; H-primary
  access itself is an external dependency.
- Dual extraction/GRADE of the Goehring ledger rows
  remains human-owed (Gen 9 §3); until then they are
  design precedent, never scored evidence.
- Deep ACE padding/norm and Kang 2021 directionality
  stay UNVERIFIED (Gen 9 desk queue); J4 neither
  needs nor settles them.

## 12. Standing state

`promoted FALSE`. FROZEN retained. G3b BLOCKED.
Validation set 0. No candidate scored, no cell
moved, no weights trained, no bench run: Gen 10 J4
files the *spec* Gen 9 asked humans to choose,
priced at T0, gated by HP-J1-4 before it can even
reach the bench that could kill it.

*End. GEN10-J4 = GEN6-J2 + GEN7-J3 + M-J4-1 (named
Goehring-class A1). T0 latency floor 8.0 ms;
everything that matters is measured later or kills it.*
