# Step 0 verification — channels & development

> **Route (GOAL §9):** Sol 6.1 high (generation-execution worker).
> **Actual runtime model:** `muse-wonder-full-1.0` (fallback — Sol 6.1
> unavailable in this runtime; substitution disclosed here per §9 rule 3,
> not silently downgraded).
> **Verified date:** 2026-11-02. **Status:** agent pre-extraction only
> (GOAL §9) — human-led dual extraction on all load-bearing claims is
> still pending; nothing here is gate-deciding until a human extractor
> independently verifies it.
> **Method:** `web_search` to locate, then inspected full text /
> authoritative full records only: PubMed full abstracts via NCBI
> E-utilities (`efetch`, `db=pubmed`, abstract text), open-access journal
> full-text PDFs for the two Kral reviews (author-hosted publisher PDFs,
> text-extracted and read), and the *ENT & Audiology News* feature only
> as a pointer to the *Hearing Research* 2025 citation (then verified
> against PubMed + the journal PDF). Search snippets were never used as
> evidence. PMC HTML was reCAPTCHA-blocked on 2026-11-02; where a PMC
> full text could not be opened, the PubMed full abstract is the
> inspected record and that limit is stated per row.
> **Scope read first:** GOAL.md §1–§3, §8, §11, Appendix E (GOAL v2.2).

Verdicts: VERIFIED (claim matches inspected source) · CORRECTED (claim
needs the stated fix) · UNVERIFIABLE (not confirmable from inspected
full text; what was tried is stated) · REFUTED (inspected source
contradicts the claim).

---

## Summary table

| # | Claim as stated in GOAL.md | Verdict | Correct value (short) | ID |
|---|---|---|---|---|
| 1a | "Friesen, Shannon & Cruz 2001" (§1.2) supports ~4–10 effective channels | **CORRECTED** | Authors are Friesen, Shannon, **Baskent & Wang** (no Cruz). CI performance rose to 7–8 electrodes (vowels/consonants plateau ≤7; words/sentences marginal 7→10 in one device group; low performers no gain beyond 4). NH vocoder listeners kept improving to ≥20 channels. "4–10" is a defensible gloss of the CI range, not a number the paper states | PMID 11519582; DOI 10.1121/1.1381538 |
| 1b | "and successors; vocoder and spread-of-excitation work" support 4–10 range (§1.2, §3.4, §4.2 G1 point anchor 8) | **CORRECTED** | Later perimodiolar work finds gains **beyond 8** (to 16 channels/maxima) in well-placed modern arrays — the 4–10 / point-8 anchor is device- and task-dependent and cannot be cited as a settled ceiling | PMID 31067952 (Berg et al. 2019) |
| 2 | "Two decades of current focusing (tripolar, phased array) narrowed spread at higher charge cost *without durable speech-in-noise translation*" (§1.2) | **CORRECTED** (direction right, absolute wording wrong) | Focusing does narrow spread and costs more total current / battery. Speech-in-noise results are **mixed, not uniformly absent**: one acute partial-tripolar study found +2.7 to +3 dB SRT benefit; later take-home / dynamic-focusing trials found no consistent group speech-in-noise benefit. "Without durable translation" is supportable only if "durable" = take-home/clinical adoption; as written it erases a positive acute result | PMID 17552721; 23467170; 27317668; 36279119; 37226501 |
| 3 | "Kral et al. *Trends Neurosci* 2023" (App. E; §8H "Kral-consistent" visual-language hypothesis; §11 "Kral 2023") | **CORRECTED** | The 2023 paper is Kral & Sharma, *Crossmodal plasticity in hearing loss* — a **crossmodal-plasticity review, not a sensitive-period paper**. It argues crossmodal reorganization does **not** close critical periods, is reversible/dynamic, and does not harm preconditions for restoration — which does support §8H. The Kral sensitive-period review is **Kral & Sharma 2012**, *Trends Neurosci* | PMID 36990952 (2023); PMID 22104561 (2012) |
| 4 | "*Hearing Research* 2025 nine-months paper" (§11, App. E) | **VERIFIED** (paper identified; see content caveat) | Kral, Kishon-Rabin, O'Donoghue & Romeo, *Sensorimotor contingencies in congenital hearing loss: The critical first nine months*, Hear Res 2025;467:109401. It is a **narrative review/proposal**, not a trial: it proposes first-year (framed as first-nine-months) sensorimotor synchrony as critical, while still citing a ~3-year critical period for therapy. Any GOAL use as causal proof for a 9-month deadline would overstate it | PMID 40907462; DOI 10.1016/j.heares.2025.109401 |
| 5 | "'~3.5 years' is a P1-derived heuristic, not a universal deadline" (§1.2; origin: Sharma et al) | **VERIFIED** | Origin is Sharma, Dorman & Spahr 2002 (Ear Hear): P1 CAEP latency normalized within ~6 mo when deprivation was ≲3.5 y; variable plasticity to ~7 y; greatly reduced after 7 y. A P1-latency finding in congenitally deaf CI children — correctly described in GOAL as a heuristic, not a language deadline | PMID 12476090; follow-up PMID 15855038 |

No claim below was left UNVERIFIABLE or REFUTED outright; the
corrections in 1a, 1b, 2 and 3 are load-bearing for GOAL §4.2 G1,
§8 Family A, and §8 Family H respectively and are detailed in full.

---

## 1. Friesen et al. 2001 — channels (GOAL §1.2, §3.4, §4.2 G1, App. E)

**Claim as stated:** "primary psychophysics (Friesen, Shannon & Cruz
2001 and successors; vocoder and spread-of-excitation work) supports
roughly 4–10 *effective* spectral channels for speech tasks, varying by
listener/task" (§1.2). Frozen baseline repeats "G1 effective channels
4–10" (§3.4) with a point anchor of 8 (§4.2).

### 1a. Exact citation and what was actually shown — CORRECTED

- **Correct citation:** Friesen LM, Shannon RV, **Baskent D, Wang X**.
  Speech recognition in noise as a function of the number of spectral
  channels: comparison of acoustic hearing and cochlear implants.
  *J Acoust Soc Am*. 2001 Aug;110(2):1150–1163.
  **DOI 10.1121/1.1381538 · PMID 11519582.**
  There is **no author named Cruz** on this paper. GOAL's
  "Friesen, Shannon & Cruz" must be corrected wherever it appears.
- **Design (inspected: PubMed full abstract, PMID 11519582):**
  speech recognition (vowel, consonant, word, sentence) as a function
  of number of spectral channels (noise bands for acoustic hearing;
  electrodes for CI) at SNRs of +15, +10, +5, 0 dB and in quiet.
  **N = 5** normal-hearing (NH) listeners (noise-band vocoder),
  **N = 10** Nucleus-22 CI listeners, **N = 9** Advanced Bionics
  Clarion CI listeners. Three speech-processing strategies (SPEAK,
  CIS, SAS) performed similarly.
- **What channel counts were actually shown:**
  - CI listeners: performance "improved as the number of electrodes
    increased (**up to seven or eight**) for all conditions."
  - Vowel/consonant recognition (SPEAK) "did not improve with more
    than **seven** electrodes" at any noise level.
  - Word/sentence recognition: only a "**marginally significant**"
    increase from **seven to ten** electrodes, and only in the
    Nucleus-22 group.
  - Best CI listeners improved up to **seven** electrodes; low
    performers "did not increase in performance as the number of
    electrodes was increased beyond **four**."
  - NH vocoder listeners: performance "continued to increase up to
    **at least 20 channels**" — i.e. the vocoder arm does **not**
    support a 4–10 ceiling; it shows the acoustic system can use far
    more spectral channels than these CI listeners could.
  - Authors' conclusion: "most CI subjects are not able to fully
    utilize the spectral information provided by the number of
    electrodes used in their implant."
- **Locator:** PubMed abstract, Results sentences quoted above
  (PMID 11519582). Journal full text (JASA 110:1150–1163) was not
  open-access on 2026-11-02; no number in this row comes from beyond
  the abstract, and none is needed to correct the author list or the
  channel counts, which the abstract states explicitly.
- **Assessment for GOAL:** "roughly 4–10 effective channels" is a
  *fair gloss* of the span between the low-performer plateau (~4) and
  the marginal word/sentence gain (7→10) in these 2001-era devices,
  but the paper itself never states "4–10 effective channels," and
  its headline CI plateau is **7–8**. GOAL should cite it as
  "plateau at ~7–8 electrodes for most speech materials in 2001-era
  arrays (range across listeners/materials ~4 to a marginal 10)"
  rather than as a direct measurement of "4–10 effective channels."

### 1b. Successor evidence for a 4–10 range — CORRECTED

- **Inspected successor:** Berg KA et al. Speech recognition as a
  function of the number of channels in perimodiolar electrode
  recipients. *J Acoust Soc Am*. 2019 Mar;145(3):1556.
  **DOI 10.1121/1.5092350 · PMID 31067952 · PMCID PMC6435372**
  (PMC HTML reCAPTCHA-blocked 2026-11-02; PubMed full abstract
  inspected).
- **Design:** **N = 30** adult CI recipients with perimodiolar arrays
  imaging-verified entirely in scala tympani; CIS with 4, 8, 10, 16
  channels and n-of-m with 16 maxima; monosyllables, sentences in
  quiet and at +5 dB SNR, vowels, consonants, spectral modulation
  detection, sound quality.
- **Findings (abstract, numbered results):** significant gains for
  speech in quiet with **16 vs 8**-channel CIS; 16-of-m significantly
  better than 8- and 10-channel CIS across monosyllables, sentences
  (quiet and noise), consonants, spectral modulation and quality;
  benefit of 16 vs 8 maxima inversely correlated with
  electrode-to-modiolus distance. Authors: these data "demonstrate
  greater channel independence with perimodiolar electrode arrays as
  compared to previous studies with straight electrodes."
- **Assessment for GOAL:** successor evidence **does not** support
  treating 4–10 (or the §4.2 point anchor of 8) as a device-general
  ceiling. With modern perimodiolar placement, adult listeners can
  exploit more than 8–10 channels/maxima on several speech tasks.
  The frozen-baseline G1 anchor (point 8, PASS ≥12 Track P / ≥16
  Track R) therefore needs Step 1 to state explicitly which array
  type, task, and maxima-vs-channels definition the "8" refers to —
  otherwise a contemporary perimodiolar standard device could
  approach the Track P PASS bar on the anchor task, and the
  "sensitivity at 4 and 10" (§4.2) would not capture that. This row
  does **not** refute current-spread limits; it refutes citing
  Friesen 2001 + "successors" as if successors uniformly confirm
  4–10.

---

## 2. Current focusing (tripolar / phased array) — GOAL §1.2, §8 Family A

**Claim as stated:** "Two decades of current focusing (tripolar,
phased array) narrowed spread at higher charge cost *without durable
speech-in-noise translation* — any new focusing claim must explain
that failure (§8, Family A)."

**Verdict: CORRECTED.** The physics half (narrower spread, higher
current/charge cost) is verified. The outcome half is too absolute:
acute laboratory speech-in-noise benefit **has** been reported; what
has not materialized is *consistent* benefit in take-home /
group-level testing or clinical adoption. GOAL's kill-criterion
framing for Family A survives, but the premise sentence should read
"without **consistent** speech-in-noise translation in take-home
testing" and must acknowledge the positive acute result it asks
challengers to explain.

### 2a. Narrowed spread + charge cost — VERIFIED

- **Phased array (origination):** van den Honert C, Kelsall DC.
  Focused intracochlear electric stimulation with phased array
  channels. *J Acoust Soc Am*. 2007 Jun;121(6):3703–3716.
  **DOI 10.1121/1.2722047 · PMID 17552721.** Method/validation in
  **N = 3** human subjects with 22-electrode perimodiolar arrays.
  Abstract results: "(1) focusing is realizable with realistic
  precision; **(2) focusing comes at the cost of increased total
  stimulation current**; (3) uncanceled voltages beyond the array
  ends are weak except at the two end channels; (4) close
  perimodiolar positioning may be important for minimizing
  stimulation current." Channel interaction from monopolar current
  spread was "substantially eliminated" *in the voltage-cancellation
  sense measured*, not in a speech-outcome sense — this paper has
  **no speech-perception endpoint**.
- **Tripolar spread reduction:** Srinivasan et al. 2013 (below),
  abstract: "partial tripolar stimulation has been shown to reduce
  spread of excitation relative to monopolar stimulation" (citing
  prior work; the claim is presented as established background, and
  the study's question is whether it translates to speech).
- **Charge/battery cost quantified in a take-home trial:**
  van Groesen et al. 2023 (below): dynamic current focusing
  "**reduced average battery life by 48% (5.1 hours)** (p < 0.001)
  compared to MP" — the clearest inspected quantification of the
  "higher charge cost" clause.

### 2b. Speech-in-noise outcomes — MIXED (GOAL wording corrected)

| Study (inspected PubMed full abstract) | N + design | Speech-in-noise result |
|---|---|---|
| Srinivasan AG, Padilla M, Shannon RV, Landsberger DM. *Hear Res* 2013;299:29–36. DOI 10.1016/j.heares.2013.02.004 · **PMID 23467170** · PMCID PMC3639477 | Adult CI users (abstract does not state N — **not invented here**; PMC full text reCAPTCHA-blocked 2026-11-02, so N is UNVERIFIED from inspected text); acute lab comparison of experimental monopolar vs partial-tripolar strategies matched on electrodes, filterbanks, rate, loudness (both at lower rate than clinical) | **Positive:** "significant improvement in speech perception in noise with partial tripolar stimulation. All subjects benefited… mean improvement in speech recognition threshold of **2.7 dB** (digits in noise) and **3 dB** (sentences in noise)." Caveat in abstract: experimental monopolar was worse than clinical strategy; partial-tripolar showed "no acute deficit relative to the clinical" — i.e. the +3 dB is vs a degraded experimental monopolar comparator, not vs the clinical map |
| Bierer JA, Litvak L. *Trends Hear* 2016;20:2331216516653389. DOI 10.1177/2331216516653389 · **PMID 27317668** | **9 ears in 8** adult Advanced Bionics HiRes90k listeners; 6 experimental programs (14-ch partial tripolar vs monopolar ± channel deactivation); vowel/consonant identification (not speech-in-noise SRT) | **Null at group level:** "Across subjects, performance was similar with pTP and MP programs." Poorer performers (<62% vowel ID) "tended to perform better" with all-channel pTP and with reduced-channel MP. Conclusion: reducing channel interaction "**may** benefit poorer performing CI listeners" |
| van Groesen NRA et al. *Ear Hear* 2023;44(2):306–317. DOI 10.1097/AUD.0000000000001282 · **PMID 36279119** | **13 fitted, 9 completed**; single-blinded within-subject crossover **take-home** trial, dynamic current focusing (DCF, dynamic partial tripolar) vs monopolar, 3-week adaptation periods; matrix sentence-in-noise test, spectral ripple (SMRT/STRIPES), SSQ | **Null for speech-in-noise:** "No significant differences… on speech-in-noise recognition at conversational (65 dB) and soft (45 dB) levels." SMRT +0.40 ripples/octave at 65 dB (p = 0.02, **ns after Bonferroni**). Authors: "considering previous studies, **DCF does not consistently improve speech recognition in noise over MP**" |
| Caswell-Midwinter B, Arenberg JG. *Trends Hear* 2023;27:23312165231176157. DOI 10.1177/23312165231176157 · **PMID 37226501** | **14 ears**, implanted adults; 14-channel dynamic-focusing (fixed vs individualized K) vs monopolar, matched pulse parameters/loudness; sentences + vowels in quiet and 4-talker babble | **Null at group level, individual benefit:** "speech recognition in quiet and noise was similar between strategies" at group level; some individuals benefited in noise, pattern "generally unclear" beyond associations with focused thresholds and duration of hearing loss. Opening line: "Results on the speech perception benefits of these strategies have been **mixed**" |

- **No clinical translation endpoint was inspected** (no FDA label /
  ClinicalTrials.gov record for a tripolar or phased-array clinical
  strategy was retrieved in this pass). The statement "no durable
  clinical adoption" is therefore **UNVERIFIABLE from inspected
  records here** — it is consistent with the take-home nulls above
  but a registry/label search is still owed before GOAL asserts it
  as fact. What was tried: PubMed E-utilities searches for focusing
  systematic reviews and take-home trials (2026-11-02); no
  ClinicalTrials.gov query was run in this worker's scope.
- **Net correction for Family A:** a new focusing claim must explain
  three things, not one "failure": (i) why the acute +2.7/+3 dB SRT
  benefit (Srinivasan 2013, vs a non-clinical comparator) did not
  reproduce as a group effect in take-home testing (van Groesen
  2023, N = 9 completers — itself small); (ii) the ~48% battery-life
  cost; (iii) why benefit, when present, concentrates in poorer
  performers / specific electrode-neuron interfaces (Bierer &
  Litvak 2016; Caswell-Midwinter & Arenberg 2023).

---

## 3. Kral et al., *Trends in Neurosciences* 2023 — CORRECTED

**Claim as stated:** Appendix E lists "Kral et al. *Trends Neurosci*
2023" among anchors; §11 Step 0 lists "Kral 2023"; §8 Family H states
"Hypothesis (Kral-consistent): visual language supports language
development without harming auditory outcomes." §1.2's
graded-sensitive-period paragraph carries no citation in-text but is
the claim cluster this anchor is presumably meant to support.

- **Exact 2023 citation (verified):** Kral A, Sharma A. Crossmodal
  plasticity in hearing loss. *Trends Neurosci*. 2023
  May;46(5):377–393. **DOI 10.1016/j.tins.2023.02.004 ·
  PMID 36990952 · PMCID PMC10121905.** Two authors ("Kral et al." is
  loose but not wrong in substance; "Kral & Sharma 2023" is exact).
  Design: narrative **review** (no new data, no N).
- **What it actually claims (inspected: PubMed full abstract +
  open-access publisher PDF, pp. 377–378 Highlights/Introduction):**
  - Crossmodal reorganization "has significant limits, is dependent
    on pre-existing circuitry and top-down interactions, and…
    extensive reorganization is often absent."
  - "The evidence does **not** support the hypothesis that
    crossmodal reorganization is responsible for **closing critical
    periods** in deafness"; crossmodal plasticity is "dynamically
    adaptable," begins as early as mild–moderate loss, and shows
    "reversibility when hearing is restored."
  - "Crossmodal plasticity does not appear to affect the neuronal
    preconditions for successful hearing restoration."
  - Full-text Introduction (p. 377): the traditional recommendation
    "not to use visual communication (sign language) before cochlear
    implantation" rested on a massive-takeover concept that "is not
    consistent with recent findings and requires modification";
    crossmodal reorganization is argued to be "not detrimental for
    neurosensory restoration; instead, it is compensatory."
- **What it is not:** it is **not** the Kral sensitive-period paper
  and does not itself establish sensitive-period gradients, a ~3.5 y
  or ~3 y window, or language-outcome timing claims. Citing "Kral
  2023" for §1.2's sensitive-period gradient claims would be a
  mis-citation.
- **Correct Kral sensitive-period citation:** Kral A, Sharma A.
  Developmental neuroplasticity after cochlear implantation.
  *Trends Neurosci*. 2012 Feb;35(2):111–122.
  **DOI 10.1016/j.tins.2011.09.004 · PMID 22104561 ·
  PMCID PMC3561718.** Review discussing "time limits for, and
  mechanistic constraints on, sensitive periods for cochlear
  implantation" in congenitally deaf animals and children (PubMed
  full abstract inspected). If GOAL wants a Kral anchor for
  sensitive periods, this is it — still a review, not primary data.
- **Assessment for §8H:** the "(Kral-consistent)" tag on Family H is
  **supported** by the actual 2023 paper: visual communication before
  CI is not shown to harm restoration preconditions, per this
  review. But GOAL should cite it as what it is — a crossmodal-
  plasticity review arguing *against* the takeover-closes-the-window
  hypothesis — and must not let "Kral-consistent" smuggle in
  sensitive-period causal claims the 2023 paper does not make.
  GOAL §1.2's own framing ("graded-sensitive, not cliff-edged") is
  *compatible* with Kral & Sharma 2023's anti-cliff argument about
  crossmodal closure specifically; it is not *derived* from it.

---

## 4. *Hearing Research* 2025 "nine-months" paper — VERIFIED (identified)

**Claim as stated:** "*Hearing Research* 2025 nine-months paper"
(§11 Step 0 list; Appendix E anchor). GOAL text does not attribute a
specific numeric finding to it beyond the W0 (0–9 mo) window framing
in §1.2/§3.3, where W0 benefit is explicitly labeled "a hypothesis to
test, not a premise."

- **Exact paper (verified against PubMed record + open-access
  journal PDF):** Kral A, Kishon-Rabin L, O'Donoghue GM, Romeo RR.
  Sensorimotor contingencies in congenital hearing loss: The
  critical first nine months. *Hear Res*. 2025 Nov;467:109401.
  **DOI 10.1016/j.heares.2025.109401 · PMID 40907462.**
  Received 29 Apr 2025; accepted 11 Aug 2025; available online
  13 Aug 2025; CC BY open access. (Located via the citation in
  Král & O'Donoghue's *ENT & Audiology News* feature "The first
  nine months," 7 Jan 2026, ref 1 — used as a pointer only.)
- **Design:** **Review Article** (14 pp., journal PDF inspected,
  pp. 1–3 + Summary). No new cohort, no N, no trial. It does report
  one descriptive analysis: manufacturer sales data (11 countries,
  2017–2023) showing <20% of children implanted within the first
  3 years received the CI in the first year (Fig. 1A/B; one-way
  ANOVA F(6,68) = 0.39, p = 0.88 for change over time) — a
  practice-pattern statistic, not an outcome effect.
- **What it actually claims (Summary, p. 1, verbatim substance):**
  hearing/language acquisition is "well-possible within an early
  critical period of **3 years**, however, the earlier the access to
  sound is provided, the better outcomes can be expected"; some
  consequences of first-year deprivation are exacerbated when
  auditory development desynchronizes from other sensory/motor
  systems (sensorimotor contingencies); authors "**propose** that
  the first year includes critical developmental steps" for
  connectivity of language/cognitive networks. Introduction (p. 1)
  notes FDA minimum CI ages of 9–12 months (citing Lieu et al.
  2020) as a contributor to typical implantation in year 2–3, and
  that "effective hearing restoration before 9–12 months" has been
  shown beneficial in cited prior studies.
- **Assessment for GOAL:** the paper exists and is correctly
  identified — verdict VERIFIED on identity. But its evidentiary
  weight is that of an expert **proposal/review**: the "critical
  first nine months" is the authors' framing hypothesis built on
  sensorimotor-synchrony reasoning, explicitly coexisting with a
  ~3-year therapy critical period in the same abstract. GOAL's
  current usage (W0 causal benefit = hypothesis to test, §1.2/§8F/H)
  is the correct weight. It must not be upgraded in Step 1 to
  evidence *that* intervention before 9 months causally preserves
  cortex or improves language; the inspected text contains no such
  primary result.

---

## 5. P1 CAEP ~3.5-year heuristic origin (Sharma et al.) — VERIFIED

**Claim as stated:** "'~3.5 years' is a P1-derived heuristic, not a
universal deadline" (§1.2, point 3); Appendix E / §5.3 treat P1 CAEP
as a mechanism/surrogate measure, never a sole G3 pass.

- **Origin paper (exact):** Sharma A, Dorman MF, Spahr AJ. A
  sensitive period for the development of the central auditory
  system in children with cochlear implants: implications for age of
  implantation. *Ear Hear*. 2002 Dec;23(6):532–539.
  **DOI 10.1097/00003446-200212000-00004 · PMID 12476090.**
- **Design (PubMed full abstract inspected):** P1 cortical auditory
  evoked potential (CAEP) latency vs age-matched normal-hearing
  peers; **N = 104** congenitally deaf children implanted at ages
  1.3–17.5 y plus **3** congenitally deaf adults; independent
  variable = duration of deafness before implantation.
- **Findings:** children with ≲**3.5 y** of deprivation "evidenced
  age-appropriate latency responses within 6 mo after the onset of
  electrical stimulation"; children with ≥7 y of deprivation had
  abnormal cortical response latencies to speech. Conclusions:
  "a sensitive period of about 3.5 yr during which the human
  central auditory system remains maximally plastic. Plasticity
  remains in some, but not all children until approximately age 7.
  After age 7, plasticity is greatly reduced."
- **Longitudinal follow-up using the same cutoffs:** Sharma A,
  Dorman MF, Kral A. The influence of a sensitive period on central
  auditory development in children with unilateral and bilateral
  cochlear implants. *Hear Res*. 2005 May;203(1-2):134–143.
  **DOI 10.1016/j.heares.2004.12.010 · PMID 15855038.**
  **N = 21** unilateral + **2** bilateral CI children implanted
  before 3.5 y or after 7 y (cutoffs explicitly "based on the
  sensitive period… described in [Ear Hear. 23(6), 532]"); early-
  implanted children showed rapid CAEP morphology/P1-latency
  development, late-implanted children aberrant morphology and
  slower P1 decreases; a child whose second ear was implanted
  after age 7 showed late-implanted-like responses in that ear.
- **Assessment for GOAL:** VERIFIED. The 3.5 y figure is a
  P1-latency normalization finding (cross-sectional in 2002,
  small-N longitudinal in 2005), with an explicit graded tail to
  ~7 y in the original conclusions — i.e. the source itself is
  graded, not cliff-edged. GOAL's "heuristic, not a universal
  deadline" and its §5.3 surrogate restrictions (P1 = mechanism
  measure, never sole G3 evidence) accurately reflect the source.
  Two cautions for Step 1: (i) P1 latency to speech sounds is not a
  language outcome — any W2/W3 language inference needs the §5.3
  proxy-chain validation GOAL already requires; (ii) the 2002
  cohort's earliest implantation age was 1.3 y, so the paper says
  nothing direct about a 0–9-month (W0) advantage.

---

## Unresolved / owed to human dual extraction

1. **Srinivasan et al. 2013 N** — not stated in the PubMed abstract;
   PMC full text (PMC3639477) was reCAPTCHA-blocked on 2026-11-02.
   Do not cite an N for this study until the full text is opened.
2. **Clinical-adoption status of focusing strategies** — no FDA
   label or ClinicalTrials.gov record was inspected in this pass;
   "no durable translation" as a regulatory/market fact remains
   UNVERIFIABLE here (separate from the verified take-home nulls).
3. **Friesen 2001 and Sharma 2002 journal full texts** — paywalled;
   all numbers above are from PubMed full abstracts, which state
   the load-bearing counts explicitly. Human extractor with journal
   access should confirm against full text (esp. Friesen channel
   sets tested per device, which the abstract does not enumerate).
4. **Spread-of-excitation primary sources** behind GOAL's
   "spread-of-excitation work" phrase were not individually pinned
   in this pass; Berg 2019 + the focusing set bound the claim, but
   Step 1's ripple-to-channels conversion model (§4.2) still needs
   its own cited sources — none were verified here.
5. All five claims remain **agent pre-extraction only**; per GOAL
   §9 a human extractor independent of the holder must verify
   before any of these values pin the frozen baseline or score a
   gate cell.
