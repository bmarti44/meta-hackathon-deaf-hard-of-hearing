# Gen 1 adaptation note — ID→track mapping + `adapt_extraction.py` limitation

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-02**. GOAL v2.2.
> **G3b BLOCKED; no promotion possible at v1. FROZEN retained.**

## Documented Gen 1 candidate-ID → track table (binding for this re-score)

| Gen 1 candidate ID | Kind | Gen 0 parent(s) (survivors only) | Track | G1 treatment |
|---|---|---|---|---|
| `GEN1-P1` | Sequenced portfolio recombinant | G + H + A-standard (clinical monopolar comparator arm, not focal challenger) | P | NA disclosed; device verdict frozen-equivalent; no G1 win |
| `GEN1-A1` | Mutant (1 logged change: kill-test design) | A | P (device) | Applicable — INSUFFICIENT |
| `GEN1-Ga` | Mutant (1 logged change: concurrent comparison) | G | P (pathway) | NA pre-declared |
| `GEN1-H1` | Mutant (1 logged change: identification + norms) | H | P (pathway) | NA pre-declared |
| `GEN1-F1m` | Mutant (1 logged change: concurrent comparison) | F (F1 arm only) | P (pathway) | NA pre-declared |

B (retired-killed), C/D (watch), E (parked) are **not** parents
of any row. Track R contains no Gen 1 candidate.

## Adapter limitation (observed, not assumed)

`research/scoring/adapt_extraction.py` hard-codes
`TRACK = {"A","B",...,"H"}` and silently skips every other
candidate ID. Observed on this re-score's input:

```text
$ python3 research/scoring/adapt_extraction.py research/gen01/scoring/extract-gen1.csv /tmp/gen1_stock_adapted.csv
adapted 0 rows -> /tmp/gen1_stock_adapted.csv        # all 41 GEN1-* rows skipped
```

Control run confirming the stock adapter is otherwise sound:
re-adapting `extraction_v1_2026-11-02.csv` reproduces the
committed `adapted_v1.csv` byte-identically (185 rows, `diff`
clean). The limitation is the ID map only.

## What was done instead (no silent code edit)

- `extract-gen1.csv` keeps the frozen 14-column Gen 0 schema
  (`extraction-schema.md`); its `candidate` values `GEN1-*`
  extend that schema's column-1 enumeration (A–H / FROZEN /
  Q0-* / PORTFOLIO) — deviation declared here and in the CSV
  header, not hidden.
- `adapted-gen1.csv` was written **manually** (build script
  `/tmp/build_gen1_extract.py`) applying `adapt_extraction.py`'s
  exact published rules — sublabel collapse
  (G1-spectral/G1-temporal→G1, G2-music→G2), verdict map
  (NA-prereg→NA, PROVISIONAL-SIGNAL→INSUFFICIENT), numerics only
  from bare-number `effect` (none exist in Gen 1 — all blank) —
  with the single documented substitution of the ID→track
  table above for the hard-coded A–H map.
- `gate_table.py` was **not edited**. It accepts arbitrary
  candidate strings and Track P/R, forces G3b INSUFFICIENT, and
  produced `gate-matrix-gen1.md` deterministically. Its fixed
  header text (written before Step 3, referring to Gen 0) is
  retained verbatim in that output; it describes the *code's*
  provenance, not this input — do not read "No Gen 0 extraction
  CSV was seen" as applying to the Gen 1 re-score, which
  explicitly re-uses that CSV as inherited evidence.
- Repo tests: `python3 -m unittest` in `research/scoring` →
  **Ran 18 tests, OK** (unchanged code).

A future `adapt_extraction.py` v2 taking a `--track-map` file
would remove the manual step; until human freeze, this note is
the mapping of record. Post-freeze edits = new candidate.
