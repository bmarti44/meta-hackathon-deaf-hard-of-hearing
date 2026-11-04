"""Gen24 judge = Gen22 rules with the Gen24 candidate name/policy (snr in policy): the real
Gen21 S48 s17 fixture (relabelled hard60) reproduces the Gen22 fixture
numbers; a Gen22 (cap30) log or dev rows are refused."""
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "gen22"))


def _load(name, path):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


G23 = _load("judge_screen_g24", HERE / "judge_screen.py")
J22 = G23.J22
T22 = _load("test_judge_screen_g22_for24", HERE.parent / "gen22" / "test_judge_screen.py")

POL = G23.POLICY
assert POL == {"mode": "scratch", "loss": "sisdr", "snr": "hard60", "steps": 24000} and G23.CAND == "hard60"


def _cs5(tmp):
    log, bench, dev = T22._fixture(tmp)
    log["loss"] = "sisdr"; log["snr"] = "hard60"
    for r in dev["rows"]:
        if r["system"] == "cap30":
            r["system"] = "hard60"
    return log, bench, dev


def _judge(tmp, log, bench, dev, **kw):
    import json
    for n, obj in (("log", log), ("bench", bench), ("dev", dev)):
        (tmp / f"{n}.json").write_text(json.dumps(obj))
    return J22.judge(T22.CTRL_LOG, tmp / "log.json", T22.CTRL_BENCH, tmp / "bench.json", tmp / "dev.json",
                     20261117, cand="hard60", policy=POL, **kw)


def test_fixture_reproduces_gen22_numbers(tmp_path):
    rows, checks, verdict = _judge(tmp_path, *_cs5(tmp_path))
    assert abs(rows["val_gain_m5"][0] - 0.4409) < 1e-4 and abs(rows["bench_gain_m5"][0] + 0.1267) < 1e-4
    assert rows["dev_targets_improved"] == 8 and verdict == "FAIL"


def test_gen22_log_refused(tmp_path):
    log, bench, dev = _cs5(tmp_path)
    log["loss"] = "cap30"
    with pytest.raises(J22.Invalid):
        _judge(tmp_path, log, bench, dev)


def test_gen22_dev_rows_refused(tmp_path):
    log, bench, dev = T22._fixture(tmp_path)
    log["loss"] = "sisdr"; log["snr"] = "hard60"
    with pytest.raises(J22.Invalid):
        _judge(tmp_path, log, bench, dev)


def test_legacy_snr_log_refused(tmp_path):
    log, bench, dev = _cs5(tmp_path)
    log["snr"] = "legacy"
    with pytest.raises(J22.Invalid):
        _judge(tmp_path, log, bench, dev)
