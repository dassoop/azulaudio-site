"""Render the Azul Audio logo SVGs (master copies in the Transpose repo) to greyscale ink masks.

mark()  -> the squid alone (assets/AzulMark.svg)
word()  -> squid + "Azul Audio" (assets/AzulAudio.svg)

Ink is white (255) on black (0), cropped to the artwork, so callers can tint it any colour.
macOS only: uses Quick Look (qlmanage) to rasterise, after padding the SVG into a square viewBox
because Quick Look always renders square.
"""
import pathlib, re, subprocess, tempfile
from PIL import Image, ImageOps

SRC = pathlib.Path.home() / "_Files/02_Development/01_Projects/02_In Progress/Workspace_PitchShifter/assets"
PX = 4000


def _render(svg_path):
    text = svg_path.read_text()
    m = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([-\d.]+) ([-\d.]+)"', text)
    x, y, w, h = map(float, m.groups())
    side = max(w, h) * 1.04
    vb = f'{x - (side - w) / 2:.2f} {y - (side - h) / 2:.2f} {side:.2f} {side:.2f}'
    text = re.sub(r'<svg([^>]*?) width="[^"]*" height="[^"]*" viewBox="[^"]*"',
                  rf'<svg\1 width="{PX}" height="{PX}" viewBox="{vb}"', text, count=1)
    with tempfile.TemporaryDirectory() as tmp:
        sq = pathlib.Path(tmp) / "sq.svg"
        sq.write_text(text)
        subprocess.run(["qlmanage", "-t", "-s", str(PX), "-o", tmp, str(sq)], check=True, capture_output=True)
        ink = ImageOps.invert(Image.open(pathlib.Path(tmp) / "sq.svg.png").convert("L"))
    return ink.crop(ink.point(lambda v: 255 if v > 20 else 0).getbbox())


def mark():
    return _render(SRC / "AzulMark.svg")


def word():
    return _render(SRC / "AzulAudio.svg")


def tinted(mask, rgb):
    im = Image.new("RGBA", mask.size, tuple(rgb) + (0,))
    im.putalpha(mask)
    return im


def fit_in(im, box_w, box_h):
    k = min(box_w / im.width, box_h / im.height)
    return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)


def on_square(im, size, margin, bg=(0, 0, 0, 0)):
    canvas = Image.new("RGBA", (size, size), bg)
    im = fit_in(im, size - 2 * margin, size - 2 * margin)
    canvas.alpha_composite(im, ((size - im.width) // 2, (size - im.height) // 2))
    return canvas
