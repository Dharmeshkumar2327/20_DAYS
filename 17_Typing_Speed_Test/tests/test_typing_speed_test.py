"""Unit tests for the Typing Speed Test core logic.

Run from the project root:
    python -m unittest discover tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing_speed_test import calculate_results, get_rating  # noqa: E402
from sentences import SENTENCES  # noqa: E402


class TestCalculateResults(unittest.TestCase):
    def test_perfect_typing(self):
        text = "Hello world"
        result = calculate_results(text, text, 60)
        self.assertEqual(result["accuracy"], 100.0)
        self.assertEqual(result["correct_words"], 2)
        # 11 characters / 5 = 2.2 words in 1 minute
        self.assertEqual(result["gross_wpm"], 2.2)
        self.assertEqual(result["net_wpm"], result["gross_wpm"])

    def test_typo_reduces_accuracy(self):
        result = calculate_results("Hello world", "Hellp world", 10)
        self.assertLess(result["accuracy"], 100)
        self.assertEqual(result["correct_words"], 1)
        self.assertLess(result["net_wpm"], result["gross_wpm"])

    def test_empty_input(self):
        result = calculate_results("Hello world", "", 5)
        self.assertEqual(result["gross_wpm"], 0)
        self.assertEqual(result["accuracy"], 0)
        self.assertEqual(result["correct_words"], 0)

    def test_zero_time_does_not_crash(self):
        result = calculate_results("abc", "abc", 0)
        self.assertGreater(result["gross_wpm"], 0)


class TestRating(unittest.TestCase):
    def test_ratings(self):
        self.assertIn("Lightning", get_rating(80))
        self.assertIn("Excellent", get_rating(55))
        self.assertIn("Good", get_rating(40))
        self.assertIn("practising", get_rating(25))
        self.assertIn("steady", get_rating(10))


class TestSentences(unittest.TestCase):
    def test_all_levels_have_sentences(self):
        for level in ("easy", "medium", "hard"):
            self.assertTrue(len(SENTENCES[level]) > 0)


if __name__ == "__main__":
    unittest.main()
