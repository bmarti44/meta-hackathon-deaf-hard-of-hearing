# Step 3 scoring summary — Gen 0 synthesis (A–H, Q0)

> **Model routing (GOAL §9).** Requested: **xhigh scorer/synthesis**.
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-02**. GOAL v2.2.
> **Authority:** synthesis of agent pre-extraction + skeptic +
> three LLM judges = **triage only** (GOAL §9/protocol §9). Human
> experts decide freezes; human dual extraction, freeze, and the
> H-1…H-8 roster remain **PENDING**. Everything here is
> sensitivity-only screening on design evidence (validation set = 0,
> exploratory-after-seen = YES).
> **Headline (unanimous skeptic + 3 judges, confirmed
> deterministically below): no gate PASS anywhere, G3b BLOCKED for
> every candidate, no promotion (all `promoted FALSE`), FROZEN
> retained by default. No high-confidence win claim is made.**

## 1. What was built and run (commands + observed outputs)

**Inputs read:** `extraction_template.csv`, `extract-AB.csv`,
`extract-CDE.csv`, `extract-FGH.csv`, narratives `score-A…H.md`,
`Q0-verdict.md`, `step3-skeptic.md` (D1–D17), `judge-1/2/3.md`,
`protocol.md`, GOAL §7, all eight candidate FMEA tables.

**Consolidated file:** `extraction_v1_2026-11-02.csv` = template
starter rows (32) + AB (71) + CDE (41) + FGH (55) = **199 rows**.
Adjudication rule: a row verdict was *changed* only where the
skeptic's binding list prescribes it (D1 grade, D4, D5) or ≥2
judges explicitly concur on that row's verdict; every other
dissent is preserved verbatim as `[SYNTH: …]` in the `claim`
field. Applied changes (build log, verbatim summary):

```text
wrote 199 rows -> research/gen00/scoring/extraction_v1_2026-11-02.csv
candidates: A45 B32 F20 G19 H19 C17 D17 E16 Q0-P6 Q0-A4 FROZEN3 Q0-L1
verdicts: INSUFFICIENT170 PROVISIONAL-SIGNAL15 NA-prereg7 FAIL7
grades: UNASSESSED199
```

- **D1 (27 rows):** agent `Low`/`VeryLow` → `UNASSESSED`
  (unanimous). AB already carried UNASSESSED.
- **D5:** H ASL-CDI (PMID 32180180) PROVISIONAL-SIGNAL →
  INSUFFICIENT-for-effect (unanimous).
- **D4:** Q0-L PROVISIONAL-SIGNAL → INSUFFICIENT, carried as
  RECORD label fact, excluded from all tallies (unanimous).
- **E G4-AAV:** INSUFFICIENT → NA-prereg (J1+J3 uphold stated NA:
  no AAV in mechanism; neither evidence gap nor pass).
- **Encoding fix:** D `NA-struct` advance-criterion row recoded
  `G1-spectral` so `gate_table.py` accepts it; verdict unchanged
  (D G1 already INSUFFICIENT; no cell moves).
- **Annotation-only (majority keeps verdict):** D8 window-
  triplication (A PMID 17552721, B PMID 24760189 — count once);
  J2-Diss-1 PROVISIONAL-NULL dissent on A's 3 adult nulls; D2 as
  qualified by J1-DISSENT-1 + J2-Diss-3 on C's 2 rows; D3 +
  J1-DISSENT-2 dissent on D's 2 rows; D7 + J2-Diss-2 dissent on
  F's P1 row; D6 on G's yield row; D17 characterisations on all
  7 FAIL rows (see §2).

**Deterministic run (exactly as commissioned):**

```text
$ cd research/scoring && python3 adapt_extraction.py ../gen00/scoring/extraction_v1_2026-11-02.csv ../gen00/scoring/adapted_v1.csv && python3 gate_table.py ../gen00/scoring/adapted_v1.csv --out ../gen00/scoring/gate-matrix-gen0.md
adapted 185 rows -> ../gen00/scoring/adapted_v1.csv
exit=0
```

185 adapted rows = 199 − FROZEN (3) − Q0-P/A/L (11), which the
adapter skips by design. Adapted verdicts: INSUFFICIENT 171,
NA 7, FAIL 7, PASS **0**. `PROVISIONAL-SIGNAL` collapses to
INSUFFICIENT (`adapt_extraction.py`, GOAL §5.2); sublabels
collapse to G1–G6. Repo tests: `python3 -m unittest` in
`research/scoring` → **Ran 18 tests, OK**. This run also retires
skeptic debt **D15**: C/D/E are no longer narrative-only — their
cells below are `gate_table.py` output. **D16 stands:** C–H
remain stress-untested (A/B only: no verdict change,
INSUFFICIENT-proxy-reported).

**FMEA:** `fmea_v1.csv` built from the eight candidate Appendix C
tables (8 × 18 = **144 harm rows** inspected). **Zero rows carry
a numeric probability band** (`<0.1% / 0.1-1% / 1-5% / >5%`);
every applicable row is UNPINNABLE (A–D) or INSUFFICIENT/no P0
rate pinned (E–H, U13), the rest NA. Per instructions they were
skipped and documented, so the file is header-only and no band
was invented. Verified inconsequential:

```text
$ python3 gate_table.py ../gen00/scoring/adapted_v1.csv --fmea ../gen00/scoring/fmea_v1.csv --out /tmp/gate-fmea.md
$ diff ../gen00/scoring/gate-matrix-gen0.md /tmp/gate-fmea.md
IDENTICAL with/without --fmea (0 numeric-band rows)
```

## 2. Gate matrix — interpretation

Deterministic output (`gate-matrix-gen0.md` §a, worst applicable
window per gate; G3b forced INSUFFICIENT):

| cand | track | G1 | G2 | G3a | G3b | G4 | G5 | G6 |
|---|---|---|---|---|---|---|---|---|
| A | P | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | **FAIL** |
| B | P | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | **FAIL** |
| F | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF |
| G | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF |
| H | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF |
| C | R | INSUFF | INSUFF | INSUFF | INSUFF | **FAIL** | INSUFF | **FAIL** |
| D | R | INSUFF | INSUFF | INSUFF | INSUFF | **FAIL** | INSUFF | INSUFF |
| E | R | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | **FAIL** | **FAIL** |

- **No PASS exists at any anchor, window, or stratum; G3b
  BLOCKED** forces promotion FALSE for all eight (§d of the gate
  file: A/B device — not PASS on G1–G6; F/G/H pathway — not PASS
  on G2–G6; C/D/E watch-list — never promoted for infants). No
  promotion is asserted anywhere in this synthesis.
- **All 7 FAILs are completeness / staging / presumptive (D17);
  none is a measured harm at ≥Moderate GRADE, and no
  INSUFFICIENT may be read as safety.** Strongest-first (J3):
  E G5/G6 (bilateral infant CPA staging) ≈ C G6 (no adult FIH +
  durability + power/heat) > B G6 element-2 (lifetime refill/
  revision count unstateable) > C/D G4 (G4-AAV presumptive,
  gate-collapsed; "presumptive" mandatory) > A G6 (**disputed**
  strict-reading sensitivity FAIL — no numeric timeline; J1/J3
  agree it flips to INSUFFICIENT under the looser reading or one
  stated number). C/D G4 FAIL enters via the G4-AAV sublabel
  collapse; G4 proper is INSUFFICIENT.
- **Provisional signals, counted per distinct study (D8) — the
  only honest arithmetic:** A = 1 mechanism study (PMID
  17552721, originator lab, N=3) + 3 adult null studies (J2
  dissent: never "4 signals"); B = 1 (PMID 24760189, inventor
  lab, 2-week deafness ≠ congenital); C = 0 replications, 1
  inventor programme with 2 subsystem/preparation signals
  (emitter gerbil + opsin rodent/NHP; majority J1/J2 wording),
  0 system-level G1 results; D = 0-as-support (both rows fail
  their own conjuncts — ectopic/adjacent, no ABR); F = 0-as-
  support (D7); G = 0 (D6: yield ≠ pathway); H = 0 (D5
  applied); E = 0. No G1 cell has non-inventor replication; no
  T4 language data exist for any candidate; every mediation
  chain is UNRESOLVED (protocol §7 caps all language claims).
- **Coverage debt (D14) stands.** Merged distinct
  candidate×subgate×window cells = 120 (A–H 117 + Q0 3),
  matching the skeptic; ~42 of 162 pre-registered Level-1 cells
  still have no row. Unrowed ≠ scored INSUFFICIENT; no
  completeness claim is made. All absence claims are bounded
  (D9): *inspected PubMed/CTgov records, 2026-11-02; Embase /
  EU CTIS / ChiCTR / ANZCTR unsearched.*

## 3. Lexicographic rankings (GOAL §7) + sensitivity notes

Deterministic output (§b/§c). Every numeric tie-break input
(`delta_g2_db`, `delta_g3a_sd`, `g1_channels`, `burden_rank`,
G5 aggregate) is **NA for every candidate** — no measured effect
was extractable — so ranks are decided solely by FAIL /
INSUFFICIENT counts, then candidate name.

**Track P:** 1 F, 2 G, 3 H (0 FAIL, 6 INSUFFICIENT each) →
4 A, 5 B (1 FAIL, 6 INSUFFICIENT each). No G4/G5 veto FAIL in
Track P. **Track R:** 1 C, 2 D, 3 E — *pure name order*: all
have `g1_channels` NA and G5 aggregate NA (empty FMEA, §1), so
this ordering carries no evidence content whatsoever.

**D17 sensitivity (run, not asserted).** Flipping A's disputed
G6 FAIL → INSUFFICIENT and re-running gives A: 0 FAIL but
**7** INSUFFICIENT (all 7 gates applicable to a device) vs
F/G/H's 6 (G1 NA excluded) — so A stays rank 4 and the Pareto
set is unchanged. The ranking is robust to the one disputed
FAIL, but for a bookkeeping reason, not an evidential one.

**Evidence-completeness sensitivity (GOAL §7's own warning:
fewest-INSUFFICIENT favours studied incumbents — here it
favours pathways with an NA gate).** Rowed evidence per
candidate (extraction_v1): A 45 rows/20 cells, B 32/21,
F 20/15, G 19/13, H 19/11, C 17/12, D 17/13, E 16/12. The
lexicographic leaders F/G/H are *not* the best-evidenced
candidates — they lead because they never incurred a
completeness FAIL and have one fewer applicable gate, while
having zero measured effects; the most-studied candidates
(A/B) trail only on G6 completeness. **Ranks 1–5 must not be
read as a winner ordering:** on a zero-PASS, zero-measured-
effect, validation-empty base the ranking sorts paperwork
states, not expected child benefit.

**Pareto set (§e, transparency only):** Track P = {F, G, H}
(A/B dominated solely via the FAIL count). Track R = {C, D, E}
— all three non-dominated (C/E: 2 FAIL/5 INSUFFICIENT; D:
1 FAIL/6 INSUFFICIENT; every other objective tied at missing).
Per GOAL §7, ranking/promotion use the lexicographic rule, not
Pareto; nothing here promotes.

## 4. Kill / park / advance verdicts (adjudicated)

| cand | verdict | basis (skeptic + judge majority) |
|---|---|---|
| A | kill **UNEVALUABLE** | Fibrotic/growing-model spread test at pre-stated safe charge has never been run; no charge-density limit exists (C9). Never "survived" (D10); adverse direction is a prior, not a result. J1+J3. |
| B | **KILLED as specified** (lifetime arm ii TRIGGERED) | No branch declared; no kinetics/duration for either branch; lifetime burden unstateable. **Lenient-reading reversal preserved (D11):** defer-until-handoff reading → kill-pending; a human judge may reverse without re-litigating evidence; advancement barred under either reading. J1+J3 uphold TRIGGERED, J2 defers. Arms (i) tonotopy, (iii) stim×outgrowth: UNEVALUABLE. |
| C | park **not yet triggered** | 24-month rule runs from a human freeze that has not occurred; "2028-11-02" only under an assumed 2026-11-02 freeze, sliding day-for-day (D12). Adult optogenetic FIH start: not observed. |
| D | advance criterion **UNMET**; not killed | 0/5 conjuncts met by any inspected record (bounded wording, D9). Criterion-gated watch continues; no calendar date. |
| E | **PARKED, 0/3** | Bench primary ✗, T2 chronic denominators ✗, adult feasibility ✗. "Chronic cat 6-month" remains **REFUTED** (PMID 38379760 = surgical model). Neither retire-for-harm nor clearance is possible without denominators. |
| F | kill **never runnable** (D10) | No concurrently measured frozen pathway; neither conjunct evaluable. F-vib harm uncharacterised both directions. |
| G | kill **never runnable** (D10) | Both arms indeterminate; Q0 UNDECIDABLE neither supports nor refutes the preservation premise. |
| H | both arms **UNEVALUABLE, not cleared** | (a) no encouragement/IV estimate exists; (b) post-CI auditory harm explicitly **not cleared** (Fitzpatrick 2016 controls). |

## 5. Q0 verdict

**Q0 = UNDECIDABLE-no-data** (unanimous; thresholds verified
unmoved against `Q0-thresholds.md`). Q0-P: tissue *presence*
(27/28, 17/17) is not the patency/cannulability estimand;
Madgar 78% (PMID 40052291, hearing preservation) correctly
excluded. Q0-A: the only implant+AAV record is concurrent
(Pfingst PMID 28776202); no post-establishment retention
estimand exists. Q0-L: RECORD label fact only (D4; human PDF
re-read still owed). All Q0-dependent G4 cells read
INSUFFICIENT. Bounded wording (D9) as in §2.

## 6. Survivors for Gen 1 (GOAL §7), recombine/mutate inputs

GOAL §7 STOP conditions are not met (no frozen survivor; gaps
not yet twice attacked). §7's "retire dominated" is *not*
applied mechanically to A: its Pareto domination rests solely
on the disputed G6 paperwork FAIL (§3 sensitivity), which
human judges may reverse — retiring the most-studied device
candidate on that count would encode the artefact §7 itself
discloses. Gen 1 inputs (parents, not winners):

- **A — mutate (one logged change per child):** state numeric
  timeline (+ safe-charge limit) → G6 flips; then run the
  pre-specified kill-test model (fibrotic + growing geometry,
  frozen seeds, battery floor). Non-inventor take-home
  replication vs clinical map is the only G1/G2 route.
- **F, G, H — carry as untested pathway parents:** each owes a
  prospective decision-time, treatment-policy comparison vs a
  concurrently measured frozen pathway (F: W0 audibility dose;
  G: turnaround/time-to-access + gene-first capture, never
  therapy efficacy credited to routing, D13; H: encouragement
  design + post-CI NI). J3-21: available-now *components* ≠
  deliverable *pathway* — never shorten to "deliverable now".
- **Recombination (rule 3 — evidenced interfaces only):** no
  pair has combination data. The only Gen 1-legal joins are
  *sequenced portfolios with a stated interface experiment*:
  a device parent (A) × pathway parent (F/G/H) as a Gen 1
  portfolio with G1-NA disclosed and device G1 stated at
  portfolio level. **B×D remains forbidden** (no T1 co-delivery
  data); B×F is moot (B retired). No slogan cross is proposed.
- **C — Track R watch parent:** thermal-dose inputs are
  *uncomputable* today (threshold ≠ margin); full-text dose
  extraction + adult FIH watch. Park clock starts only at a
  real freeze.
- **D — watch-only:** advancement solely via the 5-conjunct
  criterion; the two marker reports are mechanism inputs, not
  support (D3).
- **E — parked, no Gen 1 child:** re-entry requires all three
  park conditions (bench primary with charge-density limits
  first — the cheapest unlock).

**Retired list:** **B as specified** (kill arm ii; resurrection
= new candidate: declared branch + inspected kinetics ≥5 y or
refill plan + frozen tonotopy protocol + silence census).
Parked (not retired): E. Watch-only (not retired, not
advanced): C, D. Nothing else is retired; nothing is promoted.

## 7. Unresolved gaps, ranked (decision-relevance × tractability)

| # | gap | relevance | tractability |
|---|---|---|---|
| 1 | Human dual extraction + named expert freeze (H-1…H-8) — gates every grade, kill reversal, convention (D11/D17, J-dissents) | blocks all promotion | process act, no new science |
| 2 | G3b co-design (B01) — sole structural bar to any Track P promotion | blocks all promotion | co-design act; human-owned |
| 3 | A numeric timeline + per-contact safe-charge limit (flips G6; makes kill test statable) | decides A's rank + testability | days; stated numbers only |
| 4 | ~42 unrowed Level-1 cells (D14) + Embase/CTIS/ChiCTR/ANZCTR searches behind every absence claim (D9) | bounds all absence/kill wording | extraction labour |
| 5 | A kill-test model run (fibrotic/growing, frozen seeds) | decides A | computation, pre-specified |
| 6 | Frozen instruments/ranges U10/U11 + G5 P0 harm rates U13 + pathway baselines U09 | unblocks G2/G3a/G5 scoring for all | registry/extraction work |
| 7 | C full-text thermal-dose extraction (energy/pulse, duty cycle, ΔT model) | decides whether C G5 is even computable | extraction + modelling |
| 8 | Q0 decider studies (post-establishment AAV; prospective patency n/N by band) | decides G's premise + all Q0-G4 cells | new primary studies (slow) |
| 9 | E bench primary + chronic denominators; B successor kinetics + silence census | decides E re-entry / any B successor | new primary data (slow) |
| 10 | F/G/H concurrent-pathway T4 cohorts; C adult FIH; D large-animal criterion | decides all pathway + Track R advancement | new trials (slowest) |

C–H cost-dictionary stress re-scoring (D16) remains owed as
labelling; for C/D/E no human rate exists for it to move.

## 8. Prohibitions carried into Gen 1

D1–D17 apply verbatim to any downstream text: per-study signal
counting (D8); no corroboration/replication language for any
single-programme signal; Q0-L never a signal (D4); Downie
yield and F-P1 never pathway evidence (D6/D7); no CHORD/
Otarmeni efficacy credited to G (D13); B's kill always printed
with its D11 reversal; C's park date only as
freeze-assumption-dependent (D12); A/F/G/H kills as "never
runnable/unevaluable", never "survived" (D10); H harm arm
printed as *not cleared*; every FAIL labelled
completeness/staging/presumptive (D17); every absence claim
bounded (D9). **No candidate is promotable, no ranking above
is a winner claim, and FROZEN is retained by default.**

*Files: `extraction_v1_2026-11-02.csv`, `adapted_v1.csv`,
`gate-matrix-gen0.md`, `fmea_v1.csv` (all this directory);
build script `/tmp/build_extraction_v1.py`.*
