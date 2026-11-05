"""Gen35 decision (Astra's engineering rule, extended per her pre-launch review). Tolerances are engineering, not clinical.

V0 well-formed and provenant: every panel x seed x arm has EXACTLY the registered key set (unique keys, matched across
   arms), every required metric present, numeric and finite; checkpoint hashes and polarities equal the frozen table in
   repair.POLARITY; A0 for seed 17 reproduces Gen34's audited Gen19 P1 rows exactly.
Research path (arms A0 existing / A1 sign / A2 repair), all seeds:
 R1 signed alpha > 0 on every target-only clip and ear: P1 target-only, P3, P5 (all three levels).
 R2 mean waveform error A2 < A1 for every seed x P1 setting x ear, every seed for P3, every seed x P5 level x setting x ear.
 R3 SI-SDR(A2) - SI-SDR(A0) >= -0.01 dB and STOI(A2) - STOI(A0) >= -0.001 for every P1 noisy item-ear, P2 item and
    P4 scene-ear.
 R4 ILD error(A2) - ILD error(A0) <= 0.05 dB and ITD error(A2) <= ITD error(A0) for every P1 item and P4 scene.
 R5 clip fraction(A2) <= clip fraction(A0) for every row-ear in P1-P6; alignment lag(A2) == 0 for every target-only
    ear/clip in P1, P3 and P5; RMS(A2) <= RMS(A0) on P6 silence and on every P6 transition tail.
Exported entry point (arms E0 published / E1 sign / E2 repair), gated separately, all seeds:
 E1 signed alpha > 0 on every X3 and X3q clip.
 E2 mean waveform error E2 < E1 for every seed x X3 level x setting, and every seed for X3q.
 E3 SI-SDR(E2) - SI-SDR(E0) >= -0.01 dB and STOI(E2) - STOI(E0) >= -0.001 for every X1 and X2 item.
 E5 clip(E2) <= clip(E0) for every X row; lag(E2) == 0 on every X3 and X3q clip; RMS(E2) <= RMS(E0) on X4 silence and
    every X4 transition tail.
REPAIR ACCEPTED (inference only) iff V0 and every research and export check pass; otherwise INVESTIGATE (no rescue).
"""
from __future__ import annotations
import argparse, itertools, json, math, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(R / "screen_v2")); sys.path.insert(0, str(R / "gen21")); sys.path.insert(0, str(R / "gen15"))
SEEDS = (17, 18, 19)
A_ARMS = ("A0_existing", "A1_sign", "A2_repair")
E_ARMS = ("E0_published", "E1_sign", "E2_repair")
SHARED = ("sisdr_L", "sisdr_R", "stoi_L", "stoi_R", "wave_err_L", "wave_err_R", "ild_target_err_db", "ild_mixture_dist_db", "itd_err_samples")
TALKERS, SETTINGS, AZ, SNRS, LEVELS = (1, 2, 3, 4), ("low", "medium", "high"), (-60, -30, 30, 60), (-5.0, 0.0, 5.0, 10.0), (0.035, 0.14, 0.56)


def _expected():
    from panel_v2 import TARGETS
    p1 = {(t, s, a, n) for t in TALKERS for s in SETTINGS for a in AZ for n in SNRS + (None,)}
    p2 = {(sp, c, m, n) for sp in TARGETS for c in range(4) for m in range(4) for n in (-5.0, 0.0)}
    p3 = {(sp, c) for sp in TARGETS for c in range(4)}
    p4 = {(c, a) for c in range(4) for a in (-60.0, -30.0, 30.0, 60.0)}
    p5 = {(t, s, a, lv) for t in TALKERS for s in SETTINGS for a in AZ for lv in LEVELS}
    x1 = {(t, s, a, n) for t in TALKERS for s in SETTINGS for a in AZ for n in SNRS}
    p6 = {("silence", None, None, None)} | {("transition", t, s, a) for t in TALKERS for s in SETTINGS for a in AZ}
    two = lambda *ms: tuple(f"{m}_{e}" for m in ms for e in "LR")
    spec = {  # panel: (key fields, expected keys, arms, required metrics, extra required on target-only P1 rows)
        "P1": (("talker", "setting", "az", "snr"), p1, A_ARMS, SHARED + two("alpha", "mean", "clip")),
        "P2": (("spk", "crop", "mix", "snr"), p2, A_ARMS, ("sisdr", "stoi", "clip")),
        "P3": (("spk", "crop"), p3, A_ARMS, ("sisdr", "stoi", "wave_err", "alpha", "mean", "clip", "lag")),
        "P4": (("crop", "target_az"), p4, A_ARMS, ("ild_target_err_db", "itd_err_samples") + two("sisdr", "stoi", "clip")),
        "P5": (("talker", "setting", "az", "level"), p5, A_ARMS, two("alpha", "wave_err", "clip", "lag")),
        "P6": (("kind", "talker", "setting", "az"), p6, A_ARMS, ("rms", "mean", "clip")),
        "X1": (("talker", "setting", "az", "snr"), x1, E_ARMS, ("sisdr", "stoi", "clip")),
        "X2": (("spk", "crop", "mix", "snr"), p2, E_ARMS, ("sisdr", "stoi", "clip")),
        "X3": (("talker", "setting", "az", "level"), p5, E_ARMS, ("alpha", "wave_err", "mean", "clip", "lag")),
        "X3q": (("spk", "crop"), p3, E_ARMS, ("sisdr", "stoi", "wave_err", "alpha", "mean", "clip", "lag")),
        "X4": (("kind", "talker", "setting", "az"), p6, E_ARMS, ("rms", "mean", "clip")),
    }
    return spec


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def judge(rows_p):
    import repair as RP
    D = json.loads(Path(rows_p).read_text()); spec = _expected()
    idx, ok, why = {}, True, []
    for r in D["rows"]:
        p = r.get("panel")
        if p not in spec:
            ok = False; why.append(f"unknown panel {p}"); continue
        kf, _, arms, _ = spec[p]
        k = tuple(r.get(f) for f in kf)
        if r.get("seed") not in SEEDS or r.get("arm") not in arms:      # unregistered seed/arm groups are rejected
            ok = False; why.append(f"unregistered group {p} {r.get('seed')} {r.get('arm')}")
        if p == "P1" and r.get("cond") != ("target_only" if k[3] is None else "noisy"):   # labels must match the key
            ok = False; why.append(f"P1 cond label inconsistent with snr for {k}")
        slot = idx.setdefault((p, r.get("seed"), r.get("arm")), {})
        if k in slot:
            ok = False; why.append(f"duplicate {p} {r.get('seed')} {r.get('arm')} {k}")
        slot[k] = r
    for p, (kf, keys, arms, req) in spec.items():
        for s in SEEDS:
            for a in arms:
                got = idx.get((p, s, a), {})
                if set(got) != keys:
                    ok = False; why.append(f"{p} {s} {a}: key set != registered ({len(got)} vs {len(keys)})")
                for k, r in got.items():
                    need = req + (("lag_L", "lag_R") if p == "P1" and k[3] is None else ())
                    if not all(_num(r.get(m)) for m in need):
                        ok = False; why.append(f"{p} {s} {a} {k}: missing or non-finite metric")
    prov = all(D["checkpoints"][str(s)]["sha256"] in RP.POLARITY and RP.POLARITY[D["checkpoints"][str(s)]["sha256"]] == D["polarity"][str(s)]
               and D["checkpoints"][str(s)]["sha256"] == RP.sha(RP.CKPTS[s]) for s in SEEDS)
    G = json.loads((R / "gen34" / "audit_s17.json").read_text())
    g19 = {(r["talker"], r["setting"], r["az"], r["snr"]): r for r in G["rows"] if r["system"] == "gen19"}
    a0 = idx.get(("P1", 17, "A0_existing"), {})
    v1 = set(a0) == set(g19) and all(a0[k][m] == g19[k][m] for k in g19 for m in SHARED)
    checks = {"V0_well_formed_provenant_v1_reproduced": bool(ok and prov and v1)}
    if not checks["V0_well_formed_provenant_v1_reproduced"]:
        return {"checks": checks, "verdict": "INVESTIGATE", "why": why[:50], "provenance": prov, "v1_reproduced": v1}
    g = lambda p, s, a: idx[(p, s, a)]
    mean = statistics.fmean
    # ---- research path ----
    r1 = all(r[f"alpha_{e}"] > 0 for s in SEEDS for k, r in g("P1", s, "A2_repair").items() if k[3] is None for e in "LR")
    r1 &= all(r["alpha"] > 0 for s in SEEDS for r in g("P3", s, "A2_repair").values())
    r1 &= all(r[f"alpha_{e}"] > 0 for s in SEEDS for r in g("P5", s, "A2_repair").values() for e in "LR")
    r2, r2d = True, {}
    for s in SEEDS:
        for st, e in itertools.product(SETTINGS, "LR"):
            m = [mean(r[f"wave_err_{e}"] for k, r in g("P1", s, a).items() if k[3] is None and k[1] == st) for a in ("A1_sign", "A2_repair")]
            r2d[f"P1|{s}|{st}|{e}"] = m; r2 &= m[1] < m[0]
        m = [mean(r["wave_err"] for r in g("P3", s, a).values()) for a in ("A1_sign", "A2_repair")]
        r2d[f"P3|{s}"] = m; r2 &= m[1] < m[0]
        for lv, st, e in itertools.product(LEVELS, SETTINGS, "LR"):
            m = [mean(r[f"wave_err_{e}"] for k, r in g("P5", s, a).items() if k[3] == lv and k[1] == st) for a in ("A1_sign", "A2_repair")]
            r2d[f"P5|{s}|{lv}|{st}|{e}"] = m; r2 &= m[1] < m[0]
    r3, w3 = True, [0.0, 0.0]
    for s in SEEDS:
        for p, ears, filt in (("P1", "LR", lambda k: k[3] is not None), ("P2", None, lambda k: True), ("P4", "LR", lambda k: True)):
            A0, A2 = g(p, s, "A0_existing"), g(p, s, "A2_repair")
            for k, r in A2.items():
                if not filt(k):
                    continue
                for e in (ears or [None]):
                    sfx = f"_{e}" if e else ""
                    ds, dt = r[f"sisdr{sfx}"] - A0[k][f"sisdr{sfx}"], r[f"stoi{sfx}"] - A0[k][f"stoi{sfx}"]
                    w3 = [min(w3[0], ds), min(w3[1], dt)]; r3 &= ds >= -0.01 and dt >= -0.001
    r4, w4 = True, [0.0, 0.0]
    for s in SEEDS:
        for p in ("P1", "P4"):
            A0, A2 = g(p, s, "A0_existing"), g(p, s, "A2_repair")
            for k, r in A2.items():
                di, dt = r["ild_target_err_db"] - A0[k]["ild_target_err_db"], r["itd_err_samples"] - A0[k]["itd_err_samples"]
                w4 = [max(w4[0], di), max(w4[1], dt)]; r4 &= di <= 0.05 and dt <= 0
    r5 = True
    for s in SEEDS:
        for p in ("P1", "P2", "P3", "P4", "P5", "P6"):
            A0, A2 = g(p, s, "A0_existing"), g(p, s, "A2_repair")
            for k, r in A2.items():
                cl = [c for c in ("clip", "clip_L", "clip_R") if c in r]
                r5 &= all(r[c] <= A0[k][c] for c in cl)
        r5 &= all(r[f"lag_{e}"] == 0 for k, r in g("P1", s, "A2_repair").items() if k[3] is None for e in "LR")
        r5 &= all(r["lag"] == 0 for r in g("P3", s, "A2_repair").values())
        r5 &= all(r[f"lag_{e}"] == 0 for r in g("P5", s, "A2_repair").values() for e in "LR")
        A0, A2 = g("P6", s, "A0_existing"), g("P6", s, "A2_repair")
        r5 &= all(A2[k]["rms"] <= A0[k]["rms"] for k in A2)
    checks.update({"R1_polarity_positive": bool(r1), "R2_waveform_error_below_sign_only": bool(r2), "R3_no_noisy_loss": bool(r3),
                   "R4_no_cue_loss": bool(r4), "R5_clip_delay_silence_not_worse": bool(r5)})
    # ---- exported entry point ----
    e1 = all(r["alpha"] > 0 for s in SEEDS for p in ("X3", "X3q") for r in g(p, s, "E2_repair").values())
    e2, e2d = True, {}
    for s in SEEDS:
        for lv, st in itertools.product(LEVELS, SETTINGS):
            m = [mean(r["wave_err"] for k, r in g("X3", s, a).items() if k[3] == lv and k[1] == st) for a in ("E1_sign", "E2_repair")]
            e2d[f"X3|{s}|{lv}|{st}"] = m; e2 &= m[1] < m[0]
        m = [mean(r["wave_err"] for r in g("X3q", s, a).values()) for a in ("E1_sign", "E2_repair")]
        e2d[f"X3q|{s}"] = m; e2 &= m[1] < m[0]
    e3, we3 = True, [0.0, 0.0]
    for s in SEEDS:
        for p in ("X1", "X2"):
            E0, E2 = g(p, s, "E0_published"), g(p, s, "E2_repair")
            for k, r in E2.items():
                ds, dt = r["sisdr"] - E0[k]["sisdr"], r["stoi"] - E0[k]["stoi"]
                we3 = [min(we3[0], ds), min(we3[1], dt)]; e3 &= ds >= -0.01 and dt >= -0.001
    e5 = True
    for s in SEEDS:
        for p in ("X1", "X2", "X3", "X3q", "X4"):
            E0, E2 = g(p, s, "E0_published"), g(p, s, "E2_repair")
            e5 &= all(r["clip"] <= E0[k]["clip"] for k, r in E2.items())
        e5 &= all(r["lag"] == 0 for p in ("X3", "X3q") for r in g(p, s, "E2_repair").values())
        E0, E2 = g("X4", s, "E0_published"), g("X4", s, "E2_repair")
        e5 &= all(E2[k]["rms"] <= E0[k]["rms"] for k in E2)
    checks.update({"E1_export_polarity_positive": bool(e1), "E2_export_waveform_error_below_sign_only": bool(e2),
                   "E3_export_no_noisy_loss": bool(e3), "E5_export_clip_delay_silence_not_worse": bool(e5)})
    verdict = "REPAIR ACCEPTED (inference only)" if all(checks.values()) else "INVESTIGATE"
    return {"checks": checks, "verdict": verdict, "R2_means": r2d, "R3_worst": w3, "R4_worst": w4, "E2_means": e2d, "E3_worst": we3,
            "polarity": D["polarity"], "decoder_bias": D["decoder_bias"]}


def judge_safe(rows_p):
    try:
        return judge(rows_p)
    except Exception as e:  # noqa: BLE001  malformed rows -> INVESTIGATE, never a pass
        return {"checks": {"well_formed": False}, "verdict": "INVESTIGATE", "error": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rows", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    doc = judge_safe(a.rows)
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(json.dumps(doc["checks"]), doc["verdict"])


if __name__ == "__main__":
    main()
