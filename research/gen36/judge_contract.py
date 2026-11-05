"""Gen36 decision (Astra's single conjunctive rule from her Gen35 review). Engineering tolerances, not clinical.
REPAIR ACCEPTED (inference release only, owner approval required; promoted FALSE) iff, for every seed:
 G0 well-formed and bound: every panel x seed x arm has EXACTLY its registered key set (unique; only registered
    groups), every required metric numeric and finite; the release files equal the audited tensors and the row
    document's contract equals contract.build_table(); the fresh material hash equals the sealed manifest.json, and
    F2 'representable' comes from manifest.json (never from rows); X3 'representable' is recomputed from the audio.
 G1 signed projection > 0 for the candidate on every target-only row (F2 all levels/rates/formats, X3, X3q).
 G2 waveform error: mean wave_err(C) < mean wave_err(E1) in every target-only cell (F2 level x rate x format; X3 level;
    X3q); and on every REPRESENTABLE target-only row, wave_err(C) <= wave_err(E1) and |AC-gain error|(C) <= (E1).
 G3 noisy: SI-SDR(C) - SI-SDR(E1) >= -0.01 dB and STOI_DC(C) - STOI_DC(E1) >= -0.001 on every F1, X1 and X2 row
    (STOI_DC = STOI on mean-removed signals; ordinary STOI is reported only).
 G4 research path vs the EQUALLY FLUSHED comparator (A2 vs A1): ILD error +<= 0.05 dB and no ITD-error increase on
    every P1 item and P4 scene; zero lag on every P1 target-only ear; P6 silence and tail RMS(A2) <= A1.
 G5 candidate output: pre-write peak <= -1 dBFS (+1e-6) on every row; decoded F rows peak <= -1 dBFS plus the codec's
    quantisation step (PCM_16: 1/32768; FLOAT: 1e-6); no sample at or beyond full scale; X4 silence/tail RMS(C) <= E0.
Otherwise INVESTIGATE (no fallback candidate, no threshold rescue).
"""
from __future__ import annotations
import argparse, itertools, json, math, statistics, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
for p in ("gen35", "gen34", "gen33", "gen24", "bench-n6", "gen15", "screen_v2", "gen21"):
    sys.path.insert(0, str(R / p))
sys.path.insert(0, str(HERE))
SEEDS = (17, 18, 19)
EXP = ("E0_published", "E1_sign", "C_candidate")
RES = ("A1_sign", "A2_repair")
RATES = (16000, 44100, 48000)
FMTS = ("WAV_PCM_16", "WAV_FLOAT", "FLAC_PCM_16")
CEIL = 10 ** (-1 / 20)
NOISY = ("sisdr", "stoi", "stoi_dc", "peak", "sat", "pre_write_peak")
TONLY = NOISY + ("alpha", "wave_err", "ac_gain_err_db", "lag")


def _spec():
    from panel_v2 import TARGETS
    man = json.loads((HERE / "manifest.json").read_text())
    f1 = {(k["spk"], k["utt"], k["snr"], r, f) for k in man["items"]["F1"] for r in RATES for f in FMTS}
    f2 = {(k["spk"], k["utt"], k["level"], r, f) for k in man["items"]["F2"] for r in RATES for f in FMTS}
    T, S, A, N = (1, 2, 3, 4), ("low", "medium", "high"), (-60, -30, 30, 60), (-5.0, 0.0, 5.0, 10.0)
    x1 = {(t, s, a, n) for t in T for s in S for a in A for n in N}
    x2 = {(sp, c, m, n) for sp in TARGETS for c in range(4) for m in range(4) for n in (-5.0, 0.0)}
    x3 = {(t, s, a, lv) for t in T for s in S for a in A for lv in (0.035, 0.14, 0.56)}
    x3q = {(sp, c) for sp in TARGETS for c in range(4)}
    x4 = {("silence", None, None, None)} | {("transition", t, s, a) for t in T for s in S for a in A}
    p1 = {(t, s, a, n) for t in T for s in S for a in A for n in N + (None,)}
    p4 = {(c, a) for c in range(4) for a in (-60.0, -30.0, 30.0, 60.0)}
    return man, {
        "F1": (("spk", "utt", "snr", "rate", "fmt"), f1, EXP, NOISY),
        "F2": (("spk", "utt", "level", "rate", "fmt"), f2, EXP, TONLY),
        "X1": (("talker", "setting", "az", "snr"), x1, EXP, NOISY),
        "X2": (("spk", "crop", "mix", "snr"), x2, EXP, NOISY),
        "X3": (("talker", "setting", "az", "level"), x3, EXP, TONLY),
        "X3q": (("spk", "crop"), x3q, EXP, TONLY),
        "X4": (("kind", "talker", "setting", "az"), x4, EXP, ("rms", "pre_write_peak")),
        "P1": (("talker", "setting", "az", "snr"), p1, RES, ("ild_target_err_db", "itd_err_samples")),
        "P4": (("crop", "target_az"), p4, RES, ("ild_target_err_db", "itd_err_samples")),
        "P6": (("kind", "talker", "setting", "az"), x4, RES, ("rms",)),
    }


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def judge(rows_p, rebuild=True):
    import contract
    D = json.loads(Path(rows_p).read_text()); man, spec = _spec()
    idx, ok, why = {}, True, []
    for r in D["rows"]:
        p = r.get("panel")
        if p not in spec:
            ok = False; why.append(f"unknown panel {p}"); continue
        kf, _, arms, _ = spec[p]
        if r.get("seed") not in SEEDS or r.get("arm") not in arms:
            ok = False; why.append(f"unregistered group {p} {r.get('seed')} {r.get('arm')}"); continue
        k = tuple(r.get(f) for f in kf)
        slot = idx.setdefault((p, r["seed"], r["arm"]), {})
        if k in slot:
            ok = False; why.append(f"duplicate {p} {k}")
        slot[k] = r
    for p, (kf, keys, arms, req) in spec.items():
        for s, a in itertools.product(SEEDS, arms):
            got = idx.get((p, s, a), {})
            if set(got) != keys:
                ok = False; why.append(f"{p} {s} {a}: key set != registered ({len(got)} vs {len(keys)})")
            for k, r in got.items():
                need = req + (("lag_L", "lag_R") if p == "P1" and k[3] is None else ())
                if not all(_num(r.get(m)) for m in need):
                    ok = False; why.append(f"{p} {s} {a} {k}: missing or non-finite metric")
    try:
        table = contract.build_table()
        bound = {h: list(v) for h, v in table.items()} == D.get("contract") and D.get("fresh_material_sha256") == man["material_sha256"]
    except SystemExit as e:
        bound = False; why.append(str(e))
    rep_f2 = {(k["spk"], k["utt"], k["level"]): k["representable"] for k in man["items"]["F2"]}
    rep_x3 = {}
    if rebuild:
        import numpy as np
        import recorded_panel as P
        items, _, _ = P.build()
        for it in items:
            if it["snr"] is None:
                mono = 0.5 * (it["mL"] + it["mR"])
                for lv in (0.035, 0.14, 0.56):
                    rep_x3[(it["talker"], it["setting"], it["az"], lv)] = bool(np.max(np.abs((lv / P.RMS_IN * mono).astype(np.float32))) <= 1.0)
    else:
        rep_x3 = {k: k[3] != 0.56 for k in spec["X3"][1]}
    checks = {"G0_well_formed_and_bound": bool(ok and bound)}
    if not checks["G0_well_formed_and_bound"]:
        return {"checks": checks, "verdict": "INVESTIGATE", "why": why[:50]}
    g = lambda p, s, a: idx[(p, s, a)]
    mean = statistics.fmean
    g1 = all(r["alpha"] > 0 for s in SEEDS for p in ("F2", "X3", "X3q") for r in g(p, s, "C_candidate").values())
    g2, g2d = True, {}
    for s in SEEDS:
        cells = {}
        for k in spec["F2"][1]:
            cells.setdefault(("F2", k[2], k[3], k[4]), []).append(k)
        for k in spec["X3"][1]:
            cells.setdefault(("X3", k[3]), []).append(k)
        cells[("X3q",)] = list(spec["X3q"][1])
        for cell, ks in cells.items():
            p = cell[0]
            mc = mean(g(p, s, "C_candidate")[k]["wave_err"] for k in ks); me = mean(g(p, s, "E1_sign")[k]["wave_err"] for k in ks)
            g2d[f"{s}|{cell}"] = [me, mc]; g2 &= mc < me
        for p, rep in (("F2", lambda k: rep_f2[(k[0], k[1], k[2])]), ("X3", lambda k: rep_x3[k]), ("X3q", lambda k: True)):
            C, E = g(p, s, "C_candidate"), g(p, s, "E1_sign")
            for k in spec[p][1]:
                if rep(k):
                    g2 &= C[k]["wave_err"] <= E[k]["wave_err"] and C[k]["ac_gain_err_db"] <= E[k]["ac_gain_err_db"]
    g3, w3 = True, [0.0, 0.0]
    for s in SEEDS:
        for p in ("F1", "X1", "X2"):
            C, E = g(p, s, "C_candidate"), g(p, s, "E1_sign")
            for k in spec[p][1]:
                ds, dt = C[k]["sisdr"] - E[k]["sisdr"], C[k]["stoi_dc"] - E[k]["stoi_dc"]
                w3 = [min(w3[0], ds), min(w3[1], dt)]; g3 &= ds >= -0.01 and dt >= -0.001
    g4 = True
    for s in SEEDS:
        for p in ("P1", "P4"):
            A1, A2 = g(p, s, "A1_sign"), g(p, s, "A2_repair")
            for k in spec[p][1]:
                g4 &= A2[k]["ild_target_err_db"] - A1[k]["ild_target_err_db"] <= 0.05 and A2[k]["itd_err_samples"] <= A1[k]["itd_err_samples"]
        g4 &= all(r[f"lag_{e}"] == 0 for k, r in g("P1", s, "A2_repair").items() if k[3] is None for e in "LR")
        A1, A2 = g("P6", s, "A1_sign"), g("P6", s, "A2_repair")
        g4 &= all(A2[k]["rms"] <= A1[k]["rms"] for k in spec["P6"][1])
    g5 = True
    for s in SEEDS:
        for p in ("F1", "F2", "X1", "X2", "X3", "X3q", "X4"):
            C = g(p, s, "C_candidate")
            for k in spec[p][1]:
                r = C[k]; g5 &= r["pre_write_peak"] <= CEIL + 1e-6
                if p in ("F1", "F2"):
                    tol = 1 / 32768 if "PCM_16" in k[4] else 1e-6
                    g5 &= r["peak"] <= CEIL + tol and r["sat"] == 0
                elif "sat" in r:
                    g5 &= r["sat"] == 0
        C, E0 = g("X4", s, "C_candidate"), g("X4", s, "E0_published")
        g5 &= all(C[k]["rms"] <= E0[k]["rms"] for k in spec["X4"][1])
    checks.update({"G1_polarity_positive": bool(g1), "G2_waveform_and_gain": bool(g2), "G3_no_noisy_loss": bool(g3),
                   "G4_research_spatial_vs_equally_flushed": bool(g4), "G5_headroom_and_decoded_peaks": bool(g5)})
    verdict = "REPAIR ACCEPTED (inference only)" if all(checks.values()) else "INVESTIGATE"
    return {"checks": checks, "verdict": verdict, "G2_cell_means": g2d, "G3_worst": w3}


def judge_safe(rows_p, rebuild=True):
    try:
        return judge(rows_p, rebuild)
    except Exception as e:  # noqa: BLE001  malformed input -> INVESTIGATE, never a pass
        return {"checks": {"well_formed": False}, "verdict": "INVESTIGATE", "error": f"{type(e).__name__}: {e}"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rows", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    doc = judge_safe(a.rows)
    Path(a.out).write_text(json.dumps(doc, indent=1, default=str))
    print(json.dumps(doc["checks"]), doc["verdict"])


if __name__ == "__main__":
    main()
