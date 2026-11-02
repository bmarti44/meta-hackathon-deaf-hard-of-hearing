# Gap attack (round 1) — multi-registry + Q0 second search

> **Model routing (GOAL §9).** Requested route: **Sol 6.1**.
> Actual runtime model: **`muse-wonder-full-1.0`** (probe
> 2026-11-02: sol-6.1 route rejected / not in catalog).
> Substitution disclosed per §9 rule 3. No claim here is
> Sol 6.1 work. **Date: 2026-11-02.** GOAL v2.2.
>
> **Attack identity.** Promotion-blocking-gap attack,
> round 1 (GOAL §7 rule 4), against Step 5 §6 gaps #7
> (search completeness: EU CTIS / ChiCTR / ANZCTR
> unsearched; all absence claims bounded) and #4 (Q0
> decider data). Inputs read before searching:
> `research/Step5-decision-no-winner.md` §6,
> `research/gen00/Q0-thresholds.md` (§§2.1–2.3 estimands),
> `research/gen00/Q0-verdict.md`,
> `research/gen00/protocol.md` §3 (frozen databases,
> S-Q0a/S-Q0b, S-REG), `research/step0/`
> `verify-epidemiology-q0.md` (E4a–E4d), Step 1 pin
> summary header. Thresholds were **not** moved.
>
> **Evidence rule.** Inspected records only: PubMed
> E-utilities full MEDLINE abstracts, ClinicalTrials.gov
> API v2 full records, EU Clinical Trials Register (EU
> CTR legacy) search-result pages via `web_fetch`, WHO
> ICTRP `Trial2.aspx` mirror of one ChiCTR record, and
> one ANZCTR `TrialReview.aspx` record via `web_fetch`.
> `web_search` was used only to locate record numbers;
> snippets are never cited as evidence. No number below
> was invented; every count traces to an inspected API
> response or page quoted in §5. Human dual extraction
> remains **PENDING**; this file decides no gate and
> re-scores no candidate.
>
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.**
> Nothing here can promote any Track-P candidate.

## Verdict in one paragraph

**Q0 stays Q0-UNDECIDABLE — sub-label no-data.** The
independent second search found no post-CI scala-patency
n/N under the §2.1 estimand and no post-CI AAV A1/A2
retention estimand under §2.2, so no component can be
zoned and the mandatory sensitivities (70%/90%;
0.70/0.90; 5/15 dB) remain inapplicable, not failed.
Two absence wordings from Gen 0 must nevertheless be
**narrowed** (bounded search, 2026-11-02): (i) EU OTOF
AAV trials do exist in inspected EU records (EudraCT
2022-000079-38 / CTIS 2024-511342-40-00; CTIS
2023-504466-28-00 via inspected cross-reference) and
both exclude prior CI in the treated ear; (ii) a
registered same-ear post-CI AAV study now exists
(NCT07752888, EA0010, single-subject design, **no
results posted** in the inspected record) — it supplies
a design, not a Q0-A estimand. The multi-registry gap
is **partially attacked, not closed**: EU CTR legacy
was searched; CTIS public-search UI, ANZCTR keyword
search, and ChiCTR direct search were not executable
as text-inspectable searches in this runtime (§2.4),
so no ANZCTR/ChiCTR/CTIS-UI absence claim is made.

## 1. Frozen strings (fixed before results were read)

Run date for every string: **2026-11-02**. Registry
terms follow protocol §3 S-REG narrowed to the four
assigned concepts; PubMed Q0 strings are **new**
(independent of frozen S-Q0a/S-Q0b) per assignment.

### 1.1 Registry terms (per registry interface)

```text
R1: OTOF AAV          (plus single-term controls: OTOF; otoferlin)
R2: optical cochlear  (plus: optogenetic)
R3: neurotrophin cochlear (plus: neurotrophin)
R4: auditory nerve implant (plus: auditory nerve)
Control: cochlear implant (proves the interface returns hits)
```

EU CTR executes the text field as entered at
`clinicaltrialsregister.eu/ctr-search/search?query=…`.
Counts below are the page's own "Trials with a
EudraCT protocol (n)" / "Query did not match" lines.

### 1.2 PubMed Q0 second-search strings (NEW)

```text
N-Q0-1a (post-implant scala patency imaging CT):
("cochlear implant"[tiab] AND scala[tiab] AND patency[tiab]
 AND (imaging[tiab] OR "computed tomography"[tiab] OR CT[tiab]))
N-Q0-1b (widened patency check):
("scala tympani"[tiab] AND patency[tiab] AND "cochlear implant"[tiab])
N-Q0-2 (explant / reimplantation scala):
((explant*[tiab] OR reimplant*[tiab]) AND scala[tiab]
 AND "cochlear implant"[tiab])
N-Q0-3a (AAV previously implanted cochlea, animal):
(("adeno-associated virus"[tiab] OR AAV[tiab])
 AND ("previously implanted"[tiab] OR "implanted cochlea"[tiab]
      OR "cochlear implant"[tiab]) AND animal[tiab])
N-Q0-3b (AAV + CI census, re-run):
(("adeno-associated virus"[tiab] OR AAV[tiab])
 AND "cochlear implant"[tiab])
```

Q0-P eligibility (Q0-thresholds §2.1): % of implanted
ears patent/cannulable for later infusion, n/N by
time-since-implant band, pre-stated access definition;
denominator includes explanted/failed/ungradeable.
Q0-A eligibility (§2.2): AAV delivered **after** an
established implant vs same-study unimplanted
comparator, with A1 (transduction retention ratio)
and A2 (threshold-improvement difference). Sequence
classes (i) before/concurrent, (ii) after established,
(iii) unclear — only (ii) counts.

## 2. Registry attack — what was inspected

### 2.1 EU: CTR legacy searched; CTIS via cross-reference

EU CTR search pages (inspected via `web_fetch`,
2026-11-02; register header states 44,416 EudraCT
trials and that Regulation 536/2014 trials are in
CTIS — so EU CTR ≠ CTIS and zeros below are EU-CTR
zeros only):

| Term | EudraCT hits (page count) | Inspected result |
|---|---|---|
| `OTOF` | 0 ("Query did not match") | Gene-symbol spelling misses the trial below — term sensitivity, logged |
| `otoferlin` | **1** | EudraCT **2022-000079-38**, protocol DB-OTO-001, sponsor Decibel Therapeutics, start 2023-05-09, Phase 1/2 intracochlear DB-OTO (CHORD) |
| `optical cochlear` | 0 | No match |
| `optogenetic` | 0 | No match |
| `neurotrophin cochlear` | 0 | No match |
| `neurotrophin` | 1 | EudraCT 2022-003050-32 (FAB122 in ALS, Ferrer) — **not cochlear**; excluded on full title |
| `auditory nerve implant` | 0 | No match |
| `auditory nerve` | 14 | All 14 protocol numbers listed on the results page; sponsors are drug programmes (e.g. Novartis, Pfizer, Roche, Biogen) — none is a penetrating auditory-nerve-implant trial on title/protocol inspection of the results list |
| `cochlear implant` (control) | 7 | Interface works; 7 EudraCT numbers returned (2017-002377-19, 2015-002672-25, 2015-003929-34, 2012-005002-22, 2021-004323-33, 2015-002602-36, 2015-005278-40) |

The EU CTR trial-detail page for 2022-000079-38/ES was
fetched, but the text processor returned field labels
without values; **no detail value is cited from it**.
Eligibility facts below come from the inspected
ClinicalTrials.gov API v2 full record for the same
trial, which carries both identifiers
(EUDRACT 2022-000079-38; CTIS 2024-511342-40-00).

CTIS proper (`euclinicaltrials.eu/search-for-clinical-
trials/`) is a JavaScript application: `web_fetch`
returns the shell page without result rows, and the
guessed JSON endpoint returned 403. CTIS existence
for OTOF AAV is therefore established **only** by
inspected CTgov secondary-ID fields, not by a CTIS-UI
search:

- **CHORD / DB-OTO (NCT05788536; CTIS
  2024-511342-40-00; EUDRACT 2022-000079-38).**
  Status RECRUITING (verified 2026-08 in record).
  Key exclusion 6: *"History or presence of cochlear
  implants in the ear(s) to be infused with DB-OTO."*
  Cannot answer Q0-A (label-eligible ears only) —
  confirms Gen 0 Q0-L handling, now on an EU record.
- **AUDIOGENE / SENS-501 (NCT06370351; CTIS
  2023-504466-28-00).** Status ACTIVE_NOT_RECRUITING;
  children 6–31 months. Exclusion: *"Patients with a
  prior or current cochlear implant."* Same Q0
  consequence.
- **AK-OTOF (NCT05821959; CTIS 2026-525943-33-00)**
  appears in the inspected CTgov `OTOF` census
  (totalCount 15) with a CTIS secondary ID; its full
  eligibility text was not separately pulled in this
  pass, so no eligibility claim is made for it here.

Bounded wording: *no optical-cochlear, optogenetic,
neurotrophin-cochlear, or auditory-nerve-implant
trial was found in EU CTR legacy under the §1.1
terms on 2026-11-02.* CTIS-UI absence for those
concepts is **not** claimed (UI not searched).

### 2.2 ChiCTR: direct blocked; one mirrored record

Direct ChiCTR (`chictr.org.cn/searchprojEN.html`)
returned HTTP **405** with an Aliyun WAF block page
("your request has been blocked…") to scripted fetch,
and an empty processed body to `web_fetch`. **No
ChiCTR keyword search was executed; no ChiCTR absence
claim is made for any §1.1 term.**

One ChiCTR OTOF record was located by registration
number and inspected in full as the WHO ICTRP mirror
(`Trial2.aspx?TrialID=ChiCTR2200063181`, register
ChiCTR, last refreshed 2025-09-15 in the mirror):

- **ChiCTR2200063181** — RRG-003 AAV-OTOF, Eye & ENT
  Hospital of Fudan University; registered
  2022-09-01; recruiting in mirror; round-window
  injection dose groups. Exclusion 8: *"implants
  (such as cochlear implants) are present in the ear
  (on the same side of the intended surgery)"* (with
  a stated exceptions note). Same-ear post-CI
  delivery is therefore excluded by design in this
  record; it cannot answer Q0-A.
- ICTRP free-text `Search.aspx?query=…` returned the
  portal error page ("temporarly unavailable") for
  all three test queries, so ICTRP could not
  substitute for a ChiCTR keyword sweep.

Post-CI ChiCTR relevance runs the other way: the
only inspected same-ear post-CI AAV design (§2.5,
NCT07752888) is a China-site study registered on
ClinicalTrials.gov. Whether a ChiCTR counterpart
exists is **unresolved** (direct search blocked);
do not assert either way.

### 2.3 ANZCTR: records inspectable, search not run

`TrialSearch.aspx` states *"This page requires
JavaScript enabled to work correctly"*; scripted
fetch hits a Cloudflare managed-challenge page.
**No ANZCTR keyword search was executed; no ANZCTR
absence claim is made for any §1.1 term.**

That ANZCTR full records *are* text-inspectable when
addressed directly was verified on one record
(`TrialReview.aspx?id=23330`, NCT06642935, totally
implantable CI feasibility in adults — imported from
ClinicalTrials.gov; irrelevant to R1–R4 except as an
access proof). Closing this leg needs a human
browser search or an ANZCTR data export (§4).

### 2.4 Access log (so round 2 does not repeat dead ends)

| Route | Result on 2026-11-02 |
|---|---|
| EU CTR `ctr-search/search?query=` via `web_fetch` | **Works** (counts + result lists inspected) |
| Same URL via `curl` | "Request Rejected" (WAF) — do not use |
| CTIS search UI via `web_fetch` | Shell only, no rows (JS app) |
| CTIS guessed API `/ctis-public-api/search` | HTTP 403 |
| ChiCTR search page | HTTP 405 WAF block / empty body |
| WHO ICTRP `Trial2.aspx?TrialID=` | **Works** (single-record mirror) |
| WHO ICTRP `Search.aspx?query=` | Portal error page |
| ANZCTR `TrialSearch.aspx` | JS-required / Cloudflare challenge |
| ANZCTR `TrialReview.aspx?id=` via `web_fetch` | **Works** (single record) |
| ClinicalTrials.gov API v2 | **Works** (full records inspected) |
| PubMed E-utilities | **Works** (counts + MEDLINE abstracts) |

### 2.5 The one design that changes Q0 wording

**NCT07752888 — EA0010 in OTOF patients who have
received cochlear implantation** (Shanghai EmayGene;
site Wuhan, China; full CTgov API record inspected).
Official title: safety/tolerability/efficacy of
EA0010 in OTOF hearing loss *"Who Have Received
Cochlear Implantation."* Design: single-center,
single-arm, open-label; **enrollment count 1
(ACTUAL)**; status ACTIVE_NOT_RECRUITING; start
2026-05-23; first posted 2026-08-07; primary
completion estimated 2027-05-31. Intervention as
registered: single intratympanic injection through
the stapes annular ligament **into the implanted
cochlea**, dual AAV at 2.0×10¹¹ vg/ear total
(10–40 µL), ages 1–17 y, click ABR ≥80 dBnHL.
Primary outcome is AE/SAE/DLT incidence to Week 26.
**`hasResults: false`** — no results, no patency
data, no transduction or threshold outcome posted.

Q0 scoring: sequence class **(ii) by design** (AAV
after established CI, same ear) — the first
inspected human design of the right *shape*. It
still cannot zone Q0-A: no unimplanted comparator,
no A1/A2 readout, n=1 registry target, zero results.
It refutes only the unqualified sentence "no human
post-CI AAV study exists"; the correct bounded
sentence is now: *one registered single-subject
post-CI AAV study was found (bounded search,
2026-11-02); no post-CI AAV efficacy result was
inspected.* Q0-thresholds §2.3 minima still fail on
every count.

Neighbouring record, explicitly **not** class (ii)
evidence: **NCT05901480** (OTOV101, Otovia) excludes
*bilateral* CI / major inner-ear surgery but *"not
include unilateral cochlear implantation"*; the
record does not state that the implanted ear is the
injected ear. Sequence **(iii) unclear**; never
counts toward Q0-A.

### 2.6 Optical / neurotrophin / ANI registry reads

- **Optical cochlear.** EU CTR 0/0 (above). CTgov
  term searches (API, inspected): `optical cochlear
  implant` totalCount 6; `optogenetic cochlear`
  totalCount **0**. The one relevant full record,
  **NCT05110183** (Northwestern, ENROLLING_BY_
  INVITATION, est. n=30), is an intra-operative
  **infrared** opto-electrical feasibility test in
  adults (18–89 y) undergoing translabyrinthine
  tumour surgery with cochlear sacrifice: transient
  light-delivery + CAP recording over 30 minutes,
  children explicitly excluded, `hasResults: false`.
  Per protocol §3 S-C discipline, non-optogenetic
  infrared stimulation is never pooled with
  optogenetic oCI. Bounded conclusion: *no human
  optogenetic optical-CI trial was found in EU CTR
  legacy or ClinicalTrials.gov term searches on
  2026-11-02; one adult intra-operative infrared
  feasibility record exists.* Candidate C's "no
  adult FIH" wording should be re-bounded to
  *optogenetic* FIH; the infant G6 consequence is
  unchanged (adult, transient, non-optogenetic).
- **Neurotrophin cochlear.** EU CTR 0 (exact phrase;
  single-term hit is ALS, excluded). CTgov
  `neurotrophin cochlear` totalCount **0**. Bounded
  absence only for those two sources/terms/date.
- **Auditory nerve implant.** EU CTR exact phrase 0;
  broad `auditory nerve` 14 drug trials, none ANI.
  CTgov `auditory nerve implant` totalCount 101 is
  a noisy term expansion (first-page titles are CI,
  ABI compassionate use, vestibular, vagus-nerve
  and unrelated records); only the first page was
  title-screened, so **no CTgov ANI absence claim**
  is made from it. EU-CTR bounded absence stands;
  ANI human-trial absence remains incompletely
  attacked (§4).

## 3. Q0 second search (PubMed, NEW strings)

All counts are E-utilities `esearch` counts on
2026-11-02; every record in N-Q0-1/N-Q0-3a and all
23 records in N-Q0-2 were abstract-screened from
inspected MEDLINE records. The broad control
`(explantation OR reimplantation) AND cochlear`
returned 450 hits and was **not** screened; no claim
rests on it.

### 3.1 N-Q0-1: patency imaging — pre-implant, wrong direction

N-Q0-1a = **4** hits (PMIDs 8614729, 8570248,
3110517, 3108799); N-Q0-1b = **5** hits (the same
four + PMID 23119861). All five abstracts inspected:

- PMIDs 8570248 (1996, n=28), 8614729 (1996, n=79),
  3110517 (1987, 36 ears), 3108799 (1986, n=6) assess
  **pre-operative** HRCT prediction of scala patency
  in unimplanted CI *candidates* (ossification from
  disease, surgical candidacy). Time runs backwards
  relative to Q0-P: patency *before* first implant
  says nothing about cannulatability *after* an
  implanted course. Ineligible for §2.1 on cohort,
  timing, and endpoint.
- PMID 23119861 (2002) is a surgical-landmark study
  (Jacobson's nerve); "patency" is incidental text.
  Ineligible.

**No inspected abstract reports post-implant scala
patency/cannulatability n/N by time band at any
GRADE.** Bounded statement: PubMed, N-Q0-1a/b,
2026-11-02.

### 3.2 N-Q0-2: explant/reimplantation — close, still not patency

N-Q0-2 = **23** hits, all abstract-screened. The set
is mostly explant-force models, electrode-position
revision studies, case reports, and false hits
(neonatal explant cultures). Two series carry
insertion-success numerators and are the strongest
attack on Q0-P this round — both fail §2.1, for
stated reasons:

- **Sterkers et al. 2015 (PMID 25843784)** — 45
  reimplanted prelingually deafened children (of 539
  implanted 1990–2013): complete insertion in scala
  tympani in **42**, scala vestibuli in **1**,
  partial in **2**; mean insertion angle 330.5° →
  311.8° (p=0.48). **Why this is not a patency %:**
  denominator = selected device-failure/medical
  reimplantations, not all implanted ears; endpoint
  = electrode-array insertion completeness through
  (or around) the existing sheath/track, not
  infusion cannulatability under a pre-stated access
  definition; no time-since-implant banding; era
  1990–2013 devices. Entering 42/45 into the ≥80%
  HIGH test would repeat exactly the 78%
  hearing-preservation conflation Q0-thresholds was
  pre-registered to prevent. Logged as a *neighbour*
  (re-entry usually surgically possible), never as
  a bracketed Q0-P zone.
- **PMID 37489512 (2023)** — revision with same
  manufacturer; intra-operative CT scalar location /
  modiolar distance / insertion depth before vs
  after revision; 5 additional ST→SV translocations
  after revision. **N is not in the abstract**
  (deciding use forbidden per §2.3.4 in any case);
  endpoint is array position, not patency.
  Ineligible.

Remaining hits add mechanism colour only (e.g.
non-removable array case with scala-vestibuli rescue,
PMIDs 37943372/37845537; retained bands in a
temporal-bone case, PMID 24915284; 8-cat
explant/reimplant histology, PMID 2802465) — none
reports the §2.1 estimand. **Q0-P still cannot be
zoned.**

### 3.3 N-Q0-3: post-CI AAV — no class-(ii) animal estimand

N-Q0-3a = **2** hits, both inspected: PMID 32331858
(2020 review of neurotrophin gene therapy — non-
primary) and PMID 31222416 (2019, AAV-BDNF/GDNF in
neonatally deafened cats, **no electrical implant** —
unimplanted transduction/survival; cannot form a
post-CI retention ratio). Neither is class (ii).

N-Q0-3b census = **17** hits (Gen 0 screened 13
under a narrower string; the 4 additional records
were inspected here): PMID 42470357 (2026 OTOF
commentary), PMID 41516362 (2026 GJB2 review),
PMID 41366521 (2026 channelrhodopsin engineering —
AAV opsin to mouse/gerbil SGNs, optical implant
testing, **no established electrical implant**, so
not Q0-A), PMID 20301429 (GeneReviews OTOF chapter —
non-primary). The previously screened Pfingst record
(PMID 28776202) was re-inspected: *"inoculated with
an adeno-associated viral vector … and implanted"* —
class **(i) concurrent**, confirming Gen 0. No
inspected abstract delivers AAV after an established
implant + fibrosis course against a same-study
unimplanted comparator with A1 + A2 readouts.

**Q0-A still cannot be zoned.** EA0010 (§2.5) is
the human class-(ii) *design* counterpart with no
results; it does not substitute for the missing T2
estimand and must not be cited as efficacy either
way.

### 3.4 Q0 re-score under frozen thresholds

| Column | After this attack |
|---|---|
| Q0-L (label) | Unchanged, now corroborated on EU records: CHORD (CTIS 2024-511342-40-00), AUDIOGENE (CTIS 2023-504466-28-00), and ChiCTR2200063181 each exclude CI in the treated ear (inspected eligibility text). Label ≠ biology, both directions. |
| Q0-P (patency) | **Cannot be zoned.** No §2.1 n/N. Nearest neighbours (pre-implant HRCT; 42/45 re-insertion) explicitly excluded with reasons above. Sensitivities inapplicable. |
| Q0-A (post-CI AAV) | **Cannot be zoned.** No §2.2 A1/A2. One registered human class-(ii) design (NCT07752888, n=1, no results) + zero class-(ii) animal primaries in N-Q0-3. Sensitivities inapplicable. |

Composite (§3 row 4 of Q0-thresholds): **Q0-
UNDECIDABLE-no-data stands.** §2.3 minima still fail
(tier/estimand, GRADE ≥Moderate, human dual
extraction, denominators, validation independence).
No bracketed provisional zones are offered: 42/45
and the pre-implant CT accuracies are not point
estimates of the Q0 estimands. All Q0-dependent
gate cells remain INSUFFICIENT; Family G is neither
credited with a preserved biological option nor
penalised as if foreclosure were disproven. This
attack changes **wording bounds**, not scores.

## 4. What round 2 must do (gap not closed)

1. **Human-browser registry completion** (the three
   legs this runtime could not execute): CTIS UI
   search for R1–R4 with EUCT numbers + screenshots/
   exports filed; ANZCTR keyword search for R1–R4
   (ACTRN list or explicit zero per term); ChiCTR
   keyword search incl. Chinese terms for OTOF AAV /
   EA0010 and a direct check for an EA0010 ChiCTR
   counterpart. Until then every synthesis must keep
   "(bounded search, 2026-11-02, EU CTR legacy +
   ClinicalTrials.gov + PubMed; CTIS-UI/ANZCTR/
   ChiCTR keyword searches not executed)".
2. **ANI sweep completion:** screen the CTgov ANI
   term set beyond page 1 with device-specific terms
   (penetrating / intraneural / Utah array auditory)
   before any ANI human-trial absence sentence.
3. **EA0010 watch:** re-pull NCT07752888 at each
   generation; if results post, extract as a
   single-subject safety/feasibility record only —
   Q0-A zoning still requires the §2.2 comparator
   design (T2 established-implant animal study
   remains the decider specified in Q0-verdict).
4. **Q0-P decider unchanged:** prospective patency
   n/N by time band with pre-stated blinded access
   definition (Q0-verdict § ranked gaps). Reimplant
   insertion-success series (Sterkers-type) may
   inform its feasibility assumptions but must never
   be entered as patency %.
5. **Wording fixes owed in Gen 0/1 files** (human
   freeze decision, not made here): re-bound
   candidate-C "no adult FIH" to optogenetic FIH
   given NCT05110183; replace any "no human post-CI
   AAV study" phrasing with the §2.5 bounded
   sentence; keep all other absence claims in the
   §4.1 bounded form. Embase remains unsearched.

## 5. Reproducibility (inspected URLs, 2026-11-02)

- PubMed: `eutils.ncbi.nlm.nih.gov/entrez/eutils/
  esearch.fcgi?db=pubmed&term=<§1.2 string>&retmode=
  json` (counts: N-Q0-1a 4; N-Q0-1b 5; N-Q0-2 23;
  N-Q0-3a 2; N-Q0-3b 17) + `efetch.fcgi?…&rettype=
  medline&retmode=text` for all screened abstracts.
- EU CTR: `clinicaltrialsregister.eu/ctr-search/
  search?query=<term>` via `web_fetch` for OTOF,
  otoferlin, optical+cochlear, optogenetic,
  neurotrophin, neurotrophin+cochlear,
  auditory+nerve, auditory+nerve+implant,
  cochlear+implant.
- CTgov API v2: `clinicaltrials.gov/api/v2/studies/
  {NCT07752888,NCT05901480,NCT05788536,NCT06370351,
  NCT05110183}` (full records) + term queries
  `OTOF+AAV` (3), `OTOF` (15), `optical+cochlear+
  implant` (6), `optogenetic+cochlear` (0),
  `neurotrophin+cochlear` (0),
  `auditory+nerve+implant` (101, page-1 screened).
- ICTRP mirror: `trialsearch.who.int/Trial2.aspx?
  TrialID=ChiCTR2200063181`. ANZCTR access proof:
  `anzctr.org.au/Trial/Registration/TrialReview.aspx?
  id=23330&isClinicalTrial=True`.
- Failed routes (do not re-try unchanged): CTIS UI
  rows, `/ctis-public-api/search` (403), ChiCTR
  direct (405), ICTRP `Search.aspx` (error page),
  ANZCTR `TrialSearch.aspx` (JS/Cloudflare),
  EU CTR via curl (WAF reject).

*No DOI, PMID, registry number, N, or percentage in
this file was invented. Registry target/actual
enrollment counts are reported as posted and are
never treated as outcome data. Future-dated registry
milestones are posted estimates, not results.*


