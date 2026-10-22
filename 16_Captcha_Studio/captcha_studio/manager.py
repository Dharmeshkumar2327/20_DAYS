"""
Server-side CAPTCHA lifecycle: issue -> verify -> expire.

Security features
-----------------
* The answer is **never stored in plain text** - only an HMAC-SHA256 digest
  keyed with a server secret.
* Verification uses ``hmac.compare_digest`` (constant-time, no timing leaks).
* Every challenge is **single-use** (deleted after a correct answer).
* Challenges **expire** after ``ttl_seconds``.
* Limited **attempts** per challenge (brute-force protection).
* Optional per-client **rate limiting** for issuing new challenges.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum

from .image_engine import Difficulty, ImageCaptchaGenerator
from .text import math_challenge, random_text


class Mode(str, Enum):
    TEXT = "text"
    MATH = "math"


class VerifyResult(str, Enum):
    OK = "ok"
    WRONG = "wrong"
    EXPIRED = "expired"
    NOT_FOUND = "not_found"
    TOO_MANY_ATTEMPTS = "too_many_attempts"


class RateLimitError(RuntimeError):
    pass


@dataclass
class Challenge:
    id: str
    image_png: bytes
    mode: Mode
    difficulty: Difficulty
    expires_at: float
    audio_digits: str | None = None   # only set for numeric challenges


@dataclass
class _Record:
    digest: bytes
    expires_at: float
    attempts_left: int
    audio_digits: str | None = None
    created_at: float = field(default_factory=time.time)


class CaptchaManager:
    def __init__(
        self,
        secret_key: bytes | None = None,
        ttl_seconds: int = 120,
        max_attempts: int = 3,
        case_sensitive: bool = False,
        rate_limit: int = 20,            # max challenges per client ...
        rate_window: int = 60,           # ... per this many seconds
        clock=time.time,
    ) -> None:
        self._secret = secret_key or secrets.token_bytes(32)
        self.ttl = ttl_seconds
        self.max_attempts = max_attempts
        self.case_sensitive = case_sensitive
        self.rate_limit = rate_limit
        self.rate_window = rate_window
        self._clock = clock
        self._store: dict[str, _Record] = {}
        self._issued: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()
        self._generators: dict[Difficulty, ImageCaptchaGenerator] = {}
        self.stats = {"issued": 0, "passed": 0, "failed": 0, "expired": 0}

    # ------------------------------------------------------------- internals
    def _normalise(self, answer: str) -> str:
        answer = "".join(answer.split())          # ignore whitespace
        return answer if self.case_sensitive else answer.lower()

    def _digest(self, challenge_id: str, answer: str) -> bytes:
        msg = f"{challenge_id}:{self._normalise(answer)}".encode()
        return hmac.new(self._secret, msg, hashlib.sha256).digest()

    def _generator(self, difficulty: Difficulty) -> ImageCaptchaGenerator:
        if difficulty not in self._generators:
            self._generators[difficulty] = ImageCaptchaGenerator(difficulty)
        return self._generators[difficulty]

    def _check_rate(self, client_id: str | None) -> None:
        if client_id is None:
            return
        now = self._clock()
        q = self._issued[client_id]
        while q and now - q[0] > self.rate_window:
            q.popleft()
        if len(q) >= self.rate_limit:
            raise RateLimitError("too many CAPTCHA requests, slow down")
        q.append(now)

    def purge_expired(self) -> int:
        now = self._clock()
        with self._lock:
            dead = [k for k, r in self._store.items() if r.expires_at < now]
            for k in dead:
                del self._store[k]
            self.stats["expired"] += len(dead)
        return len(dead)

    # ---------------------------------------------------------------- public
    def issue(
        self,
        difficulty: Difficulty | str = Difficulty.MEDIUM,
        mode: Mode | str = Mode.TEXT,
        length: int = 6,
        client_id: str | None = None,
    ) -> Challenge:
        difficulty, mode = Difficulty(difficulty), Mode(mode)
        self._check_rate(client_id)
        self.purge_expired()

        if mode is Mode.MATH:
            mc = math_challenge()
            shown, answer = mc.question, mc.answer
        else:
            charset = {Difficulty.EASY: "upper_alnum",
                       Difficulty.MEDIUM: "alnum",
                       Difficulty.HARD: "complex"}[difficulty]
            shown = answer = random_text(length, charset)

        cid = secrets.token_urlsafe(16)
        png = self._generator(difficulty).generate_bytes(shown)
        expires = self._clock() + self.ttl
        audio = answer if answer.isdigit() else None
        with self._lock:
            self._store[cid] = _Record(self._digest(cid, answer), expires,
                                       self.max_attempts, audio)
            self.stats["issued"] += 1
        return Challenge(cid, png, mode, difficulty, expires, audio)

    def verify(self, challenge_id: str, answer: str) -> VerifyResult:
        with self._lock:
            rec = self._store.get(challenge_id)
            if rec is None:
                return VerifyResult.NOT_FOUND
            if rec.expires_at < self._clock():
                del self._store[challenge_id]
                self.stats["expired"] += 1
                return VerifyResult.EXPIRED
            if hmac.compare_digest(rec.digest, self._digest(challenge_id, answer)):
                del self._store[challenge_id]          # single use
                self.stats["passed"] += 1
                return VerifyResult.OK
            rec.attempts_left -= 1
            self.stats["failed"] += 1
            if rec.attempts_left <= 0:
                del self._store[challenge_id]
                return VerifyResult.TOO_MANY_ATTEMPTS
            return VerifyResult.WRONG

    def attempts_left(self, challenge_id: str) -> int:
        rec = self._store.get(challenge_id)
        return rec.attempts_left if rec else 0

    def audio_digits(self, challenge_id: str) -> str | None:
        rec = self._store.get(challenge_id)
        return rec.audio_digits if rec else None

    def __len__(self) -> int:
        return len(self._store)
