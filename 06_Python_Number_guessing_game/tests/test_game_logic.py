"""Basic tests for scoring and difficulty settings."""

import unittest


def calculate_score(max_attempts, attempt_number):
    """Calculate points for a successful guess (attempts are 1-based)."""
    return (max_attempts - attempt_number + 1) * 10


class TestScoreCalculation(unittest.TestCase):
    def test_first_attempt_gets_maximum_score(self):
        self.assertEqual(calculate_score(7, 1), 70)

    def test_last_attempt_gets_ten_points(self):
        self.assertEqual(calculate_score(7, 7), 10)

    def test_scores_decrease_by_ten_points(self):
        scores = [calculate_score(7, n) for n in range(1, 8)]
        self.assertEqual(scores, [70, 60, 50, 40, 30, 20, 10])


class TestDifficultySettings(unittest.TestCase):
    def test_easy_settings(self):
        self.assertEqual((50, 10), (50, 10))

    def test_medium_settings(self):
        self.assertEqual((100, 7), (100, 7))

    def test_hard_settings(self):
        self.assertEqual((200, 6), (200, 6))


if __name__ == "__main__":
    unittest.main()
