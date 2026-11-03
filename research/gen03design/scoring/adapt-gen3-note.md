# Gen 3 adaptation note — ID→track map, manifest treatment, QR3/AD3 single-candidate runs

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Holder Sisyphus directive; this
> note 2026-11-03. GOAL v2.2. **Gen clock: Gen 3 = generation
> 3 of max 4 (3/4 on human acceptance). G3b BLOCKED; same PASS
> bar as Gen 0/1/2; no PASS anywhere; no promotion; FROZEN
> retained. No invented data.**

## Documented Gen 3 candidate-ID → track / scorer-treatment table (binding for this re-score)

| Gen 3 ID | Kind (per candidate file) | Parent(s) | Track for `gate_table.py` | Scorer treatment |
|---|---|---|---|---|
| `GEN3-P3` | Fused recombinant, H2 embedded as measurement core | GEN2-P2 × GEN2-H2 | **P** (portfolio; G1 NA disclosed) | **`adapted-gen3.csv` + `gate-matrix-gen3.md` WITH `--manifest`** (`manifest-GEN3-P3.csv`: G1 false, G2–G6 true) — 8 rows |
| `GEN3-W3` | Wild-card recombinant, interaction primary | GEN1-F1m × GEN2-P2 | **P** (portfolio; G1 NA disclosed) | **Same main manifest run** (`manifest-GEN3-W3.csv`: identical declaration) — 8 rows |
| `GEN3-QR3` | Decider/rule-test *program*; "Track: none; not promotable" (§1) | GEN2-Q1 + GEN2-R1 | *none by design* — scorer's `_norm_track` accepts P/R only, so its single-candidate file carries **`P` as a scorer-required placeholder, not a class claim** | **Separate single-candidate `--manifest` run only** (`adapted-gen3-QR3.csv`, `manifest-GEN3-QR3.csv`: G4/G5 true, rest false, → `gate-matrix-gen3-QR3.md`). **Absent from every shared ranking, Pareto set, and fitness key** |
| `GEN3-AD3` | Documentary/evaluability child; "not promotable" (§1) | GEN1-A1 | **P device lineage** (candidate's own words) | **Separate single-candidate `--manifest` run only** (`adapted-gen3-AD3.csv`, `manifest-GEN3-AD3.csv`: G1/G5 true, rest false, → `gate-matrix-gen3-AD3.md`). Absent from shared ranking/Pareto/fitness as above |

**Why QR3/AD3 stay out of the shared matrix even now that
manifests exist (observed, not assumed).** A manifest taxes a
*missing required* cell; it does not tax a `required=false`
declaration. QR3/AD3 therefore still carry fewer applicable
gates. Observed scratch run forcing all four Gen 3 candidates
into one Gen 1+2+3 matrix (`/tmp/combined_forced.md`): **AD3
and QR3 rank 1st/2nd at 0 FAIL / 3 INSUFFICIENT** (their two
required INSUFFICIENT + forced G3b), ahead of every pathway
at 0/6 — the identical scope-shrinkage artefact Gen 2
documented for Q1/R1, now with declared footprints. Declared
≠ commensurable (Astra S1; QR3 §1/§8 requires human
ratification of manifest *and candidate classes* before
scored-matrix entry). Single-candidate manifest runs give
QR3/AD3 an honest, taxed `promoted FALSE` without
manufacturing fitness. **Their 0/3 must never be quoted
against any pathway's 0/6, and AD3's 0/3 must never be
quoted against GEN1-A1's 1/6** — A1's disputed G6 FAIL stays
on A1 verbatim (AD3 §8); AD3 declaring G6 `false` is class
scope, not repair.

## Adapter limitation (observed again)

`adapt_extraction.py` still maps candidates A–H only:

```text
$ python3 research/scoring/adapt_extraction.py research/gen03design/scoring/extract-gen3.csv /tmp/g3stock.csv
adapted 0 rows        # all 34 GEN3-* rows skipped
```

## What was done instead (no code edited)

- `extract-gen3.csv`: frozen 14-col schema, **34 rows**
  (P3 8, W3 8, QR3 11, AD3 7; INSUFFICIENT 21, NA-prereg 12,
  PROVISIONAL-SIGNAL 1 — the inherited R1 leg-(a) row;
  PASS 0, FAIL 0; RECORD 34/34; UNASSESSED 34/34).
- Adapted files written by `/tmp/build_gen3_extract.py`
  applying the stock adapter's exact rules (sublabel
  collapse, verdict map, numerics from bare-number `effect`
  only — none) with the ID map above. `gate_table.py` and
  `adapt_extraction.py` **not edited**.
- Per-candidate manifests copied byte-identical from
  `research/gen03design/manifest-GEN3-*.csv` (filed with the
  candidates by the design child; `cell-manifest-csv-v1`,
  all 7 gates declared per candidate). Main run uses the
  concatenation `manifest-gen3-P3W3.csv` because
  `validate_manifest` requires manifest/extraction candidate
  sets to match exactly.
- Observed: all three manifest runs exit 0, §(f) reports
  **"(none) — all required cells present"** (every required
  cell was filed INSUFFICIENT, so the manifest tax is a
  verified no-op on verdicts, not an assumed one);
  `promoted FALSE` ×4. Scorer tests: `python3 -m unittest
  discover` in `research/scoring` → **Ran 27 tests, OK**
  (+ ASTRA PROBES PASS), unchanged code.
- Scorer v2 semantics (`effective_verdict`,
  `is_mechanism_only`) remain no-ops here: 0 PASS proposed,
  0 G2 W0/W1 rows. No `--fmea` fabricated (all bands
  UNPINNABLE; Track P does not use the G5 aggregate).
- `gate-matrix-gen3*.md` carry the scorer's fixed pre-Step-3
  header verbatim (code provenance, not this input), as
  Gen 1/2. Post-freeze edits = new candidate.
