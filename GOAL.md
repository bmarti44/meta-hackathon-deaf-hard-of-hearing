# GOAL: Preserve-first, higher-resolution hearing for congenital bilateral severe-to-profound SNHL

> **GOAL.md v2.1** (2026-11-02). Supersedes v1 (`e9d4050`) after
> Round 1 dual review (Gaps 68/100, Skeptical 57/100; see
> `reviews/round-1-scores.md`). Version history: §12.
> **Status:** Research goal and operating loop. Not medical advice.
> Literature, public-data, and in-silico research only. No output
> of this project can inform the care of any current infant,
> including the author's son (see timeline honesty, §1.4).

## Contents

1. Why this project exists · 2. Novel claim & prior art ·
3. Population & frozen baseline · 4. Gates (operationalized) ·
5. Evidence, inference & the ≥90% standard · 6. Costs & stresses ·
7. Evolutionary loop · 8. Gen 0 families & tracks ·
9. Execution, team & reproducibility · 10. Regulatory/ethics path ·
11. First steps & deliverables · 12. Governance & versions ·
Appendices A–E (gate tables, candidate template, FMEA,
epidemiology arithmetic, glossary)

## 1. Why this project exists

### 1.1 Motivation and conflict disclosure

My son was born with bilateral, sensorineural, severe-to-profound
hearing loss. I have a personal stake in this field and a natural
urgency bias toward near-term fixes. That bias is a *risk to this
project*, managed in §12 (independent judges, holder recusal from
scoring, no individual-care use). This project applies the research
loop used in `~/bufferright/business` to search for strategies that
beat the S&P 500 — frozen baseline, small pre-specified challenger
families, joint promotion gates, adversarial review, generations
that keep/recombine/mutate only survivors — to congenital deafness.
Business analogies are **design principles only** until their
operational equivalents are pinned (§5); analogy is not method.

### 1.2 Three colliding facts (each graded, none overstated)

1. **Gene therapy works for a small, precisely defined subset.**
   Lunsotogene parvec-cwha (Otarmeni) received FDA accelerated
   approval (April 2026) for severe-to-profound/profound SNHL with
   *molecularly confirmed biallelic OTOF variants*, preserved
   outer-hair-cell function, and *no prior CI in the treated ear*
   (label constraints — verify against the FDA label in Step 0).
   CHORD 24-week reports describe ~80% of an *evaluable set*
   reaching PTA ≤70 dB HL — still severe loss, small N, open-label,
   surrogate endpoint, confirmatory durability pending. Eligible
   U.S. incidence is on the order of tens of newborns/year.
   *Implication:* a program serving only *OTOF* leaves the large
   majority unserved — but the exact majority fraction must be
   computed, not asserted (Appendix D).
2. **Electrical CI resolution is limited by current spread.**
   Contemporary arrays have 12–24 contacts; primary psychophysics
   (Friesen, Shannon & Cruz 2001 and successors; vocoder and
   spread-of-excitation work) supports roughly 4–10 *effective*
   spectral channels for speech tasks, varying by listener/task.
   Two decades of current focusing (tripolar, phased array)
   narrowed spread at higher charge cost *without durable
   speech-in-noise translation* — any new focusing claim must
   explain that failure (§8, Family A). Moser-lab optical CI and
   Utah penetrating implants attack the same physics but have no
   infant human data (timelines: §8, §10).
3. **Development is graded-sensitive, not cliff-edged.**
   Earlier auditory access is associated with better language on
   average, with outcome-specific sensitive-period gradients
   (cortical P1 normalization fastest early; vocabulary/syntax
   longer) and large residual variance from etiology, additional
   disabilities, family environment, and intervention intensity.
   "~3.5 years" is a P1-derived heuristic, not a universal deadline.
   Whether any 0–9-month (W0) intervention *causally* preserves
   cortex and improves later language is a **hypothesis to test**
   (§8, Families F/H), not a premise.

### 1.3 The preservation dilemma is a question, not a premise

v1 asserted early CI may foreclose later gene/cell therapy.
Reviewers correctly flagged counterexamples: atraumatic /
hearing-preservation surgery, post-CI scala patency in many ears,
explants, contralateral-ear strategies. The only hard fact today
is a *label/trial exclusion* (prior CI in treated ear), which is
not proof of biological impossibility. **Gen 0 Question Q0**
therefore tests the premise itself with graded evidence (human
temporal-bone histopathology, post-CI AAV-delivery animal data,
label exclusions listed separately from biology). If Q0 finds
sequencing easily solves the dilemma, this project pivots to
optimizing sequencing (Family G) and says so.

### 1.4 Timeline honesty

Any novel device/biologic winner here needs adult-first feasibility,
pediatric staging, and long follow-up: realistically **10–15+ years**
to routine infant use, if ever. Children deaf today — including my
son — will be served by today's CI, hearing-preservation surgery,
rapid genetics, early intervention, and signed/spoken language
access. This project serves *future* cohorts and near-term care-
pathway choices (Families G/H/A-evolving-standard). Funders and
family readers must calibrate accordingly.

## 2. Novel claim & prior art (what is actually new)

### 2.1 Honest novelty statement

The mechanisms in §8 are **other groups' programs**. This project
claims no new molecule, opsin, or electrode. Its single falsifiable
contribution is a **sequencing-and-preservation decision system**:

> **Claim C0:** For incident congenital bilateral severe-to-profound
> SNHL, a pre-registered *triage pathway* — rapid genomic/anatomic
> stratification at decision time + hearing-preservation CI
> technique + explicitly preserved contralateral/future-therapy
> options + W0 language-access bridge, with biohybrid/high-channel
> challengers admitted only through joint gates — yields better
> joint outcomes (G2/G3/G4/G6, §4) than frozen bilateral CI alone,
> *without* requiring any single >30-channel device to exist.

PRESERVE (v1 "PRESERVE-30" — the "30" is retired as an identity;
see G1) is thus a **portfolio/triage claim**: different winners by
stratum, not one genotype-agnostic device for ≥80% of children.
If C0 fails, the project reports that and keeps the frozen baseline.

### 2.2 Prior-art map (owners, not strawmen)

| Element | Owning programs (illustrative; complete in Step 0) | Status for infants |
|---|---|---|
| Optical CI (opsin + μLED) | Moser / Göttingen; industry partners | Preclinical (rodent/gerbil); no human data |
| Penetrating ANI / ABI | Utah / Blackrock / MED-EL; NIH BRAIN | Bench + chronic cat; no human ANI data |
| Neurotrophin / bionic-ear delivery | UNSW (Pinyon et al. 2014 guinea pig); eluting-array groups | No human trial 2014–2026 (must be explained) |
| Hair-cell reprogramming | Multiple academic labs (ATOH1/GFI1/POU4F3) | Neonatal-mouse/organoid; mature-cochlea failure |
| *OTOF* AAV | Regeneron (approved); Lilly/Akouos, Sensorion, others | Approved subset only |
| Hearing-preservation CI | All major manufacturers; HEARRING; dexamethasone-eluting & ECochG/robotic insertion trials | **Evolving standard** — comparator, not novel challenger |
| Rapid genomic sequencing | NSIGHT/Project Baby Bear lineage; hearing-specific panels | Clinically available; pathway integration is the gap |

Step 0 (§11) must complete this table with trials, patents/FTO
flags, and exact citations before Gen 0 scoring. Anything already
in clinical trials is reclassified as *evolving standard* and
compared against, never claimed as this project's invention.

## 3. Population & frozen baseline

### 3.1 Operational population (denominator for all % claims)

**Incident population P0:** live-born infants in a defined
jurisdiction/year (default: U.S., year pinned in Step 1) with
*congenital bilateral* SNHL meeting **both**:

- **Severity:** better-ear threshold ≥70 dB HL equivalent averaged
  0.5–4 kHz. Pre-behavioral: click/toneburst ABR estimated HL with
  correction factors stated; behavioral (VRA/play audiometry) when
  developmentally available. Grading per WHO/ASHA categories cited
  in Step 1. Asymmetry >15 dB between ears flagged (still included;
  analyzed separately).
- **Congenital:** present at birth per newborn screening + diagnostic
  ABR ≤3 months (EHDI 1-3-6), OR prelingual onset ≤6 months with
  congenital etiology (genetic/cCMV/anatomic). Later-identified and
  progressive converters (EVA, cCMV progression) are *entry-time
  strata* (§3.3), not silently pooled into P0-at-birth.

**Exclusions from P0 primary analysis** (reported, never hidden):
conductive/mixed loss with normal bone conduction; transient ABR
failure resolving by 6 months. Children with additional
disabilities are **included** and stratified (they are ~30–40% of
the real population in many cohorts; exact fraction pinned Step 1).

Every percentage (eligible fraction, response fraction) must show
numerator, denominator (P0 or named sub-denominator), jurisdiction,
and era. v1's ">95%" / "~2%" / "≥80%" figures are **retired** until
recomputed in Appendix D from primary sources with ranges.

### 3.2 Mandatory strata (report every candidate in each or mark NA)

*Etiology (explanatory, when known):* *OTOF*; *GJB2/DFNB1*;
*SLC26A4*/EVA; congenital CMV; other monogenic (gene named);
unknown after defined workup (panel/exome scope + CMV testing
timing stated). *GJB2* fractions reported by ancestry/population.

*Phenotype/anatomy (eligibility-determining):* auditory neuropathy
spectrum disorder (ANSD: present OAE/CM, absent/abnormal ABR);
cochlear nerve deficiency/aplasia (MRI-graded); cochlear
malformations (common cavity, incomplete partition I–III, EVA);
normal anatomy. *Syndromic flags:* Usher, Pendred, CHARGE,
Waardenburg, Jervell & Lange-Nielsen, other/none.

*Host/developmental:* prematurity/NICU course; additional
disabilities (vision, motor, intellectual — named instruments);
progressive/fluctuating course.

*Decision-time (point-in-time; primary for pathway claims):*
information actually available at each decision origin (birth, 3,
6, 9, 12 months) — including *genotype pending / VUS / negative*
as explicit states with turnaround-time assumptions. Explanatory
(etiology-known) analyses are secondary. A candidate may not use
a 14-month genotype to justify a 6-month decision.

*Entry-time:* identified ≤3 mo / 3–9 mo / >9 mo; progressive
converters crossing ≥70 dB after W0. W0-window claims restricted
to children identifiable in W0.

*Context (G3 confounders, §4):* home language(s); communication
modality (signed / spoken / bimodal — family-chosen, time-varying);
EI intensity (hrs/week, provider type); SES/maternal education
proxy; distance to CI center. These are stratification/adjustment
variables, never exclusion criteria.

### 3.3 Developmental windows & horizons

Primary span birth–7 years in fixed windows: **W0** 0–9 mo,
**W1** 9–24 mo, **W2** 2–3.5 y, **W3** 3.5–7 y. Windows are one
causal chain in the same children, **not** independent bets
(§5 replaces v1 walk-forward counting). Long-horizon sensitivity
to adolescence (growth, revision, battery, late fibrosis, future-
therapy eligibility, FDA 15-year gene-therapy follow-up where
applicable) is mandatory for G4/G5/G6.

### 3.4 Frozen baseline `frozen_bilateral_eCI_v1` (coarse & pinnable)

Pinned at granularity literature can actually support (Step 1
publishes the table; no fabricated 4×6×6 precision):

- Bilateral (simultaneous or sequential ≤6 mo apart — proportion
  pinned) electrical CI, contemporary arrays (12–24 contacts,
  lateral-wall/perimodiolar mix pinned by era), envelope processing.
- Age at first implant: median + IQR pinned from cited cohort/registry
  (label minimums verified per device in Step 0; v1's "9–12 mo"
  treated as cohort descriptor, not universal label).
- Hearing-aid trial, mapping schedule, EI dose: defined ranges.
- **Frozen diagnostics/language contents (stated now, so C0 cannot
  win by definition):** standard etiologic workup as routinely
  ordered (targeted genetics incl. *GJB2* where ordered, CMV
  testing, imaging — *without* guaranteed rapid turnaround, without
  a pre-committed gene-therapy-first triage rule, and without a
  preserved-ear protocol); EI referral with family-chosen modality
  (spoken / signed / bimodal as actually received — dose and
  modality mix pinned Step 1, *not* assumed spoken-only and *not*
  assumed sign-free). Family G must therefore beat *this* workup on
  turnaround/triage consequences, and H must beat *this* EI mix on
  dose/timing — or C0 correctly vanishes into evolving standard.
  Evolving-standard elements (rapid sequencing where already
  routine, preservation arrays) are a **sensitivity comparator**;
  the deciding promotion comparator is `frozen_bilateral_eCI_v1`.
- Outcomes: published meta-analytic/registry estimates with ranges
  for G2/G3/G5; G1 effective channels 4–10 (task-dependent; point
  anchor in §4.2 G1).

**Comparator-drift rule:** if standard care materially changes
(new label age, dexamethasone-eluting array approval, etc.), the
holder + one independent co-approver (§12; holder never sole-approves
a re-freeze) may freeze `v2` — with changelog, re-baselined scores,
and v1 results preserved. Silent drift is forbidden; dated
assumptions are required because challenger timelines are long.

**Non-negotiable constraints:** paper-only (no experiments run
here); reversible/additive preferred; no patient data/secrets;
Deaf-community respect operationalized as scored outcomes (§4 G3b)
and stakeholder judging (§9), not disclaimer alone.

## 4. Gates (operationalized; two tracks)

### 4.1 Why two tracks (fixing v1's impossible joint gate)

v1 required every candidate to maximize channels *and* preserve
all biology. Reviewers showed high-channel mechanisms (penetrating,
intracochlear optics, scala neurite growth, AAV reprogramming)
inherently alter biology. v2 splits promotion:

- **Track P — Preserve-first (primary; C0 lives here).** Pathway /
  incremental-device / bridge candidates. Must pass G2–G6 with
  **G4 as a hard veto** and G1 as *functional-resolution gain*
  (may be modest). Families A (evolving-standard-aware), B, F, G, H.
- **Track R — Replace-first (watch-list until adult data).**
  High-channel mechanisms accepting permanent alteration. Scored
  on G1/G2/G5 with G4 *disclosed as knowingly traded*, never
  claimed as preservation. Cannot be promoted for infants until
  adult human feasibility exists (§10). Families C, E; D long-horizon.

A candidate declares its track at pre-registration. Track R wins
never count as Track P preservation evidence. This makes the gate
set *satisfiable by construction* while keeping the trade honest.

### 4.2 Gate definitions (summary; binding numbers in Appendix A)

Appendix A is normative: per gate × window it names measure,
instrument, unit, frozen reference (pinned Step 1), PASS delta /
MCID, non-inferiority (NI) margin, minimum evidence tier (§5),
and NA rules. Headlines (defaults to confirm/pin in Step 1 with
citations; changes after freeze = new protocol version):

- **G1 Functional resolution.** *Effective channel* = number of
  independently discriminable spectral places under a stated task.
  Electrical/optical/penetrating: spread-of-excitation width
  (mm/octaves) + spectral-ripple thresholds. Regenerative/bridge:
  pre-specified functional anchor (frequency discrimination / SRT
  benefit), never raw hair-cell counts. **Anchor task & point
  baseline (pre-Step 1):** spectral-ripple discrimination in adult
  CI users / vocoder listeners; frozen point = **8 effective
  channels** (midpoint of 4–10 range; sensitivity at 4 and 10
  mandatory). **PASS (device candidates A/B, Track P): ≥12
  effective channels (1.5× point) on anchor task; PASS (Track R):
  ≥16 (2× point) — which is also the STRETCH.** "Equivalent
  functional gain" is deleted as an escape hatch: non-device
  pathway candidates (F/G/H) are **G1 = NA (pre-declared)** and
  promote only as *portfolio components* combined with a G1-passing
  or G1-NA-disclosed device/pathway at Gen 1 portfolio level;
  a portfolio may not claim a G1 win its components did not earn.
  Timing sub-gate NI (+20% ITD error) is a Step 1 placeholder to
  derive from binaural literature or delete — flagged underived. v1 ">30" is demoted to an *aspirational
  reference* (≈ count of auditory critical bands; normal cochlea
  ≈3,500 inner hair cells — 30 prosthetic channels remain coarse).
  Sub-gates: temporal coding (rate/envelope/TFS proxy) and
  bilateral synchronization (interaural timing error) — a spectral
  win with broken timing fails G1.
- **G2 Functional hearing.** Primary: speech-recognition threshold
  (SRT) in noise. **PASS: ≥3 dB SRT improvement vs frozen** (W3,
  age-valid test) with speech-in-quiet NI margin −5 percentage
  points. Music (melody/pitch battery) and localization (RMS error)
  secondary; each needs its Appendix A delta. Infant windows use
  the proxy chain (§5.3), discounted — infants cannot do ripple tasks.
- **G3a Language (any modality).** Receptive+expressive language
  *in the child's accessible modalities* (signed, spoken, or both;
  instruments per modality in Appendix A: e.g., CDI/ASL-CDI,
  PLS-5-class, IT-MAIS/LittlEARS for early auditory function).
  **PASS (modality-specific co-primaries; NO pooled SD across
  incommensurable norms): ≥0.4 SD vs frozen *within* the signed
  stratum (ASL-normed instruments) and/or *within* the spoken
  stratum (spoken-normed instruments) in ≥1 of W2/W3, NI (−0.2 SD)
  in every measured stratum/window.** Bimodal children: pre-declared
  primary = highest-modality language score + total conceptual
  vocabulary (hierarchy fixed Step 1). Family H causality is
  *not* claimed from adjustment alone (modality is family-chosen):
  H requires encouragement/observational design with stated
  identification strategy (§8). Stratified/adjusted
  for modality, home language, SES proxy, EI dose, additional
  disabilities. P1 CAEP / fNIRS are *mechanism* measures (surrogate
  criteria §5.3), never sole G3 passes.
- **G3b Communication autonomy & family outcomes (co-primary).**
  Family-reported communication autonomy / QoL instrument
  (named in Appendix A with Deaf/parent stakeholders, §9).
  **G3b scoring is BLOCKED (all cells INSUFFICIENT) until the
  instrument + MCID are co-designed and committed in Step 1.**
  **PASS: NI vs frozen; superiority claimed only with stakeholder-
  defined MCID.** A spoken-language gain with autonomy loss fails.
- **G4 Biology preservation (Track P veto).** Components (all must
  pass in Track P): residual-hearing preservation rate; SGN/hair-cell
  survival (animal tier); fibrosis/ossification grade (named scale);
  scala patency; **G4-AAV sub-gate:** any AAV-using challenger is a
  *presumptive G4 FAIL* until capsid-switch / non-viral re-dosing
  or post-exposure later-AAV efficacy is shown (anti-capsid immunity
  explicitly scored). Supporting-cell *consumption* (Family D) is
  alteration, not preservation.
- **G5 Safety & durability.** Surgical (anesthesia <12 mo,
  meningitis, facial nerve, CSF leak — malformation-specific),
  vestibular, device failure/revision, stimulation safety (charge
  density, thermal, phototoxicity), MRI compatibility, tumor/
  misrouting (neurotrophin/reprogramming), immunogenicity (opsins).
  **PASS: NI vs frozen within Appendix A margins per harm** (no
  uniform multiplier; §6). Every candidate files an FMEA (App. C).
- **G6 Deliverability (per-family, no single 80% fiction).**
  Eligible fraction of P0 *by anatomy/etiology stratum* with
  denominators (App. D); age at first access; therapy/mapping
  burden (hrs/week, visits/year); equity metrics (travel distance,
  insurance, rurality, home-language access, EHDI loss-to-follow-up);
  earliest-plausible infant timeline (§10). **PASS requires:**
  stratum coverage table complete + burden disparity vs frozen
  within Appendix A bound + timeline stated. Portfolio coverage
  (union over G/H/A/B winners by stratum) reported separately.

**Scoring states per gate-cell:** PASS / FAIL / INSUFFICIENT
(missing or below-tier evidence). **INSUFFICIENT never counts as
pass and is never judge-imputed.** Promotion (device, Track P) =
PASS on G1, G2, G3a, G3b, G4, G5, G6; promotion (pathway component
F/G/H) = PASS on G2–G6 with G1 NA disclosed, effective only inside
a Gen 1 portfolio stating its device G1 verdict — at primary *and* stress
scenarios (§6), in decision-time analysis. Anything else keeps frozen.

### 4.3 Estimand

Primary: **treatment-policy (ITT-analog)** — assigned pathway
including non-use, crossover/rescue to CI, explants, loss to
follow-up in denominators. Matched-intensity / per-protocol analyses
are secondary sensitivities (v1 conflated the two).

## 5. Evidence, inference & the ≥90% standard (de-cargo-culted)

### 5.1 What replaces v1's statistical clothing

v1 imported "≥90% + family-wise exclude-zero + walk-forward" from
trading (333 paired monthly returns, block bootstrap, same panel).
Heterogeneous animal/literature evidence has no common return unit;
judge opinion is not a bootstrap. v2 is explicit:

- **Gen 0/Gen 1 do not produce ≥90% promotion claims.** Primary
  deliverable reframed honestly: an **open evidence synthesis +
  prioritized study designs** (public, citable, usable without any
  partnership). *Adoption* by a qualified lab is a stretch outcome
  with a stated criterion (a named external group commits to run/
  fund a handoff design); absence of adoption does not falsify the
  synthesis, and engagement by incumbent program owners (§2.2) is
  never assumed. Ranked by gate scores with evidence grades.
  (v1 §"persuade an otologist to run FIH" is retired.)
- **≥90% is reserved** for a future frozen candidate evaluated on
  *prospective, paired human (or validated large-animal) data*
  under a pre-registered analysis: joint estimand = P(all Track-P
  gates pass in P0 decision-time population over W0–W3), modeled
  with stated effect/variance/dependence assumptions and sensitivity
  analyses. Until such data exist, any probability in this repo is
  labeled *modeled sub-claim, conditional on assumptions X* (e.g.,
  Monte Carlo spread-of-excitation), never a promotion probability.
- Historical response fractions are not forward probabilities.
  Overlapping windows/repeated measures are not independent trials.

### 5.2 Evidence grading & multiplicity (operational)

- **Grading:** adapted GRADE per gate-cell (High/Moderate/Low/Very
  low) + risk-of-bias tool by design (RoB 2 / ROBINS-I / SYRCLE for
  animal; named in protocol). **GRADE→score map (binding):** PASS
  requires ≥Moderate GRADE *and* Appendix A minimum tier; Low =
  provisional signal (reported, never PASS); Very low / high RoB =
  INSUFFICIENT. **Allegiance rule:** inventor-lab single-source
  claims (e.g., device-originating groups) start one GRADE level
  lower and G1 signals require non-inventor replication to PASS.
  Publication bias: trial-registry + grey-literature search (§9);
  funnel/Egger only where ≥10 studies.
- **Multiplicity:** the searched-family log (every candidate × gate
  × window × stratum scored) is published. Formal family-wise
  control applies *only* to quantitative meta-analytic sub-claims
  (primary comparisons pre-listed; Holm or hierarchical gatekeeping
  stated in protocol). Qualitative gate scores use the log for
  *discounting narrative confidence*, honestly labeled as such.
- **Held-out rule:** before Gen 0 scoring, partition evidence by
  *study* (never by rows within a study) and by date (design
  evidence ≤ freeze date; validation = later/independent labs).
  Species held-out (mouse-designed claim needs non-mouse check)
  where available. Partition manifest committed with protocol.
- **Unit of analysis:** child (ear-level data clustered by child);
  animal: animal (ear clustered). Simulation: seed set pinned.

### 5.3 Evidence tiers, translation discounts & proxy chains

| Tier | Evidence | Max use |
|---|---|---|
| T0 | In-silico / bench / in-vitro | Mechanism plausibility; never G2/G3 pass |
| T1 | Neonatal small-animal | Hypothesis generation; G1/G4 signals only, heavily discounted |
| T2 | Mature/deafened animal (incl. large-animal where relevant) | G1/G4/G5 provisional; required before Track-R advancement |
| T3 | Adult human (incl. vocoder in normal-hearing adults) | G1/G2 proxies; vocoder ≠ infant biology (see chain) |
| T4 | Pediatric human (age-matched) | Required for any infant promotion claim |

**Infant proxy chain (each arrow discounted & stated):**
animal neurophysiology (spread, synapse counts) → adult
psychophysics (ripple/SRT) → infant CAEP/behavioral (P1, VRA,
IT-MAIS) → W2/W3 language. Surrogates (P1 latency, fNIRS
cross-modal index, modeled channel count) must meet pre-stated
validation criteria (association + mediation evidence) before
counting toward G3; otherwise mechanism-only. Minimum tier per
gate is in Appendix A. **Reconciled tier rule (Appendix A governs):**
G3a PASS requires **T4**; T3+validated-chain yields at most a
provisional signal (§5.2 Low rule), never PASS.

**Developmental causal-chain requirement** (replaces v1
segment-majority walk-forward): each candidate must show its early
mechanism measure (W0/W1) *and* downstream outcome (W2/W3) from
linked cohorts, or state the mediation assumption as UNRESOLVED.
Temporal validation: hypotheses designed on earlier literature
are checked against later/independent evidence (§5.2 held-out).

## 6. Costs & stresses (per-harm scenarios, not ×2/×4)

Cost dictionary (pinned Step 1): component, base rate/range +
source (CI registries/cohorts), perspective (family / payer /
societal — all three reported), horizon (to 7 y primary; to
adolescence sensitivity), dollar year, **discount rate 3%/y
(0%/5% sensitivity)**. No invented dollar costs
for preclinical combos — report burden units instead.

**Primary scenario:** base rates. **Stress scenarios (per harm,**
at the **90th percentile / upper 95% CI bound** of published ranges,
pinned per harm in Step 1): S-revision (device failure/
reimplantation high), S-nonuse (device non-use / low wear-time
high), S-access (EHDI loss-to-follow-up + travel/insurance failure
high), S-surgical (major complication high, incl. malformation
subgroup). Promotion must survive *each* stress (gate re-scored),
not a uniform multiplier. **Decision rule stated ex ante:** e.g.,
families/clinicians accept added revision risk only if G2 SRT gain
≥ Appendix A threshold *and* G3b NI holds — trade-offs elicited
with stakeholders (§9), not assumed. Terminal accounting complete:
explants, failures, vestibular/meningitis events, deaths, loss to
follow-up in denominators.

## 7. Evolutionary loop (with a real fitness rule)

```text
Gen N candidates (Appendix B template, pre-registered, track declared)
  → score vs frozen on G1–G6 (PASS/FAIL/INSUFFICIENT, App. A)
  → adversarial review (distinct falsification target per claim)
  → LEXICOGRAPHIC FITNESS (Track P; order stakeholder-elicited
    Step 1, rank-sensitivity to order reported): 1) fewest FAILs
    (G4/G5 veto FAIL = demote last), 2) fewest INSUFFICIENT among
    applicable gates, 3) largest G2 gain, 4) largest G3a gain,
    5) G3b verdict, 6) device G1 (NA last among ties), 7) lowest
    burden (G6). Note: fewest-INSUFFICIENT favors studied incumbents
    by design — disclosed, with an evidence-completeness sensitivity
    ranking published alongside. Track R ranked separately (G1,
    then G5 aggregate = count of Appendix C harms rated ≥major
    severity × probability band, defined Step 2 in gate_table spec).
    Pareto sets reported for
    transparency but ranking/promotion uses this rule — fixing
    v1's incomparable-everything problem.
  → RECOMBINE only at evidenced interfaces (§7 rule 3);
    MUTATE one logged change per child; RETIRE dominated (visible)
  → Gen N+1 … STOP on evidence criteria (§7 rule 5), not dry counts alone.
```

**Loop rules.** (1) *Small & specified:* Gen 0 = **exactly 8**
candidates (1 per family A–H, §8; reconciles v1's 4–8/6–10/6–12
conflict). Later generations 4–8. Every candidate completes
Appendix B (mechanism, cells, route, dose/units, timing, model
system, comparator, eligibility by stratum, power/precision where
quantitative, safety monitoring, burden, regulatory class, kill
criterion) *before* scoring. (2) *All visible:* searched-family log
published; failures archived with killing evidence. (3)
*Recombination needs combination data or a stated interface
experiment* — no slogan crosses (e.g., B×D forbidden until elution +
reprogramming co-delivery has at least T1 data; B×F allowed only as
sequenced pathway, not fused product). Incompatible parents retire
or resolve. (4) *Gaps prioritized, not capped:* v1 "one gap, one
follow-up" is replaced — promotion-blocking gaps (Q0 preservation,
B tonotopy, AAV re-dosing) get repeated independent attack ranked
by decision-relevance × tractability; only the anti-rewording
`seen`-set discipline is kept (same gap, new wording ≠ new gap).
(5) *Stopping:* stop discovery when (a) a Track-P candidate is
frozen for study-design handoff, OR (b) two consecutive generations
add no candidate improving lexicographic fitness *and* all
promotion-blocking gaps have had ≥2 independent attacks, OR (c)
budget (§9) exhausted — labeled *partial*. Max **4 generations**
for non-promoting survivors without new external evidence.
(6) *Independent lenses:* biophysics, developmental neuroscience,
surgical/translational, evidence-synthesis, stakeholder (§9).
Failed/unavailable reviewer = synthesis note, never a vote.
(7) *Freeze checklist* (replaces hash ceremony — git already
hashes): candidates, Appendix A version, thresholds, held-out
manifest, analysis owner, date — committed before validation
evidence is opened. Post-freeze edits = new candidate.

**First locked computation:** `research/scoring/gate_table.py`
(§9) reading a versioned evidence-extraction CSV and emitting the
gate matrix + fitness ranking deterministically. `verify/` locks
*that* (plus epidemiology arithmetic, App. D) — named functions,
not aspirations.

## 8. Gen 0 families & tracks (8 candidates, kill criteria)

Each family → exactly 1 Gen 0 candidate (Appendix B). Timelines =
earliest-plausible *infant* use assuming adult-first staging (§10).

- **A. Focal electrical + anatomy fitting [P; evolving-standard-aware].**
  Must benchmark against dexamethasone-eluting / ECochG-guided /
  robotic-insertion standard evolution (those elements are
  comparator updates, §3.4, not challenger novelty) and explain
  prior focusing translation failure. *Kill:* no modeled spread
  reduction at safe charge in fibrotic/growing-cochlea model.
- **B. Biohybrid eluting array [P].** Pre-specify tonotopy metrics
  (place-pitch order, spread pre/post regrowth), elution duration
  vs lifetime, stimulation–outgrowth interaction, and an explicit
  account of 2014–2026 human-translation silence. *Kill:* neurite
  growth without tonotopic order at T2, or no credible lifetime
  burden plan (refill/revision count to adolescence scored in G5/G6;
  a <5 y reservoir without refill is an automatic kill).
- **C. Optical CI [R watch-list].** Scored for learning; G6 FAIL
  for infants until adult FIH + opsin immunogenicity/durability +
  power/heat data exist. Correct citations required (distinguish
  2020 multichannel μLED *EMBO Mol Med* paper from any 2026 work;
  Step 0). *Kill/park criterion:* no adult FIH start by Gen 2
  review or 24 months after Gen 0 freeze, whichever is earlier
  (calendar date written into the Gen 0 freeze checklist).
- **D. Reprogramming / beyond-*OTOF* AAV [R long-horizon].**
  Removed from infant Gen 0 *promotion* scoring. Single kill/
  advance criterion: replicated threshold restoration with
  cochlear-identity, synapsed cells in a *mature deafened
  large-animal* cochlea. Until met (by anyone), D = literature
  watch only. AAV-immunity sub-gate (G4-AAV) applies throughout.
- **E. Penetrating ANI/ABI [R watch-list].** Must report chronic
  in-vivo denominators (e.g., cat 6-month success/failure,
  migration) alongside bench aging/pulse data, plus infant CPA-
  access anatomical analysis. Presumptive G5/G6 fail for bilateral
  infants with CI alternative. *Park until adult human feasibility.*
- **F. W0 auditory bridge — re-specified [P].** Bone conduction
  cannot overcome ≥70 dB SNHL audibility and vibrotactile input
  risks *increasing* somatosensory cross-modal recruitment; v1 F
  as written is therefore split: F1 = *aided-access optimization*
  (early HA fitting, wear-time, ECochG/CAEP-guided timing) with
  dose + falsifying W2 endpoint; vibrotactile contingency only as
  exploratory sub-candidate with named harm monitoring (false
  reassurance / delayed CI = G5 event). **F1 precondition stated:**
  at ≥70 dB SNHL, aided audibility will often remain insufficient
  for spoken-language access — F1 claims are limited to audibility/
  timing optimization and earlier CI decision, never HA-as-substitute.
  *Kill:* no audibility or time-to-CI gain vs frozen workup.
- **G. Diagnosis & sequencing pathway [P; C0 core — NEW].** Rapid
  genomic + CMV + imaging triage at decision time: gene-therapy-
  first where label-eligible, immediate hearing-preservation CI
  otherwise. Includes genomic-counselling, VUS/incidental-finding
  consent & return-of-results, and mis-triage harms (App. C rows).
  The v2 unilateral-CI + preserved-ear variant is **dropped from
  Gen 0**: it is delayed second-ear implantation, conflicts with
  §10 never-delay and bilateral gates, and lacks stated equipoise;
  it may return only as a bounded Gen ≥1 candidate with rescue-
  timing rule + equipoise justification + binaural-cost accounting.
  Gen 0 directly tests Q0 (§1.3; decision rule gated in Step 2
  protocol: patency % + post-CI AAV-efficacy thresholds defined
  *before* Q0 evidence is scored) and G-vs-frozen (§3.4 contents)
  on time-to-access, language, and preserved options. *Kill:* no
  time-to-access or option-preservation gain over frozen workup.
  *This is the expected near-term winner if any* — data must confirm.
- **H. Visual-language-first W0 bridge [P; NEW].** Early signed/
  visual communication exposure (dose-specified, family-chosen)
  scored on G3a (language any modality), G3b, *and* later auditory
  outcomes post-CI. Hypothesis (Kral-consistent): visual language
  supports language development without harming auditory outcomes.
  Design: encouragement / prospective observational with pre-stated
  identification strategy (modality remains family-chosen; no
  randomization of language modality). *Kill:* G3a NI fails in
  signed stratum or post-CI auditory harm signal at ≥Moderate GRADE.
  Never framed as competitor to CI; sequenced with G/A.

*Worked satisfiability example (Track P, paper-level):* G (triage
preserves the *OTOF* ear pre-CI, immediate preservation-CI for
others) + H (W0 signed input) + A-standard (atraumatic array)
plausibly passes G4 (no AAV pre-exposure, patent scala), G5
(standard surgical risks), G3a/b (earlier language access), G6
(available now) as a *pathway portfolio* with **G1 = NA disclosed**
(§4.2: no channel claim; device G1 verdict inherited from the
standard array and stated as frozen-equivalent, not a G1 win).
Gen 0 must test
— not assume — each cell; the example proves the gate set is
non-empty, answering the Round 1 satisfiability objection.

## 9. Execution, team & reproducibility

**Agent contract.** Every research agent returns `complete`,
`evidence[]` (inspected full texts/data/code only — snippets are
pointers), `unresolved[]`, plus a structured claims table
(claim | source DOI/PMID | tier | gate-cell | effect + N) and gate
scores in the extraction-CSV schema. Provenance = commit + source
ID + page/table (the v1 undefined `result.ref` is replaced by this
schema). Scale fan-out to the question; batch counts never prove
completeness.

**Evidence-synthesis methods (PRISMA-like, pre-registered).**
Databases: PubMed, Embase (if accessible — access gap disclosed if
not), ClinicalTrials.gov, FDA labels/decisions; search strings +
dates frozen in protocol; **human-led dual extraction on all
load-bearing claims** (agents may pre-extract; a human extractor
independently verifies + sampled error audit with error rate
reported — agent-only Step 0 verification is circular and banned
for gate-deciding claims); inclusion/exclusion flow
published; bias tools per §5.2. Simulations: named model +
version + parameters + seeds (e.g., finite-element cochlea model
or vocoder config — pinned Step 1). Datasets: manifest with DOI,
licence, hash; large data gitignored, manifests committed.
No-overwrite evidence rule: corrections are new versions.

**Human expertise (required, not optional).** Before any
freeze-for-handoff: named reviewers covering pediatric otology,
auditory neuroscience, trial/biostatistics, regulatory, and
Deaf-community + parent stakeholders. Judge eligibility, blinding
to candidate authorship where feasible, and disagreement
adjudication (majority + written dissent preserved) stated in
protocol. LLM judges *triage*; human experts *decide* freezes.
Until partners are secured, deliverables are labeled open
synthesis (§5.1); adoption is a stretch criterion, never assumed.

**Resources & budget (define before Gen 0).** Holder sets: compute/
literature-access budget, calendar bound per generation, and
advisory-recruitment plan. IP/freedom-to-operate: Gen 0 includes
an FTO flag per family (owner/patent families) — research use
only; no design-around advice. Repo layout (corrected paths):

```text
GOAL.md README.md STATUS.md (append-only)
research/gen00/ gen01/ … (protocol + freeze checklist per gen)
research/frozen_baseline/  research/scoring/gate_table.py
data/ (gitignored payloads)  reviews/ (round records, judge reports)
verify/ (locks for gate_table + epi arithmetic once stable)
```

README "how to run a generation" is added *with* `gate_table.py`,
not claimed before it exists (v1 error corrected).

## 10. Regulatory & ethics translational path

Per-family checklist required in Appendix B: product class
(device PMA / biologic BLA / combination — lead center),
preclinical package (GLP tox, biodistribution/shedding for AAV,
CMC), IDE/HDE considerations, DSMB, endpoint/surrogate acceptance,
long-term follow-up (15 y for integrating/AAV per FDA guidance
where applicable). **Staging is adult-first** for any novel
device/biologic: adult feasibility → older children → infants,
each stage gated. **Ethical comparators:** unilateral add-on,
sequencing, or standard-CI-controlled designs with prospect of
direct benefit — never a delayed-CI control arm for congenital
profound loss. Every trial sketch states equipoise, rescue-to-CI
criteria, parental consent (+ assent when age-appropriate),
irreversible-intervention consent specifics (optogenetics/editing),
and stopping rules for persistent harm. A named regulatory/trialist
reviewer is a Gen 0 completion gate (§9). Timelines in G6 use this
staging; families unable to reach infants within ~15 y are Track-R
watch-list by definition.

Scope guardrails: no enrollment, diagnosis, or treatment
recommendation from this repo; population-level genetics only;
Deaf gain respected via G3b + stakeholder co-design of Appendix A
MCIDs; animal→infant discount per §5.3 in every claim.

## 11. First steps & deliverables

- **Step 0 — Verify sources.** Replace/verify *every* load-bearing
  citation against full text (FDA Otarmeni label + CHORD N/endpoint;
  Friesen et al. channels; Kral 2023; Hearing Research 2025; Liu
  2025; Qiao 2024; EMBO oCI papers disambiguated; ANI bench + cat
  chronic data; reprogramming papers; Danish cohort PMID 37441990;
  per-device FDA CI age labeling). Full DOI/PMID + N + design +
  verified date. Unverifiable claims deleted or downgraded.
- **Step 1 — Pin baseline + Appendix A numbers + cost dictionary**
  (§§3–6) with citations and ranges. Commit before challenger scoring.
- **Step 2 — Pre-register Gen 0** (8 Appendix-B candidates + Q0
  decision thresholds (§8G) + held-out manifest + freeze checklist
  + extraction-CSV schema + `gate_table.py` with passing tests +
  pinned software environment — all committed *before* Step 3).
  Label exploratory-
  after-seen honestly (cf. `durable_strategy.py` header).
- **Step 3 — Sweep → skeptics → judges → gate_table scoring.**
  Publish searched-family log + all INSUFFICIENT cells.
- **Step 4 — One recombination round (Gen 1)** per §7 fitness rule.
- **Step 5 — Decide:** freeze Track-P survivor as *study-design
  handoff* (animal protocol and/or adult-feasibility sketch per
  §10 — never infant FIH from literature alone), or record
  no-promotion with killing evidence. Append to `STATUS.md`.

**Gen 0→1 deliverable:** gate matrix vs frozen (all 8 candidates,
both tracks ranked separately), Q0 verdict, surviving recombinant(s)
or explicit no-winner statement, retired candidates with kill
evidence, unresolved gaps by name, epidemiology/coverage tables
(App. D), and *no* ≥90% claim (§5.1).

## 12. Governance & versions

**Holder** (repo owner): sets budget, freezes baseline versions,
approves handoffs. Holder does **not** sole-score candidates
(personal-stake COI, §1.1); scoring requires independent judges
+ human experts (§9). **Analysis owner** per generation named in
freeze checklist. **GOAL amendments:** versioned (v1→v2…), changelog
in `STATUS.md`, gates never amended retroactively within a frozen
generation. **Project abandonment:** stop and publish negative
synthesis if (a) Q0 + Gen 0 show frozen/evolving-standard already
dominates on joint gates, (b) budget exhausted without Track-P
survivor after Gen 1, or (c) human-expert review judges handoff
designs non-viable. Abandonment with full logs is a successful
outcome of the loop, as in the business project ("keep SPY/frozen").

*Version history:* v1 (e9d4050) initial PRESERVE-30. v2:
two-track gates, operationalized Appendix A, de-cargo-culted
inference, Families G/H, Q0, per-harm stresses, adult-first path,
recomputed-epidemiology requirement — per Round 1 reviews.
v2.1 (this file): Round 2 fixes — G1 NA/portfolio rule + point
anchor, frozen diagnostics/EI contents, modality co-primaries,
GRADE→score map, FAIL-first fitness, G/H design+kills, unilateral
variant dropped, human dual extraction, open-synthesis deliverable.

## Appendix A. Gate operationalization (normative skeleton)

Step 1 fills "Frozen ref" + confirms MCIDs with citations and
stakeholder input (§9); the completed table is versioned with the
Gen 0 protocol. NA = not measurable that window (pre-declared).

| Gate–window | Measure / instrument | PASS vs frozen | NI margin | Min tier |
|---|---|---|---|---|
| G1 W1–W3 | Spread (mm/oct) + ripple (rip/oct); TFS/rate proxy; ITD error (µs); **F/G/H: NA** | Devices: ≥12 (P) / ≥16 (R) vs point 8 (§4.2) | Timing +20%* | T2/T3 + chain |
| G2 W3 (primary) | SRT-in-noise dB (age-valid, e.g. closed/open-set per age); quiet % | ≥3 dB better | Quiet −5 pp | T4 (T3 provisional) |
| G2-music W2–W3 | Melody/pitch battery (named Step 1), % correct | ≥10 pp better | −5 pp | T4 |
| G2 W2 | Word recognition %; localization RMS° (when testable) | ≥10 pp; ≥10° better | −5 pp; +5° | T4 |
| G2 W0–W1 | CAEP detection, VRA thresholds (mechanism only) | No PASS; chain input | — | T4 |
| G3a W2/W3 | Modality-matched SS (signed / spoken separately; bimodal hierarchy §4.2) | ≥+0.4 SD *within stratum* | −0.2 SD every stratum | T4 |
| G3a W1 | IT-MAIS/LittlEARS + CDI | NI + trajectory | −0.2 SD equiv | T4 |
| G3b W1–W3 | Stakeholder-named family QoL/autonomy scale | Superiority per MCID | NI per MCID | T4 |
| G4 all | Residual-hearing %; fibrosis grade (0–4 histopath scale named Step 1); SGN density; G4-AAV re-dose demo | All components ≥ frozen | Per-component in Step 1 | T2 (+T4 RH) |
| G5 all/adolesc. | Per-harm rates (App. C list) | NI per harm | Margins Step 1 from registry ranges | T2/T4 |
| G6 all | Stratum coverage % of P0; hrs/wk; visits/yr; miles; timeline y | Table complete + disparity bound Step 1 | — | Literature/registry |

Missing-data: INSUFFICIENT (§4.2). Competing interventions
(modality switch, rescue CI) handled per estimand (§4.3). Floor/
ceiling: instruments with >20% at bound trigger pre-stated
alternative. Music battery + exact SRT test named in Step 1.
*Timing NI flagged underived (§4.2) — derive or delete in Step 1.

## Appendix B. Candidate specification template (all fields required)

ID/track · mechanism & target cells · delivery route & dose/units ·
timing by window & decision origin · model system/comparator ·
eligibility by §3.2 stratum (incl. ANSD/CND/malformation/syndromic/
comorbid verdicts) · G1–G6 measurement plan (App. A cells) ·
power/precision (quantitative claims) · FMEA summary (App. C) ·
burden (hrs/wk, visits, surgeries) · regulatory class & staging
(§10) · FTO flag · kill criterion · parentage (Gen ≥1) + single
mutation log · exploratory-after-seen label (Y/N + what was seen).

## Appendix C. FMEA / risk register (mandatory rows per candidate)

Anesthesia <12 mo · meningitis · facial nerve · CSF leak/gusher ·
vestibular loss · residual-hearing loss · device failure/revision ·
MRI incompatibility · charge/thermal/phototoxic injury · AAV
immunity/shedding · opsin immunogenicity · neurotrophin misrouting/
tumor signal · reprogramming off-fate/tumor · nerve injury/migration ·
elution depletion · false reassurance/delayed standard care (F/H) ·
genomic mis-triage / VUS distress / incidental findings (G) ·
binaural deprivation from delayed second ear (any sequential design).
Scales: severity 1 minor / 2 moderate / 3 major / 4 catastrophic;
probability bands <0.1% / 0.1–1% / 1–5% / >5% per child (horizon
stated). Each row: severity, probability + source tier, mitigation,
G5 input, persistent-harm stopping rule.

## Appendix D. Epidemiology & coverage arithmetic (Step 1 deliverable)

Tables to build from primary sources with ranges (no single-cohort
point estimates as universals): (D1) congenital bilateral ≥70 dB
incidence at birth vs all congenital HL (separate!); (D2) etiologic
fractions by population/era (*GJB2* by ancestry; *SLC26A4*; cCMV —
bilateral-at-birth vs progressive/asymmetric split; unknown after
modern genomic workup vs pre-genomic cohorts); (D3) anatomic
fractions (CND, malformations, ANSD); (D4) per-family eligible
numerators over P0 + portfolio union. v1 figures stay retired
until D1–D4 are committed with code (`verify/`-locked arithmetic).

## Appendix E. Glossary & sources

AAV adeno-associated virus · ABR auditory brainstem response ·
ABI auditory brainstem implant · ANI auditory nerve implant ·
ANSD auditory neuropathy spectrum disorder · CAEP cortical auditory
evoked potential · CDI MacArthur-Bates Communicative Development
Inventories · CPA cerebellopontine angle · ECochG electrocochleography ·
EHDI Early Hearing Detection & Intervention · EVA enlarged
vestibular aqueduct · FIH first-in-human · MCID minimal clinically
important difference · NI non-inferiority · PTA pure-tone average ·
SGN spiral ganglion neuron · SRT speech-recognition threshold ·
TFS temporal fine structure · VUS variant of uncertain significance.

**Sources:** v2 deliberately carries *no* verified bibliography —
Step 0 (§11) builds it at DOI/PMID level. Anchors to verify first:
FDA Otarmeni label/CHORD; Friesen et al. 2001 + channel-interaction
successors; Kral et al. *Trends Neurosci* 2023; *Hearing Research*
2025 nine-months paper; Liu 2025; Qiao 2024; Dieter/Moser *EMBO Mol
Med* 2020 (+ any 2026 oCI paper, distinguished); ANI *Bioelectronic
Medicine* bench + cat chronic reports; Pinyon et al. 2014;
ATOH1-program papers incl. mature-cochlea limits; PMID 37441990;
per-device FDA CI labeling. Business templates: `business/INTENT.md`,
`AGENTS.md`/`STATUS.md`, `research/durable_strategy.py`.

---

*Most Gen 0 candidates should lose. Frozen bilateral CI — and its
evolving hearing-preservation standard — is strong. Beating it
jointly on listening, language (any modality), autonomy,
preservation, safety, and access would be a real advance.
Claiming victory on one modeled channel count would not.*
