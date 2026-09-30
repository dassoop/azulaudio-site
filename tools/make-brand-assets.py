#!/usr/bin/env python3
"""Build Moonbase store branding + product icons into brand/moonbase/.

Wordmark source: the Azul Audio SVG in the Transpose repo (assets/AzulAudio.svg), rendered to an ink
mask first (see brand/moonbase/README.md). Icons are crops of each product's cover.

    python3 tools/make-brand-assets.py <ink-mask.png>
"""
import pathlib, sys
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "moonbase"
OUT.mkdir(parents=True, exist_ok=True)
DARK, WHITE = (16, 16, 16), (255, 255, 255)


def tinted(mask, rgb):
    im = Image.new("RGBA", mask.size, rgb + (0,))
    im.putalpha(mask)
    return im


def fit(im, w=None, h=None):
    if w: return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)


def pad_square(im, size, margin):
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    inner = size - 2 * margin
    im = fit(im, w=inner) if im.width >= im.height else fit(im, h=inner)
    canvas.paste(im, ((size - im.width) // 2, (size - im.height) // 2), im)
    return canvas


# --- Wordmark + logo from the ink mask --------------------------------------------------------
ink = Image.open(sys.argv[1]).convert("L")
# split the wave mark from the letters at the first fully empty column gap
cols = [ink.crop((x, 0, x + 1, ink.height)).getextrema()[1] for x in range(ink.width)]
gap = next(x for x in range(ink.width // 8, ink.width) if all(c < 20 for c in cols[x:x + 12]))
wave = ink.crop((0, 0, gap, ink.height)); wave = wave.crop(wave.point(lambda v: 255 if v > 20 else 0).getbbox())

for name, rgb in (("dark", DARK), ("white", WHITE)):
    fit(tinted(ink, rgb), w=2000).save(OUT / f"azul-wordmark-{name}.png", optimize=True)
    pad_square(tinted(wave, rgb), 1024, 120).save(OUT / f"azul-logo-{name}.png", optimize=True)


# --- Product icons: top-left crop of each product's square cover (title + UI corner), rounded tile ---
S, R = 1024, 200
# crop = share of the cover kept from the top-left; Transpose needs more to fit its longer title

def cover_icon(cover_path, out_name, crop):
    cover = Image.open(ROOT / cover_path).convert("RGB")
    side = round(min(cover.size) * crop)
    icon = cover.crop((0, 0, side, side)).resize((S, S), Image.LANCZOS).convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], R, fill=255)
    icon.putalpha(mask)
    icon.save(OUT / out_name, optimize=True)

cover_icon("img/scatter-cover.png", "icon-scatter.png", 0.62)
cover_icon("img/transpose-cover.png", "icon-transpose.png", 0.70)

print("wrote", sorted(p.name for p in OUT.glob("*.png")))
