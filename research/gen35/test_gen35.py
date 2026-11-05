"""Gen35 checks: registered polarity per checkpoint; A0 is exactly the Gen34 v1 path; A1/A2 use the flushed delay;
A2 removes the decoder bias and is positively signed on held-out speech; export_enhance reproduces the published
enhance.py (snapshot in research/gen35/published/) and its repair changes only polarity and DC."""
import importlib.util, sys
from pathlib import Path
import numpy as np, pytest, torch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HERE.parent / "gen33"))
import repair as RP  # noqa: E402
import linked  # noqa: E402


def _speech():
    import soundfile as sf
    f = sorted(Path("/tmp/gen12dl/LibriSpeech/dev-clean/5694").rglob("*.flac"))[0]
    x, _ = sf.read(f); x = x[:3 * 16000]
    return (x / np.sqrt(np.mean(x ** 2)) * 0.14).astype(np.float32)


def test_registered_polarity():
    pol = RP.registered_polarity()
    assert [pol[RP.sha(RP.CKPTS[s])] for s in (17, 18, 19)] == [-1, 1, -1]


@pytest.mark.parametrize("seed", [17, 18, 19])
def test_arms(seed):
    A = RP.Arms(RP.CKPTS[seed]); x = _speech(); o = A.outputs(x)
    v1, _ = linked.pair_fn(RP.CKPTS[seed], "independent")(x, x)
    assert np.array_equal(o["A0_existing"], np.asarray(v1, np.float32))           # exactly the Gen34 v1 path
    w = slice(256, -256)
    assert np.allclose(o["A2_repair"] + A.polarity * A.bias, o["A1_sign"], atol=1e-6)
    assert RP.signed_alpha(x, o["A2_repair"], w) > 0.5                             # positively signed on held-out speech
    assert abs(float(np.mean(o["A2_repair"][w]))) < abs(float(np.mean(o["A1_sign"][w])))
    assert np.array_equal(o["A0_existing"][-63:], np.zeros(63, np.float32))        # v1 pads the last 63 samples
    assert np.allclose(o["A1_sign"][:-63], A.polarity * o["A0_existing"][:-63], atol=1e-6)


def test_export_matches_published():
    spec = importlib.util.spec_from_file_location("pub_enh", HERE / "published" / "enhance.py")
    pub = importlib.util.module_from_spec(spec); spec.loader.exec_module(pub)
    A = RP.Arms(RP.CKPTS[17]); x = (0.5 * _speech()).astype(np.float32)
    y_pub = pub.enhance(x, 16000, model=A.model)
    y_ours = RP.export_enhance(x, A.model)
    assert np.allclose(y_pub, y_ours, atol=1e-6)
    y_rep = RP.export_enhance(x, A.model, (A.polarity, A.bias)); w = slice(256, -256)
    assert RP.signed_alpha(x, y_rep, w) > 0 and RP.signed_alpha(x, y_pub, w) < 0
    assert abs(float(np.mean(y_rep[w]))) < abs(float(np.mean(y_pub[w])))


def _synthetic_rows():
    """A complete, rule-satisfying synthetic run (P1 A0 seed 17 copied from the Gen34 audit for V0)."""
    import json as _j
    spec = JR._expected()
    G = _j.loads((HERE.parent / "gen34" / "audit_s17.json").read_text())
    g19 = {(r["talker"], r["setting"], r["az"], r["snr"]): r for r in G["rows"] if r["system"] == "gen19"}
    rows = []
    for p, (kf, keys, arms, req) in spec.items():
        for s in JR.SEEDS:
            for a in arms:
                for k in keys:
                    r = {"panel": p, "seed": s, "arm": a, **dict(zip(kf, k))}
                    for m in req + ("lag_L", "lag_R"):
                        r[m] = 0.0
                    for m in [m for m in r if m.startswith("alpha")]:
                        r[m] = 1.0
                    if p == "P1":
                        r["cond"] = "target_only" if k[3] is None else "noisy"
                        if s == 17:                     # every arm carries the audited values; A0 must match them exactly
                            r.update({m: g19[k][m] for m in JR.SHARED})
                    for m in [m for m in r if m.startswith("wave_err")]:
                        if not (p == "P1" and s == 17 and a == "A0_existing"):
                            r[m] = -10.0 if a in ("A2_repair", "E2_repair") else -5.0
                    rows.append(r)
    import repair as _RP
    return {"rows": rows, "checkpoints": {str(s): {"sha256": _RP.sha(_RP.CKPTS[s])} for s in JR.SEEDS},
            "polarity": {str(s): _RP.POLARITY[_RP.sha(_RP.CKPTS[s])] for s in JR.SEEDS}, "decoder_bias": {}}


spec_j = importlib.util.spec_from_file_location("judge_repair_t", HERE / "judge_repair.py")
JR = importlib.util.module_from_spec(spec_j); spec_j.loader.exec_module(JR)


def test_judge_accepts_complete_and_refuses_astra_attacks(tmp_path):
    import copy, json as _j
    base = _synthetic_rows(); p = tmp_path / "rows.json"
    p.write_text(_j.dumps(base)); assert JR.judge_safe(p)["verdict"] == "REPAIR ACCEPTED (inference only)"
    def run(mut):
        d = copy.deepcopy(base); mut(d); p.write_text(_j.dumps(d)); return JR.judge_safe(p)["verdict"]
    # a missing P2 item
    assert run(lambda d: d["rows"].remove(next(r for r in d["rows"] if r["panel"] == "P2"))) == "INVESTIGATE"
    # the whole P5 high level replaced by duplicates of another level
    def p5(d):
        keep = [r for r in d["rows"] if not (r["panel"] == "P5" and r["level"] == 0.56)]
        dup = [dict(r) for r in d["rows"] if r["panel"] == "P5" and r["level"] == 0.14]
        d["rows"] = keep + dup
    assert run(p5) == "INVESTIGATE"
    # export silence rows missing, replaced by duplicates
    def x4(d):
        sil = [r for r in d["rows"] if r["panel"] == "X4" and r["kind"] == "silence"]
        d["rows"] = [r for r in d["rows"] if r not in sil] + [dict(next(r for r in d["rows"] if r["panel"] == "X4" and r["kind"] == "transition"))]
    assert run(x4) == "INVESTIGATE"
    # a missing metric, a boolean metric, an unregistered checkpoint hash
    assert run(lambda d: d["rows"][5].pop(next(m for m in d["rows"][5] if m.startswith("sisdr") or m == "rms" or m == "alpha"))) == "INVESTIGATE"
    assert run(lambda d: d["rows"].__setitem__(9, {**d["rows"][9], "clip": True} if "clip" in d["rows"][9] else {**d["rows"][9], "clip_L": True})) == "INVESTIGATE"
    assert run(lambda d: d["checkpoints"]["18"].__setitem__("sha256", "0" * 64)) == "INVESTIGATE"
    # Astra verification attacks: relabelled P1 target-only row hiding bad values; unregistered seed/arm groups
    def relabel(d):
        r = next(r for r in d["rows"] if r["panel"] == "P1" and r["arm"] == "A2_repair" and r["snr"] is None and r["seed"] == 19)
        r.update({"cond": "noisy", "alpha_L": -1.0, "wave_err_L": 100.0, "lag_L": 80})
    assert run(relabel) == "INVESTIGATE"
    def bad_value_keep_label(d):                     # same bad values without relabelling are also caught by the rules
        r = next(r for r in d["rows"] if r["panel"] == "P1" and r["arm"] == "A2_repair" and r["snr"] is None and r["seed"] == 19)
        r.update({"alpha_L": -1.0, "lag_L": 80})
    assert run(bad_value_keep_label) == "INVESTIGATE"
    assert run(lambda d: d["rows"].append({**d["rows"][0], "seed": 20})) == "INVESTIGATE"
    assert run(lambda d: d["rows"].append({**d["rows"][0], "arm": "A9_other", "sisdr_L": None})) == "INVESTIGATE"
    # rules extended to P3/P5/X3 waveform error, P4 per-ear scores, clip/lag everywhere
    def worse(panel, metric, val, arm):
        def f(d):
            r = next(r for r in d["rows"] if r["panel"] == panel and r["arm"] == arm and metric in r); r[metric] = val
        return f
    def worse_all(panel, metric, val, arm):         # the R2/E2 rules are on means: worsen the whole panel for one seed
        def f(d):
            for r in d["rows"]:
                if r["panel"] == panel and r["arm"] == arm and r["seed"] == 18 and metric in r:
                    r[metric] = val
        return f
    assert run(worse_all("P3", "wave_err", 0.0, "A2_repair")) == "INVESTIGATE"
    assert run(worse_all("P5", "wave_err_L", 0.0, "A2_repair")) == "INVESTIGATE"
    assert run(worse_all("X3", "wave_err", 0.0, "E2_repair")) == "INVESTIGATE"
    assert run(worse_all("X3q", "wave_err", 0.0, "E2_repair")) == "INVESTIGATE"
    assert run(worse("P4", "sisdr_R", -1.0, "A2_repair")) == "INVESTIGATE"
    assert run(worse("P2", "clip", 0.5, "A2_repair")) == "INVESTIGATE"
    assert run(worse("P3", "lag", 3, "A2_repair")) == "INVESTIGATE"
    assert run(worse("X1", "stoi", -0.5, "E2_repair")) == "INVESTIGATE"
    assert run(worse("X4", "rms", 1.0, "E2_repair")) == "INVESTIGATE"


def test_unregistered_checkpoint_refused(tmp_path):
    bad = tmp_path / "x.pt"; torch.save(torch.load(RP.CKPTS[17], weights_only=False) | {"note": 1}, bad)
    with pytest.raises(SystemExit, match="not a registered checkpoint"):
        RP.Arms(bad)
