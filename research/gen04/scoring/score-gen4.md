# Gen 4 re-score (FINAL) — P4 / W4 / QR4 / AD4 vs Gen 3 parents; combined Gen 0–4 fitness; clock 4/4

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Holder Sisyphus directive;
> scored 2026-11-03. GOAL v2.2.
> **Gen clock: Gen 4 = generation 4 of max 4 (4/4). After
> Gen 4 the generation clock is exhausted without new
> external evidence** (an executed attack result, a
> post-freeze validation record under human siding amendment,
> or a documentary object that did not previously exist) —
> and a Gen 5 additionally requires humans to re-open the
> clock by signed amendment. Agent filings can do neither.
> **Authority:** agent re-score = triage only. Human dual
> extraction, protocol/freeze/held-out update, H-1…H-8,
> manifest/class/convention ratification, ~20 HOLDER-PIN
> rulings: **PENDING**.
> **Headline: no PASS, no FAIL, G3b BLOCKED, `promoted
> FALSE` ×4, FROZEN retained. P4/W4 tie P3/W3 (and every
> earlier joint-best pathway) cell-for-cell at 0 FAIL /
> 6 INSUFFICIENT — the fourth consecutive generation with
> zero lexicographic movement, exactly as
> `gen04/fitness-application.md` §1 predicted in print
> before any scorer ran ("0 FAIL / all-INS, promoted
> FALSE… finalization moves evaluability, not evidence").
> This run confirms that prediction; it is not progress
> and must not be narrated as surprise. QR4/AD4 are
> non-promotable classes in separate manifest runs; their
> 0/3 is scope, not fitness. STOP is still not met —
> the loop ends by clock exhaustion (4/4), not by STOP.
> That distinction is the terminal record's first line.**

## 1. Method — same bar, finalization rule, manifest treatment, disclosed breach

**PASS bar unchanged (Gen 0–4):** ≥Moderate *human-verified*
GRADE **and** Appendix A v1 minimum tier, enforced by scorer
v2 (`effective_verdict`, `is_mechanism_only`) — both no-ops
here (0 PASS proposed, 0 G2 W0/W1 rows). All 34 rows
RECORD/UNASSESSED; INSUFFICIENT never passes, never safety
(D10/D17); G3b BLOCKED forces INSUFFICIENT + `promoted FALSE`.

**Finalization rule (Gen 4 form of the design-only rule).**
P4/W4/QR4 state "scores nothing": exact flip definition
(M-5), precision gates (M-6/7), frozen SII bands, executable
Stage 0/1 checklists make cells *evaluable-by-design* only.
Rejected as PASS inflation: counting frozen-form crispness,
checklist completeness, or PROPOSED-FROZEN conventions as
results. PROPOSED-FROZEN ≠ ratified; every HOLDER-PIN is
unsigned.

**AD4 is the one exception — and it still moves no cell.**
AD4 *executed* AD3's documentary protocol at agent scope
(§3). Its output is an absence: no filed pin, no model run,
no kill verdict. Evidence about documentability is not a
gate cell.

**Who enters which matrix.** P4/W4 enter
`gate-matrix-gen4.md` **with `--manifest`**
(`manifest-gen4-P4W4.csv`; declarations verified identical
to Gen 3 modulo ID). QR4/AD4 each get a **single-candidate
`--manifest` run** and appear in no shared ranking/Pareto/
fitness key (`adapt-gen4-note.md`: forcing them in ranks
AD4/QR4 1st/2nd at 0/3 over every pathway at 0/6 — observed
again, rejected again). All three runs report §(f) "all
required cells present": every required cell was filed
INSUFFICIENT, so `--manifest` changed no verdict —
verified, not assumed. **No 0/3-vs-0/6 cross-class
comparison, ever.**

**No new validation evidence.** Gen 4 ran no sweep;
**validation set remains 0**. The one evidence-touching row
(QR4 G4-AAV leg a, PMID 42362868) is inherited verbatim as
PROVISIONAL-SIGNAL → INSUFFICIENT under its printed ceiling
(paper alone cannot retire leg (a)). AD4's execution is new
*documentary* evidence about a source class, not validation
of any candidate. No Gen 0–3 cell moves.

**Sequence breach, fourth filing, disclosed.**
`gen04/fitness-application.md` recommends **no Gen 4
scoring** until Gen3-summary §4's sequence lands, and §4.7
said if no attack can land "the correct act is no Gen 4 at
all." This re-score (like the Gen 4 filing itself) runs
under holder/worker direction against that printed advice;
it is triage/sensitivity only. Disclosure does not cure
the breach. Scoring does not reset the no-improvement
counter and does not re-open the clock.

**Files & commands (observed, this session):**

```text
research/gen04/scoring/extract-gen4.csv   34 rows 14-col: INS 21, NA-prereg 12, PROV-SIG 1, PASS 0, FAIL 0 (built /tmp/build_gen4_extract.py)
$ python3 research/scoring/adapt_extraction.py .../extract-gen4.csv /tmp/g4stock.csv -> adapted 0 rows (A-H map; GEN4 successor still owed)
adapted-gen4.csv 16 rows (P4+W4); adapted-gen4-QR4.csv 11; adapted-gen4-AD4.csv 7 (manual ID map, adapt-gen4-note.md)
manifests: manifest-GEN4-{P4,W4,QR4,AD4}.csv (byte-identical to gen04/ filings; declarations = Gen3 modulo ID, verified) + manifest-gen4-P4W4.csv
$ cd research/scoring && python3 gate_table.py ../gen04/scoring/adapted-gen4.csv --manifest ../gen04/scoring/manifest-gen4-P4W4.csv --out ../gen04/scoring/gate-matrix-gen4.md (exit 0)
$ likewise QR4/AD4 single-candidate runs (exit 0 each; section (f): no missing required cells; promoted FALSE x4)
$ python3 -m unittest discover  # research/scoring: Ran 27 tests, OK (+ ASTRA PROBES PASS), code unedited
combined: Gen0 adapted_v2 233 + Gen1 41 + Gen2 16 + Gen3 main 16 + Gen4 main 16 = 322 rows -> /tmp/combined_gen01234.md (scratch, S4)
rejected-artefact probe: + QR4/AD4 (340 rows) -> /tmp/combined_forced4.md (scratch, S1/S4)
```

## 2. Gate matrices (deterministic)

Main run (`gate-matrix-gen4.md` §a, with `--manifest`):

| candidate | parent | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INS* |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN4-P4 | GEN3-P3 | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |
| GEN4-W4 | GEN3-W3 | NA | INS | INS | INS | INS | INS | INS | 0 | 6 |

Single-candidate manifest runs (not fitness-comparable):

| candidate | parent | cells | FAILs | INS | note |
|---|---|---|---|---|---|
| GEN4-QR4 | GEN3-QR3 | G4 INS§, G5 INS, G3b INS‡, G1/G2/G3a/G6 NA† | 0 | 3 | track `P` is scorer placeholder only; no stage executed |
| GEN4-AD4 | GEN3-AD3 | G1 INS, G5 INS, G3b INS‡, G2/G3a/G4/G6 NA† | 0 | 3 | executed absence is not a cell (§3); A1's G6 FAIL stays on A1 |

\*Applicable gates (main run only). †Manifest
`required=false` with inherited §8 reasons = declared
non-claims, never "fine." ‡Scorer forces G3b INSUFFICIENT
(BLOCKED) despite `false` declaration. §QR4 G4 = worst of
Q0-P INS, Q0-A INS, leg (a) PROV-SIG→INS, leg (b) INS,
leg (c) INS; nothing retired. All numerics NA for all
four, as Gen 0–3. Main-run order (P4 above W4) and Pareto
{P4, W4} are name tie-breaks. No winner.

**Cell-by-cell vs parents — every cell "=".**
P4 vs P3: G1 NA→NA; G2/G3a/G4/G5/G6 INS→INS; G3b INS
(BLOCKED). Paper gain, verdict-flat: flip definition now
exact (M-5), scale-B/contrast precision gates stated
(M-6/7), enrolment barred until HP-P4-4/5 — signed cells
remain INSUFFICIENT-unscoreable-scale until run/elected;
scoreability kill defined, unevaluated. W4 vs W3: identical
pattern; bands (SII <0.35/0.35–0.65/>0.65), interaction
contrast and band kill now exact but PROPOSED-FROZEN;
HP-W4-2 enrolment-blocking; signed cells still not claimed
(P4 owns scale). QR4 vs QR3: same footprint, same cells;
Stages 0–1 now executable, no stage executed, Stage 2
excluded; **Q0 UNDECIDABLE-no-data; G4-AAV presumption
stands in every leg.** AD4 vs AD3: §3.

## 3. AD4 execution + the A1-model question — condition NOT met, no re-run

**What AD4 did (inspected here, not just cited):**
`ad4-extraction-record.csv` + `candidate-AD4-…md` §2:
5 FDA documents fetched from `accessdata.fda.gov`
2026-11-03, hashed, full-text searched with pypdf 6.21.4 —
3 SSEDs (MED-EL P000025/S134; AB P960058/S167; Cochlear
P970051/S172) + Cochlear 686-pp Physician's Package Insert
+ MED-EL P000025C (scanned, 0 extractable text). Result:
**charge-density / µC-per-phase / pulse-width /
contact-area / max-current / battery-hours specifications
are ABSENT from every inspected document.** The only
electrical numbers found — stimulation **720–2400
Hz/channel (total 5760–14400 Hz, 6–20 channels/maxima,
Nucleus 24 CIS/ACE)** — are clinical programming ranges,
**explicitly not P-2 fields**. Per-pin triage (not
declarations): P-1 PARTIAL (devices named, per-contact
areas absent); **P-2 NOT FILEABLE from this class**; P-3
NOT FILED; P-4 untouched; P-5 ASSUMED map stands.

**Therefore the commissioned conditional — "if AD4 found
real device specs, re-run the A1 model with them flagged
agent-extracted" — does not trigger.** Verified in source
this session: `research/gaps/a1_model/model.py` PARAMS
still carry `shannon_k_limit 1.85` (sens 1.5/1.79/2.0),
`contact_area_cm2 0.003`, `pulse_width_us 25.0`, all
labelled ASSUMED in-source ("no named device filed in
workspace"). Substituting stimulation rates for any of
these would be pin-shopping (D-AD3-1) and is refused.
Independently, **no solve is licensed at all** until
HP-AD4-1 signs/replaces the R-1 convergence criterion
(AD4 §4). **A1's kill therefore remains UNEVALUABLE**
(the artefact attack's split verdict carries verbatim:
grade-3/0.25 mm zero retired as grid artefact; magnitudes
unconverged; case not rehabilitated), its disputed G6
FAIL remains on GEN1-A1, and decline-to-retire carries.
AD4 vs AD3 is **not comparable as improvement**: same two
required cells, both still INS; AD4's gain is knowledge
about where pins *aren't*, usable by humans to aim at
other source classes (manufacturer manuals, PMA device
sections) or to declare UNEVALUABLE-documentary — a human
act (AD4 §5). Even a successful future pin filing +
model run could never PASS any gate (agent-triage/UNASSESSED
rows; T0 can never PASS G1 — A1 §8); at most it would make
the kill evaluable.

## 4. Combined Gen 0–4 fitness table; clock 4/4; STOP final state

Combined run (322 adapted rows, scratch
`/tmp/combined_gen01234.md`; Track P lexicographic key:
veto → FAILs → INS → numerics, all NA):

| Gen | Candidates at joint-best 0 FAIL / 6 INS | Below joint-best | Non-comparable classes (never in this key) |
|---|---|---|---|
| 0 | F, G, H | A, B (1 FAIL / 6 INS, disputed G6) | C, D, E (Track R watch-list; FAILs 2/1/2) |
| 1 | GEN1-F1m, -Ga, -H1, -P1 | GEN1-A1 (1/6, carried G6 FAIL) | — |
| 2 | GEN2-H2, -P2 | — | GEN2-Q1, -R1 (extract-only) |
| 3 | GEN3-P3, -W3 | — | GEN3-QR3, -AD3 (single-candidate 0/3) |
| 4 | **GEN4-P4, -W4** | — | GEN4-QR4, -AD4 (single-candidate 0/3) |

Thirteen Track-P pathways (F, G, H + 4 Gen 1 + 2 Gen 2 +
2 Gen 3 + 2 Gen 4) sit at **0/6, all numerics NA, all
`promoted FALSE`**; then A, B, GEN1-A1 at 1/6. Within-tie
order is a name tie-break, not fitness and not a winner
claim. **No candidate in five scored generations (0–4) has
ever improved lexicographic fitness over Gen 0's joint
best.** Sensitivities (all rejected or flat): force
QR4/AD4 in → spurious 0/3 lead (observed `/tmp/combined_forced4.md`);
score PROV-SIG leg (a) → collapses INS; count finalization
crispness or AD4's executed absence as a result → rejected
(§1/§3); reorder §7 steps 3–7 → all NA, ties unchanged;
evidence-completeness (disclosed inverse) → Gen 4 backwards
again (34 design cells, 1 inherited abstract-level
reference, 1 executed documentary absence that is not a
cell).

**STOP check (GOAL §7 rule 5) — FINAL state at 4/4:**

| Condition | Status |
|---|---|
| (a) Track-P frozen for handoff | **Not met** — 0 PASS in 4 generations; structurally impossible while G3b BLOCKED |
| (b-i) Two consecutive generations, no improvement | **Met at Gen 2; now four consecutive** (Gen 1, 2, 3, 4 each tie). Counter over-met; finalization/scoring does not reset it |
| (b-ii) All promotion-blocking gaps ≥2 independent attacks | **Not met** — gaps 1 (human gates), 2 (G3b), 5 (pins/margins), 8 (human-reversible) at **0/2 as gaps**. Gen 4 designs are not attacks. AD4 is **one** executed documentary attack on gap 5's A1 sub-pin set (agent scope, human confirmation owed) — at most 1 attack on one sub-item, not ≥2 on the gap |
| (c) Budget exhausted | Not stated |
| Max-4 clock | **4/4 — EXHAUSTED.** No Gen 5 without new external evidence **and** human clock amendment |

**⇒ STOP still not met**, held solely by (b-ii), for the
third consecutive filing. The loop ends not by STOP but
by exhaustion. Endgame (pre-committed in
`gen04/fitness-application.md` §5, unchanged by this
score): **Branch A** (handoff) unavailable; **Branch B**
((b)-STOP) pending-execution of the fully specified attack
queue; **Branch C (honest terminal record, FROZEN retained)
is today's standing state**; Branch D rejected in advance.

**Retire/promote:** nothing promoted, resurrected, or
newly retired in any generation. P4/W4 join the
non-promoting survivors as final forms; QR4/AD4 live
non-promotable designs/protocols; all Gen 0–3 dispositions
unchanged (A1 decline-to-retire carries; H2b
retired-at-birth). FROZEN retained.

## 5. Kill status (none triggered, none cleared — D10)

| candidate | state |
|---|---|
| GEN4-P4 | Inherited kills + scoreability kill (exact form); no cohort — unevaluated |
| GEN4-W4 | Inherited kills + band kill (exact form); no bands/data — unevaluated |
| GEN4-QR4 | No stage executed; no leg retired/confirmed; bookkeeping-kill untestable pre-data |
| GEN4-AD4 | No own kill; A1 kill **UNEVALUABLE** (§3); EVALUABLE vs UNEVALUABLE-documentary is a pending *human* declaration |

## 6. Unresolved — the terminal owed-work register

1. **Humans, all of it:** freeze/protocol/held-out update;
   dual extraction (incl. AD4's 5 docs + OCR/visual read of
   P000025C + PMID 42362868); H-1…H-8; ~20 HOLDER-PIN
   rulings (HP-W4-2, HP-P4-4/5 enrolment-blocking; HP-AD4-1
   gates any model solve); G3b co-design (sole structural
   promotion bar, untouched by 4 generations); manifest +
   candidate-class + convention ratification; `GEN-*`
   adapter successor; endgame branch selection (A/B/C).
2. **P-2/P-3/P-4 pins unfound** in the inspected FDA
   SSED/label class; manufacturer-manual / original-PMA
   classes unsearched (named for humans, AD4 §5). Until a
   human files or declares, A1 stays UNEVALUABLE.
3. **Validation set = 0** after 4/4 generations. Monitoring
   per Branch C: frozen sweep strings re-run quarterly as
   new dated files (first 2027-02); human siding amendment
   before opening any post-freeze record (NCT07752888,
   est. 2027-05-31, first). Post-freeze edits = new
   candidate — and at 4/4 there is no generation to absorb
   one without the revival rule above.

**D1–D17 carry verbatim.** No ranking is a winner; no
0/3-vs-0/6; AD4 is not an A1 repair and its triage is not
a declaration; kills never survived/cleared; H harm not
cleared; PMID 42362868 DESIGN never validation; Q0
UNDECIDABLE-no-data; G4-AAV presumption stands;
PROPOSED-FROZEN ≠ ratified; no Gen 5 without new external
evidence + human clock amendment.
**FROZEN retained. G3b BLOCKED. Clock 4/4 — exhausted.**

*Files (this directory): `extract-gen4.csv`,
`adapted-gen4.csv`, `adapted-gen4-QR4.csv`,
`adapted-gen4-AD4.csv`, `adapt-gen4-note.md`,
`manifest-GEN4-{P4,W4,QR4,AD4}.csv`,
`manifest-gen4-P4W4.csv`, `gate-matrix-gen4.md`,
`gate-matrix-gen4-QR4.md`, `gate-matrix-gen4-AD4.md`.
Build script `/tmp/build_gen4_extract.py`; scratch
`/tmp/combined_gen01234.md`, `/tmp/combined_forced4.md`,
`/tmp/g4stock.csv`. Inputs: `gen04/{fitness-application,
candidate-P4/W4/QR4/AD4,manifest-GEN4-*,ad4-extraction-record.csv}`;
`gen03design/Gen3-summary.md` §4 + `scoring/score-gen3.md`;
`gen02/Gen2-summary.md`; `gen01/candidate-A1-killtest.md`;
`gaps/a1_model/model.py` (PARAMS inspected, not run);
adapted inputs Gen 0–3 as listed in §1.*
