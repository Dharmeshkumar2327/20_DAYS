import unittest
from utils import build_payload

class PayloadTests(unittest.TestCase):
    def test_url_requires_scheme(self):
        with self.assertRaises(ValueError):
            build_payload("Website URL", "github.com")

    def test_url_valid(self):
        self.assertEqual(
            build_payload("Website URL", "https://github.com/Dharmeshkumar2327"),
            "https://github.com/Dharmeshkumar2327"
        )

    def test_email(self):
        self.assertEqual(build_payload("Email", "user@example.com"), "mailto:user@example.com")

    def test_phone(self):
        self.assertEqual(build_payload("Phone", "+91 9876543210"), "tel:+919876543210")

    def test_wifi(self):
        self.assertEqual(build_payload("Wi-Fi", "CampusNet;pass123;WPA"),
                         "WIFI:T:WPA;S:CampusNet;P:pass123;;")

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            build_payload("Text", "  ")

if __name__ == "__main__":
    unittest.main()
