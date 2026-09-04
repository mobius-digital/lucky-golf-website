(function(){
  var root = document.getElementById('lg-bogo');
  var dataEl = document.getElementById('lgb-data');
  if (!root || !dataEl) return;

  var D;
  try { D = JSON.parse(dataEl.textContent); } catch(e){ return; }

  var HATS   = (D.hats || []).filter(function(h){ return h && h.id; });
  var UPSELL = D.upsell || [];
  var BUNDLE = D.bundle || 3;
  var CARTURL = D.cartUrl || '/cart';
  if (!HATS.length) return;

  var HAT_BY_ID = {};
  HATS.forEach(function(h){ HAT_BY_ID[h.id] = h; });
  var UNIT = HATS[0].price;                       /* cents */

  var grid   = document.getElementById('bgo-grid');
  var rail   = document.getElementById('bgo-rail');
  var slotsEl= document.getElementById('bgo-slots');
  var hd     = document.getElementById('bgo-hd');
  var sub    = document.getElementById('bgo-sub');
  var totBox = document.getElementById('bgo-tot');
  var totV   = document.getElementById('bgo-tot-v');
  var totSv  = document.getElementById('bgo-tot-sv');
  var goBtn  = document.getElementById('bgo-go');
  var live   = document.getElementById('bgo-live');
  var md     = document.getElementById('bgo-md');

  var COPY = {
    empty:   root.querySelector('#bgo-hd').textContent.trim(),
    emptySub:'Two at ' + money(UNIT) + ', then the third one’s free.'
  };

  function money(cents){
    var n = (cents || 0) / 100;
    return '$' + (n % 1 === 0 ? n.toFixed(0) : n.toFixed(2));
  }
  function esc(s){ var d = document.createElement('div'); d.textContent = (s==null?'':s); return d.innerHTML; }
  function root_(){ return (window.Shopify && Shopify.routes && Shopify.routes.root) || '/'; }

  /* ---------------- cart ----------------
     Shopify owns the cart and the discount. Nothing here computes a price it
     could instead read back: totals come from final_line_price, which already
     has the automatic Buy-2-Get-1 applied, so the rail cannot drift from
     checkout. */
  var cart = {items:[]};

  /* Requests go over XMLHttpRequest. Note that this does NOT dodge anything:
     BOTH window.fetch and XMLHttpRequest are wrapped on this store, by
     Shopify's own AddToCartListener, which only observes the call for
     analytics. Keeping the wrapper in the path is deliberate, so bundle adds
     still show up in tracking. The drawer is handled separately below. */
  function req(method, path, body){
    return new Promise(function(resolve, reject){
      var x = new XMLHttpRequest();
      x.open(method, root_() + path, true);
      x.setRequestHeader('Accept', 'application/json');
      if (body) x.setRequestHeader('Content-Type', 'application/json');
      x.onload = function(){
        try { resolve(JSON.parse(x.responseText)); } catch(e){ reject(e); }
      };
      x.onerror = reject;
      x.send(body ? JSON.stringify(body) : null);
    });
  }
  function getCart(){ return req('GET', 'cart.js'); }
  function post(path, body){ return req('POST', path, body); }

  /* Writes go to /cart/update.js, never /cart/add.js. add.js returns only the
     line it touched, so it needs a second cart.js call to repaint, and it takes
     a delta, so two clicks in flight at once race each other. update.js takes
     absolute quantities for any number of lines and returns the whole cart, so
     one call does everything and repeat clicks are idempotent. Every hat is a
     single-variant product, so one variant id is exactly one line. */

  /* THE DRAWER. Diagnosed against the live storefront, not guessed at.
     This store has no <cart-drawer>; the slide cart is the UpCart app, and an
     add is what opens it (it puts .upcartPopupShow on <body>). UpCart ships a
     documented opt-out, upcartShouldSkipAddToCart, which the app defines as
     `e => false`. Redefining it to return true was verified live to stop the
     drawer opening at all. This file only loads on the bundle page, so the
     override cannot affect add-to-cart anywhere else on the site.
     settleCart() is the belt-and-braces pass for anything that slips through,
     plus Dawn's cart-notification, which this theme also has. */
  function armQuietCart(){
    try { window.upcartShouldSkipAddToCart = function(){ return true; }; } catch(e){}
  }
  function settleCart(){
    /* We added behind UpCart's back, so tell it to re-read the cart. Without
       this its drawer shows a stale bag the next time it is opened. */
    try { if (typeof window.upcartRefreshCart === 'function') window.upcartRefreshCart(); } catch(e){}
    var until = Date.now() + 1800;
    (function tick(){
      if (document.body.classList.contains('upcartPopupShow')){
        try { if (typeof window.upcartCloseCart === 'function') window.upcartCloseCart(); } catch(e){}
        document.body.classList.remove('upcartPopupShow');
      }
      var n = document.querySelector('cart-notification');
      if (n) n.classList.remove('active', 'animate');
      var d = document.querySelector('cart-drawer');
      if (d && d.classList.contains('active')){
        if (typeof d.close === 'function') d.close(); else d.classList.remove('active', 'animate');
      }
      document.body.classList.remove('overflow-hidden');
      if (Date.now() < until) setTimeout(tick, 90);
    })();
  }

  /* ---------------- optimistic writes ----------------
     A cart write on this store measures ~490ms. The old code waited for it
     before repainting AND dropped any click that arrived meanwhile, so a fast
     reader tapping three hats got one tile updating half a second late and two
     taps silently thrown away.
     Now a click updates `pending` and repaints on the spot, and the network
     catches up behind it. `pending` holds the absolute quantity the reader has
     asked for; every read below prefers it over the cart, so the page always
     shows the reader's own intent. Clicks made during a request are coalesced
     into the NEXT request rather than dropped, which is why /cart/update.js is
     the right endpoint: it takes every line in one call. */
  var pending = {};
  var inFlight = false;

  function flush(){
    if (inFlight) return;
    var ids = Object.keys(pending);
    if (!ids.length) return;
    inFlight = true;
    var sent = {};
    ids.forEach(function(k){ sent[k] = pending[k]; });
    armQuietCart();            /* re-arm every time: the app can redefine it */
    settleCart();
    post('cart/update.js', {updates: sent}).then(function(c){
      if (c && c.items) cart = c;
      /* only clear what this request actually carried: anything the reader
         changed while it was in the air must survive and go out next */
      ids.forEach(function(k){ if (pending[k] === sent[k]) delete pending[k]; });
      inFlight = false; paint(); settleCart(); flush();
    }).catch(function(){
      pending = {}; inFlight = false;      /* drop the guess, trust Shopify */
      getCart().then(function(c){ cart = c; paint(); }).catch(function(){});
    });
  }

  function bump(id, next, msg){
    pending[id] = Math.max(0, next);
    paint(msg);                            /* instant, before any request */
    flush();
  }

  function qtyOf(id){
    if (pending.hasOwnProperty(id)) return pending[id];
    var n = 0;
    cart.items.forEach(function(i){ if (i.variant_id === id) n += i.quantity; });
    return n;
  }
  function hatUnits(){
    var n = 0; HATS.forEach(function(h){ n += qtyOf(h.id); }); return n;
  }
  /* hat units in a stable order, for the rail slots: confirmed cart lines keep
     their order, anything only pending is appended */
  function hatUnitList(){
    var out = [], seen = {};
    cart.items.forEach(function(i){
      var h = HAT_BY_ID[i.variant_id];
      if (!h || seen[h.id]) return;
      seen[h.id] = 1;
      for (var k = 0; k < qtyOf(h.id); k++) out.push(h);
    });
    HATS.forEach(function(h){
      if (seen[h.id]) return;
      for (var k = 0; k < qtyOf(h.id); k++) out.push(h);
    });
    return out;
  }
  /* the real money, straight from Shopify. While a write is still in the air
     Shopify has not priced the change yet, so mirror the discount's own rule
     (every BUNDLE-th hat free, cheapest one given away) until it answers. */
  function bundleTotals(){
    if (Object.keys(pending).length){
      var prices = hatUnitList().map(function(h){ return h.price; });
      var was = prices.reduce(function(a, b){ return a + b; }, 0);
      var free = Math.floor(prices.length / BUNDLE);
      var saved = prices.slice().sort(function(a, b){ return a - b; })
                        .slice(0, free).reduce(function(a, b){ return a + b; }, 0);
      return {paid: was - saved, was: was, saved: saved};
    }
    var fin = 0, orig = 0;
    cart.items.forEach(function(i){
      if (!HAT_BY_ID[i.variant_id]) return;
      fin  += (i.final_line_price != null ? i.final_line_price : i.line_price);
      orig += (i.original_line_price != null ? i.original_line_price : i.line_price);
    });
    return {paid:fin, was:orig, saved:Math.max(0, orig - fin)};
  }

  /* ---------------- tiles ---------------- */
  function paintGrid(){
    /* innerHTML below replaces every tile, which throws focus away. A reader on
       a keyboard pressing Enter on "Add to bundle" was landing back on <body>,
       losing their place in a ten-card grid on the one action this page exists
       for. Remember which control held focus and hand it back afterwards. */
    var act = document.activeElement, keep = null;
    if (act && grid.contains(act)){
      keep = act.getAttribute('data-inc') ? ['inc', act.getAttribute('data-inc')]
           : act.getAttribute('data-dec') ? ['dec', act.getAttribute('data-dec')]
           : null;
    }
    var n = hatUnits(), armed = (n % BUNDLE) === (BUNDLE - 1);
    grid.innerHTML = HATS.map(function(h){
      var q = qtyOf(h.id), free = armed && h.available;
      var price = free
        ? '<span class="was">' + money(h.price) + '</span><span class="nowfree">Free</span>'
        : money(h.price);
      var act;
      if (!h.available){
        act = '<button class="lgb-btn lgb-btn-line lgb-btn-sm" type="button" disabled><span>Sold out</span></button>';
      } else if (q > 0){
        act = '<div class="bgo-step" role="group" aria-label="How many ' + esc(h.name) + '">'
            +   '<button type="button" data-dec="' + h.id + '" aria-label="Remove one ' + esc(h.name) + '">&minus;</button>'
            +   '<span class="n">' + q + '</span>'
            +   '<button type="button" data-inc="' + h.id + '" aria-label="Add another ' + esc(h.name) + '">+</button>'
            + '</div>';
      } else {
        act = '<button class="lgb-btn ' + (free ? 'lgb-btn-foil' : 'lgb-btn-ink') + ' lgb-btn-sm" type="button" data-inc="' + h.id + '">'
            +   '<span>' + (free ? 'Add it free' : 'Add to bundle') + '</span></button>';
      }
      return '<div class="bgo-card"' + (q ? ' data-picked' : '') + (h.available ? '' : ' data-out') + '>'
        + (q ? '<span class="tick" aria-hidden="true">' + q + ' in bundle</span>' : '')
        + (h.available ? '' : '<span class="oos">Sold out</span>')
        + '<a class="bgo-ph" href="' + esc(h.url) + '" tabindex="-1" aria-hidden="true">'
        +   '<img src="' + esc(h.img) + '" alt="" width="344" height="344" loading="lazy" decoding="async"></a>'
        + '<span class="nm">' + esc(h.name) + '</span>'
        + '<span class="pr">' + price + '</span>'
        + '<div class="act">' + act + '</div></div>';
    }).join('');
    /* The control may have changed shape under them: "Add to bundle" becomes a
       stepper on the first pick, and the stepper's minus becomes "Add to
       bundle" again at zero. Either way the same hat keeps a [data-inc], so
       that is the fallback. Programmatic focus does not trigger :focus-visible
       after a mouse click, so a mouse reader sees no ring appear. */
    if (keep){
      var again = grid.querySelector('[data-' + keep[0] + '="' + keep[1] + '"]')
               || grid.querySelector('[data-inc="' + keep[1] + '"]');
      if (again) again.focus();
    }
  }

  /* ---------------- rail ---------------- */
  var lastN = null, lastArmed = null, first = true;

  function paintRail(msg){
    var n = hatUnits();
    var freeCount = Math.floor(n / BUNDLE);
    var armed = (n % BUNDLE) === (BUNDLE - 1);
    var t = bundleTotals();

    var units = hatUnitList();
    var start = Math.floor(n / BUNDLE) * BUNDLE;
    if (n > 0 && n % BUNDLE === 0) start = n - BUNDLE;

    if (!slotsEl.childElementCount){
      var html = '';
      for (var s = 0; s < BUNDLE; s++){
        var lbl = s === BUNDLE - 1 ? 'Free' : String(s + 1);
        html += '<div class="bgo-slot' + (s === BUNDLE - 1 ? ' free' : '') + '">'
             +  '<span class="dot"></span><img alt="" width="60" height="60"><span class="lb">' + lbl + '</span></div>';
      }
      slotsEl.innerHTML = html;
    }
    [].slice.call(slotsEl.children).forEach(function(el, i){
      var u = units[start + i], img = el.querySelector('img');
      if (u){ el.setAttribute('data-filled','true'); if (img.getAttribute('src') !== u.img) img.setAttribute('src', u.img); }
      else { el.removeAttribute('data-filled'); img.removeAttribute('src'); }
      if (i === BUNDLE - 1){ armed ? el.setAttribute('data-armed','true') : el.removeAttribute('data-armed'); }
    });

    var state = 'empty', H, S;
    if (n === 0){
      H = COPY.empty; S = COPY.emptySub;
    } else if (armed){
      state = 'armed';
      H = 'Third one’s free. Go on.'; S = 'Any hat on the page, we’re not fussy.';
    } else if (n % BUNDLE === 0){
      state = 'done';
      H = freeCount === 1 ? 'That’s your three' : 'That’s ' + freeCount + ' free hats';
      S = n + ' hats, ' + money(t.paid) + (t.saved ? ', and you saved ' + money(t.saved) + '.' : '.');
    } else {
      state = 'part';
      H = n === 1 ? 'One down' : n + ' in';
      S = 'Add one more and the next one’s free.';
    }
    rail.setAttribute('data-state', state);
    hd.textContent = H;
    sub.textContent = S;

    totBox.hidden = n === 0;
    totV.textContent = money(t.paid);
    totSv.textContent = t.saved > 0 ? 'You saved ' + money(t.saved) : '';
    goBtn.hidden = n < BUNDLE;
    rail.setAttribute('data-show','true');

    if (lastArmed === false && armed){
      rail.classList.remove('fire'); void rail.offsetWidth; rail.classList.add('fire');
      setTimeout(function(){ rail.classList.remove('fire'); }, 1200);
    }
    if (live && msg) live.textContent = msg;

    /* the dialog waits for the bundle to be FINISHED, never for the unlock */
    if (!first && lastN !== null && n > lastN && n > 0 && n % BUNDLE === 0) openMd();

    lastN = n; lastArmed = armed; first = false;
    pad();
  }

  function paint(msg){ paintGrid(); paintRail(msg); }

  /* ---------------- upsell rows ---------------- */
  var sel = {};
  UPSELL.forEach(function(p){
    var d = null;
    for (var i = 0; i < p.variants.length; i++){ if (p.variants[i].available){ d = p.variants[i]; break; } }
    sel[p.handle] = d ? d.opts.slice() : (p.options || []).map(function(o){ return o.values[0]; });
  });
  function variantOf(p){
    var want = sel[p.handle];
    for (var i = 0; i < p.variants.length; i++){
      var v = p.variants[i], ok = true;
      for (var k = 0; k < want.length; k++){ if (v.opts[k] !== want[k]){ ok = false; break; } }
      if (ok) return v;
    }
    return null;
  }
  function rowHtml(p){
    var v = variantOf(p), ok = !!(v && v.available);
    var opts = (p.options || []).map(function(o, i){
      return '<label class="bgo-opt"><span class="l">' + esc(o.name) + '</span>'
        + '<select data-up="' + esc(p.handle) + '" data-axis="' + i + '">'
        + o.values.map(function(val){
            return '<option value="' + esc(val) + '"' + (sel[p.handle][i] === val ? ' selected' : '') + '>' + esc(val) + '</option>';
          }).join('')
        + '</select></label>';
    }).join('');
    /* Same card as a hat tile, so the upsell reads like the rest of the site
       instead of like a list. .bgo-card carries the well, border and hover. */
    return '<div class="bgo-card bgo-upcard">'
      + '<a class="bgo-ph" href="' + esc(p.url) + '" tabindex="-1" aria-hidden="true">'
      +   '<img src="' + esc(p.img) + '" alt="" width="344" height="344" loading="lazy" decoding="async"></a>'
      + '<span class="nm">' + esc(p.name) + '</span>'
      + (p.why ? '<span class="why">' + esc(p.why) + '</span>' : '')
      + '<span class="pr">' + money(v ? v.price : p.price) + '</span>'
      + (opts ? '<div class="bgo-opts">' + opts + '</div>' : '')
      + '<div class="act">'
      +   (ok ? '<button type="button" class="lgb-btn lgb-btn-ink lgb-btn-sm" data-up-add="' + esc(p.handle) + '"><span>Add</span></button>'
             : '<button type="button" class="lgb-btn lgb-btn-line lgb-btn-sm" disabled><span>Sold out</span></button>')
      + '</div></div>';
  }
  function paintUpsell(){
    var by = {apparel:[], club:[]};
    UPSELL.forEach(function(p){ (by[p.group] || by.club).push(p); });
    [['bgo-up-apparel', by.apparel], ['bgo-up-club', by.club], ['bgo-up-page', by.club]]
      .forEach(function(pair){
        var el = document.getElementById(pair[0]);
        if (el) el.innerHTML = pair[1].map(rowHtml).join('');
        if (el && !pair[1].length && el.parentElement) el.parentElement.hidden = true;
      });
  }

  /* ---------------- modal ---------------- */
  var mdLast = null;
  var FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';
  function openMd(){
    if (!md || md.getAttribute('data-open') === 'true') return;
    mdLast = document.activeElement;
    md.hidden = false;
    /* rAF does not fire in a backgrounded tab; without the timeout the reader
       returns to a locked page behind an invisible dialog */
    var reveal = function(){ md.setAttribute('data-open','true'); };
    requestAnimationFrame(reveal); setTimeout(reveal, 60);
    document.body.style.overflow = 'hidden';
    var x = md.querySelector('.bgo-md-x'); if (x) x.focus();
  }
  function closeMd(){
    if (!md || md.getAttribute('data-open') !== 'true') return;
    md.setAttribute('data-open','false');
    document.body.style.overflow = '';
    setTimeout(function(){ md.hidden = true; }, 260);
    if (mdLast && mdLast.focus) mdLast.focus();
  }

  /* ---------------- events ---------------- */
  document.addEventListener('click', function(e){
    var inc = e.target.closest('[data-inc]');
    if (inc && root.contains(inc)){
      e.preventDefault();
      var id = +inc.getAttribute('data-inc'), h = HAT_BY_ID[id];
      if (!h || !h.available) return;
      var wasArmed = (hatUnits() % BUNDLE) === (BUNDLE - 1);
      bump(id, qtyOf(id) + 1,
           h.name + (wasArmed ? ' added free.' : ' added to the bundle.'));
      return;
    }
    var dec = e.target.closest('[data-dec]');
    if (dec && root.contains(dec)){
      e.preventDefault();
      var did = +dec.getAttribute('data-dec');
      var have = qtyOf(did);
      if (!have) return;
      bump(did, have - 1,
           (HAT_BY_ID[did] ? HAT_BY_ID[did].name : 'Hat') + ' removed.');
      return;
    }
    var ua = e.target.closest('[data-up-add]');
    if (ua && root.contains(ua)){
      e.preventDefault();
      var handle = ua.getAttribute('data-up-add');
      var p = UPSELL.filter(function(x){ return x.handle === handle; })[0];
      var v = p && variantOf(p);
      if (!v || !v.available) return;
      var lbl = ua.querySelector('span'), was = lbl.textContent;
      bump(v.id, qtyOf(v.id) + 1, p.name + ' added to the bag.');
      ua.setAttribute('data-added','true'); lbl.textContent = 'Added';
      setTimeout(function(){ ua.removeAttribute('data-added'); lbl.textContent = was; }, 1400);
      return;
    }
    if (e.target.closest('[data-bgo-close]')){ e.preventDefault(); closeMd(); }
  });

  document.addEventListener('change', function(e){
    var s = e.target.closest('select[data-up]');
    if (!s || !root.contains(s)) return;
    sel[s.getAttribute('data-up')][+s.getAttribute('data-axis')] = s.value;
    paintUpsell();
  });

  document.addEventListener('keydown', function(e){
    if (!md || md.hidden) return;
    if (e.key === 'Escape'){ closeMd(); return; }
    if (e.key !== 'Tab') return;
    var f = [].slice.call(md.querySelectorAll(FOCUSABLE)).filter(function(el){ return el.offsetParent !== null; });
    if (!f.length) return;
    var a = f[0], z = f[f.length - 1];
    if (e.shiftKey && document.activeElement === a){ e.preventDefault(); z.focus(); }
    else if (!e.shiftKey && document.activeElement === z){ e.preventDefault(); a.focus(); }
  });

  function pad(){ document.body.style.paddingBottom = rail.offsetHeight + 'px'; }
  window.addEventListener('resize', pad);

  /* hero arithmetic reads the real hat price */
  [].slice.call(root.querySelectorAll('[data-unit-price]')).forEach(function(el){ el.textContent = money(UNIT); });
  var dealSum = root.querySelector('[data-deal-sum]');
  if (dealSum) dealSum.textContent = money(UNIT * (BUNDLE - 1)) + ' for ' + BUNDLE;

  armQuietCart();
  paintUpsell();
  getCart().then(function(c){ cart = c; paint(); }).catch(function(){ paint(); });
})();
