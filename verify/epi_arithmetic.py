"""Appendix D epidemiology arithmetic D1-D4 (range inputs, locked).

Model routing (GOAL S9): requested Sol 6.1 (high; code deterministic);
actual runtime model `muse-wonder-full-1.0` fallback (Sol 6.1 unavailable
in this runtime), same effort split. Substitution disclosed per S9 rule 3.
No claim in this file is Sol 6.1 work.

Date: 2026-11-02. Status: pre-registration artefact committed BEFORE
Step 3 scoring (GOAL S11 Step 2). No Step 3 result informed this code.

Exploratory-after-seen label: YES. Evidence seen before writing this
code, exactly: GOAL.md v2.2 S4, S5, S7, S8, S10 and Appendices A-C
(Appendix D formulas via S3/S11 context);
research/frozen_baseline/frozen_bilateral_eCI_v1.md S2 (the D1-D4
arithmetic locked here, transcribed verbatim in docstrings);
research/frozen_baseline/Step1-pin-summary.md and AppendixA-v1.md;
research/step0/Step0-verified-bibliography.md S2 (E-rows: denominators
never pooled) and S4. NOT seen: any Gen 0 extraction CSV or Step 3 output.

G3b note (applies to every candidate scored with these denominators):
G3b BLOCKED => all G3b cells INSUFFICIENT; no promotion possible at v1.
Coverage arithmetic here can never by itself promote a candidate.

Range convention: a range is a (low, high) tuple with low <= high.
None means UNPINNABLE (frozen S2): it propagates as None and is never
replaced by a point estimate, a Fortnum-style substitute, or a pooled
cohort value. No epidemiology number is hard-coded in this module.
Pure stdlib, deterministic.
"""

from __future__ import annotations

Range = tuple[float, float]


def _check(r: Range, name: str, *, positive: bool = False) -> Range:
    low, high = r
    if low > high:
        raise ValueError(f"{name}: low {low} > high {high}")
    if positive and low <= 0:
        raise ValueError(f"{name}: denominator range must be > 0, got {r}")
    if low < 0:
        raise ValueError(f"{name}: counts/fractions must be >= 0, got {r}")
    return r


def add_ranges(a: Range | None, b: Range | None) -> Range | None:
    if a is None or b is None:
        return None
    _check(a, "a"); _check(b, "b")
    return (a[0] + b[0], a[1] + b[1])


def mul_ranges(a: Range | None, b: Range | None) -> Range | None:
    if a is None or b is None:
        return None
    _check(a, "a"); _check(b, "b")
    products = (a[0] * b[0], a[0] * b[1], a[1] * b[0], a[1] * b[1])
    return (min(products), max(products))


def div_ranges(a: Range | None, b: Range | None) -> Range | None:
    if a is None or b is None:
        return None
    _check(a, "numerator"); _check(b, "denominator", positive=True)
    return (a[0] / b[1], a[1] / b[0])


# --- D1 (frozen S2): N_P0 = N_bilateral_severe + N_bilateral_profound;
# Incidence_P0 = N_P0 / N_screened_births_HSFS; Incidence_1000 = 1000x.
# HSFS severe band is 71-90 / profound 91+ (see >=70 vs >=71 note there);
# this code adds whatever SNHL rows the human extractor supplies.

def d1_n_p0(n_bilateral_severe: Range | None,
            n_bilateral_profound: Range | None) -> Range | None:
    """D1 numerator range. None (UNPINNABLE) if either band is missing."""
    return add_ranges(n_bilateral_severe, n_bilateral_profound)


def d1_incidence(n_p0: Range | None,
                 n_screened_births: Range | None) -> Range | None:
    """Incidence per birth. Denominator must be the HSFS screened-births
    count from the same table, never an external births total."""
    return div_ranges(n_p0, n_screened_births)


def d1_incidence_per_1000(n_p0: Range | None,
                          n_screened_births: Range | None) -> Range | None:
    inc = d1_incidence(n_p0, n_screened_births)
    return None if inc is None else (1000.0 * inc[0], 1000.0 * inc[1])


# --- D2 (frozen S2): f_e = N_e / N_denominator(e) [denominator named per
# row]; Range_e = [min, max] over eligible cohorts (never a pooled point);
# N_e(P0) = f_e_range x N_P0 only if f_e's denominator is P0-like,
# otherwise blank. Overlap rule: sum_e f_e need not = 1.

def d2_fraction(n_e: float | None, n_denominator: float | None) -> float | None:
    if n_e is None or n_denominator is None:
        return None
    if n_denominator <= 0:
        raise ValueError("denominator must be > 0")
    if n_e < 0 or n_e > n_denominator:
        raise ValueError(f"N_e {n_e} outside [0, denominator {n_denominator}]")
    return n_e / n_denominator


def d2_fraction_range(cohort_fractions: list[float]) -> Range | None:
    """[min, max] over eligible cohorts; empty list = UNPINNABLE (None).
    Never pools cohorts into one point estimate."""
    if not cohort_fractions:
        return None
    for f in cohort_fractions:
        if not 0.0 <= f <= 1.0:
            raise ValueError(f"fraction {f} outside [0, 1]")
    return (min(cohort_fractions), max(cohort_fractions))


def d2_n_e_p0(f_e_range: Range | None, n_p0: Range | None,
              *, denominator_p0_like: bool) -> Range | None:
    """N_e(P0) = f_e_range x N_P0 ONLY if the fraction's denominator is
    P0-like; otherwise blank (None), however good the cohort looks."""
    if not denominator_p0_like:
        return None
    return mul_ranges(f_e_range, n_p0)


def d2_fraction_sum(f_e_ranges: list[Range]) -> Range | None:
    """Sum of etiologic fraction ranges, reported as-is. The D2 overlap
    rule says this need NOT equal 1 (categories overlap); this function
    deliberately never normalizes or asserts a partition."""
    total: Range | None = (0.0, 0.0)
    for r in f_e_ranges:
        total = add_ranges(total, r)
    return total


# --- D3 (frozen S2): anatomic/phenotype fractions over one common P0-like
# denominator; normal anatomy is the remainder only once the other rows
# exist on that same denominator and are mutually exclusive.

def d3_fraction(n_phenotype: float | None,
                n_denominator: float | None) -> float | None:
    return d2_fraction(n_phenotype, n_denominator)


def d3_normal_anatomy_remainder(
        phenotype_ranges: list[Range | None]) -> Range | None:
    """1 - sum(phenotype fractions) as a range: (1 - sum highs,
    1 - sum lows). Valid ONLY for mutually exclusive rows on a common
    denominator (frozen S2); caller must guarantee that. Any missing
    row makes the remainder UNPINNABLE (None)."""
    if any(r is None for r in phenotype_ranges):
        return None
    ranges = [r for r in phenotype_ranges if r is not None]
    for r in ranges:
        _check(r, "phenotype fraction")
        if r[1] > 1.0:
            raise ValueError(f"fraction range {r} exceeds 1")
    lo = 1.0 - sum(r[1] for r in ranges)
    hi = 1.0 - sum(r[0] for r in ranges)
    if lo < 0.0:
        raise ValueError("phenotype fraction highs sum above 1; rows cannot "
                         "all be mutually exclusive on one denominator")
    return (lo, hi)


# --- D4 (frozen S2): Eligible_F = sum over strata s in F's eligibility
# set of N_s(P0); Coverage_F = Eligible_F / N_P0; PortfolioUnion = size
# of the stratum-level union (double-counted strata counted once -
# inclusion-exclusion at the stratum table, never a sum of coverages).

def _sum_strata(stratum_counts: dict[str, Range | None],
                strata: set[str]) -> Range | None:
    total: Range | None = (0.0, 0.0)
    for s in sorted(strata):
        if s not in stratum_counts:
            raise KeyError(f"stratum {s!r} not in stratum_counts")
        total = add_ranges(total, stratum_counts[s])
        if total is None:
            return None
    return total


def d4_eligible(stratum_counts: dict[str, Range | None],
                eligibility_set: set[str]) -> Range | None:
    """Eligible_F. A stratum with UNPINNABLE count (None) in the set
    makes the whole numerator None - never silently dropped."""
    return _sum_strata(stratum_counts, set(eligibility_set))


def d4_coverage(eligible: Range | None, n_p0: Range | None) -> Range | None:
    return div_ranges(eligible, n_p0)


def d4_portfolio_union(stratum_counts: dict[str, Range | None],
                       eligibility_sets: list[set[str]]) -> Range | None:
    """PortfolioUnion: each stratum counted once across families."""
    union: set[str] = set()
    for s in eligibility_sets:
        union |= set(s)
    return _sum_strata(stratum_counts, union)


def d4_portfolio_coverage(stratum_counts: dict[str, Range | None],
                          eligibility_sets: list[set[str]],
                          n_p0: Range | None) -> Range | None:
    return d4_coverage(d4_portfolio_union(stratum_counts, eligibility_sets), n_p0)

