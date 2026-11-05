"""Audit of the direct-arrival rule over every RIR in a manifest.

For each RIR (after the registered truncation): the v1 peak index, the
superseding onset-rule index, the shift, the largest |h| before the new
onset, the energy before the onset (re total), the onset-to-arrival
refinement, and the
arrival under -14 dB / -26 dB thresholds (sensitivity). Writes
selftest/arrival_audit.json and prints a summary.

Usage: /tmp/gen9env/bin/python research/gen27/audit_arrival.py [manifest]
"""
import json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rirbank as rb  # noqa: E402


def arrival_at(h, db):
    a = np.abs(h)
    o = int(np.argmax(a >= 10 ** (db / 20) * a.max()))
    return o + int(np.argmax(a[o:o + rb.ONSET_REFINE + 1]))


def main():
    man = json.loads(Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "rir_manifest.json").read_text())
    rows = []
    for r in man["rooms"]:
        for f in r["rirs"]:
            h = rb.truncate(rb.read_rir(rb.FILE_ROOT / f["file"]))
            a = np.abs(h); m = a.max()
            old, new = rb.direct_index_peak(h), rb.direct_index(h)
            onset = int(np.argmax(a >= 10 ** (rb.ONSET_DB / 20) * m))
            rows.append({"file": f["file"], "split": r["split"], "family": r["family"], "peak_idx": old, "arrival_idx": new,
                         "shift_ms": (old - new) * 1000 / rb.FS, "arrival_amp_re_peak": float(a[new] / m),
                         "onset_idx": onset, "refine_samples": new - onset,
                         "energy_before_onset_re_total_db": float(10 * np.log10((h[:onset] ** 2).sum() / (h ** 2).sum() + 1e-30)),
                         "energy_onset_to_arrival_re_total_db": float(10 * np.log10((h[onset:new] ** 2).sum() / (h ** 2).sum() + 1e-30)),
                         "arrival_m14db": arrival_at(h, -14.0), "arrival_m26db": arrival_at(h, -26.0)})
    sh = np.array([x["shift_ms"] for x in rows])
    amp = np.array([x["arrival_amp_re_peak"] for x in rows])
    sens = [x for x in rows if abs(x["arrival_m14db"] - x["arrival_idx"]) > 16 or abs(x["arrival_m26db"] - x["arrival_idx"]) > 16]
    summ = {"n_rirs": len(rows), "n_changed": int((sh != 0).sum()), "n_shift_gt_1ms": int((sh > 1).sum()),
            "n_shift_gt_5ms": int((sh > 5).sum()), "max_shift_ms": float(sh.max()),
            "shift_ms_p50_p90_p99": [float(np.percentile(sh, q)) for q in (50, 90, 99)],
            "arrival_amp_re_peak_min": float(amp.min()), "n_arrival_amp_lt_0.3": int((amp < 0.3).sum()),
            "max_energy_before_onset_db": float(max(x["energy_before_onset_re_total_db"] for x in rows)),
            "max_refine_samples": int(max(x["refine_samples"] for x in rows)),
            "n_threshold_sensitive_gt_1ms": len(sens),
            "by_split_changed_gt_1ms": {s: int(sum(1 for x in rows if x["split"] == s and x["shift_ms"] > 1)) for s in
                                       ("train", "eval_synth", "eval_measured")},
            "largest_shifts": sorted(rows, key=lambda x: -x["shift_ms"])[:8], "threshold_sensitive": sens[:12]}
    (HERE / "selftest").mkdir(exist_ok=True)
    (HERE / "selftest" / "arrival_audit.json").write_text(json.dumps({"summary": summ, "rows": rows}, indent=1))
    print(json.dumps({k: v for k, v in summ.items() if k not in ("largest_shifts", "threshold_sensitive")}, indent=1))
    for x in summ["largest_shifts"]:
        print("shift", round(x["shift_ms"], 2), "ms", x["file"], x["peak_idx"], "->", x["arrival_idx"], "amp", round(x["arrival_amp_re_peak"], 2))
    for x in summ["threshold_sensitive"]:
        print("sensitive", x["file"], x["arrival_m26db"], x["arrival_idx"], x["arrival_m14db"])


if __name__ == "__main__":
    main()
