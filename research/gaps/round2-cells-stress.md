# Gap attack round 2 — completeness debts D14 (unrowed cells) + D16 (C–H stress) + extraction_v2 proposals

> **Requested route:** Sol 6.1. **Actual runtime model:**
> `muse-wonder-full-1.0`, disclosed per GOAL §9 rule 3.
> **Date:** 2026-11-02. **Scope:** GOAL §7 rule 4 round 2 on
> Step 5 §6 item 7 sub-gaps D14/D16 (`step3-skeptic.md` §8–9),
> which sat at 0/2 attacks after round 1
> (`round1-summary.md` §2, gap 7). **Inputs inspected:**
> `round1-summary.md`, `gap-skeptic.md`, my round-1 file
> `attack-fulltext.md` (§3 extractions, §4 bookkeeping),
> `searched-family-log.md` (§§1–3, 6–7),
> `extraction_v1_2026-11-02.csv` (199 data rows, 14 cols),
> `extraction-schema.md`, `extraction_template.csv`,
> `cost_dictionary_v1.md` (§§4, 6), `step3-skeptic.md`.
> **Evidence rule:** inspected records only; no number below
> is new — every rate is transcribed from the cost dictionary
> / family log with its PROVISIONAL/UNPINNABLE label.
> **Status:** agent work only; human dual extraction still
> PENDING. This file edits no earlier file, decides no gate,
> and makes no PASS, promotion, or "stress survived" claim.

## 0. Headline

- **D14:** the true unrowed count against `extraction_v1`
  is **48 Level-1 cells**, not "~42" (reconciliation in
  §1.2). All 48 are now filed as explicit INSUFFICIENT rows
  in `round2-unrowed-cells.csv` (14-col frozen schema).
  Joining that file to v1 leaves **0** Level-1 cells
  unrowed. No gate verdict changes: every one of the 48 was
  already functionally INSUFFICIENT; it is now *scored*
  INSUFFICIENT instead of absent.
- **D16:** the §6 stress template was actually filled per
  candidate for C–H (§2; 36 candidate-reads). Result:
  **0 verdict flips determinable, 0 FAIL-direction moves
  determinable; every flip question is UNPINNABLE** because
  the NI margin (U13/U17), the candidate's own rate, or both
  do not exist. "Unchanged" below always means "already
  INSUFFICIENT or completeness-FAIL at base, so the proxy
  has nothing to move" — it never means a stress was passed.
- **extraction_v2:** round-1 full texts change `effect`/`n`
  on exactly **6 existing v1 rows** (3 sources). Two
  upgraded sources (Pfingst 2015, Keppeler 2020) have *no*
  v1 row and are therefore excluded from the update list
  (§3.2) — filing them would be new rows, not updates.

## 1. D14 — the unrowed Level-1 cells, enumerated

### 1.1 Method

Expected set = the 162 Level-1 cells transcribed from
`searched-family-log.md` §§2.1–2.6 (A–D 23 each = 92; E 22;
F 14; G 12; H 16; FROZEN G3b 3; Q0-L/P/A 3). Actual set =
distinct `candidate × gate × window` in
`extraction_v1_2026-11-02.csv` (`#` headers skipped, CSV
parsed, not grepped). A cell counts as rowed only at its
exact pre-registered window: per family-log §1, windows are
distinct cells, so a W3 row does not satisfy a W1 cell and a
W0 row does not satisfy an ALL cell. One refinement over a
naive triple count: candidate H splits G3a by modality *at
Level 1* (§2.5), so H G3a cells are checked against the
`modality=` stratum, not merely the triple. Script:
`/tmp/enumerate_unrowed.py` (scratch, re-runnable);
independent re-check after CSV generation in §4.

### 1.2 Reconciliation: why 48, not ~42

The skeptic's "~42" was `162 − 120 distinct triples` on the
pre-synthesis extracts (167 rows). Against v1 the honest
bridge is:

| Step | Count |
|---|---|
| Level-1 cells pre-registered (family log §2.7) | 162 |
| …as distinct (candidate, gate, window) triples (H's 7 G3a cells collapse to 3 triples) | 158 |
| Distinct triples present in `extraction_v1` (199 data rows) | 123 |
| …of which at non-Level-1 addresses (§1.4) | 11 |
| Level-1 triples actually covered (123 − 11) | 112 |
| Missing triples (158 − 112) | 46 |
| + H G3a cells hidden inside a present triple but with no row at the pre-registered modality (W2 spoken; W3 bimodal) | 2 |
| **Unrowed Level-1 cells** | **48** |

So D14's "~42" understated the debt by 6, because the
subtraction credited 11 rows sitting at addresses the
Level-1 family never pre-registered. Distribution of the
48: **C 12, D 12, E 11, H 4, A 3, B 3, F 2, G 1** (FROZEN
and Q0 complete). By gate: G2 13, G3a 9, G1-spectral 6,
G1-temporal 6, G2-music 5, G5 5, G4 4. The pattern is
exactly what the file histories predict: A/B were extracted
window-by-window; C/D/E were filed W3/ALL-only, so every
W0–W2 and ADOL cell of theirs is missing.

### 1.3 The 48 cells (all filed in `round2-unrowed-cells.csv`)

| Candidate (§) | Unrowed cells |
|---|---|
| A (§2.1) | G2 W0 · G2-music W2 · G4 ADOL |
| B (§2.1) | G2 W0 · G2-music W2 · G4 ADOL |
| C (§2.1) | G1-spectral W1, W2 · G1-temporal W1, W2 · G2 W0, W1, W2 · G2-music W2 · G3a W1, W2 · G4 ADOL · G5 ADOL |
| D (§2.1) | G1-spectral W1, W2 · G1-temporal W1, W2 · G2 W0, W1, W2 · G2-music W2 · G3a W1, W2 · G4 ADOL · G5 ADOL |
| E (§2.2) | G1-spectral W1, W2 · G1-temporal W1, W2 · G2 W0, W1, W2 · G2-music W2 · G3a W1, W2 · G5 ADOL |
| F (§2.3) | G2 W0 · G5 ALL |
| G (§2.4) | G3a W1 |
| H (§2.5) | G2 W2 · G3a W2 spoken · G3a W3 bimodal · G5 ALL |

Judgment calls, stated so a human can reverse them:

1. **E G1-temporal windows.** Family-log §2.2 expands E to
   W1–W3 by the A–D convention but flags the alternative
   (one ALL cell → E = 20, family = 160) as open item 1.
   This attack keeps the log's headline 22-cell reading.
   On the alternative, unrowed = 47 (drop E W1/W2, add E
   G1-temporal ALL, which also has no row). Either way E's
   temporal cells are INSUFFICIENT; only the count moves.
2. **G2-music W2 filed as INSUFFICIENT, not NA-prereg.**
   The plans transcribe W2 as "presumptive NA (no validated
   toddler battery)" (§2.1). Family-log §2.7 requires the
   missing cells to appear as explicit INSUFFICIENT rows,
   and NA-prereg is a pre-declared structural state (only
   F/G/H G1 carry it in v1). The 5 W2 music rows therefore
   print INSUFFICIENT with the presumptive-NA reason in the
   claim; reclassifying them to NA-prereg is a one-line
   human re-freeze decision, not an agent call.
3. **G4-AAV is not a Level-1 cell.** It is a Level-2 read
   inside the G4 ALL cell (§3.2: "7 reads [8 with G4-AAV]
   inside 1 Level-1 ALL cell"). v1's four G4-AAV rows
   (B/C/D/E) therefore neither satisfy nor add Level-1
   cells; A–D G4 ADOL remains unrowed despite them.
4. **H G3a W3 pooled row satisfies no modality cell.**
   v1's Fitzpatrick row is `modality=pooled-as-reported`;
   per family-log §3 a pooled value "cannot silently
   support a per-stratum verdict", so W3 bimodal stays
   unrowed even though the (H, G3a, W3) triple is present.
   Likewise W2 has signed ×2 + bimodal rows but no spoken.
5. **F/H G5 ALL vs their W0 rows.** F and H pre-register G5
   at ALL (§§2.3/2.5); v1 filed their delay/false-reassurance
   rows at W0. W0 ⊂ ALL in time but is a different cell
   address; the ALL (birth–7 y) read is unrowed. The new
   placeholder cross-references the W0 rows in its claim
   via the sibling-window note rather than duplicating them.

### 1.4 The 11 v1 triples at non-Level-1 addresses (not errors — but they cover nothing)

`B/C/D/E G4-AAV ALL` (Level-2 reads, call 3 above);
`D G1-spectral NA` (advance-criterion check row — decision
record, not a window cell); `F G2-music W3` (F's Level-1
plan has no G2-music row at all — §2.3 lists none; the v1
row is a defensible cap-reminder but enlarges the family
without the dated amendment family-log §1 requires);
`F G5 W0`, `F G6 W0`, `G G5 W0`, `G G6 W0`, `H G5 W0`
(pathway rows filed at the decision window instead of, or
as well as, ALL). None is deleted or moved by this attack;
they are listed so the §1.2 arithmetic is auditable and so
the human pass can either amend the family log to adopt
them or leave them as extra reads. What they may not do is
continue to be silently netted against the 162.

### 1.5 What the CSV does and does not do

`round2-unrowed-cells.csv`: 5 `#` provenance lines + frozen
14-column header + 48 rows, one per cell above, each
`source_id=UNVERIFIABLE`, `tier=RECORD`,
`grade=UNASSESSED`, empty `effect`/`n`,
`verdict_proposed=INSUFFICIENT`, extractor
`agent:muse-wonder-full-1.0/high`, date 2026-11-02 —
the same shape as v1's own gap rows. Each claim names the
family-log section, the sibling windows that do exist in
v1, and the gate-specific reason the cell cannot be read
from them (U10/U11/U13/U17 as applicable). The file is an
*append candidate* for a future human-frozen
extraction_v2; it does not modify v1, and joining it
changes no gate-matrix cell (round-1 §3 totals stand:
Gen 0 still 0 PASS / 7 FAIL / 46 INSUFFICIENT at gate
level — the 48 rows make previously invisible
INSUFFICIENTs explicit at window level, which is the whole
point of D14). Level-2 completeness (≈527 reads, §3.9) is
**not** claimed and remains mostly unrowed.

## 2. D16 — C–H stress re-scoring, actually run through the §6 template

### 2.1 Method and proxy inputs (transcribed, labels intact)

Template: `searched-family-log.md` §6.3 (one row per
re-scored read; one harm moved at a time; joint worst-case
not run, per §6.2 it is an extra sensitivity only).
Run-level fields are hoisted here instead of repeated per
row: `run_date` 2026-11-02, `extractor`
agent:muse-wonder-full-1.0, and the mandatory note
*proxy ≠ 90th percentile* applies to every row. Exposure
map (which scenario touches which read for which candidate)
is transcribed from §6.2, not re-invented. Inputs
(`cost_dictionary_v1.md` §6 = family-log §6.1):

| Scenario | Base → stress proxy | Pin |
|---|---|---|
| S-revision | H1 post-2000 reimplantation 3.2% → **3.7%** (upper 95% CI); sensitivities alongside only: pre-2000 upper 9.2%, H2 revision upper 8.5% (different definition — never averaged) | PMID 35973054; PMID 37254261 (PROVISIONAL, mixed adult+child) |
| S-nonuse | H3 <8 h/day complement 6.8% (5 y) / 12.3% (10 y) → **10.0% / 17.1%** (upper-bound complements). Complete 0 h/day non-use: base+stress **UNPINNABLE** | PMID 24518403 (PROVISIONAL, <8 h/day only) |
| S-access | H4 LTF/D latest era: diagnosis 31.3%, EI 20.3% → era-max **42.1% / 39.4%**; includes loss-to-*documentation*; P0-specific LTF UNPINNABLE | PMID 31745502 (PROVISIONAL proxy) |
| S-surgical (meningitis) | H5 overall 0.07% → **0.10%**; H6 malformation 0.12%/ear → **0.380%/ear** (per-child conversion owed) | PMID 36864717; PMID 37317518 (PROVISIONAL) |
| S-surgical (major composite; facial/CSF/anaesthesia <12 mo/vestibular/death) | H7 major 5.0% point, stress **UNPINNABLE**; all other harms base+stress **UNPINNABLE** | PMID 24889283 (PROVISIONAL point) |

The A/B precedent this extends: v1 carries three A stress
rows (S-revision, S-nonuse, S-surgical+S-access; each
"VERDICT CHANGE: none … INSUFFICIENT-proxy-reported") and
one combined B sentence to the same effect. The tables
below give C–H the same treatment, read by read.

### 2.2 Filled template — candidates C, D, E (device/biologic)

Base verdicts are the v1 rows cited; "candidate rate" is
NOT-MEASURED everywhere (no C, D, or E human or chronic
rate exists in inspected records).

| Scenario | Candidate × gate read (base verdict in v1) | Margin / boundary | Outcome |
|---|---|---|---|
| S-revision | C × G5 revision-hazard (INSUFFICIENT, C G5 ALL) | NI margin U13 — does not exist; no human oCI device exists to revise | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-revision | C × G6 surgeries/child (FAIL — pre-specified staging) | FAIL is structural (no adult FIH), stress-independent | Unchanged FAIL; stress adds nothing and cannot flip it up or down |
| S-nonuse | C × G2/G3a treatment-policy (INSUFFICIENT) | No human C data at any wear-time; 0 h/day read UNPINNABLE | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-nonuse | C × G6 burden (FAIL staging) | Frozen non-use U16; datalogged hrs/day owed | Unchanged; flip **UNPINNABLE** |
| S-access | C × G6 coverage (FAIL staging; coverage element INSUFFICIENT) | Coverage % INSUFFICIENT while D1–D4 blank; disparity caps unratified | Cannot flip a PASS (none attainable); flip **UNPINNABLE** |
| S-surgical | C × G5 meningitis (INSUFFICIENT) | Proxy is frozen-*class*, not oCI; margin U13 | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-surgical | C × G5 phototoxic/thermal/opsin-immunogenicity (INSUFFICIENT; candidate-central) | No base rate inspected at all — base+stress UNPINNABLE; thermal-dose extraction still owed | INSUFFICIENT (no proxy exists to report); flip **UNPINNABLE** |
| S-surgical | C × G4 disclosure (INSUFFICIENT; G4-AAV FAIL presumptive) | Surgical proxies do not enter histology/AAV reads (§6.2); margins U17 | No flip path; presumptive FAIL stands on its own pre-registered rule, not on stress |
| S-revision | D × G5, device components only (INSUFFICIENT, D G5 ALL) | D as specified has no implanted device of its own; downstream CI device cross-ref only; margin U13 | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-nonuse | D × G2/G3a treatment-policy (INSUFFICIENT) | Watch-only; no human D data; wear-time belongs to the downstream CI the child still receives | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-access | D × G6 coverage (INSUFFICIENT) | D1–D4 blank (U01/U06); no timeline until advance criterion met | Cannot flip a PASS; flip **UNPINNABLE** |
| S-surgical | D × G5 meningitis/composite (INSUFFICIENT) | Frozen-class proxy; margin U13; H7 stress itself UNPINNABLE | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-surgical | D × G5 off-fate/tumour (INSUFFICIENT; candidate-central) | No inspected rate; surveillance owed | INSUFFICIENT (no proxy); flip **UNPINNABLE** |
| S-revision | E × G5 revision/migration (FAIL — presumptive staging, §8E) | E's pre-registered denominators are future-T2 exact-CI endpoints with no N asserted (§2.2); FAIL is structural | Unchanged FAIL; a rate stress cannot be run on a cohort that does not exist; flip **UNPINNABLE** |
| S-nonuse | E × G2/G3a treatment-policy (INSUFFICIENT) | No human ANI data; parked before any wear-time exists | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-access | E × G6 (FAIL — presumptive, ~15 y rule) | Structural; coverage U01/U06 | Unchanged; flip **UNPINNABLE** |
| S-surgical | E × G5 meningitis/composite; nerve injury/migration (FAIL staging; per-harm reads INSUFFICIENT) | 2 CPA surgeries bilateral is structural; nerve-injury/migration rates UNPINNABLE; bench charge-density primary UNVERIFIABLE (D2b) | Per-harm: INSUFFICIENT-proxy-reported (meningitis) / INSUFFICIENT no-proxy (nerve, migration); flip **UNPINNABLE** |

### 2.3 Filled template — pathway candidates F, G, H

F/G/H implant nothing themselves; §6.2 routes their
S-revision/S-surgical exposure through the downstream CI
cross-reference and their own FMEAs transcribe "no causal
path" for the surgical rows. Those transcriptions are
auditable candidate claims, repeated here as such, not
endorsed findings.

| Scenario | Candidate × gate read (base verdict in v1) | Margin / boundary | Outcome |
|---|---|---|---|
| S-revision | F/G/H × G5 (each INSUFFICIENT; F & H at W0, ALL filed §1) | Downstream CI only; margin U13; candidate adds no revision hazard of its own as specified | INSUFFICIENT-proxy-reported (cross-ref); flip **UNPINNABLE** |
| S-nonuse | F × G2/G3a — HA wear-time *is* the F1 dose (INSUFFICIENT) | H3 proxies are CI-derived; transport to infant HA wear unvalidated in inspected records; the decisive 0 h/day read is UNPINNABLE → cell is INSUFFICIENT-proxy-reported *by construction* (§6.2) | Flip **UNPINNABLE**; direction pre-registered (more non-use dilutes the F1 chain toward null) but unmeasurable at v1 |
| S-nonuse | F × G6 burden; G/H × G2/G3a via downstream CI wear (INSUFFICIENT) | Frozen wear/non-use U09/U16 unmeasured; second-ear non-use must stay unpooled | INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-access | F × G6 time-to-CI-decision (INSUFFICIENT) — primary F read | Frozen HA-trial dose/turnaround U09: a win vs an unmeasured baseline is already ruled INSUFFICIENT; era-max LTF/D (all-HL, incl. documentation loss) widens, never narrows, that gap | Cannot flip a PASS; P0-specific flip **UNPINNABLE** |
| S-access | G × G6 time-to-first-access/turnaround (INSUFFICIENT) — primary G read | Same U09 bar; decision-time denominators (5 origins × ≥3 genotype states) unmeasured | Cannot flip a PASS; flip **UNPINNABLE** |
| S-access | H × G6 EI dose / Deaf-mentor availability (INSUFFICIENT) — primary H read | Frozen EI contents U09 unmeasured; mentor-supply disparity unmeasured | Cannot flip a PASS; flip **UNPINNABLE** |
| S-access | F/G/H × G3a via delayed entry (INSUFFICIENT) | Entry-time strata pre-registered; stress changes stratum *mix*; NI-every-stratum rule is the safeguard, not the proxy | Flip **UNPINNABLE** |
| S-surgical | F/H × G5 anaesthesia/meningitis/facial/CSF (INSUFFICIENT) | No surgery in candidate — "no causal path" per own FMEA (transcribed); downstream CI cross-ref inherits the frozen-class proxy and U13 | Cross-ref only: INSUFFICIENT-proxy-reported; flip **UNPINNABLE** |
| S-surgical | G × G5 mis-triage/VUS/incidental (INSUFFICIENT; candidate-central) | No inspected mis-triage audit rate; U13 | INSUFFICIENT (no proxy); flip **UNPINNABLE** |
| S-surgical | F/G/H × G5 delay-to-standard-CI (INSUFFICIENT; shared candidate-central harm) | Delay-event rates UNPINNABLE (U13); rescue rules are design mitigations, not observed counts | INSUFFICIENT (no proxy); flip **UNPINNABLE** |

Reads with **no flip path for any candidate** (transcribed
§6.2, confirmed unchanged by this run): G1-spectral/
temporal (flip only on head-to-head ripple/spread +
replication — so C's PROVISIONAL-SIGNAL cannot be stressed
into or out of existence), G2-music (capped provisional
regardless), G3b (BLOCKED regardless — stress never
unblocks co-design), Q0-P/Q0-A (flip only on §2.3-grade
patency/AAV studies, not cost proxies). Revision/non-use
events enter G2/G3a primaries only through
treatment-policy denominators; dropping them in a
per-protocol re-read is a §4 sensitivity, never run here
as a primary.

### 2.4 D16 verdict

Rows run: 17 (C/D/E) + 10 table rows for F/G/H covering
19 candidate-reads once grouped F/G/H rows are ungrouped
— **36 candidate-reads total**. Outcomes:
**0 flips, 0 FAIL-direction determinations, 36/36 flip
questions UNPINNABLE**, each for a named reason in the
margin column (margin U13/U17 missing, candidate rate
NOT-MEASURED, frozen baseline U09/U16 missing, coverage
denominators D1–D4 blank, or no causal path/structural
verdict that stress cannot reach). This is the same shape
as the A/B result and the same shape §6.2 predicted — the
difference from round 1 is that the template is now filled
candidate by candidate instead of asserted in one
sentence, which is what D16 ("a reason, not a run")
demanded. It buys no robustness claim: with true 90th
percentiles UNPINNABLE (V09), no ratified margins, and no
candidate rates, there is nothing here that could have
failed. C–H may now be quoted as *"stress template run
2026-11-02; every cell INSUFFICIENT-proxy-reported,
verdict-flip UNPINNABLE"* — and still never as stress
survived, stress passed, or robust.

> *Mandatory footer (family-log §6.3): "True
> 90th-percentile stresses UNPINNABLE (V09/U13); proxy cells
> read INSUFFICIENT-proxy-reported, never 'stress
> survived'. No promotion depends on this table at v1 (G3b
> BLOCKED)."*

## 3. extraction_v2 row updates — proposed, listed only (v1 untouched)

Inclusion rule applied strictly: a row appears below only
if a round-1 full text (`attack-fulltext.md` §3, skeptic-
upheld S2) changes that *existing v1 row's* `effect` or
`n` field. Claim-wording improvements, qualifier
retirements, and sources with no v1 row are excluded and
accounted for in §3.2. Nothing here is applied to v1; per
schema §1 each change would land as a new row version in a
dated `extraction_v2` file at human re-freeze, with
`source_id` locator updated from `@ Abstract` to the PMC
section and `extractor` gaining the human verifier.

### 3.1 The 6 rows (3 sources)

| # | v1 row | Field | v1 value → proposed v2 value (locator) |
|---|---|---|---|
| U1 | A × G2 × W3, Srinivasan PMID 23467170 | `n` | `n=NOT-IN-ABSTRACT` → **n=6 adult CI subjects (HINT SRT n=5; digits n=6)** (PMC3639477 §2.1/Table 1, §3; fulltext §3.1) |
| U1 | same row | `effect` | "+2.7 dB digits; +3 dB sentences" → **mean SRT improvement 3.01 dB HINT (Exp-MP 15.3 vs Exp-TP 12.29 dB, n=5) and 2.71 dB digits (3.79 vs 1.08 dB, n=6), partial tripolar vs experimental monopolar; clinical-map HINT 10.6 dB, n.s. vs Exp-TP** (PMC3639477 §3). Derived-vs-printed: all printed |
| U2 | A × G4 × ALL, Kamakura PMID 27371868 | `effect` | "fibrous tissue + new bone 17/17; new-bone % volume negatively correlated with CNC" → append Table 2 distribution: **scala tympani fibrous 36.15% (range 9.93–61.54), new bone 20.13% (2.69–45.90), total new tissue 56.29% (14.48–95.14); whole-cochlea total 36.08%** (PMC5018452 Table 2; fulltext §3.2). Ranges are *computed from* the 17 per-case rows — keep that label (skeptic S2). `n=17 bones` unchanged |
| U3 | Q0-P × G4 × ALL, Kamakura PMID 27371868 | `effect` | Same appendix as U2 (current text: presence + correlation, "no patency %"). The "(no patency %)" guard must survive the edit verbatim: tissue-% of scala volume is not a cannulability numerator (fulltext §3.2; skeptic §5) |
| U3b | B × G4 × ALL (combined Seyyedi + Kamakura row) | `effect` | "frozen-context only: granulomatous 27/28; fibrous+new bone 17/17 (adult archival)" → the Kamakura half may take the same Table 2 appendix as U2; the Seyyedi half is untouched. `n=28 bones; 17 bones` unchanged. Listed separately so the combined row is not silently half-updated |
| U4 | C × G1-spectral × W3, Dieter PMID 32596983 | `n` | `n=NOT-IN-ABSTRACT animals` → **n=39 gerbils total (35 AAV-PHP.B-CatCh injected; 15/35 oABR-positive; 12 ICC datasets; 4 non-injected controls)** — denominators staged, never summed (PMC7411546 Animals/Results; fulltext §3.7) |
| U4 | same row | `effect` | "qualitative: spectrally selective tonotopic activation…" → append measured spread (blocks of 4 μLEDs only): **0.95/1.93/2.94/3.06 octaves at d′ 1.5/2/2.5/3 (100–150 µm pitch)**; single-μLED spread unmeasured. Discussion's electrical octaves are quoted from Dieter 2019 — do **not** enter them as this row's effect (fulltext §3.7) |
| U5 | C × G4-AAV × ALL, Dieter PMID 32596983 | `n` | `n=NOT-IN-ABSTRACT` → same staged denominators as U4 (the AAV exposure N is the 35 injected). `effect` unchanged; presumptive-FAIL verdict untouched (rule-based, not N-based) |

Borderline, proposed but flagged separable: **C × G4 ×
ALL** (same Dieter source) currently has empty
`effect`/`n`. Filling them (n as U4; effect: basilar-
membrane piercing in both X-ray-imaged implants, 2/2
imaged — fulltext §3.7) is technically an effect/N change
from empty, so it is listed here as **U6-optional**; a
holder who reads "update" as "revise a non-empty field"
should strike it and treat it as a new-row decision
instead. Either way it is Track-R disclosure content and
changes no verdict.

Effect on verdicts if all of U1–U5/U3b (+U6) are adopted:
**none.** U1's row stays barred as PASS evidence
(degraded comparator, acute, n=5–6 adults — skeptic §5);
U2/U3 add a distribution, not a patency estimand (Q0 stays
UNDECIDABLE-no-data); U4/U5 strengthen the paperwork of a
T2 single-programme acute rodent signal without touching
its GRADE ceiling. No tier, grade, or comparator field
changes on any of the 6.

### 3.2 Deliberately excluded (and why)

- **Pfingst 2015 (PMID 26209185, PMC4674315)** — upgraded
  in round 1 (B5 lifted; 3/3/3 arms; pre-implant AAV), but
  `extraction_v1` contains **no row for this source**
  (grep count 0, §4). v1's Pfingst-row is a *different
  paper* (Q0-A × G4, PMID 28776202, JARO 2017, n=18+5);
  writing 2015 numbers into it would be a conflation
  error of exactly the kind Step 0 exists to prevent.
  Filing the 2015 paper is a new-row decision for the
  human pass, not a v2 update.
- **Keppeler 2020 (PMID 32718992, PMC7611895)** — upgraded
  from title-only (within-animal 4.1 vs 6.9/6.9 octaves;
  n=2/arm behaviour), but likewise **no v1 row exists**
  (grep count 0). New-row candidate; excluded by the
  ONLY-updates rule. Its Fig. 5 Ns are figure-only and its
  Fig. 4 N is internally discrepant (4 vs 5) — any future
  row must carry both caveats (fulltext §3.8).
- **Downie 2020 (PMID 31827275), G × G6 × W0 row** — full
  text still blocked; `effect` (56% vs 21%) and `n`
  (59/106; 22/106; 106/156) are unchanged by round 1. The
  phantom-erratum deletion (PMID 33293699) touches only
  the row's claim text ("errata unchecked" → one genuine
  correction, contents unchecked): a claim-field
  bookkeeping item already listed in round-1 §3, not an
  effect/N update.
- **Pinyon 2014 (PMID 24760189; 7 v1 rows)** — paywall
  confirmed; N/arm and eABR numerics remain unextracted,
  so all 7 rows' `n=NOT-IN-ABSTRACT` stand. Browne 2016
  (in-vitro HEK293) has no v1 row and substitutes for
  nothing.
- **Dieter/Keppeler/Moser review (PMID 32227585)** —
  bibliographic upgrade only; no N or effect exists to
  move, and no v1 row cites it.

## 4. Reproducibility and checks run

All 2026-11-02, this session, from workspace root:

1. `python3 /tmp/enumerate_unrowed.py` — builds the 162-cell
   expected set from family-log §§2.1–2.6, parses v1 (199
   data rows, 14 cols, 123 distinct triples), prints the
   §1.2 bridge, the 48 unrowed cells with sibling windows,
   and the 11 extra triples.
2. `python3 /tmp/make_unrowed_csv.py` — writes
   `round2-unrowed-cells.csv` (48 rows); re-parses it and
   asserts 14 columns on header + every row.
3. Independent join check (separate snippet, not the
   generator): v1 + round-2 CSV → still-missing = `[]`;
   distinct triples 169 = 158 expected + 11 extra,
   as §1.2 predicts.
4. Source-presence counts in v1 for §3 (`grep -c` per
   PMID): 23467170 ×1, 27371868 ×3, 32596983 ×3,
   26209185 ×0, 32718992 ×0, 26826485 ×0, 32227585 ×0 —
   the zeros are the load-bearing evidence for §3.2.
5. C–H G4/G5/G6 base verdicts for §2 printed from v1 by
   parsed CSV (not from memory of the narratives).

Scratch scripts live in `/tmp` per convention and are not
part of the deliverable; the two research files are.

## 5. What is still owed after this attack

- **Gap-7 attack count:** this is **1/2** on the D14 and
  D16 sub-gaps (first completed attack on each; round 1 had
  0/2). Embase remains 0/2. No promotion-blocking gap
  reaches ≥2 because of this file, and the §7 rule-5(b)
  stop counter is unchanged.
- Human decisions queued by §1.3 (E temporal windows;
  G2-music W2 NA-vs-INSUFFICIENT; adopt-or-not the 11 extra
  triples) and by §3 (adopt U1–U6 into a frozen
  extraction_v2; new-row decisions for Pfingst 2015 /
  Keppeler 2020 with human figure reads).
- A real stress *test* (as opposed to template) still
  needs what §2's margin column lists per row: ratified
  U13/U17 margins, one measured candidate rate, frozen
  U09/U16 baselines, D1–D4 denominators. Until at least the
  margins exist, every future run of this template returns
  the same UNPINNABLE column by construction — re-running
  it without those inputs is not a second independent
  attack.
- Level-2 rows (≈527 reads), `gate_table.py` runs for
  C/D/E (D15, untouched here), and everything in
  `round1-summary.md` §6 remain exactly as owed.

*Unresolved: all margins, all candidate rates, Level-2
completeness, and every human gate. Closed by this file:
only the invisibility of 48 INSUFFICIENT cells and the
un-run state of the C–H stress template. No cell is PASS,
no candidate is promoted, no stress is survived.*
