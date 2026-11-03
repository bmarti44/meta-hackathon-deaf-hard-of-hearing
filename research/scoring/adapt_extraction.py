"""Adapt Gen 0 extraction CSV (14-col, research/gen00/extraction-schema.md)
to gate_table extraction-csv-v1 (12-col). Closes Step 2 skeptic F1.

Model routing: requested Sol 6.1 (deterministic code); actual
muse-wonder-full-1.0 fallback. Date: 2026-11-02. Pre-registration
BEFORE Step 3 scoring. G3b BLOCKED => INSUFFICIENT (gate_table also
forces this). Mapping rules (documented, no silent invention):
- track: A,B,F,G,H -> P; C,D,E -> R (GOAL S4.1/S8). FROZEN/Q0 rows skipped.
- gate sublabels collapse: G1-spectral/G1-temporal -> G1; G2-music -> G2;
  G4-AAV -> G4 (gate_table takes worst verdict per gate, so no loss of FAILs).
- verdict_proposed -> verdict: NA-prereg/NA -> NA; PROVISIONAL-SIGNAL ->
  INSUFFICIENT (GOAL S5.2: Low/provisional never PASS; gate_table has no
  provisional state); PASS/FAIL/INSUFFICIENT pass through.
- delta_g2_db/delta_g3a_sd/g1_channels: parsed from effect only if effect
  is a bare number; else blank. burden_rank: blank (assigned at scoring).
Usage: python3 adapt_extraction.py in.csv out.csv
"""
import csv
import sys

TRACK = {"A": "P", "B": "P", "C": "R", "D": "R", "E": "R", "F": "P", "G": "P", "H": "P"}
GATE = {"G1-spectral": "G1", "G1-temporal": "G1", "G2-music": "G2", "G4-AAV": "G4"}
VERDICT = {"NA-prereg": "NA", "NA": "NA", "PROVISIONAL-SIGNAL": "INSUFFICIENT",
           "PASS": "PASS", "FAIL": "FAIL", "INSUFFICIENT": "INSUFFICIENT"}
OUT = ["candidate", "track", "gate", "window", "stratum", "tier", "grade",
       "delta_g2_db", "delta_g3a_sd", "g1_channels", "burden_rank", "verdict"]


def _num(s):
    try:
        return str(float(s))
    except (TypeError, ValueError):
        return ""


def adapt(rows, track_map=None):
    tracks = dict(TRACK)
    if track_map:
        tracks.update(track_map)
    out = []
    for r in rows:
        cand = (r.get("candidate") or "").strip()
        if cand not in tracks:
            continue
        gate = GATE.get((r.get("gate") or "").strip(), (r.get("gate") or "").strip())
        verdict = VERDICT.get((r.get("verdict_proposed") or "").strip())
        if verdict is None:
            raise ValueError(f"unknown verdict_proposed: {r.get('verdict_proposed')!r}")
        eff = _num((r.get("effect") or "").strip())
        out.append({
            "candidate": cand, "track": tracks[cand], "gate": gate,
            "window": (r.get("window") or "").strip(),
            "stratum": (r.get("stratum") or "").strip(),
            "tier": (r.get("tier") or "").strip(),
            "grade": (r.get("grade") or "").strip(),
            "delta_g2_db": eff if gate == "G2" else "",
            "delta_g3a_sd": eff if gate == "G3a" else "",
            "g1_channels": eff if gate == "G1" else "",
            "burden_rank": "", "verdict": verdict,
        })
    return out


def load_track_map(path):
    with open(path, newline="") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    out = {}
    for r in csv.DictReader(lines):
        cand, track = (r.get("candidate") or "").strip(), (r.get("track") or "").strip().upper()
        if track not in ("P", "R"):
            raise ValueError(f"track-map: bad track {track!r} for {cand!r}")
        out[cand] = track
    return out


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--track-map=")]
    maps = [a.split("=", 1)[1] for a in argv[1:] if a.startswith("--track-map=")]
    if len(args) != 2:
        print(__doc__)
        return 2
    track_map = load_track_map(maps[0]) if maps else None
    with open(args[0], newline="") as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    rows = list(csv.DictReader(lines))
    adapted = adapt(rows, track_map)
    with open(args[1], "w", newline="") as f:
        f.write("# adapted by adapt_extraction.py from Gen0 14-col schema; schema: extraction-csv-v1\n")
        w = csv.DictWriter(f, fieldnames=OUT)
        w.writeheader()
        w.writerows(adapted)
    print(f"adapted {len(adapted)} rows -> {args[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
