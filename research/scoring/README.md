# Scoring: gate_table.py (+ verify/epi_arithmetic.py)

> **Model routing (GOAL §9):** requested **Sol 6.1**, high (code
> deterministic); actual runtime model **`muse-wonder-full-1.0`
> fallback** (Sol 6.1 unavailable in this runtime), same effort
> split. Substitution disclosed per §9 rule 3. No claim here is
> Sol 6.1 work.
> **Date:** 2026-11-02. **Pre-registration:** this code is committed
> **BEFORE Step 3 scoring** (GOAL §11 Step 2); no Step 3 result
> informed it.
> **Exploratory-after-seen: YES.** Seen before writing, exactly:
> GOAL.md v2.2 §4, §5, §7, §8, §10 + Appendices A–C;
> `research/frozen_baseline/Step1-pin-summary.md` + `AppendixA-v1.md`;
> `research/frozen_baseline/frozen_bilateral_eCI_v1.md` §2 (D1–D4);
> `research/step0/Step0-verified-bibliography.md` §2 + §4.
> NOT seen: any Gen 0 candidate extraction CSV, any Step 3 output.
> **G3b BLOCKED ⇒ all G3b cells INSUFFICIENT; no promotion possible
> at v1** (GOAL §4.2). This is stated for every candidate in every
> table `gate_table.py` emits — including the demo below.
> No citations or epidemiology numbers are invented in this package:
> demo fixtures are synthetic and labelled as such.

## Environment (pinned)

```text
$ python3 --version
Python 3.14.8
$ python3 -m pytest --version
/Users/bmarti44/.local/bin/python3: No module named pytest
```

pytest is absent, so tests use stdlib `unittest` (runnable under
pytest unchanged). Pure stdlib only; no randomness, no clock.

## Files

| File | Role |
|---|---|
| `gate_table.py` | Gate matrix + fitness ranking (this spec) |
| `test_gate_table.py` | 15 unittest cases (see Coverage) |
| `demo_extraction.csv`, `demo_fmea.csv` | SYNTHETIC fixtures (invented verdicts; not candidates) |
| `demo_matrix.md` | Exact CLI output on the demo fixtures |
| `../../verify/epi_arithmetic.py` | Appendix D D1–D4 range arithmetic |
| `../../verify/test_epi_arithmetic.py` | 13 unittest cases for D1–D4 |

## Extraction CSV schema (`extraction-csv-v1`)

One row per candidate × gate × window × stratum extraction cell.
Comment lines starting with `#` (schema-version / provenance header)
are skipped. Columns, in order:

| Column | Values |
|---|---|
| `candidate` | Candidate ID (Appendix B); one track per candidate |
| `track` | `P` or `R` (`Track P`/`Track R` also accepted) |
| `gate` | `G1`, `G2`, `G3a`, `G3b`, `G4`, `G5`, `G6` |
| `window` | `W0`, `W1`, `W2`, `W3`, … (free text, carried, not ordered) |
| `stratum` | §3.2 stratum label (free text) |
| `tier` | Evidence tier T0–T4 (§5.3; carried for audit) |
| `grade` | GRADE label (§5.2; carried for audit) |
| `delta_g2_db` | G2 SRT gain vs frozen, dB (empty/`NA` = unreported) |
| `delta_g3a_sd` | G3a gain vs frozen, SD within stratum |
| `g1_channels` | Effective channels on the G1 anchor task |
| `burden_rank` | G6 burden rank; **lower is less burden** |
| `verdict` | `PASS` / `FAIL` / `INSUFFICIENT` / `NA` only |

Rules enforced by the loader: missing required column, unknown
gate/track/verdict, or non-numeric numeric field ⇒ exit 2 with the
line number. A candidate declaring two tracks ⇒ error. `tier` and
`grade` travel with the row for human audit; the deterministic
scorer never upgrades a verdict from them (PASS-requires-≥Moderate
is a judge-side rule, §5.2, applied before extraction).

Candidate-level numerics for ranking: `delta_g2_db` = max over the
candidate's G2 rows (any row if no G2 row carries it);
`delta_g3a_sd` likewise over G3a rows; `g1_channels` likewise over
G1 rows; `burden_rank` = min over rows. Extractors should put each
value on its own gate's primary-window row; repeats must agree by
convention (max/min only picks one deterministically).

### Optional FMEA CSV (`--fmea`, Track R G5 aggregate)

Columns: `candidate,harm,severity,probability_band`. Severity is
Appendix C 1–4. Probability bands (App. C): `<0.1%`, `0.1-1%`,
`1-5%`, `>5%` (`%` may be omitted). **G5 aggregate = Σ over harms
with severity ≥ 3 of weight {`<0.1%`:1, `0.1-1%`:2, `1-5%`:3,
`>5%`:4}**; lower is better. No FMEA rows ⇒ `NA`, ranked last on
that key — never imputed as 0.

## What the code emits

CLI: `python3 gate_table.py input.csv --out matrix.md [--fmea f.csv]`
(without `--out`, Markdown goes to stdout).

- **(a) Gate matrix** candidate × gate. Each cell = worst
  *applicable* window/stratum verdict (`FAIL` < `INSUFFICIENT` <
  `PASS`); `NA` rows are non-applicable and ignored; all-`NA` ⇒
  `NA`; a gate with **no rows ⇒ `INSUFFICIENT`** (missing evidence
  is never judge-imputed, §4.2). **G3b is forced `INSUFFICIENT`
  for every candidate regardless of input** (BLOCKED flag), with
  the note "G3b BLOCKED ⇒ INSUFFICIENT; no promotion possible at
  v1" on every candidate row.
- **(b) Track P lexicographic ranking** (GOAL §7), ascending key:
  1. G4/G5 `FAIL` demoted last (veto), then fewest `FAIL`s;
  2. fewest `INSUFFICIENT` among applicable gates (forced G3b
  counts once for everyone at v1 — disclosed bias toward studied
  incumbents, §7); 3. largest G2; 4. largest G3a; 5. G3b verdict
  (constant at v1); 6. largest G1 (**`NA`/missing last**);
  7. lowest burden. Candidate name is a final reproducibility
  tie-break only, not a GOAL rule. Missing numerics rank last.
- **(c) Track R ranking:** largest G1 (NA/missing last), then
  smallest G5 aggregate (missing FMEA last), then name.
- **(d) Promotion (GOAL §4.2):** Track P *device* = `PASS` on
  G1, G2, G3a, G3b, G4, G5, G6; Track P *pathway* (`G1 = NA`
  disclosed — the only G1-NA route §4.2 allows, families F/G/H) =
  `PASS` on G2–G6. Track R is never promoted (watch-list,
  §4.1/§10). Because G3b is forced INSUFFICIENT, **every v1
  result is `FALSE`**; the blocking gates are listed per candidate.
- **(e) Pareto set:** non-dominated candidates *within each track*
  over (−FAILs, −INSUFFICIENT, G2, G3a, G1, −burden, −G5-agg),
  missing = worst. Transparency only; ranking/promotion use
  (b)/(d) (GOAL §7).

## verify/epi_arithmetic.py (Appendix D, D1–D4)

Range inputs are `(low, high)` tuples; `None` = UNPINNABLE and
propagates (never a point estimate). Formulas transcribed from
`frozen_bilateral_eCI_v1.md` §2: **D1** `N_P0 = severe + profound`,
incidence per birth / per 1000 over HSFS screened births; **D2**
`f_e = N_e / N_denominator(e)`, range = [min, max] over cohorts
(never pooled), `N_e(P0) = f_e × N_P0` **only if**
`denominator_p0_like=True`, overlap sum reported un-normalized;
**D3** phenotype fractions + normal-anatomy remainder (mutually
exclusive rows, one denominator, missing row ⇒ `None`); **D4**
`Eligible_F` = Σ stratum counts, `Coverage = Eligible / N_P0`,
portfolio union counts shared strata once (never a sum of
coverages). Synthetic demo run (fixture numbers, not data):

```text
D1 demo(synthetic): N_P0= (30.0, 37.0) per1000= (0.3, 0.37)
D2 non-P0-like -> None
D4 union cov -> (0.35, 0.4)
```

## Coverage (tests)

`test_gate_table.py`: worst-window + missing-gate matrix; forced
G3b INSUFFICIENT (P and R); INSUFFICIENT counting excludes NA;
lexicographic order (FAILs → INSUFFICIENT → G2; G3a → burden);
G4 **and** G5 veto demotion past a 2-FAIL non-veto candidate;
G1-NA-last; promotion FALSE when G3b INSUFFICIENT, plus isolated
§4.2 logic (device / pathway / Track R); G5 aggregate severity
floor + band weights; Track R G1→G5-agg; Pareto domination; CSV
loading + bad-verdict rejection.
`test_epi_arithmetic.py`: D1 ranges + None + zero-denominator; D2
no-pooling, P0-like gate, overlap sum > 1 un-normalized; D3
remainder + missing-row None + overlap rejection; D4 eligible /
coverage / union-once / None-poisoning / unknown-stratum error.

## Test run (exact output, 2026-11-02)

```text
$ cd research/scoring && python3 -m unittest test_gate_table -v
...
----------------------------------------------------------------------
Ran 15 tests in 0.003s

OK
$ cd verify && python3 -m unittest test_epi_arithmetic -v
...
----------------------------------------------------------------------
Ran 13 tests in 0.000s

OK
```

## Demo run (exact output)

Command (from `research/scoring/`):

```text
python3 gate_table.py demo_extraction.csv --fmea demo_fmea.csv --out demo_matrix.md
```

`demo_matrix.md` contents, verbatim (also committed as that file):

<!-- DEMO-OUTPUT-START -->
```markdown
# Gate matrix + fitness ranking (deterministic, gate_table.py)

> Model routing (GOAL S9): requested **Sol 6.1** (high; code
> deterministic); actual **`muse-wonder-full-1.0` fallback**, same
> effort split. Date: **2026-11-02**. Pre-registration: generated by
> code committed **BEFORE Step 3 scoring**.
> Exploratory-after-seen: **YES** - GOAL.md v2.2 S4/S5/S7/S8/S10 +
> Appendices A-C, Step1-pin-summary.md, AppendixA-v1.md,
> frozen_bilateral_eCI_v1.md S2, and Step0-verified-bibliography.md
> S2/S4 were seen before this code was written. No Gen 0 extraction
> CSV or Step 3 output was seen.
> **G3b BLOCKED => every G3b cell INSUFFICIENT; no promotion is
> possible at v1** (GOAL S4.2). INSUFFICIENT is never imputed.

## (a) Gate matrix (candidate x gate, worst applicable window)

| candidate | track | G1 | G2 | G3a | G3b | G4 | G5 | G6 | G3b/promotion note |
|---|---|---|---|---|---|---|---|---|---|
| DEMO-P-DEVICE | P | PASS | PASS | PASS | INSUFFICIENT | PASS | PASS | PASS | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-PATHWAY | P | NA | PASS | PASS | INSUFFICIENT | PASS | PASS | PASS | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-VETO | P | PASS | PASS | PASS | INSUFFICIENT | FAIL | PASS | PASS | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-A | R | PASS | FAIL | INSUFFICIENT | INSUFFICIENT | FAIL | INSUFFICIENT | FAIL | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-B | R | PASS | PASS | INSUFFICIENT | INSUFFICIENT | FAIL | INSUFFICIENT | FAIL | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |

## (b) Track P lexicographic ranking (GOAL S7)

| rank | candidate | veto(G4/G5 FAIL) | FAILs | INSUFFICIENT | delta_g2_db | delta_g3a_sd | G3b | g1_channels | burden_rank | note |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | DEMO-P-DEVICE | - | 0 | 1 | 4.5 | 0.5 | INSUFFICIENT | 14 | 2 | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| 2 | DEMO-P-PATHWAY | - | 0 | 1 | 4.5 | 0.5 | INSUFFICIENT | NA | 1 | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| 3 | DEMO-P-VETO | DEMOTED | 1 | 1 | 9 | 0.9 | INSUFFICIENT | 20 | 1 | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |

## (c) Track R ranking (G1, then G5 aggregate)

G5 aggregate = sum over FMEA harms with severity >= 3 of probability-band weight {<0.1%:1, 0.1-1%:2, 1-5%:3, >5%:4} (--fmea input; NA = no FMEA rows, ranked last on this key).

| rank | candidate | g1_channels | g5_aggregate | note |
|---|---|---|---|---|
| 1 | DEMO-R-B | 24 | 1 | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| 2 | DEMO-R-A | 24 | 4 | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |

## (d) Promotion check (GOAL S4.2)

| candidate | track | promoted | reason |
|---|---|---|---|
| DEMO-P-DEVICE | P | FALSE | device: not PASS on G3b; G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-PATHWAY | P | FALSE | pathway (G1 NA disclosed): not PASS on G3b; G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-VETO | P | FALSE | device: not PASS on G3b,G4; G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-A | R | FALSE | Track R watch-list, never promoted for infants; G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-B | R | FALSE | Track R watch-list, never promoted for infants; G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |

## (e) Pareto set (non-dominated, within track; transparency only)

| candidate | track | note |
|---|---|---|
| DEMO-P-DEVICE | P | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-PATHWAY | P | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-P-VETO | P | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-A | R | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |
| DEMO-R-B | R | G3b BLOCKED => INSUFFICIENT; no promotion possible at v1 |

Ranking/promotion use the lexicographic rule (b)/(d), not the Pareto set (GOAL S7). Missing numeric inputs rank last on their key and are shown as NA; they are never imputed.
```
<!-- DEMO-OUTPUT-END -->

Reading the demo: `DEMO-P-DEVICE` outranks `DEMO-P-PATHWAY`
only at key 6 (G1 NA-last) despite the pathway's lower burden;
`DEMO-P-VETO` is demoted last despite the largest G2/G3a/G1
(a G4 FAIL is a Track P veto); `DEMO-R-A`'s W2 FAIL makes its
G2 cell FAIL (worst window); Track R ties on G1 = 24 break on
G5 aggregate (1 < 4); every candidate's promotion is FALSE
because G3b is BLOCKED. Without `--fmea`, both Track R rows show
`g5_aggregate = NA` and order by name after G1.

