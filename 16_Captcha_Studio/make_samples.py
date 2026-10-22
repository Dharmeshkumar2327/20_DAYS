"""Regenerate the sample images shown in the README:  python make_samples.py"""

from pathlib import Path

from captcha_studio import ImageCaptchaGenerator, make_grid, math_challenge

OUT = Path(__file__).parent / "samples"
OUT.mkdir(exist_ok=True)

samples = [
    # (file name, label, generator, text)
    ("1_easy.png", "EASY  -  answer: K7MP4X",
     ImageCaptchaGenerator("easy", theme="mint"), "K7MP4X"),
    ("2_medium.png", "MEDIUM  -  answer: 9Pyth0n4d@tA6",
     ImageCaptchaGenerator("medium", width=500, height=110), "9Pyth0n4d@tA6"),
    ("3_hard.png", "HARD  -  answer: Qx#4mT",
     ImageCaptchaGenerator("hard"), "Qx#4mT"),
]
mc = math_challenge()
samples.append(("4_math.png", f"MATH  -  answer: {mc.answer}",
                ImageCaptchaGenerator("medium", theme="sunset", rotation=10), mc.question))

images, labels = [], []
for name, label, gen, text in samples:
    img = gen.generate(text)
    img.save(OUT / name)
    images.append(img.resize((360, int(360 * img.height / img.width))) if img.width != 360 else img)
    labels.append(label)
    print("saved", OUT / name, "->", label)

make_grid(images, labels, cols=2).save(OUT / "gallery.png")
print("saved", OUT / "gallery.png")
