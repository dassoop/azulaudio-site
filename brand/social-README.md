# Azul Audio social kit

Built by `python3 tools/make-social-kit.py` from the site's brand sources. Don't edit the images by hand; rebuild them.

## Upload map

| Platform | Slot | File | Notes |
|---|---|---|---|
| Instagram | Profile picture | `instagram/ig-profile-1080.png` | Shown as a circle (110 px). |
| | Post | `instagram/ig-post-square-1080x1080.jpg`, `ig-post-portrait-1080x1350.jpg` | Brand/intro posts. |
| | Story / Reel background | `instagram/ig-story-1080x1920.jpg` | The wordmark stays clear of the story UI at the top and bottom. |
| | Highlight covers | `instagram/highlights/ig-highlight-*.png` | Azul, Transpose, Scatter. Post each as a story, then set it as the cover. |
| TikTok | Profile picture | `tiktok/tiktok-profile-1080.png` | Shown as a circle. |
| | Video cover / background | `tiktok/tiktok-cover-1080x1920.jpg` | Kept clear of the caption and side buttons. |
| YouTube | Profile picture | `youtube/yt-profile-800.png` | 800x800, shown as a circle. |
| | Banner | `youtube/yt-banner-2560x1440.jpg` | The wordmark sits inside the 1546x423 area that every device shows. `_guide-yt-banner-safe-areas.jpg` marks that area and is not for upload. |
| | Video watermark | `youtube/yt-watermark-150.png` | Studio → Customisation → Branding. |
| | Thumbnail background | `youtube/yt-thumbnail-bg-1280x720.jpg` | Put the video title on top. |
| Facebook | Profile picture | `facebook/fb-profile-720.png` | Shown as a circle. |
| | Cover photo | `facebook/fb-cover-1640x924.jpg` | Desktop crops it to the middle band, phones trim the sides. The wordmark fits both. |
| | Link post image | `facebook/fb-link-post-1200x630.jpg` | Same as the site's link preview. |

Other profile-picture backgrounds: `profile/azul-avatar-{teal,dark,ocean,white}-1080.png`. Teal is the default everywhere, so use the same one on every account.

Logos (transparent PNG): `logos/azul-wordmark-{white,dark,teal}.png`, `logos/azul-squid-{white,dark,teal}.png`.
Use white on photos and dark backgrounds, and dark or teal on light ones.

## Brand

| | Value |
|---|---|
| Teal (brand, buttons, avatar background) | `#078A82` |
| Teal light (accents on dark only) | `#0BB4AA` |
| Ink / dark background | `#101010` / `#151515` |
| White | `#FFFFFF` |
| Heading font | Onest (500–700), Google Fonts |
| Body font | Inter (400, 600), Google Fonts |
| Photo | Ocean hero (`img/hero.jpg`), darkened about 30–35% behind white logos |
| Site | https://azulaudio.com · support@azulaudio.com |

## Sources

- Squid and wordmark: master SVGs in `Workspace_PitchShifter/assets/` (`AzulMark.svg`, `AzulAudio.svg`), rendered by `tools/logo_masks.py` (macOS).
- Product highlight icons: `brand/moonbase/icon-*.png` (run `tools/make-brand-assets.py` first if the covers change).
