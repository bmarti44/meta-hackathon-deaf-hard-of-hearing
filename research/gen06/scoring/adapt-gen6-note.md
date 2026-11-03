# Gen 6 adaptation note — ID→track map, manifest treatment, J2 conditional run

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-03. Gen 6 under
> GOAL v2.3** (no generation cap, no loop stop rules; clock/STOP
> machinery superseded, not applied here).
> **G3b BLOCKED; same PASS bar as Gen 0–5; no PASS; FROZEN
> retained. Inspected records only; no invented data.**

## Documented Gen 6 candidate-ID → track / scorer-treatment table (binding for this score)

| Gen 6 ID | Kind (per candidate file) | Parent | Track | Scorer treatment |
|---|---|---|---|---|
| `GEN6-P6` | DEEPEN: P5 + M-P6-1 only (*GJB2* branch executable, R-P6-1…10) | GEN5-P5 | **P** (G1 NA disclosed) | **`adapted-gen6.csv` + `gate-matrix-gen6.md` WITH `--manifest`** (`manifest-gen6-main.csv`, 7 rows — sole fielded-form Gen 6 candidate) |
| `GEN6-J2` | DEEPEN: J1 + M-J2-1 only (named comparator C-J2 + staged pediatric protocol); "Track P **iff HP-J1-4 G1=NA signs**" | GEN5-J1 | *P conditional — unsigned* | **Separate conditional single-candidate `--manifest` run only** (`adapted-gen6-J2-conditional.csv` → `gate-matrix-gen6-J2-conditional.md`). Absent from every shared ranking/Pareto/fitness key until HP-J1-4 signs |

`resweep.md` and `attack-gjb2-doses.md` are not candidates and
file no rows; both state DESIGN-only, validation set 0, no cell
moves (verified against their admission tables this session).

**Why J2 stays out of the shared matrix (lineage's own gate).**
J2 §1/fielding fence inherits J1's HP-J1-4 fence in full: unfielded
pending the G1=NA ruling; if denied, J1 and J2 are withdrawn
together, never re-scored as a device. Naming the comparator and
staging the protocol (M-J2-1) did not sign the ruling. No scope
artefact: J2 declares 6 applicable gates; the forced probe
(`score-gen6.md` §1/§4) ties it at 0/6 — observed, disclosed, and
still excluded.

**⚑ Manifest provenance difference vs Gen 5 (flagged).**
`manifest-GEN6-J2.csv` was filed with the candidate in
`research/gen06/` and is copied here byte-identical (verified
identical to GEN5-J1's modulo ID). **P6 filed no manifest CSV**
(its design task specified none); `manifest-GEN6-P6.csv` here is
a **transcription by this scoring step** of the declaration
printed in `candidate-P6.md` §1 ("identical to P5/P4: G1 `false`,
G2–G6 `true`") — mechanically verified identical to
`manifest-GEN5-P5.csv` modulo ID. Declared ≠ ratified: class/
manifest ratification PENDING, and a human may still replace the
transcription; no verdict depends on it beyond the §(f) no-op
below.

**No G4-AAV row in Gen 6 (not a softening).** P6 administers zero
product; the referred-ear presumptive FAIL is owned by GEN5-I1/I2
(filed Gen 5, QR4 legs unretired) exactly as P5 handled it — P6
files G4 INSUFFICIENT on its I1* process leg and claims no AAV
preservation. J2 touches no biology (Gen 0 B/E logic). Nothing in
`attack-gjb2-doses.md` retires any leg: anti-capsid/biodistribution/
shedding/redose were searched-absent in both *GJB2* papers, so
C/D/I1/I2/K1 G4-AAV FAILs stand untouched.

## Adapter limitation (observed again)

```text
$ python3 research/scoring/adapt_extraction.py research/gen06/scoring/extract-gen6.csv /tmp/g6stock.csv
adapted 0 rows        # all 16 GEN6-* rows skipped (A–H map only; GEN-* successor still owed since Gen 2)
```

## What was done instead (no code edited)

- `extract-gen6.csv`: frozen 14-col schema, **16 rows** (8 per
  candidate: 7 gates + G2-music; INSUFFICIENT 14, NA-prereg 2 —
  P6/J2 G1; FAIL 0, PASS 0; RECORD 16/16; UNASSESSED 16/16; every
  numeric blank, no bare-number effect anywhere (one inherited
  qualitative G6 descriptor, "nothing measured") — no Stage/cohort
  data exist, SKY-GJB2 human
  dose/capsid/volume and J2 bench latency/power/locked-N are absent
  from inspected records, never invented). Built by
  `/tmp/build_gen6.py` from the Appendix B gate plans of
  `candidate-P6.md` (§4, R-P6-1…10) and `candidate-J2-ai-pediatric.md`
  (§3 G1–G6 plan) as inspected. **Verified mechanically in the
  build: adapted P6 ≡ adapted GEN5-P5 modulo ID; adapted J2 ≡
  adapted GEN5-J1 modulo ID; both manifests ≡ parents' modulo ID**
  (build asserts; run output `EQUIVALENCE OK`).
- `gate_table.py` and `adapt_extraction.py` **not edited**. Observed:
  both manifest runs exit 0, §(f) reports **"(none) — all required
  cells present"** (manifest tax a verified no-op on verdicts);
  `promoted FALSE` ×2. Scorer tests: `python3 -m unittest discover`
  in `research/scoring` → **Ran 27 tests, OK** (+ ASTRA PROBES PASS).
- Scorer v2 semantics (`effective_verdict`, `is_mechanism_only`) are
  again no-ops: 0 PASS proposed, 0 G2 W0/W1 rows. No `--fmea`
  fabricated (P6 probabilities are "Design risk", J2's mostly
  "Unstated/bench-measurable" — inventing App. C bands refused).
  `gate-matrix-gen6*.md` carry the scorer's fixed pre-Step-3 header
  verbatim (code provenance), as Gen 1–5.
