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
  // null = "Coming soon" and the buy button is disabled.
  prices: {
    scatter: '$20',
    transpose: null,
  },
};
