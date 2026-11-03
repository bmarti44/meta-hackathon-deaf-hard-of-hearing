"""Second unstick: original, exploratory calculations using stdlib only.

Run: PYTHONDONTWRITEBYTECODE=1 python3 research/unstick2/analyze.py
Writes results.json and cell-addresses.csv beside this file. No historical edits.
Aggregate-data sensitivities are not IPD analyses or clinical gate verdicts.
Synthetic causality counterexample is not inference on the published checkpoint.
"""
from collections import Counter
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import random
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "research/scoring"))
import gate_table as gt


def beta_cf(a, b, x):
    """Continued fraction for incomplete beta; convergence checked."""
    tiny = 1e-300
    c, d = 1.0, 1.0 - (a + b) * x / (a + 1)
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 10001):
        for aa in (m * (b - m) * x / ((a + 2*m - 1) * (a + 2*m)),
                   -(a + m) * (a + b + m) * x / ((a + 2*m) * (a + 2*m + 1))):
            d = 1 + aa*d
            c = 1 + aa/c
            d = 1.0 / (d if abs(d) > tiny else tiny)
            c = c if abs(c) > tiny else tiny
            delta = d*c
            h *= delta
        if abs(delta - 1) < 2e-14:
            return h
    raise ArithmeticError("incomplete beta did not converge")


def ibeta(a, b, x):
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    bt = math.exp(math.lgamma(a+b)-math.lgamma(a)-math.lgamma(b)
                  + a*math.log(x) + b*math.log1p(-x))
    if x < (a+1)/(a+b+2):
        return bt * beta_cf(a, b, x)/a
    return 1 - bt*beta_cf(b, a, 1-x)/b


def t_cdf(t, df):
    tail = .5*ibeta(df/2, .5, df/(df+t*t))
    return 1-tail if t >= 0 else tail


def t_quantile(p, df):
    lo, hi = -1000.0, 1000.0
    for _ in range(100):
        mid = (lo+hi)/2
        if t_cdf(mid, df) < p:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2


def mean_interval(n, mean, sd, level=.95):
    half = t_quantile((1+level)/2, n-1)*sd/math.sqrt(n)
    return [mean-half, mean+half]


def augment_summary(n, mean, sd, extra):
    # Sufficient-statistic reconstruction, NOT invented participant values.
    count = n+len(extra)
    total = n*mean+sum(extra)
    sumsq = (n-1)*sd*sd+n*mean*mean+sum(v*v for v in extra)
    new_mean = total/count
    new_sd = math.sqrt((sumsq-count*new_mean*new_mean)/(count-1))
    return count, new_mean, new_sd


def fisher_two_sided(a, b, c, d):
    n1, n2, k = a+b, c+d, a+c
    denom = math.comb(n1+n2, k)
    probabilities = {x: math.comb(n1, x)*math.comb(n2, k-x)/denom
                     for x in range(max(0, k-n2), min(n1, k)+1)}
    observed = probabilities[a]
    return sum(v for v in probabilities.values() if v <= observed+1e-14)


def threshold_analysis(s):
    n, mean, sd = s["n_complete"], s["mean_benefit_db"], s["sd_paired_benefit_db"]
    ci = mean_interval(n, mean, sd)
    statistic = (mean-3)/(sd/math.sqrt(n))
    missing = []
    for value in [-10, -5, 0, 3, 5.9]:
        nn, mm, ss = augment_summary(n, mean, sd, [value]*(s["n_enrolled"]-n))
        missing.append({"assumed_benefit_each_missing_db": value, "n": nn,
                        "mean_db": mm, "sd_db": ss, "approx_ci95": mean_interval(nn, mm, ss)})
    # Bound on comparator uplift/transport attenuation b; no cross-trial subtraction.
    penalties = [{"hypothetical_penalty_db": b, "remaining_mean_db": mean-b,
                  "remaining_ci95_lower_db": ci[0]-b} for b in [0, .25, .5, 1, 2, 3, 4]]
    # Sensitivity to all reported paired inputs rounded to 0.1 dB.
    corners = [mean_interval(n, m, ss)[0] for m in [mean-.05, mean+.05]
               for ss in [sd-.05, sd+.05]]
    # Minimum # >3 consistent with the rounded mean/variance: between-group SS lower bound.
    total_ss = (n-1)*sd*sd
    possible_counts = [r for r in range(1, n+1)
                       if n*(n-r)/r*(mean-3)**2 <= total_ss+1e-12]
    return {"status": "Exploratory aggregate reanalysis; t-model assumption, not author analysis",
            "approx_mean_ci95": ci, "t_above_3": statistic,
            "one_sided_p_mean_le_3": 1-t_cdf(statistic, n-1),
            "two_sided_p_mean_eq_3": 2*(1-t_cdf(statistic, n-1)),
            "ci95_lower_rounding_range": [min(corners), max(corners)],
            "max_penalty_for_point_mean_at_least_3": mean-3,
            "max_penalty_for_ci95_lower_at_least_3": ci[0]-3,
            "missing_outcome_sensitivity": missing,
            "penalty_sensitivity": penalties,
            "moment_bound_min_count_above_3": min(possible_counts),
            "moment_bound_warning": "Necessary lower bound only, not observed responder count; ignores other published rank/median constraints",
            "assumptions": ["Independent paired listener differences", "Approximate normal mean inference at small n",
                            "Rounded summary statistics", "Missing values are scenarios, not observations",
                            "No multiplicity correction; no pediatric or commercial-comparator transport"]}


def mask_model(x, global_statistics):
    """Synthetic multiplicative denoiser; global vs cumulative normalization.

    A nonlinear model can have zero pre-echo to an isolated impulse despite
    future dependence of its nonzero outputs. This is a counterexample, NOT
    a reimplementation of the clinical study's neural network.
    """
    if global_statistics:
        mu = sum(x)/len(x)
        var = sum((v-mu)**2 for v in x)/len(x)
    out, total, squares = [], 0.0, 0.0
    for i, value in enumerate(x):
        if not global_statistics:
            total += value
            squares += value*value
            mu = total/(i+1)
            var = max(0, squares/(i+1)-mu*mu)
        z = (value-mu)/math.sqrt(var+1e-8)
        out.append(value/(1+math.exp(-z)))
    return out


def causality_analysis(card, architecture):
    offsets = {0}
    for _ in range(card["n_repeats"]):
        for block in range(card["n_blocks"]):
            dilation = 2**block
            offsets = {old + tap*dilation for old in offsets for tap in [-1, 0, 1]}
    frames_right = max(offsets)
    assert frames_right == card["n_repeats"]*(2**card["n_blocks"]-1)
    rng = random.Random(20261103)
    prefix = [rng.uniform(-1, 1) for _ in range(512)]
    signal_a = prefix+[rng.uniform(-.2, .2) for _ in range(512)]
    signal_b = prefix+[rng.uniform(4, 6) for _ in range(512)]
    impulse = [0.0]*1024
    impulse[512] = 1.0
    results = {}
    for label, global_statistics in [("noncausal_global", True), ("causal_cumulative_control", False)]:
        ia = mask_model(impulse, global_statistics)
        ya, yb = mask_model(signal_a, global_statistics), mask_model(signal_b, global_statistics)
        # Leave 16 samples before the common-prefix boundary: nominal 1 ms budget.
        differences = [abs(a-b) for a,b in zip(ya[:496], yb[:496])]
        results[label] = {"impulse_pre_echo_max": max(abs(v) for v in ia[:512]),
                          "impulse_first_nonzero_sample": next(i for i,v in enumerate(ia) if v != 0),
                          "prefix_difference_max_beyond_16_sample_budget": max(differences),
                          "prefix_difference_rms": math.sqrt(sum(d*d for d in differences)/len(differences))}
    assert results["noncausal_global"]["impulse_pre_echo_max"] == 0
    assert results["noncausal_global"]["prefix_difference_max_beyond_16_sample_budget"] > .01
    assert results["causal_cumulative_control"]["prefix_difference_max_beyond_16_sample_budget"] == 0
    return {"status": "T0 synthetic falsification and conditional dependency analysis; no weights executed",
            "seed": 20261103, "latent_dependency_min_frame": min(offsets),
            "latent_dependency_max_frame": max(offsets), "latent_receptive_field_frames": len(offsets),
            "conditional_convolution_future_ms": frames_right*card["stride"]*1000/card["sample_rate"],
            "encoder_kernel_ms": card["kernel_size"]*1000/card["sample_rate"],
            "global_norm_dependency": "Whole supplied segment if gLN is active; no fixed 1 ms bound",
            "configuration_unverified": ["Actual study checkpoint", "Study software version", "causal", "norm_type"],
            "toy_prefix_experiments": results}


def cluster_bounds(s):
    k, n = s["early_short_followup_positive_ears"], s["early_short_followup_children"]
    return {"status": "Conditional arithmetic from search-extracted counts; full-text verification pending",
            "possible_children_with_at_least_one_positive_ear": [math.ceil(k/2), min(k, n)],
            "child_level_tables": [{"positive_children_early": a, "early_children": n,
                                    "positive_children_other": 0, "other_children": s["other_children"],
                                    "fisher_two_sided": fisher_two_sided(a,n-a,0,s["other_children"])}
                                   for a in range(math.ceil(k/2), min(k,n)+1)],
            "interpretation": "No independent-ear inference; no causal effect of implant age; no AAV efficacy, patency or eligibility result"}


def coherence_analysis():
    """Population cross-spectrum of independent, equal-power plane waves.

    S11=S22=N, S12=sum(exp(i*k*d*direction_cosine)); MSC=|S12/N|^2.
    A horizontal ring samples uniform azimuth, a sphere uniform direction
    cosine. This diagnoses J3 B.3.2's ring/spherical-reference ambiguity.
    No speech, head/room response, processor geometry or tolerance is assumed.
    """
    rows = []
    for spacing in [.01, .02, .18]:
        for frequency in [100, 500, 1000, 2000, 4000, 8000]:
            kd = 2*math.pi*frequency*spacing/343.0
            spherical_amplitude = math.sin(kd)/kd
            sphere_quadrature = sum(math.cos(kd*(-1+(j+.5)*2/4096)) for j in range(4096))/4096
            assert abs(sphere_quadrature-spherical_amplitude) < 2e-6
            row = {"assumed_spacing_m": spacing, "frequency_hz": frequency,
                   "spherical_amplitude": spherical_amplitude,
                   "spherical_msc": spherical_amplitude**2,
                   "sphere4096_msc": sphere_quadrature**2}
            for count in [8, 32, 4096]:
                real = sum(math.cos(kd*math.cos(2*math.pi*j/count)) for j in range(count))/count
                imag = sum(math.sin(kd*math.cos(2*math.pi*j/count)) for j in range(count))/count
                row[f"ring{count}_msc"] = real*real+imag*imag
            rows.append(row)
    with (HERE/"coherence.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return {"status": "T0 ideal-field calculation; no actual bench run or acceptance threshold",
            "formula": "MSC = abs(mean(exp(i*k*d*direction_cosine)))**2",
            "speed_of_sound_assumed_m_s": 343.0,
            "example": next(r for r in rows if r["assumed_spacing_m"] == .02 and r["frequency_hz"] == 4000),
            "ring4096_max_msc_error_vs_sphere": max(abs(r["ring4096_msc"]-r["spherical_msc"]) for r in rows),
            "conclusion": "A denser horizontal ring does not become a spherical field; use geometry-matched squared coherence"}


def audit():
    specs = [
        ("gen00", "adapted_v2.csv", "gate-matrix-gen0-v2.md", None),
        ("gen01", "adapted-gen1.csv", "gate-matrix-gen1.md", None),
        ("gen02", "adapted-gen2.csv", "gate-matrix-gen2.md", None),
        ("gen03design", "adapted-gen3.csv", "gate-matrix-gen3.md", "manifest-gen3-P3W3.csv"),
        ("gen04", "adapted-gen4.csv", "gate-matrix-gen4.md", "manifest-gen4-P4W4.csv"),
        ("gen05", "adapted-gen5.csv", "gate-matrix-gen5.md", "manifest-gen5-main.csv"),
        ("gen06", "adapted-gen6.csv", "gate-matrix-gen6.md", "manifest-gen6-main.csv"),
        ("gen07", "adapted-gen7.csv", "gate-matrix-gen7.md", "manifest-gen7-main.csv")]
    rows, checks = [], []
    for gen, source, matrixfile, manifestfile in specs:
        folder = ROOT/"research"/gen/"scoring"
        rr = gt.load_extraction(folder/source)
        manifest = gt.load_manifest(folder/manifestfile) if manifestfile else None
        matrix = gt.build_gate_matrix(rr, manifest)
        missing = gt.find_missing_required_cells(rr, manifest) if manifest else None
        rendered = gt.render_markdown(gt.summarize(rr, matrix), missing)
        same = rendered == (folder/matrixfile).read_text()
        assert same, matrixfile
        checks.append({"input": str((folder/source).relative_to(ROOT)), "rows": len(rr), "matrix_equal": same})
        rows.extend(rr)
    assert len(rows) == 370
    assert not any(r.verdict == "PASS" for r in rows)
    matrix = gt.build_gate_matrix(rows)
    assert not any(gt.check_promotion(r.track, matrix[r.candidate])[0] for r in rows)
    addresses = []
    for relative in ["gen05/scoring/extract-gen5.csv", "gen06/scoring/extract-gen6.csv", "gen07/scoring/extract-gen7.csv"]:
        path = ROOT/"research"/relative
        numbered = [(i, s) for i,s in enumerate(path.read_text().splitlines(), 1) if not s.startswith("#")]
        reader = csv.DictReader(io.StringIO("\n".join(s for _,s in numbered)))
        for data in reader:
            if data["candidate"] in ["GEN5-J1", "GEN6-J2", "GEN5-P5", "GEN6-P6", "GEN7-P7"] and data["gate"] in ["G2", "G2-music", "G4", "G5"]:
                # These files have one physical line per CSV record; reader.line_num handles header.
                addresses.append({"file": str(path.relative_to(ROOT)), "line": numbered[reader.line_num-1][0],
                                  **{k:data[k] for k in ["candidate", "gate", "window", "stratum", "verdict_proposed"]}})
    with (HERE/"cell-addresses.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(addresses[0]))
        writer.writeheader()
        writer.writerows(addresses)
    return {"historical_reproduction": checks, "rows": len(rows), "candidates": len(matrix),
            "row_verdicts": dict(Counter(r.verdict for r in rows)),
            "grades": dict(Counter(r.grade for r in rows)), "promoted": 0,
            "candidate_gates": matrix,
            "note": "J conditional tables excluded; J3 is not a scored candidate"}


def main():
    # Independent identities check numeric routines used for scientific inference.
    assert abs(t_cdf(1,1)-.75) < 1e-12
    assert abs(t_quantile(.975,9)-2.262157162854) < 1e-10
    assert abs(fisher_two_sided(5,0,0,6)-1/462) < 1e-12
    assert augment_summary(3,2,1,[4]) == (4,2.5,math.sqrt(5/3))
    inputs = json.loads((HERE/"inputs.json").read_text())
    results = {"date": "2026-11-03", "authority": "Agent exploratory analysis; no adoption or promotion",
               "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "goal_sha256": hashlib.sha256((ROOT/"GOAL.md").read_bytes()).hexdigest(),
               "input_sha256": hashlib.sha256((HERE/"inputs.json").read_bytes()).hexdigest(),
               "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "python": sys.version, "numeric_self_checks": "passed",
               "srt": threshold_analysis(inputs["srt"]),
               "causality": causality_analysis(inputs["model_card"], inputs["architecture_scenario"]),
               "coherence": coherence_analysis(),
               "ohc": cluster_bounds(inputs["ohc_pointer"]), "audit": audit()}
    (HERE/"results.json").write_text(json.dumps(results, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:results[k] for k in ["srt","causality","coherence","ohc"]}, indent=2))
    print("Historical matrices reproduced:", len(results["audit"]["historical_reproduction"]),
          "rows:", results["audit"]["rows"], "verdicts:", results["audit"]["row_verdicts"])


if __name__ == "__main__":
    main()
