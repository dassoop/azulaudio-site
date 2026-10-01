# Moonbase branding (azul-audio.moonbase.sh)

Upload in the Moonbase dashboard. Moonbase's docs give no size or format rules for logos or icons,
so these are large PNGs with transparent backgrounds. The customer portal and checkout are light,
so use the **dark** logo/wordmark there; the white ones are for dark backgrounds.

| File | Use |
|---|---|
| `azul-wordmark-dark.png` (2000x290) | Account settings → Theme → wordmark |
| `azul-logo-dark.png` (1024 sq) | Account settings → Theme → logo (square mark) |
| `azul-wordmark-white.png`, `azul-logo-white.png` | Dark backgrounds |
| `icon-scatter.png` (1024 sq) | Scatter product → icon (top-left crop of `img/scatter-cover.png`) |
| `icon-transpose.png` (1024 sq) | Transpose product → icon (top-left crop of `img/transpose-cover.png`) |

## Theme settings (to match azulaudio.com)

- Brand colour: `#078A82` (the site's teal; the lighter `#0BB4AA` is too low-contrast behind white text)
- Contrast colour: `#FFFFFF`
- Heading font: Onest · Body font: Inter (both Google Fonts)
- Corners: Soft · Buttons: Light

## Rebuild

`python3 tools/make-brand-assets.py`. The logo and wordmark come straight from the master SVGs in
`Workspace_PitchShifter/assets/` (`AzulMark.svg`, `AzulAudio.svg`) via `tools/logo_masks.py` (Quick Look
render, macOS). Icons are crops of `img/scatter-cover.png` and `img/transpose-cover.png`, so rebuild the
covers first.
