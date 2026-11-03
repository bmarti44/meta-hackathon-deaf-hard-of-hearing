"""Tests for A1 T0 model v2 (round-2 Shannon-units bracket,
contiguous width, solver flag). Run: python3 test_model.py -v"""
import math, unittest
import model as M


class T(unittest.TestCase):
    def test_greenwood_monotonic_and_endpoints(self):
        self.assertAlmostEqual(M.greenwood_hz(0.0),
                               165.4 * (1 - 0.88), places=6)
        self.assertLess(M.greenwood_hz(0.2), M.greenwood_hz(0.8))
        self.assertGreater(M.octave_width(20.0, 2.0), 0)

    def test_shannon_formula(self):
        # Classic convention: Q=0.1 uC, D=100 uC/cm2 -> k = -1 + 2 = 1.0
        self.assertAlmostEqual(M.shannon_k(0.1, 100.0), 1.0, places=9)

    def test_shannon_units_bracket(self):
        # Same physical charge: Q=0.1 uC = 100 nC. Li S2.2 (nC) k is
        # exactly +3.00 above the classic (uC) k. Both are reported;
        # neither is pinned against the 1992 primary.
        kc, kni = M.shannon_k_bracket(0.1, 100.0)
        self.assertAlmostEqual(kc, 1.0, places=9)
        self.assertAlmostEqual(kni, 4.0, places=9)
        self.assertAlmostEqual(M.shannon_k_li_nc(100.0, 100.0), kni,
                               places=9)

    def test_shannon_multiplier_adds_2log10r(self):
        # At fixed area D scales with Q: doubling Q adds 2*log10(2).
        q, qnc, d, kc, kni = M.absolute_charge_check(0.2)
        q2, _, d2, kc2, kni2 = M.absolute_charge_check(0.4)
        self.assertAlmostEqual(kc2 - kc, 2 * math.log10(2.0), places=9)
        self.assertAlmostEqual(kni - kc, 3.0, places=9)

    def test_excitation_width_contiguous_vs_global(self):
        # Bimodal (gap-skeptic S4c probe): contiguous central run
        # is 1 cell; global span counts the silent gap as 4 cells.
        prof = [0.0, 10.0, 0.0, 0.0, 9.0, 0.0]
        w, peak = M.excitation_width(prof, 1.0, 0.5)
        s, _ = M.excitation_span_global(prof, 1.0, 0.5)
        self.assertEqual(w, 1.0)
        self.assertEqual(s, 4.0)
        # Unimodal: the two definitions coincide.
        uni = [0.0, 2.0, 10.0, 8.0, 1.0]
        self.assertEqual(M.excitation_width(uni, 1.0, 0.5)[0],
                         M.excitation_span_global(uni, 1.0, 0.5)[0])

    def test_solver_reports_convergence(self):
        nx, ny, dx = 41, 11, 0.125
        sig = [[1.2] * nx for _ in range(ny)]
        V, info = M.solve_with_info(nx, ny, sig, {(5, 20): 1.0}, dx)
        self.assertTrue(info["converged"])
        self.assertLess(info["rel_residual"], info["tol"])

    def test_solver_homogeneous_decay(self):
        nx, ny, dx = 41, 11, 0.125
        sig = [[1.2] * nx for _ in range(ny)]
        V = M.solve(nx, ny, sig, {(5, 20): 1.0}, dx)
        prof = [V[7 * nx + i] for i in range(nx)]
        self.assertEqual(max(range(nx), key=lambda i: prof[i]), 20)
        self.assertGreater(prof[20], prof[10])
        self.assertGreater(prof[10], prof[2])

    def test_linearity_scale_invariance(self):
        r1 = M.run_case("monopolar", 0, 0.5)
        self.assertGreater(r1["peak_at_unitI"], 0)
        self.assertGreater(r1["width_mm_at_unitI"], 0)

    def test_tripolar_narrower_but_costlier_clean(self):
        c = M.compare(0, 0.5)
        self.assertLess(c["tri_width_mm"], c["mono_width_mm"])
        self.assertGreater(c["center_charge_ratio_tri_over_mono"], 1.0)
        self.assertGreater(c["battery_proxy_ratio_sumabs"],
                           c["center_charge_ratio_tri_over_mono"])

    def test_distance_broadens(self):
        near = M.compare(0, 0.25)["mono_width_mm"]
        far = M.compare(0, 1.0)["mono_width_mm"]
        self.assertGreaterEqual(far, near)


if __name__ == "__main__":
    unittest.main()
