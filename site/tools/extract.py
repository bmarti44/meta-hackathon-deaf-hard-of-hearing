#!/tmp/gen9env/bin/python
"""Extract site/data/*.json from committed research artifacts.

Run from repo root:  /tmp/gen9env/bin/python site/tools/extract.py
Every number on the site that is not prose comes from this script.
"""
import json, subprocess, sys, re
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "site" / "data"
OUT.mkdir(exist_ok=True)
B = ROOT / "research" / "bench-n6"
PY = sys.executable

def load(p): return json.loads(Path(p).read_text())
def dump(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1))
    print("wrote", name)

# ---------- 1. Scorecard: run the project's own kpi_scorecard.py ----------
gen19_benches = [B/"bench_v2_gen19.json", B/"benchv2_gen19s2.json", B/"benchv2_gen19s3.json"]
cmd = [PY, str(B/"kpi_scorecard.py"), "--spatial", str(B/"spatial_gen19.json"),
       "--candidate", "gen19", "--babble-kind", "crowd"]
for b in gen19_benches: cmd += ["--bench", str(b)]
res = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, check=True).stdout
rows = []
pat = re.compile(r"^\[(PASS|FAIL|INFO)\] (.+?)\s+actual=(.+?) required (.+?)(?: \| stretch (.+?): (PASS|no))?$")
for line in res.splitlines():
    m = pat.match(line.strip())
    if not m: continue
    st, kpi, actual, req, stretch, sok = m.groups()
    rows.append({"kpi": kpi.strip(), "status": st, "actual": actual.strip(), "required": req.strip(),
                 "stretch": stretch, "stretch_pass": (sok == "PASS") if sok else None})
verdict = [l for l in res.splitlines() if l.startswith("ALL REQUIRED")][0].split(":",1)[1].strip()
# stable row ids for the site's /api/explain?row=<id> (order follows kpi_scorecard.py output)
ROW_IDS = ["crowd_sisdr", "crowd_stoi", "crowd_ace", "crowd_m5", "crowd_0", "crowd_m5_stoi", "crowd_every_seed",
           "crowd_vs_gate", "ssn", "white", "quiet_abs", "quiet_stoi", "ild", "itd", "ild_distortion"]
assert len(rows) == len(ROW_IDS), (len(rows), len(ROW_IDS))
for r, rid in zip(rows, ROW_IDS): r["id"] = rid
dump("scorecard.json", {"source": "research/bench-n6/kpi_scorecard.py on 3 Gen 19 seeds + spatial_gen19.json",
                        "candidate": "gen19", "rows": rows, "verdict": verdict,
                        "n_required": sum(r["status"] != "INFO" for r in rows),
                        "n_pass": sum(r["status"] == "PASS" for r in rows)})

# ---------- 2. Per-SNR crowd gains (seed-mean + per-seed), all systems ----------
def per_snr(bench, system, kind="crowd", key="sisdr"):
    base = {r["crop"]: r for r in bench["rows"] if r["system"] == "unproc"}
    out = {}
    for snr in [-5.0, 0.0, 5.0, 10.0]:
        vals = [r[key] - base[r["crop"]][key] for r in bench["rows"]
                if r["system"] == system and r["kind"] == kind and r["snr_db"] == snr]
        out[str(int(snr))] = float(np.mean(vals))
    return out

def normalize(bench, name):
    """Rename the bench's own candidate system (meta.candidate) to `name`."""
    src = bench["meta"].get("candidate")
    if src and src != name:
        bench["summary"][name] = bench["summary"].pop(src)
        for r in bench["rows"]:
            if r["system"] == src: r["system"] = name
    return bench
benches = [normalize(load(p), "gen19") for p in gen19_benches]
systems = ["gen19", "causal_gate", "oracle_noncausal"]
kinds = ["crowd", "competing", "ssn", "white-heldout"]
snr = {"snrs": [-5, 0, 5, 10], "systems": {}, "per_seed_crowd_gen19": [], "conditions": {}}
for s in systems:
    per_seed = [per_snr(b, s) for b in benches]
    snr["systems"][s] = {k: float(np.mean([p[k] for p in per_seed])) for k in per_seed[0]}
snr["per_seed_crowd_gen19"] = [per_snr(b, "gen19") for b in benches]
snr["per_seed_crowd_stoi_gen19"] = [per_snr(b, "gen19", key="stoi") for b in benches]
for k in kinds:
    snr["conditions"][k] = {s: {q: float(np.mean([per_snr(b, s, k)[q] for b in benches])) for q in ["-5","0","5","10"]} for s in systems}
# overall deltas from summaries (seed-mean)
summ = {}
for s in systems:
    summ[s] = {}
    for k in kinds + ["quiet"]:
        for metric in ["d_sisdr", "d_stoi", "d_ace_electro_corr", "d_voc_estoi"]:
            summ[s].setdefault(k, {})[metric] = float(np.mean([b["summary"][s][k][metric]["mean"] for b in benches]))
        summ[s][k]["sisdr_abs"] = float(np.mean([b["summary"][s][k]["sisdr"] for b in benches]))
snr["summary_seed_mean"] = summ
snr["white_voc_estoi_per_seed_gen19"] = [b["summary"]["gen19"]["white-heldout"]["d_voc_estoi"]["mean"] for b in benches]
snr["checkpoint_sha256"] = [b["meta"]["checkpoint_sha256"] for b in benches]
# Gen 22 cap30 seed-17 bench vs Gen 19 seed-17
g22 = normalize(load(B/"benchv2_g22cap30s17.json"), "gen22")
snr["gen22_cap30_s17_crowd"] = per_snr(g22, "gen22")
snr["gen19_s17_crowd"] = per_snr(benches[0], "gen19")
dump("bench_snr.json", snr)

# ---------- 3. VAL -5 dB trajectories (seed 17): Gen 19 vs Gen 22 cap30 ----------
def traj(log):
    return [{"step": e["step"], "m5": e["val"]["-5.0"]["d_sisdr"], "m5_stoi": e["val"]["-5.0"]["d_stoi"],
             "zero": e["val"]["0.0"]["d_sisdr"]} for e in log["val_log"]]
g19log = load(ROOT/"research/gen19/weights/train_log_seed20261117.json")
g22log = load(ROOT/"research/gen22/weights/train_log_cap30_scratch_seed20261117.json")
dump("val_traj.json", {"seed": 20261117, "note": "fixed VAL panel, every 2000 steps; d_sisdr vs unprocessed, dB",
                       "series": {"gen19": traj(g19log), "gen22_cap30": traj(g22log)}})

# ---------- 4. Model facts ----------
rf = g19log["receptive_field"]
dump("model.json", {"params": g19log["params"], "steps": g19log["steps"], "wall_s": g19log["wall_s"],
                    "batch": g19log["batch"], "seg_s": g19log["seg_s"],
                    "algorithmic_latency_ms_max": rf["algorithmic_latency_ms_max"],
                    "algorithmic_latency_samples_max": rf["algorithmic_latency_samples_max"],
                    "future_samples": rf["future_samples"], "past_context_s": rf["past_context_s"],
                    "causality_post_max_prefix_diff": max(c["max_diff_prefix_P"] for c in g19log["causality_post"]),
                    "weights_sha256": g19log["weights_sha256"], "pool_n_files": g19log["pool_n_files"],
                    "pool_n_speakers": len(g19log["pool_files"])})

# ---------- 5. Gen 22 screen + Gen 21 replication (verbatim judge outputs) ----------
dump("gen22_screen.json", load(ROOT/"research/gen22/screen_s17.json"))
dump("gen21_replication.json", load(ROOT/"research/gen21/replication_judgment.json"))
