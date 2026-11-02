# Gap attack P0 denominator — round 1 (Step 5 §6 item 3)

> **Requested route:** Sol 6.1. **Actual runtime model:**
> `muse-wonder-full-1.0` (probe 2026-11-02: sol-6.1 route
> rejected/not in catalog), disclosed per GOAL §9 rule 3.
> **Date:** 2026-11-02. **Type:** promotion-blocking-gap
> attack round 1 (GOAL §7 rule 4). Agent pre-extraction
> only; human dual extraction still pending. Nothing here
> edits any frozen/proposed-pin file; §7 is a proposal.
>
> **Evidence rule for this file:** inspected records only
> (`web_fetch` full API JSON / MEDLINE abstracts / PMC XML,
> and PDFs saved by `web_fetch` then text-extracted locally
> with `pypdf`, see §2-R0). Search snippets were pointers to
> URLs only and are never cited as values. No number is
> invented; every derivation was executed in Python against
> `verify/epi_arithmetic.py` conventions.

## 0. Verdict

**D1 moves, P0 does not pin.** The CDC EHDI table that
Steps 0–1 could not read is now read (§2-R0 is the new fact
that changes everything below). It yields a documented,
HSFS-convention numerator/denominator (§3), but it does
**not** yield the frozen P0 quantity — better-ear ≥70 dB
children — because HSFS publishes by-ear marginals only.
So:

| Quantity | Status after this attack |
|---|---|
| HSFS documented bilateral SNHL severe+profound, ear-averaged (§3) | **PROVISIONAL** (agent-extracted, arithmetically reconciled; human visual re-read owed) |
| D1 as defined by pin P02 (better-ear ≥70, congenital, at birth) | **still UNPINNABLE** from published HSFS marginals; bounds in §3.3 |
| D2 *OTOF* P0 fraction | **still UNPINNABLE**; first inspected primary fractions now on record (§5), none P0-like |
| D2 additional-disabilities P0 fraction | **still UNPINNABLE**; first inspected primary cohort value now on record (§6), not P0-like |
| D3 / D4 | unchanged **UNPINNABLE** (dependency chain U06 intact) |

The honest one-line summary for any coverage use:
**810 documented ear-averaged children-equivalent is a
counting convention, not 810 P0 children** — it exceeds the
logical maximum possible both-ears-≥71 count (804, §3.3),
which proves the two quantities differ. G6 coverage cells
therefore remain INSUFFICIENT.

## 1. Inputs read

- `research/Step5-decision-no-winner.md` §6 item 3 (this
  attack's charter) and §5.4 (D1 UNPINNABLE consequence).
- `research/step0/verify-epidemiology-q0.md` claims 2, 3a-iv,
  3b, and its §5 owed-extractions list (items 1–3 are the
  three targets here).
- `research/frozen_baseline/frozen_bilateral_eCI_v1.md` §2
  (D1–D4 arithmetic + the three extractor caveats: SNHL row,
  by-ear↔better-ear mapping, ≥70 vs ≥71) and
  `Step1-pin-summary.md` §§2–4 (P01/P02/P05; U01/U04–U06).
- `verify/epi_arithmetic.py` D1–D4 range conventions
  (`None` = UNPINNABLE propagates; no substitute points).

Routes Steps 0/1 already tried and **not** repeated as if
new: `cdc.gov` landing page (403), archive.cdc.gov PDF
fetch without an extractor, RestoredCDC mirror landing
page, GeneReviews HTML (reCAPTCHA), Gallaudet via secondary
citations only. Every route in §2 is one they did not try
or could not complete.

## 2. Routes attacked (each inspected or failure-recorded)

### R0 — PDF extraction capability probe (NEW, decisive)

Step 0 recorded `pdftotext`/PyMuPDF/PyPDF2/pdfplumber
absent. Re-probed 2026-11-02 in this runtime: still absent,
**but** `pypdf` 6.21.4 installs from the local pip cache
into `/tmp/pylibs`, and `web_fetch` saves binary PDFs to
disk. Archive.cdc.gov PDFs therefore became inspectable
primary text. All CDC numbers in §3 come from
`pypdf` layout-mode extraction of:

- `12_2022_HSFS_Type-and-Severity.pdf` (6 pp., Aug 2024) —
  the D1 target table;
- `01_2022-HSFS_Data-Summary.pdf` (denominator + follow-up);
- `2022-Annual-EHDI-Data.pdf` (same summary, corroborating);
- `12_2021-HSFS_Type-and-Severity-Table.pdf` (replication).

Extraction caveat, stated once: the rotated type labels
(Sensorineural/Conductive/Mixed/Type Unknown/Auditory
Neuropathy) on p.3 do not extract. Block identity is
**inferred** from (i) the p.6 type order and (ii) exact
arithmetic matches — Conductive block sums to 288.0,
Mixed to 324.5, Auditory Neuropathy to 150.5
children-equivalent, each exactly the p.6 bilateral
numerator; all five blocks' ear sums reproduce the printed
Totals by Ear (3,518 R / 3,510 L) and by Child (3,514)
exactly (§3.1). A human visual confirmation of block order
is still owed and would take minutes; until then SNHL-row
identity carries the PROVISIONAL label. Two internal PDF
inconsistencies found, neither used: p.5 chart table lists
Bilateral numerator 3,408/Unilateral 2,050 against the
p.3/p.4 totals 3,520/2,104; p.6 Type-Unknown bilateral
prints 150.5 (duplicating the AN value) against p.3 block
sum 418.5. This file relies only on the p.3 detailed table,
which is internally consistent to the unit.

### R1 — data.cdc.gov Socrata catalog API (NEW: dead end)

Inspected in full via catalog API
(`api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov`):
`q=EHDI` → 0 results; `q=hearing loss children` → 0;
`q=hearing` → 10 hits, all occupational/DHDS/Household
Pulse (e.g. "Trends in Worker Hearing Loss…"). Unscoped
`q=hearing` returns municipal code-enforcement "hearings".
**Conclusion: no EHDI/HSFS dataset exists on Socrata.**
HSFS is PDF-only. (The CDC data-portal metastore endpoint
tried returned HTTP 404.)

### R2 — CDC pages via alternative hosts (mixed)

- `cdc.gov/hearing-loss-children/data/…` — HTTP 403 again
  (recorded, not retried to death).
- `stacks.cdc.gov/view/cdc/154437/…DS1.pdf` (2021 national
  summary on Stacks) — HTTP 403 on fetch. Stacks search
  hits (pointers only) show Stacks holds the same HSFS
  *national summaries* (2007–2021, e.g. cdc_111819/154437),
  i.e. no type-and-severity table beyond what R0 extracted
  from archive.cdc.gov. Route documented; no added value.
- `archive.cdc.gov` — **worked** (R0). This is an official
  CDC archive host, not a third-party mirror; the
  RestoredCDC/`chiachoob` mirrors found by search were used
  as URL pointers only, never as sources.

### R3 — NCHAM / InfantHearing data tables (dead end)

Search located NCHAM webinar transcripts and slide decks
re-presenting CDC pie charts (degree/laterality shares,
2018–2020 era) and the NCHAM book. No independent
NCHAM-published severity×laterality×type table with
numerators was located; their numbers are CDC HSFS
re-presentations, so they cannot triangulate HSFS — they
*are* HSFS, at lower resolution. Not used.

### R4 — State EHDI report triangulation (1 state, inspected)

Michigan EHDI Program Report 2013 (2007–2011 data, 49 pp.,
extracted with pypdf; Tables 6/8, p.23). Child-level
classification (degree on 0.5–4 kHz average; ASHA bands
identical to HSFS): permanent bilateral
moderately-severe-to-profound (≥56 dB) prevalence
**0.5 per 1,000 live births** (2007–2011 pooled; yearly
0.4–0.5 in the visible Table 8 rows); permanent sensorineural
(all degrees/orientations) 1.1/1,000; auditory neuropathy
excluded from degree analysis. Uses in §3.4: a child-level
≥56 dB rate must exceed any ≥71 dB rate, and it does.
Limits: one state, 2007–2011, all permanent types pooled in
the ≥56 cell, degree definition per child (ear rule not
stated in extracted text). Triangulation, never a D1 input.

### R5 — Published newborn-screening cohorts via PubMed

Full MEDLINE abstracts inspected (E-utilities). Yields:
Antoni 2016 (PMID 26520479, Île-de-France, 27,885 births,
AABR 35 dB): severity mix reported as % of hearing-impaired
children (severe 12%, profound 29%, moderate 59%; 25%
normalized by end of follow-up) — the abstract's "bilateral
hearing loss in 0.63% of infants" cannot be reconciled to a
permanent bilateral ≥70 birth incidence without the full
text (transient inclusion evident), so **no number is taken
from it**. Fortnum 2001 full text re-attacked two ways:
PMC XML (`PMC48157`) returns front-matter only
("publisher does not allow downloading of the full text in
XML form"); EuropePMC `fullTextXML` returns HTTP 500. Its
≥70 child-level severity split therefore remains
uninspected — Fortnum stays quarantined context exactly as
Step 1 left it. No U.S. cohort abstract with a child-level
bilateral severe/profound per-1,000 was found in the
bounded searches run (queries in working log; absence here
is absence in this search, not proof of none).

### R6 — *OTOF* + additional disabilities via PubMed/PMC

§§5–6. Includes two more documented failures: Downie 2020
gene-level table (`PMC7171096`) — PMC XML is front-only,
EuropePMC `fullTextXML` HTTP 500 (twice), PMC OA service
HTTP 404; GeneReviews `NBK1251` — HTML and the
`/pdf/Bookshelf_NBK1251.pdf` endpoint both return the
reCAPTCHA interstitial on `ncbi.nlm.nih.gov`, so
GeneReviews Prevalence text remains uninspected (snippet
copies on mirror hosts were not used as evidence).

## 3. D1 — what the 2022 HSFS table actually pins

### 3.1 The table (inspected, p.3; ASHA bands p.1)

Bands: Moderately severe 56–70, **Severe 71–90, Profound
91+** dB HL. Respondents providing type/severity data: 55
(49 states, 5 territories, 1 district). Total reported
D/HH children 6,272; with type/severity 6,026 (246 later
resolved to typical hearing). Bilateral 3,520 children
(by CDC's ears→children averaging, incl. 6 unknown-ear),
unilateral 2,104, laterality unknown 402.

Sensorineural block, bilateral ears (R/L), the D1 rows:

| Band | Right | Left | Ear-avg "children" |
|---|---|---|---|
| Moderately severe (56–70) | 293 | 292 | 292.5 |
| **Severe (71–90)** | **237** | **259** | **248.0** |
| **Profound (91+)** | **567** | **557** | **562.0** |
| Unknown severity | 58 | 54 | 56.0 |

(full block: Slight 44/39, Mild 566/559, Moderate 573/567;
block ear sums R 2,338 / L 2,327 → 2,332.5 children-equiv.,
vs p.6 SNHL bilateral 2,336 with unknown-ear cases added.)
CDC's printed method (p.3 footnote, p.4): *"to translate
ears to children, we take the average of both ears."*

### 3.2 Documented numerator / denominator / rate

Executed arithmetic (`epi_arithmetic.d1_*`):

- `N_severe + N_profound` (frozen §2 formula, applied to
  CDC ear-averages) = 248 + 562 = **810 children-equivalent**.
- Denominator (Data Summary p.2): screened
  **3,547,774** of 3,616,776 occurrent births reported by
  the same 55 respondents (98.1%).
- Rate = **0.23 per 1,000 screened** (0.228; 0.224 per
  1,000 births). Profound-only 0.158/1,000 screened.
- All-D/HH separate cell (Appendix D requires reporting
  separately): documented **6,272 confirmed D/HH,
  1.7 per 1,000 births** (CDC's own prevalence line).
- 2021 replication (same method, 52 respondents): SNHL
  bilateral severe ear-avg 241.0, profound 531.5, sum
  **772.5** — same order, no rate computed (2021 screened
  denominator not extracted in this pass; do not borrow
  2022's).

### 3.3 Why 810 is not N_P0 (the better-ear problem)

Pin P02 requires better-ear ≥70 dB, i.e. **both** ears ≥71
in HSFS bands (the ≥70-vs-≥71 one-dB seam is the least of
the problems). HSFS gives only per-ear marginals:
right ears severe+profound = 804, left = 816, over
≈2,332.5 bilateral SNHL children-equivalent. The joint
both-ears count is bounded only by Fréchet:
`max(0, 804+816−2332.5) = 0 ≤ N_both ≥71 ≤ min(804,816) = 804`.
The lower bound is clinically absurd and mathematically
correct — the marginals alone cannot distinguish "mostly
symmetric severe/profound" from pathological pairings.
Note the ear-average (810) **exceeds** the both-ears
maximum (804): averaging ears is a bookkeeping convention
for totals, not a joint-severity count. Conversely
at-least-one-ear ≥71 lies in [816, 1,620]. Neither bound
pins P0. Additional non-identity with P0, each documented
in the same release: (i) 56 bilateral SNHL
children-equivalent are unknown-severity, 418.5 bilateral
children-equivalent are type-unknown, 402 children are
laterality-unknown — allocation unknown; (ii) cases are
*documented diagnoses*, and **44.8% (29,188/65,128)** of the
refer pool had no documented diagnosis (LFU/LTD 34.0%) —
documented count is a floor for diagnosed incidence, not
incidence; (iii) HSFS does not separate congenital-at-birth
from early-diagnosed progressive in this table (403
"additional cases" e.g. late-onset are reported elsewhere,
excluded here, but the 6,272 are not certified
congenital-only); (iv) 1.9% unscreened.

Completeness sensitivity (frozen §2 range method, stated
assumptions, **not** proposed pins): screened-only
adjustment 810/0.981 ≈ 826; missing-at-random diagnosis
adjustment 810/0.552 ≈ 1,468 ear-averaged
children-equivalent — the MAR assumption is almost
certainly false upward (no-documented-diagnosis is enriched
for typical hearing/transient), so 1,468 is an illustrative
ceiling on a convention, still not a better-ear count.
**Proposed D1 range is therefore two-layer (§7):**
documented ear-averaged [810] as the sourced floor of a
named convention, better-ear P0 count UNPINNABLE pending
child-level cross-tabulation (CDC/state microdata request
is the named pinning action — the states collect by-ear
data per child; only the *publication* is marginal).

### 3.4 Triangulation check

Michigan child-level permanent bilateral ≥56 dB:
0.5/1,000 (2007–2011). CDC 2022 SNHL bilateral ≥56
ear-averaged: (292.5+248+562)/3,547,774 = 0.31/1,000
screened. Ordering holds (71+ ⊂ 56+; SNHL-only ear-avg
0.23 < SNHL 56+ 0.31 < MI all-permanent-type 56+ 0.5,
different state/era/denominator/child-vs-ear rule). No
contradiction; no pooling. This also behaves against
Fortnum's quarantined context (~1/1,000 for >40 dB
better-ear at UNHS/age 3): a ≥71 subset at ~0.2/1,000
documented is coherent. Coherence is not a pin.

## 4. What did not yield a child-level ≥70 count

Every route that could have supplied the joint
distribution, and its failure mode: Socrata (no dataset,
R1); Stacks (403 + same summaries, R2); NCHAM (CDC
re-presentation, R3); state reports (Michigan bins ≥56
pooled; no state ≥71 child-level table located this pass,
R4); cohort abstracts (severity as % of impaired, transient
contamination, or full text unavailable — Antoni/Fortnum,
R5); HSFS HTML/Excel (none exists; PDF is the publication).
**Definitive statement:** the better-ear ≥70 U.S. 2022
count is UNPINNABLE *from published aggregates*; it is
pinnable in principle from jurisdiction microdata, which is
a data-request action, not a literature action.

## 5. *OTOF* fraction — first inspected primaries, still no P0 fraction

| Source (inspected) | Fraction | Denominator (why not P0) |
|---|---|---|
| Rodríguez-Ballesteros 2008, PMID 18381613 (full abstract) | Spain 23/708 = 3.2%; Colombia 2/83; Argentina 2/30; separate AN cohort 11/20 | Autosomal-recessive nonsyndromic HI referral cohorts; screened p.Gln829X-first → biallelic non-Q829X missed, so a **lower bound** within its denominator; non-U.S., not newborn-ascertained, not ≥70-cut |
| Baux 2017, PMID 29196752 / PMC5711943 (EuropePMC full text) | 3 *OTOF* patients (all profound) among 207 referred NSHL families (1.4% of families, descriptive only) | French diagnostic-referral families, multistep testing; not population/newborn |
| Russian ANSD study 2020, PMID 32476384 (full abstract) | 5/28 (18%) | Bilateral ANSD children at a center — ANSD denominator, not congenital HL |
| Ford 2023, PMID 37679651 / PMC10511631 (abstract + full text) | "1–8% of congenital, nonsyndromic hearing loss" | **Secondary** — full text cites GeneReviews (Azaiez) for the range; systematic review's own data are 422 case-report individuals; all authors Decibel Therapeutics (sponsor of OTOF therapy) |

Sloan-Heggen 2016 (PMID 26969326, U.S. N=1,119, 39%
diagnosed, 49 genes) gives no *OTOF* numerator in the
abstract; its gene table is full-text-owed. Korean ANSD
papers (PMIDs 30482216, 26632695) are ANSD/variant-spectrum
denominators. GeneReviews NBK1251 remains uninspected (R6).

**Verdict:** `f_OTOF(P0)` stays **UNPINNABLE** — every
inspected denominator is AR-NSHI referrals, ANSD, or
congenital NSHL broadly, and `epi_arithmetic.d2_n_e_p0`
correctly returns `None` for all (`denominator_p0_like=
False`). The §1.2 "tens of newborns/year" gloss remains
uncomputed: multiplying 810 by 1–8% (→ 8–65) is shown here
only to forbid it — wrong numerator (convention, §3.3)
times wrong denominator (NSHL ≠ bilateral ≥70 P0, and
*OTOF* skews profound/ANSD so the P0-conditional fraction
is not the NSHL fraction in either direction known).

## 6. Additional disabilities — first inspected primary, still no P0 fraction

| Source (inspected full abstract) | Value | Denominator / definition |
|---|---|---|
| Ching 2013 (LOCHI), PMID 23462376 | **107/451 (24%)** additional disabilities; also ANSD 44/451 (10%) | Prospective population-based; children born 2002–2007 presenting <3 y to Australian Hearing (NSW/Vic/S-Qld), all degrees/devices (70% HA, 30% CI at 3 y); ascertainment "reported"/clinical records — instruments not named in abstract |
| Peterson 2023, PMID 38661773 | ~65% of teacher-caseload students (N=451 students, one midwestern state); abstract also secondarily cites GRI Annual Survey 2013 "almost 40%" | Educationally-significant disability = receiving special-education services beyond deafness; school-age caseload, teacher survey. The GRI figure inside this abstract is a secondary citation, **not** the GRI primary report (still uninspected; no fetchable primary PDF located this pass) |
| (context) PMID 35943238, tertiary clinic audit N=518 | 348/518 (67.2%) "medical comorbidities" | Broader construct (any medical comorbidity), clinic-ascertained — not the §3.1 construct |

The 24% → ~40% → 65% spread across (age ~3 population
cohort) → (school survey) → (teacher caseloads) is itself
the inspected evidence that the fraction is
definition/ascertainment/age-bound, exactly as Step 0
hypothesized from pointers. **P0 fraction (congenital
bilateral ≥70 infants, named instruments, stated age)
stays UNPINNABLE**; Ching is now the provisional cohort row
(non-U.S., all-degree — never a P0 input). Cupples 2018
(PMID 29732729) draws its N=67 from LOCHI's AD subgroup and
adds types, not a new denominator.

## 7. Proposed D1–D4 update (proposal only — frozen file untouched)

For `frozen_bilateral_eCI_v1.md` §2 at human re-freeze.
Nothing below is gate-deciding; U01 narrows, does not close.

**D1 (proposed new state: PARTIALLY SOURCED / P0 cell
UNPINNABLE).** Add sourced rows: 2022 occurrent births
3,616,776; screened 3,547,774 (98.1%); all documented D/HH
6,272 (1.7/1,000 births); bilateral SNHL ear-averaged
severe 248.0 / profound 562.0 / sum 810 (0.23/1,000
screened) — PROVISIONAL (agent pypdf extraction,
arithmetically reconciled to printed totals; human visual
re-read + rotated-label check owed). Keep the P0
better-ear ≥70 cell **blank (UNPINNABLE)** with the new
reason text: marginals-only publication; both-ears ≥71
SNHL ∈ [0, 804] formally; ear-average is a CDC total
convention that exceeds that maximum. Pinning action
(change of kind): child-level by-ear cross-tab via CDC
EHDI / state microdata request, or a freeze decision that
redefines D1 operationally as the HSFS ear-averaged
convention (a definitional amendment to P02 — holder
decision, flagged, never silent). Also fixes U02 partially:
ASHA bands are now inspected (HSFS p.1: severe 71–90,
profound 91+); WHO bands still uninspected.

**D2 (proposed additions, all PROVISIONAL cohort rows, all
P0 cells blank).** *OTOF*: Rodríguez-Ballesteros AR-NSHI
3.2% Spain (lower-bound method), Baux 3/207 families, Ford
1–8% secondary-with-COI — P0 fraction UNPINNABLE,
"tens/year" stays uncomputed. Additional disabilities:
LOCHI 107/451 (24%) provisional cohort value replaces the
unverified "~30–40%" pointer as the citable row, with
Peterson/GRI-secondary shown to mark definition spread;
P0 fraction UNPINNABLE pending definition+instruments+age
pin per §3.2. Pinning actions unchanged in kind:
P0-like U.S. newborn genomic cohort (Sloan-Heggen gene
table + GeneReviews human read are the cheap next steps);
D/HH-Plus definition decision.

**D3 (proposed context only).** ANSD bilateral
children-equivalent 150.5 of 3,520 bilateral D/HH (4.3%),
2022 HSFS — but 115.5 of the 150.5 are unknown-severity,
so no ≥70 ANSD cell. LOCHI ANSD 44/451, Michigan AN
0.1/1,000 as further non-P0 context. All D3 P0 cells stay
UNPINNABLE.

**D4 (no change).** Chain U01×U04×U05 still broken at the
first link for P0-as-defined; every coverage numerator
stays `None` in `epi_arithmetic`. Consequence travels:
**G6 coverage remains INSUFFICIENT for every candidate**;
this attack, alone, unblocks no gate. It converts the top
documentation gap from "table unreadable" to "table read,
quantity not identifiable from marginals" — progress of
the §7-rule-4 kind, and it spends attack round 1 of the
(at most 2) the stopping rule budgets for this gap. Any
round 2 should be the microdata request, not more
literature searching.

## 8. Reproducibility

URLs fetched 2026-11-02 (all `web_fetch`, statuses in §2):
archive.cdc.gov HSFS 2022 documents 01/12 + 2022 annual
compilation + 2021 document 12; Michigan MDHHS EHDI
Report 2013 PDF; Socrata catalog API queries (EHDI /
hearing loss children / hearing, domain data.cdc.gov);
NCBI E-utilities MEDLINE for PMIDs 26520479, 18381613,
23462376, 26969326, 29196752, 29732729, 32476384,
35943238, 37679651, 38661773 (+ ANSD/negative searches);
EuropePMC fullTextXML PMC5711943, PMC10511631 (success),
PMC48157, PMC7171096 (HTTP 500); PMC XML PMC48157,
PMC7171096 (front-only). PDF text: `pypdf` 6.21.4
(`PYTHONPATH=/tmp/pylibs`), layout mode; all arithmetic
re-executed against `verify/epi_arithmetic.py` in this
session (block-sum reconciliation, Fréchet bounds,
sensitivities in §3). Scratch extraction scripts/outputs
under `/tmp` (not deliverables).

*No DOI, PMID, N, or percentage in this file comes from a
search snippet. Where a number could not be inspected, the
route and failure are recorded instead.*
