# Gen 2 re-score — P2 / H2 / Q1 / R1 vs frozen & Gen 1 parents

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. **Holder-directed continuation
> 2026-11-02**; scored 2026-11-03. GOAL v2.2.
> **Gen clock: Gen 2 = generation 2 of max 4.**
> **Authority:** agent re-score on existing evidence = triage
> only. Human dual extraction, freeze, H-1…H-8 roster PENDING.
> **Headline: no gate PASS anywhere, no FAIL, G3b BLOCKED,
> `promoted FALSE` for every promotable candidate, FROZEN
> retained. Neither promotable Gen 2 child improves
> lexicographic fitness over its Gen 1 parent(s) — both tie
> cell-for-cell. Q1/R1 claim no self-verdict and cannot
> improve fitness by their own construction (see §1). The
> §7(5b) no-improvement counter therefore reaches 2/2 —
> exactly the spend the Gen 2 fitness application warned
> against (§4) — but STOP is still not met, because the
> gaps conjunct remains false.**

## 1. Method — same bar, design-only rule, sweep flagged

**PASS bar (unchanged):** ≥Moderate *human-verified* GRADE
**and** Appendix A v1 minimum tier; scorer v2
(`gate_table.py:175-208`) now enforces both mechanically
(`effective_verdict` downgrades sub-Moderate/sub-tier
PASSes) and excludes G2 W0–W1 mechanism rows
(`is_mechanism_only`). Both rules are no-ops here — **0
PASS proposed, 0 G2 W0/W1 rows** — so v2 moves no Gen 2
cell. Grade is UNASSESSED on all 33 rows; tier is RECORD
(design statements) on all 33; INSUFFICIENT never passes
and is never safety (D10/D17); G3b BLOCKED forces
INSUFFICIENT + `promoted FALSE` regardless.

**Design-only rule (as Gen 1).** All four Gen 2 files are
pre-registration designs stating "scores nothing"; none
reports a study, cohort, audit, or count. Pre-specifying
an estimand/kill makes a cell *evaluable-by-design*
(printed in the extraction `claim`) and supplies no
effect, so every such cell stays INSUFFICIENT. Rejected
as PASS inflation: counting I1*'s crispness, H2's ruler
design, Q1's estimand generation-plan, or R1's leg
separation as results.

**Who enters the matrix.** Only the two promotable
Track-P candidates, P2 and H2 (`adapted-gen2.csv`, 16
rows). Q1 (decider study, "claims no gate PASS for
itself") and R1 (rule-test, "earns no gate verdict") are
**extract-only** (17 rows) and scored narratively in §3,
because their own §8 scorer notes exclude them from
`gate_table.py` until a cell manifest exists (review
§5). The observed cost of ignoring that: a scratch run
including them ranks R1/Q1 "first/second" (2–3
INSUFFICIENT) by NA scope-shrinkage — an artefact, not
fitness (`adapt-gen2-note.md`). H2, by contrast, keeps
the full H1 pathway footprint: its §8 "no H2 claim"
gates are silent omissions = INSUFFICIENT (Gen 1
convention), not new NAs — otherwise the same artefact
would apply.

**Sweep (flagged, per task).** The 2026-11-03 sweep
admitted **zero validation evidence; the validation set
remains empty (0)**. Exactly one extract row touches
external results at all — GEN2-R1 G4-AAV leg (a), PMID
42362868 — and it is scored **PROVISIONAL-SIGNAL →
INSUFFICIENT**, flagged in-row as late-found DESIGN
(epub 2026-06-26 ≤ freeze), abstract-level agent
pre-extraction, single-arm n=4, inventor/trial group,
full-text human dual extraction + ChiCTR2200063181
inspection owed. **No cell in this re-score uses
validation evidence, because none exists.** Nothing in
the sweep moves any Gen 0/1 cell, Q0, or the G4-AAV
applications to C/D.

**Files & commands (observed outputs, this session):**

```text
research/gen02/scoring/extract-gen2.csv    33 rows, 14-col: INS 19, NA-prereg 13, PROV-SIG 1, PASS 0, FAIL 0
$ python3 research/scoring/adapt_extraction.py research/gen02/scoring/extract-gen2.csv /tmp/gen2_stock_adapted.csv
adapted 0 rows        # A-H map only; documented in adapt-gen2-note.md
research/gen02/scoring/adapted-gen2.csv    16 rows (P2+H2), manual adaptation, documented map
$ cd research/scoring && python3 gate_table.py ../gen02/scoring/adapted-gen2.csv --out ../gen02/scoring/gate-matrix-gen2.md  (exit 0)
$ python3 -m unittest discover   # research/scoring: Ran 18 tests, OK (+ ASTRA PROBES PASS)
control: stock adapter on Gen0 extraction reproduces adapted_v1.csv byte-identically (diff clean)
combined check: Gen1 adapted (41 rows) + Gen2 adapted (16) -> /tmp/combined_gen12.md (scratch, §4)
rejected-artefact probe: + Q1/R1 forced in -> /tmp/combined_qr.md (scratch, §1/§4)
```

`gate_table.py` and `adapt_extraction.py` were **not
edited**. **Sequence breach repeated, disclosed:**
fitness-application §6 requires a Gen 2 protocol +
freeze checklist + held-out-manifest update *before*
any Gen 2 scoring; none exists, and its §1 warns that
scoring Gen 2 design-only "would tie again and spend
no-improvement counter 2/2 for nothing." This re-score
is performed under holder/workflow direction with that
warning carried verbatim into §4; it is triage/sensitivity
until humans freeze. That does not cure the breach.

## 2. Gate matrix (deterministic, `gate-matrix-gen2.md` §a)

| candidate | Gen 1 parent(s) | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INSUFF* |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN2-P2 | GEN1-P1 + GEN1-Ga | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN2-H2 | GEN1-H1 | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN2-Q1 | GEN0-G Q0 via GEN1-Ga | NA† | NA† | NA† | NA†‡ | INS | INS | NA† | — | — |
| GEN2-R1 | G4-AAV rule | NA† | NA† | NA† | NA†‡ | INS§ | NA† | NA† | — | — |

\*Applicable gates only (matrix candidates). INS =
INSUFFICIENT. †Narrative-only NA with reasons printed
(candidate §8); **not a verdict and not counted in any
fitness key** — Q1/R1 are absent from the matrix, the
ranking, and Pareto by design. ‡In any candidate matrix
the scorer would force G3b INSUFFICIENT (BLOCKED)
despite the NA declaration. §R1 G4 = worst of legs
(a) provisional-signal→INS, (b) INS, (c) INS; no leg
retired, presumption stands. No G4/G5 veto FAIL; every
numeric fitness input (`delta_g2_db`, `delta_g3a_sd`,
`g1_channels`, `burden_rank`, G5 aggregate) is NA for
all candidates, exactly as Gen 0/1. Matrix ranking
(H2 above P2) and Pareto {H2, P2} separate nothing —
identical keys, candidate-name tie-break only,
explicitly "not a GOAL rule". No ranking here is a
winner claim.

## 3. Cell-by-cell vs Gen 1 parents

Every promotable cell is **unchanged** ("="). What
changed is evaluability and defect-repair *on paper*,
printed per candidate. Q1/R1 have no parent cells to
tie — their rows are first filings of a footprint, not
improvements.

### GEN2-P2 vs GEN1-P1 & GEN1-Ga — = = = = = = =

| gate | parents → P2 | Basis |
|---|---|---|
| G1 | NA → NA | Portfolio NA disclosed, frozen-equivalent, ≥12 bar not claimed (§8). No G1 win; claiming one would FAIL the NA rule |
| G2 / G2-music | INS → INS | Same-test W3 deltas pre-specified behind I1\*/I2/I3 (§8); unenrolled. CHORD/Otarmeni barred as pathway effects (D13); CAMP capped provisional |
| G3a | INS → INS | Conventions inherited; signed cells now *explicitly* unscorable until H2's ratified scale exists (§8) — an honest narrowing, not a gain. U10/U11 stand |
| G3b | INS → INS | BLOCKED |
| G4 | INS → INS | **The generation's real design repair, still verdict-flat:** I1's incoherent median rule (Step 4 skeptic) is replaced by I1\* — primary zero-tolerance *process* leg (≥1 audit-trailed attributable day = FAIL event; observable only under single-protocol ownership) + secondary distributional NI leg whose margin is **unratified** and therefore sensitivity-only (§3). No audit/enrolment/counts; patency defers to Q1-type data; Q0 UNDECIDABLE; no C13 FAIL |
| G5 | INS → INS | I1\* event/mis-triage counts now observable-by-design; zero observed; bands UNPINNABLE (U13) |
| G6 | INS → INS | Stepped-wedge **committed** (Ga's wedge-or-cohort indecision resolved on paper); turnaround/time-to-access still unmeasured on both sides; caps unratified; D1–D4 blank |
| Kill | unevaluable → **evaluable-by-design, not evaluated** | I1\* process leg is the first crisp per-child interface kill in the lineage; component kills inherited. Unevaluable ≠ survived (D10) |

### GEN2-H2 vs GEN1-H1 — = = = = = = = (bundle removed)

| gate | H1 → H2 | Basis |
|---|---|---|
| G1 | NA → NA | Pre-declared |
| G2 | INS → INS | H2 runs **no** auditory contrast (§8); post-CI harm inherited and explicitly **not cleared** (Fitzpatrick 2016 base insufficient). H2 must never be quoted as non-harm evidence |
| G3a | INS → INS | H2's entire content: norming-discordance design for the signed stratum. Discordance tolerance **unratified**, no norming sample exists; by its own §1/§8 H2 cannot earn a G3a PASS, only make one scoreable later. Spoken cells untouched (U10/U11) |
| G3b | INS → INS | BLOCKED — most dependent lineage; ruler ≠ construct |
| G4/G5 | INS → INS | No claim; inherited harm accounting; kill (b) attached but **not evaluable by H2** (§12) |
| G6 | INS → INS | Representativeness-by-subgroup is a future study output; precision targets unmet/unset (§9) |
| Kill | (a) re-pointed, **unevaluable** | New (a\*) *scoreability* kill (kills the ruler, not Family H); inherited (a)/(b) unevaluable, harm not cleared. The split **subtracts** H1's identification bundle rather than restating GEN0-H §5 — it removes the Step 4 bundle-or-restatement defect and buys no verdict |

### GEN2-Q1 — decider study, no self-verdict (extract-only)

| footprint | verdict | Basis |
|---|---|---|
| G4 / Q0-P | INS | Would generate the first cannulability n/N by time band under a pre-stated access definition. Sweep: **zero** prospective patency n/N exists. Species/construct/dose/N are freeze-addendum items, UNPINNABLE in-file. Revision-series/DPOAE-title records are not patency percentages and were not entered as any |
| G4 / Q0-A | INS | Would generate retention A1+A2 vs same-study unimplanted comparator, S2.3 minima as design-kill, thresholds inherited verbatim + **unratified** (sensitivity-only reads until ratification). Sweep: zero sequence-(ii); NCT07752888 (n=1, no results, est. 2027-05-31) can never decide this alone. **Q0 stays UNDECIDABLE-no-data** |
| G5 | INS | Animal-safety inputs only; nothing dosed |
| G1/G2/G3a/G3b/G6 | NA† | Scope-fenced AAV-naïve established-implant question; T2 earns itself no promotion gate (§1) |
| Kill | unevaluable | Q1 is killable *as decider* (S2.3 failure) only once executed; today there is no executed form. Its value is that the missing estimand now has an owner — a gap-attack design, not fitness |

### GEN2-R1 — rule-test, no self-verdict (extract-only); sweep row flagged

| G4-AAV leg | verdict | Basis |
|---|---|---|
| (a) NAb → contralateral re-dose | **PROVISIONAL-SIGNAL → INS** ⚑ | **The one sweep-affected cell in Gen 2 — DESIGN-side, not validation.** PMID 42362868 (n=4 contralateral re-administration; abstract-level ABR >95→43/63/80/53 dB at 26 wk; sweep §3.4) is the first human evidence against the *strong form* of this leg, and the sweep's own label is "provisional signal — awaiting human extraction," which scores INSUFFICIENT under the bar (UNASSESSED; v2 would downgrade any PASS). Inventor/trial group, single-arm, no replication, ChiCTR uninspected, full-text dual extraction owed ⇒ **leg (a) is NOT retired**; R1's retiring standard (≥Moderate after extraction/RoB + ≥1 non-inventor or held-out-side input, §3) is unmet by a wide margin |
| (b) Established-implant delivery | INS | Assigned wholly to Q1 (binding fence); zero data; says nothing in either direction |
| (c) Same-ear re-dose | INS | T2 spec only; untested (42362868 ears were contralateral and implant-naïve — estimand substitution into (b)/(c)/Q0 is the named D-R1-2 failure and was not committed) |
| G1/G2/G3a/G3b/G5/G6 | NA† | Not R1's estimands (§8); re-dose safety signals route to the G5 record, never an R1 verdict |
| Kill | unevaluable | Per-leg retire/confirm kills now *defined* for the first time — the presumption is at falsifiable risk on paper and **stands unchanged in every application** (C/D G4-AAV cells, sequencing rationales) until a leg meets its standard through the human process |

## 4. Combined fitness run & STOP counter (the spend, stated plainly)

**No Gen 2 candidate improves lexicographic fitness.**
The combined Gen 1 + Gen 2 deterministic run (57 rows
+ header, `/tmp/combined_gen12.md`, scratch) sorts
Track P as: GEN1-F1m, GEN1-Ga, GEN1-H1, GEN1-P1,
**GEN2-H2, GEN2-P2** (all 0 FAIL / 6 INSUFFICIENT / all
numerics NA), then GEN1-A1 (1/6, carried disputed FAIL).
P2 exactly ties its joint-best parents P1/Ga; H2
exactly ties H1; all within-group order is the
candidate-name tie-break, not fitness. A1/F1m (no Gen 2
child) are unchanged; A1's decline-to-retire carries
over (disputed paperwork FAIL + 7-vs-6 artefact).
Promotion FALSE for P2/H2; Q1/R1 are non-promotable by
construction and appear in no ranking.

**Sensitivities (order/conclusion stable under all):**

| Sensitivity | Effect |
|---|---|
| Force Q1/R1 into the matrix (rejected; scratch observed) | R1 0/2, Q1 0/3 spuriously "lead" by NA scope-shrinkage + forced G3b. Forbidden by their §8 and review §5; **not** an improvement, does not reset the counter |
| Count H2's "no-claim" gates as NA (rejected) | Same artefact in miniature; contradicts the Gen 1 silent-omission=INS convention. Not adopted |
| Score R1 leg (a) PROVISIONAL-SIGNAL | Collapses to INSUFFICIENT (adapter rule; v2 GRADE/tier enforcement). Even the inflated reading retires nothing |
| Score design-adequate cells as provisional (rejected, as Gen 1) | Bit-identical collapse to INSUFFICIENT. No improvement manufacturable |
| G1-NA counted INSUFFICIENT; G2↔G3a/G3b order swaps; G1 anchors | All candidates move together / all keys NA. Ties unchanged |
| Evidence-completeness (disclosed inverse) | Gen 2 goes *backwards* again: 33 design cells, of which exactly 1 references (abstract-level) results — vs parents' study rows. Paperwork order ≠ merit |

**STOP check, GOAL §7 rule 5 — updated:**

| Condition | Status after this re-score |
|---|---|
| (a) Track-P candidate frozen for handoff | **Not met.** Structurally impossible while G3b BLOCKED; 0 PASS |
| (b) generation conjunct: two consecutive generations, no lexicographic improvement | **Now met: counter 2/2.** Gen 1 (1/2, Step 4 §2) + Gen 2 (this re-score: both promotable children tie their parents; Q1/R1 cannot count as improvements — §1 artefact rejected). This is the exact outcome fitness §1/§6 and the sweep §5.3 predicted for scoring a design-only Gen 2, and it is spent under holder direction, triage-only, with the Gen 2 protocol/freeze still owed (breach disclosed §1) |
| (b) gaps conjunct: **all** promotion-blocking gaps ≥2 independent attacks | **Not met, unchanged.** Round-2 §2/§5 stands: gaps 1 (human gates), 2 (G3b), 5 (pins/margins), 8 (human-reversible) at **0/2**; gaps 3/4 at 1 (4 partial); gap 6 + gap-7/full-texts the only ≥2. Gen 2 *designs* are not completed attacks: Q1 files the first Q0-decider **design** (gap 4 still 1 partial, zero data), R1 files the first G4-AAV falsification **design** (AAV-re-dosing still **0/2 completed** — the deciding extraction of 42362868 has not happened), H2 files a design against one gap-5 pin (SD scale; still 0 pins ratified). Designs aim future attacks; they are not attacks |
| (c) Budget exhausted (`partial`) | Not stated. Not met |
| Max-4 clock | **2/4** |

**⇒ STOP not met** — but the margin has narrowed in the
worst way: only the un-attacked-gaps conjunct now stands
between the loop and a (b)-stop, and a *third*
consecutive design-only generation would add nothing
except clock (3/4) while the same conjunct does all the
work. The cheapest counter-relevant moves are no longer
designs: they are the owed attacks themselves (human
extraction of PMID 42362868 = first real R1 leg-(a)
attack; Q1 freeze-addendum → executed T2 study; A1
kill-test run; G3b co-design — review §7). Saying
"discovery may continue" without that sentence would be
exactly the dishonest counter advance round-2 §5 warned
about; with this re-score the advance is at least
recorded, evidenced, and tied to a genuinely-new-design
generation (review §6 permission), not a rewording.

**Retire/promote:** nothing promoted, resurrected, or
newly retired. P2/H2 join the non-promoting survivors;
Q1/R1 are live designs with no survivor semantics until
executed; H2b stays retired-at-birth; B/C/D/E statuses
and all G4-AAV applications unchanged. FROZEN retained.

## 5. Kill status (all unevaluable; none triggered, none cleared)

| candidate | kill state after re-score |
|---|---|
| GEN2-P2 | Evaluable-by-design (I1\* process leg crisp), NOT EVALUATED — no protocol opened, distributional margin + attributable-delay conventions unratified |
| GEN2-H2 | (a\*) scoreability kill defined, tolerance unratified, no sample; inherited (a)/(b) not evaluable by H2; **harm not cleared** |
| GEN2-Q1 | No executed form to judge against S2.3 minima; Q0 UNDECIDABLE-no-data in both directions — LOST and RETAINED premises both alive |
| GEN2-R1 | No leg has met either its retire or its confirm standard; presumption stands *untested*, now with named tests. Leg (a) has a provisional signal against its strong form — a signal is not a retirement |

## 6. Unresolved (what would move the next re-score)

1. **Humans first, as before:** Gen 2 protocol + freeze
   checklist + held-out-manifest update (owed *before*
   this scoring), dual extraction, H-1…H-8. Until then
   every row above is UNASSESSED triage.
2. **G3b co-design (B01)** — still the sole structural
   bar to any promotion and the review's highest-leverage
   action; untouched by Gen 2.
3. **First real attacks the Gen 2 designs license:**
   human full-text dual extraction of PMID 42362868 +
   ChiCTR2200063181 (R1 leg a — the only Gen 2 item that
   could *retire something* without a new trial);
   Q1 freeze addendum (species/construct/dose/N from
   inspected sources) → executed T2 decider; H2
   stakeholder discordance-tolerance + instrument
   ratification; P2 NI-margin/attributable-delay
   ratification. All conventions above remain
   sensitivity-only until ratified.
4. **Scorer cell-manifest repair** (review §5) — without
   it, Q1/R1-class candidates can never enter a matrix
   honestly, and future mixed PASS/INSUFFICIENT records
   remain unsafe in the reducer (v2 fixed grade/tier +
   mechanism rows only).
5. Validation set = **0**; re-sweep on the stated
   cadence with frozen strings (sweep §5.1/§6). Any
   post-freeze results (NCT07752888 first) need a human
   siding amendment *before* opening. Post-freeze edits
   to any candidate = new candidate.

**Prohibitions D1–D17 carry verbatim.** No yield-as-
pathway (D6), no CHORD-to-routing credit (D13), no
patency/Q0 numbers from revision series, contralateral
re-dose, or titles; kills never "survived/cleared"
(D10); H harm *not cleared*; 42362868 is DESIGN, never
"validation"; no ranking above is a winner claim;
**FROZEN retained by default. G3b BLOCKED.**

*Files: `extract-gen2.csv`, `adapted-gen2.csv`,
`adapt-gen2-note.md`, `gate-matrix-gen2.md` (this
directory); build script `/tmp/build_gen2_extract.py`;
combined/artefact checks `/tmp/combined_gen12.md`,
`/tmp/combined_qr.md` (scratch, not committed evidence).
Inputs: GOAL §7; `gen01/Step4-gen1-summary.md`;
`reviews/codex-astra-external-review.md` §5–§6;
`gaps/round2-summary.md` §2/§4–§6;
`gen02/{fitness-application,new-evidence-sweep,
candidate-P2/H2/Q1/R1}`; `gen01/scoring/score-gen1.md`.*
