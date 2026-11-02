# Frozen baseline `frozen_bilateral_eCI_v1` — PROPOSED pin (Step 1)

> **Status: PROPOSED PIN — NOT FROZEN.** Holder + independent
> co-approver freeze (GOAL §3.4, §12) is **PENDING**. Human dual
> extraction (§9) is **PENDING**. Nothing in this file is
> gate-deciding until both are done. This file proposes pins
> only where inspected evidence supports them; everything else
> is marked PROVISIONAL or UNPINNABLE below.
>
> **Date:** 2026-11-02. **GOAL:** v2.2 (§3–§6, Appendices A/D).
> **Step 0 source:** `research/step0/Step0-verified-bibliography.md`
> (read in full; rows cited as E/O/D/Ch + number).
>
> **Model routing (GOAL §9):** Step 1 worker requested
> **Sol 6.1, high**; actual runtime model
> **`muse-wonder-full-1.0` fallback** (Sol 6.1 unavailable in
> this runtime) at the same effort split. Substitution
> disclosed per §9 rule 3. No claim in this file is Sol 6.1 work.
>
> **Evidence rule applied:** pins come ONLY from Step-0-verified
> rows or NEW sources inspected in this Step 1 pass via
> `web_fetch` of PubMed (E-utilities MEDLINE full abstract
> records) / FDA / ClinicalTrials.gov full records. Search
> snippets were never used as evidence. Abstract-level evidence
> pins as **PROVISIONAL (human extraction pending)**. Missing
> evidence is **UNPINNABLE** + what would pin it. No number,
> DOI, PMID, or NCT in this file was invented.
>
> **New sources inspected in this pass (2026-11-02):**
> N1 Zhuchkova et al. 2026, PMID 42162288 (MEDLINE abstract);
> N2 Friis et al. 2023, PMID 37441990 (MEDLINE abstract,
> re-inspected; = Step 0 E1); N3 Fortnum et al. 2001,
> PMID 11546698 (MEDLINE abstract; = Step 0 E2c);
> N4 Geers et al. 2009, PMID 19155289 (MEDLINE abstract);
> N5 WHO *World Report on Hearing* landing page
> (who.int/publications/i/item/9789240020481 — publication
> identity only; grade table is in the report PDF, not in the
> inspected page text). Failed inspections are logged in §7.

## Contents

1. P0 definition (pinned / provisional / unpinnable)
2. Appendix D tables D1–D4 + epidemiology arithmetic (formulas)
3. Frozen device / pathway contents (§3.4)
4. Frozen outcome ranges: G2, G3a, G3b, G5
5. Evolving-standard sensitivity comparator
6. What would pin every UNPINNABLE cell (checklist)
7. Inspection log (this pass)

## 1. P0 definition

### 1.1 Jurisdiction and year — PROPOSED pin

**P0 jurisdiction: United States. P0 birth year: 2022.**

Justification: GOAL §3.1 defaults to the U.S. with the year
pinned in Step 1. 2022 is the only U.S. birth year for which
Step 0 located the correct primary source — CDC EHDI Hearing
Screening & Follow-up Survey (HSFS) 2022, incl. the
Type-and-Severity table (Step 0 E2a: severe 71–90 / profound
91+ × laterality over screened births). Pinning the year to
2022 therefore pins P0 to a *named, locatable* denominator
source rather than to a year with no located source. The
2022 numerator itself is **UNPINNABLE today** (§2, D1):
the HSFS PDFs fetched binary in both Step 0 and this pass
with no text extractor in the runtime, and `cdc.gov`
returned 403. Choosing 2022 does not manufacture the number;
it fixes *which* human PDF extraction will supply it.

Sensitivity: if the holder + co-approver prefer the most
recent HSFS year available at freeze, the year changes and
D1 must be re-extracted for that year. Jurisdiction and year
must never be changed silently (§3.4 comparator-drift rule).

### 1.2 Severity criterion — definition pinned, grading refs UNPINNABLE

**Pinned (from GOAL §3.1, unchanged):** better-ear threshold
≥70 dB HL equivalent, averaged 0.5–4 kHz; asymmetry >15 dB
flagged, still included, analyzed separately.

**WHO grading: UNPINNABLE in this pass.** The WHO *World
Report on Hearing* (2021) landing page was inspected (N5)
and confirms the publication's identity, but the grade table
itself is inside the report PDF, which was not text-inspected
here. No WHO dB bands are quoted in this file. *What would
pin it:* human extraction of the grade table (better-ear
0.5–4 kHz average; severe / profound / complete bands) from
the report PDF, with table/page locator, recorded as a new
version of this file.

**ASHA grading: UNPINNABLE in this pass.** ASHA's
degree-of-hearing-loss page returned a 404 body on fetch
(2026-11-02), and the ASHA Audiology Information Series PDF
(`ais-type-degree-and-configuration-of-hearing-loss.pdf`)
fetched as binary (230,873 bytes) with no text extractor in
the runtime — the same blocker as Step 0 E2a. Search-result
text suggesting "Severe 71–90 / Profound 91+" was **not**
used: snippets are never evidence. *What would pin it:*
human extraction of that ASHA PDF (Clark 1981 bands as
reproduced by ASHA), with page locator.

Consequence: until one grading source is human-extracted,
P0's "≥70 dB HL equivalent" is operational only as written
in §3.1 (a numeric cut), and no WHO/ASHA grade *label*
(e.g. "severe", "profound") may be attached to a P0 child
from this file. Note the boundary risk explicitly: if the
extracted ASHA bands are severe 71–90 / profound 91+, then
a ≥70 dB cut and a ≥71 dB cut differ by the 70 dB stratum;
the freeze must state whether P0 is ≥70 or ≥71 and must not
drift between them. That decision is for the freeze, on
extracted evidence — it is not made here.

### 1.3 ABR correction approach — approach pinned, numeric corrections UNPINNABLE

**Pinned approach (from GOAL §3.1):** pre-behavioral
thresholds are click/toneburst ABR *estimated* HL (eHL) with
correction factors stated; behavioral (VRA / play audiometry)
when developmentally available. Formally, per frequency f:

```text
eHL(f) = ABR threshold(f) [dB nHL] − correction(f) [dB]
PTA_eHL = mean{ eHL(0.5), eHL(1), eHL(2), eHL(4 kHz) }
P0 severity met iff better-ear PTA_eHL ≥ 70 dB
```

**Numeric correction(f) values: UNPINNABLE in this pass.**
A PubMed E-utilities search for the Stapells tone-evoked ABR
threshold-estimation meta-analysis returned no items under
the query used, and no inspected full record in Step 0 or
this pass states frequency-specific nHL→eHL corrections.
Correction values circulating in secondary/slide sources
were not inspected to the required standard and are **not**
reproduced here. Inventing them would move children across
the 70 dB boundary invisibly.

*What would pin it:* one named protocol/guideline full text
(e.g. a national early-assessment guidance or the Stapells
meta-analysis full text) human-extracted for: stimulus
(click vs toneburst), transducer, corrections at
0.5/1/2/4 kHz for infants, and the stated normal cut-off.
Until then, any cohort scored against P0 must report raw
dB nHL by frequency *alongside* eHL, so the correction can
be applied retroactively once pinned.

### 1.4 Congenital criterion, exclusions, strata — pinned as definitions

Unchanged from GOAL §3.1–§3.2 (definitions, not numbers):
congenital = present at birth per newborn screening +
diagnostic ABR ≤3 months (EHDI 1-3-6), OR prelingual onset
≤6 months with congenital etiology (genetic / cCMV /
anatomic). Later-identified and progressive converters
(EVA, cCMV progression) are entry-time strata, never
silently pooled into P0-at-birth. Exclusions from the
primary analysis (reported, never hidden): conductive/mixed
loss with normal bone conduction; transient ABR failure
resolving by 6 months. Children with additional
disabilities are included and stratified; the "~30–40%"
fraction in §3.1 remains **UNVERIFIED** (Step 0 E3b) and is
not pinned here (see D2 note). All §3.2 strata (etiology,
phenotype/anatomy, syndromic flags, host/developmental,
decision-time, entry-time, context) carry over unchanged.
Every percentage downstream must show numerator, denominator
(P0 or named sub-denominator), jurisdiction (U.S.), and era
(2022 births, unless a stratum table names another cohort).

## 2. Appendix D tables D1–D4 + arithmetic

Rules (GOAL Appendix D): primary sources with ranges; no
single-cohort point estimate as a universal. Formulas below
are explicit so `verify/` can lock the arithmetic later;
**no code is written in Step 1** and no formula output is
asserted until its inputs are pinned.

### D1. Congenital bilateral ≥70 dB incidence — NUMERATOR UNPINNABLE

| Cell | Value | Status | Source |
|---|---|---|---|
| U.S. births, 2022 (denominator frame) | — | UNPINNABLE here | Not inspected in Step 0/Step 1; use HSFS screened-births denominator from the same table, not an external births total, once extracted |
| Bilateral severe (71–90) + profound (91+), by ear, 2022 births | — | **UNPINNABLE** | CDC EHDI HSFS 2022 Type-and-Severity table: located (Step 0 E2a), fetched binary, no extractor; `cdc.gov` 403 in this pass; CDC Stacks PDF 403; mirror hosts unreachable/non-authoritative (§7) |
| All congenital HL (any degree/laterality) | — | UNPINNABLE here | Same HSFS extraction owed; must be reported *separately* from the ≥70 dB bilateral cut (Appendix D) |
| Morton & Nance 2006 | — | UNUSABLE for P0 cut | Step 0 E2b: no abstract on PubMed record (PMID 16707752); broad definitions; cannot be relabelled bilateral ≥70 dB |

**Non-substitute context (never a D1 input):** Fortnum
et al. 2001 (PMID 11546698; DOI 10.1136/bmj.323.7312.536;
PMC48157), re-inspected this pass (N3): UK children born
1980–1995, better-ear **>40 dB** (0.5–4 kHz) permanent
childhood hearing impairment, N=17,160. Prevalence 0.91/1000
(95% CI 0.85–0.98) at age 3 rising to 1.65 (1.62–1.68) at
9–16 y; ascertainment-adjusted 1.07 and 2.05. UNHS yield
~1/1000 with 50–90% more diagnosed by age 9. This is
**>40 dB, UK, 1980–1995 births, prevalence by age** — it
bounds the broader PCHI population and proves birth
incidence ≠ lifetime P0 (progressive entry), but it has no
≥70 dB split in the inspected abstract and **must not**
be substituted for, scaled into, or averaged with a U.S.
2022 bilateral ≥70 dB numerator. Status: PROVISIONAL
(abstract-level; PMC48157 full text not line-inspected).

**Arithmetic (to be locked by `verify/` once inputs exist):**

```text
N_P0(2022)      = N_bilateral_severe + N_bilateral_profound
                  (HSFS Type-and-Severity, by-ear table,
                   sensorineural rows only — see caveat)
Incidence_P0    = N_P0 / N_screened_births_HSFS        [per birth]
Incidence_1000  = 1000 × Incidence_P0                 [per 1000]
Range           = [low, high] from HSFS reporting bounds:
                  low  = documented cases only
                  high = low adjusted for loss-to-follow-up /
                         undocumented-diagnosis fraction as
                         reported in the same HSFS release
                  (method stated at extraction; never a
                   silently chosen inflation factor)
```

Caveats the extractor must resolve from the table itself:
(i) HSFS type rows (sensorineural vs conductive/mixed/
auditory-neuropathy) — P0 counts SNHL only, so the SNHL row
definition governs; (ii) "by ear" bilateral counting vs
better-ear PTA — the mapping to §1.2's better-ear ≥70 dB
rule must be stated, not assumed; (iii) 70 dB exactly falls
below a 71–90 "severe" band — see the ≥70 vs ≥71 freeze
decision in §1.2. Until D1 exists, **all P0 head-counts,
coverage percentages, and the §1.2 "tens of newborns/year"
OTOF gloss stay blank** (Step 0 §5 item 2; E3a-iv/O1d).

### D2. Etiologic fractions — cohort values PROVISIONAL; P0 fractions mostly UNPINNABLE

All values are Step-0 rows E1/E3 (abstract-level) unless
noted. Denominators differ by row and must never be pooled.

| Etiology | Inspected value (denominator) | P0 fraction | Source |
|---|---|---|---|
| *SLC26A4* / Pendred / EVA | 14/100 (14% = 13% Pendred + 1% non-syndromic), Danish pediatric CI recipients, implanted 2020–2022, Aarhus | **UNPINNABLE** (CI-selected, population-specific; no U.S. P0 source inspected) | PMID 37441990 (E1, E3a-ii; re-inspected N2) |
| *GJB2*/DFNB1 | "Most common" within non-syndromic 21/100 — **no numerator in abstract**, Danish CI cohort. Australian exome cohort: *GJB2/6*-only testing positive 22/106 (21%) vs exome diagnosis 59/106 (56%), bilateral moderate–profound, births 2016–17 | **UNPINNABLE** by ancestry (ancestry figures snippet-only in Step 0; Downie 2021 errata unchecked — Step 0 A15) | PMID 37441990; PMID 31827275, DOI 10.1038/s41431-019-0553-8 (E3a-i) |
| Congenital CMV | Grosse 2008 review: ~14% of cCMV children develop any SNHL; 3–5% bilateral moderate-to-profound; 15–20% of all bilateral moderate-to-profound SNHL attributable to cCMV. Danish: cCMV-DNA+ 23/100 CI recipients | **UNPINNABLE** at ≥70 dB-at-birth cut (Grosse is broader: moderate+, includes progression → upper-bound guide only; do not average the two denominators) | PMID 17959414 (E3a-iii); PMID 37441990 |
| *OTOF* | No % endorsed. GeneReviews NBK1251 blocked (reCAPTCHA) in Step 0; "1–8%"-style figures snippet-only with shifting denominators | **UNPINNABLE** | E3a-iv / O1d |
| Unknown after workup | 31/100 (31%) Danish CI cohort (workup scope per that cohort; ~half of unknowns had inner-ear malformations, n=16) | UNPINNABLE for P0 under a *defined modern* workup (panel/exome scope + CMV timing must be stated per §3.2) | PMID 37441990 (N2) |
| Hereditary (any) / syndromic / TORCH (Danish, context) | 44% hereditary; 23% syndromic; 25% TORCH-associated — **categories overlap, do not sum** | Not P0 fractions (CI-recipient mix) | PMID 37441990 (E1) |
| Additional disabilities | No primary-source range inspected ("~30–40%" unverified) | **UNPINNABLE** | E3b; owed: Gallaudet Annual Survey primary report or defined infant cohort + instruments + ascertainment age |

Danish-cohort use-note (E1, skeptic A2): the abstract's
"23 congenital + remaining 47 progressive" sums to 70, not
100; the other 30 are unexplained in the abstract. Do not
quote "47" against N=100. Friis 2023 is a CI-recipient
etiology mix — **not incidence, not a P0 denominator**.

**Arithmetic (per etiology e, once a P0-like source exists):**

```text
f_e            = N_e / N_denominator(e)     [denominator named per row]
Range_e        = [ min over eligible cohorts, max over eligible cohorts ]
                 (never a pooled point from one cohort)
N_e(P0, 2022)  = f_e_range × N_P0(2022)     [only if f_e's denominator
                                             is P0-like; otherwise blank]
Overlap rule:  sum_e f_e need not = 1 (overlapping categories,
               e.g. Danish hereditary/syndromic/TORCH) — report
               overlaps, never force a partition.
```

### D3. Anatomic / phenotype fractions — UNPINNABLE

| Phenotype (§3.2) | Value | Status |
|---|---|---|
| Cochlear nerve deficiency/aplasia (MRI-graded) | — | UNPINNABLE: no inspected source in Step 0/Step 1 |
| Cochlear malformations (common cavity, IP I–III, EVA) | Danish context only: inner-ear malformations in n=16 of 31 unknown-etiology CI recipients (PMID 37441990, N2) — not a P0 fraction, EVA not separable | UNPINNABLE for P0 |
| ANSD (present OAE/CM, absent/abnormal ABR) | — | UNPINNABLE: no inspected P0 source; *OTOF*-ANSD overlap unquantified (E3a-iv) |
| Normal anatomy (remainder) | — | UNPINNABLE until rows above exist with a common denominator |

*What would pin D3:* a P0-like (congenital bilateral
≥70 dB, population-ascertained, not CI-selected) cohort
with MRI grading + ANSD criteria stated, human-extracted
in full. CI-recipient anatomy mixes (like Friis) overstate
implantable anatomy by selection and must be labelled as
such if used at all.

### D4. Per-family eligible numerators / portfolio union — UNPINNABLE until D1–D3

```text
Eligible_F     = sum over strata s in F's eligibility set of N_s(P0)
Coverage_F     = Eligible_F / N_P0(2022)          [range from D1/D2 ranges]
PortfolioUnion = | union over winning families F of Eligible_F |
                 (stratum-level union; double-counted strata
                  counted once — inclusion–exclusion at the
                  stratum table, never sum of coverages)
```

No D4 number is asserted in Step 1: N_P0 does not exist
yet (D1), etiologic f_e are not P0 fractions (D2), and
anatomic strata are empty (D3). The one label-defined
eligibility that *is* pinned (Step 0 O1b, authoritative
record) is the Otarmeni subset definition — biallelic
*OTOF*, preserved outer-hair-cell function, no prior CI in
the same ear, severe-to-profound/profound SNHL (any
frequency >90 dB HL per USPI §1) — but its P0 *numerator*
stays blank until D1 × an *OTOF* fraction can be computed.

## 3. Frozen device / pathway contents (§3.4)

Granularity rule (§3.4): pin only what literature supports.
"Frozen" below means *proposed-frozen pending co-approval*.

| Element | Proposed frozen content | Status / source |
|---|---|---|
| Laterality & surgery pattern | Bilateral electrical CI; simultaneous OR sequential ≤6 mo apart. **Proportion simultaneous vs sequential: UNPINNABLE** for U.S. P0 — no inspected registry/cohort reports it. Danish context only: the 23 congenital severe-to-profound bilateral children in Friis 2023 were "simultaneously implanted" (abstract wording) — a single-centre Danish practice descriptor, **labelled cohort, not universal**, and not a U.S. proportion | Definition pinned (GOAL §3.4); proportion UNPINNABLE. PMID 37441990 (N2) |
| Arrays | Contemporary arrays, 12–24 contacts, envelope processing (GOAL §3.4). **Lateral-wall vs perimodiolar mix by era: UNPINNABLE** — no inspected source reports an era mix. G1 caution: modern perimodiolar data show gains beyond 8–10 channels (Step 0 Ch1b, Berg 2019, PMID 31067952), so the array mix materially affects the G1 anchor and must be pinned before G1 scoring, with channels-vs-maxima defined | Contact range = GOAL descriptor; mix UNPINNABLE |
| Age at first implant | **Median + IQR: UNPINNABLE.** Best inspected cohort value is a *mean + range*: Friis 2023 congenital severe-to-profound bilateral subset (n=23 of N=100) implanted at **8–14 months, mean 10.5 months**, simultaneously. No median/IQR in the abstract. **Labelled cohort (Aarhus, 2020–2022), not universal**; U.S. P0 median/IQR requires a U.S. cohort/registry full-text extraction | PROVISIONAL cohort mean/range (PMID 37441990, N2); median/IQR UNPINNABLE |
| Label minima (context for age, not the age pin) | Cochlear Nucleus: ≥9 mo (FDA SSED P970051/S172, 2020). MED-EL: ≥7 mo **provisional** (SSED P000025/S134 via mirror, FDA re-pull owed). Advanced Bionics: unverified (12 mo = pointer only). No universal FDA minimum exists; "9–12 mo" is a cohort descriptor, not a label | Step 0 O4a–O4d |
| Hearing-aid trial | A pre-CI hearing-aid trial is part of the frozen pathway (GOAL §3.4; label context: Cochlear 9–24 mo indication requires limited binaural HA benefit, O4a). **Trial duration / fitting / benefit criterion: UNPINNABLE** — no inspected source states a pinnable range. Family F1 caution (§8F): at ≥70 dB, aided audibility often remains insufficient — the HA trial must never be scored as a CI substitute | Presence pinned; dose UNPINNABLE |
| Mapping schedule | **UNPINNABLE** (visits/year, schedule): no inspected source. *Would pin:* manufacturer/clinic protocol or registry visit data, human-extracted, stated as visits in year 1 vs later years | UNPINNABLE |
| Diagnostics (frozen contents, so C0 cannot win by definition) | Standard etiologic workup as routinely ordered: targeted genetics incl. *GJB2* where ordered, CMV testing, imaging — **without** guaranteed rapid turnaround, **without** a pre-committed gene-therapy-first triage rule, **without** a preserved-ear protocol. Turnaround times: UNPINNABLE (no inspected pathway study; Step 0 §4 rapid-sequencing row unverified) | Contents pinned (GOAL §3.4 verbatim intent); turnaround UNPINNABLE |
| Early intervention (frozen contents) | EI referral with **family-chosen modality** (spoken / signed / bimodal as actually received) — *not* assumed spoken-only, *not* assumed sign-free. **Dose (hrs/week) and modality mix: UNPINNABLE** — no inspected source reports U.S. P0 EI dose/modality ranges. *Would pin:* EHDI/Part-C or cohort data with hrs/week + provider type + modality, by stratum | Contents pinned; dose/mix UNPINNABLE |

Consequence for scoring: Families G and H must beat *these*
frozen diagnostics/EI contents on turnaround/triage (G) and
dose/timing (H). While turnaround and dose are UNPINNABLE,
G/H gate cells depending on them read **INSUFFICIENT**, not
PASS — a challenger cannot beat an unmeasured baseline.

**Claim cap (§3.4, carried into this pin):** beating this
frozen baseline but not the evolving-standard comparator
(§5) claims only an *implementation gap*, never a C0 win.
The deciding promotion comparator remains this file.

## 4. Frozen outcome ranges: G2, G3a, G3b, G5

Appendix A requires a frozen reference per gate. Honest
summary: **no absolute frozen outcome range can be pinned
from inspected evidence today.** What exists is relative
(bilateral vs unilateral) and single-cohort evidence,
recorded below as PROVISIONAL context. Absolute SRT dB,
language standard-score, and per-harm rate references for
*bilateral-CI P0 children by window (W2/W3)* are
UNPINNABLE until full-text human extraction of named
meta-analyses/registries. Gate cells needing an absolute
frozen reference therefore read INSUFFICIENT at Step 1.

### G2 Functional hearing (SRT in noise primary; quiet, music, localization secondary)

- **Frozen absolute SRT-in-noise (W3): UNPINNABLE.** No
  inspected meta-analysis reports an absolute SRT dB range
  for bilateral-CI children on an age-valid test.
- **PROVISIONAL relative anchor (abstract-level):**
  Zhuchkova et al. 2026 (N1; PMID 42162288;
  DOI 10.1007/s00405-026-10302-z), systematic review +
  meta-analysis, 50 studies qualitative / 20 in
  meta-analyses, children with congenital/early-onset
  bilateral deafness, BiCI vs UniCI: speech perception in
  noise **SMD +0.70 (p<0.001)**, sound localisation
  **SMD +0.74 (p<0.001)**, favouring BiCI; earlier
  implantation + shorter inter-implant interval → larger
  benefits. This supports *bilateral > unilateral* — i.e.
  it validates the frozen comparator's bilaterality — but
  an SMD vs UniCI is **not** a frozen SRT value and cannot
  anchor Appendix A's "≥3 dB better than frozen" PASS.
  Converting SMD→dB without the full text (per-study tests,
  SDs, ages) would invent numbers. Full-text human
  extraction owed; heterogeneity flagged by the authors.
- Music battery + exact SRT test: **not yet named with
  citations** (Appendix A Step-1 debt) — UNPINNABLE here;
  naming them requires inspected test-validation sources,
  not assertion. W0–W1 remain mechanism-only (no G2 PASS).

### G3a Language, any modality (modality-specific co-primaries; no pooled SD)

- **Frozen within-stratum language range (spoken stratum,
  W2/W3): UNPINNABLE as a bilateral-P0 range.**
  PROVISIONAL context, two inspected abstracts:
  (a) N1: receptive vocabulary **SMD +0.65** favouring
  BiCI over UniCI (relative, heterogeneous — authors note
  greater heterogeneity for language than auditory
  measures). (b) Geers et al. 2009 (N4; PMID 19155289;
  DOI 10.1093/deafed/enn046): 153 U.S. children with CIs in
  auditory-oral programs, mean age 5 y 10 mo;
  age-appropriate scores in 50% (receptive vocabulary),
  58% (expressive vocabulary), 46% (verbal intelligence),
  47% (receptive language), 39% (expressive language);
  younger implantation → higher scores after controls.
  Geers is **spoken-modality, auditory-oral-selected,
  bilaterality unspecified in the abstract, 2009-era** —
  it must not be relabelled a bilateral-P0 frozen range,
  and its percentages must not be converted to SD units.
- **Signed stratum: UNPINNABLE.** No inspected source
  reports ASL-normed outcomes for P0 bilateral-CI children.
  Per §4.2, no pooled SD across incommensurable norms is
  permitted, so the spoken context above **cannot** fill
  the signed cell. Bimodal hierarchy (highest-modality
  score + total conceptual vocabulary) remains to be fixed
  at freeze with stakeholder input.
- *What would pin G3a:* full-text extraction of
  bilateral-specific longitudinal cohorts/meta-analyses
  reporting standard scores (mean, SD, N) by modality
  stratum at W2/W3, with additional-disabilities and EI-dose
  stratification per §3.2.

### G3b Communication autonomy & family outcomes — BLOCKED (do not invent)

**G3b scoring is BLOCKED. All G3b cells read INSUFFICIENT.**
Per GOAL §4.2, G3b stays blocked until a family-reported
communication-autonomy / QoL instrument **and** its MCID
are co-designed with Deaf-community and parent stakeholders
(§9) and committed. **This file does not invent, name, or
shortlist an instrument or MCID.** N1's abstract-level
statement that quality-of-life ratings were "consistently
higher in BiCI users" names no instrument and no MCID and
therefore cannot unblock G3b; it is recorded here only so
it is not mistaken for a G3b pin. A spoken-language gain
with autonomy loss fails (§4.2) — but neither can be scored
until the co-design below is done. PASS, once unblocked,
is NI vs frozen, with superiority only against the
stakeholder-defined MCID (Appendix A).

**Co-design protocol needed to unblock G3b (specification,
not an instrument):**

1. **Panel:** Deaf-community stakeholders (incl. Deaf
   adults with and without CIs), hearing and Deaf parents of
   P0-like children across modality choices (spoken /
   signed / bimodal), plus pediatric otology, audiology,
   early-intervention, and biostatistics members (§9).
   Holder recused from scoring per §12; panel membership,
   eligibility, and dissent handling named in the protocol
   before any instrument discussion.
2. **Construct first, instrument second:** panel defines
   what "communication autonomy" means observably at
   W1/W2/W3 (e.g. domains named by families, in families'
   languages/modalities) *before* reviewing candidate
   instruments, so an off-the-shelf scale cannot smuggle in
   a spoken-only construct.
3. **Instrument requirements (pre-stated):** validated (or
   formally adapted + re-validated) for deaf/hard-of-hearing
   children and for signed as well as spoken home languages;
   family-reported; floor/ceiling ≤20% per Appendix A rule
   or a pre-stated alternative; administration burden stated
   (minutes, language access, cost).
4. **MCID elicitation:** anchor-based (family global-rating
   anchors) with distribution-based sensitivity, elicited
   from the panel and a broader family sample — not set by
   investigators alone. NI margin derived from the MCID,
   stated per window. Trade-off elicitation (§6: what added
   revision/burden risk families accept for stated G2 gains
   *only if* G3b NI holds) is done in the same process.
5. **Commitment:** instrument + version, scoring, MCID,
   NI margin, missing-data rule, and per-window cells are
   written into Appendix A as a new protocol version,
   co-approved (holder + independent co-approver), and
   committed **before** any G3b cell is scored. Until that
   commit exists, every candidate's G3b = INSUFFICIENT and
   no Track-P promotion is possible (§4.2 promotion rule).

### G5 Safety & durability (per-harm NI vs frozen; Appendix C list)

- **Frozen per-harm rates: UNPINNABLE.** No inspected
  registry/meta-analysis in Step 0 or this pass reports
  pinnable pediatric bilateral-CI rates for the Appendix C
  harms (anesthesia <12 mo, meningitis, facial nerve, CSF
  leak/gusher, vestibular loss, residual-hearing loss,
  device failure/revision, MRI incompatibility, etc.).
  A PubMed search for a pediatric CI device-failure/revision
  meta-analysis returned no items under the query used (§7);
  revision percentages in secondary sources were not
  inspected to standard and are **not** reproduced here.
- **PROVISIONAL qualitative anchor only:** N1 (abstract):
  "Surgical and vestibular complications were infrequent
  and did not exceed those reported for UniCI." No rates,
  no denominators, no horizon — unusable as NI margins.
- **Related but non-frozen value (do not misfile as G5):**
  hearing-preservation 78% of ears (95% CI 71–85%), mean
  age 9.68 y, mean PTA 60.48→70.95 dB, 24 studies / 567
  patients (Step 0 E4c; PMID 40052291) describes older,
  better-hearing ears — it is **not** a P0-infant
  residual-hearing or G4/G5 rate and ≠ scala patency.
- *What would pin G5:* CI registry/cohort full-text
  extraction with per-harm numerator/denominator, horizon
  (to 7 y primary; adolescence sensitivity), malformation
  subgroups, and device-era stratification; stress values
  at the 90th percentile / upper 95% CI per §6. Until then
  Appendix A G5 margins cannot be filled and G5 = the
  FMEA-completeness check only (severity × probability
  bands per Appendix C, sources tier-labelled).

### G1 / G4 / G6 frozen references (for completeness)

- **G1:** GOAL point anchor = 8 effective channels
  (spectral-ripple, adult CI/vocoder; sensitivity at 4 and
  10; PASS ≥12 Track P / ≥16 Track R). Step 0 Ch1a/Ch1b
  corrections apply (Friesen, Shannon, Baskent & Wang 2001,
  plateau ~7–8 in 2001-era arrays; Berg 2019 perimodiolar
  gains beyond 8–10). Ripple-to-channels conversion model
  + spread-of-excitation citations: still owed — the anchor
  is **PROVISIONAL** until Step 1's model is published with
  array/task/channels-vs-maxima definitions. Timing NI
  (+20% ITD) remains flagged underived: derive or delete
  at freeze. F/G/H pathway candidates: G1 = NA (pre-declared).
- **G4 (Track-P veto):** frozen reference = bilateral eCI
  itself (residual-hearing preservation, fibrosis grade on
  a named 0–4 scale, SGN survival, scala patency). The
  fibrosis scale is **not yet named with a citation**, and
  post-CI patency % / post-CI AAV efficacy have no direct
  inspected evidence either way (Step 0 E4a/E4b) — G4
  numeric references are UNPINNABLE; Q0 thresholds must be
  pre-defined in Step 2 before Q0 evidence is scored (§8G).
- **G6:** coverage needs D1–D4 (§2); burden needs mapping/
  EI dose (§3); equity metrics (distance, insurance,
  rurality, EHDI loss-to-follow-up) need the same HSFS
  extraction as D1. All UNPINNABLE today except the
  *requirement* itself: stratum table complete + disparity
  bound + timeline stated.

## 5. Evolving-standard sensitivity comparator

Sensitivity comparator only — never the deciding promotion
comparator (§3.4). A candidate beating §3 but not this
section claims an implementation gap, never a C0 win.
Each element lists its Step-0 verification state; unverified
elements are comparator *placeholders*, not facts.

| Element | Evolving-standard content | Verification state |
|---|---|---|
| *OTOF* gene therapy (label subset) | Lunsotogene parvec-cwha (Otarmeni), FDA accelerated approval 2026-04-23 (STN 125874), for biallelic *OTOF* + preserved OHC function + no prior CI in same ear; studied 10 mo–16 y (N=24 treated; 16/20 ≤70 dB HL at Week 24, label set). Gene-therapy-first for this subset is evolving standard, not challenger novelty | VERIFIED (authoritative record), label numbers single-source pending human re-read (Step 0 O1–O2, A5) |
| Other *OTOF* AAV (trial-stage) | Lilly/Akouos AK-OTOF NCT05821959 (Phase 3, recruiting, est. N=48); Sensorion SENS-501 NCT06370351 (Phase 1/2, active-not-recruiting, est. N=12; discontinuation unverified); Otovia NCT05901480 (status UNKNOWN/stale) | Registry-verified (Step 0 O3a–O3c); efficacy not verified |
| Lower label ages | MED-EL ≥7 mo (2025, provisional mirror SSED) vs frozen-era minima; may shift real-world age-at-implant below the Danish 8–14 mo cohort descriptor. Holder + co-approver to decide at freeze whether this triggers a `v2` re-freeze (comparator-drift rule) — **not decided in this file** | PROVISIONAL (Step 0 O4b/B6) |
| Hearing-preservation surgery / arrays | Atraumatic technique, preservation arrays as current care. Pediatric preservation 78% (older ears, E4c) is context only | Comparator class per GOAL §2.2; trial-level contents UNVERIFIED in Step 0 |
| Dexamethasone-eluting arrays; ECochG-guided / robotic insertion | Named in GOAL §2.2/§8A as standard evolution to benchmark Family A against | **UNVERIFIED in Step 0** — no trial record inspected. Must not be scored as available standard until a registry/label record is human-inspected |
| Rapid genomic sequencing where already routine | Rapid panel/exome + CMV + imaging triage with turnaround fast enough to affect the first-implant decision (Family G's core, where already standard). Diagnostic-yield context only: exome 59/106 (56%) vs *GJB2/6*-only 22/106 (21%), Downie 2020 (E3a-i, errata unchecked) | Pathway/turnaround UNVERIFIED (Step 0 §4); yield abstract-level |
| Current-focusing / anatomy-based fitting | Tripolar/phased-array/dynamic focusing: spread narrowing at charge/battery cost, *without consistent* take-home speech-in-noise translation (acute Srinivasan 2013 +2.7/+3 dB vs degraded comparator; take-home nulls; −48% battery, Step 0 Ch2). Comparator evolution to acknowledge, not a frozen win | Abstract-level (Ch2a/Ch2b); clinical adoption unverified |

Sensitivity reporting rule: every Gen 0 score is reported
twice — vs §3 (deciding) and vs this section (sensitivity)
— with divergences named. If an element above is verified
as routine care before the freeze, the freeze decides
explicitly whether it migrates into `v2`; silent migration
is forbidden and `v1` results are preserved (§3.4).

## 6. What would pin every UNPINNABLE cell (freeze checklist)

In dependency order. Each item = human extraction (holder-
independent extractor + sampled audit, §9) unless noted.

1. CDC EHDI HSFS 2022 Type-and-Severity + screened-births +
   loss-to-follow-up (→ D1, G6 equity). Resolve SNHL-row,
   by-ear vs better-ear, and ≥70 vs ≥71 issues (§§1.2, 2-D1).
2. WHO *World Report on Hearing* grade table AND/OR ASHA
   degree bands PDF, with locators (→ §1.2 labels).
3. Named infant ABR protocol full text: nHL→eHL corrections
   at 0.5/1/2/4 kHz (→ §1.3).
4. *OTOF* fraction: GeneReviews NBK1251 Prevalence + one
   P0-like genomic cohort (→ D2, D4, "tens/year" verdict).
   Plus ancestry-stratified *GJB2* (with Downie errata
   check), non-Danish *SLC26A4*, cCMV ≥70 dB-at-birth split.
5. Additional-disabilities primary source with definition/
   instruments/ascertainment age (→ D2, §3.2 strata).
6. P0-like anatomy cohort: MRI CND grades, malformation
   classes, ANSD criteria (→ D3).
7. U.S. bilateral-CI cohort/registry: simultaneous vs
   sequential proportion; age-at-first-implant median+IQR;
   array-type mix by era; HA-trial duration/criterion;
   mapping visits/year; EI hrs/week + modality mix (→ §3).
8. Bilateral-CI outcome full texts: absolute SRT-in-noise
   (named age-valid test) at W3; language standard scores
   by modality stratum at W2/W3 incl. signed-stratum
   ASL-normed data (→ G2/G3a). Start: Zhuchkova 2026 (N1)
   full text — per-study tests/SDs/ages, heterogeneity.
9. Per-harm pediatric CI rates with denominators/horizons/
   malformation subgroups (→ G5 margins + §6 stresses).
10. G3b stakeholder co-design (§4-G3b): instrument + MCID
    committed as new Appendix A version (→ unblocks G3b).
11. FDA re-pulls: MED-EL SSED P000025/S134 from
    accessdata.fda.gov; Advanced Bionics P960058 labelling
    (→ §3 label context, §5 drift decision).
12. G1 ripple-to-channels model + spread citations; timing
    NI derived or deleted; G4 fibrosis scale named (→ App. A).

Until items 1–10 land, this baseline can be *proposed* but
not honestly frozen, and Gen 0 cells depending on them read
INSUFFICIENT. That is the correct Step-1 outcome under the
evidence rules — not a gap to paper over with estimates.

## 7. Inspection log (this Step 1 pass, 2026-11-02)

Inspected (full records): PubMed E-utilities MEDLINE for
PMIDs 42162288 (N1), 37441990 (N2), 11546698 (N3),
19155289 (N4); WHO World Report on Hearing landing page
(N5, identity only). All other numbers above are Step-0
rows cited by ID — see
`research/step0/Step0-verified-bibliography.md` §2.

Attempted, not inspected (hence UNPINNABLE, not evidence):
`cdc.gov/hearing-loss-children/data/` — HTTP 403;
restored-CDC EHDI 2022 page — timeout; CDC Stacks HSFS
PDF (`cdc_133104_DS1.pdf`) — HTTP 403; CDC HSFS mirror
hosts from search results — DNS failure / non-authoritative
(mirrors never used as evidence in any case);
`asha.org/public/hearing/degree-of-hearing-loss` — 404
body; ASHA AIS PDF — fetched binary (230,873 bytes), no
text extractor in runtime. PubMed searches returning no
items under the exact queries used: Stapells tone-evoked
ABR meta-analysis; pediatric CI device-failure/revision
meta-analysis. "No items under this query" is a bounded-
search result, not proof of absence (Step 0 B3 discipline).

*Proposed pin authored 2026-11-02. Requested model Sol 6.1
high; actual `muse-wonder-full-1.0` fallback (header).
Freeze: PENDING holder + independent co-approver (§3.4/§12).
Human dual extraction: PENDING (§9). Next version of this
file supersedes — never silently edits — any cell above.*





