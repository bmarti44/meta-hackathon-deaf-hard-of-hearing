# Q0 verdict — scored ONLY against pre-registered Q0-thresholds.md

> **Model routing (GOAL §9).** Requested route: **Sol 6.1, high**
> (generation-execution worker). Actual runtime model:
> **`muse-wonder-full-1.0` fallback** (Sol 6.1 unavailable in this
> runtime). Substitution disclosed per §9 rule 3. No claim here is
> Sol 6.1 work. **Date: 2026-11-02.** GOAL v2.2.
>
> **Scoring authority:** `research/gen00/Q0-thresholds.md` (written
> BEFORE Q0 scoring) — patency zones (§2.1), AAV-retention zones
> (§2.2), evidence minima (§2.3), composite rule (§3), UNDECIDABLE
> sub-labels (§4). No threshold was moved after seeing Step 3
> results. Inputs: Step 0 E4a–E4d/O1b (post-skeptic bibliography)
> + targeted new inspected search 2026-11-02 (frozen S-Q0a/S-Q0b
> + logged narrowings; PubMed E-utilities full abstracts + CTgov
> API v2 full record only; snippets never evidence). Human dual
> extraction PENDING; human ratification of §2 conventions
> PENDING. Exploratory-after-seen: YES.
>
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.** Whatever Q0
> returns, no Track P promotion is possible at v1, and a Q0 result
> favouring Family G would not promote G.

## Verdict

# Q0-UNDECIDABLE — sub-label: UNDECIDABLE-no-data

Neither Q0-P nor Q0-A has an eligible study reporting its
pre-registered estimand, so neither component can be placed in
any §2 zone and the §3 composite cannot fire. This is the outcome
`Q0-thresholds.md` anticipated (§4 expectation note); naming it
here is a score under fixed thresholds, not a softened failure.

**Sub-label choice, justified.** §4 requires exactly one.
*No-data* is correct because the missing objects are the estimands
themselves: no inspected study reports patency/cannulability
n/N (%) by time-since-implant band (§2.1), and no inspected study
delivers AAV after an established implant+fibrosis course against
a same-study unimplanted comparator with A1+A2 readouts (§2.2).
Neighbouring evidence exists and is characterised below without
changing the sub-label: histology series are eligible-*type* but
report tissue presence/volume instead of the patency estimand
(and are abstract-level, adult, older-device — would be
below-GRADE even as presence evidence); AAV-near-implant studies
are ineligible-sequence designs (would be below-tier by design).
*UNDECIDABLE-unratified* does not apply as the sub-label because
it requires evidence meeting §2.3 — evidence fails first. The
unratified-convention cap is nevertheless live governance: even
had point estimates existed, verdicts under unratified §2 numbers
would be sensitivity-only (protocol §6).

## Three columns — never merged (Q0-thresholds §1)

| Column | Finding under pre-registered rules |
|---|---|
| **Q0-L (label)** | **Established label fact about the studied population.** Otarmeni USPI §1: biallelic *OTOF*, preserved OHC function, **no prior CI in the same ear** (Step 0 O1b, authoritative record; §2.1 confirm LP/P variants; no numeric age limits, O1c — studied 10 mo–16 y). Corroborated at abstract level by the 2026 first-approval summary (PMID 42547733, inspected 2026-11-02) restating the same indication, and by CHORD registry record NCT05788536 (inspected 2026-11-02). Human PDF re-read of label numbers still owed (A5) — that debt concerns efficacy Ns, not the §1 eligibility wording relied on here. Q0-L says nothing about biology in unstudied post-CI ears, in either direction. Biology ≠ permission, and exclusion ≠ impossibility. |
| **Q0-P (patency)** | **Cannot be zoned.** No patency % exists to compare with HIGH ≥80% / INTERMEDIATE >50–<80% / LOW ≤50% (sensitivities 70%/90% likewise inapplicable — there is no point estimate to re-cut, and no 95% interval to test zone-crossing). |
| **Q0-A (post-CI AAV efficacy)** | **Cannot be zoned.** No retention ratio (A1) and no functional dB difference (A2) exist to compare with RETAINED ≥0.80 + ≤10 dB / PARTIAL / LOST ≤0.50 or >20 dB (sensitivities 0.70/0.90, 5/15 dB likewise inapplicable). Single-readout or unstable-ratio fallbacks never arise. |

## Q0-P evidence against §2.1 + §2.3

Estimand required: % of implanted ears (pre-stated age/array/
route/time-band cohort, denominator = all implanted ears incl.
explanted/failed/ungradeable) whose scala tympani is patent/
cannulable for later infusion under a pre-stated access
definition; primary read at the longest time band available at
≥Moderate GRADE; cross-band pooling forbidden.

What was inspected (all abstract-level, all design-set):

- **Seyyedi & Nadol 2014** (PMID 25122600; 28 bones/21 subjects):
  granulomatous reaction 27/28 (96.4%), eosinophil infiltration
  7/28; Seyyedi & Nadol **0–3** per-segment grades basal > distal.
  Establishes near-universal *presence* of tissue response in
  adult, older-device, cochleostomy-era archival bones. Reports
  no cannulatability endpoint, no time-band patency n/N.
- **Kamakura & Nadol 2016** (PMID 27371868; 17 bones): fibrous
  tissue + new bone in 17/17; CNC negatively correlated with
  new-bone % volume, not fibrous %. Volume/distribution is the
  variable; no patency threshold, no infusion test, absolute %
  volumes not in abstract (PMC full text located-not-inspected —
  neither set, held-out manifest §2.9).
- **Hodge et al. 2021** (PMID 34607995; 13 implanted + 4 control
  bones): **otosclerosis only** — cochleostomy → basal obliteration,
  round window → minimal. Route-dependence in a diseased adult
  substrate; CORRECTED against infant generalisation (Step 0 E4a).
- **Madgar et al. 2025** (PMID 40052291; 24 studies/567 patients):
  hearing preservation 78% of ears (95% CI 71–85%), mean age
  9.68 y, pre-op PTA ~60 dB, I²≈80%. Explicitly **not** patency
  and **not** P0-infant evidence (E4c correction). Entering 78%
  into the ≥80% zone test would be exactly the conflation the
  thresholds were pre-registered to prevent; it is excluded from
  Q0-P and logged as an INSUFFICIENT non-substitute row.

Targeted new search (2026-11-02, exact strings in
`extract-FGH.csv` Q0-P gap row): frozen S-Q0a = 2,105 PubMed hits
(broad histopathology yield); logged narrowings
patency/cannulate/infusion = 98 hits, scala-tympani +
patency/ossification/obliteration = 87 hits. Screening in this
pass found tissue-presence/volume histology and revision/
ossification contexts — **no inspected abstract reports the §2.1
estimand at any GRADE**. That is a bounded-search statement
(PubMed, 2026-11-02; Embase inaccessible, EU CTIS/ChiCTR/ANZCTR
not searched — gap disclosed; absence wording never universal).

§2.3 minima for Q0-P: tier *type* met (human histology) but
estimand absent; GRADE ≥Moderate ✗ (VeryLow after adult-archival/
older-device indirectness + abstract cap); human dual extraction
✗ PENDING; denominators for patency ✗; independence/validation ✗
(validation set = 0; all inputs design-set Nadol-lab archival
series). **Fails 4 of 5 minima plus the estimand itself.**

## Q0-A evidence against §2.2 + §2.3

Estimand required: AAV delivered **after** an established implant
(in situ through a pre-stated fibrosis/healing course) vs same-
study unimplanted/sham comparator, same vector/dose/route, with
A1 (transduction retention ratio) **and** A2 (threshold-improvement
difference). Sequence discipline (protocol S-Q0b): only class
(ii) post-establishment delivery counts; (i) before/concurrent and
(iii) unclear never answer Q0-A.

What was inspected (all abstract-level):

- **Pfingst et al. 2017** (PMID 28776202, abstract inspected
  2026-11-02; mature guinea pigs, neomycin-deafened): ears were
  *"inoculated with AAV.Ntf3 and implanted"* — **class (i)
  concurrent**, 18 AAV.Ntf3 + 5 empty-AAV animals (+43 comparison
  ears as reported); 78% of AAV.Ntf3 ears showed better SGN
  survival than deafened controls. Valuable neurotrophin data;
  ineligible for Q0-A on sequence, comparator (implanted controls,
  not unimplanted same-dose AAV), and readouts (SGN/ECAP, not
  A1 retention or A2 threshold restoration). This inspection also
  *resolves without over-claiming* the Step 0 E4b downgrade:
  PMC4674315 itself remains located-not-inspected (do not cite its
  sequence/numbers); PMID 28776202 is a distinct, inspected
  abstract from the same programme whose concurrent sequence is
  explicit in the abstract.
- **Duarte et al. 2018** (PMID 30017876): neonatal mice, Anc80L65
  opsin, mean 74% SGN expression, **no implant at all** — T1,
  below the T2 minimum; an unimplanted-neonatal transduction %
  cannot form a post-CI retention ratio.
- Remaining narrowed-set abstracts (13 hits for `"cochlear
  implant" AND "adeno-associated"`, all screened): optogenetic-
  vector work without established electrical implants (e.g.
  PMIDs 37081855, 32865750), neurotrophin/implant-health reviews
  and methods (32331858, 34883366), label/approval summary
  (42547733) — classes (i)/(iii) or non-primary. Frozen S-Q0b
  broad yield = 192 hits. CHORD (NCT05788536) treats only
  label-eligible (no-prior-CI) ears by design and therefore
  cannot answer Q0-A. No human post-CI AAV data are asserted to
  exist. Bounded search: PubMed + CTgov CHORD record,
  2026-11-02; Embase/CTIS/ChiCTR/ANZCTR gap disclosed.

§2.3 minima for Q0-A: tier/design ✗ (no T2 established-implant
study); GRADE ✗; human dual extraction ✗; per-arm N for the
estimand ✗ (no eligible arms); independence/validation ✗.
**Fails all five.** The immunity caveat (§2.2) is moot: with no
first-exposure post-CI efficacy, G4-AAV re-dosing remains a
separate presumptive FAIL for AAV-using challengers.

## Composite (§3) and mandatory sensitivities

§3 row 4 applies verbatim: *evidence below §2.3 minima for either
component needed to place it → Q0-UNDECIDABLE.* Rows 1–3
(NO-FORECLOSURE / FORECLOSURE / PARTIAL) each require at least one
zoned component at ≥Moderate GRADE; none exists. Sensitivities
(70%/90%; 0.70/0.90; 5/15 dB) are **inapplicable, not failed**:
a sensitivity analysis re-cuts an estimate, and there is no
estimate. Headline therefore carries no bracketed provisional
zones — at Low GRADE §4 would permit bracketed zones *if point
estimates existed*; presence fractions (27/28, 17/17) and the 78%
preservation rate are not point estimates of the Q0 estimands and
must not be dressed as `[LOW]`/`[HIGH]` bracketed zones.
Decision-time note: nothing here is back-dated as knowable at
implant-decision time beyond Q0-L itself.

## Binding consequences (§4) — applied in Gen 0 scoring

1. **The preservation dilemma remains a question, not a premise.**
   Neither "CI forecloses gene therapy" nor "sequencing easily
   solves it" may be asserted. In `score-G.md`, G claims only its
   measured cells (diagnostic yield as provisional signal; all
   pathway consequences INSUFFICIENT) and is neither credited
   with an established "preserved biological option" nor penalised
   as if foreclosure were disproven.
2. **All Q0-dependent cells read INSUFFICIENT**: G4 scala-patency
   component (all candidates), G's option-preservation claim in
   its biological arm, and the Q0-P/Q0-A rows in
   `extract-FGH.csv`. Q0-L remains separately reportable as above.
3. **Ranked gap / handoff study designs** (paper-only designs,
   §5.1 deliverable — in the order that unblocks the composite):
   a. *Q0-A decider (highest leverage, no eligible study exists):*
      T2 mature/deafened large- or small-animal study per §2.2 —
      implant + pre-stated fibrosis course, then AAV (named
      capsid/promoter/transgene, vg/ear + volume + route) vs
      same-study unimplanted comparator; blinded A1 cell counts +
      A2 ABR/PTA improvement; per-arm N with animal as unit;
      SYRCLE-complete; non-inventor replication pre-committed.
   b. *Q0-P decider:* prospective patency series per §2.1 —
      modern arrays, insertion route recorded, pre-stated blinded
      access definition (surgical cannulation at revision/explant,
      or validated imaging grade), n/N by time-since-implant band
      with explanted/ungradeable ears retained in N; pediatric
      transportability addressed head-on rather than by adult-
      archival analogy. Human full-text extraction of PMC5018452
      volumes would sharpen (not replace) this design.
   c. *Cheap completions:* human dual extraction of E4a full texts
      + USPI label numbers (A5); multi-registry re-run
      (CTIS/ChiCTR/ANZCTR) + Embase for the absence claims;
      ratification or replacement of §2 conventions by H-1…H-3 +
      stakeholders so a future decider study lands on ratified
      numbers.
4. UNDECIDABLE does not block the rest of Gen 0 screening and is
   not by itself a dry round (§4.4, GOAL §7 rule 5).
5. Re-opening only on new §2.3-meeting (validation-side) evidence
   or threshold re-freeze — never by rewording (`seen` discipline).

## Extraction pointers

Rows: `extract-FGH.csv` candidates `Q0-L` (1), `Q0-P` (5),
`Q0-A` (3), all `verdict_proposed` INSUFFICIENT except Q0-L at
PROVISIONAL-SIGNAL under the agent-only cap (label fact stated
above; the CSV verdict vocabulary has no "record-established"
state and PASS is forbidden for agent-only rows). `gate_table.py`
skips Q0 rows by design (adapter TRACK map) — Q0 is decided by
this file under Q0-thresholds, not by the gate matrix.
