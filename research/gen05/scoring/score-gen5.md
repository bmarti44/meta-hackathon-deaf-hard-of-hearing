# Gen 5 score — I1 / I2 / J1 / K1 / P5 vs frozen; combined Gen 0–5 fitness; cell-movement audit

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Scored **2026-11-03. Gen 5 under
> GOAL v2.3** (§7 rule 5: no generation cap, no loop stopping
> rule — the v2.2 clock/STOP machinery is superseded and is not
> applied, reported, or revived; per-candidate kills and FMEA
> harm stops are kept as falsifiability/safety, §5).
> **Authority:** agent score = triage only. Human dual
> extraction, protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: no PASS. `promoted FALSE` ×5. G3b BLOCKED.
> FROZEN retained. One flagged difference vs Gen 1–4 filings:
> I1/I2/K1 each carry a real G4 FAIL cell (G4-AAV presumptive
> FAIL, Gen 0 C/D precedent) — Gen 5 is the first generation
> since Gen 0 to file FAILs, and they are entries, not
> regressions: no Gen 0–4 cell moves. P5 ties GEN4-P4 (and
> every earlier joint-best pathway) cell-for-cell at 0 FAIL /
> 6 INSUFFICIENT — the fifth consecutive scored generation
> with zero lexicographic improvement, confirming
> `gen05/fitness-application.md` §1's in-advance prediction
> ("0 FAIL — presumptive G4-AAV excepted — / all-INS,
> promoted FALSE, movement expected zero") exactly, including
> its exception. J1 is unfielded (HP-J1-4 unsigned) and scores
> only in a separate conditional run.**

## 1. Method — same bar, design-only rule, manifest treatment

**PASS bar unchanged (Gen 0–5):** ≥Moderate *human-verified*
GRADE **and** Appendix A v1 minimum tier, enforced by scorer
v2 (`effective_verdict`, `is_mechanism_only`) — both no-ops
here (0 PASS proposed, 0 G2 W0/W1 rows). All 40 rows
RECORD/UNASSESSED; INSUFFICIENT never passes, never safety
(D10/D17); G3b BLOCKED forces INSUFFICIENT + `promoted FALSE`.

**Design-only rule (as Gen 1–4).** All five candidates state
"scores nothing": registry existence (NCT07627971 recruiting,
no results), frozen decision-rule skeletons (I2), adult T3
lab gains vs stale baselines (J1), and T1 mouse rescue
(I1/K1) make cells *evaluable-by-design* only. Rejected as
PASS inflation: counting SONIX's existence as an I1 signal
(candidate §3 bars it), counting I2's rule crispness over I1
(same evidence — adapted rows verified identical modulo ID),
counting J1's adult intelligibility gains toward the ≥3 dB
pediatric bar vs the *current commercial processor* (no
inspected record for that comparator exists), and filling
any dose/capsid/N blank from anything but an inspected full
record (HP-I1-1, HP-I2-1, HP-K1-1 — all unsigned, all cells
dose-dependent therefore INSUFFICIENT).

**The G4-AAV exception — FAILs filed, not softened.** The
one verdict a design *can* earn today is the presumptive
one: Gen 0 scored C and D `G4-AAV = FAIL` for AAV delivery
without re-dose demonstration, and I1/I2/K1 print the same
presumption in their own Appendix B. Scoring them
INSUFFICIENT would silently promote the new families above
C/D on identical facts. Each files G4-AAV FAIL alongside a
G4 INSUFFICIENT row; worst-verdict sets G4 = FAIL
(`adapt-gen5-note.md`). This is the fitness-application's
printed exception landing as designed, not a surprise and
not a kill (§5).

**Who enters which matrix.** I1/I2/K1 (Track R) + P5
(Track P) enter `gate-matrix-gen5.md` **with `--manifest`**
(`manifest-gen5-main.csv`, 28 rows; declarations verified:
P5 ≡ P4 modulo ID, I2 ≡ I1). J1 gets a **conditional
single-candidate `--manifest` run** and appears in no shared
ranking/Pareto/fitness key — not a scope artefact (it
declares 6 applicable gates and the forced probe ties it at
0/6, §4) but its own fielding gate: HP-J1-4 (G1=NA) is
unsigned, and its file bars scoring-as-pathway before that
ruling and bars re-scoring as a device if denied. Both runs
report §(f) "all required cells present": every required
cell was filed, so `--manifest` changed no verdict —
verified, not assumed.

**No new validation evidence.** The Gen 5 sweep records are
design inputs for the candidates they motivated
(exploratory-after-seen = Y in every file): PMIDs
41402290/40121530 (I1), 38853168/37030808 (J1),
40968144/40764318/32493795/40059830 (K1), NCT07627971
(no results), NCT06025032 (withdrawn, N=0). **Validation
set remains 0.** No Gen 0–4 cell moves (§3).

**Sequence note.** `gen05/fitness-application.md` §3
declined to run the scorer at design stage. This score runs
under holder/worker direction as the Gen 5 scoring step; it
is triage/sensitivity only and, under v2.3, no stop, clock,
or branch consequence attaches to it either way.

**Files & commands (observed, this session):**

```text
research/gen05/scoring/extract-gen5.csv   40 rows 14-col: INS 35, FAIL 3 (G4-AAV), NA-prereg 2, PASS 0 (built /tmp/build_gen5_extract.py)
$ python3 research/scoring/adapt_extraction.py .../extract-gen5.csv /tmp/g5stock.csv -> adapted 0 rows (A-H map; GEN5 successor still owed)
adapted-gen5.csv 32 rows (P5+I1+I2+K1); adapted-gen5-J1-conditional.csv 8 (manual ID map, adapt-gen5-note.md)
manifests: manifest-GEN5-{I1,I2,J1,K1,P5}.csv (byte-identical to gen05/ filings) + manifest-gen5-main.csv (28 rows)
$ cd research/scoring && python3 gate_table.py ../gen05/scoring/adapted-gen5.csv --manifest ../gen05/scoring/manifest-gen5-main.csv --out ../gen05/scoring/gate-matrix-gen5.md (exit 0)
$ likewise J1 conditional run (exit 0; section (f): no missing required cells in either run; promoted FALSE x5)
$ python3 -m unittest discover  # research/scoring: Ran 27 tests, OK (+ ASTRA PROBES PASS), code unedited
combined: Gen0 adapted_v2 233 + Gen1 41 + Gen2 16 + Gen3 main 16 + Gen4 main 16 + Gen5 main 32 = 354 rows -> /tmp/combined_gen012345.md (scratch, S4)
conditional probe: + J1 (362 rows) -> /tmp/combined_forced5.md (scratch, S1/S4)
```

## 2. Gate matrices (deterministic)

Main run (`gate-matrix-gen5.md` §a, with `--manifest`):

| candidate | track | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INS* |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN5-P5 | P | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN5-I1 | R | INS | INS | INS | INS | **FAIL†** | INS | INS | 1 | 6 |
| GEN5-I2 | R | INS | INS | INS | INS | **FAIL†** | INS | INS | 1 | 6 |
| GEN5-K1 | R | INS | INS | INS | INS | **FAIL†** | INS | INS | 1 | 6 |

Conditional single-candidate run (not fielded; not in any
fitness key):

| candidate | condition | cells | FAILs | INS | note |
|---|---|---|---|---|---|
| GEN5-J1 | HP-J1-4 G1=NA **unsigned** | G1 NA‡, G2–G6 INS | 0 | 6 | if HP-J1-4 signs, enters Track P at 0/6; if denied, withdrawn — never re-scored as a device |

\*Applicable gates. †G4 = worst of G4 INSUFFICIENT
(unmeasured residual-hearing/patency/immunity cells) and
G4-AAV **FAIL** (presumptive, Gen 0 C/D rule; QR4 legs
unretired). ‡Manifest `required=false` with proposed-NA
reason = declared non-claim pending ruling, never "fine."
All numerics NA for all five, as Gen 0–4. Track R order
(I1, I2, K1) and Pareto {P5} ∪ {I1, I2, K1} are name
tie-breaks on NA keys (g1_channels NA, G5 aggregate NA —
no `--fmea` fabricated). No winner.

## 3. Cell-movement audit — vs every prior generation (flagged)

**Gen 0–4 cells: zero movement.** No Gen 5 record is
validation for any earlier candidate; no earlier extraction
row was edited; the combined run (§4) reproduces every
Gen 0–4 cell from `score-gen4.md` §4 unchanged (F/G/H 0/6;
A/B/GEN1-A1 1/6 with disputed G6 FAIL; C 2 FAIL, D 1 FAIL,
E 2 FAIL on Track R; P/W lineages 0/6 throughout). In
particular: G4-AAV presumption is **not** retired for C/D
by anything Gen 5 inspected; Q0 stays UNDECIDABLE-no-data;
A1's kill stays UNEVALUABLE (J1 inherits no A evidence and
its file says so); H harm not cleared.

**P5 vs GEN4-P4 — every cell "=" (verified mechanically:**
adapted rows identical modulo ID; manifest identical modulo
ID). Paper gain, verdict-flat: the *GJB2* decision-time
stratum (M-P5-1) adds a reportable cell that prints
INSUFFICIENT-precision (App. D numerator unpinned, zero
enrolment, HP-P4-4/5 still enrolment-blocking); SONIX
results are barred as P5 effects (D13 extended in print).
The mutation is decidable-against-the-current-world, not
fitter. Its per-stratum branch kill (collapse to P4) is
unevaluated (§5).

**I2 vs I1 — every cell "=" (verified mechanically).**
M-I2-1 freezes decision rules (sentinel staging, ≤3 dose
levels, rescue-to-CI, 3/N safety bounds) around named
blanks; identical evidence, identical cells, including the
joint G4-AAV FAIL. I2 does not outrank I1 on paperwork —
the combined Track R name order (I1 before I2) is the
tie-break, not a result.

**New-family entries (movement of the frontier, not of any
existing cell):**

- ⚑ **First FAIL cells filed since Gen 0.** I1/I2/K1 enter
  Track R at **1 FAIL / 6 INS**, tying D (1/6) and ahead of
  C/E (2 FAILs) *on FAIL count alone*. **This must not be
  read as Track R improvement:** the Track R ranking key
  (G1 channels, then G5 aggregate) is NA/NA for all six
  candidates, so the scorer returns a six-way name
  tie-break; and C/E's second FAILs came from *evidence
  rows* (G6/G5) that Gen 5 candidates have not yet lived
  long enough to file — the disclosed evidence-completeness
  inverse again (40 design rows vs Gen 0's 233 evidence
  rows). Fewer FAILs here means less examined, not better.
- ⚑ **J1 would tie the Track P joint best if fielded**
  (forced probe: rank-inside-tie at 0/6, `/tmp/combined_forced5.md`)
  — flagged and withheld: HP-J1-4 unsigned ⇒ unfielded ⇒
  no fitness. Quoting J1 at 0/6 against any pathway before
  that ruling repeats the QR/AD error in a new costume.
- K1 additionally files its G4 FAIL with the
  irreversible-edit disclosure and carries PMID 32493795's
  transient-rescue pattern as a standing class warning in
  claim text; its D-style advance criterion (replicated
  ≥6 mo durable restoration, mature animal, genome-wide
  off-target) is unmet and unevaluated.

## 4. Combined Gen 0–5 fitness table

Combined run (354 adapted rows, scratch
`/tmp/combined_gen012345.md`; Track P lexicographic key:
veto → FAILs → INS → numerics, all NA; Track R: G1 → G5
aggregate, both NA for every candidate):

| Gen | Track P at joint-best 0 FAIL / 6 INS | Track P below joint-best | Track R (watch; key NA/NA, name order only) | Non-comparable / unfielded (never in any key) |
|---|---|---|---|---|
| 0 | F, G, H | A, B (1 FAIL / 6 INS, disputed G6) | C (FAIL G4,G6), D (FAIL G4), E (FAIL G5,G6) | — |
| 1 | GEN1-F1m, -Ga, -H1, -P1 | GEN1-A1 (1/6, carried G6 FAIL) | — | — |
| 2 | GEN2-H2, -P2 | — | — | GEN2-Q1, -R1 (extract-only) |
| 3 | GEN3-P3, -W3 | — | — | GEN3-QR3, -AD3 (single-candidate 0/3) |
| 4 | GEN4-P4, -W4 | — | — | GEN4-QR4, -AD4 (single-candidate 0/3) |
| 5 | **GEN5-P5** | — | **GEN5-I1, -I2, -K1 (each FAIL G4† / 6 INS)** | **GEN5-J1 (conditional 0/6, HP-J1-4 unsigned)** |

Fourteen Track-P pathways (F, G, H + 4 Gen 1 + 2 Gen 2 +
2 Gen 3 + 2 Gen 4 + P5) sit at **0/6, all numerics NA, all
`promoted FALSE`**; then A, B, GEN1-A1 at 1/6. Six Track-R
candidates (C, D, E, I1, I2, K1) sit on an NA/NA key.
Within-tie order is a name tie-break, not fitness and not
a winner claim. **No candidate in six scored generations
(0–5) has ever improved lexicographic fitness over Gen 0's
joint best.** Under v2.3 that sentence is a description,
not a stop trigger: no cap, no loop stop, no branch is
owed or taken. Sensitivities (all rejected or flat): force
J1 in → 0/6 tie for an unfielded candidate (observed,
withheld, §3); file G4-AAV as INSUFFICIENT → I1/I2/K1 at
0/7, falsely above D — refused (§1); count registry
existence, I2 rule-freezing, or adult T3 gains as results →
rejected (§1); reorder §7 steps 3–7 → all NA, ties
unchanged; evidence-completeness (disclosed inverse) →
Gen 5 backwards (40 design cells over abstract/registry
records; animal Ns and all doses absent).

**Retire/promote:** nothing promoted, resurrected, or newly
retired in any generation. P5 joins the non-promoting
survivors as P4's current form (P4 not retired — P5's branch
kill collapses *to* P4); I1/I2/K1 join the Track R
watch-list beside C/D/E; J1 awaits a human ruling to exist
as a scored candidate at all. All Gen 0–4 dispositions
unchanged (A1 decline-to-retire carries; H2b
retired-at-birth). Step 5's no-winner decision stands.
FROZEN retained.

## 5. Kill status (none triggered, none cleared — D10)

| candidate | state |
|---|---|
| GEN5-P5 | All P4 kills inherited (Ga, H-arm/I2, I1* process FAIL, I3, M-5 scoreability) + M-P5-1 per-stratum branch kill (collapse to P4); no cohort — all unevaluated |
| GEN5-I1 | Anchor kill (SONIX no ABR signal / G5 signal at ≥Moderate) unevaluated; NCT07627971 has no results (est. primary completion 2027-12) |
| GEN5-I2 | Desk-kill arm live: HP-I2-1 blanks cannot yet be filled from an inspected record — design is *retireable on that ground today* by its own print, but retirement is a human act; Stage-A kills unevaluated (no Stage A data exist) |
| GEN5-K1 | Per-variant kills + D-style advance criterion unevaluated/unmet; NCT06025032 withdrawal (N=0) is fragility evidence, not a kill event for K1 as filed |
| GEN5-J1 | ≥3 dB / quiet-NI / wear-time kills unevaluated; desk-kill (HP-J1-1/2 unfileable) and fielding gate (HP-J1-4) both pending human/source acts |
| G4-AAV (I1/I2/K1) | Presumptive FAIL is a filed cell, **not** a triggered kill and **not** a cleared veto: it retires only via QR4 legs; it blocks any Track-P/preservation reading until then |

## 6. Unresolved — owed-work register (Gen 5 increment)

1. **Humans:** dual extraction of all sweep PMIDs/NCTs (full
   texts; animal Ns and doses the abstracts lack — I1/I2/K1
   dose cells are INSUFFICIENT *by design* until then);
   HOLDER-PIN rulings HP-J1-4 (J1's existence gate), HP-I1-4
   (Track-P G-interface), HP-I1-1…3, HP-I2-1…3, HP-J1-1…3,
   HP-K1-1…3, HP-P4-1…6 + HP-P5-*; App. D P0 numerators;
   G3b co-design (sole structural promotion bar, untouched
   by five generations); manifest/class ratification;
   `GEN-*` adapter successor (stock still adapts 0 rows);
   Gen 5 protocol/freeze/held-out.
2. **Search completeness:** Embase/EU CTIS/ChiCTR/ANZCTR
   unsearched — every absence claim bounded to
   PubMed + ClinicalTrials.gov as inspected 2026-11-03.
3. **Validation set = 0** after Gen 5. Monitoring: quarterly
   dated re-sweep of NCT07627971 (est. 2027-12) and
   NCT07032038; SONIX results, when they exist, are held-out
   validation for I1/I2 — never retrofitted design. Under
   v2.3 the loop continues on that queue.

**D1–D17 carry verbatim.** No ranking is a winner; no
cross-track or 0/3-vs-0/6 comparison; J1's conditional 0/6
is not quoted as fitness; presumptive FAIL ≠ kill ≠ cleared;
kills never survived/cleared; H harm not cleared; Q0
UNDECIDABLE-no-data; A1 UNEVALUABLE; G4-AAV presumption
stands for C/D/I1/I2/K1 alike; registry existence is never
a signal; doses absent from inspected records stay blank.
**FROZEN retained. G3b BLOCKED. No PASS, no winner — and
under v2.3, no stop.**

*Files (this directory): `extract-gen5.csv`,
`adapted-gen5.csv`, `adapted-gen5-J1-conditional.csv`,
`adapt-gen5-note.md`, `manifest-GEN5-{I1,I2,J1,K1,P5}.csv`,
`manifest-gen5-main.csv`, `gate-matrix-gen5.md`,
`gate-matrix-gen5-J1-conditional.md`. Build script
`/tmp/build_gen5_extract.py`; scratch
`/tmp/combined_gen012345.md`, `/tmp/combined_forced5.md`,
`/tmp/g5stock.csv`. Inputs: `gen05/{candidate-I1/I2/J1/K1/P5,
manifest-GEN5-*,fitness-application.md,broaden-sweep.md}`;
`gen04/scoring/{score-gen4.md,adapt-gen4-note.md,
extract-gen4.csv,adapted-gen4.csv}`;
`gen04/Gen4-summary.md` §6; `Step5-decision-no-winner.md`;
Gen 0 `extraction_v2_2026-11-02.csv` (G4-AAV precedent rows
C/D inspected this session); adapted inputs Gen 0–4 as
listed in §1.*
