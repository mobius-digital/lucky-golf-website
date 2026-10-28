/* The Black Friday page (sections/lg-bfcm.liquid). Round 5.
   Phase from the clock (Central time), the countdown (last 48h only), the mail code applied for postcard visitors,
   deal cards that price a set and open the choose-your-lofts sheet, a tabbed shop whose cards fill a tray, the ladder
   meter, the bar as the receipt, polo add, and the two list forms (Klaviyo client API).
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
  if (giftMin === 1) {
    var lad1 = $('[data-lad-1]'); if (lad1) lad1.textContent = cfg.say.lad1Mail;
    $$('[data-bf-gift-at]').forEach(function (el) { el.textContent = cfg.say.plusMail; });
  }

  /* ---------------------------------------------------------------- clock: only inside the last N hours */
  var clock = $('[data-bf-clock]'), ends = $('[data-bf-ends]'), end = Date.parse(cfg.end);
  var two = function (n) { return (n < 10 ? '0' : '') + n; };
  function tick() {
    if (!clock || !end) return;
    var left = end - Date.now(), show = left > 0 && left <= cfg.clockHours * 3600000;
    clock.hidden = !show; if (ends) ends.hidden = show;
    if (!show) return;
    var t = Math.floor(left / 1000);
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
  var member = !!want || !!q.get('utm_medium') && /email|sms/i.test(q.get('utm_medium'));
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
  var listBox = $('[data-bf-list]'); if (listBox) listBox.hidden = member;

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
  var isLow = function (v) { return v.a && v.q > 0 && v.q < cfg.lowAt; };
  var lowRow = function (vs) { var a = vs.filter(function (v) { return v.a; }); return a.length > 0 && a.filter(isLow).length * 2 > a.length; };
  var pieceName = function (v) { return (v.loft ? v.loft.replace(/^(\d+)(\w)$/, '$1° $2') + (v.fin ? ' ' + v.fin : '') + ' ' : '') + v.club.name.replace(/ 02 (Gold|Black)$/, ' 02'); };
  var CH = {};
  var handOf = function (c) { return CH[c.key] || HAND; };
  var clubVariants = function (c, fin, h) { var hh = h || HAND; return c.variants.filter(function (v) { return v.hand === hh && (!(c.finish || fin) || v.fin.toLowerCase() === (c.finish || fin).toLowerCase()); }); };
  var TRAY = [];
  var giftsWorth = function () { return cfg.worth.towel + cfg.worth.divot; };

  /* ---------------------------------------------------------------- deal cards: price the set, open the loft sheet */
  /* a piece = { club, fin, loft, v (fixed variant) | opts (variants to pick from) } */
  function piece(tok) {
    var p = tok.trim().split(':'), loft = (p[1] || '').toUpperCase(), fin = p[2] || '';
    var cs = CLUBS.filter(function (x) { return x.key === p[0] && (!fin || !x.finish || x.finish.toLowerCase() === fin.toLowerCase()); });
    if (!cs.length) return null;
    var opts = []; cs.forEach(function (x) { opts = opts.concat(clubVariants(x, fin)); });
    opts = opts.filter(function (v) { return v.a; });
    if (!opts.length) return null;
    if (loft) { var v = opts.filter(function (x) { return x.loft === loft; })[0]; return v ? { club: v.club, v: v, opts: [v] } : null; }
    return { club: cs[0], v: opts.length === 1 ? opts[0] : null, opts: opts };
  }
  /* same wedge three times: start them four degrees apart (50/54/58), not all on the first loft */
  function spread(ps) {
    var groups = {};
    ps.forEach(function (p, j) { if (!p.v && p.opts.length > 1) { var k = p.club.key + '|' + p.opts[0].fin; (groups[k] = groups[k] || []).push(j); } });
    Object.keys(groups).forEach(function (k) {
      var idx = groups[k], opts = ps[idx[0]].opts, n = idx.length;
      var want = n === 3 ? ['50K', '54K', '58K'] : n === 2 ? ['54K', '58K'] : ['56K'];
      idx.forEach(function (j, i) {
        var v = opts.filter(function (o) { return o.loft === want[i]; })[0] || opts[Math.min(opts.length - 1, Math.round(i * (opts.length - 1) / Math.max(1, n - 1)))];
        ps[j].pick = v;
      });
    });
    return ps;
  }
  function setSaving(ps) {
    var n = ps.length, cut = off(n), gifts = n >= giftMin ? giftsWorth() : 0;
    var cover = ps.some(function (p) { return p.club.cover; }) ? cfg.worth.cover : 0;
    return { cut: cut, gifts: gifts, cover: cover, total: cut + gifts + cover };
  }
  var SETS = {};
  function drawCards() {
    $$('[data-card]').forEach(function (card, i) {
      var soon = (card.getAttribute('data-soon') || '').split(' ').indexOf(phase) > -1;
      var live = $('[data-card-live]', card), soonEl = $('[data-card-soon]', card), btn = $('[data-card-btn]', card), sbtn = $('[data-card-btn-soon]', card);
      if (live) live.hidden = soon; if (soonEl) soonEl.hidden = !soon; if (btn) btn.hidden = soon; if (sbtn) sbtn.hidden = !soon;
      card.classList.toggle('is-soon', soon);
      var toks = (card.getAttribute('data-pieces') || '').split(',').map(function (t) { return t.trim(); }).filter(Boolean);
      if (!toks.length) return;
      var ps = toks.map(piece);
      if (ps.some(function (p) { return !p; })) { card.hidden = true; return; }
      ps = spread(ps);
      SETS[i] = ps; card.setAttribute('data-set', i);
      var n = ps.length, t = ps.reduce(function (a, p) { return a + (p.v || p.pick || p.opts[0]).p; }, 0);
      var sv = setSaving(ps);
      var pr = $('[data-card-price]', card); if (pr) pr.innerHTML = '<b>' + money(t - sv.cut) + '</b><s>' + money(t) + '</s>' + (t - sv.cut >= cfg.ship ? '<em>Ships free</em>' : '');
      var sl = $('[data-card-save]', card);
      if (sl) {
        var bits = [money(sv.cut) + ' off'];
        if (sv.gifts) bits.push('towel + divot tool'); else if (n >= giftMin && !cfg.giftsGone) bits.push('towel + divot tool');
        if (sv.cover) bits.push('head cover');
        sl.innerHTML = '<b>You save ' + money(sv.total) + '</b>' + (bits.length > 1 ? '<span>' + esc(bits.join(' + ')) + '</span>' : '');
      }
      var kit = $('[data-card-kit]', card);
      if (kit) {
        var cnt = {}, order = [];
        ps.forEach(function (p) { var nm = p.club.name; if (!cnt[nm]) { cnt[nm] = 0; order.push(nm); } cnt[nm]++; });
        var chips = order.map(function (nm) { return '<i>' + (cnt[nm] > 1 ? cnt[nm] + ' × ' : '') + esc(nm) + '</i>'; });
        if (n >= giftMin && !cfg.giftsGone) chips.push('<i class="is-free">Free towel</i>', '<i class="is-free">Free divot tool</i>');
        if (sv.cover) chips.push('<i class="is-free">Free head cover</i>');
        kit.innerHTML = chips.join('');
      }
      var lo = $('[data-card-low]', card); if (lo) lo.hidden = soon || !ps.some(function (p) { return p.v ? isLow(p.v) : lowRow(p.opts); });
    });
  }

  /* ---------------------------------------------------------------- the loft sheet */
  var sheet = $('[data-sheet]'), CUR = null;
  function openSheet(i, name) {
    CUR = SETS[i].map(function (p) { return { club: p.club, opts: p.opts, v: p.v || p.pick || p.opts[0] }; });
    $('[data-sheet-name]').textContent = name;
    var ln = $('[data-sheet-line]'); if (ln && ln.getAttribute('data-was')) ln.textContent = ln.getAttribute('data-was');
    sheetMode(false); drawHands(); drawSheet();
    sheet.hidden = false; document.body.classList.add('bf-lock');
    setTimeout(function () { var f = $('select, button', $('[data-sheet-rows]')); if (f) f.focus(); }, 50);
  }
  function closeSheet() { sheet.hidden = true; document.body.classList.remove('bf-lock'); CUR = null; sheet.classList.remove('is-next'); sheetMode(false); }
  function sheetMode(next) {
    ['[data-hands]', '[data-sheet-rows]', '[data-sheet-lines]', '.bf-r-total', '[data-sheet-add]'].forEach(function (q) { var el = $(q, sheet); if (el) el.hidden = next; });
    var f = $('[data-sheet-form]', sheet); if (f) f.hidden = !next;
  }
  function openNext() {
    var nc = $('[data-next]'); if (!nc) return;
    $('[data-sheet-name]').textContent = $('.bf-card-name', nc).textContent;
    var ln = $('[data-sheet-line]'); if (ln) { ln.setAttribute('data-was', ln.getAttribute('data-was') || ln.textContent); ln.textContent = $('.bf-card-line', nc).textContent; }
    sheetMode(true); sheet.classList.add('is-next'); sheet.hidden = false; document.body.classList.add('bf-lock');
    setTimeout(function () { var f = $('[data-sheet-form] input', sheet); if (f) f.focus(); }, 50);
  }
  function drawSheet() {
    if (!CUR) return;
    $('[data-sheet-rows]').innerHTML = CUR.map(function (p, j) {
      var pick = p.opts.length > 1
        ? '<select class="bf-sel" data-sheet-pick="' + j + '" aria-label="Loft">' + p.opts.map(function (v) { return '<option value="' + v.id + '"' + (v.id === p.v.id ? ' selected' : '') + '>' + esc(v.label) + (isLow(v) ? ' · running low' : '') + '</option>'; }).join('') + '</select>'
        : '<span class="bf-fixed">' + esc(p.v.label || p.club.name) + '</span>';
      return '<div class="bf-sheet-row"><img src="' + esc(p.club.img) + '" alt=""><div><b><a href="' + esc(p.club.url) + '">' + esc(p.club.name) + '</a></b>' + (p.club.cover ? '<small>Free head cover</small>' : '') + '</div>' + pick + '<span>' + money(p.v.p) + '</span></div>';
    }).join('');
    var n = CUR.length, t = CUR.reduce(function (a, p) { return a + p.v.p; }, 0), sv = setSaving(CUR), lines = [];
    if (sv.cut) lines.push(['Black Friday, ' + n + (n >= 3 ? '+' : '') + ' clubs', '−' + money(sv.cut), 'is-cut']);
    if (!cfg.giftsGone) lines.push(['Towel + divot tool', n >= giftMin ? 'Free' : '2+ clubs', n >= giftMin ? 'is-free' : 'is-dim']);
    if (CUR.some(function (p) { return p.club.cover; })) lines.push(['Head cover', 'Free', 'is-free']);
    lines.push(['Shipping', t - sv.cut >= cfg.ship ? 'Free' : 'From $18', t - sv.cut >= cfg.ship ? 'is-free' : 'is-dim']);
    $('[data-sheet-lines]').innerHTML = lines.map(function (l) { return '<li class="' + l[2] + '"><span>' + esc(l[0]) + '</span><b>' + esc(l[1]) + '</b></li>'; }).join('');
    $('[data-sheet-total]').textContent = money(t - sv.cut);
  }

  /* ---------------------------------------------------------------- the shop: tabs, cards, meter */
  function drawHands() {
    $$('[data-hands]').forEach(function (box) {
      box.innerHTML = [['R', 'Right'], ['L', 'Left']].map(function (h) {
        return '<button type="button" class="bf-chip" data-hand="' + h[0] + '" aria-pressed="' + (HAND === h[0]) + '">' + h[1] + ' hand</button>'; }).join('');
    });
  }
  function cardHtml(c) {
    var hd = handOf(c), vs = clubVariants(c, null, hd);
    if (!vs.length) return '';
    var price = Math.min.apply(null, vs.map(function (v) { return v.p; }));
    var inTray = TRAY.filter(function (id) { return BY[id].club === c; }).length;
    var pick = vs.length > 1
      ? '<select class="bf-sel" data-pick aria-label="Loft">' + vs.map(function (v) { return '<option value="' + v.id + '"' + (v.a ? '' : ' disabled') + '>' + esc(v.label) + (v.a ? (isLow(v) ? ' · running low' : '') : ' · sold out') + '</option>'; }).join('') + '</select>'
      : (vs[0].a ? '<input type="hidden" data-pick value="' + vs[0].id + '">' : '<span class="bf-out">Sold out</span>');
    var can = vs.some(function (v) { return v.a; });
    return '<article class="bf-pc' + (c.drop ? ' is-drop' : '') + '"><a class="bf-pc-ph" href="' + esc(c.url) + '"><img src="' + esc(c.img) + '" alt="' + esc(c.name) + '" loading="lazy">'
      + (c.drop ? '<i class="bf-st is-on">New</i>' : lowRow(vs) ? '<i class="bf-st is-low">Running low</i>' : '') + '</a>'
      + '<div class="bf-pc-bd"><h3><a href="' + esc(c.url) + '">' + esc(c.name) + '</a> <span>' + money(price) + '</span></h3>'
      + (c.stars ? '<i class="bf-stars">' + c.stars + ' ★</i>' : '')
      + (c.line ? '<p>' + esc(c.line) + (c.cover ? ' Cover on us.' : '') + '</p>' : '')
      + '<div class="bf-hand" role="group" aria-label="Hand">' + [['R', 'Right hand'], ['L', 'Left hand']].map(function (h) { return '<button type="button" data-chand="' + h[0] + '" data-ckey="' + esc(c.key) + '" aria-pressed="' + (hd === h[0]) + '">' + h[1] + '</button>'; }).join('') + '</div>'
      + '<div class="bf-pick">' + pick + (can ? '<button type="button" class="bf-add' + (inTray ? ' is-in' : '') + '" data-add>' + (inTray ? 'Added ×' + inTray : 'Add to set') + '</button>' : '') + '</div></div></article>';
  }
  function drawRows() {
    $$('[data-rows]').forEach(function (box) {
      var g = box.getAttribute('data-rows'); if (g === 'apparel') return;
      box.innerHTML = CLUBS.filter(function (c) { return c.drop ? (g === 'putters' && phase !== 'mail') : c.group === g; }).map(cardHtml).join('');
    });
  }
  function showTab(t) {
    $$('[data-tab]').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-tab') === t)); });
    $$('[data-rows]').forEach(function (box) { box.hidden = box.getAttribute('data-rows') !== t; });
  }
  /* the deals: one wide card at a time; arrows on desktop, the swipe on phones, dots for both */
  var cars = $('[data-cars]'), track = cars && $('[data-cards]', cars), dots = cars && $('[data-cars-dots]', cars);
  function carsCards() { return track ? $$('.bf-card', track).filter(function (c) { return !c.hidden && c.offsetParent !== null; }) : []; }
  function carsIdx() { var cs = carsCards(); if (!cs.length) return 0; var x = track.scrollLeft, best = 0; cs.forEach(function (c, i) { if (Math.abs(c.offsetLeft - x) < Math.abs(cs[best].offsetLeft - x)) best = i; }); return best; }
  function drawCars() {
    if (!cars) return;
    var cs = carsCards(), i = CI < 0 ? carsIdx() : CI;
    if (dots) dots.innerHTML = cs.map(function (c, j) { return '<i' + (j === i ? ' class="is-on"' : '') + '></i>'; }).join('');
    var pv = $('[data-cars-prev]', cars), nx = $('[data-cars-next]', cars);
    if (pv) pv.disabled = i <= 0; if (nx) nx.disabled = i >= cs.length - 1;
  }
  var CI = -1;
  function carsGo(d) { var cs = carsCards(), i = Math.max(0, Math.min(cs.length - 1, (CI < 0 ? carsIdx() : CI) + d)); CI = i; if (cs[i]) track.scrollTo({ left: cs[i].offsetLeft - track.offsetLeft, behavior: 'smooth' }); setTimeout(drawCars, 450); }
  if (track) { var tmr; track.addEventListener('scroll', function () { clearTimeout(tmr); tmr = setTimeout(function () { CI = -1; drawCars(); }, 160); }, { passive: true }); }
  function drawMeter() {
    var n = TRAY.length;
    $$('[data-m]').forEach(function (li) { var k = +li.getAttribute('data-m'); li.classList.toggle('is-on', n >= k && (k < 3 || n >= 3)); li.classList.toggle('is-next', n + 1 === k); });
  }

  /* ---------------------------------------------------------------- the bar is the receipt */
  var bar = document.querySelector('[data-bf-bar]');
  function drawBar() {
    drawMeter();
    if (!bar) return;
    var n = TRAY.length;
    bar.hidden = !n || phase === 'over';
    page.classList.toggle('has-bar', !bar.hidden);
    if (!n) return;
    var t = TRAY.reduce(function (a, id) { return a + BY[id].p; }, 0), cut = off(n);
    $('[data-bar-total]', bar).textContent = money(t - cut);
    $('[data-bar-sub]', bar).textContent = n + (n === 1 ? ' club' : ' clubs') + (cut ? ' · ' + money(cut) + ' off' : '') + (n >= giftMin && !cfg.giftsGone ? ' · towel + divot free' : '') + (t - cut >= cfg.ship ? ' · ships free' : '');
    var nu = $('[data-bar-nudge]', bar), msg = n === 1 ? 'One more club: $50 off' + (giftMin === 2 && !cfg.giftsGone ? ', towel and divot tool on us.' : '.') : n === 2 ? 'One more: $100 off and it ships free.' : '';
    nu.textContent = msg; nu.hidden = !msg;
  }

  /* ---------------------------------------------------------------- add to bag */
  function track(items) {
    var value = items.reduce(function (a, i) { return a + (BY[i.id] ? BY[i.id].p : 0) * i.quantity; }, 0) / 100;
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
  function emptyTray() { TRAY = []; setTimeout(function () { drawRows(); drawBar(); }, 1800); }

  page.addEventListener('click', function (e) {
    var el;
    if (el = e.target.closest('[data-card][data-set]')) {
      if (el.classList.contains('is-soon')) { if (listBox) { listBox.hidden = false; listBox.scrollIntoView({ behavior: 'smooth' }); } return; }
      openSheet(+el.getAttribute('data-set'), el.getAttribute('data-name')); return;
    }
    if (el = e.target.closest('[data-cars-prev]')) { carsGo(-1); return; }
    if (el = e.target.closest('[data-cars-next]')) { carsGo(1); return; }
    if (el = e.target.closest('[data-card][data-next]')) { openNext(); return; }
    if (el = e.target.closest('a[data-card].is-soon')) { e.preventDefault(); if (listBox) { listBox.hidden = false; listBox.scrollIntoView({ behavior: 'smooth' }); } return; }
    if (e.target.closest('[data-sheet-close]')) { closeSheet(); return; }
    if (el = e.target.closest('[data-sheet-add]')) { if (CUR) addIds(CUR.map(function (p) { return p.v.id; }), el).then(function () { setTimeout(closeSheet, 1200); }); return; }
    if (el = e.target.closest('[data-tab]')) { showTab(el.getAttribute('data-tab')); return; }
    if (el = e.target.closest('[data-chand]')) { CH[el.getAttribute('data-ckey')] = el.getAttribute('data-chand'); drawRows(); return; }
    if (el = e.target.closest('[data-gtab]')) { var g = el.getAttribute('data-gtab'); $$('[data-gtab]').forEach(function (b) { b.setAttribute('aria-selected', String(b === el)); }); $$('[data-grow]').forEach(function (r) { r.hidden = r.getAttribute('data-grow') !== g; }); return; }
    if (el = e.target.closest('[data-row-prev],[data-row-next]')) { var tr = $('[data-row-track]', el.closest('[data-grow]')); tr.scrollBy({ left: (el.hasAttribute('data-row-next') ? 1 : -1) * tr.clientWidth * .9, behavior: 'smooth' }); return; }
    if (el = e.target.closest('[data-hand]')) {
      HAND = el.getAttribute('data-hand'); try { localStorage.setItem('lg_hand', HAND); } catch (x) {}
      TRAY = []; drawHands(); drawRows(); drawCards(); drawBar();
      if (CUR) { CUR = CUR.map(function (p) { var fresh = piece(p.club.key + ':' + (p.opts.length === 1 ? p.v.loft : '') + ':' + (p.v.fin || '')); return fresh ? { club: fresh.club, opts: fresh.opts, v: fresh.v || fresh.opts[0] } : p; }); drawSheet(); }
      return;
    }
    if (el = e.target.closest('[data-add]')) {
      var pc = el.closest('.bf-pc'), pk = $('[data-pick]', pc), id = pk ? +pk.value : 0;
      if (!BY[id] || !BY[id].a) return;
      if (TRAY.length < 6) TRAY.push(id);
      drawRows(); drawBar(); return;
    }
    if (el = e.target.closest('[data-polo-add]')) { var sel = $('select', el.closest('.bf-pc')); if (sel && sel.value) addIds([+sel.value], el); return; }
  });
  page.addEventListener('change', function (e) {
    var sel = e.target.closest('[data-sheet-pick]'); if (!sel || !CUR) return;
    var p = CUR[+sel.getAttribute('data-sheet-pick')]; p.v = BY[+sel.value] || p.v; drawSheet();
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && CUR) closeSheet(); });
  if (bar) bar.addEventListener('click', function (e) {
    var b = e.target.closest('[data-bar-add]'); if (!b || !TRAY.length) return;
    addIds(TRAY.slice(), b).then(emptyTray);
  });

  /* ---------------------------------------------------------------- the lists (Klaviyo client API, same as the giveaway page) */
  $$('[data-bf-form]').forEach(function (form) {
    var list = form.getAttribute('data-list') || cfg.klaviyo.list;
    if (!cfg.klaviyo.key || !list) return;
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var em = form.querySelector('[name=email]'), msg = $('[data-bf-form-msg]', form), email = em.value.trim();
      var say = function (t) { msg.textContent = t; msg.hidden = !t; };
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { say('That email looks off. Try it again?'); em.focus(); return; }
      var btn = form.querySelector('[type=submit]'); btn.disabled = true;
      fetch('https://a.klaviyo.com/client/subscriptions/?company_id=' + encodeURIComponent(cfg.klaviyo.key), {
        method: 'POST', headers: { 'Content-Type': 'application/vnd.api+json', 'revision': '2025-07-15' },
        body: JSON.stringify({ data: { type: 'subscription', attributes: { custom_source: form.getAttribute('data-source') || 'Black Friday page',
          profile: { data: { type: 'profile', attributes: { email: email, subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } } } } } },
          relationships: { list: { data: { type: 'list', id: list } } } } })
      }).then(function (r) { if (!r.ok && r.status !== 202) throw r; say('You\'re on it. Watch your inbox.'); em.value = ''; try { if (window.fbq) fbq('track', 'Lead'); } catch (x) {} })
        .catch(function () { say('That didn\'t go through. Try once more?'); btn.disabled = false; });
    });
  });

  /* Klaviyo's free-shipping pop-up covers the hero for postcard visitors; keep it off this page */
  new MutationObserver(function () {
    $$('div[role="dialog"][aria-label*="POPUP" i], .needsclick.kl-private-reset-css-Xuajs1', document).forEach(function (el) {
      if (el.closest('[data-bf-page]')) return;
      var root = el.closest('.needsclick') || el; root.style.display = 'none';
    });
  }).observe(document.body, { childList: true, subtree: true });

  drawHands(); drawCards(); drawRows(); showTab('wedges'); drawBar(); drawCars();
  window.addEventListener('resize', drawCars);
})();
