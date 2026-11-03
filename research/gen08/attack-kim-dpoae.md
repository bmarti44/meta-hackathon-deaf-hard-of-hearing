# Attack — Kim et al. post-CI DPOAE in OTOF (ASTRA rank 3, unstick-2)

**Header:** Sol 6.1 requested; actual model **muse-wonder-full-1.0**; date **2026-11-03**.
Inspected primary sources only; no invented data. Agent extraction, not human
extraction/adjudication. This file attacks/verifies one pointer; it creates no
candidate, manifest, or scoring change.

**Verdict up front:** the pointer in [codex-unstick-2.md](../../reviews/codex-unstick-2.md)
(§ "additional biological lead") **verifies as a real, retrievable report** and the
child-level bound it computed from search extracts can now be replaced by an exact
count. **It moves no Q0/G4 premise cell to a new scoring state** — the unstick-2
expectation of "zero whole-gate PASS from this report alone" is **verified**. What
changes is only the evidence ledger: from *no directly inspected post-CI OTOF
physiology cohort* to *one small descriptive human cohort showing post-CI OHC
function in a subset*. Q0-P (patency/cannulability), Q0-A (post-CI AAV
transduction/function) and every scored G4 component remain exactly as they were.

## 1. Retrieval record (all three commissioned routes attempted)

| Route | Result |
|---|---|
| NCBI E-utilities efetch, `db=pmc&id=13555795` | **Success.** Full JATS XML, 26,744 bytes. This is the route that worked. |
| Europe PMC `rest/PMC13555795/fullTextXML` | **Success.** Full-text XML, 24,555 bytes; body text concordant with PMC XML. `rest/PMC13555795/supplementaryFiles` also succeeded (zip: figure webp/gif + supplement docx). Direct `europepmc.org/.../bin/` file and PDF-render URLs returned 403. |
| Publisher PDF (Wiley `doi/pdfdirect/10.1002/mco2.71006`) via pypdf | **Failed.** Wiley returned 403 (HTML); PMC PDF URL returned an HTML interstitial, not a PDF. No PDF was obtained, so no pypdf parse was possible (`pypdf` is also not installed in this environment). Nothing in this file depends on the PDF: main text, Figure 1 and the supplement were all obtained via the two XML routes. |

Source identity (from PMC XML front matter + PubMed efetch, concordant):
Kim C-H, Kim BJ (equal first authors), Koo J-W, Tran N-T, Kim Y, Choi BY.
"Preservation of Distortion Product Otoacoustic Emission After Cochlear
Implantation in Children With *OTOF*-Related Deafness." *MedComm* 7(9):e71006,
September 2026. PMID 42719247; PMC13555795; DOI 10.1002/mco2.71006. Article type:
Letter / brief report. Received 2026-01-24, accepted 2026-07-31 (Europe PMC XML
history). CC BY 4.0. Single centre: Seoul National University Bundang Hospital.
IRB B-2601-1023-111, consent waived (retrospective).

## 2. What the paper is (main text + supplement, inspected in full)

- Cross-sectional analysis of a retrospective cohort: **11 children** with
  confirmed biallelic *OTOF* variants, CI at SNUBH **2012–2022**, slim straight
  or slim modiolar arrays, soft-surgery technique stated for all. CI duration at
  DPOAE assessment **2–11 years**. "Space-for-time substitution": different
  children at different durations stand in for a longitudinal trajectory; the
  authors state the design cannot establish individual trajectories, cannot
  separate natural DFNB9 progression from implantation effects, and cannot
  identify an age threshold.
- DPOAEs at f2 = 1–8 kHz. Classification (supplement, aligned to the Regeneron
  DB-OTO trial NCT05788536 as the authors describe it): **Well** = SNR ≥6 dB at
  ≥3 frequencies; **Partial** = ≥6 dB at 2 frequencies or ≥5 dB at ≥3;
  **Minimal** = ≥6 dB at 1; **Not preserved** otherwise. "Detectable OHC
  function" = Well/Partial/Minimal.
- Authors' headline (ear level): among 5 children implanted ≤12 months and
  assessed within 6 years, **7/10 ears** detectable; **0/12 ears** in the
  remainder (implanted >12 months **or** duration ≥6 years). Fisher exact
  p = 0.001 (authors); GEE exchangeable p < 0.001 (authors).

## 3. Per-child / per-ear extraction (Figure 1C, transcribed from the inspected figure)

Electrode strings are verbatim from the figure. "Reg. Yes" = the figure's
"Met Regeneron Trial Criteria? (SNR ≥6 dB)" column. Five children have **two**
assessment rows (see §5, finding F1).

| Pt | Year of CI | Age at CI (mo) | CI duration (yr) | OHC Right | OHC Left | Reg. R | Reg. L | Electrode R / L |
|---|---|---|---|---|---|---|---|---|
| 1 | 2022.09 | 10 | 2 | Partial | Partial | No | No | CI632 / CI632 |
| 1 (2nd row) | — | — | 3 | Not | Minimal | No | No | — |
| 2 | 2020.07 | 10 | 3 | Partial | Well | No | **Yes** | CI632 / CI632 |
| 3 | 2020.07 | 10 | 4 | Not | Minimal | No | No | CI632 / CI632 |
| 4 | 2020.06 | 10 | 4.5 | Not | Partial | No | No | CI632 / CI632 |
| 4 (2nd row) | — | 10* | 5.5 | Not | Partial | No | No | — |
| 5 | 2019.05 | 12 | 5 | Not | Well | No | **Yes** | CI532 / CI532 |
| 5 (2nd row) | — | — | 6 | Not | Partial | No | No | — |
| 6 | 2019.03 | 16 | 5 | Not | Not | No | No | CI532 / CI532 |
| 6 (2nd row) | — | — | 6 | Not | Not | No | No | — |
| 7 | 2017.08 | 14 | 7.6 | Not | Not | No | No | CI532 / CI532 |
| 8 | 2016.12 | 14 | 8 | Not | Not | No | No | CI422 / CI422 |
| 9 | 2016.12 | 14 | 8 | Not | Not | No | No | CI422 / CI422 |
| 10 | 2012.12 | 35 | 11 | Not | Not | No | No | FLEX28 / FLEX28 |
| 11 | 2019.10 | 60 | 2 | Not | Not | No | No | CI532 / CI532 |
| 11 (2nd row) | — | — | 5 | Not | Not | No | No | — |

\* The "10" repeats in the age column on Pt 4's second row as printed; on other
second rows the age cell is blank. Figure 1A independently shows two DPOAE
assessment dots (with paired duration labels, e.g. "2 yr, 3 yr" for Pt 1,
"5 yr, 6 yr" for Pt 5/Pt 6, "2 yr, 5 yr" for Pt 11), confirming the second rows
are repeat assessments, not a transcription artefact.

Cross-check, Figure 1B representative SNR tables (ear side not labelled in the
figure; not assigned here): Pt 2 "Well" — SNR 9.8/20.0/24.3/13.2/5.8 dB at
2/2.8/4/6/8 kHz (≥6 dB at 4 frequencies ✓ Well); Pt 1 "Partial" — 12.1/12.6/4.0
at 4/6/8 kHz (≥6 at 2 ✓); Pt 3 "Minimal" — 4.3/3.2/1.6/12.9 at 2.8/4/6/8 kHz
(≥6 at 1 ✓); Pt 5 "None" — −2.1/5.6/−12.7/−6.5 (≥6 at 0 ✓). The classifications
are internally consistent with the supplement's definitions.

### Extraction gaps (named, not filled)

- **Middle-ear status: not reported.** Neither the main text nor the supplement
  mentions tympanometry, otoscopy, effusion screening, or any per-ear/per-visit
  middle-ear variable for this cohort. The only effusion discussion is about
  Santarelli et al. 2024 (their ref 5), whose warning the authors endorse:
  middle-ear effusion can make OAEs disappear and thereby *underestimate* OHC
  preservation. So every "Not preserved" ear above is compatible with (a) true
  OHC loss, (b) transient middle-ear pathology at the visit, or (c) both — the
  report as inspected does not let the reader separate them. This biases the
  detectable fraction *downward*, i.e. against the authors' own positive claim;
  it does not rescue a null.
- **Pre-operative DPOAE per ear: not tabulated.** Figure 1B shows pre-CI traces
  for four representative cases only. "Preservation" in the headline is
  therefore *post-operative detectability*, not demonstrated within-ear
  retention against each ear's own baseline for all 22 ears.
- **Not reported in inspected text/figure:** simultaneous vs sequential
  bilateral surgery, insertion approach/depth, post-op audiometric thresholds
  (no PTA/residual-hearing numbers at all), imaging, genetics detail beyond
  "biallelic *OTOF*", or any CI-off functional hearing measure.

## 4. Recomputed child-level bounds (replaces the unstick-2 provisional arithmetic)

Method: Fisher exact test recomputed from the hypergeometric distribution
(`math.comb`, two-sided by probability ordering; with a zero cell the two-sided
and greater one-sided values coincide in every table below). Script kept outside
the repo at `/tmp/kim_recompute.py` during this session; the tables below are
sufficient to reproduce every number by hand.

| Counting rule | Early group (≤12 mo, <6 yr window) | Remainder | Fisher exact p | Status |
|---|---|---|---|---|
| Authors' headline, ear level | 7/10 | 0/12 | **0.00070** (authors report 0.001 ✓) | As published |
| Unstick-2 bound from search extract (7 +ve ears among 5 bilateral children ⇒ 4–5 children) | 4/5 to 5/5 children | 0/6 | 0.01515 to 0.002165 | Now superseded |
| **Exact child level, any-ear detectable (from Fig. 1C)** | **5/5 children** | **0/6 children** | **0.002165** | Resolves the bound at its favourable end |
| Ear level, latest assessment row per child | 6/10 | 0/12 | 0.00281 | Sensitivity only (see F1) |
| Child level, any ear meeting the figure's Regeneron "Yes" column | 2/5 (Pt 2, Pt 5) | 0/6 | 0.182 | Not significant |
| Ear level, Regeneron "Yes" | 2/10 | 0/12 | 0.195 | Not significant |

Reading of these numbers, with the attacks applied:

1. **The child-level signal is real as arithmetic and does not depend on
   treating ears as independent.** Every one of the 5 early-implanted children
   has at least one detectable ear; none of the other 6 does, under earliest-row,
   latest-row and ever-positive counting alike (the child classification is
   identical under all three). The exact child-level p (0.0022) is the honest
   replacement for both the authors' ear-level Fisher/GEE and the unstick-2
   bounds. The authors' GEE p < 0.001 should not be quoted: 11 clusters with
   complete separation (0 events in one arm) is exactly where GEE Wald
   inference is unreliable.
2. **The headline is one specific counting choice.** 7/10 is reproducible from
   Figure 1C only as *earliest assessment per ear* or *ever-detectable per ear*
   within the window. On the *latest* row per child it is 6/10 (Pt 1 right ear
   goes Partial at 2 yr → Not at 3 yr). Neither choice overturns the direction;
   the magnitude "70% of ears" should be cited as 6–7 of 10 depending on rule.
3. **The strong-criterion result is much weaker.** Only 2 of 22 ears in the
   whole cohort (both left ears: Pt 2 at 3 yr, Pt 5 at 5 yr) meet the figure's
   own "Regeneron trial criteria — Yes" column. Five of the seven "detectable"
   headline ears are Partial/Minimal below that bar. Anyone citing this paper
   as "70% meet DB-OTO-style OHC criteria" would be wrong by the paper's own
   figure: the trial-criterion figure is 2/10 early ears (2/5 children),
   not significant against 0/12 at this N.
4. **Nothing here identifies *why*.** Implant age, CI duration, calendar era
   and electrode are almost perfectly confounded across the two groups: the
   early group is Pt 1–5 (CI 2019–2022, CI632 in four, durations 2–5 yr); the
   remainder mixes older-implanted children (Pt 10 at 35 mo/11 yr/FLEX28,
   Pt 11 at 60 mo) with longer-duration ones (Pt 7–9 at 14 mo but 7.6–8 yr,
   CI532/CI422). Pt 11 (60 mo, assessed at only 2 yr, both ears Not) is the
   single observation that speaks for age-over-duration; one child cannot carry
   that attribution. The authors say the same ("preclude any definitive
   conclusion about a specific age threshold") — verified, not a new criticism.

## 5. Findings from the attack

- **F1 — Internal tension in the assessment count.** The supplement describes a
  "comprehensive single-time-point audiological assessment" and an ear-level
  analysis of 22 ears, yet Figure 1A/C show a second assessment for Pt 1, 4, 5,
  6 and 11 (16 assessment-rows, 32 assessment-ears). The inspected text never
  states which row entered the Fisher/GEE analysis for those children, and the
  grouping definition creates a direct puzzle: Pt 5's left ear is still
  Partial at exactly 6 yr, but "duration ≥6 years" belongs to the remainder
  arm, which is reported as 0/12 — consistent only if each ear was entered
  once (at its earlier/in-window assessment, or ever-positive), not per
  assessment. **Unresolved from the inspected sources;** it changes 7/10→6/10
  under latest-row counting but does not change any child-level conclusion.
- **F2 — Middle-ear confounding is acknowledged in principle, uncontrolled in
  the data as reported** (§3 gaps). Direction of bias is toward undercounting
  preservation, so the positive subset is conservative but every negative ear
  is individually uninterpretable.
- **F3 — DPOAE ≠ the project's target biology.** The authors themselves state
  DPOAE presence/absence "cannot be assumed to signify overall cochlear
  integrity" (their STRC example). For *OTOF* the therapeutic target is the
  inner-hair-cell synapse; a working cochlear amplifier (OHCs) is at most a
  neighbouring-structure survival signal. A present DPOAE does not show IHCs
  are present/transducible, and an absent DPOAE does not show they are gone.
- **F4 — Consistency with Santarelli et al. 2024 is as the authors describe it**
  (their ref 5, PMC10718209, cited in the inspected text): DPOAEs detectable
  years after CI in at least one implanted *OTOF* ear with thicker electrodes
  (CI24RE(CA)/CI512), implanted at 33 months, still detectable ~3.6 yr later.
  Kim is therefore a second, larger (still small) cohort pointing the same way,
  not a lone outlier. (Santarelli itself was not re-extracted in this pass;
  this sentence reports Kim's inspected characterisation of it.)

## 6. Does it move any Q0 / G4 premise cell? (expected: no whole-gate change — verified)

Checked against [AppendixA-v1 §7.1](../frozen_baseline/AppendixA-v1.md) (G4
per-component rules, Track P: all applicable components must pass) and
[QR4 Stage 1](../gen04/candidate-QR4-stage01-executable.md) (Q0-P/Q0-A readouts
and thresholds). Cell in question: [Gen0 adapted line 173](../gen00/scoring/adapted_v2.csv)
`G,G4,ALL,etiology=OTOF` — currently INSUFFICIENT.

| Premise / component | What it needs | What Kim supplies | Moves? |
|---|---|---|---|
| Q0-P scala patency / cannulability % by time band (Appendix: "Q0's core missing number", UNPINNABLE, no PASS/FAIL possible in v1) | Imaging/histology/infusion evidence that the scala can be re-cannulated post-CI | Nothing. A DPOAE is an ear-canal acoustic measurement; it carries no information about fibrosis in the scala or whether a cannula/infusate can pass the array | **No** |
| Q0-A1 % named target cells transduced post-CI; Q0-A2 ABR improvement | A post-CI AAV (or other biologic) delivery experiment with transduction + function readouts | Nothing. No biologic was given to any child; OHCs are not the *OTOF* target cell (F3) | **No** |
| G4 residual-hearing preservation (% ears, pre-stated PTA-shift definition, T4, frozen ref UNPINNABLE for P0 infants) | Audiometric thresholds pre/post with a stated shift definition | No thresholds reported at all; DPOAE detectability is not a PTA-shift endpoint and cannot be converted into one | **No** |
| G4 SGN / hair-cell survival (density or count, method stated; T2; frozen point and numeric margin UNPINNABLE) | Histological density/count in a named model vs frozen/sham | A functional human OHC signal in 5/11 children — citable in an evidence ledger as descriptive support that OHCs *can* remain functional post-CI in *OTOF* ears, but it is not a density/count, has no frozen comparator, and the margin is UNPINNABLE by construction | **No** (ledger note only) |
| G4 fibrosis/new bone (Seyyedi & Nadol 0–3 per segment) | Histology | Nothing | **No** |
| G4-AAV presumptive FAIL for AAV challengers | Capsid-switch / re-dose / post-exposure efficacy evidence | Nothing | **No** |

**Whole-gate consequence: none.** G4 for the *OTOF* G-lineage stays
INSUFFICIENT; Q0 stays undecidable with Q0-P and Q0-A both untouched; the
Otarmeni label exclusion (Q0-L) is a regulatory fact this physiology paper
cannot affect — Kim's own framing is only that such data "may serve as a
reference for future investigations," which is exactly the weight it can bear
here.

**What it does change** (evidence ledger, not scoring):

1. The premise "post-CI cochleae in *OTOF* children have no measurable hair-cell
   function left, so post-CI biological strategies have no substrate" is now
   **directly inspected and false as a universal** for OHCs: 5/5 children
   implanted ≤12 months had ≥1 ear with detectable OHC function 2–5 years
   later (2/5 at the figure's strict trial-criterion level). The existing
   pro-biology premise of QR4-style reasoning gets a real human descriptive
   cohort behind it instead of a search-extract pointer.
2. The unstick-2 provisional child-level bound (4–5 of 5, p 0.015–0.0022) is
   replaced by the exact 5/5 vs 0/6, p = 0.002165 — its favourable end,
   conditional on Figure 1C as transcribed.
3. For choosing/simulating QR4's post-CI model (unstick-2 rank-3 stated aim),
   the usable quantitative anchors are: detectable-OHC fraction concentrated
   in the ≤12-month/short-duration/slim-array corner and zero outside it;
   within-child ear discordance is common (Pt 3, 4, 5 each have one Not ear),
   so any model that treats "child preserved / not" as all-or-none at the ear
   level is wrong — ear-level processes (insertion, middle ear, local
   progression) are doing real work in this data.
4. It does **not** support any clinical-eligibility claim for post-CI gene
   therapy, any 12-month threshold, or any statement about IHC survival,
   transduction, patency or hearing benefit. Any downstream document citing
   Kim for those would be over-citing it; F1–F3 above are the standing
   caveats to attach.

## 7. Provenance

- PMC XML: `efetch.fcgi?db=pmc&id=13555795` (26,744 bytes). Europe PMC
  fullTextXML (24,555 bytes) and supplementaryFiles zip (figure webp 69,156
  bytes; supplement docx 24,255 bytes, text extracted from
  `word/document.xml` — methods/ethics only, no data table; all per-child data
  are in Figure 1C). PubMed efetch for PMID 42719247 (identity cross-check).
- Publisher PDF: not obtained (Wiley 403; PMC/Europe PMC PDF endpoints
  403/HTML interstitial). If a future pass needs the PDF for figure-resolution
  reasons, Figure 1 as obtained (820×619) was sufficient to transcribe every
  Figure 1C cell and to cross-check Figure 1B's SNR tables against the
  supplement's classification rules; one cell-level ambiguity survives
  (Pt 4 second-row age "10", flagged in §3) and it affects nothing downstream.
- All counts, group definitions and thresholds in §4 are recomputed from §3's
  transcription; no number in this file is copied from a search snippet.
- Design-side evidence only; validation allocation unchanged; GOAL.md not
  edited; no scoring CSV touched.

