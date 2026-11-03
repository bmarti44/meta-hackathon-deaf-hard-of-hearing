# Gen 6 score — P6 / J2 vs frozen; combined Gen 0–6 fitness; cell-movement audit

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Scored **2026-11-03. Gen 6 under
> GOAL v2.3** (§7 rule 5: no generation cap, no loop stopping
> rule — v2.2 clock/STOP machinery superseded, not applied,
> reported, or revived; per-candidate kills and FMEA harm stops
> kept as falsifiability/safety, §5).
> **Authority:** agent score = triage only. Human dual
> extraction, protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: no PASS. `promoted FALSE` ×2. G3b BLOCKED.
> FROZEN retained. ⚑ Zero Gen 0–5 cells move (mechanically
> diffed, §3). P6 ties GEN5-P5/GEN4-P4 cell-for-cell at
> 0 FAIL / 6 INSUFFICIENT — the sixth consecutive scored
> generation with zero lexicographic improvement, confirming
> Gen5-summary §4.7's prediction and candidate-P6's own
> in-advance fitness note. J2 is unfielded (HP-J1-4 still
> unsigned) and scores only in a separate conditional run.**

## 1. Method — same bar, design-only rule, manifest treatment

**PASS bar unchanged (Gen 0–6):** ≥Moderate *human-verified*
GRADE **and** Appendix A v1 minimum tier, enforced by scorer
v2 (`effective_verdict`, `is_mechanism_only`) — both no-ops
here (0 PASS proposed, 0 G2 W0/W1 rows). All 16 rows
RECORD/UNASSESSED; INSUFFICIENT never passes, never safety
(D10/D17); G3b BLOCKED forces INSUFFICIENT + `promoted FALSE`.

**Design-only rule (as Gen 1–5).** Both candidates state
"scores nothing": per-child rule executability against a
recruiting registry record with no results (P6), and a named
comparator plus staged bench→adult→pediatric protocol with
no stage run (J2), make cells *evaluable-by-design* only.
Rejected as PASS inflation: counting R-P6-1…10 crispness over
P5 (same evidence — adapted rows verified identical modulo
ID), counting SONIX eligibility structure as a P6 signal
(branch rules bar it; SONIX/CHORD/DB-OTO results are never P6
effects, D13), counting the manufacturer-run adult SCAN2+
ForwardFocus ~4.2–4.3 dB (PMID 41046328, N=20 adults) or J1's
adult T3 records toward J2's ≥3 dB pediatric bar vs C-J2 (J2
itself bars adult data as pediatric claim and as variance
source), and filling any dose/latency/power/N blank from
anything but an inspected record (HP-I1-1, HP-J2-1/6 — all
unsigned).

**No new FAIL filed — and that is not progress.** Gen 6 files
no G4-AAV row: P6 administers zero product (referred-ear
presumptive FAIL remains GEN5-I1/I2's, filed Gen 5, exactly
as P5) and J2 touches no biology. `attack-gjb2-doses.md`
(full-text PMID 41402290 doses/Ns; PMID 40121530 paywalled,
abstract-only, dose cells left blank) deepens already-seen
DESIGN records and found anti-capsid/redose/biodistribution
searched-absent — it retires no QR4 leg, so the five standing
G4-AAV FAILs (C/D/I1/I2/K1) are untouched. Fewer FAILs in a
two-candidate design generation means less examined, not
better (evidence-completeness inverse, as Gen 5).

**Who enters which matrix.** P6 (Track P) enters
`gate-matrix-gen6.md` **with `--manifest`**
(`manifest-gen6-main.csv`, 7 rows). J2 gets a **conditional
single-candidate `--manifest` run** and appears in no shared
ranking/Pareto/fitness key — HP-J1-4 (G1=NA) remains unsigned
and J2 inherits J1's fence in full (if denied, J1+J2 withdrawn
together, never re-scored as a device). Both runs report §(f)
"all required cells present": `--manifest` changed no verdict
— verified, not assumed. ⚑ P6's manifest is a scoring-step
transcription of its printed §1 declaration (candidate filed
no CSV; J2's was candidate-filed) — `adapt-gen6-note.md`.

**No new validation evidence.** Every Gen 6 record is DESIGN
(exploratory-after-seen = Y): NCT07627971 full record (no
results, est. primary completion 2027-12), PMIDs
41085057/40690227 (external *OTOF* world, D13),
NCT07752888 (N=1 registry pointer, Q0 unchanged),
41402290/40121530 dose attack, J2's manufacturer/journal
comparator records. **Validation set remains 0.** No Gen 0–5
cell moves (§3).

**Files & commands (observed, this session):**

```text
research/gen06/scoring/extract-gen6.csv   16 rows 14-col: INS 14, NA-prereg 2, FAIL 0, PASS 0 (built /tmp/build_gen6.py; EQUIVALENCE OK asserts)
$ python3 research/scoring/adapt_extraction.py .../extract-gen6.csv /tmp/g6stock.csv -> adapted 0 rows (A-H map; GEN-* successor still owed)
adapted-gen6.csv 8 rows (P6); adapted-gen6-J2-conditional.csv 8 (manual ID map, adapt-gen6-note.md)
manifests: manifest-GEN6-P6.csv (transcribed, P6 S1), manifest-GEN6-J2.csv (byte-identical copy of gen06/ filing), manifest-gen6-main.csv (7 rows)
$ cd research/scoring && python3 gate_table.py ../gen06/scoring/adapted-gen6.csv --manifest ../gen06/scoring/manifest-gen6-main.csv --out ../gen06/scoring/gate-matrix-gen6.md (exit 0)
$ likewise J2 conditional run (exit 0; section (f): no missing required cells in either run; promoted FALSE x2)
$ python3 -m unittest discover  # research/scoring: Ran 27 tests, OK (+ ASTRA PROBES PASS), code unedited
combined: Gen0 adapted_v2 233 + Gen1 41 + Gen2 16 + Gen3 main 16 + Gen4 main 16 + Gen5 main 32 = 354 base -> /tmp/combined_base.md (scratch)
combined main6: 354 + P6 8 = 362 rows -> /tmp/combined_gen0123456.md (scratch; base-vs-main6 cell diff = [] )
conditional probe: + J1 + J2 (378 rows) -> /tmp/combined_forced6.md (scratch, S3/S4)
```

## 2. Gate matrices (deterministic)

Main run (`gate-matrix-gen6.md` §a, with `--manifest`):

| candidate | track | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INS* |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN6-P6 | P | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |

Conditional single-candidate run (not fielded; not in any
fitness key):

| candidate | condition | cells | FAILs | INS | note |
|---|---|---|---|---|---|
| GEN6-J2 | HP-J1-4 G1=NA **unsigned** (inherited) | G1 NA‡, G2–G6 INS | 0 | 6 | if HP-J1-4 signs, J-lineage enters Track P at 0/6 (J2 supersedes J1 as design of record only if humans adopt it); if denied, J1+J2 withdrawn — never re-scored as a device |

\*Applicable gates. ‡Manifest `required=false` with proposed-NA
reason = declared non-claim pending ruling, never "fine."
All numerics NA for both, as Gen 0–5. No `--fmea` fabricated.
No winner.

## 3. Cell-movement audit — vs every prior generation (flagged)

**⚑ Gen 0–5 cells: zero movement — verified mechanically,**
not asserted: the 354-row Gen 0–5 base run and the 362-row
main combined run were both executed this session and their
gate matrices diffed candidate-by-candidate (`MOVED = []`,
23 base candidates reproduced identically; sole addition
GEN6-P6). No earlier extraction row was edited. In
particular: G4-AAV presumption not retired for C/D/I1/I2/K1
by the dose attack (no anti-capsid/redose data in either
*GJB2* paper; PMID 40121530 dose cells remain blank behind
paywall); I1's anchor kill still unevaluated (SONIX no
results until ~2027-12 est.); Q0 stays UNDECIDABLE-no-data
(NCT07752888 is a pointer); A1's kill stays UNEVALUABLE;
H harm not cleared; DB-OTO/GT-vs-CI (PMIDs 41085057/40690227)
move no P/I/J cell (D13, held-out rules).

**P6 vs GEN5-P5 — every cell "=" (verified mechanically:**
adapted rows and manifest identical modulo ID, build asserts).
Paper gain, verdict-flat: R-P6-1…10 give the *GJB2* branch
per-child dispositions (age/cohort-inactionable,
never-delay-conflict, eligibility-silent→frozen incl. the
correction that CND/malformation are *not* SONIX exclusions
as inspected) that print INSUFFICIENT-precision (App. D
numerators unpinned, zero enrolment, HP-P4-4/5 enrolment-
blocking, HP-P6-1/2 unsigned — branch executable on paper,
inert in the world until HP-P6-2). Depth bought a falsifiable
process question, not fitness. Branch kill (collapse P6→P5→P4)
unevaluated (§5).

**J2 vs GEN5-J1 — every cell "=" (verified mechanically).**
M-J2-1 names C-J2 (child's own Cochlear Nucleus 8/Kanso 3
SmartSound iQ2+SCAN2 as labeled per age band; MED-EL secondary
stratum) and stages bench→adult→pediatric→trajectory gates;
identical verdicts, identical fence. Key Gen 6 narrowing,
recorded not scored: no inspected manufacturer record shows
shipped DNN multi-talker separation — what ships
(classification+NR+beamforming, age-gated) is already worth
~4 dB in manufacturer-run adults, so J2's claim is narrowed
to co-located/diffuse-babble headroom. That shrinks the claim;
it moves no cell.

**Frontier entries (movement of the tie, not of any cell):**

- ⚑ **P6 is the 15th Track-P pathway at joint-best 0/6**
  (combined §b ranks 1–15 all 0 FAIL / 6 INS, numerics NA;
  within-tie order is the name tie-break — GEN6-P6 prints
  14th, H 15th, by spelling, not merit).
- ⚑ **J2 would tie the same joint best if fielded** (forced
  378-row probe: J1 and J2 both 0/6, no base cell disturbed)
  — flagged and withheld: HP-J1-4 unsigned ⇒ J-lineage
  unfielded ⇒ no fitness for either J candidate.
- ⚑ **No FAIL cells filed in Gen 6** (vs 3 in Gen 5) — a
  composition artefact (no new AAV candidate), explicitly
  not Track R improvement; the six Track-R candidates sit
  on the same NA/NA key as Gen 5 left them.

## 4. Combined Gen 0–6 fitness table

Combined main run (362 adapted rows, scratch
`/tmp/combined_gen0123456.md`; Track P lexicographic key:
veto → FAILs → INS → numerics, all NA; Track R: G1 → G5
aggregate, both NA for every candidate):

| Gen | Track P at joint-best 0 FAIL / 6 INS | Track P below joint-best | Track R (watch; key NA/NA, name order only) | Non-comparable / unfielded (never in any key) |
|---|---|---|---|---|
| 0 | F, G, H | A, B (1 FAIL / 6 INS, disputed G6) | C (FAIL G4,G6), D (FAIL G4), E (FAIL G5,G6) | — |
| 1 | GEN1-F1m, -Ga, -H1, -P1 | GEN1-A1 (1/6, carried G6 FAIL) | — | — |
| 2 | GEN2-H2, -P2 | — | — | GEN2-Q1, -R1 (extract-only) |
| 3 | GEN3-P3, -W3 | — | — | GEN3-QR3, -AD3 (single-candidate 0/3) |
| 4 | GEN4-P4, -W4 | — | — | GEN4-QR4, -AD4 (single-candidate 0/3) |
| 5 | GEN5-P5 | — | GEN5-I1, -I2, -K1 (each FAIL G4† / 6 INS) | GEN5-J1 (conditional 0/6, HP-J1-4 unsigned) |
| 6 | **GEN6-P6** | — | — (no new Track R candidate) | **GEN6-J2 (conditional 0/6, HP-J1-4 unsigned)** |

†G4-AAV presumptive FAIL (Gen 0 C/D rule), Gen 5 filing,
unretired in Gen 6. Fifteen Track-P pathways (F, G, H +
4 Gen 1 + 2 Gen 2 + 2 Gen 3 + 2 Gen 4 + P5 + P6) sit at
**0/6, all numerics NA, all `promoted FALSE`**; then A, B,
GEN1-A1 at 1/6. Six Track-R candidates (C, D, E, I1, I2, K1)
unchanged on an NA/NA key. Within-tie order is a name
tie-break, not fitness and not a winner claim. **No candidate
in seven scored generations (0–6) has ever improved
lexicographic fitness over Gen 0's joint best.** Under v2.3
that sentence is a description, not a stop trigger: no cap,
no loop stop, no branch owed or taken. Sensitivities (all
rejected or flat): force J1+J2 in → 0/6 ties for unfielded
candidates (observed, withheld, §3); count registry
eligibility structure, rule executability, dose-attack depth,
or adult/manufacturer SRT gains as results → rejected (§1);
file a P6 G4-AAV FAIL → double-counts I1's product cell
against a zero-product pathway (refused, as P5); reorder §7
steps 3–7 → all NA, ties unchanged; evidence-completeness
(disclosed inverse) → Gen 6 backwards (16 design cells; the
generation's only full-text gain, mouse/NHP doses, is DESIGN
for I-lineage and files no Gen 6 candidate cell).

**Retire/promote:** nothing promoted, resurrected, or newly
retired in any generation. P6 joins the non-promoting
survivors as the P-lineage's current form (P5/P4 not retired —
P6's branch kill collapses *to* them); J2 supersedes J1 as
J-lineage design of record only if humans adopt it, and both
await HP-J1-4 to exist as scored candidates at all. All
Gen 0–5 dispositions unchanged. FROZEN retained.

## 5. Kill status (none triggered, none cleared — D10)

| candidate | state |
|---|---|
| GEN6-P6 | All P4/P5 kills inherited (Ga, H-arm/I2, I1* process FAIL, I3, M-5 scoreability) + executable branch arm (no gain in `referral-actionable` cell; any attributable delay day in pilot audit; empty-actionable-cell dead branch; I1 anchor kill ⇒ auto-close via HP-P5-1); no cohort, no pilot audit — all unevaluated |
| GEN6-J2 | K1 bench desk-kill, K2 adult <3 dB, K3 pediatric <3 dB/precision, K4 quiet/music/localization/alarm/wear-time NI — all unevaluated (no Stage 0–3 data); fielding gate HP-J1-4 pending before any of them can be spent on children |
| G4-AAV (C/D/I1/I2/K1) | Presumptive FAILs stand; Gen 6 dose attack retired no QR4 leg (anti-capsid/redose searched-absent); not triggered kills, not cleared vetoes |

## 6. Unresolved — owed-work register (Gen 6 increment)

1. **Humans:** HP-J1-4 ruling (now gates two J designs);
   HP-P6-1 (silent-state eligibility) + HP-P6-2 (disposition
   ratification — until then no `referral-actionable` may be
   acted on); HP-J2-1…6 (bench measurements, comparator/AB
   file, test pinning, locked N from pilot variance);
   licensed PMID 40121530 full-text extraction (its dose/N
   cells remain INSUFFICIENT); dual extraction + GRADE of
   all resweep records; App. D P0 numerators; G3b co-design
   (sole structural promotion bar, untouched by six design
   generations); manifest/class ratification (incl. the
   transcribed P6 manifest); `GEN-*` adapter successor
   (stock still adapts 0 rows; manual surface now spans six
   generations); Gen 6 protocol/freeze/held-out.
2. **Search completeness:** Embase/EU CTIS/ChiCTR/ANZCTR
   unsearched — every absence claim bounded to PubMed +
   ClinicalTrials.gov as inspected 2026-11-03.
3. **Validation set = 0** after Gen 6. Monitoring: quarterly
   dated re-sweep of NCT07627971 (est. 2027-12; R-P6-10
   auto-freeze on status/results change) and NCT07032038;
   SONIX results, when they exist, are held-out validation
   for I1/I2 — never retrofitted into P6 rules. Under v2.3
   the loop continues on that queue.

**D1–D17 carry verbatim.** No ranking is a winner; no
cross-track or 0/3-vs-0/6 comparison; J1/J2 conditional 0/6
never quoted as fitness; presumptive FAIL ≠ kill ≠ cleared;
kills never survived/cleared; H harm not cleared; Q0
UNDECIDABLE-no-data; A1 UNEVALUABLE; G4-AAV presumption
stands for C/D/I1/I2/K1 alike; registry existence/structure
is never a signal; doses absent from inspected records stay
blank. **FROZEN retained. G3b BLOCKED. No PASS, no winner —
and under v2.3, no stop.**

*Files (this directory): `extract-gen6.csv`,
`adapted-gen6.csv`, `adapted-gen6-J2-conditional.csv`,
`adapt-gen6-note.md`, `manifest-GEN6-P6.csv`,
`manifest-GEN6-J2.csv`, `manifest-gen6-main.csv`,
`gate-matrix-gen6.md`, `gate-matrix-gen6-J2-conditional.md`.
Build script `/tmp/build_gen6.py`; scratch
`/tmp/combined_base.md`, `/tmp/combined_gen0123456.md`,
`/tmp/combined_forced6.md`, `/tmp/g6stock.csv`. Inputs:
`gen06/{candidate-P6,candidate-J2-ai-pediatric,
manifest-GEN6-J2.csv,resweep.md,attack-gjb2-doses.md}`;
`gen05/{Gen5-summary.md §4,candidate-J1/I1/P5 (via parents),
scoring/{score-gen5.md,adapt-gen5-note.md,extract-gen5.csv,
adapted-gen5.csv,adapted-gen5-J1-conditional.csv,
manifest-GEN5-*}}`; `reviews/codex-unstick.md` §2 (DESIGN
dispositions as carried by both candidates); adapted inputs
Gen 0–5 as listed in §1. Prior workflow results 1–2
(resweep+P6; J2+dose attack) used as evidence pointers and
re-inspected at source this session.*
