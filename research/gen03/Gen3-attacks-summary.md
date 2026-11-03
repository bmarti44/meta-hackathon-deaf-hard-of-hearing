# Gen 3 attacks summary — synthesis of `research/gen03/`

> **Model routing (GOAL S9).** Requested: **xhigh**
> (synthesis; caller string "Gen3-attacks synthesis").
> Actual: **`muse-wonder-full-1.0`**. Date: **2026-11-03**.
> Inputs read in full: `attack-scorer-manifest.md`,
> `attack-42362868.md`, `attack-A1-artefact.md`,
> `research/gen02/Gen2-summary.md`,
> `reviews/codex-astra-gen2-review.md`, `STATUS.md`,
> GOAL S7 loop rules; prior workflow results 1–3 via
> handoff (treated as pointers, re-verified below).
> **Headline: three bounded attacks executed, zero gate
> cells changed, zero PASS, zero promotions, zero kills
> moved. What moved is evaluability and rhetoric only:
> the scorer can now tax missing required cells, one
> in-model zero is retired as a grid artefact (direction
> only, magnitudes unconverged), and PMID 42362868 is
> extracted deeper but formally cannot retire R1 leg (a)
> as written. FROZEN retained. G3b BLOCKED. Q0
> UNDECIDABLE-no-data.**

## 1. These attacks are not a generation — clock unchanged

The directory name `gen03/` is a filing location, not a
generation claim. State it exactly:

- **Generation clock: still Gen 2 = 2/4** (GOAL S7 rule 5:
  max 4 generations). **No-improvement counter: still
  2/2.** Neither advanced, reset, nor re-spent here.
- A generation under GOAL S7 rules 1–2 files 4–8 new
  candidates, each completing Appendix B *before*
  scoring. This round filed **zero new candidates**,
  scored **zero candidates to a new verdict**, and was
  commissioned as the opposite of a generation: Astra
  gen2 review S4 ("attacks now, no new design generation
  now"; "a bounded attack/completion round *outside the
  generation counter*. Do not rename gap attacks 'Gen 3'
  to advance the clock"). All three attack headers carry
  the same fence verbatim.
- Nothing in this round licenses calling the next
  candidate batch "Gen 4", counting this round as the
  third consecutive no-improvement generation, or
  claiming the counter was reset by "progress". The next
  real generation, if ever filed, is Gen 3 = 3/4 — and
  S4 below argues it is not yet justified.
- The Gen 2 sequence breach (scoring before protocol +
  freeze checklist + held-out-manifest update, counter
  spent for a tie; Gen2-summary S3) is **not cured** by
  this round. The scorer repair is prospective only;
  no retro-repair was applied to the Gen 2 record.

## 2. Cells changed — exactly zero (independent re-run)

This synthesis re-ran, in this session (not copied from
the attack files):

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/scoring
# Ran 27 tests OK (18 pre-existing + 9 manifest) + ASTRA PROBES PASS
PYTHONDONTWRITEBYTECODE=1 python3 research/gaps/a1_model/test_model.py -v
# Ran 10 tests OK
PYTHONDONTWRITEBYTECODE=1 python3 research/scoring/gate_table.py <adapted.csv> --out /tmp/...
# Gen0 v2 / Gen1 / Gen2: all cmp-clean vs filed matrices (table below)
# Gen2 + correct manifest: filed matrix as exact prefix + section (f) "(none)"
cd research/gaps/a1_model && python3 run_artefact_fine.py 0.125,0.0625,0.03125
# physics columns identical to filed artefact_fine.csv (wall_seconds excepted);
# dx=0.015625 row inspected in the filed CSV, not independently re-executed here
```

| Object | Changed | Unchanged (exact, re-verified) |
|---|---|---|
| Gen 0 v2 gate matrix (`gate-matrix-gen0-v2.md`, 8 cand. x 7 gates) | **0 of 56 cells** | 5,395 B, SHA-256 `f256e1f2…d91f74`, `cmp` clean |
| Gen 1 gate matrix (`gate-matrix-gen1.md`, 5 x 7) | **0 of 35 cells** | 4,295 B, SHA-256 `87a1093c…3a990`, `cmp` clean |
| Gen 2 gate matrix (`gate-matrix-gen2.md`, 2 x 7) | **0 of 14 cells** | 2,850 B, SHA-256 `a9e45c1f…3980` (matches Astra S1), `cmp` clean |
| **All filed gate cells** | **0 of 105** | PASS total still **0**; Gen2 P2/H2 still `NA, INS x6`, 0 FAIL / 6 INS, `promoted FALSE` |
| Extraction / adapted CSVs (incl. Gen 2's 33 rows) | **0 rows edited** | The one PROVISIONAL-SIGNAL row (GEN2-R1 G4-AAV leg (a), PMID 42362868) still reads PROVISIONAL-SIGNAL -> INSUFFICIENT, RECORD / UNASSESSED; adjudication in S3.2 is prose, not a CSV edit |
| Q0 verdict + thresholds | 0 | UNDECIDABLE-no-data; patency / retention thresholds unmoved, unratified |
| Kill verdicts | 0 | B killed as specified (carried); A/F/G/H + GEN1-A1 kills UNEVALUABLE — none triggered, none cleared (D10) |
| G4-AAV presumption (all applications to C/D) | 0 | Stands unchanged; leg (a) not retired, not confirmed (S3.2) |
| A1 filed sweep (`results_v2.csv`, 12 rows, dx=0.125) | 0 rows | New `artefact_fine.csv` (4 rows) is additive; interpretation change in S3.3 is not a gate cell |
| Filed matrices on disk | 0 files rewritten | `git status`: only `research/scoring/{gate_table.py, README.md}` modified + new `test_manifest.py`, `run_artefact_fine.py`, `artefact_fine.csv`, `research/gen03/` |

No PASS inflation, and no hidden movement via re-ranking:
the three matrices regenerate byte-for-byte under the
repaired scorer without a manifest, so every lexicographic
key, Pareto set, and promotion check is literally the
filed bytes.

## 3. What each attack actually bought

### 3.1 Scorer cell-manifest repair — evaluability, not fitness

`attack-scorer-manifest.md`; code in
`research/scoring/gate_table.py` (`ManifestCell`,
`load_manifest`, `validate_manifest`,
`find_missing_required_cells`), 9 new tests in
`test_manifest.py`, README updated.

- **Defect closed:** pre-repair, an all-`NA` gate stayed
  `NA` and S7 step 2 counted INSUFFICIENT among applicable
  gates only, so NA scope-shrinkage *improved* fitness
  (the rejected Gen 2 artefact: forced Q1/R1 ranked
  spuriously first at 0/3, 0/2). Optional `--manifest`
  (`cell-manifest-csv-v1`: `candidate,gate,window,required`)
  makes the manifest the entry ticket (candidate sets must
  match exactly; every candidate x gate declared true/false,
  else exit 2), turns each missing required cell into an
  explicit INSUFFICIENT listed in new section (f) (an `NA`
  row does not satisfy a required cell; a missing window
  caps a PASS), and leaves `required=false` as a filed,
  ratifiable declaration rather than silent absence.
- **Proof it taxes the artefact:** the synthetic Q1-like
  fixture reproduces the spurious rank-1 (2 INS) without a
  manifest and is penalized to 6 INS / loses with one.
- **Fences kept:** no manifest ⇒ pre-repair behaviour
  byte-for-byte (S2 above); no real Q1/R1/H2 scoring run;
  the manifest makes scope *declared and taxed*, it does
  **not** make Q1/R1/H2 commensurable with pathways —
  candidate-class placement (incl. H2 beside measurement
  deliverables, Astra S1) remains a human, prospective
  decision. `adapt_extraction.py`'s A–H ID-map successor
  (0 rows on `GEN2-*` IDs) is still owed. Pre-existing
  `demo_matrix.md` staleness untouched, disclosed.

### 3.2 PMID 42362868 vs R1 leg-(a) — deeper extraction, formal NO

`attack-42362868.md` (486 lines). Adjudicates **only**
whether this paper meets the R1 leg-(a) RETIRE standard
as written (`candidate-R1-g4aav-falsification.md` S3).
Answer: **No — and extraction alone cannot, verified
from the R1 text** (Astra S3 upheld).

- **Acquisition (inspected outcomes, no circumvention):**
  main text **NOT obtained** — no PMCID (PubMed elink /
  PMC efetch), Europe PMC `pmcid=None, isOpenAccess=N`,
  publisher PDF returns an HTML subscription preview
  (pypdf `PdfStreamError`). Open adjuncts extracted with
  locators ([Abs]/[SD-Fig4]/[Supp pN]/[Prev]): MOESM1
  supplementary protocols PDF (133 pp.) and MOESM5
  Source Data XLSX (11 sheets). MOESM2 reporting summary
  unextractable via pypdf; ChiCTR2200063181 direct access
  HTTP 405, **not inspected**.
- **What is now known that abstract-only scoring lacked:**
  N=4, ages 2.2–3.4 y, ear order P1 R→L / P2 L→R / P3 R→L /
  P4 R→L; follow-up P1/P2 52 wk, P3/P4 26 wk; per-ear,
  per-frequency ABR from Source Data Fig. 4 (censored
  `>95` baselines; first-ear columns are maintenance
  during second-ear follow-up, not pre-treatment);
  inter-dose intervals derived for P2 = 61 wk, P4 = 31 wk
  (P1/P3 not inspected); AEs abstract-only (0 DLT at
  6 wk, 1 grade-3 neutrophil decrease, 0 SAE). Agent-
  recomputed 0.5–4 kHz means reproduce the abstract's
  26-wk second-ear 43/63/80/53 dB exactly (42.5/62.5/
  80.0/52.5) — two-route corroboration of direction and
  rough magnitude.
- **Why retirement still fails — 5 of 8 conjuncts:**
  (2) n/N denominator unknown (Fig. 3 selection flow
  paywalled; responder-enrichment unexcluded); (3) NAb
  pre/post unmet (only a pooled pre-second-dose range
  1:135–1:3,645; no per-patient, post-dose, assay, or
  titre–response pairing); (6) **human dual extraction
  absent** (single agent; main text paywalled);
  (7) GRADE **UNASSESSED**, not the required ≥Moderate
  human-assessed grade; (8) **zero non-inventor /
  held-out input** — paper, mouse arm, protocols, source
  data, and ChiCTR are one inventor-program DESIGN-side
  study (validation set still 0). Elements 6–8 fail no
  matter what the paywalled text contains. R1's standard
  is itself an unratified proposal; under GOAL S4.2's
  escape wording a retire act is likewise a human ruling.
- **Disposition unchanged:** late-found DESIGN,
  PROVISIONAL-SIGNAL → INSUFFICIENT; leg (a) "challenged,
  unresolved under the decision standard" — the categorical
  slogan narrows, the presumptive rule does not retire.
  No leak to legs (b)/(c), Q0, or any gate cell. Gen2-
  summary S4(3)'s "only item that could retire anything"
  is overstrong and is corrected by this attack: it could
  retire only with an added independent input or a
  prospective human amendment of the standard.

### 3.3 A1 grade-3 / 0.25 mm artefact — zero retired, case not rehabilitated

`attack-A1-artefact.md`; new `run_artefact_fine.py` +
`artefact_fine.csv` (4 rows); `model.py` untouched.
Filed label stands: T0 modelled sub-claim, not a G1 PASS.

| dx (mm) | mono (cells) | tri (cells) | reduction | Q ratio |
|---|---|---|---|---|
| 0.125 | 0.375 (3) | 0.375 (3) | **0.00%** | 1.042 |
| 0.0625 | 0.4375 (7) | 0.4375 (7) | **0.00%** | 1.049 |
| 0.03125 | 0.53125 (17) | 0.46875 (15) | **11.76%** | 1.068 |
| 0.015625 | 0.60938 (39) | 0.54688 (35) | **10.26%** | 1.091 |

- **Answer:** the sweep's sole exact zero survives one
  halving and **vanishes at dx=0.03125**, staying non-zero
  at 0.015625. All 8 solves CG-converged (residuals
  <1e-9); contiguous = global width throughout; the
  dx=0.125 row reproduces `results_v2.csv` exactly. The
  interpolation probe identifies the mechanism — a
  quantisation tie/crossing at the 50%-of-peak threshold
  (interpolated reduction already ~5% where cell counts
  tie) — so the abrupt 0 → 11.8% jump is an endpoint
  artefact signature, not a physical discontinuity.
- **Honestly not converged:** both widths grow at every
  refinement (mono +62.5%, tri +45.8% coarse→finest; last
  step +5 fine cells, ~15–17%), Q increments grow. No
  continuum percentage may be quoted; every number for
  this case must carry its dx. Only *direction* (tripolar
  narrower) is robust.
- **Split verdict:** the exact zero is retired as a grid
  artefact, but the case is **not** rehabilitated as
  evidence — the SGN reading line lies inside the assumed
  0.375 mm sheath at *every* grid (`sgn_in_sheath=True`),
  and whether an in-sheath reading is admissible is a
  geometry/rubric question refinement cannot answer.
  **GEN1-A1 kill remains UNEVALUABLE** (named device,
  safe-charge limit, battery floor, growing geometry,
  grade rubric, freeze all still missing). Six other
  sweep cases still have no fine-grid run.

## 4. Loop state after the attacks

**STOP (GOAL S7 rule 5): NOT met** — identical verdict to
Gen 2, now with three more completed attacks behind it:

| Condition | State |
|---|---|
| (a) Track-P candidate frozen for handoff | **False** — 0 PASS anywhere; structurally impossible while G3b BLOCKED |
| (b-i) Two consecutive generations, no lexicographic improvement | **True — counter 2/2** (Gen 1 + Gen 2; this attack round is not a generation, S1) |
| (b-ii) *All* promotion-blocking gaps ≥2 independent attacks | **False** — see ledger below; gaps 1/2/5/8 still 0/2 |
| (c) Budget exhausted | Not stated |

Gap-attack ledger (Step 5 S6 items 1–8; round-2 counting
rule: one filed, executed attack per gap, partials
flagged; skeptic/synthesis passes never counted). Only
one line is even arguable, and it changes no verdict:

| Gap | After Gen 2 | After gen03 attacks |
|---|---|---|
| 1 Human gates (dual extraction, freeze, H-1…H-8) | 0/2 | **0/2** — agent extraction is not a human gate |
| 2 G3b co-design | 0/2 | **0/2** — untouched |
| 3 P0 denominator | 1/2 | 1/2 |
| 4 Q0 decider data | 1/2 partial | 1/2 partial — 42362868 supplies no Q0-P/Q0-A estimand |
| 5 Frozen absolutes/margins | 0/2 | **0/2** — no pin ratified |
| 6 A1 kill test | ≥2 (still UNEVALUABLE) | ≥2 — artefact sub-attack adds depth, verdict unchanged |
| 7 Search completeness | mixed (full-texts sub-gap ≥2) | mixed — 42362868 main text + ChiCTR join the owed list |
| 8 Human-reversible items | 0/2 | **0/2** — more decisions queued, none taken |
| *AAV re-dosing (S7 rule-4 named example)* | *0/2 completed* | *At most 1/2 partial* — one filed, executed extraction+adjudication attack, paywall-limited and non-decisive by its own S6; whether the human panel counts it as "completed" is theirs to rule. Under either count (0/2 or 1/2) STOP (b-ii) stays false, and re-reading this one study can never supply attack #2 (no independence)* |

Candidate / claim state, all unchanged: P2 and H2 non-
promoting survivors (Pareto tie, 0/6); Q1 and R1 live
designs with no survivor/winner semantics, extract-only;
A1/F1m carry over with no Gen 2/3 child (A1×F1m still
blocked on A1's unevaluable kill); H harm not cleared
(H2 must never be quoted as non-harm evidence);
validation set **0**; every Gen 2 row still RECORD /
UNASSESSED triage. **FROZEN retained by default. G3b
BLOCKED. Prohibitions D1–D17 carry verbatim.**

Net assessment: this round did exactly what Astra
commissioned — it converted three rhetorical debts into
filed, checkable results (a scorer that can no longer
reward scope-shrinkage, an extraction that proves its
own ceiling, a model zero shown to be quantisation) —
and it moved no verdict, because every remaining
verdict-moving step is human-owned or primary-data-bound.
Agent-side document work on these three fronts is now
exhausted: further agent re-readings of PMID 42362868,
further scorer features without a human-ratified manifest
to enforce, or further A1 refinements without a pre-stated
convergence criterion would be rewording, not attacks.

## 5. Next rock-push options, ranked

Ranking key: GOAL S7 rule 4 (decision-relevance x
tractability), Astra gen2 S4 order updated for what this
round closed, win-path W1–W8 ownership. Options 1–2 are
parallel human tracks, not a sequence; 3 gates any future
scoring; 4–5 are executability work; 6 is calendar-bound.
The anti-option is stated last because it is the one the
loop keeps reaching for.

1. **G3b co-design + measurement authority (W2; gap 2,
   0/2).** The sole absolute bar: with G3b BLOCKED every
   G3b cell is INSUFFICIENT and no Track-P promotion is
   possible at v1, whatever else lands. Commission the
   Deaf/parent co-design deliverable with named measurement
   leadership — instrument per window, MCID/NI specification,
   feasibility evidence — and repair H2's estimand alongside
   it (its per-child NI classification misapplies GOAL
   S4.2's pathway-vs-frozen margin; Astra S2). Longest lead
   time, highest leverage: start first. Co-design alone
   earns no G3b PASS; signatures alone complete nothing.
2. **Complete PMID 42362868 humanly, with its ceiling
   stated up front (W3/W5; AAV re-dosing, at most 1/2).**
   Nearest document-based decision: institutional main-text
   access (Fig. 3 denominator, per-patient dose/NAb pre/post
   + assay, P1/P3 intervals, AE tables, cohort overlap),
   ChiCTR2200063181 inspected directly, MOESM2 rendered,
   then human dual extraction + GRADE/RoB/allegiance, a
   human ruling ratifying or prospectively amending R1's
   borrowed retire standard, and a search for ≥1 non-
   inventor/held-out input. Ceiling, non-negotiable: under
   the standard as written this paper alone **cannot**
   retire leg (a) even perfectly extracted (S3.2 elements
   7–8). The deliverable is a completable attack and a
   narrowed rhetoric, not a promised retirement.
3. **Prospective scoring readiness — before any further
   scoring (W1/W4/W7; gaps 1/5/8 inputs).** Now
   implementable, newly unblocked by S3.1: humans ratify
   candidate classes and a per-class cell manifest
   prospectively (including H2's placement beside
   measurement deliverables); file the `adapt_extraction.py`
   successor for `GEN-*` IDs; produce the owed Gen 2/3
   protocol + freeze checklist + held-out-manifest update
   and name the H-1…H-8 roster / analysis owner; ratify
   the conventions Gen 2 left sensitivity-only (P2 NI
   margin + delay bounds, H2 discordance tolerance, Q0
   thresholds). No retro-repair of the Gen 2 sequence;
   post-freeze edits = new candidate.
4. **Executable protocols → primary data (W6; gaps 4/6).**
   The only route by which any PASS can ever exist:
   finish P2's attribution/audit/missing-log rules and
   comparative time-to-activation analysis; file Q1's
   freeze addendum (species/construct/dose/course/N from
   inspected sources, in a model where the construct can
   plausibly restore function) and execute the T2 decider
   for Q0-P/Q0-A; design R1 leg-(c)'s second-dose-specific
   readout (ABR alone cannot separate second-dose
   expression from first-dose persistence). Execute only
   when people, parameters, and resources exist.
5. **A1 evaluability package (gap 6, ≥2 attacks but
   UNEVALUABLE).** Supply what S3.3 proved refinement
   cannot: named device, safe-charge limit, battery floor,
   growing-cochlea geometry, per-grade fibrosis rubric,
   freeze addendum, a holder pre-stated convergence
   criterion (then dx=0.0078125 — ~40+ min extrapolated —
   or re-implementation under a new freeze), and a ruling
   on in-sheath SGN admissibility. Until then A1 carries
   direction-only weight and A1×F1m stays deferred.
6. **Validation accrual on a stated cadence (W5; gap 7).**
   Re-run the sweep's frozen strings as new dated files;
   human siding amendment *before* opening any post-freeze
   record (NCT07752888, est. 2027-05-31, first); complete
   Embase/CTIS/ANZCTR/ChiCTR so absence claims can be
   bounded honestly. This fills only with calendar time;
   late-found pre-freeze records stay DESIGN, never
   re-sided as validation.
7. **Anti-option — do not file a design-only Gen 3 now.**
   Two consecutive scored design-only generations produced
   two cell-for-cell ties and spent the counter; Gen 2
   judged its four-question supply saturated and Astra
   downgraded two of the four to elaborations. A Gen 3
   candidate generation becomes defensible only if a
   completed attack or measurement decision above motivates
   a concrete new intervention/interface specification with
   an honest prospective comparison (Astra S4). If none of
   options 1–5 is executable, the correct act is **no
   generation at all**: FROZEN retained, the owed human
   work as the headline, a deferred-work record and bounded
   monitoring cadence — not a third scored tie at clock 3/4,
   and not formal abandonment (STOP is not met).

*End. Gen `gen03/` = bounded attack round, not generation 3.
Clock 2/4. Counter 2/2. STOP not met. Cells changed: 0 of 105.
Scores nothing new.*
