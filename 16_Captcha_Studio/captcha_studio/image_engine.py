"""
Image CAPTCHA engine written from scratch with Pillow + NumPy.

Pipeline for every image:

    background gradient  ->  background noise (dots / grid)
    ->  render each character on its own layer (random font, size, rotation, colour)
    ->  paste characters with random overlap and vertical jitter
    ->  sine-wave warp (non-linear distortion that breaks simple OCR)
    ->  interference curves (Bezier lines through the text)
    ->  foreground speckle noise  ->  optional blur

Difficulty presets control how aggressive each step is.
"""

from __future__ import annotations

import io
import math
import secrets
from dataclasses import dataclass, replace
from enum import Enum
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

_rng = secrets.SystemRandom()

DEFAULT_FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass(frozen=True)
class Style:
    """All tunable parameters of the renderer."""

    width: int = 360
    height: int = 110
    font_size_range: tuple[int, int] = (48, 60)
    rotation: int = 15                 # max degrees each character is rotated
    overlap: float = 0.10              # 0 = no overlap, 0.3 = heavy overlap
    jitter_y: int = 6                  # vertical jitter of characters, px
    wave_amplitude: float = 3.0        # sine-warp amplitude, px
    wave_period: float = 120.0         # sine-warp period, px
    curves: int = 1                    # number of interference curves
    curve_width: int = 2
    dots: int = 60                     # foreground speckles
    bg_dots: int = 200                 # background noise dots
    grid: bool = False                 # faint background grid
    blur: float = 0.0                  # gaussian blur radius
    theme: str = "lavender"


PRESETS: dict[Difficulty, Style] = {
    Difficulty.EASY: Style(
        rotation=8, overlap=0.0, jitter_y=3, wave_amplitude=1.5, curves=0,
        dots=20, bg_dots=80,
    ),
    Difficulty.MEDIUM: Style(),
    Difficulty.HARD: Style(
        font_size_range=(50, 62), rotation=25, overlap=0.15, jitter_y=8,
        wave_amplitude=4.5, wave_period=100.0, curves=2, curve_width=2,
        dots=150, bg_dots=400, grid=True, blur=0.4, theme="night",
    ),
}

# (background top, background bottom, list of text colours, noise colour)
THEMES: dict[str, tuple[tuple, tuple, list[tuple], tuple]] = {
    "lavender": ((243, 240, 255), (225, 222, 250),
                 [(88, 96, 200), (120, 80, 190), (60, 110, 190)], (150, 150, 220)),
    "mint":     ((236, 252, 245), (210, 240, 228),
                 [(20, 120, 90), (30, 90, 120), (90, 110, 40)], (120, 190, 160)),
    "sunset":   ((255, 243, 230), (255, 222, 205),
                 [(190, 70, 50), (160, 60, 120), (200, 110, 20)], (230, 160, 130)),
    "night":    ((28, 32, 52), (16, 18, 30),
                 [(255, 210, 90), (120, 220, 255), (255, 130, 170)], (90, 100, 150)),
}


class ImageCaptchaGenerator:
    """Render text into a distorted CAPTCHA image.

    >>> gen = ImageCaptchaGenerator(difficulty="hard")
    >>> img = gen.generate("Py7h@n")        # PIL.Image
    >>> gen.save("Py7h@n", "captcha.png")
    """

    def __init__(
        self,
        difficulty: Difficulty | str = Difficulty.MEDIUM,
        fonts: Sequence[str | Path] | None = None,
        **overrides,
    ) -> None:
        base = PRESETS[Difficulty(difficulty)]
        self.style: Style = replace(base, **overrides) if overrides else base
        if self.style.theme not in THEMES:
            raise ValueError(f"unknown theme {self.style.theme!r}; choose from {list(THEMES)}")
        self.font_paths = [Path(f) for f in fonts] if fonts else sorted(DEFAULT_FONT_DIR.glob("*.ttf"))
        self._font_cache: dict[tuple[Path, int], ImageFont.FreeTypeFont] = {}

    # ------------------------------------------------------------------ public
    def generate(self, text: str) -> Image.Image:
        if not text:
            raise ValueError("text must not be empty")
        s = self.style
        top, bottom, palette, noise = THEMES[s.theme]

        img = self._gradient(s.width, s.height, top, bottom)
        draw = ImageDraw.Draw(img)
        if s.grid:
            self._grid(draw, noise)
        self._dots(draw, s.bg_dots, noise, radius=1)

        self._paste_text(img, text, palette)
        img = self._wave(img, s.wave_amplitude, s.wave_period)

        draw = ImageDraw.Draw(img)
        for _ in range(s.curves):
            self._curve(draw, _rng.choice(palette), s.curve_width)
        self._dots(draw, s.dots, _rng.choice(palette), radius=2)

        if s.blur:
            img = img.filter(ImageFilter.GaussianBlur(s.blur))
        return img

    def generate_bytes(self, text: str, fmt: str = "PNG") -> bytes:
        buf = io.BytesIO()
        self.generate(text).save(buf, format=fmt)
        return buf.getvalue()

    def save(self, text: str, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.generate(text).save(path)
        return path

    # ---------------------------------------------------------------- helpers
    def _font(self, size: int) -> ImageFont.ImageFont:
        if not self.font_paths:
            return ImageFont.load_default(size=size)
        path = _rng.choice(self.font_paths)
        key = (path, size)
        if key not in self._font_cache:
            self._font_cache[key] = ImageFont.truetype(str(path), size)
        return self._font_cache[key]

    @staticmethod
    def _gradient(w: int, h: int, top: tuple, bottom: tuple) -> Image.Image:
        t = np.linspace(0.0, 1.0, h)[:, None, None]
        arr = (1 - t) * np.array(top) + t * np.array(bottom)
        arr = np.broadcast_to(arr, (h, w, 3)).astype(np.uint8)
        return Image.fromarray(arr, "RGB")

    def _grid(self, draw: ImageDraw.ImageDraw, colour: tuple) -> None:
        w, h = self.style.width, self.style.height
        step = _rng.randint(14, 22)
        for x in range(0, w, step):
            draw.line([(x, 0), (x + _rng.randint(-10, 10), h)], fill=colour, width=1)
        for y in range(0, h, step):
            draw.line([(0, y), (w, y + _rng.randint(-6, 6))], fill=colour, width=1)

    def _dots(self, draw: ImageDraw.ImageDraw, n: int, colour: tuple, radius: int) -> None:
        w, h = self.style.width, self.style.height
        for _ in range(n):
            x, y = _rng.randrange(w), _rng.randrange(h)
            r = _rng.randint(0, radius)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=colour)

    def _render_char(self, ch: str, colour: tuple) -> Image.Image:
        s = self.style
        font = self._font(_rng.randint(*s.font_size_range))
        left, top, right, bottom = font.getbbox(ch)
        w, h = right - left + 8, bottom - top + 8
        layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(layer).text((4 - left, 4 - top), ch, font=font, fill=colour + (255,))
        angle = _rng.uniform(-s.rotation, s.rotation)
        return layer.rotate(angle, resample=Image.BICUBIC, expand=True)

    def _paste_text(self, img: Image.Image, text: str, palette: list[tuple]) -> None:
        s = self.style
        glyphs = [self._render_char(ch, _rng.choice(palette)) for ch in text]
        # total width after overlap, then shrink uniformly if it doesn't fit
        widths = [g.width for g in glyphs]
        total = sum(widths) - int(s.overlap * sum(widths[1:]))
        usable = s.width - 24
        if total > usable:
            scale = usable / total
            glyphs = [g.resize((max(1, int(g.width * scale)), max(1, int(g.height * scale))),
                               Image.BICUBIC) for g in glyphs]
            widths = [g.width for g in glyphs]
            total = sum(widths) - int(s.overlap * sum(widths[1:]))
        x = (s.width - total) // 2
        for i, g in enumerate(glyphs):
            y = (s.height - g.height) // 2 + _rng.randint(-s.jitter_y, s.jitter_y)
            y = max(0, min(s.height - g.height, y))
            img.paste(g, (x, y), g)
            step = g.width
            if i + 1 < len(glyphs):
                step -= int(s.overlap * glyphs[i + 1].width)
            x += step

    @staticmethod
    def _wave(img: Image.Image, amplitude: float, period: float) -> Image.Image:
        """Shift every column vertically (and every row horizontally) by a sine wave."""
        if amplitude <= 0:
            return img
        arr = np.asarray(img)
        h, w = arr.shape[:2]
        phase_x, phase_y = _rng.uniform(0, 2 * math.pi), _rng.uniform(0, 2 * math.pi)
        ys, xs = np.mgrid[0:h, 0:w]
        src_y = ys + amplitude * np.sin(2 * math.pi * xs / period + phase_x)
        src_x = xs + amplitude * 0.5 * np.sin(2 * math.pi * ys / (period / 2) + phase_y)
        src_y = np.clip(np.rint(src_y), 0, h - 1).astype(int)
        src_x = np.clip(np.rint(src_x), 0, w - 1).astype(int)
        return Image.fromarray(arr[src_y, src_x])

    def _curve(self, draw: ImageDraw.ImageDraw, colour: tuple, width: int) -> None:
        """Draw a cubic Bezier curve across the image."""
        w, h = self.style.width, self.style.height
        p0 = (_rng.randint(0, w // 6), _rng.randint(h // 4, 3 * h // 4))
        p3 = (_rng.randint(5 * w // 6, w), _rng.randint(h // 4, 3 * h // 4))
        p1 = (_rng.randint(w // 6, w // 2), _rng.randint(0, h))
        p2 = (_rng.randint(w // 2, 5 * w // 6), _rng.randint(0, h))
        pts = []
        for t in np.linspace(0, 1, 80):
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            pts.append((x, y))
        draw.line(pts, fill=colour, width=width, joint="curve")


def make_grid(images: Iterable[Image.Image], labels: Iterable[str] | None = None,
              cols: int = 2, pad: int = 16) -> Image.Image:
    """Combine several CAPTCHA images into one labelled gallery image."""
    images = list(images)
    labels = list(labels) if labels else [""] * len(images)
    w = max(i.width for i in images)
    h = max(i.height for i in images)
    label_h = 26 if any(labels) else 0
    rows = math.ceil(len(images) / cols)
    sheet = Image.new("RGB", (cols * (w + pad) + pad, rows * (h + label_h + pad) + pad), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(DEFAULT_FONT_DIR / "DejaVuSans-Bold.ttf"), 15)
    except OSError:
        font = ImageFont.load_default()
    for idx, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(idx, cols)
        x = pad + c * (w + pad)
        y = pad + r * (h + label_h + pad)
        if lab:
            draw.text((x, y), lab, fill=(40, 40, 60), font=font)
        sheet.paste(im, (x, y + label_h))
    return sheet
