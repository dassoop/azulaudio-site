#!/usr/bin/env python3
"""Build the social media branding kit into brand/social/ (and brand/azul-social-kit.zip).

Profile pictures, banners/covers and post/story backgrounds for Instagram, TikTok, YouTube and Facebook,
all made from the same sources as the site: the squid + wordmark master SVGs (tools/logo_masks.py),
the ocean hero photo (img/hero.jpg), the product covers, and the site palette.

    python3 tools/make-social-kit.py
"""
import pathlib, shutil, sys
from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "brand" / "social"
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from logo_masks import mark, word, tinted, fit_in

# Mono palette (2026-10-06): black + white; the ocean photo is the only colour.
INK, WHITE = (16, 16, 16), (255, 255, 255)

MARK, WORD = mark(), word()
HERO = Image.open(ROOT / "img/hero.jpg").convert("RGB")


def ocean(w, h, shade=0.35, centering=(0.5, 0.45)):
    """The hero photo cropped to w x h and darkened, like the site's share image."""
    bg = ImageOps.fit(HERO, (w, h), Image.LANCZOS, centering=centering)
    return Image.blend(bg, Image.new("RGB", (w, h), (0, 0, 0)), shade).convert("RGBA")


def flat(w, h, rgb):
    return Image.new("RGBA", (w, h), rgb + (255,))


def put(canvas, mask, rgb, box_w, box_h, cx=None, cy=None):
    """Tint an ink mask and centre it (on cx, cy) inside a box_w x box_h area."""
    im = fit_in(tinted(mask, rgb), box_w, box_h)
    cx = canvas.width // 2 if cx is None else cx
    cy = canvas.height // 2 if cy is None else cy
    canvas.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
    return canvas


def save(im, rel):
    path = OUT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jpg":
        im.convert("RGB").save(path, quality=92, optimize=True)
    else:
        im.save(path, optimize=True)
    print(f"  {rel}  {im.width}x{im.height}")


if OUT.exists():
    shutil.rmtree(OUT)

# --- Profile pictures: squid centred, sized for a circle crop (mark inside the middle ~58%) --------
# One master per background; every platform shows avatars as circles, so the same file works everywhere.
AV = 1080
avatars = {
    "black": put(flat(AV, AV, INK), MARK, WHITE, 620, 620),
    "ocean": put(ocean(AV, AV, 0.30, (0.5, 0.5)), MARK, WHITE, 620, 620),
    "white": put(flat(AV, AV, WHITE), MARK, INK, 620, 620),
}
for name, im in avatars.items():
    save(im, f"profile/azul-avatar-{name}-1080.png")

# --- Logos (transparent) ---------------------------------------------------------------------------
for name, rgb in (("white", WHITE), ("black", INK)):
    save(fit_in(tinted(WORD, rgb), 3000, 3000), f"logos/azul-wordmark-{name}.png")
    canvas = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))
    save(put(canvas, MARK, rgb, 1840, 1840), f"logos/azul-squid-{name}.png")

# --- Instagram -------------------------------------------------------------------------------------
save(avatars["black"], "instagram/ig-profile-1080.png")
save(put(ocean(1080, 1080), WORD, WHITE, 800, 800), "instagram/ig-post-square-1080x1080.jpg")
save(put(ocean(1080, 1350), WORD, WHITE, 800, 800), "instagram/ig-post-portrait-1080x1350.jpg")
# Stories/Reels: keep the wordmark clear of the top 250 px and bottom 340 px UI
save(put(ocean(1080, 1920, 0.35, (0.5, 0.5)), WORD, WHITE, 820, 820, cy=880), "instagram/ig-story-1080x1920.jpg")

# Highlight covers: Instagram shows the middle as a circle; the art sits in the centre square
def highlight(art, name, bg=INK, size=560):
    c = flat(1080, 1920, bg)
    art = fit_in(art, size, size)
    c.alpha_composite(art, ((1080 - art.width) // 2, (1920 - art.height) // 2))
    save(c, f"instagram/highlights/ig-highlight-{name}.png")

highlight(tinted(MARK, WHITE), "azul")
for prod in ("transpose", "scatter"):
    icon = Image.open(ROOT / f"brand/moonbase/icon-{prod}.png").convert("RGBA")
    highlight(icon, prod, size=760)   # product tile fills most of the circle

# --- TikTok ----------------------------------------------------------------------------------------
save(avatars["black"], "tiktok/tiktok-profile-1080.png")
# Video cover/background: TikTok's caption and buttons cover the bottom ~420 px and the right ~140 px
save(put(ocean(1080, 1920, 0.35, (0.5, 0.5)), WORD, WHITE, 760, 760, cx=500, cy=860), "tiktok/tiktok-cover-1080x1920.jpg")

# --- YouTube ---------------------------------------------------------------------------------------
save(avatars["black"].resize((800, 800), Image.LANCZOS), "youtube/yt-profile-800.png")
# Banner 2560x1440; only the centre 1546x423 shows on every device, so the wordmark stays inside it
banner = ocean(2560, 1440, 0.30, (0.5, 0.5))
put(banner, WORD, WHITE, 1150, 300)
save(banner, "youtube/yt-banner-2560x1440.jpg")
# Safe-area guide (not for upload): shows what phones (1546x423) and desktops (2560x423) see
guide = banner.copy()
d = ImageDraw.Draw(guide)
for (w, h), col in (((1546, 423), (255, 80, 80)), ((2560, 423), (255, 210, 60))):
    d.rectangle([(2560 - w) // 2, (1440 - h) // 2, (2560 + w) // 2 - 1, (1440 + h) // 2 - 1], outline=col, width=6)
save(guide, "youtube/_guide-yt-banner-safe-areas.jpg")
# Video watermark (bottom-right of videos): 150x150, one colour on transparent
wm = Image.new("RGBA", (150, 150), (0, 0, 0, 0))
save(put(wm, MARK, WHITE, 130, 130), "youtube/yt-watermark-150.png")
# Thumbnail background 1280x720 (add the video title on top in your editor)
save(put(ocean(1280, 720), WORD, WHITE, 560, 160, cy=600), "youtube/yt-thumbnail-bg-1280x720.jpg")

# --- Facebook --------------------------------------------------------------------------------------
save(avatars["black"].resize((720, 720), Image.LANCZOS), "facebook/fb-profile-720.png")
# Cover 1640x924: desktop shows the middle 1640x624 band, phones the full height with sides trimmed
cover = ocean(1640, 924, 0.30, (0.5, 0.5))
put(cover, WORD, WHITE, 900, 260)
save(cover, "facebook/fb-cover-1640x924.jpg")
save(put(ocean(1200, 630), WORD, WHITE, 860, 860), "facebook/fb-link-post-1200x630.jpg")

# --- Zip -------------------------------------------------------------------------------------------
shutil.copy(ROOT / "brand/social-README.md", OUT / "README.md")
zip_path = shutil.make_archive(str(ROOT / "brand" / "azul-social-kit"), "zip", OUT.parent, OUT.name)
print("wrote", zip_path)
