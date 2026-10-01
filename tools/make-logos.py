#!/usr/bin/env python3
"""Build the site's logo files from the master SVGs (see tools/logo_masks.py).

    python3 tools/make-logos.py

Writes img/logo-white.png (top bar), img/favicon-32.png, img/apple-touch-icon.png and
img/wordmark-white.png (used by tools/make-transpose-cover.py).
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from logo_masks import mark, word, tinted, on_square, fit_in

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "img"
WHITE, TILE = (255, 255, 255), (21, 21, 21, 255)

m, w = mark(), word()
on_square(tinted(m, WHITE), 512, 8).save(IMG / "logo-white.png", optimize=True)
# Tab + home-screen icons: white squid on the site's dark grey, so they show on light and dark UIs
on_square(tinted(m, WHITE), 32, 3, TILE).save(IMG / "favicon-32.png", optimize=True)
on_square(tinted(m, WHITE), 180, 22, TILE).convert("RGB").save(IMG / "apple-touch-icon.png", optimize=True)
fit_in(tinted(w, WHITE), 2000, 2000).save(IMG / "wordmark-white.png", optimize=True)
print("wrote img/logo-white.png, favicon-32.png, apple-touch-icon.png, wordmark-white.png")
