# Gen 7 held-out monitoring — quarterly watch protocol for NCT07627971, NCT07032038, NCT07752888

> **Model routing (GOAL §9).** Requested: **Sol 6.1**.
> Actual: **`muse-wonder-full-1.0`**, disclosed per §9
> rule 3. **Date: 2026-11-03. Gen 7 under GOAL v2.3**
> (no generation cap, no loop stop; PASS bar unchanged).
> Inputs: `gen06/Gen6-summary.md` §4 item 5 (held-out
> monitoring, quarterly dated re-sweeps — the push this
> file executes); `gen06/resweep.md` §§1–2, 4, 8
> (admissions rules, SONIX and EA0010 records as
> inspected); `gen06/candidate-P6.md` R-P6-5/R-P6-10
> (HP-P5-3 quarterly source-of-record discipline, auto-
> freeze); `gen05/broaden-sweep.md` §§2.4, 3 (Rincell-1
> record and revisit trigger); `gen05/Gen5-summary.md`
> §4.5 (same queue item, Gen 5 form). **Inspected
> records only; no invented data.** Registry facts below
> were re-fetched from ClinicalTrials.gov API v2 on
> 2026-11-03 and agree with the Gen 6 inspections where
> they overlap; agent inspection = pre-extraction, human
> dual extraction PENDING. **This file scores nothing,
> moves no cell, and admits nothing to the validation
> set (still 0). G3b BLOCKED. FROZEN retained.**
>
> **What "setup" means here.** Gen 5 and Gen 6 both
> queued "quarterly dated re-sweeps" as an obligation
> without filing the procedure. This file files it:
> exact queries (§3), a field-level diff list (§4), a
> dated calendar (§5), per-trial change actions (§6),
> and — the load-bearing part — a **pre-opening siding
> rule draft** (§7) written *now*, while all three
> records show `hasResults: false`, so that the first
> results posting cannot be sided after the fact. §7 is
> a draft for human ratification (HP-MON-1, §9); until
> ratified it binds agents only in its conservative
> direction (when in doubt: DESIGN, do not open).

## 1. Watched records — state as inspected 2026-11-03

| NCT | Program (official title, abbreviated) | Status | Enrolment | Est. primary completion | `hasResults` | Why this project watches it |
|---|---|---|---|---|---|---|
| NCT07627971 | SONIX / SKY-GJB2-001: single unilateral intracochlear SKY-GJB2, pediatric *GJB2* (Skylark Bio) | RECRUITING (verified 2026-08; last update posted 2026-08-27; started 2026-05-28) | 10 estimated (Older 4 aged 2–7 y; Younger 6 aged 9 mo–<2 y) | **2027-12** (completion 2028-06) | false | I1/I2 anchor kill + P6 branch source of record; first *candidate* validation source in the record (Gen6-summary §4.5) |
| NCT07032038 | Rincell-1 otic neural progenitor cell therapy + standard care vs standard care, adults with neural hearing loss eligible for CI (Rinri) | NOT_YET_RECRUITING (verified 2026-09; last update posted 2026-10-01; est. start 2027-09) | 20 estimated | **2029-05** (completion 2029-08) | false | Gen 5 first-reserve family: revisit trigger = first human safety readout → re-sweep as candidate Family L (broaden-sweep §3). No current candidate predicts it |
| NCT07752888 | EA0010 in *OTOF*-mutation patients who have received CI | ACTIVE_NOT_RECRUITING (verified 2026-08; last update posted 2026-08-12; started 2026-05-23) | **1 actual** | **2027-05-31** (completion 2027-07-31) | false | First human-ward Q0 (post-CI delivery) pointer. Q0 remains UNDECIDABLE-no-data; a registry record with N=1 and no results is not data (resweep §4) |

Notes on provenance, so the table is not over-read:
(a) NCT07627971 and NCT07752888 rows reproduce the
Gen 6 full-record inspections (resweep §§2, 4) and were
confirmed unchanged in status/enrolment/dates by the
2026-11-03 API v2 re-fetch. (b) NCT07032038 was
**secondary-source only** in Step 0/Gen 0 and inspected
at registry level in Gen 5 (status NOT_YET_RECRUITING,
verified 2026-09, est. start 2027-09); today's re-fetch
adds the dates in the table (last update 2026-10-01,
primary completion 2029-05, enrolment 20 estimated =
Gen 5's "2 cohorts × 10 planned"). No eligibility,
outcome, or intervention detail beyond Gen 5's
inspection is asserted from the re-fetch. (c) Dose/
capsid/volume for SKY-GJB2 remain **absent** from the
NCT07627971 record (HP-I1-1 stands); route detail for
EA0010 beyond resweep §4's truncated clause remains
**not asserted**. Registry existence/structure is never
a signal (D-rules, carried).

## 2. Standing rules this protocol may not reinterpret

Carried verbatim in substance from resweep §1 and the
D-rules; the watch executes them, it does not amend
them:

1. Already-seen or late-found **pre-freeze** records are
   DESIGN, never validation. No human freeze has
   occurred as of 2026-11-03.
2. Validation requires post-freeze, pre-registered,
   **unopened** evidence. Validation set = 0 until §7's
   procedure is both ratified and satisfied.
3. Registry existence, recruiting status, target N, and
   amendments are eligibility/monitoring facts only —
   never efficacy or safety signals.
4. External-program results (SONIX, Rincell-1, EA0010,
   DB-OTO) are never this project's candidate effects
   (D13). SONIX results, when they exist, are
   validation-side material for I1/I2's anchor kill —
   never retrofitted into P6 rules (R-P6-10).
5. Agents never self-update P6's source of record:
   updates enter only via the quarterly dated re-check
   ratified under **HP-P5-3** (P6 R-P6-5). A monitoring
   finding is a *proposed* source-of-record update until
   that ratification.
6. Every absence claim is bounded: this watch covers
   ClinicalTrials.gov + PubMed. Embase / EU CTIS /
   ChiCTR / ANZCTR remain **unsearched** (Gen 5–6 bound,
   unchanged); §3.3 files the owed expansion as a named
   gap, not as coverage.

## 3. Exact registry queries (run verbatim; log raw responses)

### 3.1 ClinicalTrials.gov API v2 — per-record status pull (results-blind form)

The routine quarterly pull uses the **fields-limited**
form, which returns status/structure *without* any
results section — this is the technical enforcement of
§7's do-not-open rule, not a courtesy:

```
https://clinicaltrials.gov/api/v2/studies?query.term=NCT07627971&fields=NCTId,BriefTitle,OverallStatus,StatusVerifiedDate,StartDate,PrimaryCompletionDate,CompletionDate,LastUpdatePostDate,HasResults,EnrollmentCount,EnrollmentType,LeadSponsorName,Phase&format=json
https://clinicaltrials.gov/api/v2/studies?query.term=NCT07032038&fields=NCTId,BriefTitle,OverallStatus,StatusVerifiedDate,StartDate,PrimaryCompletionDate,CompletionDate,LastUpdatePostDate,HasResults,EnrollmentCount,EnrollmentType,LeadSponsorName,Phase&format=json
https://clinicaltrials.gov/api/v2/studies?query.term=NCT07752888&fields=NCTId,BriefTitle,OverallStatus,StatusVerifiedDate,StartDate,PrimaryCompletionDate,CompletionDate,LastUpdatePostDate,HasResults,EnrollmentCount,EnrollmentType,LeadSponsorName,Phase&format=json
```

Full-record pull (eligibility/outcomes/design diffing,
§4) — permitted quarterly **only while `hasResults`
is false**; the moment any record flips to true, this
form is barred to agents until §7 opening is authorized,
because the full record carries the results section:

```
https://clinicaltrials.gov/api/v2/studies/NCT07627971?format=json
https://clinicaltrials.gov/api/v2/studies/NCT07032038?format=json
https://clinicaltrials.gov/api/v2/studies/NCT07752888?format=json
```

Human-clickable counterparts (same records, for the
HP-P5-3 ratifier): `https://clinicaltrials.gov/study/`
+ NCT number. Registry history (what changed between
postings) is checked on the study page's history view at
ratification; agents record `LastUpdatePostDate` each
quarter so a silent amendment cannot pass unnoticed
between checks.

### 3.2 PubMed (E-utilities) — companion publication watch

Journal publication can precede registry results posting
(DB-OTO precedent, resweep §3.1: NEJM 2026 results while
NCT05788536 still showed `hasResults: false`). A
registry-only watch would therefore miss exactly the
event §7 exists for. Run each quarter, `retmax=50`,
results **title-level only** for agents once §7's seal
is in force for that program (abstracts of a *results*
paper are results; see §7.4):

```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22SKY-GJB2%22%20OR%20NCT07627971%20OR%20SONIX%5BTitle%5D&retmode=json&retmax=50
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22Rincell-1%22%20OR%20NCT07032038%20OR%20%22otic%20neural%20progenitor%22&retmode=json&retmax=50
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=%22EA0010%22%20OR%20NCT07752888&retmode=json&retmax=50
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=(GJB2%20gene%20therapy%20hearing)%20AND%202026%3A3000%5Bpdat%5D&retmode=json&retmax=50
```

New PMIDs are logged by number + title (§8). Reviews/
editorials are logged as such and admitted as nothing
(resweep §2 precedent). Sponsor press releases and
conference abstracts are pointers only, per the standing
evidence rule — logged, never extracted as data.

### 3.3 Owed expansion (named gap, not coverage)

EU CTIS, ChiCTR, ANZCTR, and Embase remain unsearched
for all three programs. EA0010 in particular may have
non-US registry footprints this watch cannot see. Until
a human-licensed search closes this (Gen6-summary §4
item 3), every quarterly log line carries the bound:
"absence = within ClinicalTrials.gov + PubMed on this
date." The watch does not silently upgrade its own scope
by adding a registry mid-stream; scope changes are
HP-MON-2 amendments (§9), dated, so pre/post coverage
remains distinguishable in the log.

## 4. Field-level diff checklist (every quarterly run, all three records)

Compare against the previous quarter's archived raw
response; file the diff, not a summary impression:

- [ ] `overallStatus` and `statusVerifiedDate`
- [ ] `hasResults` (the §7 trigger field)
- [ ] `lastUpdatePostDate` (any advance with no status
      change = amendment to identify at ratification)
- [ ] enrolment count **and** type flips
      (ESTIMATED → ACTUAL is itself a reportable event)
- [ ] start / primary-completion / completion dates
      (slips re-date §5's event-driven checks)
- [ ] eligibility criteria text (SONIX: P6 R-P6-1…10 bind
      rule-by-rule to this text — any change is a
      proposed source-of-record update under HP-P5-3,
      and P6 dispositions from a superseded text are an
      audit failure per P6 FMEA)
- [ ] primary/secondary outcome measures text (an outcome
      redefinition before results is a §7.4.4 event)
- [ ] arms/interventions text (incl. any appearance of
      dose/capsid/volume language in NCT07627971 —
      HP-I1-1's missing content; if it appears it is
      logged verbatim and still moves no cell by itself)
- [ ] sponsor / collaborators / locations count
      (structure facts only, §2 rule 3)
- [ ] new PubMed PMIDs per §3.2 (number + title +
      publication type)

## 5. Calendar — next check dates

Quarterly anchor = the 3rd of the month, quarterly from
the 2026-11-03 inspection that filed this protocol.
Event-driven rows tighten cadence inside the window
where a results posting becomes plausible; the quarterly
rows never lapse.

| Date | Type | Scope |
|---|---|---|
| **2027-02-03** | Quarterly Q1 | All three records, §3+§4 in full |
| **2027-05-03** | Quarterly Q2 | All three; NCT07752888 enters its est. primary-completion month (2027-05-31) — §7 seal check for EA0010 is the headline item |
| 2027-06-03 | Event-driven | NCT07752888 only (monthly until completion 2027-07-31 or results event) |
| 2027-07-03 | Event-driven | NCT07752888 only |
| **2027-08-03** | Quarterly Q3 | All three |
| **2027-11-03** | Quarterly Q4 | All three; NCT07627971 one quarter from est. primary completion — confirm §7 predictions for I1/I2 are filed and sealed before 2027-12 |
| 2027-12-03, then monthly | Event-driven | NCT07627971 only, from its est. primary-completion month (2027-12) until results event or a dated slip re-anchors the window |
| **2028-02-03** | Quarterly | All three; SONIX completion horizon 2028-06 |
| quarterly thereafter | Quarterly | NCT07032038 becomes the long pole (est. start 2027-09, primary completion 2029-05): quarterly until first-dosed is a matter of inspected record, then §6's revisit trigger governs |

A missed date is logged as missed with the actual run
date beside it; back-dating a check to its scheduled
date is falsifying the source of record and is barred.
Any §4 trigger (status flip, `hasResults` flip, outcome-
text change) found at any check starts §6/§7 actions
immediately — actions do not wait for the next quarter.

## 6. Per-trial change actions (what a diff *does*)

**NCT07627971 (SONIX).** (i) Status → suspended /
terminated / withdrawn, **or** results posted ⇒
**R-P6-10 auto-freeze fires**: no new P6
`referral-actionable` dispositions until human review
under HP-P5-1/HP-P5-3 reopens, redefines, or retires the
branch. The monitoring log records the firing; only
humans lift it. (ii) Eligibility/outcome text change ⇒
proposed source-of-record update to HP-P5-3; P6 keeps
running on the prior ratified text or freezes if humans
so rule — agents do not pick. (iii) Results posted ⇒
§7 governs opening; the results are the **I1/I2 anchor-
kill input** (I1: no ABR signal at primary completion,
or G5 signal at ≥Moderate GRADE ⇒ branch auto-close via
HP-P5-1, per P6 §6) and are never P6 effects.
(iv) Dose/capsid/volume appearing in the record ⇒
HP-I1-1 narrows; Gen6-summary §4.7's I3 condition ("a
public SONIX dose record supplies a clinical-product
dose I2's rules can bind") becomes evaluable *by humans*;
agents file the verbatim text and stop there.

**NCT07032038 (Rincell-1).** Status → RECRUITING or
first-dosed becoming inspected fact ⇒ log + continue
quarterly (recruiting is a structure fact, §2 rule 3).
**First human safety readout** (registry results or
peer-reviewed record) ⇒ the Gen 5 revisit trigger fires:
re-sweep cell therapy as candidate Family L is *proposed
to humans*; until then cell therapy stays first-reserve,
not a candidate. No current candidate has a kill,
prediction, or cell bound to this trial — §7.3 makes
that explicit so a readout cannot be claimed as any
existing candidate's validation.

**NCT07752888 (EA0010).** Any results event ⇒ §7
governs; whatever emerges bears on **Q0 as a question**
(first human post-CI delivery data) and on QR4's design
context. It does not, by existing, retire any G4-AAV leg:
QR4 Stages 0→1 remains the only pre-registered route to
that (Gen6-summary §4 item 4), and the G4 clause
"unstudied post-CI AAV claimed preserved = FAIL" stands
until human GRADE of actual data says otherwise.
Enrolment staying at 1 actual through completion is
itself the finding to log plainly, not a disappointment
to narrate around.

## 7. Siding rule — DRAFT, written pre-opening (HP-MON-1)

*Drafted 2026-11-03 while all three records show
`hasResults: false` and no results publication for any
of the three programs is in the inspected record. That
timing is the point: a siding rule written after results
exist is a rationalisation with a date on it.*

### 7.1 Definitions

- **Opening** a record = any project member or agent
  inspecting result *content*: a registry results
  section, a results-paper abstract/full text, a results
  press release with numbers, or a conference results
  presentation. Status fields, `hasResults`, titles, and
  "results posted on <date>" metadata are **not**
  opening — §3.1's fields-limited pull exists precisely
  to keep monitoring possible without opening.
- **Sealed prediction** = a dated, human-signed statement,
  filed before opening, of what a named candidate's
  already-filed kill/advance criteria predict for a named
  record's named outcome, in the candidate's own units
  where they exist. Predictions are filed by hash +
  timestamp in the monitoring log (§8); content may be
  kept sealed until opening, existence may not.
- **Freeze** = the human protocol/freeze act owed since
  Gen 0 (H-pins PENDING). This draft does not create a
  freeze; it specifies what a freeze must contain for
  these three records to be sideable at all.

### 7.2 The rule (draft)

A result from a watched record is admitted as
**validation** for a named candidate **iff all** of:
(a) the human freeze predates the first opening of that
result by anyone on the project (agents included);
(b) a sealed prediction for that candidate × that record
× that outcome predates the opening; (c) the opening is
performed or witnessed by the named human extractor pair
and logged with date/time in §8 before any agent
processes the content; (d) human dual extraction +
GRADE follow — agent pre-extraction of opened results
is labeled as such and scores nothing alone.
**Any element missing ⇒ the result is DESIGN**
(exploratory-after-seen: Y) for every candidate,
permanently for that record-outcome pair. There is no
appeal, re-seal, or "we obviously would have predicted"
route: a prediction reconstructed after opening is a
postdiction, and filing one as validation is the exact
failure this rule exists to prevent.

### 7.3 Per-record prediction slots (state today: all empty)

| Record | Candidate(s) with a fileable prediction | Prediction content available to seal (candidate's own filed words) | Status 2026-11-03 |
|---|---|---|---|
| NCT07627971 | GEN5-I1, GEN5-I2 (anchor kill); GEN6-P6 branch (process only) | I1 anchor kill as filed: no ABR signal at SONIX primary completion (or G5 signal at ≥Moderate GRADE) kills I1 and auto-closes the P6 branch via HP-P5-1. SONIX's own secondary outcome is ABR threshold change (dB HL) — the measurable the kill binds to. **"ABR signal" has no filed numeric threshold in I1 as inspected** ⇒ HP-MON-1 must either adopt the kill verbatim as a qualitative prediction (weaker: a two-sided reading dispute is pre-programmed) or humans file a numeric operationalisation *before* opening. Agents may not supply the number | **No freeze, no sealed prediction.** If SONIX results were opened today they would be DESIGN for I1/I2 by §7.2 — the record's first validation candidate is one unsigned human act away from being spendable or losable |
| NCT07032038 | None | No filed candidate, kill, or cell references Rincell-1 outcomes. The Gen 5 revisit trigger is a *re-sweep* trigger, not a prediction | Any readout is DESIGN/re-sweep input by construction; it can become validation only for a future Family-L candidate frozen before a *later* readout |
| NCT07752888 | None (Q0 is a question, not a candidate; QR4 is a program design) | No candidate predicts an EA0010 outcome; Q0's current state (UNDECIDABLE-no-data) is a statement about evidence absence, not a forecast | Any result is DESIGN for candidate purposes; its effect on Q0's *label* is a human GRADE act after extraction, never an automatic consequence of posting |

### 7.4 Contamination rules

1. If any agent run, web snippet, news item, or
   collaborator communication brings result *content*
   into the project before §7.2 is satisfied for that
   record, the log records the contamination (date,
   channel, what was seen) and that record-outcome pair
   is DESIGN from that moment. Pretending not to have
   seen it is barred; the honest cost of contamination
   is the loss of one validation slot, which is cheaper
   than a corrupt validation set.
2. Journal-first publication (DB-OTO pattern) counts
   identically to registry results: the seal is over
   *content*, not over ClinicalTrials.gov. §3.2 therefore
   runs title-only for a program once its prediction is
   sealed.
3. Partial postings (e.g. safety-only results, first-
   cohort-only) open only the outcomes they contain; the
   seal survives for un-posted outcomes **only if** the
   sealed prediction named outcomes separately. A lumped
   prediction is spent by the first partial opening —
   another reason §7.3's SONIX operationalisation must be
   outcome-specific.
4. Sponsor amendments to outcome text after a prediction
   is sealed (§4 checklist catches these) do not break
   the seal, but the prediction is thenceforth read
   against *both* outcome versions and the discrepancy
   is filed; silently following the amended outcome is
   barred.

### 7.5 What this draft deliberately does not do

It sets no efficacy threshold for any trial (not the
watch's competence), grades nothing, and creates no
freeze. Ratification (HP-MON-1) plus an actual freeze
plus sealed predictions are three separate human acts;
this file's existence satisfies none of them. The
earliest date by which the SONIX slot must be sealed to
be worth anything is *before first opening*, which —
given journal-first risk — means the binding deadline is
**not** 2027-12; it is as soon as humans can act, and
certainly before the 2027-11-03 quarterly check (§5)
that this protocol schedules as the last seal audit.

## 8. Quarterly log template (append-only; one block per run)

```
## Run <actual-date> (scheduled <date>; runner <agent/human>)
Bound: ClinicalTrials.gov + PubMed only (§3.3).
| NCT | status | hasResults | lastUpdatePosted | enrolment (n, type) | PC date | diff vs prior archive | §6 action fired? |
| NCT07627971 |  |  |  |  |  |  |  |
| NCT07032038 |  |  |  |  |  |  |  |
| NCT07752888 |  |  |  |  |  |  |  |
New PMIDs (§3.2): <numbers + titles + type, or "none">
Eligibility/outcome text changes: <verbatim diff or "none">
Seal state (§7.3): <predictions filed/sealed since last run, by hash>
Contamination events (§7.4.1): <none | description>
Raw responses archived at: <paths>
HP-P5-3 proposed source-of-record updates: <none | items>
```

First entry is this file's §1 table (run 2026-11-03,
scheduled = protocol creation, diff baseline = Gen 6
inspections for NCT07627971/NCT07752888, Gen 5
inspection for NCT07032038; no §6 action fired; seal
state: nothing sealed; contamination: none known).

## 9. HOLDER-PINs

Carried: **HP-P5-3** (quarterly source-of-record
ratification — this protocol is its executable form;
monitoring findings bind P6 only through it) ·
HP-P5-1 (branch reopen/retire after R-P6-10) ·
HP-I1-1 (SONIX dose absence; §4 watches for its
resolution) · I1/I2 anchor kill (unevaluated; its
evaluation input is §7-governed).
New: **HP-MON-1** ratify or amend §7 and file/reject the
§7.3 SONIX prediction (including the "ABR signal"
operationalisation decision) — time-critical per §7.5 ·
**HP-MON-2** scope/cadence amendments (§3.3 registries,
§5 dates) as dated amendments, never silent edits ·
**HP-MON-3** name the human extractor pair who own
opening (§7.2c) and the log's custodian (H-1…H-8
PENDING as throughout).
Unpinned ⇒ the watch still runs (status facts are
cheap and safe), but nothing it ever finds can be sided
above DESIGN. That asymmetry is intentional.

## 10. Standing state

Validation set **0**. Q0 UNDECIDABLE-no-data. I1/I2
anchor kill unevaluated (cannot evaluate before
2027-12 est.). G4-AAV stands for C/D/I1/I2/K1. G3b
BLOCKED. FROZEN retained. No PASS, no winner, no stop
(v2.3): the next scheduled act in this workstream is
the **2027-02-03** quarterly run — unless humans take
up HP-MON-1 first, which §7.5 argues is the only item
on this page that gets more expensive every quarter it
waits.

*End. Gen 7 monitoring setup under GOAL v2.3.
Inspected records only; scores nothing; opens nothing.*
