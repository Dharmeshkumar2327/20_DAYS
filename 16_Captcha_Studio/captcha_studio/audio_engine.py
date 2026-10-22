"""
Audio CAPTCHA (accessibility for visually-impaired users).

Wraps ``captcha.audio.AudioCaptcha`` from the `captcha` package
(https://pypi.org/project/captcha/). The built-in voice files only contain
digits, so audio challenges are numeric.
"""

from __future__ import annotations

from pathlib import Path

try:
    from captcha.audio import AudioCaptcha as _AudioCaptcha
except ImportError:  # optional dependency
    _AudioCaptcha = None


class AudioUnavailableError(RuntimeError):
    pass


class AudioCaptchaGenerator:
    def __init__(self, voicedir: str | None = None) -> None:
        if _AudioCaptcha is None:
            raise AudioUnavailableError(
                "Audio CAPTCHA needs the 'captcha' package:  pip install captcha"
            )
        self._engine = _AudioCaptcha(voicedir=voicedir) if voicedir else _AudioCaptcha()

    @staticmethod
    def _check(digits: str) -> None:
        if not digits.isdigit():
            raise ValueError("audio CAPTCHA text must contain digits only")

    def generate_bytes(self, digits: str) -> bytes:
        self._check(digits)
        return bytes(self._engine.generate(digits))

    def save(self, digits: str, path: str | Path) -> Path:
        self._check(digits)
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._engine.write(digits, str(path))
        return path


def audio_available() -> bool:
    return _AudioCaptcha is not None
