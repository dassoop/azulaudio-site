# Moonbase branding (azul-audio.moonbase.sh)

Upload in the Moonbase dashboard. Moonbase's docs give no size or format rules for logos or icons,
so these are large PNGs with transparent backgrounds. Moonbase draws the **logo on the brand colour**
(black since 2026-10-06), so upload the **white** logo. It shows the wordmark on both light and dark
headers, so no single-colour wordmark works; it's left empty and headers show logo + "Azul Audio" text.

| File | Use |
|---|---|
| `azul-logo-white.png` (1024 sq) | Account settings → Branding → Logo (**in use**) |
| `azul-wordmark-dark.png`, `azul-wordmark-white.png` (2000x309) | Not uploaded (see above) |
| `azul-logo-dark.png` | Light backgrounds elsewhere |
| `icon-scatter.png` (1024 sq) | Scatter product → icon (top-left crop of `img/scatter-cover.png`) |
| `icon-transpose.png` (1024 sq) | Transpose product → icon (top-left crop of `img/transpose-cover.png`) |

## Theme settings (to match azulaudio.com)

- Brand colour: `#101010` (mono palette, 2026-10-06; was teal `#078A82`)
- Contrast colour: `#FFFFFF`
- Heading font: Inter · Body font: Inter (Moonbase has no Onest; the site uses Onest headings)
- Corners: Sharp · Buttons: Outlined · Cards: Outlined

## Rebuild

`python3 tools/make-brand-assets.py`. The logo and wordmark come straight from the master SVGs in
`Workspace_PitchShifter/assets/` (`AzulMark.svg`, `AzulAudio.svg`) via `tools/logo_masks.py` (Quick Look
render, macOS). Icons are crops of `img/scatter-cover.png` and `img/transpose-cover.png`, so rebuild the
covers first.
