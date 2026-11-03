# Gen 5 adaptation note — ID→track map, manifest treatment, J1 conditional run

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-03. Gen 5 under
> GOAL v2.3** (no generation cap, no loop stop rules; Gen 4
> clock/STOP machinery superseded by v2.3, not applied here).
> **G3b BLOCKED; same PASS bar as Gen 0–4; no PASS; FROZEN
> retained. Inspected records only; no invented data.**

## Documented Gen 5 candidate-ID → track / scorer-treatment table (binding for this score)

| Gen 5 ID | Kind (per candidate file) | Parent | Track | Scorer treatment |
|---|---|---|---|---|
| `GEN5-P5` | DEEPEN (a): P4 + M-P5-1 only (*OTOF*→*OTOF*+*GJB2* triage) | GEN4-P4 | **P** (G1 NA disclosed) | **`adapted-gen5.csv` + `gate-matrix-gen5.md` WITH `--manifest`** (`manifest-gen5-main.csv`) |
| `GEN5-I1` | NEW Family I (*GJB2* AAV product) | — | **R** | **Same main manifest run** (tracks ranked separately inside one run, as Gen 0) |
| `GEN5-I2` | DEEPEN (b): I1 + M-I2-1 only (staged dose/age-descent rules; dose blanks named) | GEN5-I1 | **R** | **Same main manifest run** |
| `GEN5-K1` | NEW Family K (base editing, long-horizon watch) | — | **R** | **Same main manifest run** |
| `GEN5-J1` | NEW Family J (AI front-end); "Track P **iff HP-J1-4 G1=NA signs**; if denied, not fielded" | — | *P conditional — unsigned* | **Separate conditional single-candidate `--manifest` run only** (`adapted-gen5-J1-conditional.csv` → `gate-matrix-gen5-J1-conditional.md`). Absent from every shared ranking/Pareto/fitness key until HP-J1-4 signs |

**Why J1 stays out of the shared matrix (candidate's own gate, not
scorer taste).** J1 §1 requires the HP-J1-4 G1=NA ruling *before
scoring* and states J1 is withdrawn — never re-scored as a device —
if denied. Its manifest `false` is therefore a *proposed* NA, unlike
P5's inherited ratified-form NA. Unlike QR/AD (Gen 3/4) there is **no
scope artefact**: J1 declares 6 applicable gates, and the forced
probe (`/tmp/combined_forced5.md`, 362 rows) places it at the same
0/6 as every joint-best pathway — observed, disclosed, and still
excluded, because an unfielded candidate has no fitness to report.

**G4-AAV treatment (the one place Gen 5 differs from Gen 1–4
filings).** Gen 0 precedent (C, D): an AAV candidate with no
capsid-switch/non-viral re-dose or post-exposure later-AAV efficacy
demonstration files `G4-AAV = FAIL` (presumptive; protocol S6,
App. A-v1 §7.1), which sets the G4 cell to FAIL via worst-verdict.
I1, I2, and K1 (dual-AAV delivery in inspected mouse work) each file
that row in `extract-gen5.csv` — a real FAIL cell, disclosed as a
Track R trade, exactly as their candidate files print ("G4-AAV
presumptive FAIL stands"). Filing it `INSUFFICIENT` instead would
flatter the new families against C/D and is refused. QR4 legs (a)
NAb/contralateral, (b) established-implant delivery, (c) same-ear
re-dose remain unretired; nothing in the Gen 5 sweep touches them
(NCT07627971: recruiting, no results).

**Manifests verified:** `manifest-GEN5-{I1,I2,J1,K1,P5}.csv` here
are byte-identical copies of the `research/gen05/` filings (7 rows
each). P5's declaration is **identical to GEN4-P4's modulo candidate
ID** (checked mechanically this session); I2's = I1's. Main run uses
concatenation `manifest-gen5-main.csv` (28 rows: I1, I2, K1, P5)
because `validate_manifest` requires manifest/extraction candidate
sets to match exactly. Class ratification still PENDING —
declared ≠ commensurable.

## Adapter limitation (observed again)

```text
$ python3 research/scoring/adapt_extraction.py research/gen05/scoring/extract-gen5.csv /tmp/g5stock.csv
adapted 0 rows        # all 40 GEN5-* rows skipped (A–H map only; GEN5 successor still owed)
```

## What was done instead (no code edited)

- `extract-gen5.csv`: frozen 14-col schema, **40 rows** (8 per
  candidate: 7 gates + G2-music for P5/J1, + G4-AAV for I1/I2/K1;
  INSUFFICIENT 35, FAIL 3 — the G4-AAV rows, NA-prereg 2 — P5/J1 G1;
  PASS 0; RECORD 40/40; UNASSESSED 40/40; every effect/numeric blank —
  abstracts carry no extractable bare-number effect vs any bar, and
  doses/Ns are absent, never invented). Built by
  `/tmp/build_gen5_extract.py` from the five candidate files'
  Appendix B gate plans as inspected. P5's rows are GEN4-P4's
  verdicts/tiers modulo ID with the M-P5-1 claim annotation (verified:
  adapted P5 ≡ adapted P4 modulo ID; adapted I2 ≡ adapted I1 modulo
  ID — I2's tighter rules are evaluability, not fitness, as its file
  prints).
- `gate_table.py` and `adapt_extraction.py` **not edited**. Observed:
  both manifest runs exit 0, §(f) reports **"(none) — all required
  cells present"** (manifest tax a verified no-op on verdicts);
  `promoted FALSE` ×5. Scorer tests: `python3 -m unittest discover`
  in `research/scoring` → **Ran 27 tests, OK** (+ ASTRA PROBES PASS).
- Scorer v2 semantics (`effective_verdict`, `is_mechanism_only`) are
  again no-ops: 0 PASS proposed, 0 G2 W0/W1 rows. No `--fmea`
  fabricated (candidate FMEA probability bands are mostly "Unstated";
  inventing bands to feed the Track R G5 aggregate is refused — it
  stays NA for I1/I2/K1 exactly as for C/D/E). `gate-matrix-gen5*.md`
  carry the scorer's fixed pre-Step-3 header verbatim (code
  provenance), as Gen 1–4.
