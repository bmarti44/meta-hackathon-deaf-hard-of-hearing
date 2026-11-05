"""Gen33 versioned stereo runner: the registered spatial scenes, processed independently or linked.

Writes a document in judge_v3's spatial format (so judge_v3.spatial_gates can be applied unchanged):
- "existing": research/bench-n6/spatial_bench.py's 4 scenes and systems (unproc, gate_independent, gate_linked,
  candidate), replicated in-process with the candidate replaced by the chosen stereo processor;
- "crossed_rows": judge_v3.run_spatial's 16 crossed scenes (4 babble crops at SNR -5/0/5/10 x target azimuth
  -60/-30/30/60 with the crowd at the mirror azimuth);
- "extra_rows" (registered Gen33 addition): per-ear SI-SDR and STOI against each ear's clean target, for every crossed
  scene ("noisy") and for the same scenes with the crowd removed ("target_only"), plus ILD/ITD errors for target-only.
In --mode independent the existing and crossed rows must reproduce the legacy documents exactly (tested).

Usage: python research/gen33/spatial_linked.py --ckpt CK --mode independent|linked --name NAME --out OUT.json
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / "bench-n6")); sys.path.insert(0, str(R / "gen15")); sys.path.insert(0, str(HERE))
from baselines import CausalSpectralGate  # noqa: E402
from bench import build_crops  # noqa: E402
from spatial import LinkedSpectralGate, ild_per_band, itd_samples, render_at  # noqa: E402
from spatial_bench import TARGET_AZ  # noqa: E402
import linked  # noqa: E402

TR = slice(256, -256)


sys.path.insert(0, str(R / "gen24"))
from train13 import _si_sdr_np as _sisdr  # noqa: E402  the established implementation (mean-removed; Astra pre-launch blocking 2)


def _stoi(ref, est):
    from pystoi import stoi
    return float(stoi(ref.astype(np.float64), est.astype(np.float64), 16000, extended=False))


def run(ckpt, mode, name, extras=True):
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    pair = linked.pair_fn(ckpt, mode)
    sha = hashlib.sha256(Path(ckpt).read_bytes()).hexdigest()
    # --- existing bench, replicated from spatial_bench.py main() ---
    systems = {
        "unproc": lambda L, R_: (L, R_),
        "gate_independent": lambda L, R_: (CausalSpectralGate().process(L), CausalSpectralGate().process(R_)),
        "gate_linked": lambda L, R_: LinkedSpectralGate().process_stereo(L, R_),
        name: lambda L, R_: pair(L, R_),
    }
    rows = []
    for i, c in enumerate(crops):
        taz = TARGET_AZ[i % len(TARGET_AZ)]; naz = -taz
        cl, cr = render_at(c["clean"], taz); nl, nr = render_at(c["noise"], naz)
        mixL, mixR = cl + nl, cr + nr
        ild_tgt, ild_mix = ild_per_band(cl, cr), ild_per_band(mixL, mixR)
        itd_tgt = itd_samples(cl, cr)
        for sname, fn in systems.items():
            oL, oR = fn(mixL.copy(), mixR.copy())
            ild = ild_per_band(oL, oR)
            rows.append({"crop": i, "target_az": taz, "noise_az": naz, "snr_db": c["snr_db"], "system": sname,
                         "ild_target_err_db": float(np.mean(np.abs(ild - ild_tgt))),
                         "ild_distortion_db": float(np.mean(np.abs(ild - ild_mix))),
                         "itd_err_samples": float(abs(itd_samples(oL, oR) - itd_tgt))})
    summary = {s: {k: float(np.mean([r[k] for r in rows if r["system"] == s]))
                   for k in ["ild_target_err_db", "ild_distortion_db", "itd_err_samples"]} for s in systems}
    existing = {"meta": {"candidate": name, "checkpoint_sha256": sha, "gen15": str(ckpt), "mode": mode},
                "summary": summary, "rows": rows, "note": "ASSUMED head model; distortion comparisons only"}
    # --- crossed scenes, replicated from judge_v3.run_spatial ---
    crossed, extra = [], []
    for i, c in enumerate(crops):
        for taz in TARGET_AZ:
            cl, cr = render_at(c["clean"], taz); nl, nr = render_at(c["noise"], -taz)
            mL, mR = cl + nl, cr + nr
            ild_t, itd_t = ild_per_band(cl, cr), itd_samples(cl, cr)
            outs = {"unproc": (mL, mR), name: pair(mL.copy(), mR.copy())}
            for sname, (oL, oR) in outs.items():
                crossed.append({"crop": i, "snr_db": c["snr_db"], "target_az": taz, "noise_az": -taz, "system": sname,
                                "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL, oR) - ild_t))),
                                "itd_err_samples": float(abs(itd_samples(oL, oR) - itd_t))})
            if not extras:
                continue
            tgt = {"unproc": (cl, cr), name: pair(cl.copy(), cr.copy())}
            for cond, od in (("noisy", outs), ("target_only", tgt)):
                for sname, (oL, oR) in od.items():
                    rec = {"cond": cond, "crop": i, "snr_db": c["snr_db"], "target_az": taz, "system": sname,
                           "sisdr_L": _sisdr(cl[TR], oL[TR]), "sisdr_R": _sisdr(cr[TR], oR[TR]),
                           "stoi_L": _stoi(cl[TR], oL[TR]), "stoi_R": _stoi(cr[TR], oR[TR])}
                    if cond == "target_only":
                        rec["ild_target_err_db"] = float(np.mean(np.abs(ild_per_band(oL, oR) - ild_t)))
                        rec["itd_err_samples"] = float(abs(itd_samples(oL, oR) - itd_t))
                    extra.append(rec)
    return {"meta": {"candidate": name, "checkpoint_sha256": sha, "ckpt": str(ckpt), "mode": mode},
            "existing": existing, "crossed_rows": crossed, "extra_rows": extra,
            "note": "ASSUMED head model (spatial.py); crossed scenes = 4 crops x 4 target azimuths, crowd at mirror; "
                    "Gen33 runner (independent|linked)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True); ap.add_argument("--mode", choices=["independent", "linked"], required=True)
    ap.add_argument("--name", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    doc = run(a.ckpt, a.mode, a.name)
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(f"WROTE {a.out} existing={doc['existing']['summary'][a.name]}")


if __name__ == "__main__":
    main()
