/* The club buy box (templates/product.club.json). Data: window.LG_CLUB, written by the section from
   the product's live variants. Wedges (a Loft option): hand, loft chips, 1 to 3 wedge sets, the
   readout and the helper. Everything else: one chip row per option with more than one value. */
document.addEventListener('DOMContentLoaded', function(){
  var D = window.LG_CLUB; if (!D) return;
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var money = function(c){ return '$' + (c % 100 ? (c / 100).toFixed(2) : Math.round(c / 100)); };
  var toast = function(m){ if (window.Lucky && Lucky.toast) Lucky.toast(m); };
  var form = $('[data-club-form]'), vid = $('[data-vid]'), pre = $('[data-preprop]'), btn = $('[data-atc]'), sticky = $('[data-sticky]');
  var nf = $('#md-notify form[data-notify]');
  /* a variant's state: in stock, pre-order (at 0, still sold, and the product is set to pre-order) or out */
  function st(v){
    if (!v || !v.a) return 'out';
    if (D.mode === 'preorder' && v.m && v.q <= 0 && v.c === 'continue') return 'pre';
    return 'in';
  }
  var backLine = function(){ return D.month ? 'Back in ' + D.month : 'Sold out'; };
  var preLine = function(){ return 'Pre-order' + (D.month ? ', ships in ' + D.month : ''); };
  var flash = false;
  function openNotify(v, what){
    if (nf && v) nf.setAttribute('data-variant', v.id);
    var l = $('[data-notify-line]');
    if (l){ if (!l.getAttribute('data-default')) l.setAttribute('data-default', l.textContent);
      /* "on its way back" only with a restock month; with no date it stays the plain line */
      l.textContent = what && D.month ? 'The ' + what + " is on its way back. Drop your email and you'll get one message when it lands." : l.getAttribute('data-default'); }
    var m = $('#md-notify'); if (m) m.hidden = false;
  }
  if (window.LuckyBag) LuckyBag.onChange(function(){ if (!flash) return; flash = false;
    btn.setAttribute('data-done', ''); btn.textContent = 'In the bag';
    setTimeout(function(){ btn.removeAttribute('data-done'); paint(); }, 1600); });

  var paint = function(){};

  if (D.wedge) (function(){
    /* ---------------------------------------------------------- wedges */
    var handOf = function(v){ return D.hi > -1 ? v.o[D.hi] : ''; };
    var loftKey = function(raw){ var m = String(raw).match(/(\d+)\s*°?\s*([A-Za-z])?/); return m ? m[1] + (m[2] ? m[2].toUpperCase() : D.grind) : raw; };
    var HANDS = [], LOFTS = [], seen = {};
    D.variants.forEach(function(v){
      var h = handOf(v); if (HANDS.indexOf(h) < 0) HANDS.push(h);
      var k = loftKey(v.o[D.li]); if (!seen[k]){ seen[k] = 1; var m = k.match(/^(\d+)(\w)$/); LOFTS.push({ k: k, n: m[1], g: m[2], label: m[1] + '° ' + m[2] }); }
    });
    var handLabel = function(h){ return /left/i.test(h) ? 'Left hand' : /right/i.test(h) ? 'Right hand' : h; };
    var handed = function(){ return /left/i.test(state.hand) ? 'left' : 'right'; };
    var state = { hand: HANDS[0], picked: [], n: 1 };
    var find = function(k){ return D.variants.filter(function(v){ return handOf(v) === state.hand && loftKey(v.o[D.li]) === k; })[0]; };
    var dead = function(k){ return st(find(k)) === 'out'; };
    var nice = function(k){ var l = LOFTS.filter(function(x){ return x.k === k; })[0]; return l ? l.label : k; };
    function firstLive(){ var l = LOFTS.filter(function(v){ return !dead(v.k); }); return l.length ? l[Math.min(4, l.length - 1)].k : null; }
    var sv = D.variants.filter(function(v){ return v.id === D.start; })[0];
    if (sv){ state.hand = handOf(sv); state.picked = [loftKey(sv.o[D.li])]; }
    else if (LOFTS.some(function(l){ return l.k === '56' + D.grind; })) state.picked = ['56' + D.grind];
    function isOut(){ return state.n === 1 && state.picked.length === 1 && dead(state.picked[0]); }
    function unit(){ var v = find(state.picked[0]) || D.variants[0]; return v.p; }

    paint = function(){
      state.picked = state.picked.filter(function(k){ return state.n === 1 || !dead(k); });
      if (!state.picked.length && state.n === 1){ var f = firstLive(); state.picked = f ? [f] : [LOFTS[0].k]; }
      $('[data-hand]').innerHTML = HANDS.map(function(h){
        return '<button class="lg-chip" type="button" data-h="' + esc(h) + '" aria-pressed="' + (h === state.hand) + '">' + esc(handLabel(h)) + '</button>'; }).join('');
      $('[data-lofts]').innerHTML = LOFTS.map(function(l){
        var d = dead(l.k), ex = find(l.k);
        if (!ex) return '';
        return '<button class="lg-chip" type="button" data-l="' + l.k + '" aria-pressed="' + (state.picked.indexOf(l.k) > -1) + '"'
          + (d ? ' data-dead aria-label="' + esc(l.label) + ', ' + esc(backLine().toLowerCase()) + '"' : ' aria-label="' + esc(l.label) + '"')
          + '>' + l.n + '°<small>' + l.g + '</small></button>'; }).join('');
      var out = LOFTS.filter(function(l){ return find(l.k) && dead(l.k); }).map(function(l){ return l.label; });
      var sn = $('[data-stocknote]');
      if (out.length){ var last = out.pop(), names = out.length ? out.join(', ') + ' and ' + last : last;
        sn.innerHTML = '<b>' + esc(names) + ', ' + handed() + '-handed, ' + (out.length ? 'are' : 'is') + ' ' + (D.month ? 'back in ' + esc(D.month) : 'sold out') + '.</b> Everything else ships now.';
        sn.hidden = false; } else sn.hidden = true;
      $$('[data-set] button').forEach(function(b){ b.setAttribute('aria-pressed', String(+b.getAttribute('data-n') === state.n)); });
      var need = state.n - state.picked.length, u = unit(), sum = u * state.n, o = isOut();
      var pv = find(state.picked[0]), ps = st(pv), anyPre = state.picked.some(function(k){ return st(find(k)) === 'pre'; });
      $('[data-pickn]').textContent = state.picked.length ? '· ' + state.picked.map(nice).join(', ') : '';
      $('[data-sethint]').textContent = state.n === 1 ? "Two or more and shipping's on us" : need > 0 ? 'Tap ' + need + ' more loft' + (need > 1 ? 's' : '')
        : state.n + ' lofts, ' + money(u) + ' each' + (sum >= D.free * 100 ? ", shipping's on us" : '');
      $('[data-price-note]').hidden = state.n === 1;
      $('[data-price]').textContent = money(u);
      btn.textContent = o ? "Tell me when it's back" : need > 0 ? 'Tap ' + need + ' more loft' + (need > 1 ? 's' : '') + ' first'
        : (anyPre ? preLine() : 'Put ' + (state.n > 1 ? 'all ' + state.n : 'it') + ' in the bag') + ' · ' + money(sum);
      btn.setAttribute('aria-disabled', String(need > 0));
      var line = $('[data-stockline]');
      line.classList.toggle('is-out', o);
      line.textContent = o ? nice(state.picked[0]) + ', ' + handed() + '-handed, ' + (D.month ? 'is back in ' + D.month : 'is sold out')
        : anyPre ? preLine() : D.inStock;
      if (pv) vid.value = pv.id;
      pre.disabled = !(state.n === 1 && ps === 'pre'); pre.value = 'ships ' + (D.month || 'soon');
      $('[data-sticky-name]').textContent = D.title + ' · ' + state.picked.map(nice).join(', ');
      $('[data-sticky-price]').textContent = o ? backLine() : money(sum) + (state.n > 1 ? ' · ' + state.n + ' wedges' : '');
      $('[data-atc-sticky]').textContent = o ? 'Tell me' : D.atc;
      sticky.classList.toggle('is-one', state.n === 1);
      $('[data-sb-hand]').innerHTML = HANDS.map(function(h){ return '<option value="' + esc(h) + '"' + (h === state.hand ? ' selected' : '') + '>' + esc(handLabel(h)) + '</option>'; }).join('');
      $('[data-sb-loft]').innerHTML = LOFTS.filter(function(l){ return find(l.k); }).map(function(l){ return '<option value="' + l.k + '"' + (state.picked[0] === l.k ? ' selected' : '') + '>' + esc(l.label) + (dead(l.k) ? ' · ' + esc(backLine().toLowerCase()) : '') + '</option>'; }).join('');
      readout(o);
    };
    function readout(o){
      var p = state.picked, S = D.sheet || {};
      var cols = p.map(function(k){ var m = k.match(/^(\d+)(\w)$/), s = (S[m[2]] || {})[m[1]], d = dead(k);
        return '<div class="ro-c' + (d ? ' is-out' : '') + '"><b>' + m[1] + '°<small>' + m[2] + ' grind</small></b><dl>'
          + (s ? '<dt>Bounce</dt><dd>' + s[0] + '°</dd><dt>Lie</dt><dd>' + s[1] + '°</dd><dt>Length</dt><dd>' + s[2] + '&Prime;</dd>' : '')
          + (D.headg ? '<dt>Head</dt><dd>' + esc(D.headg) + '</dd>' : '') + '</dl></div>'; });
      for (var i = p.length; i < state.n; i++) cols.push('<div class="ro-c"><b style="color:var(--lg-ink-38)">&middot;&middot;&middot;</b><dl><dt>Tap a loft</dt><dd></dd></dl></div>');
      $('[data-readout]').innerHTML = '<div class="ro-hd"><span class="lg-label">' + (state.n > 1 ? 'Your set' : 'Your pick') + '</span>'
        + '<span class="lg-label lg-live' + (o ? ' is-out' : '') + '"><i></i>' + (o ? esc(backLine()) : 'In stock') + '</span></div>'
        + '<div class="ro-g' + (state.n === 1 ? ' is-one' : '') + '" style="--n:' + state.n + '">' + cols.join('') + '</div>';
    }
    document.addEventListener('click', function(e){
      var el;
      if (el = e.target.closest('[data-lofts] button')){
        var k = el.getAttribute('data-l'), i = state.picked.indexOf(k);
        if (el.hasAttribute('data-dead') && state.n > 1){ toast(nice(k) + " is " + (D.month ? 'back in ' + D.month : 'sold out') + ", so it can't go in a set yet."); return; }
        if (state.n === 1) state.picked = [k];
        else if (i > -1){ if (state.picked.length > 1) state.picked.splice(i, 1); }
        else if (state.picked.length < state.n) state.picked.push(k);
        else { state.picked.shift(); state.picked.push(k); }
        paint(); return;
      }
      if (el = e.target.closest('[data-set] button')){
        state.n = +el.getAttribute('data-n');
        if (state.picked.length > state.n) state.picked = state.picked.slice(-state.n);
        paint(); return;
      }
      if (el = e.target.closest('[data-hand] button')){ state.hand = el.getAttribute('data-h'); paint(); return; }
    });
    $('[data-sb-hand]').addEventListener('change', function(){ state.hand = this.value; paint(); });
    $('[data-sb-loft]').addEventListener('change', function(){ state.picked = [this.value]; state.n = 1; paint(); });
    form.addEventListener('submit', function(e){
      if (isOut()){ e.preventDefault(); e.stopPropagation(); openNotify(find(state.picked[0]), nice(state.picked[0])); return; }
      if (state.picked.length < state.n){ e.preventDefault(); e.stopPropagation(); if (window.Lucky) Lucky.jump('lofts'); return; }
      if (state.n > 1){ e.preventDefault(); e.stopPropagation();
        var items = state.picked.map(function(k){ var v = find(k), it = { id: v.id, quantity: 1 };
          if (st(v) === 'pre') it.properties = { 'Pre-order': 'ships ' + (D.month || 'soon') }; return it; });
        flash = true; LuckyBag.add(items).catch(function(){ flash = false; }); return; }
      flash = true;
    });
    /* the helper */
    (function(){
      var box = $('[data-helper]'); if (!box) return; var pw = 46, open = null;
      var has = function(g){ return LOFTS.some(function(l){ return l.g === g; }); };
      function calc(){ var b = pw + 6, l = [b, b + 4, b + 8].map(function(x){ return Math.min(60, Math.max(50, Math.round(x / 2) * 2)); }), g = open === 'yes' && has('S') ? 'S' : 'K';
        if (g === 'S') l = l.map(function(x){ return [52, 56, 60].reduce(function(a, c){ return Math.abs(c - x) < Math.abs(a - x) ? c : a; }); });
        return { lofts: l.filter(function(x, i, a){ return a.indexOf(x) === i; }), g: g }; }
      function draw(){ var r = calc();
        box.innerHTML = '<h4>1 · My pitching wedge is</h4><div class="lg-chips">' + [44, 45, 46, 47, 48].map(function(x){ return '<button class="lg-chip" type="button" data-pw="' + x + '" aria-pressed="' + (x === pw) + '">' + x + '°</button>'; }).join('')
          + '</div><h4>2 · Do you open the face around the green?</h4><div class="lg-chips"><button class="lg-chip" type="button" data-face="no" aria-pressed="' + (open === 'no') + '">Not really, I set up square</button><button class="lg-chip" type="button" data-face="yes" aria-pressed="' + (open === 'yes') + '">Yes, flops and bunkers</button></div>'
          + '<div class="rec"><b>' + r.lofts.map(function(l){ return l + '°'; }).join(' · ') + ' · ' + r.g + ' grind</b>'
          + (open === null ? 'Answer the second one and we\'ll pick the grind. Until then, it\'s the K.' : (r.g === 'K' ? 'The K: set it square and it behaves, in all six lofts.' : 'The S: opens up clean, in the 52, 56 and 60.'))
          + '</div><div class="md-foot"><button class="lg-btn-line" type="button" data-use>Use these lofts</button></div>'; }
      box.addEventListener('click', function(e){ var b;
        if (b = e.target.closest('[data-pw]')){ pw = +b.getAttribute('data-pw'); draw(); return; }
        if (b = e.target.closest('[data-face]')){ open = b.getAttribute('data-face'); draw(); return; }
        if (e.target.closest('[data-use]')){ var r = calc(), picks = r.lofts.map(function(l){ return l + r.g; }).filter(function(k){ return find(k) && !dead(k); }).slice(0, 3);
          if (!picks.length){ var f = firstLive(); picks = f ? [f] : []; } state.n = Math.max(1, picks.length); state.picked = picks; paint();
          $('#md-helper').hidden = true; if (window.Lucky) Lucky.jump('lofts'); } });
      draw();
    })();
  })();
  else (function(){
    /* ---------------------------------------------------------- one chip row per option */
    var n = (D.variants[0] || { o: [] }).o.length, pick = [];
    var sv = D.variants.filter(function(v){ return v.id === D.start; })[0] || D.variants.filter(function(v){ return v.a; })[0] || D.variants[0];
    for (var i = 0; i < n; i++) pick[i] = sv.o[i];
    var label = function(i, v){ return i === D.hi ? (/left/i.test(v) ? 'Left hand' : /right/i.test(v) ? 'Right hand' : v) : v; };
    var variant = function(){ return D.variants.filter(function(v){ return v.o.every(function(x, i){ return x === pick[i]; }); })[0]; };
    $$('[data-opt]').forEach(function(g){ var i = +g.getAttribute('data-opt');
      $$('button', g).forEach(function(b){ var dv = D.variants.filter(function(v){ return v.o[i] === b.getAttribute('data-v'); });
        if (dv.every(function(v){ return st(v) === 'out'; })) b.setAttribute('data-dead', ''); }); });
    paint = function(){
      $$('[data-opt]').forEach(function(g){ var i = +g.getAttribute('data-opt');
        $$('button', g).forEach(function(b){ b.setAttribute('aria-pressed', String(b.getAttribute('data-v') === pick[i])); });
        var lb = $('[data-pick="' + i + '"]'); if (lb) lb.textContent = pick[i] ? '· ' + label(i, pick[i]) : '';
        var sel = $('[data-sb-opt="' + i + '"]'); if (sel) sel.value = pick[i]; });
      var v = variant(), s = st(v);
      var line = $('[data-stockline]');
      line.textContent = s === 'in' ? D.inStock : s === 'pre' ? preLine() : backLine();
      line.classList.toggle('is-out', s === 'out');
      btn.textContent = s === 'out' ? "Tell me when it's back" : (s === 'pre' ? preLine() : D.atc) + ' · ' + money(v.p);
      $('[data-price]').textContent = money((v || D.variants[0]).p);
      if (v) vid.value = v.id;
      pre.disabled = s !== 'pre'; pre.value = 'ships ' + (D.month || 'soon');
      var last = n - 1, many = $$('[data-opt]').length;
      $('[data-sticky-name]').textContent = D.title + (n && pick[last] ? ' · ' + label(last, pick[last]) : '');
      $('[data-sticky-price]').textContent = s === 'out' ? backLine() : money(v.p);
      $('[data-atc-sticky]').textContent = s === 'out' ? 'Tell me' : D.atc;
      var mon = $('[data-mon-stock]'); if (mon){ mon.textContent = s === 'out' ? backLine() : 'In stock'; mon.parentNode.classList.toggle('is-out', s === 'out'); }
    };
    document.addEventListener('click', function(e){ var b = e.target.closest('[data-opt] button'); if (!b) return;
      pick[+b.closest('[data-opt]').getAttribute('data-opt')] = b.getAttribute('data-v'); paint(); });
    document.addEventListener('change', function(e){ var s = e.target.closest('[data-sb-opt]'); if (!s) return; pick[+s.getAttribute('data-sb-opt')] = s.value; paint(); });
    form.addEventListener('submit', function(e){
      var v = variant();
      if (st(v) === 'out'){ e.preventDefault(); e.stopPropagation(); openNotify(v); return; }
      flash = true;
    });
  })();

  /* the sticky bar: once the real button has scrolled away, until the footer */
  $('[data-atc-sticky]').addEventListener('click', function(){ if (form.requestSubmit) form.requestSubmit(); else btn.click(); });
  (function(){
    var ftr = $('.lg-ftr');
    function p(){ var on = form.getBoundingClientRect().bottom < 0 && (!ftr || ftr.getBoundingClientRect().top > innerHeight);
      if (on !== sticky.hasAttribute('data-on')){ sticky.toggleAttribute('data-on', on); if (window.Lucky && Lucky.guide && Lucky.guide.place) Lucky.guide.place(); } }
    addEventListener('scroll', p, { passive: true }); addEventListener('resize', p); p();
  })();

  /* gallery dots (phone) */
  (function(){ var g = $('[data-gal]'), d = $('[data-dots]'); if (!g || !d || !d.children.length) return; var n = g.children.length; d.children[0].classList.add('on');
    g.addEventListener('scroll', function(){ var i = Math.round(g.scrollLeft / (g.scrollWidth / n)); [].forEach.call(d.children, function(x, k){ x.classList.toggle('on', k === i); }); }, { passive: true }); })();

  /* the gallery shows five; the button opens the rest */
  var ga = $('[data-gal-all]');
  if (ga) ga.addEventListener('click', function(){ var g = $('[data-gal]'); g.classList.add('is-all'); ga.setAttribute('aria-expanded', 'true'); ga.hidden = true; });

  /* rails and tabs further down the page */
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-railarrows] button');
    if (b){ var r = $('[data-rail]:not([hidden])'); if (r) r.scrollBy({ left: (b.getAttribute('aria-label') === 'Next' ? 1 : -1) * 520, behavior: 'smooth' }); return; }
    var m = e.target.closest('[data-moodseg] button');
    if (m){ var mood = $('#finishes'), k = m.getAttribute('data-m');
      $$('[data-moodseg] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === m)); });
      mood.setAttribute('data-metal', k);
      $$('[data-mh]', mood).forEach(function(h){ h.hidden = h.getAttribute('data-mh') !== k; });
      $$('[data-rail]', mood).forEach(function(r){ r.hidden = r.getAttribute('data-rail') !== k; }); return; }
    var t = e.target.closest('[data-spectabs] button');
    if (t){ $$('[data-spectabs] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === t)); });
      $$('[data-spectab]').forEach(function(p){ p.hidden = p.getAttribute('data-spectab') !== t.getAttribute('data-tab'); }); return; }
    var g = e.target.closest('[data-specseg] button');
    if (g){ $$('[data-specseg] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === g)); });
      $$('[data-spec]').forEach(function(tb){ tb.hidden = tb.getAttribute('data-spec') !== g.getAttribute('data-g'); }); }
  });

  /* reviews: the proximity chart from the live Judge.me histogram, then the latest reviews */
  var R = window.LG_CLUB_REVIEWS;
  if (R && $('#prox') && window.Lucky && Lucky.proximity) Lucky.proximity($('#prox'), R.nums ? { counts: R.totals } : { counts: R.totals, nums: false });
  if (R && $('#jm-list')) (function(){
    var filt = 0, sort = 'recent', shown = 6, S = R.list;
    var star = function(n){ return '★★★★★'.slice(0, n) + '☆☆☆☆☆'.slice(0, 5 - n); };
    $('#jm-filters').innerHTML = ['All', 5, 4, 3, 2, 1].map(function(k, i){ return '<button class="lg-chip" type="button" data-f="' + (i ? k : 0) + '" aria-pressed="' + (!i) + '">' + (i ? k + ' ★ · ' + (R.totals[k] || 0) : 'All · ' + R.total) + '</button>'; }).join('');
    function draw(){
      var l = S.filter(function(r){ return !filt || r.r === filt; }).slice();
      l.sort(sort === 'high' ? function(a, b){ return b.r - a.r || (b.d > a.d ? 1 : -1); } : sort === 'low' ? function(a, b){ return a.r - b.r || (b.d > a.d ? 1 : -1); } : function(a, b){ return b.d > a.d ? 1 : -1; });
      $('#jm-count').textContent = 'The latest ' + Math.min(shown, l.length) + (filt ? ' at ' + filt + ' stars' : '') + ' of ' + (filt ? (R.totals[filt] || 0) : R.total) + '.';
      $('#jm-list').innerHTML = l.slice(0, shown).map(function(r){
        return '<div class="jm-item"><span class="lg-stars" aria-label="' + r.r + ' out of 5" style="line-height:1;color:var(--lg-star)">' + star(r.r) + '</span>' + (r.t ? '<b>' + esc(r.t) + '</b>' : '') + '<p>' + esc(r.q) + '</p><small>' + esc(r.n) + (r.v ? ' · Verified buyer' : '') + ' · ' + esc(r.d) + '</small></div>'; }).join('');
      var more = shown < l.length, full = $('[data-jdgm-full]');
      $('#jm-more').hidden = !more && !(full && full.hidden);
    }
    $('#jm-filters').addEventListener('click', function(e){ var b = e.target.closest('[data-f]'); if (!b) return; filt = +b.getAttribute('data-f'); shown = 6;
      $$('#jm-filters button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === b)); }); draw(); });
    $('#jm-sort').addEventListener('change', function(){ sort = this.value; draw(); });
    $('#jm-more').addEventListener('click', function(){
      if (shown < S.length){ shown += 6; draw(); return; }
      var full = $('[data-jdgm-full]'); if (full){ full.hidden = false; $('#jm-list').hidden = true; $('#jm-count').hidden = true; $('.jm-bar').hidden = true; } this.hidden = true; });
    $('[data-readall]').addEventListener('click', function(){ var jm = $('#jm'), o = !jm.hidden; jm.hidden = o; this.setAttribute('aria-expanded', String(!o)); $('i', this).textContent = o ? '+' : '−'; if (!o) draw(); });
  })();

  paint();
});
