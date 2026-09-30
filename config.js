// The only file to edit when Moonbase details change.
window.AZUL = {
  // Moonbase account URL (Account settings -> whitelist this site's domain there too).
  moonbase: 'https://azul-audio.moonbase.sh',

  // Moonbase product IDs, from each product's page in the Moonbase dashboard.
  // TODO: replace with the real IDs once the products are created.
  products: {
    scatter: 'scatter',
    transpose: 'transpose',
  },

  // Display prices (Moonbase checkout shows the real price, tax and currency).
  // null = shows "Coming soon" instead of a price.
  prices: {
    scatter: '$20',
    transpose: '$29',
  },

  // false = buy buttons read "Coming soon" and are disabled.
  // Turn on only once the product is purchasable in Moonbase.
  onSale: {
    scatter: false,
    transpose: false,
  },
};
