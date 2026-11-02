# Step 3 adversarial skeptic — Gen 0 scoring (A–H, Q0)

> **Model routing (GOAL §9).** Requested: **xhigh skeptic**. Actual:
> **`muse-wonder-full-1.0`**. **Date: 2026-11-02.** GOAL v2.2.
> **Scope read:** all of `research/gen00/scoring/` (`extract-AB.csv`,
> `score-A.md`, `score-B.md`, `searched-family-log.md`) + the scoring
> files that landed at gen00 root (`extract-CDE.csv`, `extract-FGH.csv`,
> `score-C..H.md`, `Q0-verdict.md`) + candidates/protocol/Q0-thresholds/
> schema as cited. Counts below recomputed by parsing the CSVs
> (#-headers skipped): 167 rows, 120 distinct candidate×gate×window.
> **This file issues no new PASS. Its downgrade list (§9) is binding
> on synthesis.** Human dual extraction + freeze still PENDING;
> everything here and upstream is sensitivity-only screening.
> **G3b: BLOCKED (INSUFFICIENT) all candidates — no Track P promotion.**

## 1. PASS below Moderate / below tier — CLEAN, with a grade-inflation catch

- **Zero PASS rows** in 167 (AB 71, CDE 41, FGH 55). No abstract was
  upgraded to PASS. This part survives falsification.
- **FALSIFIED as printed: the GRADE column.** AB correctly carries
  `UNASSESSED` on all 71 rows. CDE (12 rows) and FGH (15 rows) print
  agent-assigned `Low`/`VeryLow`, and the C–H narratives present them
  in summary tables as "Tier / GRADE" (e.g. C G1 "T2 / Low").
  `extraction-schema.md` §78: agent grades stay UNASSESSED-capped for
  gate purposes until human verification. A synthesis reader quoting
  "Low GRADE" quotes a grade nobody human assigned. **Downgrade D1.**

## 2. Inventor-lab single-source G1 — every G1 signal is one

| Signal | Source | Skeptic finding |
|---|---|---|
| A spread-narrowing | van den Honert & Kelsall, PMID 17552721, N=3, originator lab | Single-source, qualitative, adverse charge cost. Correctly provisional; synthesis may not call it replication-adjacent. |
| B neurite regrowth | Pinyon, PMID 24760189, UNSW inventor lab | Sole primary, no N/numerics in abstract, 2-wk deafness ≠ congenital. Correctly provisional. |
| C tonotopy (×2 rows) | Dieter PMID 32596983 + Alekseev PMID 40721511 | **Two rows, one inventor ecosystem (Moser group lineage).** Printing two PROVISIONAL-SIGNAL rows mimics independent corroboration; it is not. Counts as **one** signal. **D2.** |
| D conversion (×2 rows) | Liu PMID 38103445 + McGovern PMID 38266052 | Both *fail* the candidate's own conjuncts (ectopic/adjacent, no ABR). A "signal" whose inspected content is negative on the deciding criteria is mechanism trivia, not support. Synthesis must not list D among "candidates with signals" without that sentence attached. **D3.** |

No G1 cell has non-inventor replication. None was PASSed — good —
but no synthesis sentence may upgrade any of the above to
"replicated", "converging", or "multi-study".

## 3. Abstract-level upgraded / category errors in PROVISIONAL-SIGNAL

Provisional is the correct cap, but four rows put non-effects in an
effect-shaped verdict, inviting synthesis miscounts:

1. **Q0-L row (FGH): PROVISIONAL-SIGNAL, RECORD/UNASSESSED.** A label
   eligibility fact is not a signal. It must be carried as RECORD
   fact (with A5 human PDF re-read still owed), never counted in any
   "signals found" tally and never as evidence for/against biology. **D4.**
2. **H ASL-CDI (PMID 32180180):** instrument existence in deaf-of-deaf
   norms. Measurability ≠ H effect (narrative says so; the CSV verdict
   still reads as support). Downgrade to INSUFFICIENT-for-effect. **D5.**
3. **G yield (Downie PMID 31827275, 59/106 vs 22/106):** yield ≠
   turnaround/time-to-access; moderate–profound ⊋ P0; design-set;
   errata unchecked. Forbidden as G6/G-pathway support. **D6.**
4. **F P1 (PMID 42194183, VeryLow):** retrospective, wrong comparator
   (unilateral CI), ~27 mo fitting ≠ W0, aided-threshold selection
   hides exactly F1's precondition failure. Mechanism-consistency
   only; forbidden as F1 audibility/time-to-CI evidence. **D7.**
5. **Triple-counting by window:** A (PMID 17552721) and B
   (PMID 24760189) each appear as PROVISIONAL-SIGNAL at W1, W2 **and**
   W3 — one study, three rows. Any synthesis tally of "9 provisional
   signals (AB)" is false arithmetic: distinct studies = A 4
   (1 mechanism + 3 nulls), B 1. Report per-study, collapses to
   INSUFFICIENT at gate level. **D8.**

## 4. G3b non-INSUFFICIENT — CLEAN

24/24 G3b rows INSUFFICIENT (recomputed). All narratives print
BLOCKED. No leakage found. Promotion correctly impossible for every
candidate incl. C0/G. Survives.

## 5. Q0 threshold moved post-hoc — CLEAN on numbers, fragile on search

- Zones in `Q0-verdict.md` match `Q0-thresholds.md` exactly (80/50%,
  0.80/10 dB, sensitivities 70/90, 0.70/0.90, 5/15 dB — verified
  line-by-line). UNDECIDABLE-no-data is the pre-registered outcome,
  thresholds written before scoring. No post-hoc move found.
- **But:** verdict rests on bounded PubMed/CTgov inspection only;
  Embase + EU CTIS/ChiCTR/ANZCTR owed (scorers disclose). Synthesis
  wording must stay "no eligible estimand study found in inspected
  records (2026-11-02)", never "no such study exists". **D9.**
- Madgar 78% (PMID 40052291) correctly excluded as non-patency in
  both Q0-verdict and score-A. Survives.

## 6. Kill criteria — one evasion risk, two judgment-dependent calls

| Candidate | Scorer call | Skeptic verdict |
|---|---|---|
| A spread-at-safe-charge | UNEVALUABLE | Honest. But synthesis must not write "A survives": A is *untested against its kill*, with adverse direction (current cost, −48% battery PMID 36279119, take-home nulls). "Not killed" ≠ "alive and well". **D10.** |
| B lifetime arm | TRIGGERED → killed as specified | **Judgment-dependent.** Scorer's own lenient reading (defer until handoff filed) flips it to pending. Both readings recorded — synthesis must carry the disagreement, not just "B killed". Banned: citing the kill while omitting the sensitivity. **D11.** |
| B tonotopy arm | UNEVALUABLE | Correct: "ectopic branching" + no order metric/denominators kills nothing and clears nothing. |
| C park 2028-11-02 | Not yet triggered | **Date is fictional until freeze exists** (human freeze PENDING; scorer flags day-for-day slide). Synthesis must not print 2028-11-02 without "under assumed freeze date". **D12.** |
| D advance criterion | UNMET | Bounded PubMed only (S-D 517, probe 9, 3 inspected). Correct wording already bounded; synthesis may not shorten to "met by no one". **D9 applies.** |
| E park | 0/3, remains parked | Clean. "Chronic cat 6-mo" REFUTED (PMID 38379760 surgical model) — synthesis must keep REFUTED, not soften to "unverified". Bench numbers (6.3B pulses) stay excluded. |
| F / G / H | NOT KILLED, indeterminate | Logically correct (no concurrent frozen test exists), **structurally evasive if read as endurance**: F/G/H can never be killed by evidence that cannot be generated against unmeasured baselines (U09). Synthesis must say "kill test has never been runnable", not "passed kill check". **D10 applies.** H both arms unevaluable — incl. *not cleared* on post-CI auditory harm. |

## 7. Decision-time / treatment-policy violations — flagged upstream, still live

- F P1 row: retrospective, device-use duration differs by group —
  no decision-time analysis exists (narrative admits). Row stays
  provisional-by-cap only. **D7.**
- G: Downie has no decision origin; CHORD/Otarmeni efficacy is the
  therapy's, not G's routing effect (score-G correct). Synthesis
  crediting G with label outcomes (16/20 etc.) = decision-time +
  attribution violation. **D13.**
- A van Groesen: 13 fitted/9 completed — treatment-policy requires
  the 4 non-completers in-denominator; abstract reporting breaches
  it, direction only weakens A. Correctly handled upstream; keep.
- No row anywhere uses post-decision genotype/results to justify an
  earlier decision. No direct violation entered into a verdict.

## 8. Structural defects synthesis must inherit honestly

1. **Coverage gap (~42 cells).** `searched-family-log.md` enumerates
   162 Level-1 cells and states 130 without starter rows "must appear
   as explicit INSUFFICIENT rows". Delivered: 120 distinct
   candidate×gate×window cells. ~42 pre-registered cells have no row
   at all (distribution: H 11, C/E 12 each vs plans of 16–23).
   Unrowed ≠ INSUFFICIENT-scored. Synthesis may not claim complete
   A–H×gate×window scoring. **D14.**
2. **No `gate_table.py` run evidenced for C/D/E.** AB and F/G/H print
   deterministic matrices (all INSUFFICIENT/FAIL-completeness,
   promoted FALSE); C–E files only state adjudication *requires* it.
   C/D/E gate tables are narrative-only until run. **D15.**
3. **No cost-dictionary stress re-scoring for C–H.** Only A/B run
   S-revision/S-nonuse/S-access/S-surgical (verdict-change: none,
   INSUFFICIENT-proxy-reported — correctly never "stress survived").
   C–H G5/G6 cells are stress-untested; family-log flip table says
   UNPINNABLE, which is a reason, not a run. **D16.**
4. **FAILs are all completeness/staging/presumptive, none measured:**
   A G6 + B G6 (strict reading; scorer admits looser reading flips A
   to INSUFFICIENT — **D17**: print as disputed sensitivity FAIL, not
   hard FAIL), C G6 pre-specified, C/D G4-AAV presumptive (C's rests
   on Low/T2 abstract "virus-mediated" with capsid unasserted — the
   *rule* is pre-registered, the *AAV-use premise* is abstract-level;
   keep "presumptive" in every citation), E G5/G6 staging. No FAIL
   in the set is a ≥Moderate measured harm; synthesis must not
   narrate any as demonstrated danger, nor any INSUFFICIENT as safety.
5. **Split file locations** (AB in `scoring/`, C–H + Q0 at gen00
   root) + validation set = 0 + exploratory-after-seen = YES for
   everything: any synthesis "winner", ranking, or ≥90%/promotion
   language is forbidden on this evidence base regardless of cell
   pattern. FROZEN-by-default is the only defensible headline.

## 9. BINDING DOWNGRADE LIST (synthesis must apply verbatim)

- **D1** All agent `Low`/`VeryLow` grades → read `UNASSESSED`
  (human-unverified) everywhere synthesis quotes GRADE.
- **D2** C G1 = one inventor-ecosystem signal, not two studies.
- **D3** D "signals" = conjunct-failing mechanism reports; never
  listed as candidate support without the failure sentence.
- **D4** Q0-L = RECORD label fact (A5 re-read owed), excluded from
  all signal tallies and from biology claims both directions.
- **D5** H ASL-CDI → INSUFFICIENT-for-effect (measurability only,
  ≤73 mo, deaf-of-deaf norms).
- **D6** G Downie yield forbidden as pathway/G6 evidence.
- **D7** F P1 row forbidden as F1 audibility/time-to-CI evidence.
- **D8** Count provisional signals per distinct study (A 4 incl.
  3 nulls, B 1, C 1, D 0-as-support, F 0-as-support, G 0, H 0),
  never per window-row.
- **D9** All absence claims bounded: "in inspected PubMed/CTgov
  records, 2026-11-02; Embase/CTIS/ChiCTR/ANZCTR unsearched".
- **D10** A/F/G/H kill status = "kill test never runnable /
  unevaluable", never "survived/passed kill check"; H harm arm
  explicitly *not cleared*.
- **D11** B kill printed with its lenient-reading reversal attached.
- **D12** C park date printed only as freeze-assumption-dependent.
- **D13** No Otarmeni/CHORD efficacy number attributed to G.
- **D14** State the ~42 unrowed Level-1 cells; no completeness claim.
- **D15** C/D/E labelled "narrative-scored; gate_table run owed".
- **D16** C–H labelled stress-untested (A/B: no verdict change,
  INSUFFICIENT-proxy-reported).
- **D17** A (and B element-1) G6 FAIL = disputed strict-reading
  sensitivity FAIL; all seven FAIL rows labelled
  completeness/staging/presumptive, none measured-harm.

**Net skeptic judgment:** the scoring never PASSes what it must not,
never leaks G3b, and never moves Q0 — the load-bearing disciplines
hold. What does not hold is presentation arithmetic: inflated grade
labels, window-triplicated and same-lab-duplicated signals,
non-effects in effect verdicts, ~42 missing cells, and
judgment-dependent FAIL/kill calls at risk of hardening in
synthesis. With D1–D17 applied, the honest Gen 0 Step 3 headline is:
**no candidate promotable (G3b BLOCKED), no gate PASS anywhere,
FROZEN retained by default, B killed-as-specified under a recorded
disagreement, every other kill test unevaluable, Q0 UNDECIDABLE-no-data.**
