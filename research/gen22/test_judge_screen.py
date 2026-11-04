"""judge_screen fixtures (Astra pre-launch review item 6): real Gen21 S48
seed-17 artifacts stand in for a candidate; provenance violations must
raise Invalid and failed safeguards must FAIL."""
import copy
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judge_screen as J  # noqa: E402

R = HERE.parent
CTRL_LOG = R / "gen21/weights/train_log_r48_seed20261117.json"
CTRL_BENCH = R / "bench-n6/bench_v2_gen19.json"
S48_LOG = R / "gen21/weights/train_log_s48_seed20261117.json"
S48_BENCH = R / "bench-n6/benchv2_g21s48_48k.json"
DEV = R / "gen21/dev_audit.json"
CAND = "c" * 64


def _fixture(tmp):
    s48 = json.loads(S48_LOG.read_text())
    final = [e for e in s48["val_log"] if e["lifetime_step"] == 48000][0]
    log = {"seed": 20261117, "mode": "scratch", "loss": "cap30", "steps": 24000, "lifetime_steps": 24000,
           "weights_sha256": CAND, "val_log": [dict(final, step=24000, lifetime_step=24000)]}
    bench = json.loads(S48_BENCH.read_text())
    bench["meta"]["checkpoint_sha256"] = CAND
    ctrl_sha = json.loads(CTRL_BENCH.read_text())["meta"]["checkpoint_sha256"]
    rows = []
    for r in json.loads(DEV.read_text())["rows"]:
        if r["system"] == "parent":
            rows.append(dict(r, system="control"))
        elif r["system"] == "s48_48k":
            rows.append(dict(r, system="cap30", sha256=CAND))
    assert {r["sha256"] for r in rows if r["system"] == "control"} == {ctrl_sha}
    return log, bench, {"rows": rows}


def _judge(tmp, log, bench, dev):
    for n, obj in (("log", log), ("bench", bench), ("dev", dev)):
        (tmp / f"{n}.json").write_text(json.dumps(obj))
    return J.judge(CTRL_LOG, tmp / "log.json", CTRL_BENCH, tmp / "bench.json", tmp / "dev.json", 20261117)


def test_real_s48_fixture_fails_on_bench(tmp_path):
    rows, checks, verdict = _judge(tmp_path, *_fixture(tmp_path))
    assert abs(rows["val_gain_m5"][0] - 0.4409) < 1e-4 and abs(rows["bench_gain_m5"][0] + 0.1267) < 1e-4
    assert rows["dev_targets_improved"] == 8 and checks["6_dev_panel"] and not checks["1_m5_gain_ge_0.30_both"]
    assert verdict == "FAIL"


def test_advance_path(tmp_path):
    log, bench, dev = _fixture(tmp_path)
    for it in log["val_log"][0]["items"]:
        if it["snr"] == -5.0:
            it["d_sisdr"] += 1.0; it["d_stoi"] += 0.01
    cand = bench["meta"]["candidate"]
    for r in bench["rows"]:
        if r["system"] == cand and r["kind"] == "crowd" and r["snr_db"] == -5.0:
            r["sisdr"] += 1.0; r["stoi"] += 0.01
    assert _judge(tmp_path, log, bench, dev)[2] == "ADVANCE"


def test_failed_ci_lower_bound_fails(tmp_path):
    log, bench, dev = _fixture(tmp_path)
    bench["summary"][bench["meta"]["candidate"]]["crowd"]["d_stoi"]["ci_lo"] = -0.001
    rows, checks, verdict = _judge(tmp_path, log, bench, dev)
    assert not checks["5_other_required_rows"] and verdict == "FAIL"


@pytest.mark.parametrize("breakage", ["missing_target", "wrong_dev_hash", "interim_ckpt", "bench_hash", "policy",
                                      "wrong_seed", "no_0db_panel", "one_crop_replacement", "duplicate_item"])
def test_provenance_violations_raise(tmp_path, breakage):
    log, bench, dev = _fixture(tmp_path)
    if breakage == "missing_target":
        dev["rows"] = [r for r in dev["rows"] if r["spk"] != "6313"]
    elif breakage == "wrong_dev_hash":
        for r in dev["rows"]:
            if r["system"] == "cap30":
                r["sha256"] = "d" * 64
    elif breakage == "interim_ckpt":
        log = copy.deepcopy(log); log["lifetime_steps"] = 22000
    elif breakage == "bench_hash":
        bench["meta"]["checkpoint_sha256"] = "e" * 64
    elif breakage == "policy":
        log["loss"] = "sisdr"
    elif breakage == "wrong_seed":
        log["seed"] = 20261118
    elif breakage == "no_0db_panel":
        dev["rows"] = [r for r in dev["rows"] if r["snr"] != 0.0]
    elif breakage == "one_crop_replacement":  # 16 items/target kept, but all from crop 0
        for r in dev["rows"]:
            r["crop"], r["mix"] = 0, (r["crop"] * 4 + r["mix"])
    elif breakage == "duplicate_item":
        dev["rows"].append(dict(dev["rows"][0]))
    with pytest.raises(J.Invalid):
        _judge(tmp_path, log, bench, dev)
