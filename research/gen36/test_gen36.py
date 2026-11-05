"""Gen36 checks: release tensors bound to the audited checkpoints; enhance_v2 refuses unregistered files, applies the
contract (positive sign, no DC), restores the input level when the cap does not bind, never exceeds -1 dBFS; the judge
accepts a complete rule-satisfying run and refuses incomplete, relabelled, unregistered or failing ones."""
import copy, importlib.util, json, sys
from pathlib import Path
import numpy as np, pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "gen35"))
import contract, enhance_v2  # noqa: E402

spec = importlib.util.spec_from_file_location("jc", HERE / "judge_contract.py"); JC = importlib.util.module_from_spec(spec); spec.loader.exec_module(JC)


def _speech(rms):
    import soundfile as sf
    f = sorted(Path("/tmp/gen12dl/LibriSpeech/dev-clean/5694").rglob("*.flac"))[1]
    x, _ = sf.read(f); x = x[:4 * 16000]
    return (x / np.sqrt(np.mean(x ** 2)) * rms).astype(np.float32)


@pytest.fixture(scope="module")
def table():
    t = contract.build_table(); enhance_v2.bind_contract(t); return t


@pytest.mark.parametrize("name", ["model.safetensors", "seed18.safetensors", "seed19.safetensors"])
def test_candidate_contract(table, name):
    m = enhance_v2.load_model(str(contract.RELEASE_DIR / name))
    x = _speech(0.03)                                  # quiet: the headroom cap should not bind
    y, info = enhance_v2.enhance(x, 16000, m)
    w = slice(256, -256)
    assert np.dot(y[w], x[w]) > 0 and abs(float(np.mean(y[w]))) < 2e-3
    assert np.max(np.abs(y)) <= enhance_v2.CEIL + 1e-6
    if info["headroom_gain"] == 1.0:
        assert abs(np.sqrt(np.mean(y.astype(np.float64) ** 2)) - np.sqrt(np.mean(x.astype(np.float64) ** 2))) < 1e-4
    loud = _speech(0.4)                                # loud: the cap binds, peak stays at -1 dBFS
    y2, info2 = enhance_v2.enhance(loud, 48000, m)
    assert info2["headroom_gain"] < 1.0 and np.max(np.abs(y2)) <= enhance_v2.CEIL + 1e-6


def test_unregistered_refused(table, tmp_path):
    import shutil
    p = tmp_path / "x.safetensors"; shutil.copy(contract.RELEASE_DIR / "model.safetensors", p)
    with open(p, "ab") as f:
        f.write(b" ")
    with pytest.raises(SystemExit, match="no registered output contract"):
        enhance_v2.load_model(str(p))


def _synthetic(table):
    man, sp = JC._spec(); rows = []
    for p, (kf, keys, arms, req) in sp.items():
        for s in JC.SEEDS:
            for a in arms:
                for k in keys:
                    r = {"panel": p, "seed": s, "arm": a, **dict(zip(kf, k))}
                    for m in req + (("lag_L", "lag_R") if p == "P1" and k[3] is None else ()):
                        r[m] = 0.0
                    if "alpha" in r: r["alpha"] = 1.0
                    if "wave_err" in r: r["wave_err"] = -20.0 if a == "C_candidate" else -3.0
                    if "peak" in r: r["peak"] = 0.5
                    if "pre_write_peak" in r: r["pre_write_peak"] = 0.5
                    rows.append(r)
    return {"rows": rows, "contract": {h: list(v) for h, v in table.items()}, "fresh_material_sha256": man["material_sha256"]}


def test_judge_complete_and_attacks(table, tmp_path):
    base = _synthetic(table); p = tmp_path / "r.json"
    def run(mut=None):
        d = copy.deepcopy(base)
        if mut: mut(d)
        p.write_text(json.dumps(d)); return JC.judge_safe(p, rebuild=False)["verdict"]
    assert run() == "REPAIR ACCEPTED (inference only)"
    assert run(lambda d: d["rows"].remove(next(r for r in d["rows"] if r["panel"] == "F1"))) == "INVESTIGATE"           # missing
    assert run(lambda d: d["rows"].append(dict(next(r for r in d["rows"] if r["panel"] == "F2")))) == "INVESTIGATE"     # duplicate
    assert run(lambda d: d["rows"].append({**d["rows"][0], "seed": 20})) == "INVESTIGATE"                             # unregistered seed
    assert run(lambda d: d["rows"].append({**d["rows"][0], "arm": "Z"})) == "INVESTIGATE"                             # unregistered arm
    assert run(lambda d: d.__setitem__("fresh_material_sha256", "x")) == "INVESTIGATE"                                # unsealed material
    assert run(lambda d: d.__setitem__("contract", {})) == "INVESTIGATE"                                              # unbound contract
    def setv(panel, arm, m, v, where=lambda r: True, all_=False):
        def f(d):
            hits = [r for r in d["rows"] if r["panel"] == panel and r["arm"] == arm and m in r and where(r)]
            for r in (hits if all_ else hits[:1]): r[m] = v
        return f
    assert run(setv("F2", "C_candidate", "alpha", -0.5)) == "INVESTIGATE"                                             # G1
    assert run(setv("X3q", "C_candidate", "wave_err", 0.0, all_=True)) == "INVESTIGATE"                               # G2 mean
    rep = next(k for k in JC._spec()[0]["items"]["F2"] if k["representable"])
    assert run(setv("F2", "C_candidate", "ac_gain_err_db", 3.0, lambda r: (r["spk"], r["utt"], r["level"]) == (rep["spk"], rep["utt"], rep["level"]))) == "INVESTIGATE"  # G2 item
    assert run(setv("F1", "C_candidate", "stoi_dc", -0.01)) == "INVESTIGATE"                                          # G3
    assert run(setv("X2", "C_candidate", "sisdr", -0.5)) == "INVESTIGATE"                                             # G3
    assert run(setv("P4", "A2_repair", "itd_err_samples", 1.0)) == "INVESTIGATE"                                      # G4
    assert run(setv("P1", "A2_repair", "lag_L", 2, lambda r: r["snr"] is None)) == "INVESTIGATE"                     # G4 lag
    assert run(setv("F1", "C_candidate", "peak", 0.95)) == "INVESTIGATE"                                              # G5 decoded peak
    assert run(setv("X2", "C_candidate", "pre_write_peak", 0.95)) == "INVESTIGATE"                                    # G5 pre-write
    assert run(setv("X4", "C_candidate", "rms", 1.0)) == "INVESTIGATE"                                                # G5 silence
    assert run(setv("F2", "C_candidate", "representable", False)) == "REPAIR ACCEPTED (inference only)"               # labels in rows are ignored
    assert run(setv("F1", "C_candidate", "sisdr", True)) == "INVESTIGATE"                                             # boolean metric
