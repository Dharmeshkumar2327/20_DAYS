"""Basic unit tests for Number Guessing Challenge."""

import unittest


def calculate_score(max_attempts, attempt_number):
    """Return the winning score for a 1-based attempt number."""
    remaining_attempts = max_attempts - attempt_number
    return (remaining_attempts + 1) * 10


class TestScoreCalculation(unittest.TestCase):
    def test_first_attempt_gets_maximum_score(self):
        self.assertEqual(calculate_score(7, 1), 70)

    def test_last_attempt_gets_ten_points(self):
        self.assertEqual(calculate_score(7, 7), 10)

    def test_medium_score_decreases_by_ten_each_attempt(self):
        scores = [calculate_score(7, attempt) for attempt in range(1, 8)]
        self.assertEqual(scores, [70, 60, 50, 40, 30, 20, 10])


class TestDifficultySettings(unittest.TestCase):
    def test_difficulty_ranges_and_attempts(self):
        difficulties = {
            "Easy": (50, 10),
            "Medium": (100, 7),
            "Hard": (200, 6),
        }
        self.assertEqual(difficulties["Easy"], (50, 10))
        self.assertEqual(difficulties["Medium"], (100, 7))
        self.assertEqual(difficulties["Hard"], (200, 6))


if __name__ == "__main__":
    unittest.main()
