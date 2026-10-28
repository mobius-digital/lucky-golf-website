/* The Black Friday page (sections/lg-bfcm.liquid). Round 4.
   Phase from the clock (Central time), the countdown (last 48h only), the mail code applied for postcard visitors,
   deal cards that add a whole set, club cards with loft chips that fill a tray, the bar as the receipt,
   polo add, and the join-the-list form (Klaviyo client API).
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
  var lad1 = $('[data-lad-1]'); if (lad1 && giftMin === 1) lad1.textContent = cfg.say.lad1Mail;

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
  var low = function (vs) { return vs.some(isLow); };
  /* a whole card is "running low" only when most of its lofts are */
  var lowRow = function (vs) { var a = vs.filter(function (v) { return v.a; }); return a.length > 0 && a.filter(isLow).length * 2 > a.length; };
  var pieceName = function (v) { return v.loft ? v.loft.replace(/^(\d+)(\w)$/, '$1° $2') + (v.fin ? ' ' + v.fin : '') : v.club.name; };
  var TRAY = [];

  /* ---------------------------------------------------------------- deal cards that add a set */
  function resolve(tok) {
    var p = tok.trim().split(':');
    var loft = p[1] ? p[1].toUpperCase() : '', fin = p[2] || '';
    var all = []; CLUBS.forEach(function (x) { if (x.key === p[0]) all = all.concat(x.variants); });
    return all.filter(function (v) { return v.hand === HAND && (!loft || v.loft === loft) && (!fin || v.fin.toLowerCase() === fin.toLowerCase()) && v.a; })[0] || null;
  }
  var SETS = {};
  function drawCards() {
    $$('[data-card]').forEach(function (card, i) {
      var toks = (card.getAttribute('data-pieces') || '').split(',').map(function (t) { return t.trim(); }).filter(Boolean);
      if (!toks.length) return;
      var vs = toks.map(resolve);
      var pr = $('[data-card-price]', card), ul = $('[data-card-pieces]', card), btn = $('[data-card-add]', card), lo = $('[data-card-low]', card);
      if (vs.some(function (v) { return !v; })) { card.hidden = true; return; }
      var n = vs.length, t = vs.reduce(function (a, v) { return a + v.p; }, 0), cut = off(n);
      SETS[i] = vs; card.setAttribute('data-set', i);
      if (pr) pr.innerHTML = '<b>' + money(t - cut) + '</b> <s>' + money(t) + '</s>' + (t - cut >= cfg.ship ? '<small>Ships free</small>' : '');
      if (ul) { ul.innerHTML = vs.map(function (v) { return '<li>' + esc(pieceName(v)) + '</li>'; }).join(''); ul.hidden = false; }
      if (lo) lo.hidden = !low(vs);
      if (btn) btn.hidden = phase === 'over';
    });
  }

  /* ---------------------------------------------------------------- club cards with loft chips */
  function drawHands() {
    var box = $('[data-hands]'); if (!box) return;
    box.innerHTML = [['R', 'Right hand'], ['L', 'Left hand']].map(function (h) {
      return '<button type="button" class="bf-chip" data-hand="' + h[0] + '" aria-pressed="' + (HAND === h[0]) + '">' + h[1] + '</button>'; }).join('');
  }
  function cardHtml(c) {
    var vs = c.variants.filter(function (v) { return v.hand === HAND && (!c.finish || v.fin.toLowerCase() === c.finish.toLowerCase()); });
    if (!vs.length) return '';
    var price = Math.min.apply(null, vs.map(function (v) { return v.p; }));
    var chips = vs.length === 1
      ? (vs[0].a ? '<button type="button" class="bf-add' + (TRAY.indexOf(vs[0].id) > -1 ? ' is-in' : '') + '" data-add="' + vs[0].id + '">' + (TRAY.indexOf(vs[0].id) > -1 ? 'In the tray' : 'Add to set') + '</button>' : '<span class="bf-out">Sold out</span>')
      : vs.map(function (v) {
        var inTray = TRAY.filter(function (id) { return id === v.id; }).length;
        return '<button type="button" class="bf-chip' + (inTray ? ' is-in' : '') + '" data-add="' + v.id + '"' + (v.a ? '' : ' disabled aria-disabled="true"') + '>'
          + esc(v.label || 'Add') + (inTray ? ' <i>×' + inTray + '</i>' : '') + '</button>'; }).join('');
    return '<article class="bf-pc' + (c.drop ? ' is-drop' : '') + '"><a class="bf-pc-ph" href="' + esc(c.url) + '"><img src="' + esc(c.img) + '" alt="' + esc(c.name) + '" loading="lazy">'
      + (c.drop ? '<i class="bf-st is-on">New</i>' : lowRow(vs) ? '<i class="bf-st is-low">Running low</i>' : '') + '</a>'
      + '<div class="bf-pc-bd"><h3><a href="' + esc(c.url) + '">' + esc(c.name) + '</a> <span>' + money(price) + '</span></h3>'
      + (c.line ? '<p>' + esc(c.line) + '</p>' : '')
      + '<div class="bf-chips">' + chips + '</div></div></article>';
  }
  function drawRows() {
    $$('[data-rows]').forEach(function (box) {
      var g = box.getAttribute('data-rows');
      box.innerHTML = CLUBS.filter(function (c) { return c.drop ? (g === 'putters' && phase !== 'mail') : c.group === g; }).map(cardHtml).join('');
    });
  }

  /* ---------------------------------------------------------------- the bar is the receipt */
  var bar = document.querySelector('[data-bf-bar]');
  function drawBar() {
    if (!bar) return;
    var n = TRAY.length;
    bar.hidden = !n || phase === 'over';
    page.classList.toggle('has-bar', !bar.hidden);
    if (!n) return;
    var t = TRAY.reduce(function (a, id) { return a + BY[id].p; }, 0), cut = off(n);
    $('[data-bar-total]', bar).textContent = money(t - cut);
    $('[data-bar-sub]', bar).textContent = n + (n === 1 ? ' club' : ' clubs') + (cut ? ' · you save ' + money(cut) : '') + (n >= giftMin && !cfg.giftsGone ? ' · towel + divot free' : '') + (t - cut >= cfg.ship ? ' · ships free' : '');
    var nu = $('[data-bar-nudge]', bar), msg = n === 1 ? 'One more club and $50 comes off.' : n === 2 ? 'One more: $100 off and it ships free.' : '';
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
    if (el = e.target.closest('[data-card-add]')) { var s = SETS[+el.closest('[data-set]').getAttribute('data-set')]; if (s) addIds(s.map(function (v) { return v.id; }), el); return; }
    if (el = e.target.closest('[data-polo]')) { addIds([+el.getAttribute('data-polo')], el); return; }
    if (el = e.target.closest('[data-hand]')) { HAND = el.getAttribute('data-hand'); try { localStorage.setItem('lg_hand', HAND); } catch (x) {} TRAY = []; drawHands(); drawRows(); drawCards(); drawBar(); return; }
    if (el = e.target.closest('[data-add]')) {
      var id = +el.getAttribute('data-add'); if (!BY[id] || !BY[id].a) return;
      var have = TRAY.indexOf(id);
      if (el.classList.contains('is-in') && have > -1) TRAY.splice(have, 1); else if (TRAY.length < 6) TRAY.push(id);
      drawRows(); drawBar(); return;
    }
  });
  if (bar) bar.addEventListener('click', function (e) {
    var b = e.target.closest('[data-bar-add]'); if (!b || !TRAY.length) return;
    addIds(TRAY.slice(), b).then(emptyTray);
  });

  /* ---------------------------------------------------------------- join the list (Klaviyo client API, same as the giveaway page) */
  var form = $('[data-bf-form]');
  if (form && cfg.klaviyo.key && cfg.klaviyo.list) form.addEventListener('submit', function (e) {
    e.preventDefault();
    var em = form.querySelector('[name=email]'), msg = $('[data-bf-form-msg]'), email = em.value.trim();
    var say = function (t) { msg.textContent = t; msg.hidden = !t; };
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { say('That email looks off. Try it again?'); em.focus(); return; }
    var btn = form.querySelector('[type=submit]'); btn.disabled = true;
    fetch('https://a.klaviyo.com/client/subscriptions/?company_id=' + encodeURIComponent(cfg.klaviyo.key), {
      method: 'POST', headers: { 'Content-Type': 'application/vnd.api+json', 'revision': '2025-07-15' },
      body: JSON.stringify({ data: { type: 'subscription', attributes: { custom_source: 'Black Friday page',
        profile: { data: { type: 'profile', attributes: { email: email, subscriptions: { email: { marketing: { consent: 'SUBSCRIBED' } } } } } } },
        relationships: { list: { data: { type: 'list', id: cfg.klaviyo.list } } } } })
    }).then(function (r) { if (!r.ok && r.status !== 202) throw r; say('You\'re on it. Watch your inbox.'); em.value = ''; try { if (window.fbq) fbq('track', 'Lead'); } catch (x) {} })
      .catch(function () { say('That didn\'t go through. Try once more?'); btn.disabled = false; });
  });

  /* Klaviyo's free-shipping pop-up covers the hero for postcard visitors; keep it off this page */
  new MutationObserver(function () {
    $$('div[role="dialog"][aria-label*="POPUP" i], .needsclick.kl-private-reset-css-Xuajs1', document).forEach(function (el) {
      if (el.closest('[data-bf-page]')) return;
      var root = el.closest('.needsclick') || el; root.style.display = 'none';
    });
  }).observe(document.body, { childList: true, subtree: true });

  drawHands(); drawCards(); drawRows(); drawBar();
})();
