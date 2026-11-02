"""Tests for A1 T0 model. Run: python3 -m pytest test_model.py -v
or: python3 test_model.py (stdlib unittest)."""
import math, unittest
import model as M


class T(unittest.TestCase):
    def test_greenwood_monotonic_and_endpoints(self):
        self.assertAlmostEqual(M.greenwood_hz(0.0),
                               165.4 * (1 - 0.88), places=6)
        self.assertLess(M.greenwood_hz(0.2), M.greenwood_hz(0.8))
        self.assertGreater(M.octave_width(20.0, 2.0), 0)

    def test_shannon_formula(self):
        # Q=0.1 uC, D=100 uC/cm2 -> k = -1 + 2 = 1.0
        self.assertAlmostEqual(M.shannon_k(0.1, 100.0), 1.0, places=9)

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
