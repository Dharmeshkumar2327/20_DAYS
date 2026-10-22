"""
Challenge text generation.

Uses the ``secrets`` module (cryptographically secure randomness) instead of
``random`` so that challenges cannot be predicted by an attacker.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass

# Characters that humans often confuse (0/O, 1/l/I, 5/S, 2/Z, 8/B) are removed.
SAFE_UPPER = "ACDEFGHJKLMNPQRTUVWXY"
SAFE_LOWER = "abcdefghjkmnpqrstuvwxyz"
SAFE_DIGITS = "34679"
SAFE_SYMBOLS = "@#$%&"

CHARSETS = {
    "digits": "0123456789",
    "alpha": SAFE_UPPER + SAFE_LOWER,
    "alnum": SAFE_UPPER + SAFE_LOWER + SAFE_DIGITS,
    "upper_alnum": SAFE_UPPER + SAFE_DIGITS,
    "complex": SAFE_UPPER + SAFE_LOWER + SAFE_DIGITS + SAFE_SYMBOLS,
}


def random_text(length: int = 6, charset: str = "alnum") -> str:
    """Return a random challenge string built from a named charset (or a raw string)."""
    if length < 1:
        raise ValueError("length must be >= 1")
    alphabet = CHARSETS.get(charset, charset)
    if not alphabet:
        raise ValueError("charset must not be empty")
    return "".join(secrets.choice(alphabet) for _ in range(length))


@dataclass(frozen=True)
class MathChallenge:
    """A simple arithmetic challenge, e.g. question='7 + 5 = ?' and answer='12'."""

    question: str
    answer: str


def math_challenge(max_operand: int = 12) -> MathChallenge:
    """Generate a small arithmetic problem whose answer is never negative."""
    a = secrets.randbelow(max_operand) + 1
    b = secrets.randbelow(max_operand) + 1
    op = secrets.choice(["+", "-", "x"])
    if op == "-" and b > a:
        a, b = b, a
    result = {"+": a + b, "-": a - b, "x": a * b}[op]
    return MathChallenge(question=f"{a} {op} {b} = ?", answer=str(result))
