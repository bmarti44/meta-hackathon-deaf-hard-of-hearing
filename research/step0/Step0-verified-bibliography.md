# Step 0 verified bibliography — synthesis (agent pre-extraction)

> **Date:** 2026-11-02. Source files read in full for this synthesis:
> `verify-epidemiology-q0.md`, `verify-otof-fda.md`,
> `verify-devices-biology.md`, `verify-channels-development.md`,
> `skeptic.md`. GOAL.md v2.2 read for §1–§3, §8, §11, Appendix E
> claim wording (plus §2.2, §3.4/§4.2, §9 for this synthesis).
> GOAL.md is **not edited** by this file; §3 below lists the
> corrections it requires.
>
> **Model + effort per role (GOAL §9 rule 1; substitution disclosed
> per rule 3).** All routes below requested the Sol 6.1 family;
> Sol 6.1 was unavailable in this runtime and every agent ran on
> the fallback at the same effort split. No agent below is Sol 6.1.
>
> | Role | Requested (§9) | Actual runtime model |
> |---|---|---|
> | Worker: epidemiology & Q0 (`verify-epidemiology-q0.md`) | Sol 6.1, high | `muse-wonder-full-1.0` fallback |
> | Worker: OTOF / FDA / CI age labels (`verify-otof-fda.md`) | Sol 6.1, high | `muse-wonder-full-1.0` fallback |
> | Worker: devices & biology (`verify-devices-biology.md`) | Sol 6.1, high | `muse-wonder-full-1.0` fallback |
> | Worker: channels & development (`verify-channels-development.md`) | Sol 6.1, high | `muse-wonder-full-1.0` fallback |
> | Adversarial skeptic (`skeptic.md`) | Sol 6.1, xhigh | `muse-wonder-full-1.0` fallback |
> | This Step 0 synthesis | Sol 6.1, xhigh | `muse-wonder-full-1.0` fallback |
>
> **GOAL §9 status — agent pre-extraction only; human dual
> extraction PENDING.** Agents may pre-extract; a human extractor
> independent of the holder must independently verify every
> load-bearing claim below, with a sampled error audit, before
> any claim is gate-deciding. Agent-only verification — including
> the skeptic pass and this synthesis — is circular for
> gate-deciding purposes and is **not** dual extraction. Until
> that human pass is done: no row in §2 pins a frozen-baseline
> number, decides Q0, or scores a Gen 0 gate cell. Rows marked
> VERIFIED below mean "matches the record the agent inspected on
> 2026-11-02, at the evidence level stated" — nothing more.
>
> **Skeptic outcome in one line:** trust the identifiers and
> headline numbers (15 of 18 falsification attempts UPHELD; no
> fabricated DOI/PMID/N/% found); discount every verdict label
> one notch (§2 applies that discount). Skeptic refs `A1–A18`,
> `B1–B8` below are to `skeptic.md`.

## 1. How to read the verdicts in §2

Verdicts are the **post-skeptic** verdicts. Where the skeptic
downgraded a worker verdict, §2 shows the downgraded form and
cites the skeptic row; the worker files keep their original
wording (no-overwrite rule, §9).

- **VERIFIED (abstract-level)** — skeptic B1 applied: the number
  matches the inspected PubMed full abstract exactly, but the
  journal full text was not line-inspected. Abstracts omit
  per-arm Ns, attrition, and definitions; these rows may not pin
  a frozen-baseline number until full-text human extraction.
- **VERIFIED (authoritative record)** — rests on an inspected
  full record beyond an abstract (FDA product page/USPI text,
  FDA SSED, ClinicalTrials.gov API v2 full record, PMC XML).
  "Single-source" is added where skeptic A5/A6/B6 requires it.
- **No record found (bounded search, 2026-11-02)** — skeptic B3
  applied: replaces every worker "VERIFIED absence". One
  term-based registry query on one date cannot verify a
  universal negative (EU CTIS / ChiCTR / ANZCTR unsearched).
- **CORRECTED** — claim needs the stated fix. **REFUTED** —
  inspected record contradicts the claim as written.
  **UNVERIFIABLE** — not confirmable from inspected records;
  what was tried is in the worker file and §5. Search snippets
  were never evidence in any source file (skeptic B8: UPHELD).

Prefixes: **E** = epidemiology/Q0, **O** = OTOF/FDA, **D** =
devices/biology, **Ch** = channels/development. Numbers follow
the worker files' row numbering.

## 2. Master claims table (skeptic downgrades applied)

| # | Claim | Final verdict | Correct value | DOI / PMID / NCT / FDA doc | N + design | Locator |
|---|---|---|---|---|---|---|
| E1 | "Danish cohort PMID 37441990" anchor (§11, App. E) | VERIFIED (abstract-level); CORRECTED against use as incidence/P0 denominator; skeptic A1 UPHELD, A2 gap added | Friis et al., *Int J Pediatr Otorhinolaryngol* 2023;171:111640. 100 Danish pediatric CI recipients (54F/46M, 0–17 y), implanted 2020–2022, Aarhus. Hereditary 44%; *SLC26A4* 14% (13% Pendred + 1% non-syndromic); syndromic 23%; non-syndromic 21% (*GJB2* most common, no numerator in abstract); TORCH 25%; cCMV-DNA+ 23%; unknown 31%. Categories overlap — do not sum. Only 23 had congenital severe-to-profound bilateral HL (implanted 8–14 mo, mean 10.5). **Gap (A2):** abstract's "23 congenital + remaining 47 progressive" = 70, not 100; other 30 unexplained in abstract — do not quote "47" against N=100 | PMID 37441990; DOI 10.1016/j.ijporl.2023.111640 | N=100; single-centre retrospective CI-recipient cohort | PubMed abstract Methods/Results/Conclusions |
| E2a | CDC EHDI as bilateral ≥70 dB incidence source | UNVERIFIABLE at the ≥70 dB bilateral cut | Not established. `cdc.gov` 403; EHDI 2022 HSFS PDFs fetched binary, no extractor in runtime; mirror not authoritative. Snippet rates not evidence. Right source = 2022 HSFS Type-and-Severity table (severe 71–90 / profound 91+ × laterality over screened births), human PDF extraction owed | CDC EHDI HSFS 2022: `01_2022-HSFS_Data-Summary.pdf`; `12_2022_HSFS_Type-and-Severity.pdf` (located, not text-inspected) | U.S. EHDI survey, births 2022; denominator not inspected | — (no inspected table cell) |
| E2b | Morton & Nance 2006 as incidence source | Identity VERIFIED; UNVERIFIABLE for ≥70 dB bilateral incidence; CORRECTED against citing for P0 cut | Morton & Nance, *N Engl J Med* 2006;354(20):2151–2164. PubMed record has no abstract; full-text PDF binary, not extracted. Widely quoted ~1.3–1.9/1000 figures are snippet-only here and use broad (≥35–40 dB-class, unilateral-included) definitions — cannot be relabelled bilateral ≥70 dB | PMID 16707752; DOI 10.1056/NEJMra050700 | Narrative review; no primary N | PubMed MEDLINE TI/PG/AID (no AB field) |
| E2c | Fortnum et al. 2001 (successor/comparator) | VERIFIED (abstract-level) for >40 dB better-ear PCHI only | UK ascertainment, born 1980–1995; better-ear >40 dB (0.5–4 kHz). Prevalence 0.91/1000 (0.85–0.98) at age 3 → 1.65 (1.62–1.68) at 9–16 y; adjusted 1.07 / 2.05. UNHS yield ~1/1000, 50–90% more by age 9 (progressive entry — birth incidence ≠ lifetime P0). No ≥70 dB split in abstract; PMC48157 not line-inspected | PMID 11546698; DOI 10.1136/bmj.323.7312.536; PMC48157 | N=17,160 children; retrospective total ascertainment, UK | PubMed abstract Results |
| E3a-i | *GJB2*/DFNB1 fractions by ancestry (§3.2) | Cohort values VERIFIED (abstract-level); ancestry-stratified universal range UNVERIFIABLE | Danish: *GJB2* most common within non-syndromic 21%, no numerator — no Danish *GJB2* % extractable. Downie 2020 (Australian population exome): *GJB2/6*-only testing 22/106 (21%) vs exome 59/106 (56%). **Errata caveat (A15):** Downie record carries two 2021 errata; contents unchecked — human extractor to confirm they don't touch these numbers. Ancestry-specific figures were snippet-only | PMID 37441990; PMID 31827275; DOI 10.1038/s41431-019-0553-8 | N=100 (Danish CI); 106/156 consented (Australian bilateral mod–profound, births 2016–17, WES+microarray) | PubMed abstracts Results (both) |
| E3a-ii | *SLC26A4*/EVA/Pendred fraction | Danish value VERIFIED (abstract-level); general P0 fraction UNVERIFIABLE | Danish CI cohort: 14/100 (14%) = 13% Pendred + 1% non-syndromic — high, population-specific, CI-selected. No second inspected source for U.S./P0 fraction; Downie gene-level table (PMC7171096) located, not line-inspected | PMID 37441990; DOI 10.1016/j.ijporl.2023.111640 | N=100 | Abstract Results + Conclusions |
| E3a-iii | Congenital CMV fractions | VERIFIED (abstract-level), two denominators kept separate; skeptic A14 UPHELD | Grosse et al. 2008 (universal-screening review): ~14% of cCMV children develop any SNHL; 3–5% bilateral moderate-to-profound; 15–20% of all bilateral moderate-to-profound SNHL attributable to cCMV. Broader than P0 ≥70 dB, includes progression — upper-bound guide only. Danish: cCMV-DNA+ 23/100 CI recipients. Do not average | PMID 17959414; DOI 10.1016/j.jcv.2007.09.004; PMID 37441990 | Systematic review (pooled N not in abstract); Danish N=100 | Abstract Results (both) |
| E3a-iv | *OTOF* fraction; §1.2 "tens of newborns/year" | UNVERIFIABLE — "tens/year" is unverified arithmetic until recomputed | GeneReviews NBK1251 blocked (reCAPTCHA). "1–8%"-style figures snippet-only with shifting denominators (congenital HL vs AR nonsyndromic vs ANSD). No % endorsed. Owed: GeneReviews Prevalence + one P0-like genomic cohort, then explicit recomputation (see also O1d) | GeneReviews NBK1251 (located, not inspected) | — | — |
| E3b | Additional disabilities "~30–40%" (§3.1) | UNVERIFIABLE as primary-source range | Gallaudet Annual Survey chain located via secondary citations only; reports not inspected. Snippet cohort values range ~15% (CI longitudinal) to ~40% (school D/HH survey) — definition/ascertainment-bound. Step 1 must pin population, definition/instruments, ascertainment age; school-age fraction must not be applied to P0 infants unadjusted | None relied on. Pointer: Gallaudet Research Institute Annual Survey (2011 report on 2009–10; 2013) | — | — |
| E4a | Q0: post-CI human fibrosis/ossification; scala-patency % | Tissue response VERIFIED (abstract-level); patency-for-AAV % UNVERIFIABLE | Seyyedi & Nadol 2014: granulomatous reaction 27/28 (96.4%), basal > distal. Kamakura & Nadol 2016: fibrous tissue + new bone 17/17; new-bone % volume (not fibrous %) negatively correlated with CNC scores. Hodge 2021: **otosclerosis only** — cochleostomy → basal obliteration, round window → minimal; CORRECTED against generalising to infant cochleae. No inspected source reports "% scala patent/cannulable for later infusion" by time-since-implant. Series are small (17–28 bones), adult, older-device — presence of tissue is near-universal; volume/distribution is the variable | Seyyedi PMID 25122600, DOI 10.1097/MAO.0000000000000540, PMC4165780; Kamakura PMID 27371868, DOI 10.1016/j.heares.2016.06.015, PMC5018452; Hodge PMID 34607995, DOI 10.1097/MAO.0000000000003327, PMC8595606 | 28 bones/21 subjects; 17 bones (3D volumetry); 17 bones (13 implanted + 4 controls, otosclerosis) | Abstracts Methods/Results (all three) |
| E4b | Q0: AAV delivery after established CI (animal) | CORRECTED (sequence claim downgraded per skeptic B5 to UNVERIFIABLE-pending-inspection) / negative half = bounded-search result | The sequencing conclusion ("AAV inoculated prior to implant insertion", PMC4674315) rests on located excerpts; abstract-level MEDLINE inspection of that paper was not completed — **do not cite its sequence or numbers from Step 0**. What stands (B3 form): no post-CI (established implant/fibrosis) AAV-delivery primary study was found in this bounded search. Q0 currently has no direct animal evidence either way on post-CI transduction | PMC4674315 (*Hear Res* 2015, Pfingst group) — located, not inspected to standard | Adult guinea pigs, ototoxically deafened; exact N not verified | — |
| E4c | Q0: hearing-preservation residual-hearing rates | VERIFIED (abstract-level); CORRECTED against applying to ≥70 dB infants; skeptic A13 UPHELD | Madgar et al. 2025: pediatric CI hearing preservation in **78% of ears (95% CI 71–85%)**, I²=79.96%; mean age 9.68 y; mean PTA 60.48 → 70.95 dB. Preservation definitions vary by primary study; durability not established by abstract. ≠ scala patency for AAV; ≠ evidence about <12-mo ≥70 dB infants | PMID 40052291; DOI 10.1002/ohn.1180 | 24 studies, 567 patients; meta-analysis of proportions | Abstract Results |
| E4d | Otarmeni "no prior CI" = label exclusion (§1.2/§1.3) | VERIFIED as label fact — **via O1b (supersedes this row's partial verdict; skeptic A6)** | Epi worker verified only the FDA announcement (23 Apr 2026) and could not text-inspect its label PDF (binary); otof worker text-extracted the USPI and quoted exact §1 wording (O1b). Operative locus = USPI §1 (O1b), not "unknown". §1.3 separation stands: label exclusion = regulatory fact about studied population, not biological impossibility; conversely unstudied ≠ "preserved option" for Family G scoring | FDA news release 23 Apr 2026; USPI (see O1b) | Regulatory documents | FDA announcement ¶1; USPI §1 via O1b |
| O1a | Otarmeni FDA accelerated approval, April 2026 (§1.2(1)) | VERIFIED (authoritative record); skeptic A3 UPHELD against live FDA page | Approval letter **April 23, 2026**; STN 125874; lunsotogene parvec-cwha; OTARMENI; Regeneron. SBRA April 22, 2026. Accelerated approval on Week-24 average-PTA hearing-sensitivity improvement; continued approval contingent on confirmatory trial | FDA OTARMENI product page (STN 125874; Package Insert media 192098) + USPI (`otarmeni_fpi.pdf`, 5 pp., text-extracted) | BLA dual-AAV1; basis Study DB-OTO-001, N=24 treated (O2b) | FDA page Supporting Documents; USPI p.1 Highlights + §1 |
| O1b | Indication incl. prior-CI exclusion (§1.2(1)) | VERIFIED (authoritative record) with exact-wording correction; supersedes E4d partial verdict (A6) | USPI §1 verbatim substance: "pediatric and adult patients with severe-to-profound and profound sensorineural hearing loss (any frequency >90 dB HL) associated with molecularly confirmed biallelic variants in the OTOF gene, preserved outer hair cell function, and **no prior cochlear implant in the same ear**." GOAL "treated ear" = label "same ear". Limitations: not recommended if imaging shows inner-ear access infeasible. §2.1: confirm biallelic likely-pathogenic/pathogenic variants | USPI (above) | — (label) | USPI p.1 Highlights, §1, §2.1 |
| O1c | Otarmeni labelled age limits | CORRECTED: no numeric age limits in indication | Indication says only "pediatric and adult" — no minimum/maximum. Studied: 24 pediatric patients aged 10 mo–16 y (§8.4; median 2 y §14); ≥65 y not studied (§8.5). "≥10 mo labelled minimum" would be wrong: 10 mo = youngest studied | USPI §§1, 8.4, 8.5, 14 | N=24, 10 mo–16 y | USPI p.3, pp.4–5 |
| O1d | "Tens of newborns/year" U.S. incidence (§1.2(1)) | UNVERIFIABLE (agrees with E3a-iv) | No incidence figure in USPI or FDA product page. Must be computed in Appendix D from primary epidemiology; press figures not evidence | — | — | USPI full text + FDA page (absence) |
| O2a | CHORD (DB-OTO-001) design | VERIFIED (authoritative record + abstract-level) | Phase 1/2, open-label, multicenter, single-arm (non-randomized, masking NONE), single ascending-dose unilateral → bilateral expansion (Parts A/B/C). Single intracochlear infusion, **7.2×10¹² vg/ear in 0.24 mL**. Registry: RECRUITING, est. enrollment 36, start 2023-06-27, est. primary completion 2029-02-26, est. completion 2032 (updated 2026-08-05). NEJM wording: "open-label, single-group, first-in-human registrational study" | NCT05788536 (CTgov API v2, inspected); PMID 41085057; DOI 10.1056/NEJMoa2400521; USPI §14 | See O2b | CTgov modules; PubMed abstract Methods; USPI §14 |
| O2b | CHORD N enrolled vs evaluable | VERIFIED (authoritative record; label numbers single-source per A5) — three Ns, do not conflate | (i) Label treated: **N=24** (10 unilateral, 14 bilateral), median 2 y (10 mo–16 y). (ii) Label efficacy: **20** completed Week-24 assessments (1 without data imputed non-responder). (iii) NEJM first report: **12 enrolled**. Registry 36 = target, not enrolled N | USPI §§6.1, 14 Tables 1–2; PMID 41085057; NCT05788536 | 24 treated / 20 efficacy / 12 NEJM cut; single-arm open-label | USPI p.3 §6.1, §14; abstract Results |
| O2c | "~80% reaching PTA ≤70 dB HL" (§1.2(1)) | Numbers UPHELD (A4/A5); set attribution CORRECTED; "NEJM 2025" issue year REFUTED (A4) | Label set: **16/20 = 80% (95% CI 56–94%)** ≤70 dB HL at Week 24 (single-source PDF extraction, A5 — human re-read owed). NEJM cut: **9/12 = 75% (43–95; P=1.1×10⁻¹³)**. "~80% of an evaluable set" = label 20, not NEJM 12. Cite paper as **epub Oct 2025; issue *NEJM* 2026 Mar 12;394(11):1074–1083**. GOAL gloss "still severe loss" imprecise per-patient: label also reports 9/20 (45%) ≤45 dB, 3/20 (15%) ≤25 dB at Week 24 | USPI §14 Table 2; DOI 10.1056/NEJMoa2400521; PMID 41085057 | 16/20 (label); 9/12 (NEJM) | USPI §14 Table 2 + following text; abstract Results |
| O2d | CHORD endpoints ("surrogate, confirmatory pending") | VERIFIED (authoritative record + abstract-level; label results single-source per A5) | Primary: average PTA (0.5/1/2/4 kHz) ≤70 dB HL at Week 24. Key secondary: ABR click ≤90 dB nHL — label 14/20 = 70% (46–88%); NEJM 9/12 both endpoints. FDA label wording is "improvement of hearing sensitivity", not "surrogate" — GOAL's gloss is supported in substance (accelerated approval, confirmatory contingent), not verbatim | USPI §§1, 14 Table 2; NCT05788536 outcomes; PMID 41085057 | Single-arm; Week 24 (label) / to Week 104 (registry) | USPI §14; CTgov outcomesModule |
| O2e | CHORD durability | VERIFIED (authoritative record; label subset single-source per A5), bounded | Median safety follow-up 45 weeks (9–115). Week-48 subset: 10/12 (83%) ≤70 dB; 8/12 ≤45; 5/12 ≤25; 9/12 ABR ≤90. One rescue CI ~8 mo post-dose (treatment failure). <1-y median, subset only — not long-term durability; registry follow-up to Week 104, completion est. 2032 | USPI §§6.1, 14; NCT05788536 | 12/20 at Week 48 | USPI §6.1; §14 post-Table-2 paras |
| O3a | AK-OTOF (Lilly/Akouos) status | VERIFIED (registry); "Phase 1/2" CORRECTED as stale; skeptic A18 UPHELD via CTgov API | NCT05821959 (AK-OTOF-101 / AAVAnc80-hOTOF, LY888891; sponsor Eli Lilly): phases **["PHASE3"]**, RECRUITING, est. N=48, start 2023-09-15, est. primary completion 2028-10, completion 2029-12 (updated 2026-09-29). No FDA approval. Efficacy claims not verified here | NCT05821959 (CTgov API v2) | Est. N=48; non-randomized sequential open-label | CTgov identification/status/design/description |
| O3b | SENS-501 (Sensorion) status | Registry VERIFIED; discontinuation UNVERIFIABLE (pointer only) | NCT06370351 (AUDIOGENE): Phase 1/2, children 6–31 mo, est. N=12, **ACTIVE_NOT_RECRUITING** (updated 2026-07-08), est. primary completion 2027-07, completion 2031-07. June 2026 discontinuation located via search + secondary trade news; sponsor primary fetch timed out, no registry termination record inspected — "discontinued" must not be asserted from Step 0 | NCT06370351 (CTgov API v2) | Est. N=12; non-randomized sequential open-label | CTgov status/design |
| O3c | Other *OTOF* AAV programs | One registry pointer VERIFIED; completeness UNVERIFIABLE | Otovia OTOV101 NCT05901480: status UNKNOWN (last known RECRUITING), est. N=25, updated 2024-05-08 — stale, do not present as currently recruiting. Chinese academic programs (e.g. Fudan AAV1-hOTOF, ChiCTR) located in secondary sources only; no registry/journal record inspected — no ID/N/status asserted | NCT05901480 (CTgov API v2) | Est. N=25 (Otovia) | CTgov identification/status/design |
| O4a | Cochlear Nucleus pediatric minimum age (FDA) | VERIFIED (authoritative record): 9 months | Nucleus 24: children **9–24 mo** with bilateral profound SNHL + limited binaural HA benefit (≥2 y: severe-to-profound). Approval March 17, 2020 | FDA SSED P970051/S172 (accessdata.fda.gov, text-extracted) | Labelling supplement (literature-based expansion) | SSED p.1 §§I–II |
| O4b | MED-EL pediatric minimum age (FDA) | CORRECTED to 7 months — **mirror-verified, provisional** (skeptic B6 DOWNGRADE) | Expanded indication: **7 mo–17 y 11 mo** bilateral SNHL; 7–11 mo requires profound (PTA3 ≥90 dB HL). Approval November 26, 2025 (prior: ≥18 mo 2001 → 12 mo S006). PDF came via `fda.innolitics` mirror, not accessdata.fda.gov — 7 mo is provisional until re-pulled from FDA. Triggers §3.4 comparator-drift consideration either way | FDA SSED P000025/S134 (mirror copy, text-extracted) | Panel-track PMA supplement | SSED pp.1–2 §§I–II |
| O4c | Advanced Bionics pediatric minimum age (FDA) | UNVERIFIABLE against inspected FDA record (12 mo = pointer only) | No AB SSED/labelling PDF inspected (PMA P960058 page HTTP 400). Secondary pointers (manufacturer IFUs; 2021 PMC review PMC8660172, PMID 34912165, DOI 10.1055/s-0041-1739370, full text inspected) consistent with long-standing 12-mo criterion. AB July 2026 expansion = SSD/asymmetric loss, not bilateral minimum-age lowering. Do not cite "AB = 12 mo (FDA-verified)" from Step 0 | P960058 (not inspected); PMC8660172 (secondary) | — | PMC full text; AB press page |
| O4d | "9–12 mo" = cohort descriptor, not universal label (§3.4) | VERIFIED as correct caution — now understated | Minima differ by maker and era: Cochlear 9 mo (2020), MED-EL 7 mo provisional (2025), AB unverified (pointer 12 mo). No universal FDA minimum exists. Step 1 must pin era + per-device mix | P970051/S172; P000025/S134 | — | SSEDs §II |
| D1a | "2020 multichannel μLED *EMBO Mol Med* paper" (Dieter) | CORRECTED (conflation of 3 papers, D1b/D1c); content VERIFIED (abstract-level); skeptic A7 UPHELD | Dieter A et al., "μLED-based optical cochlear implants…", *EMBO Mol Med* 2020;12(8):e12387. Acute stimulation in **adult Mongolian gerbils**; **16 thin-film μLEDs**; tonotopic activation, hearing + deaf gerbils; virus-mediated opsin. Acute ≠ chronic, behavioral, or human | DOI 10.15252/emmm.202012387; PMID 32596983 | N not in abstract; acute gerbil device feasibility | PubMed abstract |
| D1b | Single "2020 multichannel" paper (implicit) | CORRECTED — distinct second paper; narrow existence/title claim UPHELD (skeptic B4) | Keppeler D et al., "Multichannel optogenetic stimulation of the auditory pathway using microfabricated LED cochlear implants in rodents", *Sci Transl Med* 2020. Carries the "Multichannel optogenetic stimulation…" title — must not be merged with D1a. Only DOI→PMID mapping inspected; findings beyond title not asserted | DOI 10.1126/scitranslmed.abb8086; PMID 32718992 | Rodent; N not verified | PubMed DOI esearch |
| D1c | "Dieter/Moser *EMBO Mol Med* 2020" (singular) | CORRECTED — third 2020 item is a review; existence UPHELD narrowly (B4) | Dieter, Keppeler & Moser, "Towards the optical cochlear implant…", *EMBO Mol Med* 2020;12:e11618. Review/perspective — not experimental μLED evidence. Locator = publisher reference list; full text not separately inspected; no findings claimed | DOI 10.15252/emmm.201911618 | N/A (review) | Springer chapter reference list |
| D1d-i | 2025/2026 Moser optogenetics (ChReef) | VERIFIED (abstract-level); skeptic A8 UPHELD | Alekseev A et al., "Efficient and sustained optogenetic control of sensory and cardiac systems", *Nat Biomed Eng* ©2025, issue 2026 Feb;10(2):277–292. ChReef (ChRmine variant; 80 fS; ~30 ms closing); auditory-pathway stimulation in **rodents and NHP** at nanojoule thresholds. No human auditory subjects. 2025-DOI/2026-issue dual dating is correct | DOI 10.1038/s41551-025-01461-1; PMID 40721511 | N not in abstract; multi-system animal study | PubMed abstract |
| D1d-ii | 2026 *EMBO Mol Med* multichannel oCI paper | **Existence/DOI VERIFIED to Crossref-abstract level** (skeptic A9 — worker implied doubt REFUTED); numbers still unscored | DOI resolves via Crossref to "Multichannel optical cochlear implants enable spectrally distinct auditory activity", *EMBO Mol Med*, published **2026-10-22** (Albrecht/Koert/…/Moser): ChReef in gerbil SGNs + oCIs of **5–10 green LEDs**, ICC thresholds <200 nJ. Workers' "3 non-matching PMIDs" = query-syntax artifact; proper `[AID]` search = 0 PubMed hits (not yet indexed). Full text not inspected (Springer auth-redirect) — N/findings remain UNVERIFIABLE beyond Crossref abstract. Worker detail "AAV-PHP.S" appears in no inspected record: **DOWNGRADED unverified — delete or source it** | DOI 10.1038/s44321-026-00541-2 (Crossref record; no PMID at 2026-11-02) | Gerbil (Crossref abstract); N not verified | Crossref record (skeptic A9); Springer page located, full text not inspected |
| D1e | "No human / no infant human data" (optical CI) | CORRECTED + bounded-search form (B3): no optogenetic-oCI human record found; separate adult IR feasibility exists | Optogenetic (Moser-type) oCI: no human efficacy data in inspected records (gerbil/rodent/NHP only); infant claim holds a fortiori. Must be separated from non-optogenetic infrared stimulation: Northwestern NCT05110183 = acute intraoperative light-delivery + CAP test during translabyrinthine surgery in ears slated for labyrinthectomy; enrolling by invitation (verified 2026-05; start 2025-04-20; est. completion 2027-12-31); **no results posted**; not pediatric, no opsin, not hearing restoration. Registry N not quoted (truncated fetch) — do not cite an N | NCT05110183 (CTgov API v2) | Single-session intraoperative add-on (~30 min); N not verified | CTgov Identification/Status/Description |
| D2a | ANI *Bioelectronic Medicine* paper | VERIFIED (abstract-level) as concept/review; CORRECTED if read as bench-data paper; skeptic A17 UPHELD | Lenarz T et al., "The auditory nerve implant—concept and device description…", *Bioelectron Med* 2025;11:26. Human translation framed as future: device "validated in chronic animal studies" = future work; "Once in humans…" conditional. No N, denominators, or bench numbers in abstract. Correction notice 2025;11:31 | DOI 10.1186/s42234-025-00188-3; PMID 41131644; correction DOI 10.1186/s42234-025-00197-2 | N/A (review) | PubMed abstract |
| D2b | ANI bench aging/pulse data ("6.3 billion pulses" etc.) | UNVERIFIABLE from inspected primaries — pointers only, must not enter scoring | Pulse/aging numbers exist only in secondary news summaries (Utah-slant "AN-USA", 3×5 shanks). Primary bench DOI/PMID not located; no full text inspected. Step 0 must produce the primary citation (N devices/electrodes, failure definition, charge density) or record bench durability as INSUFFICIENT | — (no verified ID) | — | Search log; contrast D2a abstract |
| D2c | "Chronic cat" / 6-month denominators (§8E example) | REFUTED as stated for located feline paper; chronic denominators UNVERIFIABLE | Thomas WM et al., *Front Neurosci* 2024;18:1308663 is a **surgical-model development** study "for future chronic animal work" — not a 6-month success/migration cohort. Historical cat intraneural work is acute (≤52 h class). "Pilot Chronic Evaluation…" title located in listings, full record not inspected. No verified cat N, duration, success/failure, or migration rate exists in Step 0. Exact animal N here not verified (PMC blocked/429) | DOI 10.3389/fnins.2024.1308663; PMID 38379760; PMC10877721; concept history PMID 41131644 | Cat surgical-feasibility model; N not verified | Frontiers full text (aims/discussion); PubMed record |
| D2d | "No human ANI data" | No record found (bounded search, B3) — replaces worker "VERIFIED" | CTgov term query 2026-11-02 found no ANI interventional trial; concept review (D2a) is pre-translation; cadaveric/congress-abstract work ≠ human in-vivo data. EU CTIS unsearched; repeat with frozen strings before Gen 0 freeze. Infant CPA-access anatomy: not verified (no inspected study) | — (registry query 2026-11-02) | — | PMID 41131644 abstract; CTgov API v2 query |
| D3a | Pinyon et al. 2014 identity/journal | VERIFIED (abstract-level) — journal confirmed | Pinyon JL et al. (Housley GD senior), "Close-field electroporation gene delivery using the cochlear implant electrode array enhances the bionic ear", *Sci Transl Med* 2014;6(233):233ra54. UNSW affiliation confirmed | DOI 10.1126/scitranslmed.3008177; PMID 24760189 | Guinea pig bilateral ototoxic model; N not in abstract | PubMed MEDLINE TI/SO/FAU/AD |
| D3b | Pinyon exact findings | VERIFIED (abstract-level); numeric thresholds UNVERIFIABLE without full text | CI-array electroporation of BDNF cDNA → SGN neurite regrowth after 2-wk ototoxic atrophy; GFP control failed. Ectopic branching reported; eABR lower thresholds/wider dynamic range (no numbers in abstract). Limits: short-deafness model ≠ congenital lifelong deafness; tonotopic order not established; eABR ≠ speech; no durability/tumor data in abstract | DOI 10.1126/scitranslmed.3008177; PMID 24760189 | BDNF vs GFP vs unimplanted; N/arm not in abstract | PubMed abstract |
| D3c | "No human trial 2014–2026" (Pinyon mechanism) | No record found (bounded search, B3) for Pinyon mechanism specifically; cause of silence unexplained | CTgov query (CI + BDNF/neurotrophin) returned `{"studies":[]}`. Non-equivalent neighbors must not be conflated: NCT05040217 = AAV2-BDNF for Alzheimer's (brain); NCT07032038 = auditory-progenitor **cell** therapy per secondary reporting (registry not inspected — no details asserted). §8B "must be explained" remains an open gap: no inspected record establishes why (safety/durability/IP/funding unknown). Frozen multi-registry search (CTgov+CTIS+ANZCTR) owed | No NCT (Pinyon mechanism). Neighbors: NCT05040217; NCT07032038 (secondary only) | N/A | CTgov API v2 response 2026-11-02 |
| D4a | "Liu 2025" (reprogramming) | UNVERIFIABLE as cited — delete or fully specify; nearest anchor is Liu 2024; skeptic A16 UPHELD | No record uniquely matches "Liu 2025". Nearest: Liu Y et al., *Hear Res* 2024;441:108916 — mature guinea-pig flat epithelium, adenoviral GAPS; MyVIIa+ cells **under** (not within) epithelium at 1–2 mo; no ABR/threshold restoration in abstract; N/arm not stated ("larger N at two months"). Whether GOAL meant this (mis-dated) or another Liu is indeterminate. Must not be scored | Nearest: DOI 10.1016/j.heares.2023.108916; PMID 38103445 | Mature guinea pig severe-lesion model; N not stated | PubMed abstract |
| D4b | "Qiao 2024" (reprogramming) | UNVERIFIABLE as cited — delete or fully specify; must not be scored | No Qiao-first-author 2024 reprogramming record found. Historical Qiao AAV-delivery co-authorship (2019-era vector work) and an unrelated 2026 OHC paper are category errors if cited here | — (no verified ID) | — | Search log 2026-11-02 |
| D4c | Mature-cochlea reprogramming "failure" | CORRECTED: conversion occurs without verified hearing restoration; §8D advance criterion unmet in inspected records. Sub-item (ii) findings DOWNGRADED pointer-level (B4) | (i) McGovern et al., *PNAS* 2024;121(5):e2304680121: 3-factor reprogramming of nonsensory cells **adjacent to** organ of Corti in mature mouse; no ABR-restoration claim asserted here (PMC XML front matter inspected). (ii) McGovern et al., *PNAS Nexus* 2024;3(10):pgae445: "1-/2-factor insufficient in adult supporting cells" rests on secondary-list located abstract text — **pointer-level until PubMed/PMC record directly inspected (B4)**. Supporting-cell consumption = alteration (G4). No inspected record = replicated threshold restoration + cochlear identity + synapses in mature deafened **large-animal** cochlea. Family D = literature watch stands | (i) DOI 10.1073/pnas.2304680121; PMID 38266052; PMC10835112. (ii) DOI 10.1093/pnasnexus/pgae445; PMC11477985 (PMID not asserted) | Adult mouse; N/experiment not verified. No large animal, no human | (i) PMC XML (E-utilities). (ii) HRP list + located PDF (abstract-level, secondary) |
| Ch1a | "Friesen, Shannon & Cruz 2001" → ~4–10 channels (§1.2, §3.4, §4.2 G1) | CORRECTED (authors + gloss); numbers VERIFIED (abstract-level); skeptic A10 UPHELD | Correct authors: Friesen, Shannon, **Baskent & Wang** — no Cruz. *J Acoust Soc Am* 2001;110(2):1150–1163. CI plateau **7–8 electrodes** (vowel/consonant ≤7; word/sentence marginal 7→10 in Nucleus-22 only; low performers no gain beyond 4). NH vocoder improved to **≥20 channels** — vocoder arm does not support a 4–10 ceiling. "4–10" is a fair gloss of the span, never stated by the paper; cite as "plateau ~7–8 (range ~4 to marginal 10), 2001-era arrays" | PMID 11519582; DOI 10.1121/1.1381538 | N=5 NH, N=10 Nucleus-22, N=9 Clarion; SNRs +15/+10/+5/0 dB + quiet | PubMed abstract Results |
| Ch1b | Successors confirm 4–10 / point-8 anchor | CORRECTED: modern perimodiolar data show gains beyond 8–10 | Berg et al. 2019 (*J Acoust Soc Am* 145(3):1556): imaging-verified scala-tympani perimodiolar recipients; 16-ch CIS > 8-ch (speech in quiet), 16 maxima > 8/10 across tasks incl. noise; benefit inversely tied to electrode-modiolus distance. Does not refute current spread; refutes "successors uniformly confirm 4–10". Step 1 must state array/task/channels-vs-maxima definition for the point-8 anchor (PASS ≥12 P / ≥16 R) | PMID 31067952; DOI 10.1121/1.5092350; PMC6435372 | N=30 adults; CIS 4/8/10/16 + n-of-m 16 maxima | PubMed abstract (PMC HTML blocked) |
| Ch2a | Focusing narrows spread at higher charge cost | VERIFIED (abstract-level) | Phased array (van den Honert & Kelsall 2007): focusing realizable, "at the cost of increased total stimulation current" — voltage-cancellation sense, no speech endpoint. Tripolar spread reduction = established background per Srinivasan 2013. Battery cost quantified: dynamic focusing −48% battery life (5.1 h, p<0.001) vs monopolar (van Groesen 2023) | PMID 17552721; DOI 10.1121/1.2722047; PMID 23467170; PMID 36279119 | N=3 (2007 validation); see Ch2b | PubMed abstracts |
| Ch2b | "Without durable speech-in-noise translation" (§1.2) | CORRECTED: outcomes mixed — acute positive, take-home null; clinical-adoption fact UNVERIFIABLE from inspected records | Srinivasan 2013 (*Hear Res* 299:29–36): partial-tripolar +2.7 dB (digits) / +3 dB (sentences) SRT vs **degraded experimental monopolar**, no acute deficit vs clinical map; N not in abstract (PMC3639477 blocked — do not cite N). Bierer & Litvak 2016: group null, poorer performers tended better (9 ears/8 listeners; vowels/consonants, not SRT). van Groesen 2023 take-home crossover (13 fitted, 9 completed): null in noise; authors: "does not consistently improve". Caswell-Midwinter & Arenberg 2023 (14 ears): group null, unclear individual benefit. No FDA-label/CTgov adoption record inspected in this pass | PMID 23467170, DOI 10.1016/j.heares.2013.02.004, PMC3639477; PMID 27317668, DOI 10.1177/2331216516653389; PMID 36279119, DOI 10.1097/AUD.0000000000001282; PMID 37226501, DOI 10.1177/23312165231176157 | As stated per study; Srinivasan N UNVERIFIED | PubMed abstracts (each) |
| Ch3 | "Kral et al. *Trends Neurosci* 2023" (§8H tag; §11; App. E) | CORRECTED (identity/topic); §8H support VERIFIED at partial-full-text level (skeptic B2 DOWNGRADE) | Exact: Kral & Sharma, "Crossmodal plasticity in hearing loss", *Trends Neurosci* 2023;46(5):377–393 — crossmodal-plasticity **review, not sensitive-period paper**. Claims (abstract + publisher PDF pp.377–378 only — 2 pp. of 377–393, B2): crossmodal reorganization does not close critical periods, is reversible/compensatory, does not harm restoration preconditions; "no sign before CI" advice needs modification. Supports §8H as tagged. Sensitive-period anchor is Kral & Sharma **2012**, *Trends Neurosci* 35(2):111–122 (still a review). Human extractor to confirm no later passage reverses intro framing | 2023: PMID 36990952, DOI 10.1016/j.tins.2023.02.004, PMC10121905. 2012: PMID 22104561, DOI 10.1016/j.tins.2011.09.004, PMC3561718 | Reviews; no N | PubMed abstracts; 2023 PDF pp.377–378 (partial) |
| Ch4 | *Hearing Research* 2025 "nine-months" paper (§11, App. E) | Identity/thesis VERIFIED (abstract-level + partial PDF); Fig. 1 stats DOWNGRADED partial-PDF (skeptic A12) | Kral, Kishon-Rabin, O'Donoghue & Romeo, "Sensorimotor contingencies in congenital hearing loss: The critical first nine months", *Hear Res* 2025 Nov;467:109401 (received 29 Apr, accepted 11 Aug, online 13 Aug 2025; CC BY). **Narrative review/proposal — no cohort, no trial.** Proposes first-year sensorimotor synchrony as critical while citing "~3-year critical period" for therapy in same abstract ("We propose…"). Fig. 1 sales-data stat (F(6,68)=0.39, p=0.88; <20% implanted in year 1) rests on PDF pp.1–3+Summary of 14 pp. — partial, unverified by skeptic. GOAL's W0 = "hypothesis to test" is the correct weight; must not be upgraded to causal 9-mo evidence | PMID 40907462; DOI 10.1016/j.heares.2025.109401 | Review; sales-data description (11 countries, 2017–2023) per partial PDF | PubMed abstract; journal PDF pp.1–3 + Summary (partial) |
| Ch5 | "~3.5 years" = P1 heuristic, not deadline (§1.2) | VERIFIED (abstract-level); skeptic A11 UPHELD | Sharma, Dorman & Spahr 2002 (*Ear Hear* 23(6):532–539): P1 latency normalized within 6 mo if deprivation ≲3.5 y; variable plasticity to ~7 y; greatly reduced after 7 y. Follow-up Sharma et al. 2005 (*Hear Res* 203:134–143; N=21+2) uses same cutoffs. Cautions: P1 ≠ language outcome (§5.3 proxy chain still owed); 2002 earliest implant 1.3 y — says nothing direct about W0 (0–9 mo) advantage | PMID 12476090, DOI 10.1097/00003446-200212000-00004; PMID 15855038, DOI 10.1016/j.heares.2004.12.010 | N=104 + 3 adults (2002, cross-sectional); N=21+2 (2005) | PubMed abstracts (both) |

Tier note for Gen 0 (from D-file, carried unchanged): every
device/biology item in D-rows is T0–T2 (bench/rodent/gerbil/
guinea pig/cat model; one adult intraoperative IR protocol with
no results). None supports a G2/G3 PASS. Inventor-lab allegiance
downgrade (§5.2) applies to Moser-group, ANI-consortium, UNSW,
and Groves-lab single-source claims. No verified response
fraction with a P0 denominator exists anywhere in §2.

Registry-date note (skeptic B7, UPHELD): future-looking registry
fields (NCT05788536 updated 2026-08-05; SENS-501 2026-07-08;
CHORD completion 2032; NCT05110183 verified 2026-05) all precede
the 2026-11-02 verification date as *postings* or are estimates;
A18 independently confirms 2026 registry dates are genuine. No
date correction required.
## 3. Corrections required to GOAL.md text (do not edit here)

Holder + independent co-approver to apply (§12); this file lists
but does not make these edits. Grouped by GOAL location.
Skeptic "fix before Step 1" items (A4/A5/A6/A9/B1/B3/B6/A2/A15)
are marked ★.

### §1.2, fact 1 (gene therapy)

1. **C1 — Pin the 80% to its set and fix the gloss.** "~80% of an
   evaluable set" = FDA-label 16/20, not NEJM 9/12=75%; state the
   three Ns (24 treated / 20 efficacy / 12 NEJM). "Still severe
   loss" describes the endpoint threshold, not every responder:
   add 9/20 ≤45 dB, 3/20 ≤25 dB at Week 24 (label; single-source,
   human re-read pending, ★A5). Cite the paper as epub Oct 2025,
   issue Mar 2026 wherever "NEJM 2025" phrasing is implied
   (★A4). Keep "treated ear" only as gloss for label "same ear";
   quote USPI §1 verbatim in any Step 1 text (O1b). Do not state
   a labelled minimum age — none exists (O1c).
2. **C2 — "Tens of newborns/year" and "large majority" stay
   uncomputed.** No *OTOF* fraction with a named denominator was
   verified (E3a-iv/O1d). Retain "must be computed (Appendix D)"
   and do not let "on the order of tens" harden into an input
   until D1/D2 exist.

### §1.2, fact 2 (CI resolution) + §3.4 + §4.2 G1

3. **C3 — Fix the Friesen citation everywhere** (also App. E):
   "Friesen, Shannon, Baskent & Wang 2001" (no Cruz);
   DOI 10.1121/1.1381538. Replace "supports roughly 4–10
   effective spectral channels" with the plateau wording:
   "~7–8 electrodes for most materials in 2001-era arrays (range
   ~4 to a marginal 10); NH vocoder ≥20" (Ch1a). Carry
   "(abstract-level)" until full-text extraction (★B1).
4. **C4 — Qualify the G1 point anchor.** Berg 2019 shows gains
   beyond 8–10 in modern perimodiolar arrays (Ch1b). §3.4 "G1
   4–10" and §4.2 point-8 (PASS ≥12/≥16) need a Step 1 footnote
   stating array type, task, and channels-vs-maxima definition,
   or a contemporary standard device approaches the Track P bar
   on the anchor task. "Spread-of-excitation work" behind the
   ripple-to-channels model still needs its own citations
   (Ch-unresolved 4).
5. **C5 — Reword the focusing sentence.** "Without durable
   speech-in-noise translation" → "without *consistent*
   speech-in-noise translation in take-home testing", acknowledging
   Srinivasan 2013's acute +2.7/+3 dB (vs degraded comparator),
   the take-home nulls, and ~48% battery cost (Ch2b).
   "No durable clinical adoption" as a market/regulatory fact
   remains unverified — do not assert it until a label/registry
   search is done. Family A (§8A) challengers must explain all
   three, not one "failure".

### §1.2, fact 2–3 / §8H / Kral anchors

6. **C6 — Narrow "no human data" sentences.** Use bounded-search
   wording everywhere (★B3): "No human data for optogenetic oCI
   found in bounded search (2026-11-02); no infant human data for
   any optical CI. Separate adult acute intraoperative infrared
   feasibility (NCT05110183, no results) is not optogenetic-oCI
   evidence" (D1e). Same form for ANI (D2d) and Pinyon (D3c).
7. **C7 — Cite Kral correctly, twice.** *Trends Neurosci* 2023 =
   Kral & Sharma crossmodal-plasticity review — supports §8H,
   establishes no sensitive-period gradient (Ch3, partial-PDF
   caveat ★B2). Sensitive-period review = Kral & Sharma 2012.
   *Hear Res* 2025 nine-months paper = narrative proposal
   coexisting with a ~3-y critical period (Ch4); GOAL's W0-
   hypothesis framing is correct and must not be upgraded in
   Step 1; its Fig. 1 stats are partial-PDF extraction (★A12).
   Sharma 2002 supports "3.5 y = heuristic" but says nothing
   about 0–9 mo (Ch5).

### §2.2 prior-art rows (see §4 below for completed table)

8. **C8 — Split conflations.** (a) Three distinct 2020 oCI
   papers (D1a μLED experimental / D1b Keppeler / D1c review);
   add ChReef 2025/2026 (D1d-i) and the now-existence-verified
   2026 *EMBO Mol Med* paper (D1d-ii, ★A9; delete "AAV-PHP.S").
   (b) **ANI ≠ ABI**: separate rows; ABI has existing clinical
   use and was not verified in Step 0 — do not score it from
   ANI rows. (c) "Bench + chronic cat" → concept review +
   surgical-feasibility cat model; bench/chronic primaries
   missing (D2b/D2c). (d) "Mature-cochlea failure" → "mature-
   cochlea conversion without demonstrated functional hearing
   restoration" (D4c). (e) *OTOF* "others" → named rows with
   registry states as of 2026-11-02 (O3a Phase 3, O3b/O3c).

### §3.1 / §3.4 / Appendix D (epidemiology & baseline)

9. **C9 — Keep "~30–40%" flagged as unverified.** §3.1's
   additional-disabilities range has no primary-source support
   yet (E3b); Step 1 pins population/definition/instruments/
   ascertainment age before any use. Same for *GJB2*-by-ancestry
   ranges (§3.2): only cohort values exist (E3a-i, Downie
   errata check ★A15).
10. **C10 — Danish cohort use-note.** Appendix D may use Friis
    2023 only as CI-recipient etiology mix; add the abstract's
    23+47≠100 gap note (★A2) and the overlap warning. It is not
    incidence and not a P0 denominator (E1).
11. **C11 — Device-age comparator drift.** §3.4 "9–12 mo"
    caution is now understated: Cochlear 9 mo verified, MED-EL
    7 mo provisional pending FDA re-pull (★B6), AB unverified.
    Step 1 pins era + device mix; holder+co-approver decide
    whether MED-EL 2025 triggers the v2 re-freeze rule. Kral
    2025's "FDA minimum 9–12 mo" line is likewise outdated —
    do not propagate it.

### §8 families / §11 / Appendix E

12. **C12 — Family B/C/D/E wording.** B: Pinyon verifies
    electroporation, not elution/lifetime-reservoir claims;
    2014–2026 silence is an unexplained gap, not a verified
    cause (D3c). C: corrected citations per C8(a); opsin
    immunogenicity/durability/power-heat remain unverified —
    Track-R park logic stands. D: delete or fully specify
    "Liu 2025" and "Qiao 2024" (D4a/D4b, per §11's own rule);
    anchors become Liu 2024 + McGovern 2024×2 with limits.
    E: rewrite "(e.g., cat 6-month success/failure, migration)"
    as a missing-evidence requirement, not an implied dataset
    (D2c); ABI split per C8(b); infant CPA anatomy unverified.
13. **C13 — Family A/G/Q0.** A kill premise per C5. G/Q0:
    label-vs-biology kept separate with USPI §1 locus (O1b,
    ★A6 reconciliation: epi-file's "locus unknown" is
    superseded); post-CI patency % and post-CI AAV delivery
    have no direct evidence in either direction (E4a/E4b) —
    Step 2 must name what evidence could ever decide them
    before scoring Q0. Hearing-preservation 78% (E4c) must not
    be cited as patency or as infant evidence.
14. **C14 — Appendix E bibliography.** Replace shorthand
    anchors with §2's DOI/PMID-level citations at the stated
    evidence level; update "Kral 2023", "Liu 2025", "Qiao 2024",
    "EMBO oCI", "ANI bench + cat" entries per C7/C8/C12.
    §11 Step 0 checklist items map to §2 as: FDA/CHORD → O1–O2
    (done, human re-read owed); Friesen → Ch1; Kral → Ch3;
    Hear Res 2025 → Ch4; Liu/Qiao → D4a/D4b (delete/specify);
    EMBO oCI → D1; ANI → D2 (primaries still missing);
    reprogramming → D4c; Danish → E1; CI age labels → O4
    (AB + MED-EL re-pull owed).
## 4. Prior-art table §2.2 — completed to Step 0 evidence (2026-11-02)

Replaces GOAL §2.2's illustrative table for Step 1 use once
C8 is applied. "Owner (verified)" means the owner/sponsor is
named in an inspected record in §2; GOAL's illustrative names
that Step 0 did not inspect are marked *unverified here* and
must not be cited as verified. **FTO: no patent or
freedom-to-operate search was performed or inspected in Step 0
by any worker or the skeptic.** Every FTO cell therefore reads
"Not assessed" — this is the completed-to-evidence state, not
an omission to fill by inference. Gen 0 still owes an FTO flag
per family (§9, App. B); "Not assessed" must travel with each
candidate until a named patent search exists. Anything with a
verified clinical trial/approval is *evolving standard* per
§2.2 and is compared against, never claimed as novelty.

| Element (§2.2, splits per C8) | Owner / program (verified basis) | Trials / regulatory (inspected records only) | Status for infants (post-skeptic wording) | FTO flag | Step 0 refs |
|---|---|---|---|---|---|
| Optical CI — optogenetic (opsin + LED) | Moser group / Göttingen (author groups on D1a–D1d records; "industry partners" *unverified here* — no partnership record inspected) | No optogenetic-oCI trial record found (bounded search). **Not this row:** NCT05110183 (Northwestern infrared intraoperative feasibility, enrolling by invitation, no results) — non-optogenetic, adult, see next row | Preclinical: gerbil (D1a, D1d-ii), rodent (D1b), rodent+NHP auditory (D1d-i). No human data found (bounded search, 2026-11-02); no infant data. Opsin safety/power/heat unverified | **Not assessed** (no patent search) | D1a–D1d |
| Optical stimulation — infrared, non-optogenetic (new row; separation per D1e) | Northwestern (sponsor per CTgov record description; full sponsor field to be human-confirmed) | NCT05110183: acute intraoperative CAP feasibility during labyrinthectomy-ear surgery; start 2025-04-20, est. completion 2027-12-31, no results posted; N not verified | Adults only (surgical ears slated for labyrinthectomy). Not a hearing-restoration trial; no infant relevance as evidence | **Not assessed** | D1e |
| Penetrating ANI (auditory nerve implant) | ANI concept consortium (Lenarz/Solzbacher/Rieth et al., D2a); Utah-slant-array lineage per secondary summaries only. GOAL names "Utah / Blackrock / MED-EL; NIH BRAIN" — **company/funder ownership unverified here** (no company or grant record inspected) | No ANI interventional trial found (CTgov term query, bounded search). No FDA record inspected | Concept + cat surgical-feasibility model only; bench and chronic-survival primaries missing. No human data found (bounded search). Presumptive park (§8E) stands | **Not assessed** | D2a–D2d |
| ABI (auditory brainstem implant) — **split out of ANI row** | Not verified in Step 0. GOAL named "Utah / Blackrock / MED-EL" jointly for ANI/ABI — no ABI owner, label, or trial record was inspected by any worker | Not assessed in Step 0 (no registry/label record inspected) | Different device class (cochlear-nucleus surface array) with existing clinical use per D-file scope note — **that use was not itself verified here**. Needs its own Step 0/1 verification (indications, pediatric use, outcomes) before any §8E scoring; do not score from ANI rows | **Not assessed** | D §2 scope note |
| Neurotrophin / bionic-ear delivery (Pinyon mechanism: CI-array electroporation BDNF) | UNSW — Pinyon/Housley group (affiliation verified, D3a). "Eluting-array groups" (GOAL) = different delivery mode, *unverified here* (no elution citation inspected) | No Pinyon-mechanism human trial found 2014–2026 (bounded search; CTgov zero-hit query). Non-equivalent neighbors: NCT05040217 (AAV2-BDNF, Alzheimer's); NCT07032038 (progenitor cell therapy + CI, secondary-source only) | Guinea pig only (abstract-level; ectopic branching, short-deafness model). Cause of 2014–2026 silence unexplained — open §8B gap | **Not assessed** | D3a–D3c |
| Hair-cell reprogramming (ATOH1/GFI1/POU4F3 ± SIX1) | Groves lab lineage (McGovern 2024×2; Liu 2024 co-authors Groves/Raphael per D4a) — verified at authorship level; no company/program owner verified | No human trial record inspected or asserted in Step 0 | Neonatal/organoid framing corrected: mature mouse conversion + ectopic mature guinea-pig marker+ cells, **without verified threshold restoration**. §8D large-animal criterion unmet; literature watch only. "Liu 2025"/"Qiao 2024" deleted as citations | **Not assessed** | D4a–D4c |
| *OTOF* AAV — approved | Regeneron Pharmaceuticals (FDA product page manufacturer; USPI holder) — verified | **FDA accelerated approval 2026-04-23**, STN 125874, label per O1b/O1c. Pivotal CHORD NCT05788536 (RECRUITING, est. N=36 target; efficacy per O2). Confirmatory durability pending | Approved subset only (biallelic *OTOF*, preserved OHC, no prior CI same ear; studied 10 mo–16 y). *Evolving standard* for that subset | **Not assessed** (approval ≠ FTO opinion; no patent search) | O1–O2 |
| *OTOF* AAV — Lilly/Akouos AK-OTOF | Eli Lilly and Company (registry sponsor; Akouos subsidiary per registry description) — verified at registry level | NCT05821959: **PHASE3**, RECRUITING, est. N=48 (updated 2026-09-29; skeptic-confirmed). No approval | Trial-stage; efficacy not verified in Step 0. *Evolving standard* candidate — compare, never claim | **Not assessed** | O3a |
| *OTOF* AAV — Sensorion SENS-501 | Sensorion (program name per registry NCT06370351) — registry level | NCT06370351: Phase 1/2, ACTIVE_NOT_RECRUITING, est. N=12, ages 6–31 mo (updated 2026-07-08). Discontinuation = pointer only, unverified | Trial-stage (registry state). Do not assert discontinued or active-recruiting beyond registry wording | **Not assessed** | O3b |
| *OTOF* AAV — others | Otovia Therapeutics OTOV101 (registry) — registry level. Fudan/ChiCTR academic programs: secondary sources only, owners/IDs **unverified** | NCT05901480: UNKNOWN status (stale, updated 2024-05-08), est. N=25. ChiCTR census not done | Unknown/stale. Completeness UNVERIFIABLE; human census owed before §2.2 "others" is closed | **Not assessed** | O3c |
| Hearing-preservation CI (comparator) | Manufacturers verified only via FDA age-label records: Cochlear (Nucleus 24), MED-EL (provisional mirror SSED). Advanced Bionics label, HEARRING, dexamethasone-eluting / ECochG / robotic-insertion programs: **not verified in Step 0** (no trial records inspected) | Age labels: Cochlear ≥9 mo (P970051/S172, 2020); MED-EL ≥7 mo provisional (P000025/S134, 2025, mirror); AB unverified (pointer 12 mo). No dexamethasone/ECochG/robotic trial record inspected — GOAL's "trials" phrasing for those remains uncompleted | **Evolving standard — comparator, not challenger** (unchanged). Pediatric preservation 78% (E4c) is older/better-hearing ears, not P0 infants | **Not assessed** | O4a–O4d, E4c |
| Rapid genomic sequencing / triage pathway | Not verified in Step 0. GOAL names "NSIGHT/Project Baby Bear lineage; hearing-specific panels" — no NSIGHT/Baby Bear record, turnaround study, or panel-yield primary was assigned or inspected. Nearest inspected evidence is diagnostic yield only: Downie exome 56% vs *GJB2/6*-only 21% (E3a-i, abstract-level) | No pathway/trial record inspected | "Clinically available; pathway integration is the gap" remains a GOAL assertion, **not Step-0-verified**. Family G (§8G) needs its own verification (turnaround, VUS/return-of-results, hearing-specific cohorts) before Gen 0 scoring | **Not assessed** | E3a-i (yield only) |

What §4 does not do: it does not complete owners for
Blackrock/MED-EL-ANI, optical-CI industry partners, eluting
arrays, ABI, or rapid sequencing, and it completes no FTO
cell — because Step 0 inspected no such record. Presenting any
of those as verified would invent evidence. They are carried
into §5 as named Step 1 work.

## 5. Unresolved list (everything Step 0 could not verify)

Workers' and skeptic's unresolved items agree; skeptic B8
upheld the UNVERIFIABLE discipline (no snippet number leaked
into a verified cell). Ordered by what blocks Step 1/Gen 0.

**Gate-blocking (human dual extraction / Step 1 cannot pin
without these):**

1. **Human dual extraction on every §2 row** (§9) — pending,
   extractor independent of holder + sampled error audit.
   First targets: USPI label numbers (16/20, 14/20, Week-48
   10/12 — single-source PDF extraction, skeptic A5) by direct
   human PDF re-read incl. §§1/4/14 locators; Downie 2021
   errata contents (A15); Kral 2023 full text beyond pp.377–378
   (B2) and Kral 2025 beyond pp.1–3 (A12); NEJM full text
   beyond abstract (subgroups, per-ear, speech outcomes).
2. **P0 denominator (Appendix D1):** CDC EHDI 2022 HSFS
   Type-and-Severity table (bilateral severe+profound over
   screened births + loss-to-follow-up). Until extracted, all
   P0 head-counts, coverage %, and §1.2 "tens/year" stay blank.
   Morton & Nance full text likewise unextracted (and unusable
   for the ≥70 dB cut regardless).
3. **Etiologic fractions (D2):** *OTOF* fraction (GeneReviews
   NBK1251 Prevalence + P0-like genomic cohort); ancestry-
   stratified *GJB2*; non-Danish *SLC26A4*; P0-at-birth (vs
   progressive) cCMV split. Located-but-uninspected PMC texts:
   PMC7171096 (gene table), PMC5018452 (% new-bone volumes),
   PMC4674315 (AAV sequence/N, see E4b skeptic downgrade).
4. **Additional-disabilities fraction:** Gallaudet Annual
   Survey primary report (or defined infant cohort) with
   definition/instruments/ascertainment age (§3.2).
5. **Q0-deciding evidence does not yet exist in inspected
   form:** post-CI scala-patency % (pediatric, modern-array,
   round-window, by time-since-implant) and post-CI (established
   fibrosis) AAV-transduction efficacy, either direction.
   Step 2 protocol must pre-define thresholds *and* name what
   evidence type could supply them; adult archival histopathology
   (N=17–28) alone cannot.
6. **FDA label re-pulls:** MED-EL SSED P000025/S134 from
   accessdata.fda.gov (mirror provisional, B6); Advanced
   Bionics current FDA labelling/SSED for P960058 (minimum age
   unverified; 12 mo is a pointer).

**Citation/evidence gaps (scoring must read INSUFFICIENT):**

7. **ANI primaries:** bench aging/pulse paper (DOI, N devices,
   failure definition, charge density); any true chronic-
   survival cohort with denominators/migration/histology
   ("Pilot Chronic Evaluation…" full record); infant CPA-access
   anatomy. **ABI:** entirely unverified — own verification owed.
8. **Optical CI full texts:** Dieter/Keppeler N + spread-of-
   excitation numbers; 2026 *EMBO Mol Med* full text/PubMed
   record (Crossref abstract only; "AAV-PHP.S" deleted);
   NCT05110183 enrollment N; chronic opsin immunogenicity/
   durability and power/heat quantification (§8C).
9. **Pinyon/reprogramming full texts:** Pinyon N/arms, eABR
   effect sizes, histology denominators, duration, post-2014
   follow-ups; McGovern×2 + Liu 2024 conversion %, bundle/
   synapse maturity, ABR/DPOAE (incl. nulls), supporting-cell
   depletion, durability; direct PubMed/PMC inspection of
   *PNAS Nexus* pgae445 (B4). Elution-delivery citations
   (Family B) still missing as a separate set.
10. **Channels/development full texts:** Srinivasan 2013 N
    (PMC3639477); Friesen 2001/Sharma 2002 journal texts
    (channel sets per device); focusing clinical-adoption
    label/registry search; primary spread-of-excitation sources
    for the §4.2 ripple-to-channels model.
11. **Absence claims to re-run frozen:** optogenetic-oCI /
    ANI / Pinyon human-trial absences with pre-registered
    multi-registry strings + dates (CTgov + EU CTIS + ChiCTR +
    ANZCTR) per §9 (B3). Sensorion discontinuation primary
    (sponsor release / registry history); complete *OTOF*
    "others" census incl. ChiCTR.
12. **§2.2 completions still owed:** all FTO flags (named patent
    searches, research-use only); optical-CI industry partners;
    ANI company/funder ownership; hearing-preservation
    evolution trials (dexamethasone-eluting, ECochG, robotic);
    rapid-sequencing pathway evidence (NSIGHT/Baby Bear lineage,
    turnaround, hearing-specific triage outcomes) for Family G.

**Explicitly retired (do not resurrect without new primaries):**
"Liu 2025", "Qiao 2024", "Friesen, Shannon & Cruz", "NEJM 2025"
(issue-year sense), "AAV-PHP.S" (2026 oCI detail), "cat 6-month
denominators exist", any ≥70 dB bilateral incidence point
estimate, any *OTOF* %, "AB = 12 mo (FDA-verified)".

*No DOI, PMID, NCT, N, or percentage in this synthesis was
invented: every identifier above appears in a verify-*.md file
or in skeptic.md's independently fetched records (Crossref
10.1038/s44321-026-00541-2; CTgov NCT05821959 re-check), all
dated 2026-11-02. Synthesis model/effort: header table.
Human dual extraction: PENDING — nothing here is gate-deciding.*





