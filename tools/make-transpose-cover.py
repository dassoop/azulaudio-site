#!/usr/bin/env python3
"""Build img/transpose-cover.png, the square promo image, in the style of Scatter's cover:
product name in thin type, the plugin UI in the middle, Azul Audio mark
bottom left. Uses img/transpose-ui.png (UiSnapshot --on, all-notuner) and img/logo-white.png.

    python3 tools/make-transpose-cover.py
"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
S = 1200                                   # output size (square)
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"
LIGHT, THIN = 7, 12                        # face indexes in HelveticaNeue.ttc
BLUE, PURPLE, YELLOW, RED = (61, 120, 196), (126, 91, 181), (183, 150, 47), (185, 74, 79)   # plugin accents


def background():
    img = Image.new("RGB", (S, S))
    top, bottom = (24, 25, 30), (40, 42, 50)
    d = ImageDraw.Draw(img)
    for y in range(S):
        t = y / (S - 1)
        d.line([(0, y), (S, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    # faint sine waves in the four effect colours, like Scatter's cube texture
    waves = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    w = ImageDraw.Draw(waves)
    for i, (col, amp, cyc, phase, yc) in enumerate([
        (BLUE, 90, 1.6, 0.0, 330), (PURPLE, 70, 2.1, 0.8, 420), (YELLOW, 110, 1.3, 1.9, 900), (RED, 80, 2.4, 2.7, 990),
    ]):
        for k in range(3):
            pts = [(x, yc + 18 * k + amp * math.sin(2 * math.pi * (x / S * cyc) + phase)) for x in range(0, S + 1, 6)]
            w.line(pts, fill=col + (78 - 20 * k,), width=3)
    waves = waves.filter(ImageFilter.GaussianBlur(1.2))
    img.paste(waves, (0, 0), waves)
    return img


def rounded(im, r):
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = im.convert("RGBA"); out.putalpha(mask)
    return out


img = background()
d = ImageDraw.Draw(img)

# Title
title_font = ImageFont.truetype(FONT, 150, index=THIN)
x0, ty, tracking = 52, 44, 10          # letter-spaced like Scatter's title
x = x0
for ch in "Transpose":
    d.text((x, ty), ch, font=title_font, fill=(255, 255, 255))
    x += title_font.getlength(ch) + tracking

# Plugin UI, centred, rounded, with a soft shadow
ui = Image.open(ROOT / "img/transpose-ui.png").convert("RGBA")
uw = S - 2 * 40
uh = round(ui.height * uw / ui.width)
ui = rounded(ui.resize((uw, uh), Image.LANCZOS), 18)
uy = 420
shadow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle([40, uy + 18, 40 + uw, uy + 18 + uh], 22, fill=(0, 0, 0, 170))
shadow = shadow.filter(ImageFilter.GaussianBlur(24))
img.paste(shadow, (0, 0), shadow)
img.paste(ui, (40, uy), ui)

# Azul Audio mark, bottom left
logo = Image.open(ROOT / "img/logo-white.png").convert("RGBA")
bbox = logo.getbbox(); logo = logo.crop(bbox)
lh = 62
logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
ly = S - 56 - lh
img.paste(logo, (x0, ly), logo)
word_font = ImageFont.truetype(FONT, 62, index=LIGHT)
d.text((x0 + logo.width + 14, ly + lh / 2), "Azul Audio", font=word_font, fill=(255, 255, 255), anchor="lm")

out = ROOT / "img/transpose-cover.png"
img.save(out, optimize=True)
print("wrote", out.relative_to(ROOT), img.size)
