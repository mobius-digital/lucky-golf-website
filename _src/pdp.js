/* ==========================================================================
   PDP — behavior shared by all three product templates
   Gallery, the N-axis buy box, accordions, the cross-sell rails and the
   review widget. The club, apparel and gear templates each add only what is
   genuinely theirs; everything here would otherwise be copied three ways and
   drift. Loaded before page-<template>.js, which may use LG_PDP.
   ========================================================================== */
/* The product record, injected by tools/build.py from _src/data/products.json,
   which tools/normalize-products.py derives from a Shopify pull. Every price,
   SKU, option axis and availability flag below is live store state — none of
   it is typed by hand, so re-pulling the catalogue updates the page. */
var PD = {{PRODUCT_JSON}};

/* How each axis presents itself. This is page furniture, not catalogue data,
   so it stays here rather than in products.json: `val` echoes the choice back
   beside the label, `help` hangs a link off the right of the label row. */
var PD_AXIS_UI = {
  hand:     {val: true},
  loft:     {help: {href: '#loft', text: 'Not sure? →'}},
  /* the combined Loft & grind axis — 50K, 52K, 52S. The help link goes to
     the grind explainer, because the grind is the half of this choice
     nobody arrives knowing. */
  loftgrind:{help: {href: '#grinds', text: 'Which grind? →'}},
  /* the size guide is a MODAL now, not a section on the page (Cole
     2026-07-31), so this opens it rather than jumping down the page */
  size:     {help: {md: 'md-size', text: 'Size guide →'}},
  gripsize: {val: true}
};



/* Reviews for THIS product, from _src/data/reviews/<id>.json. Verbatim
   Judge.me, spanning every rating so the star filter and the histogram agree.
   The curated 4-star-and-up rule governs the pull quotes, not this widget —
   a widget that hides its 1-stars is a widget nobody believes. */
var PD_REVIEWS = {{REVIEWS_JSON}};

/* The browse rail under the fold. Rows are product ids in the copy file;
   build.py resolves each to live price, rating and stock so a sold-out
   neighbor says so without anyone remembering to update this page. */
var PD_OAV = {{OAV_JSON}};

/* Highlight-reel briefs from the copy file. No footage exists, so each card
   is a labelled slot describing the clip that belongs there. */
var PD_REEL = {{REEL_JSON}};

/* Cart cross-sell, from the copy file. Read by core's paintUpsell(); rows
   already in the bag are filtered out there. */
var LG_CART_UPSELL = {{UPSELL_JSON}};

/* Finish-the-look cross-sell: polos and hats only. Cole's call — gear is a
   grab-bag, apparel completes the look and is the same voice as the club. */
var PD_KIT = [
  {sku:'LGA-CP-Contour', nm:'Contour Classic Polo', pr:'$67', sizes:'{{link:p/polo-contour}}',
   why:'Classic collar, tailored fit, UPF 50+.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/TopographyStyle1.webp?v=1779472755'},
  {sku:'LGA-BP-Blackout', nm:'Blackout Blade Polo', pr:'$67', sizes:'{{link:p/polo-blackout}}',
   why:'Blade collar, no buttons. Quieter than it sounds.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/StrokePlay1.webp?v=1779472570'},
  {sku:'HAT-5P-SB-IBTBL-BL', nm:'It’s Better To Be Lucky Hat', pr:'$29',
   why:'Five-panel, snapback, the line on the front.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/39.webp?v=1784585347'},
  {sku:'HAT-5P-SB-CRSV-BBLU-MONO', nm:'Baby Blue Cursive Hat', pr:'$29',
   why:'Monochrome script. Goes with the gold.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/30_203d7c7f-8680-4d32-bf41-18d0d4877086.webp?v=1784585347'}
];

(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var STAR = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>';
  var STAR_OFF = '<svg viewBox="0 0 24 24" class="off"><use href="#star"/></svg>';
  function starRow(n){
    var o = ''; for (var i = 1; i <= 5; i++) o += (i <= n ? STAR : STAR_OFF); return o;
  }
  function fmtDate(iso){
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p = iso.split('-'); return p[2].replace(/^0/,'') + ' ' + m[+p[1]-1] + ' ' + p[0];
  }

  /* ---------------------------------------------------------------- gallery */
  var gal = $('#gal');
  if (gal){
    var slides = [].slice.call(gal.querySelectorAll('.gal-slide'));
    var thumbs = $('.gal-thumbs');
    var at = 0;
    slides.forEach(function(s, i){
      var src = s.querySelector('img').getAttribute('src');
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'gal-th';
      b.setAttribute('aria-current', i === 0 ? 'true' : 'false');
      b.setAttribute('aria-label', 'Image ' + (i + 1) + ' of ' + slides.length);
      b.innerHTML = '<img src="' + src + '" alt="" loading="lazy">';
      b.addEventListener('click', function(){ show(i); });
      thumbs.appendChild(b);
    });
    var ths = [].slice.call(thumbs.children);
    function show(i){
      at = (i + slides.length) % slides.length;
      slides.forEach(function(s, n){
        if (n === at) s.setAttribute('data-on', ''); else s.removeAttribute('data-on'); });
      ths.forEach(function(t, n){ t.setAttribute('aria-current', String(n === at)); });
      $('#gal-i').textContent = at + 1;
    }
    $('[data-p]', gal).addEventListener('click', function(){ show(at - 1); });
    $('[data-n]', gal).addEventListener('click', function(){ show(at + 1); });
    gal.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft'){ e.preventDefault(); show(at - 1); }
      if (e.key === 'ArrowRight'){ e.preventDefault(); show(at + 1); }
    });
  }

  /* ====================================================== variant selection
     N axes, driven entirely by PD.options and PD.variants. The store needs
     0, 1 and 2 axes today (GAMEPLAN 2a) and a third when the KBS shaft
     upgrade lands, so nothing below knows what "hand" or "loft" mean.

     Two things the old two-axis version got away with and this cannot:

     * Availability is `avail`, never `qty > 0`. Shopify oversells some lines
       (the glove ships at qty -3) and holds others at qty 0 while still
       selling them. Quantity is no longer surfaced at all — the stock line
       says when it ships and nothing more (Cole, 2026-07-31).
     * Price is per variant. Grips run $9.95 / $11.95 / $14.95 across
       Standard / Midsize / Jumbo, so the price repaints on selection.
     ======================================================================= */

  /* The rules themselves live in _src/variants.js — no DOM, no page state, so
     tools/test-variants.js can run them over all 44 products instead of only
     the two-axis one this page renders. */
  var V = LG_VARIANTS;
  var AXES = PD.options || [];
  var sel = V.selectionFor(PD);        /* one value key per axis; [''] if none */

  function variant(){ return V.variantFor(PD, sel); }
  function offered(i, val){ return V.offered(PD, sel, i, val); }
  function chosenLabels(){ return V.labels(PD, sel); }
  function labelOf(i){ return chosenLabels()[i] || ''; }

  var proxy = document.createElement('button');   /* lets core's [data-add]
    delegate do the actual cart work, so quantity is just N clicks and there
    is one add-to-cart code path on the whole site */
  proxy.type = 'button'; proxy.setAttribute('data-add', ''); proxy.hidden = true;
  proxy.setAttribute('aria-hidden', 'true'); proxy.tabIndex = -1;
  document.body.appendChild(proxy);

  function paintPickers(){
    var host = $('#pickers'); if (!host) return;
    var out = '', i, n;
    for (i = 0; i < AXES.length; i++){
      var ax = AXES[i], ui = PD_AXIS_UI[ax.key] || {};
      out += '<div class="opt"><div class="opt-hd"><span class="lbl">' + esc(ax.name) + '</span>';
      /* {{link:none}} rather than a literal hash: a modal trigger is a real
         anchor that genuinely goes nowhere, and saying so out loud is what
         keeps a bare hash a build error everywhere else (HANDOFF §10a). */
      if (ui.help) out += ui.help.md
        ? '<a class="help" href="{{link:none}}" data-md-open="' + esc(ui.help.md) + '">'
          + esc(ui.help.text) + '</a>'
        : '<a class="help" href="' + esc(ui.help.href) + '">' + esc(ui.help.text) + '</a>';
      else if (ui.val) out += '<span class="val">' + esc(labelOf(i)) + '</span>';
      out += '</div><div class="chips" role="group" aria-label="' + esc(ax.name) + '">';
      for (n = 0; n < ax.values.length; n++){
        var v = ax.values[n], dead = !offered(i, v.k);
        out += '<button class="chip" type="button"'
          + ' aria-pressed="' + (v.k === sel[i] ? 'true' : 'false') + '"'
          + (dead ? ' disabled aria-label="' + esc(v.label) + ', out of stock"' : '')
          + ' data-axis="' + i + '" data-val="' + esc(v.k) + '">' + esc(v.label) + '</button>';
      }
      out += '</div>';
      /* No SKU printed here. Cole 2026-07-31: no SKU is shown anywhere on a
         PDP. It is still carried on every variant for the cart, and it is
         still never synthesised — it just does not render. */
      out += '</div>';
    }
    host.innerHTML = out;
  }

  function sync(){
    var v = variant() || {sku: '', price: PD.price, avail: false, qty: 0};
    var labels = chosenLabels();
    var variantLabel = labels.join(' · ');
    var money = '$' + v.price;

    if ($('#bx-amt')) $('#bx-amt').textContent = money;
    if ($('#atc-bar-v')) $('#atc-bar-v').textContent = variantLabel || PD.title;

    var stock = $('#stock'), st = $('#stock-t');
    if (stock && st){
      if (!v.avail){
        stock.setAttribute('data-out', '');
        st.textContent = labels.length
          ? 'Out of stock in ' + labels.join(' ').toLowerCase()
          : 'Out of stock';
      } else {
        stock.removeAttribute('data-out');
        /* qty can be zero or negative on a sellable variant — that is a
           backorder, not low stock, so only a real positive count qualifies */
        /* The stock line says WHEN it ships and nothing else. It used to
           publish the exact unit count on anything under 25, which is inventory
           data a shopper has no use for and we have no reason to broadcast. */
        st.textContent = 'In stock — ships in 1–2 business days';
      }
    }
    [['#atc', 'Add to cart · ' + money], ['#atc2', 'Add to cart']].forEach(function(p){
      var b = $(p[0]); if (!b) return;
      b.disabled = !v.avail;
      var s = b.querySelector('span'); if (s) s.textContent = v.avail ? p[1] : 'Out of stock';
    });
    proxy.setAttribute('data-sku', v.sku);
    proxy.setAttribute('data-name', PD.name + (labels.length ? ' ' + labels[labels.length - 1] : ''));
    proxy.setAttribute('data-price', money);
    proxy.setAttribute('data-img', PD.img);
    proxy.setAttribute('data-variant', variantLabel);
  }

  document.addEventListener('click', function(e){
    var c = e.target.closest('[data-axis]');
    if (!c || c.disabled) return;
    var i = +c.getAttribute('data-axis');
    sel[i] = c.getAttribute('data-val');
    V.reconcile(PD, sel, i);
    paintPickers(); sync();
  });

  var qty = $('#qty');
  document.addEventListener('click', function(e){
    var q = e.target.closest('[data-q]');
    if (q && qty){
      qty.value = Math.max(1, Math.min(9, (+qty.value || 1) + (+q.getAttribute('data-q'))));
    }
  });
  ['#atc', '#atc2'].forEach(function(sel){
    var b = $(sel); if (!b) return;
    b.addEventListener('click', function(){
      if (b.disabled) return;
      var n = (sel === '#atc' && qty) ? Math.max(1, Math.min(9, +qty.value || 1)) : 1;
      for (var i = 0; i < n; i++) proxy.click();
      var s = b.querySelector('span'), was = s.textContent;
      s.textContent = 'Added'; setTimeout(function(){ s.textContent = was; }, 1400);
    });
  });
  paintPickers(); sync();

  /* ------------------------------------------------------------ accordions */
  [].forEach.call(document.querySelectorAll('.acc-hd'), function(h){
    h.addEventListener('click', function(){
      var open = h.getAttribute('aria-expanded') === 'true';
      h.setAttribute('aria-expanded', String(!open));
      var body = document.getElementById(h.getAttribute('aria-controls'));
      if (body) body.hidden = open;
    });
  });

  /* ------------------------------------------------- others also viewed */
  var oav = $('#oav');
  if (oav) oav.innerHTML = PD_OAV.map(function(o){
    return '<article class="oav-i">'
      + '<div class="oav-ph">'
      /* an empty tag used to render as a small black square on every card
         without a callout — no tag, no element */
      +   (o.tag ? '<span class="oav-tag"' + (o.out ? ' data-out' : '') + '>'
                   + esc(o.tag) + '</span>' : '')
      +   '<img src="' + o.img + '" alt="' + esc(o.nm) + '" loading="lazy" width="600" height="600">'
      + '</div>'
      + '<div class="oav-bd"><a class="oav-nm stretch" href="' + o.href + '">' + esc(o.nm) + '</a>'
      +   '<div class="oav-meta"><span class="oav-pr">' + esc(o.pr) + '</span>'
      +   '<span class="oav-rt">' + esc(o.rt) + '</span></div></div>'
      + '</article>';
  }).join('');

  /* ------------------------------------------------- finish the setup */
  var kit = $('#kit');
  if (kit) kit.innerHTML = PD_KIT.map(function(o){
    return '<article class="kit-i">'
      + '<div class="kit-ph"><img src="' + o.img + '" alt="' + esc(o.nm) + '" loading="lazy" width="600" height="600"></div>'
      + '<div class="kit-bd"><span class="kit-nm">' + esc(o.nm) + '</span>'
      +   '<span class="kit-why">' + esc(o.why) + '</span>'
      +   '<div class="kit-bot"><span class="kit-pr">' + esc(o.pr) + '</span>'
      +   (o.sizes
          /* sized product: there is nothing sensible to add without a size,
             so it links to its own page instead of pretending to be one-click */
          ? '<a class="btn btn-line btn-sm" href="' + o.sizes + '"><span>Choose size</span>'
            + '<span class="ar">&rarr;</span></a>'
          : '<button class="btn btn-ink btn-sm" type="button" data-add data-sku="' + esc(o.sku)
            + '" data-name="' + esc(o.nm) + '" data-price="' + esc(o.pr) + '" data-img="' + o.img
            + '" data-variant=""><span>Add</span></button>')
      +   '</div></div>'
      + '</article>';
  }).join('');

  /* =====================================================================
     REVIEWS — Judge.me shape. The histogram is the real 551-review
     distribution; the list is a 47-review sample that preserves that
     distribution, so filtering by star rating returns a believable set.
     ===================================================================== */
  var JM_TOTALS = PD_REVIEWS.totals, JM_TOTAL = PD_REVIEWS.total, JM_PAGE = 6;
  var jmFilter = 0, jmSort = 'recent', jmShown = JM_PAGE;

  function jmPool(){
    var list = PD_REVIEWS.sample.filter(function(r){ return !jmFilter || r.r === jmFilter; });
    list = list.slice();
    if (jmSort === 'high') list.sort(function(a,b){ return b.r - a.r || (a.d < b.d ? 1 : -1); });
    else if (jmSort === 'low') list.sort(function(a,b){ return a.r - b.r || (a.d < b.d ? 1 : -1); });
    else list.sort(function(a,b){ return a.d < b.d ? 1 : a.d > b.d ? -1 : 0; });
    return list;
  }
  function paintBars(){
    var box = $('#jm-bars'); if (!box) return;
    box.innerHTML = [5,4,3,2,1].map(function(k){
      var pct = Math.round(JM_TOTALS[k] / JM_TOTAL * 100);
      return '<button class="row" type="button" data-star="' + k + '"'
        + ' aria-label="Show only ' + k + ' star reviews">'
        + '<span class="k">' + k + ' ★</span>'
        + '<span class="t"><i style="width:' + Math.max(pct, 1) + '%"></i></span>'
        + '<span class="v">' + JM_TOTALS[k] + '</span></button>';
    }).join('');
  }
  function paintFilters(){
    var box = $('#jm-filters'); if (!box) return;
    var opts = [[0, 'All']].concat([5,4,3,2,1].map(function(k){ return [k, k + ' ★']; }));
    box.innerHTML = opts.map(function(o){
      return '<button class="jm-f" type="button" data-star="' + o[0] + '"'
        + ' aria-pressed="' + (jmFilter === o[0]) + '">' + o[1] + '</button>';
    }).join('');
  }
  function paintList(){
    var box = $('#jm-list'), more = $('#jm-more'), cnt = $('#jm-count');
    if (!box) return;
    var pool = jmPool();
    if (!pool.length){
      box.innerHTML = '<p class="jm-empty">No reviews at that rating in this sample.</p>';
      if (more) more.hidden = true;
      if (cnt) cnt.textContent = '';
      return;
    }
    box.innerHTML = pool.slice(0, jmShown).map(function(r){
      return '<article class="jr">'
        + '<div class="jr-top">'
        +   '<span class="jr-av" aria-hidden="true">' + esc(r.n.charAt(0).toUpperCase()) + '</span>'
        +   '<span class="jr-who"><b>' + esc(r.n) + '</b>'
        +     '<span>' + (r.v ? 'Verified buyer · ' : '') + fmtDate(r.d) + '</span></span>'
        +   '<span class="jr-stars" role="img" aria-label="' + r.r + ' out of 5">' + starRow(r.r) + '</span>'
        + '</div>'
        + (r.t ? '<h4>' + esc(r.t) + '</h4>' : '')
        + '<p>' + esc(r.q) + '</p>'
        + '</article>';
    }).join('');
    if (more) more.hidden = jmShown >= pool.length;
    if (cnt){
      var scale = jmFilter ? JM_TOTALS[jmFilter] : JM_TOTAL;
      cnt.textContent = 'Showing ' + Math.min(jmShown, pool.length) + ' of ' + pool.length
        + ' in this sample · ' + scale + ' live'
        + (jmFilter ? ' at ' + jmFilter + ' star' : '');
    }
  }
  function jmSetFilter(star){
    jmFilter = star; jmShown = JM_PAGE;
    paintFilters(); paintList();
    var sec = $('#reviews'); if (sec) sec.scrollIntoView({block:'nearest'});
  }
  document.addEventListener('click', function(e){
    var f = e.target.closest('.jm-f'), b = e.target.closest('.jm-bars .row');
    if (f){ jmSetFilter(+f.getAttribute('data-star')); return; }
    if (b){ jmSetFilter(+b.getAttribute('data-star')); return; }
    if (e.target.closest('#jm-more')){ jmShown += JM_PAGE; paintList(); }
  });
  var sortSel = $('#jm-sort');
  if (sortSel) sortSel.addEventListener('change', function(){
    jmSort = sortSel.value; jmShown = JM_PAGE; paintList();
  });
  paintBars(); paintFilters(); paintList();
})();
