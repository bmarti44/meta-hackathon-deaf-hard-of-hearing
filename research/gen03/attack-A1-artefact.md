# Gen 3 bounded attack A1 — grade-3 / 0.25 mm artefact case at fine grids

> **Model routing.** Requested: **Sol 6.1**. Actual:
> **`muse-wonder-full-1.0`**. Date: **2026-11-02**.
> **Status: bounded attack, not a new generation.** Per the
> Astra adjudication (`reviews/codex-astra-gen2-review.md`
> §4: "attacks now, no new design generation now"; "Keep
> A1's named-device/convergence prerequisites explicit"),
> this filing adds **no new candidate**, edits **no
> `model.py` semantics**, changes no gate cell, and does
> not advance the generation clock (Gen 2 = 2/4, counter
> 2/2 per `research/gen02/Gen2-summary.md`). FROZEN
> retained, G3b BLOCKED, Q0 undecidable — none of that is
> touched here.
> **LABEL (GOAL §5.1): T0 modelled sub-claim, conditional
> on the round-1 §3 assumptions.** Not a G1 PASS. Not a
> promotion probability.
> **Inspected records only:** the two files above read in
> full, plus `research/gaps/attack-A1-killtest.md`,
> `research/gaps/round2-A1-fix.md`, and
> `research/gaps/a1_model/{model.py, run_sweep.py,
> run_convergence.py, test_model.py, results_v2.csv,
> convergence.csv}`. No new literature, no new search,
> no invented parameters: every number below is re-derived
> from the filed model at a stated `dx`.

## 1. Question

The 12-case sweep (`results_v2.csv`, `dx = 0.125` mm)
contains exactly one zero: **grade 3 (proxy), electrode–
neuron distance 0.25 mm — monopolar 0.375 mm, tripolar
0.375 mm, width reduction 0.0%**, Q ratio 1.042. Round 1
(§4, §7) labelled it "treat as grid artefact, not
evidence": at that grid the SGN reading line (0.25 mm
above the electrode row) lies inside the 0.375 mm grade-3
sheath, and both widths are 3 cells. Round 2 (§5, §6
item 8) left it explicitly unresolved: the five-case
convergence series did not include it, and "fine-grid
runs of … the grade-3/0.25 mm artefact case" were owed.

**Attack question: at `dx = 0.03125` mm (and
`0.015625` mm if runtime allows), does the
zero-reduction persist or vanish?**

## 2. Method — same model, finer grids only

New script `research/gaps/a1_model/run_artefact_fine.py`
(new file; `model.py` untouched — verified: empty
`git diff` on `model.py`, and v1/v2/convergence CSV md5s
unchanged, §6). It calls `model.run_case` once per arm
(the same solves `model.compare` performs) for grade 3,
distance 0.25 mm, at `dx = dy ∈ {0.125, 0.0625, 0.03125,
0.015625}` mm, and derives the reduction / Q / battery
ratios with `compare`'s own arithmetic. Endpoint
unchanged: contiguous SGN-line run at ≥50% of peak
(`excitation_width`, v2.2); global span also recorded.

Two geometry facts, checked analytically from
`model.py:249-262` (not assumed):

- **No length snaps on any grid here.** Every physical
  length in this case is an exact integer multiple of
  every spacing used: electrode `y = 0.375`, wall 0.25,
  sheath 0.375, distance 0.25, contact spacing 1.0,
  domain 20×2 mm (e.g. at 0.015625: 24, 16, 24, 16, 64,
  1280×128 cells). Refinement changes discretisation
  only, never the geometry.
- **The SGN line is inside the sheath at every grid.**
  `sgn_j − elec_j = 0.25` mm < sheath thickness
  0.375 mm on all four grids (`sgn_in_sheath = True` in
  every CSV row; sheath occupies rows
  `elec_j … elec_j + sheath_rows − 1`, upward from the
  electrode row, full-length layer as filed). Finer
  grids therefore cannot "resolve away" the in-sheath
  placement — they can only resolve the width
  quantisation. The verdict in §5 splits exactly there.

Sanity anchor: the `dx = 0.125` row reproduces the
filed `results_v2.csv` grade-3/0.25 row **exactly**
(widths, 0.0%, Q 1.0420420998139974, battery
1.9798799896465948, both residuals) — the new script is
wired to the same model, not a variant of it.

## 3. Results (`a1_model/artefact_fine.csv`, 4 rows)

Loudness-balanced as filed. All 8 solves: CG converged,
rel. residual 7.85e-10–9.99e-10 < tol 1e-9 (iterations
219/217 → 1687/1635 across the series). Contiguous
width = global span in all 4 rows, both arms (profiles
unimodal at every grid).

| dx (mm) | nx×ny | mono mm (cells) | tri mm (cells) | red. % | Q ratio | batt | wall s |
|---|---|---|---|---|---|---|---|
| 0.125 | 161×17 | 0.37500 (3) | 0.37500 (3) | **0.00** | 1.0420 | 1.9799 | 0.7 |
| 0.0625 | 321×33 | 0.43750 (7) | 0.43750 (7) | **0.00** | 1.0491 | 1.9932 | 5.1 |
| 0.03125 | 641×65 | 0.53125 (17) | 0.46875 (15) | **11.76** | 1.0683 | 2.0297 | 40.7 |
| 0.015625 | 1281×129 | 0.60938 (39) | 0.54688 (35) | **10.26** | 1.0907 | 2.0724 | 322.9 |

**Answer: the zero does not persist.** It survives one
halving (0.0625 mm, still an exact 7-vs-7-cell tie) and
**vanishes at 0.03125 mm** (17 vs 15 cells, 11.76%),
remaining non-zero at 0.015625 mm (39 vs 35 cells,
10.26%). Runtime allowed the finest grid: full series
6 min 11 s (stdlib CG, Python 3.14.8), of which the
0.015625 pair is 323 s.

## 4. Convergence — honestly: not converged

The vanishing of the zero is the only robust statement.
The magnitudes are **not grid-converged**, by the same
standard round 2 §4 applied (last-step change is the
minimum discretisation uncertainty):

| step | Δ mono | Δ tri | Δ red. | ΔQ |
|---|---|---|---|---|
| 0.125 → 0.0625 | +0.0625 mm (1 fine cell) | +0.0625 (1) | 0.0 pp | +0.007 |
| 0.0625 → 0.03125 | +0.0938 (3) | +0.0313 (1) | +11.8 pp | +0.019 |
| 0.03125 → 0.015625 | +0.0781 (5) | +0.0781 (5) | −1.5 pp | +0.022 |

- Both widths **grow at every refinement** (coarse →
  finest: mono +62.5%, tri +45.8%), and the increments
  do not shrink (mono +1, +3, +5 fine cells). The last
  step alone moves each width by ~15–17% of its value.
  There is no defensible continuum width, and no
  Richardson extrapolation (quantised endpoint,
  non-shrinking steps).
- The reduction percentage is doubly unstable: it jumps
  0 → 11.76% on one halving, then falls to 10.26% only
  because the monopolar denominator keeps growing.
  (The absolute width *difference* is 0.0625 mm at both
  fine grids — 2 cells at 0.03125, 4 at 0.015625 — but
  with both widths still drifting by 5 fine cells per
  step, that coincidence buys no converged difference
  either.)
- Q ratio drifts **up with growing increments**
  (+0.007, +0.019, +0.022; 1.042 → 1.091 overall):
  not converged, worse-behaved than the round-2
  grade-0 cases. Quote it as ≈1.04–1.09 across grids,
  never as the coarse 1.042.
- Absolute `peak_at_unitI` falls ~5× per halving
  (1.48e-2 → 1.14e-4 mono): peaks are per-grid
  quantities only; nothing below uses them across
  grids. All claims rest on within-grid ratios and
  fraction-of-peak widths.

**Quoting rule for this case (extends round-2 §4):**
any number must carry its `dx`. The finest-grid values
(0.609 / 0.547 mm, 10.3%, Q 1.09 at `dx = 0.015625` mm)
are best-available with discretisation uncertainty of
at least the last-step changes above — i.e. the true
model-continuum reduction could plausibly be several
pp either side of ~10%, and the widths have no
demonstrated limit at the grids run.

### 4a. Mechanism check (diagnostic, not the filed endpoint)

A throwaway probe (re-solving `dx` = 0.125/0.0625/
0.03125 and linearly interpolating the 50%-of-peak
crossing between the straddling SGN-line nodes) shows
why the cell-count zero was a quantisation tie:

| dx | interp. mono (mm) | interp. tri (mm) | interp. red. % | cell-count red. % |
|---|---|---|---|---|
| 0.125 | 0.434 | 0.412 | 5.0 | 0.0 |
| 0.0625 | 0.478 | 0.452 | 5.6 | 0.0 |
| 0.03125 | 0.540 | 0.494 | 8.6 | 11.8 |

At the coarse grids both arms' crossings fall inside
the same edge cells (normalised edge values at
0.0625 mm: mono 0.616 inside / 0.476 outside; tri
0.593 / 0.441), so integer cell counts tie while the
underlying discrete profiles already differ. At
0.03125 mm the tripolar value at offset ±8 cells is
0.493 — just below the 0.5 threshold — against
monopolar 0.537, flipping the count by one cell per
side and *overshooting* the interpolated reduction
(11.8% vs 8.6%). The abrupt 0 → 11.8% jump is thus
exactly the expected signature of a quantised endpoint
crossing a threshold, not a physical discontinuity.
This probe changes no endpoint; it is reported only as
the mechanism behind §3.

## 5. Verdict

Split, as §2 foreshadowed:

1. **The exact zero is retired as a grid artefact.**
   "Grade 3 / 0.25 mm shows no tripolar narrowing"
   was a 3-cell (then 7-cell) counting tie. At both
   fine grids the filed endpoint gives tripolar
   narrower than monopolar in this case, consistent
   in direction with every other case-grid the model
   has produced (round-2 §4: 15/15; now +2 fine grids
   here). This case no longer supplies a zero at any
   grid finer than 0.0625 mm (six other sweep cases
   still have no fine-grid run at all; round-2 §4
   covered five cases, none of them this one).
2. **The case itself is not thereby rehabilitated as
   evidence.** The SGN line sits inside the assumed
   grade-3 sheath at *every* grid (distance 0.25 <
   sheath 0.375 mm) in a full-length-layer sheath
   geometry that round 2 already flagged as unphysical
   in extent (S4c(ii), unchanged). What the fine grids
   measure is the potential profile *within that
   modelled layer*. Whether a neuron line should ever
   be read there is a geometry/rubric question the
   missing Seyyedi–Nadol per-grade map (round-1 §6
   item 5, still ASSUMED) owns — refinement cannot
   answer it.
3. **No converged magnitude replaces the zero.** Per
   §4, "~10–12% at fine grids" is a `dx`-qualified,
   still-drifting model output, not a continuum value.
   It must not be quoted as the case's reduction, and
   round-1 §4's table keeps its `dx = 0.125` mm
   qualification for all 12 rows.
4. **Kill verdict unchanged: GEN1-A1 remains
   UNEVALUABLE** — neither killed nor kill-cleared
   (round-1 §6 items 1–6 and round-2 §6 items 7–8 all
   stand; removing the sole in-model "no reduction"
   row does not supply the named device, safe-charge
   limit, battery floor, growing geometry, grade
   rubric, or freeze that the decision rule needs).
   Nothing here may be quoted as "A1 survived". No
   gate cell, clock, counter, or STOP element moves.

What would close the numerical part of item 8 for this
case (not done, not claimed): a holder pre-stated
convergence criterion, then either a `dx = 0.0078125`
mm run (pure-Python CG scaling from the 323 s finest
pair estimates ~40+ min — an extrapolation, labelled
as such, not attempted) or a re-implementation under a
new freeze — plus a decision on whether an in-sheath
SGN reading line is admissible at all. Until then this
case carries direction-only weight, same as the rest
of the model.

## 6. Files and reproduce

Changed/added (nothing else edited; other Gen-3 attack
files and scoring edits in the tree are sibling tasks,
not this one):

- `research/gen03/attack-A1-artefact.md` (this file)
- `research/gaps/a1_model/run_artefact_fine.py` (new;
  SHA-256 `a9704bcd…f13c46abffee0`)
- `research/gaps/a1_model/artefact_fine.csv` (new,
  4 rows; SHA-256 `e91fe0fb…57e1d406` — contains a
  `wall_seconds` column, so the hash is run-specific;
  all physics columns are deterministic, no RNG,
  `SEED = 20261102`)

Untouched, md5 verified before/after: `model.py`
(empty `git diff`), `results.csv`
(`30cd31ce…`), `results_v2.csv` (`b9ec23c5…`),
`convergence.csv` (`3d0fee59…`) — matching round 2 §5.

```
cd research/gaps/a1_model
python3 test_model.py -v        # 10 tests — OK (run this session)
python3 run_artefact_fine.py    # 4 grids -> artefact_fine.csv (~6 min)
python3 run_artefact_fine.py 0.125,0.0625,0.03125   # subset, ~45 s
```

Python 3.14.8, stdlib only. The §4a interpolation probe
was a throwaway script under `/tmp` (definition in §4a;
values printed there), not a deliverable.
