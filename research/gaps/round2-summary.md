# Gap attacks round 2 — summary, stop-counter, and the win path

> **Requested route:** xhigh synthesis (Sol 6.1 requested).
> **Actual runtime model:** `muse-wonder-full-1.0`, disclosed
> per GOAL §9 rule 3. **Date:** 2026-11-02. **Inputs:** the
> three round-2 attack files (`round2-pdf-labels.md`,
> `round2-A1-fix.md`, `round2-cells-stress.md` +
> `round2-unrowed-cells.csv`), `round2-skeptic.md`
> (independent re-derivations: 2 PDFs re-extracted MD5-exact,
> A1 v2 re-run, 48-cell recount, `gate_table.py` join test),
> `round1-summary.md` (counting rule + round-1 ledger),
> GOAL §§5.2/5.3/6/7/9/11/12 + Appendix A,
> `Step5-decision-no-winner.md` §§1–6, both gate matrices,
> `Step1-pin-summary.md` §§4–5 (U01–U18, amendments A1–A6),
> `freeze-checklist.md` §6 (roster H-1…H-8), `STATUS.md`.
> Agent synthesis only; human dual extraction still PENDING.
> This file decides no gate, edits no earlier file, and makes
> no PASS, promotion, "stress survived", or ≥90% claim.

## 1. Headline

Round 2 filed **three attacks, changed zero gate cells, zero
verdicts, and zero survivors** — and the skeptic proved the
zero end-to-end: `adapt_extraction.py` → `gate_table.py` on
extraction_v1 (185 adapted rows) and on v1 + the 48 new rows
(233) emit **byte-identical** matrices, each reproducing the
filed `gate-matrix-gen0.md` exactly (0 PASS; FAIL only at
A-G6, B-G6, C-G4, C-G6, D-G4, E-G5, E-G6; G3b BLOCKED
everywhere). What round 2 actually bought is paperwork
honesty, in full: four label qualifiers retirable at the next
human pass (Otarmeni single-source, MED-EL mirror-provisional,
AB unverified, WHO located-not-inspected); one hoped-for input
proven absent (the Seyyedi–Nadol rubric is verbal anchors
only — no grade→thickness map exists in that source); the A1
model repaired to v2 with its verdict honestly unchanged
(UNEVALUABLE; direction only on the 15 case-grids run,
magnitudes not grid-converged, Shannon k bracketed +3.00 with
the primary unpinned); 48 previously invisible Level-1 cells
now rowed-as-INSUFFICIENT (never quote this as Level-2
completeness — the ≈527 Level-2 reads remain mostly unrowed);
and the C–H stress template filled for 36 candidate-reads,
36/36 flip questions UNPINNABLE for a named missing input
each. Nothing reaches the Step 3 PASS bar (≥Moderate GRADE
*and* Appendix A minimum tier, §5.2/§5.3; inventor-lab
single-source starts one GRADE lower, G1 needs non-inventor
replication; agent-only verification banned for gate-deciding
claims, §9; gates never amended retroactively within a frozen
generation, §12). Step 5 no-winner stands unchanged.

## 2. Attacks completed per promotion-blocking gap (§7 rule 5b count)

Counting rule: round-1-summary §2, unchanged — one *completed
independent attack* = one filed attack executed against that
gap; a file addressing two gaps counts once toward each; a
partial attack counts as 1, flagged. Skeptic passes are
falsification of attack files, **not** attacks, and are never
counted (neither round's). Gaps are Step 5 §6 items 1–8.
Round-2 attack files: `round2-pdf-labels.md` (PDF),
`round2-A1-fix.md` (A1), `round2-cells-stress.md` (CS).

| Gap (Step 5 §6) | After R1 | Round-2 increment | Now |
|---|---|---|---|
| 1. Human gates (dual extraction, freeze, roster H-1…H-8) | 0/2 | **+0.** PDF does the re-reads as agent *pre*-extraction and expressly disclaims gap 1 (§8.6); an agent re-read is not a human gate | **0/2** |
| 2. G3b co-design (B01) | 0/2 | +0. Untouched; no instrument, no MCID exists | **0/2** |
| 3. P0 denominator + Appendix D | 1/2 | +0. PDF's WHO Table 1.3 is U02 paperwork (adult bands; the table itself bars intervention use); no by-ear cross-tab, P02 decision, or D1–D4 denominator moved. D1 stays: documented ear-average 810, better-ear count UNPINNABLE, Fréchet [0,804] | **1/2** |
| 4. Q0 decider data | 1/2 partial | +0. PDF verifies the Q0-L *label* fact twice over (USPI §1 "no prior cochlear implant in the same ear"; §4 "None") — a RECORD fact, never gate evidence. No patency % (Q0-P) and no post-CI AAV estimand (Q0-A) exists in any inspected source; CS U2/U3 add a tissue-% distribution, not the patency estimand | **1/2 partial** |
| 5. Frozen absolutes/margins + Step 1 A1–A6 | 0/2 | +0 *as an attack*. Inputs arrived (label minima MED-EL ≥7 mo / AB ≥12 mo; Seyyedi rubric shown numeric-free) but no absolute, margin, or amendment was pinned: U09/U16 baselines, U10/U11 instruments/absolutes, U13/U17 margins all still missing, which is exactly why CS §2 returns UNPINNABLE by construction | **0/2** |
| 6. A1 addendum / kill test | 1/2 non-evaluable | **+1 whole-gap attack (A1-fix)** — S4 fixes executed: contiguous `excitation_width` (global span co-printed, equal on all 27 profiles), Shannon bracketed, dx 0.125/0.0625/0.03125 series filed (last-step moves −2.9/+4.3/−0.6/−0.8/+8.35 pp, grade-3 non-monotone ⇒ not converged; quote widths only with dx); v2 sweep byte-identical on shared columns. *Plus* +1 documentary sub-attack inside this gap (PDF §7, Seyyedi rubric prerequisite — first attack on that prerequisite; result: input does not exist). Verdict still UNEVALUABLE; A1-fix §6 items 1–8 all stand | **≥2 ✓** (2 whole-gap; 3 counting the rubric sub-attack — threshold met under either count) |
| 7. Search completeness | 1/2 on 2 sub-gaps, 0 elsewhere | Split verdict — see sub-table below | **Mixed** |
| 8. Human-reversible items (B kill D11, A G6 D17, H1 split, P1 I1, ratifications) | 0/2 | +0. Round 2 *queues* more human decisions (CS §1.3/§5, PDF §8) but files no decider attack; every item still awaits the human panel | **0/2** |

Gap 7 by sub-gap (the only honest granularity — gap 7 as a
whole is **not** at ≥2 while any sub-gap sits below it):

| Gap-7 sub-gap | After R1 | Round-2 increment | Now |
|---|---|---|---|
| Full texts owed | 1/2 (`attack-fulltext.md`, 5/9 upgraded) | **+1 (PDF)** — self-declared second independent attack (§8.6), skeptic-confirmed on 2/5 bodies MD5-exact. Attack count ≠ closure: Pinyon 2014 paywalled, Downie blocked, Shannon 1992 primary unread, MED-EL/WHO/Seyyedi not skeptic-re-pulled | **≥2 ✓ (sub-gap only)** |
| Registry completeness (CTIS/ANZCTR/ChiCTR…) | 1/2 partial | +0. No registry search ran in round 2; every absence sentence keeps its bounded form | 1/2 partial |
| D14 — unrowed Level-1 cells | 0/2 | +1 (CS §1): true count **48**, not ~42 (162 cells → 158 triples; v1 199 rows/123 triples, 11 at non-Level-1 addresses, 112 covered, 46 missing + 2 H-G3a modality cells). All 48 filed INSUFFICIENT; invisibility closed at Level 1 only | 1/2 |
| D16 — C–H stress runs | 0/2 | +1 (CS §2): template filled, 36 reads, 0 flips determinable. Re-running it without U13/U17 margins, a candidate rate, U09/U16 baselines, or D1–D4 is **not** a second attack (CS §5) | 1/2 |
| Embase | 0/2 | +0 | 0/2 |

Cross-reference to §7 rule 4's named examples: **Q0
preservation** = gap 4, 1/2 partial, unchanged. **B
tonotopy** = 0/2 (no tonotopy data inspected in round 2;
Pinyon still paywalled; the Seyyedi rubric is a fibrosis
scale, not tonotopy). **AAV re-dosing** = 0/2 (no re-dose
data; Dieter rows U4/U5 are first-exposure T2 rodent, and
G4-AAV presumptive FAIL logic is untouched).

**Answer to "which gaps are now at ≥2": exactly one Step 5
item — gap 6 (A1) — and exactly one sub-gap — gap 7 /
full-texts-owed.** Gaps 1, 2, 5, 8 remain at 0; gaps 3, 4 at
1 (4 partial); gap-7 sub-gaps registries/D14/D16 at 1, Embase
at 0. Reaching ≥2 closes nothing: gap 6 at ≥2 is still
UNEVALUABLE with eight missing inputs, and full-texts at ≥2
still has unread primaries. The count is a stop-rule floor
(§5), not a progress grade and not a budget cap.

## 3. Cells changed — exactly zero (skeptic-adjudicated)

| Object | Changed | Unchanged (exact) |
|---|---|---|
| Gen 0 gate matrix (8 × 7) | 0 | 56 cells: 0 PASS, 7 FAIL, 3 NA, 46 INSUFFICIENT |
| Gen 1 gate matrix (5 × 7) | 0 | 35 cells: 0 PASS, 1 FAIL, 4 NA, 30 INSUFFICIENT |
| Q0 verdict | 0 | UNDECIDABLE-no-data (thresholds patency ≥80%/≤50%; AAV ≥0.80 + ≤10 dB — unmoved, unratified) |
| Kill verdicts | 0 | B retired as specified; A/F/G/H and A1 kills UNEVALUABLE |
| PASS total, Gen 0 + Gen 1 | 0 | **0** |

Per-candidate adjudication is `round2-skeptic.md` §4: eight
plausible change candidates tested, eight fail the Step 3
bar. Closest call, for the record: **Q0-L / G×G4** on the
now-twice-verified USPI §1 fact — still bookkeeping only,
because Q0-L sits INSUFFICIENT in frozen v1, can move only
via a human-frozen extraction_v2 (§9/§12), and G's G4 needs
a patency % no source supplies. The other seven fail on:
label minima are pins not cells (holder re-freeze act);
A1 is T0, never a pass (§5.3), magnitudes unconverged;
stress template has 0 determinable flips and no ≥Moderate
≥major harm signal was extracted; extraction_v2 U1–U5 hit
GRADE/tier ceilings (U1 T3 n=5–6 degraded comparator, G2
PASS needs T4; U4/U5 single-lab T2, allegiance downgrade,
no non-inventor replication); Seyyedi rubric *removes* an
input; WHO bands are non-intervention descriptors; the 48
rows are INSUFFICIENT by construction (and §1's matrix
identity proves they move nothing).

Bookkeeping proposed in round 2, **none applied, none
touching a gate cell** (cumulative with round-1-summary
§3's six unapplied items): PDF §8 items 1–5 (retire three
qualifiers + Otarmeni single-source with FDA 16-pp.
pagination and the §1-vs-§4 correction; U02 WHO locator;
N4/V05 rubric reworded to "no quantitative rubric exists;
physical mapping is a holder pin"); CS §3 extraction_v2
U1–U5/U3b (+U6-optional) effect/N updates on 6 existing
rows, with Pfingst 2015 (PMID 26209185) and Keppeler 2020
(32718992) correctly *excluded* — both have zero v1 rows,
so filing them is a human new-row decision; CS §1.3's five
judgment calls queued for reversal-or-ratification (E
temporal windows 48-vs-47, G2-music W2 INSUFFICIENT-vs-NA,
G4-AAV Level-2 status, H pooled-row rule, F/H G5 ALL-vs-W0)
plus adopt-or-leave on the 11 non-Level-1 v1 triples; A1
quoting discipline (widths only with dx; contiguous width
quoted only while global span is co-printed; "direction
robust" scoped to the 15 case-grids — the grade-3/0.25 mm
artefact case was not refined).

Survivor set after round 2 — identical to Step 5 and
round 1: non-promoting survivors A, F, G, H with Gen 1
children A1, F1m, Ga, H1, P1; C and D Track-R watch
(never promotable for infants); E parked; B retired. C0
remains untested; `frozen_bilateral_eCI_v1` remains the
retained *proposed* pin; no Track-P candidate is frozen.

## 4. Is Gen 2 justified? No.

Same stated test as round-1-summary §4 — Gen 2 designs are
justified only if the survivor set or a verdict changes.
Round 2 supplies neither (§3 is zero in every row, now
pipeline-proven rather than argued). Every Gen 2 trigger
named in round 1 was checked against round-2 output and
none has occurred: no human re-freeze reversing a kill or
redefining D1/P02; A1 documentary inputs not pinned (§6
items 1–8 stand — round 2 *added* two documented blockers,
unresolved Shannon basis and unconverged magnitudes); no
first Q0 estimand data (a label fact is not an estimand);
no G3b instrument. A Gen 2 now would recombine the same
survivors on the same evidence that made every Gen 1 child
tie its parent cell-for-cell, with no new evidenced
interface (§7 rule 3) and no newly evaluable kill test.
Continuation is **human gates + primary evidence (§6), not
a design generation.** Spending Gen 2 anyway would also
dishonestly advance the §5(b) generation counter — see §5.

## 5. Updated stop-counter (§7 rule 5)

| Stop condition | Status after round 2 |
|---|---|
| (a) Track-P candidate frozen for handoff | Not met. Structurally impossible at v1 (G3b BLOCKED, human extraction pending, pins unfrozen); 0 PASS cells |
| (b) Two consecutive generations, no lexicographic improvement **and** all promotion-blocking gaps ≥2 attacks | Not met on **either** conjunct. Generation conjunct: **1/2**, unchanged (Gen 1 tied Gen 0; no Gen 2 ran, §4 says running one is unjustified, so the counter cannot honestly advance). Gap conjunct: **1 of 8 items** (gap 6) **+ 1 sub-gap** (gap-7 full-texts) at ≥2; the rule needs *all* — gaps 1/2/5/8 at 0, 3/4 at 1, gap-7 remainder at 0–1, B-tonotopy and AAV-re-dosing at 0 (§2) |
| (c) Budget exhausted (labelled *partial*) | Not stated by the holder; rule unarmed (no budget values set, freeze-checklist §5); not met |
| Generation clock (max 4, non-promoting survivors, no new external evidence) | **1/4** (Gen 1). Gap rounds do not move it |

**Stop-counter summary: 0 of 3 stop conditions met.**
Round 2 moves only the gap conjunct of (b), from "0 gaps at
≥2" to "1 item + 1 sub-gap at ≥2" — real but nowhere near
the all-gaps threshold, and the two gaps that block every
PASS by construction (1: human gates, 2: G3b) are still at
**zero**, where agent rounds cannot move them at all. This
is not a §12 abandonment state; it is the Step 5 state plus
two spent attack rounds. Discovery remains unstoppable
under (b) and unpromotable under (a) until §6 happens.

## 6. THE WIN PATH — every remaining action that could ever produce a PASS / promotion

**Premise, stated once and binding on everything below:**
there is no agent step left on this path. Two rounds have
shown agents can retire qualifiers, row invisible cells,
repair models, and prove zeros — and cannot satisfy §9
human dual extraction, cannot co-design G3b, cannot freeze
pins, cannot set margins, and cannot generate T2–T4 primary
data. Every action below is owned by the **holder**,
**stakeholders** (Deaf-community + parent reviewers, roster
H-5/H-6), or **named human experts/labs** (H-1 pediatric
otology, H-2 auditory neuroscience, H-3 trial/biostatistics,
H-4 regulatory, H-7 independent extractor, H-8 independent
co-approver — freeze-checklist §6; all slots currently
PENDING/unnamed). "Win" also needs its honest ceiling:
promotion under GOAL §11 Step 5 means *freezing one Track-P
survivor (A/F/G/H lineage only — C/D/E are Track-R and can
never be promoted for infants) as a study-design handoff*
(animal protocol and/or adult-feasibility sketch, §10
adult-first staging) — never infant first-in-human from
literature, and never a ≥90% claim, which §5.1 reserves for
a later frozen candidate on prospective paired human (or
validated large-animal) data under a pre-registered analysis.
Steps are ordered by dependency: each is necessary; skipping
or reordering W1–W5 makes later PASSes illegitimate, and W6 is
where PASS-grade evidence can first come into existence (each
W6 study itself pre-registered before enrolment/data; W7 then
freezes the generation before it is scored).

**Step W1 — Holder funds and staffs the human path**
*(owner: holder; §9/§12).* Set the budget + calendar bound
per generation (currently unstated — until set, stop rule
(c) is unarmed and no lab work can be commissioned); recruit
and name, with conflicts disclosed: H-1…H-8, the G3b
co-design panel, and a per-generation analysis owner. The
holder co-approves freezes but never sole-scores (personal-
stake COI, §1.1/§12). *Why agents cannot:* budget, consent,
and accountability are not delegable to a model; unfilled
roster = no freeze by rule (protocol §9: tie or missing
quorum = no freeze). *Unlocks:* everything below has a
legitimate decision-maker.

**Step W2 — Stakeholders co-design G3b and ratify the
conventions** *(owners: stakeholders H-5/H-6 with H-1/H-2/
H-3; gaps 2 + 8).* Elect one of the three divergent G3b
protocols (Step 1 amendment A1c), then deliver the B01
deliverable: a named family QoL/autonomy instrument (W1–W3)
+ MCID + NI margin, committed by re-freeze, prospective
only. In the same elicitation act, ratify-or-replace every
invented convention that currently caps scoring at
sensitivity-only (amendment A4): G1 anchor 8 / PASS ≥12 (P),
≥16 (R) with 4/10/16 sensitivities; G2 ≥3 dB, quiet −5 pp;
G3a +0.4/−0.2 SD; G6 disparity caps 5 pp/1.25×; G4 ≥1-grade
FAIL; the §7 lexicographic fitness order; the §6
acceptable-added-risk trade-off rule (needs G3b NI); and Q0
thresholds (H-1/H-2/H-3 + stakeholders, majority + written
dissent preserved). *Why agents cannot:* MCIDs and trade-offs
are values held by Deaf people and families, not quantities
extractable from PDFs; §10 bars assuming them. *Unlocks:*
G3b cells become scoreable at all — until this step,
promotion is impossible *by construction* whatever else
improves (§4.2; Step 5 §1 blocker 1).

**Step W3 — Independent human dual extraction + error audit**
*(owner: H-7, independent of holder or externally audited
if holder-extracted; gap 1; §9).* Independently re-extract
every load-bearing/gate-deciding row (Step 0 bibliography,
extraction_v1's 199 rows, both gap rounds) with a sampled
error audit and reported error rate; LLM/agent rows remain
pre-extraction until the `+human:H-7` form lands. Named
visual/licensed re-reads still owed inside this step:
Pinyon 2014 (paywalled; 7 v1 rows' Ns), Downie 2020 +
genuine correction contents, Shannon 1992 *IEEE TBME*
primary (unit basis — A1 §6 item 7), CDC HSFS rotated
labels, Sloan-Heggen/GeneReviews tables, and the three
round-2 bodies the skeptic did not re-pull (MED-EL S134
byte-identity, WHO Table 1.3, Seyyedi XML). Same act
disposes of the queued bookkeeping: round-1 §3's six items
+ round-2 §3 above (PDF §8.1–5; extraction_v2 U1–U6
adopt/reject; new-row decisions for Pfingst 2015/Keppeler
2020 incl. figure reads; CS §1.3 judgment calls; the 48
rows' admission into extraction_v2). *Why agents cannot:*
§9 bans agent-only verification for gate-deciding claims as
circular — this is the binding reason round 2 moved zero
cells (skeptic §4). *Unlocks:* verified inputs that a freeze
may legitimately score.

**Step W4 — Holder + co-approver re-freeze (Appendix A v2 /
extraction_v2 / baseline v2)** *(owners: holder + H-8, on
H-1…H-7 advice; gaps 5 + 8; §12 — prospective only, v1
matrices never retro-edited).* One signed act must land:
Step 1 amendments A1–A6 (cross-file reconciliation X1–X4;
cite-or-UNPINNABLE the U11 instruments — PLS-5/CELF/spoken
CDI/IT-MAIS/LittlEARS/HINT-C, ASL >73 mo, pediatric CAMP;
per-cell labels; threshold governance; tier downgrades;
GOAL text fixes); the missing absolutes and margins without
which gates cannot PASS even with perfect candidate data —
U10 frozen G2/G3a absolute ranges, U13 P0 per-harm rates +
every G5 NI margin + true 90th-percentile stresses, U17 G4
numerics (residual-hearing/SGN/patency margins; grade→
physical-thickness pin now that Seyyedi is known verbal-only),
U09/U16 frozen burden/non-use baselines, U01/U04–U06 ⇒
D1–D4 denominators (requires W6e data or the P02 redefinition
decision below); the comparator decision (do verified label
minima — MED-EL 7 mo, AB 12 mo, Cochlear 9 mo — trigger a
comparator v2?); the P0 fork (child-level by-ear cross-tab
via CDC EHDI/state microdata request, *or* a flagged P02
amendment redefining D1 as the HSFS ear-averaged convention —
holder decision, never silent); D/HH-Plus definition; and
the human-reversibles (B kill lenient reading D11, A G6
D17, H1 mutation split/re-log, P1 interface-I1 rewrite).
Resurrecting B additionally requires a *new* candidate
(declared branch + inspected kinetics + frozen tonotopy
margins). *Why agents cannot:* freezing is a signature act
with a named co-approver; margins are stakeholder/expert
judgments over registry rates, not extractions. *Unlocks:* a
freezable ruler — PASS becomes *evaluable*, not yet earned.

**Step W5 — Close the human-only search remainder**
*(owners: H-7/experts with licensed + browser access; gaps
4/7).* Embase (if licensed — access gap disclosed if not);
CTIS-UI, ANZCTR, ChiCTR keyword searches with filed exports;
ANI ClinicalTrials.gov sweep beyond page 1 with device terms;
NCT07752888 (post-CI AAV, n=1) re-pulled each round — design
only until results post; and a holder decision on Level-2
rowing (≈527 reads) and `gate_table.py` C/D/E runs (D15).
Until done, every absence claim (incl. C's no-adult-FIH G6
FAIL basis) keeps its bounded form. *Why agents cannot:*
these routes need licensed databases and interactive UIs
this runtime cannot execute (round-1 file documents the
failures). *Unlocks:* unbounded absence claims; removes the
last "searched-only-where-cheap" discount on narrative
confidence (§5.2).

**Step W6 — Generate the missing primary evidence at
Appendix A tiers** *(owners: named external labs/trialists
under H-1…H-4 oversight; funded at W1; each study
pre-registered before enrolment/data are seen).* This is the long pole and
the only step that can create a PASS: literature, models,
and re-extraction cannot, because the binding tiers are
T4 (pediatric human) for G2/G3a/G3b PASS, T2+T4 components
for G4/G5, and G1 needs non-inventor replication (§5.2/5.3,
App. A). Named workstreams, each tied to the cells it
could ever move:

- **W6a. Q0 deciders** (gap 4; designs Ga/Q0 in Step 5 §5):
  a T2 established-implant AAV-delivery study in a
  fibrosed-implant model (retention ≥0.80 + ≤10 dB estimand)
  and a prospective scala-patency n/N by time-since-implant
  band under a pre-stated blinded access definition
  (≥80%/≤50% thresholds). Reimplant insertion-success series
  must never be entered as patency %. *Moves:* Q0 verdict,
  hence G×G4 and every sequencing claim.
- **W6b. A1/A kill test made evaluable, then run** (gap 6):
  first the documentary pins (W4-dependent): holder-named
  array + manufacturer per-contact charge-density limit +
  contact areas (human-extracted), pre-stated safety-margin
  divisor, named-device battery floor, growing-geometry
  ages/dimensions, Shannon primary unit pin (W3), pre-stated
  grid-convergence criterion + fine-grid runs incl. the
  grade-3/0.25 mm case, localized-sheath geometry — then
  code + thresholds committed *before* outputs (W7). Even a
  clean in-silico pass is T0 (mechanism only); G1 movement
  needs the T2 fibrotic/growing-cochlea result at safe
  charge vs the named frozen array, non-inventor replicated.
- **W6c. Candidate staged evidence, adult-first** (§10:
  adult feasibility → older children → infants; ethical
  comparators only — unilateral add-on/sequencing/standard-
  CI-controlled, never delayed-CI control; rescue-to-CI
  criteria; DSMB; consent/assent): per survivor, linked
  W0/W1 mechanism + W2/W3 downstream cohorts (§5.3 causal
  chain) measuring G1 spread/ripple head-to-head, G2
  same-test SRT vs concurrently measured frozen cohort,
  G3a modality-stratified language on W4-cited instruments,
  G3b on the W2 instrument, G4 residual hearing/fibrosis/
  SGN/patency vs same-model comparator, G5 per-harm rates
  against W4 margins (surviving *each* §6 stress at true
  90th percentiles), G6 coverage/burden vs W4 baselines.
  Pathway survivors' prioritized designs already exist as
  paper (Ga decision-time comparison first — the direct C0
  test; H1 encouragement; F1m concurrent audibility/time-
  to-CI; P1 interfaces after I1 rewrite) — W6 is running
  them, not redesigning them. Track-R C/D/E advancement
  criteria (adult FIH; replicated large-animal restoration;
  adult human feasibility) live here too but lead at most
  to watch-list movement, never infant promotion.
- **W6d. B-tonotopy / AAV-re-dosing watch** (rule-4 gaps at
  0/2): no search creates this data; only new T2 tonotopic-
  order results and post-exposure re-dose efficacy (capsid-
  switch/non-viral) count. Do not spend rounds re-proving
  absence.
- **W6e. Epidemiology primaries** (gap 3): CDC EHDI/state
  by-ear microdata (or W4's P02 decision), P0-like cohorts
  for U04 etiologic and U05 anatomic fractions, registry
  extractions for U09/U13/U16 — feeding D1–D4 so any G6
  coverage % can exist.

*Why agents cannot:* agents run no animals, enroll no
children, hold no IDE/BLA path, and produce no GRADE-raising
replication; every number above must be measured in the
world. *Unlocks:* the first cells that can legitimately
read PASS (or FAIL on measured harm — a win-path step that
kills a candidate cleanly is still progress the loop is
designed to buy).

**Step W7 — Freeze the new generation before scoring it**
*(owners: analysis owner + holder/H-8; §7 rules 1/7, §11
Steps 2–3 rerun honestly).* Pre-register candidates
(Appendix B complete; Gen 2 becomes justified *here*, on
W6-changed evidence or W4-changed verdicts — and only here),
protocol + search strings, held-out manifest v2 (validation
set non-empty for the first time: later/independent-lab
studies, partitioned by study/date/species), extraction_v2
schema, freeze checklist signed (freeze-checklist §6 rule:
candidates reviewed, A1–A5 landed or waived-in-writing,
scorer tested, holder + H-8 signatures, analysis owner
named; H-1…H-7 + G3b panel additionally required for any
freeze-*for-handoff*) — all committed before validation
evidence is opened. Post-freeze edits = new candidate.
*Why agents cannot:* the checklist's force is the human
signatures and the unopened-evidence discipline behind them.

**Step W8 — Human-expert decision: freeze-for-handoff or
recorded no-promotion** *(owners: H-1…H-6 expert panel —
LLM judges triage only; holder + H-8 co-sign; §9/§11
Step 5/§12).* Score the frozen generation deterministically
(`gate_table.py` + adapter, already built and diff-clean),
adversarially review, then decide. Promotion requires, for
one Track-P candidate, *jointly*: PASS on every applicable
gate (device: G1–G6 incl. G3b; pathway F/G/H lineage: G1 NA
pre-declared + G2–G6 PASS) at ≥Moderate GRADE and App. A
tier, G4/G5 no veto, each §6 per-harm stress re-scored
without a verdict flip on ratified margins (GOAL §6 wording:
promotion must survive each stress), fitness order as
ratified at W2 — with dissent
preserved verbatim and any G4/G5/G3b dissent answered in
writing before promotion. The deliverable on success is the
study-design handoff (animal protocol / adult-feasibility
sketch) + adoption test (§5.1: a named external group
commits to run/fund it — currently not met, not claimed).
On failure: no-promotion with killing evidence, survivors
carried under the 4-generation clock, and — only with W6
evidence in hand — an honest Gen 2. Terminal honesty:
if W8's panel judges handoff designs non-viable, or Q0 +
scoring show frozen/evolving-standard dominance, or W1
budget exhausts without a survivor, §12 abandonment with
full logs ("keep frozen") is a *successful* loop outcome,
not a failure to be edited around.

What is deliberately **not** on the win path (agent-doable
but win-irrelevant, stated so no future round mistakes it
for progress toward PASS): further qualifier retirements,
Level-2 rowing for its own sake, stress-template re-runs
without W4 margins, A1 refinements without W6b pins, Gen 2
designs before W7, and any rewording of a gap as a new
attack (§7 rule 4 `seen`-set). Agents remain useful inside
W3/W5/W7 as pre-extractors and mechanics under the named
humans — never as substitutes for them (§9 rule 2).

## 7. Reproducibility

This synthesis introduces no new external number. Every
value traces to: `round2-pdf-labels.md` (§§2–9; PDFs:
Otarmeni USPI `fda.gov/media/192098` 1,610,337 B MD5
`512657d0…` 16 pp.; MED-EL S134 605,138 B `5e67120f…`;
AB S167 672,091 B `790d0b93…`; WHO 8,435,712 B `b7e9bd95…`;
Seyyedi XML 126,668 B `a70bb077…`), `round2-A1-fix.md`
(+ `a1_model/` v2: `results.csv` MD5 `30cd31ce…` untouched,
`results_v2.csv` `b9ec23c5…`, `convergence.csv` 15 rows;
10/10 tests), `round2-cells-stress.md` +
`round2-unrowed-cells.csv` (48 rows × 14 cols, all
INSUFFICIENT; C12 D12 E11 H4 A3 B3 F2 G1 — re-parsed and
confirmed in this session), `round2-skeptic.md` §§1–5 (its
own re-extractions, model re-runs, recount, and the
byte-identical matrix join), `round1-summary.md` §§2–6,
`Step5-decision-no-winner.md` §§1–6,
`Step1-pin-summary.md` §§4–5, `freeze-checklist.md` §6,
both gate matrices (cell totals counted from the files),
GOAL §§5–7/9–12 + Appendix A, and `STATUS.md`. Skeptic
scratch in `/tmp/skep2/`; round-2 children scratch in
`/tmp/` per their §reproduce sections. `git status` at
writing: round-2 `a1_model/` v2 edits modified, round-2
deliverables untracked — no frozen, scored, or round-1
file was touched by round 2 or by this summary.

*Unresolved: everything §6 lists, in that order. No gap is
closed (two counts reached ≥2; zero gaps closed), no cell
is PASS, no candidate is promoted or newly killed, C0 is
still untested, and the next move belongs to the holder
(W1), not to another agent round.*

