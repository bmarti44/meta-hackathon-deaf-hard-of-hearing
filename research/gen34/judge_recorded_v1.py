"""Gen34 asset judge (judge_recorded_v1): VALID ASSET or INVALID, from integrity checks only (Astra's Gen33 review).
Model scores never decide whether the asset is accepted; they are reported descriptively by run_audit.py.

Checks (all must pass):
 A1 provenance: every needed BRUDEX file is in the fetch manifest, its sha256 on disk matches, and the licence file
    on disk is MIT; the source is doi 10.5281/zenodo.8340195.
 A2 speaker-overlap audit: research/gen34/speaker_audit.json exists, names its basis, and records no overlap between
    the BRUDEX talkers and any speaker used to train or tune Gen19/Gen32 (LibriSpeech train-clean-100 / dev-clean).
 A3 complete grid: for every system, exactly the 192 noisy + 48 target-only items, unique, with registered metadata.
 A4 channel/delay: for every target-only item in the 'low' setting, the broadband level difference and the
    cross-correlation lag of the recorded left/right reference both point to the loudspeaker's side (negative
    azimuth = left louder and earlier).
 A5 bypass identity: every bypass output equals its input exactly.
 A6 duplicate-baseline zero difference: two independent Gen19 runs give identical rows.
 A7 every metric finite; checkpoint hashes match the registered Gen19 and Gen32 files; material hash reproduces.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(HERE))
import recorded_panel as P  # noqa: E402

REG = {"gen19": "80000b64c413ebb878f08695d8744ead8ecf9b183de57cb21acae6157470f367",
       "gen32": "645a062323718958158f32af4398ce3759aae541168db08a3fe286dba57c90b3"}


def needed_files():
    return [P.speech_path(t, s, az).name for t in P.TALKERS for s in P.SETTINGS for az in P.AZ] + \
           [P.noise_path(s).name for s in P.SETTINGS]


def judge(audit_p, rebuild=True):
    A = json.loads(Path(audit_p).read_text())
    checks, notes = {}, {}
    man = json.loads((P.DATA / "manifest.json").read_text())
    lic = (Path("/tmp/brudex_dl/LICENSE").read_text() if Path("/tmp/brudex_dl/LICENSE").exists() else "")
    ok = "10.5281/zenodo.8340195" in man.get("source", "") and "MIT" in lic
    for f in needed_files():
        e = man["files"].get(f)
        ok = ok and e is not None and (P.DATA / f).exists() and hashlib.sha256((P.DATA / f).read_bytes()).hexdigest() == e["sha256"]
    checks["A1_provenance"] = bool(ok)
    au_p = HERE / "speaker_audit.json"
    au = json.loads(au_p.read_text()) if au_p.exists() else {}
    checks["A2_speaker_overlap_audit"] = bool(au.get("overlap") is False and au.get("basis"))
    grid = {(t, s, az, snr) for t in P.TALKERS for s in P.SETTINGS for az in P.AZ for snr in P.SNRS + (None,)}
    by = {}
    ok = True
    for r in A["rows"]:
        k = (r["talker"], r["setting"], r["az"], r["snr"])
        ok = ok and k not in by.get(r["system"], {})
        by.setdefault(r["system"], {})[k] = r
        ok = ok and r["cond"] == ("target_only" if r["snr"] is None else "noisy")
    ok = ok and set(by) == {"bypass", "gen19", "gen19_repeat", "gen32"} and all(set(v) == grid for v in by.values())
    checks["A3_complete_grid"] = bool(ok and len(grid) == 240)
    a4, ok = [], True
    if rebuild:
        items, mh, _ = P.build()
        for it in items:
            if it["cond"] != "target_only" or it["setting"] != "low":
                continue
            L, R_ = it["rL"].astype(np.float64), it["rR"].astype(np.float64)
            ild = 10 * np.log10(np.sum(L ** 2) / np.sum(R_ ** 2))
            seg = slice(P.T0, P.T0 + 3 * P.FS)
            # lag d maximising sum_t L[t] * R[t + d]; d > 0 means the right ear hears it later (left leads)
            lag = max(range(-64, 65), key=lambda d: float(np.dot(L[seg], R_[P.T0 + d:P.T0 + d + 3 * P.FS])))
            want_left = it["az"] < 0
            good = (ild > 0) == want_left and (lag > 0) == want_left and lag != 0
            a4.append({"talker": it["talker"], "az": it["az"], "ild_db": float(ild), "lag_samples": lag, "ok": bool(good)})
            ok = ok and good
        checks["A7_material_hash_reproduces"] = mh == A["material_sha256"]
    checks["A4_channel_delay"] = bool(ok and len(a4) == 16)
    checks["A5_bypass_identity"] = all(r.get("bypass_identical") is True for r in by.get("bypass", {}).values())
    checks["A6_duplicate_baseline_zero_difference"] = all(by["gen19"][k] == {**by["gen19_repeat"][k], "system": "gen19"} for k in grid)
    fin = all(math.isfinite(v) for r in A["rows"] for v in r.values() if isinstance(v, float))
    ck = all(A["checkpoints"][k]["sha256"] == REG[k] for k in REG)
    checks["A7_finite_and_registered_checkpoints"] = bool(fin and ck)
    verdict = "VALID ASSET" if all(checks.values()) else "INVALID"
    return {"checks": checks, "verdict": verdict, "a4_rows": a4}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--audit", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    assert not Path(a.out).exists(), f"REFUSED: {a.out} exists"
    doc = judge(a.audit)
    Path(a.out).write_text(json.dumps(doc, indent=1))
    print(json.dumps(doc["checks"]), doc["verdict"])


if __name__ == "__main__":
    main()
