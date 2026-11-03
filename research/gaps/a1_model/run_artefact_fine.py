"""Gen-3 bounded attack A1: grade-3 / distance-0.25 mm artefact case.

Question: at dx=dy=0.125 mm this is the only sweep case with
0.0% width reduction (0.375 mm in both arms; results_v2.csv).
Round 1 called it a probable grid artefact (SGN line inside
the 0.375 mm sheath); the round-2 convergence series did not
include it. This script reruns exactly that case on the
finer dyadic grids dx=dy in {0.125, 0.0625, 0.03125,
0.015625} mm, with model.py semantics unchanged.

Every physical length in this case is an exact multiple of
every grid spacing used (electrode_y 0.375, modiolar wall
0.25, grade-3 sheath 0.375, distance 0.25, contact spacing
1.0, domain 20x2 mm), so no length snaps to a different
value on any grid here; only discretisation changes.

Uses model.run_case directly (one solve per arm) so solver
residuals/iterations and peaks are recorded; the derived
ratios use the same arithmetic as model.compare.
Writes artefact_fine.csv. Run: python3 run_artefact_fine.py
"""
import csv, os, sys, time
import model as M

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "artefact_fine.csv")
GRADE, DIST = 3, 0.25
DXS = (0.125, 0.0625, 0.03125, 0.015625)
if len(sys.argv) > 1:  # optional subset, e.g. 0.125,0.0625
    DXS = tuple(float(v) for v in sys.argv[1].split(","))

rows = []
print("| dx | nx | ny | elec_j | sheath_rows | sgn_j | sgn_in_sheath "
      "| mono mm (cells) | tri mm (cells) | red % | Q ratio | batt "
      "| mono_conv | tri_conv | s |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for dx in DXS:
    p = dict(M.PARAMS); p.update({"dx_mm": dx, "dy_mm": dx})
    # Geometry bookkeeping recomputed with model.run_case's own
    # formulas (model.py:253-260); not a semantics change.
    elec_j = max(1, int(round(p.get("electrode_y_mm", 0.375) / dx)))
    wall_rows = max(1, int(round(p.get("modiolar_wall_mm", 0.25) / dx)))
    ny = int(p["domain_height_mm"] / dx) + 1
    sgn_j = min(elec_j + max(1, round(DIST / dx)), ny - 2)
    thick, _sig = M.GRADE_PROXY[GRADE]
    sheath_rows = int(round(thick / dx))
    sgn_in_sheath = elec_j <= sgn_j < elec_j + sheath_rows
    t0 = time.time()
    m = M.run_case("monopolar", GRADE, DIST, p=p)
    t = M.run_case("tripolar", GRADE, DIST, p=p)
    dt = time.time() - t0
    q_ratio = t["current_for_unit_peak"] / m["current_for_unit_peak"]
    batt = (t["current_for_unit_peak"] * t["total_abs_current_factor"]
            / m["current_for_unit_peak"])
    row = {
        "grade": GRADE, "distance_mm": DIST, "dx_mm": dx,
        "nx": m["nx"], "ny": m["ny"], "elec_j": elec_j,
        "wall_rows": wall_rows, "sheath_mm": thick,
        "sheath_rows": sheath_rows, "sgn_j": sgn_j,
        "sgn_in_sheath": sgn_in_sheath,
        "sgn_offset_above_elec_mm": (sgn_j - elec_j) * dx,
        "sgn_depth_into_sheath_mm": max(0.0, (sgn_j - elec_j) * dx),
        "sheath_top_j_exclusive": elec_j + sheath_rows,
        "mono_width_mm": m["width_mm_at_unitI"],
        "tri_width_mm": t["width_mm_at_unitI"],
        "mono_width_cells": m["width_mm_at_unitI"] / dx,
        "tri_width_cells": t["width_mm_at_unitI"] / dx,
        "mono_span_global_mm": m["span_global_mm_at_unitI"],
        "tri_span_global_mm": t["span_global_mm_at_unitI"],
        "mono_width_oct": m["width_oct"], "tri_width_oct": t["width_oct"],
        "mono_peak_at_unitI": m["peak_at_unitI"],
        "tri_peak_at_unitI": t["peak_at_unitI"],
        "width_reduction_pct": 100.0 * (1 - t["width_mm_at_unitI"]
                                        / m["width_mm_at_unitI"]),
        "center_charge_ratio_tri_over_mono": q_ratio,
        "battery_proxy_ratio_sumabs": batt,
        "mono_converged": m["solver_converged"],
        "tri_converged": t["solver_converged"],
        "mono_rel_residual": m["solver_rel_residual"],
        "tri_rel_residual": t["solver_rel_residual"],
        "mono_iterations": m["solver_iterations"],
        "tri_iterations": t["solver_iterations"],
        "wall_seconds": dt,
    }
    rows.append(row)
    print(f"| {dx} | {row['nx']} | {row['ny']} | {elec_j} | "
          f"{sheath_rows} | {sgn_j} | {sgn_in_sheath} | "
          f"{row['mono_width_mm']:.5f} ({row['mono_width_cells']:.0f}) | "
          f"{row['tri_width_mm']:.5f} ({row['tri_width_cells']:.0f}) | "
          f"{row['width_reduction_pct']:.2f} | {q_ratio:.4f} | "
          f"{batt:.4f} | {row['mono_converged']} | "
          f"{row['tri_converged']} | {dt:.1f} |", flush=True)

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"\nwrote {OUT} ({len(rows)} rows), SEED={M.SEED}")
