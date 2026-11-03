# Temporal validation sweep — new external evidence since Gen 0 freeze

> **Model routing (GOAL §9).** Requested: **Sol 6.1, high**
> (generation-execution worker). Actual: **`muse-wonder-full-1.0`**
> at the same effort split (Sol 6.1 unavailable in this runtime);
> substitution disclosed per §9 rule 3. No claim here is Sol 6.1 work.
> **Holder-directed continuation:** 2026-11-02. **Sweep run:**
> 2026-11-03. **GOAL:** v2.2. **Gen clock: Gen 2 = generation 2 of
> max 4** (§7 rule 5). This file is evidence scouting *for* a possible
> Gen 2; it runs no generation, scores no candidate, and advances no
> counter by itself.
> **G3b BLOCKED** (all cells INSUFFICIENT; no Track-P promotion
> possible at v1). **Same PASS bar** (§5.2: ≥Moderate GRADE +
> Appendix A minimum tier + human verification). **No invented
> data:** every item below is an inspected PubMed record (E-utilities
> `esearch`/`esummary`/`efetch`) or ClinicalTrials.gov API v2 record,
> fetched 2026-11-03. Snippets, press releases, and search-engine
> results were not used. Embase / EU CTIS / ChiCTR / ANZCTR were
> **not** searched (D9 bound applies to every absence sentence here).
> **Authority:** agent pre-extraction / triage only. Admission of any
> study to either set is a human manifest amendment
> (`research/gen00/heldout-manifest.md` §5), not this file's act.

## 0. Headline

**Zero studies are admitted to the validation set. The validation
set remains empty (0 entries), exactly as at freeze.** One record
is date-eligible for validation and is irrelevant to every gate
cell (PMID 42972158, §3.6). Everything else new-looking in 2026 was
first published/registered **on or before** the 2026-11-02 freeze
and can therefore enter, at most, as *late-found Design*
(manifest §1 rule 2; protocol §3) by human amendment — or is
already a Design-set study unit. **Q0 remains
UNDECIDABLE-no-data; no gate cell in Gen 0 or Gen 1 changes; no
PASS is created; FROZEN retained.**

Two structural facts must travel with that headline:

1. **The post-freeze window is one day long** (freeze 2026-11-02 →
   sweep 2026-11-03). A near-zero validation yield is therefore
   structural, not a search failure. Temporal validation can only
   accrue with calendar time; this sweep's durable product is the
   re-runnable frozen-string protocol in §1 and the late-found
   Design queue in §4, not a validation harvest.
2. **The substantive catch is pre-freeze 2026 literature the Design
   set never contained** — most importantly a human AAV
   re-administration trial report (PMID 42362868, §3.4). Per the
   manifest these are late-found Design candidates. Calling any of
   them "validation" would be exactly the retroactive re-siding
   manifest §1 rules 2/6/7 forbid, and dressing a Gen 2 around them
   as if they were held-out confirmation would repeat, in evidence
   form, the rewording the external review forbids in design form
   (`reviews/codex-astra-external-review.md` §6: Gen 2 permitted
   only with a genuinely new falsification design; rewording
   existing designs forbidden).

## 1. Frozen strings, databases, dates (reproducibility block)

Strings are the Gen 0 protocol strings verbatim
(`research/gen00/protocol.md`, "Frozen search strings"), run
unfiltered by language, 2026-11-03, two date slices each:
**(a) post-freeze** `pdat 2026/11/03–2026/12/31` plus an
`edat 2026/11/03` entry-date check (catches records entered after
freeze with earlier cover dates), and **(b) 2026-to-freeze**
`pdat 2026/01/01–2026/11/02` (the late-found Design trawl).
**First-publication date = epub date where present**, not issue
date (manifest §3.1 "first published"); issue-dated Nov/Dec 2026
records with Sep/Oct 2026 epub dates are pre-freeze and are
counted as such below.

| # | Topic (task item) | String as run (PubMed) | Hits (b) 2026→freeze | Hits (a) post-freeze |
|---|---|---|---|---|
| 2 | CHORD / AK-OTOF / *OTOF* | `(OTOF[tiab] OR otoferlin[tiab] OR DB-OTO[tiab] OR "AK-OTOF"[tiab] OR lunsotogene[tiab] OR Otarmeni[tiab])` | 54 | 0 (pdat); 0 (edat) |
| 3 | Optical CI | S-C verbatim: `("optical cochlear implant*"[tiab] OR "optogenetic*"[tiab] OR opsin*[tiab] OR channelrhodopsin*[tiab] OR ChReef[tiab]) AND (cochlea*[tiab] OR auditory[tiab] OR "spiral ganglion"[tiab])` | 32 | 0; 0 |
| 4a | Post-CI patency | S-Q0a verbatim (protocol.md) | 129 | 1 by issue date = PMID 42861365, epub 2026-09-25 ⇒ pre-freeze, true post-freeze **0**; edat 0 |
| 4b | AAV after CI | S-Q0b verbatim (protocol.md), sequence classes (i)/(ii)/(iii) applied at screening | 26 | 0; 0 |
| 5 | Signed language / CI | S-H verbatim (protocol.md) | 193 | 0; 0 |
| 6 | Rapid genomic pathway | S-G verbatim (protocol.md) | 135 | 0 (pdat); **1 (edat)** = PMID 42972158, epub 2026-11-03 |

ClinicalTrials.gov API v2 (`/api/v2/studies/{NCT}`, format=json),
inspected in full 2026-11-03: **NCT07752888, NCT05788536 (CHORD),
NCT05821959 (AK-OTOF), NCT06370351 (SENS-501), NCT07778641**.
Registry date queries (`filter.advanced`, run 2026-11-03):
`AREA[StudyFirstPostDate]RANGE[2026-11-03,MAX]` × {OTOF,
optogenetic, sign language cochlear, genomic hearing loss} →
**0 / 0 / 0 / 0**; `AREA[LastUpdatePostDate]RANGE[2026-11-03,MAX]`
× OTOF → **0**; `AREA[ResultsFirstPostDate]RANGE[2026-01-01,MAX]`
× OTOF → **0**; `AREA[StudyFirstPostDate]RANGE[2026-01-01,
2026-11-02]` × OTOF → **2** (NCT07752888, NCT07778641; both §3.1).

Screening: all 569 slice-(b) records title-screened; 20-record
shortlist abstract-inspected via `efetch` (§3). One shortlist
record carries no abstract text in PubMed (PMID 42719247) and is
graded title-only below. Scratch: `/tmp/sweep_out.txt`,
`/tmp/sweep2_out.txt`, `/tmp/ctgov_out.txt`, `/tmp/abstracts_out.txt`.

## 2. Admission rules applied (held-out manifest, condensed)

From `heldout-manifest.md` §§1/3 — a study enters **Validation**
only if *all* hold: first published/registered **after
2026-11-02**; inspected to standard (abstract minimum; full text +
human dual extraction before any PASS use); logged by human
amendment before influencing any score; non-mouse check for
mouse-designed claims; non-inventor lab for replication credit
(same-lab later work = weaker "temporal validation (same-lab)").
By-study siding: registry + label + journal reports of one trial =
**one study unit** (CHORD rule). Records dated ≤2026-11-02 first
inspected now = **late-found Design**, never Validation.
Extraction upgrades stay inside Design. When in doubt, demote to
Design (rule 7). Verdicts below use exactly three labels:
**VALIDATION** (admissible, pending human amendment) /
**DESIGN** (late-found or already-Design; human amendment decides
queue entry) / **NEITHER** (irrelevant, wrong estimand, or below
inspection standard — supports no cell).

## 3. Per-item verdicts

### 3.1 Item 1 — NCT07752888 (post-CI AAV, n=1): results?

**No results. Verdict: DESIGN (already-known pre-freeze study;
results pending). No cell affected now; future results could bear
on Q0-A / G×G4 context only, never as a Q0 decider alone.**

Inspected record (API v2, 2026-11-03): *Safety, Tolerability, and
Efficacy of EA0010 in Patients With OTOF Mutations-Related Hearing
Loss Who Have Received Cochlear Implantation* — Shanghai EmayGene;
**ACTIVE_NOT_RECRUITING**; first posted **2026-08-07**, last update
posted 2026-08-12 (both pre-freeze); actual enrolment **n=1**;
ages 1–17 y, biallelic *OTOF*, click ABR ≥80 dB nHL, prior CI
required; single unilateral intratympanic dual-AAV-*OTOF*
(2.0×10¹¹ vg/ear) via the stapes annular ligament into the
implanted cochlea; primary outcome = AE/SAE/DLT incidence to
week 26; primary completion **estimated 2027-05-31**;
`hasResults: false`, no results section, no results-first-post
date. This matches the round-2 disposition verbatim ("design only
until results post", `research/gaps/round2-summary.md` W5).

Siding note for the human panel (flagged, not decided here): the
trial was registered and read *before* freeze, so under manifest
§1 rules 1–2 the study unit is Design-sided; its eventual results
report will be first-*published* after freeze. The manifest does
not cleanly cover "pre-freeze registration, post-freeze results";
rule 7 (when in doubt, demote to Design) is the conservative
default, and any other siding needs a written human amendment
*before* results are opened. Either way, an n=1 open-label safety
case cannot estimate the Q0-A retention fraction
(`Q0-thresholds.md`: ≥0.80 retention + ≤10 dB) and must never be
entered as a patency or post-CI-AAV efficacy percentage.

The only other 2026-first-posted *OTOF* registration,
**NCT07778641** (first posted 2026-08-21), is a NOT_YET_RECRUITING
observational *OTOF*-variant prevalence study in ANSD with no
intervention and no results. **Verdict: NEITHER** (could at most
inform future G6/Appendix D stratum numerators as Design context
if humans choose; it tests no candidate).

### 3.2 Item 2 — CHORD / AK-OTOF new results 2026

**No new results for either. Verdict: DESIGN study units,
unchanged. No cell affected (in particular G×G2/G4 and Q0-L stay
exactly as scored; D13 prohibition — never credit CHORD/Otarmeni
efficacy to routing — stands).**

- **CHORD NCT05788536** (Regeneron DB-OTO): RECRUITING; last update
  posted **2026-08-05** (pre-freeze); estimated enrolment 36;
  primary completion estimated 2029; `hasResults: false`. No
  post-freeze update exists (LastUpdatePost query = 0). The 2026
  PubMed *OTOF* slice contains no new CHORD results paper — the
  NEJM report (PMID 41085057) remains the journal arm of the same
  Design study unit (manifest §2.2). Remaining 2026 *OTOF* items
  are reviews/editorials/label summaries (e.g. PMID 42868222
  *Ear Hear* review, epub 2026-10-13; PMID 42752727 JAMA
  Otolaryngol Viewpoint on newborn screening, one-sentence
  abstract; PMID 42547733 first-approval summary, already in the
  Gen 0 record): **NEITHER** — framing only, no new N, no new
  endpoint.
- **AK-OTOF NCT05821959** (Lilly/Akouos AAVAnc80-hOTOF): RECRUITING,
  Phase 3 per registry; last update posted **2026-09-29** —
  identical to the date already recorded in manifest §2.2, i.e.
  nothing has changed since freeze; `hasResults: false`;
  exclusion still bars CI in the ear(s) to be treated. Parts B–D
  (incl. Part D sequential contralateral dosing) are pre-freeze
  design features, not results.
- **SENS-501** (same program family, checked for completeness):
  trial NCT06370351 ACTIVE_NOT_RECRUITING, last update 2026-07-08,
  no results. One genuinely new 2026 paper exists — **PMID
  42318138** (Boudra et al., *Mol Ther Adv*, DOI
  10.1016/j.omta.2026.201762; epub 2026-05-19; erratum PMID
  42565089) — but its abstract reports **preclinical data only**:
  dual-AAV8-*OTOF* in *Otof*⁻/⁻ mice (IHC expression, auditory
  restoration from 3 weeks, sustained to 10 months; abstract gives
  no N/arm) plus GLP toxicology in non-human primates with the
  clinical injection device. Sponsor-authored (Sensorion =
  inventor; allegiance downgrade applies). **Verdict: DESIGN**
  (late-found; same program as Design record O3b). Cells it could
  ever touch, after human full-text extraction only: background
  T1/T2 context for beyond-label *OTOF* programs — it is not human
  efficacy, not a pathway comparison, and moves no G/D cell.
- **PMID 42444129** (Tao et al., *Mol Ther*, DOI
  10.1016/j.ymthe.2026.07.021; epub 2026-07-13): AAV-WM04 capsid,
  directed evolution in adult mouse cochlea, near-complete IHC
  transduction, selective IHC transduction in NHP, dual-AAV *OTOF*
  restoration in humanized *Otof* mouse (no Ns in abstract).
  **Verdict: DESIGN** (late-found T1/T2 vector context). Cells:
  none now; at most future D-family background. Mouse-designed ⇒
  any future claim from it needs the manifest non-mouse check; the
  abstract's NHP sentence is transduction, not threshold
  restoration, and is not the §8D large-animal advance criterion.

### 3.3 Item 3 — Optical CI new in-vivo

**No new independent in-vivo evidence; no adult first-in-human.
Verdict: one already-DESIGN study now fully indexed, two
late-found DESIGN candidates, all inventor-lab (Göttingen/Moser
group). C cells unchanged (Track R watch; G6 FAIL for infants
stands). The §8C kill/park clock is untouched by anything here.**

- **PMID 42918880** (Albrecht et al., *EMBO Mol Med*, 2026-10-22) —
  DOI **10.1038/s44321-026-00541-2 is identical to Design-set entry
  D1d-ii** (manifest §2.3, "Published 2026-10-22… no PMID at
  2026-11-02"). It is therefore the *same Design study*, now
  PMID-indexed with an inspectable abstract: ChReef in gerbil SGNs
  + oCI of **5–10 green LEDs**; inferior-colliculus thresholds
  <200 nJ; tonotopically ordered, spectrally distinct activity vs
  electrical; LDA channel discriminability favouring optical; some
  LEDs elicited multiple spectral peaks at higher intensities.
  **Verdict: DESIGN (extraction upgrade within Design, manifest
  §1 rule 5 — explicitly not validation).** Cell relevance:
  C×G1-spectral mechanism context only. It does not supply ≥16
  independently discriminable channels (5–10 emitters ≠ effective
  channels — the external review §3 makes the same point of the
  16-emitter precedent), is acute, single-species (gerbil),
  inventor-lab, and unreplicated; under §5.2 it cannot PASS C×G1
  and under the manifest's pre-registered need (non-inventor
  replication; chronic data; adult human feasibility) it checks
  none of the validation boxes.
- **PMID 41366521** (Roos et al., *EMBO Mol Med*, DOI
  10.1038/s44321-025-00350-z; epub **2025-12-09**, 2026 issue):
  f-ChR2 TC channelrhodopsin; AAV expression in mouse SGNs
  (responses beyond 300 Hz) and gerbil multichannel blue-LED oCI
  (single-LED rates ≥100 Hz). Göttingen inventor group.
  **Verdict: DESIGN** (late-found; first-published 2025, so doubly
  ineligible as validation). Cell: C×G1-temporal mechanism context
  only.
- **PMID 42648323** (Khurana et al., *J Neural Eng*, 2026-09-24):
  FraSCO **in-silico** (T0) human-cochlea oCI model, 64 modelled
  channels, 1,000 modelled SGNs; claims are model outputs
  ("predicted to be less impacted by noisy backgrounds").
  Göttingen. **Verdict: DESIGN** (late-found T0). Cell: none —
  T0 never passes G1/G2 (§5.3); useful only as a benchmarking
  design input. The remaining 29 S-C hits are non-cochlear
  optogenetics (cortex/amygdala/birdsong etc.): **NEITHER**.

### 3.4 Item 4 — Post-CI patency / AAV-after-CI new studies

**No Q0-P patency estimand and no Q0-A sequence-(ii) study exists
in the inspected 2026 record. Q0 stays UNDECIDABLE-no-data. One
adjacent human study (AAV re-administration, contralateral ear) is
the sweep's most decision-relevant late-found DESIGN candidate —
and it is not a post-CI study.**

S-Q0b (26 hits, all title-screened; relevant abstracts inspected):
**zero** sequence-(ii) records (AAV delivered *after* an
established implant/fibrosis). The slice is reviews (PMIDs
42868211, 42868209, 42614064…), in-vitro *GJB2* prime editing
(42562992), and PMID 42861365 (mRNA-LNP biodistribution in
**neonatal mouse, no implant**, epub 2026-09-25) — all
**NEITHER** for Q0-A. S-Q0a (129 hits): **zero** prospective
scala-patency n/N by time-since-implant under a pre-stated access
definition. Closest records, none of which may be entered as a
patency percentage (round-2 W6a warning applies verbatim):

- **PMID 42362868** (Fan et al., *Nat Med*, DOI
  10.1038/s41591-026-04505-4; epub 2026-06-26) — *Re-administration
  of AAV-mediated gene therapy for OTOF-related deafness.* Fudan
  group; ChiCTR2200063181 (registry itself **not inspected** —
  ChiCTR gap, D9). Mouse arm: AAV1-h*OTOF* re-administration to the
  **contralateral** ear at peak serum NAb titres rescued hearing.
  Human arm: **n=4**, ages 2.2–3.4 y, pre-existing NAbs
  1:135–1:3,645, second dose in the **contralateral (previously
  untreated, unimplanted)** ear; no dose-limiting toxicity at
  6 weeks; 26-week average ABR thresholds in second ears improved
  from >95 dB to 43 / 63 / 80 / 53 dB; AEs grade 1–2 except one
  grade-3 neutrophil decrease; no SAEs; follow-up 26–52 weeks.
  **Verdict: DESIGN (late-found; human amendment + full-text dual
  extraction required before any use). Explicitly NOT validation**
  (epub 2026-06-26 ≤ freeze) **and NOT a Q0 decider**: the treated
  cochleae were implant-naïve, so the Q0-A estimand (AAV efficacy
  *in an established-implant, fibrosed cochlea*) is untouched, and
  same-ear re-dosing was not tested. Cells it could affect *in a
  future human-frozen re-score only*: the **G4-AAV sub-gate
  narrative** (GOAL §4.2: AAV challengers are presumptive G4 FAILs
  "until capsid-switch / non-viral re-dosing **or post-exposure
  later-AAV efficacy** is shown" — this is the first abstract-level
  human evidence in that third category, hence relevant to
  D×G4-AAV and to the AAV-re-dosing watch gap that round 2 left at
  0/2 attacks) and, secondarily, G×G4 sequencing context
  (contralateral-ear strategies). Why it still moves no cell now:
  single-arm, n=4, inventor/trial group (allegiance downgrade), no
  non-inventor replication, ABR-threshold surrogate without the
  Appendix A G2/G3 chain, agent abstract-level pre-extraction
  only. Best honest label today: *provisional signal — awaiting
  human extraction*, which under the Step 3 bar scores
  INSUFFICIENT.
- **PMID 42843343** (Chen et al., *Cell Rep Med*, epub 2026-10-07)
  — *OTOF* VUS-reclassification pipeline (same Fudan trial,
  ChiCTR2200063181): VUS in ~half of 135 biallelic-*OTOF* patients;
  functional pipeline reclassified 8 VUS, yielding definite
  diagnoses for 38 patients; 7 treated with auditory improvement
  (one near-normal, sustained 1.5 y). **Verdict: DESIGN**
  (late-found). Cells: could inform a future G/Ga **G6
  eligibility-numerator** discussion (VUS as a decision-time state
  is already a §3.2 stratum) — but it reports no decision-time
  turnaround comparison vs frozen workup, so it is not pathway
  evidence (protocol S-G note; D6) and moves no cell now. Filed
  here rather than §3.6 because it travelled with the AAV slice;
  it belongs to item 6 taxonomically.
- **PMID 41521754** (Liu et al., *Acta Otolaryngol*, epub
  2026-01-12): retrospective **77 reimplantations**; residual
  packing material associated with more fibrous adhesion,
  granulation, cochlear ossification, and cochleostomy
  re-expansion at revision. **Verdict: DESIGN** (late-found).
  Cells: Q0-P *context* and G4/G5 surgical-technique background
  only. Revision difficulty in a selected reimplantation series
  is not a scala-patency numerator/denominator.
- **PMID 41977423** (Braack et al., *Int J Mol Sci*, 2026-04-02):
  pirfenidone hydrogel at round window reduced CI-induced
  intracochlear tissue reaction ~40% vs vehicle at 2 months in
  **guinea pigs** (micro-CT; p=0.0297; dexamethasone comparator
  ~36%; **no per-arm N in abstract**). **Verdict: DESIGN**
  (late-found T2, non-Nadol lab). Cells: A/G4 fibrosis-mechanism
  background in a future extraction; an anti-fibrotic adjunct is
  also evolving-standard territory (dexamethasone comparator),
  not challenger novelty (§3.4).
- **PMID 42049515** (Wu et al., *J Neurosci*, 2026-06-03):
  hearing-preservation CI in **mice** (all male) induced apical
  primary neural degeneration — synapse loss exceeding IHC loss
  7.1-fold by 16 weeks despite preserved thresholds.
  **Verdict: DESIGN** (late-found T1/T2). Cells: G4
  (SGN/synapse-survival component) mechanism background for the
  frozen comparator itself; mouse-only ⇒ headlined as such, needs
  non-mouse corroboration before any tier argument.
- **PMID 42719247** (Kim et al., *MedComm*, epub 2026-09-09):
  *"Preservation of DPOAE After Cochlear Implantation in Children
  With OTOF-Related Deafness"* — the PubMed record inspected
  2026-11-03 contains **no abstract text** (title/affiliation
  only). **Verdict: NEITHER until inspected to standard**
  (manifest §3.2 abstract minimum; §2.9 located-not-inspected).
  Queued for human full-text pull because the title, if borne
  out, would bear on OHC-preservation context for Q0/G4 — no
  number from it is asserted anywhere in this file.

### 3.5 Item 5 — Signed-language / CI outcome new cohorts

**No new cohort tests the H estimand (early signed/visual exposure
→ G3a within-stratum language effect and/or post-CI auditory
outcomes, vs frozen EI mix). H/H1 cells unchanged; H's post-CI
harm question remains not-cleared (Step 4 §1).** Of 193 S-H hits,
only five title-match CI/bimodal/outcome territory; the rest are
sign-linguistics, education, health-access, and technology papers
(**NEITHER**). Abstract-inspected:

- **PMID 42765866** (Wen et al., *Am J Audiol*, 2026-09-21; DOI
  10.1044/2026_AJA-25-00313): Epic Cosmos 2015–2024; 39,111 CI
  recipients, 1,070 (2.7%) ASL-preferring; ASL users more
  socioeconomically vulnerable (SES/SVI ORs ~1.7) with higher
  explantation odds (multivariate OR 2.55). Cross-sectional,
  database-coded language preference, **no language or auditory
  outcome**, no exposure-timing or dose, confounding by
  indication/SES unresolvable from the abstract. **Verdict:
  DESIGN** (late-found) as **G6/equity context** for H/P1 (who
  ASL-using CI recipients are; explant burden belongs in G5/G6
  denominators) — it must not be read as an H harm signal
  (explantation ≠ the Appendix A post-CI auditory-harm estimand)
  nor as any G3a/G3b evidence.
- **PMID 42678229** (Coppola et al., *Child Dev*, 2026-09-01):
  120 DHH + 58 hearing children, 3.1–7.6 y; earlier language
  access (either modality) predicted number-concept accuracy;
  modality itself did not. **Verdict: NEITHER** for gate purposes
  (developmental-psychology outcome is not a G3a modality-normed
  language score; no CI-stratified intervention comparison).
  Directionally consistent with H's framing hypothesis; framing
  is not evidence (§5.3).
- **PMID 41782207** (Cheng et al., *J Child Lang*, 2026-03-05):
  deaf **adults** (12 native + 12 early-ASL + 16 early
  signing-system signers); early signing-system exposure
  associated with weaker ASL word-order representation.
  **Verdict: NEITHER** (adult retrospective exposure, no CI
  cohort, no pediatric language endpoint). Remaining CI-adjacent
  titles (PMIDs 41591887 values brief; 41835090 hearing children
  of deaf mothers; 41589221 single case study): **NEITHER**.

### 3.6 Item 6 — Rapid genomic pathway outcome studies

**No 2026 study reports a rapid-genomic *pathway* outcome
(decision-time turnaround → time-to-access / language / preserved
options vs frozen workup). G/Ga cells unchanged.** S-G's 135 hits
are overwhelmingly gene-discovery case reports and yield cohorts;
diagnostic yield alone is not pathway evidence (protocol S-G
note; external review §3 on G×G6/Downie; D6).

- **PMID 42972158** (Behroozi et al., *J Mol Neurosci*, DOI
  10.1007/s12031-026-02619-5; **epub 2026-11-03**): single Iranian
  case of *KARS1*-related leukoencephalopathy-with-deafness
  diagnosed by WES + 41-case literature review. This is the
  sweep's **only date-eligible validation candidate** (first
  published after freeze; independent lab; human). **Verdict:
  NEITHER** — date eligibility is necessary, not sufficient: it
  checks no pre-registered hypothesis or cell (manifest §3.3),
  sits outside P0's primary analysis (syndromic progressive
  leukoencephalopathy case report, n=1), and reports no pathway,
  turnaround, or outcome comparison. It is recorded here so the
  "validation = 0" headline is auditable, and should **not** be
  logged as a validation entry.
- **PMID 42073420** (Taiber et al., *Life*, 2026-04-07): pooled
  sequencing diagnostic yield ~47% bilateral vs ~5% unilateral
  childhood HL (meta-analysis; searched PubMed/Google
  Scholar/Cochrane per abstract). **Verdict: DESIGN**
  (late-found) as Appendix D / G6 *yield-input* context only —
  the same non-pathway limitation as Downie; moves no cell.
- **PMID 42453194** (She et al., *Front Genet*, epub 2026-06-30):
  Qingyuan, China; 22,819 newborns 2017–2023, concurrent hearing +
  9/23-variant genetic screening, follow-up to 2.5 y (25 confirmed
  HL, 0.11%; 994 carriers). **Verdict: DESIGN** (late-found) as
  screening-programme context. Not a rapid-turnaround or
  decision-time triage comparison; variant-panel screening of all
  newborns is a different intervention from candidate G's
  post-refer genomic triage; no language/access endpoint.
- **PMID 42843343** (VUS pipeline) is cross-filed at §3.4:
  DESIGN, G6-eligibility context, not pathway evidence.
- No NSIGHT/Project Baby Bear-lineage rapid-genome hearing-pathway
  paper appears in the inspected 2026 S-G slice, and no new
  genomic-pathway trial was first-posted after freeze (CTgov query
  = 0). Absence bound: PubMed + ClinicalTrials.gov only,
  2026-11-03 (D9).

## 4. Consolidated admission table

| Study unit | First pub/reg | Verdict | Cell(s) it could ever affect (future human-frozen re-score only) |
|---|---|---|---|
| PMID 42972158 *KARS1* case | 2026-11-03 | **NEITHER** (date-eligible, hypothesis-irrelevant) | none |
| NCT07752888 EA0010 post-CI *OTOF* | reg. 2026-08-07 | **DESIGN** (known; no results; completion est. 2027-07) | Q0-A context; G×G4 — never a decider at n=1 |
| NCT07778641 ANSD *OTOF* prevalence | reg. 2026-08-21 | **NEITHER** | (App. D context at most) |
| NCT05788536 CHORD / NCT05821959 AK-OTOF / NCT06370351 SENS-501 | pre-freeze; no results; no post-freeze update | **DESIGN** (existing units, unchanged) | none now |
| PMID 42318138 SENS-501 preclinical | epub 2026-05-19 | **DESIGN** (late-found, inventor T1/T2+NHP tox) | program background only |
| PMID 42444129 AAV-WM04 | epub 2026-07-13 | **DESIGN** (late-found mouse/NHP-transduction) | D background only |
| PMID 42918880 multichannel oCI | 2026-10-22 | **DESIGN** (= D1d-ii; extraction upgrade) | C×G1 mechanism context |
| PMID 41366521 f-ChR2 TC | epub 2025-12-09 | **DESIGN** (late-found, inventor mouse/gerbil) | C×G1-temporal context |
| PMID 42648323 FraSCO | 2026-09-24 | **DESIGN** (late-found T0) | none (design input) |
| PMID 42362868 AAV re-administration | epub 2026-06-26 | **DESIGN** (late-found; n=4 human, contralateral) | **G4-AAV sub-gate** (D; G context) — provisional signal at best |
| PMID 42843343 *OTOF* VUS pipeline | epub 2026-10-07 | **DESIGN** (late-found) | G/Ga×G6 eligibility context |
| PMID 41521754 reimplantation packing | epub 2026-01-12 | **DESIGN** (late-found, n=77 revision series) | Q0-P context; G4/G5 technique |
| PMID 41977423 pirfenidone anti-fibrotic | 2026-04-02 | **DESIGN** (late-found guinea-pig T2, N not in abstract) | A×G4 mechanism background |
| PMID 42049515 post-CI neural degeneration | 2026-06-03 | **DESIGN** (late-found mouse) | G4 SGN/synapse background (frozen itself) |
| PMID 42719247 DPOAE post-CI *OTOF* | epub 2026-09-09 | **NEITHER** (no abstract in record; full text owed) | (Q0/G4 context if ever inspected) |
| PMID 42765866 ASL-using CI recipients | 2026-09-21 | **DESIGN** (late-found cross-sectional DB) | H/P1×G6 equity context |
| PMIDs 42678229, 41782207 | 2026 | **NEITHER** (wrong outcome/population) | none |
| PMID 42073420 yield meta-analysis | 2026-04-07 | **DESIGN** (late-found yield input) | App. D / G6 input context |
| PMID 42453194 Qingyuan newborn screening | epub 2026-06-30 | **DESIGN** (late-found programme cohort) | App. D context |
| **Validation admissions from this sweep** | — | **0** | — |

## 5. What this means for Gen 2 (and what it must not be used for)

1. **Temporal validation is still an empty set looking for
   calendar time.** No hypothesis designed on the Gen 0 Design set
   has yet acquired a later/independent check. The manifest's
   pre-registered validation needs (its §3 table) remain the
   shopping list, now with two dated watch items: NCT07752888
   results (earliest plausible after estimated primary completion
   2027-05-31 — an estimate in the record, not a promise) and any
   post-2026-11-02 results publications from CHORD/AK-OTOF/
   SENS-501, each requiring a human siding amendment *before*
   opening (§3.1 note). Re-running §1's strings on a stated
   cadence (e.g. quarterly) is cheap and is the only honest way
   this set fills; each re-run is a new dated sweep file, never
   an edit of this one.
2. **The one new-evidence hook that could legitimately shape a
   Gen 2 falsification design is PMID 42362868** — because it
   attacks a named presumptive-FAIL rule (G4-AAV) rather than a
   score. A genuinely new Gen 2 question it enables (stated here
   as a *design input*, not a candidate): pre-register what
   contralateral re-administration success does and does not
   imply for sequencing — e.g. a falsification design separating
   (a) NAb-barrier claims (now with human data against the strong
   form), from (b) established-implant delivery claims (still
   zero data), from (c) same-ear re-dose claims (untested) — with
   kill criteria that retire whichever sequencing rationale
   depends on the falsified leg. That is new because Gen 0/Gen 1
   treated G4-AAV as an untested presumption; it would cease to
   be new the moment it merely re-scores Ga/P1 with 42362868
   pasted in as "validation." Per the external review §6, the
   former is permitted Gen 2 work; the latter is forbidden
   rewording. Note the asymmetry the design must respect:
   42362868 weakens "AAV once ⇒ never again anywhere" but says
   nothing in favour of "AAV works after CI" — a Gen 2 that
   claimed Q0 movement from it would be manufacturing the very
   estimand substitution this project has repeatedly retired.
3. **Nothing here spends or saves the generation clocks by
   itself.** Gen 2 (= generation 2 of max 4) remains unrun; the
   §7(b) no-improvement counter still stands at 1/2 from Gen 1,
   and a design-only Gen 2 would spend 2/2 for nothing (Step 4 §2
   warning, unchanged by this sweep). G3b co-design remains the
   binding structural bar and the external review's
   highest-leverage action; no item in §3 touches it.
4. **Prohibitions carried forward:** do not quote any §3 item as
   "validation," "held-out confirmation," or a PASS input; do not
   convert 41521754 revision findings, 42362868 contralateral
   results, or 42719247's title into patency/Q0 numbers; do not
   credit *OTOF* therapy efficacy to pathway G/Ga (D13); do not
   treat yield (42073420, 42453194, 42843343) as pathway effect
   (D6); 5–10 (or 16) emitters are not effective channels.

## 6. Unresolved / owed after this sweep

- Human manifest-amendment decisions for every DESIGN verdict in
  §4 (admit as late-found Design with full-text dual extraction,
  or leave in neither-set); this file admits nothing by itself.
- Full texts owed before any use: PMIDs 42362868, 42843343,
  42918880 (figure-level channel counts), 42719247 (no abstract
  exists in the PubMed record), 41521754, 42765866.
- ChiCTR2200063181 registry record uninspected (the Fudan
  re-administration/VUS trial unit); EU CTIS/ANZCTR/Embase
  remainders from round 2 W5 still open — every absence claim
  above is bounded to PubMed + ClinicalTrials.gov, 2026-11-03.
- Siding rule for pre-freeze-registered trials reporting results
  post-freeze (NCT07752888 first; CHORD/AK-OTOF behind it):
  needs a prospective human amendment before the first such
  results report is opened.
- Re-sweep cadence and owner (holder decision); until set, the
  validation set's emptiness as of 2026-11-03 is the last
  verified state.

*End. Inputs: GOAL v2.2 §7; `research/gen01/Step4-gen1-summary.md`;
`reviews/codex-astra-external-review.md` (esp. §6);
`research/gaps/round2-summary.md`; `research/gen00/heldout-manifest.md`
§§1–3; `research/gen00/protocol.md` frozen strings. All external
records above were fetched and read 2026-11-03 via NCBI
E-utilities and the ClinicalTrials.gov API v2; counts, dates, and
quotations are transcribed from those responses (`/tmp/sweep_out.txt`,
`/tmp/sweep2_out.txt`, `/tmp/ctgov_out.txt`, `/tmp/abstracts_out.txt`).*
