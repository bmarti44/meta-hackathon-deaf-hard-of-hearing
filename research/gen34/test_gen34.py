"""Gen34 checks: mixing math (SNR from summed bilateral energy, one noise multiplier and one input gain shared by
both ears, so interaural level differences are preserved), the judge's lag-sign convention, grid and duplicate checks."""
import importlib.util, json, sys
from pathlib import Path
import numpy as np, pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import recorded_panel as P  # noqa: E402


def test_make_item_snr_and_shared_gains():
    rng = np.random.default_rng(1); n = 5 * P.FS
    sL = rng.normal(size=n); sR = 0.5 * sL                     # target louder on the left
    nL = rng.normal(size=n) * 0.3; nR = rng.normal(size=n) * 0.3
    for snr in P.SNRS:
        it = P.make_item(sL, sR, nL, nR, snr)
        w = slice(P.T0, None)
        k = it["rL"][w].astype(np.float64) / sL[w]              # one input gain
        assert np.allclose(it["rR"][w] / sR[w], k[0], rtol=1e-5) and np.allclose(k, k[0], rtol=1e-5)
        dL, dR = it["mL"][w] - it["rL"][w], it["mR"][w] - it["rR"][w]
        gL, gR = np.dot(dL, nL[w]) / np.dot(nL[w], nL[w]), np.dot(dR, nR[w]) / np.dot(nR[w], nR[w])
        assert abs(gL - gR) < 1e-5 * abs(gL)                    # one noise multiplier for both ears
        es = np.sum(it["rL"][w].astype(np.float64) ** 2) + np.sum(it["rR"][w].astype(np.float64) ** 2)
        en = np.sum(dL.astype(np.float64) ** 2) + np.sum(dR.astype(np.float64) ** 2)
        assert abs(10 * np.log10(es / en) - snr) < 1e-3
        rms = np.sqrt(0.5 * (np.mean(it["mL"].astype(np.float64) ** 2) + np.mean(it["mR"].astype(np.float64) ** 2)))
        assert abs(rms - P.RMS_IN) < 1e-5
    t = P.make_item(sL, sR, nL, nR, None)
    assert np.array_equal(t["mL"], t["rL"]) and np.array_equal(t["mR"], t["rR"])


def _judge():
    spec = importlib.util.spec_from_file_location("jr1", HERE / "judge_recorded_v1.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def _rows():
    rows = []
    for sysn in ("bypass", "gen19", "gen19_repeat", "gen32"):
        for t in P.TALKERS:
            for s in P.SETTINGS:
                for az in P.AZ:
                    for snr in P.SNRS + (None,):
                        r = {"system": sysn, "talker": t, "setting": s, "az": az, "snr": snr,
                             "cond": "target_only" if snr is None else "noisy", **{m: 1.0 for m in P.METRICS}}
                        if sysn == "bypass":
                            r["bypass_identical"] = True
                        rows.append(r)
    return rows


def test_judge_grid_duplicate_and_bypass_checks(tmp_path):
    J = _judge()
    base = {"material_sha256": "x", "rows": _rows(), "checkpoints": {k: {"sha256": v} for k, v in J.REG.items()}}
    p = tmp_path / "a.json"; p.write_text(json.dumps(base))
    c = J.judge(p, rebuild=False)["checks"]
    assert c["A3_complete_grid"] and c["A5_bypass_identity"] and c["A6_duplicate_baseline_zero_difference"]
    assert c["A7_finite_and_registered_checkpoints"] and c["A2_recording_overlap_excluded_by_provenance"]
    for m in P.METRICS:                                             # every prescribed metric must be present and finite
        bad = json.loads(json.dumps(base)); del bad["rows"][7][m]; p.write_text(json.dumps(bad))
        assert not J.judge(p, rebuild=False)["checks"]["A7_finite_and_registered_checkpoints"], m
    bad = json.loads(json.dumps(base)); bad["rows"][3]["stoi_R"] = True; p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A7_finite_and_registered_checkpoints"]
    bad = json.loads(json.dumps(base)); bad["rows"] = [r for r in bad["rows"] if r["system"] != "gen19"]
    p.write_text(json.dumps(bad))
    v = J.judge_safe(p, rebuild=False)                              # malformed: INVALID, never an exception
    assert v["verdict"] == "INVALID"
    p.write_text("{not json"); assert J.judge_safe(p, rebuild=False)["verdict"] == "INVALID"
    p.write_text(json.dumps(base))
    bad = json.loads(json.dumps(base)); bad["rows"].pop(5); p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A3_complete_grid"]
    bad = json.loads(json.dumps(base)); bad["rows"].append(dict(bad["rows"][0])); p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A3_complete_grid"]
    bad = json.loads(json.dumps(base))
    next(r for r in bad["rows"] if r["system"] == "gen19_repeat")["sisdr_L"] = 1.0000001; p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A6_duplicate_baseline_zero_difference"]
    bad = json.loads(json.dumps(base))
    next(r for r in bad["rows"] if r["system"] == "bypass")["bypass_identical"] = False; p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A5_bypass_identity"]
    bad = json.loads(json.dumps(base)); bad["checkpoints"]["gen32"]["sha256"] = "0" * 64; p.write_text(json.dumps(bad))
    assert not J.judge(p, rebuild=False)["checks"]["A7_finite_and_registered_checkpoints"]


def test_metrics_include_mixture_distortion_and_waveform_error():
    rng = np.random.default_rng(2); n = 3 * P.FS
    r = rng.normal(size=n).astype(np.float32); rr = (0.5 * r).astype(np.float32)
    m = P.metrics(r, rr, r, rr, r, rr)
    assert set(m) == set(P.METRICS)
    assert m["wave_err_L"] < -100 and m["ild_target_err_db"] < 1e-9 and m["ild_mixture_dist_db"] < 1e-9
    m2 = P.metrics(r, rr, 0.5 * r, rr, r, rr)                     # gain change: SI-SDR blind, waveform error not
    assert m2["sisdr_L"] > 100 and m2["wave_err_L"] > -10 and m2["ild_target_err_db"] > 5
