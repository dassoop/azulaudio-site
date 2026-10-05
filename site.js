// Wires the page to Moonbase: buy buttons, cart, account. No build step, no dependencies.
(function () {
  var cfg = window.AZUL;

  // Prices and buy-button state from config.js
  document.querySelectorAll('[data-price]').forEach(function (el) {
    var p = cfg.prices[el.dataset.price];
    el.textContent = p || 'Coming soon';
  });
  document.querySelectorAll('[data-buy]').forEach(function (btn) {
    if (!cfg.prices[btn.dataset.buy] || !cfg.onSale[btn.dataset.buy]) {
      btn.disabled = true;
      btn.textContent = 'Coming soon';
    }
  });
  document.querySelectorAll('[data-add]').forEach(function (btn) {   // Add to cart: only when on sale
    if (!cfg.prices[btn.dataset.add] || !cfg.onSale[btn.dataset.add]) btn.remove();
  });

  // Hero video: desktop only, and only shown once it's really playing. Phones, reduced motion, data saver,
  // or a blocked autoplay (e.g. iOS Low Power Mode) keep the still image that sits behind it.
  var hv = document.querySelector('.hero video');
  if (hv) {
    var wantVideo = window.matchMedia('(min-width: 761px)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches &&
      !(navigator.connection && navigator.connection.saveData);
    if (!wantVideo) {
      hv.remove();
    } else {
      hv.addEventListener('playing', function () { hv.classList.add('playing'); });
      hv.src = hv.dataset.src;
      var p = hv.play();
      if (p && p.catch) p.catch(function (e) {
        // NotAllowedError = autoplay refused (keep the still). Anything else, e.g. a background tab
        // pausing media to save power, retries once the tab is visible; the still shows meanwhile.
        if (e && e.name === 'NotAllowedError') { hv.remove(); return; }
        document.addEventListener('visibilitychange', function retry() {
          if (document.hidden) return;
          document.removeEventListener('visibilitychange', retry);
          hv.play().catch(function () { hv.remove(); });
        });
      });
    }
  }

  // Home: transparent bar over the hero, dark once scrolled
  if (document.body.classList.contains('home')) {
    var onScroll = function () { document.body.classList.toggle('scrolled', window.scrollY > 40); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Mobile menu
  var toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      document.body.classList.toggle('nav-open');
    });
  }

  // Products dropdown: click/tap toggles (hover also opens it on desktop via CSS)
  document.querySelectorAll('.dropdown-toggle').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var dd = btn.parentElement;
      var open = dd.classList.toggle('open');
      btn.setAttribute('aria-expanded', open);
    });
  });
  function closeDropdowns() {
    document.querySelectorAll('.dropdown.open').forEach(function (dd) {
      dd.classList.remove('open');
      dd.querySelector('.dropdown-toggle').setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('click', function (e) { if (!e.target.closest('.dropdown')) closeDropdowns(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDropdowns(); });
  // Following a nav link (e.g. Products -> /#products on the home page) closes the mobile menu
  document.querySelectorAll('.nav a').forEach(function (l) {
    l.addEventListener('click', function () { document.body.classList.remove('nav-open'); closeDropdowns(); });
  });

  function notice(msg) {
    var el = document.querySelector('.store-notice');
    if (!el) {
      el = document.createElement('div');
      el.className = 'store-notice';
      document.body.appendChild(el);
    }
    el.textContent = msg;
    el.classList.add('show');
    setTimeout(function () { el.classList.remove('show'); }, 5000);
  }

  function run(fn) {
    if (!window.Moonbase) {
      notice('The store is still loading. Try again in a moment.');
      return;
    }
    try {
      var r = fn(window.Moonbase);
      if (r && r.catch) r.catch(function (e) { console.error(e); notice('Store error: ' + e.message); });
    } catch (e) {
      console.error(e);
      notice('Store error: ' + e.message);
    }
  }

  document.addEventListener('click', function (e) {
    var buy = e.target.closest('[data-buy]');
    var add = e.target.closest('[data-add]');
    var cart = e.target.closest('[data-cart]');
    var account = e.target.closest('[data-account]');
    var trial = e.target.closest('[data-trial]');
    if (buy) {
      e.preventDefault();
      run(function (M) { return M.purchase({ product_id: cfg.products[buy.dataset.buy] }); });
    } else if (add) {
      e.preventDefault();
      run(function (M) { return M.add_to_cart({ product_id: cfg.products[add.dataset.add] }); });
    } else if (cart) {
      e.preventDefault();
      run(function (M) { return M.view_cart(); });
    } else if (trial) {   // trial download: Moonbase asks the visitor to sign in or sign up first
      e.preventDefault();
      run(function (M) { return M.download_product({ product_id: cfg.products[trial.dataset.trial] }); });
    } else if (account) {
      e.preventDefault();
      run(function (M) { return M.view_account(); });
    }
  });

  // Load Moonbase's embedded storefront; our own nav replaces its floating toolbar.
  var s = document.createElement('script');
  s.src = 'https://assets.moonbase.sh/storefront/moonbase.js';
  s.onload = function () {
    window.Moonbase.setup(cfg.moonbase, { toolbar: { enabled: false } });
    // Old WooCommerce links redirect here with ?account or ?cart
    var q = new URLSearchParams(location.search);
    if (q.has('account')) run(function (M) { return M.view_account(); });
    if (q.has('cart')) run(function (M) { return M.view_cart(); });
  };
  document.head.appendChild(s);
})();
