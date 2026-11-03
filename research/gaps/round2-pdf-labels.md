# Gap attack (round 2) — PDF labels via the pypdf unlock

> **Requested model:** Sol 6.1. **Actual model:**
> `muse-wonder-full-1.0`, disclosed per GOAL §9 rule 3.
> **Date:** 2026-11-02. **Inputs read first:**
> `research/gaps/round1-summary.md`,
> `research/gaps/gap-skeptic.md`, and the round-1
> full-text file `research/gaps/attack-fulltext.md`
> (plus the Step 0 rows under attack in
> `research/step0/verify-otof-fda.md` and
> `verify-epidemiology-q0.md` §4a/4d).
> **Scope:** round1-summary §6 items 1 and 5 — the
> human-visual re-reads that round 1 proved an agent
> can now do as *pre-extraction*: Otarmeni USPI
> numbers, MED-EL SSED re-pull, Advanced Bionics
> label, WHO grade table, Seyyedi–Nadol rubric.
> **Evidence rule:** inspected records only. Every
> value below was read in a PDF saved from its
> authoritative host and text-extracted locally with
> `pypdf`, or (item 5) in a full NCBI `efetch`
> `db=pmc` XML body. Search snippets were pointers
> to URLs only. No number was invented; where a
> document does not state a value, this file says so.
>
> **Status:** agent pre-extraction. Human dual
> extraction (GOAL §9) is still PENDING. Nothing
> here is gate-deciding, promotes any candidate, or
> changes any gate cell. It retires *qualifiers*.

## 1. Method — the round-1 unlock, applied and stress-tested

Round 1 established (attack-P0 §2-R0, skeptic S1):
`web_fetch` saves binary PDFs to disk and `pypdf`
6.21.4 (local pip cache, `/tmp/pylibs`) extracts
them. This round applies that route to FDA/WHO
hosts that Step 0 could not text-inspect. Two
method findings, both load-bearing for later rounds:

1. **The unlock works on `accessdata.fda.gov` and
   `fda.gov/media`.** All three FDA PDFs below were
   saved by `web_fetch` at their authoritative URLs
   and extracted page by page (sizes and MD5s in §7).
2. **`web_fetch` silently truncates saved binaries
   at 5 MiB.** The WHO report fetched as 8,435,712 B
   but was saved as exactly 5,242,880 B; `pypdf`
   then fails with "Invalid object in /Pages" — a
   truncation artefact, not a corrupt source. The
   identical authoritative URL re-downloaded with
   `curl` gave the full 8,435,712 B (272 pp.), which
   extracts cleanly. This is the one deviation from
   a pure `web_fetch` route in this file; it is
   recorded, and the byte-size match against the
   `web_fetch` header is the cross-check. Any future
   agent must compare saved size against fetched
   size before trusting a >5 MiB PDF.

Page locators give both the PDF page and, where the
document prints its own pagination, the printed page.

## 2. Scoreboard

| # | Target (Step 0 debt) | Route | Result |
|---|---|---|---|
| 1 | Otarmeni USPI §1 locus + §14 Table 2 (O1b/O2, A5) | FDA `media/192098`, 16 pp., `pypdf` | **VERIFIED in full.** All Step 0 numbers exact; prior-CI locus is §1, §4 is "None" (§3) |
| 2 | MED-EL ≥7 mo, mirror-provisional (O4b, skeptic B6) | `accessdata.fda.gov` P000025S134B.pdf, 43 pp. | **VERIFIED from FDA.** Byte-identical to the mirror copy; provisional qualifier retirable (§4) |
| 3 | Advanced Bionics minimum age UNVERIFIABLE (O4c) | `accessdata.fda.gov` P960058S167B.pdf, 50 pp. | **RESOLVED: 12 months**, bilateral profound, in current FDA SSED §II (§5) |
| 4 | WHO grade bands, U02 located-not-inspected | WHO IRIS bitstream PDF, 272 pp. (§1 note 2) | **EXTRACTED verbatim**, Table 1.3, printed p.38 (§6) |
| 5 | Seyyedi–Nadol 0–3 per-grade rubric uninspected (N4, A1 X6) | `efetch db=pmc` PMC4165780, 126,668 B, `<body>` present | **EXTRACTED — and it is only verbal anchors.** No numeric cutoffs exist in the paper (§7) |

Gate consequence: **zero cells change** (Step 3 PASS
bar: ≥Moderate GRADE + human dual extraction +
frozen pins + G3b). What changes is paperwork:
three qualifiers (MED-EL provisional, AB
unverified, WHO located-not-inspected) and one
single-source caveat (Otarmeni label numbers) can
be retired at the next human pass, and one owed
input (Seyyedi rubric → physical thickness for A1)
is proven not to exist in its source.

## 3. Item 1 — Otarmeni USPI (FDA media 192098, 16 pp.)

**Document identity note.** Step 0 inspected a
Regeneron-hosted `otarmeni_fpi.pdf` described as
5 pp. The FDA-hosted Package Insert at
`https://www.fda.gov/media/192098/download?attachment`
(1,610,337 B; MD5 `512657d0…`) is **16 pages**,
"Revised: 4/2026", "Initial U.S. Approval: 2026",
each page footered "Regeneron - Internal". The
16-page FDA copy is the authoritative record used
here; every Step 0 number checked against it
matches exactly, so the 5-page copy was evidently
an excerpt or earlier pagination — future citations
should use the FDA 16-page pagination below.

### 3.1 Prior-CI locus — §1 Indications, NOT §4

Verbatim (Highlights p.1 and Full Prescribing
Information §1, **p.2**):

> "OTARMENI is indicated for the treatment of
> pediatric and adult patients with severe-to-
> profound and profound sensorineural hearing loss
> (any frequency >90 dB HL) associated with
> molecularly confirmed biallelic variants in the
> OTOF gene, **preserved outer hair cell function,
> and no prior cochlear implant in the same ear**."

- **§4 Contraindications (p.8): "None."** The
  prior-CI condition is therefore an *indication
  eligibility* element of the studied population,
  not a contraindication. Any downstream sentence
  calling it a contraindication is wrong.
- Limitations of Use (p.1, p.2): not recommended
  where preoperative imaging shows inner-ear access
  not feasible (abnormal mastoid pneumatization /
  clinically significant middle/inner-ear anatomic
  variations). Dose-confirmation (§2.1, p.2):
  "Confirm patient has biallelic, likely pathogenic
  or pathogenic OTOF variants."
- Accelerated-approval basis (§1, p.2): improvement
  of hearing sensitivity by average PTA at Week 24;
  continued approval contingent on confirmatory
  trial. Step 0 O1b/O1c are confirmed verbatim,
  including: **no numeric age limit in §1**;
  §8.4 (p.10) 24 pediatric patients aged 10 months
  to 16 years; §8.5 (p.10) not studied ≥65 y.

### 3.2 §14 Table 2 and Week 48 (pp.13–14)

§14 (p.13): Study DB-OTO-001 (NCT05788536),
single-arm; enrolled profound SNHL (>90 dB HL,
PTA 0.5/1/2/4 kHz + ABR), OHC activity by OAE,
CI candidates; **"Patients with cochlear implants
in the same ear to be treated … were excluded"**
(trial exclusion, distinct from the §1 label
wording). Treated **N=24** (10 unilateral,
14 bilateral; 7.2×10¹² vg/ear in 0.24 mL); median
age 2 y (range 10 mo–16 y). Safety follow-up
(§6.1, p.9): median 45 weeks (range 9–115).

Efficacy set (p.13): "Of the 24 patients, 20 had
completed efficacy assessments at 24 weeks"
(5 with prior contralateral CI, 2 with contralateral
CI in the same surgical session).

**Table 2 (p.14)** — primary: average-PTA ≤70 dB HL
at Week 24, **16/20 (80%), 95% CI 56–94%**; key
secondary: ABR click ≤90 dB nHL, **14/20 (70%),
95% CI 46–88%**. Footnotes: (a) bilateral patients
contribute the better ear; (b) 1 patient without
Week-24 data imputed non-responder — so the
denominator 20 is *efficacy set including one
imputation*, not 20 completers with data.
Text after Table 2 (p.14): 9/20 (45%) ≤45 dB HL,
3/20 (15%) ≤25 dB HL at Week 24; one same-ear
rescue CI ~8 months post-dose after failure.

**Week 48 (p.14):** 12 of the 20 evaluated;
9/9 evaluated Week-24 responders maintained
response + 1 late responder = **10/12 (83%)
≤70 dB HL**; 8/12 (67%) ≤45, 5/12 (42%) ≤25,
9/12 (75%) ABR ≤90 dB nHL. This is a 12/20
subset, not the full efficacy set — quoting
"83% at Week 48" without the 12/20 denominator
stage repeats the error round 1 flagged for
Dieter attrition.

**Verdict:** Step 0 O1b, O1c, O2b, O2c, O2d, O2e
all verified verbatim against the FDA-hosted
label with page locators above. The A5
"single-source pending human re-read" caveat can
be retired *as an agent-extraction matter*; the
§9 human dual-extraction requirement itself is
untouched.

## 4. Item 2 — MED-EL SSED P000025/S134 from accessdata.fda.gov

Authoritative copy:
`https://www.accessdata.fda.gov/cdrh_docs/pdf/P000025S134B.pdf`
(605,138 B, 43 pp.; MD5 `5e67120f…`), saved by
`web_fetch`, extracted with `pypdf`. The Step 0
mirror copy (`fda.innolitics.com/pdf/P000025S134.pdf`)
re-downloaded this round is **byte-identical**
(`cmp` clean, same MD5) — the mirror was faithful,
and skeptic B6's provisional downgrade can now be
retired on an inspected FDA original.

§I (printed p.1 of 43): PMA P000025/S134, FDA
Notice of Approval **November 26, 2025**; original
PMA August 20, 2001 (≥18 mo), expanded S006
(18→12 mo); "The current panel-track supplement
was submitted to expand indications … for children
aged **7 months to 17 years, 11 months**."

§II Indications for Use (pp.1–2 of 43), pediatric
bilateral SNHL tiers verbatim in substance:

- **7–11 mo:** profound SNHL, PTA3 (500/1000/2000 Hz)
  **≥90 dB HL** (p.1 bottom → p.2 top).
- **12–71 mo:** moderately-severe to profound low
  frequencies (PTA3 ≥55 dB HL) and severe-to-profound
  high frequencies (thresholds not better than
  70 dB HL at 2000–8000 Hz).
- **6 y to 17 y 11 mo:** moderate-to-profound low
  frequencies (LFPTA at 250/500/1000 Hz >40 dB HL,
  not better than 65 dB HL at 3000–8000 Hz).
- Under 12 mo: repeatable behavioural results
  consistent with objective/electrophysiological
  results; 1–3 mo hearing-aid trial strongly
  recommended where feasible (p.2).

**Verdict:** Step 0 O4b "CORRECTED to 7 months"
is **VERIFIED from accessdata.fda.gov**. Bookkeeping
for the human pass: delete "mirror-provisional"
wherever it travels (frozen baseline §label-minima
row, Step 1 V03, O4d). The §3.4 comparator-drift
question (does a 2025 7-month minimum trigger a
v2 re-freeze?) is a holder decision, unchanged by
this extraction.

## 5. Item 3 — Advanced Bionics P960058 pediatric minimum age

Step 0 O4c was UNVERIFIABLE (PMA page HTTP 400;
12 mo pointer only). The current supplement SSED
resolves it from an FDA original:
`https://www.accessdata.fda.gov/cdrh_docs/pdf/P960058S167B.pdf`
(672,091 B, 50 pp.; MD5 `790d0b93…`).

§I (printed p.1 of 50): HiResolution™ Bionic Ear
System, P960058/S167, FDA Notice of Approval
**July 22, 2026** (the SSD/AHL expansion; press
announcement July 28, 2026). History in the same
paragraph: original pediatric PMA P960058 approved
June 26, 1997 "for children as young as 12 months
with profound, bilateral sensorineural deafness";
P940022 combined into P960058 in 2002.

§II Indications for Use (pp.1–2 of 50) restates
the **current bilateral** criteria in full:

- Adults ≥18 y: severe-to-profound bilateral SNHL
  (≥70 dB HL), postlingual, ≤50% HINT.
- **Children 12 months through 17 years:**
  profound bilateral SNHL (**≥90 dB HL**); hearing
  aids ≥6 mo (2–17 y) or ≥3 mo (12–23 mo), waived
  if ossification on x-ray; lack-of-benefit
  definitions by age (IT-MAIS/MAIS or ≤20% MLNT
  under 4 y; ≤12% PBK or ≤30% HINT-C at ≥4 y).

The new unilateral indications in the same §II
(AHL/SSD, pp.2–3) set a *different* pediatric
floor — children **5–17 y**, profound (4PTA
≥90 dB HL), ≤5% aided monosyllabic score — and
must not be conflated with the bilateral 12-month
minimum. §II also confirms no bilateral
minimum-age lowering accompanied the 2026
expansion.

**Verdict:** AB bilateral pediatric minimum is
**12 months (FDA-verified)**, profound ≥90 dB HL.
O4c's pointer is confirmed; "AB unverified" can
be retired. Label-minima set is now fully
FDA-sourced: Cochlear ≥9 mo (P970051/S172, Step 0),
MED-EL ≥7 mo (S134, §4 above), AB ≥12 mo (S167).
"No universal FDA minimum" (O4d) stands.

## 6. Item 4 — WHO hearing-grade table (World Report on Hearing 2021)

Authoritative copy: WHO publication page
`who.int/publications/i/item/9789240020481` →
Download link
`iris.who.int/server/api/core/bitstreams/5c3fc19f-11c9-4488-af3f-7e636b982aca/content`
(ISBN 978-92-4-002048-1, © WHO 2021; 8,435,712 B,
272 PDF pages; MD5 `b7e9bd95…`; §1 note 2 for the
`web_fetch` 5 MiB truncation and `curl` fallback).
Older `iris…/bitstream/handle/10665/339913/…` URLs
now return only a DSpace JS shell — the bitstream
UUID URL on the current WHO publications page is
the working authoritative route.

**Table 1.3 "Grades of hearing loss and related
hearing experience"**, printed **p.38** (PDF p.56),
§1.3.4 (printed pp.37–38). Threshold column =
better-ear average at 500/1000/2000/4000 Hz
(table footnote ‡):

| Grade | Better-ear threshold |
|---|---|
| Normal hearing | Less than 20 dB |
| Mild | 20 to <35 dB |
| Moderate | 35 to <50 dB |
| Moderately severe | 50 to <65 dB |
| Severe | 65 to <80 dB |
| Profound | 80 to <95 dB |
| Complete / total / deafness | 95 dB or greater |
| Unilateral | <20 dB better ear, ≥35 dB worse ear |

Binding table notes (p.38, verbatim in substance):
"for epidemiological use and applicable to adults";
audiometric descriptors "should not be used as the
sole determinant in the assessment of disability
or the provision of intervention(s) including
hearing aids or cochlear implants." §1.3.4 text
(printed p.37): the revised system lowers mild
onset from 26 dB to 20 dB vs the earlier WHO
system, adds moderately-severe/complete categories
and unilateral loss.

**Seams that must travel with any quotation**
(none is new; all are now locatable): WHO
"severe" starts at 65 dB and "profound" at 80 dB
(better-ear 4-frequency average, adults,
epidemiology) — neither aligns with the project's
P02 pin (better-ear ≥70 dB HL, 0.5–4 kHz), the
CDC HSFS ASHA bands (Severe 71–90, Profound 91+,
by ear; skeptic S1), or any device label above
(MED-EL profound PTA3 ≥90; AB profound ≥90).
Attaching a WHO grade *label* to a numeric cut
from another system is exactly the error frozen
§3.1/P02 already forbids; this extraction supplies
the WHO bands for U02, it does not license that
attachment. ASHA-band primary extraction (as
opposed to the HSFS p.1 ASHA table read in S1)
remains the only unclosed part of U02.

## 7. Item 5 — Seyyedi & Nadol 2014 rubric (PMC4165780)

Route: `efetch.fcgi?db=pmc&id=4165780`
(126,668 B, `<body>` present, NIHMS606805;
PMID 25122600, DOI 10.1097/MAO.0000000000000540,
*Otol Neurotol* 35(9):1545–1551). A1 round 1 got
HTTP 500 from Europe PMC and left the rubric
uninspected (X6); the NCBI route works.

**Design (Methods and Materials):** 28 temporal
bones / 21 subjects (mean age 78 y, range 57–92;
6 Advanced Bionics, 22 Cochlear Nucleus; all
cochleostomy insertions; implantation 1–23 y,
mean 11). Five elements — lymphocytic (L),
foreign-body giant-cell (GC), eosinophil (E)
infiltration, fibrosis (F), new bone (B) — each
scored **0–3** at three 1-mm segments (first 1 mm
at cochleostomy; midway; last 1 mm from tip),
"using a grading system, as illustrated in
Figure 2 … by a blinded otopathologist."

**The complete per-grade rubric in the paper is
the Table 2 footnote**, verbatim:

> "(0= none, 1= mild infiltration or presence,
> 2= moderate infiltration or presence,
> 3= severe infiltration or presence)"

Figure 2's caption anchors the grades only by
photomicrograph exemplars (e.g. grade 1 mild
fibrosis at tip in case 6; grade 2 moderate
fibrosis mid-array in case 14; grade 3 severe
fibrosis + new bone at cochleostomy in case 19).
**There are no numeric cutoffs anywhere in the
XML body** — no cells per area, no sheath
thickness in µm, no % scala occupied, no
second rater or reliability statistic. Two
in-paper inconsistencies are flagged, not
resolved: Fig. 2d captions "moderate lymphocytic
infiltration (grade 1)" (word and number disagree
under the paper's own footnote), and Results
names the single non-reactor "case # 27" although
Table 1 numbers patients 1–21 (bone numbering is
never defined in the XML text).

Results confirmed at full-text level: giant-cell
infiltration in ≥1 segment in 27/28 bones;
lymphocytic 25/28 (89.2%); eosinophil 7/28 (25%);
all elements worse at cochleostomy than mid/tip
(Table 3, mostly p<0.01; eosinophil tip-vs-
cochleostomy p=0.129 n.s.); no correlation with
implantation duration (Table 5, all n.s.).

**Consequence for A1 (round1-summary §6 item 5):**
the owed "Seyyedi–Nadol rubric → physical
(thickness, σ) map" cannot be supplied from this
source, because the source grades are ordinal
verbal severity with exemplar images only. Any
grade→thickness mapping in A1 remains an
ASSUMED modelling choice requiring a holder pin
or a different, quantitative source (e.g.
Kamakura volumetric %, round-1 fulltext §3.2 —
which is a distribution, still not a per-grade
thickness). This closes the *extraction* debt by
proving the cupboard bare; it does not make the
A1 kill test evaluable. Appendix A N4 should also
correct "tip−1 mm" to the paper's "last 1 mm
from the tip" segment definition.

## 8. Bookkeeping proposed (not applied; no earlier file edited)

1. Retire "label numbers single-source pending
   human re-read" for Otarmeni §§1/8.4/14 (frozen
   evolving-standard row, Step 1 V10): replace with
   the FDA 16-page pagination in §3. Keep the
   indication-vs-contraindication distinction
   (§4 = None) explicit wherever Q0-L is stated.
2. Retire MED-EL "≥7 mo provisional (mirror)"
   (frozen label-minima row, V03, O4b/O4d):
   "≥7 mo (FDA SSED P000025/S134, verified from
   accessdata.fda.gov; 7–11 mo profound PTA3
   ≥90 dB HL)".
3. Retire AB "unverified (12 mo pointer only)"
   (same rows, O4c): "≥12 mo bilateral profound
   ≥90 dB HL (FDA SSED P960058/S167 §II)".
   Do not import the SSD/AHL 5-year floor into
   bilateral rows.
4. U02: WHO bands now extracted with locator
   (§6). ASHA primary + the standing "no grade
   label attaches to P02" rule unchanged.
5. Appendix A N4 / Step 1 V05: record that the
   Seyyedi–Nadol rubric **has been** extracted and
   consists solely of the Table 2 verbal anchors +
   Fig. 2 exemplars; delete "per-grade rubric
   unextracted" as a future-extraction promise and
   replace it with "no quantitative rubric exists
   in source; physical mapping is a holder pin".
6. No gate cell, verdict, survivor, or stop-counter
   change follows from any of the above (Step 3
   bar; human dual extraction and G3b still block).
   Round-2 attack count, for the §7 rule 5 ledger:
   this file is a second independent attack on the
   *full-texts-owed sub-gap* of Step 5 §6 item 7
   and a first documentary attack on the A1-rubric
   prerequisite inside item 6; it is not an attack
   on gaps 1, 2, 3, 4, 5, or 8.

## 9. Reproducibility

All fetched 2026-11-02. PDFs: saved by `web_fetch`
(except WHO, §1 note 2), copied to `/tmp`,
extracted with `pypdf` 6.21.4 (`PYTHONPATH=/tmp/pylibs`),
page-tagged text in `/tmp/otarmeni.txt`,
`/tmp/medel.txt`, `/tmp/ab.txt`, `/tmp/who_table.txt`
(scratch, not deliverables).

| Record | URL | Bytes | Pages | MD5 (prefix) |
|---|---|---|---|---|
| Otarmeni USPI | `fda.gov/media/192098/download?attachment` | 1,610,337 | 16 | `512657d0…` |
| MED-EL SSED | `accessdata.fda.gov/cdrh_docs/pdf/P000025S134B.pdf` | 605,138 | 43 | `5e67120f…` |
| AB SSED | `accessdata.fda.gov/cdrh_docs/pdf/P960058S167B.pdf` | 672,091 | 50 | `790d0b93…` |
| WHO WRH 2021 | `iris.who.int/server/api/core/bitstreams/5c3fc19f-…/content` | 8,435,712 | 272 | `b7e9bd95…` |
| Seyyedi XML | `eutils…/efetch.fcgi?db=pmc&id=4165780` | 126,668 | — | `a70bb077…` |

Corroborations executed: MED-EL mirror vs FDA
original `cmp`-identical; WHO `web_fetch` header
size (8,435,712) vs `curl` download size (identical)
vs saved-file size (5,242,880 = 5 MiB truncation);
Seyyedi XML retrieved by both `web_fetch` and
`curl` at identical 126,668 B. Probe failures
recorded and not retried to death: `iris…/handle/`
URLs → DSpace JS shell; `iris…/rest/bitstreams/
1334317/retrieve` → HTTP 403; several guessed
`pdf25/` SSED paths → 404 (working path is
`cdrh_docs/pdf/` as above; see URLs).

*Unresolved after this attack: human dual extraction
of every number above (the §9 gate this file cannot
satisfy); ASHA primary bands (U02 remainder);
whether MED-EL 7 mo triggers a comparator v2
re-freeze (holder decision); a quantitative
grade→thickness source for A1, which Seyyedi–Nadol
does not contain; and everything round1-summary §6
lists under gaps 1–5 and 8. No gap is closed, no
cell is PASS, and Step 5's no-winner decision is
unaffected.*
