# Gen 1 re-score — P1 / A1 / Ga / H1 / F1m vs frozen & Gen 0 parents

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-02**. GOAL v2.2.
> **Authority:** agent re-score on existing evidence = triage
> only. Human dual extraction, freeze, H-1…H-8 roster PENDING.
> **Headline: no gate PASS anywhere, G3b BLOCKED for all five,
> `promoted FALSE` for all five, FROZEN retained. No Gen 1
> candidate improves lexicographic fitness over its Gen 0
> parent(s) — every child ties its parent cell-for-cell. The
> Gen 1 designs buy *evaluability* (runnable estimands/kills),
> not gate verdicts.**

## 1. Method — same bar, existing evidence only, no PASS inflation

**PASS bar (unchanged from Step 3):** ≥Moderate *human-verified*
GRADE **and** Appendix A v1 minimum tier (protocol §6 GRADE→score
map); abstract/agent-only evidence caps at PROVISIONAL-SIGNAL,
which `gate_table.py` collapses to INSUFFICIENT; grade is
UNASSESSED on every agent row; INSUFFICIENT never passes and is
never safety (D10/D17). Convention deltas (G1 "8", ≥3 dB,
±0.4/0.2 SD, G6 caps) remain sensitivity-only. G3b BLOCKED forces
G3b INSUFFICIENT and `promoted FALSE` regardless.

**What a Gen 1 design file can and cannot do to a verdict.** All
five Gen 1 candidates are pre-registration *designs* stating "scores
nothing"; they report no new study, model run, cohort, or count.
Re-scoring therefore uses only: (a) inherited Gen 0 extraction
evidence (`extraction_v1_2026-11-02.csv`, referenced per row, never
duplicated — parent findings are not re-counted as child findings,
D8), and (b) the design's own pre-specification. Where a design
pre-specifies an estimand/comparator/kill rule, the cell is scored
on **design adequacy** in the precise sense the candidate itself
uses — *the kill/estimand is now runnable* — and that adequacy is
printed in the extraction `claim`. Design adequacy supplies no
effect, no tier-qualifying result, and no GRADE, so under the same
bar every such cell remains **INSUFFICIENT**. The two readings we
reject as PASS inflation: counting a pre-specified endpoint as a
measured endpoint, and counting "kill now runnable" as "kill
cleared/survived" (D10). Cells move only where Appendix A makes a
*completeness* fact scorable with no data — exactly one in Gen 1,
and it moves nothing (A1's carried G6 FAIL, §3).

**Files & commands (observed outputs):**

```text
research/gen01/scoring/extract-gen1.csv    41 gate-cell rows, 14-col schema
  verdicts_proposed: INSUFFICIENT 36, NA-prereg 4, FAIL 1, PASS 0; grades UNASSESSED 41
$ python3 research/scoring/adapt_extraction.py research/gen01/scoring/extract-gen1.csv /tmp/gen1_stock_adapted.csv
adapted 0 rows        # adapter maps A-H only; limitation documented in adapt-gen1-note.md
research/gen01/scoring/adapted-gen1.csv    41 rows, manual adaptation, documented GEN1-* -> P map
$ cd research/scoring && python3 gate_table.py ../gen01/scoring/adapted-gen1.csv --out ../gen01/scoring/gate-matrix-gen1.md  (exit 0)
$ python3 -m unittest        # research/scoring: Ran 18 tests, OK
```

Control: stock adapter re-run on the Gen 0 extraction reproduces
committed `adapted_v1.csv` byte-identically. A combined
parents+children run (Gen 0 A/F/G/H adapted rows + Gen 1 adapted
rows, `/tmp/combined_matrix.md`, scratch only) was used for the
cross-generation fitness check in §4. `gate_table.py` was not
edited. FMEA: Gen 1 delta rows carry **zero numeric probability
bands** (all UNPINNABLE, as in Gen 0) — no `--fmea` input was
fabricated; Track P does not use the G5 aggregate and Track R is
empty in Gen 1, so this is inconsequential (same state as Gen 0's
header-only `fmea_v1.csv`).

## 2. Gate matrix (deterministic output, `gate-matrix-gen1.md` §a)

| candidate | parent(s) | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INSUFF* |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN1-P1 | G+H+A-std | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN1-A1 | A | INS | INS | INS | INS | INS | INS | **FAIL†** | 1 | 6 |
| GEN1-Ga | G | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN1-H1 | H | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN1-F1m | F (F1) | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |

\* Applicable gates only. INS = INSUFFICIENT. †A1 G6 = disputed
strict-reading completeness FAIL carried verbatim from A (D17).
No G4/G5 veto FAIL; no PASS at any anchor (G1 4/8/10/16 included —
A1 has no channel numerator under any anchor); every numeric
fitness input (`delta_g2_db`, `delta_g3a_sd`, `g1_channels`,
`burden_rank`) is NA for all five, exactly as in Gen 0. Gen 1
lexicographic order (matrix §b: F1m, Ga, H1, P1, then A1) separates
nothing — ranks 1–4 are the candidate-name reproducibility
tie-break over identical keys, **not a winner ordering**. Pareto
set (transparency only): {P1, Ga, H1, F1m}; A1 is dominated solely
via the same disputed FAIL that dominated A — the Step 3 decline
to retire on that artefact carries over unchanged (§4).

## 3. Cell-by-cell: Gen 1 child vs Gen 0 parent(s)

Every cell is **unchanged** from its parent ('=' below). What
changed is printed per candidate: evaluability gains, and the one
explicitly-carried defect.

### GEN1-A1 vs A — = = = = = = = (G6 FAIL carried, by design)

| gate | A → A1 | Basis |
|---|---|---|
| G1 | INS → INS | Mutation fully pre-specifies the T0 kill-test (fibrotic 0–3 + growing geometries, spread mm/oct, pinned seeds, battery floor, decision rule). Test **not run**; per-contact safe-charge limit **not yet filed** — by the child's own rule the test stays UNEVALUABLE until filed pre-unblinding. T0 output alone could never PASS G1 (≥12 ch + head-to-head ripple/spread + non-inventor replication still owed). Inherited: 1 inventor-lab mechanism study (PMID 17552721) + 3 adult nulls, per-study (D8) |
| G2/G2-music | INS → INS | No new data; T3 adult nulls/barred degraded-comparator win (PMID 23467170) below T4; CAMP capped provisional. No ≥Moderate NI breach to FAIL on |
| G3a | INS → INS | No language data; U10/U11/>73 mo gaps stand |
| G3b | INS → INS | BLOCKED |
| G4 | INS → INS | No comparative biology; Q0 UNDECIDABLE; veto neither passed nor triggered |
| G5 | INS → INS | C9 narrowed to a *procedure* for filing the limit + C9-delta FMEA row; limit itself still unfiled, rates U13. Design narrows C9, does not close it |
| G6 | **FAIL → FAIL†** | Child §1 explicitly rejects the numeric-timeline fix as a second mutation, so A's disputed completeness FAIL (stage sequence, no numeric year; App. A §7.3) carries verbatim. Looser reading flips both A and A1 to INSUFFICIENT (sensitivity, §4). Not measured harm (D17) |
| Kill | UNEVALUABLE → UNEVALUABLE (now *specifiable*) | Runnable only once model/version/seeds + named-device charge limit are filed in the freeze addendum; until then unevaluable, never "survived" (D10) |

### GEN1-F1m vs F — = = = = = = =

| gate | F → F1m | Basis |
|---|---|---|
| G1 | NA → NA | Pre-declared; no channel claim (any claim = FAIL of NA rule, none made) |
| G2 | INS → INS | W0–W1 no PASS exists (mechanism). W3 same-test downstream now pre-specified vs concurrent frozen; no result. Tumuklu PMID 42194183 stays mechanism context (D7); Sharma P1 never W0 evidence |
| G3a | INS → INS | W2 falsifying endpoint pre-specified; uncited instruments U11/frozen SS U10; mediation UNRESOLVED |
| G3b/G4/G5 | INS → INS | BLOCKED; nothing implanted (no numeric G4 PASS constructible, U17); false-reassurance/F-vib harm INSUFFICIENT both directions, F-vib exploratory never pooled |
| G6 | INS → INS | **Design-adequacy gain:** audibility (SII/wear) + time-to-CI estimands vs a *concurrently measured* frozen HA trial — cures the U09 unmeasured-baseline defect *for this contrast if run*. Zero measurements exist; D1–D4 blank; N UNPINNABLE → same verdict. Timeline stated; no FAIL |
| Kill | never runnable → **runnable, not run** | Both conjuncts (audibility, time-to-CI) now have a concurrent denominator on paper. Unevaluable ≠ survived (D10) |

### GEN1-Ga vs G — = = = = = = =

| gate | G → Ga | Basis |
|---|---|---|
| G1 | NA → NA | Portfolio/frozen-equivalent disclosure inherited |
| G2/G3a | INS → INS | Downstream decision-time secondaries pre-specified; CHORD/Otarmeni (NCT05788536) outcomes barred as Ga effects (D13); U10/U11 stand |
| G3b | INS → INS | BLOCKED |
| G4 | INS → INS | Option preservation gains a stated numerator/denominator (ear-level, child-clustered) but no count; patency/Q0 UNDECIDABLE; no unstudied post-CI AAV claimed (no C13 FAIL) |
| G5 | INS → INS | Harm co-primary (non-eligible time-to-CI must not lengthen) + wedge-confounding deltas pre-specified; rates UNPINNABLE, zero counts |
| G6 | INS → INS | **Largest design-adequacy gain in Gen 1:** primaries (sample→counselled-result days; origin→first-access days, treatment-policy) vs concurrent P07, hierarchical gatekeeping, negative-control turnaround. Still unmeasured on both sides; Downie yield (PMID 31827275) barred as endpoint (D6 — Ga inherits G's one PROVISIONAL-SIGNAL yield row, which collapses to INSUFFICIENT and is not re-counted here); "tens/year" never an input |
| Kill | never runnable → **runnable, not run** | Both arms evaluable once enrolled; until ratified meaningful-gain bounds + data exist: unevaluable (D10) |

### GEN1-H1 vs H — = = = = = = =

| gate | H → H1 | Basis |
|---|---|---|
| G1 | NA → NA | Pre-declared |
| G2 | INS → INS | Post-CI NI test sharpened (same-test, CI-age stratified, per-child delay accounting); **harm arm explicitly NOT cleared** — controlling synthesis Fitzpatrick 2016 (PMID 26684476) still grades the base insufficient. INSUFFICIENT is not safety |
| G3a | INS → INS | **Design-adequacy gain:** offer-only randomization + contact-time-matched attention control; ITT primary, IV dose secondary with first-stage/weak-instrument→INSUFFICIENT rule, exclusion/monotonicity probes, negative control; ASL-CDI always exposure-reported with dual-SD scaling (norm SD *and* P0 hearing-parent SD, ratification pending), vocabulary≠morphosyntax cap, >73 mo INSUFFICIENT (Judge 2 ##19–22). No encouragement/IV estimate exists; U10/U11 stand |
| G3b | INS → INS | BLOCKED — H1 most dependent on the blocked construct, stated not evaded |
| G4/G5 | INS → INS | No biology altered; CI-delay (sev 3) rate UNPINNABLE, counts now observable-by-design only; encouragement-pressure/contamination deltas filed |
| G6 | INS → INS | Frozen EI mix to be measured concurrently and attention-control burden counted in-arm; coverage/mentor supply unmeasured |
| Kill | both UNEVALUABLE → both **evaluable-by-design, not evaluated** | (a) signed NI on ratified scale, (b) post-CI harm ≥Moderate. Neither triggered nor cleared (D10) |

### GEN1-P1 vs G, H (and A-standard) — = with every parent, plus interface exposure

P1 has no Gen 0 cell of its own; compared against its best
parents it matches F/G/H exactly: G1 **NA disclosed**
(frozen-equivalent, clinical monopolar — **no G1 win**, and the
≥12-channel bar explicitly not claimed; claiming one would FAIL
the NA rule), G2–G6 all INSUFFICIENT, 0 FAILs. Its only
scorable-now content is recombination legality: no pair has
combination data, so each join exists solely as a stated interface
experiment with a FAIL rule — I1 (triage→allocation, any attributable
non-eligible delay = I1 FAIL), I2 (H parallel, CI-delay/post-CI harm
fires H kill arm b), I3 (anatomy documentation at zero added days).
That is §7-rule-3 compliant and creates three *new ways to fail*
later, none evaluable today; it creates no evidence now. Pooled
component signals, CHORD-to-routing credit (D13), and Downie-yield-
as-pathway (D6) remain forbidden. FMEA deltas D-P1-1…3 (handoff
delay compounding, messaging conflict, W0–W1 burden stacking) are
filed with UNPINNABLE bands. Q0 stays UNDECIDABLE; patency/G4 cells
INSUFFICIENT. P1 is therefore **not** a G×H slogan cross and **not**
an improvement: it is two INSUFFICIENT parents under one timeline,
awaiting interface data.

## 4. Lexicographic fitness & GOAL §7 stopping rule (b) — the answer

**No Gen 1 candidate improves lexicographic fitness.** On every
GOAL §7 key — (veto) G4/G5 FAIL, 1) FAIL count, 2) INSUFFICIENT
count among applicable gates, 3) G2 gain, 4) G3a gain, 5) G3b,
6) G1 channels (NA last), 7) burden — each child is **exactly tied**
with its parent (mutants) or with the joint-best parents (P1).
The combined parents+children deterministic run makes the tie
mechanical: Track P sorts as F, G, GEN1-F1m, GEN1-Ga, GEN1-H1,
GEN1-P1, H (all 0 FAIL / 6 INSUFFICIENT / all numerics NA), then
A, GEN1-A1 (1 FAIL / 6). All movement inside those groups is
`gate_table.py`'s final candidate-name tie-break, which its own
docstring states is "a final reproducibility tie-break only (not a
GOAL rule)". Name order is not fitness: F1m sitting above H in that
table is alphabetisation, and reading it as improvement would be
exactly the PASS inflation this re-score forbids.

**Sensitivities (fitness order stable under all):**

| Sensitivity | Effect |
|---|---|
| A/A1 disputed G6 FAIL → INSUFFICIENT (looser timeline reading) | A and A1 both 0 FAIL / **7** INSUFFICIENT (7 applicable device gates) — still behind all pathways (6), still tied to each other. No child improves |
| Count G1-NA as INSUFFICIENT (non-binding what-if) | All pathway parents and children rise to 7 together. Ties unchanged. (Not adopted: NA is pre-declared, §4.2) |
| G1 anchors 4/10/16 | A1 INSUFFICIENT under every anchor — no numerator exists at any anchor. No movement |
| Swap G2↔G3a, move G3b (App. A sensitivity rows) | All keys NA/INSUFFICIENT for all — nothing to separate |
| Score "design-adequate" cells as PROVISIONAL-SIGNAL (rejected reading) | Collapses to INSUFFICIENT in `gate_table.py` by construction; ranking bit-identical. Even the inflated reading cannot manufacture an improvement |
| Evidence-completeness ranking (disclosed inverse) | Gen 1 children are *less* evidenced than parents by construction (41 design/record gate-cells vs parents' 103 study rows A45+F20+G19+H19). On completeness, Gen 1 goes backwards — further proof ranks here sort paperwork states, not child benefit |

**Stopping rule §7(5):** (a) no Track P candidate frozen for
handoff — not met. (b) *"two consecutive generations add no
candidate improving lexicographic fitness **and** all
promotion-blocking gaps have had ≥2 independent attacks"* — Gen 1
is the **first** consecutive no-improvement generation (counter =
1 of 2), and the second conjunct is false regardless: human dual
extraction/freeze, G3b co-design (B01), A numeric timeline +
safe-charge limit, U09–U13 pins, and Q0 decider studies have had
**zero** completed attacks, let alone two independent ones. (b) is
therefore **not met**, on both conjuncts independently. (c) budget
exhaustion not stated. **⇒ STOP not met. Discovery does not stop
on this re-score.** Two honest corollaries must travel with that:
(i) if Gen 2 also adds design-only candidates with no new external
evidence, the (b) counter reaches 2 and only the un-attacked-gaps
conjunct would then stand between the loop and a *partial* stop —
the cheapest way to keep the loop meaningful is data (A1's filed
kill-test run; one concurrent-pathway pilot), not more designs;
(ii) the §7 "max 4 generations for non-promoting survivors without
new external evidence" clock is now at generation 1 of 4.

**Retire-dominated:** mechanically applying it would retire A1
(dominated via FAIL count only). We do not, for Step 3 §6's stated
reason, unchanged: the domination is the disputed paperwork FAIL
plus the 7-vs-6 applicable-gate artefact §7 itself discloses, and
A1 is the only child whose single mutation can produce a near-term
*verdict-moving* result (a run kill-test). No other retirement,
promotion, or resurrection arises. B stays retired-killed (D11
reversal travels), C/D watch, E parked — none were parents, none
were re-scored.

## 5. Kill status (all unevaluable; none triggered, none cleared)

| child | kill state after re-score |
|---|---|
| GEN1-A1 | UNEVALUABLE — design frozen on paper; safe-charge limit + named model/version/seeds still to be filed, model unrun. Directional priors adverse; priors are not results |
| GEN1-F1m | Runnable-by-design, NOT RUN — no concurrent audibility/time-to-CI measurement exists. F-vib kill independent, harm uncharacterised both directions |
| GEN1-Ga | Runnable-by-design, NOT RUN — no concurrent turnaround/time-to-access counts. Q0-pivot arm UNDECIDABLE, neither supports nor refutes |
| GEN1-H1 | Both arms evaluable-by-design, NOT EVALUATED — signed NI breach untested; post-CI harm **not cleared** |
| GEN1-P1 | Unevaluable — fires only via component kills or I1–I3 interface FAILs; no interface has data |

## 6. Unresolved (what would move the next re-score, ranked as Step 3 §7)

1. Human dual extraction + expert freeze (H-1…H-8) — every row here
   is UNASSESSED agent pre-extraction; also owed *before* scoring
   per `gen01/README.md`: Gen 1 protocol + freeze checklist +
   held-out-manifest update. This re-score is sensitivity-only
   until then.
2. G3b co-design (B01) — sole structural bar to any Track P
   promotion, Gen 1 included.
3. A1 freeze addendum: named model/version/seeds + per-contact
   safe-charge numeric limit filed **before** outputs opened, then
   the run — the only Gen 1 artefact that can change a kill (and
   feed G1/G5-C9) without a new trial. A's/A1's numeric timeline
   remains owed as a *separate* future child (one-mutation rule).
4. U09–U13/U17 pins (concurrent frozen variances, cited spoken
   instruments U11, frozen SS U10, P0 harm rates U13) + D1–D4
   denominators — without them Ga/F1m/H1/P1 primaries cannot be
   sized or pass even if enrolled tomorrow.
5. Any post-2026-11-02 external evidence enters per held-out
   manifest as validation/late-found design — never silently
   pooled into these rows (D9 bounded absence: inspected
   PubMed/CTgov 2026-11-02; Embase/EU CTIS/ChiCTR/ANZCTR
   unsearched). Post-freeze edits to any candidate = new candidate.

**Prohibitions D1–D17 carry verbatim** (Step 3 §8): per-study signal
counting; no yield-as-pathway (D6), no F-P1-as-pathway (D7), no
CHORD efficacy to routing (D13); kills as never-runnable/
unevaluable, never "survived" (D10); H harm printed *not cleared*;
no ranking above is a winner claim; **FROZEN retained by default.**

*Files: `extract-gen1.csv`, `adapted-gen1.csv`,
`adapt-gen1-note.md`, `gate-matrix-gen1.md` (this directory);
build script `/tmp/build_gen1_extract.py`; combined cross-gen
check `/tmp/combined_matrix.md` (scratch, not committed evidence).*
