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
    assert info["bound"] == "level"                    # quiet input: the level gain is the smaller one
    xa = x.astype(np.float64) - x.mean()
    assert abs(np.sqrt(np.mean(y.astype(np.float64) ** 2)) - np.sqrt(np.mean(xa ** 2))) < 1e-5   # DC-free level restored
    loud = _speech(0.4)                                # loud: the headroom cap is the smaller gain
    y2, info2 = enhance_v2.enhance(loud, 48000, m)
    assert info2["bound"] == "headroom" and abs(np.max(np.abs(y2)) - enhance_v2.CEIL) < 1e-6


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
                    r = {"panel": p, "seed": s, "arm": a, **{f: v for (f, _), v in zip(kf, k)}}
                    need = req + (tuple(f"{m}_{e}" for m in ("alpha", "wave_err", "lag", "ac_gain_err_db") for e in "LR") if p == "P1" and k[3] is None else ())
                    for m in need:
                        r[m] = 0 if m.startswith("lag") else 0.0
                    for m in [m for m in r if m.startswith("alpha")]:
                        r[m] = 1.0
                    for m in [m for m in r if m.startswith("wave_err")]:
                        r[m] = -20.0 if a in ("C_candidate", "A2_repair") else -3.0
                    for m in ("peak", "pre_write_peak"):
                        if m in r: r[m] = 0.5
                    rows.append(r)
    import enhance_v2
    return {"rows": rows, "contract": {h: list(v) for h, v in table.items()},
            "release": {n: contract.RELEASE_SHA[n] for n in contract.RELEASE}, "release_config_sha256": contract.RELEASE_CONFIG_SHA,
            "release_enhance_sha256": contract.PUBLISHED_ENHANCE_SHA, "model_module_sha256": enhance_v2.model_module_sha(),
            "fresh_material_by_seed": {str(s): man["material_sha256"] for s in JC.SEEDS}}


def test_judge_complete_and_attacks(table, tmp_path):
    base = _synthetic(table); p = tmp_path / "r.json"
    def run(mut=None, rebuild=False):
        d = copy.deepcopy(base)
        if mut: mut(d)
        p.write_text(json.dumps(d)); return JC.judge_safe(p, rebuild=rebuild)["verdict"]
    OK = "REPAIR ACCEPTED (inference only)"
    assert run() == OK
    first = lambda d, pan, **kw: next(r for r in d["rows"] if r["panel"] == pan and all(r.get(k) == v for k, v in kw.items()))
    # structure
    assert run(lambda d: d["rows"].remove(first(d, "F1"))) == "INVESTIGATE"
    assert run(lambda d: d["rows"].append(dict(first(d, "F2")))) == "INVESTIGATE"
    assert run(lambda d: d["rows"].append({**d["rows"][0], "seed": 20})) == "INVESTIGATE"
    assert run(lambda d: d["rows"].append({**d["rows"][0], "arm": "Z"})) == "INVESTIGATE"
    # Astra pre-launch attacks: missing P1 snr key (also with rebuild), boolean identity, negative peak / abs gain
    assert run(lambda d: first(d, "P1", snr=None).pop("snr")) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1").__setitem__("utt", True)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1").__setitem__("seed", True)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F2", arm="C_candidate").__setitem__("peak", -0.1)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F2", arm="C_candidate").__setitem__("ac_gain_err_db", -1.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F2", arm="C_candidate").__setitem__("sat", 2.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F2", arm="C_candidate").__setitem__("lag", 0.5)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1").__setitem__("sisdr", True)) == "INVESTIGATE"
    # binding
    assert run(lambda d: d.__setitem__("fresh_material_by_seed", {"17": d["fresh_material_by_seed"]["17"]})) == "INVESTIGATE"
    assert run(lambda d: d.__setitem__("contract", {})) == "INVESTIGATE"
    assert run(lambda d: d.__setitem__("release_config_sha256", "0" * 64)) == "INVESTIGATE"
    assert run(lambda d: d.__setitem__("model_module_sha256", "0" * 64)) == "INVESTIGATE"
    assert run(lambda d: d["release"].__setitem__("seed18.safetensors", "0" * 64)) == "INVESTIGATE"
    # rule coverage
    def setall(pan, arm, m, v, where=lambda r: True):
        def f(d):
            for r in d["rows"]:
                if r["panel"] == pan and r["arm"] == arm and m in r and where(r): r[m] = v
        return f
    assert run(setall("X3", "C_candidate", "wave_err", -3.0, lambda r: r["setting"] == "high" and r["seed"] == 18)) == "INVESTIGATE"  # one X3 setting
    assert run(lambda d: first(d, "F2", arm="C_candidate", level="overload").__setitem__("ac_gain_err_db", 9.0)) == "INVESTIGATE"  # overload item
    assert run(lambda d: first(d, "X3q", arm="C_candidate").__setitem__("lag", 3)) == "INVESTIGATE"                    # export lag
    assert run(lambda d: first(d, "P1", arm="A2_repair", snr=None).__setitem__("wave_err_L", 0.0)) == "INVESTIGATE"  # research preservation
    assert run(lambda d: first(d, "P1", arm="A2_repair", snr=None).__setitem__("alpha_R", -1.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "P1", arm="A2_repair", snr=-5.0).__setitem__("stoi_dc_L", -0.5)) == "INVESTIGATE"  # research per-ear noisy
    assert run(lambda d: first(d, "P4", arm="A2_repair").__setitem__("sisdr_R", -0.5)) == "INVESTIGATE"
    assert run(lambda d: first(d, "P4", arm="A2_repair").__setitem__("itd_err_samples", 1.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1", arm="C_candidate").__setitem__("stoi_dc", -0.01)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1", arm="C_candidate").__setitem__("peak", 0.95)) == "INVESTIGATE"
    assert run(lambda d: first(d, "X2", arm="C_candidate").__setitem__("pre_write_peak", 0.95)) == "INVESTIGATE"
    assert run(lambda d: first(d, "X4", arm="C_candidate").__setitem__("rms", 1.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "P6", arm="A2_repair").__setitem__("rms", 1.0)) == "INVESTIGATE"
    # Astra verification attacks: research AC-gain worsening, impossible STOI values, manifest tampering
    assert run(setall("P1", "A2_repair", "ac_gain_err_db_L", 9.0, lambda r: r["snr"] is None)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1", arm="C_candidate").__setitem__("stoi_dc", 2.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "P4", arm="A2_repair").__setitem__("stoi_dc_L", 2.0)) == "INVESTIGATE"
    assert run(lambda d: first(d, "F1", arm="E0_published").__setitem__("stoi", -1.5)) == "INVESTIGATE"


def test_manifest_tampering_refused(table, tmp_path, monkeypatch):
    """Removing 63 of 64 F1 items from the manifest while keeping its claimed hash must not pass (Astra)."""
    base = _synthetic(table)
    man = json.loads((HERE / "manifest.json").read_text())
    keep = man["items"]["F1"][:1]
    tampered = {**man, "items": {**man["items"], "F1": keep}}
    real = Path.read_bytes
    def fake_read_bytes(self):
        if self.name == "manifest.json" and self.parent == HERE:
            return json.dumps(tampered).encode()
        return real(self)
    monkeypatch.setattr(Path, "read_bytes", fake_read_bytes)
    d = copy.deepcopy(base)
    d["rows"] = [r for r in d["rows"] if r["panel"] != "F1" or (r["spk"], r["utt"], r["snr"]) == (keep[0]["spk"], keep[0]["utt"], keep[0]["snr"])]
    p = tmp_path / "r.json"; p.write_text(json.dumps(d))
    assert JC.judge_safe(p, rebuild=True)["verdict"] == "INVESTIGATE"
