/* ==========================================================================
   THE REVIEW WIDGET — one implementation, two pages.

   It was inside pdp.js, which only product pages load. `32-reviews.html` needs
   the same histogram, the same star filter, the same sort and the same
   pagination over the union of every pull — and a second implementation of
   "which reviews am I showing" is the last thing this site needs (the same
   argument that put the quick-add picker on LG_VARIANTS rather than on its own
   availability rules, §21a).

   So: mount it on a root element and hand it data. The PDP mounts one product;
   the reviews page mounts all of them and adds a product filter.

   `data` is the shape of _src/data/reviews/<id>.json:
     { total, totals:{5..1}, sample:[ {n,r,t,d,q,v,rep} ] }
   plus, on the reviews page only, `p` and `pn` per review (product id and
   name) and a `products` list for the filter chips.

   The 4-star-and-up rule governs curated pull quotes, NOT this widget. A
   widget that hides its 1-stars is a widget nobody believes (HANDOFF §9).
   ========================================================================== */
var LG_REVIEWS = (function(){
  var STAR = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>';
  var STAR_OFF = '<svg viewBox="0 0 24 24" class="off"><use href="#star"/></svg>';

  function esc(s){
    return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; });
  }
  function starRow(n){
    var o = ''; for (var i = 1; i <= 5; i++) o += (i <= n ? STAR : STAR_OFF); return o;
  }
  function fmtDate(iso){
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p = iso.split('-'); return p[2].replace(/^0/,'') + ' ' + m[+p[1]-1] + ' ' + p[0];
  }

  function mount(root, data, opts){
    if (!root || !data) return null;
    opts = opts || {};
    var PAGE = opts.page || 6;
    var $ = function(s){ return root.querySelector(s); };

    var star = 0, sort = 'recent', shown = PAGE, prod = '';

    /* Every review currently in scope: the product filter narrows first, the
       star filter second, so the histogram can redraw for one product. */
    function scoped(){
      return prod ? data.sample.filter(function(r){ return r.p === prod; }) : data.sample;
    }
    /* Live totals for whatever is in scope. On the PDP that is always the
       product's own real histogram; on the reviews page a product filter
       swaps to that product's, which is the only honest thing to draw —
       summing sampled reviews would report a distribution nobody publishes. */
    function totals(){
      if (!prod) return data.totals;
      var p = (data.products || []).filter(function(x){ return x.id === prod; })[0];
      return (p && p.totals) || data.totals;
    }
    function scopedTotal(){
      if (!prod) return data.total;
      var p = (data.products || []).filter(function(x){ return x.id === prod; })[0];
      return (p && p.total) || data.total;
    }

    function pool(){
      var list = scoped().filter(function(r){ return !star || r.r === star; }).slice();
      if (sort === 'high') list.sort(function(a,b){ return b.r - a.r || (a.d < b.d ? 1 : -1); });
      else if (sort === 'low') list.sort(function(a,b){ return a.r - b.r || (a.d < b.d ? 1 : -1); });
      else list.sort(function(a,b){ return a.d < b.d ? 1 : a.d > b.d ? -1 : 0; });
      return list;
    }

    function paintScore(){
      var t = totals(), n = scopedTotal(), box = $('#jm-avg'), cnt = $('#jm-cnt');
      if (!box && !cnt) return;
      var sum = 0, all = 0;
      [5,4,3,2,1].forEach(function(k){ sum += k * (t[k] || 0); all += (t[k] || 0); });
      if (box) box.textContent = all ? (Math.round(sum / all * 100) / 100).toFixed(2) : '—';
      if (cnt) cnt.textContent = 'Based on ' + n + ' reviews';
    }
    function paintBars(){
      var box = $('#jm-bars'); if (!box) return;
      var t = totals(), n = scopedTotal();
      box.innerHTML = [5,4,3,2,1].map(function(k){
        var pct = n ? Math.round((t[k] || 0) / n * 100) : 0;
        return '<button class="row" type="button" data-star="' + k + '"'
          + ' aria-label="Show only ' + k + ' star reviews">'
          + '<span class="k">' + k + ' ★</span>'
          + '<span class="t"><i style="width:' + Math.max(pct, 1) + '%"></i></span>'
          + '<span class="v">' + (t[k] || 0) + '</span></button>';
      }).join('');
    }
    function paintFilters(){
      var box = $('#jm-filters'); if (!box) return;
      var opts_ = [[0, 'All']].concat([5,4,3,2,1].map(function(k){ return [k, k + ' ★']; }));
      box.innerHTML = opts_.map(function(o){
        return '<button class="jm-f" type="button" data-star="' + o[0] + '"'
          + ' aria-pressed="' + (star === o[0]) + '">' + o[1] + '</button>';
      }).join('');
    }
    /* Product chips. Only rendered where the page supplied a product list, so
       the PDP is untouched by this. */
    function paintProducts(){
      var box = $('#jm-prods'); if (!box || !data.products) return;
      var rows = [{id:'', name:'Every club', total:data.total}].concat(data.products);
      box.innerHTML = rows.map(function(p){
        return '<button class="jm-p" type="button" data-prod="' + esc(p.id) + '"'
          + ' aria-pressed="' + (prod === p.id) + '">'
          + esc(p.name) + '<span>' + p.total + '</span></button>';
      }).join('');
    }
    function paintList(){
      var box = $('#jm-list'), more = $('#jm-more'), cnt = $('#jm-count');
      if (!box) return;
      var list = pool();
      if (!list.length){
        box.innerHTML = '<p class="jm-empty">No reviews at that rating in this sample.</p>';
        if (more) more.hidden = true;
        if (cnt) cnt.textContent = '';
        return;
      }
      box.innerHTML = list.slice(0, shown).map(function(r){
        return '<article class="jr">'
          + '<div class="jr-top">'
          +   '<span class="jr-av" aria-hidden="true">' + esc(r.n.charAt(0).toUpperCase()) + '</span>'
          +   '<span class="jr-who"><b>' + esc(r.n) + '</b>'
          +     '<span>' + (r.v ? 'Verified buyer · ' : '') + fmtDate(r.d) + '</span></span>'
          +   '<span class="jr-stars" role="img" aria-label="' + r.r + ' out of 5">' + starRow(r.r) + '</span>'
          + '</div>'
          + (r.t ? '<h4>' + esc(r.t) + '</h4>' : '')
          + '<p>' + esc(r.q) + '</p>'
          /* which club it is about, on the all-clubs page only */
          + (r.pn ? '<p class="jr-on">on <a href="' + esc(r.ph || '') + '">' + esc(r.pn) + '</a></p>' : '')
          + '</article>';
      }).join('');
      if (more) more.hidden = shown >= list.length;
      if (cnt){
        var t = totals();
        var scale = star ? (t[star] || 0) : scopedTotal();
        cnt.textContent = 'Showing ' + Math.min(shown, list.length) + ' of ' + list.length
          + ' in this sample · ' + scale + ' live'
          + (star ? ' at ' + star + ' star' : '');
      }
    }

    function setStar(s){
      star = s; shown = PAGE;
      paintFilters(); paintList();
      root.scrollIntoView({block:'nearest'});
    }
    function setProduct(id){
      prod = id; star = 0; shown = PAGE;
      paintProducts(); paintScore(); paintBars(); paintFilters(); paintList();
      root.scrollIntoView({block:'nearest'});
    }

    /* Delegation is scoped to the root, not to document — two widgets on one
       page would otherwise both answer the same click. */
    root.addEventListener('click', function(e){
      var f = e.target.closest('.jm-f'),
          b = e.target.closest('.jm-bars .row'),
          p = e.target.closest('.jm-p');
      if (p){ setProduct(p.getAttribute('data-prod')); return; }
      if (f){ setStar(+f.getAttribute('data-star')); return; }
      if (b){ setStar(+b.getAttribute('data-star')); return; }
      if (e.target.closest('#jm-more')){ shown += PAGE; paintList(); }
    });
    var sortSel = $('#jm-sort');
    if (sortSel) sortSel.addEventListener('change', function(){
      sort = sortSel.value; shown = PAGE; paintList();
    });

    paintProducts(); paintScore(); paintBars(); paintFilters(); paintList();
    return {setStar: setStar, setProduct: setProduct};
  }

  return {mount: mount, starRow: starRow, fmtDate: fmtDate, esc: esc};
})();
