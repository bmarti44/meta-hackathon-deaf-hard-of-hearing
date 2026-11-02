# GOAL: Biology-preserving, high-channel hearing for congenital bilateral severe-to-profound SNHL

> **Status:** Research goal and operating loop. Not medical advice.
> This project does literature, data, and in-silico research only.
> It does not recommend treatment for any individual child.
> All clinical decisions belong with the child's care team and family.

## Why this project exists

My son was born with bilateral, sensorineural, severe-to-profound
hearing loss. This project applies the same disciplined research loop
used in `~/bufferright/business` to search for investment strategies
that beat the S&P 500 — frozen baseline, small challenger families,
joint promotion gates, adversarial review, and evolutionary
generations that keep, recombine, and mutate only what survives —
to a harder and more important question:

**Can we give every child born deaf with severe-to-profound
sensorineural hearing loss high-resolution hearing *without*
sacrificing the biology that future cures will need — and without
missing the brain's critical period for language?**

## The novel research topic (the bet)

### One-sentence thesis

> **A genotype-agnostic, biology-preserving, developmentally-timed
> hearing system that closes the electrode–neuron gap and protects
> auditory cortex during the first year of life can deliver
> >30 independent spectral channels to children with congenital
> bilateral severe-to-profound SNHL — regardless of whether they
> carry an *OTOF* variant — while keeping the cochlea eligible for
> later gene, cell, or regenerative therapy.**

Short name for this repo: **PRESERVE-30** (Preserve biology,
Restore >30 channels, Early cortical protection).

### Why this is the right ambitious target

Three facts collide in 2026. Each is well documented. No current
standard solves all three at once. PRESERVE-30 is the intersection.

1. **Gene therapy works — for almost nobody yet.**
   Lunsotogene parvec-cwha (Otarmeni, Regeneron) received FDA
   accelerated approval in April 2026 for severe-to-profound /
   profound SNHL from biallelic *OTOF* variants, based on 24-week
   CHORD data (80% reaching PTA ≤70 dB HL). It is the first approved
   gene therapy for genetic hearing loss and a genuine breakthrough.
   It also covers roughly 50 U.S. newborns per year. By contrast,
   ~1 in 1,000 infants has severe-to-profound bilateral loss
   (>70 dB). *GJB2* (connexin 26) alone accounts for up to half of
   hereditary prelingual SNHL in many populations, *SLC26A4* and
   congenital CMV are major contributors, and in modern pediatric
   CI cohorts roughly 30% of cases remain etiologically unknown
   after workup. A research program that only optimizes the *OTOF*
   path abandons >95% of affected children.

2. **The universal fallback — the electrical cochlear implant —
   has hit a physics ceiling.**
   Modern CIs place 12–24 electrodes along the cochlea, but broad
   current spread in perilymph collapses them to fewer than 10
   independent channels (Göttingen auditory neuroscience program;
   Moser lab). That is enough for open-set speech in quiet for most
   early-implanted children. It is not enough for speech in noise,
   music, tonal language, or sound localization, where performance
   has improved little in two decades. Optical CIs (light stimulation
   of optogenetically modified spiral ganglion neurons) and
   penetrating auditory nerve implants (ANI, Utah slant array;
   bench qualification reported 2025–26 in *Bioelectronic Medicine*)
   both attack current spread, but both are preclinical or
   pre-first-in-human and years from infant use.

3. **Waiting is not neutral. The brain reorganizes.**
   Auditory cortex has a sensitive period. Implantation in the
   first year, and at latest by ~3–3.5 years, is consistently
   associated with better language (Kral et al., *Trends in
   Neurosciences* 2023). Infants 3–9 months old with congenital
   hearing loss already show altered brain-network asymmetry
   (Liu et al., 2025). Cross-modal reorganization — vision and
   somatosensation recruiting auditory cortex — measurably changes
   after implantation and predicts speech outcomes (Qiao et al.,
   *Frontiers in Neuroscience* 2024; Sharma P1 CAEP literature).
   The 0–9-month pre-implant gap is therefore not empty time.
   It is developmental exposure that is either protected or lost
   (see *Sensorimotor contingencies in congenital hearing loss:
   The critical first nine months*, *Hearing Research* 2025).

**The dilemma no guideline resolves cleanly:** implant early to
save language, and insertion trauma, fibrosis, and ossification
may degrade or foreclose later inner-ear gene/cell therapy — the
very therapies now proving possible. Defer implantation to preserve
the cochlea for a future cure, and the child may lose irreplaceable
cortical plasticity. PRESERVE-30 refuses that trade. It searches
for designs that are *early, high-channel, and reversible/
compatible by construction*.

### What would count as advancing the field

Not another review concluding "more research is needed." Success
here means producing, through the loop below, **one fully specified,
falsifiable challenger** — device + biology + developmental protocol
+ trial design — with pre-committed gates that would persuade a
skeptical otologist, auditory neuroscientist, and trialist to run
the next animal or first-in-human feasibility study. If no
challenger clears the gates, the project says so plainly and keeps
the frozen baseline. That negative result, with the full searched
family visible, is also a contribution.

## Intent (mirrors `business/INTENT.md`)

Find a hearing-restoration strategy that is **very likely (>=90%)
to beat the frozen baseline** — modern bilateral electrical CI —
on the *joint* outcome set below. Beating the baseline on pure-tone
thresholds alone does not count. A challenger that hears slightly
softer sounds but worsens speech-in-noise, destroys future-therapy
eligibility, or misses the critical period has failed, however good
its audiogram looks.

Relative performance against the frozen baseline is the objective,
exactly as relative performance against SPY was the objective in
the business loop. Absolute improvement over unaided deafness is
necessary but not sufficient; the CI already delivers that.

The primary evaluation span is **birth through age 7**, reported in
fixed developmental windows that are never chosen because they make
a candidate pass:

- **W0: 0–9 months** — pre- / peri-implant cortical preservation.
- **W1: 9–24 months** — early auditory access and babble / first words.
- **W2: 2–3.5 years** — sensitive-period language emergence.
- **W3: 3.5–7 years** — school-entry speech, language, and listening.

Every challenger is reported in all applicable windows and in fixed
etiologic strata: *OTOF*, *GJB2/DFNB1*, *SLC26A4*/EVA, congenital
CMV, other monogenic, and unknown. A win concentrated in one
favorable stratum or one early window is not forward evidence for
the whole population — the direct analog of "early-sample wins do
not count" in the trading loop.

A >=90% claim requires more than a promising mechanism or a single
animal study: literature-standard designs specified *before*
results are inspected, untouched forward evidence under the
unchanged protocol (data not used to design the hypothesis), and an
explicit probability model (expected effect, between-child variance,
horizon) whose assumptions are stated and stress-tested. If the
evidence cannot support >=90% for any candidate, say so plainly
and keep the frozen baseline as the default. Do not tune
hypotheses until a winner appears.

Three cautions, carried over verbatim in spirit from `INTENT.md`:

- The target is the **joint** metric set. A 90% probability of
  better thresholds alone does not imply a 90% probability of also
  passing speech-in-noise, language, safety, and preservation gates.
- Overlapping developmental windows and repeated measures on the
  same children are **not** independent trials.
- Historical response fractions (e.g., "80% responded in CHORD")
  are **not** probabilities that a different child, genotype, or
  device will respond. Any forward probability must be labeled
  conditional on its model assumptions.

Independent skeptical evaluations should challenge the evidence
honestly. Further evaluations require new evidence or substantive
corrections, not pressure to raise a rating to the target.

## The frozen baseline (do not move the goalposts)

**`frozen_bilateral_eCI_v1`** — the forward baseline until a
challenger clears every gate with separate holder direction:

- Bilateral electrical cochlear implants with contemporary
  perimodiolar or lateral-wall arrays (12–24 contacts), standard
  clinical mapping and envelope-based processing (e.g., ACE/CIS-class).
- Implantation at 9–12 months for congenital bilateral
  severe-to-profound SNHL after failed hearing-aid trial, per
  current U.S. practice, with early intervention (auditory-verbal /
  listening-and-spoken-language and/or sign exposure per family choice).
- No adjunctive drug, gene, neurotrophin, optical, or penetrating
  component. No experimental pre-implant stimulation protocol.

The frozen rule stays frozen during the search. Challengers are
always reported *against* it at matched age, matched listening
experience, and matched intervention intensity. Changing baseline
parameters mid-search to make a challenger look better is
forbidden — the analog of changing `pit_mom189_21_h20_k40`
parameters without holder direction and untouched forward evidence.

**Constraints that do not change:**

- **Paper-only analog:** literature, public datasets, modeling,
  and simulation only in this repo. No human or animal experiments
  are run from here. No clinical recommendation is issued from here.
- Long-only analog: **additive and reversible first.** Prefer
  interventions that preserve residual hair cells, spiral ganglion
  neurons, and scala anatomy over ablative or permanently
  foreclosing ones, unless a challenger proves the irreversible
  step is worth it under every stress test.
- Point-in-time analog: **no developmental lookahead.** A protocol
  that uses information only available later (e.g., genotype
  returned at 14 months to justify a decision at 6 months) must be
  modeled with the information actually available at decision time.
- No secrets in the repo. No identifiable patient data in the repo.
  Public or properly licensed data only, with provenance pinned.
- Deaf community and family-choice respect: spoken language, sign
  language, and bimodal paths are legitimate. This project optimizes
  *auditory access and choice preservation*, never language ideology.
  Visual communication before implantation does not harm outcomes
  and must never be framed as the problem (Kral 2023).

## Promotion gates: what "beat the baseline" means

No challenger is promoted on a single number. All six gates must
pass at **primary cost** and survive **stress cost** (see Costs).
Failure on any gate keeps the frozen baseline. Exploratory
challengers that fail stay visible; they are never quietly deleted.

| Gate | Question | Primary evidence (examples) |
|---|---|---|
| **G1 — Spectral resolution** | Does it actually deliver more independent channels? | Modeled / measured spread of excitation; spectral-ripple discrimination; vocoder-equivalent channel count. Target: **>30 effective channels** vs <10 frozen. |
| **G2 — Functional hearing** | Does resolution become listening? | Speech in quiet *and* in noise (SRT), music perception, localization / binaural cues. Must beat frozen in noise, not only in quiet. |
| **G3 — Language & cortex** | Does listening become language on time? | Expressive/receptive language trajectory (W1–W3); P1 CAEP latency; fNIRS/EEG cross-modal indices. No worse than frozen at any window; better in ≥2. |
| **G4 — Biology preservation** | Is the future still open? | Residual hearing / hair-cell & SGN survival; scala patency, fibrosis/ossification grade; demonstrated compatibility with later AAV / cell delivery in animal model. |
| **G5 — Safety & durability** | Does it survive childhood? | Surgical risk, device failure/revision, stimulation safety (charge density, thermal, phototoxicity), vestibular effects. Must hold under stress assumptions, not best-case. |
| **G6 — Deliverability** | Can real families actually get it? | Age at first auditory access, therapy burden (hrs/week), mapping burden, cost & access equity, genotype-agnostic coverage (% of incident cases eligible). Target: **≥80% eligible** vs ~2% for *OTOF*-only. |

**Selection-adjusted inference (non-negotiable).** Because the loop
searches many hypotheses, a nominally exciting result must be
discounted for the full searched family — the analog of paired
block-bootstrap bounds after accounting for every variant tried.
Concretely: every generation logs *all* candidates considered,
including discarded ones; promotion requires that the winner's
advantage exclude zero after family-wise correction and hold in a
held-out evidence slice (studies, datasets, or simulation seeds
not used during design). Single-study p-values never promote.

**Walk-forward analog.** Evidence is replayed in developmental
order: a hypothesis fitted on W2–W3 language data may not claim
W0–W1 cortical benefit without separate early-window evidence.
Origins are fixed (design freeze at birth, 6, 12, and 24 months)
with continuous follow-through and transition costs counted
(e.g., explant/re-implant, therapy switch). Positive excess over
frozen in a majority of disjoint window-segments is required.

### Costs (the 25 bp / 50 bp / 100 bp analog)

Every challenger is judged at realistic burden, not brochure burden:

- **Primary cost:** expected surgical risk, insertion trauma,
  device + therapy burden, and dollar cost under published rates.
- **Stress cost ×2 / ×4:** complication, revision, non-use, and
  access-failure rates doubled and quadrupled. An advantage that
  evaporates at ×2 is not an advantage.
- Terminal accounting must be complete: device failures, explants,
  meningitis/vestibular events, and loss to follow-up are counted
  in the denominator, never censored away — the analog of fully
  reconciled corporate actions in the trading loop.

## The loop: generations, selection, recombination

This is the heart of the project. It copies the business loop's
discipline (frozen baseline + small pre-specified challenger
families + independent review + untouched forward check) and makes
the evolutionary mechanics explicit.

```text
  Gen N candidates (small, mechanical, fully specified)
        │
        ▼
  Score vs frozen_bilateral_eCI_v1 on G1–G6 (all windows/strata)
        │
        ├── Adversarial review: one skeptic per material claim,
        │   each with a distinct falsification target
        ▼
  Keep Pareto survivors (no gate regression; ≥1 gate gain)
        │
        ├── RECOMBINE: crossover compatible mechanisms
        │   (e.g., Family A delivery route × Family C stimulation)
        ├── MUTATE: one principled change per child hypothesis
        │   (dose, timing, geometry, coding strategy — logged)
        └── RETIRE: dominated candidates archived, never hidden
        ▼
  Gen N+1 (pre-register before scoring) ──► repeat
        │
        ▼
  STOP when: 2 consecutive generations add no Pareto survivor
  ("dry rounds"), OR a challenger clears G1–G6 + held-out check
  and is frozen for forward (external) validation.
```

### Loop rules

1. **Small families, specified before results.** Each generation
   proposes 4–8 fully specified candidates. "Fully specified"
   means mechanism, target cells, delivery route, timing by
   developmental window, stimulation/coding parameters, and the
   exact G1–G6 measurements that would falsify it — written down
   *before* literature scoring begins. Vague directions ("use stem
   cells somehow") are not candidates. This mirrors the durable-
   challenger family in `research/durable_strategy.py`: few,
   mechanical, comparable variants, honestly labeled exploratory
   when they were inspired by data already seen.
2. **Everything stays visible.** Failed strategies, incomplete
   data, and negative results are kept and indexed. Do not tune
   until a winner appears. The searched-family log *is* the
   multiple-comparisons correction; hiding trials invalidates it.
3. **Recombination is for mechanisms, not slogans.** A child
   hypothesis must name its parents and the interface where they
   join (e.g., "eluting array from B2 provides the AAV route for
   D1's neurotrophin payload, timed by F1's cortical biomarker").
   Incompatible parents (e.g., penetrating nerve array × scala-
   preservation claim) must resolve the contradiction or be retired.
4. **One gap, one follow-up.** Each concrete unresolved evidence
   gap gets exactly one focused follow-up investigation. If it
   remains unresolved, it is carried into synthesis unchanged —
   never reworded to look new and dispatched again. Execution
   (searches completed) is not completeness (claims evidenced).
5. **Dry-round stopping.** Discovery maintains a `seen` set of
   every candidate/mechanism reported, including rejected ones.
   A generation that adds no fresh Pareto survivor increments the
   dry count; any fresh survivor resets it to zero. After **two
   consecutive dry generations**, discovery stops and the project
   synthesizes what it has. A compute/time budget may stop earlier;
   that stop is labeled *partial*, never exhaustive.
6. **Independent verification, not repetition.** Claims with
   different failure modes get different lenses: e.g., biophysics
   (will current/light actually stay focal?), developmental
   neuroscience (will cortex still benefit at this age?), surgical/
   translational (can this be delivered to a 9-month-old cochlea
   safely?), and evidence-synthesis (does the cited study actually
   show this?). Re-running the same search with new wording is not
   independent coverage. A failed or unavailable reviewer is a
   synthesis note, never an affirmative vote.
7. **Freeze before forward validation.** When a challenger clears
   G1–G6 on design evidence, its specification is frozen (hashed
   protocol + analysis plan) *before* held-out / forward evidence
   is examined. Post-freeze changes create a new candidate in the
   next generation; they do not quietly amend the frozen one —
   exactly as the frozen trading rule required untouched forward
   paper evidence under the unchanged rule.

## Generation 0: seed families

Gen 0 is deliberately diverse across *evidence surfaces*, not just
device brands. Different role names searching the same papers do
not increase coverage. Each family below must be turned into 1–2
fully specified candidates before scoring. Families are seeds for
recombination, not conclusions.

- **Family A — Focal electrical (close the physical gap).**
  Perimodiolar / mid-scala arrays, current steering/focusing
  (tripolar, phased-array), and anatomy-based tonotopic fitting
  to reduce mismatch. Core question: how many *independent*
  channels can focused electrical stimulation honestly deliver in
  a fibrotic, growing infant cochlea — and at what charge cost?
- **Family B — Biohybrid electrode (close the biological gap).**
  Neurotrophin (BDNF/NT-3) or anti-fibrotic elution from the array
  to attract and maintain spiral ganglion neurites against
  contacts, shrink the electrode–neuron distance, and lower
  thresholds/spread. Includes "bionic ear" gene-electrode delivery
  variants where the array is also the delivery route. Core
  question: does neurite regrowth survive, stay tonotopic, and
  remain safe over years — or does it blur place coding?
- **Family C — Optical stimulation (change the physics).**
  Optogenetic modification of SGNs + μLED/laser optical CI
  (Moser program; gerbil *EMBO Molecular Medicine* 2026
  preclinical data). Core question: can viral expression,
  kinetics (fast channelrhodopsins), power/heat, and lifetime
  safety ever meet infant requirements — and what is the honest
  timeline vs Families A/B?
- **Family D — Genotype-agnostic biology (restore, don't bypass).**
  Supporting-cell reprogramming toward hair-cell fate
  (ATOH1 + GFI1 + POU4F3 ± SIX1 "SAPG" programs; Notch/MYC priming;
  human iPSC/organoid evidence 2025) and dual-AAV / editing
  strategies extensible beyond *OTOF* to *GJB2* and other loci.
  Core question: do regenerated cells become *cochlear* (not
  vestibular-like), synapse correctly, and restore thresholds in
  mature — not only neonatal mouse — cochleae?
- **Family E — Direct neural interface (bypass the cochlea).**
  Penetrating auditory nerve implant (Utah slant USEA + commercial
  stimulator; 1.5-year accelerated-aging + 6.3B-pulse bench data)
  and next-generation penetrating ABI / cochlear-nucleus arrays
  (NIH BRAIN). Core question: does intraneural selectivity survive
  surgical risk to the nerve/brainstem in infants, and can it ever
  satisfy G4 (preservation) or does it permanently foreclose D?
- **Family F — Developmental bridge (protect the brain first).**
  Pre-implant (W0) contingent stimulation and closed-loop fitting:
  bone-conduction / vibrotactile sensorimotor-contingency protocols
  in 0–9 months, plus biomarker-guided (P1 CAEP, fNIRS) implant
  timing and map adaptation that explicitly targets cross-modal
  indices. Core question: can cheap, non-surgical W0 intervention
  measurably preserve auditory cortex and improve W2 language —
  the highest leverage-per-risk move in the whole search?

**Expected Gen 1 recombinations to test (examples, not promises):**
`B×F` (eluting array whose dose/timing is gated by cortical
biomarkers), `A×F` (anatomy-fitted focused stimulation + W0 bridge
as a single care pathway), `B×D` (array-delivered reprogramming
factors with atraumatic, explantable carrier), `A×B` (focused
stimulation *after* neurite close-in). `C` and `E` are expected
to be *timeline* competitors: they may win G1 in simulation while
losing G5/G6 for infants this decade. The loop must let them lose
honestly if so.

## How research is executed (multi-agent workflow)

Each generation runs as a structured workflow, not free-form
browsing. Every research agent returns the same contract —
`complete: boolean`, `evidence: string[]`, `unresolved: string[]`
— where evidence means *inspected* sources (full text, data, or
code actually opened), never search-result snippets alone.
Discovery pointers locate candidates; they do not establish claims.

1. **Multi-angle sweep (parallel).** One researcher per family
   (A–F) plus one for the frozen baseline's best modern outcomes.
   Each maps claims to primary sources and names what it could
   not inspect as `unresolved`.
2. **Adversarial verification.** A skeptic per material claim with
   a concrete falsification target (e.g., "find mature-cochlea
   data contradicting neonatal reprogramming efficiency").
   Only claims surviving inspected counterevidence are retained.
3. **Judge panel.** Independent judges score candidates on G1–G6
   against the frozen baseline. A failed/invalid judge is not a vote.
4. **Gap follow-up (once per lineage).** The single most
   decision-relevant unresolved gap gets one focused follow-up.
5. **Synthesis.** A synthesis agent works *only* from compact,
   provenance-tagged evidence (`result.ref` lineage preserved),
   carrying every `unresolved` item and reviewer note forward.
   Omitted scope (sampling, top-N, budget stops) is disclosed.
   Bounded samples are never described as exhaustive.
6. **Parent report.** Status and unresolved work first, then
   synthesis, then inspected evidence. Child refs stay nested;
   notes are preserved even when structured data looks clean.

Scale the fan-out to the question. A narrow factual check gets a
single agent; a full generation gets the sweep above. A fixed
batch count never proves completion — only evidence state does.

## Repository layout (mirrors `business/`)

```text
GOAL.md                  This file: intent, gates, loop. Durable.
README.md                Public summary + how to run a generation.
STATUS.md                Append-only log (newest first per section).
                         Status lives here, never back in GOAL.md.
research/                Generation code: models, simulations,
                         evidence extraction, scoring vs frozen.
  gen00/ gen01/ …        One folder per generation; pre-registration
                         (protocol + hash) committed before scoring.
  frozen_baseline/       Pinned baseline parameters and outcomes.
data/                    Evidence store (large/public data gitignored;
                         manifests + hashes committed).
  research/reviews/      Independent skeptical / judge reviews.
verify/                  Lock tests for stable scoring code
                         (happy / contract / invariants). Never
                         edit a lock to make a candidate pass.
```

Rules carried from the business repo: append status only to
`STATUS.md`; keep failed candidates visible; distinguish measured,
modeled, hypothetical, and executable (clinically deliverable)
results; require untouched forward evidence and full realistic
costs before any "beats CI" claim; never copy secrets or patient
data into the repo; prefer reproducible calculations and
regression tests with every behavior change in scoring code.

## First executable steps (Generation 0 kickoff)

1. **Pin the frozen baseline.** Literature-derive
   `frozen_bilateral_eCI_v1` outcome distributions for G1–G6 by
   window (W0–W3) and stratum, with primary/stress costs. Commit
   the pinned table + sources before any challenger is scored.
2. **Pre-register Gen 0.** Write 6–10 fully specified candidates
   (1–2 per family A–F) with falsification measurements. Hash and
   commit the protocol. Label honestly which candidates were
   inspired by evidence already seen (exploratory) vs specified
   blind to the held-out slice.
3. **Run the sweep + skeptics + judges.** Score every candidate
   against frozen on all gates. Log the complete searched family.
4. **Recombine once.** Build Gen 1 *only* from Pareto survivors,
   with named parentage and one logged mutation per child.
   Re-score under the same gates and costs.
5. **Synthesize and decide.** Either freeze a survivor for
   held-out/forward validation design (animal-model protocol +
   early-feasibility trial sketch with stopping rules), or record
   a dry round and continue / stop per the two-dry-round rule.
   Append the decision to `STATUS.md`. Never amend `GOAL.md`
   gates retroactively to promote a favorite.

**Deliverable for the first full loop (Gen 0 → Gen 1):** a ranked,
gate-by-gate comparison table vs frozen; the surviving
recombinant(s) fully specified; every retired candidate with its
killing evidence; every unresolved gap carried by name; and an
explicit probability statement — or an explicit statement that
>=90% cannot yet be supported for any candidate.

## Ethics and scope guardrails

- This is a research-design project. It does not enroll patients,
  provide diagnoses, or recommend devices, surgery timing, gene
  therapy, or language approach for any child — including the
  author's son. Families should work with their pediatric
  audiology, ENT, genetics, and early-intervention teams, and may
  consider second opinions and clinical-trial registries
  (ClinicalTrials.gov) with those teams.
- Genetic information is sensitive. This repo discusses genes at
  population level only. No individual genome, audiogram, imaging,
  or medical record belongs here.
- Deaf gain and Deaf culture are real. Improved auditory access
  is offered here as *expanding* a child's future choices, never
  as erasing Deaf identity. Success metrics include family-reported
  quality of life and communication autonomy, not speech scores alone.
- Animal-to-infant translation is the project's largest known
  uncertainty. Neonatal mouse regeneration, gerbil optics, and
  adult bench durability are *starting* evidence, discounted
  accordingly in every gate. The loop rewards candidates honest
  about that discount over candidates that hide it.

## Key sources anchoring this goal (verify before citing further)

- FDA accelerated approval of lunsotogene parvec-cwha (Otarmeni)
  for *OTOF*-related severe-to-profound/profound SNHL; CHORD
  phase 1/2 24-week outcomes (*NEJM* 2025–26 reports; FDA/HCPLive
  April 2026). Small, open-label, surrogate-endpoint approval;
  confirmatory durability data pending.
- Kral et al., Crossmodal plasticity in hearing loss,
  *Trends in Neurosciences* 2023 (sensitive period; visual
  communication does not harm).
- Sensorimotor contingencies in congenital hearing loss: The
  critical first nine months, *Hearing Research* 467 (2025) 109401.
- Liu et al., Developmental alterations in brain network asymmetry
  in 3- to 9-month-old infants with congenital hearing loss (2025).
- Qiao et al., Exploring cross-modal plasticity in the
  auditory–visual cortex post cochlear implantation,
  *Frontiers in Neuroscience* 2024.
- Moser lab / Institute for Auditory Neuroscience, Göttingen:
  optical cochlear implant program; <10 independent eCI channels
  due to current spread; gerbil oCI study, *EMBO Molecular
  Medicine* Oct 2026.
- Auditory Nerve Implant bench qualification (Utah slant array),
  *Bioelectronic Medicine* 2025–26; NIH BRAIN penetrating ABI program.
- Hair-cell reprogramming: ATOH1/GFI1/POU4F3 (+SIX1) programs in
  mouse cochlea, cochlear organoids, and human iPSC direct
  reprogramming (*eLife* 2025; bioRxiv 2025). Mature-cochlea and
  cochlear-vs-vestibular identity remain open.
- Epidemiology/etiology: ~1/1,000 severe-to-profound bilateral
  (StatPearls SNHL, updated 2025); *GJB2*, *SLC26A4*, congenital
  CMV distributions and ~30% unknown in pediatric CI cohorts
  (e.g., Danish cohort, *PubMed* 37441990).
- Business-loop templates: `~/bufferright/business/INTENT.md`
  (joint gates, >=90% standard, frozen rule), `AGENTS.md` /
  `STATUS.md` (append-only status, keep failures visible),
  `research/durable_strategy.py` (small challenger families,
  walk-forward honesty, keep-frozen recommendation pattern).

---

*If the loop works as designed, most Gen 0 candidates will lose.
That is the point. The frozen CI is a strong baseline that has
given a generation of deaf children spoken language. Beating it
honestly — on channels, language, preservation, safety, and access
together — would be a real advance. Claiming to beat it on one
favorable number would not.*
