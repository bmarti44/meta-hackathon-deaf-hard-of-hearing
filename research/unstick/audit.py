"""Read-only audit of historical scores and synthetic scorer contract probes.

Run from any directory: PYTHONDONTWRITEBYTECODE=1 python3 research/unstick/audit.py
Synthetic fixtures are NOT research evidence or new candidates. Stdlib only.
Prints JSON; never edits the production scorer, evidence, or GOAL.
"""
from collections import Counter
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research/scoring"))
import gate_table as gt


def row(gate, verdict="PASS", window="W3", tier="T4", stratum="all"):
    return gt.Row("SYNTHETIC-NOT-EVIDENCE", "P", gate, window, stratum,
                  tier, "Moderate", None, None, None, None, verdict)


def gate(rows, name):
    return gt.build_gate_matrix(rows)["SYNTHETIC-NOT-EVIDENCE"][name]


def main():
    pairs = [
        ("gen00/scoring/adapted_v2.csv", "gen00/scoring/gate-matrix-gen0-v2.md", None),
        ("gen01/scoring/adapted-gen1.csv", "gen01/scoring/gate-matrix-gen1.md", None),
        ("gen02/scoring/adapted-gen2.csv", "gen02/scoring/gate-matrix-gen2.md", None),
        ("gen03design/scoring/adapted-gen3.csv", "gen03design/scoring/gate-matrix-gen3.md", "gen03design/scoring/manifest-gen3-P3W3.csv"),
        ("gen04/scoring/adapted-gen4.csv", "gen04/scoring/gate-matrix-gen4.md", "gen04/scoring/manifest-gen4-P4W4.csv"),
    ]
    all_rows, history = [], []
    for source, filed, manifest in pairs:
        rows = gt.load_extraction(ROOT / "research" / source)
        all_rows.extend(rows)
        cells = gt.load_manifest(ROOT / "research" / manifest) if manifest else None
        matrix = gt.build_gate_matrix(rows, cells)
        missing = gt.find_missing_required_cells(rows, cells) if cells is not None else None
        rendered = gt.render_markdown(gt.summarize(rows, matrix), missing).encode()
        existing = (ROOT / "research" / filed).read_bytes()
        assert rendered == existing, filed
        history.append({"input": source, "rows": len(rows), "matrix_equal": True,
                        "matrix_sha256": hashlib.sha256(rendered).hexdigest()})
    assert len(all_rows) == 322
    assert not any(r.verdict == "PASS" for r in all_rows)

    # These are diagnostic observations, not expected promotion behavior.
    probes = {
        "fixed_G2_mechanism_does_not_veto_W3": gate([row("G2"), row("G2", "INSUFFICIENT", "W0")], "G2"),
        "fixed_T0_G1_PASS_downgraded": gate([row("G1", tier="T0")], "G1"),
        "old_insufficient_and_new_pass_same_cell": gate([row("G2", "INSUFFICIENT"), row("G2")], "G2"),
        "G3a_W1_no_superiority_encoded_INS_blocks_W3": gate([row("G3a", "INSUFFICIENT", "W1"), row("G3a")], "G3a"),
        "G4_T2_residual_hearing_wrongly_accepted_at_gate_level": gate([row("G4", tier="T2", stratum="residual-hearing")], "G4"),
        "G2_label_pass_zero_effect_not_checked": gate([replace(row("G2"), delta_g2_db=0.0)], "G2"),
        "blocked_G3b_PASS_stays_INS_intentional": gate([row("G3b")], "G3b"),
        "blocked_G3b_FAIL_also_overwritten": gate([row("G3b", "FAIL")], "G3b"),
    }
    manifest = [gt.ManifestCell("SYNTHETIC-NOT-EVIDENCE", g, "*", g == "G4") for g in gt.GATES]
    partial = [row("G4", stratum="only-one-component-and-one-stratum")]
    probes["manifest_accepts_one_G4_component_for_whole_gate"] = {
        "missing": len(gt.find_missing_required_cells(partial, manifest)),
        "G4": gt.build_gate_matrix(partial, manifest)["SYNTHETIC-NOT-EVIDENCE"]["G4"],
    }
    assert probes["fixed_G2_mechanism_does_not_veto_W3"] == "PASS"
    assert probes["fixed_T0_G1_PASS_downgraded"] == "INSUFFICIENT"
    assert probes["old_insufficient_and_new_pass_same_cell"] == "INSUFFICIENT"
    assert probes["G3a_W1_no_superiority_encoded_INS_blocks_W3"] == "INSUFFICIENT"
    assert probes["G4_T2_residual_hearing_wrongly_accepted_at_gate_level"] == "PASS"
    assert probes["G2_label_pass_zero_effect_not_checked"] == "PASS"
    assert probes["blocked_G3b_PASS_stays_INS_intentional"] == "INSUFFICIENT"
    assert probes["blocked_G3b_FAIL_also_overwritten"] == "INSUFFICIENT"
    assert probes["manifest_accepts_one_G4_component_for_whole_gate"] == {"missing": 0, "G4": "PASS"}

    # Proposed G3b qualification-study feasibility arithmetic, NOT clinical data.
    # At a hypothetical true 10% missing rate, estimate precision per modality.
    # Probability bounds use independent Bernoulli approximation, not clustering.
    n_complete, missing_rate = 100, 0.10
    precision = {
        "assumed_missing_rate": missing_rate,
        "n_complete_per_modality": n_complete,
        "approx_95pct_missing_rate_halfwidth": 1.96 * math.sqrt(missing_rate * (1-missing_rate) / n_complete),
        "recruitment_target_per_modality_at_20pct_attrition": math.ceil(n_complete / .8),
        "zero_events_one_sided_95pct_upper_n100": 1 - .05 ** (1/n_complete),
        "caution": "Planning assumptions only; no power claim for MCID, invariance, or joint promotion.",
    }
    out = {
        "scope": "Exploratory audit; all probes synthetic; no evidence re-scored or generation created",
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "goal_sha256": hashlib.sha256((ROOT / "GOAL.md").read_bytes()).hexdigest(),
        "historical_reproduction": history,
        "combined_rows": len(all_rows),
        "combined_row_verdicts": dict(Counter(r.verdict for r in all_rows)),
        "combined_grades": dict(Counter(r.grade for r in all_rows)),
        "synthetic_probes": probes,
        "measurement_study_precision": precision,
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
