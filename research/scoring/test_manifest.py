"""Tests for the cell manifest (--manifest) in gate_table.py.

Gen 3 bounded attack on Astra review S5 (required-cell completeness).
Requested model: Sol 6.1; actual: muse-wonder-full-1.0. Date: 2026-11-02.
All verdicts/numbers are synthetic fixtures, not literature values.
G3b BLOCKED => forced INSUFFICIENT throughout, as in test_gate_table.py.

Run: python3 -m unittest test_manifest -v   (from research/scoring/)
"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from gate_table import (  # noqa: E402
    GATES, ManifestCell, Row, build_gate_matrix, find_missing_required_cells,
    load_manifest, main, rank_track_p, render_markdown, summarize,
    validate_manifest,
)

EXTRACT_HEADER = ("candidate,track,gate,window,stratum,tier,grade,"
                  "delta_g2_db,delta_g3a_sd,g1_channels,burden_rank,verdict\n")


def row(candidate, gate, verdict, window="W3", track="P", g2=None):
    return Row(candidate, track, gate, window, "all", "T4", "Moderate",
               g2, None, None, None, verdict)


def full_rows(candidate, verdict="INSUFFICIENT", g1="NA", g2val=4.0):
    out = []
    for gate in GATES:
        v = g1 if gate == "G1" else verdict
        out.append(row(candidate, gate, v, g2=g2val if gate == "G2" else None))
    return out


def manifest_for(candidate, required_gates=None, window="*"):
    required_gates = GATES if required_gates is None else required_gates
    return [ManifestCell(candidate, g, window, g in required_gates)
            for g in GATES]


def write_manifest(directory, text):
    p = Path(directory) / "manifest.csv"
    p.write_text(text)
    return p


class TestLoadManifest(unittest.TestCase):
    def test_load_any_window_and_required_variants(self):
        with tempfile.TemporaryDirectory() as d:
            p = write_manifest(d, "candidate,gate,window,required\n"
                                  "X,G2,W3,true\nX,G1,,false\nX,G4,ALL,1\n")
            cells = load_manifest(p)
        self.assertEqual(cells, [ManifestCell("X", "G2", "W3", True),
                                 ManifestCell("X", "G1", "*", False),
                                 ManifestCell("X", "G4", "*", True)])

    def test_load_rejects_missing_column_bad_required_duplicate_bad_gate(self):
        cases = ["candidate,gate,window\nX,G2,W3\n",
                 "candidate,gate,window,required\nX,G2,W3,maybe\n",
                 "candidate,gate,window,required\nX,G2,W3,true\nX,G2,w3,false\n",
                 "candidate,gate,window,required\nX,G9,W3,true\n"]
        for text in cases:
            with tempfile.TemporaryDirectory() as d:
                with self.assertRaises(ValueError, msg=text):
                    load_manifest(write_manifest(d, text))


class TestMissingRequiredCell(unittest.TestCase):
    def test_missing_required_window_caps_pass_gate_at_insufficient(self):
        rows = full_rows("X", verdict="PASS", g1="PASS")
        manifest = manifest_for("X") + [ManifestCell("X", "G6", "W4", True)]
        missing = find_missing_required_cells(rows, manifest)
        self.assertEqual(missing, [ManifestCell("X", "G6", "W4", True)])
        self.assertEqual(build_gate_matrix(rows, manifest)["X"]["G6"],
                         "INSUFFICIENT")
        s = summarize(rows, build_gate_matrix(rows, manifest))[0]
        # forced G3b + manifest-missing G6; without manifest G6 stays PASS
        self.assertEqual(s.n_insufficient, 2)
        self.assertEqual(build_gate_matrix(rows)["X"]["G6"], "PASS")

    def test_na_row_does_not_satisfy_and_optional_cell_not_penalized(self):
        rows = full_rows("X")  # G1 = NA, rest INSUFFICIENT
        required = manifest_for("X")  # G1 required -> NA does not satisfy
        self.assertEqual([c.gate for c in
                          find_missing_required_cells(rows, required)], ["G1"])
        self.assertEqual(build_gate_matrix(rows, required)["X"]["G1"],
                         "INSUFFICIENT")  # was NA without a manifest
        optional = manifest_for("X", required_gates=[g for g in GATES
                                                     if g != "G1"])
        self.assertEqual(find_missing_required_cells(rows, optional), [])
        self.assertEqual(build_gate_matrix(rows, optional)["X"]["G1"], "NA")

    def test_specific_window_satisfied_only_by_that_window(self):
        rows = [row("X", "G2", "PASS", window="W2")]
        cell_w3 = ManifestCell("X", "G2", "W3", True)
        cell_any = ManifestCell("X", "G2", "*", True)
        self.assertEqual(find_missing_required_cells(rows, [cell_w3]),
                         [cell_w3])
        self.assertEqual(find_missing_required_cells(rows, [cell_any]), [])


class TestScopeShrinkagePenalized(unittest.TestCase):
    """Q1/R1 artefact (gen02 adapt note): NA scope shrinkage must no
    longer rank a narrow design ahead of a full-footprint candidate."""

    def _rows(self):
        full = full_rows("FULL")                    # G1 NA, 6x INS
        narrow = [row("QLIKE", g, "INSUFFICIENT" if g == "G4" else "NA")
                  for g in GATES]                   # only G4 (+forced G3b)
        return full + narrow

    def test_without_manifest_shrinkage_wins_with_manifest_it_does_not(self):
        rows = self._rows()
        naive = summarize(rows, build_gate_matrix(rows))
        naive_by = {s.candidate: s for s in naive}
        self.assertEqual(naive_by["QLIKE"].n_insufficient, 2)  # G3b + G4
        self.assertEqual([s.candidate for s in rank_track_p(naive)][0],
                         "QLIKE")  # the spurious lead, reproduced

        req = [g for g in GATES if g != "G1"]
        manifest = manifest_for("FULL", req) + manifest_for("QLIKE", req)
        fixed = summarize(rows, build_gate_matrix(rows, manifest))
        fixed_by = {s.candidate: s for s in fixed}
        # G2/G3a/G5/G6 now explicit INSUFFICIENT: 6, same footprint tax as FULL
        self.assertEqual(fixed_by["QLIKE"].n_insufficient, 6)
        self.assertEqual(fixed_by["FULL"].n_insufficient, 6)
        self.assertEqual([s.candidate for s in rank_track_p(fixed)],
                         ["FULL", "QLIKE"])  # FULL's real G2 value now decides
        missing = find_missing_required_cells(rows, manifest)
        # G3b is also listed (its NA row satisfies nothing) but is
        # already forced INSUFFICIENT, so it adds no extra count.
        self.assertEqual([(c.candidate, c.gate) for c in missing],
                         [("QLIKE", "G2"), ("QLIKE", "G3a"), ("QLIKE", "G3b"),
                          ("QLIKE", "G5"), ("QLIKE", "G6")])


class TestManifestIsTheEntryTicket(unittest.TestCase):
    def test_candidate_set_mismatch_and_undeclared_gate_are_errors(self):
        rows = full_rows("X") + full_rows("Y")
        with self.assertRaises(ValueError):  # Y has no manifest
            validate_manifest(rows, manifest_for("X"))
        with self.assertRaises(ValueError):  # Z declared, no rows
            validate_manifest(full_rows("X"),
                              manifest_for("X") + manifest_for("Z"))
        incomplete = [c for c in manifest_for("X") if c.gate != "G6"]
        with self.assertRaises(ValueError):  # G6 undeclared != NA
            validate_manifest(full_rows("X"), incomplete)
        with self.assertRaises(ValueError):  # and via build_gate_matrix
            build_gate_matrix(rows, manifest_for("X"))


class TestRenderAndCli(unittest.TestCase):
    def test_render_section_f_only_in_manifest_mode(self):
        rows = full_rows("X")
        plain = render_markdown(summarize(rows, build_gate_matrix(rows)))
        self.assertNotIn("(f) Cell manifest", plain)
        manifest = manifest_for("X")  # G1 required but NA -> missing
        text = render_markdown(
            summarize(rows, build_gate_matrix(rows, manifest)),
            manifest_missing=find_missing_required_cells(rows, manifest))
        self.assertIn("(f) Cell manifest", text)
        self.assertIn("| X | G1 | * | true | MISSING -> INSUFFICIENT |", text)

    def test_cli_manifest_exit_codes(self):
        with tempfile.TemporaryDirectory() as d:
            extract = Path(d) / "in.csv"
            lines = "".join(
                f"X,P,{g},W3,all,T4,Moderate,,,,,"
                f"{'NA' if g == 'G1' else 'INSUFFICIENT'}\n" for g in GATES)
            extract.write_text(EXTRACT_HEADER + lines)
            manifest = write_manifest(
                d, "candidate,gate,window,required\n" + "".join(
                    f"X,{g},*,{'false' if g == 'G1' else 'true'}\n"
                    for g in GATES))
            out = Path(d) / "out.md"
            self.assertEqual(main([str(extract), "--manifest", str(manifest),
                                   "--out", str(out)]), 0)
            self.assertIn("all required cells present", out.read_text())
            bad = write_manifest(d, "candidate,gate,window,required\n"
                                    "X,G2,*,true\n")
            self.assertEqual(main([str(extract), "--manifest", str(bad),
                                   "--out", str(out)]), 2)
            self.assertEqual(main([str(extract), "--out", str(out)]), 0)
            self.assertNotIn("(f)", out.read_text())


if __name__ == "__main__":
    unittest.main()
