"""Spatial-cue distortion bench: does processing destroy direction?

Scenes: clean target at an azimuth + babble at another, rendered
with spatial.py's ASSUMED head model. Per system we report
  * ild_target_err_db: mean |ILD(output) - ILD(clean target)| over
    ACE bands (can the target still be located from level cues)
  * ild_distortion_db: mean |ILD(output) - ILD(mixture)| (how much
    the processor itself moved the cues)
  * itd_err_samples vs the clean target's ITD.
Unprocessed scores ild_distortion 0 by construction. A system that
"cleans" by scrambling cues fails here even if SI-SDR improves.

Run: /tmp/gen9env/bin/python research/bench-n6/spatial_bench.py \
       [--gen15 research/gen15/weights/causal_seed20261115.pt]
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "gen15"))

from baselines import CausalSpectralGate  # noqa: E402
from bench import build_crops, load_gen15  # noqa: E402
from spatial import LinkedSpectralGate, ild_per_band, itd_samples, render_at  # noqa: E402

TARGET_AZ = [-60.0, -30.0, 30.0, 60.0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gen15", default=str(HERE.parent / "gen15" / "weights" / "causal_seed20261115.pt"))
    ap.add_argument("--candidate-name", default="candidate")
    ap.add_argument("--out", default=str(HERE / "spatial_results.json"))
    a = ap.parse_args()
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    gen15 = load_gen15(a.gen15)
    systems = {
        "unproc": lambda L, R: (L, R),
        "gate_independent": lambda L, R: (CausalSpectralGate().process(L), CausalSpectralGate().process(R)),
        "gate_linked": lambda L, R: LinkedSpectralGate().process_stereo(L, R),
        a.candidate_name: lambda L, R: (gen15(L), gen15(R)),
    }
    rows = []
    for i, c in enumerate(crops):
        taz = TARGET_AZ[i % len(TARGET_AZ)]
        naz = -taz
        cl, cr = render_at(c["clean"], taz)
        nl, nr = render_at(c["noise"], naz)
        mixL, mixR = cl + nl, cr + nr
        ild_tgt, ild_mix = ild_per_band(cl, cr), ild_per_band(mixL, mixR)
        itd_tgt = itd_samples(cl, cr)
        for name, fn in systems.items():
            oL, oR = fn(mixL.copy(), mixR.copy())
            ild = ild_per_band(oL, oR)
            rows.append({"crop": i, "target_az": taz, "noise_az": naz, "snr_db": c["snr_db"],
                         "system": name,
                         "ild_target_err_db": float(np.mean(np.abs(ild - ild_tgt))),
                         "ild_distortion_db": float(np.mean(np.abs(ild - ild_mix))),
                         "itd_err_samples": float(abs(itd_samples(oL, oR) - itd_tgt))})
        print(f"scene {i+1}/{len(crops)} target@{taz:+.0f} noise@{naz:+.0f}", flush=True)
    summary = {}
    for name in systems:
        sel = [r for r in rows if r["system"] == name]
        summary[name] = {k: float(np.mean([r[k] for r in sel]))
                         for k in ["ild_target_err_db", "ild_distortion_db", "itd_err_samples"]}
    import hashlib
    ck_sha = hashlib.sha256(Path(a.gen15).read_bytes()).hexdigest() if a.gen15 else None
    Path(a.out).write_text(json.dumps({"meta": {"candidate": a.candidate_name,
                                                 "checkpoint_sha256": ck_sha, "gen15": a.gen15},
                                        "summary": summary, "rows": rows,
                                        "note": "ASSUMED head model; distortion comparisons only"}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
