"""Run with:  python -m pytest -q     (or)     python -m unittest discover tests"""

import io
import sys
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from captcha_studio import (CHARSETS, CaptchaManager, Difficulty, ImageCaptchaGenerator,  # noqa: E402
                            RateLimitError, VerifyResult, math_challenge, random_text)


class FakeClock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


class TestText(unittest.TestCase):
    def test_length_and_charset(self):
        for name, alphabet in CHARSETS.items():
            s = random_text(8, name)
            self.assertEqual(len(s), 8)
            self.assertTrue(set(s) <= set(alphabet), name)

    def test_no_ambiguous_chars(self):
        s = "".join(random_text(50, "alnum") for _ in range(20))
        self.assertFalse(set(s) & set("0O1lI"))

    def test_math_answer_is_correct(self):
        for _ in range(200):
            m = math_challenge()
            a, op, b = m.question.split()[:3]
            expected = {"+": int(a) + int(b), "-": int(a) - int(b), "x": int(a) * int(b)}[op]
            self.assertEqual(int(m.answer), expected)
            self.assertGreaterEqual(int(m.answer), 0)

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            random_text(0)


class TestImage(unittest.TestCase):
    def test_every_difficulty_renders(self):
        for d in Difficulty:
            img = ImageCaptchaGenerator(d).generate("Ab3#xY")
            self.assertEqual(img.size, (360, 110))

    def test_custom_size_and_png_bytes(self):
        png = ImageCaptchaGenerator("easy", width=500, height=100).generate_bytes("9Pyth0n4d@tA6")
        self.assertEqual(Image.open(io.BytesIO(png)).size, (500, 100))

    def test_images_are_randomised(self):
        gen = ImageCaptchaGenerator("medium")
        self.assertNotEqual(gen.generate_bytes("SAME"), gen.generate_bytes("SAME"))

    def test_bad_theme(self):
        with self.assertRaises(ValueError):
            ImageCaptchaGenerator(theme="rainbow")


class TestManager(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        self.mgr = CaptchaManager(secret_key=b"k" * 32, ttl_seconds=60, max_attempts=3,
                                  rate_limit=5, rate_window=60, clock=self.clock)

    def _issue_known(self, answer="Hello7"):
        """Issue a challenge and overwrite its answer so tests know it."""
        ch = self.mgr.issue("easy")
        self.mgr._store[ch.id].digest = self.mgr._digest(ch.id, answer)
        return ch

    def test_correct_answer_case_insensitive_and_single_use(self):
        ch = self._issue_known("Hello7")
        self.assertEqual(self.mgr.verify(ch.id, " hel lo7 "), VerifyResult.OK)
        self.assertEqual(self.mgr.verify(ch.id, "Hello7"), VerifyResult.NOT_FOUND)

    def test_attempt_limit(self):
        ch = self._issue_known()
        self.assertEqual(self.mgr.verify(ch.id, "x"), VerifyResult.WRONG)
        self.assertEqual(self.mgr.verify(ch.id, "y"), VerifyResult.WRONG)
        self.assertEqual(self.mgr.verify(ch.id, "z"), VerifyResult.TOO_MANY_ATTEMPTS)
        self.assertEqual(self.mgr.verify(ch.id, "Hello7"), VerifyResult.NOT_FOUND)

    def test_expiry(self):
        ch = self._issue_known()
        self.clock.t += 61
        self.assertEqual(self.mgr.verify(ch.id, "Hello7"), VerifyResult.EXPIRED)

    def test_answer_not_stored_in_plain_text(self):
        ch = self._issue_known("Secret9")
        self.assertNotIn(b"secret9", self.mgr._store[ch.id].digest)
        self.assertEqual(len(self.mgr._store[ch.id].digest), 32)   # SHA-256

    def test_math_mode_has_audio_digits(self):
        ch = self.mgr.issue("medium", mode="math")
        self.assertTrue(ch.audio_digits.isdigit())

    def test_rate_limit(self):
        for _ in range(5):
            self.mgr.issue("easy", client_id="1.2.3.4")
        with self.assertRaises(RateLimitError):
            self.mgr.issue("easy", client_id="1.2.3.4")
        self.clock.t += 61
        self.mgr.issue("easy", client_id="1.2.3.4")    # window has passed

    def test_purge_expired(self):
        for _ in range(3):
            self.mgr.issue("easy")
        self.clock.t += 120
        self.assertEqual(self.mgr.purge_expired(), 3)
        self.assertEqual(len(self.mgr), 0)


class TestWebApp(unittest.TestCase):
    def setUp(self):
        import app as webapp
        self.webapp = webapp
        self.client = webapp.app.test_client()

    def test_full_flow(self):
        r = self.client.post("/api/captcha", json={"difficulty": "hard"})
        self.assertEqual(r.status_code, 200)
        cid = r.get_json()["id"]
        img = self.client.get(f"/api/captcha/{cid}.png")
        self.assertEqual(img.mimetype, "image/png")

        wrong = self.client.post("/api/verify", json={"id": cid, "answer": "nope"}).get_json()
        self.assertEqual(wrong["result"], "wrong")

        mgr = self.webapp.manager
        mgr._store[cid].digest = mgr._digest(cid, "known1")
        ok = self.client.post("/api/verify", json={"id": cid, "answer": "KNOWN1"}).get_json()
        self.assertTrue(ok["success"])

    def test_page_loads(self):
        self.assertIn(b"CAPTCHA Studio", self.client.get("/").data)


if __name__ == "__main__":
    unittest.main()
