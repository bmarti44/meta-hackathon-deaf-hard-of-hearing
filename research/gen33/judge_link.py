"""Gen33 decision rule (Astra's Gen32 review; registered in research/gen33/prereg.md). Feasibility only, never ADVANCE.

Inputs (all from spatial_linked.py, same scenes): Gen32 LINKED (candidate), Gen32 independent, Gen19 independent;
optional Gen19 linked (descriptive only). The original SP gate uses judge_v3.spatial_gates unchanged, with the
registered Gen19 self-test document as its control.

PASS ("linkage feasibility passed") requires all of:
 L1 original SP passes for the linked candidate vs Gen19 (judge_v3.spatial_gates, unchanged);
 L2 crossed-scene mean target-ILD error (16 scenes) strictly below independent Gen32's;
 L3 in every SNR x mirrored-direction subset (4 SNRs x left/right targets, 2 scenes each), mean target-ILD error and
    mean ITD error are each <= independent Gen19's;
 L4 mean per-ear (both ears pooled) SI-SDR and STOI differences, linked minus control, are >= 0 against BOTH independent
    Gen32 and independent Gen19, in every noisy SNR x direction subset and in each mirrored target-only subset (left, right).
Any failure rejects this specific wrapper.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE.parent
SNRS = (-5.0, 0.0, 5.0, 10.0)
DIRS = {"left": lambda az: az < 0, "right": lambda az: az > 0}


def _load_judge_v3():
    spec = importlib.util.spec_from_file_location("judge_v3_g33", R / "gen27" / "judge_v3.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


GRID = {(i, az) for i in range(4) for az in (-60.0, -30.0, 30.0, 60.0)}
SNR_OF_CROP = {0: -5.0, 1: 0.0, 2: 5.0, 3: 10.0}


def _need(cond, msg):
    if not cond:
        raise SystemExit(f"INVALID: {msg}")


def _keyed(rows, what):
    """Complete, unique 16-scene grid with registered metadata and finite metrics (Astra pre-launch blocking 1)."""
    ks = [(r["crop"], r["target_az"]) for r in rows]
    _need(len(ks) == len(set(ks)), f"{what}: duplicate scenes")
    _need(set(ks) == GRID, f"{what}: scenes != registered 16-scene grid")
    for r in rows:
        _need(r["snr_db"] == SNR_OF_CROP[r["crop"]], f"{what}: SNR metadata != registered")
        _need(all(math.isfinite(v) for k, v in r.items() if isinstance(v, float)), f"{what}: non-finite metric")
    return {(r["crop"], r["target_az"]): r for r in rows}


def _crossed(doc):
    n = doc["meta"]["candidate"]
    return _keyed([r for r in doc["crossed_rows"] if r["system"] == n], f"crossed {n}")


def _extra(doc, cond):
    n = doc["meta"]["candidate"]
    rows = [r for r in doc["extra_rows"] if r["system"] == n and r["cond"] == cond]
    out = _keyed(rows, f"extra {cond} {n}")
    need = ("sisdr_L", "sisdr_R", "stoi_L", "stoi_R") + (("ild_target_err_db", "itd_err_samples") if cond == "target_only" else ())
    _need(all(all(m in r for m in need) for r in out.values()), f"extra {cond} {n}: missing metrics")
    return out


def _mean(xs):
    xs = list(xs)
    assert xs and all(math.isfinite(x) for x in xs), "empty or non-finite subset"
    return statistics.fmean(xs)


def compare(cand, ctrls, snr_of):
    """Per-ear SI-SDR/STOI differences (cand - control) for every gating subset."""
    out = {}
    subsets = {f"noisy|{snr:+.0f}|{d}": ("noisy", [k for k in cand["noisy"] if snr_of[k[0]] == snr and f(k[1])])
               for snr in SNRS for d, f in DIRS.items()}
    subsets.update({f"target_only|{d}": ("target_only", [k for k in cand["target_only"] if f(k[1])]) for d, f in DIRS.items()})
    for sname, (cond, ks) in subsets.items():
        _need(len(ks) == (2 if cond == "noisy" else 8), f"subset {sname} has {len(ks)} scenes")
    for cname, ctrl in ctrls.items():
        for c in ("noisy", "target_only"):
            _need(set(ctrl[c]) == set(cand[c]) == GRID, f"{cname} {c} grid != candidate grid")
        for sname, (cond, ks) in subsets.items():
            for m in ("sisdr", "stoi"):
                diffs = [cand[cond][k][f"{m}_{e}"] - ctrl[cond][k][f"{m}_{e}"] for k in ks for e in ("L", "R")]
                out[f"{cname}|{sname}|{m}"] = _mean(diffs)
    return out


def judge(linked_p, g32_p, g19_p, g19_ctrl_p, g19_linked_p=None):
    J = _load_judge_v3()
    LK, G32, G19, G19C = (json.loads(Path(p).read_text()) for p in (linked_p, g32_p, g19_p, g19_ctrl_p))
    assert LK["meta"]["mode"] == "linked" and G32["meta"]["mode"] == "independent" and G19["meta"]["mode"] == "independent"
    assert LK["meta"]["checkpoint_sha256"] == G32["meta"]["checkpoint_sha256"], "linked and independent Gen32 must share weights"
    assert G19["meta"]["checkpoint_sha256"] == G19C["meta"]["checkpoint_sha256"]
    # the new independent Gen19 run must reproduce the registered control exactly
    assert G19["crossed_rows"] == G19C["crossed_rows"] and G19["existing"]["rows"] == G19C["existing"]["rows"]
    rep, sp = J.spatial_gates(LK, G19C, LK["meta"]["checkpoint_sha256"], G19C["meta"]["checkpoint_sha256"])
    L1 = sp["SP_spatial_existing_and_no_worsening"]
    lk, g32, g19 = _crossed(LK), _crossed(G32), _crossed(G19)
    ctrl_un = _keyed([r for r in G19C["crossed_rows"] if r["system"] == "unproc"], "crossed unproc (registered control)")
    for D in (LK, G32, G19):
        un = _keyed([r for r in D["crossed_rows"] if r["system"] == "unproc"], "crossed unproc")
        _need(all(un[k] == ctrl_un[k] for k in GRID), "unprocessed crossed scenes differ between documents")
        for c in ("noisy", "target_only"):
            ue = _keyed([r for r in D["extra_rows"] if r["system"] == "unproc" and r["cond"] == c], f"extra unproc {c}")
            ref = _keyed([r for r in LK["extra_rows"] if r["system"] == "unproc" and r["cond"] == c], f"extra unproc {c} (linked doc)")
            _need(all(ue[k] == ref[k] for k in GRID), f"unprocessed extra {c} rows differ between documents")
    snr_of = {k[0]: lk[k]["snr_db"] for k in lk}
    ild_lk, ild_32 = _mean(r["ild_target_err_db"] for r in lk.values()), _mean(r["ild_target_err_db"] for r in g32.values())
    L2 = ild_lk < ild_32
    l3 = {}
    for snr in SNRS:
        for d, f in DIRS.items():
            ks = [k for k in lk if snr_of[k[0]] == snr and f(k[1])]
            assert len(ks) == 2
            for m in ("ild_target_err_db", "itd_err_samples"):
                c, g = _mean(lk[k][m] for k in ks), _mean(g19[k][m] for k in ks)
                l3[f"{snr:+.0f}|{d}|{m}"] = {"linked": c, "gen19": g, "worsening": c - g}
    L3 = all(v["worsening"] <= 0 for v in l3.values())
    cand = {c: _extra(LK, c) for c in ("noisy", "target_only")}
    ctrls = {"gen32_indep": {c: _extra(G32, c) for c in ("noisy", "target_only")},
             "gen19_indep": {c: _extra(G19, c) for c in ("noisy", "target_only")}}
    l4 = compare(cand, ctrls, snr_of)
    L4 = all(v >= 0 for v in l4.values())
    # descriptive only (Muse pre-launch notes 1 and 4): each ear separately, worst ear, and target-only cue errors
    desc = {}
    for cname, ctrl in ctrls.items():
        for c in ("noisy", "target_only"):
            for m in ("sisdr", "stoi"):
                dl = [cand[c][k][f"{m}_L"] - ctrl[c][k][f"{m}_L"] for k in GRID]
                dr = [cand[c][k][f"{m}_R"] - ctrl[c][k][f"{m}_R"] for k in GRID]
                desc[f"{cname}|{c}|{m}"] = {"left_ear": _mean(dl), "right_ear": _mean(dr),
                                             "worst_ear_per_scene_mean": _mean(min(a, b) for a, b in zip(dl, dr))}
    for nm, ex in (("linked", cand["target_only"]), ("gen32_indep", ctrls["gen32_indep"]["target_only"]),
                   ("gen19_indep", ctrls["gen19_indep"]["target_only"])):
        desc[f"target_only_cues|{nm}"] = {m: _mean(ex[k][m] for k in GRID) for m in ("ild_target_err_db", "itd_err_samples")}
    checks = {"L1_original_SP": L1, "L2_mean_ILD_below_independent_gen32": L2,
              "L3_no_ILD_ITD_worsening_vs_gen19_any_subset": L3, "L4_per_ear_sisdr_stoi_nonnegative_vs_both": L4}
    doc = {"checks": checks, "verdict": "LINKAGE FEASIBILITY PASSED" if all(checks.values()) else "REJECTED",
           "sp_report": rep, "crossed_mean_ild": {"linked": ild_lk, "gen32_indep": ild_32,
                                                   "gen19_indep": _mean(r["ild_target_err_db"] for r in g19.values())},
           "L3": l3, "L4": l4, "descriptive": desc,
           "shas": {"gen32": G32["meta"]["checkpoint_sha256"], "gen19": G19["meta"]["checkpoint_sha256"]}}
    if g19_linked_p:  # descriptive only: linkage applied to the accepted baseline
        GL = json.loads(Path(g19_linked_p).read_text())
        assert GL["meta"]["mode"] == "linked" and GL["meta"]["checkpoint_sha256"] == G19["meta"]["checkpoint_sha256"]
        gl = _crossed(GL)
        doc["descriptive_gen19_linked"] = {
            "crossed_mean_ild": _mean(r["ild_target_err_db"] for r in gl.values()),
            "crossed_mean_itd": _mean(r["itd_err_samples"] for r in gl.values()),
            "per_ear_vs_gen19_indep": compare({c: _extra(GL, c) for c in ("noisy", "target_only")},
                                              {"gen19_indep": ctrls["gen19_indep"]}, snr_of)}
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--linked", required=True); ap.add_argument("--gen32", required=True)
    ap.add_argument("--gen19", required=True); ap.add_argument("--gen19-ctrl", required=True)
    ap.add_argument("--gen19-linked", default=None); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    doc = judge(a.linked, a.gen32, a.gen19, a.gen19_ctrl, a.gen19_linked)
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(json.dumps(doc["checks"]), doc["verdict"])
    print("crossed mean ILD", {k: round(v, 4) for k, v in doc["crossed_mean_ild"].items()})


if __name__ == "__main__":
    main()
