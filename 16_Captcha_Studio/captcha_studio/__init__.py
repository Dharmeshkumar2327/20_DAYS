"""CAPTCHA Studio - generate, serve and verify image & audio CAPTCHAs."""

from .audio_engine import AudioCaptchaGenerator, AudioUnavailableError, audio_available
from .image_engine import THEMES, Difficulty, ImageCaptchaGenerator, Style, make_grid
from .manager import CaptchaManager, Challenge, Mode, RateLimitError, VerifyResult
from .text import CHARSETS, math_challenge, random_text

__version__ = "2.0.0"

__all__ = [
    "AudioCaptchaGenerator", "AudioUnavailableError", "audio_available",
    "ImageCaptchaGenerator", "Difficulty", "Style", "THEMES", "make_grid",
    "CaptchaManager", "Challenge", "Mode", "RateLimitError", "VerifyResult",
    "random_text", "math_challenge", "CHARSETS",
]
