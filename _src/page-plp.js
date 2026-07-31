/* ==========================================================================
   COLLECTION / PLP
   One script, seven pages. Everything it renders comes from the collection
   record injected by tools/build.py — the tiles, the facet chips and the
   sort options are all derived, so adding a product to products.json puts it
   on the right page with no edit here.
   ========================================================================== */
var PLP = {{COLLECTION_JSON}};

(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };

  var grid = $('#plp-grid');
  if (!grid) return;

  var items = PLP.products || [];
  var facetOn = null;          /* family key, or null for everything */
  var stockOnly = false;
  var sort = 'featured';

  /* ------------------------------------------------------------- controls */
  function paintFacets(){
    var box = $('#plp-facets');
    if (!box) return;
    /* one family means one chip, which filters nothing — leave the row empty
       and the stylesheet collapses it */
    if (!PLP.facets || PLP.facets.length < 2){ box.innerHTML = ''; return; }
    var out = '<button class="chip" type="button" data-facet="" aria-pressed="'
      + (facetOn === null) + '">All</button>';
    for (var i = 0; i < PLP.facets.length; i++){
      var f = PLP.facets[i];
      out += '<button class="chip" type="button" data-facet="' + esc(f.k) + '"'
        + ' aria-pressed="' + (facetOn === f.k) + '">' + esc(f.label) + '</button>';
    }
    box.innerHTML = out;
  }

  /* "Best reviewed" is only honest where reviews exist. Clubs have Judge.me
     ratings; nothing in apparel or gear does yet, so the option is removed
     rather than left to sort by a field that is null for every row. */
  function trimSort(){
    var sel = $('#plp-sort');
    if (!sel) return;
    if (!items.some(function(p){ return p.rating; })){
      var opt = sel.querySelector('[value="rated"]');
      if (opt) opt.parentNode.removeChild(opt);
    }
  }

  /* ------------------------------------------------------------ selection */
  function visible(){
    var list = items.filter(function(p){
      if (facetOn && p.family !== facetOn) return false;
      if (stockOnly && !p.inStock) return false;
      return true;
    });
    /* Sold-out products sink to the bottom of every ordering. They are still
       worth showing — a collection that hides them looks thinner than the
       range actually is — but nothing sold out should lead a grid. */
    var by = {
      'price-asc':  function(a, b){ return a.price - b.price; },
      'price-desc': function(a, b){ return b.price - a.price; },
      'name':       function(a, b){ return a.title < b.title ? -1 : a.title > b.title ? 1 : 0; },
      'rated':      function(a, b){
                      return (b.rating ? b.rating.avg : -1) - (a.rating ? a.rating.avg : -1); },
      'featured':   function(){ return 0; }
    }[sort] || function(){ return 0; };

    return list.map(function(p, i){ return [p, i]; })
      .sort(function(x, y){
        if (x[0].inStock !== y[0].inStock) return x[0].inStock ? -1 : 1;
        return by(x[0], y[0]) || x[1] - y[1];    /* stable: fall back to input order */
      })
      .map(function(pair){ return pair[0]; });
  }

  /* ---------------------------------------------------------------- paint */
  function stars(r){
    var pct = (r.avg / 5 * 100).toFixed(1);
    var five = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>';
    five = five + five + five + five + five;
    return '<span class="stars" style="--pct:' + pct + '%" role="img"'
      + ' aria-label="' + r.avg + ' out of 5, ' + r.count + ' reviews">'
      + '<span class="s-bg">' + five + '</span><span class="s-fg">' + five + '</span></span>';
  }

  /* No review count on a product card, ever (Cole, 2026-07-31). The variant
     summary carries this slot instead — it answers a question the shopper
     actually has while browsing. */
  function tile(p){
    var out = !p.inStock;
    return '<article class="ptile rv"' + (out ? ' data-out' : '') + '>'
      + '<div class="pt-ph">'
      + (p.img
          ? '<img src="' + esc(p.img) + '" alt="' + esc(p.title) + '" loading="lazy"'
            + ' width="800" height="800" decoding="async">'
          /* Lucky Golf Tees is the one product with no photo in Shopify at all,
             so it gets a labelled slot rather than a broken image */
          : '<div class="ph"><span class="lbl"><span class="mono k">Photo needed</span>'
            + '<span class="mono">' + esc(p.title) + '</span></span></div>')
      + (out ? '<span class="pt-tag">Sold out</span>' : '')
      + '</div>'
      + '<span class="pt-sku">' + esc(p.code) + '</span>'
      + '<a class="stretch" href="' + esc(p.href) + '"><span class="pt-nm">'
        + esc(p.name) + '</span></a>'
      + (p.summary ? '<p class="pt-sum">' + esc(p.summary) + '</p>' : '')
      + '<span class="pt-meta"><span class="pt-pr">' + esc(p.priceLabel) + '</span></span>'
      /* Quick add. A product with exactly one sellable variant can go straight
         in the bag; anything with a choice to make cannot, so it links to its
         own page instead of pretending to be one-click. Same rule as the PDP
         cross-sell tiles. */
      + '<div class="pt-add">'
      + (out
          ? '<span class="pt-out">Sold out</span>'
          : p.addSku
            ? '<button class="btn btn-ink btn-sm" type="button" data-add'
              + ' data-sku="' + esc(p.addSku) + '" data-name="' + esc(p.name) + '"'
              + ' data-price="' + esc(p.priceLabel) + '" data-img="' + esc(p.img || '') + '"'
              + ' data-variant=""><span>Add</span></button>'
            : '<a class="btn btn-line btn-sm" href="' + esc(p.href) + '"><span>'
              + esc(p.chooseLabel || 'Choose options') + '</span><span class="ar">&rarr;</span></a>')
      + '</div>'
      + '</article>';
  }

  function paint(){
    var list = visible();
    grid.innerHTML = list.map(tile).join('');
    grid.hidden = !list.length;
    var empty = $('#plp-empty');
    if (empty) empty.hidden = !!list.length;

    var count = $('#plp-count');
    if (count){
      var total = items.length;
      count.textContent = list.length === total
        ? total + (total === 1 ? ' product' : ' products')
        : list.length + ' of ' + total + (total === 1 ? ' product' : ' products');
    }
    /* core.js reveals .rv on scroll; tiles painted after that pass would stay
       invisible, so they are marked shown as they are created */
    [].forEach.call(grid.querySelectorAll('.rv'), function(el){ el.classList.add('in'); });
  }

  /* --------------------------------------------------------------- events */
  document.addEventListener('click', function(e){
    var f = e.target.closest('[data-facet]');
    if (f){
      facetOn = f.getAttribute('data-facet') || null;
      paintFacets(); paint();
      return;
    }
    if (e.target.closest('#plp-instock')){
      stockOnly = !stockOnly;
      $('#plp-instock').setAttribute('aria-pressed', String(stockOnly));
      paint();
      return;
    }
    if (e.target.closest('#plp-clear')){
      facetOn = null; stockOnly = false;
      $('#plp-instock').setAttribute('aria-pressed', 'false');
      paintFacets(); paint();
    }
  });

  var sortSel = $('#plp-sort');
  if (sortSel) sortSel.addEventListener('change', function(){ sort = sortSel.value; paint(); });

  /* you are already here — the current collection is not a place to go next */
  var here = $('#plp-sibs [data-c="' + PLP.id + '"]');
  if (here) here.parentNode.removeChild(here);

  trimSort();
  paintFacets();
  paint();
})();
