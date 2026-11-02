# Extraction schema (Step 2) — Gen 0 evidence CSV

> **Model routing (GOAL §9).** Requested route for this file:
> **Sol 6.1, high** (generation-execution worker). Actual
> runtime model: **`muse-wonder-full-1.0` fallback** at the
> same effort split (Sol 6.1 unavailable in this runtime).
> Substitution disclosed per §9 rule 3. No claim here is
> Sol 6.1 work.
>
> **Date:** 2026-11-02. **GOAL:** v2.2. **Status:
> PRE-REGISTRATION — schema frozen BEFORE Step 3 scoring.**
> Template file: `extraction_template.csv` (same headers,
> same date). Changes after scoring starts = schema v2 with
> migration note; v1 extracts preserved (no-overwrite rule).
>
> **Exploratory-after-seen label: YES.** Seen before writing:
> GOAL.md v2.2 §9 agent contract (structured claims table:
> claim | source DOI/PMID | tier | gate-cell | effect + N —
> this schema is its CSV operationalization, in the column
> order mandated at Step 2); Step 0 bibliography §2 verdict/
> locator discipline (abstract vs authoritative-record levels,
> post-skeptic downgrades, "N not in abstract" preservation);
> Step 1 pin summary + Appendix A v1 (gate-cell definitions,
> PINNED/PROVISIONAL/UNPINNABLE/BLOCKED labels, convention
> flags). The schema therefore encodes lessons from seen
> failures (conflated Ns, missing denominators, degraded
> comparators) — it does not encode any Step 3 result, none
> of which existed at writing.
>
> **G3b BLOCKED (applies to every candidate).** Every G3b row
> for candidates A–H and frozen has `verdict_proposed =
> INSUFFICIENT`, empty `effect`, and a `claim` printing "G3b:
> BLOCKED (INSUFFICIENT) — co-design pending" (see template
> starter rows). **No Track P promotion is possible at v1.**
> Schema validators must reject any G3b row proposing PASS/
> FAIL at v1.
>
> **No invented citations or numbers.** The template's starter
> rows assert no effect, no N, and no source finding — they
> pre-register blocked/unpinnable states only. Example values
> in §2 are format illustrations labelled EXAMPLE.

## 1. File format

- One **row per claim**: candidate × gate × window × stratum
  × source. A study informing 3 cells = 3 rows (same
  `source_id`, different gate/window/stratum) — but held-out
  siding is by study (`heldout-manifest.md`), never by row.
- UTF-8 CSV, comma-delimited, `"` quoting (RFC-4180 style).
  Free-text fields (`claim`, `effect`, `comparator`) must not
  contain unescaped newlines; use `; ` for lists inside a cell.
- Lines starting with `#` are provenance-header comments
  (template lines 1–n). Parsers — including `gate_table.py`
  when written — must skip leading `#` lines, then read the
  column-header row. Comment lines are never data.
- Column order is frozen (v1): `candidate,gate,window,
  stratum,claim,source_id,tier,grade,effect,n,comparator,
  verdict_proposed,extractor,verified_date`.
- Empty = **not yet extracted / not reported by source** (the
  distinction is stated in `claim`, e.g. "N not in abstract").
  Empty never means zero. `NA` is a deliberate value only
  where §2 allows it.
- Extract extractions into a new versioned file per Step 3
  batch (e.g. `extraction_v1_YYYY-MM-DD.csv`); the template
  itself is never overwritten with data.

## 2. Columns (frozen definitions)

| # | Column | Definition + allowed values |
|---|---|---|
| 1 | `candidate` | `A`…`H` (one Gen 0 candidate per GOAL §8 family), `FROZEN` (frozen_bilateral_eCI_v1 reference rows), `Q0-P`, `Q0-A`, `Q0-L` (Q0 components per `Q0-thresholds.md`), or `PORTFOLIO` (Gen ≥1 only). Candidate files (Appendix B) define what each letter *is*; the CSV never redefines a candidate. Track (P/R) is looked up from the candidate file, not stored here (single source of truth). |
| 2 | `gate` | `G1-spectral`, `G1-temporal`, `G2`, `G2-music`, `G3a`, `G3b`, `G4`, `G4-AAV`, `G5`, `G6` (Appendix A v1 §2 cells), or `NA-struct` for Appendix B completeness rows (FMEA filed? timeline stated?) that feed a gate without being its effect estimate. Claim cap rows comparing evolving standard use the same gate with `comparator` stating "evolving-standard (sensitivity)". |
| 3 | `window` | `W0` (0–9 mo), `W1` (9–24 mo), `W2` (2–3.5 y), `W3` (3.5–7 y), `ADOL` (adolescence sensitivity), `ALL` (pre-declared window-spanning, e.g. G4 histology), or `NA` (source has no age mapping — reason in `claim`). Decision-time origin, when the claim is decision-time, is prefixed in `stratum` (see below), not here. |
| 4 | `stratum` | `; `-separated `key=value` pairs from GOAL §3.2, e.g. `etiology=OTOF; anatomy=normal; modality=signed; decision_origin=6mo; genotype_state=pending`. Keys: `etiology, anatomy, syndromic, comorbidity, entry_time, decision_origin, genotype_state, modality, home_language, ei_dose, species, lab`. **Mandatory:** `species` for every animal/bench row (= `human` for human rows); `lab` (originating group) for every T0–T3 row (allegiance rule, protocol §6); `modality` for every G3a row. Unreported stratifiers = `key=unreported` (never omitted silently on G3/G6 rows). Pooled-across-strata source values keep `stratum=pooled-as-reported` + pooling warning in `claim`. |
| 5 | `claim` | One falsifiable sentence: what this row asserts for this cell, incl. direction and the exact quantity in `effect`. Must carry travelling labels where they apply: `PROVISIONAL` / `CONVENTION` / `abstract-level` / `design-only` / `mouse-only` / `vs degraded comparator` / `N not in abstract`. G3b rows: fixed BLOCKED sentence (§header). No promotional language; write the claim a skeptic could kill. |
| 6 | `source_id` | Primary identifier + locator: `PMID:########` and/or `DOI:10.…` and/or `NCT########` / `FDA:STN-or-PMA-id`, followed by ` @ ` + locator (`Abstract Results`, `USPI §14 Table 2`, `p.3 §6.1`, `CTgov outcomesModule`, …). Registry rows add `as-posted YYYY-MM-DD`. Step 0/1 cross-ref in brackets where one exists, e.g. `[Step0 Ch1a]`, `[AppA N1]` — cross-ref never replaces the primary ID. Sources without a verified ID (`source_id=UNVERIFIABLE`) cannot support PASS/FAIL; the row exists to log the gap. |
| 7 | `tier` | `T0` `T1` `T2` `T3` `T4` per GOAL §5.3 (see protocol §7), or `RECORD` (label/registry fact), or `REVIEW` (narrative review — framing only). Animal maturity/deafening that determines T1-vs-T2 is stated in `claim`/`stratum`. Minimum-tier check vs Appendix A v1 §2 happens at scoring, not by inflating `tier` here. |
| 8 | `grade` | Adapted GRADE **for this cell** after RoB tool + downgrades (protocol §§5–6): `High`, `Moderate`, `Low`, `VeryLow`, or `UNASSESSED` (pre-extraction default). RoB tool + headline downgrade reasons appended in `claim` (e.g. `RoB:SYRCLE; -1 allegiance inventor-lab; -1 indirect adult-archival`). Agent-proposed grades stay `UNASSESSED`-capped for gate purposes until human verification (§3) — the word in this column is a proposal like `verdict_proposed`. |
| 9 | `effect` | Extracted effect **verbatim in source units** with uncertainty as reported: e.g. (EXAMPLE format) `SRT diff -3.2 dB (95% CI -5.0 to -1.4); BKB-SIN SNR-50`. Forbidden conversions (Step 1 P11): no SMD→dB, no RR→%, no ripple→channels arithmetic, no unilateral→bilateral doubling, no pooled SD. Dual-report non-convertible rulers as separate rows. Qualitative-only sources: `qualitative: <exact finding>` — never a paraphrased number. G3b / unpinnable rows: empty. |
| 10 | `n` | Denominators verbatim: `n=<analysed>/<enrolled or implanted>` per arm where comparative (`n=16/20 label set` style), unit named (`children`, `ears clustered in N children`, `animals`, `bones`, `devices`, `seeds`). All three CHORD-style Ns (treated/evaluable/report-cut) recorded where a source has them — never conflated (Step 0 O2b lesson). `n=NOT-IN-ABSTRACT` / `n=NOT-REPORTED` preserved as such; rows without extractable N cannot decide Q0 or PASS a numeric cell (Q0-thresholds §2.3). Registry target N labelled `target`. |
| 11 | `comparator` | What `effect` is against, named concretely: `frozen_bilateral_eCI_v1 (concurrent cohort, <array/era>)`, `evolving-standard (sensitivity)`, `same-study sham/unimplanted`, `clinical map`, `degraded experimental monopolar [flag]`, `none-single-arm`, `vocoder-simulation`, … "vs control" alone is invalid. Head-to-head G1 rows name the frozen array type/era/fitting (App.A §3.2 bar). |
| 12 | `verdict_proposed` | Proposer's cell suggestion: `PASS`, `FAIL`, `INSUFFICIENT`, `PROVISIONAL-SIGNAL` (Low GRADE / below-tier-but-reportable / design-only), or `NA-prereg` (pre-declared NA such as F/G/H G1). This is **not** the adjudicated verdict: judges + `gate_table.py` produce verdicts; disagreement preserves both (dissent rule). Validators enforce: G3b→`INSUFFICIENT` only; `grade=Low/VeryLow/UNASSESSED` → never `PASS`; `tier` below App.A minimum → never `PASS`; G4-AAV rows default `FAIL` until re-dose evidence (protocol §6). |
| 13 | `extractor` | Who extracted + who verified: `<extractor-id>` where agent ids include model+effort (e.g. `agent:muse-wonder-full-1.0/high`) and human ids are roster slots/names once filled (`human:H-7`). Dual extraction recorded as `<pre-extractor>+<human-verifier>`; agent-only rows are pre-extraction by definition (protocol §8). Holder-extracted load-bearing rows require the `+external-audit:<id>` form. |
| 14 | `verified_date` | `YYYY-MM-DD` of the *inspection* this row rests on (re-inspection = new row version, old row retained in prior CSV version). Pre-registration starter rows carry `2026-11-02` (the date the blocked/unpinnable state was verified against Step 0/1 files). Registry "updated" dates belong in `source_id`, not here. |

## 3. Validation & scoring handoff (for `gate_table.py`)

Until `gate_table.py` exists (Step 2 completion item,
`freeze-checklist.md`), validators are manual + peer-checked.
The script, once written, must implement at minimum:

1. Skip `#` header lines; enforce §2 allowed values; reject
   forbidden conversions flagged in `effect` patterns is out
   of scope — human audit owns that check.
2. Enforce §2.12 validator rules + GRADE map (protocol §6):
   PASS requires `grade ∈ {High, Moderate}` (human-verified)
   AND tier ≥ Appendix A minimum AND decision-time analysis
   flags present; else downgrade to PROVISIONAL-SIGNAL /
   INSUFFICIENT with reason emitted, never silent.
3. Join `source_id` → `heldout-manifest.md` side; flag
   design-only would-be passes; flag `species=mouse`-only cells.
4. Emit gate matrix (PASS/FAIL/INSUFFICIENT per candidate ×
   gate × window), searched-family log (all rows incl.
   INSUFFICIENT), and lexicographic ranking (protocol §7) —
   deterministically, from the CSV + Appendix A version only.
5. Refuse to emit a promotion verdict while any required
   G3b cell is INSUFFICIENT — i.e. always, at v1 (print the
   BLOCKED banner instead).

Sampled error audit (protocol §8): human verifier re-extracts
a pre-stated random sample of agent rows; error rate reported
in the Step 3 synthesis header. Rows failing audit are
corrected as new versions; systematic error in a field
triggers full re-extraction of that field.

## 4. Worked format examples (EXAMPLE — not data)

```csv
# EXAMPLE rows illustrating format only. Effects below restate
# Step 0 §2 headline values at abstract level to show field
# use; they are NOT Step 3 extractions and decide nothing.
A,G1-spectral,W3,species=human; lab=EXAMPLE,EXAMPLE ripple claim abstract-level design-only,PMID:16158665 DOI:10.1121/1.1944567 @ Abstract [AppA N1],T3,UNASSESSED,ripple threshold in rip/oct (dual-report; no channels conversion),n=NOT-IN-ABSTRACT,same-study frozen array (named in full text owed),PROVISIONAL-SIGNAL,agent:muse-wonder-full-1.0/high,2026-11-02
```

*End. Companion template: `extraction_template.csv`. Rules
referenced: `protocol.md` §§5–8, `heldout-manifest.md`,
`Q0-thresholds.md` §2.3, Appendix A v1 §2.*
