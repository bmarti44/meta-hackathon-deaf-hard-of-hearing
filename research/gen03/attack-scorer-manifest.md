# Gen 3 bounded attack — scorer cell-manifest repair (Astra review §1/§4.4, S5)

> **Model routing.** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-02**.
> **Status: bounded attack, not a new generation.** Per the Astra
> adjudication (`reviews/codex-astra-gen2-review.md` §4: "attacks
> now, no new design generation now"), this filing adds **no new
> candidate**, re-scores **no candidate to a new verdict**, and
> does not advance the generation clock (still Gen 2 = 2/4,
> counter 2/2), change STOP, lift G3b BLOCKED, or alter FROZEN.
> **Inspected records only:** the Astra review and
> `research/gen02/Gen2-summary.md` read in full; plus
> `research/scoring/{gate_table.py, README.md,
> test_gate_table.py}`, `research/gen02/scoring/
> {adapted-gen2.csv, adapt-gen2-note.md}`, and the filed Gen 0
> v2 / Gen 1 / Gen 2 matrices re-executed below. No literature,
> no new search, no invented data — all fixture verdicts in the
> new tests are synthetic and labelled so.

## 1. Defect attacked

Astra §1: required-cell completeness is not proved by the scorer;
forcing Q1/R1 in "reproduces the spurious R1 0/2 and Q1 0/3 lead
caused by reduced applicable scope." Mechanism in pre-repair
`gate_table.py`: an all-`NA` gate cell stays `NA`
(`worst_verdict`), and §7 step 2 counts `INSUFFICIENT` **among
applicable gates only** (`summarize`), so declaring gates `NA`
shrinks the denominator and *improves* fitness. A gate with a
`PASS` in one window and an unreported required window is
likewise silently complete. Gen 2 could only refuse Q1/R1
machine entry (extract-only, `adapt-gen2-note.md`); the repair
owed was a declared cell manifest (Gen2-summary §4(6)).

## 2. Repair (implemented, `research/scoring/`)

Optional `--manifest` on `gate_table.py`; **no manifest ⇒
pre-repair behaviour, byte-for-byte** (§4). Schema
`cell-manifest-csv-v1`: `candidate,gate,window,required`
(`window` empty/`*`/`ANY`/`ALL` = any window; `required`
`true/false`, also `1/0`, `yes/no`). New API: `ManifestCell`,
`load_manifest`, `validate_manifest`,
`find_missing_required_cells`; `build_gate_matrix(rows,
manifest=None)` and `render_markdown(summaries,
manifest_missing=None)` are backward-compatible extensions.

With a manifest:

1. **Entry ticket.** Manifest and extraction candidate sets must
   match exactly, and every candidate × gate must be declared
   `true` or `false`. Undeclared gate, extra/unknown candidate,
   duplicate cell, bad gate or `required` value ⇒ exit 2 with
   the offending cells named. A Q1/R1-class design enters a
   manifest run only by *declaring* its footprint.
2. **Missing required cell = explicit `INSUFFICIENT`.** A
   `true` cell satisfied by no applicable (non-`NA`) row at
   that candidate/gate/window contributes `INSUFFICIENT` to its
   gate: it caps a `PASS` from other windows, converts an
   all-`NA` gate from `NA` to `INSUFFICIENT`, and is counted at
   §7 step 2. Every such cell is listed in new output section
   **(f)** (`MISSING -> INSUFFICIENT`), never silently absent.
3. **Declared non-requirement is visible, not silent.**
   `required=false` cells are never penalized — but the `false`
   is a filed, ratifiable declaration, which is the honest form
   of Q1/R1's "not applicable to us" claims.

## 3. Tests (`research/scoring/test_manifest.py`, 9 new)

| Test | Asserts |
|---|---|
| `TestLoadManifest` (2) | any-window/`required` parsing; missing column, bad `required`, duplicate, bad gate all rejected |
| `TestMissingRequiredCell` (3) | missing required **window** caps a `PASS` gate at `INSUFFICIENT` (`n_insufficient` 1→2 incl. forced G3b); `NA` row does not satisfy, `false` cell not penalized; window specificity (`W2` row ≠ `W3` requirement, `*` satisfied) |
| `TestScopeShrinkagePenalized` (1) | Synthetic Q1-like footprint (only G4 applicable): **without** manifest it reproduces the artefact (2 INS, ranks first); **with** a manifest requiring G2–G6 it takes 6 INS, ties the full-footprint candidate on step 2, and loses on the real G2 value. Missing list = G2/G3a/G3b/G5/G6 (G3b already forced, no double count) |
| `TestManifestIsTheEntryTicket` (1) | candidate-without-manifest, manifest-without-rows, and undeclared-gate all raise |
| `TestRenderAndCli` (2) | section (f) only in manifest mode; CLI exit 0 complete manifest / exit 2 incomplete / exit 0 no manifest |

Run (this session): `python3 -m unittest discover -s
research/scoring` → **Ran 27 tests, OK** (18 pre-existing + 9
new) **+ `ASTRA PROBES PASS`**. One deliberate stderr line in
the CLI test is the expected exit-2 error message.

## 4. Regression: filed matrices byte-compare (no manifest)

Re-run with `--out` against each filed matrix, before and after
the edit (identical results; CLI-to-stdout adds exactly one
trailing newline vs the `--out` file, as Astra noted):

| Input | Filed matrix | Bytes | Filed SHA-256 | After repair |
|---|---|---:|---|---|
| `gen00/scoring/adapted_v2.csv` | `gate-matrix-gen0-v2.md` | 5,395 | `f256e1f2…` | **byte-identical** (`cmp` clean) |
| `gen01/scoring/adapted-gen1.csv` | `gate-matrix-gen1.md` | — | — | **byte-identical** (`cmp` clean) |
| `gen02/scoring/adapted-gen2.csv` | `gate-matrix-gen2.md` | 2,850 | `a9e45c1f…` (matches Astra §1) | **byte-identical** (`cmp` clean) |

Completeness check in the other direction: re-running Gen 2
**with** a correct manifest (P2/H2: G1 `false`, G2–G6 `true`,
any window) yields the filed matrix as an exact prefix plus
section (f) reporting "(none) — all required cells present".
No filed matrix, CSV, score, or candidate file was modified.
Known pre-existing staleness, **not** caused or fixed here:
`research/scoring/demo_matrix.md` already differed from the
demo CLI output before this edit (v2 grade/tier downgrades on
the synthetic Track R rows); left untouched as out of scope.

## 5. What this does NOT do (fences)

- **No commensurability claim.** Astra §1: "A cell manifest
  alone would not make Q1/R1/H2 commensurable with pathways."
  Agreed. The manifest makes scope *declared and taxed*, not
  equal. Whether a `false`-heavy footprint may be ranked
  beside pathways — and H2's prospective reclassification
  beside measurement/attack deliverables — remains a human
  candidate-class decision (Astra §4(4)), not a scorer default.
- **No new scoring of Q1/R1/H2** was run for the record; the
  Q1-like test is a synthetic unit fixture. Scoring them for
  real needs humans to first ratify a manifest per candidate
  class, prospectively (no retro-repair of the Gen 2 sequence).
- **No adapter repair:** `adapt_extraction.py`'s A–H ID map
  (Gen2-summary §4(6) second half) is untouched; still owed a
  declared successor before any future generation is scored.
- Stratum-level required cells are out of scope of the
  commissioned schema (`candidate,gate,window,required`); a
  required cell is satisfied by any stratum's applicable row.
  A G2 W0/W1 mechanism row counts as *present* for its declared
  cell but is still excluded from gate aggregation — disclosed
  in code, consistent with the v2 `is_mechanism_only` rule.
- No verdict, promotion, kill, Q0, G3b, or STOP state changes.
  **FROZEN retained. G3b BLOCKED.**

*End. Bounded attack filed under `research/gen03/` per holder
direction; not generation 3 and does not advance the clock.*
