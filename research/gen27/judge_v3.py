"""Gen27 judgment (DRAFT for registration): Astra's gates, verbatim intent
(research/gen27/astra-agenda-review.md, item 5). Per seed, candidate minus
the same-seed Gen19 final. ADVANCE requires every gate:

 R1 reverberant primary (panel_rev 'synthetic': 16 voices x 6 held-out rooms
    x {-5, 0} dB): mean SI-SDR gain >= +0.30 dB, equal weight per
    (voice, room) cell (each cell averages its 4 crops x 4 crowds x 2 SNRs;
    the grid is balanced, so this is also equal weight per SNR);
    R1b paired 95% bootstrap lower bound > 0 resampling voices AND rooms
    independently (10,000 draws, seed 20261204);
    R1c >= 10/16 voice means > 0.
 C  consistency: mean SI-SDR gain >= 0 and mean STOI gain >= 0 in every
    (stratum in {synthetic, measured}) x (SNR in {-5, 0}) cell.
 D  dry screen (screen-v2 panel, unchanged): at -5 and at 0 dB, mean SI-SDR
    gain >= 0 and mean STOI gain >= 0; voice-bootstrap lower bounds
    (judge_v2.speaker_bootstrap) > -0.15 dB and > -0.003. An inconclusive
    safeguard (bound at or below the margin) does not pass.
 S2/S3 bench-v2 safeguards from judge_v2 (quiet >= 25 dB, dSTOI >= -0.02;
    crowd/SSN/white rows). Dry bench results by SNR, including -5 dB, are
    reported descriptively.
 SP spatial: existing gates (kpi_scorecard: candidate target-ILD error <
    unprocessed; ITD error <= unprocessed) on the existing spatial bench, plus
    no mean worsening vs Gen19 in target-ILD error or ITD error separately
    (a) at hard SNR (-5 dB scenes) and (b) for each mirrored direction set
    (targets left, targets right) of the extended crossed scenes.
 Provenance/completeness: registered rev material + RIR manifest + dry
    material hashes; control rows == Gen19 same-seed sha, candidate rows ==
    candidate sha (panel_rev, screen-v2, bench, spatial); complete,
    duplicate-free grids; every metric finite. Violations raise Invalid
    (verdict INVALID, never ADVANCE).
 Replication (`--replicate j17 j18 j19`): 3-seed mean primary gain >= +0.30,
    gain > 0 in >= 2/3 seeds, two-way clustered lower bound of the 3-seed
    cell means > 0, and C/D/S2/S3/SP pass in every seed.
These are engineering advancement thresholds, not clinical differences.

Usage:
  python research/gen27/judge_v3.py --rev R.json --panel P.json --bench B.json \
      --spatial-cand SC.json --spatial-ctrl SG.json --cand NAME --cand-sha SHA --seed 17 [--out J.json]
  python research/gen27/judge_v3.py --run-spatial CKPT --name NAME --out S.json
  python research/gen27/judge_v3.py --replicate J17.json J18.json J19.json
"""
from __future__ import annotations
import argparse, hashlib, json, math, statistics, subprocess, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parent
sys.path.insert(0, str(R / "screen_v2"))
import judge_v2  # noqa: E402

TARGETS = judge_v2.TARGETS
SNRS = (-5.0, 0.0)
BOOT_DRAWS, BOOT_SEED = 10000, 20261204
# Registered after the Gen19-vs-Gen19 self-test build (see prereg_draft.md).
REGISTERED_REV_MATERIAL = None  # filled by --register from the self-test output; None = refuse
REGISTERED_RIR_MANIFEST = None
REG_FILE = HERE / "registered_hashes.json"
if REG_FILE.exists():
    _reg = json.loads(REG_FILE.read_text())
    REGISTERED_REV_MATERIAL, REGISTERED_RIR_MANIFEST = _reg["rev_material_sha256"], _reg["rir_manifest_sha256"]

Invalid = judge_v2.Invalid
_need = judge_v2._need


def _finite(*xs):
    return all(isinstance(x, (int, float)) and math.isfinite(x) for x in xs)


def check_rev_grid(P, name, sha, n_synth_rooms=6, n_meas_rooms=6):
    rs = [r for r in P["rows"] if r["system"] == name]
    _need(len(rs) > 0 and {r["sha256"] for r in rs} == {sha}, f"rev {name} hash {({r['sha256'] for r in rs})} != {sha}")
    _need(all(_finite(r["d_sisdr"], r["d_stoi"], r["sisdr"], r["stoi"]) for r in rs), f"rev {name} has non-finite metrics")
    out = {}
    for st, nr in (("synthetic", n_synth_rooms), ("measured", n_meas_rooms)):
        sel = [r for r in rs if r["stratum"] == st]
        rooms = sorted({r["room_id"] for r in sel})
        _need(len(rooms) == nr, f"rev {name} {st}: {len(rooms)} rooms != {nr}")
        grid = {(rm, t, c, m, s) for rm in rooms for t in TARGETS for c in range(4) for m in range(4) for s in SNRS}
        ks = [(r["room_id"], r["spk"], r["crop"], r["mix"], r["snr"]) for r in sel]
        _need(len(ks) == len(set(ks)) and set(ks) == grid, f"rev {name} {st} grid incomplete or duplicated")
        out[st] = {k: r for k, r in zip(ks, sel)}
    to = [r for r in rs if r["stratum"] == "target_only"]
    rooms = sorted({r["room_id"] for r in to})
    ks = [(r["room_id"], r["spk"], r["crop"]) for r in to]
    _need(len(rooms) == n_synth_rooms + n_meas_rooms and len(ks) == len(set(ks))
          and set(ks) == {(rm, t, c) for rm in rooms for t in TARGETS for c in range(4)},
          f"rev {name} target-only grid incomplete or duplicated")
    out["target_only"] = {k: r for k, r in zip(ks, to)}
    return out


def two_way_bootstrap(cell, draws=BOOT_DRAWS, seed=BOOT_SEED):
    """cell: (n_voices, n_rooms) array of per-cell mean gains. Resample voices
    and rooms independently with replacement; mean over the drawn cross."""
    rng = np.random.default_rng(seed)
    nv, nr = cell.shape
    vi = rng.integers(0, nv, size=(draws, nv))
    ri = rng.integers(0, nr, size=(draws, nr))
    m = np.array([cell[np.ix_(vi[d], ri[d])].mean() for d in range(draws)])
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def rev_gates(P, cand, cand_sha, ctrl_sha):
    C = check_rev_grid(P, "control", ctrl_sha)
    X = check_rev_grid(P, cand, cand_sha)
    syn = C["synthetic"]
    rooms = sorted({k[0] for k in syn})
    d = {k: X["synthetic"][k]["d_sisdr"] - syn[k]["d_sisdr"] for k in syn}
    cell = np.array([[statistics.fmean(d[k] for k in syn if k[1] == t and k[0] == rm) for rm in rooms] for t in TARGETS])
    voice = cell.mean(1)
    gain = float(cell.mean())
    ci = two_way_bootstrap(cell)
    cons = {}
    for st in ("synthetic", "measured"):
        for s in SNRS:
            ks = [k for k in C[st] if k[4] == s]
            cons[f"{st}|{s}"] = {"sisdr": statistics.fmean(X[st][k]["d_sisdr"] - C[st][k]["d_sisdr"] for k in ks),
                                 "stoi": statistics.fmean(X[st][k]["d_stoi"] - C[st][k]["d_stoi"] for k in ks)}
    per_room = {rm: float(cell[:, j].mean()) for j, rm in enumerate(rooms)}
    to = {k: X["target_only"][k]["sisdr"] - C["target_only"][k]["sisdr"] for k in C["target_only"]}
    to_stoi = {k: X["target_only"][k]["d_stoi"] - C["target_only"][k]["d_stoi"] for k in C["target_only"]}
    report = {"primary_gain": gain, "primary_ci": ci, "per_voice": dict(zip(TARGETS, map(float, voice))),
              "voices_improved": int((voice > 0).sum()), "per_room": per_room, "rooms": rooms,
              "cell": cell.tolist(), "consistency": cons,
              "target_only_sisdr_gain": statistics.fmean(to.values()),
              "target_only_stoi_gain": statistics.fmean(to_stoi.values()),
              "target_only_cand_abs_sisdr": statistics.fmean(r["sisdr"] for r in X["target_only"].values())}
    checks = {"R1a_rev_gain_ge_0.30": _finite(gain) and gain >= 0.30,
              "R1b_voice_room_ci_lo_gt_0": _finite(ci[0]) and ci[0] > 0,
              "R1c_ge_10_of_16_voices": report["voices_improved"] >= 10,
              "C_consistency_each_snr_and_stratum": all(_finite(v["sisdr"], v["stoi"]) and v["sisdr"] >= 0 and v["stoi"] >= 0
                                                        for v in cons.values())}
    return report, checks


def dry_gates(panel_rows, cand, ctrl_sha, cand_sha):
    """Dry screen D on the screen-v2 panel rows (grid/hash checked by judge_v2)."""
    key = lambda r: (r["spk"], r["crop"], r["mix"], r["snr"])  # noqa: E731
    C = {key(r): r for r in panel_rows if r["system"] == "control"}
    X = {key(r): r for r in panel_rows if r["system"] == cand}
    _need(set(C) == set(X) == judge_v2.GRID, "dry panel grid mismatch")
    _need(all(_finite(r["d_sisdr"], r["d_stoi"]) for r in list(C.values()) + list(X.values())), "dry panel has non-finite metrics")
    rep, ok = {}, True
    for s in SNRS:
        ks = [k for k in judge_v2.GRID if k[3] == s]
        g = {k: X[k]["d_sisdr"] - C[k]["d_sisdr"] for k in ks}
        gt = {k: X[k]["d_stoi"] - C[k]["d_stoi"] for k in ks}
        pv = {t: statistics.fmean(g[k] for k in ks if k[0] == t) for t in TARGETS}
        pvt = {t: statistics.fmean(gt[k] for k in ks if k[0] == t) for t in TARGETS}
        lo, lo_t = judge_v2.speaker_bootstrap(pv)[0], judge_v2.speaker_bootstrap(pvt)[0]
        m, mt = statistics.fmean(g.values()), statistics.fmean(gt.values())
        rep[str(s)] = {"sisdr_gain": m, "stoi_gain": mt, "sisdr_lo": lo, "stoi_lo": lo_t}
        ok = ok and _finite(m, mt, lo, lo_t) and m >= 0 and mt >= 0 and lo > -0.15 and lo_t > -0.003
    return rep, {"D_dry_screen_both_snrs": ok}


def bench_by_snr(B):
    cand = B["meta"]["candidate"]
    out = {}
    for kind in sorted({r["kind"] for r in B["rows"]}):
        for snr in sorted({r["snr_db"] for r in B["rows"] if r["kind"] == kind}):
            c = {(r["spk"], r["crop"]): r for r in B["rows"] if r["system"] == cand and r["kind"] == kind and r["snr_db"] == snr}
            u = {(r["spk"], r["crop"]): r for r in B["rows"] if r["system"] == "unproc" and r["kind"] == kind and r["snr_db"] == snr}
            ks = sorted(set(c) & set(u))
            if ks:
                out[f"{kind}|{snr}"] = {"n": len(ks), "d_sisdr": statistics.fmean(c[k]["sisdr"] - u[k]["sisdr"] for k in ks),
                                        "d_stoi": statistics.fmean(c[k]["stoi"] - u[k]["stoi"] for k in ks)}
    return out


# ---------------- spatial safeguard ----------------
def run_spatial(ckpt, name, out):
    """Existing bench (subprocess, unchanged) + extended crossed scenes:
    the same 4 babble crops (SNR -5/0/5/10) x target azimuth {-60,-30,30,60}
    with the crowd at the mirror azimuth, rendered by spatial.render_at."""
    bench = R / "bench-n6"
    tmp = Path(out).with_suffix(".existing.json")
    r = subprocess.run([sys.executable, str(bench / "spatial_bench.py"), "--gen15", str(ckpt),
                        "--candidate-name", name, "--out", str(tmp)], capture_output=True, text=True, cwd=str(R.parent))
    _need(r.returncode == 0, f"spatial_bench failed: {r.stderr[-1500:]}")
    existing = json.loads(tmp.read_text())
    sys.path.insert(0, str(bench)); sys.path.insert(0, str(R / "gen15"))
    from bench import build_crops, load_gen15
    from spatial import ild_per_band, itd_samples, render_at
    from spatial_bench import TARGET_AZ
    crops = [c for c in build_crops(1) if c["kind"].startswith("babble")]
    enh = load_gen15(str(ckpt))
    rows = []
    for i, c in enumerate(crops):
        for taz in TARGET_AZ:
            cl, cr = render_at(c["clean"], taz)
            nl, nr = render_at(c["noise"], -taz)
            mL, mR = cl + nl, cr + nr
            ild_t, itd_t = ild_per_band(cl, cr), itd_samples(cl, cr)
            for sysname, (oL, oR) in (("unproc", (mL, mR)), (name, (enh(mL.copy()), enh(mR.copy())))):
                rows.append({"crop": i, "snr_db": c["snr_db"], "target_az": taz, "noise_az": -taz, "system": sysname,
                             "ild_target_err_db": float(np.mean(np.abs(ild_per_band(oL, oR) - ild_t))),
                             "itd_err_samples": float(abs(itd_samples(oL, oR) - itd_t))})
    sha = hashlib.sha256(Path(ckpt).read_bytes()).hexdigest()
    doc = {"meta": {"candidate": name, "checkpoint_sha256": sha, "ckpt": str(ckpt)},
           "existing": existing, "crossed_rows": rows,
           "note": "ASSUMED head model (spatial.py); crossed scenes = 4 crops x 4 target azimuths, crowd at mirror"}
    Path(out).write_text(json.dumps(doc, indent=1))
    return doc


def spatial_gates(SC, SG, cand_sha, ctrl_sha):
    _need(SC["meta"]["checkpoint_sha256"] == cand_sha and SC["existing"]["meta"]["checkpoint_sha256"] == cand_sha,
          "spatial candidate hash mismatch")
    _need(SG["meta"]["checkpoint_sha256"] == ctrl_sha and SG["existing"]["meta"]["checkpoint_sha256"] == ctrl_sha,
          "spatial control hash mismatch")
    cn, gn = SC["meta"]["candidate"], SG["meta"]["candidate"]
    s, unp = SC["existing"]["summary"][cn], SC["existing"]["summary"]["unproc"]
    mets = ("ild_target_err_db", "itd_err_samples")
    _need(_finite(*(s[m] for m in mets), *(unp[m] for m in mets)), "spatial existing summary non-finite")
    existing_ok = s["ild_target_err_db"] < unp["ild_target_err_db"] and s["itd_err_samples"] <= unp["itd_err_samples"]
    key = lambda r: (r["crop"], r["target_az"])  # noqa: E731
    c = {key(r): r for r in SC["crossed_rows"] if r["system"] == cn}
    g = {key(r): r for r in SG["crossed_rows"] if r["system"] == gn}
    _need(len(c) == len(g) == 16 and set(c) == set(g), "spatial crossed grid incomplete")
    _need(all(_finite(r[m]) for r in list(c.values()) + list(g.values()) for m in mets), "spatial crossed non-finite")
    subsets = {"hard_snr_-5": [k for k in c if c[k]["snr_db"] == -5.0],
               "mirror_left_targets": [k for k in c if k[1] < 0],
               "mirror_right_targets": [k for k in c if k[1] > 0]}
    rep, ok = {"existing": {"cand": {m: s[m] for m in mets}, "unproc": {m: unp[m] for m in mets}}}, existing_ok
    for nm, ks in subsets.items():
        _need(len(ks) > 0, f"spatial subset {nm} empty")
        rep[nm] = {}
        for m in mets:
            dc, dg = statistics.fmean(c[k][m] for k in ks), statistics.fmean(g[k][m] for k in ks)
            rep[nm][m] = {"cand": dc, "gen19": dg, "worsening": dc - dg}
            ok = ok and dc <= dg
    return rep, {"SP_spatial_existing_and_no_worsening": bool(ok)}


def judge(rev_p, panel_p, bench_p, sc_p, sg_p, cand, cand_sha, seed,
          reg_rev=None, reg_manifest=None):
    reg_rev = reg_rev or REGISTERED_REV_MATERIAL
    reg_manifest = reg_manifest or REGISTERED_RIR_MANIFEST
    _need(reg_rev is not None and reg_manifest is not None, "reverberant material/manifest hashes not registered")
    P = json.loads(Path(rev_p).read_text())
    _need(P.get("material_sha256") == reg_rev, f"rev material {P.get('material_sha256')} != registered")
    _need(P.get("rir_manifest_sha256") == reg_manifest, "rir manifest != registered")
    _need(P.get("dry_material_sha256") == judge_v2.REGISTERED_MATERIAL, "rev panel dry replay != screen-v2 material")
    v2_rows, v2_checks, _ = judge_v2.judge(panel_p, bench_p, cand, cand_sha, seed)  # provenance + S2/S3
    ctrl_sha = v2_rows["ctrl_sha"]
    rev_rep, rev_chk = rev_gates(P, cand, cand_sha, ctrl_sha)
    dry_rep, dry_chk = dry_gates(json.loads(Path(panel_p).read_text())["rows"], cand, ctrl_sha, cand_sha)
    B = json.loads(Path(bench_p).read_text())
    sp_rep, sp_chk = spatial_gates(json.loads(Path(sc_p).read_text()), json.loads(Path(sg_p).read_text()), cand_sha, ctrl_sha)
    checks = {**rev_chk, **dry_chk, "S2_quiet": v2_checks["S2_quiet"], "S3_other_rows": v2_checks["S3_other_rows"], **sp_chk}
    checks = {k: bool(v) for k, v in checks.items()}
    report = {"seed": seed, "cand": cand, "cand_sha": cand_sha, "ctrl_sha": ctrl_sha, "rev": rev_rep, "dry": dry_rep,
              "dry_v2_descriptive": {str(k): {kk: vv for kk, vv in v.items() if kk != "per_voice"} for k, v in v2_rows["panel"].items()},
              "bench_by_snr": bench_by_snr(B), "spatial": sp_rep}
    return report, checks, ("ADVANCE" if all(checks.values()) else "FAIL")


def replicate(paths):
    J = [json.loads(Path(p).read_text()) for p in paths]
    _need(len(J) == 3 and sorted(j["seed"] for j in J) == [17, 18, 19], "replication needs seeds 17, 18, 19")
    _need(all(j["verdict"] != "INVALID" for j in J), "a seed judgment is INVALID")
    rooms = J[0]["report"]["rev"]["rooms"]
    _need(all(j["report"]["rev"]["rooms"] == rooms for j in J), "room sets differ across seeds")
    cells = np.array([j["report"]["rev"]["cell"] for j in J])
    _need(np.isfinite(cells).all(), "non-finite cell gains")
    mean_cell = cells.mean(0)
    gains = [j["report"]["rev"]["primary_gain"] for j in J]
    lo = two_way_bootstrap(mean_cell)[0]
    safe = [k for k in J[0]["checks"] if not k.startswith("R1")]
    checks = {"three_seed_gain_ge_0.30": float(mean_cell.mean()) >= 0.30,
              "positive_in_ge_2_of_3": sum(g > 0 for g in gains) >= 2,
              "clustered_lo_gt_0": math.isfinite(lo) and lo > 0,
              "safeguards_every_seed": all(j["checks"][k] for j in J for k in safe)}
    return {"gains": gains, "three_seed_gain": float(mean_cell.mean()), "lo": lo}, checks, \
        ("RETAIN (fresh-material confirmation next)" if all(checks.values()) else "FAIL")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev"); ap.add_argument("--panel"); ap.add_argument("--bench")
    ap.add_argument("--spatial-cand"); ap.add_argument("--spatial-ctrl")
    ap.add_argument("--cand"); ap.add_argument("--cand-sha"); ap.add_argument("--seed", type=int, default=17)
    ap.add_argument("--run-spatial"); ap.add_argument("--name")
    ap.add_argument("--replicate", nargs=3)
    ap.add_argument("--register", nargs=2, metavar=("REV_PANEL_JSON", "MANIFEST"),
                    help="write registered_hashes.json from a self-test panel and the manifest")
    ap.add_argument("--out")
    a = ap.parse_args()
    if a.register:
        P = json.loads(Path(a.register[0]).read_text())
        REG_FILE.write_text(json.dumps({"rev_material_sha256": P["material_sha256"],
                                        "rir_manifest_sha256": hashlib.sha256(Path(a.register[1]).read_bytes()).hexdigest(),
                                        "dry_material_sha256": P["dry_material_sha256"]}, indent=1))
        print(REG_FILE.read_text()); return
    if a.run_spatial:
        doc = run_spatial(a.run_spatial, a.name, a.out)
        print(json.dumps(doc["existing"]["summary"], indent=1)); return
    if a.replicate:
        rep, checks, verdict = replicate(a.replicate)
        print(rep, checks, f"\nGEN27 REPLICATION {verdict}"); return
    try:
        report, checks, verdict = judge(a.rev, a.panel, a.bench, a.spatial_cand, a.spatial_ctrl, a.cand, a.cand_sha, a.seed)
    except Invalid as e:
        report, checks, verdict = {"error": str(e)}, {}, "INVALID"
        print(f"INVALID: {e}")
    if verdict != "INVALID":
        r = report["rev"]
        print(f"rev primary gain {r['primary_gain']:+.4f} dB (voice+room CI {r['primary_ci'][0]:+.3f}..{r['primary_ci'][1]:+.3f}), "
              f"voices improved {r['voices_improved']}/16")
        print("consistency", {k: (round(v['sisdr'], 4), round(v['stoi'], 5)) for k, v in r["consistency"].items()})
        print("dry", {k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in report["dry"].items()})
        print("target-only (descriptive)", round(r["target_only_sisdr_gain"], 4), round(r["target_only_stoi_gain"], 5))
        print("spatial", json.dumps(report["spatial"]))
    print(f"checks {checks}\nGEN27 SCREEN {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "report": report, "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
