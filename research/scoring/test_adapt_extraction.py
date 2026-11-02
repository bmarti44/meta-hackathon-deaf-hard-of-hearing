"""Tests for adapt_extraction (Step 2 skeptic F1 fix). Routing header:
requested Sol 6.1 deterministic; actual muse-wonder-full-1.0. 2026-11-02."""
import unittest

from adapt_extraction import adapt


def row(**kw):
    base = {"candidate": "G", "gate": "G3b", "window": "W2", "stratum": "x",
            "tier": "T4", "grade": "UNASSESSED", "effect": "",
            "verdict_proposed": "INSUFFICIENT"}
    base.update(kw)
    return base


class TestAdapt(unittest.TestCase):
    def test_track_and_skip(self):
        out = adapt([row(candidate="C"), row(candidate="FROZEN"), row(candidate="Q0-P")])
        self.assertEqual([(r["candidate"], r["track"]) for r in out], [("C", "R")])

    def test_gate_collapse_and_verdicts(self):
        out = adapt([row(candidate="F", gate="G1-spectral", verdict_proposed="NA-prereg"),
                     row(candidate="A", gate="G4-AAV", verdict_proposed="PROVISIONAL-SIGNAL")])
        self.assertEqual(out[0]["gate"], "G1")
        self.assertEqual(out[0]["verdict"], "NA")
        self.assertEqual(out[1]["gate"], "G4")
        self.assertEqual(out[1]["verdict"], "INSUFFICIENT")

    def test_unknown_verdict_raises(self):
        with self.assertRaises(ValueError):
            adapt([row(verdict_proposed="MAYBE")])


if __name__ == "__main__":
    unittest.main()
