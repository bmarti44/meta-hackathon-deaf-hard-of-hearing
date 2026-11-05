"""Gen36 runner: the candidate output contract (enhance_v2) vs the published export (E0) and sign-only (E1), plus the
research-path spatial/silence checks against an EQUALLY FLUSHED comparator (A1 vs A2). Rows only; judge_contract.py
applies the registered rule.

Export arms (mono): E0 published enhance.py core then np.clip (as its CLI writer does); E1 = E0 with the registered
polarity (then np.clip); C = enhance_v2 (contract + DC-free level + one headroom-capped gain; no clip).
Fresh panels (sealed manifest, research/gen36/manifest.py), written to a file and DECODED before scoring:
  rates 16000 / 44100 / 48000 x formats WAV PCM_16, WAV FLOAT, FLAC PCM_16.
  F1 noisy 64 items: SI-SDR, STOI (raw, descriptive), STOI_DC (gated), peaks, saturation.
  F2 target-only 48 items (two representable levels + labelled overload): alpha, unadjusted waveform error vs the
     input (the export restores the input's level), absolute AC-gain error, lag, peaks, saturation.
Regression panels (16 kHz, in memory, the writer's clip emulated for E0/E1): X1 BRUDEX noisy mono 192, X2 dry 512,
  X3 BRUDEX target-only x 3 levels 144, X3q quiet 64, X4 silence + 48 transitions.
Research path (Gen35 Arms; A1 sign + flush vs A2 sign + flush + bias removal): P1 BRUDEX 240 per ear (ILD/ITD error,
  lag on target-only), P4 16 crossed spatial scenes (ILD/ITD error), P6 silence + 48 transitions (RMS).
Usage: python research/gen36/run_contract.py --out research/gen36/contract_rows.json
"""
from __future__ import annotations
import argparse, io, json, sys, time
from multiprocessing import get_context
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parent
for p in ("gen35", "gen34", "gen33", "gen24", "bench-n6", "gen15", "screen_v2", "gen21"):
    sys.path.insert(0, str(R / p))
sys.path.insert(0, str(HERE))

RATES = (16000, 44100, 48000)
FMTS = (("WAV", "PCM_16"), ("WAV", "FLOAT"), ("FLAC", "PCM_16"))
EXPORT = ("E0_published", "E1_sign", "C_candidate")
RELEASE = {17: "model.safetensors", 18: "seed18.safetensors", 19: "seed19.safetensors"}


def _setup(seed):
    import contract, enhance_v2, repair as RP
    from safetensors.torch import load_file
    import importlib.util
    table = contract.build_table(); enhance_v2.bind_contract(table)
    rel = contract.RELEASE_DIR / RELEASE[seed]
    cand = enhance_v2.load_model(str(rel))
    # the published enhance.py imports 'model_causal'; make that name resolve to the PUBLISHED module (by path), not gen15's
    saved = sys.modules.get("model_causal"); sys.modules["model_causal"] = enhance_v2.PM
    try:
        spec = importlib.util.spec_from_file_location("pub_enh", R / "gen35" / "published" / "enhance.py")
        pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
    finally:
        if saved is None:
            sys.modules.pop("model_causal", None)
        else:
            sys.modules["model_causal"] = saved
    assert pub.CausalTasNetEnh is enhance_v2.PM.CausalTasNetEnh, "published enhance.py did not bind the published model"
    pmodel = pub.load_model(str(rel))
    pol, bias = cand._contract
    def arms(x, sr):
        e0 = pub.enhance(x, sr, model=pmodel)
        return {"E0_published": (e0, float(np.max(np.abs(e0)))), "E1_sign": (pol * e0, float(np.max(np.abs(e0)))),
                "C_candidate": (lambda o: (o[0], float(np.max(np.abs(o[0])))))(enhance_v2.enhance(x, sr, cand))}
    return arms, RP


def _write_decode(y, sr, fmt, arm):
    import soundfile as sf
    buf = io.BytesIO()
    out = y if arm == "C_candidate" else np.clip(y, -1.0, 1.0)      # the published CLI writer clips; the candidate does not
    sf.write(buf, out, sr, format=fmt[0], subtype=fmt[1]); buf.seek(0)
    d, sr2 = sf.read(buf, dtype="float64"); assert sr2 == sr
    return d


def _resamp(x, sr):
    from math import gcd
    from scipy.signal import resample_poly
    if sr == 16000:
        return np.asarray(x, np.float64)
    g = gcd(16000, sr)
    return resample_poly(np.asarray(x, np.float64), sr // g, 16000 // g)


def _metrics(ref, d, sr, target_only):
    import repair as RP
    from pystoi import stoi
    from train13 import _si_sdr_np
    tr = slice(int(0.016 * sr), -int(0.016 * sr))
    r, y = np.asarray(ref, np.float64)[tr], np.asarray(d, np.float64)[tr]
    out = {"sisdr": _si_sdr_np(r, y), "stoi": float(stoi(r, y, sr)), "stoi_dc": float(stoi(r - r.mean(), y - y.mean(), sr)),
           "peak": float(np.max(np.abs(d))), "sat": float(np.mean(np.abs(d) >= 1.0))}
    if target_only:
        w = slice(int(0.016 * sr), len(ref) - int(0.016 * sr))
        out.update({"alpha": RP.signed_alpha(ref, d, w), "wave_err": RP.wave_err_db(ref, d, w),
                    "ac_gain_err_db": float(abs(20 * np.log10((np.std(y) + 1e-12) / (np.std(r) + 1e-12)))),
                    "lag": RP.peak_lag(ref, d, w, max_lag=int(80 * sr / 16000))})
    return out


def _fresh(seed):
    import manifest as M
    arms, _ = _setup(seed); items, mh, _ = M.build(); rows = []
    seed_hash = mh
    for it in items:
        to = it["panel"] == "F2"
        for sr in RATES:
            x = _resamp(it["mix"], sr).astype(np.float32); ref = _resamp(it["clean"], sr)
            outs = arms(x, sr)
            for arm, (y, prepeak) in outs.items():
                for fmt in FMTS:
                    d = _write_decode(y, sr, fmt, arm)
                    key = {"spk": it["spk"], "utt": it["utt"], ("level" if to else "snr"): (it["level"] if to else it["snr"])}
                    rec = {"panel": it["panel"], "seed": seed, "arm": arm, **key, "rate": sr, "fmt": f"{fmt[0]}_{fmt[1]}",
                           "pre_write_peak": prepeak, **_metrics(x if to else ref, d, sr, to)}
                    if to:
                        rec["representable"] = it["representable"]
                    rows.append(rec)
    return {"fresh_material_by_seed": {str(seed): seed_hash}, "rows": rows}


def _regress(seed):
    import recorded_panel as P
    from panel_v2 import build_items
    arms, _ = _setup(seed); rows = []
    def em(arm, y):
        return y if arm == "C_candidate" else np.clip(y, -1.0, 1.0)
    items, _, _ = P.build()
    for it in items:
        mono = (0.5 * (it["mL"] + it["mR"])).astype(np.float32); ref = 0.5 * (it["rL"].astype(np.float64) + it["rR"].astype(np.float64))
        if it["cond"] == "noisy":
            for arm, (y, pk) in arms(mono, 16000).items():
                rows.append({"panel": "X1", "seed": seed, "arm": arm, **{k: it[k] for k in ("talker", "setting", "az", "snr")},
                             "pre_write_peak": pk, **_metrics(ref, em(arm, y), 16000, False)})
        else:
            for lv in (0.035, 0.14, 0.56):
                xin = (lv / P.RMS_IN * mono).astype(np.float32)
                for arm, (y, pk) in arms(xin, 16000).items():
                    rows.append({"panel": "X3", "seed": seed, "arm": arm, **{k: it[k] for k in ("talker", "setting", "az")}, "level": lv,
                                 "representable": bool(np.max(np.abs(xin)) <= 1.0), "pre_write_peak": pk,
                                 **_metrics(xin, em(arm, y), 16000, True)})
            xx = np.concatenate([mono[:3 * 16000], np.zeros(2 * 16000, np.float32)])
            for arm, (y, pk) in arms(xx, 16000).items():
                tail = em(arm, y)[-24000:].astype(np.float64)
                rows.append({"panel": "X4", "seed": seed, "arm": arm, "kind": "transition", **{k: it[k] for k in ("talker", "setting", "az")},
                             "rms": float(np.sqrt(np.mean(tail ** 2))), "pre_write_peak": pk})
    for arm, (y, pk) in arms(np.zeros(2 * 16000, np.float32), 16000).items():
        rows.append({"panel": "X4", "seed": seed, "arm": arm, "kind": "silence", "talker": None, "setting": None, "az": None,
                     "rms": float(np.sqrt(np.mean(np.asarray(y, np.float64) ** 2))), "pre_write_peak": pk})
    seen = set()
    for it in build_items():
        for arm, (y, pk) in arms(it["mix_wav"], 16000).items():
            rows.append({"panel": "X2", "seed": seed, "arm": arm, "spk": it["spk"], "crop": it["crop"], "mix": it["mix"], "snr": it["snr"],
                         "pre_write_peak": pk, **_metrics(it["clean"], em(arm, y), 16000, False)})
        k = (it["spk"], it["crop"])
        if k not in seen:
            seen.add(k)
            for arm, (y, pk) in arms(it["clean"], 16000).items():
                rows.append({"panel": "X3q", "seed": seed, "arm": arm, "spk": it["spk"], "crop": it["crop"], "pre_write_peak": pk,
                             **_metrics(it["clean"], em(arm, y), 16000, True)})
    return {"rows": rows}


def _research(seed):
    import recorded_panel as P
    from bench import build_crops
    from spatial import ild_per_band, itd_samples, render_at
    from spatial_bench import TARGET_AZ
    _, RP = _setup(seed); A = RP.Arms(RP.CKPTS[seed]); rows = []
    items, _, _ = P.build()
    for it in items:
        oL, oR = A.outputs(it["mL"]), A.outputs(it["mR"]); w = P.score_window(len(it["rL"]))
        ild_t, itd_t = ild_per_band(it["rL"][w], it["rR"][w]), itd_samples(it["rL"][w], it["rR"][w])
        for arm in ("A1_sign", "A2_repair"):
            rec = {"panel": "P1", "seed": seed, "arm": arm, **{k: it[k] for k in ("talker", "setting", "az", "snr")},
                   "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL[arm][w], oR[arm][w]) - ild_t))),
                   "itd_err_samples": float(abs(itd_samples(oL[arm][w], oR[arm][w]) - itd_t))}
            for e, ref, o in (("L", it["rL"], oL[arm]), ("R", it["rR"], oR[arm])):
                q = _metrics(ref[w], o[w], 16000, it["snr"] is None)
                rec[f"sisdr_{e}"] = q["sisdr"]; rec[f"stoi_dc_{e}"] = q["stoi_dc"]
                if it["snr"] is None:
                    rec[f"alpha_{e}"] = RP.signed_alpha(ref, o, w); rec[f"wave_err_{e}"] = RP.wave_err_db(ref, o, w)
                    rec[f"lag_{e}"] = RP.peak_lag(ref, o, w)
            rows.append(rec)
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    for i, c in enumerate(crops):
        for taz in TARGET_AZ:
            cl, cr = render_at(c["clean"], taz); nl, nr = render_at(c["noise"], -taz)
            oL, oR = A.outputs((cl + nl).astype(np.float32)), A.outputs((cr + nr).astype(np.float32))
            ild_t, itd_t = ild_per_band(cl, cr), itd_samples(cl, cr)
            for arm in ("A1_sign", "A2_repair"):
                rec = {"panel": "P4", "seed": seed, "arm": arm, "crop": i, "target_az": taz,
                       "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL[arm], oR[arm]) - ild_t))),
                       "itd_err_samples": float(abs(itd_samples(oL[arm], oR[arm]) - itd_t))}
                for e, ref, o in (("L", cl, oL[arm]), ("R", cr, oR[arm])):
                    q = _metrics(ref, o, 16000, False); rec[f"sisdr_{e}"] = q["sisdr"]; rec[f"stoi_dc_{e}"] = q["stoi_dc"]
                rows.append(rec)
    o = A.outputs(np.zeros(2 * 16000, np.float32))
    for arm in ("A1_sign", "A2_repair"):
        rows.append({"panel": "P6", "seed": seed, "arm": arm, "kind": "silence", "talker": None, "setting": None, "az": None,
                     "rms": float(np.sqrt(np.mean(o[arm].astype(np.float64) ** 2)))})
    for it in [i for i in items if i["snr"] is None]:
        o = A.outputs(np.concatenate([it["mL"][:3 * 16000], np.zeros(2 * 16000, np.float32)]))
        for arm in ("A1_sign", "A2_repair"):
            rows.append({"panel": "P6", "seed": seed, "arm": arm, "kind": "transition", **{k: it[k] for k in ("talker", "setting", "az")},
                         "rms": float(np.sqrt(np.mean(o[arm][-24000:].astype(np.float64) ** 2)))})
    return {"rows": rows}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    import contract
    table = contract.build_table()                   # refuses unless the release files equal the audited tensors
    import enhance_v2
    t0 = time.time(); rows = []; by_seed = {}
    jobs = [(f, s) for f in (_fresh, _regress, _research) for s in (17, 18, 19)]
    with get_context("spawn").Pool(a.workers) as pool:
        res = [pool.apply_async(f, (s,)) for f, s in jobs]
        for r in res:
            out = r.get(); rows += out["rows"]; by_seed.update(out.get("fresh_material_by_seed", {}))
            print(f"job done {time.time()-t0:.0f}s rows={len(rows)}", flush=True)
    doc = {"panel": "gen36_output_contract", "fresh_material_by_seed": by_seed,
           "release": {RELEASE[s]: contract.sha(contract.RELEASE_DIR / RELEASE[s]) for s in RELEASE},
           "release_config_sha256": contract.sha(contract.RELEASE_DIR / "config.json"),
           "release_enhance_sha256": contract.sha(contract.RELEASE_DIR / "enhance.py"),
           "model_module_sha256": enhance_v2.model_module_sha(),
           "contract": {h: list(v) for h, v in table.items()}, "rows": rows}
    Path(a.out).write_text(json.dumps(doc))
    print(f"WROTE {a.out} rows={len(rows)} {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
