"""Deterministic gate matrix + fitness ranking (GOAL S4/S5/S7, App. A-C).

Model routing (GOAL S9): requested Sol 6.1 (high; code deterministic);
actual runtime model `muse-wonder-full-1.0` fallback (Sol 6.1 unavailable
in this runtime), same effort split. Substitution disclosed per S9 rule 3.
No claim in this file is Sol 6.1 work.

Date: 2026-11-02. Status: pre-registration artefact committed BEFORE
Step 3 scoring (GOAL S11 Step 2). No Step 3 result informed this code.

Exploratory-after-seen label: YES. Evidence seen before writing this
code, exactly: GOAL.md v2.2 S4, S5, S7, S8, S10 and Appendices A-C;
research/frozen_baseline/Step1-pin-summary.md and AppendixA-v1.md;
research/frozen_baseline/frozen_bilateral_eCI_v1.md S2 (D1-D4 formulas);
research/step0/Step0-verified-bibliography.md S2 and S4. NOT seen: any
Gen 0 candidate extraction CSV, any Step 3 sweep/scoring output.

G3b BLOCKED (GOAL S4.2, AppendixA-v1 S6, Step1-pin-summary B01): every
G3b cell is forced INSUFFICIENT, so no promotion is possible at v1.
This is stated for every candidate in every emitted table.

Pure stdlib. Deterministic: no randomness, no clock, sorted tie-breaks.
CLI: python3 gate_table.py input.csv --out matrix.md [--fmea fmea.csv]
"""

from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

SCHEMA_VERSION = "extraction-csv-v1"
REQUIRED_COLUMNS = (
    "candidate", "track", "gate", "window", "stratum", "tier", "grade",
    "delta_g2_db", "delta_g3a_sd", "g1_channels", "burden_rank", "verdict",
)
GATES = ("G1", "G2", "G3a", "G3b", "G4", "G5", "G6")
VERDICTS = ("PASS", "FAIL", "INSUFFICIENT", "NA")
TRACKS = ("P", "R")
G3B_NOTE = "G3b BLOCKED => INSUFFICIENT; no promotion possible at v1"
_WORST_ORDER = {"FAIL": 0, "INSUFFICIENT": 1, "PASS": 2}
_G3B_RANK = {"PASS": 0, "INSUFFICIENT": 1, "FAIL": 2, "NA": 3}
PROBABILITY_BAND_WEIGHTS = {"<0.1%": 1, "0.1-1%": 2, "1-5%": 3, ">5%": 4}
FMEA_COLUMNS = ("candidate", "harm", "severity", "probability_band")


def _norm_gate(raw: str) -> str:
    g = raw.strip()
    upper = g.upper()
    for gate in GATES:
        if upper == gate.upper():
            return gate
    raise ValueError(f"unknown gate {raw!r}; expected one of {GATES}")


def _norm_track(raw: str) -> str:
    t = raw.strip().upper()
    if t.startswith("TRACK"):
        t = t.replace("TRACK", "", 1).strip()
    if t not in TRACKS:
        raise ValueError(f"unknown track {raw!r}; expected P or R")
    return t


def _parse_float(raw: str, field: str, line: int) -> float | None:
    s = (raw or "").strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        return float(s)
    except ValueError:
        raise ValueError(f"line {line}: {field}={raw!r} is not numeric") from None


@dataclass(frozen=True)
class Row:
    candidate: str
    track: str
    gate: str
    window: str
    stratum: str
    tier: str
    grade: str
    delta_g2_db: float | None
    delta_g3a_sd: float | None
    g1_channels: float | None
    burden_rank: float | None
    verdict: str


@dataclass(frozen=True)
class FmeaHarm:
    candidate: str
    harm: str
    severity: int
    probability_band: str


def _read_csv_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.lstrip().startswith("#")]
    reader = csv.DictReader(lines)
    if reader.fieldnames is None:
        raise ValueError(f"{path}: empty CSV (no header)")
    fields = [f.strip() for f in reader.fieldnames]
    rows = [{(k or "").strip(): (v or "") for k, v in r.items() if k}
            for r in reader if any((v or "").strip() for v in r.values())]
    return rows, fields


def load_extraction(path: str | Path) -> list[Row]:
    rows, fields = _read_csv_rows(Path(path))
    missing = [c for c in REQUIRED_COLUMNS if c not in fields]
    if missing:
        raise ValueError(f"extraction CSV missing columns {missing} "
                         f"(schema {SCHEMA_VERSION})")
    out: list[Row] = []
    for i, r in enumerate(rows, start=2):
        candidate = r["candidate"].strip()
        verdict = r["verdict"].strip().upper()
        if not candidate:
            raise ValueError(f"line {i}: candidate is empty")
        if verdict not in VERDICTS:
            raise ValueError(f"line {i}: verdict {verdict!r} not in {VERDICTS}")
        out.append(Row(
            candidate=candidate, track=_norm_track(r["track"]),
            gate=_norm_gate(r["gate"]), window=r["window"].strip(),
            stratum=r["stratum"].strip(), tier=r["tier"].strip(),
            grade=r["grade"].strip(),
            delta_g2_db=_parse_float(r["delta_g2_db"], "delta_g2_db", i),
            delta_g3a_sd=_parse_float(r["delta_g3a_sd"], "delta_g3a_sd", i),
            g1_channels=_parse_float(r["g1_channels"], "g1_channels", i),
            burden_rank=_parse_float(r["burden_rank"], "burden_rank", i),
            verdict=verdict))
    return out


def parse_probability_band(raw: str) -> str:
    s = (raw or "").strip().replace(" ", "").replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("0.1-1", "0.1-1%").replace("1-5", "1-5%") if "%" not in s else s
    if s not in PROBABILITY_BAND_WEIGHTS:
        raise ValueError(f"unknown probability band {raw!r}; expected one of "
                         f"{tuple(PROBABILITY_BAND_WEIGHTS)} (App. C)")
    return s


def g5_aggregate(harms: list[FmeaHarm]) -> int:
    """Track R G5 aggregate: sum of probability-band weights over FMEA
    harms with severity >= 3 (major/catastrophic, App. C). Lower is better."""
    return sum(PROBABILITY_BAND_WEIGHTS[h.probability_band]
               for h in harms if h.severity >= 3)


def load_fmea(path: str | Path) -> dict[str, list[FmeaHarm]]:
    rows, fields = _read_csv_rows(Path(path))
    missing = [c for c in FMEA_COLUMNS if c not in fields]
    if missing:
        raise ValueError(f"FMEA CSV missing columns {missing}")
    out: dict[str, list[FmeaHarm]] = {}
    for i, r in enumerate(rows, start=2):
        try:
            sev = int(float(r["severity"]))
        except ValueError:
            raise ValueError(f"line {i}: severity {r['severity']!r} not an int 1-4") from None
        if sev not in (1, 2, 3, 4):
            raise ValueError(f"line {i}: severity {sev} not in 1-4 (App. C)")
        harm = FmeaHarm(r["candidate"].strip(), r["harm"].strip(), sev,
                        parse_probability_band(r["probability_band"]))
        out.setdefault(harm.candidate, []).append(harm)
    return out


def worst_verdict(verdicts: list[str]) -> str:
    """Worst applicable verdict: FAIL < INSUFFICIENT < PASS. NA rows are
    non-applicable and ignored; all-NA is NA; no rows is INSUFFICIENT
    (missing evidence, never judge-imputed - GOAL S4.2)."""
    applicable = [v for v in verdicts if v != "NA"]
    if not verdicts:
        return "INSUFFICIENT"
    if not applicable:
        return "NA"
    return min(applicable, key=lambda v: _WORST_ORDER[v])


def build_gate_matrix(rows: list[Row]) -> dict[str, dict[str, str]]:
    """(a) Candidate x gate matrix. Each cell is the worst applicable
    window/stratum verdict for that gate. G3b is forced INSUFFICIENT
    for every candidate regardless of input (BLOCKED, S4.2)."""
    by: dict[str, dict[str, list[str]]] = {}
    for row in rows:
        by.setdefault(row.candidate, {}).setdefault(row.gate, []).append(row.verdict)
    matrix: dict[str, dict[str, str]] = {}
    for candidate in sorted(by):
        matrix[candidate] = {g: worst_verdict(by[candidate].get(g, [])) for g in GATES}
        matrix[candidate]["G3b"] = "INSUFFICIENT"
    return matrix


@dataclass(frozen=True)
class Summary:
    candidate: str
    track: str
    matrix: dict[str, str]
    n_fails: int
    n_insufficient: int
    veto_fail: bool
    delta_g2_db: float | None
    delta_g3a_sd: float | None
    g1_channels: float | None
    burden_rank: float | None
    g5_agg: int | None


def summarize(rows: list[Row], matrix: dict[str, dict[str, str]],
              fmea: dict[str, list[FmeaHarm]] | None = None) -> list[Summary]:
    fmea = fmea or {}
    out: list[Summary] = []
    for candidate in sorted(matrix):
        cand = [r for r in rows if r.candidate == candidate]
        tracks = sorted({r.track for r in cand})
        if len(tracks) != 1:
            raise ValueError(f"candidate {candidate!r} declares tracks {tracks}; one only")
        m = matrix[candidate]
        applicable = [v for v in m.values() if v != "NA"]

        def best(field: str, gate: str) -> float | None:
            vals = [getattr(r, field) for r in cand if r.gate == gate
                    and getattr(r, field) is not None]
            if not vals:
                vals = [getattr(r, field) for r in cand if getattr(r, field) is not None]
            return max(vals) if vals else None

        burdens = [r.burden_rank for r in cand if r.burden_rank is not None]
        out.append(Summary(
            candidate=candidate, track=tracks[0], matrix=m,
            n_fails=sum(1 for v in applicable if v == "FAIL"),
            n_insufficient=sum(1 for v in applicable if v == "INSUFFICIENT"),
            veto_fail=(m["G4"] == "FAIL" or m["G5"] == "FAIL"),
            delta_g2_db=best("delta_g2_db", "G2"),
            delta_g3a_sd=best("delta_g3a_sd", "G3a"),
            g1_channels=best("g1_channels", "G1"),
            burden_rank=min(burdens) if burdens else None,
            g5_agg=g5_aggregate(fmea[candidate]) if candidate in fmea else None))
    return out


def _desc(value: float | None) -> float:
    return -value if value is not None else float("inf")


def track_p_key(s: Summary) -> tuple:
    """(b) GOAL S7 Track P lexicographic fitness, ascending = better.
    1 G4/G5 veto FAIL demoted last, then fewest FAILs; 2 fewest
    INSUFFICIENT among applicable; 3 largest G2; 4 largest G3a;
    5 G3b verdict (constant INSUFFICIENT at v1); 6 largest G1 with
    NA/missing last; 7 lowest burden. Candidate name is a final
    reproducibility tie-break only (not a GOAL rule)."""
    g1_na = s.matrix["G1"] == "NA" or s.g1_channels is None
    return (1 if s.veto_fail else 0, s.n_fails, s.n_insufficient,
            _desc(s.delta_g2_db), _desc(s.delta_g3a_sd),
            _G3B_RANK[s.matrix["G3b"]],
            1 if g1_na else 0, 0.0 if g1_na else -s.g1_channels,  # type: ignore[operator]
            s.burden_rank if s.burden_rank is not None else float("inf"),
            s.candidate)


def track_r_key(s: Summary) -> tuple:
    """(c) Track R ranking: largest G1 first (NA/missing last), then
    smallest G5 aggregate (missing FMEA last), then candidate name."""
    g1_na = s.matrix["G1"] == "NA" or s.g1_channels is None
    return (1 if g1_na else 0, 0.0 if g1_na else -s.g1_channels,  # type: ignore[operator]
            s.g5_agg if s.g5_agg is not None else float("inf"), s.candidate)


def rank_track_p(summaries: list[Summary]) -> list[Summary]:
    return sorted((s for s in summaries if s.track == "P"), key=track_p_key)


def rank_track_r(summaries: list[Summary]) -> list[Summary]:
    return sorted((s for s in summaries if s.track == "R"), key=track_r_key)


def check_promotion(track: str, matrix: dict[str, str]) -> tuple[bool, str]:
    """(d) GOAL S4.2 promotion. Track P device: PASS on G1,G2,G3a,G3b,
    G4,G5,G6. Track P pathway (F/G/H, G1=NA disclosed): PASS on G2-G6.
    Track R is never promoted (watch-list, S4.1/S10). Pathway vs device
    is read off G1==NA (the only G1-NA route S4.2 allows). At v1 the
    forced G3b INSUFFICIENT makes every result False."""
    if track != "P":
        return False, f"Track R watch-list, never promoted for infants; {G3B_NOTE}"
    if matrix.get("G1") == "NA":
        needed = ("G2", "G3a", "G3b", "G4", "G5", "G6")
        kind = "pathway (G1 NA disclosed)"
    else:
        needed = GATES
        kind = "device"
    blocking = [g for g in needed if matrix.get(g) != "PASS"]
    if blocking:
        return False, f"{kind}: not PASS on {','.join(blocking)}; {G3B_NOTE}"
    return True, f"{kind}: PASS on all required gates"


def _objectives(s: Summary) -> tuple[float, ...]:
    """Pareto objectives, all 'larger is better': -fails, -insufficient,
    G2, G3a, G1, -burden, -G5agg. Missing = worst (-inf after sign)."""
    def mx(v: float | None) -> float:
        return v if v is not None else float("-inf")

    def mn(v: float | None) -> float:
        return -v if v is not None else float("-inf")
    return (-s.n_fails, -s.n_insufficient, mx(s.delta_g2_db), mx(s.delta_g3a_sd),
            mx(None if s.matrix["G1"] == "NA" else s.g1_channels),
            mn(s.burden_rank), mn(float(s.g5_agg) if s.g5_agg is not None else None))


def pareto_set(summaries: list[Summary]) -> list[Summary]:
    """(e) Non-dominated candidates within each track. A dominates B if
    A is at least as good on every objective and strictly better on one."""
    out: list[Summary] = []
    for track in TRACKS:
        group = [s for s in summaries if s.track == track]
        for s in group:
            so = _objectives(s)
            dominated = any(
                o is not s and all(a >= b for a, b in zip(_objectives(o), so))
                and any(a > b for a, b in zip(_objectives(o), so))
                for o in group)
            if not dominated:
                out.append(s)
    return sorted(out, key=lambda s: (s.track, s.candidate))


def _fmt(value: float | int | None) -> str:
    if value is None:
        return "NA"
    return f"{value:g}"


_HEADER = """# Gate matrix + fitness ranking (deterministic, gate_table.py)

> Model routing (GOAL S9): requested **Sol 6.1** (high; code
> deterministic); actual **`muse-wonder-full-1.0` fallback**, same
> effort split. Date: **2026-11-02**. Pre-registration: generated by
> code committed **BEFORE Step 3 scoring**.
> Exploratory-after-seen: **YES** - GOAL.md v2.2 S4/S5/S7/S8/S10 +
> Appendices A-C, Step1-pin-summary.md, AppendixA-v1.md,
> frozen_bilateral_eCI_v1.md S2, and Step0-verified-bibliography.md
> S2/S4 were seen before this code was written. No Gen 0 extraction
> CSV or Step 3 output was seen.
> **G3b BLOCKED => every G3b cell INSUFFICIENT; no promotion is
> possible at v1** (GOAL S4.2). INSUFFICIENT is never imputed.
"""


def render_markdown(summaries: list[Summary]) -> str:
    lines = [_HEADER, "## (a) Gate matrix (candidate x gate, worst applicable window)", ""]
    lines.append("| candidate | track | " + " | ".join(GATES) + " | G3b/promotion note |")
    lines.append("|---|---|" + "---|" * len(GATES) + "---|")
    for s in sorted(summaries, key=lambda x: (x.track, x.candidate)):
        cells = " | ".join(s.matrix[g] for g in GATES)
        lines.append(f"| {s.candidate} | {s.track} | {cells} | {G3B_NOTE} |")
    lines += ["", "## (b) Track P lexicographic ranking (GOAL S7)", "",
              "| rank | candidate | veto(G4/G5 FAIL) | FAILs | INSUFFICIENT | "
              "delta_g2_db | delta_g3a_sd | G3b | g1_channels | burden_rank | note |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(rank_track_p(summaries), start=1):
        lines.append(f"| {i} | {s.candidate} | {'DEMOTED' if s.veto_fail else '-'} | "
                     f"{s.n_fails} | {s.n_insufficient} | {_fmt(s.delta_g2_db)} | "
                     f"{_fmt(s.delta_g3a_sd)} | {s.matrix['G3b']} | {_fmt(s.g1_channels)} | "
                     f"{_fmt(s.burden_rank)} | {G3B_NOTE} |")
    lines += ["", "## (c) Track R ranking (G1, then G5 aggregate)", "",
              "G5 aggregate = sum over FMEA harms with severity >= 3 of "
              "probability-band weight {<0.1%:1, 0.1-1%:2, 1-5%:3, >5%:4} "
              "(--fmea input; NA = no FMEA rows, ranked last on this key).", "",
              "| rank | candidate | g1_channels | g5_aggregate | note |",
              "|---|---|---|---|---|"]
    for i, s in enumerate(rank_track_r(summaries), start=1):
        lines.append(f"| {i} | {s.candidate} | {_fmt(s.g1_channels)} | "
                     f"{_fmt(s.g5_agg)} | {G3B_NOTE} |")
    lines += ["", "## (d) Promotion check (GOAL S4.2)", "",
              "| candidate | track | promoted | reason |", "|---|---|---|---|"]
    for s in sorted(summaries, key=lambda x: (x.track, x.candidate)):
        ok, reason = check_promotion(s.track, s.matrix)
        lines.append(f"| {s.candidate} | {s.track} | {str(ok).upper()} | {reason} |")
    pareto = pareto_set(summaries)
    lines += ["", "## (e) Pareto set (non-dominated, within track; transparency only)", "",
              "| candidate | track | note |", "|---|---|---|"]
    for s in pareto:
        lines.append(f"| {s.candidate} | {s.track} | {G3B_NOTE} |")
    if not pareto:
        lines.append("| (none) | | |")
    lines += ["", "Ranking/promotion use the lexicographic rule (b)/(d), not "
              "the Pareto set (GOAL S7). Missing numeric inputs rank last "
              "on their key and are shown as NA; they are never imputed.", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gate matrix + GOAL S7 fitness ranking")
    ap.add_argument("input", help=f"extraction CSV (schema {SCHEMA_VERSION})")
    ap.add_argument("--out", help="output Markdown path (default: stdout)")
    ap.add_argument("--fmea", help="optional FMEA CSV: candidate,harm,severity,probability_band")
    args = ap.parse_args(argv)
    try:
        rows = load_extraction(args.input)
        fmea = load_fmea(args.fmea) if args.fmea else {}
        summaries = summarize(rows, build_gate_matrix(rows), fmea)
    except (ValueError, OSError) as exc:
        print(f"gate_table: error: {exc}", file=sys.stderr)
        return 2
    text = render_markdown(summaries)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

