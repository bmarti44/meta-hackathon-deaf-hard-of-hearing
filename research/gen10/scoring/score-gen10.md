# Gen 10 score — J4 conditional (unfielded); Goehring ledger delta; combined audit

> **Model routing (GOAL §9).** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Scored **2026-11-03. Gen 10 under
> GOAL v2.3** (no generation cap, no loop stop rules).
> **Authority:** agent score = triage only. Human dual
> extraction, protocol/freeze/held-out, H-1…H-8, manifest/class
> ratification, every HOLDER-PIN: **PENDING**.
> **Headline: no PASS. `promoted FALSE`. G3b BLOCKED. FROZEN
> retained. J4 is UNFIELDED (HP-J1-4 unsigned) and scores only
> in a separate conditional run at 0 FAIL / 6 INSUFFICIENT —
> cell-for-cell its parent GEN6-J2, exactly as the design-only
> rule requires: no weights, no bench, no listener data exist.
> ⚑ Zero Gen 0–7 cells move (mechanically diffed, §3); the
> combined main matrix stays 370 rows. Goehring 2017/2019
> enter as 2 DESIGN ledger rows that mechanically cannot mint
> a `delta_g2_db` (§1). Naming a buildable causal A1 bought
> evaluability and two desk-kills of neighbouring designs
> (candidate §3.3) — it bought no fitness.**

## 1. Method — same bar, design-only rule, ledger separation

**PASS bar unchanged (Gen 0–7):** ≥Moderate *human-verified*
GRADE **and** Appendix A v1 minimum tier (G2/G3a/G3b T4),
enforced judge-side and by scorer `effective_verdict` — a
no-op here (0 PASS proposed). All 8 J4 rows RECORD/UNASSESSED;
INSUFFICIENT never passes, never safety (D10/D17); G3b BLOCKED
forces INSUFFICIENT + `promoted FALSE`. **Validation set 0.**

**Design-only rule (as Gen 1–7).** J4 is a spec
([candidate-J4-causal.md](../candidate-J4-causal.md)): no
weights trained, no §2.5 causality audit run on a real graph,
no J3 bench, no Stage 1/2 listener. Rejected as PASS
inflation, each barred by the candidate itself: counting the
§3 **T0 latency floor (8.0 ms arithmetic; 2.0 ms headroom to
B1)** as HP-J2-1 measured latency/power; counting Goehring
SRTs (+0.4 dB NS / +3.4 dB babble vs *unprocessed*, adults,
2019 at 20/10 ms framing J4 retimes to 8/4 — effects
expressly non-transferring, candidate §2.4) toward J4's ≥3 dB
bar vs C-J2/SCAN 2; counting causality-by-construction as a
passed B3 (the §2.5 suffix-replay Δ=0 bar and J3 shift test
decide, on a locked build that does not exist); filling any
filterbank-`B`/N/power blank from anything but HP-J4-1..3
human freezes (all PENDING). No `--fmea` fabricated (candidate
§8 probabilities are design tiers, not App. C bands).

**Ledger vs scoring (Gen 8 rule, carried).**
[ledger-delta.csv](../ledger-delta.csv) adds **2 DESIGN rows**
to the Gen 8 external ledger (its 7 rows untouched):
`EXT-GOEHRING2017` (N=14; MT +1.4/+5.4/+0.4 NS, ST
+2.3/+6.4/+2.0 dB vs unprocessed ACE; paper CIs NOT REPORTED)
and `EXT-GOEHRING2019` (N=10; babble +3.4 dB t(9)=7.2,
traffic +2.0 dB NS; CIs agent-derived from reported *t*,
labelled in-cell), from full-text extraction
([attack-causal-extraction.md](../attack-causal-extraction.md)
§§1–2, PMC5256482/PMC6773603). Guards verified by execution
this session: file not named `extract-*.csv`; `EXT-*` keys
absent from every track map (`adapt()` with the Gen 10 map =
**0 rows**); no bare-number `effect`, so no vs-frozen
`delta_g2_db` tie-break can be minted even on INSUFFICIENT
rows. Gaultier 2024 (bounded-lookahead), Kang 2021 and Deep
ACE (causality UNVERIFIED) file **no** new ledger row — Deep
ACE's Gen 8 rows already stand. Human dual extraction/GRADE
pending on both new rows; `grade=UNASSESSED` ⇒ neither can
PASS, and neither is on J4's critical path (design precedent
only, candidate §11).

**Who enters which matrix.** J4 gets a **conditional
single-candidate `--manifest` run** and appears in no shared
ranking/Pareto/fitness key — HP-J1-4 (G1=NA) unsigned, fence
inherited in full (deny ⇒ J1/J2/J3/J4 withdrawn together).
Manifest is candidate-filed
([manifest-GEN10-J4.csv](../manifest-GEN10-J4.csv), consumed
in place; §(f) "all required cells present" — manifest tax a
verified no-op). Full adapter detail:
[adapt-gen10-note.md](./adapt-gen10-note.md).

**Files & commands (observed, this session):**

```text
extract-gen10.csv  8 rows 14-col: INS 7, NA-prereg 1, FAIL 0, PASS 0 (built /tmp/build_gen10.py from candidate-J4 App B)
ledger-delta.csv   2 rows 14-col DESIGN (same build script; Gen8 ledger untouched)
$ python3 adapt_extraction.py extract-gen10.csv adapted-gen10-J4-conditional.csv --track-map=track-map-gen10.csv -> adapted 8 rows
$ python3 adapt_extraction.py extract-gen10.csv /tmp/g10stock.csv -> adapted 0 rows (no-map control)
$ python3 adapt_extraction.py ../ledger-delta.csv /tmp/g10ledger_adapted.csv --track-map=track-map-gen10.csv -> adapted 0 rows (ledger guard)
$ python3 gate_table.py adapted-gen10-J4-conditional.csv --manifest ../manifest-GEN10-J4.csv --out gate-matrix-gen10-J4-conditional.md (exit 0; §f all required cells present; promoted FALSE)
adapted J4 == adapted GEN6-J2 modulo ID (EQUIVALENCE OK); manifests == modulo candidate (MANIFEST OK)
$ python3 -m unittest discover (research/scoring) -> Ran 27 tests OK + ASTRA PROBES PASS; scorer code unedited
combined main: Gen0-7 adapted 233+41+16+16+16+32+8+8 = 370 rows -> /tmp/combined370.md (scratch)
forced probe (withheld): 370 + J4 8 = 378 -> /tmp/combined378forced.md (scratch; cell diff MOVED=[], §3)
```

## 2. Gate matrix (deterministic, `--manifest`, conditional)

| candidate | condition | G1 | G2 | G3a | G3b | G4 | G5 | G6 | FAILs | INS |
|---|---|---|---|---|---|---|---|---|---|---|
| GEN10-J4 | HP-J1-4 G1=NA **unsigned** (inherited) | NA‡ | INS | INS | INS | INS | INS | INS | 0 | 6 |

‡Manifest `required=false` with proposed-NA reason = declared
non-claim pending ruling, never "fine." All numerics NA
(`delta_g2_db`/`delta_g3a_sd`/`g1_channels`/`burden_rank`),
as Gen 0–7. No winner. If HP-J1-4 signs, the J-lineage enters
Track P at this same 0/6 (J4 supersedes J2 as design of
record only if humans adopt it); if denied, withdrawn — never
re-scored as a device.

## 3. Cell-movement audit

**⚑ Gen 0–7 cells: zero movement — verified mechanically.**
The 370-row Gen 0–7 main run and the 378-row forced probe
were both executed this session; gate matrices diffed
candidate-by-candidate: 25 base candidates reproduced
identically, `MOVED = []`, sole addition GEN10-J4. No earlier
extraction row edited; Gen 8/9 filed no scored rows, so the
main combined matrix is unchanged at **370 rows, zero PASS**
(Gen9-summary §3 carried). In particular: the two new
ledger rows move no cell (ledger ≠ scoring, §1); Schulz stays
A2-offline-only; G4-AAV presumptive FAILs (C/D/I1/I2/K1),
Q0 UNDECIDABLE-no-data, H harm not cleared — all untouched.

**J4 vs GEN6-J2 — every cell "=" (verified mechanically:**
adapted rows + manifest identical modulo ID). Paper gain,
verdict-flat: M-J4-1 converts J2's abstract A1 ("a causal DNN
build") into one auditable spec whose T0 arithmetic already
desk-kills its two neighbours (2019-as-published 20/10
framing: 20.0 ms floor = B2 before compute; waveform-WOLA
variant: 12.0 ms > B1) and pre-files kills K-J4-0..4. Depth
bought a bench-decidable question, not fitness.

**Frontier entry (movement of the tie, not of any cell):**

- ⚑ **J4 would be the 17th Track-P entry at joint-best
  0 FAIL / 6 INSUFFICIENT if fielded** (forced 378-row probe:
  17 rows at 0/6 vs 16 in the 370-row main run, numerics NA).
  Its forced print position (7th) is the **name tie-break**
  (`GEN10-…` sorts early) — spelling, not merit — and is
  **withheld**: HP-J1-4 unsigned ⇒ no fitness quoted for any
  J candidate (Gen 6 rule, carried).
- ⚑ **No FAIL/PASS cells filed in Gen 10** — a composition
  fact (one design candidate, zero data), explicitly not
  improvement. Fewer examined cells ≠ better (evidence-
  completeness inverse, as Gen 5/6).

## 4. Kill status (none triggered, none cleared — D10)

| candidate | state |
|---|---|
| GEN10-J4 | K-J4-0 desk audit (index/norm/suffix-replay Δ=0), K1 bench B1–B10 measured, K-J4-2 adult <3 dB vs SCAN 2 / precision, K-J4-3 pediatric Band-A <3 dB / precision, K-J4-4 NI bundle (quiet/music/localisation/alarm/wear-time) — **all unevaluated** (no build exists for any of them to bite on); fielding gate HP-J1-4 pending before any can be spent |
| Ledger rows | No kill attaches; `EXT-GOEHRING2017/2019` are DESIGN precedent — their babble/traffic nulls are candidate §4/§8 design inputs (held-out-noise screen, honest prior), not J4 results |

## 5. Unresolved — owed-work register (Gen 10 increment)

Ranked blockers and the "closest-to-movable" verdict are
synthesised in [Gen10-summary.md](../Gen10-summary.md) §3 — the
score file asserts only what the scorer observed. Owed here:
HP-J1-4 ruling; manifest/class ratification (candidate-filed
manifest unratified); HP-J4-1..3 freezes; training + K-J4-0
audit on a real locked graph; HP-J3-1/2 (B4/B6/B7/B9 blanks)
→ Stage 0 measured HP-J2-1; HP-J2-2/4/5/6; human dual
extraction/GRADE of both ledger rows (2017 CIs figure-only —
digitisation/author data; would grade the *ledger*, never J4);
G3b co-design (universal promotion bar); Gen 10
protocol/freeze/held-out. **Validation set = 0.**

**D1–D17 carry verbatim.** No ranking is a winner; conditional
0/6 never quoted as fitness; external benefit ≠ project PASS;
T0 arithmetic never quoted as measurement; kills never
survived/cleared. **FROZEN retained. G3b BLOCKED. No PASS, no
winner — and under v2.3, no stop.**

*Files (this directory): `extract-gen10.csv`,
`adapted-gen10-J4-conditional.csv`, `adapt-gen10-note.md`,
`track-map-gen10.csv`, `gate-matrix-gen10-J4-conditional.md`;
parent dir: `candidate-J4-causal.md`,
`manifest-GEN10-J4.csv`, `attack-causal-extraction.md`,
`ledger-delta.csv`. Build script `/tmp/build_gen10.py`;
scratch `/tmp/combined370.{csv,md}`,
`/tmp/combined378forced.{csv,md}`, `/tmp/g10stock.csv`,
`/tmp/g10ledger_adapted.csv`. Inputs: `gen09/{Gen9-summary,
causal-dnn-search}.md`; `gen06/scoring/{extract-gen6,
adapted-gen6-J2-conditional,manifest-GEN6-J2,score-gen6}`;
`gen07/scoring/score-gen7.md`; `gen08/{external-evidence-
ledger.csv,ledger-note.md}`; adapted inputs Gen 0–7 as in §1.
Prior workflow results 1–2 (causal extraction; J4 candidate +
manifest) used as evidence and re-inspected at source this
session.*
