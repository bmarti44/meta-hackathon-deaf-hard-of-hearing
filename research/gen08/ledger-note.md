# Gen08 ledger note — external evidence vs scoring

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **muse-wonder-full-1.0**, 2026-11-03. Agent design work, not
> human extraction/adjudication. Inspected only; no invented data.
> Source of record: [reviews/codex-unstick-2.md](../../reviews/codex-unstick-2.md)
> (Astra second unstick, read in full) and
> [research/unstick2/inputs.json](../unstick2/inputs.json).
> GOAL.md, Appendix A, and every prior `extract-*.csv` are unchanged.

## What this delta files

[external-evidence-ledger.csv](external-evidence-ledger.csv) — one
DESIGN row per external contrast (7 rows, 14-col schema of
[gen00/extraction-schema.md](../gen00/extraction-schema.md),
`grade=UNASSESSED`, `verdict_proposed=INSUFFICIENT` throughout):
Schulz 2026 (DOI 10.3389/fauot.2025.1746635), Borjigin 2024
(PMID 38853168), Gajecki 2023 (PMID 37030808), Fused Deep ACE
(arXiv:2310.01122 v1), DB-OTO/CHORD (PMID 41085057), and Cheng
JAMA (PMID 40690227) as its two distinct contrasts, Fig. 3B
(disyllable thresholds) and Fig. 3C (singing in-tune).

Each `claim` states both halves: the external result as Astra
inspected it, and the gap to the destination cell (population /
intervention identity / comparator / endpoint / quiet NI). Filing a
row changes no destination verdict: GEN5-J1 and GEN6-J2 `G2×W3`,
J `G5`, G/Ga `G2×W3×OTOF`, and `G2-music×W3` all remain
INSUFFICIENT. Real external benefit ≠ project PASS (Astra L5).

## Ledger vs scoring separation (the load-bearing rule)

- **Ledger `effect`** = source units against the *named external
  comparator* in the `comparator` column (unprocessed mixtures,
  bilateral ACE without NR, pretreatment, unilateral CI). It is
  never "vs frozen."
- **Scorer `delta_g2_db`** ([gate_table.py](../scoring/gate_table.py),
  [adapt_extraction.py](../scoring/adapt_extraction.py)) means
  **SRT gain versus `frozen_bilateral_eCI_v1`**, and the
  lexicographic ranking consumes it even from INSUFFICIENT rows.
  Putting Schulz's 5.9 dB there would fabricate a vs-frozen
  tie-break for an unimplemented candidate. Astra prohibits this
  explicitly (L36: "Inserting 5.9 there would create a misleading
  tie-break"). The same ban covers Cheng's 6.3 (a difference of
  medians in dB SPL, not a dB SNR-50 mean effect) and any
  pp→dB conversion of Borjigin (forbidden-conversion rule,
  schema §2.9).
- **Mechanical guards, verified at build:** the file is not named
  `extract-*.csv`; candidate keys are `EXT-*` ledger keys with no
  track-map entry, so `adapt_extraction.adapt()` skips every row
  (0 adapted rows); no `effect` cell is a bare number, so the
  adapter's bare-number rule could not mint a `delta_g2_db` even
  if a key were ever mapped. Do not add `EXT-*` to a track map,
  rename this file into a generation extraction, or copy its
  effects into a scored candidate row.
- **What would make an external number scoreable:** intervention
  and estimand identity — the exact external processor/therapy,
  the cell's named comparator in the same experiment, the cell's
  population/window and endpoint, and quiet −5-pp NI where G2
  requires it (Appendix A v1 §2/§4; Astra L34–L36). An exact
  replication could inherit evidence for *that* contrast; sharing
  the label "DNN" or "gene therapy" cannot. Until then these rows
  are T3/T4 external support for *design decisions* (e.g. Astra's
  ranked pushes: causal-checkpoint replay, correct-comparator
  adult study), at most provisional signal under the Appendix,
  and GRADE stays UNASSESSED pending human dual extraction.

## Limits carried from Astra, not laundered here

Targeted search, not a systematic resweep. Gajecki 2023 and
DB-OTO are abstract-level in the review (IEEE 418; NEJM 403);
Fused Deep ACE is preprint v1, not the final 2024 journal version;
Schulz raw paired differences and supplements were not obtained;
the Keles checkpoint's serialized `causal`/`norm_type` remain
unverified (the 382.5-ms figure is conditional on upstream
defaults). Every opened result is DESIGN, not retrospectively
held-out evidence; no validation count changes (Astra L105).
No non-significant contrast above is read as non-inferiority, and
Cheng Fig. 3C does not erase the poorer GT+CI localization Astra
notes at L19.
