"""Tests for gate_table.py (unittest; pytest is absent in this runtime).

Model routing (GOAL S9): requested Sol 6.1 (high; code deterministic);
actual runtime model `muse-wonder-full-1.0` fallback, same effort split.
Date: 2026-11-02. Pre-registration BEFORE Step 3 scoring.
Exploratory-after-seen: YES - GOAL.md v2.2 S4/S5/S7/S8/S10 + Appendices
A-C, Step1-pin-summary.md, AppendixA-v1.md, frozen_bilateral_eCI_v1.md
S2, Step0-verified-bibliography.md S2/S4 were seen. No Gen 0 extraction
CSV or Step 3 output was seen. G3b BLOCKED => all G3b cells
INSUFFICIENT; no promotion possible at v1 (asserted for every candidate
built here). All verdicts/numbers in this file are synthetic fixtures,
not literature values.

Run: python3 -m unittest test_gate_table -v   (from research/scoring/)
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_table import (  # noqa: E402
    GATES, FmeaHarm, Row, build_gate_matrix, check_promotion, g5_aggregate,
    load_extraction, pareto_set, parse_probability_band, rank_track_p,
    rank_track_r, summarize, worst_verdict,
)


def rows_for(candidate, track="P", verdicts=None, g2=4.0, g3a=0.5,
             g1=12.0, burden=2.0, extra=()):
    verdicts = verdicts or {}
    rows = []
    for gate in GATES:
        v = verdicts.get(gate, "PASS")
        rows.append(Row(candidate, track, gate, "W3", "all", "T4", "Moderate",
                        g2 if gate == "G2" else None,
                        g3a if gate == "G3a" else None,
                        g1 if gate == "G1" else None,
                        burden if gate == "G6" else None, v))
    rows.extend(extra)
    return rows


def summaries_of(all_rows, fmea=None):
    return summarize(all_rows, build_gate_matrix(all_rows), fmea)


class TestMatrixAndInsufficient(unittest.TestCase):
    def test_worst_applicable_window(self):
        self.assertEqual(worst_verdict(["PASS", "FAIL"]), "FAIL")
        self.assertEqual(worst_verdict(["PASS", "INSUFFICIENT"]), "INSUFFICIENT")
        self.assertEqual(worst_verdict(["PASS", "NA"]), "PASS")
        self.assertEqual(worst_verdict(["NA", "NA"]), "NA")
        self.assertEqual(worst_verdict([]), "INSUFFICIENT")

    def test_matrix_worst_window_and_missing_gate(self):
        extra = [Row("X", "P", "G2", "W2", "all", "T4", "Moderate",
                     1.0, None, None, None, "FAIL")]
        rows = [r for r in rows_for("X", extra=extra) if r.gate != "G6"]
        m = build_gate_matrix(rows)["X"]
        self.assertEqual(m["G2"], "FAIL")
        self.assertEqual(m["G6"], "INSUFFICIENT")  # missing, never imputed

    def test_g3b_forced_insufficient_for_every_candidate(self):
        rows = rows_for("X", verdicts={"G3b": "PASS"}) + \
            rows_for("Y", track="R", verdicts={"G3b": "PASS"})
        m = build_gate_matrix(rows)
        self.assertEqual(m["X"]["G3b"], "INSUFFICIENT")
        self.assertEqual(m["Y"]["G3b"], "INSUFFICIENT")

    def test_insufficient_count_excludes_na(self):
        s = summaries_of(rows_for("X", verdicts={"G1": "NA", "G6": "INSUFFICIENT"},
                                  g1=None))[0]
        self.assertEqual(s.n_insufficient, 2)  # forced G3b + G6, not NA G1
        self.assertEqual(s.n_fails, 0)


class TestTrackPLexicographic(unittest.TestCase):
    def test_lexicographic_order_fails_then_insufficient_then_g2(self):
        rows = (rows_for("A", g2=4.0) + rows_for("B", g2=3.0)
                + rows_for("C", verdicts={"G2": "FAIL"}, g2=10.0)
                + rows_for("D", verdicts={"G6": "INSUFFICIENT"}, g2=10.0))
        order = [s.candidate for s in rank_track_p(summaries_of(rows))]
        self.assertEqual(order, ["A", "B", "D", "C"])

    def test_g3a_then_burden_tiebreaks(self):
        rows = (rows_for("A", g3a=0.4, burden=1.0)
                + rows_for("B", g3a=0.6, burden=9.0)
                + rows_for("C", g3a=0.6, burden=3.0))
        order = [s.candidate for s in rank_track_p(summaries_of(rows))]
        self.assertEqual(order, ["C", "B", "A"])  # G3a first, then burden

    def test_veto_fail_demoted_last_despite_fewer_fails(self):
        rows = (rows_for("VETO", verdicts={"G4": "FAIL"}, g2=99.0)
                + rows_for("TWOFAIL", verdicts={"G2": "FAIL", "G6": "FAIL"}))
        order = [s.candidate for s in rank_track_p(summaries_of(rows))]
        self.assertEqual(order, ["TWOFAIL", "VETO"])

    def test_g5_veto_also_demotes(self):
        rows = rows_for("A", verdicts={"G5": "FAIL"}) + rows_for("B")
        order = [s.candidate for s in rank_track_p(summaries_of(rows))]
        self.assertEqual(order, ["B", "A"])

    def test_g1_na_last_among_ties(self):
        rows = (rows_for("PATH", verdicts={"G1": "NA"}, g1=None)
                + rows_for("DEV", g1=12.0))
        order = [s.candidate for s in rank_track_p(summaries_of(rows))]
        self.assertEqual(order, ["DEV", "PATH"])


class TestPromotion(unittest.TestCase):
    def test_promotion_false_when_g3b_insufficient(self):
        s = summaries_of(rows_for("X"))[0]  # all PASS in, G3b forced out
        ok, reason = check_promotion(s.track, s.matrix)
        self.assertFalse(ok)
        self.assertIn("G3b", reason)
        self.assertIn("no promotion possible at v1", reason)

    def test_promotion_logic_isolated_from_v1_block(self):
        all_pass = {g: "PASS" for g in GATES}
        self.assertTrue(check_promotion("P", all_pass)[0])
        pathway = dict(all_pass, G1="NA")
        self.assertTrue(check_promotion("P", pathway)[0])
        self.assertFalse(check_promotion("P", dict(pathway, G3b="INSUFFICIENT"))[0])
        self.assertFalse(check_promotion("R", all_pass)[0])  # watch-list
        self.assertFalse(check_promotion("P", dict(all_pass, G4="FAIL"))[0])


class TestTrackRAndPareto(unittest.TestCase):
    def test_g5_aggregate_severity_floor_and_weights(self):
        harms = [FmeaHarm("R1", "a", 3, parse_probability_band("0.1-1")),
                 FmeaHarm("R1", "b", 4, ">5%"),
                 FmeaHarm("R1", "c", 2, ">5%"),  # severity < 3: excluded
                 FmeaHarm("R1", "d", 3, "<0.1%")]
        self.assertEqual(g5_aggregate(harms), 2 + 4 + 1)

    def test_track_r_g1_then_g5_aggregate(self):
        rows = (rows_for("R1", track="R", g1=20.0)
                + rows_for("R2", track="R", g1=16.0)
                + rows_for("R3", track="R", g1=20.0))
        fmea = {"R1": [FmeaHarm("R1", "a", 3, "1-5%")],
                "R3": [FmeaHarm("R3", "a", 3, "<0.1%")]}
        order = [s.candidate for s in rank_track_r(summaries_of(rows, fmea))]
        self.assertEqual(order, ["R3", "R1", "R2"])

    def test_pareto_excludes_dominated(self):
        rows = (rows_for("STRONG", g2=5.0, g3a=0.6, burden=1.0)
                + rows_for("WEAK", g2=3.0, g3a=0.4, burden=4.0)
                + rows_for("TRADE", g2=5.0, g3a=0.4, burden=0.5))
        names = {s.candidate for s in pareto_set(summaries_of(rows))}
        self.assertEqual(names, {"STRONG", "TRADE"})


class TestCsvLoading(unittest.TestCase):
    HEADER = ("candidate,track,gate,window,stratum,tier,grade,delta_g2_db,"
              "delta_g3a_sd,g1_channels,burden_rank,verdict\n")

    def test_load_and_bad_verdict_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            good = Path(d) / "in.csv"
            good.write_text("# extraction-csv-v1\n" + self.HEADER
                            + "X,P,G2,W3,all,T4,Moderate,4.0,,,,PASS\n")
            self.assertEqual(load_extraction(good)[0].delta_g2_db, 4.0)
            bad = Path(d) / "bad.csv"
            bad.write_text(self.HEADER + "X,P,G2,W3,all,T4,Moderate,,,,,MAYBE\n")
            with self.assertRaises(ValueError):
                load_extraction(bad)


if __name__ == "__main__":
    unittest.main()
