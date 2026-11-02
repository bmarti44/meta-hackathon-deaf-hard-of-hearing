# Step 0 verification — epidemiology & Q0 preservation

> **Route:** GOAL §9 Sol 6.1 high (generation-execution worker).
> **Actual runtime model:** `muse-wonder-full-1.0` fallback — Sol 6.1
> unavailable in this runtime; substitution disclosed per GOAL §9 rule 3.
> **Verified date:** 2026-11-02 (all rows).
> **Status:** Agent pre-extraction only (GOAL §9). Human-led dual
> extraction on load-bearing claims is still pending and has not been
> done. No row below may decide a gate until a human extractor
> independently verifies it.
> **Method:** `web_search` to locate, `web_fetch` to inspect PubMed
> full abstracts (via NCBI E-utilities MEDLINE records), PMC full-text
> landing pages, and the FDA press announcement. Search snippets are
> pointers only and are never cited as evidence. PDFs fetched as binary
> (CDC EHDI 2022 PDFs, Morton & Nance NEJM PDF, Otarmeni full
> prescribing information PDF) could not be text-extracted with the
> tools available in this runtime (`pdftotext`, PyMuPDF, PyPDF2,
> pdfplumber all absent) — numbers visible only in those PDFs or in
> search snippets are marked UNVERIFIABLE, not VERIFIED.
> GOAL.md sections read before verification: §1–§3, §8, §11, Appendix E
> (plus §9 for routing/extraction rules).

## Summary verdicts

| # | Claim area | Headline verdict |
|---|---|---|
| 1 | PMID 37441990 "Danish cohort" | VERIFIED as a Danish pediatric CI etiology cohort (N=100); CORRECTED if used as population incidence or as a congenital bilateral ≥70 dB denominator — it is neither |
| 2 | Congenital bilateral ≥70 dB incidence (CDC EHDI; Morton & Nance) | UNVERIFIABLE at the ≥70 dB bilateral cut from inspected text; VERIFIED only for broader cuts (>40 dB better-ear, Fortnum; Morton & Nance identity) |
| 3a | Etiologic fractions: GJB2 / SLC26A4 / cCMV / OTOF | Mixed: cohort-specific fractions VERIFIED (Danish, Australian exome, Grosse cCMV); universal/ancestry-stratified GJB2, SLC26A4 and OTOF ranges UNVERIFIABLE from inspected full text in this pass |
| 3b | Additional disabilities "~30–40%" (§3.1) | UNVERIFIABLE as a primary-source-verified range in this pass; pointer sources only (Gallaudet Annual Survey secondary citations) |
| 4a | Q0: post-CI human temporal-bone fibrosis/ossification | VERIFIED that fibrous tissue/new bone and granulomatous reaction are near-universal in small archival series; scala-patency % for future AAV delivery UNVERIFIABLE (no inspected source reports it as such) |
| 4b | Q0: post-CI AAV delivery (animal) | CORRECTED: inspected animal work delivers AAV *before/at* implantation, not after established CI; no inspected study of AAV delivery into a previously implanted, fibrosed cochlea was found — UNVERIFIABLE for the post-CI sequencing question |
| 4c | Q0: hearing-preservation residual-hearing rates | VERIFIED (pediatric meta-analysis, 78% of ears) with major caveats: mean age ~9.7 y, pre-op PTA ~60 dB — not the congenital ≥70 dB infant population |
| 4d | Label exclusion vs biology | VERIFIED as a *label/indication* fact (FDA announcement inspected); full label text UNVERIFIABLE (PDF binary). Label exclusion ≠ biological impossibility — GOAL §1.3 framing stands |

---

## Claim 1 — PMID 37441990, Danish cohort

| Field | Detail |
|---|---|
| Claim as stated in GOAL.md | §11 Step 0 and Appendix E list "Danish cohort PMID 37441990" as an anchor to verify. GOAL v2.2 makes no numeric claim from it in §§1–3 (v1 figures retired, §3.1). |
| Verdict | **VERIFIED** (identity, population, N, outcomes below); **CORRECTED** against any use as (i) population incidence of congenital bilateral ≥70 dB SNHL or (ii) a P0 denominator |
| Correct value (inspected PubMed full abstract, NCBI E-utilities MEDLINE record) | Friis et al., *Int J Pediatr Otorhinolaryngol* 2023;171:111640. Retrospective cohort of **100 Danish pediatric CI recipients** (54 F / 46 M, age 0–17 y), all implanted **2020–2022** at Aarhus. Outcomes are *cause of HL* and *implantation age*, not incidence and not language/hearing outcomes. Hereditary HL 44/100 (44%); *SLC26A4* pathogenic variants 14/100 (14%; conclusions break this out as 13% Pendred + 1% non-syndromic); syndromic 23%; non-syndromic 21% (most common gene *GJB2* — no *GJB2* numerator in abstract); TORCH risk factors 25%; congenital CMV DNA positive 23/100 (23%); unknown cause 31/100 (31%), of whom 16 had inner-ear malformations. HL diagnosed at newborn hearing screening in 70%. Only **23 children** had congenital severe-to-profound *bilateral* HL with simultaneous implantation at 8–14 months (mean 10.5 mo); in 47 cases HL was progressive and implantation occurred when criteria were reached. Percentages overlap (hereditary/syndromic/TORCH/cCMV are not mutually exclusive in the abstract) and must not be summed. |
| DOI / PMID | PMID 37441990; DOI 10.1016/j.ijporl.2023.111640 |
| N + design | N=100 children; single-centre retrospective CI-recipient cohort, Denmark, implant years 2020–2022 |
| Locator | PubMed abstract, Methods/Results/Conclusions paragraphs (MEDLINE `AB` field) |
| Verified date | 2026-11-02 |

**Implication for GOAL:** Usable in Appendix D only as a *CI-recipient*
etiology mix (selected, implanted population; mixed congenital +
progressive; ages 0–17). It does not estimate P0 (§3.1: congenital
bilateral ≥70 dB at birth) and its *SLC26A4* 14% / cCMV-DNA 23% figures
must not be ported to a U.S. newborn denominator without a stated
transportability argument.

---

## Claim 2 — Congenital bilateral ≥70 dB incidence

GOAL §3.1 defines P0 at better-ear ≥70 dB HL (0.5–4 kHz) and Appendix D
requires D1 to separate "congenital bilateral ≥70 dB incidence at birth"
from "all congenital HL". No numeric ≥70 dB incidence is asserted in
GOAL v2.2 §§1–3 (correctly retired). The verification question is
whether the named sources support such a number.

### 2a. CDC EHDI

| Field | Detail |
|---|---|
| Claim as stated | CDC EHDI named (assignment; GOAL §3.1 EHDI 1-3-6) as the incidence source |
| Verdict | **UNVERIFIABLE** at the bilateral ≥70 dB cut in this pass |
| What was tried | (1) `cdc.gov/hearing-loss-children/data/` — HTTP 403 on fetch. (2) CDC EHDI 2022 HSFS Data Summary PDF and Type-and-Severity PDF via `archive.cdc.gov` — fetched as binary PDFs; no PDF text extractor available in runtime, so table cells (severity × laterality × type) could not be inspected. (3) RestoredCDC mirror of the 2022 EHDI annual-data page — inspected, but it is an independent mirror (archived 2025-01-06, "not affiliated with CDC"), i.e. not an authoritative full record, and the landing page lists documents rather than the severity table itself. Search-snippet values (e.g. "1.7 per 1,000 screened", "6,272 children, 2022") are pointers only and are **not** reported here as verified. |
| Correct value | Not established from inspected authoritative text. Do not compute a ≥70 dB bilateral rate from snippets. The 2022 HSFS Type-and-Severity table (by ear: type × severity bands incl. severe 71–90 / profound 91+, bilateral vs unilateral) is the right primary source and must be extracted by a human with PDF access, with screened-births denominator and loss-to-follow-up stated. |
| DOI/PMID/doc | CDC EHDI Hearing Screening & Follow-up Survey 2022: `01_2022-HSFS_Data-Summary.pdf`; `12_2022_HSFS_Type-and-Severity.pdf` (both located, neither text-inspected) |
| N + design | U.S. state/territory EHDI program survey, births 1 Jan–31 Dec 2022 (denominator = screened infants; exact N not inspected) |
| Locator | — (no inspected table cell) |
| Verified date | 2026-11-02 (attempt date) |

### 2b. Morton & Nance 2006 and successors

| Field | Detail |
|---|---|
| Claim as stated | Morton & Nance (or successors) as incidence source (assignment) |
| Verdict | **VERIFIED** (bibliographic identity only); **UNVERIFIABLE** for any ≥70 dB bilateral incidence; **CORRECTED** against citing it for the P0 cut — its headline incidence is for a much broader case definition |
| Correct value (inspected) | Morton CC, Nance WE. "Newborn hearing screening — a silent revolution." *N Engl J Med* 2006;354(20):2151–2164. PubMed record carries **no abstract text** (review article), so no incidence number is inspectable in the authoritative record fetched. The full-text PDF was located (InfantHearing.org copy) but fetched as binary and could not be text-extracted; the widely quoted "1.33/1000 (UK) / 1.86/1000 (US)" figures were visible only in search snippets and are therefore **not verified here**. Even if confirmed by human extraction, those figures concern sensorineural loss at a low threshold (≥35–40 dB class definitions, unilateral included after adjustment) — they cannot be relabelled as bilateral ≥70 dB incidence. |
| DOI / PMID | PMID 16707752; DOI 10.1056/NEJMra050700 |
| N + design | Narrative review; no primary N |
| Locator | PubMed MEDLINE record (TI/PG/AID fields); no `AB` field exists |
| Verified date | 2026-11-02 |

| Field | Successor/comparator inspected: Fortnum et al. 2001 |
|---|---|
| Verdict | **VERIFIED** for >40 dB better-ear permanent childhood hearing impairment (PCHI); not a ≥70 dB or congenital-only-at-birth estimate |
| Correct value | UK questionnaire ascertainment, children born 1980–1995 resident in 1998; case = better-ear >40 dB averaged 0.5–4 kHz. 17,160 individual children from 26,000 notifications. Prevalence 0.91/1000 live births (95% CI 0.85–0.98) at age 3 rising to 1.65 (1.62–1.68) at 9–16 y; under-ascertainment-adjusted 1.07 (1.03–1.12) and 2.05 (2.02–2.08). UNHS yield "close to 1/1000 live births" with 50–90% more diagnosed by age 9 (progressive/late-onset entry — directly relevant to GOAL §3.1 entry-time strata, and a warning against treating birth incidence as lifetime P0). Severity split at ≥70 dB is not in the abstract; full text (PMC48157) was not line-inspected in this pass. |
| DOI / PMID | PMID 11546698; DOI 10.1136/bmj.323.7312.536; PMC48157 |
| N + design | N=17,160 children; retrospective total ascertainment, UK |
| Locator | PubMed abstract Results paragraph |
| Verified date | 2026-11-02 |

**Bottom line for Appendix D1:** From inspected text, the defensible
statements are (i) broad congenital/early PCHI is on the order of
~1/1000 live births at >40 dB better-ear definitions at birth/age 3,
rising with age; (ii) the bilateral ≥70 dB-at-birth subset is **not yet
sourced**. Human extraction of CDC HSFS 2022 Type-and-Severity (and/or
a severity-banded registry) is required before any P0 head-count,
"tens of newborns/year" *OTOF* arithmetic (§1.2), or coverage % is
computed. Any single-point ≥70 dB incidence in a future draft without
that table should be treated as fabricated.

---

## Claim 3 — Etiologic fractions + additional disabilities

### 3a(i). GJB2 / DFNB1

| Field | Detail |
|---|---|
| Claim as stated | §3.2 requires *GJB2* fractions "by ancestry/population"; no universal % asserted in v2.2 |
| Verdict | **VERIFIED** only as cohort-specific values below; **UNVERIFIABLE** as an ancestry-stratified universal range in this pass |
| Correct values (inspected abstracts) | (1) Danish CI cohort (PMID 37441990): *GJB2* named most common gene within non-syndromic HL (21/100 non-syndromic); **no GJB2 numerator in abstract** — a Danish GJB2 % cannot be extracted from the inspected record. (2) Australian population-based exome cohort, Downie et al. 2020 (below): standard-of-care *GJB2/6* sequencing alone diagnosed 22/106 (21%) of infants with moderate–profound bilateral HI, vs 59/106 (56%) for exome — i.e. in that population/era, GJB2/6-only testing captures roughly one fifth, and most genetic diagnoses lie elsewhere. Ancestry-specific figures (e.g. European vs East Asian vs sub-Saharan African) appeared only in search snippets/secondary reviews in this pass and are not reported as verified. |
| DOI / PMID | PMID 37441990 (10.1016/j.ijporl.2023.111640); PMID 31827275 (10.1038/s41431-019-0553-8) |
| N + design | N=100 (Danish CI recipients); N=106/156 approached consented (Australian newborn-screening-detected bilateral moderate–profound HI, births 2016–2017, WES + microarray) |
| Locator | Both: PubMed abstract Results |
| Verified date | 2026-11-02 |

### 3a(ii). SLC26A4 / EVA / Pendred

| Field | Detail |
|---|---|
| Verdict | **VERIFIED** as Danish-cohort value; **UNVERIFIABLE** as a general P0 fraction |
| Correct value | Danish CI cohort: *SLC26A4* pathogenic variants 14/100 (14%) of pediatric CI recipients; authors' conclusion splits this as 13% Pendred syndrome + 1% non-syndromic. This is a high, population-specific (Danish) CI-selected figure. No second inspected primary source in this pass establishes a U.S./P0 *SLC26A4* fraction; the Australian exome abstract does not enumerate genes beyond the GJB2/6 comparator (gene-level breakdown is in PMC full text PMC7171096, located but not line-inspected here). |
| DOI / PMID | PMID 37441990; DOI 10.1016/j.ijporl.2023.111640 |
| N + design | N=100, as above |
| Locator | Abstract Results + Conclusions |
| Verified date | 2026-11-02 |

### 3a(iii). Congenital CMV (cCMV)

| Field | Detail |
|---|---|
| Verdict | **VERIFIED** (two inspected sources, different denominators — keep separate per Appendix D2) |
| Correct values | (1) Grosse, Ross & Dollard 2008, systematic review of unbiased universal-newborn-CMV-screening studies: ~14% of children with congenital CMV develop SNHL of some type; **3–5% develop bilateral moderate-to-profound SNHL**; among *all* children with bilateral moderate-to-profound SNHL, estimated **15–20% attributable to congenital CMV**. Note the case definition is bilateral *moderate*-to-profound, broader than P0 ≥70 dB, and includes postnatal progression captured in follow-up — it is an upper-bound guide for the P0-at-birth cCMV fraction, not a direct estimate. (2) Danish CI cohort: congenital CMV DNA positive in 23/100 (23%) of CI recipients (retrospective DNA testing; CI-selected, includes progressive cases). The two figures answer different questions and must not be averaged. |
| DOI / PMID | PMID 17959414; DOI 10.1016/j.jcv.2007.09.004 (*J Clin Virol* 2008;41(2):57–62). Danish: PMID 37441990 |
| N + design | Systematic review (50 references; screened-cohort subset for unbiased estimates — pooled N not stated in abstract); Danish N=100 |
| Locator | Abstract Results (both) |
| Verified date | 2026-11-02 |

### 3a(iv). OTOF

| Field | Detail |
|---|---|
| Claim as stated | §1.2: eligible U.S. incidence "on the order of tens of newborns/year"; majority fraction "must be computed" (Appendix D) |
| Verdict | **UNVERIFIABLE** (fraction of congenital HL due to biallelic *OTOF*) from inspected full text in this pass; the "tens/year" order-of-magnitude is therefore also not yet verified arithmetic |
| What was tried | GeneReviews *OTOF*-Related Hearing Loss (NBK1251) — NCBI Books fetch returned a reCAPTCHA interstitial, no inspected text. Secondary sources (systematic-review abstracts, payer policies, press releases) were located via search but their "1–8% of congenital nonsyndromic HL" / "~1% of congenital deafness" style figures are snippet-visible only here and use shifting denominators (congenital HL vs AR nonsyndromic vs ANSD). Per the no-invention rule, no OTOF % is reported as verified. Human extraction should take the GeneReviews Prevalence section (population-specific: e.g. Japanese vs Spanish cohorts) plus one primary genomic cohort with a P0-like denominator, then recompute §1.2 explicitly. |
| DOI / PMID | GeneReviews NBK1251 (located, not inspected). No PMID relied upon |
| N + design | — |
| Locator | — |
| Verified date | 2026-11-02 (attempt date) |

### 3b. Additional disabilities "~30–40%" (§3.1)

| Field | Detail |
|---|---|
| Claim as stated | §3.1: children with additional disabilities "are ~30–40% of the real population in many cohorts; exact fraction pinned Step 1" |
| Verdict | **UNVERIFIABLE** as a primary-source-inspected range in this pass (directionally consistent with pointer literature; not verified) |
| What was tried | Located the usual citation chain — Gallaudet Research Institute Annual Survey of Deaf and Hard of Hearing Children and Youth (2009–2010 / 2013 reports, "~40%") — only via secondary citations (ASHA, textbook and journal secondary mentions) in search results; the Annual Survey reports themselves were not fetched/inspected as full records. Cohort values visible in snippets vary widely by definition and ascertainment (e.g. ~15% in a severe-to-profound CI longitudinal cohort vs ~40% in school-survey D/HH populations vs 25–50% ranges in review text), which confirms GOAL's "in many cohorts" hedge but also shows the range is definition-bound (educationally significant disability vs diagnosed neurodevelopmental condition; all-D/HH school population vs congenital bilateral ≥70 dB infants). No number is endorsed here. Step 1 must pin: source population, disability definition/instruments (§3.2 already requires named instruments), and age at ascertainment — a school-age survey fraction must not be applied to P0 infants without adjustment. |
| DOI / PMID | None relied upon. Pointer: Gallaudet Research Institute Annual Survey reports (2011 report on 2009–2010 data; 2013) — to be human-inspected |
| N + design | — (not inspected) |
| Locator | — |
| Verified date | 2026-11-02 (attempt date) |

---

## Claim 4 — Q0 preservation evidence (GOAL §1.3, §8G)

GOAL correctly treats "early CI forecloses later gene/cell therapy" as a
question. Evidence below is separated into (a) human histopathology,
(b) animal AAV-after-CI data, (c) hearing-preservation surgery outcomes,
(d) label/trial exclusions (regulatory fact, not biology).

### 4a. Human temporal-bone post-CI histopathology

| Source (inspected abstract) | Finding relevant to Q0 | N + design | Locator |
|---|---|---|---|
| Seyyedi & Nadol 2014, *Otol Neurotol* 35(9):1545–1551. PMID 25122600; DOI 10.1097/MAO.0000000000000540; PMC4165780 | Granulomatous/foreign-body reaction to electrode in **27/28 (96.4%)** temporal bones; eosinophil infiltration 7/28 (25%). Fibrosis/new-bone/inflammatory scores (0–3 scale, 3 segments) significantly greater at basal turn near cochleostomy than distally (p<0.05). **Verdict: VERIFIED** that an intracochlear tissue response is near-universal in this archival series and is insertion-trauma-graded. The abstract does **not** report a "% scala patent / % re-accessible for future infusion" endpoint — patency-for-AAV cannot be read off it. | 28 temporal bones / 21 subjects, Mass. Eye & Ear archival collection, multichannel CIs (adult, older-era devices; MeSH: Aged/Middle Aged) | Abstract Methods/Results |
| Kamakura & Nadol 2016, *Hear Res* 339:132–141. PMID 27371868; DOI 10.1016/j.heares.2016.06.015; PMC5018452 | Fibrous tissue **and** new bone found in **all 17/17** specimens. Post-op CNC word score positively correlated with total SGN count, negatively with % volume of **new bone** (scala tympani, scala media/vestibuli, whole cochlea), not with % fibrous tissue volume. New bone in scala media/vestibuli correlated with insertional trauma (esp. basilar membrane). **Verdict: VERIFIED.** Implication: some new tissue is effectively universal; its *volume/distribution*, not its presence/absence, is the variable — binary "patent vs obliterated" framings will mislead Q0. Absolute % volumes are in PMC full text (located, not line-inspected here). | 17 temporal bones, patients implanted in life; 3D volumetric reconstruction (Amira) | Abstract Results |
| Hodge et al. 2021, *Otol Neurotol* 42(10):1492–1498. PMID 34607995; DOI 10.1097/MAO.0000000000003327; PMC8595606 | In **otosclerosis** CI temporal bones: cochleostomy insertion → extensive osteoneogenesis/fibrosis at basal turn, "often obliterating scala tympani", sometimes extending to scala media/vestibuli, near-universal hydrops; round-window insertion → minimal intracochlear osteoneogenesis. Unimplanted contralateral ears: no intracochlear osteoneogenesis. **Verdict: VERIFIED for otosclerosis only — CORRECTED against generalising to congenital infant cochleae.** Supports insertion-route dependence (round window < cochleostomy) as a preservation variable. | 17 HTB total: 13 implanted + 4 contralateral controls, all cochlear otosclerosis | Abstract Results/Conclusion |

**Scala-patency rate verdict: UNVERIFIABLE.** No inspected source
reports the Q0-deciding quantity — proportion of implanted (still less
pediatric, modern-array, round-window) ears in which the scala remains
cannulable/infusible for a later biologic, by time-since-implant.
Archival series are small (N=17–28 bones), adult, older-device,
cochleostomy-heavy, and selected (temporal-bone donors). They establish
*that* fibrosis/neo-ossification occurs basally and scales with trauma;
they do not establish that post-CI delivery is impossible, nor a patency
%. GOAL §8G's requirement to pre-define patency % thresholds *before*
scoring Q0 is therefore not yet satisfiable from this literature alone;
Step 2 protocol must name what evidence (e.g. explant/reimplant series,
imaging patency grades, post-CI infusion animal work) would fill it.

### 4b. Post-CI AAV delivery — animal data

| Field | Detail |
|---|---|
| Verdict | **CORRECTED / UNVERIFIABLE for the post-CI question.** Inspected/located animal AAV+CI work delivers vector *before or at* implantation in acutely deafened ears — the reverse sequence from Q0's "CI first, AAV years later into a fibrosed cochlea". |
| Evidence | Guinea-pig neurotrophin gene-therapy + CI programme (Pfingst group): animals deafened (neomycin), **inoculated with AAV.*Ntf3* (or AAV.Empty control) prior to / at implant insertion**, then implanted; ECAP/SGN outcomes followed (e.g. *Hear Res* 2015 insertion-trauma paper, PMC4674315 — PMC landing page located; sequence "inoculated … prior to implant insertion" visible in located full-text excerpts; abstract-level MEDLINE inspection of this specific paper was not completed in this pass, so effect sizes/SGN counts are **not** reported as verified). Searches for AAV transduction *after* established implantation/fibrosis, post-explant AAV delivery, or AAV-OTOF rescue in a previously implanted ear returned no primary study. Absence here is absence of located evidence in this bounded search, not proof none exists — but Q0 currently has **no direct animal evidence** that AAV delivered after CI (with mature fibrous sheath/new bone) transduces target cells or restores function, and none that it cannot. |
| DOI / PMID | PMC4674315 (Pfingst et al., *Hear Res* 2015) — located, not fully inspected; do not cite its numbers from this file |
| N + design | Adult guinea pigs, ototoxically deafened (exact N not verified in this pass) |
| Locator | — |
| Verified date | 2026-11-02 |

### 4c. Hearing-preservation surgery — residual-hearing rates

| Field | Detail |
|---|---|
| Verdict | **VERIFIED** (meta-analytic rate below); **CORRECTED** against applying it to congenital bilateral ≥70 dB infants, who by definition have little/no preserveable acoustic hearing at speech frequencies |
| Correct value | Madgar et al. 2025, *Otolaryngol Head Neck Surg* 172(5):1539–1547: systematic review/meta-analysis (PRISMA; 5 databases; studies before Aug 2024) of hearing preservation after **pediatric** CI: 24 studies, **567 patients**; mean age 9.68 y (95% CI 8.27–11.09); mean PTA 60.48 dB pre-op → 70.95 dB post-op; **hearing preservation in 78% of ears (95% CI 71–85%)**, I²=79.96% (high heterogeneity). No significant association with sex, surgical approach, electrode array, topical steroids, or initial PTA. "Preservation" definitions vary by primary study (any measurable residual vs complete/partial per HEARRING-type scales — not harmonised in abstract); durability beyond early follow-up not established by this abstract. |
| DOI / PMID | PMID 40052291; DOI 10.1002/ohn.1180 |
| N + design | 24 studies, 567 pediatric patients; meta-analysis of proportions |
| Locator | Abstract Results |
| Verified date | 2026-11-02 |

**Q0 reading:** Atraumatic/hearing-preservation technique preserves
*measurable acoustic hearing* in roughly three quarters of (older,
better-hearing) pediatric ears short-term — evidence that modern CI
need not destroy all cochlear structure/function. It is **not** evidence
that scala patency for future AAV infusion is preserved in 78% of ears,
and not evidence about infants implanted at <12 months with ≥70 dB
loss. Keep the three Q0 sub-questions (residual hearing / histologic
tissue response / future-delivery feasibility) as separate gate inputs;
conflating them is the main error this literature invites.

### 4d. Label exclusions — separate from biology

| Field | Detail |
|---|---|
| Claim as stated | §1.2/§1.3: Otarmeni approval requires biallelic *OTOF*, preserved OHC function, and *no prior CI in treated ear* "(label constraints — verify against the FDA label in Step 0)"; §1.3: this is a label/trial exclusion, "not proof of biological impossibility" |
| Verdict | **VERIFIED (partial)** at FDA-announcement level; **UNVERIFIABLE** at full-label level in this pass |
| Correct value | FDA press announcement 23 Apr 2026 (inspected, fda.gov): FDA approved Otarmeni (lunsotogene parvec-cwha), described as first dual-AAV gene therapy, for pediatric and adult patients with severe-to-profound/profound SNHL associated with molecularly confirmed biallelic *OTOF* variants. The announcement text fetched was truncated before the preserved-OHC / no-prior-CI wording, and the Full Prescribing Information PDF (Regeneron/Decibel host, located) fetched as binary and could not be text-inspected. Therefore the exact label locus of "no prior cochlear implant in the same ear" (Indication §1 vs Contraindications §4 vs trial-eligibility description §14) is **not verified here** and must be human-extracted from the label PDF with section/page locator. GOAL §1.3's conceptual separation stands regardless: even a contraindication-grade label statement is a *regulatory* fact about the studied population, not evidence about scala patency or AAV transduction post-CI (see 4a/4b, where the biological evidence is currently thin in both directions). Conversely, trial *exclusion* of prior-CI ears means efficacy/safety in such ears is unstudied — "not proven impossible" must not be upgraded to "preserved option" in Family G scoring without the missing delivery evidence. |
| DOI / PMID / doc | FDA News Release, 23 Apr 2026, "FDA Approves First-Ever Gene Therapy for Treatment of Genetic Hearing Loss…" (fda.gov). Label: OTARMENI (lunsotogene parvec-cwha) Full Prescribing Information PDF (located, not text-inspected) |
| N + design | Regulatory document; CHORD N/endpoints are a separate Step 0 worker's assignment — not verified here |
| Locator | FDA announcement ¶1 (indication sentence). Label section: unlocated (see above) |
| Verified date | 2026-11-02 |

---

## What Step 1 / human dual extraction must still do (from this file)

1. Extract CDC EHDI 2022 HSFS Type-and-Severity table (PDF) → first
   sourced bilateral severe (71–90) + profound (91+) count over screened
   births, with loss-to-follow-up bounds. Until then Appendix D1 and
   all P0 head-counts stay blank.
2. Extract GeneReviews OTOF Prevalence + one P0-like genomic cohort →
   OTOF fraction with named denominator; recompute §1.2 "tens/year".
3. Inspect Gallaudet Annual Survey primary report (or a defined
   infant cohort) → additional-disabilities fraction with definition,
   instruments, and ascertainment age matching §3.2.
4. Line-inspect PMC full texts already located (PMC7171096 gene-level
   table; PMC5018452 % new-bone volumes; PMC4674315 AAV.Ntf3 sequence/N)
   before citing any number beyond the abstracts verified above.
5. Extract Otarmeni label PDF §§1/4/14 → exact prior-CI locus + locator.
6. Decide, in the Step 2 protocol, what evidence type could ever
   supply a post-CI scala-patency % and post-CI AAV-transduction
   verdict; archival adult histopathology alone cannot.

*No DOI, PMID, N, or percentage in this file was invented. Every
VERIFIED row traces to an inspected PubMed MEDLINE abstract record or
the inspected FDA announcement on 2026-11-02. Everything else is
labelled UNVERIFIABLE with the attempt recorded.*
