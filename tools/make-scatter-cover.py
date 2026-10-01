#!/usr/bin/env python3
"""Rebuild img/scatter-cover.png with the current Azul Audio wordmark.

Scatter's cover only exists as a 484 px render with the old logo baked in
(brand/source/scatter-cover-original.png). This paints out the old wordmark in the bottom-left
corner (OpenCV inpaint over its dark pixels) and pastes the new wordmark at the same size/colour.

    python3 tools/make-scatter-cover.py      # needs img/wordmark-white.png from tools/make-logos.py
"""
import pathlib
import cv2
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "brand/source/scatter-cover-original.png"
OUT = ROOT / "img/scatter-cover.png"

im = cv2.imread(str(SRC))
H, W = im.shape[:2]
x0, y0, x1, y1 = 8, 438, 200, 476                      # old wordmark area
roi = cv2.cvtColor(im[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY)
mask = np.zeros((H, W), np.uint8)
mask[y0:y1, x0:x1] = cv2.dilate(((roi < int(np.median(roi)) - 18) * 255).astype(np.uint8),
                                np.ones((3, 3), np.uint8), iterations=2)
clean = Image.fromarray(cv2.cvtColor(cv2.inpaint(im, mask, 5, cv2.INPAINT_TELEA), cv2.COLOR_BGR2RGB)).convert("RGBA")

word = Image.open(ROOT / "img/wordmark-white.png").convert("RGBA")
mh = 28                                                 # old wordmark was ~22 px tall + squid head room
word = word.resize((round(word.width * mh / word.height), mh), Image.LANCZOS)
dark = Image.new("RGBA", word.size, (17, 17, 17, 0)); dark.putalpha(word.getchannel("A"))
clean.alpha_composite(dark, (12, 470 - mh))
clean.convert("RGB").save(OUT, optimize=True)
print("wrote", OUT.relative_to(ROOT), clean.size)
