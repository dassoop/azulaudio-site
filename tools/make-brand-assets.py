#!/usr/bin/env python3
"""Build Moonbase store branding + product icons into brand/moonbase/.

Wordmark source: the Azul Audio SVG in the Transpose repo (assets/AzulAudio.svg), rendered to an ink
mask first (see brand/moonbase/README.md). Icons are drawn here.

    python3 tools/make-brand-assets.py <ink-mask.png>
"""
import math, pathlib, sys
from PIL import Image, ImageDraw, ImageFilter

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


# --- Product icons (1024 square, rounded tile) ------------------------------------------------
S, R = 1024, 200

def tile(fill):
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, S - 1, S - 1], R, fill=fill)
    return im


def clip_to_tile(layer, base):
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, S - 1, S - 1], R, fill=255)
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", (S, S), 0), mask))
    base.alpha_composite(layer)
    return base


# Transpose: the plugin's four effect glyphs, 2x2, in their accent colours on the plugin's panel grey
def sine(d, box, cycles, amp_frac, col, width, phase=0.0, alpha=255, x_shift=0.0):
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; cy = (y0 + y1) / 2
    pts = [(x0 + x_shift * w + t / 60 * (w * (1 - x_shift)), cy - h * amp_frac * math.sin(2 * math.pi * (t / 60 * cycles + phase))) for t in range(61)]
    d.line(pts, fill=col + (alpha,), width=width, joint="curve")

t = tile((30, 31, 35, 255))
layer = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
BLUE, PURPLE, YELLOW, RED = (61, 120, 196), (126, 91, 181), (183, 150, 47), (185, 74, 79)
m, g = 150, 70; cell = (S - 2 * m - g) / 2
boxes = [(m + c * (cell + g), m + r * (cell + g), m + c * (cell + g) + cell, m + r * (cell + g) + cell) for r in range(2) for c in range(2)]
lw = 26
sine(d, boxes[0], 1.5, 0.30, BLUE, lw)                                   # Transpose: sine
x0, y0, x1, y1 = boxes[1]; hh = y1 - y0
for i in range(3):                                                       # Harmony: stacked sines
    sine(d, (x0, y0 + hh * (0.05 + 0.3 * i), x1, y0 + hh * (0.35 + 0.3 * i)), 1.5, 0.28, PURPLE, lw - 6)
sine(d, boxes[2], 1.25, 0.26, YELLOW, lw, alpha=140, x_shift=0.22)       # Detune: staggered pair
x0, y0, x1, y1 = boxes[2]; sine(d, (x0, y0, x1 - (x1 - x0) * 0.22, y1), 1.25, 0.26, YELLOW, lw)
x0, y0, x1, y1 = boxes[3]; w, h = x1 - x0, y1 - y0                        # Chaos: jagged line
P = [(0, .55), (.12, .10), (.22, .80), (.31, .35), (.42, .95), (.52, .20), (.60, .65), (.71, .05), (.82, .85), (.91, .40), (1, .60)]
d.line([(x0 + px * w, y0 + (0.15 + 0.7 * py) * h) for px, py in P], fill=RED + (255,), width=lw - 4, joint="curve")
clip_to_tile(layer, t).save(OUT / "icon-transpose.png", optimize=True)

# Scatter: its cover's cube field + blue bar-and-dashes motif on the cover grey
t = tile((82, 82, 83, 255))
layer = Image.new("RGBA", (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
import random; rnd = random.Random(7)
for _ in range(34):                                                      # scattered cubes, like the cover
    s = rnd.randint(50, 170); x = rnd.randint(-40, S - 40); y = rnd.randint(-40, S - 40)
    shade = rnd.randint(105, 175); a = rnd.randint(70, 170)
    d.rectangle([x, y, x + s, y + s], fill=(shade, shade, shade + 2, a))
    d.polygon([(x, y), (x + s * .3, y - s * .3), (x + s * 1.3, y - s * .3), (x + s, y)], fill=(shade + 30, shade + 30, shade + 32, a))
layer = layer.filter(ImageFilter.GaussianBlur(2))
t = clip_to_tile(layer, t)
d = ImageDraw.Draw(t); SB = (46, 174, 255, 255)
bar_y, bh = 600, 54
d.rectangle([150, bar_y, 520, bar_y + bh], fill=SB)                       # long bar + three dashes
for i in range(3):
    x = 585 + i * 105; d.rectangle([x, bar_y, x + 64, bar_y + bh], fill=SB)
# white "S" block glyph above the bar would need a font; the motif alone reads as Scatter at icon size
t.save(OUT / "icon-scatter.png", optimize=True)

print("wrote", sorted(p.name for p in OUT.glob("*.png")))
