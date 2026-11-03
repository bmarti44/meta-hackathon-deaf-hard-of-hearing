"""A1 kill-test sweep v2 (deterministic, SEED pinned in model.py).
Writes results_v2.csv (v1 results.csv preserved untouched for
md5 provenance) and prints the table for ../round2-A1-fix.md.
Run: python3 run_sweep.py"""
import csv, os
import model as M

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_v2.csv")
rows = []
print("| grade(proxy) | dist mm | mono mm | tri mm | mono oct | tri oct "
      "| width red. % | Q ratio | batt proxy |")
print("|---|---|---|---|---|---|---|---|---|")
for grade in (0, 1, 2, 3):
    for dist in (0.25, 0.5, 1.0):
        c = M.compare(grade, dist)
        rows.append(c)
        print(f"| {grade} | {dist} | {c['mono_width_mm']:.2f} | "
              f"{c['tri_width_mm']:.2f} | {c['mono_width_oct']:.2f} | "
              f"{c['tri_width_oct']:.2f} | {c['width_reduction_pct']:.1f} | "
              f"{c['center_charge_ratio_tri_over_mono']:.2f} | "
              f"{c['battery_proxy_ratio_sumabs']:.2f} |")

print("\nSensitivity (grade 2, dist 0.5 unless varied):")
base = M.PARAMS
for label, kw in [
    ("sigma_f=0.5 (partial-tripolar)", {"sigma_f": 0.5}),
    ("sigma_f=1.0 (full tripolar)", {"sigma_f": 1.0}),
    ("sheath sigma=1.2 (no shunt block)", {"sigma_sheath_override": 1.2}),
    ("sheath sigma=0.0334 at grade-2 thickness",
     {"sigma_sheath_override": 0.0334}),
]:
    c = M.compare(2, 0.5, **kw)
    print(f"- {label}: width red. {c['width_reduction_pct']:.1f}%, "
          f"Q ratio {c['center_charge_ratio_tri_over_mono']:.2f}, "
          f"batt {c['battery_proxy_ratio_sumabs']:.2f}")
for label, over in [
    ("threshold_frac=0.3", {"threshold_frac": 0.3}),
    ("threshold_frac=0.7", {"threshold_frac": 0.7}),
    ("spacing=0.7mm", {"contact_spacing_mm": 0.7}),
    ("spacing=1.5mm", {"contact_spacing_mm": 1.5}),
    ("perilymph=1.43 S/m", {"sigma_perilymph_S_per_m": 1.43}),
    ("L=28mm (oct only)", {"cochlea_length_mm": 28.0}),
]:
    p = dict(base); p.update(over)
    c = M.compare(2, 0.5, p=p)
    print(f"- {label}: mono {c['mono_width_mm']:.2f}mm/"
          f"{c['mono_width_oct']:.2f}oct tri {c['tri_width_mm']:.2f}mm/"
          f"{c['tri_width_oct']:.2f}oct red. "
          f"{c['width_reduction_pct']:.1f}% Q "
          f"{c['center_charge_ratio_tri_over_mono']:.2f}")

print("\nASSUMED-current Shannon BLOCK -- bracketed, NOT a limit:")
for ima in (0.2, 0.5, 1.0, 2.0):
    q, qnc, d, kc, kni = M.absolute_charge_check(ima)
    print(f"- I={ima} mA x 25us: Q={qnc:.1f} nC/ph ({q:.4f} uC/ph), "
          f"D={d:.1f} uC/cm2/ph (area 0.003 cm2 ASSUMED), "
          f"k_classic_uC={kc:.2f} / k_Li_nC={kni:.2f} "
          f"(boundary 1.5-2.0 cited in both; primary unpinned)")

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)
print(f"\nwrote {OUT} ({len(rows)} rows), SEED={M.SEED}")
