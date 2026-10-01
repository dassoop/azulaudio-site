#!/usr/bin/env python3
"""Build img/share-home.png, the 1200x630 link-preview image (iMessage, Slack, Discord, Facebook):
the hero ocean photo, darkened, with the white Azul Audio wordmark centred.

    python3 tools/make-share-image.py      # needs img/wordmark-white.png from tools/make-logos.py
"""
import pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
W, H = 1200, 630

bg = ImageOps.fit(Image.open(ROOT / "img/hero.jpg").convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.45))
shade = Image.new("RGB", (W, H), (0, 0, 0))
bg = Image.blend(bg, shade, 0.35).convert("RGBA")

word = Image.open(ROOT / "img/wordmark-white.png").convert("RGBA")
ww = 860
word = word.resize((ww, round(word.height * ww / word.width)), Image.LANCZOS)
bg.alpha_composite(word, ((W - word.width) // 2, (H - word.height) // 2))
bg.convert("RGB").save(ROOT / "img/share-home.png", optimize=True)
print("wrote img/share-home.png", bg.size)
