# Replace the Azul Audio logo before launch

**Done 2026-09-30 for the site (#1–7) and the Moonbase files (#8–12): the squid logo.** The plugin side (#13–15)
was done in the Transpose repo (`0ec6103`). Still to do: upload #8, #9 in the Moonbase dashboard; #16 (NI artwork).

Rebuild everything after a future logo change:
```bash
python3 tools/make-logos.py && python3 tools/make-scatter-cover.py && python3 tools/make-transpose-cover.py \
  && python3 tools/make-brand-assets.py && python3 tools/bust-cache.py
```
(re-render `img/transpose-*.png` from the plugin first; see README "Images").

_Inventory taken 2026-09-30. Two versions of the logo are in use:_
- **Mark**: the wave symbol alone.
- **Wordmark**: wave + "Azul Audio" text.

_Today both come from one master file: `Workspace_PitchShifter/assets/AzulAudio.svg` (the wordmark;
the mark is its left part). Replace that file first, then work down this list._

## Site (this repo, https://azulaudio.com)

| # | File | Logo | Used by | How to update |
|---|---|---|---|---|
| 1 | `img/logo-white.png` (512 sq, white on transparent) | Mark | Top-bar logo on `index.html`, `scatter/`, `transpose/`, `404.html`; also the mark on the Transpose cover | Replace the file (white, transparent, square) |
| 2 | `img/favicon-32.png` | Mark | Browser tab icon, every page + `404.html` | Replace (32x32) |
| 3 | `img/apple-touch-icon.png` | Mark | iPhone/iPad home-screen icon, every page | Replace (180x180, no transparency) |
| 4 | `img/scatter-cover.png` | Wordmark, baked in bottom-left | Scatter card (home), Scatter page gallery | Needs a new Scatter cover. No source file here, only this 484 px render |
| 5 | `img/transpose-cover.png` | Wordmark, drawn bottom-left (#1 + "Azul Audio" typed in Helvetica Neue Light) | Transpose card (home), Transpose page gallery | `python3 tools/make-transpose-cover.py` after #1 and #6. If the new wordmark shouldn't be mark + typed text, change the script to paste the wordmark image |
| 6 | `img/transpose-ui.png` | Wordmark in the plugin's footer (the plugin draws it) | Transpose page gallery, input to #5 | Re-render from the updated plugin: `./build/UiSnapshot <dir> --on` → `all-notuner.png` (see README "Images") |
| 7 | `img/transpose-{transpose,harmony,detune,chaos}.png` | None (crops stop above the footer) | Transpose effects section | Re-crop only if the plugin UI changes elsewhere |

Text, not images (change only if the name changes): `<title>`s, the home hero `<h1>Azul Audio</h1>`,
`alt="Azul Audio"` on the top-bar logo, and the footer "Copyright © 2026 Azul Audio".

After changing files: `python3 tools/bust-cache.py`, commit, push. The hash stamps make browsers fetch the
new images straight away.

## Moonbase (dashboard at app.moonbase.sh, no API for these)

| # | Where | Logo | Our file | How to update |
|---|---|---|---|---|
| 8 | Account settings → Theme → **Wordmark** | Wordmark, dark | `brand/moonbase/azul-wordmark-dark.png` | Upload new |
| 9 | Account settings → Theme → **Logo** | Mark, dark | `brand/moonbase/azul-logo-dark.png` | Upload new |
| 10 | (spares) | White versions | `brand/moonbase/azul-{wordmark,logo}-white.png` | Regenerate for completeness |
| 11 | Scatter product → icon | None: top-left crop of #4 (title + UI), stops above the logo | `brand/moonbase/icon-scatter.png` | Rebuild only if #4 changes (`tools/make-brand-assets.py`) |
| 12 | Transpose product → icon | None: top-left crop of #5 | `brand/moonbase/icon-transpose.png` | Rebuild only if #5 changes |

#8 and #9 are what the customer portal, the checkout overlay and Moonbase's emails show (receipts,
password reset). `tools/make-brand-assets.py` rebuilds 8–12 from an ink mask of the new wordmark.
Steps are in `brand/moonbase/README.md`. It assumes the mark is the left part of the wordmark with a
gap before the text; revisit if the new logo is laid out differently.

## Outside this repo (the logo appears there too, and the site screenshots come from it)

| # | Where | Logo | Notes |
|---|---|---|---|
| 13 | Transpose plugin UI footer: `Source/PluginEditor.cpp` draws `assets/AzulAudio.svg` (BinaryData) | Wordmark | Replacing the SVG updates it; black is recoloured at runtime (`replaceColour`), so keep the new SVG single-colour black |
| 14 | Transpose activation window: `Source/Licensing.cpp` (licensing session, in progress) draws the same SVG | Wordmark | Same file, same recolour note |
| 15 | Windows installer icon `installer/assets/Transpose.ico` and Mac installer backgrounds `installer/assets/mac-background{,-dark}.png` | Mark | `installer/assets/make-assets.py` regenerates them from `assets/AzulAudio.svg` (pulls out the wave `<g clip-path>` group, so the new SVG needs a similar structure or the script needs updating) |
| 16 | Scatter itself: Native Access tile/artwork (hosted by NI) and the Kontakt instrument's UI | Check | Not in any repo. NI's product artwork only changes if you send them new art. The screenshot of Scatter's UI here (`img/scatter-ui.png`) shows no Azul logo |

Old WordPress site (dingleberry): being retired ~2026-10-30, no change needed.

## Order

1. New master SVG → `Workspace_PitchShifter/assets/AzulAudio.svg`.
2. Plugin (#13–15): rebuild, `make-assets.py`, re-render UiSnapshot `--on`.
3. Site (#1–6): replace files, rebuild the Transpose cover, new Scatter cover, bust cache, push.
4. Moonbase (#8–12): regenerate `brand/moonbase/`, upload.
