/* The Black Friday page (sections/lg-bfcm.liquid).
   Phase from the clock (Central time), the countdown, the mail code applied for postcard visitors,
   the receipt that does the ladder math, one-tap sets, and a build-your-own tray with a sticky total.
   The ladder here only DISPLAYS the price: the real discount is the "Lucky club ladder" function at checkout. */
(function () {
  var cfg = window.LG_BF, page = document.querySelector('[data-bf-page]');
  if (!cfg || !page) return;
  var $ = function (s, r) { return (r || page).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || page).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var money = function (c) { return '$' + (c % 100 ? (c / 100).toFixed(2) : Math.round(c / 100)); };
  var off = function (n) { return n >= 3 ? 10000 : n === 2 ? 5000 : 0; };

  /* ---------------------------------------------------------------- phase */
  var q = new URLSearchParams(location.search);
  var phase = 'mail';
  cfg.phases.forEach(function (p) { if (p[1] && Date.now() >= Date.parse(p[1])) phase = p[0]; });
  if (q.get('bf_phase')) phase = q.get('bf_phase');
  page.setAttribute('data-phase', phase);
  $$('[data-bf-show]').forEach(function (el) { el.hidden = el.getAttribute('data-bf-show').split(' ').indexOf(phase) < 0; });
  var giftMin = cfg.giftsGone ? 99 : phase === 'mail' ? 1 : 2;

  /* ---------------------------------------------------------------- clock */
  var clock = $('[data-bf-clock]'), end = Date.parse(cfg.end);
  var two = function (n) { return (n < 10 ? '0' : '') + n; };
  function tick() {
    if (!clock || !end) return;
    var t = Math.max(0, Math.floor((end - Date.now()) / 1000));
    $('[data-d]', clock).textContent = Math.floor(t / 86400);
    $('[data-h]', clock).textContent = two(Math.floor(t % 86400 / 3600));
    $('[data-m]', clock).textContent = two(Math.floor(t % 3600 / 60));
  }
  tick(); setInterval(tick, 30000);

  /* ---------------------------------------------------------------- the code */
  var ticket = $('[data-bf-code]');
  var code = (phase === 'list' && cfg.codes.list) ? cfg.codes.list : cfg.codes.mail;
  if (ticket) $('[data-code-text]', ticket).textContent = code;
  var src = (q.get('utm_source') || '').toLowerCase();
  var sources = (cfg.autoSources || '').toLowerCase().split(/[\s,]+/).filter(Boolean);
  var want = q.get('code') || (sources.indexOf(src) > -1 ? code : '');
  try { if (!want) want = sessionStorage.getItem('lg_bf_code') || ''; } catch (e) {}
  if (want && (phase === 'mail' || phase === 'list')) {
    fetch('/discount/' + encodeURIComponent(want), { credentials: 'same-origin' }).then(function () {
      try { sessionStorage.setItem('lg_bf_code', want); } catch (e) {}
      if (!ticket) return;
      $('[data-code-text]', ticket).textContent = want;
      $('[data-code-off]', ticket).hidden = true;
      $('[data-code-on]', ticket).hidden = false;
      ticket.classList.add('is-on');
    }).catch(function () {});
  }

  /* ---------------------------------------------------------------- the clubs */
  var CLUBS = cfg.clubs || [];
  var BY = {};
  CLUBS.forEach(function (c) {
    var hi = c.opts.findIndex(function (o) { return /hand/i.test(o); });
    var fi = c.opts.findIndex(function (o) { return /finish/i.test(o); });
    var li = c.opts.findIndex(function (o) { return /loft/i.test(o); });
    c.variants.forEach(function (v) {
      v.club = c;
      v.hand = hi > -1 ? (/left/i.test(v.o[hi]) ? 'L' : 'R') : 'R';
      v.fin = fi > -1 ? v.o[fi] : '';
      var m = li > -1 ? String(v.o[li]).match(/(\d+)\s*°?\s*([A-Za-z])?/) : null;
      v.loft = m ? m[1] + (m[2] || 'K').toUpperCase() : '';
      v.label = [m ? m[1] + '°' + (m[2] ? ' ' + m[2].toUpperCase() : '') : '', fi > -1 && !c.finish ? v.fin : ''].filter(Boolean).join(' ');
      BY[v.id] = v;
    });
  });
  var HAND = 'R';
  try { HAND = localStorage.getItem('lg_hand') === 'L' ? 'L' : 'R'; } catch (e) {}
  if (q.get('hand')) HAND = /^l/i.test(q.get('hand')) ? 'L' : 'R';

  /* ---------------------------------------------------------------- the receipt */
  var SAMPLE = { 1: 'Carver 02 Gold', 2: 'Carver 02 Gold', 3: 'Carver 02 Gold' };
  var nSel = 3;
  function receipt(n) {
    nSel = n;
    $$('[data-n]').forEach(function (b) { b.setAttribute('aria-selected', String(+b.getAttribute('data-n') === n)); });
    $$('[data-rung]').forEach(function (li) { li.classList.toggle('is-on', +li.getAttribute('data-rung') === n); });
    var unit = 9900, sub = unit * n, cut = off(n), gift = n >= giftMin, shipFree = sub - cut >= cfg.ship;
    var lines = [];
    lines.push([n + ' × ' + SAMPLE[n], money(sub)]);
    if (cut) lines.push(['Black Friday, ' + n + (n >= 3 ? '+' : '') + ' clubs', '−' + money(cut), 'is-cut']);
    lines.push(['Towel + divot tool', gift ? 'Free' : (cfg.giftsGone ? 'Gone' : '2+ clubs'), gift ? 'is-free' : 'is-dim']);
    lines.push(['Shipping', shipFree ? 'Free' : 'From $18', shipFree ? 'is-free' : 'is-dim']);
    $('[data-r-lines]').innerHTML = lines.map(function (l) { return '<li class="' + (l[2] || '') + '"><span>' + esc(l[0]) + '</span><b>' + esc(l[1]) + '</b></li>'; }).join('');
    $('[data-r-total]').textContent = money(sub - cut);
    var sv = $('[data-r-save]');
    sv.textContent = cut ? 'You keep ' + money(cut) + '. Buy a sleeve of balls with it.' : 'Add one more club and the price drops $50.';
  }
  var r1 = $('[data-rung-text="1"]');
  if (r1) r1.textContent = giftMin === 1 ? 'Free towel + divot tool' : 'Our everyday price';
  var d = $('[data-r-date]'); if (d) d.textContent = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }).toUpperCase();
  page.addEventListener('click', function (e) { var b = e.target.closest('[data-n]'); if (b) receipt(+b.getAttribute('data-n')); });
  if ($('[data-r-lines]')) receipt(3);

  /* ---------------------------------------------------------------- one-tap sets */
  function resolve(tok) {
    var p = tok.trim().split(':'), c = CLUBS.filter(function (x) { return x.key === p[0]; })[0];
    if (!c) return null;
    var loft = p[1] ? p[1].toUpperCase() : '', fin = p[2] || '';
    var all = []; CLUBS.forEach(function (x) { if (x.key === p[0]) all = all.concat(x.variants); });
    return all.filter(function (v) { return v.hand === HAND && (!loft || v.loft === loft) && (!fin || v.fin.toLowerCase() === fin.toLowerCase()) && v.a; })[0] || null;
  }
  var SETS = [];
  function drawSets() {
    var box = $('[data-sets]'); if (!box) return;
    SETS = String(cfg.sets || '').split(/\r?\n/).map(function (line) {
      var p = line.split('|'); if (p.length < 3) return null;
      var vs = p[2].split(',').map(resolve);
      if (vs.some(function (v) { return !v; })) return null;
      return { name: p[0].trim(), line: p[1].trim(), vs: vs };
    }).filter(Boolean);
    box.innerHTML = SETS.map(function (s, i) {
      var n = s.vs.length, t = s.vs.reduce(function (a, v) { return a + v.p; }, 0), cut = off(n);
      var pics = s.vs.map(function (v, j) { return '<img src="' + esc(v.img || v.club.img) + '" alt="" loading="lazy" style="--i:' + (j - (n - 1) / 2) + '">'; }).join('');
      return '<article class="bf-set">'
        + '<div class="bf-set-ph" aria-hidden="true">' + pics + '<i class="bf-set-tag">Save ' + money(cut) + '</i></div>'
        + '<div class="bf-set-bd"><h3>' + esc(s.name) + '</h3><p>' + esc(s.line) + '</p>'
        + '<ul>' + s.vs.map(function (v) { return '<li>' + esc(v.loft ? v.loft.replace(/^(\d+)(\w)$/, '$1° $2') + (v.fin ? ' ' + v.fin : '') : v.club.name) + '</li>'; }).join('') + '</ul>'
        + '<p class="bf-set-pr"><b>' + money(t - cut) + '</b> <s>' + money(t) + '</s></p>'
        + '<button type="button" class="lg-btn lg-btn-block" data-set="' + i + '">' + esc(cfg.say.add) + '</button></div></article>';
    }).join('');
    box.closest('section').hidden = box.closest('section').hidden || !SETS.length;
  }

  /* ---------------------------------------------------------------- build your own */
  var TRAY = [];
  function drawHands() {
    var box = $('[data-hands]'); if (!box) return;
    box.innerHTML = [['R', 'Right hand'], ['L', 'Left hand']].map(function (h) {
      return '<button type="button" class="bf-chip" data-hand="' + h[0] + '" aria-pressed="' + (HAND === h[0]) + '">' + h[1] + '</button>'; }).join('');
  }
  function drawRows() {
    var box = $('[data-rows]'); if (!box) return;
    box.innerHTML = CLUBS.map(function (c, ci) {
      var vs = c.variants.filter(function (v) { return v.hand === HAND && (!c.finish || v.fin.toLowerCase() === c.finish.toLowerCase()); });
      if (!vs.length) return '';
      var price = Math.min.apply(null, vs.map(function (v) { return v.p; }));
      var chips = vs.length === 1
        ? (vs[0].a ? '<button type="button" class="bf-add" data-add="' + vs[0].id + '">Add</button>' : '<span class="bf-out">Sold out</span>')
        : vs.map(function (v) {
          var inTray = TRAY.filter(function (id) { return id === v.id; }).length;
          return '<button type="button" class="bf-chip' + (inTray ? ' is-in' : '') + '" data-add="' + v.id + '"' + (v.a ? '' : ' disabled aria-disabled="true"') + '>'
            + esc(v.label || 'Add') + (inTray ? ' <i>×' + inTray + '</i>' : '') + '</button>'; }).join('');
      return '<article class="bf-row"><a class="bf-row-ph" href="' + esc(c.url) + '"><img src="' + esc(c.img) + '" alt="' + esc(c.name) + '" loading="lazy"></a>'
        + '<div class="bf-row-bd"><h3><a href="' + esc(c.url) + '">' + esc(c.name) + '</a> <span>' + money(price) + '</span></h3>'
        + (c.line ? '<p>' + esc(c.line) + '</p>' : '')
        + '<div class="bf-chips">' + chips + '</div></div></article>';
    }).join('');
  }

  /* ---------------------------------------------------------------- the bar */
  var bar = document.querySelector('[data-bf-bar]');
  function drawBar() {
    if (!bar) return;
    var n = TRAY.length;
    bar.hidden = !n || phase === 'over';
    if (!n) return;
    var t = TRAY.reduce(function (a, id) { return a + BY[id].p; }, 0), cut = off(n);
    $('[data-bar-total]', bar).textContent = money(t - cut);
    $('[data-bar-sub]', bar).textContent = n + (n === 1 ? ' club' : ' clubs') + (cut ? ' · you save ' + money(cut) : '') + (n >= giftMin && !cfg.giftsGone ? ' · towel + divot free' : '');
    var nu = $('[data-bar-nudge]', bar), msg = n === 1 ? 'Add 1 more club and save $50.' : n === 2 ? 'Add 1 more and save $100 instead of $50.' : '';
    nu.textContent = msg; nu.hidden = !msg;
  }

  /* ---------------------------------------------------------------- add to bag */
  function track(items) {
    var value = items.reduce(function (a, i) { return a + BY[i.id].p * i.quantity; }, 0) / 100;
    try { if (window.fbq) fbq('track', 'AddToCart', { value: value, currency: 'USD', content_type: 'product', content_ids: items.map(function (i) { return String(i.id); }), num_items: items.length }); } catch (e) {}
  }
  function addIds(ids, btn) {
    var m = {}; ids.forEach(function (id) { m[id] = (m[id] || 0) + 1; });
    var items = Object.keys(m).map(function (id) { return { id: +id, quantity: m[id] }; });
    if (btn) btn.setAttribute('aria-busy', 'true');
    var go = window.LuckyBag && LuckyBag.add ? LuckyBag.add(items)
      : fetch('/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' }, body: JSON.stringify({ items: items }) })
        .then(function (r) { if (!r.ok) throw r; location.href = '/cart'; });
    return Promise.resolve(go).then(function () {
      track(items);
      if (btn) { var was = btn.textContent; btn.removeAttribute('aria-busy'); btn.textContent = 'In your bag'; setTimeout(function () { btn.textContent = was; }, 1800); }
    }).catch(function () { if (btn) { btn.removeAttribute('aria-busy'); btn.textContent = 'Try again'; } });
  }

  page.addEventListener('click', function (e) {
    var el;
    if (el = e.target.closest('[data-set]')) { var s = SETS[+el.getAttribute('data-set')]; if (s) addIds(s.vs.map(function (v) { return v.id; }), el); return; }
    if (el = e.target.closest('[data-hand]')) { HAND = el.getAttribute('data-hand'); try { localStorage.setItem('lg_hand', HAND); } catch (x) {} TRAY = []; drawHands(); drawRows(); drawSets(); drawBar(); return; }
    if (el = e.target.closest('[data-add]')) {
      var id = +el.getAttribute('data-add'); if (!BY[id] || !BY[id].a) return;
      var have = TRAY.indexOf(id);
      if (el.classList.contains('is-in') && have > -1) TRAY.splice(have, 1); else if (TRAY.length < 6) TRAY.push(id);
      drawRows(); drawBar(); return;
    }
  });
  if (bar) bar.addEventListener('click', function (e) {
    var b = e.target.closest('[data-bar-add]'); if (!b || !TRAY.length) return;
    addIds(TRAY.slice(), b).then(function () { TRAY = []; setTimeout(function () { drawRows(); drawBar(); }, 1800); });
  });

  /* Klaviyo's free-shipping pop-up covers the hero for postcard visitors; keep it off this page */
  new MutationObserver(function () {
    $$('div[role="dialog"][aria-label*="POPUP" i], .needsclick.kl-private-reset-css-Xuajs1', document).forEach(function (el) {
      if (el.closest('[data-bf-page]')) return;
      var root = el.closest('.needsclick') || el; root.style.display = 'none';
    });
  }).observe(document.body, { childList: true, subtree: true });

  drawHands(); drawSets(); drawRows(); drawBar();
})();
