/* LUCKY GOLF · FREE HAT, FREE POLO · the gift guard (promo ends Fri Sept 25, 2026)
   Loaded on every page from layout/theme.liquid. The promo page runs the full
   version in gwp-promo.js; this is the small one for everywhere else.

   Why it exists: the gifts are priced ($29 / $67) and made free by automatic
   discounts. If the bag drops under $90 / $140 somewhere other than the promo
   page (the UpCart drawer on a product page, the /cart page), the discount stops
   applying and the gift would be charged. This takes the gift back out instead.

   It only ever REMOVES a gift line (marked with the _gwp_gift property), and
   only when the bag no longer qualifies, or when there is more than one.
   Remove this script tag from theme.liquid after the promo ends. */
(function () {
  if (window.__gwpGuard || document.getElementById('gwp')) return;
  window.__gwpGuard = true;

  /* $90 / $140 in the store's currency, converted for shoppers browsing in
     another one (Shopify Markets), the same way Shopify converts the cart. */
  var RATE = parseFloat(window.Shopify && Shopify.currency && Shopify.currency.rate) || 1;
  var T1 = Math.round(9000 * RATE), T2 = Math.round(14000 * RATE), PROP = '_gwp_gift';
  var root = (window.Shopify && Shopify.routes && Shopify.routes.root) || '/';
  var ownFetch = window.fetch.bind(window);
  var CART_WRITE = /\/cart\/(add|change|update|clear)(\.js)?(\?|$)/;
  var busy = false, again = false, timer = null;

  function json(path, body) {
    var o = { credentials: 'same-origin', headers: { 'Accept': 'application/json' } };
    if (body) { o.method = 'POST'; o.headers['Content-Type'] = 'application/json'; o.body = JSON.stringify(body); }
    return ownFetch(root + path, o).then(function (r) { return r.json(); });
  }

  function check() {
    if (busy) { again = true; return; }
    busy = true;
    json('cart.js').then(function (cart) {
      var paid = 0, gifts = [];
      (cart.items || []).forEach(function (l) {
        var g = l.properties && l.properties[PROP];
        if (g) gifts.push({ key: l.key, qty: l.quantity, need: g === 'polo' ? T2 : T1, slot: g === 'polo' ? 'polo' : 'hat' });
        else paid += (l.final_line_price != null ? l.final_line_price : l.line_price) || 0;
      });
      var seen = {}, jobs = [];
      gifts.forEach(function (g) {
        if (paid < g.need || seen[g.slot]) jobs.push({ id: g.key, quantity: 0 });
        else { seen[g.slot] = true; if (g.qty > 1) jobs.push({ id: g.key, quantity: 1 }); }
      });
      var p = Promise.resolve();
      jobs.forEach(function (j) { p = p.then(function () { return json('cart/change.js', j); }); });
      return p.then(function () {
        if (jobs.length) {
          try { if (typeof window.upcartRefreshCart === 'function') window.upcartRefreshCart(); } catch (e) {}
          document.dispatchEvent(new CustomEvent('cart:refresh', { bubbles: true }));
        }
      });
    }).catch(function () {}).then(function () {
      busy = false;
      if (again) { again = false; soon(); }
    });
  }
  function soon() { clearTimeout(timer); timer = setTimeout(check, 350); }

  try {
    var pageFetch = window.fetch;
    window.fetch = function (input) {
      var p = pageFetch.apply(this, arguments);
      var url = typeof input === 'string' ? input : (input && input.url) || '';
      if (CART_WRITE.test(url)) p.then(soon, function () {});
      return p;
    };
    var xOpen = XMLHttpRequest.prototype.open, xSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (m, u) { this.__gwpCart = CART_WRITE.test(String(u)); return xOpen.apply(this, arguments); };
    XMLHttpRequest.prototype.send = function () {
      if (this.__gwpCart) this.addEventListener('loadend', soon);
      return xSend.apply(this, arguments);
    };
  } catch (e) {}

  /* The /cart page updates by reloading, so also check on every page load. */
  document.addEventListener('visibilitychange', function () { if (document.visibilityState === 'visible') soon(); });
  soon();
})();
