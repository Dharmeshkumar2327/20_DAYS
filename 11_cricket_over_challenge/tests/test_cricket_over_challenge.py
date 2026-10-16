"""Unit tests for Cricket Over Challenge."""

import unittest

from cricket_over_challenge import get_ball_result


class TestGetBallResult(unittest.TestCase):
    def test_dot_ball(self):
        self.assertEqual(get_ball_result(1), ("🔴 Dot ball! No run.", 0, False))
        self.assertEqual(get_ball_result(2), ("🔴 Dot ball! No run.", 0, False))

    def test_single_and_double(self):
        self.assertEqual(get_ball_result(3)[1:], (1, False))
        self.assertEqual(get_ball_result(4)[1:], (1, False))
        self.assertEqual(get_ball_result(5)[1:], (2, False))
        self.assertEqual(get_ball_result(6)[1:], (2, False))

    def test_three_four_six(self):
        self.assertEqual(get_ball_result(7)[1:], (3, False))
        self.assertEqual(get_ball_result(8)[1:], (4, False))
        self.assertEqual(get_ball_result(9)[1:], (6, False))

    def test_out(self):
        self.assertEqual(get_ball_result(10)[1:], (0, True))

    def test_invalid_roll_raises_value_error(self):
        for invalid_roll in (0, 11, -1, 1.5):
            with self.subTest(roll=invalid_roll):
                with self.assertRaises(ValueError):
                    get_ball_result(invalid_roll)


if __name__ == "__main__":
    unittest.main()
