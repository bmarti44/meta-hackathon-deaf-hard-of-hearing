"""Tests for epi_arithmetic.py D1-D4 (unittest; pytest absent here).

Model routing (GOAL S9): requested Sol 6.1 (high; code deterministic);
actual runtime model `muse-wonder-full-1.0` fallback, same effort split.
Date: 2026-11-02. Pre-registration BEFORE Step 3 scoring.
Exploratory-after-seen: YES - GOAL.md v2.2 S4/S5/S7/S8/S10 + Appendices
A-C, frozen_bilateral_eCI_v1.md S2 (D1-D4 formulas), Step1-pin-summary.md,
AppendixA-v1.md, Step0-verified-bibliography.md S2/S4 were seen. No
Gen 0 extraction CSV or Step 3 output was seen. G3b BLOCKED => all G3b
cells INSUFFICIENT; no promotion possible at v1 - coverage numbers from
these functions never promote any candidate. Fixture numbers below are
synthetic arithmetic inputs, not epidemiology values.

Run: python3 -m unittest test_epi_arithmetic -v   (from verify/)
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from epi_arithmetic import (  # noqa: E402
    d1_incidence, d1_incidence_per_1000, d1_n_p0, d2_fraction,
    d2_fraction_range, d2_fraction_sum, d2_n_e_p0,
    d3_normal_anatomy_remainder, d4_coverage, d4_eligible,
    d4_portfolio_coverage, d4_portfolio_union,
)


class TestD1(unittest.TestCase):
    def test_n_p0_and_incidence_ranges(self):
        self.assertEqual(d1_n_p0((10.0, 12.0), (20.0, 25.0)), (30.0, 37.0))
        inc = d1_incidence((30.0, 37.0), (1000.0, 1000.0))
        self.assertEqual(inc, (0.03, 0.037))
        self.assertEqual(d1_incidence_per_1000((30.0, 37.0), (1000.0, 1000.0)),
                         (30.0, 37.0))

    def test_unpinnable_propagates(self):
        self.assertIsNone(d1_n_p0(None, (1.0, 2.0)))
        self.assertIsNone(d1_incidence((30.0, 37.0), None))

    def test_zero_denominator_rejected(self):
        with self.assertRaises(ValueError):
            d1_incidence((1.0, 1.0), (0.0, 10.0))


class TestD2(unittest.TestCase):
    def test_fraction_and_range_never_pooled(self):
        self.assertEqual(d2_fraction(14.0, 100.0), 0.14)
        self.assertEqual(d2_fraction_range([0.14, 0.21]), (0.14, 0.21))
        self.assertIsNone(d2_fraction_range([]))

    def test_n_e_p0_only_when_denominator_p0_like(self):
        self.assertIsNone(d2_n_e_p0((0.1, 0.2), (100.0, 100.0),
                                    denominator_p0_like=False))
        self.assertEqual(d2_n_e_p0((0.1, 0.2), (100.0, 200.0),
                                   denominator_p0_like=True), (10.0, 40.0))

    def test_overlap_sum_need_not_equal_one(self):
        total = d2_fraction_sum([(0.4, 0.5), (0.4, 0.5), (0.2, 0.3)])
        self.assertEqual(total, (1.0, 1.3))  # reported, not normalized


class TestD3(unittest.TestCase):
    def test_remainder_range(self):
        self.assertEqual(d3_normal_anatomy_remainder([(0.1, 0.2), (0.05, 0.1)]),
                         (0.7, 0.85))

    def test_missing_row_makes_remainder_unpinnable(self):
        self.assertIsNone(d3_normal_anatomy_remainder([(0.1, 0.2), None]))

    def test_overlapping_highs_rejected(self):
        with self.assertRaises(ValueError):
            d3_normal_anatomy_remainder([(0.6, 0.7), (0.3, 0.4)])


class TestD4(unittest.TestCase):
    COUNTS = {"s1": (10.0, 12.0), "s2": (20.0, 20.0), "s3": (5.0, 8.0)}

    def test_eligible_and_coverage(self):
        self.assertEqual(d4_eligible(self.COUNTS, {"s1", "s3"}), (15.0, 20.0))
        self.assertEqual(d4_coverage((15.0, 20.0), (100.0, 100.0)), (0.15, 0.2))

    def test_portfolio_union_counts_shared_stratum_once(self):
        union = d4_portfolio_union(self.COUNTS, [{"s1", "s2"}, {"s2", "s3"}])
        self.assertEqual(union, (35.0, 40.0))  # not a sum of coverages
        cov = d4_portfolio_coverage(self.COUNTS, [{"s1", "s2"}, {"s2", "s3"}],
                                    (100.0, 100.0))
        self.assertEqual(cov, (0.35, 0.4))

    def test_unpinnable_stratum_poisons_numerator(self):
        counts = dict(self.COUNTS, s2=None)
        self.assertIsNone(d4_eligible(counts, {"s1", "s2"}))
        self.assertEqual(d4_eligible(counts, {"s1"}), (10.0, 12.0))

    def test_unknown_stratum_is_an_error_not_a_zero(self):
        with self.assertRaises(KeyError):
            d4_eligible(self.COUNTS, {"nope"})


if __name__ == "__main__":
    unittest.main()
