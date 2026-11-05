"""judge_v3 (and judge_v2 bench completeness) on synthetic and real inputs.

Gate logic: zero gain fails only the gain gates; a uniform gain passes them;
the two-way bootstrap resamples rooms; the measured stratum, each SNR and
the target-only conditions are checked separately; the dry screen treats an
inconclusive bound as a failure; spatial worsening at hard SNR or on one
mirrored side fails.
Completeness (Astra Gen27 pre-launch review, blocking 2): NaN, missing,
duplicated, wrong-hash and wrong-room rows are INVALID; deleting the -5 dB
bench rows, deleting/duplicating a bench row or tampering with the stored
bench summary is INVALID; spatial duplicates, wrong crop IDs or scene
metadata, empty existing-bench rows and tampered summaries are INVALID.
Replication (blocking 3): her adversarial case (empty checks, 1x1 cells) is
INVALID, as are non-Boolean checks, wrong order, wrong control hashes,
repeated candidate hashes and a seed-17 screen that did not ADVANCE.
"""
import copy, hashlib, importlib.util, json, math
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


J = load("judge_v3", HERE / "judge_v3.py")
SYN = {f"syn{i}": ("short", "short", "medium", "medium", "long", "long")[i] for i in range(6)}
MEAS = {f"meas{i}": ("short", "short", "medium", "medium", "long", "long")[i] for i in range(6)}


@pytest.fixture(scope="module")
def man(tmp_path_factory):
    p = tmp_path_factory.mktemp("m") / "manifest.json"
    rooms = [{"room_id": k, "split": "eval_synth", "stratum": v} for k, v in SYN.items()] + \
            [{"room_id": k, "split": "eval_measured", "stratum": v} for k, v in MEAS.items()] + \
            [{"room_id": "trainroom", "split": "train", "stratum": "short"}]
    p.write_text(json.dumps({"rooms": rooms}))
    return p


def rev_panel(gain_fn=lambda st, rm, t, s: 0.0, stoi_fn=lambda st, rm, t, s: 0.0, to_fn=lambda st: (0.0, 0.0), seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for st, rooms in (("synthetic", SYN), ("measured", MEAS)):
        for rm, rt in rooms.items():
            for t in J.TARGETS:
                for c in range(4):
                    for m in range(4):
                        for s in J.SNRS:
                            base, bt = float(rng.normal(3, 1)), float(rng.normal(0.05, 0.02))
                            common = {"stratum": st, "room_id": rm, "rt60_stratum": rt, "spk": t, "crop": c, "mix": m,
                                      "snr": s, "sisdr": 5.0, "stoi": 0.8}
                            rows.append({"system": "control", "sha256": "C", **common, "d_sisdr": base, "d_stoi": bt})
                            rows.append({"system": "cand", "sha256": "X", **common,
                                         "d_sisdr": base + gain_fn(st, rm, t, s), "d_stoi": bt + stoi_fn(st, rm, t, s)})
            for t in J.TARGETS:
                for c in range(4):
                    dg, dt = to_fn(st)
                    for sysn, sha, g, gt in (("control", "C", 0.0, 0.0), ("cand", "X", dg, dt)):
                        rows.append({"system": sysn, "sha256": sha, "stratum": "target_only", "room_stratum": st,
                                     "room_id": rm, "rt60_stratum": rt, "spk": t, "crop": c, "mix": None, "snr": None,
                                     "sisdr": 20.0 + g, "stoi": 0.95 + gt, "d_sisdr": g, "d_stoi": gt})
    return {"rows": rows}


def test_zero_gain_fails_gain_gates_only(man):
    rep, chk = J.rev_gates(rev_panel(), "cand", "X", "C", man)
    assert rep["primary_gain"] == 0.0 and rep["voices_improved"] == 0
    assert {k for k, v in chk.items() if not v} == {"R1a_rev_gain_ge_0.30", "R1b_voice_room_ci_lo_gt_0", "R1c_ge_10_of_16_voices"}
    assert set(rep["by_room"]) == set(SYN) | set(MEAS)  # room-by-room report


def test_uniform_gain_passes_primary(man):
    rep, chk = J.rev_gates(rev_panel(lambda *a: 0.5, lambda *a: 0.001), "cand", "X", "C", man)
    assert abs(rep["primary_gain"] - 0.5) < 1e-9 and all(chk.values())


def test_room_resampling_widens_interval(man):
    g = lambda st, rm, t, s: 3.6 if rm == "syn0" else -0.12  # noqa: E731
    rep, chk = J.rev_gates(rev_panel(g), "cand", "X", "C", man)
    assert chk["R1a_rev_gain_ge_0.30"] and rep["primary_ci"][0] <= 0 and not chk["R1b_voice_room_ci_lo_gt_0"]


def test_measured_stratum_and_snr_consistency_separate(man):
    _, chk = J.rev_gates(rev_panel(lambda st, rm, t, s: 0.5 if st == "synthetic" else -0.01), "cand", "X", "C", man)
    assert chk["R1a_rev_gain_ge_0.30"] and not chk["C_consistency_each_snr_and_stratum"]
    _, chk2 = J.rev_gates(rev_panel(lambda st, rm, t, s: 1.0 if s == -5.0 else -0.01), "cand", "X", "C", man)
    assert chk2["R1a_rev_gain_ge_0.30"] and not chk2["C_consistency_each_snr_and_stratum"]
    _, chk3 = J.rev_gates(rev_panel(lambda *a: 0.5, lambda st, rm, t, s: -0.001 if s == 0.0 else 0.0), "cand", "X", "C", man)
    assert not chk3["C_consistency_each_snr_and_stratum"]


@pytest.mark.parametrize("which,vals", [("measured", (-0.01, 0.0)), ("synthetic", (0.0, -0.001)), ("measured", (0.0, -0.001))])
def test_target_only_safeguard_separate_conditions(man, which, vals):
    _, chk = J.rev_gates(rev_panel(lambda *a: 0.5, lambda *a: 0.001, lambda st: vals if st == which else (0.1, 0.01)),
                         "cand", "X", "C", man)
    assert chk["R1a_rev_gain_ge_0.30"] and not chk["T_target_only_nonworsening"]


@pytest.mark.parametrize("mut", ["nan", "drop", "dup", "hash", "wrong_room", "to_wrong_room", "to_drop_room", "stratum_label"])
def test_rev_invalid_inputs(man, mut):
    P = rev_panel()
    rows = P["rows"]
    if mut == "nan":
        rows[7]["d_sisdr"] = float("nan")
    elif mut == "drop":
        del rows[11]
    elif mut == "dup":
        rows.append(copy.deepcopy(rows[3]))
    elif mut == "hash":
        rows[5]["sha256"] = "other"
    elif mut == "wrong_room":  # rename a synthetic room: counts stay 6, ids no longer match the manifest
        for r in rows:
            if r["room_id"] == "syn3" and r["stratum"] != "target_only":
                r["room_id"] = "trainroom"
    elif mut == "to_wrong_room":  # target-only rooms must match the manifest too
        for r in rows:
            if r["room_id"] == "meas2" and r["stratum"] == "target_only":
                r["room_id"] = "trainroom"
    elif mut == "to_drop_room":
        P["rows"] = [r for r in rows if not (r["stratum"] == "target_only" and r["room_id"] == "syn1")]
    else:
        for r in rows:
            if r["room_id"] == "syn0":
                r["rt60_stratum"] = "long"
    with pytest.raises(J.Invalid):
        J.rev_gates(P, "cand", "X", "C", man)


def dry_rows(gain=0.0, stoi=0.0, spread=0.0):
    rows = []
    for t, c, m, s in sorted(J.judge_v2.GRID):
        jit = spread * (1 if J.TARGETS.index(t) % 2 else -1)
        rows.append({"system": "control", "spk": t, "crop": c, "mix": m, "snr": s, "d_sisdr": 2.0, "d_stoi": 0.03})
        rows.append({"system": "cand", "spk": t, "crop": c, "mix": m, "snr": s, "d_sisdr": 2.0 + gain + jit, "d_stoi": 0.03 + stoi})
    return rows


def test_dry_screen():
    assert J.dry_gates(dry_rows(), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]
    assert not J.dry_gates(dry_rows(gain=-0.01), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]
    assert not J.dry_gates(dry_rows(spread=0.6), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]  # inconclusive -> FAIL
    bad = dry_rows(); bad[4]["d_stoi"] = float("nan")
    with pytest.raises(J.Invalid):
        J.dry_gates(bad, "cand", "C", "X")
    dup = dry_rows(); dup.append(copy.deepcopy(dup[1]))
    with pytest.raises(J.Invalid):
        J.dry_gates(dup, "cand", "C", "X")


# ---------------- spatial ----------------
def spatial_doc(name, sha, worsen=None):
    ex_rows = []
    for i in range(4):
        for s in J.SP_EXISTING_BASE + (name,):
            ex_rows.append({"crop": i, "target_az": J.SP_AZ[i], "noise_az": -J.SP_AZ[i], "snr_db": J.SP_SNR[i], "system": s,
                            "ild_target_err_db": 6.0 if s == "unproc" else 5.0, "ild_distortion_db": 0.5,
                            "itd_err_samples": 5.75 if s == "unproc" else 4.0})
    summ = {s: {m: float(np.mean([r[m] for r in ex_rows if r["system"] == s])) for m in ("ild_target_err_db", "ild_distortion_db", "itd_err_samples")}
            for s in J.SP_EXISTING_BASE + (name,)}
    rows = []
    for i in range(4):
        for az in J.SP_AZ:
            for s in ("unproc", name):
                ild = 7.0 if s == "unproc" else 5.0
                if s == name and worsen and worsen(J.SP_SNR[i], az):
                    ild += 0.2
                rows.append({"crop": i, "snr_db": J.SP_SNR[i], "target_az": az, "noise_az": -az, "system": s,
                             "ild_target_err_db": ild, "itd_err_samples": 4.0})
    return {"meta": {"candidate": name, "checkpoint_sha256": sha},
            "existing": {"meta": {"candidate": name, "checkpoint_sha256": sha}, "summary": summ, "rows": ex_rows},
            "crossed_rows": rows}


def test_spatial_gates():
    sg = spatial_doc("gen19", "C")
    assert J.spatial_gates(spatial_doc("cand", "X"), sg, "X", "C")[1]["SP_spatial_existing_and_no_worsening"]
    assert not J.spatial_gates(spatial_doc("cand", "X", lambda s, az: s == -5.0), sg, "X", "C")[1]["SP_spatial_existing_and_no_worsening"]
    assert not J.spatial_gates(spatial_doc("cand", "X", lambda s, az: az < 0 and s == 10.0), sg, "X", "C")[1]["SP_spatial_existing_and_no_worsening"]


def _sp_mut(mut):
    d = spatial_doc("cand", "X")
    if mut == "hash":
        d["meta"]["checkpoint_sha256"] = "Y"
    elif mut == "nan":
        d["crossed_rows"][2]["itd_err_samples"] = float("nan")
    elif mut == "dup_crossed":
        d["crossed_rows"].append(copy.deepcopy(d["crossed_rows"][0]))
    elif mut == "dup_existing":
        d["existing"]["rows"].append(copy.deepcopy(d["existing"]["rows"][3]))
    elif mut == "wrong_crop":
        d["crossed_rows"][5]["crop"] = 7
    elif mut == "wrong_scene_snr":
        d["crossed_rows"][5]["snr_db"] = 10.0 if d["crossed_rows"][5]["snr_db"] != 10.0 else -5.0
    elif mut == "wrong_noise_az":
        d["existing"]["rows"][0]["noise_az"] = d["existing"]["rows"][0]["target_az"]
    elif mut == "empty_existing_rows":  # summaries remain, rows gone
        d["existing"]["rows"] = []
    elif mut == "tampered_summary":
        d["existing"]["summary"]["cand"]["ild_target_err_db"] = 1.0
    elif mut == "unproc_differs":
        next(r for r in d["crossed_rows"] if r["system"] == "unproc")["ild_target_err_db"] += 0.5
    return d


@pytest.mark.parametrize("mut", ["hash", "nan", "dup_crossed", "dup_existing", "wrong_crop", "wrong_scene_snr", "wrong_noise_az",
                                 "empty_existing_rows", "tampered_summary", "unproc_differs"])
def test_spatial_invalid(mut):
    with pytest.raises(J.Invalid):
        J.spatial_gates(_sp_mut(mut), spatial_doc("gen19", "C"), "X", "C")


def test_two_way_bootstrap_deterministic_and_zero():
    assert J.two_way_bootstrap(np.zeros((16, 6))) == (0.0, 0.0)
    c = np.random.default_rng(1).normal(0.4, 0.3, (16, 6))
    lo, hi = J.two_way_bootstrap(c)
    assert J.two_way_bootstrap(c) == (lo, hi) and lo < c.mean() < hi and math.isfinite(lo)


# ---------------- judge_v2 bench completeness (real bench file) ----------------
BENCH = HERE.parent / "bench-n6" / "bench_v2_gen19.json"
V2PANEL = HERE.parent / "screen_v2" / "selftest" / "panel_gen19_vs_gen19_s17.json"
SHA19 = "80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367"
_need_bench = pytest.mark.skipif(not (BENCH.exists() and V2PANEL.exists()), reason="bench/panel files absent")


@_need_bench
def test_judge_v2_selftest_unchanged():
    _, chk, verdict = J.judge_v2.judge(V2PANEL, BENCH, "selftest", SHA19, 17)
    assert verdict == "FAIL" and chk["S2_quiet"] and chk["S3_other_rows"]
    ref = json.loads((HERE.parent / "screen_v2" / "selftest" / "judge_selftest_s17.json").read_text())
    assert chk == ref["checks"]


@_need_bench
@pytest.mark.parametrize("mut", ["drop_all_m5", "drop_one_unproc", "dup_cand", "tampered_summary", "wrong_spk", "nan"])
def test_judge_v2_bench_invalid(tmp_path, mut):
    B = json.loads(BENCH.read_text())
    if mut == "drop_all_m5":  # Astra's demonstration: S2/S3 used to pass with every -5 dB row deleted
        B["rows"] = [r for r in B["rows"] if r["snr_db"] != -5.0]
    elif mut == "drop_one_unproc":
        B["rows"].remove(next(r for r in B["rows"] if r["system"] == "unproc" and r["kind"] == "ssn"))
    elif mut == "dup_cand":
        B["rows"].append(copy.deepcopy(next(r for r in B["rows"] if r["system"] == "gen19")))
    elif mut == "tampered_summary":
        B["summary"]["gen19"]["crowd"]["d_sisdr"]["ci_lo"] = 9.0
    elif mut == "wrong_spk":
        next(r for r in B["rows"] if r["system"] == "gen19" and r["kind"] == "crowd")["spk"] = "84"
    else:
        next(r for r in B["rows"] if r["system"] == "unproc" and r["kind"] == "quiet")["stoi"] = float("nan")
    p = tmp_path / "b.json"; p.write_text(json.dumps(B))
    with pytest.raises(J.Invalid):
        J.judge_v2.judge(V2PANEL, p, "selftest", SHA19, 17)


# ---------------- replication (blocking 3) ----------------
def _gen19(tmp_path):
    d = tmp_path / "g19"; d.mkdir(exist_ok=True)
    for s in (17, 18, 19):
        (d / f"causal_seed{20261100 + s}.pt").write_bytes(f"ctrl{s}".encode())
    return d, {s: hashlib.sha256(f"ctrl{s}".encode()).hexdigest() for s in (17, 18, 19)}


def _seed_doc(seed, ctrl, gain=0.5, verdict="ADVANCE"):
    cell = np.full((16, 6), gain)
    checks = {k: True for k in J.GAIN_GATES + J.SAFEGUARDS}
    return {"seed": seed, "verdict": verdict, "checks": checks,
            "report": {"rev_material_sha256": "RM", "rir_manifest_sha256": "MS", "dry_material_sha256": J.judge_v2.REGISTERED_MATERIAL,
                       "ctrl_sha": ctrl, "cand_sha": f"cand{seed}",
                       "rev": {"voices": list(J.TARGETS), "rooms": sorted(SYN), "cell": cell.tolist(), "primary_gain": float(cell.mean())}}}


def _rep(docs, man, g19):
    return J.replicate(docs, manifest=man, reg_rev="RM", reg_manifest="MS", gen19_dir=g19)


def test_replication_valid_retains_and_safeguard_failure_fails(man, tmp_path):
    g19, c = _gen19(tmp_path)
    docs = [_seed_doc(s, c[s]) for s in (17, 18, 19)]
    assert _rep(docs, man, g19)[2].startswith("RETAIN")
    docs[2]["checks"]["SP_spatial_existing_and_no_worsening"] = False; docs[2]["verdict"] = "FAIL"
    assert _rep(docs, man, g19)[2] == "FAIL"


def test_replication_astra_adversarial_case_invalid(man, tmp_path):
    g19, c = _gen19(tmp_path)
    docs = [{"seed": s, "verdict": "ADVANCE", "checks": {},
             "report": {"rev": {"cell": [[1.0]], "primary_gain": 1.0, "rooms": ["x"]}}} for s in (17, 18, 19)]
    with pytest.raises(J.Invalid):
        _rep(docs, man, g19)


@pytest.mark.parametrize("mut", ["empty_checks", "non_bool", "missing_key", "cell_1x1", "room_order", "voice_order",
                                 "ctrl_hash", "same_cand", "s17_fail", "reg_hash", "gain_mismatch", "nan_cell"])
def test_replication_invalid(man, tmp_path, mut):
    g19, c = _gen19(tmp_path)
    docs = [_seed_doc(s, c[s]) for s in (17, 18, 19)]
    d = docs[1]
    if mut == "empty_checks":
        d["checks"] = {}
    elif mut == "non_bool":
        d["checks"]["D_dry_screen_both_snrs"] = 1
    elif mut == "missing_key":
        del d["checks"]["T_target_only_nonworsening"]
    elif mut == "cell_1x1":
        d["report"]["rev"]["cell"] = [[0.5]]
    elif mut == "room_order":
        d["report"]["rev"]["rooms"] = list(reversed(d["report"]["rev"]["rooms"]))
    elif mut == "voice_order":
        d["report"]["rev"]["voices"] = list(reversed(J.TARGETS))
    elif mut == "ctrl_hash":
        d["report"]["ctrl_sha"] = c[17]
    elif mut == "same_cand":
        d["report"]["cand_sha"] = docs[0]["report"]["cand_sha"]
    elif mut == "s17_fail":
        docs[0]["verdict"] = "FAIL"
    elif mut == "reg_hash":
        d["report"]["rir_manifest_sha256"] = "old"
    elif mut == "gain_mismatch":
        d["report"]["rev"]["primary_gain"] = 2.0
    else:
        d["report"]["rev"]["cell"][0][0] = float("nan")
    with pytest.raises(J.Invalid):
        _rep(docs, man, g19)


# ---------------- real self-test files ----------------
ST = HERE / "selftest"
_need_st = pytest.mark.skipif(not (ST / "panel_rev_gen19_vs_gen19_s17.json").exists(), reason="self-test material not built")


def _real(**kw):
    return J.judge(ST / "panel_rev_gen19_vs_gen19_s17.json", V2PANEL, BENCH,
                   ST / "spatial_selftest_s17.json", ST / "spatial_gen19_s17.json", "selftest", SHA19, 17, **kw)


@_need_st
def test_selftest_gen19_vs_itself_fails_only_gain_gates():
    rep, chk, verdict = _real(selftest=True)
    assert verdict == "FAIL" and rep["rev"]["primary_gain"] == 0.0
    assert {k for k, v in chk.items() if not v} == set(J.GAIN_GATES)


@_need_st
def test_selftest_guards():
    with pytest.raises(J.Invalid):
        _real(selftest=True, reg_rev="0" * 64)        # wrong registered material
    with pytest.raises(J.Invalid):
        _real()                                        # candidate == control without --selftest
    with pytest.raises(J.Invalid):
        _real(selftest=True, reg_manifest="0bc488e1ccbe8e90b23b070ca05eec269981671ad83bc64f31d7672daade272b")  # v1 manifest
