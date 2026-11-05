"""Gen35 runner: every panel x seeds 17/18/19 x arms A0/A1/A2, plus the exported entry point (as published and
repaired). Writes rows only; judge_repair.py applies the registered engineering rule.

Panels:
 P1 BRUDEX (Gen34 asset, 240 items: 192 noisy + 48 target-only), research path, recorded_panel.metrics per arm, plus
    signed alpha / output mean / clip fraction / alignment lag per ear on target-only items.
 P2 dry development panel (screen v2 material 557ad44f..., 512 mono items): SI-SDR, STOI per arm.
 P3 quiet: the 64 unique clean crops of P2 alone: SI-SDR, STOI, waveform error, signed alpha, output mean.
 P4 spatial: the 16 crossed scenes (gen33 geometry): target-ILD error, ITD error per arm.
 P5 levels: P1 target-only items at input RMS 0.035 / 0.14 / 0.56: signed alpha, waveform error, clip fraction per ear.
 P6 silence: 2 s of zeros; and a transition (first 3 s of each P1 target-only item, then 2 s of zeros, RMS 0.14):
    output RMS and mean of the silent tail [last 1.5 s].
 P7 exported entry point (published Hugging Face enhance.py core, mono): on P1 target-only items (mono mix-down,
    reference = mean of the two recorded ears) at the three levels and on silence: as published and repaired.
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
                rec[f"alpha_{e}"] = RP.signed_alpha(r, o, w); rec[f"mean_{e}"] = float(np.mean(o[w]))
                rec[f"clip_{e}"] = float(np.mean(np.abs(o) > 1.0))
                if it["cond"] == "target_only":
                    rec[f"lag_{e}"] = RP.peak_lag(r, o, w)
            rows.append(rec)
    return seed, mh, rows


def _p2p3(seed):
    from panel_v2 import build_items
    from pystoi import stoi
    from train13 import _si_sdr_np
    A = RP.Arms(RP.CKPTS[seed]); tr = slice(256, -256); rows = []
    items = build_items()
    for it in items:
        o = A.outputs(it["mix_wav"])
        for arm in RP.ARMS:
            rows.append({"panel": "P2", "seed": seed, "arm": arm, "spk": it["spk"], "crop": it["crop"], "mix": it["mix"], "snr": it["snr"],
                         "sisdr": _si_sdr_np(it["clean"][tr], o[arm][tr]),
                         "stoi": float(stoi(it["clean"][tr].astype(np.float64), o[arm][tr].astype(np.float64), 16000))})
    seen = set()
    for it in items:
        k = (it["spk"], it["crop"])
        if k in seen:
            continue
        seen.add(k); o = A.outputs(it["clean"])
        for arm in RP.ARMS:
            rows.append({"panel": "P3", "seed": seed, "arm": arm, "spk": it["spk"], "crop": it["crop"],
                         "sisdr": _si_sdr_np(it["clean"][tr], o[arm][tr]),
                         "stoi": float(stoi(it["clean"][tr].astype(np.float64), o[arm][tr].astype(np.float64), 16000)),
                         "wave_err": RP.wave_err_db(it["clean"], o[arm], tr), "alpha": RP.signed_alpha(it["clean"], o[arm], tr),
                         "mean": float(np.mean(o[arm][tr]))})
    return seed, rows


def _rest(seed):
    import recorded_panel as P
    from bench import build_crops
    from spatial import ild_per_band, itd_samples, render_at
    from spatial_bench import TARGET_AZ
    A = RP.Arms(RP.CKPTS[seed]); rows = []
    # P4 spatial crossed scenes
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    for i, c in enumerate(crops):
        for taz in TARGET_AZ:
            cl, cr = render_at(c["clean"], taz); nl, nr = render_at(c["noise"], -taz)
            mL, mR = cl + nl, cr + nr
            ild_t, itd_t = ild_per_band(cl, cr), itd_samples(cl, cr)
            oL, oR = A.outputs(mL.astype(np.float32)), A.outputs(mR.astype(np.float32))
            for arm in RP.ARMS:
                rows.append({"panel": "P4", "seed": seed, "arm": arm, "crop": i, "snr_db": c["snr_db"], "target_az": taz,
                             "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL[arm], oR[arm]) - ild_t))),
                             "itd_err_samples": float(abs(itd_samples(oL[arm], oR[arm]) - itd_t))})
    items, _, _ = P.build()
    tgt = [it for it in items if it["cond"] == "target_only"]
    # P5 levels
    for it in tgt:
        w = P.score_window(len(it["rL"]))
        for lv in LEVELS:
            g = lv / P.RMS_IN
            outs = {e: A.outputs((g * it[f"m{e}"]).astype(np.float32)) for e in ("L", "R")}
            for arm in RP.ARMS:
                rec = {"panel": "P5", "seed": seed, "arm": arm, "level": lv, **{k: it[k] for k in ("talker", "setting", "az")}}
                for e in ("L", "R"):
                    ref = g * it[f"r{e}"].astype(np.float64); o = outs[e][arm]
                    rec[f"alpha_{e}"] = RP.signed_alpha(ref, o, w); rec[f"wave_err_{e}"] = RP.wave_err_db(ref, o, w)
                    rec[f"clip_{e}"] = float(np.mean(np.abs(o) > 1.0))
                rows.append(rec)
    # P6 silence and transitions
    z = np.zeros(2 * 16000, np.float32); o = A.outputs(z)
    for arm in RP.ARMS:
        rows.append({"panel": "P6", "seed": seed, "arm": arm, "kind": "silence",
                     "rms": float(np.sqrt(np.mean(o[arm].astype(np.float64) ** 2))), "mean": float(np.mean(o[arm]))})
    for it in tgt:
        x = np.concatenate([it["mL"][:3 * 16000], np.zeros(2 * 16000, np.float32)]); o = A.outputs(x)
        for arm in RP.ARMS:
            tail = o[arm][-24000:].astype(np.float64)
            rows.append({"panel": "P6", "seed": seed, "arm": arm, "kind": "transition", **{k: it[k] for k in ("talker", "setting", "az")},
                         "rms": float(np.sqrt(np.mean(tail ** 2))), "mean": float(np.mean(tail))})
    # P7 exported entry point, as published and repaired
    for it in tgt:
        mono_in = 0.5 * (it["mL"] + it["mR"]); ref = 0.5 * (it["rL"].astype(np.float64) + it["rR"].astype(np.float64))
        w = P.score_window(len(ref))
        for lv in LEVELS:
            g = lv / P.RMS_IN
            for variant, rep in (("published", None), ("repaired", (A.polarity, A.bias))):
                y = RP.export_enhance((g * mono_in).astype(np.float32), A.model, rep)
                rows.append({"panel": "P7", "seed": seed, "variant": variant, "level": lv, **{k: it[k] for k in ("talker", "setting", "az")},
                             "alpha": RP.signed_alpha(ref, y, w), "wave_err_norm": RP.wave_err_db(ref * (np.std(y[w]) / (np.std(ref[w]) + 1e-12)), y, w),
                             "mean": float(np.mean(y[w])), "clip": float(np.mean(np.abs(y) > 1.0))})
    for variant, rep in (("published", None), ("repaired", (A.polarity, A.bias))):
        y = RP.export_enhance(np.zeros(2 * 16000, np.float32), A.model, rep)
        rows.append({"panel": "P7", "seed": seed, "variant": variant, "kind": "silence", "rms": float(np.sqrt(np.mean(y.astype(np.float64) ** 2)))})
    return seed, rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    t0 = time.time(); rows = []; mh = None
    jobs = [(_p1, s) for s in RP.CKPTS] + [(_p2p3, s) for s in RP.CKPTS] + [(_rest, s) for s in RP.CKPTS]
    with get_context("spawn").Pool(a.workers) as pool:
        res = [pool.apply_async(f, (s,)) for f, s in jobs]
        for r in res:
            out = r.get()
            if len(out) == 3:
                mh = out[1]; rows += out[2]
            else:
                rows += out[1]
            print(f"job done {time.time()-t0:.0f}s rows={len(rows)}", flush=True)
    doc = {"panel": "gen35_output_repair", "brudex_material_sha256": mh,
           "checkpoints": {s: {"path": str(p.relative_to(RP.REPO)), "sha256": RP.sha(p)} for s, p in RP.CKPTS.items()},
           "polarity": {s: RP.registered_polarity()[RP.sha(p)] for s, p in RP.CKPTS.items()},
           "decoder_bias": {s: RP.Arms(p).bias for s, p in RP.CKPTS.items()}, "rows": rows}
    Path(a.out).write_text(json.dumps(doc))
    print(f"WROTE {a.out} rows={len(rows)} {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
