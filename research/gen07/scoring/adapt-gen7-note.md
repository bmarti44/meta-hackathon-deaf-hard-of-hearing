# Gen 7 adapter note — `--track-map` path, no manual adaptation

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-03. Gen 7 under
> GOAL v2.3** (no generation cap, no loop stop rules).
> **G3b BLOCKED; same PASS bar as Gen 0–6; no PASS; FROZEN
> retained. Inspected records only; no invented data.**

## Candidate-ID → track / scorer-treatment table (binding)

| Gen 7 ID | Kind | Parent | Track | Treatment |
|---|---|---|---|---|
| `GEN7-P7` | DEEPEN: P6 + M-P7-1 only (retrospective shadow-audit estimand) | GEN6-P6 | **P** (G1 NA disclosed) | `adapted-gen7.csv` via stock adapter `--track-map=track-map-gen7.csv`; `gate-matrix-gen7.md` WITH `--manifest` |

`candidate-J3-bench.md` files **no rows**: it states verbatim
"J3 is not a scored candidate" — it is the executable form of
GEN6-J2 Stage 0, unfielded pending HP-J1-4. Scoring it would be
the governance error the candidate itself names. `monitoring.md`
and `resweep2.md` are not candidates and file no rows.

**⚑ Machinery debt discharged (Gen6-summary §4.6).** Gen 7 is
the first generation adapted with **no manual adapted-CSV
construction**: `adapt_extraction.py --track-map=` maps
`GEN7-P7 → P` from `track-map-gen7.csv` (2 lines). Observed:

```text
$ python3 research/scoring/adapt_extraction.py extract-gen7.csv adapted-gen7.csv --track-map=track-map-gen7.csv
adapted 8 rows
$ python3 research/scoring/adapt_extraction.py extract-gen7.csv /tmp/g7stock.csv   # no map, control
adapted 0 rows        # A–H built-in map only, as Gen 2–6
```

Adapted P7 ≡ adapted GEN6-P6 modulo ID (verified mechanically,
`EQUIVALENCE OK`) — expected: M-P7-1 changes the estimand, not
any gate cell, and no audit data exist. `gate_table.py` /
`adapt_extraction.py` **not edited** this generation.

**Manifest.** P7 filed no manifest CSV (as P6);
`manifest-GEN7-P7.csv` / `manifest-gen7-main.csv` are scoring-step
transcriptions of the §1 declaration ("identical to P6/P5/P4:
G1 `false`, G2–G6 `true`"). Ratification PENDING; §(f) reports
all required cells present (manifest tax a verified no-op).
