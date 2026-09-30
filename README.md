# azulaudio.com

Static site for Azul Audio. No build step: plain HTML/CSS/JS. Checkout, customer accounts, serials,
licenses and downloads are handled by Moonbase's embedded storefront (`moonbase.js`).

## Edit

- `config.js`: Moonbase account URL, product IDs, display prices, and `onSale` (enables each Buy button). The only file to touch for store changes.
- `index.html`, `scatter/`, `transpose/`: pages (use relative paths, e.g. `../img/...`). Header/footer are repeated in each page.
- `site.js`: wires `data-buy="<key>"`, `data-cart`, `data-account` to Moonbase.
- `product/scatter-kontakt-8/`, `shop/`, `cart/`, `checkout/`, `my-account/`: redirect stubs for old WooCommerce URLs.

## Before pushing

```bash
python3 tools/bust-cache.py
```

Stamps every local CSS/JS/image link with `?v=<content hash>` so visitors never get a stale mix of
old and new files (GitHub Pages lets browsers cache for 10 minutes). Safe to re-run.

## Run locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080 (paths are root-relative, so serve from this folder).

## Moonbase setup

1. Create products; copy each product ID into `config.js`.
2. Account settings → whitelist `azulaudio.com` and `www.azulaudio.com`.
3. Scatter: Key Codes generator + NI serial list; Native Access steps in the fulfillment message.
4. Transpose: Releases with Mac/Windows installers.

## Deploy (GitHub Pages, DNS stays on Linode)

Live preview: https://dassoop.github.io/azulaudio-site/ (Pages builds from `main`, repo root).
Paths are relative so the site works both there and on the custom domain (`404.html` uses root paths and
only styles correctly on the custom domain).

Cutover to azulaudio.com:
1. `git mv CNAME.cutover CNAME`, commit, push (Pages then serves azulaudio.com; the github.io URL redirects there).
2. Linode DNS for azulaudio.com: apex A records -> 185.199.108.153, 185.199.109.153, 185.199.110.153,
   185.199.111.153; `www` CNAME -> `dassoop.github.io`.
3. Repo Settings -> Pages -> Enforce HTTPS once the certificate is issued.
4. Moonbase account settings: whitelist `azulaudio.com` and `www.azulaudio.com` if checkout is blocked.
