"""KPI scorecard: bench JSON in, PASS/FAIL table out. Targets in KPI.md.

Run: /tmp/gen9env/bin/python research/bench-n6/kpi_scorecard.py \
  --bench research/bench-n6/bench_results_run2.json \
  --spatial research/bench-n6/spatial_results.json --candidate gen15_causal
"""
from __future__ import annotations
import argparse, json
from pathlib import Path

import numpy as np


def _row(name, actual, required, ok, stretch=None, stretch_ok=None, required_row=True):
    return {"kpi": name, "actual": actual, "required": required, "pass": bool(ok),
            "stretch": stretch, "stretch_pass": None if stretch_ok is None else bool(stretch_ok),
            "required_row": required_row}


def score_kpis(summary, per_snr_babble_d, spatial_summary, candidate,
               gate_name="causal_gate", linked_name="gate_linked", spatial_candidate=None,
               babble_kind="babble-heldout-spk", evidence_complete=True,
               per_snr_stoi=None, seed_crowd_means=None):
    c = summary[candidate]
    b = c[babble_kind]
    rows = [
        _row("babble dSI-SDR", round(b["d_sisdr"]["mean"], 2), ">=+3.0 & CIlo>0",
             b["d_sisdr"]["mean"] >= 3.0 and b["d_sisdr"]["ci_lo"] > 0,
             ">=+5.0", b["d_sisdr"]["mean"] >= 5.0),
        _row("babble dSTOI", round(b["d_stoi"]["mean"], 3), ">=+0.03 & CIlo>0",
             b["d_stoi"]["mean"] >= 0.03 and b["d_stoi"]["ci_lo"] > 0,
             ">=+0.06", b["d_stoi"]["mean"] >= 0.06),
        _row("babble dACE-electro", round(b["d_ace_electro_corr"]["mean"], 3), ">=+0.05 & CIlo>0",
             b["d_ace_electro_corr"]["mean"] >= 0.05 and b["d_ace_electro_corr"]["ci_lo"] > 0,
             ">=+0.10", b["d_ace_electro_corr"]["mean"] >= 0.10),
        _row("babble dSI-SDR @-5dB", round(per_snr_babble_d.get(-5.0, float("nan")), 2), ">=+1.5",
             per_snr_babble_d.get(-5.0, -9) >= 1.5, ">=+3.0", per_snr_babble_d.get(-5.0, -9) >= 3.0),
        _row("babble dSI-SDR @0dB", round(per_snr_babble_d.get(0.0, float("nan")), 2), ">=+1.5",
             per_snr_babble_d.get(0.0, -9) >= 1.5, ">=+3.0", per_snr_babble_d.get(0.0, -9) >= 3.0),
        _row("babble dSTOI @-5dB (no-harm guard)", round((per_snr_stoi or {}).get(-5.0, float("nan")), 3), ">=0",
             (per_snr_stoi or {}).get(-5.0, -9) >= 0, ">=+0.02", (per_snr_stoi or {}).get(-5.0, -9) >= 0.02),
        _row("every seed crowd dSI-SDR > 0",
             None if not seed_crowd_means else [round(v, 2) for v in seed_crowd_means], ">0 all seeds",
             bool(seed_crowd_means) and min(seed_crowd_means) > 0),
        _row("babble SI-SDR > classical gate", round(b["sisdr"], 2),
             f"> {round(summary[gate_name][babble_kind]['sisdr'], 2)}",
             b["sisdr"] > summary[gate_name][babble_kind]["sisdr"]),
        _row("SSN dSI-SDR", round(c["ssn"]["d_sisdr"]["mean"], 2), ">=+3.0",
             c["ssn"]["d_sisdr"]["mean"] >= 3.0, ">=+5.0", c["ssn"]["d_sisdr"]["mean"] >= 5.0),
        _row("white dSI-SDR", round(c["white-heldout"]["d_sisdr"]["mean"], 2), ">=0",
             c["white-heldout"]["d_sisdr"]["mean"] >= 0, ">=+1.5", c["white-heldout"]["d_sisdr"]["mean"] >= 1.5),
        _row("quiet abs SI-SDR", round(c["quiet"]["sisdr"], 1), ">=25",
             c["quiet"]["sisdr"] >= 25, ">=30", c["quiet"]["sisdr"] >= 30),
        _row("quiet dSTOI", round(c["quiet"]["d_stoi"]["mean"], 3), ">=-0.02",
             c["quiet"]["d_stoi"]["mean"] >= -0.02, ">=-0.01", c["quiet"]["d_stoi"]["mean"] >= -0.01),
    ]
    # Spatial is a co-equal required goal: absent/mismatched spatial
    # evidence makes the verdict INCOMPLETE, never PASS (Astra review).
    spatial_present = bool(spatial_summary and spatial_candidate in spatial_summary)
    incomplete = not evidence_complete or not spatial_present
    if spatial_present:
        s = spatial_summary[spatial_candidate]
        unp = spatial_summary["unproc"]
        rows += [
            _row("target-ILD error (dB)", round(s["ild_target_err_db"], 2), f"<{round(unp['ild_target_err_db'], 2)} (unproc)",
                 s["ild_target_err_db"] < unp["ild_target_err_db"],
                 ">=30% below unproc", s["ild_target_err_db"] <= 0.7 * unp["ild_target_err_db"]),
            _row("ITD error (samples)", round(s["itd_err_samples"], 1), f"<={round(unp['itd_err_samples'], 1)} (unproc)",
                 s["itd_err_samples"] <= unp["itd_err_samples"]),
            # Diagnostic only: perfect target recovery "fails" mixture-ILD
            # deviation by design, so it must never gate (Astra review).
            _row("ILD distortion vs mixture (diagnostic)", round(s["ild_distortion_db"], 2),
                 "diagnostic only", True, required_row=False),
        ]
    return {"candidate": candidate, "rows": rows, "incomplete": incomplete,
            "all_required_pass": (not incomplete) and all(r["pass"] for r in rows if r["required_row"])}


def _merge_seed_summaries(summaries, candidate, gate_name="causal_gate"):
    """Seed-mean of per-seed summaries; CI lo/hi widened to min/max
    across seeds (conservative; not a population CI)."""
    merged = {gate_name: summaries[0][gate_name]}
    kinds = summaries[0][candidate].keys()
    merged[candidate] = {}
    for kind in kinds:
        e0 = summaries[0][candidate][kind]
        e = {"n": e0.get("n")}
        for k, v in e0.items():
            if isinstance(v, dict) and "mean" in v:
                e[k] = {"mean": float(np.mean([s[candidate][kind][k]["mean"] for s in summaries])),
                        "ci_lo": float(np.min([s[candidate][kind][k]["ci_lo"] for s in summaries])),
                        "ci_hi": float(np.max([s[candidate][kind][k]["ci_hi"] for s in summaries]))}
            elif isinstance(v, (int, float)) and k != "n":
                e[k] = float(np.mean([s[candidate][kind][k] for s in summaries]))
        merged[candidate][kind] = e
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bench", required=True, action="append",
                    help="one per seed; >=3 required for a complete verdict")
    ap.add_argument("--spatial", default=None)
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--spatial-candidate", default=None)
    ap.add_argument("--babble-kind", default="babble-heldout-spk",
                    help="legacy: babble-heldout-spk | v2: crowd or competing")
    a = ap.parse_args()
    benches = [json.loads(Path(p).read_text()) for p in a.bench]
    summaries = []
    for b in benches:
        s = dict(b["summary"])
        src = b.get("meta", {}).get("candidate")
        if src and src != a.candidate and src in s:
            s[a.candidate] = s.pop(src)
            for r in b["rows"]:
                if r["system"] == src:
                    r["system"] = a.candidate
        summaries.append(s)
    per_snr, per_snr_stoi, seed_crowd_means, cells_complete = {}, {}, [], True
    for bench in benches:
        base = {r["crop"]: r for r in bench["rows"] if r["system"] == "unproc"}
        crowd_vals = [r["sisdr"] - base[r["crop"]]["sisdr"] for r in bench["rows"]
                      if r["system"] == a.candidate and r["kind"] == a.babble_kind]
        seed_crowd_means.append(float(np.mean(crowd_vals)) if crowd_vals else float("nan"))
    for snr in [-5.0, 0.0, 5.0, 10.0]:
        for key, store in [("sisdr", per_snr), ("stoi", per_snr_stoi)]:
            seed_vals = []
            for bench in benches:
                base = {r["crop"]: r for r in bench["rows"] if r["system"] == "unproc"}
                vals = [r[key] - base[r["crop"]][key] for r in bench["rows"]
                        if r["system"] == a.candidate and r["kind"] == a.babble_kind and r["snr_db"] == snr]
                if not vals or not np.all(np.isfinite(vals)):
                    cells_complete = False
                seed_vals.append(float(np.mean(vals)) if vals else float("nan"))
            store[snr] = float(np.mean(seed_vals)) if np.all(np.isfinite(seed_vals)) else float("nan")
    summary = _merge_seed_summaries(summaries, a.candidate)
    bench_hashes = {b.get("meta", {}).get("checkpoint_sha256") for b in benches}
    spatial_doc = json.loads(Path(a.spatial).read_text()) if a.spatial else None
    spatial = spatial_doc["summary"] if spatial_doc else None
    spatial_hash = (spatial_doc or {}).get("meta", {}).get("checkpoint_sha256")
    distinct_hashes = {h for h in bench_hashes if h}
    evidence_complete = (len(distinct_hashes) >= 3 and cells_complete
                         and spatial_hash is not None and spatial_hash in distinct_hashes)
    card = score_kpis(summary, per_snr, spatial, a.candidate,
                      spatial_candidate=a.spatial_candidate or a.candidate,
                      babble_kind=a.babble_kind, evidence_complete=evidence_complete,
                      per_snr_stoi=per_snr_stoi, seed_crowd_means=seed_crowd_means)
    for r in card["rows"]:
        st = "PASS" if r["pass"] else "FAIL"
        if not r["required_row"]:
            st = "INFO"
        sx = "" if r["stretch"] is None else f" | stretch {r['stretch']}: {'PASS' if r['stretch_pass'] else 'no'}"
        print(f"[{st}] {r['kpi']:38s} actual={r['actual']} required {r['required']}{sx}")
    verdict = ("INCOMPLETE - seed/spatial/hash evidence missing or mismatched" if card["incomplete"]
               else "PASS - earns Stage C listening" if card["all_required_pass"]
               else "FAIL - keep optimizing")
    print(f"ALL REQUIRED: {verdict}")


if __name__ == "__main__":
    main()
