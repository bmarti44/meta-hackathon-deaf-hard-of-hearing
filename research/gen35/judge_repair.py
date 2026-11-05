"""Gen35 decision (Astra's pre-registered engineering rule; tolerances are engineering, not clinical).

REPAIR ACCEPTED (inference repair only, promoted FALSE) iff all hold for arm A2 (repair) in every seed:
 V0 the rows are complete (exact counts per panel/seed/arm) and A0 for seed 17 reproduces Gen34's audited Gen19 rows on
    every shared metric exactly (v1 reproduction);
 R1 polarity positive: signed alpha > 0 on every target-only clip and ear: P1 target-only, P3 quiet, and P5 at all
    three input levels;
 R2 waveform error improves over sign-only: for every seed x BRUDEX setting x ear, mean target-only wave_err(A2) <
    mean wave_err(A1);
 R3 no noisy loss: for every P1 noisy item-ear and every P2 item, SI-SDR(A2) - SI-SDR(A0) >= -0.01 dB and
    STOI(A2) - STOI(A0) >= -0.001;
 R4 no cue loss: for every P1 item and every P4 scene, ILD error(A2) - ILD error(A0) <= 0.05 dB and
    ITD error(A2) <= ITD error(A0);
 R5 clipping, delay and silence do not worsen: clip fraction(A2) <= clip fraction(A0) for every P1/P5 row-ear;
    alignment lag(A2) == 0 on every P1 target-only ear; P6 silence and every transition tail: RMS(A2) <= RMS(A0).
Failure means investigate, with no threshold rescue. P7 (exported entry point) is reported, not gated.
"""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
SEEDS = (17, 18, 19)
ARMS = ("A0_existing", "A1_sign", "A2_repair")
SHARED = ("sisdr_L", "sisdr_R", "stoi_L", "stoi_R", "wave_err_L", "wave_err_R", "ild_target_err_db", "ild_mixture_dist_db", "itd_err_samples")


def _key(r, ks):
    return tuple(r[k] for k in ks)


def judge(rows_p):
    D = json.loads(Path(rows_p).read_text()); rows = D["rows"]
    out, checks = {}, {}
    by = {}
    for r in rows:
        by.setdefault((r["panel"], r["seed"], r.get("arm") or r.get("variant")), []).append(r)
    expect = {"P1": 240, "P2": 512, "P3": 64, "P4": 16, "P5": 48 * 3, "P6": 1 + 48}
    complete = all(len(by.get((p, s, a), [])) == n for p, n in expect.items() for s in SEEDS for a in ARMS)
    complete = complete and all(len(by.get(("P7", s, v), [])) == 48 * 3 + 1 for s in SEEDS for v in ("published", "repaired"))
    finite = all(all(math.isfinite(v) for v in r.values() if isinstance(v, float)) for r in rows)
    G = json.loads((R / "gen34" / "audit_s17.json").read_text())
    k1 = ("talker", "setting", "az", "snr")
    g19 = {_key(r, k1): r for r in G["rows"] if r["system"] == "gen19"}
    a0 = {_key(r, k1): r for r in by.get(("P1", 17, "A0_existing"), [])}
    v1 = set(a0) == set(g19) and all(a0[k][m] == g19[k][m] for k in g19 for m in SHARED)
    checks["V0_complete_finite_and_v1_reproduced"] = bool(complete and finite and v1)

    def idx(p, s, a, ks):
        return {_key(r, ks): r for r in by.get((p, s, a), [])}

    r1 = True
    for s in SEEDS:
        r1 &= all(r[f"alpha_{e}"] > 0 for r in by[("P1", s, "A2_repair")] if r["cond"] == "target_only" for e in "LR")
        r1 &= all(r["alpha"] > 0 for r in by[("P3", s, "A2_repair")])
        r1 &= all(r[f"alpha_{e}"] > 0 for r in by[("P5", s, "A2_repair")] for e in "LR")
    checks["R1_polarity_positive"] = bool(r1)
    r2, r2d = True, {}
    for s in SEEDS:
        for st in ("low", "medium", "high"):
            for e in "LR":
                m2 = statistics.fmean(r[f"wave_err_{e}"] for r in by[("P1", s, "A2_repair")] if r["cond"] == "target_only" and r["setting"] == st)
                m1 = statistics.fmean(r[f"wave_err_{e}"] for r in by[("P1", s, "A1_sign")] if r["cond"] == "target_only" and r["setting"] == st)
                r2d[f"{s}|{st}|{e}"] = {"A1_sign": m1, "A2_repair": m2}; r2 &= m2 < m1
    checks["R2_waveform_error_improves_over_sign_only"] = bool(r2)
    r3, worst3 = True, {"sisdr": 0.0, "stoi": 0.0}
    for s in SEEDS:
        A0, A2 = idx("P1", s, "A0_existing", k1), idx("P1", s, "A2_repair", k1)
        for k, r in A2.items():
            if r["cond"] != "noisy":
                continue
            for e in "LR":
                ds, dt = r[f"sisdr_{e}"] - A0[k][f"sisdr_{e}"], r[f"stoi_{e}"] - A0[k][f"stoi_{e}"]
                worst3["sisdr"] = min(worst3["sisdr"], ds); worst3["stoi"] = min(worst3["stoi"], dt)
                r3 &= ds >= -0.01 and dt >= -0.001
        k2 = ("spk", "crop", "mix", "snr")
        B0, B2 = idx("P2", s, "A0_existing", k2), idx("P2", s, "A2_repair", k2)
        for k, r in B2.items():
            ds, dt = r["sisdr"] - B0[k]["sisdr"], r["stoi"] - B0[k]["stoi"]
            worst3["sisdr"] = min(worst3["sisdr"], ds); worst3["stoi"] = min(worst3["stoi"], dt)
            r3 &= ds >= -0.01 and dt >= -0.001
    checks["R3_no_noisy_loss"] = bool(r3)
    r4, worst4 = True, {"ild": 0.0, "itd": 0.0}
    for s in SEEDS:
        for p, ks in (("P1", k1), ("P4", ("crop", "target_az"))):
            A0, A2 = idx(p, s, "A0_existing", ks), idx(p, s, "A2_repair", ks)
            for k, r in A2.items():
                di = r["ild_target_err_db"] - A0[k]["ild_target_err_db"]; dt = r["itd_err_samples"] - A0[k]["itd_err_samples"]
                worst4["ild"] = max(worst4["ild"], di); worst4["itd"] = max(worst4["itd"], dt)
                r4 &= di <= 0.05 and dt <= 0
    checks["R4_no_cue_loss"] = bool(r4)
    r5 = True
    for s in SEEDS:
        for p, ks in (("P1", k1), ("P5", ("talker", "setting", "az", "level"))):
            A0, A2 = idx(p, s, "A0_existing", ks), idx(p, s, "A2_repair", ks)
            r5 &= all(A2[k][f"clip_{e}"] <= A0[k][f"clip_{e}"] for k in A2 for e in "LR")
        r5 &= all(r[f"lag_{e}"] == 0 for r in by[("P1", s, "A2_repair")] if r["cond"] == "target_only" for e in "LR")
        kk = ("kind", "talker", "setting", "az")
        A0 = {_key({**{"talker": None, "setting": None, "az": None}, **r}, kk): r for r in by[("P6", s, "A0_existing")]}
        A2 = {_key({**{"talker": None, "setting": None, "az": None}, **r}, kk): r for r in by[("P6", s, "A2_repair")]}
        r5 &= set(A0) == set(A2) and all(A2[k]["rms"] <= A0[k]["rms"] for k in A2)
    checks["R5_clipping_delay_silence_not_worse"] = bool(r5)
    rep = {}
    for s in SEEDS:
        for v in ("published", "repaired"):
            rs = [r for r in by.get(("P7", s, v), []) if "alpha" in r]
            sil = [r for r in by.get(("P7", s, v), []) if r.get("kind") == "silence"]
            rep[f"{s}|{v}"] = {"alpha_min": min(r["alpha"] for r in rs), "alpha_mean": statistics.fmean(r["alpha"] for r in rs),
                               "abs_mean_max": max(abs(r["mean"]) for r in rs), "clip_max": max(r["clip"] for r in rs),
                               "silence_rms": sil[0]["rms"] if sil else None}
        for a in ARMS:
            sil = [r for r in by[("P6", s, a)] if r["kind"] == "silence"][0]
            rep[f"{s}|research|{a}|silence"] = {"rms": sil["rms"], "mean": sil["mean"]}
    verdict = "REPAIR ACCEPTED (inference only)" if all(checks.values()) else "INVESTIGATE"
    return {"checks": checks, "verdict": verdict, "R2_means": r2d, "R3_worst": worst3, "R4_worst": worst4,
            "P7_exported_descriptive": rep, "polarity": D["polarity"], "decoder_bias": D["decoder_bias"]}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rows", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    try:
        doc = judge(a.rows)
    except Exception as e:  # noqa: BLE001  malformed rows -> INVESTIGATE, never a pass
        doc = {"checks": {"well_formed": False}, "verdict": "INVESTIGATE", "error": f"{type(e).__name__}: {e}"}
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(json.dumps(doc["checks"]), doc["verdict"])


if __name__ == "__main__":
    main()
