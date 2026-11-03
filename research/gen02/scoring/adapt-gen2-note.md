# Gen 2 adaptation note — ID→track mapping, Q1/R1 exclusion, adapter limitation

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. **Holder-directed continuation
> 2026-11-02**; this note 2026-11-03. GOAL v2.2.
> **Gen clock: Gen 2 = generation 2 of max 4. G3b BLOCKED;
> same PASS bar as Gen 0/1; no PASS anywhere; no promotion;
> FROZEN retained. No invented data.**

## Documented Gen 2 candidate-ID → track / scorer-treatment table (binding for this re-score)

| Gen 2 ID | Kind (per candidate file) | Parent(s) | Track for `gate_table.py` | In `adapted-gen2.csv` / gate matrix? |
|---|---|---|---|---|
| `GEN2-P2` | Fused portfolio recombinant (1 logged change: fuse + I1→I1*) | GEN1-P1 × GEN1-Ga | **P** (portfolio; G1 NA disclosed) | **Yes** — 8 rows |
| `GEN2-H2` | Mutant split child (1 subtraction: norming only) | GEN1-H1 | **P** (pathway; G1 NA pre-declared) | **Yes** — 8 rows |
| `GEN2-Q1` | Decider study; claims no gate PASS for itself (T2; §1/§8) | GEN0-G Q0 obligation via GEN1-Ga | *none assigned* | **No — extract-only.** Its §8: scoring it on G1/G2/G3a/G3b/G6 "would be the category error review S5 warns the scorer cannot yet police — cell manifest repair owed before any machine scoring includes Q1" |
| `GEN2-R1` | Rule-test; "not promotable, earns no gate verdict" (§1) | G4-AAV presumptive rule + sweep hook | *none* ("Track: none") | **No — extract-only.** Its §8 scorer note: "R1 must be excluded from `gate_table.py` candidate matrices until a cell manifest exists" |

GEN1-A1 and GEN1-F1m have **no Gen 2 child** (fitness §8:
A1×F1m cross rejected/deferred); both carry over unchanged
and are not re-scored as Gen 2 rows. Retired sibling
`GEN2-H2b` is not a candidate (H2 §1) and has no rows.
Track R contains no Gen 2 candidate.

**Why exclusion is not optional (observed artefact).** A
scratch run forcing Q1/R1 into the matrix on their own
declared footprints (`/tmp/combined_qr.md`, scratch only)
ranks **GEN2-R1 first (0 FAIL / 2 INSUFFICIENT) and
GEN2-Q1 second (0/3)**, ahead of every real candidate —
purely because NA rows shrink the applicable-gate count
at §7 step 2 while the scorer forces their NA G3b back to
INSUFFICIENT. That is scope shrinkage, not fitness. It is
the exact failure their §8 notes and external-review §5
(no cell manifest / no required-vs-optional distinction)
predict. Counting it would falsely reset the §7(5b)
no-improvement counter. Q1/R1 are therefore scored
**narratively, cell-by-cell, in `score-gen2.md` only**,
on their declared footprints.

## Adapter limitation (observed, not assumed)

`research/scoring/adapt_extraction.py` hard-codes
`TRACK = {"A","B",...,"H"}` and silently skips every
other candidate ID — unchanged since Gen 1. Observed:

```text
$ python3 research/scoring/adapt_extraction.py research/gen02/scoring/extract-gen2.csv /tmp/gen2_stock_adapted.csv
adapted 0 rows -> /tmp/gen2_stock_adapted.csv      # all 33 GEN2-* rows skipped
```

Control: re-adapting `extraction_v1_2026-11-02.csv`
reproduces committed `adapted_v1.csv` byte-identically
(185 rows, `diff` clean, this session). The limitation
is the ID map only.

## What was done instead (no silent code edit)

- `extract-gen2.csv` keeps the frozen 14-column schema
  (33 gate-cell rows: P2 8, H2 8, Q1 8, R1 9; verdicts
  INSUFFICIENT 19, NA-prereg 13, PROVISIONAL-SIGNAL 1,
  PASS 0, FAIL 0; tier RECORD 33/33; grade UNASSESSED
  33/33). `GEN2-*` extends the schema col-1 enumeration —
  deviation declared in the CSV header, as for Gen 1.
- `adapted-gen2.csv` (16 rows: P2+H2 only) was written
  by `/tmp/build_gen2_extract.py` applying the stock
  adapter's exact published rules — sublabel collapse
  (G1-spectral→G1, G2-music→G2, G4-AAV→G4), verdict map
  (NA-prereg→NA, PROVISIONAL-SIGNAL→INSUFFICIENT),
  numerics only from bare-number `effect` (none in the
  adapted set) — with the single documented substitution
  of the ID→track table above. `gate_table.py` was
  **not edited**.
- **Scorer v2 semantics, verified in source this session**
  (`research/scoring/gate_table.py:175-208`):
  `effective_verdict` downgrades any PASS below
  Moderate GRADE or below the Appendix A minimum tier
  to INSUFFICIENT; `is_mechanism_only` excludes G2 W0–W1
  rows from aggregation. Both are **no-ops on Gen 2 by
  construction** (0 PASS proposed anywhere; 0 G2 W0/W1
  rows), so v2 changes no Gen 2 cell — stated so nobody
  credits/blames the v2 fix for this matrix. Tests:
  `python3 -m unittest discover` in `research/scoring`
  → **Ran 18 tests, OK** (+ `ASTRA PROBES PASS`), this
  session, unchanged code.
- `gate-matrix-gen2.md` carries the scorer's fixed
  header text (written before Step 3, referring to
  Gen 0) verbatim; it describes the *code's* provenance,
  not this input — same caveat as Gen 1.
- No `--fmea` input was fabricated: all Gen 2 FMEA
  probability bands are UNPINNABLE (candidate §10s),
  Track P does not use the G5 aggregate, Track R is
  empty — as Gen 0/1.

A future scorer version with a declared cell manifest
(review §5) is the precondition for machine-scoring
Q1/R1-class candidates; until then this note is the
mapping of record. Post-freeze edits = new candidate.
