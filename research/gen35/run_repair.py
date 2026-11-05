"""Gen35 runner (rewritten per Astra's pre-launch review): every panel x seeds 17/18/19 x arms. Rows only; the
registered rule is applied by judge_repair.py.

Research path, arms A0 existing / A1 sign / A2 repair (per ear where stereo):
 P1 BRUDEX 240 items: recorded_panel.metrics + alpha, mean, clip per ear; lag per ear on target-only items.
 P2 dry panel (screen v2, 512 mono items): SI-SDR, STOI, clip.
 P3 quiet: the 64 unique clean crops of P2: SI-SDR, STOI, waveform error, alpha, mean, clip, lag.
 P4 spatial: the 16 crossed scenes: ILD/ITD error, per-ear SI-SDR/STOI vs each ear's clean target, clip per ear.
 P5 levels: BRUDEX target-only items at input RMS 0.035 / 0.14 / 0.56: alpha, waveform error, clip, lag per ear.
 P6 silence (2 s zeros) and speech-to-silence transitions (3 s of each target-only item then 2 s zeros): RMS and mean
    of the output (silence) or of its last 1.5 s (transition), clip.
Exported entry point (the published enhance.py core, mono), arms E0 published / E1 sign / E2 repair:
 X1 BRUDEX noisy 192 items, mono mix-down; reference = mean of the two recorded ears: SI-SDR, STOI, clip.
 X2 dry panel 512 items: SI-SDR, STOI, clip.
 X3 target-only: BRUDEX target-only items (mono) at the three levels, and the 64 quiet crops. The export restores the
    output to the INPUT's RMS, and for target-only input the input IS the reference, so the unadjusted waveform error
    against the input is the correctly scaled comparison: alpha, waveform error, clip, lag.
 X4 silence and speech-to-silence transitions as in P6: RMS, mean, clip.
Usage: python research/gen35/run_repair.py --out research/gen35/repair_rows.json
"""
from __future__ import annotations
import argparse, json, sys, time
from multiprocessing import get_context
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parent
for p in ("gen34", "gen33", "gen24", "bench-n6", "gen15", "screen_v2", "gen21"):
    sys.path.insert(0, str(R / p))
sys.path.insert(0, str(HERE))
import repair as RP  # noqa: E402

LEVELS = (0.035, 0.14, 0.56)
TR = slice(256, -256)


def _clip(o):
    return float(np.mean(np.abs(o) > 1.0))


def _p1(seed):
    import recorded_panel as P
    A = RP.Arms(RP.CKPTS[seed]); items, mh, _ = P.build(); rows = []
    for it in items:
        oL, oR = A.outputs(it["mL"]), A.outputs(it["mR"])
        w = P.score_window(len(it["rL"]))
        for arm in RP.ARMS:
            rec = {"panel": "P1", "seed": seed, "arm": arm, **{k: it[k] for k in ("talker", "setting", "az", "snr", "cond")}}
            rec.update(P.metrics(it["rL"], it["rR"], oL[arm], oR[arm], it["mL"], it["mR"]))
            for e, r, o in (("L", it["rL"], oL[arm]), ("R", it["rR"], oR[arm])):
                rec[f"alpha_{e}"] = RP.signed_alpha(r, o, w); rec[f"mean_{e}"] = float(np.mean(o[w])); rec[f"clip_{e}"] = _clip(o)
                if it["cond"] == "target_only":
                    rec[f"lag_{e}"] = RP.peak_lag(r, o, w)
            rows.append(rec)
    return {"brudex_material_sha256": mh, "rows": rows}


def _p2p3x2(seed):
    from panel_v2 import build_items
    from pystoi import stoi
    from train13 import _si_sdr_np
    A = RP.Arms(RP.CKPTS[seed]); rows = []
    items = build_items()
    st = lambda c, o: float(stoi(c[TR].astype(np.float64), o[TR].astype(np.float64), 16000))
    for it in items:
        k = {"spk": it["spk"], "crop": it["crop"], "mix": it["mix"], "snr": it["snr"]}
        o = A.outputs(it["mix_wav"])
        for arm in RP.ARMS:
            rows.append({"panel": "P2", "seed": seed, "arm": arm, **k, "sisdr": _si_sdr_np(it["clean"][TR], o[arm][TR]),
                         "stoi": st(it["clean"], o[arm]), "clip": _clip(o[arm])})
        x = RP.export_arms(it["mix_wav"], A)
        for arm in RP.EXPORT_ARMS:
            rows.append({"panel": "X2", "seed": seed, "arm": arm, **k, "sisdr": _si_sdr_np(it["clean"][TR], x[arm][TR]),
                         "stoi": st(it["clean"], x[arm]), "clip": _clip(x[arm])})
    seen = set()
    for it in items:
        key = (it["spk"], it["crop"])
        if key in seen:
            continue
        seen.add(key)
        for panel, outs, arms in (("P3", A.outputs(it["clean"]), RP.ARMS), ("X3q", RP.export_arms(it["clean"], A), RP.EXPORT_ARMS)):
            for arm in arms:
                o = outs[arm]
                rows.append({"panel": panel, "seed": seed, "arm": arm, "spk": it["spk"], "crop": it["crop"],
                             "sisdr": _si_sdr_np(it["clean"][TR], o[TR]), "stoi": st(it["clean"], o),
                             "wave_err": RP.wave_err_db(it["clean"], o, TR), "alpha": RP.signed_alpha(it["clean"], o, TR),
                             "mean": float(np.mean(o[TR])), "clip": _clip(o), "lag": RP.peak_lag(it["clean"], o, TR)})
    return {"rows": rows}


def _rest(seed):
    import recorded_panel as P
    from bench import build_crops
    from pystoi import stoi
    from spatial import ild_per_band, itd_samples, render_at
    from spatial_bench import TARGET_AZ
    from train13 import _si_sdr_np
    A = RP.Arms(RP.CKPTS[seed]); rows = []
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    for i, c in enumerate(crops):                                                          # P4
        for taz in TARGET_AZ:
            cl, cr = render_at(c["clean"], taz); nl, nr = render_at(c["noise"], -taz)
            mL, mR = (cl + nl).astype(np.float32), (cr + nr).astype(np.float32)
            ild_t, itd_t = ild_per_band(cl, cr), itd_samples(cl, cr)
            oL, oR = A.outputs(mL), A.outputs(mR)
            for arm in RP.ARMS:
                rec = {"panel": "P4", "seed": seed, "arm": arm, "crop": i, "snr_db": c["snr_db"], "target_az": taz,
                       "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL[arm], oR[arm]) - ild_t))),
                       "itd_err_samples": float(abs(itd_samples(oL[arm], oR[arm]) - itd_t))}
                for e, ref, o in (("L", cl, oL[arm]), ("R", cr, oR[arm])):
                    rec[f"sisdr_{e}"] = _si_sdr_np(ref[TR], o[TR])
                    rec[f"stoi_{e}"] = float(stoi(ref[TR].astype(np.float64), o[TR].astype(np.float64), 16000)); rec[f"clip_{e}"] = _clip(o)
                rows.append(rec)
    items, _, _ = P.build()
    tgt = [it for it in items if it["cond"] == "target_only"]
    noisy = [it for it in items if it["cond"] == "noisy"]
    for it in tgt:                                                                         # P5 + X3 levels
        w = P.score_window(len(it["rL"]))
        mono_in = 0.5 * (it["mL"] + it["mR"])
        for lv in LEVELS:
            g = lv / P.RMS_IN
            outs = {e: A.outputs((g * it[f"m{e}"]).astype(np.float32)) for e in ("L", "R")}
            for arm in RP.ARMS:
                rec = {"panel": "P5", "seed": seed, "arm": arm, "level": lv, **{k: it[k] for k in ("talker", "setting", "az")}}
                for e in ("L", "R"):
                    ref = g * it[f"r{e}"].astype(np.float64); o = outs[e][arm]
                    rec[f"alpha_{e}"] = RP.signed_alpha(ref, o, w); rec[f"wave_err_{e}"] = RP.wave_err_db(ref, o, w)
                    rec[f"clip_{e}"] = _clip(o); rec[f"lag_{e}"] = RP.peak_lag(ref, o, w)
                rows.append(rec)
            xin = (g * mono_in).astype(np.float32); x = RP.export_arms(xin, A)
            for arm in RP.EXPORT_ARMS:
                rows.append({"panel": "X3", "seed": seed, "arm": arm, "level": lv, **{k: it[k] for k in ("talker", "setting", "az")},
                             "alpha": RP.signed_alpha(xin, x[arm], w), "wave_err": RP.wave_err_db(xin, x[arm], w),
                             "mean": float(np.mean(x[arm][w])), "clip": _clip(x[arm]), "lag": RP.peak_lag(xin, x[arm], w)})
    for it in noisy:                                                                       # X1
        from pystoi import stoi as _st
        w = P.score_window(len(it["rL"]))
        ref = 0.5 * (it["rL"].astype(np.float64) + it["rR"].astype(np.float64))
        x = RP.export_arms((0.5 * (it["mL"] + it["mR"])).astype(np.float32), A)
        for arm in RP.EXPORT_ARMS:
            rows.append({"panel": "X1", "seed": seed, "arm": arm, **{k: it[k] for k in ("talker", "setting", "az", "snr")},
                         "sisdr": _si_sdr_np(ref[w], x[arm][w]), "stoi": float(_st(ref[w], x[arm][w].astype(np.float64), 16000)),
                         "clip": _clip(x[arm])})
    z = np.zeros(2 * 16000, np.float32)                                                    # P6 + X4
    for panel, outs, arms in (("P6", A.outputs(z), RP.ARMS), ("X4", RP.export_arms(z, A), RP.EXPORT_ARMS)):
        for arm in arms:
            o = outs[arm].astype(np.float64)
            rows.append({"panel": panel, "seed": seed, "arm": arm, "kind": "silence", "talker": None, "setting": None, "az": None,
                         "rms": float(np.sqrt(np.mean(o ** 2))), "mean": float(np.mean(o)), "clip": _clip(o)})
    for it in tgt:
        x = np.concatenate([it["mL"][:3 * 16000], np.zeros(2 * 16000, np.float32)])
        for panel, outs, arms in (("P6", A.outputs(x), RP.ARMS), ("X4", RP.export_arms(x, A), RP.EXPORT_ARMS)):
            for arm in arms:
                tail = outs[arm][-24000:].astype(np.float64)
                rows.append({"panel": panel, "seed": seed, "arm": arm, "kind": "transition", **{k: it[k] for k in ("talker", "setting", "az")},
                             "rms": float(np.sqrt(np.mean(tail ** 2))), "mean": float(np.mean(tail)), "clip": _clip(outs[arm])})
    return {"rows": rows}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    RP.registered_polarity()                      # refuses unregistered checkpoints before any work
    t0 = time.time(); rows = []; mh = None
    jobs = [(_p1, s) for s in RP.CKPTS] + [(_p2p3x2, s) for s in RP.CKPTS] + [(_rest, s) for s in RP.CKPTS]
    with get_context("spawn").Pool(a.workers) as pool:
        res = [pool.apply_async(f, (s,)) for f, s in jobs]
        for r in res:
            out = r.get(); rows += out["rows"]; mh = out.get("brudex_material_sha256", mh)
            print(f"job done {time.time()-t0:.0f}s rows={len(rows)}", flush=True)
    doc = {"panel": "gen35_output_repair", "brudex_material_sha256": mh,
           "checkpoints": {str(s): {"path": str(p.relative_to(RP.REPO)), "sha256": RP.sha(p)} for s, p in RP.CKPTS.items()},
           "polarity": {str(s): RP.POLARITY[RP.sha(p)] for s, p in RP.CKPTS.items()},
           "decoder_bias": {str(s): RP.Arms(p).bias for s, p in RP.CKPTS.items()}, "rows": rows}
    Path(a.out).write_text(json.dumps(doc))
    print(f"WROTE {a.out} rows={len(rows)} {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
