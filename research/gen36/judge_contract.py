"""Gen36 decision (Astra's single conjunctive rule; amended per her pre-launch review). Engineering tolerances.
REPAIR ACCEPTED (inference release only, owner approval required; promoted FALSE) iff, for every seed:
 G0 schema and binding:
    - every row's panel/seed/arm is registered; every key field is PRESENT with the registered type (no bools, no
      missing fields read as null); each panel x seed x arm has EXACTLY its registered key set, unique;
    - every required metric is present, numeric, finite and inside its domain (peaks/RMS/ILD/ITD/abs-gain >= 0,
      saturation fraction in [0, 1], lag an integer);
    - release safetensors/config/enhance/model module hashes and the contract table equal the registered ones and
      contract.build_table(); every seed's fresh material hash equals the sealed manifest.json; with rebuild, the
      manifest is rebuilt from the audio and must reproduce the sealed hash.
 G1 signed projection > 0 for the candidate on every export target-only row (F2, X3, X3q) and for A2 on every P1
    target-only ear.
 G2 target preservation: mean wave_err(C) < mean wave_err(E1) in every cell (F2 level x rate x format; X3 level x
    setting; X3q); on EVERY export target-only row (overload included) wave_err(C) <= E1 and |AC gain error|(C) <= E1;
    research P1 target-only: mean wave_err(A2) < A1 per setting x ear, and wave_err(A2) <= A1 on every item-ear.
 G3 noisy quality: SI-SDR(C) - SI-SDR(E1) >= -0.01 dB and STOI_DC(C) - STOI_DC(E1) >= -0.001 on every F1/X1/X2 row;
    the same per ear for A2 vs A1 on every P1 noisy item and P4 scene.
 G4 alignment and cues: lag(C) == 0 on every export target-only row; vs the EQUALLY FLUSHED A1: ILD error +<= 0.05 dB
    and no ITD-error increase on every P1 item and P4 scene; lag(A2) == 0 on every P1 target-only ear; P6 RMS(A2) <= A1.
 G5 headroom: candidate pre-write peak <= -1 dBFS (+1e-6) everywhere; decoded F rows peak <= -1 dBFS + codec step
    (PCM_16 1/32768, FLOAT 1e-6) and no sample at full scale; X4 silence/tail RMS(C) <= E0.
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
NONNEG = {"peak", "pre_write_peak", "rms", "ac_gain_err_db", "ild_target_err_db", "itd_err_samples"}
UNIT = {"sat"}
INTS = {"lag", "lag_L", "lag_R"}


def _isint(v):
    return isinstance(v, int) and not isinstance(v, bool)


def _isflt(v):
    return isinstance(v, float) or _isint(v)


T_SPK = lambda v: isinstance(v, str)
T_INT = _isint
T_SNR = lambda v: _isflt(v) and not isinstance(v, bool)
T_SNR_OR_NONE = lambda v: v is None or T_SNR(v)
T_LEVEL = lambda v: v == "overload" or (T_SNR(v))
T_RATE = lambda v: _isint(v) and v in RATES
T_FMT = lambda v: v in FMTS
T_STR = lambda v: isinstance(v, str)
T_STR_OR_NONE = lambda v: v is None or isinstance(v, str)
T_INT_OR_NONE = lambda v: v is None or _isint(v)


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
    ears = lambda *ms: tuple(f"{m}_{e}" for m in ms for e in "LR")
    return man, {  # panel: (key fields with types, keys, arms, required metrics)
        "F1": ((("spk", T_SPK), ("utt", T_INT), ("snr", T_SNR), ("rate", T_RATE), ("fmt", T_FMT)), f1, EXP, NOISY),
        "F2": ((("spk", T_SPK), ("utt", T_INT), ("level", T_LEVEL), ("rate", T_RATE), ("fmt", T_FMT)), f2, EXP, TONLY),
        "X1": ((("talker", T_INT), ("setting", T_STR), ("az", T_INT), ("snr", T_SNR)), x1, EXP, NOISY),
        "X2": ((("spk", T_SPK), ("crop", T_INT), ("mix", T_INT), ("snr", T_SNR)), x2, EXP, NOISY),
        "X3": ((("talker", T_INT), ("setting", T_STR), ("az", T_INT), ("level", T_SNR)), x3, EXP, TONLY),
        "X3q": ((("spk", T_SPK), ("crop", T_INT)), x3q, EXP, TONLY),
        "X4": ((("kind", T_STR), ("talker", T_INT_OR_NONE), ("setting", T_STR_OR_NONE), ("az", T_INT_OR_NONE)), x4, EXP, ("rms", "pre_write_peak")),
        "P1": ((("talker", T_INT), ("setting", T_STR), ("az", T_INT), ("snr", T_SNR_OR_NONE)), p1, RES,
               ("ild_target_err_db", "itd_err_samples") + ears("sisdr", "stoi_dc")),
        "P4": ((("crop", T_INT), ("target_az", T_SNR)), p4, RES, ("ild_target_err_db", "itd_err_samples") + ears("sisdr", "stoi_dc")),
        "P6": ((("kind", T_STR), ("talker", T_INT_OR_NONE), ("setting", T_STR_OR_NONE), ("az", T_INT_OR_NONE)), x4, RES, ("rms",)),
    }


def _metric_ok(m, v):
    if m in INTS:
        return _isint(v)
    if not (_isflt(v) and math.isfinite(v)):
        return False
    if m in NONNEG and v < 0:
        return False
    if m in UNIT and not (0 <= v <= 1):
        return False
    return True


def judge(rows_p, rebuild=True):
    import contract, enhance_v2
    D = json.loads(Path(rows_p).read_text()); man, spec = _spec()
    idx, ok, why = {}, True, []
    for r in D["rows"]:
        p = r.get("panel")
        if p not in spec:
            ok = False; why.append(f"unknown panel {p}"); continue
        kf, _, arms, _ = spec[p]
        if not _isint(r.get("seed")) or r.get("seed") not in SEEDS or r.get("arm") not in arms:
            ok = False; why.append(f"unregistered group {p} {r.get('seed')} {r.get('arm')}"); continue
        if not all(f in r and t(r[f]) for f, t in kf):
            ok = False; why.append(f"{p}: missing or mistyped key field in {[(f, r.get(f)) for f, _ in kf]}"); continue
        k = tuple(r[f] for f, _ in kf)
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
                need = req
                if p == "P1" and k[3] is None:
                    need = req + tuple(f"{m}_{e}" for m in ("alpha", "wave_err", "lag") for e in "LR")
                if not all(m in r and _metric_ok(m, r[m]) for m in need):
                    ok = False; why.append(f"{p} {s} {a} {k}: missing, non-finite or out-of-domain metric")
    bound = True
    try:
        table = contract.build_table()
        bound &= {h: list(v) for h, v in table.items()} == D.get("contract")
        bound &= D.get("release") == {n: contract.RELEASE_SHA[n] for n in contract.RELEASE}
        bound &= D.get("release_config_sha256") == contract.RELEASE_CONFIG_SHA
        bound &= D.get("release_enhance_sha256") == contract.PUBLISHED_ENHANCE_SHA
        bound &= D.get("model_module_sha256") == contract.PUBLISHED_MODEL_MODULE_SHA == enhance_v2.model_module_sha()
        bound &= D.get("fresh_material_by_seed") == {str(s): man["material_sha256"] for s in SEEDS}
        if rebuild:
            import manifest as M
            bound &= M.build()[1] == man["material_sha256"]
    except SystemExit as e:
        bound = False; why.append(str(e))
    if not bound:
        why.append("binding failed")
    checks = {"G0_schema_and_binding": bool(ok and bound)}
    if not checks["G0_schema_and_binding"]:
        return {"checks": checks, "verdict": "INVESTIGATE", "why": why[:50]}
    g = lambda p, s, a: idx[(p, s, a)]
    mean = statistics.fmean
    TO = lambda k: k[3] is None
    g1 = all(r["alpha"] > 0 for s in SEEDS for p in ("F2", "X3", "X3q") for r in g(p, s, "C_candidate").values())
    g1 &= all(r[f"alpha_{e}"] > 0 for s in SEEDS for k, r in g("P1", s, "A2_repair").items() if TO(k) for e in "LR")
    g2, g2d = True, {}
    for s in SEEDS:
        cells = {}
        for k in spec["F2"][1]:
            cells.setdefault(("F2", k[2], k[3], k[4]), []).append(k)
        for k in spec["X3"][1]:
            cells.setdefault(("X3", k[3], k[1]), []).append(k)
        cells[("X3q",)] = list(spec["X3q"][1])
        for cell, ks in cells.items():
            p = cell[0]
            me, mc = (mean(g(p, s, a)[k]["wave_err"] for k in ks) for a in ("E1_sign", "C_candidate"))
            g2d[f"{s}|{cell}"] = [me, mc]; g2 &= mc < me
        for p in ("F2", "X3", "X3q"):
            C, E = g(p, s, "C_candidate"), g(p, s, "E1_sign")
            g2 &= all(C[k]["wave_err"] <= E[k]["wave_err"] and C[k]["ac_gain_err_db"] <= E[k]["ac_gain_err_db"] for k in spec[p][1])
        A1, A2 = g("P1", s, "A1_sign"), g("P1", s, "A2_repair")
        for st, e in itertools.product(("low", "medium", "high"), "LR"):
            ks = [k for k in spec["P1"][1] if TO(k) and k[1] == st]
            m1, m2 = mean(A1[k][f"wave_err_{e}"] for k in ks), mean(A2[k][f"wave_err_{e}"] for k in ks)
            g2d[f"{s}|P1|{st}|{e}"] = [m1, m2]; g2 &= m2 < m1
        g2 &= all(A2[k][f"wave_err_{e}"] <= A1[k][f"wave_err_{e}"] for k in spec["P1"][1] if TO(k) for e in "LR")
    g3, w3 = True, [0.0, 0.0]
    for s in SEEDS:
        for p in ("F1", "X1", "X2"):
            C, E = g(p, s, "C_candidate"), g(p, s, "E1_sign")
            for k in spec[p][1]:
                ds, dt = C[k]["sisdr"] - E[k]["sisdr"], C[k]["stoi_dc"] - E[k]["stoi_dc"]
                w3 = [min(w3[0], ds), min(w3[1], dt)]; g3 &= ds >= -0.01 and dt >= -0.001
        for p, filt in (("P1", lambda k: not TO(k)), ("P4", lambda k: True)):
            A1, A2 = g(p, s, "A1_sign"), g(p, s, "A2_repair")
            for k in spec[p][1]:
                if filt(k):
                    for e in "LR":
                        ds, dt = A2[k][f"sisdr_{e}"] - A1[k][f"sisdr_{e}"], A2[k][f"stoi_dc_{e}"] - A1[k][f"stoi_dc_{e}"]
                        w3 = [min(w3[0], ds), min(w3[1], dt)]; g3 &= ds >= -0.01 and dt >= -0.001
    g4 = all(r["lag"] == 0 for s in SEEDS for p in ("F2", "X3", "X3q") for r in g(p, s, "C_candidate").values())
    for s in SEEDS:
        for p in ("P1", "P4"):
            A1, A2 = g(p, s, "A1_sign"), g(p, s, "A2_repair")
            g4 &= all(A2[k]["ild_target_err_db"] - A1[k]["ild_target_err_db"] <= 0.05 and A2[k]["itd_err_samples"] <= A1[k]["itd_err_samples"]
                      for k in spec[p][1])
        g4 &= all(r[f"lag_{e}"] == 0 for k, r in g("P1", s, "A2_repair").items() if TO(k) for e in "LR")
        A1, A2 = g("P6", s, "A1_sign"), g("P6", s, "A2_repair")
        g4 &= all(A2[k]["rms"] <= A1[k]["rms"] for k in spec["P6"][1])
    g5 = True
    for s in SEEDS:
        for p in ("F1", "F2", "X1", "X2", "X3", "X3q", "X4"):
            C = g(p, s, "C_candidate")
            for k in spec[p][1]:
                r = C[k]; g5 &= r["pre_write_peak"] <= CEIL + 1e-6
                if p in ("F1", "F2"):
                    g5 &= r["peak"] <= CEIL + (1 / 32768 if "PCM_16" in k[4] else 1e-6) and r["sat"] == 0
                elif "sat" in r:
                    g5 &= r["sat"] == 0
        C, E0 = g("X4", s, "C_candidate"), g("X4", s, "E0_published")
        g5 &= all(C[k]["rms"] <= E0[k]["rms"] for k in spec["X4"][1])
    checks.update({"G1_polarity_positive": bool(g1), "G2_target_preservation": bool(g2), "G3_noisy_quality": bool(g3),
                   "G4_alignment_and_cues": bool(g4), "G5_headroom": bool(g5)})
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
