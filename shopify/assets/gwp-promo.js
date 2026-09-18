/* ============================================================================
   LUCKY GOLF · TIERED GIFT WITH PURCHASE

   Five things this file is careful about, four of them learned on the BOGO
   page and one of them learned from the store's cart app:

   1. SHOPIFY OWNS THE SUBTOTAL. Both tiers are decided by a number read back
      out of /cart.js after every write. Nothing here accumulates a running
      total, so the page cannot drift from checkout.

   2. GIFT LINES ARE NOT MONEY. They are stripped out of that subtotal before
      either threshold is tested, which is what stops a free polo from paying
      for itself.

   3. WRITES ARE SERIALISED, NOT FIRED. Every cart call goes on one promise
      chain. Two fast clicks queue instead of racing, and a gift can only be
      added by the one handler that holds the chain. That is the double-add
      guard: not a flag somebody has to remember to clear.

   4. A REFUSAL IS SAID OUT LOUD. 422 is what a sold-out gift variant looks
      like from here. Silence is how a broken cart hides for a day.

   5. THE DRAWER IS NOT OURS. This store's slide cart is the UpCart app, which
      intercepts add-to-cart and opens itself. We opt out for the life of this
      page and tell it to re-read the cart afterwards, or it shows a stale bag.

   The page is built on lucky.css, so this file never touches a colour, a font
   or a layout. It toggles aria-pressed, hidden, data-state and text. Nothing
   here rebuilds markup with innerHTML, which is why a reader on a keyboard
   never loses their place.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.getElementById('gwp');
  var dataEl = document.getElementById('gwp-data');
  if (!root || !dataEl) return;

  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }

  /* ---------------------------------------------------------------- config
     Every id and every string arrives from Liquid. Nothing below is typed
     into this file, which is why changing a threshold in the theme editor
     changes the behaviour without a deploy. */
  var T1 = parseInt(root.getAttribute('data-tier1'), 10) || 0;
  var T2 = parseInt(root.getAttribute('data-tier2'), 10) || 0;
  /* Free shipping. Checked against the live store on 2026-09-18: $128 and
     $166 carts paid $18 ground, a $198 cart got FREE SHIPPING. It is the
     third line the bar counts toward once both gifts are in. */
  var SHIP = parseInt(root.getAttribute('data-ship'), 10) || 0;
  /* The thresholds are set in the store's currency (USD). A shopper browsing in
     another currency (Shopify Markets; found live on a phone showing RSD) gets
     cart totals in that currency, so convert the lines with the same rate
     Shopify uses, or every club would look like it clears $140. */
  var RATE = parseFloat(window.Shopify && Shopify.currency && Shopify.currency.rate) || 1;
  if (RATE !== 1) { T1 = Math.round(T1 * RATE); T2 = Math.round(T2 * RATE); SHIP = Math.round(SHIP * RATE); }
  var COPY = {
    /* Two labels per tier and they are not interchangeable. g1/g2 are the
       mid-sentence ones ("your free polo") because every template below drops
       them somewhere other than the first word. bar1/bar2 are the standalone
       ones on the phone bar, where the label IS the sentence. Using the card
       headline in both places produced "The hat and a polo is waiting". */
    g1: root.getAttribute('data-gift1-short') || '',
    g2: root.getAttribute('data-gift2-short') || '',
    bar1: root.getAttribute('data-bar-gift1') || '',
    bar2: root.getAttribute('data-bar-gift2') || '',
    start: root.getAttribute('data-copy-start') || '',
    away1: root.getAttribute('data-copy-away1') || '',
    away2: root.getAttribute('data-copy-away2') || '',
    hit1: root.getAttribute('data-copy-hit1') || '',
    hit2: root.getAttribute('data-copy-hit2') || '',
    shipAway: root.getAttribute('data-copy-ship-away') || '',
    pick: root.getAttribute('data-copy-pick') || '',
    locked: root.getAttribute('data-copy-locked') || '',
    add: root.getAttribute('data-copy-add') || '',
    adding: root.getAttribute('data-copy-adding') || '',
    added: root.getAttribute('data-copy-added') || '',
    soldout: root.getAttribute('data-copy-soldout') || '',
    claim: root.getAttribute('data-copy-claim') || '',
    claimed: root.getAttribute('data-copy-claimed') || '',
    giftLost: root.getAttribute('data-copy-gift-lost') || '',
    giftWon: root.getAttribute('data-copy-gift-won') || '',
    error: root.getAttribute('data-copy-error') || '',
    giftSoldOut: root.getAttribute('data-copy-soldout-gift') || '',
    magsHat: root.getAttribute('data-mags-hat') || '',
    magsPolo: root.getAttribute('data-mags-polo') || '',
    magsGo: root.getAttribute('data-mags-go') || '',
    pop1Title: root.getAttribute('data-pop1-title') || '',
    pop1Body: root.getAttribute('data-pop1-body') || '',
    pop1More: root.getAttribute('data-pop1-more') || '',
    pop2Title: root.getAttribute('data-pop2-title') || '',
    pop2Body: root.getAttribute('data-pop2-body') || '',
    pop2More: root.getAttribute('data-pop2-more') || '',
    popShip: root.getAttribute('data-pop-ship') || ''
  };

  var GIFTS = D.gifts || {};
  var PRODUCTS = {};
  (D.products || []).forEach(function (p) { PRODUCTS[p.id] = p; });

  /* Which variant ids are gifts, and which tier each belongs to. This is the
     set that gets subtracted from the subtotal. */
  var GIFT_TIER_OF = {};
  Object.keys(GIFTS).forEach(function (slot) {
    var tier = slot === 'polo' ? 2 : 1;
    (GIFTS[slot].variants || []).forEach(function (v) { GIFT_TIER_OF[v.id] = tier; });
  });
  var GIFT_PROP = '_gwp_gift';

  /* ------------------------------------------------------------------ dom */
  var railEl = document.getElementById('gwp-rail');
  var sayEl = document.getElementById('gwp-say');
  var fillEl = document.getElementById('gwp-fill');
  var ballEl = document.getElementById('gwp-ball');
  var pickEl = document.getElementById('gwp-pick');
  var lastPct = null;
  var railSumEl = document.getElementById('gwp-rail-sum');
  var barSumEl = document.getElementById('gwp-bar-sum');
  var barGiftEl = document.getElementById('gwp-bar-gift');
  var toastEl = document.getElementById('gwp-toast');
  var nodeEls = [].slice.call(root.querySelectorAll('.gwp-node'));
  var giftEls = [].slice.call(root.querySelectorAll('[data-gift]'));
  var cardEls = [].slice.call(root.querySelectorAll('.gwp-card'));

  /* ---------------------------------------------------------------- money
     The store's own format string, so a currency change in Shopify does not
     need a change here. */
  var FMT = D.moneyFormat || '${{amount}}';
  function money(cents) {
    cents = Math.round(cents || 0);
    var neg = cents < 0;
    cents = Math.abs(cents);
    function group(str, sep) { return str.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1' + sep); }
    var out = FMT.replace(/\{\{\s*(\w+)\s*\}\}/g, function (_, name) {
      var whole = Math.floor(cents / 100);
      var part = ('0' + (cents % 100)).slice(-2);
      switch (name) {
        case 'amount_no_decimals': return group(String(whole), ',');
        case 'amount_with_comma_separator': return group(String(whole), '.') + ',' + part;
        case 'amount_no_decimals_with_comma_separator': return group(String(whole), '.');
        case 'amount_with_apostrophe_separator': return group(String(whole), "'") + '.' + part;
        default: return group(String(whole), ',') + '.' + part;
      }
    });
    return (neg ? '-' : '') + out;
  }
  /* A threshold is a round number, so "$90" reads better than "$90.00" in a
     sentence. Anything with cents in it keeps them. */
  function moneyShort(cents) {
    var s = money(cents);
    return cents % 100 === 0 ? s.replace(/([.,])00\b/, '') : s;
  }
  function fill(tpl, vars) {
    return String(tpl || '').replace(/\{(\w+)\}/g, function (m, k) {
      return Object.prototype.hasOwnProperty.call(vars, k) ? vars[k] : m;
    });
  }

  /* ---------------------------------------------------------------- speak */
  var toastTimer = null;
  var toastText = toastEl && toastEl.querySelector('[data-toast-text]');
  var toastMags = toastEl && toastEl.querySelector('.gwp-toast-mags');
  /* Mags only shows up for good news. An error with a bird on it is a joke
     at the customer's expense. */
  function toast(msg, mags) {
    if (!msg || !toastEl) return;
    (toastText || toastEl).textContent = msg;
    if (toastMags) toastMags.hidden = !mags;
    toastEl.classList.toggle('has-mags', !!(mags && toastMags));
    toastEl.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.hidden = true; }, 5200);
  }

  /* ----------------------------------------------------------- the drawer */
  function armQuietCart() {
    try { window.upcartShouldSkipAddToCart = function () { return true; }; } catch (e) {}
  }
  function settleCart() {
    try { if (typeof window.upcartRefreshCart === 'function') window.upcartRefreshCart(); } catch (e) {}
    var until = Date.now() + 1500;
    (function tick() {
      if (document.body.classList.contains('upcartPopupShow')) {
        try { if (typeof window.upcartCloseCart === 'function') window.upcartCloseCart(); } catch (e) {}
        document.body.classList.remove('upcartPopupShow');
      }
      var n = document.querySelector('cart-notification');
      if (n) n.classList.remove('active', 'animate');
      var d = document.querySelector('cart-drawer');
      if (d && d.classList.contains('active')) {
        if (typeof d.close === 'function') d.close(); else d.classList.remove('active', 'animate');
      }
      document.body.classList.remove('overflow-hidden');
      if (Date.now() < until) setTimeout(tick, 90);
    })();
  }

  /* ------------------------------------------------------------ cart calls
     The three documented Cart AJAX endpoints and nothing else. Every one
     resolves with a parsed body, including a refusal, because a 422 from
     /cart/add.js carries the reason and throwing it away is how a sold-out
     gift looks like a bug. */
  function base() { return (window.Shopify && Shopify.routes && Shopify.routes.root) || '/'; }
  /* Our own calls use the fetch the page had before we started watching it
     (see "cart changes from elsewhere" below), so they never trigger a re-read. */
  var ownFetch = window.fetch.bind(window);
  function call(method, path, body) {
    var opts = { method: method, headers: { 'Accept': 'application/json' }, credentials: 'same-origin' };
    if (body) {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(body);
    }
    return ownFetch(base() + path, opts).then(function (r) {
      return r.json().then(
        function (j) { return { ok: r.ok, status: r.status, body: j }; },
        function () { return { ok: r.ok, status: r.status, body: null }; }
      );
    });
  }
  function getCart() { return call('GET', 'cart.js'); }
  function addToCart(id, qty, props) {
    var item = { id: id, quantity: qty };
    if (props) item.properties = props;
    return call('POST', 'cart/add.js', { items: [item] });
  }
  function changeLine(key, qty) { return call('POST', 'cart/change.js', { id: key, quantity: qty }); }

  /* One chain. Every write is appended to it, so two clicks land in the order
     they were made and a gift add can never interleave with a gift removal. */
  var chain = Promise.resolve();
  function queue(fn) {
    var run = chain.then(fn, fn);
    chain = run.catch(function () {});
    return run;
  }

  /* Reads are coalesced: a burst of cart changes from elsewhere on the page
     produces one /cart.js call, not one per event. */
  var refreshTimer = null;
  function refresh(delay) {
    clearTimeout(refreshTimer);
    refreshTimer = setTimeout(function () {
      queue(function () {
        return getCart().then(function (r) {
          if (r.body && r.body.items) { cart = r.body; return reconcile(); }
        });
      });
    }, delay == null ? 220 : delay);
  }

  /* ------------------------------------------------------------ cart model */
  var cart = { items: [] };

  function isGiftLine(line) {
    if (GIFT_TIER_OF[line.variant_id]) return true;
    return !!(line.properties && line.properties[GIFT_PROP]);
  }
  function giftTierOfLine(line) {
    if (GIFT_TIER_OF[line.variant_id]) return GIFT_TIER_OF[line.variant_id];
    var p = line.properties && line.properties[GIFT_PROP];
    return p === 'polo' ? 2 : p ? 1 : 0;
  }
  /* The number both tiers are tested against: everything the reader is
     actually paying for, with the gifts taken out. */
  function paidSubtotal() {
    var n = 0;
    (cart.items || []).forEach(function (line) {
      if (isGiftLine(line)) return;
      n += (line.final_line_price != null ? line.final_line_price : line.line_price) || 0;
    });
    return n;
  }
  function giftLines(slot) {
    var tier = slot === 'polo' ? 2 : 1;
    return (cart.items || []).filter(function (l) {
      return isGiftLine(l) && giftTierOfLine(l) === tier;
    });
  }
  function tierOf(sub) {
    if (T2 && sub >= T2) return 2;
    if (T1 && sub >= T1) return 1;
    return 0;
  }

  /* --------------------------------------------------------- reconciliation
     Runs after every read. It only ever REMOVES: a gift the reader no longer
     qualifies for, and any duplicate of one they do. Adding is always the
     reader's own click, because they choose the colour. */
  var lastTier = null;
  var reconciling = false;

  function reconcile() {
    if (reconciling) { paint(); return Promise.resolve(); }
    var tier = tierOf(paidSubtotal());
    var jobs = [];
    var lost = [];

    ['hat', 'polo'].forEach(function (slot) {
      if (!GIFTS[slot]) return;
      var need = slot === 'polo' ? 2 : 1;
      var lines = giftLines(slot);
      if (!lines.length) return;

      if (tier < need) {
        lines.forEach(function (l) { jobs.push({ key: l.key, qty: 0 }); });
        lost.push(slot === 'polo' ? COPY.g2 : COPY.g1);
        return;
      }
      /* Qualified, but holding more than one. Two tabs, a double tap that beat
         the queue, or a line that survived from an older cart. Trim to one
         rather than shipping two free polos. */
      lines.forEach(function (l, i) {
        if (i > 0) jobs.push({ key: l.key, qty: 0 });
        else if (l.quantity > 1) jobs.push({ key: l.key, qty: 1 });
      });
    });

    if (!jobs.length) { announceTier(tier); paint(); return Promise.resolve(); }

    reconciling = true;
    var p = Promise.resolve();
    jobs.forEach(function (j) {
      p = p.then(function () {
        armQuietCart();
        return changeLine(j.key, j.qty).then(function (r) {
          if (r.body && r.body.items) cart = r.body;
        });
      });
    });
    return p.then(function () {
      reconciling = false;
      settleCart();
      if (lost.length) toast(fill(COPY.giftLost, { gift: lost.join(' and ') }));
      announceTier(tierOf(paidSubtotal()));
      paint();
    }, function () { reconciling = false; paint(); });
  }

  /* One gold pulse on the card that just opened, so the eye knows where to go. */
  function cue(slot) {
    var el = document.getElementById('gwp-gift-' + slot);
    if (!el) return;
    el.classList.remove('is-cue'); void el.offsetWidth; el.classList.add('is-cue');
  }

  /* A tier crossing is worth a toast. A tier already open on page load is
     not, which is what lastTier === null guards. */
  function announceTier(tier) {
    if (lastTier !== null && tier > lastTier) {
      if (!magsEl) toast(fill(COPY.giftWon, { gift: tier >= 2 ? COPY.g2 : COPY.g1 }), true);
      cue(tier >= 2 ? 'polo' : 'hat');
    }
    lastTier = tier;
  }

  /* ============================== CHIP PICKERS ==============================
     lucky.css gives .lg-chip and no dropdown, so every option axis is a row of
     chips with aria-pressed. Reading a selection means reading the pressed
     chip in each group.
     ====================================================================== */
  function chipsIn(scope, attr) { return [].slice.call(scope.querySelectorAll('[' + attr + ']')); }
  function axisCount(chips, attr) {
    var max = -1;
    chips.forEach(function (c) { max = Math.max(max, parseInt(c.getAttribute(attr), 10)); });
    return max + 1;
  }
  function readSel(chips, attr) {
    var out = [];
    chips.forEach(function (c) {
      if (c.getAttribute('aria-pressed') === 'true') out[parseInt(c.getAttribute(attr), 10)] = c.getAttribute('data-val');
    });
    for (var i = 0; i < axisCount(chips, attr); i++) if (out[i] == null) out[i] = '';
    return out;
  }
  function writeSel(chips, attr, want) {
    chips.forEach(function (c) {
      var ax = parseInt(c.getAttribute(attr), 10);
      c.setAttribute('aria-pressed', c.getAttribute('data-val') === want[ax] ? 'true' : 'false');
    });
  }
  function matchVariant(spec, want) {
    if (!want || !want.length) return (spec.variants || [])[0] || null;
    for (var i = 0; i < spec.variants.length; i++) {
      var v = spec.variants[i], ok = true;
      for (var k = 0; k < want.length; k++) { if (v.opts[k] !== want[k]) { ok = false; break; } }
      if (ok) return v;
    }
    return null;
  }
  /* Can this value be bought at all, given what is chosen on the OTHER axes?
     The chip stays clickable either way: switching to it is what makes it
     available again, and disabling it would hide that. It just says so, and
     the other axes repair themselves on the click. */
  function usable(spec, want, axis, val) {
    for (var i = 0; i < spec.variants.length; i++) {
      var v = spec.variants[i];
      if (!v.available || v.opts[axis] !== val) continue;
      var ok = true;
      for (var k = 0; k < want.length; k++) {
        if (k !== axis && v.opts[k] !== want[k]) { ok = false; break; }
      }
      if (ok) return true;
    }
    return false;
  }
  function markChips(chips, attr, spec, want) {
    chips.forEach(function (c) {
      var ax = parseInt(c.getAttribute(attr), 10);
      var dead = !usable(spec, want, ax, c.getAttribute('data-val'));
      if (dead) c.setAttribute('data-dead', 'true'); else c.removeAttribute('data-dead');
      c.setAttribute('aria-label', c.getAttribute('data-val') + (dead ? ', ' + COPY.soldout.toLowerCase() : ''));
    });
  }
  /* The reader picked a value that does not exist alongside their other
     choices. Rather than a dead end, move the other axes to the first
     combination that keeps the value they just asked for. */
  function repair(spec, want, axis) {
    var v = matchVariant(spec, want);
    if (v && v.available) return want;
    for (var i = 0; i < spec.variants.length; i++) {
      var c = spec.variants[i];
      if (c.available && c.opts[axis] === want[axis]) return c.opts.slice(0, want.length);
    }
    return want;
  }

  /* ------------------------------------------------------------- the rail */
  function paintRail(sub, tier) {
    /* The bar is a hole: tee at $0, a flag per tier, the green at free
       shipping. So it runs to SHIP when there is one, not to the last tier. */
    var MAX = SHIP > T2 ? SHIP : T2;
    var pct = (MAX ? Math.min(1, sub / MAX) * 100 : 0).toFixed(2);
    fillEl.style.width = pct + '%';
    /* The ball rides the front of the fill. When the bag changes it hops to
       its new spot, once. It never loops and it never moves on its own. */
    if (ballEl) {
      ballEl.style.left = pct + '%';
      if (lastPct !== null && pct !== lastPct) {
        ballEl.classList.remove('is-fly'); void ballEl.offsetWidth; ballEl.classList.add('is-fly');
      }
      lastPct = pct;
    }
    railEl.setAttribute('data-tier', String(tier));

    nodeEls.forEach(function (n) {
      var which = parseInt(n.getAttribute('data-node'), 10);
      var hit = which === 3 ? (SHIP && sub >= SHIP) : tier >= which;
      if (hit) n.setAttribute('data-hit', 'true'); else n.removeAttribute('data-hit');
    });

    var hatClaimed = giftLines('hat').length > 0;
    var poloClaimed = giftLines('polo').length > 0;
    var hasPolo = !!GIFTS.polo;
    var msg, pickSlot = null;

    if (sub <= 0) {
      msg = COPY.start;
    } else if (tier === 0) {
      msg = fill(COPY.away1, { amount: moneyShort(T1 - sub), gift: COPY.g1 });
    } else if (tier === 1) {
      if (GIFTS.hat && !hatClaimed) { msg = fill(COPY.pick, { gift: COPY.g1 }); pickSlot = 'hat'; }
      else if (hasPolo) msg = fill(COPY.away2, { amount: moneyShort(T2 - sub), gift: COPY.g2 });
      else msg = COPY.hit1;
    } else {
      if (hasPolo && !poloClaimed) { msg = fill(COPY.pick, { gift: COPY.g2 }); pickSlot = 'polo'; }
      else if (GIFTS.hat && !hatClaimed) { msg = fill(COPY.pick, { gift: COPY.g1 }); pickSlot = 'hat'; }
      else if (SHIP && sub < SHIP) msg = fill(COPY.shipAway, { amount: moneyShort(SHIP - sub) });
      else msg = COPY.hit2;
    }

    /* Only write when it changed. An aria-live region re-announces on every
       write, and a bar that repainted on scroll would talk over the page. */
    if (sayEl.textContent !== msg) sayEl.textContent = msg;
    /* A gift is waiting: the message grows a link straight to that card. The
       page never scrolls on its own; the reader decides when to go. */
    if (pickEl) {
      pickEl.hidden = !pickSlot;
      if (pickSlot) { pickEl.setAttribute('href', '#gwp-gift-' + pickSlot); pickEl.setAttribute('data-scroll-to', 'gwp-gift-' + pickSlot); }
    }

    var m = money(sub);
    if (railSumEl) railSumEl.textContent = m;
    if (barSumEl) barSumEl.textContent = m;

    if (barGiftEl) {
      if (tier >= 2) { barGiftEl.textContent = COPY.bar2; barGiftEl.removeAttribute('data-none'); }
      else if (tier === 1) { barGiftEl.textContent = COPY.bar1; barGiftEl.removeAttribute('data-none'); }
      else { barGiftEl.textContent = barGiftEl.getAttribute('data-empty') || ''; barGiftEl.setAttribute('data-none', 'true'); }
    }
  }

  /* ------------------------------------------------------------ the gifts
     THE FOIL RULE. lucky.css allows one foil button per view, and the band can
     show two gift cards at once. So only the FIRST gift that is unlocked and
     unclaimed wears the foil; the other drops to the ghost. That keeps the
     rule, and it also reads as an order: claim the hat, and the polo lights up
     behind it. A claimed button is neither, it is the done state. */
  function paintGifts(sub, tier) {
    var foilTaken = false;
    giftEls.forEach(function (el) {
      var slot = el.getAttribute('data-gift');
      var spec = GIFTS[slot];
      if (!spec) return;
      var need = parseInt(el.getAttribute('data-gift-tier'), 10) || 1;
      var threshold = parseInt(el.getAttribute('data-threshold'), 10) || 0;
      var unlocked = tier >= need;
      var claimed = giftLines(slot).length > 0;

      var lock = el.querySelector('[data-lock]');
      var lockTx = el.querySelector('[data-lock-text]');
      var pick = el.querySelector('[data-pick]');
      var btn = el.querySelector('[data-claim]');
      var chips = chipsIn(el, 'data-gift-axis');

      el.setAttribute('data-state', claimed ? 'claimed' : unlocked ? 'open' : 'locked');

      if (!unlocked) {
        if (lockTx) {
          lockTx.textContent = fill(COPY.locked, {
            amount: moneyShort(threshold),
            away: moneyShort(Math.max(0, threshold - sub)),
            gift: need === 2 ? COPY.g2 : COPY.g1
          });
        }
        if (lock) lock.hidden = false;
        if (pick) pick.hidden = true;
        return;
      }

      if (lock) lock.hidden = true;
      if (pick) pick.hidden = false;

      var want = readSel(chips, 'data-gift-axis');
      markChips(chips, 'data-gift-axis', spec, want);
      var picked = el.querySelector('[data-picked]');
      if (picked) picked.textContent = want.filter(Boolean).join(' · ');
      var v = matchVariant(spec, want);
      var ok = !!(v && v.available);

      if (btn && !btn.hasAttribute('data-busy')) {
        btn.setAttribute('data-variant-id', v ? String(v.id) : '');
        var lb = btn.querySelector('.lb');
        if (claimed) {
          btn.disabled = true;
          btn.setAttribute('data-done', 'true');
          if (lb) lb.textContent = COPY.claimed;
        } else {
          btn.removeAttribute('data-done');
          btn.disabled = !ok;
          if (lb) lb.textContent = ok ? COPY.claim : COPY.soldout;
          if (ok && !foilTaken) { btn.classList.remove('lg-btn-line'); foilTaken = true; }
          else btn.classList.add('lg-btn-line');
        }
      }
    });
  }

  /* ------------------------------------------------------------- the grid */
  function paintCard(card) {
    var spec = PRODUCTS[card.getAttribute('data-pid')];
    if (!spec) return;
    var chips = chipsIn(card, 'data-axis');
    var want = readSel(chips, 'data-axis');
    markChips(chips, 'data-axis', spec, want);

    var v = matchVariant(spec, want);
    var btn = card.querySelector('[data-add]');
    var priceEl = card.querySelector('[data-price]');

    if (priceEl && v) priceEl.textContent = moneyShort(v.price);
    if (v && v.img) {
      var img = card.querySelector('.lg-card-ph img');
      if (img && img.getAttribute('src') !== v.img) {
        img.setAttribute('src', v.img);
        img.removeAttribute('srcset');
      }
    }
    if (btn && !btn.hasAttribute('data-busy') && !btn.hasAttribute('data-done')) {
      var ok = !!(v && v.available);
      btn.setAttribute('data-variant-id', v ? String(v.id) : '');
      btn.disabled = !ok;
      var lb = btn.querySelector('.lb');
      if (lb) lb.textContent = ok ? COPY.add : COPY.soldout;
      if (ok) card.removeAttribute('data-out'); else card.setAttribute('data-out', 'true');
    }
  }

  function paint() {
    var sub = paidSubtotal();
    var tier = tierOf(sub);
    paintRail(sub, tier);
    paintGifts(sub, tier);
    paintMags(tier);
  }

  /* ============================== MAGS, THE GUIDE ============================
     Mags is the one who gets the reader to checkout. He shows up the moment a
     gift unlocks and always says exactly one next step, and tapping him does
     it: take me to the hat, take me to the polo, take me to checkout. After a
     gift is claimed a small pop-up asks the question outright (check out, or
     keep going?); closing it shrinks it into Mags, who then holds the door.
     ======================================================================== */
  var magsEl = document.getElementById('gwp-mags');
  var magsSay = magsEl && magsEl.querySelector('[data-mags-say]');
  var popEl = document.getElementById('gwp-pop');
  var popOpen = false, magsMode = null, magsBooted = false, popSeen = {};
  var lastFocus = null;
  function calm() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function hop() {
    if (!magsEl || calm()) return;
    magsEl.classList.remove('is-hop'); void magsEl.offsetWidth; magsEl.classList.add('is-hop');
  }
  function guideMode(tier) {
    var hat = giftLines('hat').length > 0, polo = giftLines('polo').length > 0;
    if (tier < 1) return null;
    if (GIFTS.hat && !hat) return 'hat';
    if (GIFTS.polo && tier >= 2 && !polo) return 'polo';
    return 'checkout';
  }
  function paintMags(tier) {
    if (!magsEl) return;
    var mode = guideMode(tier);
    if (popOpen || !mode) { magsEl.hidden = true; magsMode = mode; return; }
    var txt = mode === 'hat' ? COPY.magsHat : mode === 'polo' ? COPY.magsPolo : COPY.magsGo;
    if (magsSay.textContent !== txt) magsSay.textContent = txt;
    magsEl.setAttribute('data-mode', mode);
    var was = magsEl.hidden;
    magsEl.hidden = false;
    liftMags();
    if (magsBooted && (mode !== magsMode || was)) hop();
    magsMode = mode;
  }
  /* Desktop: before the rail sticks to the top it sits at the bottom of the
     first screen, right where Mags lives. While it is down there, Mags stands
     on top of it instead of over its message. */
  function liftMags() {
    if (!magsEl || !railEl) return;
    var lift = 0;
    if (window.innerWidth >= 750) {
      var r = railEl.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > window.innerHeight - 120) lift = Math.max(0, window.innerHeight - r.top + 12 - 24);
    }
    magsEl.style.transform = lift ? 'translateY(' + (-lift) + 'px)' : '';
  }
  var liftRaf = null;
  window.addEventListener('scroll', function () { cancelAnimationFrame(liftRaf); liftRaf = requestAnimationFrame(liftMags); }, { passive: true });
  window.addEventListener('resize', liftMags);

  function jumpTo(id) {
    var target = document.getElementById(id);
    if (!target) return;
    var gift = target.hasAttribute('data-gift');
    target.scrollIntoView({ behavior: calm() ? 'auto' : 'smooth', block: gift ? 'center' : 'start' });
    if (gift) cue(target.getAttribute('data-gift'));
    target.focus({ preventScroll: true });
  }

  function openPop(kind) {
    if (!popEl || popSeen[kind]) return;
    popSeen[kind] = true;
    var sub = paidSubtotal();
    var title = kind === 'more' ? COPY.pop1Title : COPY.pop2Title;
    var body = kind === 'more' ? fill(COPY.pop1Body, { amount: moneyShort(Math.max(0, T2 - sub)) }) : COPY.pop2Body;
    if (kind === 'done' && SHIP && sub < SHIP && COPY.popShip) body += ' ' + fill(COPY.popShip, { amount: moneyShort(SHIP - sub) });
    popEl.querySelector('[data-pop-title]').textContent = title;
    popEl.querySelector('[data-pop-body]').textContent = body;
    popEl.querySelector('[data-pop-more]').textContent = kind === 'more' ? COPY.pop1More : COPY.pop2More;
    lastFocus = document.activeElement;
    popOpen = true;
    paint();
    popEl.hidden = false;
    popEl.classList.remove('is-out'); popEl.classList.add('is-in');
    var go = popEl.querySelector('[data-pop-go]');
    if (go) go.focus({ preventScroll: true });
  }
  function closePop(after) {
    if (!popEl || popEl.hidden) return;
    var card = popEl.querySelector('.gwp-pop-card');
    popOpen = false;
    paint();                                   /* Mags comes back first, so the card has somewhere to land */
    var done = function () {
      popEl.hidden = true;
      popEl.classList.remove('is-in', 'is-out');
      card.style.transition = ''; card.style.transform = ''; card.style.opacity = '';
      hop();
      if (after) after();
      else if (magsEl && !magsEl.hidden) magsEl.focus({ preventScroll: true });
      else if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    };
    if (calm() || !magsEl || magsEl.hidden) { done(); return; }
    var a = card.getBoundingClientRect(), b = magsEl.querySelector('img').getBoundingClientRect();
    var dx = (b.left + b.width / 2) - (a.left + a.width / 2), dy = (b.top + b.height / 2) - (a.top + a.height / 2);
    popEl.classList.add('is-out');
    card.style.transition = 'transform .42s cubic-bezier(.5,0,.2,1), opacity .42s ease';
    requestAnimationFrame(function () {
      card.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(.12)';
      card.style.opacity = '0';
    });
    setTimeout(done, 440);
  }
  /* After a claim: is there a question worth asking? */
  function maybePop(slot) {
    if (!giftLines(slot).length) return;
    var tier = tierOf(paidSubtotal());
    var hat = giftLines('hat').length > 0, polo = giftLines('polo').length > 0;
    if (hat && (!GIFTS.polo || polo)) openPop('done');
    else if (hat && GIFTS.polo && tier < 2) openPop('more');
  }
  if (popEl) {
    popEl.addEventListener('click', function (e) {
      if (e.target === popEl || e.target.closest('[data-pop-close]')) { e.preventDefault(); closePop(); return; }
      if (e.target.closest('[data-pop-more]')) { e.preventDefault(); closePop(function () { jumpTo('gwp-clubs'); }); }
    });
    popEl.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); closePop(); return; }
      if (e.key !== 'Tab') return;
      var f = [].slice.call(popEl.querySelectorAll('a[href],button'));
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }


  /* ----------------------------------------------------------- the writes */
  function busy(btn, on) {
    if (!btn) return;
    if (on) {
      btn.setAttribute('data-busy', 'true');
      btn.setAttribute('aria-busy', 'true');
      btn.disabled = true;
      var lb = btn.querySelector('.lb');
      if (lb) lb.textContent = COPY.adding;
    } else {
      btn.removeAttribute('data-busy');
      btn.removeAttribute('aria-busy');
      btn.disabled = false;
    }
  }
  function flashDone(btn, label, back) {
    var lb = btn.querySelector('.lb');
    btn.setAttribute('data-done', 'true');
    if (lb) lb.textContent = label;
    setTimeout(function () {
      btn.removeAttribute('data-done');
      if (lb) lb.textContent = back;
    }, 1600);
  }
  function refused(r) {
    if (!r || !r.ok || !r.body) return true;
    return !!(r.body.status && parseInt(r.body.status, 10) >= 400);
  }
  function reasonFor(r, isGift) {
    if (r && r.status === 422) return isGift ? COPY.giftSoldOut : ((r.body && r.body.description) || COPY.error);
    return COPY.error;
  }

  function addProduct(btn) {
    var id = parseInt(btn.getAttribute('data-variant-id'), 10);
    if (!id) return;
    var card = btn.closest('.gwp-card');
    var out = card && card.querySelector('[data-qty-out]');
    var qty = out ? Math.max(1, parseInt(out.textContent, 10) || 1) : 1;

    busy(btn, true);
    queue(function () {
      armQuietCart();
      return addToCart(id, qty).then(function (r) {
        busy(btn, false);
        if (refused(r)) {
          var lb = btn.querySelector('.lb');
          if (lb) lb.textContent = COPY.add;
          toast(reasonFor(r, false));
          return getCart().then(function (c) {
            if (c.body && c.body.items) { cart = c.body; paint(); }
          });
        }
        flashDone(btn, COPY.added, COPY.add);
        settleCart();
        return getCart().then(function (c) {
          if (c.body && c.body.items) { cart = c.body; return reconcile(); }
        });
      }, function () {
        busy(btn, false);
        var lb = btn.querySelector('.lb');
        if (lb) lb.textContent = COPY.add;
        toast(COPY.error);
      });
    });
  }

  /* Claiming a gift. The whole operation sits inside one link of the chain,
     so nothing can add a second one while this is in the air. It re-reads the
     cart first rather than trusting the last paint, then swaps any existing
     gift for the chosen variant. */
  function claimGift(btn) {
    var el = btn.closest('[data-gift]');
    if (!el) return;
    var slot = el.getAttribute('data-gift');
    var need = parseInt(el.getAttribute('data-gift-tier'), 10) || 1;
    var id = parseInt(btn.getAttribute('data-variant-id'), 10);
    if (!id) return;

    busy(btn, true);
    queue(function () {
      armQuietCart();
      return getCart().then(function (c) {
        if (c.body && c.body.items) cart = c.body;

        if (tierOf(paidSubtotal()) < need) {      /* the bag moved under them */
          busy(btn, false); paint();
          return;
        }
        var existing = giftLines(slot);
        var same = existing.filter(function (l) { return l.variant_id === id; });
        if (existing.length === 1 && same.length === 1 && same[0].quantity === 1) {
          busy(btn, false); paint();
          return;
        }

        var p = Promise.resolve();
        existing.forEach(function (l) {
          p = p.then(function () {
            return changeLine(l.key, 0).then(function (r) {
              if (r.body && r.body.items) cart = r.body;
            });
          });
        });
        return p.then(function () {
          var props = {};
          props[GIFT_PROP] = slot;
          return addToCart(id, 1, props);
        }).then(function (r) {
          busy(btn, false);
          var landed = !refused(r);
          if (!landed) {
            toast(reasonFor(r, true));
            /* The variant died under us. Mark it gone so the picker stops
               offering it, then repaint from the real cart. */
            var spec = GIFTS[slot];
            if (spec) spec.variants.forEach(function (v) { if (v.id === id) v.available = false; });
          }
          settleCart();
          return getCart().then(function (c2) {
            if (c2.body && c2.body.items) { cart = c2.body; return reconcile(); }
          }).then(function () { if (landed) maybePop(slot); });
        });
      }, function () {
        busy(btn, false);
        toast(COPY.error);
      });
    });
  }

  /* ---------------------------------------------------------------- events */
  root.addEventListener('click', function (e) {
    /* a chip in the grid */
    var chip = e.target.closest('[data-axis],[data-gift-axis]');
    if (chip) {
      e.preventDefault();
      var isGift = chip.hasAttribute('data-gift-axis');
      var attr = isGift ? 'data-gift-axis' : 'data-axis';
      var scope = chip.closest(isGift ? '[data-gift]' : '.gwp-card');
      var spec = isGift ? GIFTS[scope.getAttribute('data-gift')] : PRODUCTS[scope.getAttribute('data-pid')];
      if (!spec) return;
      var chips = chipsIn(scope, attr);
      var axis = parseInt(chip.getAttribute(attr), 10);
      var want = readSel(chips, attr);
      want[axis] = chip.getAttribute('data-val');
      want = repair(spec, want, axis);
      writeSel(chips, attr, want);
      if (isGift) paint(); else paintCard(scope);
      return;
    }

    var q = e.target.closest('[data-qty]');
    if (q) {
      e.preventDefault();
      var out = q.parentElement.querySelector('[data-qty-out]');
      var next = Math.min(99, Math.max(1, (parseInt(out.textContent, 10) || 1) + parseInt(q.getAttribute('data-qty'), 10)));
      out.textContent = String(next);
      return;
    }

    var add = e.target.closest('[data-add]');
    if (add && !add.disabled) { e.preventDefault(); addProduct(add); return; }

    var claim = e.target.closest('[data-claim]');
    if (claim && !claim.disabled) { e.preventDefault(); claimGift(claim); return; }

    var mg = e.target.closest('#gwp-mags');
    if (mg) {
      e.preventDefault();
      var mode = mg.getAttribute('data-mode');
      if (mode === 'checkout') goCheckout(base() + 'checkout');
      else if (mode) jumpTo('gwp-gift-' + mode);
      return;
    }

    /* The hero CTA stays a real anchor so the keyboard and the back button
       both behave. This only upgrades the jump to a glide, and steps aside
       when the reader has asked for less motion. */
    var jump = e.target.closest('[data-scroll-to]');
    if (jump) {
      var target = document.getElementById(jump.getAttribute('data-scroll-to'));
      if (target && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: target.hasAttribute('data-gift') ? 'center' : 'start' });
        if (target.hasAttribute('data-gift')) cue(target.getAttribute('data-gift'));
        target.focus({ preventScroll: true });
      }
    }
  });

  /* The cart can move without this page touching it: a drawer, a second tab,
     the theme's own add-to-cart in the header. */
  ['cart:refresh', 'cart:update', 'cart-updated', 'upcart:cart:updated'].forEach(function (ev) {
    document.addEventListener(ev, function () { refresh(); });
  });
  window.addEventListener('pageshow', function (e) { if (e.persisted) refresh(0); });
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') refresh(300);
  });
  window.addEventListener('focus', function () { refresh(300); });

  /* Cart changes from elsewhere. The UpCart drawer removes lines with its own
     requests and fires none of the events above, so found in live testing: take
     the Stryker out in the drawer and the polo stayed, now at $67 because the
     discount no longer applied. So watch the requests themselves: any write to
     the cart, by anything on the page, gets one re-read after it lands. */
  var CART_WRITE = /\/cart\/(add|change|update|clear)(\.js)?(\?|$)/;
  try {
    var pageFetch = window.fetch;
    window.fetch = function (input) {
      var p = pageFetch.apply(this, arguments);
      var url = typeof input === 'string' ? input : (input && input.url) || '';
      if (CART_WRITE.test(url)) p.then(function () { refresh(350); }, function () {});
      return p;
    };
    var xOpen = XMLHttpRequest.prototype.open, xSend = XMLHttpRequest.prototype.send;
    XMLHttpRequest.prototype.open = function (m, u) {
      this.__gwpCart = CART_WRITE.test(String(u));
      return xOpen.apply(this, arguments);
    };
    XMLHttpRequest.prototype.send = function () {
      if (this.__gwpCart) this.addEventListener('loadend', function () { refresh(350); });
      return xSend.apply(this, arguments);
    };
  } catch (e) {}

  /* The page's own checkout buttons check the bag one last time on the way out. */
  root.addEventListener('click', function (e) {
    var a = e.target.closest('a[href$="/checkout"]');
    if (!a) return;
    e.preventDefault();
    goCheckout(a.href);
  });
  function goCheckout(href) {
    var go = function () { window.location.href = href; };
    queue(function () {
      return getCart().then(function (r) {
        if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      });
    }).then(go, go);
  }

  /* ------------------------------------------------------------- the tracer
     One shot, drawn the way a launch monitor draws it: carries to the first
     flag, hops to the second, releases to the green. Built from the real
     thresholds, and the ball flies the arc to wherever the bag is. It reads
     the same number the bar does, so the two can never disagree. */
  (function tracer() {
    var host = document.getElementById('gwp-tracer');
    if (!host || !fillEl) return;
    var MAXV = SHIP > T2 ? SHIP : T2, X = function (v) { return 40 + (v / MAXV) * 1120; };
    var stops = [T1, T2].concat(SHIP > T2 ? [SHIP] : []);
    var labels = [].slice.call(root.querySelectorAll('.gwp-node b')).map(function (b) { return b.textContent; });
    var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 1200 170'); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    var ticks = '';
    for (var i = 0; i <= 22; i++) { var tx = 40 + i * (1120 / 22); ticks += '<line x1="' + tx + '" x2="' + tx + '" y1="140" y2="' + (i % 2 ? 147 : 152) + '"/>'; }
    var d = 'M40 140', prev = 40, lift = [-60, 40, 108];
    stops.forEach(function (v, k) { var x = X(v); d += ' Q ' + ((prev + x) / 2) + ' ' + lift[k] + ' ' + x + ' 140'; prev = x; });
    var flags = stops.map(function (v, k) {
      return '<g class="yd-flag" transform="translate(' + X(v) + ' 140)"><line y2="-34"/><path d="M0 -34 L16 -28 L0 -22Z"/><text y="24" text-anchor="' + (k === stops.length - 1 ? 'end' : 'middle') + '"></text></g>';
    }).join('');
    svg.innerHTML = '<g class="yd-ticks">' + ticks + '<line x1="40" x2="1160" y1="140" y2="140"/></g>' +
      '<path class="yd-path" pathLength="1" d="' + d + '"/><circle class="yd-apex" cx="' + (40 + X(T1)) / 2 + '" cy="40" r="3.5"/>' + flags +
      '<text class="yd-tee" x="40" y="164"></text><circle class="yd-ball" cx="40" cy="140" r="6"/>';
    [].slice.call(svg.querySelectorAll('.yd-flag text')).forEach(function (t, k) { t.textContent = labels[k] || ''; });
    svg.querySelector('.yd-tee').textContent = host.getAttribute('data-tee') || '';
    var wrap = host.querySelector('.lg-wrap') || host; wrap.appendChild(svg);

    var pathEl = svg.querySelector('.yd-path'), ball = svg.querySelector('.yd-ball'), L = pathEl.getTotalLength(), cur = 0, raf = null;
    function lenAtX(x) { var lo = 0, hi = L; for (var n = 0; n < 22; n++) { var m = (lo + hi) / 2; if (pathEl.getPointAtLength(m).x < x) lo = m; else hi = m; } return lo; }
    function place(len) { cur = len; var p = pathEl.getPointAtLength(len); ball.setAttribute('cx', p.x); ball.setAttribute('cy', p.y); }
    /* A hidden tab gets no animation frames, so the ball would freeze mid-flight.
       If nobody can see it, or they asked for less motion, it just lands. */
    function fly(to) {
      cancelAnimationFrame(raf);
      if (document.hidden || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { place(to); return; }
      var from = cur, t0 = performance.now(), dur = 900 + Math.abs(to - from) * 1.1;
      (function step(now) { var k = Math.min(1, (now - t0) / dur); k = 1 - Math.pow(1 - k, 3); place(from + (to - from) * k); if (k < 1) raf = requestAnimationFrame(step); })(t0);
    }
    function sync() { var pct = parseFloat(fillEl.style.width) || 0; fly(lenAtX(40 + pct / 100 * 1120)); }
    new MutationObserver(sync).observe(fillEl, { attributes: true, attributeFilter: ['style'] });
    sync();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { host.classList.add('is-in'); o.disconnect(); } }); }, { threshold: .4 }).observe(host);
    } else host.classList.add('is-in');
  })();

  /* ------------------------------------------------------------------ boot */
  if (barGiftEl) barGiftEl.setAttribute('data-empty', barGiftEl.textContent);
  cardEls.forEach(paintCard);
  armQuietCart();
  paint();
  queue(function () {
    return getCart().then(function (r) {
      if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      paint();
    }, paint).then(function () { magsBooted = true; });
  });
})();
