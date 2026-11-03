# Gap attack A1 — round-2 model fix (Skeptic S4)

> **Model routing:** requested **Sol 6.1**; actual
> **`muse-wonder-full-1.0`** (disclosed per GOAL §9 rule 3).
> **Date:** 2026-11-02.
> **Inputs read:** `research/gaps/round1-summary.md`,
> `research/gaps/gap-skeptic.md` (esp. S4a–S4c),
> `research/gaps/attack-A1-killtest.md` (round-1 file) +
> `research/gaps/a1_model/` v1 code and `results.csv`.
> **LABEL (GOAL §5.1): T0 modelled sub-claim, conditional
> on round-1 §3 assumptions.** Not a G1 PASS. Not a
> promotion probability. No ≥90% claim.
> **Evidence discipline:** inspected records only (full
> XML/PDF bodies logged in §2); search snippets were used
> only to locate records, never as evidence; no invented
> numbers. Agent work only; human dual extraction PENDING.
> This file edits no earlier round-1 file and changes no
> gate cell.

## 1. Headline

The four sceptic-S4 fixes were executed. None changes the
kill verdict.

- **Shannon Q unit convention: NOT pinnable to one
  convention from inspected sources.** Li 2024 §2.2
  (inspected full text) prints Q in **nC/ph**; Liu 2024
  (inspected publisher PDF) prints Q in **µC/phase**;
  both cite the same k = 1.5–2.0 boundary. The Shannon
  1992 primary was inspected at abstract level only (no
  units, no numeric k; IEEE full text not accessible by
  this route). The two printed conventions differ by
  exactly **+3.00 in k**, so round-1 §5's single-k
  sentence stays withdrawn and v2 **brackets** k under
  both conventions (§2, §3).
- **Grid convergence: direction robust, magnitudes NOT
  grid-converged.** On the dx = 0.125 / 0.0625 / 0.03125 mm
  series (fixed physical geometry), tripolar is narrower
  than monopolar in all 15 case-grids and Q/battery
  ratios are stable to ~0.01–0.05, but the last refinement
  still moves width reduction by **0.6–8.4 percentage
  points** by case (grade-3 case non-monotone). No §4
  percentage may be quoted without its dx (§4).
- **`excitation_width` fixed** to the documented
  contiguous-run definition; v1 global span kept as
  `excitation_span_global`. On every swept profile in
  v1 and in the convergence series the two definitions
  coincide (unimodal profiles); they differ on the
  sceptic's bimodal probe, now a regression test (§3).
- **Sweep rerun:** `a1_model/results_v2.csv` (12 rows,
  md5 `b9ec23c5…`, reproduced identically on re-run)
  matches v1 `results.csv` (md5 `30cd31ce…`, preserved
  untouched) exactly on all shared columns at
  dx = 0.125 mm — the v2 code changes are non-perturbing
  at the v1 grid — and adds dx, global-span,
  solver-converged and residual columns. All 24 v2
  solves report CG converged (rel. residual < 1e-9).
- **Verdict: still UNEVALUABLE** (§6). Do not upgrade.
  The blocking inputs remain documentary, exactly as in
  round 1 §6, plus the now-documented facts that (i) the
  Shannon unit basis is unresolved in print and (ii)
  width magnitudes are not grid-converged.

## 2. Shannon Q unit pin attempt (inspected sources)

All bodies below were fetched and read in full this
session (2026-11-02). Li 2024 via Europe PMC
`fullTextXML` for PMC11641559 (198,617 B). Cogan 2016
via NCBI efetch `db=pmc&id=5386002` (157,458 B; Europe
PMC returned HTTP 500 for this record). Liu 2024 via
publisher PDF (IOP, 1,982,702 B, 12 pp.) saved by
`web_fetch` and extracted locally with `pypdf` 6.21.3
from the local uv wheel cache (system `python3` has no
`pypdf` installed; the cached package was put on
`sys.path` — stated plainly because "pypdf available"
is true of the cache, not of the bare interpreter).
Shannon 1992 via NCBI efetch MEDLINE for PMID 1592409;
DOI `10.1109/10.126616` resolves to IEEE Xplore, which
returned no body by this route.

### 2.1 Li et al. 2024 (PMID 38885676, PMC11641559)

Section 2.2, verbatim (XML text, whitespace normalised):

> "2.2. Predictions using the Shannon equation Two
> features, charge per phase (unit: nC ph −1 ) and charge
> density per phase (unit: μ C cm −2 ph −1 ), were used to
> calculate the k -values related to the Shannon equation
> (equation ( 1 )). We tested a range of k threshold
> values ranging from k = −4 to k = 4 … The calculated
> k -values below a given threshold (e.g. k = 1.85) were
> classified as non-damaging …"

Equation (1) in the same full text:

> "k = log10(Charge density) + log10(Charge). For the
> Shannon equation, a proposed limit between damaging
> and non-damaging was set at a range between k = 1.5
> and k = 2.0 …"

And the scoring result (abstract + §3, inspected):
"The Shannon equation yielded an accuracy of 63.9%
using a k value of 1.79", with maximum accuracy at
"k-values ranging from k = 1.79 to k = 1.86". Table 1
of the same paper likewise lists `Charge_per_phase` in
`nC ph−1` and `Charge_density_per_phase` in
`μC ph−1 cm−2`.

So Li's **printed** convention is Q in nC/ph. Whether
Li's underlying computation converted units before
applying equation (1) cannot be determined from the
inspected text (their code/data supplement was not
inspected here), and this file does not assert that
Li computed wrongly — only that their printed §2.2
unit statement, taken at face value, is the nC
convention. That is precisely the sceptic S4a point.

### 2.2 Liu et al. 2024 (PMID 38776894, DOI 10.1088/1741-2552/ad4f16)

*J. Neural Eng.* 21 (2024) 036034, publisher PDF,
extracted text (p. 7):

> "Substituting the threshold charge values … into the
> Shannon equation, log(D) = k − log(Q), where D is the
> charge density per phase in µC cm −2 phase−1 and Q is
> the total charge in µC phase −1, yielded k values that
> increased with pulse width from 0.70 ± 0.32–1.45 ±
> 0.10. As a k value lower than 1.5 typically indicates
> absence of tissue damage …"

So Liu's printed convention is Q in **µC/phase** — the
convention v1 `model.py` used — with the same numeric
1.5 boundary region. (Liu's reference [40] is Shannon
1992; [43] is Cogan 2016.) This is an application paper
(stent-electrode femoral nerve), not a Shannon
re-derivation; its weight is as an inspected,
explicit-unit restatement, not as primary evidence.

### 2.3 Cogan et al. 2016 (PMID 26792176, PMC5386002)

Full text inspected. Their "Shannon equation" section
states the boundary "on a log charge density (D) versus
log charge per phase (Q) plot as a line with the
equation: (1) log(D) = k − log(Q). Equation (1) contains
the adjustable parameter k, typically chosen between
1.5 and 2.0", derived from McCreery et al. (50 pps,
0.4 ms/phase, Pt disks 0.01–0.5 cm²), with "A k value of
1.85 was chosen for figure 1". **That sentence states
no explicit unit for Q**, so Cogan corroborates the
formula and the 1.5–2.0 / 1.85 boundary numbers but
does not pin the Q unit. (Their charge-density
quantities elsewhere are in µC cm⁻², e.g. the 30 µC cm⁻²
limit; that still does not fix the log(Q) unit basis.)

### 2.4 Shannon 1992 primary (PMID 1592409) — inaccessible

MEDLINE abstract inspected in full: "A model is
presented that represents a large body of data on safety
and damage levels of electrical stimulation…" — **no
numeric k and no units in the abstract**. The IEEE
full text (doi 10.1109/10.126616) returned no body via
this route. The primary-text unit pin therefore
remains **not done**, exactly as sceptic S4a left it;
it requires a human/licensed read of the 3-page paper.

### 2.5 Disposition: bracket, do not pick

Inspected print contains both conventions with the
same numeric boundary:

| Convention | Source (inspected body) | Q unit in log(Q) |
|---|---|---|
| Li printed | Li 2024 PMC11641559 §2.2 + Table 1 | nC/ph |
| Classic | Liu 2024, *JNE* 21:036034 p.7 (PDF) | µC/phase |
| (formula only) | Cogan 2016 PMC5386002 eq. (1) | not stated |

For the same physical charge, Q[nC] = 1000·Q[µC], so
**k_Li − k_classic = log₁₀(1000) = +3.00 exactly**,
independent of D. A charge multiplier r at fixed area
adds **2·log₁₀(r)** to k under either convention (D
scales with Q), as sceptic S4a noted — not log₁₀(r).

Bracket for the round-1 §5 ASSUMED illustration (area
0.003 cm² ASSUMED, 25 µs ASSUMED; recomputed by v2
`absolute_charge_check`, §3):

| I (mA) | Q | D (µC/cm²/ph) | k_classic (µC) | k_Li (nC) | k at r=2×, classic / Li |
|---|---|---|---|---|---|
| 0.2 | 5.0 nC/ph | 1.7 | −2.08 | +0.92 | −1.48 / +1.52 |
| 0.5 | 12.5 nC/ph | 4.2 | −1.28 | +1.72 | −0.68 / +2.32 |
| 1.0 | 25.0 nC/ph | 8.3 | −0.68 | +2.32 | −0.08 / +2.92 |
| 2.0 | 50.0 nC/ph | 16.7 | −0.08 | +2.92 | +0.52 / +3.52 |

Reading, without choosing a convention: under the
classic (µC) reading every illustrated point stays
below 1.5 even at r = 2; under Li's printed (nC)
reading the bracket crosses 1.5–2.0 already at
0.5 mA-equivalent and exceeds it at 1–2 mA. **The
illustration therefore cannot support a "far below the
boundary" sentence in either direction until the
primary unit basis is pinned** — and even then Shannon
remains a cat-cortex macro-electrode proxy that Li
(score 63.9%) and round-1 §5 already refuse as the
filed CI limit. Round-1 §5's withdrawn sentence stays
withdrawn. Formal safe charge remains
**UNPINNABLE-input**.

## 3. Code fixes in `a1_model/` (versioned v2)

Files edited/added; v1 `results.csv` preserved
untouched (md5 `30cd31cecc5759e41e9f94f009c0c39a`
before and after this round).

- **`model.py` → v2** (header carries the version log):
  - *v2.1 Shannon units.* `shannon_k` documented as the
    classic (Liu 2024) µC convention with explicit
    argument names (`charge_uc_per_phase`,
    `charge_density_uc_cm2_per_phase`); new
    `shannon_k_li_nc` (Li §2.2 nC) and
    `shannon_k_bracket` returning both (difference
    exactly 3.00). `absolute_charge_check` now returns
    `(q_uc, q_nc, D, k_classic, k_Li)` and documents the
    2·log₁₀(r) multiplier rule. Citation block quotes
    all four §2 sources; no single `k = log10(Q[uC])…`
    claim remains.
  - *v2.2 Width definition.* `excitation_width` is now
    the contiguous run about the peak index at
    ≥ frac·peak (the round-1 §3 wording). **Choice, as
    documented in the code:** the endpoint is the width
    of the central excited lobe; separated side lobes
    and the silent gap between them are not excited
    tissue and are not counted. V1 behaviour is retained
    verbatim as `excitation_span_global` for comparison,
    and both widths are reported per case.
  - *v2.3 Fixed physical geometry.* Electrode row and
    modiolar-wall rows were hard-coded counts
    (`elec_j = 3`, wall = 2 rows): refining dy silently
    moved the electrode and thinned the wall. They are
    now physical parameters `electrode_y_mm = 0.375` and
    `modiolar_wall_mm = 0.25` (equal to the v1 counts ×
    0.125 mm, so v1-grid results are unchanged — proven
    in §5), converted to rows at each dy. Without this,
    a "convergence series" would conflate discretisation
    with a geometry change. (This also explains the
    sceptic's dx = 0.0625 probe value, §4.)
  - *v2.4 Solver flag.* New `solve_with_info` returns
    relative residual, `converged` (residual < tol =
    1e-9) and iteration count; `solve` is a thin
    backward-compatible wrapper. `run_case`/`compare`
    propagate the flags. V1 returned silently at
    `max_iter = 8000`.
  - Unchanged from v1, stated plainly: physics, grade→
    (thickness, σ) ASSUMED proxy map, contact spacing/
    area/pulse-width ASSUMPTIONS, arms, loudness
    balancing, and the fibrosis sheath as a
    **full-length layer** at every column (sceptic
    S4c(ii); now also noted in the `build_sigma`
    docstring). Localising the sheath was not in this
    round's four-item mandate and is not claimed.

- **`test_model.py` → 10 tests** (v1: 6; all pass, §5).
  New: `test_shannon_units_bracket` (0.1 µC = 100 nC →
  k 1.0 vs 4.0 at D = 100), `test_shannon_multiplier_
  adds_2log10r`, `test_excitation_width_contiguous_vs_
  global` (sceptic bimodal probe `[0,10,0,0,9,0]`,
  dx = 1, frac = 0.5: contiguous **1.0**, global
  **4.0**; unimodal control where they coincide), and
  `test_solver_reports_convergence`.

- **`run_sweep.py` → v2.** Writes **`results_v2.csv`**
  (v1 file never overwritten); Shannon block prints the
  bracket. Sensitivities unchanged.

- **`run_convergence.py` (new).** The §4 series; writes
  `convergence.csv` (15 rows, incl. wall time and
  solver flags).

- **`results_v2.csv` (new, 12 rows)** and
  **`convergence.csv` (new, 15 rows)**. §5 gives md5s.

## 4. Convergence series (dx = dy = 0.125 / 0.0625 / 0.03125 mm)

`run_convergence.py`, fixed v2.3 physical geometry,
five representative cases (the full 12-case sweep at
0.03125 mm was not run; stdlib CG costs 26–41 s per
compare at the fine grid — wall times are in
`convergence.csv`). All 30 solves: CG converged,
rel. residual < 1e-9. Contiguous width = global span
in all 15 rows (profiles unimodal at every grid).

| grade | dist (mm) | dx | mono (mm) | tri (mm) | red. % | Q ratio | batt |
|---|---|---|---|---|---|---|---|
| 0 | 0.5 | 0.125 | 1.6250 | 0.8750 | 46.2 | 1.573 | 2.988 |
| 0 | 0.5 | 0.0625 | 1.6875 | 0.9375 | 44.4 | 1.586 | 3.014 |
| 0 | 0.5 | 0.03125 | 1.6562 | 0.9688 | 41.5 | 1.590 | 3.020 |
| 0 | 0.25 | 0.125 | 1.1250 | 0.8750 | 22.2 | 1.339 | 2.544 |
| 0 | 0.25 | 0.0625 | 1.1875 | 0.8125 | 31.6 | 1.351 | 2.567 |
| 0 | 0.25 | 0.03125 | 1.2188 | 0.7812 | 35.9 | 1.354 | 2.573 |
| 0 | 1.0 | 0.125 | 2.1250 | 1.1250 | 47.1 | 1.994 | 3.789 |
| 0 | 1.0 | 0.0625 | 2.1875 | 1.1875 | 45.7 | 2.012 | 3.822 |
| 0 | 1.0 | 0.03125 | 2.2188 | 1.2188 | 45.1 | 2.017 | 3.832 |
| 2 | 0.5 | 0.125 | 1.6250 | 0.8750 | 46.2 | 1.540 | 2.925 |
| 2 | 0.5 | 0.0625 | 1.6875 | 0.9375 | 44.4 | 1.581 | 3.004 |
| 2 | 0.5 | 0.03125 | 1.7188 | 0.9688 | 43.6 | 1.621 | 3.081 |
| 3 | 0.5 | 0.125 | 1.3750 | 0.8750 | 36.4 | 1.456 | 2.766 |
| 3 | 0.5 | 0.0625 | 1.4375 | 0.9375 | 34.8 | 1.481 | 2.815 |
| 3 | 0.5 | 0.03125 | 1.5938 | 0.9062 | 43.1 | 1.530 | 2.907 |

**Honest convergence assessment.** Widths are quantised
to integer cells, so the smallest resolvable change is
one dx; successive-refinement changes (0.0625 →
0.03125) and what they do and do not show:

- **Width reduction is not grid-converged.** Last-step
  changes: −2.9 pp (grade 0, 0.5 mm), +4.3 pp (grade 0,
  0.25 mm), −0.6 pp (grade 0, 1.0 mm), −0.8 pp (grade 2,
  0.5 mm), **+8.4 pp (grade 3, 0.5 mm, non-monotone:
  36.4 → 34.8 → 43.1)**. Individual widths still move
  by 1–5 fine cells on the last step (worst: grade-3
  monopolar 1.4375 → 1.5938 mm). No Richardson
  extrapolation is defensible (quantised endpoint,
  non-monotone case). Treat the finest-grid value as
  best-available with a discretisation uncertainty of
  **at least the last-step change** — i.e. several
  percentage points, ~8 pp for the grade-3 case. The
  coarse grid errs in both directions (it understates
  reduction at 0.25 mm distance, 22.2% vs 35.9% fine,
  and overstates it at 0.5 mm, 46.2% vs 41.5% fine).
- **Charge and battery ratios are near-converged for
  grade 0** (last-step |ΔQ| = 0.003–0.005) **but not
  for the sheathed cases** (grade 2: ΔQ = +0.040 on each
  refinement, still drifting up; grade 3: +0.049 last
  step). Quote sheathed-case Q ratios to at most one
  decimal with the drift stated.
- **The direction is grid-robust in all 15 case-grids:**
  tripolar narrower than monopolar (reduction range
  across the finest grid: 35.9–45.1% in these five
  cases), Q ratio 1.35–2.02, battery proxy 2.57–3.83.
  That — and only that — survives refinement, which is
  the same downgrade sceptic S4b imposed, now with
  numbers.

**Relation to the sceptic's probe.** Sceptic S4b
reported grade-0/0.5 mm at dx = 0.0625 (v1 code) as
mono 1.44 / tri 0.94 mm, reduction 34.8%, Q 1.43. V2 at
the same dx gives 1.6875 / 0.9375, 44.4%, Q 1.586. The
tripolar width agrees (0.94); the monopolar width and
Q do not, because the v1 probe necessarily ran with
v1's row-count geometry: at dy = 0.0625 the electrode
sat at y = 3 × 0.0625 = 0.1875 mm with a 0.125 mm wall,
instead of the physical 0.375 / 0.25 mm that v2.3 holds
fixed. The sceptic's conclusion (v1 numbers are
grid-dependent, direction only) is confirmed by the
cleaner series above; the probe's specific 34.8% is
superseded by the fixed-geometry series, not
contradicted in kind.

**Quoting rule going forward.** Any A1-model width or
percentage must carry its dx (and "contiguous, 50% of
peak"). Round-1 §4's "22–47%" is a dx = 0.125 mm
statement. On the finest grid run here the five checked
cases give 36–45%, with per-case discretisation
uncertainty up to ~8 pp; the remaining seven sweep
cases have no fine-grid value at all. A kill decision
stated in absolute mm (whatever threshold a future
freeze chooses) would need a convergence criterion
stated *before* the run (e.g. last-step width change
below a holder-set fraction of that threshold), which
does not exist yet.

## 5. Rerun sweep and reproducibility

Executed this session (Python 3.14.8, stdlib only;
`numpy` still absent in this runtime):

```
$ cd research/gaps/a1_model
$ python3 test_model.py -v        # Ran 10 tests in 2.026s — OK
$ python3 run_sweep.py            # writes results_v2.csv (12 rows)
$ python3 run_sweep.py            # second run: stdout identical
$ md5 results.csv                 # 30cd31cecc5759e41e9f94f009c0c39a (v1, untouched)
$ md5 results_v2.csv              # b9ec23c5ede0ceba47f538caafe9becb (both runs)
$ python3 run_convergence.py      # writes convergence.csv (15 rows)
$ md5 convergence.csv             # 3d0fee5912eed5d75b523d71a728d5c9
```

(Caveat: `convergence.csv` contains a wall-seconds
column, so its md5 is run-specific; all physics columns
are deterministic — the solver has no RNG; `SEED =
20261102` remains provenance decoration, as sceptic S4
established.)

Checks run on the outputs (scripted, this session):

- **v2 at dx = 0.125 ≡ v1:** max |v1 − v2| over the
  shared numeric columns (widths, reduction %, Q ratio,
  battery proxy, all 12 rows) = **0** exactly. The v2
  fixes therefore do not perturb any round-1 §4 number
  *at its own grid* — the §4 downgrade comes from
  refinement (§4 above), not from the code fixes.
- **Contiguous = global** in all 12 `results_v2.csv`
  rows and all 15 `convergence.csv` rows (both modes).
  The v1 span bug was benign for everything this model
  has produced so far; it is now impossible to hit
  silently because both definitions are reported.
- **Solver:** all 24 sweep solves and all 30
  convergence solves converged (rel. residual
  7.1e-10–9.9e-10 < tol 1e-9). Sceptic S4c's "unproven,
  not checked" non-convergence concern is retired for
  these runs.
- Sensitivities at grade 2 / 0.5 mm reproduce round-1
  §4 exactly (σ_f 0.5 → 30.8%/1.24×; σ_f 1.0 →
  46.2%/1.64×; threshold 30% → 52.6%, 70% → 28.6%;
  spacing 0.7 → Q 1.90×, 1.5 → 30.8%; perilymph 1.43 →
  Q 1.56×; L = 28 mm octaves only) — as they must,
  given the row check above. All remain
  dx = 0.125 mm numbers under the §4 quoting rule.
- One round-1 sensitivity wording needs care rather
  than correction: "spacing 0.7 mm" snaps to
  0.75 mm on the 0.125 grid (round(0.7/0.125) = 6
  cells); unchanged from v1, flagged here so nobody
  quotes 0.7 as exact on a coarse grid.

The grade-3 / 0.25 mm zero-reduction row (0.375 mm
both arms) is unchanged in v2 and is **not** cleared
by the convergence series (that case was not in the
five; SGN line inside the 0.375 mm sheath on a
0.125 mm grid). It remains "treat as grid artefact,
not evidence" (round-1 §4), now additionally
unresolved at any finer grid.

## 6. Verdict — still UNEVALUABLE

**GEN1-A1 is neither KILLED nor kill-cleared by this
round.** No gate cell changes (cf. round1-summary §3:
A1 model output is T0 and cannot move GEN1-A1 G1/G6 in
any case). Explicitly **not upgraded**: nothing here
may be quoted as "A1 survived", "Shannon-safe", or a
grid-converged narrowing percentage.

Missing inputs, cumulative (round-1 §6 items 1–6 stand
verbatim; sceptic additions updated by this round):

1. Named array + manufacturer per-contact max charge
   density + contact areas, human-extracted — MISSING.
2. Pre-stated safety-margin divisor — MISSING.
3. Battery floor (named device) — MISSING.
4. Growing geometry (ages/dimensions) — MISSING.
5. Seyyedi–Nadol per-grade rubric → physical map —
   MISSING (grade map here still ASSUMED).
6. Freeze/blinding: commit code + thresholds before
   outputs, human-frozen — NOT DONE (this round, like
   round 1, is exploratory; at writing `git status`
   shows the v2 edits as uncommitted modifications and
   new outputs as untracked — no freeze commit).
7. Shannon unit basis from the primary text — pin
   attempted (§2), **not achieved**: inspected print
   contains both conventions; a licensed/human read of
   Shannon 1992 *IEEE TBME* 39:424–6 is owed. Until
   then only the bracket in §2.5 may be quoted, and
   Shannon remains a refused proxy for the filed limit
   regardless of which convention wins.
8. dx/dy convergence — series now filed (§4) with the
   outcome **not converged for width magnitudes**;
   a pre-stated convergence criterion tied to the kill
   threshold, plus fine-grid runs of all 12 cases
   (and the grade-3/0.25 mm artefact case), are owed
   before any absolute-mm comparison is load-bearing.

What this round legitimately retires: the
code-vs-documentation mismatch in `excitation_width`,
the silent-CG concern for these runs, and the
ambiguity about *which* Shannon convention v1 used
(it was the classic µC one; the problem was citing
Li's nC-printed §2.2 for it). What it does not retire:
every documentary input above, the full-length-sheath
geometry (S4c(ii), unchanged), and any use of §4
round-1 percentages without a dx.

## 7. Files and reproduce

Changed/added, all under `research/gaps/` (no frozen,
scored, or round-1 file edited; `a1_model/results.csv`
byte-identical):

- `round2-A1-fix.md` (this file)
- `a1_model/model.py` (v2, version log in header)
- `a1_model/test_model.py` (10 tests)
- `a1_model/run_sweep.py` (writes `results_v2.csv`)
- `a1_model/run_convergence.py` (new)
- `a1_model/results_v2.csv`, `a1_model/convergence.csv` (new)

```
cd research/gaps/a1_model
python3 test_model.py -v       # 10 tests
python3 run_sweep.py           # §5 table + bracket -> results_v2.csv
python3 run_convergence.py     # §4 series -> convergence.csv (~3 min)
```

External records inspected in full this round:
Li 2024 PMC11641559 (Europe PMC fullTextXML);
Liu 2024 *JNE* 21:036034, PMID 38776894 (IOP publisher
PDF via `web_fetch`, `pypdf` 6.21.3 from local cache);
Cogan 2016 PMC5386002 (NCBI efetch full XML);
Shannon 1992 PMID 1592409 (MEDLINE abstract; IEEE
primary not accessible by this route). Search results
were used only to locate the Liu/Cogan records.

*Unresolved: §6 items 1–8. Verdict UNEVALUABLE —
unchanged, not upgraded. C0 untested; Step 5
no-winner stands.*
