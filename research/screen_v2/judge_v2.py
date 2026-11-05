"""Screen v2 judgment (registered in research/screen_v2/prereg.md; applies to Gen 26 onward).

ADVANCE requires all of:
 A1 panel v2 at -5 dB: mean paired gain (cand - control) in SI-SDR >= +0.30 dB
 A2 speaker-clustered 95% bootstrap CI lower bound of that gain > 0
    (resample the 16 voices with replacement, 10,000 draws, seed 20261204)
 A3 at least 10 of the 16 voices improve at -5 dB (per-voice mean gain > 0)
 A4 panel v2 at -5 dB: mean paired STOI gain >= 0
 S1 panel v2 at 0 dB: gain >= -0.15 dB and STOI gain >= -0.003
 S2 bench v2 (candidate): quiet absolute SI-SDR >= 25 dB and quiet dSTOI >= -0.02
 S3 bench v2 (candidate): crowd dSI-SDR >= 3.0, dSTOI >= 0.03, dACE-electro >= 0.05,
    each 95% CI lower bound > 0; SSN >= 3.0; white >= 0
Provenance: panel material hash == registered; control rows == Gen 19 same-seed hash;
candidate rows == candidate hash == bench meta hash; the grid is complete and duplicate-free
for both systems. The old 8-item VAL and 6-mixture bench -5 dB numbers are reported
descriptively and no longer decide.

Usage: python research/screen_v2/judge_v2.py --panel P.json --bench B.json --cand NAME --cand-sha SHA --seed 17 [--out f.json]
"""
import argparse, hashlib, json, statistics
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE.parent
REGISTERED_MATERIAL = "557ad44f3f874c25f6fe80c158844ce4a622f52db171f35c1f84464dbfb3eafb"
TARGETS = ["84", "1462", "1673", "1919", "3081", "3536", "3576", "3853", "174", "251", "422", "652", "777", "1272", "2803", "2902"]
GRID = {(t, c, m, s) for t in TARGETS for c in range(4) for m in range(4) for s in (-5.0, 0.0)}


class Invalid(Exception):
    pass


def _need(c, msg):
    if not c:
        raise Invalid(msg)


def speaker_bootstrap(per_spk, draws=10000, seed=20261204):
    v = np.array(list(per_spk.values()))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(v), size=(draws, len(v)))
    m = v[idx].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def judge(panel_p, bench_p, cand, cand_sha, seed):
    P = json.loads(Path(panel_p).read_text())
    _need(P.get("material_sha256") == REGISTERED_MATERIAL, f"panel material {P.get('material_sha256')} != registered")
    ctrl_sha = hashlib.sha256((R / "gen19" / "weights" / f"causal_seed{20261100 + seed}.pt").read_bytes()).hexdigest()
    key = lambda r: (r["spk"], r["crop"], r["mix"], r["snr"])  # noqa: E731
    sysrows = {}
    for name, sha in (("control", ctrl_sha), (cand, cand_sha)):
        rs = [r for r in P["rows"] if r["system"] == name]
        _need({r["sha256"] for r in rs} == {sha}, f"panel {name} hash {({r['sha256'] for r in rs})} != {sha}")
        ks = [key(r) for r in rs]
        _need(len(ks) == len(set(ks)) and set(ks) == GRID, f"panel {name} grid incomplete or duplicated")
        sysrows[name] = {key(r): r for r in rs}
    B = json.loads(Path(bench_p).read_text())
    _need(B["meta"]["checkpoint_sha256"] == cand_sha, "bench candidate hash != candidate")
    # bench coverage (Astra screen-v2 pre-launch review, blocking 3): bench v2, 6 items/cell,
    # complete duplicate-free candidate/unprocessed pairing with finite metrics
    _need(B["meta"].get("bench") == "v2" and B["meta"].get("n_per_cell") == 6, "bench is not v2 with n_per_cell=6")
    bk = lambda r: (r["kind"], r["snr_db"], r["spk"], r["crop"])  # noqa: E731
    cand_rows = [r for r in B["rows"] if r["system"] == B["meta"]["candidate"]]
    unp_rows = [r for r in B["rows"] if r["system"] == "unproc"]
    ck_, uk_ = [bk(r) for r in cand_rows], [bk(r) for r in unp_rows]
    _need(len(ck_) == len(set(ck_)) and set(ck_) == set(uk_) and len(ck_) > 0, "bench candidate/unprocessed grid incomplete or duplicated")
    import math
    _need(all(math.isfinite(r[m]) for r in cand_rows + unp_rows for m in ("sisdr", "stoi", "ace_electro_corr")), "bench has non-finite metrics")
    for kind in ("crowd", "ssn", "white-heldout", "quiet"):
        _need(sum(1 for k in ck_ if k[0] == kind) >= 6, f"bench has too few {kind} rows")
    out = {}
    for snr in (-5.0, 0.0):
        ks = [k for k in GRID if k[3] == snr]
        d = {k: sysrows[cand][k]["d_sisdr"] - sysrows["control"][k]["d_sisdr"] for k in ks}
        dt = {k: sysrows[cand][k]["d_stoi"] - sysrows["control"][k]["d_stoi"] for k in ks}
        per_spk = {t: statistics.fmean(d[k] for k in ks if k[0] == t) for t in TARGETS}
        out[snr] = {"gain": statistics.fmean(d.values()), "stoi_gain": statistics.fmean(dt.values()),
                    "per_voice": per_spk, "voices_improved": sum(v > 0 for v in per_spk.values()),
                    "ci": speaker_bootstrap(per_spk)}
    s = B["summary"][B["meta"]["candidate"]]
    cr = s["crowd"]
    m5, z0 = out[-5.0], out[0.0]
    checks = {
        "A1_m5_gain_ge_0.30": m5["gain"] >= 0.30,
        "A2_speaker_ci_lo_gt_0": m5["ci"][0] > 0,
        "A3_ge_10_of_16_voices": m5["voices_improved"] >= 10,
        "A4_m5_stoi_nonworsening": m5["stoi_gain"] >= 0,
        "S1_0db_safeguard": z0["gain"] >= -0.15 and z0["stoi_gain"] >= -0.003,
        "S2_quiet": s["quiet"]["sisdr"] >= 25 and s["quiet"]["d_stoi"]["mean"] >= -0.02,
        # NaN-safe: every bound individually finite and > 0 (Astra screen-v2 pre-launch review, blocking 2)
        "S3_other_rows": (all(math.isfinite(x) for x in (cr["d_sisdr"]["mean"], cr["d_stoi"]["mean"], cr["d_ace_electro_corr"]["mean"],
                                                          s["ssn"]["d_sisdr"]["mean"], s["white-heldout"]["d_sisdr"]["mean"]))
                          and cr["d_sisdr"]["mean"] >= 3.0 and cr["d_stoi"]["mean"] >= 0.03 and cr["d_ace_electro_corr"]["mean"] >= 0.05
                          and all(math.isfinite(x) and x > 0 for x in (cr["d_sisdr"]["ci_lo"], cr["d_stoi"]["ci_lo"], cr["d_ace_electro_corr"]["ci_lo"]))
                          and s["ssn"]["d_sisdr"]["mean"] >= 3.0 and s["white-heldout"]["d_sisdr"]["mean"] >= 0),
    }
    return {"panel": out, "ctrl_sha": ctrl_sha, "cand_sha": cand_sha}, checks, ("ADVANCE" if all(checks.values()) else "FAIL")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True); ap.add_argument("--bench", required=True)
    ap.add_argument("--cand", required=True); ap.add_argument("--cand-sha", required=True)
    ap.add_argument("--seed", type=int, default=17); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    rows, checks, verdict = judge(a.panel, a.bench, a.cand, a.cand_sha, a.seed)
    for snr, v in rows["panel"].items():
        print(f"panel v2 @{snr:+.0f} dB: gain {v['gain']:+.4f} dB (voice-CI {v['ci'][0]:+.3f}..{v['ci'][1]:+.3f}), STOI {v['stoi_gain']:+.4f}, voices improved {v['voices_improved']}/16")
    print(f"checks {checks}\nSCREEN-V2 {verdict}")
    if a.out:
        Path(a.out).write_text(json.dumps({"seed": a.seed, "rows": {str(k): v for k, v in rows["panel"].items()},
                                           "ctrl_sha": rows["ctrl_sha"], "cand_sha": rows["cand_sha"], "checks": checks, "verdict": verdict}, indent=1))


if __name__ == "__main__":
    main()
