# Step 4 synthesis — Gen 1 (one recombination round, GOAL §11)

> **Model routing (GOAL §9).** Requested: **Sol 6.1, xhigh**
> (synthesis). Actual: **`muse-wonder-full-1.0`**. Date:
> **2026-11-02**. GOAL v2.2.
> **Authority:** synthesis of agent designs + agent re-score +
> agent skeptic = **triage only**. Human dual extraction,
> freeze, H-1…H-8 roster PENDING. Inputs:
> `research/gen01/` (5 candidates, `fitness-application.md`,
> `README.md`, `scoring/score-gen1.md`, `step4-skeptic.md`),
> Gen 0 gate matrix + `Step3-scoring-summary.md`, GOAL §7/§11.
> Where scorer and skeptic differ, the skeptic's downgrade
> governs (it re-ran everything below).
> **Headline: no PASS anywhere in Gen 1, G3b BLOCKED for all
> five, `promoted FALSE` ×5, FROZEN retained. Every Gen 1
> child ties its Gen 0 parent(s) cell-for-cell — zero
> lexicographic fitness movement. Gen 1's entire gain is
> paperwork (design evaluability), and even that is
> incomplete and partly restates the parents. There is no
> Step 5 handoff candidate.**

## 1. Gen 0 → Gen 1 gate-matrix comparison

Same PASS bar both generations (≥Moderate human-verified
GRADE + Appendix A v1 tier; agent rows UNASSESSED cap at
INSUFFICIENT; G3b BLOCKED forces INSUFFICIENT + no
promotion). Gen 1 gate table re-run this synthesis:
`gate_table.py adapted-gen1.csv` → diff vs committed
`scoring/gate-matrix-gen1.md` **CLEAN** (skeptic §7 got the
same; adaptation re-derived 41 rows, 0 mismatches; scoring
unit tests 18 OK).

| Gen 0 parent | G1–G6 (Gen 0) | Gen 1 child | G1–G6 (Gen 1) | Δ |
|---|---|---|---|---|
| A | INS×6, G6 **FAIL†** | GEN1-A1 | INS×6, G6 **FAIL†** | none |
| F | NA, INS×6 | GEN1-F1m | NA, INS×6 | none |
| G | NA, INS×6 | GEN1-Ga | NA, INS×6 | none |
| H | NA, INS×6 | GEN1-H1 | NA, INS×6 | none |
| G + H (+ A-std‡) | NA, INS×6 each | GEN1-P1 | NA, INS×6 | none |

Gates in order G1, G2, G3a, G3b, G4, G5, G6; INS =
INSUFFICIENT. †Disputed strict-reading completeness FAIL
(no numeric timeline, D17), carried A→A1 verbatim by
design; looser reading flips both to INS and changes no
rank (7 vs 6 applicable gates). ‡P1's "A" is A-standard =
the frozen clinical-monopolar comparator, not A's focal
challenger — P1 is in substance **G + H sequenced over
frozen care** (skeptic §1).

- **Counts.** Gen 0 adapted: PASS 0 / FAIL 7 / INS 171 /
  NA 7 (185 rows). Gen 1 extract: PASS **0** / FAIL 1
  (carried) / INS 36 / NA-prereg 4; grades UNASSESSED
  41/41; tier RECORD 41/41 (design statements, not
  results). No G4/G5 veto FAIL in either generation's
  Track P; no PASS at any G1 anchor (4/8/10/16).
- **Every numeric fitness input is still NA**
  (`delta_g2_db`, `delta_g3a_sd`, `g1_channels`,
  `burden_rank`, G5 aggregate) for all 13 candidates.
- **Kills all unevaluable, none triggered, none cleared**
  (D10): A1 *specifiable only* — model/version/seeds and
  per-contact safe-charge limit deferred to a freeze
  addendum, test unrun; Ga/F1m *collectable* — verdict
  pending wedge-vs-cohort choice and ratified bounds;
  H1 evaluable-by-design only, **post-CI harm not
  cleared**; P1 fires only via component kills or I1–I3
  interface FAILs, zero interface data. Skeptic
  downgrades applied: the scorer's unqualified "runnable"
  does not survive for A1/Ga/F1m.
- **Q0 unchanged: UNDECIDABLE-no-data** (thresholds
  unmoved). No Gen 1 design touches it.

## 2. Fitness-movement verdict (§7)

**No candidate improved lexicographic fitness.** On every
§7 key (veto, FAILs, INSUFFICIENTs, G2, G3a, G3b, G1,
burden) each child exactly ties its parent (P1 ties
joint-best parents). Combined parents+children run (144
rows, skeptic-reproduced): F, G, F1m, Ga, H1, P1, H at
0 FAIL / 6 INS / all-NA, then A, A1 at 1/6 — all
within-group order is `gate_table.py`'s candidate-name
reproducibility tie-break, explicitly "not a GOAL rule".
Name order is not fitness. Stable under every reported
sensitivity (A/A1 FAIL flip; G1-NA counted INS; G1 anchor
swap; G2↔G3a / G3b order swap; even the rejected
PROVISIONAL-SIGNAL reading collapses to INS). On
evidence-completeness Gen 1 goes *backwards* (41 design
cells vs parents' 103 study rows).

**What Gen 1 actually bought — evaluability on paper,
skeptic-discounted:**

| Child | Claimed gain | Skeptic-adjusted residue |
|---|---|---|
| A1 | kill-test "fully pre-specified" | Decision-rule *shape* only; deciding facts unfiled → specifiable, not evaluable |
| Ga | concurrent decision-time primaries | Estimand hierarchy + negative controls; concurrent comparison already required by parent G; bounds unratified, design unchosen |
| F1m | concurrent audibility/time-to-CI | Same: operational detail on a parental requirement; design unchosen |
| H1 | encouragement identification | Mostly restates parent H §5 (offer-RCT/ITT/IV/attention-control already there); novel residue = norming details — bundle-or-restatement dilemma on the one-mutation rule (§7 rule: one logged change) |
| P1 | sequenced portfolio, I1–I3 | Legal under §7 rule 3 (stated experiments) but G×H stretches Step 3 §6's device×pathway enumeration; I1 median threshold incoherent + window unset; execution depends on siblings Ga/H1; adds 3 new ways to fail, no evidence |

No PASS below the bar was charged or found (skeptic
charges 4/5 fail mechanically; charge 1 non-survivor
parentage fails — all parents ∈ {A,F,G,H}, subject to the
P1 pedigree qualification above and a provisional,
pre-human-freeze survivor set).

**STOP (§7 rule 5): not met, on both (b) conjuncts.**
(a) no candidate frozen for handoff. (b) Gen 1 is the
**first** consecutive no-improvement generation (counter
**1/2**), *and* promotion-blocking gaps have had **zero**
completed attacks, let alone ≥2 independent ones
(human freeze, G3b/B01, A1 addendum, U09–U13, Q0 decider
all untouched). (c) budget exhaustion not stated.
Max-4-generations clock: **1/4**. Warning that travels
with this: a Gen 2 of more designs without new external
evidence spends counter 2/2 for nothing — the binding
need is filed limits and measured cohorts, not candidates.

**Sequence breach, disclosed (skeptic §6.3):**
`gen01/README.md` required a Gen 1 protocol + freeze
checklist + held-out-manifest update *before any scoring*.
None exists. The Gen 1 re-score, skeptic, and this
synthesis are therefore **triage only**; §7 rules 1/7
remain unsatisfied for Gen 1 as a whole.

## 3. Survivors / retired — updated record

Nothing was promoted, resurrected, or newly retired in
Gen 1. `retire dominated` is again **not** applied
mechanically to A1: its domination is the disputed
paperwork FAIL plus the 7-vs-6-gate artefact, and A1 is
the only child whose mutation can yield a near-term
verdict-moving result (a run kill-test).

| Candidate | Status after Step 4 |
|---|---|
| GEN1-A1, GEN1-F1m, GEN1-Ga, GEN1-H1, GEN1-P1 | **Non-promoting survivors** (designs only, unfrozen). Pareto {F1m, Ga, H1, P1}; A1 dominated via carried FAIL, decline-to-retire upheld. H1 pending human split/re-log (bundle vs norming-only); P1 pending I1 rewrite |
| A, F, G, H (Gen 0) | Parents; status unchanged (kills unevaluable; H harm not cleared). Superseded as design vehicles by their children, not retired |
| B | **Retired — killed as specified** (lifetime arm ii). D11 lenient reversal (kill-pending) travels with every "B killed" sentence; resurrection = new candidate only. Not a Gen 1 parent |
| C, D | Track R watch only (C park clock starts at a real freeze, D12; D advance 0/5 UNMET). Not Gen 1 parents. (Step 3 calls C a "watch parent", fitness-application "not a parent" — Gen 1 used the narrower Track-P reading; human freeze resolves) |
| E | **Parked 0/3**, no Gen 1 child. Re-entry needs all three park conditions |
| FROZEN | **Retained by default** |

## 4. Input to Step 5 (Decide)

GOAL §11 Step 5 offers exactly two outcomes: freeze a
Track-P survivor as study-design handoff, **or** record
no-promotion with killing evidence. The evidence admits
only the second:

- **There is no handoff candidate, and promotion is
  structurally impossible at v1** — not merely
  unachieved. G3b BLOCKED forces `promoted FALSE`
  regardless of every other cell; beneath that, PASS
  requires ≥Moderate *human-verified* GRADE and every
  Gen 1 row is UNASSESSED agent pre-extraction of a
  design that reports no measurement. No Gen 1 file
  contains a result a handoff could be built on.
- **Recommended Step 5 record: NO-PROMOTION after Gen 1**,
  FROZEN retained, killing/blocking evidence = this file
  §§1–2 (zero PASS, zero fitness movement, G3b BLOCKED,
  all kills unevaluable). This is a no-winner statement,
  not a near-miss: the lexicographic "leaders" order is
  alphabetisation over tied all-NA keys and must never be
  printed as a ranking of merit.
- **What Step 5 must not do:** name F1m/Ga/H1/P1 (or any
  candidate) a winner, finalist, or handoff; shorten
  "frozen-equivalent" (P1 device disclosure) to
  "equivalent"; print any kill as "survived/cleared"
  (H harm explicitly *not cleared*); credit CHORD/
  Otarmeni efficacy to routing (D13), Downie yield as
  pathway (D6), or Sharma P1 as W0 evidence (D7);
  make any ≥90% claim (§5.1).
- **Continuation is a holder/budget decision, not an
  evidence one.** Discovery has not STOPped (§2), but
  the only evidence-bearing next moves are attacks on
  gaps (§5), cheapest first: A1 freeze addendum → run
  kill-test; one concurrent-pathway pilot. §12(b)
  abandonment (budget exhausted without Track-P survivor
  after Gen 1) becomes available *if* the holder states
  budget exhaustion; it has not been stated. A further
  design-only generation is the one continuation the
  evidence argues against.

## 5. Gaps — updated, ranked (decision-relevance × tractability)

Carried from Step 3 §7 / score-gen1 §6 / skeptic §8;
Gen 1 closed none of them. Attacks completed: **0** on
every promotion-blocking gap.

| # | Gap | Gen 1 delta |
|---|---|---|
| 1 | Human dual extraction + expert freeze (H-1…H-8) — now also owes Gen 1 protocol + freeze checklist + held-out update (§2 breach), H1 split/re-log, P1 I1 rewrite, D11/D17 reversal decisions | grew |
| 2 | G3b co-design (B01) — sole structural bar to any promotion | unchanged, blocking |
| 3 | A1 freeze addendum (named model/version/seeds + per-contact safe-charge limit, filed pre-unblinding) → kill-test run; A/A1 numeric timeline as a *separate* future child | newly specifiable, unfiled |
| 4 | U09–U13/U17 pins (concurrent frozen variances, cited spoken instruments U11, frozen SS U10, P0 harm rates U13) + D1–D4 denominators — no Ga/F1m/H1/P1 primary sizable without them; Ga bounds + H1 SD-scale ratification inside this item | unchanged, blocking |
| 5 | First data of any kind: A1 model run; concurrent Ga/F1m cohort; H1 encouragement estimate; P1 I1–I3 interface observations. Q0 decider studies (post-establishment AAV; prospective patency) | zero exist |
| 6 | Carry-overs: ~42 unrowed Level-1 cells (D14); Embase/EU CTIS/ChiCTR/ANZCTR behind every absence claim (D9: inspected PubMed/CTgov 2026-11-02); C thermal-dose extraction; E bench primary; B-successor kinetics; post-2026-11-02 evidence only per held-out manifest | unchanged |

**Prohibitions D1–D17 carry verbatim.** Post-freeze edits
to any candidate = new candidate. No candidate is
promotable, no ranking above is a winner claim, and
**FROZEN is retained by default. G3b BLOCKED.**

*Files: `fitness-application.md`, `candidate-{P1,A1,Ga,H1,F1m}-*.md`,
`scoring/{extract-gen1,adapted-gen1}.csv`,
`scoring/{gate-matrix-gen1,score-gen1,adapt-gen1-note}.md`,
`step4-skeptic.md` (this directory); Gen 0 comparators in
`../gen00/scoring/`. Re-run scratch: `/tmp/step4synth-gate.md`.*
