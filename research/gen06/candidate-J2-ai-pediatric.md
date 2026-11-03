# Gen 6 Candidate J2 — DEEPEN J1: pediatric AI front-end take-home study vs a NAMED current commercial processor [Track P, G1-NA ruling still required]

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**, disclosed per §9
> rule 3. **Date: 2026-11-03. Gen 6 under GOAL v2.3**
> (no generation cap, no loop stop; PASS bar unchanged).
> Inputs: `gen05/Gen5-summary.md` §4 (push 2: HP-J1-4
> ruling; push 7: *a J1 pediatric take-home design if
> HP-J1-4 signs, benchmark = current commercial
> processor*); `gen05/candidate-J1-ai-frontend.md`
> (parent, read in full); `gen05/candidate-I1-gjb2-aav.md`
> + `gen05/candidate-P5-p4-deepened.md` (portfolio
> fences: J2 borrows no I/P effects); GOAL §§3–5, 10,
> App. A–C; `reviews/codex-unstick.md` §2 (new DESIGN
> inputs change what can be *designed*, never what has
> been *shown*; U2's comparator-definition warning is
> applied in §2 below) and §3A (readiness-to-study ≠
> evidence-of-benefit: J2 is filed strictly as the
> former). **Inspected records only; no invented data.
> G3b BLOCKED. Same PASS bar (≥Moderate human-verified
> GRADE + App. A tier). No PASS claimed; scores nothing.**
>
> **Fielding fence (unchanged from J1, restated so this
> file cannot be misread):** GEN5-J1 is *unfielded*
> pending the HP-J1-4 human ruling that G1 = NA for a
> denoiser-as-portfolio-component. **J2 inherits that
> fence in full.** Designing the pediatric study now is
> Gen 5 push 7's *conditional* design work; it fields
> nothing, enrols nobody, and earns no fitness. If
> HP-J1-4 denies NA, J1 and J2 are withdrawn together
> (a front-end that must pass a channel-count gate fails
> G1 by construction — J1 §1).

## 1. Parentage / single mutation

- **ID:** `GEN6-J2`. Track P portfolio component **iff**
  HP-J1-4 signs (as J1). Parent: **GEN5-J1 only**.
  Manifest: [`manifest-GEN6-J2.csv`](./manifest-GEN6-J2.csv)
  (declaration byte-identical in form to J1's: G1 `false`
  = NA-proposed; G2–G6 `true`).
- **Mutation M-J2-1 (the only change):** J1's two open
  placeholders — "*current commercial processor
  processing* (no inspected record exists, HP-J1-2)" and
  "future protocol: within-child crossover" — are
  replaced by (a) a **named, inspected comparator**
  (§2) and (b) a **staged, executable pediatric study**
  with frozen decision rules (§3): bench gate → adult
  bridge → pediatric take-home crossover → language-
  trajectory cohort. Mechanism, kill thresholds
  (≥3 dB / quiet NI / wear-time), FMEA harms, and every
  J1 HOLDER-PIN are inherited; what changes is that the
  comparator and the protocol are now specific enough
  to be wrong. Anti-rewording audit: J2 could not have
  been written from J1's text alone — it depends on
  manufacturer/FDA-facing records and one journal
  record (§2) that Gen 5 explicitly listed as owed
  (broaden-sweep §6 item 5).

## 2. What current commercial processors actually ship (inspected 2026-11-03) — and the named comparator

Rule applied (broaden-sweep §2.6 + codex-unstick §2/U2):
search snippets were pointers only; every feature below
was read on a manufacturer page or in a journal abstract
fetched in full. Where a source could not be text-
inspected, it is labeled pointer-only and **not** used.

### 2.1 Cochlear (PRIMARY comparator source — fully inspected)

- Current external processors: **Nucleus 8** (BTE) and
  **Kanso 3** (off-ear); the 2025 FDA-approved **Nucleus
  Nexa** system ships as Nucleus 8 Nexa / Kanso 3 Nexa
  processors carrying, per Cochlear's own launch record,
  "all the innovative features introduced with the
  Nucleus 8 Sound Processor, including SmartSound iQ 2
  with SCAN 2 and automated ForwardFocus" (Cochlear
  ProNews launch article, 2025-07-08, inspected).
- Shipped front-end, as described on Cochlear's Nucleus
  upgrade pages (inspected): **SmartSound iQ 2 with
  SCAN 2** (automatic scene classification + program
  adaptation, incl. **SNR-NR** single-microphone noise
  reduction and **WNR** wind-noise reduction) and
  **ForwardFocus** (dual-microphone spatial noise
  reduction favoring sound in front; automated within
  SCAN 2 on current processors).
- **Age gating printed by the manufacturer (load-bearing
  for §3):** SNR-NR, WNR and SCAN are approved/
  recommended for recipients **≥6 years** who can (1)
  complete objective speech-perception testing in quiet
  and noise and (2) report a preference for program
  settings. ForwardFocus "should only be activated for
  users **12 years and older** who are able to reliably
  provide feedback on sound quality…", with the printed
  caution that speech understanding may *decrease* with
  ForwardFocus in quiet (Cochlear upgrade page
  footnotes, inspected). Consequence: for most of W3
  (3.5–7 y), the *labeled-as-used* commercial front-end
  is **not** the full adult feature set. Any J2 contrast
  that quietly benchmarks a pediatric DNN against an
  adult-configured processor — or, inversely, claims a
  win against features the child could never have had
  switched on — is comparator drift in one of its two
  directions. §3 therefore defines the comparator
  *per age band, as enabled per label*, and files the
  exact feature state per child (HP-J2-2).
- Best inspected effect size for the shipped front-end:
  Nel et al., *Int J Audiol* 2026 (PMID **41046328**,
  abstract inspected; NCT05080283): prospective within-
  subject study, **20 adults** (>18 y, ≥6 mo CI
  experience), Nucleus 8 **SCAN 2 + automated
  ForwardFocus vs SCAN 2 alone**: SRT improved **4.3 dB**
  (S0Nrearhalf) and **4.2 dB** (S0N3), both p<0.001,
  plus take-home use with positive subjective ratings.
  **Allegiance:** all four authors are Cochlear Limited
  (abstract affiliation) ⇒ §5.2 one-level downgrade,
  non-inventor replication owed. **Tier T3, adult,
  manufacturer-run.** Its design value here is as (i)
  proof that a *within-subject, take-home* front-end
  crossover on this hardware is executable, and (ii) a
  warning: the shipped spatial-NR step alone is already
  worth ~4 dB in adults in rear/side-noise geometries —
  a DNN that merely re-implements "attenuate non-frontal
  sound" has no headroom left against this comparator.
  J2's hypothesis must therefore live where beamforming
  cannot: **co-located / diffuse multi-talker
  interference** (J1's mechanism; §2.4).
- Battery reference point (manufacturer, inspected):
  "all day hearing is defined as **16 hours**" (Kanso 3
  integrated battery footnote). Filed as the wear-time
  denominator convention, not as a performance claim.

### 2.2 MED-EL (secondary stratum source — inspected)

- Current BTE processor **SONNET 3** (+ RONDO 3 off-ear,
  same sound coding): **Automatic Sound Management 3.0
  (ASM 3.0) with "Adaptive Intelligence"** — automatic
  environment adaptation of volume/settings with
  background-noise reduction — plus **dual-microphone
  directionality** (focus front, reduce rear/side noise)
  and FineHearing coding (MED-EL SONNET 3 product +
  FAQ pages, inspected).
- Battery strata printed by the manufacturer (FAQ,
  inspected): up to **60 h** (2× 675 zinc-air), **17 h**
  (Rechargeable Max), **10 h** (Standard), **7 h**
  (Micro). Filed because it proves the §3 power point:
  on the smallest pediatric-plausible battery, the
  *existing* processor already budgets a 7-hour day —
  DNN compute headroom is a wear-time question before
  it is an accuracy question.
- No DNN source-separation / deep-denoising claim for a
  shipped MED-EL CI processor was found on the
  inspected manufacturer pages. Absence is bounded to
  those pages on this date; it is printed as
  "not found in inspected sources," never as proof of
  non-existence.

### 2.3 Advanced Bionics (pointer-only — NOT used as comparator evidence)

Marvel CI processors (**Naída CI M90** adult, **Sky CI
M90** pediatric) with AutoSense (Sky) OS scene
classification, ClearVoice, and UltraZoom/StereoZoom
beamforming are consistently *pointed to* by search
results, but the manufacturer PDFs fetched here were
image/binary documents that could not be text-inspected
in this environment (Sky CI M90 data sheet fetched,
1.97 MB PDF, no extractable text). Per the inspected-
records-only rule, **no AB feature, age indication, or
effect is asserted in this candidate.** Closing this
gap (IFU text inspection) is HP-J2-2 work. If HP-J2-2
cannot inspect an AB IFU, AB-hardware children are
excluded from J2's primary cohort rather than pooled
on pointer-level knowledge.

### 2.4 The research-DNN record J2 must beat *from* (full-text inspected)

- PMID **38853168** (*Sci Rep* 2024; PMC11163011 full
  text inspected for Gen 6): RNN + SepFormer single-
  microphone separation, **13 adult CI listeners**,
  offline-processed IEEE sentences in stationary (CCITT)
  and multi-talker (TTB) noise at fixed SNRs (test grid
  incl. 1 dB SNR conditions; 260 sentences = 20 × 13
  conditions). Findings as stated: both DNNs
  significantly improved intelligibility vs *unprocessed*
  mixtures — toward quiet levels in some conditions —
  with the advantage **larger in multi-talker than in
  stationary noise**; no overall quality loss on their
  clean-speech quality check. **Limits as stated in the
  paper itself (Discussion/Methods):** both models used
  **non-causal processing with access to future
  frames**; SepFormer inference took **~5× the signal
  duration** on a laptop CPU (MacBook Pro i7) — "not
  suitable for real-time applications such as a CI audio
  processor"; the delay budget for a real-time CI device
  "should be below about **10–20 ms**" to avoid
  disturbing speech production / audio-visual
  integration (their cited bound). No dB-SRT effect vs
  any commercial processor is reported; the contrast is
  DNN-vs-unprocessed, which §2.1 shows is no longer the
  clinically relevant zero.
- PMID **37030808** (*IEEE TBME* 2023; abstract
  inspected): Deep ACE — end-to-end DNN emitting a
  denoised electrodogram, "designed… without
  sacrificing processing latency" (design claim; **no
  latency in ms, no power figure, and no effect size in
  the inspected abstract**); highest intelligibility vs
  baseline algorithms in **8 CI users** (T3). Filed as
  the low-latency *architecture* precedent, not as
  latency evidence.
- **Net Gen 6 comparator conclusion (the sentence J1
  could not write):** *No inspected manufacturer record
  shows a shipped CI processor performing DNN
  multi-talker source separation.* What ships in 2026
  is scene classification + single-mic NR + spatial
  beamforming (age-gated). J2's real, falsifiable claim
  is therefore narrow and honest: **causal DNN
  separation adds ≥3 dB SRT in diffuse/co-located
  multi-talker noise, in children, on top of the named
  commercial front-end as labeled for their age — at
  ≤ filed latency and without wear-time loss.** Every
  wider claim ("AI beats current processors") is
  barred by this candidate's own §2.

### 2.5 Named comparator (binding for §3)

**C-J2 (primary): the child's own Cochlear Nucleus 8 /
Kanso 3 (incl. Nexa variants) running SmartSound iQ 2
with SCAN 2, feature state exactly as enabled for that
child's age band per §2.1 labeling** (SNR-NR/WNR/SCAN
only ≥6 y with testability + preference-report;
ForwardFocus automated state recorded, never assumed
on below 12 y), same implant, same MAP, same battery
type, within-child. **C-J2-M (secondary stratum,
reported separately, never pooled): MED-EL SONNET 3 /
RONDO 3, ASM 3.0 + dual-mic directionality as fitted.**
AB hardware: excluded from primary until HP-J2-2
inspects IFU text (§2.3). The GOAL deciding contrast
(`frozen_bilateral_eCI_v1`) is preserved by pre-filing,
per child, how C-J2 relates to frozen contents
(§3.4-style mapping at freeze; HP-J2-2): beating C-J2
is the J-lineage kill/advance question; any C0 language
additionally requires the frozen contrast and is
claim-capped as in J1 (beating only lagging care =
implementation gap, never a C0 win). Codex-unstick's
proposed Amendment C (concurrent-comparator reference)
is **proposed, not adopted** — J2 does not rely on it.

## 3. Appendix B — full specification

- **ID / track:** `GEN6-J2`, Track P portfolio component
  iff HP-J1-4 signs (G1 = NA proposed; §1 fence).
  Manifest: [`manifest-GEN6-J2.csv`](./manifest-GEN6-J2.csv).
- **Mechanism & target cells:** causal, single-/dual-
  microphone DNN source separation / deep denoising
  inserted *before* the processor's sound-coding stage
  (ACE-class coding, MAP, and charge per phase
  unchanged — J ≠ A, no Family-A evidence inherited,
  A1 stays UNEVALUABLE). No cells targeted; no biology
  touched. Intervention = investigational front-end
  **ON** vs named commercial front-end **C-J2** (§2.5),
  same hardware. Target talker rule (front / loudest /
  attended-stream heuristic + failure behavior when the
  rule is wrong) is part of the intervention definition
  and is frozen at HP-J2-3 — an underspecified target
  rule was J1's "wrong-talker selection" FMEA row and
  is a measured endpoint here, not a footnote.
- **Delivery route & dose/units:** software/firmware on
  the child's existing external processor (research
  build) or a body-worn research front-end *only* if
  its end-to-end latency/power are separately filed and
  its results are labeled non-transferable to on-
  processor claims (off-processor compute proving an
  accuracy point does not prove a deliverable product —
  the SepFormer lesson, §2.4). "Dose" = locked
  algorithm version (weights hash filed) × logged
  wear-time hrs/day (datalogging). **Latency/power
  budgets are Stage-0 bench gates, not aspirations:**
  end-to-end algorithmic + framing latency must be
  *measured* and filed (HP-J2-1) against the 10–20 ms
  disturbance bound cited in §2.4 (J2 pre-files the
  stricter working budget **≤10 ms**, human-ratifiable
  at freeze; the number is a design budget to be met
  by measurement, not a claim that any current model
  meets it); incremental current draw (mW) and battery-
  life delta on the child's actual battery type (cf.
  §2.1 16 h convention; §2.2 7–17 h strata) measured on
  bench + confirmed by take-home datalogs. Causal-only
  models are admissible; any look-ahead beyond the
  filed latency budget desk-kills the build.
- **Timing by window & decision origin:** deployable
  from first CI activation onward in principle (J1),
  but J2 *tests* where measurement is valid (§3 stages):
  bench (no humans) → adult bridge (T3, provisional
  only) → pediatric G2 cohort in **W3 (3.5–7 y)** with
  age-banded instruments → W2/W3 language-trajectory
  cohort for G3a. Decision origins 9/12 mo are
  inherited pathway facts; **no W0/W1 efficacy claim of
  any kind is filed** (infant windows are mechanism-
  chain only per App. A: CAEP/VRA/IT-MAIS, no PASS).
  Reversible at any point by reverting to C-J2
  (rollback ≤1 fitting session, pre-tested in Stage 0).
- **Model system / comparator:** C-J2 primary, C-J2-M
  secondary-separate (§2.5). Within-child crossover is
  the primary G2 design (child = unit; ear-level data
  clustered by child, §5.2). Held-out rule: algorithm
  training corpora, test sentences/noises, and any
  child whose data tuned the model are **design**
  material; validation = pre-registered test lists,
  noise corpora, and children unseen by tuning
  (partition by child and by corpus, filed at freeze).
  Adult-lab baselines from 2023–24 (unprocessed
  mixtures, CNN/RNN lab comparators) are explicitly
  **not** comparators anywhere in J2.
- **Eligibility by §3.2 stratum:** genotype/anatomy-
  agnostic in theory (all P0 CI users on C-J2/C-J2-M
  hardware); *testability* is the honest restriction
  and is reported as a stratum, never hidden:
  - **Band A (primary G2): age 6.0–7.0 y** (top of W3;
    also the first band where C-J2's SNR-NR/WNR/SCAN
    labeling and open-set sentence SRT testing coincide
    — §2.1). Requires ability to complete the filed
    SRT test in quiet + noise (a *measured* run-in
    criterion, with the excluded-for-testability count
    printed per stratum).
  - **Band B (secondary G2): age 4.0–<6.0 y**, closed-set
    / word-recognition-in-noise instruments only (App. A
    G2-W2-style cells: word recognition %, localization
    when testable). **No SRT PASS or kill is read from
    Band B**; it exists to measure direction, burden,
    wear-time, and alarm safety where open-set SRT is
    not age-valid.
  - **Band C (trajectory only): W2 entrants (2–3.5 y)**
    followed into W3 for G3a (IT-MAIS/LittlEARS + CDI →
    modality-matched language SS). No G2 claim.
  - ANSD / CND / malformation / syndromic / additional-
    disabilities: **included-and-stratified** (J1 rule);
    children who cannot perform a band's test contribute
    wear-time/safety/datalog cells and are never
    silently dropped from denominators (treatment-policy
    estimand, §4.3). Bilateral users: both processors
    run the same arm with the bilateral-synchronization
    spec of HP-J1-3 (interaural timing error measured
    on bench in Stage 0; asymmetric-arm wear is a
    protocol deviation). Bimodal (CI+HA) children:
    separate stratum (contralateral HA front-end state
    filed; DNN hearing-aid processing on the acoustic
    side is a different product class and is out of
    scope, cf. §2 — no hearing-aid DNN evidence is
    imported into a CI claim).
- **Age-valid SRT design (the measurement core):**
  GOAL App. A requires an age-valid SRT-in-noise test
  (closed/open-set per age) with the *exact* test named
  at Step 1/freeze. J2 pre-lists the candidate
  instruments and the selection rule; HP-J2-4 (humans)
  picks and pins one primary per band **before** any
  J2 data exist:
  - Band A primary candidates: a pediatric sentence-in-
    noise SRT with published child norms — **HINT-C**
    class (inspected pointer: Turkish HINT-C norms,
    PMID **36856533**, N=62 normal-hearing children
    6–12 y + 15 adults; filed only for its maturation
    finding — children did not reach adult-like
    hearing-in-noise performance until ~12 y, hence
    adult SRT effects may not be transported into W3)
    or **BKB-SIN SNR-50** class (inspected pointer:
    pediatric CI use in PMID **39379007**, where 13 of
    54 followed SSD children were capable of speech-in-
    noise testing — filed as a *testability-rate
    warning* for recruitment arithmetic, not as an
    effect estimate; its 3 dB on-vs-off figure is a
    different contrast on a different question and is
    not used anywhere in J2). US/English normative
    sources for the chosen test are HP-J2-4 inspection
    work; no norm, list-equivalency, or test–retest
    number is asserted here.
  - Geometry (frozen choice, from §2.1/§2.4 logic):
    primary SRT in **diffuse/co-located multi-talker
    babble** (the geometry where C-J2's beamformer has
    the least to offer and separation claims its
    advantage); secondary SRTs in **S0Nrearhalf /
    S0N3-style spatial babble** (the geometries where
    C-J2 is strongest — a DNN win that only appears
    after hamstringing the comparator's best geometry
    would be drift; J2 must show its primary win
    *without* losing the spatial secondaries beyond NI)
    and in **stationary speech-shaped noise**
    (specificity control: §2.4 predicts the smallest
    DNN increment there). Speech always from front
    (S0) for primary; target-talker-ambiguity
    conditions (two frontal talkers) are a filed
    secondary stress, scored for wrong-talker errors.
  - Procedure guards: adaptive SRT (SNR-50) with
    pre-filed list randomization, practice lists to
    plateau, blinded scoring of recorded responses,
    arm order randomized (AB/BA) with acclimatization
    take-home period before each lab endpoint (length
    filed at freeze; same length both arms), quiet
    co-primary measured every session (floor/ceiling
    rule per App. A: >20% at bound triggers the
    pre-stated alternative list/test). Lab SRT is the
    kill/advance readout; take-home datalogs +
    caregiver/child report are G6/G3b-adjacent
    *descriptive* cells (G3b stays BLOCKED — no
    autonomy claim is scored from them).
- **G1–G6 measurement plan (App. A cells):**
  - **G1 = NA (proposed)** — HP-J1-4 gate, §1. No
    channel claim; ripple/channel measures are not
    collected as G1 evidence. Bilateral timing is
    handled as a *safety/NI* measurement (G5/G2-
    localization), never repackaged as a G1 win.
  - **G2 (primary):** Band-A SRT-in-noise difference
    (J2 − C-J2) in primary geometry; **advance requires
    ≥3 dB** (App. A) *and* quiet NI (−5 pp) *and*
    spatial-secondary NI within filed margins.
    Band-B word-in-noise + localization RMS (App. A
    G2-W2 deltas: ≥10 pp / ≥10°, NI −5 pp / +5°) as
    secondary. Music (melody/pitch battery named at
    freeze, App. A ≥10 pp / NI −5 pp) secondary in
    Band A — separation artefacts are *expected* to
    threaten music first; a music NI breach with an SRT
    win is a filed harm pattern, not a PASS. Min tier
    T4 (adult Stage-1 = provisional only, never a G2
    PASS input).
  - **G3a:** Stage-3 trajectory cohort only:
    modality-matched language SS within stratum
    (+0.4 SD / NI −0.2 SD, W2/W3, T4). J2 states in
    advance that the crossover stages are **not**
    G3a-powered and file **no** language claim; G3a
    stays INSUFFICIENT until Stage 3 runs under its own
    freeze. Adult intelligibility (T3) + proxy chain
    yields at most a provisional signal (§5.3).
  - **G3b: BLOCKED.** Caregiver/child preference and
    wear-time are collected descriptively; no
    instrument, MCID, or autonomy inference is filed.
  - **G4:** no biology touched (stated as design fact,
    scored as a win nowhere — J1 rule). Residual
    acoustic hearing in EAS/bimodal strata: output
    limiting unchanged from C-J2 MAP (bench-verified,
    Stage 0); any level-creep from denoising gain is a
    Stage-0 fail.
  - **G5:** per-harm NI per FMEA (§4), incl. the two
    harms with dedicated test batteries: environmental/
    alarm-sound detection (filed sound set: smoke/CO
    alarm, caregiver call from behind, traffic cues —
    final set HP-J2-5 with stakeholder input) and
    localization NI.
  - **G6:** wear-time NI (hrs/day datalogged, both
    arms), battery-swap/charge events per day, fitting
    visits, exclusion-for-testability + exclusion-for-
    hardware rates by §3.2 stratum (coverage honesty:
    a front-end that only runs on one manufacturer's
    current processor covers only that stratum — App. D
    numerators still unpinned, no % asserted),
    disparity bound vs C-J2 usage as filed at freeze.
- **Staged protocol (each stage gates the next; stages
  are study-readiness units, not promotion steps —
  codex-unstick §3A distinction):**
  - **Stage 0 — bench/desk (no humans):** causal build
    meets filed latency (≤10 ms working budget) +
    power/battery-delta + bilateral-sync error +
    output-limiting checks on C-J2 hardware (or the
    build is desk-killed and Stages 1–3 do not exist).
    Objective intelligibility metrics on held-out
    corpora are reported as engineering data (T0),
    never as G2 evidence.
  - **Stage 1 — adult bridge (T3, provisional):**
    within-subject lab SRT (J2 vs C-J2, same geometries
    as §3) in experienced adult C-J2 users, replicating
    the *contrast* (not the result) of Nel et al.
    (PMID 41046328) with
    the arms J2 actually claims. Purpose: falsify
    cheaply. **Stage-1 kill: <3 dB primary-geometry
    advantage in adults ⇒ J2 does not proceed to
    children** (children are never spent on an effect
    adults cannot show; §10 staging spirit). Adult data
    file no pediatric claim.
  - **Stage 2 — pediatric take-home crossover (T4, the
    G2 decider):** Bands A+B, AB/BA randomized,
    acclimatization + lab endpoints per arm, datalogged
    wear-time, alarm battery, localization, music
    (Band A). Primary readout = Band-A primary-geometry
    SRT difference. Interim safety review after the
    first filed block of children (size at freeze) with
    stopping rules §4; no efficacy peeking outside the
    pre-filed analysis.
  - **Stage 3 — language-trajectory cohort (T4, G3a
    only if separately frozen):** Band-C entrants +
    Stage-2 graduates followed W2→W3 on the winning-or-
    standard front-end per clinical care; J2 files the
    *design slot* and the mediation assumption
    (SRT-in-noise gain → language gain) as **UNRESOLVED**
    until Stage 3 measures both in linked children
    (§5.3 chain requirement).
- **Power/precision:** **no N is asserted.** No
  pediatric within-child SRT-difference SD for this
  contrast exists in inspected records, so no power
  claim is filed (J1 rule retained). What is filed:
  the estimand (within-child mean SRT difference,
  treatment-policy: non-wear, arm refusal, and
  testability failure stay in denominators), the
  precision target form (95% CI for the difference must
  exclude both 0 and the <3 dB kill region to advance;
  a CI spanning the 3 dB line = INSUFFICIENT-precision,
  printed, not argued around), and the owed inputs
  (pilot/run-in SRT SD + testability rate per band —
  cf. the §3 testability warning — obtained under
  Stage-2 run-in or a separately frozen pilot, then N
  computed and locked before unblinded analysis).
  Nel et al. (PMID 41046328; N=20 adults, within-
  subject, 4.2–4.3 dB)
  is a feasibility pointer for the *design*, explicitly
  barred as a pediatric variance source.
- **Burden:** fitting/mapping visits as C-J2 + filed
  acclimatization/training sessions per arm (count,
  not invented hours, until Stage-1 measures them);
  daily charge/swap burden from datalogs; travel for
  lab SRT sessions reported per G6. Caregiver program-
  management burden must be **zero-added** by design
  (fully automatic arm switching by the study build;
  a front-end that needs a parent to select programs
  per environment has failed the pediatric burden test
  that C-J2's automation already passes — §2.1).
- **Regulatory:** device software change on a marketed
  processor (investigational build; class/IDE-equivalent
  route named at freeze per §10 checklist by humans).
  No surgery; adult-bridge-before-pediatric-decider
  staging as above; pediatric T4 still required for
  every infant/child claim. Off-label feature states
  (e.g., enabling ≥6 y/≥12 y-gated features below their
  labeled ages to "strengthen" the comparator) are
  **barred** unless the human protocol + ethics route
  explicitly authorizes and labels them as such.
- **FTO:** processor owners hold the deployment surface
  (J1); research-use flag only; model weights/corpora
  licenses filed at freeze. No design-around advice.
- **Exploratory-after-seen:** Y — after PMIDs 38853168
  (full text), 37030808, 41046328 (abstracts), and the
  §2 manufacturer pages, all inspected 2026-11-03.
  Validation = J2's own held-out children/corpora
  (above) or independent pediatric records; none exist
  yet. Validation set for the J-lineage remains **0**.

## 4. FMEA (App. C; J1 rows inherited, J2 staging rows marked ◆)

| Harm | Sev | Prob (tier) | Mitigation / G5 input | Stopping rule |
|---|---|---|---|---|
| Latency degrading AV synchrony / own-voice / speech production | 2 | Bench-measurable (Stage 0); 10–20 ms bound cited §2.4 | ≤10 ms filed budget; causal-only | Bench latency > budget → build desk-killed (no human exposure) |
| Separation artefacts / musical noise / wrong-talker selection | 2 | Unstated (T3 lab only) | Quiet NI + music NI + two-talker stress condition; target rule frozen HP-J2-3 | Quiet or music NI breach → kill (§5) |
| Suppression of alarms / environmental sounds (safety) | 3 | Unstated | Filed alarm-detection battery HP-J2-5, both arms, Bands A+B | Any missed-alarm signal vs C-J2 → halt arm, DSMB-equivalent review |
| Wear-time loss (battery/compute/heat) | 2 | Bench + datalog (Stages 0/2) | Battery-delta bench gate; wear-time NI (G6) | Wear-time NI breach → kill (§5) |
| Binaural timing corruption / localization loss | 2 | Bench-measurable | Bilateral-sync spec HP-J1-3; localization NI | Localization NI breach → halt bilateral arm |
| ◆ Adult-to-child transport failure (Stage-1 win, Stage-2 null) | 2 | Named risk (maturation, §3 HINT-C pointer) | Stage gates: adult result files no child claim | Stage-2 <3 dB → kill (§5); no Band-B/C rescue narrative |
| ◆ Testability exclusion bias (only "good testers" measured) | 2 | Named risk (§3 BKB-SIN pointer) | Run-in testability printed per stratum; treatment-policy denominators | Testability < freeze-filed floor in any §3.2 stratum → coverage FAIL filed, G6 INSUFFICIENT printed |
| ◆ Comparator mis-specification (feature state ≠ labeled use) | 2 | Design risk (§2.1 age gating) | Per-child feature-state file HP-J2-2; audit before analysis | Unfileable feature state → child excluded from primary, counted, never imputed |
| False reassurance / delayed standard care | 2 | Design risk | J2 never delays CI/mapping/EI; standard care continues both arms | Attributable delay = process FAIL |
| Output level-creep harming residual acoustic hearing (EAS/bimodal) | 3 | Bench-measurable | MAP/output limiting unchanged, Stage-0 verified | Any over-MAP output on bench → build desk-killed |
| Device failure/revision; MRI | 1 | = C-J2 hardware (no new implant) | Inherit frozen rates; software rollback always available | Rollback failure → halt study build |
| Anesthesia/meningitis/facial/CSF/vestibular/RH surgical loss; charge/thermal/photo; AAV; opsin; neurotrophin; reprogramming; nerve injury; elution; genomic | — | NA (no surgery, no biology, no new charge regime) with reason | Charge per phase = C-J2 MAP, bench-verified | — |

## 5. Kill criteria (proposed; human-ratified pre-scoring — all unevaluated)

**Kill J2 (and retire the J-lineage front-end claim in
this form) if any of:** (K1) Stage 0 cannot file a
causal build meeting latency/power/sync budgets on C-J2
hardware from *measured* bench records; (K2) Stage 1
adults show **<3 dB** primary-geometry SRT advantage
over C-J2; (K3) Stage 2 Band A shows **<3 dB** over
C-J2 (point estimate *or* CI failing the §3 precision
rule after the locked N — INSUFFICIENT-precision at
locked N kills the *design as powered*, and re-powering
after seeing the estimate is barred); (K4) quiet NI
(−5 pp), music NI, localization NI, alarm-battery, or
wear-time NI breach in any stage. **Advance** means
only: Stage 2 clears K3+K4 ⇒ Stage 3 may be frozen.
Nothing in J2 advances to promotion, which still
requires joint G2–G6 PASS at ≥Moderate human-verified
GRADE incl. a qualified G3b — **BLOCKED** — so the
strongest honest Gen 6 outcome for J2 is a G2 cell
moving from INSUFFICIENT to evidence-bearing. J1's
kills are subsumed (K2–K4); J1 itself is superseded as
the lineage's design of record if humans adopt J2,
and stands unretired if they do not.

## 6. HOLDER-PINs

Carried: **HP-J1-4 G1=NA ruling (fielding gate for the
whole J-lineage)** · HP-J1-3 bilateral-sync +
environmental-sound scope.
New: HP-J2-1 bench latency/power/sync measurement file
(named hardware, ms, mW, battery-hrs — measured, not
modeled) · HP-J2-2 comparator file (per-child C-J2
feature state vs labeling; C-J2↔frozen contents
mapping; AB IFU text inspection or AB exclusion
ratified) · HP-J2-3 target-talker rule + model/corpus
freeze (weights hash, held-out partition) · HP-J2-4
exact SRT/word/music tests per band + normative
sources + geometry lock (§3) · HP-J2-5 alarm-sound set
+ stopping-rule owners (named humans H-1…H-8 PENDING)
· HP-J2-6 Stage-2 locked N from pilot variance +
analysis plan (filed before unblinded data).
Unpinned ⇒ INSUFFICIENT + no scoring, as ever.

*End. GEN6-J2 = GEN5-J1 + M-J2-1 (named comparator +
staged pediatric protocol). Unfielded pending HP-J1-4.
G3b BLOCKED. FROZEN retained. Validation set 0.*
