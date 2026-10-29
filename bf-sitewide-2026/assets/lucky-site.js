/* ==========================================================================
   Lucky theme · the site layer on top of lucky.js (v4).
   The bag is Shopify's real cart: adds go through /cart/add.js so Shopify
   publishes product_added_to_cart and every web pixel (GA4, Meta, Triple
   Whale, Klaviyo) sees it. Also: the drawer with the free-shipping hole bar,
   the mega menu, the phone menu, modals, zoom, the rails, Klaviyo signups
   and "Tell me when it's back".
   ========================================================================== */
(function(){
  'use strict';
  var LG = window.LG || {};
  var R = LG.routes || { root: '/', cart: '/cart', add: '/cart/add', change: '/cart/change' };
  var FREE = +LG.freeShipping || 198;
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var money = function(cents){ var n = cents / 100; return '$' + (cents % 100 ? n.toFixed(2) : Math.round(n)); };
  var COVER = 'free-returns-package-protection';
  var isCover = function(l){ return l.handle === COVER; };
  /* reward gifts carry a hidden _lucky_gift property (the tier number) */
  var GIFT = '_lucky_gift';
  var isGift = function(l){ return !!(l.properties && l.properties[GIFT]); };
  var BAG = LG.bag || {};
  var TIERS = (BAG.tiers || []).map(function(t, i){ t.n = i + 1; return t; }).filter(function(t){ return t.on && +t.at > 0; });

  /* ------------------------------------------------------------ the bag */
  var cart = { items: [], item_count: 0, total_price: 0 };
  var subs = [];
  function emit(){ subs.forEach(function(fn){ try { fn(cart); } catch (e) {} }); setTimeout(syncGifts, 0); }
  function json(url, body){
    return fetch(url, body ? { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify(body) }
                           : { headers: { 'Accept': 'application/json' } })
      .then(function(r){ return r.json().then(function(d){ if (!r.ok) throw d; return d; }); });
  }
  function refresh(){ return json(R.cart + '.js').then(function(c){ cart = c; paint(); emit(); return c; }); }
  function goods(){ return cart.items.filter(function(l){ return !isCover(l); }); }
  function goodsTotal(){ return goods().filter(function(l){ return !isGift(l); }).reduce(function(a, l){ return a + l.final_line_price; }, 0); }

  /* ------------------------------------------------------------ rewards
     the free-shipping threshold plus up to three tiers from Theme settings > Lucky bag, as flags on
     the hole bar and one line above it; a tier with a gift puts that gift in the bag */
  function rewards(c){
    var paid = (c.items || []).filter(function(l){ return !isCover(l) && !isGift(l); });
    var t = paid.reduce(function(a, l){ return a + l.final_line_price; }, 0);
    var stops = TIERS.map(function(x){ return { at: +x.at, label: x.label || '', msg: x.msg || '' }; })
      .concat([{ at: FREE, label: 'Free shipping ' + money(FREE * 100), msg: BAG.shipMsg || "more and shipping's on us." }])
      .sort(function(a, b){ return a.at - b.at; });
    var next = stops.filter(function(x){ return x.at * 100 > t; })[0];
    var say = !paid.length ? (TIERS.length ? 'Rewards start at <b>' + money(stops[0].at * 100) + '</b>.' : 'Free shipping at <b>' + money(FREE * 100) + '</b>.')
      : next ? '<b>' + money(next.at * 100 - t) + '</b> ' + esc(next.msg)
      : '<b>' + esc(BAG.allMsg || "Shipping's on us.") + '</b>';
    /* Carver sets (snippets/lg-cs): 2+ wedges ship free while the offer runs */
    var CS = window.LG_CS, csFree = !!(CS && CS.live && CS.ship && CS.units(c) >= 2);
    if (csFree && paid.length) say = '<b>' + esc(BAG.allMsg || "Shipping's on us.") + '</b>';
    return { t: t, n: paid.length, stops: stops, say: say, freeShip: csFree || t >= FREE * 100 };
  }
  /* the Carver sets line above the bar: what one more wedge gets them */
  function csLine(c){
    var CS = window.LG_CS; if (!CS || !CS.live) return '';
    var n = CS.units(c); if (!n) return '';
    var m = CS.msg[Math.min(n, 3) - 1] || '', got = savings(c), due = CS.save(n);
    var note = CS.preview && due && !got ? '<small>Preview: the ' + money(due) + ' comes off once the WEDGE TIER discount is live.</small>' : '';
    return esc(m) + (n < 3 && CS.url ? ' <a href="' + esc(CS.url) + '">' + (CS.bf ? 'See the deals' : 'Build the set') + '</a>' : '') + note;
  }
  /* only the next flag to reach keeps its label (close tiers collided); passed ones are just gold flags */
  function flagLabels(host, rw){
    if (!host) return;
    var fl = [].slice.call(host.querySelectorAll('.lg-hole-flag')), nx = -1;
    rw.stops.some(function(x, i){ if (x.at * 100 > rw.t){ nx = i; return true; } return false; });
    if (nx < 0) nx = fl.length - 1;
    fl.forEach(function(f, i){ f.classList.toggle('is-mute', i !== nx); });
  }
  var syncing = false;
  function syncGifts(){
    if (syncing) return;
    var live = {}; TIERS.forEach(function(x){ if (x.gift) live[String(x.n)] = 1; });
    var r = rewards(cart), jobs = [];
    /* a gift whose tier was switched off (or lost its gift) comes back out */
    cart.items.forEach(function(l){ if (isGift(l) && !live[String(l.properties[GIFT])]) jobs.push(function(){ return json(R.change + '.js', { id: l.key, quantity: 0 }); }); });
    TIERS.forEach(function(x){
      if (!x.gift) return;
      var have = cart.items.filter(function(l){ return l.properties && String(l.properties[GIFT]) === String(x.n); });
      var earned = r.n && r.t >= x.at * 100;
      if (earned && !have.length) jobs.push(function(){ var p = {}; p[GIFT] = String(x.n); return json(R.add + '.js', { items: [{ id: x.gift, quantity: 1, properties: p }] }); });
      else if (!earned && have.length) have.forEach(function(l){ jobs.push(function(){ return json(R.change + '.js', { id: l.key, quantity: 0 }); }); });
      else if (earned && have[0].quantity > 1) jobs.push(function(){ return json(R.change + '.js', { id: have[0].key, quantity: 1 }); });
    });
    if (!jobs.length) return;
    syncing = true;
    jobs.reduce(function(p, j){ return p.then(j); }, Promise.resolve())
      .then(function(){ return json(R.cart + '.js'); })
      .then(function(c){ cart = c; syncing = false; paint(); subs.forEach(function(fn){ try { fn(cart); } catch (e) {} }); })
      .catch(function(){ syncing = false; });
  }

  /* ------------------------------------------------------------ add-ons
     complementary products (Search & Discovery app) first, then the fallback collection (Gear),
     then Shopify's related ones; never something already in the bag */
  /* sale prices: /cart.js has no compare-at price, so read it once per product and repaint */
  var cmp = {}, cmpAsk = {};
  function loadCompare(c){
    var need = (c.items || []).filter(function(l){ return !cmpAsk[l.handle]; });
    if (!need.length) return;
    need.forEach(function(l){ cmpAsk[l.handle] = 1; });
    Promise.all(need.map(function(l){ return fetch((R.root || '/').replace(/\/$/, '') + '/products/' + l.handle + '.js').then(function(r){ return r.ok ? r.json() : null; })
      .then(function(p){ if (p) (p.variants || []).forEach(function(v){ if (v.compare_at_price) cmp[v.id] = v.compare_at_price; }); }).catch(function(){}); }))
      .then(function(){ paint(); subs.forEach(function(fn){ try { fn(cart); } catch (e) {} }); });
  }
  function was(l){ return Math.max(l.original_line_price || 0, (cmp[l.variant_id] || 0) * l.quantity); }
  /* low stock: LG.stock only holds variants that are genuinely low (snippets/lg-stock-map) */
  var STOCK = LG.stock || {};
  function lowLine(id){ var n = STOCK[id]; return n ? String(LG.stockMsg || 'Only {n} left').replace('{n}', n) : ''; }
  function dealTags(l){ var nm = (window.LG_CS || {}).names || {}; return (l.line_level_discount_allocations || []).map(function(a){ var t = a.discount_application && a.discount_application.title; return nm[t] || t; }).filter(Boolean); }
  function savings(c){
    var s = (c.items || []).reduce(function(a, l){ return a + Math.max(0, was(l) - l.final_line_price); }, 0);
    (c.cart_level_discount_applications || []).forEach(function(d){ s += d.total_allocated_amount || 0; });
    return s;
  }
  var upsCache = {};
  function cents(v){ return typeof v === 'string' ? Math.round(parseFloat(v) * 100) : (v || 0); }
  function normalise(p){
    var vs = (p.variants || []).map(function(v){ return { id: v.id, title: v.title, available: v.available !== false, price: cents(v.price), compare: cents(v.compare_at_price) }; });
    var im = p.featured_image || (p.images && p.images[0]); if (im && typeof im === 'object') im = im.src;
    return { id: p.id, handle: p.handle, title: p.title, url: '/products/' + p.handle, image: im || '', variants: vs.filter(function(v){ return v.available; }) };
  }
  function fetchUps(pid){
    if (upsCache[pid]) return upsCache[pid];
    var U = BAG.ups || {}, root = (R.root || '/').replace(/\/$/, '');
    var get = function(url){ return fetch(url).then(function(r){ return r.ok ? r.json() : { products: [] }; }).then(function(d){ return d.products || []; }).catch(function(){ return []; }); };
    var rec = function(intent){ return get(root + '/recommendations/products.json?product_id=' + pid + '&intent=' + intent + '&limit=10'); };
    var col = function(){ return get(root + '/collections/' + encodeURIComponent(U.collection || 'gear') + '/products.json?limit=24'); };
    return upsCache[pid] = Promise.all([rec('complementary'), col(), rec('related')])
      .then(function(r){ return r[0].concat(r[1], r[2]).map(normalise); });
  }
  function upsell(host, c){
    var U = BAG.ups || {}; if (!host) return;
    var paid = (c.items || []).filter(function(l){ return !isCover(l) && !isGift(l); });
    if (!U.on || !paid.length){ host.hidden = true; host.removeAttribute('data-key'); return; }
    var inBag = {}; (c.items || []).forEach(function(l){ inBag[l.product_id] = 1; });
    var gifts = {}; TIERS.forEach(function(x){ if (x.giftHandle) gifts[x.giftHandle] = 1; });
    var key = Object.keys(inBag).sort().join(',');
    if (host.getAttribute('data-key') === key) return;
    host.setAttribute('data-key', key);
    fetchUps(paid[0].product_id).then(function(list){
      if (host.getAttribute('data-key') !== key) return;
      var seen = {}, pick = list.filter(function(p){
        if (seen[p.id] || inBag[p.id] || gifts[p.handle] || p.handle === COVER || !p.variants.length || /gift-card|-gift$/.test(p.handle)) return false;
        return (seen[p.id] = true); }).slice(0, +U.max || 3);
      if (!pick.length){ host.hidden = true; return; }
      host.innerHTML = '<p class="ups-hd">' + esc(U.title || 'Complete the bag') + '</p>' + pick.map(function(p){
        var v = p.variants[0], many = p.variants.length > 1;
        if (CUT[p.handle]) p.image = CUT[p.handle];
        return '<div class="ups-it"><a class="ph" href="' + esc(p.url) + '">' + (p.image ? '<img src="' + esc(p.image + (p.image.indexOf('?') > -1 ? '&' : '?') + 'width=160') + '" alt="" loading="lazy">' : '') + '</a>'
          + '<span class="ups-bd"><a class="nm" href="' + esc(p.url) + '">' + esc(p.title) + '</a>'
          + (many ? '<select class="lg-input ups-sel" aria-label="' + esc(p.title) + ' option">' + p.variants.map(function(x){ return '<option value="' + x.id + '" data-p="' + x.price + '">' + esc(x.title) + '</option>'; }).join('') + '</select>' : '')
          + '<span class="ups-pr">' + money(v.price) + (v.compare > v.price ? ' <s>' + money(v.compare) + '</s>' : '') + '</span></span>'
          + '<button type="button" class="lg-btn-line lg-btn-sm ups-add" data-ups="' + (many ? '' : v.id) + '">Add</button></div>';
      }).join('');
      host.hidden = false;
    });
  }
  document.addEventListener('change', function(e){
    var s = e.target.closest('.ups-sel'); if (!s) return;
    var pr = s.closest('.ups-it').querySelector('.ups-pr'), o = s.options[s.selectedIndex]; if (pr && o) pr.textContent = money(+o.getAttribute('data-p'));
  });
  document.addEventListener('click', function(e){
    var b = e.target.closest('.ups-add'); if (!b) return;
    var it = b.closest('.ups-it'), sel = it.querySelector('.ups-sel'), id = +(b.getAttribute('data-ups') || (sel && sel.value));
    if (!id) return; b.setAttribute('aria-busy', 'true');
    Bag.add([{ id: id, quantity: 1 }], { open: !!b.closest('#cd') }).catch(function(){}).then(function(){ b.removeAttribute('aria-busy'); });
  });
  /* an empty bag suggests a few things instead of just saying so */
  function emptyPicks(host){
    if (!host) return;
    var root = (R.root || '/').replace(/\/$/, '');
    (upsCache['empty'] = upsCache['empty'] || fetch(root + '/collections/' + encodeURIComponent(BAG.emptyCol || 'lucky-golf-clubs') + '/products.json?limit=12')
      .then(function(r){ return r.ok ? r.json() : { products: [] }; }).then(function(d){ return (d.products || []).map(normalise); }).catch(function(){ return []; }))
      .then(function(list){
        var pick = list.filter(function(p){ return p.variants.length && p.handle !== COVER && !/gift-card|-gift$/.test(p.handle); }).slice(0, 3);
        if (!pick.length || !host.isConnected) return;
        host.innerHTML = '<p class="ups-hd">' + esc(BAG.emptyTitle || 'Start with these') + '</p>' + pick.map(function(p){
          var v = p.variants[0], pic = CUT[p.handle] || (p.image ? p.image + (p.image.indexOf('?') > -1 ? '&' : '?') + 'width=160' : '');
          return '<div class="ups-it"><a class="ph" href="' + esc(p.url) + '">' + (pic ? '<img src="' + esc(pic) + '" alt="" loading="lazy">' : '') + '</a>'
            + '<span class="ups-bd"><a class="nm" href="' + esc(p.url) + '">' + esc(p.title) + '</a><span class="ups-pr">'
            + (p.variants.length > 1 ? 'From ' : '') + money(Math.min.apply(null, p.variants.map(function(x){ return x.price; }))) + '</span></span>'
            + '<a class="lg-btn-line lg-btn-sm ups-add" href="' + esc(p.url) + '">Shop</a></div>';
        }).join('');
        host.hidden = false;
      });
  }
  function extras(host, c){
    if (!host) return;
    var bits = [];
    if (BAG.ship) bits.push('<span>' + esc(BAG.ship) + '</span>');
    if (BAG.trust) bits.push('<span>' + esc(BAG.trust) + '</span>');
    if (BAG.payin4 && c.total_price >= 5000) bits.push('<span>Or 4 payments of ' + money(Math.ceil(c.total_price / 4)) + ' with Shop Pay.</span>');
    host.innerHTML = bits.join(''); host.hidden = !bits.length || !(c.items || []).length;
  }

  var Bag = window.LuckyBag = {
    cart: function(){ return cart; },
    onChange: function(fn){ subs.push(fn); fn(cart); },
    refresh: refresh,
    rewards: function(c){ return rewards(c || cart); },
    flagLabels: flagLabels,
    was: was, dealTags: dealTags, lowLine: lowLine, savings: function(c){ return savings(c || cart); }, csLine: function(c){ return csLine(c || cart); },
    upsell: function(host, c){ upsell(host, c || cart); },
    extras: function(host, c){ extras(host, c || cart); },
    /* items: [{ id: variantId, quantity: 1, properties: {} }] */
    add: function(items, opts){
      opts = opts || {};
      return json(R.add + '.js', { items: items }).then(function(){ return refresh(); })
        .then(function(){ hop(); if (opts.open !== false) Bag.open(); })
        .catch(function(e){ Lucky.toast((e && (e.description || e.message)) || "That didn't go in the bag. Try again?"); throw e; });
    },
    change: function(key, qty){ return json(R.change + '.js', { id: key, quantity: qty }).then(function(c){ cart = c; paint(); emit(); }); },
    open: function(){ var cd = $('#cd'); if (!cd) { location.href = R.cart; return; } cd.hidden = false; paint(); upsell($('#cd-ups'), cart); var x = $('.cd-x', cd); if (x) x.focus({ preventScroll: true }); },
    close: function(){ var cd = $('#cd'); if (cd) cd.hidden = true; }
  };
  /* the offer flipped on or off while the page was open */
  document.addEventListener('lg:cs', function(){ paint(); emit(); });
  function hop(){ var b = $('.bagbtn'); if (!b) return; b.classList.remove('is-hop'); void b.offsetWidth; b.classList.add('is-hop'); }

  var hole = null;
  /* the bag shows the product's cut-out when it has one (a lifestyle photo got a grey frame round it) */
  var CUT = LG.cutouts || {};
  var VCUT = LG.vcutouts || {};
  function img(l){ if (VCUT[l.variant_id]) return VCUT[l.variant_id]; if (CUT[l.handle]) return CUT[l.handle]; return l.image ? l.image + (l.image.indexOf('?') > -1 ? '&' : '?') + 'width=200' : ''; }
  function paint(){
    var n = goods().reduce(function(a, l){ return a + l.quantity; }, 0);
    $$('.bagbtn .n').forEach(function(el){ el.textContent = n; el.setAttribute('data-n', n); });
    var list = $('#cd-list'); if (!list) return;
    var t = goodsTotal();
    if (!n){
      list.innerHTML = '<div class="cd-empty"><span class="lg-mags"><img class="is-ink" src="' + esc(Lucky.mags.ink) + '" alt=""><img class="is-light" src="' + esc(Lucky.mags.light) + '" alt=""></span>'
        + '<p class="lg-aside" style="margin:0 auto 18px">Nothing in here yet.</p>'
        + '<a class="lg-btn-line lg-btn-sm" href="' + esc(list.getAttribute('data-empty-url') || R.root) + '">See the clubs</a></div><div class="ups" id="cd-empty-ups" hidden></div>';
      emptyPicks($('#cd-empty-ups'));
    } else {
      list.innerHTML = cart.items.map(function(l){
        if (isCover(l)) return '<div class="cd-line cd-cover"><span class="ph"></span><span><b>' + esc(l.product_title) + '</b><span class="lg-hud"><span>Free returns and lost-package cover</span></span></span>'
          + '<span class="pr">' + money(l.final_line_price) + '<button type="button" class="rm" data-rm="' + esc(l.key) + '">Remove</button></span></div>';
        var opts = (l.options_with_values || []).filter(function(o){ return o.value !== 'Default Title'; }).map(function(o){ return o.value; });
        var props = l.properties ? Object.keys(l.properties).filter(function(k){ return k.charAt(0) !== '_' && l.properties[k]; }).map(function(k){ return l.properties[k]; }) : [];
        var hud = opts.concat(props);
        if (isGift(l)) return '<div class="cd-line is-gift"><a class="ph" href="' + esc(l.url) + '">' + (l.image ? '<img src="' + esc(img(l)) + '" alt="">' : '') + '</a><span><b>' + esc(l.product_title) + '</b>'
          + '<span class="lg-hud"><span class="gift-tag">Free gift</span>' + hud.map(function(h){ return '<span>' + esc(h) + '</span>'; }).join('') + '</span></span>'
          + '<span class="pr">' + (l.final_line_price ? money(l.final_line_price) : 'Free') + (l.original_line_price > l.final_line_price ? '<s>' + money(l.original_line_price) + '</s>' : '') + '</span></div>';
        return '<div class="cd-line"><a class="ph" href="' + esc(l.url) + '">' + (l.image ? '<img src="' + esc(img(l)) + '" alt="">' : '') + '</a><span><b>' + esc(l.product_title) + '</b>'
          + (hud.length ? '<span class="lg-hud">' + hud.map(function(h){ return '<span>' + esc(h) + '</span>'; }).join('') + '</span>' : '')
          + '<span class="cd-qty"><button type="button" data-qty="' + esc(l.key) + '" data-to="' + (l.quantity - 1) + '" aria-label="One fewer">&minus;</button><span>' + l.quantity + '</span><button type="button" data-qty="' + esc(l.key) + '" data-to="' + (l.quantity + 1) + '" aria-label="One more">+</button></span>'
          + (lowLine(l.variant_id) ? '<span class="low">' + esc(lowLine(l.variant_id)) + '</span>' : '')
          + (dealTags(l).length ? '<span class="deal">' + dealTags(l).map(esc).join(' · ') + '</span>' : '')
          + '</span><span class="pr">' + money(l.final_line_price) + (was(l) > l.final_line_price ? '<s>' + money(was(l)) + '</s>' : '')
          + '<button type="button" class="rm" data-rm="' + esc(l.key) + '">Remove</button></span></div>';
      }).join('');
    }
    var csb = $('#cd-cs'); if (csb){ var cl = csLine(cart); csb.innerHTML = cl; csb.hidden = !cl; }
    var rw = rewards(cart), say = $('#cd-say');
    if (say) say.innerHTML = rw.say;
    if (!hole && $('#cd-hole') && Lucky.hole) hole = Lucky.hole($('#cd-hole'), { stops: rw.stops });
    if (hole) hole.set(rw.t / 100);
    flagLabels($('#cd-hole'), rw);
    if ($('#cd') && !$('#cd').hidden) upsell($('#cd-ups'), cart);
    extras($('#cd-extra'), cart);
    var s = $('#cd-sub'); if (s) s.textContent = money(cart.total_price);
    var sv = $('#cd-save'), save = savings(cart), sm = BAG.saveMsg || "You're saving {amount}";
    if (sv){ sv.hidden = !save || BAG.saveOn === false; sv.innerHTML = save ? esc(sm).replace('{amount}', '<b>' + money(save) + '</b>') + (sm.indexOf('{amount}') < 0 ? ' <b>' + money(save) + '</b>' : '') : ''; }
    loadCompare(cart);
    var go = $('#cd-go'); if (go) go.setAttribute('aria-disabled', String(!n));
  }

  document.addEventListener('click', function(e){
    var t;
    if (t = e.target.closest('[data-cart-open]')){ e.preventDefault(); Bag.open(); return; }
    if (t = e.target.closest('[data-cart-close]')){ e.preventDefault(); Bag.close(); return; }
    if (t = e.target.closest('[data-rm]')){ Bag.change(t.getAttribute('data-rm'), 0); return; }
    if (t = e.target.closest('[data-qty]')){ Bag.change(t.getAttribute('data-qty'), Math.max(0, +t.getAttribute('data-to'))); return; }
    if ((t = e.target.closest('#cd-go')) && t.getAttribute('aria-disabled') === 'true'){ e.preventDefault(); return; }
  });

  /* any <form data-lg-add> (a buy box) adds through the bag instead of reloading */
  document.addEventListener('submit', function(e){
    var f = e.target.closest('form[data-lg-add]'); if (!f) return;
    e.preventDefault();
    var fd = new FormData(f), props = {};
    fd.forEach(function(v, k){ var m = k.match(/^properties\[(.+)\]$/); if (m && v) props[m[1]] = v; });
    var btn = $('[type=submit]', f); if (btn) btn.setAttribute('aria-busy', 'true');
    Bag.add([{ id: +fd.get('id'), quantity: +(fd.get('quantity') || 1), properties: props }])
      .catch(function(){}).then(function(){ if (btn) btn.removeAttribute('aria-busy'); });
  });

  /* ------------------------------------------------------------ the menus */
  document.addEventListener('click', function(e){
    var b = e.target.closest('.nv > button');
    if (!b && e.target.closest('.mega')) return;
    var hover = matchMedia('(hover:hover)').matches;
    $$('.nv').forEach(function(n){
      var open = b && n.contains(b) && (hover || !n.classList.contains('is-open'));
      n.classList.toggle('is-open', !!open); var bt = $('button', n); if (bt) bt.setAttribute('aria-expanded', String(!!open));
    });
    var bu = e.target.closest('.burger');
    if (bu){ var m = $('#mnav'), o = !m.classList.contains('is-open'); m.classList.toggle('is-open', o); bu.setAttribute('aria-expanded', String(o)); }
  });
  /* hover (desktop): open on enter, stay open while the cursor is on the button or the panel,
     close a beat after it leaves both, so crossing the gap never drops the menu */
  $$('.nv').forEach(function(n){
    var t = null, bt = $('button', n);
    function open(){ clearTimeout(t); $$('.nv').forEach(function(o){ if (o !== n){ o.classList.remove('is-open'); var b = $('button', o); if (b) b.setAttribute('aria-expanded', 'false'); } });
      n.classList.add('is-open'); if (bt) bt.setAttribute('aria-expanded', 'true'); }
    function shut(){ t = setTimeout(function(){ n.classList.remove('is-open'); if (bt) bt.setAttribute('aria-expanded', 'false'); }, 220); }
    n.addEventListener('mouseenter', function(){ if (matchMedia('(hover:hover)').matches) open(); });
    n.addEventListener('mouseleave', function(){ if (matchMedia('(hover:hover)').matches) shut(); });
  });

  /* ------------------------------------------------------------ modals */
  document.addEventListener('click', function(e){
    var o = e.target.closest('[data-md-open]');
    if (o){ e.preventDefault(); var m = document.getElementById(o.getAttribute('data-md-open')); if (m){ m.hidden = false; var x = $('.md-x', m); if (x) x.focus({ preventScroll: true }); } return; }
    var c = e.target.closest('[data-md-close]');
    if (c){ var md = c.closest('.md'); if (md){ md.hidden = true; $$('video', md).forEach(function(v){ v.pause(); }); } }
  });
  document.addEventListener('keydown', function(e){
    if (e.key !== 'Escape') return;
    $$('.md').forEach(function(m){ m.hidden = true; }); Bag.close();
    $$('.nv').forEach(function(n){ n.classList.remove('is-open'); });
  });

  /* zoom */
  document.addEventListener('click', function(e){
    var zoom = $('#zoom'); if (!zoom || !zoom.showModal) return;
    var t = e.target.closest('[data-zoom]');
    if (t){ var im = $('img', zoom); im.src = t.getAttribute('data-zoom'); im.alt = ($('img', t) || {}).alt || ''; zoom.showModal(); return; }
    if (e.target.closest('[data-zoom-close]') || e.target === zoom) zoom.close();
  });

  /* rails: [data-arrows="id or class"] with Previous / Next buttons; finder tabs [data-fp] */
  document.addEventListener('click', function(e){
    var a = e.target.closest('[data-arrows] button');
    if (a){ var box = a.closest('[data-arrows]').getAttribute('data-arrows'), r = document.getElementById(box) || $('.' + box);
      if (r && r.lgStep) { r.lgStep(a.getAttribute('aria-label') === 'Next' ? 1 : -1); return; }
      if (r) r.scrollBy({ left: (a.getAttribute('aria-label') === 'Next' ? 1 : -1) * r.clientWidth * .6, behavior: 'smooth' }); return; }
    var t = e.target.closest('[data-fp]');
    if (t){ var sc = t.closest('[data-finder]') || document;
      $$('[data-fp]', sc).forEach(function(x){ x.setAttribute('aria-pressed', String(x === t)); });
      $$('[data-panel]', sc).forEach(function(p){ p.hidden = p.getAttribute('data-panel') !== t.getAttribute('data-fp'); }); }
  });

  /* community rails [data-loop]: a second copy of the tiles makes the loop endless; it slides one
     tile every 5s (paused while you hover, touch or tab into it, or when it's off screen), and on a
     mouse a video tile plays while you hover it. */
  $$('.ugc[data-loop]').forEach(function(r){
    var tiles = $$('.wild', r); if (tiles.length < 4) return;
    tiles.forEach(function(t){ var c = t.cloneNode(true); c.setAttribute('aria-hidden', 'true'); c.tabIndex = -1; r.appendChild(c); });
    function span(){ var all = $$('.wild', r); return all[tiles.length].offsetLeft - all[0].offsetLeft; }
    function step1(){ var all = $$('.wild', r); return all[1].offsetLeft - all[0].offsetLeft; }
    function wrap(){ var W = span(); if (r.scrollLeft >= W - 2) r.scrollLeft -= W; }
    r.addEventListener('scroll', function(){ clearTimeout(r._w); r._w = setTimeout(wrap, 140); }, { passive: true });
    r.lgStep = function(d){
      var W = span(), st = step1();
      if (d < 0 && r.scrollLeft < st - 2) r.scrollLeft += W;
      r.scrollBy({ left: d * st, behavior: 'smooth' });
    };
    var held = false, seen = false, still = matchMedia('(prefers-reduced-motion: reduce)').matches;
    ['mouseenter', 'focusin', 'touchstart'].forEach(function(ev){ r.addEventListener(ev, function(){ held = true; }, { passive: true }); });
    ['mouseleave', 'focusout', 'touchend'].forEach(function(ev){ r.addEventListener(ev, function(){ held = false; }, { passive: true }); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function(es){ seen = es[0].isIntersecting; }).observe(r);
    if (!still) setInterval(function(){ if (seen && !held && !document.hidden && !$('.md-post:not([hidden])')) r.lgStep(1); }, 5000);
  });
  if (matchMedia('(hover: hover)').matches) {
    document.addEventListener('mouseover', function(e){
      var t = e.target.closest && e.target.closest('.wild[data-hv]'); if (!t || t.contains(e.relatedTarget)) return;
      var v = t.querySelector('video.wild-hv');
      if (!v) { v = document.createElement('video'); v.className = 'wild-hv'; v.muted = true; v.loop = true; v.playsInline = true;
        v.setAttribute('muted', ''); v.setAttribute('playsinline', ''); v.preload = 'none'; v.src = t.getAttribute('data-hv'); t.insertBefore(v, t.firstChild.nextSibling); }
      t.classList.add('is-hv'); var pr = v.play(); if (pr && pr.catch) pr.catch(function(){});
    });
    document.addEventListener('mouseout', function(e){
      var t = e.target.closest && e.target.closest('.wild[data-hv]'); if (!t || t.contains(e.relatedTarget)) return;
      t.classList.remove('is-hv'); var v = t.querySelector('video.wild-hv'); if (v) v.pause();
    });
  }

  /* sale prices on product pages: <s data-was> + a [price, compare-at] map per variant (snippets/lg-was),
     kept in step with whichever variant the page's form holds */
  $$('[data-was-map]').forEach(function(m){
    var map; try { map = JSON.parse(m.textContent); } catch (e) { return; }
    var s = m.parentElement.querySelector('[data-was]'), box = m.closest('section') || document, pr = s && s.parentElement.querySelector('[data-price]');
    if (!s) return;
    function upd(){
      var inp = box.querySelector('form[data-lg-add] [name="id"]') || box.querySelector('[name="id"]');
      var r = inp && map[inp.value]; if (!r) return;
      var on = r[1] > r[0]; s.hidden = !on; if (on) s.textContent = money(r[1]);
      var lw = s.parentElement.querySelector('[data-low]'); if (lw){ var t = lowLine(inp.value); lw.hidden = !t; lw.textContent = t; }
    }
    if (pr) new MutationObserver(upd).observe(pr, { childList: true, characterData: true, subtree: true });
    box.addEventListener('change', function(){ setTimeout(upd, 0); });
    box.addEventListener('click', function(){ setTimeout(upd, 0); });
    upd();
  });

  /* ------------------------------------------------------------ Klaviyo */
  var KL = LG.klaviyo, REV = '2024-10-15';
  function klaviyo(path, body){
    return fetch('https://a.klaviyo.com/client/' + path + '/?company_id=' + encodeURIComponent(KL), {
      method: 'POST', headers: { 'Content-Type': 'application/vnd.api+json', 'revision': REV }, body: JSON.stringify(body) })
      .then(function(r){ if (!r.ok && r.status !== 202) throw r; });
  }
  var okEmail = function(v){ return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v || ''); };
  /* the footer / blog signup: subscribes to the list set in theme settings */
  document.addEventListener('submit', function(e){
    var f = e.target.closest('[data-news]'); if (!f) return;
    e.preventDefault(); var i = $('input[type=email]', f);
    if (!okEmail(i.value)){ i.focus(); return; }
    var list = f.getAttribute('data-list') || LG.klaviyoList;
    var done = function(){ f.outerHTML = '<p class="lg-aside" style="margin:0">Done. You&rsquo;re on the list.</p>'; };
    if (!KL || !list){ done(); return; }
    klaviyo('subscriptions', { data: { type: 'subscription', attributes: { custom_source: f.getAttribute('data-source') || 'Website',
      profile: { data: { type: 'profile', attributes: { email: i.value } } } }, relationships: { list: { data: { type: 'list', id: list } } } } })
      .then(done).catch(function(){ Lucky.toast("That didn't go through. Try again?"); });
  });
  /* back in stock: <form data-notify data-variant="123"> */
  document.addEventListener('submit', function(e){
    var f = e.target.closest('[data-notify]'); if (!f || e.defaultPrevented) return;
    e.preventDefault(); var i = $('input[type=email]', f);
    if (!okEmail(i.value)){ i.focus(); return; }
    var v = f.getAttribute('data-variant');
    var done = function(){ f.outerHTML = '<p class="lg-aside" style="margin:0">Done. You&rsquo;ll get one email when it&rsquo;s back.</p>'; };
    if (!KL || !v){ done(); return; }
    klaviyo('back-in-stock-subscriptions', { data: { type: 'back-in-stock-subscription', attributes: { channels: ['EMAIL'],
      profile: { data: { type: 'profile', attributes: { email: i.value } } } },
      relationships: { variant: { data: { type: 'catalog-variant', id: '$shopify:::$default:::' + v } } } } })
      .then(done).catch(function(){ Lucky.toast("That didn't go through. Try again?"); });
  });


  /* ------------------------------------------------------------ community posts (shoppable) */
  function openPost(sec, i){
    var tpls = $$('template[data-post-tpl]', sec); if (!tpls.length) return;
    i = (i + tpls.length) % tpls.length;
    var md = $('.md-post', sec), body = $('.pm-body', md);
    body.innerHTML = ''; body.appendChild(tpls[i].content.cloneNode(true));
    md.setAttribute('data-i', i); md.hidden = false;
    /* phones: no browser control bar on the reel, tap to pause, one button for sound (2026-10-08) */
    var v = $('video', body);
    if (v){ v.setAttribute('playsinline', ''); v.playsInline = true;
      if (window.matchMedia('(max-width:749px)').matches){ v.controls = false;
        var snd = document.createElement('button'); snd.type = 'button'; snd.className = 'pm-snd'; snd.textContent = 'Sound on';
        snd.addEventListener('click', function(){ v.muted = !v.muted; snd.textContent = v.muted ? 'Sound on' : 'Sound off'; });
        v.addEventListener('click', function(){ if (v.paused) v.play(); else v.pause(); });
        v.parentNode.appendChild(snd); }
      var pl = v.play(); if (pl && pl.catch) pl.catch(function(){}); }
    var x = $('.md-x', md); if (x) x.focus({ preventScroll: true });
  }
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-post]');
    if (t){ openPost(t.closest('[data-posts]'), +t.getAttribute('data-post')); return; }
    var st = e.target.closest('[data-post-step]');
    if (st){ var md = st.closest('.md-post'); openPost(md.closest('[data-posts]'), +md.getAttribute('data-i') + (+st.getAttribute('data-post-step'))); }
  });
  /* #menu-2 opens that menu on load (for screenshots and reviews) */
  (function(){ var m = location.hash.match(/^#menu-(\d+)$/); if (!m) return; var n = $$('.nv')[+m[1] - 1]; if (n) n.classList.add('is-open'); })();
  /* a link to #post-3 opens that post on load (shareable, and how screenshots reach it) */
  (function(){ var m = location.hash.match(/^#post-(\d+)$/); if (!m) return; var sec = $('[data-posts]'); if (sec) openPost(sec, +m[1] - 1); })();
  /* adding from a post closes the post, so the bag opens on top */
  document.addEventListener('submit', function(e){
    var md = e.target.closest('.md-post'); if (md && e.target.matches('form[data-lg-add]')) setTimeout(function(){ md.hidden = true; }, 0);
  }, true);
  document.addEventListener('keydown', function(e){
    var md = $$('.md-post').filter(function(m){ return !m.hidden; })[0]; if (!md) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') openPost(md.closest('[data-posts]'), +md.getAttribute('data-i') + (e.key === 'ArrowRight' ? 1 : -1));
  });


  /* the header slides away scrolling down, back scrolling up; never while a menu is open */
  (function(){
    var h = $('.lg-hdr'); if (!h) return; var last = scrollY, raf = null;
    window.addEventListener('scroll', function(){
      if (raf) return; raf = requestAnimationFrame(function(){ raf = null;
        var y = scrollY, open = $('.nv.is-open') || ($('#mnav') && $('#mnav').classList.contains('is-open'));
        if (!open && y > 160 && y > last + 4) h.classList.add('is-away');
        else if (y < last - 4 || y < 160) h.classList.remove('is-away');
        document.documentElement.classList.toggle('lg-hdr-away', h.classList.contains('is-away'));
        last = y; });
    }, { passive: true });
  })();

  window.LuckySite = { setSticky: function(){} };
  refresh();
})();

/* Hat + gear galleries on phones (2026-10-08): the thumbnails ARE the gallery, one full-width photo
   per swipe, with a "3 / 12" count. */
(function(){
  document.querySelectorAll('[data-swipe]').forEach(function(row){
    var n = row.children.length; if (n < 2) return;
    var c = document.createElement('p'); c.className = 'swipe-n'; c.setAttribute('aria-hidden', 'true');
    row.parentNode.insertBefore(c, row.nextSibling);
    var set = function(){ var i = Math.round(row.scrollLeft / Math.max(1, row.clientWidth)); c.textContent = (i + 1) + ' / ' + n; };
    row.addEventListener('scroll', set, { passive: true }); set();
  });
})();
