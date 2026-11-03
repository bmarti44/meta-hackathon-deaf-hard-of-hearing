# Gen 6 attack — I-lineage dose extraction: *GJB2* AAV doses / Ns / effects from full texts

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**, disclosed per §9
> rule 3. **Date: 2026-11-03. Gen 6 under GOAL v2.3**
> (no generation cap, no loop stop; PASS bar unchanged).
> Inputs: `gen05/Gen5-summary.md` §4 push 3 (human dual
> extraction + full texts; animal Ns and all doses absent
> from abstracts *by design*); `gen05/candidate-I1-gjb2-aav.md`
> (HP-I1-1); `gen05/candidate-I2-gjb2-dose-design.md`
> (HP-I2-1 desk-kill: a design whose dose cannot be sourced
> is retired, not estimated); `reviews/codex-unstick.md` §2
> (full-text inspection improves what can be assessed; it
> does not create human verification or independence — U1–U5
> stay DESIGN; this file follows the same rule).
> **Inspected records only; no invented data. G3b BLOCKED.
> Same PASS bar. No PASS claimed; scores nothing; fills no
> HOLDER-PIN by itself** (agent pre-extraction; human dual
> extraction PENDING, §9).
>
> **Headline: the dose blank is now half-filled and the
> other half is paywall-proven.** PMID 41402290 (Nat Commun,
> open access) yields a complete mouse dose–response plus
> an NHP delivery dose from inspected full text (§2).
> PMID 40121530 (Mol Ther) yields **abstract-level facts
> only**: every lawful free full-text route tried on
> 2026-11-03 returns metadata/abstract or an explicit
> not-open-access refusal (§3, proof log). Its vg doses,
> animal Ns, volumes and ABR values therefore **stay
> blank** — they are not estimated from the other paper,
> because the constructs differ (§4). The SONIX human
> product dose/capsid/volume remain absent from the
> registry record as re-inspected today (§4). HP-I1-1 /
> HP-I2-1 are **narrowed, not closed**.

## 1. Method (routes actually executed, 2026-11-03)

| route | PMID 41402290 | PMID 40121530 |
|---|---|---|
| NCBI E-utilities `esummary` (PMID→PMC/DOI) | PMC12708874; DOI 10.1038/s41467-025-66110-2 | PMC12266026; DOI 10.1016/j.ymthe.2025.03.029 |
| NCBI `efetch db=pmc` full-text XML | **Full text obtained** (206,617 B XML; ~109.6k chars text) | XML obtained (16,555 B) but **front matter + abstract only** (~7.2k chars; no body, no Methods, no figures) |
| Europe PMC `fullTextXML` | not needed | **HTTP 500** (no full text served) |
| Europe PMC search record (`resultType=core`) | not needed | `isOpenAccess: N`, `inPMC: Y`, DOI link `availability: Subscription required` |
| Europe PMC article HTML / `?pdf=render` | not needed | **HTTP 403 Forbidden** (both) |
| Europe PMC `supplementaryFiles` | not needed | Explicit refusal: *"Article with id PMC12266026 is not open access one"* |
| PMC OA service (`oa.fcgi?id=PMC…`) | not needed | **HTTP 404** (no OA package) |
| PMC XML properties (in the XML itself) | open access | `pmc-prop-open-access: no`; `pmc-prop-has-pdf: yes` (PDF exists behind the paywall) |
| `pypdf` full-text extraction | not needed (XML complete) | **Not executable**: no lawful PDF bytes were obtained to extract; `pypdf` is also not installed in this environment. No PDF was fabricated or sourced from a shadow route. |

Locators below are article section / figure / table
names as printed in the inspected XML, so a human
extractor can re-find every value without trusting this
file. Values in figure *images* (axis readouts) were not
digitized; only values stated in text/captions are filed.

## 2. PMID 41402290 — Ivanchenko et al., *Nat Commun* 2025 (FULL TEXT INSPECTED)

*Cell-specific delivery of GJB2 restores auditory function
in mouse models of DFNB1 deafness and mediates appropriate
expression in NHP cochlea.* DOI 10.1038/s41467-025-66110-2;
PMC12708874. **Allegiance (§5.2, carried from Gen 5):**
Competing Interests section states M.V.I. is a consultant
to and holds equity in Skylark Bio, K.D.K. is an employee
and holds equity in Skylark Bio, D.P.C. holds equity in
Skylark Bio; eight authors are inventors on patent
application US20230340038A1. Skylark Bio is the SONIX
(NCT07627971) sponsor per the Gen 5 inspected record.
Inventor-group single-source ⇒ GRADE starts one level
lower; nothing here is independent replication.

### 2.1 Construct (applies to every dose below)

| field | value as stated | locator |
|---|---|---|
| Capsid | **AAV9-PHP.B for all experiments** ("For all experiments, the capsid was AAV9-PHP.B") | Methods (AAV packaging) |
| Titer method | qPCR specific for the viral ITR; packaging by Boston Children's Hospital Viral Core or PackGene Biotech | Methods (AAV packaging) |
| Regulation | Two ATAC-seq-derived gene regulatory elements (GREs) flanking the *GJB2* coding sequence; CBA-promoter constructs are the non-specific comparators | Results §1; Fig. 1 |
| Transgenes | mouse *GJB2* (mmGJB2) or human *GJB2* (hsGJB2), ± C-terminal HA tag. **HA tag matters**: HA-tagged GJB2 traffics but does not fully function (see §2.2) | Results §§1–3; Fig. 5 |
| Mouse route / age | Round-window membrane (RWM) injection at **P0–P1** (neonatal); **1 µL** viral solution via Nanoliter 2000 injector | Results §1; Methods (mouse injection: "1 µl of the viral vector solution was injected") |
| Mouse models | (i) *Gjb2*^Pfl/Pfl^, Cre+ conditional knockout (profound: ABR ≥120 dB at P30); (ii) *Gjb2 Gjb6*– partial-knockdown model (the "complete restoration" model of the abstract) | Results §§2–3; Abstract |

### 2.2 Mouse doses, Ns, effects (per experiment)

| # | construct / model / age | dose (as stated) | N (as stated) | effect (as stated) | locator |
|---|---|---|---|---|---|
| M1 | AAV-GRE-mmGJB2.HA → cKO (*Gjb2*^Pfl/Pfl^ Cre+), P1 | **5 × 10¹⁰ vg** | N for this ABR cohort not stated in inspected text near the dose (morphology cohorts separately stated; human extractor to confirm from Source Data) | Structure preserved, hair cells present at P30; **ABR only +10–15 dB SPL improvement at P30; no DPOAE improvement** (abstract rounds this to "10–20 dB") | Results §2 ("Viral delivery of GJB2 with GREs rescues…"); Supp. Fig. 2a,b |
| M2 | AAV-GRE-hsGJB2 (**untagged**) → cKO, P1 | **5 × 10¹⁰ vg** | not stated in inspected text near the dose | GJB2 network fully restored at 30 d; **ABR gain ~50 dB SPL; still no DPOAE improvement** (OHC function not rescued in this severe model). Injected Cre− controls: ABR/DPOAE ≈ untreated (no vector toxicity signal at this dose, as stated) | Results §2; Supp. Fig. 2a–d |
| M3 | AAV-GRE-hsGJB2 → partial-knockdown (*Gjb2 Gjb6*–), P1 — **dose–response, the decision-grade experiment** | **High 1.4 × 10¹¹ vg; Medium 7.0 × 10¹⁰ vg; Low 3.0 × 10¹⁰ vg** (per ear; 1 µL per Methods) | At P30: **high n=7, medium n=16, low n=21**. Longitudinal: P60/P90 high n=5, medium n=7, low n=10 (thresholds) / n=9 (wave-1 amplitude); untreated controls n=6 | **P30: complete rescue of click + tone-burst ABR to untreated-control levels at all three doses**; ABR wave-1 amplitude (16 kHz) not different from controls. **P60/P90: rescue persists at high + medium; low dose shows elevated thresholds by P60** (durability is dose-dependent). DPOAE: robust rescue at P30 at all doses; persists P60/P90 at high/medium, somewhat decreased at low | Results §3; Fig. 6c–h + caption |
| M4 | AAV-GRE-hsGJB2 → partial-knockdown, morphology | **7.0 × 10¹⁰ vg/ear** | n=6 (GJB2 restoration); n=7 (hair-bundle SEM) vs n=6 + n=6 controls as captioned | Complete restoration of GJB2 expression to control levels; robust hair-bundle restoration across turns (untreated: base→apex bundle loss) | Fig. 4 caption (b–e) |
| M5 | AAV-GRE-hsGJB2.HA → partial-knockdown (tagged-construct warning) | dose not separately restated for this arm in inspected text | n=3 per captioned group | Strong correctly-localized expression **but** morphological abnormalities (reduced scala-media volume, tectorial-membrane thickening, OHC loss) ⇒ HA-tagged GJB2 "may not function properly" | Results §3; Fig. 5 |
| M6 | AAV-CBA-mmGJB2 (ubiquitous expression, negative control for specificity) | dose not stated in inspected text for this arm | not stated | **Often lethal**: severe shaking, almost all animals died by P5; null-mutant (35delG) CBA vector animals survived to ≥P30 ⇒ lethality attributed to inappropriate gap-junction coupling. This is the paper's own evidence that non-specific *GJB2* expression is dangerous — it is why promoter/GRE specificity is a safety feature, not a refinement | Results §1 |

Reading of M3 for the I-lineage (stated as interpretation,
not as paper text): the mouse minimum *durable* dose in
this construct/model is bracketed between 3.0 × 10¹⁰ vg
(P30 rescue, P60 decay) and 7.0 × 10¹⁰ vg (rescue to
≥P90). No dose below 3.0 × 10¹⁰ vg was tested in the
inspected record, so no ED50/minimum-effective-dose is
filed. All mouse dosing is **neonatal (P1), pre-degenerative**
— prevention timing, T1. Nothing here is a mature/deafened-
animal (T2) rescue, and nothing licenses a human vg number
(species/cochlear-volume scaling is not in the record and
is not invented here).

### 2.3 NHP delivery / safety (cynomolgus, *Macaca fascicularis*)

| field | value as stated | locator |
|---|---|---|
| Animals | **3 juvenile cynomolgus monkeys** total | Results §4; Supp. Table 2 / Fig. 7a (design) |
| AAV-GRE-hsGJB2.HA | **5.0 × 10¹¹ vg in 10 µL, n=3 ears** (2 animals) | Results §4; Methods (NHP) |
| AAV-CBA-eGFP (comparator) | **5.8 × 10¹¹ vg in 20 µL, n=1 ear** (first animal) | Results §4; Methods (NHP) |
| Vehicle | 10 µL formulation buffer, 1 ear | Results §4; Methods (NHP) |
| Route / rate | Transmastoid / facial-recess, trans-RWM; microinjection pump **2 µL/min**, Hamilton syringe, 29 G needle | Methods (NHP administration) |
| Follow-up | ABR before and **5 weeks** after injection, then euthanasia/histology | Results §4; Methods |
| Hearing outcome | Vehicle ear: no significant change. **2 of 3** hsGJB2.HA ears: no significant click/tone ABR change. **1 of 3** (NHP#2 left): thresholds **elevated 15–25 dB nHL at all frequencies** — authors attribute this to possible early post-operative middle-ear change; the attribution is the authors', not independently adjudicated | Results §4 (ABR paragraph) |
| Histology / immune | H&E morphology normal in treated + vehicle (minor basal-turn changes, NHP#2 left, "likely related to surgery"); IBA1 macrophage staining without the infiltration pattern the authors score as vector toxicity; hsGJB2.HA shows "minimal immune response to the vector" (Fig. 9 summary text). Expression in appropriate (GJB2-network) cell types; CBA-eGFP by contrast expressed broadly incl. hair cells (Table 1) | Results §4; Fig. 9; Table 1 |
| **Absent from inspected full text** (searched, zero hits) | **anti-capsid / neutralizing-antibody titres; biodistribution; shedding** — none of the three terms/concepts appears with data. The QR4 G4-AAV legs (re-dose / later-AAV eligibility) get **no input** from this paper | Full-text term search, 2026-11-03 |

NHP reading: N=3 animals / 5 injected-or-vehicle ears is a
delivery-and-targeting feasibility record (T1-adjacent
delivery, non-deafened), exactly as Gen 5 tiered it. The
1-of-3 threshold elevation at the only NHP dose tested is
filed here as a **named safety observation for human
extraction**, not as a rate (no rate is estimable at n=3;
rule-of-three printing remains I2's rule).

## 3. PMID 40121530 — Sun / Tan et al., *Mol Ther* 2025 (ABSTRACT ONLY — PAYWALL PROVEN)

*Combined AAV-mediated specific Gjb2 expression restores
hearing in DFNB1 mouse models.* DOI
10.1016/j.ymthe.2025.03.029; PMC12266026; *Mol Ther*
33(7):3006–3021 (2025-07-02). © The American Society of
Gene and Cell Therapy, Elsevier (as printed in the PMC
record). **Access proof:** §1 table — PMC XML is
abstract-only with `pmc-prop-open-access: no`; Europe PMC
`isOpenAccess: N`, full-text XML HTTP 500, HTML/PDF
HTTP 403, supplementary-files endpoint returns the
literal error *"not open access one"*; PMC OA package
HTTP 404. The full text exists (publisher PDF) but was
**not lawfully obtainable** with the routes available
here. Licensed/institutional access is a human act
(Gen 5 summary §4 push 3: Embase/licensed completion).

### 3.1 What the inspected abstract *does* state (filed verbatim-faithfully)

| field | abstract-stated fact |
|---|---|
| Capsids | Screened serotypes; **co-administration of AAV1 + AAV-ie** effectively targets *Gjb2*-expressing cells |
| Specificity problem + fix | Ectopic *Gjb2* expression in **hair cells causes ototoxicity**; addressed with the specific promoter **SCpro** driving exogenous *Gjb2* in both vectors |
| Mouse efficacy | Co-injection "effectively restored hearing function" in *Gjb2*-deficient mice (no dB, no N, no age-at-injection in abstract) |
| Large animals | Combined system **transduces Bama miniature pig cochleae**; inner-ear AAV in **cynomolgus monkeys did not impair hearing** and showed **"negligible systemic toxicity"** (no N, dose, route detail, or follow-up length in abstract) |

### 3.2 What stays BLANK (not estimated, not borrowed from §2)

Mouse vg/ear per vector and combined total; AAV1:AAV-ie
ratio; injection volume/rate/route/age; mouse model(s)
and per-arm Ns; ABR/DPOAE threshold values and durability
timepoints; ototoxicity dose–response; pig dose/N/route;
monkey dose/N/ears/follow-up/ABR values; anti-capsid,
biodistribution, shedding. **Every one of these cells
remains INSUFFICIENT** until a human with licensed access
inspects the version of record (incl. supplement). The
Gen 5 abstract-level tiering (T1 + large-animal
transduction/safety pointer) is unchanged.

## 4. Consequences for I1 / I2 / P5 (what this attack does and does not move)

1. **HP-I1-1 / HP-I2-1 narrowed, not closed.** There is
   now an inspected dose record for *one* construct
   (AAV9-PHP.B–GRE–GJB2: mouse 3.0 × 10¹⁰–1.4 × 10¹¹ vg in
   1 µL at P1; NHP 5.0 × 10¹¹ vg in 10 µL). I2's units
   (vg/ear, µL, rate, capsid + promoter verbatim) can be
   *illustrated* from §2 — but I2's dose levels must bind
   the **actual clinical product**, and that record is
   still blank (point 3). I2's desk-kill therefore stays
   *available* to humans; this file does not retire or
   clear it.
2. **No cross-construct dose transfer.** Three different
   specificity solutions are now on record — GREs on
   AAV9-PHP.B (§2), SCpro on AAV1+AAV-ie (§3), and
   SKY-GJB2 (undisclosed, point 3). Mouse vg from §2 must
   never be printed as the §3 or SONIX dose. The shared,
   transferable finding is qualitative and safety-shaped:
   **non-specific GJB2 expression is harmful in both
   papers** (CBA lethality by P5, §2 M6; hair-cell ectopic
   ototoxicity, §3) — specificity is load-bearing for any
   G5 assessment of this class.
3. **SONIX human dose still blank.** NCT07627971 as
   re-inspected 2026-11-03 (ClinicalTrials.gov API v2):
   recruiting; arms "Older" (4 subjects, 2–7 y) and
   "Younger" (6 subjects, 9 mo–<2 y); intervention
   "one-time unilateral intracochlear infusion" via the
   SKY-CAT device; est. primary completion 2027-12.
   **No vg dose, capsid, promoter, volume, or infusion
   rate in the record.** Registry existence remains
   barred as a signal (I1/I2/P5 rule, unchanged).
4. **G4-AAV presumptive FAIL untouched.** Neither paper
   reports anti-capsid titres, re-dosing, or later-AAV
   efficacy in inspected records (§2 searched-absent;
   §3 uninspectable). QR4 Stages 0→1 remain the only
   pre-registered retirement route (Gen 5 summary §4.4).
5. **Fitness: nothing moves.** These are the same two
   DESIGN records Gen 5 scored from abstracts, now with
   one full text behind them. Per codex-unstick §2's
   rule, deeper inspection of already-seen DESIGN
   evidence does not create validation, human GRADE, or
   a PASS. I1/I2 stay 1 FAIL / 6 INSUFFICIENT on the
   Gen 5 matrix until humans extract, grade, and score
   under a Gen 6 protocol — this file scores nothing.
6. **Owed to close the attack:** licensed *Mol Ther*
   version-of-record + supplement extraction (§3.2 list);
   Source-Data Ns for M1/M2 (§2.2 flags); SONIX
   protocol/IND-level dose record if it ever becomes a
   public inspected source. Until then the correct
   printed state is: **one construct dosed on paper, one
   construct paywalled, the human product undosed in
   public records.**

*End. Gen 6 I-lineage dose attack. G3b BLOCKED. FROZEN
retained. Human dual extraction PENDING.*
