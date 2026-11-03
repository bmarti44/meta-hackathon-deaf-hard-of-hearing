# Gen 4 adaptation note — ID→track map, manifest treatment, QR4/AD4 single-candidate runs

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Holder Sisyphus directive; this
> note 2026-11-03. GOAL v2.2. **Gen clock: Gen 4 = generation
> 4 of max 4 (4/4 — EXHAUSTED; no Gen 5 without new external
> evidence + human clock amendment). G3b BLOCKED; same PASS
> bar as Gen 0–3; no PASS anywhere; no promotion; FROZEN
> retained. No invented data.**

## Documented Gen 4 candidate-ID → track / scorer-treatment table (binding for this re-score)

| Gen 4 ID | Kind (per candidate file) | Parent | Track for `gate_table.py` | Scorer treatment |
|---|---|---|---|---|
| `GEN4-P4` | P3 FINAL, measurement core frozen-form | GEN3-P3 | **P** (portfolio; G1 NA disclosed) | **`adapted-gen4.csv` + `gate-matrix-gen4.md` WITH `--manifest`** (`manifest-gen4-P4W4.csv`) — 8 rows |
| `GEN4-W4` | W3 FINAL, interaction frozen-form | GEN3-W3 | **P** (portfolio; G1 NA disclosed) | **Same main manifest run** — 8 rows |
| `GEN4-QR4` | Decider/rule-test program, Stages 0–1 executable; "track none, not promotable" | GEN3-QR3 | *none by design* — scorer-required **`P` placeholder, not a class claim** | **Separate single-candidate `--manifest` run only** (`adapted-gen4-QR4.csv` → `gate-matrix-gen4-QR4.md`). Absent from every shared ranking/Pareto/fitness key |
| `GEN4-AD4` | Documentary protocol **executed** (agent scope); "not promotable" | GEN3-AD3 | **P device lineage** | **Separate single-candidate `--manifest` run only** (`adapted-gen4-AD4.csv` → `gate-matrix-gen4-AD4.md`). Absent from shared ranking/Pareto/fitness |

**Manifests verified:** `manifest-GEN4-{P4,W4,QR4,AD4}.csv` in
this directory are byte-identical copies of the `research/gen04/`
filings (7 rows each), and each declaration is **identical to its
Gen 3 parent's modulo candidate ID** (checked mechanically this
session: P4=G1 false/G2–G6 true; W4 same; QR4=G4/G5 true;
AD4=G1/G5 true). Main run uses concatenation
`manifest-gen4-P4W4.csv` (14 rows) because `validate_manifest`
requires manifest/extraction candidate sets to match exactly.
Class ratification still PENDING — declared ≠ commensurable.

**Why QR4/AD4 stay out of the shared matrix (observed again).**
Forcing all four into the combined Gen 0–4 run (scratch
`/tmp/combined_forced4.md`) ranks **AD4/QR4 1st/2nd at 0 FAIL /
3 INSUFFICIENT** ahead of every pathway at 0/6 — the same
scope-shrinkage artefact as Gen 2/3; the manifest taxes missing
*required* cells, not `required=false` scope. **Their 0/3 must
never be quoted against any pathway's 0/6, nor AD4's 0/3 against
GEN1-A1's 1/6** — A1's disputed G6 FAIL stays on A1 verbatim.

**AD4 special note.** AD4 is the only Gen 4 candidate with an
executed result, and its result is an *absence* (no charge pins
in the inspected FDA SSED/label class). An absence files no pin,
moves no gate cell, and licenses no A1 model re-run (see
`score-gen4.md` §3). Its adapted rows are therefore unchanged
from AD3 modulo ID; the execution is recorded in
`extract-gen4.csv` claim text and `ad4-extraction-record.csv`,
not in any verdict. Agent triage ≠ human declaration.

## Adapter limitation (observed again)

```text
$ python3 research/scoring/adapt_extraction.py research/gen04/scoring/extract-gen4.csv /tmp/g4stock.csv
adapted 0 rows        # all 34 GEN4-* rows skipped (A–H map only; GEN4 successor still owed)
```

## What was done instead (no code edited)

- `extract-gen4.csv`: frozen 14-col schema, **34 rows** (P4 8,
  W4 8, QR4 11, AD4 7; INSUFFICIENT 21, NA-prereg 12,
  PROVISIONAL-SIGNAL 1 — the inherited leg-(a) row; PASS 0,
  FAIL 0; RECORD 34/34; UNASSESSED 34/34). Built by
  `/tmp/build_gen4_extract.py` from `extract-gen3.csv` by the ID
  map above + Gen 4 source paths; verdicts/tiers/grades copied
  unchanged; AD4 G1/G5 claims updated to record the executed
  absence; P4/W4/QR4 claims annotated "finalization only."
- Adapted files carry the Gen 3 parents' rows modulo IDs —
  correct, because finalization (and AD4's absence) supplies no
  effect, numeric, or verdict. `gate_table.py` and
  `adapt_extraction.py` **not edited**.
- Observed: all three manifest runs exit 0, §(f) reports
  **"(none) — all required cells present"** (manifest tax a
  verified no-op on verdicts); `promoted FALSE` ×4. Scorer
  tests: `python3 -m unittest discover` in `research/scoring`
  → **Ran 27 tests, OK** (+ ASTRA PROBES PASS), unchanged code.
- Scorer v2 semantics (`effective_verdict`, `is_mechanism_only`)
  remain no-ops: 0 PASS proposed, 0 G2 W0/W1 rows. No `--fmea`
  fabricated. `gate-matrix-gen4*.md` carry the scorer's fixed
  pre-Step-3 header verbatim (code provenance), as Gen 1–3.
