# Step 2 pre-registration summary (Gen 0)

> **Model routing (GOAL §9):** Requested **Sol 6.1, xhigh**
> (synthesis tier). Actual runtime model:
> **`muse-wonder-full-1.0` fallback** — Sol 6.1 unavailable
> in this runtime, same effort split, substitution disclosed
> per §9 rule 3. No claim in this file is Sol 6.1 work.
>
> **Date:** 2026-11-02. **GOAL:** v2.2. **Stage:** Step 2
> synthesis, written after the Step 2 skeptic
> (`step2-skeptic.md`) and BEFORE any Step 3 scoring.
> This file scores nothing, promotes nothing, and freezes
> nothing. Candidate files were not edited for this summary.
>
> **Exploratory-after-seen label: YES.** Seen before writing:
> GOAL v2.2 (§4/§7/§8/§9/§11 + Appendices as cited);
> `STATUS.md`; all `research/gen00/` files listed in §1;
> `research/scoring/` + `verify/` code/tests; skeptic prior
> result. Not opened: any Step 3 scoring or held-out
> validation evidence (validation set = 0 entries).

## Decision: screening only, no promotion

**Step 3 may proceed as screening / falsification only.**
Sweeps, skeptics, and judge triage may run under the
pre-registered protocol to find FAILs, INSUFFICIENT cells,
and kill-criterion hits. **No promotion is possible at v1**,
for three independent reasons — any one alone blocks it:

1. **G3b BLOCKED.** Every G3b cell for candidates A–H and
   frozen is **INSUFFICIENT** until the instrument + MCID
   are co-designed with stakeholders (GOAL §4.2;
   AppendixA-v1 §6). Track-P promotion requires G3b PASS,
   so promotion is impossible regardless of other gates.
2. **Pins unfrozen.** AppendixA-v1 and the frozen baseline
   are **PROPOSED PIN — NOT FROZEN**: 12 PINNED
   (definitional only) / 13 PROVISIONAL / 18 UNPINNABLE /
   1 BLOCKED, with Step 1 amendments A1–A6 still owed and
   Q0 + Appendix A thresholds unratified conventions.
   Pre-ratification verdicts are sensitivity-only.
3. **Human extraction pending.** All Step 0/1/2 evidence is
   agent pre-extraction. Human-led dual extraction
   (independent H-7 + error audit, GOAL §9) is **PENDING**,
   so no load-bearing row is gate-deciding yet.

Additionally, **no Step 3 headline may be produced until
skeptic finding F1 is closed** (§3): the locked
`gate_table.py` cannot yet read the frozen extraction
template. Screening that does not depend on that headline
computation is unaffected; any screening output must carry
the three blockers above verbatim and must not be worded
as a promotion, ranking-for-adoption, or freeze.

Human freeze is **PENDING** (holder + H-8 co-signature,
H-1…H-7 unnamed, analysis-owner slot empty —
`freeze-checklist.md` §6). Nothing in Step 2 changes that.

## 1. Inventory (what Step 2 produced)

All dated 2026-11-02, all committed before Step 3.

| Item | Files | State |
|---|---|---|
| Candidates A–H (App. B + App. C FMEA + kill criteria) | `candidate-A-focal-electrical.md` (P), `candidate-B-biohybrid.md` (P), `candidate-C-optical.md` (R watch), `candidate-D-reprogramming.md` (R watch-only), `candidate-E-penetrating.md` (R watch), `candidate-F-w0-bridge.md` (P, G1 NA), `candidate-G-sequencing-pathway.md` (P, G1 NA), `candidate-H-visual-language.md` (P, G1 NA) | Exactly 8, 1 per §8 family; skeptic: every App. B field + 18/18 FMEA rows present in all 8 |
| Protocol | `protocol.md` | Pre-registration before scoring; held-out **by study** (§7); human freeze + dual extraction PENDING |
| Q0 thresholds | `Q0-thresholds.md` | Defined before Q0 scoring; Q0-P ≥80% / >50–<80%, Q0-A ≥0.80+≤10 dB / ≤0.50 or >20 dB; all **CONVENTION, unratified**, sensitivities mandatory |
| Held-out partition | `heldout-manifest.md` | By study, never by rows; design set enumerated; **validation = 0 entries** |
| Extraction schema | `extraction-schema.md` + `extraction_template.csv` (14 cols; track not stored) | Frozen as written; see F1 incompatibility below |
| Freeze checklist | `freeze-checklist.md` | Human freeze **PENDING** (§6); C park date formula-only, no calendar date asserted |
| Scoring code | `research/scoring/gate_table.py`, `test_gate_table.py` (15 tests), `README.md`, synthetic `demo_*.csv`/`demo_matrix.md` | S7 ranking + G3b block correct (skeptic §5); cannot read frozen template (F1) |
| Epi arithmetic | `verify/epi_arithmetic.py`, `test_epi_arithmetic.py` (13 tests) | D1–D4 range arithmetic, UNPINNABLE propagates |
| Skeptic | `step2-skeptic.md` | PASS on completeness/tests/logic; **FAIL freeze-ready** (F1) |
| This synthesis | `Step2-preregistration-summary.md` | Screening-only gate for Step 3 (above) |

Upstream pins this step depends on (not re-decided here):
`research/frozen_baseline/` — `AppendixA-v1.md`,
`frozen_bilateral_eCI_v1.md`, `cost_dictionary_v1.md`,
`Step1-pin-summary.md`, `step1-skeptic.md` (all PROPOSED,
NOT FROZEN). FTO: **Not assessed** in all 8 candidates.
Parentage: Gen 0 / mutation log N/A in all 8 (correct).

Corroboration in this synthesis session (Python 3.14.8):
`test_gate_table` 15/15 OK; `test_epi_arithmetic` 13/13 OK;
`gate_table.py` on `extraction_template.csv` reproduced
the skeptic's F1 failure verbatim — `EXIT=2`, missing
`['track','delta_g2_db','delta_g3a_sd','g1_channels',
'burden_rank','verdict']`.

## 2. Model + effort (GOAL §9)

Sol 6.1 was requested throughout and unavailable
throughout; every file ran the disclosed fallback at the
same effort split. No claim in the package is Sol 6.1 work.

| Pass | Files | Requested | Actual (disclosed) |
|---|---|---|---|
| Candidate design A–H | `candidate-A…H-*.md` | Sol 6.1, **xhigh** | `muse-wonder-full-1.0` fallback |
| Workers: protocol, Q0, held-out, extraction, freeze | `protocol.md`, `Q0-thresholds.md`, `heldout-manifest.md`, `extraction-schema.md`/`extraction_template.csv`, `freeze-checklist.md` | Sol 6.1, **high** | `muse-wonder-full-1.0` fallback |
| Code: scoring + epi | `research/scoring/*`, `verify/epi_arithmetic.py` (+ tests) | Sol 6.1, **high** (deterministic) | `muse-wonder-full-1.0` fallback |
| Skeptic | `step2-skeptic.md` | Sol 6.1, **xhigh** | `muse-wonder-full-1.0` fallback |
| **This synthesis** | `Step2-preregistration-summary.md` | Sol 6.1, **xhigh** | **`muse-wonder-full-1.0`** |

§9 rule 2 unchanged: no model tier substitutes for human
dual extraction or human freeze decisions.

## 3. Skeptic fixes owed (`step2-skeptic.md`)

**Freeze-blocking (must close before any freeze or Step 3
headline):**

- **F1 — Schema incompatibility.** Gen 0 schema (14 cols,
  gates `G1-spectral/G2-music/G4-AAV…`, verdicts
  `PROVISIONAL-SIGNAL/NA-prereg`, no `track` column) vs
  `gate_table.py` `extraction-csv-v1` (12 cols, `G1…G6`,
  `PASS/FAIL/INSUFFICIENT/NA` only). Candidate FMEA bands
  (UNPINNABLE/INSUFFICIENT) are likewise rejected, so the
  locked computation currently consumes only its own
  synthetic demo — contradicting `protocol.md` §8. Owed:
  one schema wins or a versioned adapter, plus an
  end-to-end test on a template-schema CSV + real FMEA CSV.
  Freeze condition (c) is met in letter, not in function.

**Non-blocking, owed in the same pass (new versions only;
candidate originals untouched by the skeptic and here):**

- **F2** FMEA severity divergence on identical harms
  (anaesthesia 4 in A–D vs 3 in E/G; vestibular 3 vs 2/NA)
  — harmonize or justify before any G5 aggregate is real.
- **F3** E/G (and partly F/H) boilerplate mitigations /
  generic stopping rules — replace with harm-specific text.
- **F4** Candidate F inconsistent NA logic — pick one rule.
- **F5** `summarize.best()` cross-gate fallback can smuggle
  another gate's number into G2 — require own-gate rows.
- **F6** T0/VeryLow can still yield PASS (GRADE→PASS
  judge-side in README vs script-enforced in
  `extraction-schema.md` §3.2) — one spec must win at F1.
- **F7** Candidate C park date **2028-11-02** (assumed
  freeze) vs `freeze-checklist.md` §5 formula-only —
  checklist wins; re-enter or retire C's date by amendment
  at human freeze.
- Stale cross-refs: "gate_table.py does not yet exist" /
  "held-out manifest still owed" in `protocol.md`,
  `extraction-schema.md`, `freeze-checklist.md`, A/B.

**Pre-existing pendings (disclosed in the files, not
counted against Step 2 workers, still blocking freeze):**
human holder + H-8 signatures; H-1…H-7 + analysis owner
unnamed; AppendixA-v1 A1–A6 reconciliation; human dual
extraction; Q0/App.A stakeholder ratification; G3b
co-design panel unrecruited; Step 1 cost-file H/C sources
not yet enumerated study-by-study (manifest §2.8).

What the skeptic passed, for the record: exactly 8
candidates; every Appendix B field in all 8; 18/18 FMEA
rows each with severity/tier/mitigation/stopping rule and
no invented probability bands; §8 kill criteria verbatim +
refined in all 8; Q0 pre-registered before scoring;
held-out by study; S7 veto→FAILs→INSUFFICIENT→G2→G3a→G3b→
G1-NA-last→burden implemented as written, G3b forced
INSUFFICIENT, promotion always FALSE at v1.

## 4. What Step 3 may and may not do

| Step 3 activity | Allowed? |
|---|---|
| Literature sweeps, pre-extraction, skeptic/judge triage as **screening/falsification** | **Yes** — under `protocol.md`, by-study held-out, all INSUFFICIENT cells published |
| Reporting FAIL / INSUFFICIENT / kill-criterion hits | Yes — labelled screening, agent pre-extraction until human dual extraction |
| Q0 verdicts | Sensitivity-only until ratification (`UNDECIDABLE-unratified`) |
| `gate_table.py` headline matrix on real extractions | **No** — until F1 (+ F5/F6 spec choice) closed and tested end-to-end |
| Any Track-P/R **promotion**, freeze, or ≥90% claim | **No** — G3b BLOCKED + pins unfrozen + human extraction pending (GOAL §5.1: Gen 0/1 make no ≥90% promotion claims) |
| Editing candidates in place to fix F2–F7 | No — corrections are new versions (no-overwrite rule) |

*End of Step 2 synthesis. Next gate: close F1, then Step 3
screening; freeze only on human signatures.*
