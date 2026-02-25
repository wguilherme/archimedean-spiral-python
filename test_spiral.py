import math
import unittest

from spiral import SpiralParams, generate_spiral


class TestGenerateSpiral(unittest.TestCase):

    def setUp(self):
        self.params = SpiralParams(r_start=50, r_end=146, turns=25)
        self.points = generate_spiral(self.params)

    # --- structural ---

    def test_point_count(self):
        expected = self.params.turns * self.params.points_per_turn + 1
        self.assertEqual(len(self.points), expected)

    # --- boundary conditions ---

    def test_first_point_at_r_start(self):
        x, y = self.points[0]
        self.assertAlmostEqual(math.hypot(x, y), self.params.r_start, places=10)

    def test_last_point_at_r_end(self):
        x, y = self.points[-1]
        self.assertAlmostEqual(math.hypot(x, y), self.params.r_end, places=10)

    def test_first_point_on_positive_x_axis(self):
        x, y = self.points[0]
        self.assertAlmostEqual(y, 0.0, places=10)
        self.assertGreater(x, 0)

    # --- Archimedean law: r = r_start + (r_end - r_start) * t ---

    def test_spiral_law_holds_for_every_point(self):
        total = len(self.points) - 1
        for i, (x, y) in enumerate(self.points):
            t = i / total
            expected_r = self.params.r_start + (self.params.r_end - self.params.r_start) * t
            self.assertAlmostEqual(math.hypot(x, y), expected_r, places=10,
                                   msg=f"Law violated at index {i}")

    def test_radius_increases_monotonically(self):
        radii = [math.hypot(x, y) for x, y in self.points]
        for i in range(1, len(radii)):
            self.assertGreaterEqual(radii[i], radii[i - 1],
                                    msg=f"Radius decreased at index {i}")

    # --- angle / geometry ---

    def test_full_turns_end_on_positive_x_axis(self):
        """After N full turns the endpoint should lie on the positive x-axis."""
        params = SpiralParams(r_start=10, r_end=20, turns=3, points_per_turn=360)
        pts = generate_spiral(params)
        x_last, y_last = pts[-1]
        self.assertAlmostEqual(y_last, 0.0, places=8)
        self.assertGreater(x_last, 0)

    def test_quarter_turn_lands_on_positive_y_axis(self):
        """At 1/4 of a single turn the point should be on the positive y-axis."""
        params = SpiralParams(r_start=10, r_end=20, turns=1, points_per_turn=4)
        pts = generate_spiral(params)
        # index 1 → t = 0.25, angle = π/2
        x, y = pts[1]
        self.assertAlmostEqual(x, 0.0, places=10)
        self.assertGreater(y, 0)

    # --- edge cases ---

    def test_single_turn_minimal_resolution(self):
        params = SpiralParams(r_start=1, r_end=2, turns=1, points_per_turn=4)
        pts = generate_spiral(params)
        self.assertEqual(len(pts), 5)

    def test_constant_radius_when_r_start_equals_r_end(self):
        """When r_start == r_end the result is a circle, not a spiral."""
        params = SpiralParams(r_start=50, r_end=50, turns=3, points_per_turn=360)
        pts = generate_spiral(params)
        for x, y in pts:
            self.assertAlmostEqual(math.hypot(x, y), 50.0, places=10)


if __name__ == "__main__":
    unittest.main()
