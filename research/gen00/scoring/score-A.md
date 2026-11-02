# Step 3 scoring — Candidate A (focal electrical + anatomy fitting) [Track P]

> **Model routing (GOAL §9).** Requested route: **Sol 6.1 route,
> worker high**. Actual runtime model: **`muse-wonder-full-1.0`**
> (Sol 6.1 unavailable in this runtime), same effort split.
> Substitution disclosed per §9 rule 3. No claim here is Sol 6.1 work.
>
> **Date:** 2026-11-02. **Status: agent pre-extraction scoring —
> sensitivity/screening output, never gate-deciding.** Human dual
> extraction: **PENDING**. Human freeze: **PENDING**. Human-expert
> review PENDING — open synthesis, not a freeze.
>
> **Read in full before scoring:** `protocol.md`, `Q0-thresholds.md`,
> `AppendixA-v1.md`, `Step1-pin-summary.md`,
> `Step0-verified-bibliography.md`, `candidate-A-focal-electrical.md`,
> `cost_dictionary_v1.md`, `heldout-manifest.md`,
> `extraction-schema.md` + template. Scorer additionally re-inspected
> PMID 23467170 (Srinivasan) abstract via PubMed E-utilities MEDLINE
> on 2026-11-02 (verbatim-match to Step 0). All other evidence is
> Step 0/1 **design-side, abstract-level**; validation set is empty.
>
> **Binding caps applied:** PASS requires ≥Moderate GRADE
> (human-verified) **and** Appendix A minimum tier; abstract-level /
> agent-only evidence caps at **PROVISIONAL-SIGNAL** (never PASS);
> every extraction row therefore carries `grade=UNASSESSED`. G3b all
> **INSUFFICIENT**. INSUFFICIENT never imputed. Allegiance rule,
> decision-time analysis, treatment-policy estimand applied below.
> Convention-dependent verdicts (G1 "8", G2/G3a deltas, G6 caps) are
> **sensitivity-only** (unratified). No invented numbers.
>
> **G3b: BLOCKED (INSUFFICIENT) — co-design pending.** No Track P
> promotion is possible at v1. No ≥90% claim is made.
>
> Rows: `extract-AB.csv` (42 rows for A). Deterministic check:
> `adapt_extraction.py` + `gate_table.py` → A: G1/G2/G3a/G3b/G4/G5
> INSUFFICIENT, G6 FAIL (completeness), promoted FALSE.

## Verdict summary (deciding comparator: frozen; evolving = sensitivity)

| Gate | W0 | W1 | W2 | W3 | ADOL | Headline |
|---|---|---|---|---|---|---|
| G1-spectral | — | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | No numerator at anchors 8/4/10/16 |
| G1-temporal | — | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | No numeric PASS exists in v1; metric unmeasured |
| G2 | mechanism-only | mechanism-only | INSUFFICIENT | INSUFFICIENT (provisional null signals) | — | Best acute win barred (degraded comparator) |
| G2-music | — | — | NA-reason logged* | INSUFFICIENT | — | *No validated toddler battery; W3 capped provisional, no data |
| G3a | — | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | All strata (spoken/signed/bimodal) |
| G3b | — | INSUFFICIENT | INSUFFICIENT | INSUFFICIENT | — | BLOCKED |
| G4 | ALL: INSUFFICIENT (veto neither passed nor failed) ||||| Patency/Q0 UNDECIDABLE inputs |
| G5 | ALL + ADOL: INSUFFICIENT (FMEA complete; no rate-NI possible) ||||| Stresses: no verdict change (§ below) |
| G6 | ALL: **FAIL (completeness, timeline element)** ||||| Coverage/disparity elements INSUFFICIENT |

Evolving-standard sensitivity: dexamethasone-eluting / ECochG /
robotic elements were **not verified in Step 0** (no trial record
inspected), so no evolving-standard delta can be scored; A neither
beats nor loses to it on inspected records. Any future frozen win
without a verified evolving-standard win = implementation gap only.

## G1-spectral — INSUFFICIENT at anchor 8 and sensitivities 4/10/16

Both Appendix A §3.2 bars are unmet. (1) *Convention bar* (≥12
effective channels, STRETCH ≥16): Candidate A has **no measured
channel count** — the only channel-count evidence scores the
*comparator*: Friesen plateau 7–8 on 2001 arrays (PMID 11519582;
N=5 NH / 10 Nucleus-22 / 9 Clarion) supports "8" only as a
convention, and Berg 2019 (PMID 31067952; N=30) shows modern frozen
perimodiolar arrays already gain at 16 channels/maxima over 8. At
sensitivity anchor **16** the Track P bar is therefore at/near
frozen parity; at **4/10** the bar is lower but A still has no
numerator — verdict is INSUFFICIENT under every anchor, so no
anchor sensitivity flips anything. (2) *Head-to-head bar*: no ripple
(rip/oct, Henry paradigm PMID 16158665) or spread measurement of A
vs a named frozen array in one study/model exists in inspected
records; ripple→channels conversion is UNPINNABLE and forbidden.
The spread-narrowing mechanism signal (van den Honert & Kelsall
2007, PMID 17552721, N=3, originator lab → allegiance downgrade,
non-inventor replication absent) is logged as one
PROVISIONAL-SIGNAL row per window — and it points *against* the
kill criterion (narrowing only "at the cost of increased total
stimulation current"; dynamic focusing battery −48%, PMID
36279119). Channels-vs-maxima for A is pre-declared in the candidate
file but undisclosed in any result, because there are no results.
Decision-time: all G1 inputs are adult proxies for W1–W3 child-age
claims; infants cannot perform ripple tasks, so no direct infant G1
PASS was ever available in v1.

## G1-temporal — INSUFFICIENT (no numeric PASS exists in v1)

The +20% ITD margin is DELETED (Ehlers 2017, PMID 28618809: weak/
absent ITD in congenitally deaf BiCI children even on synchronized
research processors). A declares a temporal metric must not degrade
but measures none vs frozen head-to-head → INSUFFICIENT, not NA
(silent omission rule). No FAIL: degradation is unmeasured, not shown.

## G2 — INSUFFICIENT; provisional signals are nulls

Minimum tier T4; all focusing outcome evidence is T3 adult,
abstract-level, design-side. Srinivasan 2013 (+2.7 dB digits /
+3 dB sentences) is the only positive SRT result and it is **barred
as PASS evidence**: degraded experimental monopolar comparator,
N not in abstract (re-inspected 2026-11-02), no acute deficit vs
clinical map. The chronic evidence is uniformly null at group level
— van Groesen 2023 take-home null in noise (treatment-policy caveat:
13 fitted, 9 completed; the 4 non-completers must stay in the
denominator, which can only weaken the result), Bierer & Litvak
2016 group null (9 ears/8 listeners; "poorer performers tended
better" is post-hoc and scores nothing without pre-listed
multiplicity control), Caswell-Midwinter & Arenberg 2023 group null
(14 ears). These are logged as PROVISIONAL-SIGNAL rows (direction:
null). They cannot FAIL G2 either: an NI breach needs a same-test
delta worse than −5 pp / NI boundary at ≥Moderate GRADE vs a
clinical comparator, and no inspected abstract supplies an
interval-estimated delta of that kind. W2: no pediatric data. W0–W1:
mechanism only (Sharma P1, PMID 12476090, is proxy-chain context,
not A evidence). Music: CAMP adult-only (PMID 18309572, N=8 adults)
caps W3 at provisional; no A music data → INSUFFICIENT.

## G3a / G3b — INSUFFICIENT / BLOCKED

No Candidate A language data exist in inspected records, in any
modality or window. Independent blockers also stand: spoken
instruments uncited (Step 1 U11), frozen bilateral-P0 standard
scores UNPINNABLE (U10), signed instrument beyond 73 mo UNPINNABLE.
T4 is required; P1/fNIRS could never be sole G3 evidence. G3b:
BLOCKED (INSUFFICIENT) — co-design pending, all windows.

## G4 (Track P veto) — INSUFFICIENT: veto neither passed nor triggered

No A-specific comparative biology exists. Frozen-context rows only:
Seyyedi & Nadol 0–3 (27/28 granulomatous, PMID 25122600) and
Kamakura & Nadol (fibrous + new bone 17/17, PMID 27371868) are small
adult older-device archival series — presence evidence, downgraded
for P0 transport, and they describe the comparator, not A.
Residual-hearing frozen ref is UNPINNABLE for P0 infants (Madgar
78%, PMID 40052291, is mean-age-9.68 y better-hearing ears —
corrected against infant/patency use). Scala patency: UNPINNABLE;
Q0 on current inputs is **UNDECIDABLE** (no Q0-P %, no established-
implant Q0-A study; Q0-thresholds §2.3 minima unmet), so all
Q0-dependent cells read INSUFFICIENT; the Otarmeni label exclusion
(Q0-L) stays a separate regulatory fact. No AAV → G4-AAV not
applicable. A ≥1-grade fibrosis FAIL would need same-model
comparative histology at ≥Moderate GRADE; none exists either way.

## G5 — INSUFFICIENT; stress scenarios change nothing

Completeness element met: all 18 Appendix C FMEA rows filed with
severities, honestly-UNPINNABLE probability bands, mitigations and
stopping rules (candidate §8); absence of FMEA would have been a
FAIL, and it is not absent. But **no G5 rate-NI PASS is possible in
v1** (every margin UNPINNABLE, Step 1 U13), and no ≥major-severity
absolute signal at ≥Moderate GRADE exists to FAIL it. Candidate-
central gap: C9 charge safety has **no stated numeric safe limit,
tissue-damage margin, or named-device specification** — owed, and
it is the same gap that leaves the kill criterion unevaluable.

Stress re-scoring (cost dictionary §6; true 90th percentiles
UNPINNABLE → INSUFFICIENT-proxy-reported, never "stress survived"):

| Stress | Base → stress-proxy input | Verdict change |
|---|---|---|
| S-revision | Reimplantation post-2000 3.2% → 3.7% upper 95% CI (PMID 35973054; era sensitivities 9.2% / H2 8.5% reported alongside only) | **None** — G5 INSUFFICIENT at base and stress; no A-specific revision rate exists; focusing charge/battery cost is a mechanistic reason A could be *worse*, unquantified |
| S-nonuse | <8 h/day 6.8% (5 y) / 12.3% (10 y) → 10.0% / 17.1% CI-bound complements (PMID 24518403); complete 0 h/day UNPINNABLE | **None** — INSUFFICIENT throughout; A's −48% battery-life signal (T3) is a burden risk, not a measured non-use rate |
| S-access | LTF/D latest-era 31.3% dx / 20.3% EI → era-max proxies 42.1% / 39.4% (cost H4; mixes loss-to-documentation) | **None** — G6 coverage already INSUFFICIENT; A adds imaging/mapping visits whose access cost is unmeasured |
| S-surgical | Meningitis 0.07% → 0.10% upper CI (PMID 36864717; malformation 0.12% → 0.380%/ear); major-complication stress UNPINNABLE (H7 5.0%, no CI); facial/CSF/vestibular-absolute/anaesthesia UNPINNABLE | **None** — INSUFFICIENT at base and stress; A uses frozen surgery, but infant-specific deltas are unmeasured |

§6 decision rule cannot be applied: it needs a G2 PASS **and** G3b
NI; G2 is INSUFFICIENT and G3b is BLOCKED, so no added-risk trade
is acceptable or needed on current evidence.

## G6 — FAIL (completeness, timeline element); other elements INSUFFICIENT

Appendix A §7.3 makes the timeline element scorable now: "no stated
adult-first staging timeline = G6 FAIL." Candidate A states the
stage *sequence* (in-silico/bench → T2 → adult CI users → older
children → infants) but **asserts no numeric earliest-plausible
infant timeline**, deferring the year to a handoff design that does
not exist at scoring (candidate §11). A stage list without times is
not a timeline → completeness FAIL. This FAIL is (a) sensitivity-
only (unratified convention, agent-scored), (b) explicitly
remediable by stating a justified numeric timeline, and (c) subject
to a stated sensitivity: under the looser reading that the stage
sequence alone satisfies "staging stated," this cell flips to
INSUFFICIENT. Coverage % (D1–D4 blank) and disparity-vs-frozen
(frozen gaps UNPINNABLE, caps unratified) remain INSUFFICIENT;
burden is correctly specified as concurrent deltas only (added
imaging/mapping, battery replacements), with no invented absolutes.
FTO: Not assessed (travels).

## Kill criterion — modeled spread at safe charge: UNEVALUABLE

Pre-committed kill: no modeled spread reduction at safe charge in a
fibrotic/growing-cochlea model. **No such model run exists in
inspected records** (no named model/version/parameters/seeds, no
safe-charge limit for named contacts, no battery floor tested). The
kill is therefore **neither triggered nor cleared** — A is not
killed, and it has not survived its kill test either. Directional
evidence is adverse (spread narrowing bought with current, Ch2a;
archival fibrosis/new bone near-universal, E4a; take-home nulls,
Ch2b), which raises the prior that the model test will be hard, but
substituting that impression for the pre-specified test would be
exactly the post-hoc move the protocol forbids. The model test is
the single gating next step for this candidate.

## What would change these verdicts (ranked)

1. The kill-test model itself (fibrotic + growing geometry, frozen
   seeds) with pre-stated charge/battery limits — decides survival.
2. Human full-text dual extraction of Ch1/Ch2 primaries (incl.
   Srinivasan N from PMC3639477) — lifts the abstract cap; still
   design-side, still not validation.
3. Independent (non-inventor) take-home replication vs the *clinical*
   map with ripple + spread head-to-head vs a named frozen array —
   the only route to a G1/G2 provisional upgrade; post-2026-11-02
   evidence would enter as validation per held-out manifest.
4. A stated numeric timeline — flips G6 FAIL → INSUFFICIENT.
5. Registry per-harm P0 rates → G5 margins (Step 1 U13); frozen
   absolute G2/G3a ranges (U10); G3b co-design (B01) — without
   these, most cells cannot move regardless of A-specific data.
