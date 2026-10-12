"""Unit tests for the Advanced Google Search Tool by Dharmesh Kumar."""
import unittest
from unittest.mock import patch

from advanced_google_search import build_google_url, search_many, search_google


class GoogleSearchTests(unittest.TestCase):
    def test_encodes_spaces_and_symbols(self):
        self.assertEqual(
            build_google_url('Python & "AI"'),
            'https://www.google.com/search?q=Python+%26+%22AI%22',
        )

    def test_strips_query(self):
        self.assertEqual(build_google_url("  github  "), "https://www.google.com/search?q=github")

    def test_rejects_empty_query(self):
        with self.assertRaises(ValueError):
            build_google_url("   ")

    def test_rejects_non_string(self):
        with self.assertRaises(TypeError):
            build_google_url(42)  # type: ignore[arg-type]

    def test_rejects_very_long_query(self):
        with self.assertRaises(ValueError):
            build_google_url("x" * 301)

    @patch("advanced_google_search.webbrowser.open", return_value=True)
    def test_search_google_returns_url_and_opens_browser(self, browser_open):
        url = search_google("python", open_tab=True)
        self.assertEqual(url, "https://www.google.com/search?q=python")
        browser_open.assert_called_once_with(url, new=2)

    @patch("advanced_google_search.search_google")
    def test_search_many_calls_each_query(self, mocked_search):
        mocked_search.side_effect = ["url1", "url2"]
        self.assertEqual(search_many(["python", "SQL"], open_tabs=False), ["url1", "url2"])
        self.assertEqual(mocked_search.call_count, 2)

    def test_rejects_more_than_ten_queries(self):
        with self.assertRaises(ValueError):
            search_many([f"query {i}" for i in range(11)], open_tabs=False)

    def test_rejects_invalid_delay(self):
        with self.assertRaises(ValueError):
            search_many(["python"], open_tabs=False, delay_seconds=11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
