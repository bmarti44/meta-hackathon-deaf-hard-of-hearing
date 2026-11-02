"""
A1 kill-test T0 in-silico model (attack round 1, GOAL S7 rule 4).

Transparent 2-D finite-difference volume-conduction model of an
unwound scala-tympani strip:  div( sigma(x,y) grad V ) = -I_src.

Modes: monopolar vs tripolar (focusing coefficient sigma_f; the
phased-array limit is represented by the same 3-contact weights).
Fibrosis: low-conductivity sheath around the array, thickness /
conductivity swept as a Seyyedi & Nadol grade (0-3) *proxy*.
Electrode-neuron distance swept. Endpoint: excitation width on the
SGN line in mm and octaves (Greenwood), loudness-balanced
(peak neural drive matched across modes), vs charge per phase.

Environment checked 2026-11-02: Python 3.14.8, numpy NOT
installed (ModuleNotFoundError) -> stdlib only, by design.
Deterministic: no RNG anywhere; SEED pinned for provenance only.

LABEL (GOAL S5.1): T0 modelled sub-claim, conditional on the
assumptions table in attack-A1-killtest.md. Never a G1 PASS,
never a promotion probability.

CITED parameters (full text inspected 2026-11-02):
  perilymph sigma = 1.2 S/m; bone 0.0334-0.0836 S/m; healthy
  modiolus eff. 0.2734 S/m; ossified/fibrous-filled worst case
  0.0334 S/m  -- Sriperumbudur et al. 2024, Sci Rep 14:9593,
  PMID 38671022, PMC11053021 (Europe PMC fullTextXML).
  Greenwood human: F = 165.4 * (10**(2.1*x) - 0.88), x =
  proportion of basilar-membrane length from the apex
  -- Dhanasingh 2021, PMID 33474539, PMC7801236, eq. (6);
  original: Greenwood 1990, PMID 2373794.
  Shannon: k = log10(Q[uC/ph]) + log10(D[uC/cm2/ph]);
  proposed damage boundary k = 1.5-2.0; 1.85 used as example
  threshold; best-fit 1.79-1.86 (accuracy only 63.9%)
  -- Shannon 1992, PMID 1592409 (abstract: no numeric k);
  Li et al. 2024, PMID 38885676, PMC11641559, eq. (1) + S2.2.
  Seyyedi & Nadol 0-3 severity at 3x 1-mm segments; granuloma
  27/28, basal > distal -- PMID 25122600 (MEDLINE inspected;
  AppendixA-v1 N4). Per-grade rubric NOT extracted -> the
  grade -> (thickness, sigma) map below is ASSUMED.
Everything else is ASSUMED and swept; see PARAMS.
"""
import math

SEED = 20261102  # pinned; solver is deterministic, no RNG used

PARAMS = {
    # cited
    "sigma_perilymph_S_per_m": 1.2,        # sens 1.2-1.43 (cited range)
    "sigma_bone_S_per_m": 0.0334,          # sens 0.0334-0.0836 (cited)
    "sigma_modiolus_eff_S_per_m": 0.2734,  # cited, 20% porosity
    "greenwood_A": 165.4, "greenwood_a": 2.1, "greenwood_k": 0.88,
    "shannon_k_limit": 1.85,               # sens 1.5 / 1.79 / 2.0 (cited range)
    # ASSUMED (no named device filed in workspace; swept in run)
    "domain_length_mm": 20.0,              # modelled strip, sens: convergence test
    "domain_height_mm": 2.0,               # scala + modiolar wall strip
    "dx_mm": 0.125, "dy_mm": 0.125,
    "contact_spacing_mm": 1.0,             # sens 0.7 / 1.0 / 1.5
    "contact_area_cm2": 0.003,             # 0.3 mm2; sens 0.0015-0.006
    "pulse_width_us": 25.0,                # sens 18-50
    "threshold_frac": 0.5,                 # width at >=50% of balanced peak; sens 0.3/0.7
    "cochlea_length_mm": 35.0,             # Greenwood L; sens 28-35 (33.46 cited example)
    "electrode_frac_from_apex": 0.65,      # mid-array place for octave conversion
}
# ASSUMED grade->sheath proxy map (rubric unextracted; sigma bounds cited)
GRADE_PROXY = {  # grade: (sheath thickness mm, sheath sigma S/m)
    0: (0.0, 1.2), 1: (0.125, 0.30), 2: (0.25, 0.10), 3: (0.375, 0.0334),
}


def greenwood_hz(frac_from_apex, p=PARAMS):
    return p["greenwood_A"] * (10.0 ** (p["greenwood_a"] * frac_from_apex)
                                - p["greenwood_k"])


def octave_width(center_mm_from_apex, width_mm, p=PARAMS):
    L = p["cochlea_length_mm"]
    f1 = greenwood_hz((center_mm_from_apex - width_mm / 2) / L, p)
    f2 = greenwood_hz((center_mm_from_apex + width_mm / 2) / L, p)
    return math.log2(f2 / f1)


def shannon_k(charge_uc, charge_density_uc_cm2):
    return math.log10(charge_uc) + math.log10(charge_density_uc_cm2)


def build_sigma(nx, ny, elec_j, sheath_rows, sigma_sheath, p=PARAMS):
    """sigma[j][i]; j=0 modiolar wall (bone/modiolus blend), top perilymph."""
    s = [[p["sigma_perilymph_S_per_m"]] * nx for _ in range(ny)]
    for j in range(0, 2):  # modiolar wall strip
        s[j] = [p["sigma_modiolus_eff_S_per_m"]] * nx
    for j in range(elec_j, min(ny, elec_j + sheath_rows)):
        s[j] = [sigma_sheath] * nx
    return s


def solve(nx, ny, sigma, sources, dx, tol=1e-9, max_iter=8000):
    """Conjugate gradient on 5-pt div(sigma grad V); V=0 on boundary
    (distant monopolar return). sources: dict (j,i)->current [arb. units].
    Returns flat V list. Deterministic."""
    n = nx * ny
    b = [0.0] * n
    for (j, i), cur in sources.items():
        b[j * nx + i] = cur

    def idx(j, i):
        return j * nx + i

    def matvec(x):
        y = [0.0] * n
        for j in range(ny):
            for i in range(nx):
                k = idx(j, i)
                if j == 0 or i == 0 or j == ny - 1 or i == nx - 1:
                    y[k] = x[k]
                    continue
                sij = sigma[j][i]
                acc = 0.0
                for jj, ii in ((j, i - 1), (j, i + 1), (j - 1, i), (j + 1, i)):
                    sf = 2.0 / (1.0 / sij + 1.0 / sigma[jj][ii])  # harmonic face
                    acc += sf * (x[k] - x[idx(jj, ii)])
                y[k] = acc / (dx * dx)
        return y

    x = [0.0] * n
    r = b[:]
    # boundary rows: enforce V=0 by zeroing residual there
    for j in range(ny):
        for i in range(nx):
            if j == 0 or i == 0 or j == ny - 1 or i == nx - 1:
                r[idx(j, i)] = 0.0
    pvec = r[:]
    rs = sum(v * v for v in r)
    bnorm = math.sqrt(sum(v * v for v in b)) or 1.0
    for _ in range(max_iter):
        if math.sqrt(rs) / bnorm < tol:
            break
        Ap = matvec(pvec)
        alpha = rs / sum(pv * av for pv, av in zip(pvec, Ap))
        x = [xi + alpha * pv for xi, pv in zip(x, pvec)]
        r = [ri - alpha * av for ri, av in zip(r, Ap)]
        rs_new = sum(v * v for v in r)
        pvec = [ri + (rs_new / rs) * pv for ri, pv in zip(r, pvec)]
        rs = rs_new
    return x


def excitation_width(profile, dx, frac):
    peak = max(profile)
    if peak <= 0:
        return 0.0, peak
    above = [i for i, v in enumerate(profile) if v >= frac * peak]
    return (max(above) - min(above) + 1) * dx, peak


def run_case(mode, grade, distance_mm, p=PARAMS, sigma_f=0.9,
             sigma_sheath_override=None):
    """One loudness-unit run at I_center=1 (arb.). Returns dict with
    width at unit peak-scaled current + current needed for unit peak
    (the loudness-balance cost), so charge ratios are exact."""
    dx, dy = p["dx_mm"], p["dy_mm"]
    nx = int(p["domain_length_mm"] / dx) + 1
    ny = int(p["domain_height_mm"] / dy) + 1
    elec_j = 3
    sgn_j = elec_j + max(1, round(distance_mm / dy))
    sgn_j = min(sgn_j, ny - 2)
    thick, sig_sh = GRADE_PROXY[grade]
    if sigma_sheath_override is not None:
        sig_sh = sigma_sheath_override
    sheath_rows = int(round(thick / dy))
    sigma = build_sigma(nx, ny, elec_j, sheath_rows, sig_sh, p)
    ci = nx // 2
    off = int(round(p["contact_spacing_mm"] / dx))
    if mode == "monopolar":
        src = {(elec_j, ci): 1.0}
        sum_abs = 1.0
    elif mode == "tripolar":
        src = {(elec_j, ci): 1.0,
               (elec_j, ci - off): -sigma_f / 2.0,
               (elec_j, ci + off): -sigma_f / 2.0}
        sum_abs = 1.0 + sigma_f
    else:
        raise ValueError(mode)
    V = solve(nx, ny, sigma, src, dx)
    profile = [V[sgn_j * nx + i] for i in range(nx)]
    width_mm, peak = excitation_width(profile, dx, p["threshold_frac"])
    center_mm = p["electrode_frac_from_apex"] * p["cochlea_length_mm"]
    return {
        "mode": mode, "grade": grade, "distance_mm": distance_mm,
        "sigma_sheath": sig_sh, "sheath_mm": thick, "sigma_f": sigma_f,
        "width_mm_at_unitI": width_mm, "peak_at_unitI": peak,
        "current_for_unit_peak": 1.0 / peak,
        "total_abs_current_factor": sum_abs,
        "width_oct": octave_width(center_mm, width_mm, p),
    }


def compare(grade, distance_mm, p=PARAMS, sigma_f=0.9, **kw):
    """Loudness-balanced comparison: scale each mode to the same peak.
    Charge ratio uses ACTIVE (center) contact charge (binds Shannon);
    battery proxy uses sum|I| across contacts."""
    m = run_case("monopolar", grade, distance_mm, p, sigma_f, **kw)
    t = run_case("tripolar", grade, distance_mm, p, sigma_f, **kw)
    # widths are scale-invariant (linear system, frac-of-peak width)
    q_ratio = t["current_for_unit_peak"] / m["current_for_unit_peak"]
    batt_ratio = (t["current_for_unit_peak"] * t["total_abs_current_factor"]
                  / m["current_for_unit_peak"])
    return {
        "grade": grade, "distance_mm": distance_mm,
        "mono_width_mm": m["width_mm_at_unitI"],
        "tri_width_mm": t["width_mm_at_unitI"],
        "mono_width_oct": m["width_oct"], "tri_width_oct": t["width_oct"],
        "width_reduction_pct": 100.0 * (1 - t["width_mm_at_unitI"]
                                        / m["width_mm_at_unitI"]),
        "center_charge_ratio_tri_over_mono": q_ratio,
        "battery_proxy_ratio_sumabs": batt_ratio,
    }


def absolute_charge_check(current_ma_assumed, p=PARAMS):
    """Illustrative ONLY (no named device): Q and Shannon k for an
    ASSUMED monopolar comfortable current. Not a filed limit."""
    q_uc = current_ma_assumed * 1e-3 * p["pulse_width_us"] * 1e-6 * 1e6
    d = q_uc / p["contact_area_cm2"]
    return q_uc, d, shannon_k(q_uc, d)
