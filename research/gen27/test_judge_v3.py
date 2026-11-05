"""judge_v3 gate logic on synthetic inputs: zero gain fails the gain gates;
a uniform gain passes them; the two-way bootstrap resamples rooms; the
measured stratum and each SNR are checked separately; NaN, missing and
duplicated rows are INVALID; the dry screen treats an inconclusive bound as
a failure; spatial worsening at hard SNR or on one mirrored side fails."""
import copy, importlib.util, math
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
SYN = [f"syn{i}" for i in range(6)]
MEAS = [f"meas{i}" for i in range(6)]


def rev_panel(gain_fn=lambda st, rm, t, s: 0.0, stoi_fn=lambda st, rm, t, s: 0.0, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for st, rooms in (("synthetic", SYN), ("measured", MEAS)):
        for rm in rooms:
            for t in J.TARGETS:
                for c in range(4):
                    for m in range(4):
                        for s in J.SNRS:
                            base, bt = float(rng.normal(3, 1)), float(rng.normal(0.05, 0.02))
                            common = {"stratum": st, "room_id": rm, "spk": t, "crop": c, "mix": m, "snr": s,
                                      "sisdr": 5.0, "stoi": 0.8}
                            rows.append({"system": "control", "sha256": "C", **common, "d_sisdr": base, "d_stoi": bt})
                            rows.append({"system": "cand", "sha256": "X", **common,
                                         "d_sisdr": base + gain_fn(st, rm, t, s), "d_stoi": bt + stoi_fn(st, rm, t, s)})
    for rm in SYN + MEAS:
        for t in J.TARGETS:
            for c in range(4):
                for sysn, sha in (("control", "C"), ("cand", "X")):
                    rows.append({"system": sysn, "sha256": sha, "stratum": "target_only", "room_id": rm, "spk": t,
                                 "crop": c, "mix": None, "snr": None, "sisdr": 20.0, "stoi": 0.95, "d_sisdr": 0.0, "d_stoi": 0.0})
    return {"rows": rows}


def test_zero_gain_fails_gain_gates_only():
    rep, chk = J.rev_gates(rev_panel(), "cand", "X", "C")
    assert rep["primary_gain"] == 0.0 and rep["voices_improved"] == 0
    assert not chk["R1a_rev_gain_ge_0.30"] and not chk["R1b_voice_room_ci_lo_gt_0"] and not chk["R1c_ge_10_of_16_voices"]
    assert chk["C_consistency_each_snr_and_stratum"]


def test_uniform_gain_passes_primary():
    rep, chk = J.rev_gates(rev_panel(lambda *a: 0.5, lambda *a: 0.001), "cand", "X", "C")
    assert abs(rep["primary_gain"] - 0.5) < 1e-9 and all(chk.values())


def test_room_resampling_widens_interval():
    # one synthetic room carries all the gain: mean 0.5 but rooms disagree
    g = lambda st, rm, t, s: 3.6 if rm == "syn0" else -0.12  # noqa: E731
    rep, chk = J.rev_gates(rev_panel(g, lambda *a: 0.0), "cand", "X", "C")
    assert rep["primary_gain"] >= 0.30 and chk["R1a_rev_gain_ge_0.30"]
    assert rep["primary_ci"][0] <= 0 and not chk["R1b_voice_room_ci_lo_gt_0"]


def test_measured_stratum_and_snr_consistency_separate():
    g = lambda st, rm, t, s: 0.5 if st == "synthetic" else -0.01  # noqa: E731
    _, chk = J.rev_gates(rev_panel(g), "cand", "X", "C")
    assert chk["R1a_rev_gain_ge_0.30"] and not chk["C_consistency_each_snr_and_stratum"]
    g2 = lambda st, rm, t, s: 1.0 if s == -5.0 else -0.01  # noqa: E731
    _, chk2 = J.rev_gates(rev_panel(g2), "cand", "X", "C")
    assert chk2["R1a_rev_gain_ge_0.30"] and not chk2["C_consistency_each_snr_and_stratum"]
    st = lambda st, rm, t, s: -0.001 if s == 0.0 else 0.0  # noqa: E731
    _, chk3 = J.rev_gates(rev_panel(lambda *a: 0.5, st), "cand", "X", "C")
    assert not chk3["C_consistency_each_snr_and_stratum"]


@pytest.mark.parametrize("mut", ["nan", "drop", "dup", "hash"])
def test_rev_invalid_inputs(mut):
    P = rev_panel()
    if mut == "nan":
        P["rows"][7]["d_sisdr"] = float("nan")
    elif mut == "drop":
        del P["rows"][11]
    elif mut == "dup":
        P["rows"].append(copy.deepcopy(P["rows"][3]))
    else:
        P["rows"][5]["sha256"] = "other"
    with pytest.raises(J.Invalid):
        J.rev_gates(P, "cand", "X", "C")


def dry_rows(gain=0.0, stoi=0.0, spread=0.0):
    rows = []
    for t, c, m, s in sorted(J.judge_v2.GRID):
        jit = spread * (1 if J.TARGETS.index(t) % 2 else -1)
        rows.append({"system": "control", "spk": t, "crop": c, "mix": m, "snr": s, "d_sisdr": 2.0, "d_stoi": 0.03})
        rows.append({"system": "cand", "spk": t, "crop": c, "mix": m, "snr": s, "d_sisdr": 2.0 + gain + jit, "d_stoi": 0.03 + stoi})
    return rows


def test_dry_screen():
    assert J.dry_gates(dry_rows(), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]  # zero difference passes (>= 0, lo 0 > -0.15)
    assert not J.dry_gates(dry_rows(gain=-0.01), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]
    # mean exactly 0 but voices split +-0.6: lower bound <= -0.15 -> inconclusive -> FAIL
    assert not J.dry_gates(dry_rows(spread=0.6), "cand", "C", "X")[1]["D_dry_screen_both_snrs"]
    bad = dry_rows(); bad[4]["d_stoi"] = float("nan")
    with pytest.raises(J.Invalid):
        J.dry_gates(bad, "cand", "C", "X")


def spatial_doc(name, sha, worsen=None):
    rows = []
    snrs = [-5.0, 0.0, 5.0, 10.0]
    for i in range(4):
        for az in (-60.0, -30.0, 30.0, 60.0):
            ild, itd = 5.0, 4.0
            if worsen and worsen(snrs[i], az):
                ild += 0.2
            rows.append({"crop": i, "snr_db": snrs[i], "target_az": az, "system": name, "ild_target_err_db": ild, "itd_err_samples": itd})
    ex = {"meta": {"checkpoint_sha256": sha}, "summary": {name: {"ild_target_err_db": 5.0, "itd_err_samples": 4.0},
                                                          "unproc": {"ild_target_err_db": 6.0, "itd_err_samples": 5.75}}}
    return {"meta": {"candidate": name, "checkpoint_sha256": sha}, "existing": ex, "crossed_rows": rows}


def test_spatial_gates():
    ok = J.spatial_gates(spatial_doc("cand", "X"), spatial_doc("gen19", "C"), "X", "C")[1]
    assert ok["SP_spatial_existing_and_no_worsening"]
    hard = J.spatial_gates(spatial_doc("cand", "X", lambda s, az: s == -5.0), spatial_doc("gen19", "C"), "X", "C")[1]
    assert not hard["SP_spatial_existing_and_no_worsening"]
    left = J.spatial_gates(spatial_doc("cand", "X", lambda s, az: az < 0 and s == 10.0), spatial_doc("gen19", "C"), "X", "C")[1]
    assert not left["SP_spatial_existing_and_no_worsening"]
    with pytest.raises(J.Invalid):
        J.spatial_gates(spatial_doc("cand", "Y"), spatial_doc("gen19", "C"), "X", "C")
    nan = spatial_doc("cand", "X"); nan["crossed_rows"][2]["itd_err_samples"] = float("nan")
    with pytest.raises(J.Invalid):
        J.spatial_gates(nan, spatial_doc("gen19", "C"), "X", "C")


def test_two_way_bootstrap_deterministic_and_zero():
    z = np.zeros((16, 6))
    assert J.two_way_bootstrap(z) == (0.0, 0.0)
    c = np.random.default_rng(1).normal(0.4, 0.3, (16, 6))
    assert J.two_way_bootstrap(c) == J.two_way_bootstrap(c)
    lo, hi = J.two_way_bootstrap(c)
    assert lo < c.mean() < hi and math.isfinite(lo)


ST = HERE / "selftest"
_need_st = pytest.mark.skipif(not (ST / "panel_rev_gen19_vs_gen19_s17.json").exists(), reason="self-test material not built")


@_need_st
def test_selftest_gen19_vs_itself_fails_only_gain_gates():
    sha = "80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367"
    rep, chk, verdict = J.judge(ST / "panel_rev_gen19_vs_gen19_s17.json",
                                HERE.parent / "screen_v2" / "selftest" / "panel_gen19_vs_gen19_s17.json",
                                HERE.parent / "bench-n6" / "bench_v2_gen19.json",
                                ST / "spatial_selftest_s17.json", ST / "spatial_gen19_s17.json", "selftest", sha, 17)
    assert verdict == "FAIL" and rep["rev"]["primary_gain"] == 0.0
    assert {k for k, v in chk.items() if not v} == {"R1a_rev_gain_ge_0.30", "R1b_voice_room_ci_lo_gt_0", "R1c_ge_10_of_16_voices"}


@_need_st
def test_selftest_wrong_registered_hash_is_invalid():
    sha = "80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367"
    with pytest.raises(J.Invalid):
        J.judge(ST / "panel_rev_gen19_vs_gen19_s17.json",
                HERE.parent / "screen_v2" / "selftest" / "panel_gen19_vs_gen19_s17.json",
                HERE.parent / "bench-n6" / "bench_v2_gen19.json",
                ST / "spatial_selftest_s17.json", ST / "spatial_gen19_s17.json", "selftest", sha, 17,
                reg_rev="0" * 64)
