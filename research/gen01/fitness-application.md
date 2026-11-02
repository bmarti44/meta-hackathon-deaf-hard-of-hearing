# Gen 1 fitness application — how GOAL S7 selected the Gen 1 parents

> **Model routing (GOAL S9).** Requested: **Sol 6.1, xhigh**
> (new-generation ideation). Actual: **`muse-wonder-full-1.0`**.
> Date: **2026-11-02**. GOAL v2.2.
> **Authority:** agent synthesis = triage only. Human dual
> extraction, freeze, and H-1…H-8 roster PENDING. Inputs:
> `research/gen00/scoring/gate-matrix-gen0.md` (deterministic
> `gate_table.py` output) + `Step3-scoring-summary.md` SS2–SS6.
> **G3b BLOCKED; no PASS anywhere; no promotion; FROZEN retained.**
> This file selects *parents*, never winners. Same PASS bar as
> Step 3 applies to every Gen 1 child (≥Moderate human-verified
> GRADE + Appendix A minimum tier; INSUFFICIENT never passes).

## 1. The rule applied (GOAL S7, Track P lexicographic)

Order: (veto: G4/G5 FAIL demotes last) → 1) fewest FAILs →
2) fewest INSUFFICIENT among applicable gates → 3) largest G2
gain → 4) largest G3a gain → 5) G3b verdict → 6) device G1
(NA last among ties) → 7) lowest burden (G6). Track R ranked
separately (G1, then G5 aggregate); Track R never counts as
Track P evidence. Pareto sets are transparency only.
Recombination only at evidenced interfaces or with a stated
interface experiment; one logged mutation per child;
post-freeze edits = new candidate (S7 rules 3, 7).

## 2. Inputs (deterministic gate matrix, worst applicable window)

| cand | track | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INSUFF* |
|---|---|---|---|---|---|---|---|---|---|---|
| F | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | 0 | 6 |
| G | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | 0 | 6 |
| H | P | NA | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | 0 | 6 |
| A | P | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | FAIL† | 1 | 6 |
| B | P | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | FAIL | 1 | 6 |
| C | R | INSUFF | INSUFF | INSUFF | INSUFF | FAIL‡ | INSUFF | FAIL | 2 | 5 |
| D | R | INSUFF | INSUFF | INSUFF | INSUFF | FAIL‡ | INSUFF | INSUFF | 1 | 6 |
| E | R | INSUFF | INSUFF | INSUFF | INSUFF | INSUFF | FAIL | FAIL | 2 | 5 |

\* Applicable gates only (G1 NA excluded for F/G/H). †A G6 =
disputed strict-reading completeness FAIL (no numeric timeline;
flips under looser reading, D17/J1-DISSENT-3/J3-3). ‡C/D G4 via
G4-AAV presumptive sub-gate collapse; G4 proper INSUFFICIENT.
All 7 FAILs are completeness/staging/presumptive; none is a
measured harm at ≥Moderate GRADE (D17). Every numeric
tie-break input (`delta_g2_db`, `delta_g3a_sd`, `g1_channels`,
`burden_rank`, G5 aggregate) is NA for every candidate.

## 3. Lexicographic walk (Track P)

- **Veto step:** no Track P candidate has a G4/G5 FAIL → no
  demotion. (Track R C/D/E veto/staging FAILs stay in Track R.)
- **Step 1 (FAILs):** F=G=H (0) beat A=B (1).
- **Step 2 (INSUFFICIENT):** all five tie at 6.
- **Steps 3–7:** G2, G3a, G1, burden all NA; G3b INSUFFICIENT
  for all → no separation. Residual order is candidate name.
- **Result (gate-matrix SSb): 1 F, 2 G, 3 H, 4 A, 5 B.**
  Track R (SSc): 1 C, 2 D, 3 E — pure name order (all keys NA);
  carries no evidence content.
- **Promotion (SSd): FALSE for all eight.** Rank ≠ winner.

## 4. Pareto set and retire-dominated reasoning

Pareto (SSe): Track P = {F, G, H}; Track R = {C, D, E}. A and B
are dominated *solely* via the FAIL count (every other
objective ties at INSUFFICIENT/NA). S7 says "retire dominated
(visible)" — Step 3 synthesis SS6 declines to apply it
mechanically to A, and this application **upholds that
decline**, for stated reasons:

- **B — RETIRED (killed as specified), not merely dominated.**
  Kill arm (ii) lifetime/refill TRIGGERED: no branch declared,
  no kinetics/duration for either branch, lifetime burden
  unstateable (J1+J3 uphold; J2 defers; D11 lenient-reading
  reversal — defer-until-handoff → kill-pending — travels with
  every "B killed" sentence; advancement barred under either
  reading). B's G6 FAIL survives the timeline-reading flip via
  element-2 (uncountable refill/revision operations, J3-8).
  Resurrection = *new* candidate only. **B is not a Gen 1 parent.**
- **A — dominated but NOT retired.** Its domination rests on
  the single disputed G6 paperwork FAIL. Sensitivity run
  (SS3): flip A G6 FAIL→INSUFFICIENT and A still ranks 4th
  (0 FAIL but 7 INSUFFICIENT — devices have 7 applicable gates
  vs pathways' 6); Pareto set unchanged. The ranking is robust
  to the disputed FAIL for a bookkeeping reason, not an
  evidential one. Retiring the most-studied device candidate
  (45 rows/20 cells) on that count would encode the artefact
  S7 itself discloses (fewest-INSUFFICIENT favours an NA gate).
  A's kill is UNEVALUABLE (never "survived", D10). **A is a
  Gen 1 parent (mutate only).**
- **C, D — watch-only, not retired, not parents.** Track R;
  C park not yet triggered (clock starts at a real freeze,
  D12); D advance criterion UNMET (0/5 conjuncts). Neither may
  parent a Track P child; Track R wins never count as Track P
  evidence (S4.1).
- **E — PARKED 0/3, no Gen 1 child.** Bench primary ✗, T2
  chronic denominators ✗, adult feasibility ✗. Re-entry needs
  all three park conditions.
- **F, G, H — Pareto set, carried as untested pathway parents.**
  F/G kills never runnable; H both arms UNEVALUABLE, harm arm
  explicitly *not cleared* (D10). "Available-now components"
  ≠ deliverable pathway (J3-21).

**Binding parent set for Gen 1: {A, F, G, H} only.**

## 5. Rank-sensitivity (reported, per S7)

| Sensitivity | Effect on Track P order / parents |
|---|---|
| A G6 FAIL→INSUFFICIENT (looser timeline reading) | None. A stays rank 4 (7 vs 6 INSUFFICIENT); Pareto unchanged (run in Step 3 SS3) |
| Swap steps 3↔4 (G3a before G2); move G3b above G3a (App. A v1 sensitivity rows) | None. G2/G3a both NA for all; G3b INSUFFICIENT for all — order among NA/tied keys cannot separate |
| Evidence-completeness ranking (rows/cells: A 45/20, B 32/21, F 20/15, G 19/13, H 19/11) | **Inverts the headline:** lexicographic leaders F/G/H are *not* best-evidenced; they lead on zero completeness FAILs + one fewer gate with zero measured effects. Ranks sort paperwork states, not expected child benefit — must never be read as a winner ordering |
| Count G1-NA as INSUFFICIENT-equivalent (non-binding what-if) | F/G/H rise to 7, tying A-under-flip; parent set unchanged. Not adopted: NA is pre-declared (S4.2), not missing data |
| B lenient reading (kill-pending, D11) | B rank unchanged (5th); still barred from advancing; still not a parent in Gen 1 as specified |

No sensitivity changes the parent set {A, F, G, H}, the
retirement of B-as-specified, or the no-promotion result.

## 6. STOP check and Gen 1 consequence

S7 rule 5 STOP conditions: (a) no Track P candidate frozen for
handoff; (b) promotion-blocking gaps have not had ≥2
independent attacks; (c) budget not the stated reason. **STOP
not met → one recombination/mutation round (Step 4) is the
prescribed next step.** Gen 1 (4–8 candidates, S7 rule 1)
therefore consists only of:

- **GEN1-P1** — sequenced portfolio recombinant (G + H +
  A-standard) with stated interface experiments (rule 3);
- **GEN1-A1** — A-mutant (one mutation: kill-test design);
- **GEN1-Ga** — G-mutant (one mutation: concurrent comparison);
- **GEN1-H1** — H-mutant (one mutation: identification +
  norms sharpening);
- **GEN1-F1m** — F-mutant (one mutation: concurrent comparison).

B×anything is forbidden/moot; B×D remains forbidden (no T1
co-delivery data). No slogan cross is proposed. Prohibitions
D1–D17 carry verbatim (Step 3 SS8): per-study signal counting,
no CHORD efficacy to G (D13), yield≠pathway (D6), F-P1 never
pathway evidence (D7), kills as never-runnable/unevaluable
(D10), H harm *not cleared*, bounded absence claims (D9:
inspected PubMed/CTgov 2026-11-02; Embase/EU CTIS/ChiCTR/
ANZCTR unsearched).

*End. G3b: BLOCKED (INSUFFICIENT) — co-design pending.*
