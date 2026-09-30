# azulaudio.com

Static site for Azul Audio. No build step: plain HTML/CSS/JS. Checkout, customer accounts, serials,
licenses and downloads are handled by Moonbase's embedded storefront (`moonbase.js`).

## Edit

- `config.js`: Moonbase account URL, product IDs, display prices. The only file to touch for store changes.
- `index.html`, `scatter/`, `transpose/`: pages. Header/footer are repeated in each page.
- `site.js`: wires `data-buy="<key>"`, `data-cart`, `data-account` to Moonbase.
- `product/scatter-kontakt-8/`, `shop/`, `cart/`, `checkout/`, `my-account/`: redirect stubs for old WooCommerce URLs.

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

1. Push to GitHub; Settings → Pages → deploy from `main` / root. `CNAME` already holds `azulaudio.com`.
2. Linode DNS for azulaudio.com: apex A records → 185.199.108.153, .109.153, .110.153, .111.153;
   `www` CNAME → `<github-user>.github.io`.
3. Pages → Enforce HTTPS once the certificate is issued.
