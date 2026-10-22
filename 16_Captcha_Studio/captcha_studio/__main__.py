"""
Command-line interface.

Examples
--------
python -m captcha_studio generate --text 9Pyth0n4d@tA6 --difficulty hard
python -m captcha_studio generate --count 4 --difficulty medium --theme mint --out output/
python -m captcha_studio audio --text 978 --out output/audio.wav
python -m captcha_studio demo            # interactive "type what you see" test
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import (THEMES, AudioCaptchaGenerator, AudioUnavailableError, CaptchaManager,
               Difficulty, ImageCaptchaGenerator, VerifyResult, random_text)


def cmd_generate(a: argparse.Namespace) -> None:
    overrides = {"theme": a.theme} if a.theme else {}
    gen = ImageCaptchaGenerator(a.difficulty, width=a.width, height=a.height, **overrides)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(a.count):
        text = a.text or random_text(a.length, a.charset)
        safe = "".join(c if c.isalnum() else "_" for c in text)
        path = gen.save(text, out / f"captcha_{a.difficulty}_{i + 1}_{safe}.png")
        print(f"[saved] {path}   answer = {text}")


def cmd_audio(a: argparse.Namespace) -> None:
    try:
        path = AudioCaptchaGenerator().save(a.text, a.out)
    except AudioUnavailableError as e:
        sys.exit(str(e))
    print(f"[saved] {path}")


def cmd_demo(a: argparse.Namespace) -> None:
    mgr = CaptchaManager(max_attempts=3)
    ch = mgr.issue(a.difficulty, mode=a.mode)
    path = Path("demo_captcha.png")
    path.write_bytes(ch.image_png)
    print(f"Open {path.resolve()} and type what you see (3 attempts).")
    while True:
        res = mgr.verify(ch.id, input("> "))
        if res is VerifyResult.OK:
            print("Correct - you are human!")
            return
        if res is VerifyResult.WRONG:
            print(f"Wrong, {mgr.attempts_left(ch.id)} attempt(s) left.")
            continue
        print(f"Failed: {res.value}")
        return


def main(argv=None) -> None:
    p = argparse.ArgumentParser(prog="captcha_studio", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="create image CAPTCHA files")
    g.add_argument("--text", help="fixed text (default: random)")
    g.add_argument("--count", type=int, default=1)
    g.add_argument("--length", type=int, default=6)
    g.add_argument("--charset", default="alnum", help="digits|alpha|alnum|upper_alnum|complex")
    g.add_argument("--difficulty", default="medium", choices=[d.value for d in Difficulty])
    g.add_argument("--theme", choices=list(THEMES))
    g.add_argument("--width", type=int, default=360)
    g.add_argument("--height", type=int, default=110)
    g.add_argument("--out", default="output")
    g.set_defaults(func=cmd_generate)

    au = sub.add_parser("audio", help="create an audio CAPTCHA (digits only)")
    au.add_argument("--text", required=True)
    au.add_argument("--out", default="output/captcha.wav")
    au.set_defaults(func=cmd_audio)

    d = sub.add_parser("demo", help="interactive verification demo in the terminal")
    d.add_argument("--difficulty", default="medium", choices=[x.value for x in Difficulty])
    d.add_argument("--mode", default="text", choices=["text", "math"])
    d.set_defaults(func=cmd_demo)

    args = p.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
