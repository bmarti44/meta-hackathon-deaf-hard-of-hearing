"""Gen27 judgment: Astra's gates (research/gen27/astra-agenda-review.md,
item 5), revised per her pre-launch review (astra-prelaunch-review.md,
blocking 2 and 3, non-blocking target-only safeguard). Per seed, candidate
minus the same-seed Gen19 final. ADVANCE requires every gate:

 R1 reverberant primary (panel_rev 'synthetic': 16 voices x 6 held-out rooms
    x {-5, 0} dB): mean SI-SDR gain >= +0.30 dB, equal weight per
    (voice, room) cell (each cell averages its 4 crops x 4 crowds x 2 SNRs;
    the grid is balanced, so this is also equal weight per SNR);
    R1b paired 95% bootstrap lower bound > 0 resampling voices AND rooms
    independently (10,000 draws, seed 20261204);
    R1c >= 10/16 voice means > 0.
 C  consistency: mean SI-SDR gain >= 0 and mean STOI gain >= 0 in every
    (stratum in {synthetic, measured}) x (SNR in {-5, 0}) cell.
 T  target-only (superseding registration): mean SI-SDR gain >= 0 and mean
    STOI gain >= 0 on reverberant target-only items, separately for the
    synthetic-room and measured-room conditions. Passing it does not
    establish non-harm against bypass.
 D  dry screen (screen-v2 panel, unchanged): at -5 and at 0 dB, mean SI-SDR
    gain >= 0 and mean STOI gain >= 0; voice-bootstrap lower bounds
    (judge_v2.speaker_bootstrap) > -0.15 dB and > -0.003. An inconclusive
    safeguard (bound at or below the margin) does not pass.
 S2/S3 bench-v2 safeguards from judge_v2 (exact registered bench grid;
    summary recomputed from rows). Dry bench by kind x SNR, including -5 dB,
    reported descriptively.
 SP spatial: existing gates (kpi_scorecard: candidate target-ILD error <
    unprocessed; ITD error <= unprocessed), recomputed from the existing
    bench's validated rows, plus no mean worsening vs Gen19 in target-ILD or
    ITD error separately (a) at hard SNR (-5 dB scenes) and (b) for each
    mirrored direction set (targets left, targets right) of the crossed
    scenes. Under the symmetric head model with per-ear mono processing the
    two sides carry identical evidence (redundant, not vacuous).
 Provenance/completeness: registered rev material, RIR manifest (file sha)
    and dry material hashes; rooms (synthetic, measured AND target-only)
    exactly the manifest's eval rooms with matching strata; control rows ==
    Gen19 same-seed sha, candidate rows == candidate sha (panel_rev,
    screen-v2, bench, spatial); exact registered grids with duplicates
    rejected before any dict is built; scene metadata must match the
    registered scenes; every metric finite. Violations raise Invalid
    (verdict INVALID, never ADVANCE).
 Replication (`--replicate j17 j18 j19`): requires the seed-17 screen
    ADVANCE, the explicit safeguard keys (Boolean True in every seed),
    16 x 6 cells in the fixed voice/room order, matching registered hashes
    and Gen19 control hashes per seed, distinct candidate hashes; then
    3-seed mean primary gain >= +0.30, gain > 0 in >= 2/3 seeds, two-way
    clustered lower bound of the 3-seed cell means > 0.
These are engineering advancement thresholds, not clinical differences.

Usage:
  python research/gen27/judge_v3.py --rev R.json --panel P.json --bench B.json \
      --spatial-cand SC.json --spatial-ctrl SG.json --cand NAME --cand-sha SHA --seed 17 [--selftest] [--out J.json]
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
MANIFEST = HERE / "rir_manifest.json"
REG_FILE = HERE / "registered_hashes.json"
REGISTERED_REV_MATERIAL = REGISTERED_RIR_MANIFEST = None  # None = refuse to judge
if REG_FILE.exists():
    _reg = json.loads(REG_FILE.read_text())
    REGISTERED_REV_MATERIAL, REGISTERED_RIR_MANIFEST = _reg["rev_material_sha256"], _reg["rir_manifest_sha256"]
SAFEGUARDS = ("C_consistency_each_snr_and_stratum", "T_target_only_nonworsening", "D_dry_screen_both_snrs",
              "S2_quiet", "S3_other_rows", "SP_spatial_existing_and_no_worsening")
GAIN_GATES = ("R1a_rev_gain_ge_0.30", "R1b_voice_room_ci_lo_gt_0", "R1c_ge_10_of_16_voices")
# Registered spatial scenes (bench-n6/spatial_bench.py): babble crop i at SNR -5/0/5/10,
# target at TARGET_AZ[i], crowd at the mirror; systems below.
SP_SNR = (-5.0, 0.0, 5.0, 10.0)
SP_AZ = (-60.0, -30.0, 30.0, 60.0)
SP_EXISTING_BASE = ("unproc", "gate_independent", "gate_linked")
SP_METS = ("ild_target_err_db", "itd_err_samples")

Invalid = judge_v2.Invalid
_need = judge_v2._need


def _finite(*xs):
    return all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in xs)


def eval_rooms(manifest=MANIFEST):
    """Manifest eval rooms: {room_id: (stratum_label, rt60_stratum)} per split."""
    man = json.loads(Path(manifest).read_text())
    syn = {r["room_id"]: r["stratum"] for r in man["rooms"] if r["split"] == "eval_synth"}
    meas = {r["room_id"]: r["stratum"] for r in man["rooms"] if r["split"] == "eval_measured"}
    _need(len(syn) == 6 and len(meas) == 6, "manifest does not hold 6 + 6 eval rooms")
    return syn, meas


def _unique(keys, msg):
    _need(len(keys) == len(set(keys)), f"{msg}: duplicated rows")


def check_rev_grid(P, name, sha, syn_rooms, meas_rooms):
    rs = [r for r in P["rows"] if r["system"] == name]
    _need(len(rs) > 0 and {r["sha256"] for r in rs} == {sha}, f"rev {name} hash {({r['sha256'] for r in rs})} != {sha}")
    _need(all(_finite(r["d_sisdr"], r["d_stoi"], r["sisdr"], r["stoi"]) for r in rs), f"rev {name} has non-finite metrics")
    _need({r["stratum"] for r in rs} == {"synthetic", "measured", "target_only"}, f"rev {name} has unknown strata")
    out = {}
    for st, rooms in (("synthetic", syn_rooms), ("measured", meas_rooms)):
        sel = [r for r in rs if r["stratum"] == st]
        ks = [(r["room_id"], r["spk"], r["crop"], r["mix"], r["snr"]) for r in sel]
        _unique(ks, f"rev {name} {st}")
        grid = {(rm, t, c, m, s) for rm in rooms for t in TARGETS for c in range(4) for m in range(4) for s in SNRS}
        _need(set(ks) == grid, f"rev {name} {st} grid != manifest eval rooms x registered draws")
        _need(all(r["rt60_stratum"] == rooms[r["room_id"]] for r in sel), f"rev {name} {st} room strata != manifest")
        out[st] = dict(zip(ks, sel))
    to = [r for r in rs if r["stratum"] == "target_only"]
    ks = [(r["room_id"], r["spk"], r["crop"]) for r in to]
    _unique(ks, f"rev {name} target-only")
    allr = {**{k: ("synthetic", v) for k, v in syn_rooms.items()}, **{k: ("measured", v) for k, v in meas_rooms.items()}}
    _need(set(ks) == {(rm, t, c) for rm in allr for t in TARGETS for c in range(4)},
          f"rev {name} target-only grid != manifest eval rooms x registered crops")
    _need(all(r.get("room_stratum") == allr[r["room_id"]][0] and r["rt60_stratum"] == allr[r["room_id"]][1] for r in to),
          f"rev {name} target-only room labels != manifest")
    out["target_only"] = dict(zip(ks, to))
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


def rev_gates(P, cand, cand_sha, ctrl_sha, manifest=MANIFEST):
    syn_rooms, meas_rooms = eval_rooms(manifest)
    C = check_rev_grid(P, "control", ctrl_sha, syn_rooms, meas_rooms)
    X = check_rev_grid(P, cand, cand_sha, syn_rooms, meas_rooms)
    syn = C["synthetic"]
    rooms = sorted(syn_rooms)
    d = {k: X["synthetic"][k]["d_sisdr"] - syn[k]["d_sisdr"] for k in syn}
    cell = np.array([[statistics.fmean(d[k] for k in syn if k[1] == t and k[0] == rm) for rm in rooms] for t in TARGETS])
    voice = cell.mean(1)
    gain = float(cell.mean())
    ci = two_way_bootstrap(cell)
    cons, by_room = {}, {}
    for st in ("synthetic", "measured"):
        for s in SNRS:
            ks = [k for k in C[st] if k[4] == s]
            cons[f"{st}|{s}"] = {"sisdr": statistics.fmean(X[st][k]["d_sisdr"] - C[st][k]["d_sisdr"] for k in ks),
                                 "stoi": statistics.fmean(X[st][k]["d_stoi"] - C[st][k]["d_stoi"] for k in ks)}
        for rm in sorted({k[0] for k in C[st]}):  # room-by-room report (non-gating)
            by_room[rm] = {"stratum": st, "rt60_stratum": (syn_rooms if st == "synthetic" else meas_rooms)[rm]}
            for s in SNRS:
                ks = [k for k in C[st] if k[0] == rm and k[4] == s]
                by_room[rm][str(s)] = {"sisdr_gain": statistics.fmean(X[st][k]["d_sisdr"] - C[st][k]["d_sisdr"] for k in ks),
                                       "stoi_gain": statistics.fmean(X[st][k]["d_stoi"] - C[st][k]["d_stoi"] for k in ks),
                                       "control_d_sisdr": statistics.fmean(C[st][k]["d_sisdr"] for k in ks),
                                       "control_d_stoi": statistics.fmean(C[st][k]["d_stoi"] for k in ks)}
    T = C["target_only"]
    tgt = {}
    for st in ("synthetic", "measured"):
        ks = [k for k in T if T[k]["room_stratum"] == st]
        tgt[st] = {"sisdr_gain": statistics.fmean(X["target_only"][k]["sisdr"] - T[k]["sisdr"] for k in ks),
                   "stoi_gain": statistics.fmean(X["target_only"][k]["stoi"] - T[k]["stoi"] for k in ks),
                   "control_d_sisdr": statistics.fmean(T[k]["d_sisdr"] for k in ks),
                   "control_d_stoi": statistics.fmean(T[k]["d_stoi"] for k in ks),
                   "cand_abs_sisdr": statistics.fmean(X["target_only"][k]["sisdr"] for k in ks)}
    for rm in by_room:
        ks = [k for k in T if k[0] == rm]
        by_room[rm]["target_only"] = {"sisdr_gain": statistics.fmean(X["target_only"][k]["sisdr"] - T[k]["sisdr"] for k in ks),
                                      "stoi_gain": statistics.fmean(X["target_only"][k]["stoi"] - T[k]["stoi"] for k in ks),
                                      "control_d_sisdr": statistics.fmean(T[k]["d_sisdr"] for k in ks),
                                      "control_d_stoi": statistics.fmean(T[k]["d_stoi"] for k in ks)}
    report = {"primary_gain": gain, "primary_ci": ci, "voices": list(TARGETS), "rooms": rooms,
              "per_voice": dict(zip(TARGETS, map(float, voice))), "voices_improved": int((voice > 0).sum()),
              "per_room": {rm: float(cell[:, j].mean()) for j, rm in enumerate(rooms)},
              "cell": cell.tolist(), "consistency": cons, "target_only": tgt, "by_room": by_room}
    checks = {"R1a_rev_gain_ge_0.30": _finite(gain) and gain >= 0.30,
              "R1b_voice_room_ci_lo_gt_0": _finite(ci[0]) and ci[0] > 0,
              "R1c_ge_10_of_16_voices": report["voices_improved"] >= 10,
              "C_consistency_each_snr_and_stratum": all(_finite(v["sisdr"], v["stoi"]) and v["sisdr"] >= 0 and v["stoi"] >= 0
                                                        for v in cons.values()),
              "T_target_only_nonworsening": all(_finite(v["sisdr_gain"], v["stoi_gain"]) and v["sisdr_gain"] >= 0 and v["stoi_gain"] >= 0
                                                for v in tgt.values())}
    return report, checks


def dry_gates(panel_rows, cand, ctrl_sha, cand_sha):
    """Dry screen D on the screen-v2 panel rows (hash checked by judge_v2)."""
    key = lambda r: (r["spk"], r["crop"], r["mix"], r["snr"])  # noqa: E731
    cr = [r for r in panel_rows if r["system"] == "control"]
    xr = [r for r in panel_rows if r["system"] == cand]
    _unique([key(r) for r in cr], "dry control"); _unique([key(r) for r in xr], "dry candidate")
    C, X = {key(r): r for r in cr}, {key(r): r for r in xr}
    _need(set(C) == set(X) == judge_v2.GRID, "dry panel grid mismatch")
    _need(all(_finite(r["d_sisdr"], r["d_stoi"]) for r in cr + xr), "dry panel has non-finite metrics")
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
    """Descriptive: candidate - unprocessed per kind x SNR (grid already validated by judge_v2)."""
    cand = B["meta"]["candidate"]
    out = {}
    for kind in sorted({r["kind"] for r in B["rows"]}):
        for snr in sorted({r["snr_db"] for r in B["rows"] if r["kind"] == kind}):
            c = {r["crop"]: r for r in B["rows"] if r["system"] == cand and r["kind"] == kind and r["snr_db"] == snr}
            u = {r["crop"]: r for r in B["rows"] if r["system"] == "unproc" and r["kind"] == kind and r["snr_db"] == snr}
            out[f"{kind}|{snr}"] = {"n": len(c), "d_sisdr": statistics.fmean(c[k]["sisdr"] - u[k]["sisdr"] for k in c),
                                    "d_stoi": statistics.fmean(c[k]["stoi"] - u[k]["stoi"] for k in c)}
    return out


# ---------------- spatial safeguard ----------------
def run_spatial(ckpt, name, out):
    """Existing bench (subprocess, unchanged) + crossed scenes: the same 4
    babble crops (SNR -5/0/5/10) x target azimuth {-60,-30,30,60} with the
    crowd at the mirror azimuth, rendered by spatial.render_at."""
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


def _validate_existing(doc, name):
    """Existing-bench rows: exact registered scenes x systems, no duplicates,
    finite metrics; summary recomputed from rows (must equal the stored one)."""
    ex = doc["existing"]
    systems = SP_EXISTING_BASE + (name,)
    rows = ex["rows"]
    ks = [(r["crop"], r["system"]) for r in rows]
    _unique(ks, f"spatial existing {name}")
    _need(set(ks) == {(i, s) for i in range(4) for s in systems}, f"spatial existing {name} grid != registered scenes x systems")
    for r in rows:
        i = r["crop"]
        _need(r["snr_db"] == SP_SNR[i] and r["target_az"] == SP_AZ[i] and r["noise_az"] == -SP_AZ[i],
              f"spatial existing {name} scene {i} metadata != registered")
        _need(_finite(r["ild_target_err_db"], r["ild_distortion_db"], r["itd_err_samples"]), f"spatial existing {name} non-finite")
    summ = {s: {m: statistics.fmean(r[m] for r in rows if r["system"] == s) for m in SP_METS} for s in ("unproc", name)}
    for s in summ:
        for m in SP_METS:
            _need(math.isclose(summ[s][m], ex["summary"][s][m], rel_tol=1e-12, abs_tol=1e-12),
                  f"spatial existing {name} stored summary {s}/{m} != recomputed")
    return summ


def _validate_crossed(doc, name):
    rows = doc["crossed_rows"]
    ks = [(r["crop"], r["target_az"], r["system"]) for r in rows]
    _unique(ks, f"spatial crossed {name}")
    _need(set(ks) == {(i, az, s) for i in range(4) for az in SP_AZ for s in ("unproc", name)},
          f"spatial crossed {name} grid != registered 4 crops x 4 azimuths x 2 systems")
    for r in rows:
        _need(r["snr_db"] == SP_SNR[r["crop"]] and r["noise_az"] == -r["target_az"], f"spatial crossed {name} scene metadata != registered")
        _need(_finite(*(r[m] for m in SP_METS)), f"spatial crossed {name} non-finite")
    return {k: r for k, r in zip(ks, rows)}


def spatial_gates(SC, SG, cand_sha, ctrl_sha):
    _need(SC["meta"]["checkpoint_sha256"] == cand_sha and SC["existing"]["meta"]["checkpoint_sha256"] == cand_sha,
          "spatial candidate hash mismatch")
    _need(SG["meta"]["checkpoint_sha256"] == ctrl_sha and SG["existing"]["meta"]["checkpoint_sha256"] == ctrl_sha,
          "spatial control hash mismatch")
    cn, gn = SC["meta"]["candidate"], SG["meta"]["candidate"]
    _need(SC["existing"]["meta"]["candidate"] == cn and SG["existing"]["meta"]["candidate"] == gn, "spatial candidate names inconsistent")
    s = _validate_existing(SC, cn)
    _validate_existing(SG, gn)
    existing_ok = s[cn]["ild_target_err_db"] < s["unproc"]["ild_target_err_db"] and s[cn]["itd_err_samples"] <= s["unproc"]["itd_err_samples"]
    c, g = _validate_crossed(SC, cn), _validate_crossed(SG, gn)
    # the same scenes in both documents: unprocessed rows must agree exactly
    for i in range(4):
        for az in SP_AZ:
            _need(all(c[(i, az, "unproc")][m] == g[(i, az, "unproc")][m] for m in SP_METS),
                  "spatial candidate/control unprocessed scenes differ")
    subsets = {"hard_snr_-5": [(i, az) for i in range(4) for az in SP_AZ if SP_SNR[i] == -5.0],
               "mirror_left_targets": [(i, az) for i in range(4) for az in SP_AZ if az < 0],
               "mirror_right_targets": [(i, az) for i in range(4) for az in SP_AZ if az > 0]}
    rep, ok = {"existing": {"cand": s[cn], "unproc": s["unproc"]}}, existing_ok
    for nm, ks in subsets.items():
        rep[nm] = {}
        for m in SP_METS:
            dc = statistics.fmean(c[(i, az, cn)][m] for i, az in ks)
            dg = statistics.fmean(g[(i, az, gn)][m] for i, az in ks)
            rep[nm][m] = {"cand": dc, "gen19": dg, "worsening": dc - dg}
            ok = ok and dc <= dg
    return rep, {"SP_spatial_existing_and_no_worsening": bool(ok)}


def judge(rev_p, panel_p, bench_p, sc_p, sg_p, cand, cand_sha, seed,
          reg_rev=None, reg_manifest=None, manifest=MANIFEST, selftest=False):
    """selftest=True (CLI --selftest) is the only way the candidate may be the control itself."""
    reg_rev = reg_rev or REGISTERED_REV_MATERIAL
    reg_manifest = reg_manifest or REGISTERED_RIR_MANIFEST
    _need(reg_rev is not None and reg_manifest is not None, "reverberant material/manifest hashes not registered")
    _need(hashlib.sha256(Path(manifest).read_bytes()).hexdigest() == reg_manifest, "manifest file != registered")
    P = json.loads(Path(rev_p).read_text())
    _need(P.get("material_sha256") == reg_rev, f"rev material {P.get('material_sha256')} != registered")
    _need(P.get("rir_manifest_sha256") == reg_manifest, "rev panel manifest != registered")
    _need(P.get("dry_material_sha256") == judge_v2.REGISTERED_MATERIAL, "rev panel dry replay != screen-v2 material")
    v2_rows, v2_checks, _ = judge_v2.judge(panel_p, bench_p, cand, cand_sha, seed)  # provenance + S2/S3
    ctrl_sha = v2_rows["ctrl_sha"]
    _need(cand_sha != ctrl_sha or selftest, "candidate hash equals the control hash (only --selftest allows this)")
    rev_rep, rev_chk = rev_gates(P, cand, cand_sha, ctrl_sha, manifest)
    dry_rep, dry_chk = dry_gates(json.loads(Path(panel_p).read_text())["rows"], cand, ctrl_sha, cand_sha)
    B = json.loads(Path(bench_p).read_text())
    sp_rep, sp_chk = spatial_gates(json.loads(Path(sc_p).read_text()), json.loads(Path(sg_p).read_text()), cand_sha, ctrl_sha)
    checks = {**rev_chk, **dry_chk, "S2_quiet": v2_checks["S2_quiet"], "S3_other_rows": v2_checks["S3_other_rows"], **sp_chk}
    checks = {k: bool(v) for k, v in checks.items()}
    _need(set(checks) == set(GAIN_GATES) | set(SAFEGUARDS), "gate set != registered gate set")
    report = {"seed": seed, "cand": cand, "cand_sha": cand_sha, "ctrl_sha": ctrl_sha,
              "rev_material_sha256": reg_rev, "rir_manifest_sha256": reg_manifest,
              "dry_material_sha256": judge_v2.REGISTERED_MATERIAL, "rev": rev_rep, "dry": dry_rep,
              "dry_v2_descriptive": {str(k): {kk: vv for kk, vv in v.items() if kk != "per_voice"} for k, v in v2_rows["panel"].items()},
              "bench_by_snr": bench_by_snr(B), "spatial": sp_rep}
    return report, checks, ("ADVANCE" if all(checks.values()) else "FAIL")


def replicate(docs, manifest=MANIFEST, reg_rev=None, reg_manifest=None, gen19_dir=R / "gen19" / "weights"):
    """docs: three judge_v3 outputs (dicts) for seeds 17, 18, 19. Malformed
    documents (missing fields, wrong types) are INVALID, never RETAIN."""
    try:
        return _replicate(docs, manifest, reg_rev, reg_manifest, gen19_dir)
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        raise Invalid(f"malformed replication input: {e!r}")


def _replicate(docs, manifest, reg_rev, reg_manifest, gen19_dir):
    reg_rev = reg_rev or REGISTERED_REV_MATERIAL
    reg_manifest = reg_manifest or REGISTERED_RIR_MANIFEST
    _need(len(docs) == 3 and sorted(j.get("seed") for j in docs) == [17, 18, 19], "replication needs seeds 17, 18, 19")
    J = {j["seed"]: j for j in docs}
    _need(all(j.get("verdict") in ("ADVANCE", "FAIL") for j in docs), "a seed judgment is INVALID or missing")
    _need(J[17]["verdict"] == "ADVANCE", "seed-17 screen did not ADVANCE: replication not authorised")
    rooms = sorted(eval_rooms(manifest)[0])
    cand_shas = set()
    for s, j in J.items():
        rep, chk = j["report"], j["checks"]
        _need(set(chk) == set(GAIN_GATES) | set(SAFEGUARDS) and all(type(chk[k]) is bool for k in chk),
              f"seed {s}: checks are not exactly the registered Boolean gates")
        _need(rep["rev_material_sha256"] == reg_rev and rep["rir_manifest_sha256"] == reg_manifest
              and rep["dry_material_sha256"] == judge_v2.REGISTERED_MATERIAL, f"seed {s}: registered hashes differ")
        ctrl = hashlib.sha256((gen19_dir / f"causal_seed{20261100 + s}.pt").read_bytes()).hexdigest()
        _need(rep["ctrl_sha"] == ctrl, f"seed {s}: control is not Gen19 seed {s}")
        _need(rep["cand_sha"] != ctrl, f"seed {s}: candidate equals control")
        cand_shas.add(rep["cand_sha"])
        _need(rep["rev"]["voices"] == list(TARGETS) and rep["rev"]["rooms"] == rooms, f"seed {s}: voice/room order differs")
        cell = np.array(rep["rev"]["cell"], dtype=float)
        _need(cell.shape == (16, 6) and np.isfinite(cell).all(), f"seed {s}: cells are not 16 x 6 finite")
        _need(math.isclose(float(cell.mean()), rep["rev"]["primary_gain"], rel_tol=1e-9, abs_tol=1e-12),
              f"seed {s}: stored primary gain != cell mean")
    _need(len(cand_shas) == 3, "candidate hashes are not distinct across seeds")
    cells = np.array([J[s]["report"]["rev"]["cell"] for s in (17, 18, 19)], dtype=float)
    mean_cell = cells.mean(0)
    gains = [float(c.mean()) for c in cells]
    lo = two_way_bootstrap(mean_cell)[0]
    checks = {"three_seed_gain_ge_0.30": float(mean_cell.mean()) >= 0.30,
              "positive_in_ge_2_of_3": sum(g > 0 for g in gains) >= 2,
              "clustered_lo_gt_0": math.isfinite(lo) and lo > 0,
              "safeguards_every_seed": all(J[s]["checks"][k] is True for s in J for k in SAFEGUARDS)}
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
    ap.add_argument("--selftest", action="store_true", help="allow candidate == control (self-test only)")
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
        try:
            rep, checks, verdict = replicate([json.loads(Path(p).read_text()) for p in a.replicate])
        except Invalid as e:
            rep, checks, verdict = {"error": str(e)}, {}, "INVALID"
        print(rep, checks, f"\nGEN27 REPLICATION {verdict}"); return
    try:
        report, checks, verdict = judge(a.rev, a.panel, a.bench, a.spatial_cand, a.spatial_ctrl, a.cand, a.cand_sha, a.seed,
                                        selftest=a.selftest)
    except Invalid as e:
        report, checks, verdict = {"error": str(e)}, {}, "INVALID"
        print(f"INVALID: {e}")
    if verdict != "INVALID":
        r = report["rev"]
        print(f"rev primary gain {r['primary_gain']:+.4f} dB (voice+room CI {r['primary_ci'][0]:+.3f}..{r['primary_ci'][1]:+.3f}), "
              f"voices improved {r['voices_improved']}/16")
        print("consistency", {k: (round(v['sisdr'], 4), round(v['stoi'], 5)) for k, v in r["consistency"].items()})
        print("target-only", {k: (round(v['sisdr_gain'], 4), round(v['stoi_gain'], 5)) for k, v in r["target_only"].items()})
        print("dry", {k: {kk: round(vv, 4) for kk, vv in v.items()} for k, v in report["dry"].items()})
        for rm, v in r["by_room"].items():
            print(f"room {rm:24s} {v['stratum']:9s} {v['rt60_stratum']:6s} "
                  + " ".join(f"{s}: gain {v[s]['sisdr_gain']:+.3f}/{v[s]['stoi_gain']:+.4f} ctrl {v[s]['control_d_sisdr']:+.2f}/{v[s]['control_d_stoi']:+.4f}" for s in ("-5.0", "0.0"))
                  + f" | target-only ctrl {v['target_only']['control_d_sisdr']:+.2f}/{v['target_only']['control_d_stoi']:+.4f}")
        print("spatial", json.dumps(report["spatial"]))
    print(f"checks {checks}\nGEN27 SCREEN {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "report": report, "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
