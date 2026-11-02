# Gap attacks round 1 — summary and stop-counter update

> **Requested route:** xhigh synthesis. **Actual runtime model:**
> `muse-wonder-full-1.0`, disclosed per GOAL §9 rule 3.
> **Date:** 2026-11-02. **Inputs:** the four files in
> `research/gaps/attack-*.md`, `research/gaps/gap-skeptic.md`
> (S1–S4, independently re-executed), GOAL §7 rules 4–5,
> `research/Step5-decision-no-winner.md` §§1–2, 6,
> `STATUS.md`. Agent synthesis only; human dual extraction
> still PENDING. This file decides no gate, edits no earlier
> file, and makes no PASS, promotion, or ≥90% claim.

## 1. Headline

Round 1 spent **one attack each on four gaps and changed
zero gate cells, zero verdicts, and zero survivors.**
Three attacks survived skeptic falsification intact
(P0 denominator, PMC full-text, registries/Q0); the fourth
(A1) survived its verdict but not its numbers. Nothing in
round 1 reaches the Step 3 PASS bar (≥Moderate GRADE at
Appendix A tier + human dual extraction + frozen pins +
G3b PASS). Step 5 no-winner stands unchanged.

## 2. Attacks completed per promotion-blocking gap (§7 rule 5b count)

Counting rule applied here: one *completed independent
attack* = one filed attack executed against that gap
(2026-11-02). The skeptic pass is falsification of the
attack files, **not** a second independent attack on any
gap, and is not counted. A file addressing two gaps counts
once toward each; a partial attack counts as 1, flagged.
Gaps are Step 5 §6 items 1–8 (the operative list; GOAL §7
rule 4's examples — Q0 preservation, B tonotopy, AAV
re-dosing — are cross-referenced at the end).

| Gap (Step 5 §6) | Attacks completed | Round-1 file and result |
|---|---|---|
| 1. Human gates (dual extraction, freeze, roster) | **0 / 2** | None possible by agent. All round-1 output is agent pre-extraction. |
| 2. G3b co-design (B01) | **0 / 2** | Untouched. G3b remains BLOCKED; every G3b cell INSUFFICIENT. |
| 3. P0 denominator + Appendix D | **1 / 2** | `attack-P0-denominator.md`: HSFS table read; 810 is an ear-averaged counting convention (exceeds the 804 both-ears-≥71 logical maximum), P0 cell stays UNPINNABLE. Skeptic S1 UPHELD; rotated type labels directly extracted, so one in-file caveat is retirable. |
| 4. Q0 decider data | **1 / 2, partial** | `attack-registries-Q0.md`: second search finds no §2.1 patency n/N and no §2.2 post-CI AAV estimand; Q0 stays UNDECIDABLE-no-data. EU CTR legacy + CTgov + PubMed executed; CTIS-UI / ANZCTR / ChiCTR keyword searches not executed. Skeptic S3 UPHELD. |
| 5. Frozen absolutes/margins + Step 1 amendments A1–A6 | **0 / 2** | No attack filed. |
| 6. A1 addendum / kill test | **1 / 2, non-evaluable** | `attack-A1-killtest.md` + `a1_model/`: verdict UNEVALUABLE, upheld. Skeptic S4 downgrades two outputs: §5 Shannon sentence must be withdrawn (nC-vs-µC convention shifts k by +3.00; under its own cited convention k = +0.92…+2.92, not −2.08…−0.08) and §4 width/charge ranges are direction-only (dx 0.0625 probe moves width reduction 46.2% → 34.8%). |
| 7. Search completeness | **1 / 2 on two sub-gaps; 0 / 2 on the rest** | Full texts owed: `attack-fulltext.md`, 5 of 9 rows upgraded, Downie XML and Pinyon OA proven dead by this route (S2 UPHELD on ~25 spot-checked values). Registry completeness: the same registries file as gap 4 (counts once there and once here; neither gap reaches 2). Embase, ~42 unrowed Level-1 cells, C–H stress runs: **0**. |
| 8. Human-reversible items (B kill, A G6, H1 split, P1 I1, ratifications) | **0 / 2** | No decider attack; items await human panel. Full-text Pinyon paywall confirmation does not touch B's retired status (Skeptic §5). |

Cross-reference to §7 rule 4's named examples: **Q0
preservation** = gap 4, 1/2 partial. **B tonotopy** = 0/2
(no tonotopy data inspected; Pinyon 2014 remains paywalled,
Browne 2016 is in-vitro and non-substituting). **AAV
re-dosing** = 0/2 (no re-dose data; Pfingst was pre-implant;
NCT07752888 is n=1 by design with no posted results).

**No promotion-blocking gap has reached ≥2 independent
attacks.** The maximum is 1 (gaps 3, 4, 6, and two sub-gaps
of 7); gaps 1, 2, 5, 8 and both remaining rule-4 examples
are at 0. Note: "≥2" in §7 rule 5(b) is a floor for the
stop rule, not a budget cap — one P0-file phrase
("at most 2") should not be quoted as the rule.

## 3. Cells changed — exactly zero

| Object | Changed | Unchanged (exact) |
|---|---|---|
| Gen 0 gate matrix (8 candidates × 7 gates) | 0 | 56 cells: 0 PASS, 7 FAIL, 3 NA, 46 INSUFFICIENT |
| Gen 1 gate matrix (5 candidates × 7 gates) | 0 | 35 cells: 0 PASS, 1 FAIL, 4 NA, 30 INSUFFICIENT |
| Q0 verdict | 0 | UNDECIDABLE-no-data; sensitivities inapplicable, not failed |
| Kill verdicts | 0 | B retired as specified; A/F/G/H (and A1) kills UNEVALUABLE |
| PASS total, Gen 0 + Gen 1 | 0 | **0** |

Per-cell adjudication is in `gap-skeptic.md` §5 (all G6,
GEN1-A1 G1/G6, C G1, Q0-dependent G4, B any, A G2 — each
"No" with reasons). What round 1 *did* change is paperwork
status only, and none of it is yet applied to any earlier
file. The six legitimate bookkeeping changes for the
human pass are: (1) delete phantom Downie erratum
PMID 33293699; (2) retire five abstract-level /
N-UNVERIFIED qualifiers and the Pfingst B5 downgrade;
(3) retire the CDC rotated-label *inference* caveat
(human visual check still owed); (4) adopt the bounded
registry sentences (NCT07752888 post-CI AAV; candidate-C
FIH read as *optogenetic*, cf. NCT05110183); (5) carry
the D1 two-layer form into the next human re-freeze as a
holder decision; (6) strike or bracket A1 attack §5's
Shannon sentence pending a primary-text unit pin.
Counts: **6 bookkeeping items proposed, 0 applied,
0 gate cells involved.**

Survivor set after round 1 — identical to Step 5:
non-promoting survivors A, F, G, H with Gen 1 children
A1, F1m, Ga, H1, P1; C and D Track-R watch; E parked;
B retired. C0 remains untested (neither confirmed nor
refuted); `frozen_bilateral_eCI_v1` remains the retained
proposed pin; no Track-P candidate is frozen.

## 4. Is Gen 2 justified? No.

By the stated test — Gen 2 designs are justified only if
the survivor set or a verdict changes — round 1 supplies
neither: §3 above is zero across every row. A Gen 2 round
now would recombine or mutate the same survivors on the
same evidence that made every Gen 1 child tie its parent
cell-for-cell, with no new evidenced interface (§7 rule 3)
and no newly evaluable kill test. That spends a generation
without a decision-relevant question.

Continuation is therefore **gap round 2 + human gates
(§6), not a design generation.** Gen 2 becomes arguable
only on a triggering change, e.g.: a human re-freeze that
reverses a kill or redefines D1/P02; pinned A1 documentary
inputs making its kill test evaluable; first Q0 estimand
data; or a G3b instrument existing. None has occurred.

## 5. Updated stop-counter (§7 rule 5)

| Stop condition | Status after round 1 |
|---|---|
| (a) Track-P candidate frozen for handoff | Not met. Structurally impossible at v1 (G3b BLOCKED, human extraction pending, pins unfrozen); 0 PASS cells. |
| (b) Two consecutive generations with no lexicographic improvement **and** all promotion-blocking gaps at ≥2 independent attacks | Not met on **either** conjunct. No-improvement counter: **1 / 2** (Gen 1 tied Gen 0; no Gen 2 has run, and §4 says running one now is unjustified, so this counter cannot honestly advance). Gap-attack counter: **0 gaps at ≥2** (max 1; see §2). |
| (c) Budget exhausted (labelled *partial*) | Not stated by the holder; not met. |
| Generation clock (max 4 for non-promoting survivors without new external evidence) | **1 / 4** (Gen 1). Unchanged by gap attacks. |

**Stop-counter summary: 0 of 3 stop conditions met.**
Discovery is not stoppable under (b), and round 1 does not
move it closer on the generation conjunct at all — only,
by one attack each, on the gap conjunct for gaps 3, 4, 6
and part of 7. This is not a §12 abandonment state; it is
the Step 5 state plus one spent attack round.

## 6. Next attacks, ranked (decision-relevance × tractability)

Human-only items head the list because they block every
PASS regardless of agent work; agent-executable items are
marked. "Attack" here follows §7 rule 4's repeated-
independent-attack discipline — rewording a gap is not a
new attack.

1. **Human dual extraction + visual re-reads (gap 1;
   human).** Independent re-extraction of gate-relevant
   rows; human reads of Downie + genuine correction,
   Pinyon 2014 (paywalled), CDC HSFS labels, Otarmeni USPI
   numbers, MED-EL SSED re-pull, Advanced Bionics label.
   Without this, nothing below can change a cell.
2. **G3b co-design (gap 2; human/stakeholder).**
   Instrument + MCID. Until it exists, Track-P promotion
   is impossible by construction, whatever else improves.
3. **P0 round 2 — change of kind, not more literature
   (gap 3; human/holder).** Child-level by-ear cross-tab
   via CDC EHDI / state microdata request, *or* a holder
   decision redefining D1 operationally as the HSFS
   ear-averaged convention (flagged P02 amendment, never
   silent). Cheap preliminaries: Sloan-Heggen gene table +
   GeneReviews human read; D/HH-Plus definition decision.
4. **Registry round 2 completion (gaps 4/7; human
   browser).** CTIS-UI, ANZCTR, and ChiCTR keyword
   searches with filed exports; ANI CTgov sweep beyond
   page 1 with device-specific terms; Embase if licensed.
   Until done, every absence sentence keeps its bounded
   form. NCT07752888 re-pull at each round (design only
   until results post).
5. **A1 round 2 prerequisites, documentary before
   numerical (gap 6; mixed).** In order: Shannon 1992
   primary-text unit pin (S4a); holder-named array +
   manufacturer charge limit, contact areas, battery
   floor; safety-margin divisor; growing-geometry
   ages/dimensions; Seyyedi–Nadol rubric full text. Only
   then the agent-executable numerics: dx/dy convergence
   series (S4b), contiguous-width fix, localised sheath,
   CG residual flag — followed by commit-before-outputs
   if the test is ever to be evaluable, not exploratory.
6. **Frozen absolutes/margins packet (gap 5; human
   freeze).** U09/U10/U11/U13 values plus Step 1
   amendments A1–A6 reconciliation, and the §3 six
   bookkeeping items, folded into one re-freeze act with
   the gap-8 reversibles (B kill, A G6, H1 split, P1 I1).
7. **Q0 decider *new data* (gap 4; external, slowest).**
   T2 established-implant AAV delivery study and
   prospective patency n/N by time band with a pre-stated
   blinded access definition. Highest relevance, lowest
   tractability; agent work here is design/pre-registration
   only (Ga remains the prioritised design). Reimplant
   insertion-success series must never be entered as
   patency %.
8. **B tonotopy / AAV re-dosing watch (rule-4 examples;
   no agent attack available).** B tonotopy needs the
   paywalled primary read (item 1) and, beyond that, new
   T2 data that do not exist in inspected records.
   Re-dosing needs data no search can create. Both stay
   at 0/2 until external evidence appears; do not spend
   search rounds re-proving their absence.

## 7. Reproducibility

This synthesis introduces no new external number. Every
value above traces to `research/gaps/attack-P0-denominator.md`,
`attack-fulltext.md`, `attack-registries-Q0.md`,
`attack-A1-killtest.md` (+ `a1_model/`), `gap-skeptic.md`
§§1–6 (its own re-executions: CDC PDF re-extraction,
12 PMC XMLs, CTgov/PubMed replays, A1 tests 6/6,
`results.csv` md5 `30cd31ce…`), the Gen 0/Gen 1 gate
matrices, GOAL §7, and `STATUS.md`. Cell totals in §3 are
counted from the two matrix files. `git status` at
writing: only untracked `research/gaps/` — no frozen or
scored file was touched by round 1 or by this summary.

*Unresolved: everything §6 lists. No gap is closed, no
cell is PASS, no candidate is promoted or newly killed,
and C0 is still untested.*
