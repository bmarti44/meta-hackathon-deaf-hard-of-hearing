# Gap attack A1 — kill-test T0 in-silico run (round 1)

> **Model routing:** requested **Sol 6.1**; actual
> **`muse-wonder-full-1.0`** (probe 2026-11-02: sol-6.1 route
> rejected / not in catalog). **Date:** 2026-11-02.
> **Task:** promotion-blocking-gap attack round 1 (GOAL §7
> rule 4); Step5 §6 gap 6 (A1 addendum — named model/seeds +
> per-contact safe-charge limit, then run).
> **LABEL (GOAL §5.1): T0 modelled sub-claim, conditional on
> assumptions in §3.** Not a G1 PASS. Not a promotion
> probability. No ≥90% claim.
> **Evidence discipline:** inspected records only (full
> API/text fetches logged in §2); snippets never evidence;
> no invented numbers — every parameter is cited or labelled
> ASSUMED with a sensitivity range.
> **Blinding honesty:** A1 §3 requires code + thresholds
> committed *before outputs opened*. This attack wrote code
> and ran it in one session (uncommitted, exploratory).
> It therefore **cannot** satisfy the frozen kill test even
> where numbers exist; it tests whether the test is runnable
> and what it would need. See verdict §6.

## 1. Files read first (workspace)

- `research/Step5-decision-no-winner.md` §6 gap 6 + §5.3:
  A1 kill-test "specifiable only until model/seeds/
  safe-charge filed".
- `research/gen01/candidate-A1-killtest.md` §3 (the
  pre-specification + decision rule) and §8–§9 caps.
- `research/gen00/candidate-A-focal-electrical.md` §3, §8
  row C9, §11 kill criterion (verbatim parent).
- `research/gen00/scoring/score-A.md` (kill = UNEVALUABLE;
  "the single gating next step"), judge-1/judge-3 kill rows.
- `research/step0/Step0-verified-bibliography.md` Ch2a/Ch2b
  (van den Honert PMID 17552721 charge cost; van Groesen
  PMID 36279119 −48% battery), E4a (Seyyedi PMID 25122600;
  Kamakura PMID 27371868).
- `research/frozen_baseline/AppendixA-v1.md` N4 (Seyyedi &
  Nadol **0–3**, 3× 1-mm segments; per-grade rubric
  unextracted) and §7.2 ("manufacturer specs owed").
- `research/gen01/scoring/score-gen1.md` + `step4-skeptic.md`
  (safe-charge limit + battery floor not filed → UNEVALUABLE).

**Workspace search result (2026-11-02, this attack):** no
named array, no manufacturer max charge density, no contact
area, no battery floor, and no growing-geometry
age/dimension set is filed anywhere in `research/`. Every
mention says "owed". That search (not an impression) drives
the §6 verdict.

## 2. External records inspected in full (2026-11-02)

Fetched as full API/text bodies via `web_fetch`/Europe PMC
`fullTextXML`. Search-result JSON was used only to locate
records, never as evidence.

| # | Record (inspected body) | What was taken |
|---|---|---|
| X1 | Shannon 1992, *IEEE TBME* 39:424–6, PMID 1592409 (PubMed MEDLINE, full abstract) | Model exists; **abstract contains no numeric k** — the primary alone cannot pin a limit |
| X2 | Li et al. 2024, *J Neural Eng*, PMID 38885676, PMC11641559 (full text XML) | Shannon eq. (1): k = log₁₀(Q) + log₁₀(D); §2.2 units Q nC/ph in their dataset, D µC·cm⁻²·ph⁻¹; proposed boundary **k = 1.5–2.0**, example threshold 1.85; best accuracy 63.9% at k = 1.79 (1.79–1.86 range); fit on cat-cortex epidural macro-electrodes; notes intracochlear stimulation >100 µC/cm² without neuron-function loss despite exceeding Shannon |
| X3 | Greenwood 1990, *JASA* 87:2592–605, PMID 2373794 (MEDLINE) | Identity of the frequency–position function; constants not in abstract |
| X4 | Dhanasingh 2021, PMID 33474539, PMC7801236 (full text XML) | Human Greenwood eq. (6): F = 165.4·(10^(2.1x) − 0.88), x = proportion of basilar-membrane length; worked example A = 9.0 mm → CDL 33.46 mm |
| X5 | Sriperumbudur et al. 2024, *Sci Rep* 14:9593, PMID 38671022, PMC11053021 (full text XML) | Perilymph 1.2 S/m (in-silico range to 1.43); bone 0.0334–0.0836 S/m; healthy modiolus effective 0.2734 S/m (20% porosity); pores filled with ossified bone/fibrous tissue → 0.0334 S/m worst case; gerbil modiolus 0.234→0.347 S/m after degeneration |
| X6 | Seyyedi & Nadol 2014, PMID 25122600, PMC4165780 (MEDLINE full abstract; Europe PMC fullTextXML returned HTTP 500 — full text NOT inspected) | Severity 0–3 at three 1-mm segments; granuloma 27/28 (96.4%); basal > distal. **Per-grade rubric still uninspected** |

**Safe-charge limit status: UNPINNABLE-input (formal).**
The A1 limit is min(manufacturer max for *named* contacts,
tissue threshold ÷ *pre-stated* margin), human-extracted
pre-output. None of (named device, manufacturer value,
margin) exists. Shannon k = 1.5–2.0 (X2) is used below as a
clearly-labelled **proxy sensitivity only** — it is a
cat-cortex model that X2 itself shows mispredicts
intracochlear data, so it can never be the filed limit.

## 3. Model filed by this attack

`research/gaps/a1_model/model.py` (this attack's named-model
*proposal* for the freeze addendum — human freeze PENDING,
so it is not yet "the" A1 model):

- **Physics:** 2-D FDM volume conductor on an unwound
  scala-tympani strip, ∇·(σ∇V) = −I, harmonic-mean face
  conductivities, V = 0 boundary (distant monopolar
  return), conjugate-gradient solver. Modiolar wall strip
  + perilymph + fibrosis sheath layers.
- **Arms:** monopolar vs tripolar (centre +1, flanks
  −σ_f/2 each; σ_f = 0.9 base, 0.5/1.0 sensitivity) on the
  same 3-contact geometry. Phased-array is represented by
  the same weight family. **Loudness balance:** each arm
  scaled to unit peak SGN-line potential; centre-contact
  charge ratio and Σ|I| battery proxy reported exactly
  (linear system → width at fixed fraction of peak is
  scale-invariant).
- **Endpoint:** contiguous SGN-line extent ≥50% of peak
  (sensitivity 30/70%), in mm and octaves (Greenwood X4,
  mid-array place 0.65·L). No ripple→channels conversion.
- **Fibrotic geometry:** sheath thickness/σ by grade
  proxy (below), per-segment grading collapsed to a single
  uniform grade per run (limitation, §7).
- **Growing geometry:** NOT implemented as ages — none are
  pre-stated in A1. Implemented only as electrode–neuron
  distance sweep (0.25/0.5/1.0 mm) + cochlea-length
  sensitivity for octaves. Adult strip only.
- **Seeds:** `SEED = 20261102`; solver deterministic, no
  RNG. Re-run `results.csv` md5 identical
  (`30cd31ce…`, verified twice this session).
- **Environment:** Python 3.14.8; `numpy` checked and
  **absent** (`ModuleNotFoundError`) → stdlib only.
- **Tests:** `test_model.py`, 6/6 pass (Greenwood,
  Shannon arithmetic, homogeneous decay, tripolar
  narrower-but-costlier in clean case, distance broadening).

### Parameter table (every number traced)

| Parameter | Value | Status / sensitivity |
|---|---|---|
| Perilymph σ | 1.2 S/m | CITED X5; sens 1.43 |
| Bone σ | 0.0334 S/m | CITED X5 (range to 0.0836) |
| Modiolus σ_eff | 0.2734 S/m | CITED X5 |
| Grade 0 sheath | none | by definition of scale X6 |
| Grade 1 → 0.125 mm, 0.30 S/m | — | **ASSUMED map** (σ within cited 0.0334–1.2 bounds) |
| Grade 2 → 0.25 mm, 0.10 S/m | — | **ASSUMED map**; sens σ 0.0334 / 1.2 |
| Grade 3 → 0.375 mm, 0.0334 S/m | — | **ASSUMED map**; σ = cited fibrous-filled worst case X5 |
| Greenwood A/a/k | 165.4 / 2.1 / 0.88 | CITED X4 (orig. X3) |
| Cochlea length L | 35 mm | ASSUMED; sens 28 mm; cited example 33.46 X4 |
| Strip 20×2 mm, dx = dy = 0.125 mm | — | ASSUMED numerics (width quantised to 0.125 mm) |
| Contact spacing | 1.0 mm | ASSUMED (no named array); sens 0.7 / 1.5 |
| Electrode–neuron dist. | 0.25/0.5/1.0 mm | ASSUMED sweep |
| Contact area | 0.003 cm² | ASSUMED; only affects §5 illustration |
| Pulse width | 25 µs | ASSUMED; only affects §5 illustration |
| Width threshold | 50% of peak | ASSUMED convention; sens 30/70% |
| Shannon limit (proxy only) | k = 1.85 | CITED range 1.5–2.0 X2; formal limit UNPINNABLE |

## 4. Results — primary sweep (`a1_model/results.csv`)

Loudness-balanced (equal SGN peak). Q ratio = centre-contact
charge tripolar/monopolar; batt proxy = Σ|I| ratio.

| grade(proxy) | dist mm | mono mm | tri mm | mono oct | tri oct | width red. % | Q ratio | batt proxy |
|---|---|---|---|---|---|---|---|---|
| 0 | 0.25 | 1.12 | 0.88 | 0.23 | 0.18 | 22.2 | 1.34 | 2.54 |
| 0 | 0.5 | 1.62 | 0.88 | 0.34 | 0.18 | 46.2 | 1.57 | 2.99 |
| 0 | 1.0 | 2.12 | 1.12 | 0.44 | 0.23 | 47.1 | 1.99 | 3.79 |
| 1 | 0.25 | 1.12 | 0.62 | 0.23 | 0.13 | 44.4 | 1.31 | 2.49 |
| 1 | 0.5 | 1.62 | 0.88 | 0.34 | 0.18 | 46.2 | 1.54 | 2.93 |
| 1 | 1.0 | 2.12 | 1.12 | 0.44 | 0.23 | 47.1 | 1.96 | 3.73 |
| 2 | 0.25 | 1.12 | 0.62 | 0.23 | 0.13 | 44.4 | 1.30 | 2.48 |
| 2 | 0.5 | 1.62 | 0.88 | 0.34 | 0.18 | 46.2 | 1.54 | 2.93 |
| 2 | 1.0 | 2.12 | 1.12 | 0.44 | 0.23 | 47.1 | 1.97 | 3.74 |
| 3 | 0.25 | 0.38 | 0.38 | 0.08 | 0.08 | 0.0 | 1.04 | 1.98 |
| 3 | 0.5 | 1.38 | 0.88 | 0.28 | 0.18 | 36.4 | 1.46 | 2.77 |
| 3 | 1.0 | 2.12 | 1.12 | 0.44 | 0.23 | 47.1 | 1.87 | 3.56 |

Sensitivities (grade 2, dist 0.5): partial-tripolar
σ_f = 0.5 → 30.8% reduction, Q 1.24×, batt 1.86×; full
σ_f = 1.0 → 46.2%, Q 1.64×, batt 3.28×; sheath σ forced to
1.2 or 0.0334 at grade-2 thickness → reduction unchanged
(46.2%), Q 1.57/1.54×; threshold 30% → 52.6%, 70% → 28.6%;
spacing 0.7 mm → Q 1.90×, 1.5 mm → 30.8%, Q 1.24×;
perilymph 1.43 S/m → unchanged; L = 28 mm shifts octaves
only (mono 0.42, tri 0.23).

**Reading of the modelled sub-claim.** Under these
assumptions tripolar narrowing (22–47%) persists across
the fibrosis-proxy sweep at 1.3–2.0× centre charge. The
uniform sheath behaves almost entirely as a series
resistance: loudness balancing re-scales it away, so
grades 0–2 barely move the *relative* width (absolute
voltage headroom is not modelled — a real device
compliance limit could still bind, and no device is
named). The single zero (grade 3, dist 0.25, width
0.38 mm) puts the SGN line inside the thick sheath on a
0.125-mm grid: treat as grid artefact, not evidence.
Battery proxy 2.5–3.8× Σ|I| is directionally consistent
with the inspected clinical cost signals (PMIDs 17552721,
36279119) — and there is no filed floor to test it against.

## 5. Charge / Shannon-proxy illustration (NOT the limit)

With ASSUMED area 0.003 cm² and 25 µs phase: 0.2–2.0 mA →
Q 5–50 nC/ph, D 1.7–16.7 µC/cm²/ph, Shannon k −2.08…−0.08
— far below the X2 boundary 1.5–2.0 even after the
≤2× tripolar multiplier. So *if* Shannon were the limit,
the spread arm of the kill would not fire in this model.
But X2 shows Shannon was fit on cat-cortex epidural
macro-electrodes, classifies at only 63.9% accuracy, and
is already exceeded intracochlearly without reported
neuron loss. It is the wrong instrument for a per-contact
CI limit. **Formal safe charge remains UNPINNABLE-input.**

## 6. Kill verdict — UNEVALUABLE (exact missing inputs)

Per A1 §3's own rule — "If no named-device limit can be
filed, test stays UNEVALUABLE by design — reported as
such, never passed" — and §9 (verdict must hold across the
pre-stated plausible range): **GEN1-A1 is neither KILLED
nor kill-cleared by this attack.** The decision rule
(kill iff no reduction at ≤ limit in *either* fibrotic
*or* growing geometry, or reduction only above limit /
below battery floor) cannot be evaluated because:

1. **Named array + manufacturer max charge density**
   (µC/cm²/ph) + per-contact areas, human-extracted and
   filed before outputs — MISSING (workspace search §1).
2. **Pre-stated safety-margin divisor** to a tissue-damage
   threshold — MISSING (never stated anywhere).
3. **Battery floor** (min processor h/day, named-device
   spec) — MISSING. Model battery proxy (2.5–3.8×) has
   nothing to be compared with.
4. **Growing geometry:** pre-stated ages + infant→child
   dimensions + re-derived electrode–modiolus distances
   in the freeze addendum — MISSING. This run is an adult
   strip + distance sweep; the growing arm of the rule is
   untouched. (Adult non-fibrotic reference "cannot pass
   the kill test alone", A1 §3.)
5. **Seyyedi–Nadol per-grade rubric** → physical
   thickness/conductivity map — full text uninspected
   (X6: abstract only; Europe PMC 500). Grade map here is
   ASSUMED.
6. **Freeze/blinding:** model, seeds, thresholds and code
   committed before outputs opened, human-frozen — NOT
   DONE (this attack is exploratory, one session). Any
   post-hoc change = new candidate (A1 §3).

What would make it evaluable, in order: holder names the
array → human extractor files manufacturer limit + areas
+ battery spec → addendum pins margin, ages/dimensions,
grade-rubric map, this (or another) model + seeds →
commit → run → verdict per §3 rule. Nothing in §4 may be
quoted as "A1 survived": the modelled direction (narrowing
survives a uniform sheath; charge cost 1.3–2.0×; battery
proxy 2.5–3.8×) is a T0 sub-claim about *this* model only.

## 7. Model limitations (attack on this attack)

2-D unwound strip (no coiling, no scala vestibuli/media,
no return-path anatomy); potential-at-SGN-line proxy, no
nerve-fibre activating-function/biophysical SGN model;
single place, single uniform grade (A1 wants basal/mid/tip
per segment, basal worst per X6); 0.125-mm grid quantises
widths and creates the grade-3/0.25-mm artefact; no
voltage-compliance limit (the channel through which a real
fibrosis series-resistance could kill focusing headroom);
phased-array ≠ full multi-contact optimisation; anatomy-
fitting factorial (parent §3(4)) not modelled. A finer
grid + segment-graded sheath + compliance cap are the
highest-value round-2 refinements — but they change
nothing in §6: the blocking inputs are documentary, not
numerical.

## 8. Reproduce

```
cd research/gaps/a1_model
python3 test_model.py -v     # 6 tests, stdlib unittest
python3 run_sweep.py         # prints §4 tables, writes results.csv
```
Python 3.14.8, stdlib only (numpy absent in this runtime).
Files: `model.py`, `test_model.py`, `run_sweep.py`,
`results.csv` (12 rows). Uncommitted at writing; commit is
the holder's freeze act, not this attack's.
