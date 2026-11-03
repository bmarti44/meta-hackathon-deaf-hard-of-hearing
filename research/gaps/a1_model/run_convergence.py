"""A1 v2 dx/dy convergence series (round 2, gap-skeptic S4b).
Fixed physical geometry (v2.3); dx=dy in {0.125, 0.0625, 0.03125} mm.
Representative cases only (std-lib CG cost). Writes convergence.csv.
Run: python3 run_convergence.py"""
import csv, os, time
import model as M

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "convergence.csv")
CASES = [(0, 0.5), (0, 0.25), (0, 1.0), (2, 0.5), (3, 0.5)]
rows = []
print("| grade | dist | dx | mono mm | tri mm | red % | Q ratio | batt "
      "| mono_conv | tri_conv | s |")
print("|---|---|---|---|---|---|---|---|---|---|---|")
for grade, dist in CASES:
    for dx in (0.125, 0.0625, 0.03125):
        p = dict(M.PARAMS); p.update({"dx_mm": dx, "dy_mm": dx})
        t0 = time.time()
        c = M.compare(grade, dist, p=p)
        dt = time.time() - t0
        c = dict(c); c["wall_seconds"] = dt
        rows.append(c)
        print(f"| {grade} | {dist} | {dx} | {c['mono_width_mm']:.4f} | "
              f"{c['tri_width_mm']:.4f} | {c['width_reduction_pct']:.1f} | "
              f"{c['center_charge_ratio_tri_over_mono']:.3f} | "
              f"{c['battery_proxy_ratio_sumabs']:.3f} | "
              f"{c['mono_converged']} | {c['tri_converged']} | {dt:.1f} |")
with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"\nwrote {OUT} ({len(rows)} rows), SEED={M.SEED}")
