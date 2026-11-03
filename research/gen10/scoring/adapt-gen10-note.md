# Gen 10 adapter note — `--track-map` path, conditional J4 only

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-03. Gen 10 under
> GOAL v2.3** (no generation cap, no loop stop rules).
> **G3b BLOCKED; same PASS bar as Gen 0–7; no PASS; FROZEN
> retained. Inspected records only; no invented data.**

## Candidate-ID → track / scorer-treatment table (binding)

| Gen 10 ID | Kind | Parents | Track | Treatment |
|---|---|---|---|---|
| `GEN10-J4` | DEEPEN: GEN6-J2 + GEN7-J3 + M-J4-1 only (A1 build named Goehring-class, §2.4 retiming) | GEN6-J2, GEN7-J3 | **P proposed** (G1 NA disclosed) | **Conditional single-candidate run only** — `adapted-gen10-J4-conditional.csv` via stock adapter `--track-map=track-map-gen10.csv`; `gate-matrix-gen10-J4-conditional.md` WITH `--manifest ../manifest-GEN10-J4.csv`. In **no** shared ranking/Pareto/fitness key (HP-J1-4 unsigned, as GEN5-J1/GEN6-J2) |

[attack-causal-extraction.md](../attack-causal-extraction.md)
files **no candidate rows** (external extraction; its Goehring
2017/2019 contrasts enter only as DESIGN ledger rows in
[ledger-delta.csv](../ledger-delta.csv), `EXT-*` keys, verified
`adapt()` = 0 rows in [score-gen10.md](./score-gen10.md) §1).
Gaultier 2024 / Kang 2021 / Deep ACE file no row anywhere in
Gen 10 scoring (bounded-lookahead / UNVERIFIED / UNVERIFIED —
attack §§3–5; Deep ACE Gen 8 ledger rows not duplicated).

**Stock adapter, no manual adaptation** (Gen 7 path carried):

```text
$ python3 research/scoring/adapt_extraction.py extract-gen10.csv adapted-gen10-J4-conditional.csv --track-map=track-map-gen10.csv
adapted 8 rows
$ python3 research/scoring/adapt_extraction.py extract-gen10.csv /tmp/g10stock.csv   # no map, control
adapted 0 rows        # A–H built-in map only, as Gen 2–7
```

Adapted J4 ≡ adapted GEN6-J2 modulo ID, and manifest ≡
GEN6-J2 manifest modulo candidate (both verified mechanically
this session, `EQUIVALENCE OK` / `MANIFEST OK`) — expected:
M-J4-1 names the build, it changes no gate cell, and no
weights/bench/listener data exist. `gate_table.py` /
`adapt_extraction.py` **not edited** this generation
(27 tests OK + ASTRA PASS, observed).

**Manifest.** Unlike P6/P7, J4's manifest is **candidate-filed**
([manifest-GEN10-J4.csv](../manifest-GEN10-J4.csv): G1 `false`,
G2/G3a/G3b/G4/G5/G6 `true`) and is consumed in place — no
scoring-step transcription. Ratification PENDING human;
§(f) reports all required cells present (manifest tax a
verified no-op). If HP-J1-4 denies G1=NA, J4 withdraws with
J1/J2/J3 together and is never re-scored as a device
(candidate §7, carried verbatim).
