# Gen 7 re-sweep 2 — watched-trial results check since Gen 6 re-sweep (2026-11-03)

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**, disclosed per §9
> rule 3. **Date: 2026-11-03. Gen 7 under GOAL v2.3**
> (no generation cap, no loop stop; gates/PASS bar
> unchanged). Scope (deliberately narrow): *has any
> watched trial from `gen06/resweep.md` /
> `Gen6-summary.md` §4.5 posted results, or changed
> status in a way a Gen 7 design must not ignore?*
> Method: **ClinicalTrials.gov API v2 full records
> re-fetched 2026-11-03** (`/api/v2/studies/<NCT>`);
> `hasResults`, overall status, last-update-posted,
> enrolment, and estimated primary completion compared
> field-by-field with the Gen 6 re-sweep as inspected
> the same date. No new literature sweep is claimed:
> PubMed use this session was targeted cohort/dataset
> inspection for [candidate-P7-pilot-audit.md](./candidate-P7-pilot-audit.md)
> §3 (E-utilities, PMIDs named there), not a Gen 7
> broaden-sweep. Embase/EU CTIS/ChiCTR/ANZCTR remain
> **unsearched**; every absence claim is bounded to
> ClinicalTrials.gov registry-posted results on this
> date. **Inspected records only; no invented data.
> G3b BLOCKED. Nothing here earns a PASS, scores a
> cell, or enters the validation set (still 0).**
>
> **Headline: no watched trial has posted results.
> Every record below still reads `hasResults: false`.
> No R-P6-10 auto-freeze trigger has fired, no anchor
> kill can evaluate, and no Gen 0–6 cell moves.**

## 1. Watched set and comparison basis

The watched set is exactly Gen6-summary §4.5 +
gen06/resweep §8's ledger: NCT07627971 (SONIX,
I1/I2 anchor + P6/P7 eligibility source of record),
NCT05788536 (CHORD/DB-OTO), NCT07752888 (post-CI
EA0010, Q0 pointer), NCT07032038 (Rincell-1 cell
therapy, Family-L revisit trigger), NCT05821959
(AAVAnc80-hOTOF Phase 3), NCT06370351 (SENS-501),
NCT05110183 (opto-electrical CI). Registry existence/
status is never a signal (D-rule, verbatim); status
and dates below are monitoring facts only. External-
program results, when they exist, are never this
project's candidate effects (D13, verbatim).

## 2. Results (API v2, inspected 2026-11-03)

| NCT | Program | `hasResults` | Status (Gen 6 → now) | Enrolment as inspected | Est. primary completion | Last update posted | Moved vs Gen 6 re-sweep? |
|---|---|---|---|---|---|---|---|
| NCT07627971 | SONIX / SKY-GJB2 (Skylark) | **false** | RECRUITING → RECRUITING | 10 (est.) | 2027-12 (est.) | 2026-08-27 | **No** — identical on every compared field. I1/I2 anchor kill still cannot evaluate before ~2027-12; dose/capsid/volume still absent from the record (HP-I1-1 stands); P7's A-primary (2026-11-03 dated source) is therefore the Gen 6 inspection, unchanged |
| NCT05788536 | CHORD / DB-OTO (Regeneron) | **false** | RECRUITING → RECRUITING | 36 (est.) | 2029-02-26 (est.) | 2026-08-05 | **No** — journal T4 result (PMID 41085057, Gen 6 §3.1, DESIGN/D13) still precedes any registry results posting; that asymmetry is noted, not reconciled |
| NCT07752888 | EA0010 post-CI *OTOF* | **false** | ACTIVE_NOT_RECRUITING → ACTIVE_NOT_RECRUITING | **1 (actual)** | 2027-05-31 (est.) | 2026-08-12 | **No** — still N=1 actual, no results. **Q0 remains UNDECIDABLE-no-data**; no post-CI preservation claim becomes available to any candidate |
| NCT07032038 | Rincell-1 otic progenitors (Rinri; adult FIH, CI adjunct — brief title and interventions re-inspected this fetch) | **false** | NOT_YET_RECRUITING → NOT_YET_RECRUITING | 20 (est.) | 2029-05 (est.) | **2026-10-01** (newest administrative update in the set; content of the update not diffed field-by-field beyond the fields above) | **No material move** — still zero-dosed *as a registry fact* (not yet recruiting), so the Family-L revisit trigger (first human safety readout, Gen 5 §353) is **unmet**; the update date alone is not a signal (D-rule) |
| NCT05821959 | AAVAnc80-hOTOF Phase 3 | **false** | RECRUITING → RECRUITING | 48 (est.) | 2028-10 (est.) | 2026-09-29 | **No** — recruiting, no results |
| NCT06370351 | SENS-501 (6–31 mo; prior/current CI excluded, Gen 6 §3.3) | **false** | ACTIVE_NOT_RECRUITING → ACTIVE_NOT_RECRUITING | 12 (est.) — enrolment figure as returned this fetch; Gen 6 re-sweep did not print its N, so no change is asserted | 2027-07 (est.) | 2026-07-08 | **No** — no results |
| NCT05110183 | Opto-electrical CI (adult translabyrinthine; children excluded, Gen 6 §5) | **false** | ENROLLING_BY_INVITATION → ENROLLING_BY_INVITATION | 30 (est.) | 2027-12-01 (est.) | 2026-05-06 | **No** — no results; no human oCI hearing result exists in this bounded check |

**Disposition of the whole table:** no R-P6-10
trigger (no suspension/termination/withdrawal, no
results posting) — P6's branch neither auto-freezes
nor gains anything; P7's A-primary assumption set
(HP-P7-3) is dated to a still-current record. No I1
anchor kill, QR4 leg, Q0 reading, or Family-L
trigger evaluates. All Gen 6 kills remain
**unevaluated** (D10).

## 3. What this check did not do (bounds, printed)

- **Not a literature re-sweep.** Journal results can
  precede registry postings (NCT05788536 is the
  standing example). A new journal result for a
  watched program published without a registry
  posting would **not** be caught here. The quarterly
  dated re-sweep obligation (Gen5-summary §4.5,
  Gen6-summary §4.5) in its full PubMed + registry
  form is **not discharged** by this file; this file
  discharges only the "results posted?" question.
  PubMed queries run this session (for P7 §3: Downie
  PMID 31827275, Subbiah PMID 31745502, CDaCI PMID
  37382935, LOCHI PMIDs 29020839/34249584, OtoSCOPE-
  centre PMID 41623227, delay chart reviews PMIDs
  24035734/27658178, *GJB2*-heterozygote PMID
  41367487, Shenzhen screening PMID 41477923 — all at
  abstract level, E-utilities) returned no watched-
  trial result record, but they were cohort/dataset
  queries, **not** a bounded efficacy sweep, and no
  absence claim beyond that is made.
- **Registries beyond ClinicalTrials.gov unsearched**
  (EU CTIS, ChiCTR, ANZCTR, Embase) — the standing
  bound on every absence claim in Gen 5–7 is unchanged.
- **Record internals not re-extracted.** Eligibility
  text, arms, and outcomes were not re-diffed word by
  word against Gen 6 §2/§5; a silent eligibility
  amendment inside an unchanged status would be
  caught only by the HP-P5-3 quarterly full re-check,
  which remains the governing mechanism. If holders
  act on any eligibility element, Gen 6 resweep §2's
  dated inspection must be refreshed first.

## 4. Standing state (verbatim)

G3b BLOCKED. FROZEN retained. Validation set 0. No
PASS, no winner. H harm not cleared. Q0
UNDECIDABLE-no-data. A1 UNEVALUABLE. G4-AAV stands
for C/D/I1/I2/K1. D1–D17 carry. Next full dated
re-sweep owed on the Gen 6 bounded terms (PubMed +
ClinicalTrials.gov), with Embase/EU CTIS/ChiCTR/
ANZCTR completion still owed before any absence
claim leaves bounded wording. SONIX (est. 2027-12)
remains the record's first real validation candidate
— candidate, unrealized.

*End. Gen 7 re-sweep 2 under GOAL v2.3. Inspected
registry records only; scores nothing.*
