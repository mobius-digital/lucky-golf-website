/* ==========================================================================
   CLUB PDP · the buy box and the page's own moves (design system v2).
   Availability comes from products.json through the same LG_VARIANTS engine
   the collection quick-add uses; the cart add goes through core's [data-add]
   delegate, so there is still one add-to-cart path on the whole site.

   Axes are read by KEY, not position: a wedge has hand + loftgrind, a
   putter has hand only (or one fixed hand), the hybrid has hand. Whatever
   axis the product lacks, its row is simply not rendered by the template.
   ========================================================================== */
var PD = {{PRODUCT_JSON}};
var PD_REVIEWS = {{REVIEWS_JSON}};
var PD_REEL = {{REEL_JSON}};
var LG_CART_UPSELL = {{UPSELL_JSON}};

(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };

  /* ------------------------------------------------------------ the axes */
  var V = LG_VARIANTS;
  var AX = PD.options || [];
  var HAND = AX.filter(function(a){ return a.key === 'hand'; })[0] || null;
  var LOFT = AX.filter(function(a){ return a.key === 'loftgrind' || a.key === 'loft'; })[0] || null;
  var hi = AX.indexOf(HAND), li = AX.indexOf(LOFT);
  var def = String(PD['default']).split('|');
  var state = {hand: hi > -1 ? def[hi] : null, picked: LOFT ? [def[li]] : [null], n: 1};
  function keyFor(k){ return AX.map(function(a, i){ return i === hi ? state.hand : (i === li ? k : def[i]); }).join('|'); }
  function selFor(k){ return keyFor(k).split('|'); }
  var priceOf = function(k){ var v = PD.variants[keyFor(k)]; return v ? v.price : PD.price; };
  var money = function(n){ return '$' + n; };
  var nice = function(k){ if (!LOFT) return ''; var v = LOFT.values.filter(function(x){ return x.k === k; })[0]; return v ? v.label : k; };
  function dead(k){ var v = PD.variants[keyFor(k)]; return !(v && v.avail); }
  function handDead(h){ return hi < 0 ? false : !V.offered(PD, [h], hi, h); }
  function soldList(){ return LOFT ? LOFT.values.filter(function(v){ return dead(v.k); }).map(function(v){ return v.k; }) : []; }
  function firstLive(){ if (!LOFT) return dead(null) ? undefined : null; var l = LOFT.values.filter(function(v){ return !dead(v.k); }); return l.length ? l[Math.min(4, l.length - 1)].k : undefined; }
  var handLabel = function(){ if (!HAND) return ''; var v = HAND.values.filter(function(x){ return x.k === state.hand; })[0]; return v ? v.label : ''; };

  /* ---------------------------------------------------------- the paint */
  var handBox = $('[data-hand]'), loftBox = $('[data-lofts]');
  function paintHand(){
    if (!handBox || !HAND) return;
    handBox.innerHTML = HAND.values.map(function(v){
      var d = handDead(v.k);
      return '<button class="f" type="button" data-h="' + esc(v.k) + '" aria-pressed="' + (v.k === state.hand) + '"'
        + (d ? ' disabled aria-label="' + esc(v.label) + ', out of stock"' : '') + '>' + esc(v.label) + '</button>';
    }).join('');
    var note = $('[data-handnote]');
    if (note) note.textContent = HAND.values.length === 1 ? (HAND.values[0].label + ' only') : '';
  }
  function paintLofts(){
    if (!loftBox || !LOFT) return;
    loftBox.innerHTML = LOFT.values.map(function(v){
      var d = dead(v.k), m = v.label.match(/^(\d+)°\s*(\w)$/);
      var txt = m ? m[1] + '° <small>' + m[2] + '</small>' : esc(v.label);
      return '<button type="button" class="' + (d ? 'so' : '') + '" data-l="' + esc(v.k) + '"'
        + ' aria-pressed="' + (state.picked.indexOf(v.k) > -1) + '"'
        + (d ? ' disabled aria-label="' + esc(v.label) + ', out of stock"' : ' aria-label="' + esc(v.label) + '"')
        + '>' + txt + '</button>';
    }).join('');
  }
  function stockNote(){
    var box = $('[data-stocknote]'); if (!box) return;
    var handWord = HAND ? (state.hand === 'LH' ? 'left-handed' : 'right-handed') : '';
    if (!LOFT){
      if (!dead(null)){ box.hidden = true; return; }
      box.innerHTML = '<b>Sold out' + (HAND ? ', ' + handWord : '') + '.</b> Back soon. '
        + '<a href="{{link:none}}" data-md-open="md-notify" data-what="' + esc(PD.title) + '">Tell me when it is back &rarr;</a>';
      box.hidden = false; return;
    }
    var out = soldList();
    if (!out.length){ box.hidden = true; box.innerHTML = ''; return; }
    var list = out.map(nice), last = list.pop();
    var names = list.length ? list.join(', ') + ' and ' + last : last;
    box.innerHTML = '<b>' + esc(names) + (HAND ? ', ' + handWord + ',' : '') + ' ' + (out.length > 1 ? 'are' : 'is')
      + ' back next month.</b> Everything else is in stock now. '
      + '<a href="{{link:none}}" data-md-open="md-notify" data-what="' + esc(names) + '">Tell me when it is back &rarr;</a>';
    box.hidden = false;
  }
  function renderBuy(){
    state.picked = state.picked.filter(function(k){ return !dead(k); });
    if (!state.picked.length){ var f = firstLive(); state.picked = f === undefined ? [] : [f]; }
    if (state.n < state.picked.length) state.n = state.picked.length;
    paintHand(); paintLofts(); stockNote();
    $$('[data-set] .s').forEach(function(s){
      var on = +s.getAttribute('data-n') === state.n;
      s.classList.toggle('on', on); s.setAttribute('aria-pressed', String(on));
    });
    var need = state.n - state.picked.length;
    var unit = state.picked.length ? priceOf(state.picked[0]) : PD.price;
    var pk = $('[data-pickn]'), sh = $('[data-sethint]');
    if (pk) pk.textContent = state.picked.length && LOFT ? '· ' + state.picked.map(nice).join(', ') : '';
    if (sh) sh.textContent = state.n === 1 ? 'One wedge'
      : (need > 0 ? 'Pick ' + need + ' more loft' + (need > 1 ? 's' : '')
                  : state.n + ' lofts picked · ' + money(unit) + ' each, same as one');
    $('[data-price]').textContent = money(unit) + (state.n > 1 ? ' each' : '');
    var btn = $('[data-atc]');
    btn.textContent = !state.picked.length ? 'Out of stock'
      : need > 0 ? 'Pick ' + need + ' more loft' + (need > 1 ? 's' : '') + ' first'
      : 'Add ' + (state.n > 1 ? state.n + ' wedges' : 'to bag') + ' · ' + money(unit * state.n);
    btn.setAttribute('aria-disabled', String(need > 0 || !state.picked.length));
    var line = $('[data-stockline]');
    if (line) line.innerHTML = state.picked.length ? '<b>In stock</b> · ships in 1 to 2 days' : 'Out of stock' + (HAND ? ' in this hand' : '');
    var sn = $('[data-sticky-name]'), sp = $('[data-sticky-price]');
    if (sn) sn.textContent = PD.title + (LOFT && state.picked.length ? ' · ' + state.picked.map(nice).join(', ') : (HAND ? ' · ' + handLabel() : ''));
    if (sp) sp.textContent = money(unit * Math.max(1, state.n)) + (state.n > 1 ? ' · ' + state.n + ' wedges' : '');
  }

  /* --------------------------------------------------------- the clicks */
  document.addEventListener('click', function(e){
    var el;
    if (el = e.target.closest('[data-lofts] button')){
      if (el.disabled) return;
      var k = el.getAttribute('data-l'), i = state.picked.indexOf(k);
      if (i > -1){ if (state.picked.length > 1){ state.picked.splice(i, 1); state.n = state.picked.length; } }
      else if (state.picked.length < 3){ state.picked.push(k); state.n = Math.max(state.n, state.picked.length); }
      else { state.picked.shift(); state.picked.push(k); }
      renderBuy(); return;
    }
    if (el = e.target.closest('[data-set] .s')){
      state.n = +el.getAttribute('data-n'); state.picked = state.picked.slice(0, state.n); renderBuy(); return;
    }
    if (el = e.target.closest('[data-hand] button')){
      if (el.disabled) return;
      state.hand = el.getAttribute('data-h'); renderBuy(); return;
    }
  });

  /* ------------------------------------------------- add to bag, N times.
     One hidden [data-add] proxy: core.js's delegate reads the attributes,
     adds the line, opens the drawer once (it ignores a second open). */
  var proxy = document.createElement('button');
  proxy.type = 'button'; proxy.setAttribute('data-add', ''); proxy.hidden = true;
  proxy.setAttribute('aria-hidden', 'true'); proxy.tabIndex = -1;
  document.body.appendChild(proxy);
  function addAll(btn){
    if (state.picked.length < state.n || !state.picked.length) { var lb = $('[data-lofts]') || $('[data-hand]'); if (lb) lb.scrollIntoView({behavior:'smooth', block:'center'}); return; }
    state.picked.forEach(function(k){
      var v = PD.variants[keyFor(k)];
      var variant = [handLabel(), nice(k)].filter(Boolean).join(' · ');
      proxy.setAttribute('data-sku', v.sku);
      proxy.setAttribute('data-name', PD.name + (LOFT ? ' ' + nice(k) : ''));
      proxy.setAttribute('data-price', money(v.price));
      proxy.setAttribute('data-img', PD.img);
      proxy.setAttribute('data-variant', variant);
      proxy.click();
    });
    var was = btn.textContent; btn.textContent = 'Added';
    setTimeout(function(){ btn.textContent = was; }, 1400);
  }
  $('[data-atc]').addEventListener('click', function(){ addAll(this); });
  var sticky = $('[data-sticky]');
  if (sticky) $('[data-atc-sticky]').addEventListener('click', function(){ addAll($('[data-atc]')); });

  /* -------------------------------------------- sticky bar: phones only.
     On from the moment the real button scrolls off the top, off again when
     the footer arrives. Nothing without observer support. */
  (function(){
    var cta = $('.cta'), ftr = $('.ftr');
    if (!sticky || !cta || !ftr || !('IntersectionObserver' in window)) return;
    var ctaSeen = true, footerNear = false;
    function paint(){ sticky.toggleAttribute('data-on', !ctaSeen && !footerNear); }
    new IntersectionObserver(function(es){ es.forEach(function(en){
      ctaSeen = en.isIntersecting || en.boundingClientRect.top > 0; }); paint(); }, {threshold: 0}).observe(cta);
    new IntersectionObserver(function(es){ es.forEach(function(en){
      footerNear = en.isIntersecting || en.boundingClientRect.top < 0; }); paint(); }, {threshold: 0}).observe(ftr);
  })();

  /* ------------------------------------------------- gallery dots (phone) */
  (function(){
    var gal = $('[data-gal]'), dots = $('[data-dots]');
    if (!gal || !dots) return;
    var n = gal.children.length;
    if (dots.children[0]) dots.children[0].classList.add('on');
    gal.addEventListener('scroll', function(){
      var i = Math.round(gal.scrollLeft / (gal.scrollWidth / n));
      [].forEach.call(dots.children, function(d, k){ d.classList.toggle('on', k === i); });
    }, {passive: true});
  })();

  /* --------------------------------------------------------- the helper */
  var helperBox = $('[data-helper]');
  if (helperBox && LOFT){
    var pw = 46, open = null;
    var LIVE = LOFT.values.map(function(v){ return v.k; });
    function calc(){
      var base = pw + 6;
      var lofts = [base, base + 4, base + 8].map(function(x){ return Math.min(60, Math.max(50, Math.round(x / 2) * 2)); });
      var g = open === 'yes' ? 'S' : 'K';
      if (g === 'S') lofts = lofts.map(function(l){ return [52, 56, 60].reduce(function(a, b){ return Math.abs(b - l) < Math.abs(a - l) ? b : a; }); });
      lofts = lofts.filter(function(l, i, a){ return a.indexOf(l) === i; });
      return {lofts: lofts, g: g};
    }
    function draw(){
      var r = calc();
      helperBox.innerHTML = '<h4>1 · My pitching wedge is</h4><div class="pw">'
        + [44, 45, 46, 47, 48].map(function(x){ return '<button type="button" data-pw="' + x + '" aria-pressed="' + (x === pw) + '">' + x + '°</button>'; }).join('')
        + '</div><h4>2 · Do you open the face around the green?</h4><div class="yn">'
        + '<button type="button" data-face="no" aria-pressed="' + (open === 'no') + '">Not really, I set up square</button>'
        + '<button type="button" data-face="yes" aria-pressed="' + (open === 'yes') + '">Yes, flops and bunkers</button></div>'
        + '<div class="rec"><b>' + r.lofts.map(function(l){ return l + '°'; }).join(' · ') + ' · ' + r.g + ' grind</b>'
        + (open === null ? 'Answer question 2 and the grind locks in. K is the default.'
          : (r.g === 'K' ? 'Wider sole, square setups, no surprises. All six lofts.' : 'Narrower sole, opens up clean. 52, 56 and 60.'))
        + '</div><div class="md-foot"><button class="btn" type="button" data-use>Use these</button></div>';
    }
    helperBox.addEventListener('click', function(e){
      var b;
      if (b = e.target.closest('[data-pw]')){ pw = +b.getAttribute('data-pw'); draw(); return; }
      /* data-face, not data-open: the modal shell carries data-open itself and closest() would climb to it */
      if (b = e.target.closest('[data-face]')){ open = b.getAttribute('data-face'); draw(); return; }
      if (e.target.closest('[data-use]')){
        var r = calc();
        var picks = r.lofts.map(function(l){ return l + r.g; }).filter(function(k){ return LIVE.indexOf(k) > -1 && !dead(k); }).slice(0, 3);
        if (!picks.length){ var f = firstLive(); picks = f === undefined ? [] : [f]; }
        state.n = Math.max(1, picks.length); state.picked = picks; renderBuy();
        var x = $('#md-helper [data-md-close]'); if (x) x.click();
        $('[data-lofts]').scrollIntoView({behavior: 'smooth', block: 'center'});
      }
    });
    draw();
  }

  /* ------------------------------------------------- restock email modal */
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-md-open="md-notify"]'); if (!t) return;
    var line = $('[data-notify-line]'), what = t.getAttribute('data-what');
    if (line && what) line.textContent = what + ' is on the way back. Leave an email and the day it is in stock you get one message, from a person.';
  });
  var notify = $('[data-notify]');
  if (notify) notify.addEventListener('submit', function(e){
    e.preventDefault();
    var f = notify.querySelector('input');
    if (!f.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value)){ f.focus(); return; }
    notify.innerHTML = '<p class="done" style="margin-top:14px"><b>Done.</b> One email, the day it is back.</p>';
  });

  /* ------------------------------------------------- shot / clip briefs */
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-md-open="md-shot"]'); if (!t) return;
    $('[data-shot-title]').textContent = t.getAttribute('data-title') || 'Shot needed';
    $('[data-shot-brief]').textContent = t.getAttribute('data-brief') || '';
  });

  /* ------------------------------------------------------------ zoom */
  var zoom = $('#zoom');
  if (zoom && zoom.showModal){
    document.addEventListener('click', function(e){
      var t = e.target.closest('[data-zoom]');
      if (t){ var im = zoom.querySelector('img'); im.src = t.getAttribute('data-zoom'); im.alt = (t.querySelector('img') || {}).alt || ''; zoom.showModal(); return; }
      if (e.target.closest('[data-zoom-close]') || e.target === zoom) zoom.close();
    });
  }

  /* ---------------------------------------------------- mood: the worlds */
  var mood = $('[data-mood]');
  if (mood) mood.addEventListener('click', function(e){
    var b = e.target.closest('[data-moodseg] button'); if (!b) return;
    var m = b.getAttribute('data-m'); mood.setAttribute('data-mood', m);
    $$('[data-moodseg] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === b)); });
    $$('[data-mh]', mood).forEach(function(h){ h.hidden = h.getAttribute('data-mh') !== m; });
    $$('[data-rail]', mood).forEach(function(r){ r.hidden = r.getAttribute('data-rail') !== m; });
  });
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-railarrows] button');
    if (b){ var r = $('[data-rail]:not([hidden])'); if (r) r.scrollBy({left: (b.getAttribute('aria-label') === 'Next' ? 1 : -1) * 640, behavior: 'smooth'}); return; }
    var c = e.target.closest('[data-cliparrows] button');
    if (c){ var cl = $('#clips'); if (cl) cl.scrollBy({left: (c.getAttribute('aria-label') === 'Next' ? 1 : -1) * cl.clientWidth * .5, behavior: 'smooth'}); }
  });

  /* -------------------------------------------------------------- specs */
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-spectabs] button');
    if (t){ $$('[data-spectabs] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === t)); });
      $$('[data-spectab]').forEach(function(p){ p.hidden = p.getAttribute('data-spectab') !== t.getAttribute('data-tab'); }); return; }
    var g = e.target.closest('[data-specseg] button');
    if (g){ $$('[data-specseg] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === g)); });
      $$('[data-spec]').forEach(function(tb){ tb.hidden = tb.getAttribute('data-spec') !== g.getAttribute('data-g'); }); }
  });

  /* ---------------------------------------------------------- accordion */
  document.addEventListener('click', function(e){
    var h = e.target.closest('.acc-h'); if (!h) return;
    var body = h.nextElementSibling, open = h.getAttribute('aria-expanded') === 'true';
    h.setAttribute('aria-expanded', String(!open)); body.hidden = open;
    var s = h.querySelector('span'); if (s) s.textContent = open ? '+' : '−';
  });

  /* ---------------------------------------------------------- the clips */
  var clips = $('#clips');
  if (clips) clips.innerHTML = PD_REEL.map(function(o, i){
    var title = o.title || o.kind || ('Clip ' + (i + 1));
    return o.src
      ? '<div class="clip"><video controls preload="metadata" playsinline' + (o.poster ? ' poster="' + esc(o.poster) + '"' : '') + '><source src="' + esc(o.src) + '" type="video/mp4"></video></div>'
      : '<div class="clip" data-md-open="md-shot" data-title="' + esc(title) + '" data-brief="' + esc(o.brief) + '"><small>Clip needed</small><b>' + esc(title) + '</b>' + esc(o.brief) + '</div>';
  }).join('');

  /* ------------------------------------------------------------ reviews */
  var rv = $('#reviews');
  if (rv && typeof LG_REVIEWS !== 'undefined') LG_REVIEWS.mount(rv, PD_REVIEWS);
  var ra = $('[data-readall]');
  if (ra) ra.addEventListener('click', function(){
    var jm = $('#jm'), open = !jm.hidden;
    jm.hidden = open; ra.setAttribute('aria-expanded', String(!open));
    ra.querySelector('i').textContent = open ? '+' : '−';
  });

  renderBuy();
})();
