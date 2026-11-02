# Step 2 skeptic review (Gen 0 pre-registration package)

> **Model routing (GOAL §9):** Requested **Sol 6.1, xhigh**
> (judging/skeptic tier). Actual runtime model:
> **`muse-wonder-full-1.0` fallback** — Sol 6.1 unavailable
> in this runtime, same effort split, substitution disclosed
> per §9 rule 3. No claim in this file is Sol 6.1 work.
>
> **Date:** 2026-11-02. **Stage:** Step 2 adversarial review,
> written BEFORE Step 3 scoring. This file scores nothing,
> promotes nothing, and freezes nothing (human freeze
> PENDING, `freeze-checklist.md` §6).
>
> **Exploratory-after-seen label: YES.** Seen before writing
> (exactly): GOAL.md v2.2 §4/§7/§8 (in full for §7–§8,
> Appendices A–C in full); all 8 candidate files, `protocol.md`,
> `Q0-thresholds.md`, `heldout-manifest.md`, `extraction-schema.md`,
> `extraction_template.csv`, `freeze-checklist.md` in
> `research/gen00/`; `gate_table.py`, `test_gate_table.py`,
> `README.md`, `demo_matrix.md` + demo CSVs in
> `research/scoring/`; `epi_arithmetic.py`,
> `test_epi_arithmetic.py` in `verify/`. Not opened: any
> Step 3 scoring or held-out validation evidence (validation
> set = 0 entries, manifest §3).
>
> **G3b BLOCKED (applies to every candidate A–H and frozen):**
> **all G3b cells INSUFFICIENT; no Track P promotion is
> possible at v1** (GOAL §4.2; AppendixA-v1 §6). Nothing in
> this review changes that.

## 0. Summary

| Check | Verdict |
|---|---|
| Exactly 8 candidates (§7 rule 1) | **PASS** — A–H, 1 per §8 family |
| Appendix B every field, every file | **PASS** (wording variants, §1) |
| Appendix C FMEA: all 18 rows, every file | **PASS** (quality caveats, §2) |
| Kill criteria present | **PASS** — §8 verbatim + refined, all 8 |
| Q0 thresholds before scoring | **PASS** — conventions, unratified, sensitivity-only (§3) |
| Held-out by study, not rows | **PASS** — protocol §7 + manifest §1 rule 1 (§3) |
| gate_table tests pass (re-run) | **PASS** — 15/15 + 13/13, demo byte-identical (§4) |
| Implementation matches S7 + veto + G3b | **PASS** for ranking/promotion logic (§5) |
| **Package is freeze-ready** | **FAIL — 1 load-bearing defect (F1)**: `gate_table.py` cannot read the frozen extraction template (§6). Freeze is also blocked by the pre-existing pendings (human signatures, AppendixA NOT FROZEN, dual extraction, stakeholder ratification) — disclosed in the files themselves and not counted against the workers here. |

## 1. Per-candidate Appendix B completeness (grep audit + manual check)

Method: case-insensitive grep over each file for every
Appendix B field (GOAL.md line 824–833), then manual reading
of every apparent miss. All first-pass misses were wording
variants, not absences: "cochlear nerve deficiency" for CND,
"additional disabilities" (A–D) / "comorbid" (E–H),
"Anaesthesia"/"Anesthesia", "Facial-nerve", "Exploratory-
after-seen **label:** YES" (A–D), "**Track:** P" (F/G/H).
Audit scripts run in this review: grep probes over all 8
files plus full body reads.

`Y` = field substantively present and candidate-specific;
`Y*` = present but see note; `—` = NA with stated justification.

| Appendix B field | A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|---|
| ID / track | Y | Y | Y | Y | Y | Y | Y | Y |
| Mechanism & target cells | Y | Y | Y | Y | Y | Y | Y | Y |
| Delivery route & dose/units | Y | Y | Y | Y (watch-only) | Y | Y | Y | Y |
| Timing by window & decision origin | Y | Y | Y | Y | Y | Y | Y | Y |
| Model system / comparator | Y | Y | Y | Y | Y | Y | Y | Y |
| Eligibility: ANSD | Y | Y | Y | Y | Y | Y | Y | Y |
| Eligibility: CND / cochlear nerve | Y | Y | Y | Y | Y | Y | Y | Y |
| Eligibility: malformations | Y | Y | Y | Y | Y | Y | Y | Y |
| Eligibility: syndromic | Y | Y | Y | Y | Y | Y | Y | Y |
| Eligibility: comorbid / add. disabilities | Y | Y | Y | Y | Y | Y | Y | Y |
| G1–G6 plan vs AppendixA-v1 cells (PASS/FAIL pre-specified, not scored) | Y | Y | Y | Y | Y | Y | Y | Y |
| G1 NA pre-declared (F/G/H only) | n/a | n/a | n/a | n/a | n/a | Y | Y | Y |
| G3b BLOCKED = INSUFFICIENT stated | Y | Y | Y | Y | Y | Y | Y | Y |
| Power / precision | Y | Y | Y | Y | Y | Y | Y | Y |
| FMEA summary (App. C) | Y | Y | Y | Y | Y* | Y* | Y* | Y* |
| Burden (hrs/wk, visits, surgeries) | Y | Y | Y | Y | Y | Y | Y | Y |
| Regulatory class & §10 staging | Y | Y | Y | Y | Y | Y | Y | Y |
| FTO flag | Not assessed ×8 (all files) | | | | | | | |
| Kill criterion (§8 verbatim + refined) | Y | Y | Y | Y | Y | Y | Y | Y |
| Parentage + mutation log | Gen 0 / n-a ×8 (correct per App. B: Gen ≥1 field) | | | | | | | |
| Exploratory-after-seen YES + what seen | Y | Y | Y | Y | Y | Y | Y | Y |
| Header: Sol 6.1 requested / fallback / 2026-11-02 / BEFORE Step 3 | Y | Y | Y | Y | Y | Y | Y | Y |

Candidate-specific §8 obligations checked in body reads:
A explains prior focusing failure (§3, 5 causes) and treats
dexamethasone/ECochG/robotic as comparator evolution with
the Step 0 "no trial inspected" gap named; B declares the
B-E/B-L branch, pre-specifies tonotopy metrics, states the
<5 y no-refill automatic kill, and records the 2014–2026
silence as *unexplained* with re-search obligations; C
pre-specifies the §8C infant G6 FAIL rule and separates
NCT05110183; D is watch-only with the single §8D advance
criterion and G4-AAV presumptive FAIL; E splits ABI as
unverified; F is F1-only with F-vib exploratory + harm
monitoring; G excludes the unilateral preserved-ear variant
and defers Q0 thresholds to the protocol (now supplied,
§3 below); H uses encouragement + IV identification with
no modality randomization. All 8 kill criteria are
falsifiable as written.

## 2. FMEA (Appendix C)

All 18 mandatory rows present in all 8 files (A–D as C1–C18;
E–H as 18 named rows; counted programmatically: 18/18 ×8).
Every row carries severity 1–4 or justified NA, a probability
field, a source tier, a mitigation, and a persistent-harm
stopping rule. No invented numeric probability band anywhere:
bands are UNPINNABLE (A–D) / INSUFFICIENT (E–H) with the
source that would pin them named (§7.2/U13 discipline).

Three quality findings (non-blocking, must be fixed before
any freeze-grade use of these tables):

- **F2 Severity divergence on identical harms.** Anaesthesia
  <12 mo: severity 4 in A–D, 3 in E/G. Vestibular loss: 3 in
  A–D, 2 in E/F/G, NA in H. Because Track R G5 aggregate has
  a severity-≥3 floor, the same harm would count toward the
  aggregate for C/D but not for E (vestibular) — a ranking
  artifact of parallel authorship, not evidence. Harmonize
  or justify per candidate before the aggregate is computed
  for real.
- **F3 E/G boilerplate mitigations.** "Standard mitigation
  per protocol" is repeated verbatim on 8 rows (E), 9 rows
  (G), 4 rows (F), 1 row (H), with an identical generic
  stopping rule. Formally present (Appendix C satisfied);
  substantively thin next to A–D's harm-specific entries.
  G in particular scores downstream surgical harms of CI as
  its own rows with generic text instead of cross-referencing
  the frozen FMEA as H does.
- **F4 Inconsistent NA logic in F.** A non-surgical bridge
  NA's anaesthesia/meningitis/facial/CSF but assigns
  severities to vestibular loss (2), residual-hearing loss
  (3), and MRI events (2) with no causal path stated; H
  (also non-invasive) NA's all three. Pick one rule.

## 3. Q0 thresholds and held-out partition

**Q0 (PASS as pre-registration, NOT as ratified numbers).**
`Q0-thresholds.md` is dated 2026-11-02 and labelled
PRE-REGISTRATION before any Q0 scoring; it separates
Q0-L/Q0-P/Q0-A, states zones (Q0-P ≥80% HIGH / >50–<80%
INTERMEDIATE; Q0-A ≥0.80 + ≤10 dB RETAINED / ≤0.50 or
>20 dB LOST), §2.3 evidence minima, a composite rule, and
UNDECIDABLE with 4 sub-labels + 5 binding consequences.
Every number is labelled CONVENTION pending stakeholder/
expert ratification with mandatory sensitivities (70/90%,
0.70/0.90, 5/15 dB). Skeptic endorses the *timing and
honesty*, not the numbers: 10/20 dB and 80% are unratified
proposals, and pre-ratification Q0 verdicts are correctly
sensitivity-only (UNDECIDABLE-unratified). The file also
honestly discloses that the E4a/E4b evidence void was known
when thresholds were chosen and that UNDECIDABLE is the
anticipated — but not pre-scored — outcome.

**Held-out (PASS).** Protocol §7 and manifest §1 rule 1 both
state partition **by study, never by rows**, plus date and
species rules, contamination/opening rules, and "extraction
upgrade ≠ validation". Manifest §2 enumerates the design set
(Step 0 §2 + AppendixA N1–N8, year/species/tier/IDs); §2.9
lists neither-set; **validation = 0 entries** at 2026-11-02
with admission rules. `extraction-schema.md` §1 repeats
"siding is by study, never by row". Recorded gap (author's
own unresolved, confirmed): Step 1 cost-file H/C sources are
partitioned as worker-log entries, not enumerated
study-by-study (manifest §2.8).

## 4. Test re-run (this skeptic, 2026-11-02)

Verbatim outputs from re-running in this review session
(Python 3.14.8, matches README pin; pytest absent):

```text
$ python3 -m unittest research.scoring.test_gate_table -v
test_load_and_bad_verdict_rejected (...) ... ok
test_g3b_forced_insufficient_for_every_candidate (...) ... ok
test_insufficient_count_excludes_na (...) ... ok
test_matrix_worst_window_and_missing_gate (...) ... ok
test_worst_applicable_window (...) ... ok
test_promotion_false_when_g3b_insufficient (...) ... ok
test_promotion_logic_isolated_from_v1_block (...) ... ok
test_g1_na_last_among_ties (...) ... ok
test_g3a_then_burden_tiebreaks (...) ... ok
test_g5_veto_also_demotes (...) ... ok
test_lexicographic_order_fails_then_insufficient_then_g2 (...) ... ok
test_veto_fail_demoted_last_despite_fewer_fails (...) ... ok
test_g5_aggregate_severity_floor_and_weights (...) ... ok
test_pareto_excludes_dominated (...) ... ok
test_track_r_g1_then_g5_aggregate (...) ... ok
Ran 15 tests in 0.006s — OK

$ python3 -m unittest verify.test_epi_arithmetic -v
Ran 13 tests in 0.000s — OK   (D1–D4 incl. None-propagation,
no-pooling, P0-like gate, remainder, union-once)

$ python3 research/scoring/gate_table.py \
    research/scoring/demo_extraction.csv \
    --fmea research/scoring/demo_fmea.csv --out /tmp/rerun_matrix.md
$ diff research/scoring/demo_matrix.md /tmp/rerun_matrix.md
(no output — byte-identical; Track P DEVICE > PATHWAY
(G1 NA-last) > VETO (DEMOTED); Track R B(g5=1) > A(g5=4);
all promotions FALSE)
```

Both documented invocations (`cd research/scoring && python3
-m unittest test_gate_table`; `cd verify && python3 -m
unittest test_epi_arithmetic`) also pass unchanged.

## 5. Implementation vs GOAL S7 / S4.2 (code read in full)

`track_p_key` implements exactly: veto (G4 or G5 == FAIL)
demoted first → fewest FAILs → fewest INSUFFICIENT among
applicable (NA excluded) → largest G2 → largest G3a → G3b
rank → largest G1 with NA/missing last → lowest burden →
name (reproducibility only). That is GOAL §7 items 1–7 in
order, incl. the G4/G5 veto demote-last (test asserts a
1-FAIL veto candidate ranks below a 2-FAIL non-veto one).
`build_gate_matrix` forces G3b = INSUFFICIENT for every
candidate regardless of input and treats a missing gate as
INSUFFICIENT; `check_promotion` requires all-PASS (device)
or G2–G6 PASS with G1 NA (pathway) and never promotes Track
R — every v1 result FALSE, with the BLOCKED note printed on
every candidate row. `g5_aggregate` = Σ band weights over
severity ≥3 harms (defined in README + docstring, as GOAL
§7 delegates to the Step 2 gate_table spec). `verify/
epi_arithmetic.py` D1–D4 range arithmetic with UNPINNABLE
propagation matches its README transcription. Deterministic:
no randomness/clock; sorted output.

Minor code findings (non-blocking, fix with F1):

- **F5 Cross-gate numeric fallback.** `summarize.best()`
  falls back to any gate's row when the own-gate row lacks
  the value. Probe: a 99.0 `delta_g2_db` placed on a G3a row
  became the candidate's G2 gain. README documents "any row
  if no G2 row carries it" — documented, but a silent
  smuggling path; require own-gate rows only.
- **F6 GRADE/tier unenforced.** Probe: T0 + VeryLow + PASS
  rows yield a PASS matrix (G3b forced aside). README says
  GRADE→PASS is judge-side; `extraction-schema.md` §3.2
  requires the *script* to enforce grade/tier validators
  with reasons emitted. One of the two specs must win at
  reconciliation (see F1).

## 6. Load-bearing finding (freeze-blocking)

**F1 — The two "v1" extraction schemas are incompatible;
`gate_table.py` cannot read the frozen Gen 0 template.**
Observed in this review:

```text
$ python3 research/scoring/gate_table.py \
    research/gen00/extraction_template.csv --out /tmp/x.md
gate_table: error: extraction CSV missing columns ['track',
 'delta_g2_db', 'delta_g3a_sd', 'g1_channels',
 'burden_rank', 'verdict'] (schema extraction-csv-v1)
EXIT=2
```

`extraction-schema.md` freezes 14 columns
(`candidate,gate,window,stratum,claim,source_id,tier,grade,
effect,n,comparator,verdict_proposed,extractor,
verified_date`) with track deliberately *not* stored (§2.1)
and gates `G1-spectral/G1-temporal/G2-music/G4-AAV` +
verdicts `PROVISIONAL-SIGNAL/NA-prereg`.
`gate_table.py` (`extraction-csv-v1`) requires 12 different
columns, `track` in-CSV, gates `G1…G6` only, verdicts
`PASS/FAIL/INSUFFICIENT/NA` only. Probes confirm every
schema-legal gate/verdict value above is rejected, and the
candidate FMEA probability values (UNPINNABLE/INSUFFICIENT)
are rejected by the `--fmea` loader — so at v1 the locked
computation can consume **neither** the Step 2 extraction
template **nor** the candidate FMEAs, only its own synthetic
demo. Protocol §8 promises the opposite (gate_table reads
"the extraction CSV defined in `extraction-schema.md`").
Consequences: no freeze-grade scoring headline is possible
until one schema wins or a versioned adapter is written and
tested against the template + a real FMEA CSV; freeze
condition (c) in `freeze-checklist.md` §6 ("gate_table.py
exists with passing tests") is met in letter (code + 15
passing tests exist) but not in function. This is a
parallel-work integration defect, not a S7-logic defect —
the ranking code itself is correct (§5).

Related stale cross-references (fix in the same pass):
`protocol.md` §8 "gate_table.py does not yet exist";
`extraction-schema.md` §3 "Until gate_table.py exists";
`freeze-checklist.md` §3 "DOES NOT EXIST YET — OWED";
candidates A/B "held-out manifest … still owed" (it now
exists).

## 7. Cross-file inconsistency (calendar)

**F7 — Candidate C park date vs freeze checklist.** Candidate
C commits to a calendar park date **2028-11-02** built on an
*assumed* Gen 0 freeze of 2026-11-02 (flagged as an assumption
in C §5, with a day-for-day move rule). `freeze-checklist.md`
§5 explicitly refuses that assumption ("entered by amendment,
never assumed = 2026-11-02"; no calendar date asserted). GOAL
§8C requires the calendar date *in the freeze checklist*.
Resolution owed at freeze: the checklist formula wins (date
= min[human freeze + 24 mo, Gen 2 review]); C's 2028-11-02
must be re-entered or retired by amendment the day the freeze
signs. Until then two Step 2 files state different things
about the same deadline.

## 8. Disposition

The Gen 0 pre-registration is *substantively* complete and
honest: exactly 8 fully specified candidates, kill criteria,
pre-scoring Q0 conventions, a by-study held-out partition,
and a correct, well-tested ranking implementation that
enforces the G3b block. It is **not freeze-ready**: (i) F1
schema reconciliation + an end-to-end run on a template-schema
CSV with tests; (ii) F2–F7 cleanups; (iii) the package's own
declared pendings — human holder + H-8 signatures,
AppendixA-v1 PROPOSED-NOT-FROZEN (A1–A6 owed), human dual
extraction, Q0/convention stakeholder ratification,
analysis-owner slot empty, H-1…H-7 unnamed. Gen 0 can screen;
it cannot promote — **G3b BLOCKED (INSUFFICIENT) — co-design
pending; no promotion possible at v1** — and no Step 3
headline may be produced until F1 is closed.

*End of Step 2 skeptic review. Original worker files
untouched by this review; corrections belong in new versions.*
