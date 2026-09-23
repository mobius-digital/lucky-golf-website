/* ==========================================================================
   LUCKY GOLF · lucky.js · v4.0 · the behaviour that goes with lucky.css.

   Four things, none of them page-specific:

     Lucky.guide   Mags in the corner: one line, one next step, tap = do it.
     Lucky.pop     the "check out or keep going?" question, which shrinks
                   into Mags when it closes.
     Lucky.toast   news that isn't a question. Mags only on good news.
     Lucky.hole    the progress bar (tee, flags at real thresholds, the ball).
     Lucky.tracer  the launch-monitor arc, built from the same real stops.

   Set Mags's art once, before anything else:
     Lucky.mags = { ink: '…/gwp-mags-ink.webp', light: '…/gwp-mags.webp' };

   Nothing here writes a colour or a size: that is lucky.css's job. Nothing
   here fetches the cart either: the page decides WHAT to say, this file
   only says it.
   ========================================================================== */
(function () {
  'use strict';
  var Lucky = window.Lucky = window.Lucky || {};
  Lucky.mags = Lucky.mags || { ink: '', light: '' };

  function calm() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function el(tag, cls, parent) { var e = document.createElement(tag); if (cls) e.className = cls; if (parent) parent.appendChild(e); return e; }
  function magsArt(parent) {
    var s = el('span', 'lg-mags', parent);
    var a = el('img', 'is-ink', s); a.src = Lucky.mags.ink; a.alt = '';
    var b = el('img', 'is-light', s); b.src = Lucky.mags.light || Lucky.mags.ink; b.alt = '';
    return s;
  }
  /* the nearest ground, so a guide or pop-up built in <body> still matches its page */
  function groundOf(host) {
    var g = host && host.closest && host.closest('[data-ground]');
    return g ? g.getAttribute('data-ground') : null;
  }
  function go(action) {
    if (!action) return;
    if (typeof action === 'function') return action();
    if (typeof action === 'string') {
      if (action.charAt(0) === '#') return Lucky.jump(action.slice(1));
      window.location.href = action;
    }
  }

  /* A smooth jump that respects reduced motion, and a gold pulse on arrival. */
  Lucky.jump = function (id) {
    var t = document.getElementById(id);
    if (!t) return;
    t.scrollIntoView({ behavior: calm() ? 'auto' : 'smooth', block: t.hasAttribute('data-center') ? 'center' : 'start' });
    if (!t.hasAttribute('tabindex')) t.setAttribute('tabindex', '-1');
    t.focus({ preventScroll: true });
  };

  /* ------------------------------------------------------------ the guide
     Lucky.guide.say('Tap me to check out.', '/checkout')
     Lucky.guide.say("The hat's free. Tap me and I'll show you.", '#gift-hat')
     Lucky.guide.hide()
     options (Lucky.guide.init): host (element whose ground to match),
       avoid (elements Mags should stand above when they reach the bottom
       of the screen, e.g. a sticky bar), lift (px above the bottom on phones). */
  var G = { el: null, sayEl: null, action: null, text: '', opts: {} };
  Lucky.guide = {
    init: function (opts) {
      G.opts = opts || {};
      if (G.el) return G.el;
      G.el = el('button', 'lg-guide', document.body);
      G.el.type = 'button'; G.el.hidden = true;
      var g = groundOf(G.opts.host); if (g) G.el.setAttribute('data-ground', g);
      magsArt(G.el);
      G.sayEl = el('span', 'lg-guide-say', G.el);
      G.sayEl.setAttribute('aria-live', 'polite');
      if (G.opts.lift != null) G.el.style.setProperty('--lg-guide-lift', G.opts.lift + 'px');
      G.el.addEventListener('click', function () { go(G.action); });
      var raf = null;
      var lift = function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(Lucky.guide.place); };
      window.addEventListener('scroll', lift, { passive: true });
      window.addEventListener('resize', lift);
      return G.el;
    },
    say: function (text, action) {
      Lucky.guide.init(G.opts);
      var changed = text !== G.text || G.el.hidden;
      G.text = text; G.action = action;
      G.sayEl.textContent = text;
      G.el.hidden = false;
      Lucky.guide.place();
      if (changed) Lucky.guide.hop();
    },
    hide: function () { if (G.el) G.el.hidden = true; G.text = ''; },
    hop: function () {
      if (!G.el || calm()) return;
      G.el.classList.remove('is-hop'); void G.el.offsetWidth; G.el.classList.add('is-hop');
    },
    /* Stand on top of any bar that has reached the bottom of the screen. */
    place: function () {
      if (!G.el || G.el.hidden) return;
      var lift = 0, vh = window.innerHeight;
      (G.opts.avoid || []).forEach(function (a) {
        if (!a) return;
        var r = a.getBoundingClientRect();
        if (r.height && r.top < vh && r.bottom > vh - 120) lift = Math.max(lift, vh - r.top + 12 - 24);
      });
      G.el.style.transform = lift ? 'translateY(' + (-lift) + 'px)' : '';
    },
    el: function () { return G.el; }
  };

  /* -------------------------------------------------------------- the pop
     Lucky.pop.open({
       title: "The hat's in your bag.",
       body:  "Check out now, or add $41 more and the polo's free too.",
       primary:   { label: 'Check out', href: '/checkout' },
       secondary: { label: 'Add more for the polo', action: '#clubs' },
       once: 'hat'            // optional: never ask the same question twice a visit
     });
     Closing (the x, Escape, the backdrop, the secondary button) shrinks the
     card into the guide if it is on screen. */
  var P = { el: null, seen: {}, last: null };
  function buildPop() {
    P.el = el('div', 'lg-pop', document.body);
    P.el.hidden = true;
    P.el.setAttribute('role', 'dialog'); P.el.setAttribute('aria-modal', 'true'); P.el.setAttribute('aria-labelledby', 'lg-pop-h');
    var card = el('div', 'lg-pop-card', P.el);
    var x = el('button', 'lg-pop-x', card); x.type = 'button'; x.setAttribute('aria-label', 'Close'); x.innerHTML = '&times;';
    magsArt(card);
    var h = el('h2', 'lg-d3', card); h.id = 'lg-pop-h';
    el('p', 'lg-body', card);
    var act = el('div', 'lg-pop-act', card);
    var a = el('a', 'lg-btn', act); a.setAttribute('data-pop-go', '');
    var b = el('button', 'lg-btn-line', act); b.type = 'button'; b.setAttribute('data-pop-more', '');
    P.el.addEventListener('click', function (e) {
      if (e.target === P.el || e.target.closest('.lg-pop-x')) { e.preventDefault(); Lucky.pop.close(); return; }
      if (e.target.closest('[data-pop-more]')) { e.preventDefault(); var s = P.cfg.secondary || {}; Lucky.pop.close(function () { go(s.action); }); }
    });
    P.el.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); Lucky.pop.close(); return; }
      if (e.key !== 'Tab') return;
      var f = [].slice.call(P.el.querySelectorAll('a[href],button')), first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
  Lucky.pop = {
    open: function (cfg) {
      if (cfg.once) { if (P.seen[cfg.once]) return false; P.seen[cfg.once] = true; }
      if (!P.el) buildPop();
      P.cfg = cfg;
      var g = groundOf(cfg.host || G.opts.host);
      if (g) P.el.setAttribute('data-ground', g); else P.el.removeAttribute('data-ground');
      P.el.querySelector('.lg-d3').textContent = cfg.title || '';
      P.el.querySelector('.lg-body').textContent = cfg.body || '';
      var a = P.el.querySelector('[data-pop-go]'), b = P.el.querySelector('[data-pop-more]');
      a.textContent = (cfg.primary && cfg.primary.label) || '';
      a.href = (cfg.primary && cfg.primary.href) || '#';
      a.hidden = !cfg.primary;
      if (cfg.primary && cfg.primary.onClick) a.onclick = cfg.primary.onClick; else a.onclick = null;
      b.textContent = (cfg.secondary && cfg.secondary.label) || '';
      b.hidden = !cfg.secondary;
      P.last = document.activeElement;
      if (G.el) G.el.hidden = true;
      P.el.hidden = false;
      P.el.classList.remove('is-out'); P.el.classList.add('is-in');
      (cfg.primary ? a : P.el.querySelector('.lg-pop-x')).focus({ preventScroll: true });
      return true;
    },
    close: function (after) {
      if (!P.el || P.el.hidden) return;
      var card = P.el.querySelector('.lg-pop-card');
      if (G.el && G.text) { G.el.hidden = false; Lucky.guide.place(); }
      var done = function () {
        P.el.hidden = true;
        P.el.classList.remove('is-in', 'is-out');
        card.style.transition = ''; card.style.transform = ''; card.style.opacity = '';
        Lucky.guide.hop();
        if (P.cfg && P.cfg.onClose) P.cfg.onClose();
        if (after) after();
        else if (G.el && !G.el.hidden) G.el.focus({ preventScroll: true });
        else if (P.last && P.last.focus) P.last.focus({ preventScroll: true });
      };
      if (calm() || !G.el || G.el.hidden) { done(); return; }
      var a = card.getBoundingClientRect(), m = G.el.querySelector('.lg-mags').getBoundingClientRect();
      var dx = (m.left + m.width / 2) - (a.left + a.width / 2), dy = (m.top + m.height / 2) - (a.top + a.height / 2);
      P.el.classList.add('is-out');
      card.style.transition = 'transform .42s cubic-bezier(.5,0,.2,1), opacity .42s ease';
      requestAnimationFrame(function () { card.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(.12)'; card.style.opacity = '0'; });
      setTimeout(done, 440);
    }
  };

  /* ------------------------------------------------------------ the toast
     Lucky.toast("That one's gone. Pick another, it's still free.")
     Lucky.toast("You're in.", { mags: true })   // good news only */
  var T = { el: null, timer: null };
  Lucky.toast = function (msg, opt) {
    opt = opt || {};
    if (!T.el) {
      T.el = el('div', 'lg-toast', document.body); T.el.hidden = true; T.el.setAttribute('role', 'status');
      T.mags = magsArt(T.el); T.txt = el('span', '', T.el);
    }
    T.txt.textContent = msg;
    T.mags.style.display = opt.mags ? '' : 'none';
    T.el.hidden = false;
    clearTimeout(T.timer);
    T.timer = setTimeout(function () { T.el.hidden = true; }, opt.ms || 5200);
  };

  /* ------------------------------------------------------------- the hole
     var bar = Lucky.hole(document.querySelector('.lg-hole'), {
       stops: [{ at: 9000, label: '$90 hat' }, { at: 14000, label: '$140 polo' }, { at: 19800, label: '$198 free ship' }]
     });
     bar.set(10900);   // cents, or any unit, as long as the stops use the same one */
  Lucky.hole = function (host, cfg) {
    var stops = cfg.stops || [], max = cfg.max || (stops.length ? stops[stops.length - 1].at : 1);
    host.innerHTML = '';
    var fill = el('span', 'lg-hole-fill', host), ball = el('span', 'lg-hole-ball', host), flags = [];
    host.setAttribute('aria-hidden', 'true');
    stops.forEach(function (s, i) {
      var f = el('span', 'lg-hole-flag', host);
      f.style.left = (s.at / max * 100) + '%';
      if (i === stops.length - 1) f.setAttribute('data-last', '');
      el('i', '', f); var b = el('b', '', f); b.textContent = s.label || '';
      flags.push(f);
    });
    var last = null;
    return {
      set: function (v) {
        var pct = Math.min(1, Math.max(0, v / max)) * 100;
        fill.style.width = pct + '%'; ball.style.left = pct + '%';
        if (last !== null && pct !== last && !calm()) { ball.classList.remove('is-fly'); void ball.offsetWidth; ball.classList.add('is-fly'); }
        last = pct;
        stops.forEach(function (s, i) { if (v >= s.at) flags[i].setAttribute('data-hit', ''); else flags[i].removeAttribute('data-hit'); });
        host.dispatchEvent(new CustomEvent('lucky:hole', { detail: { pct: pct } }));
      }
    };
  };

  /* --------------------------------------------------------- the contours
     One big contour map, a different part of it in every section that uses
     it. A section that sets its own --cx/--cy keeps them; the rest get a spot
     picked by their order on the page (golden-ratio steps, so neighbours never
     land near each other). Same page, same spots, every visit. Runs itself. */
  Lucky.contours = function (root) {
    var n = 0;
    [].slice.call((root || document).querySelectorAll('.lg-contour')).forEach(function (el) {
      n++;
      if (el.style.getPropertyValue('--cx')) return;
      var g = 0.61803398875, x = (0.23 + n * g) % 1, y = (0.57 + n * g * 1.7) % 1;
      el.style.setProperty('--cx', Math.round(10 + x * 80) + '%');
      el.style.setProperty('--cy', Math.round(10 + y * 80) + '%');
      el.style.setProperty('--cz', Math.round(260 + ((n * 37) % 120)) + '%');
    });
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function () { Lucky.contours(); });
  else Lucky.contours();

  /* ------------------------------------------------------- the proximity
     Lucky.proximity(el, { counts: { 5: 585, 4: 37, 3: 12, 2: 5, 1: 11 }, label: '650 reviews' })
     Every review is a ball on the green, seen from above: 5 stars inside the
     first ring, 1 star on the outside. Counts are REAL (Judge.me); a big total
     is drawn at one ball per N reviews and says so. Same counts, same picture,
     every time (the scatter is seeded, not random). */
  Lucky.proximity = function (host, cfg) {
    var c = cfg.counts || {}, total = 0, sum = 0;
    [5, 4, 3, 2, 1].forEach(function (k) { total += c[k] || 0; sum += (c[k] || 0) * k; });
    if (!total) return;
    var per = Math.max(1, Math.ceil(total / 140));
    var RX = [0, 60.72, 95.04, 124.08, 147.84, 168.96], Q = 0.636, CX = 210, CY = 150;
    var seed = 7; function rnd() { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }
    var dots = '';
    [5, 4, 3, 2, 1].forEach(function (k, band) {
      var n = Math.round((c[k] || 0) / per); if ((c[k] || 0) > 0 && n === 0) n = 1;
      for (var i = 0; i < n; i++) {
        var r = RX[band] + (RX[band + 1] - RX[band]) * (0.15 + 0.7 * rnd()), a = rnd() * Math.PI * 2;
        dots += '<circle class="px-dot" cx="' + (CX + Math.cos(a) * r).toFixed(1) + '" cy="' + (CY + Math.sin(a) * r * Q).toFixed(1) + '" r="2.3"/>';
      }
    });
    var rings = '', labels = '';
    for (var j = 1; j <= 5; j++) {
      rings += '<ellipse class="px-ring' + (j > 1 ? ' r2' : '') + '" cx="' + CX + '" cy="' + CY + '" rx="' + RX[j] + '" ry="' + (RX[j] * Q).toFixed(2) + '"/>';
      /* only the inner and outer rings get a label: five of them crowded the middle */
      if (j === 1 || j === 5) labels += '<text class="px-rl' + (j === 1 ? ' r5' : '') + '" x="' + (CX + RX[j] + 8).toFixed(1) + '" y="' + (CY - RX[j] * Q - 6).toFixed(1) + '">' + (6 - j) + ' star' + (j === 1 ? 's' : '') + '</text>';
    }
    var avg = (Math.floor(sum / total * 10) / 10).toFixed(1);   /* rounds DOWN, per the content rules */
    /* nums:false hides the per-star counts and the total. A count makes a young
       brand look smaller than it is; the shape of the bars still tells the truth. */
    var nums = cfg.nums !== false;
    var bars = [5, 4, 3, 2, 1].map(function (k) {
      var pct = (c[k] || 0) / total * 100;
      return '<div class="lg-score-row"' + (nums ? '' : ' data-nonum') + '><span>' + k + '★</span><i style="--pct:' + pct.toFixed(1) + '%"></i>'
        + (nums ? '<span>' + (c[k] || 0) + '</span>' : '') + '</div>';
    }).join('');
    host.classList.add('lg-prox');
    host.innerHTML = '<svg viewBox="0 0 420 300" role="img" aria-label="' + avg + ' out of 5 from ' + total + ' reviews, plotted as shots at the pin.">' +
      '<path class="px-axis" d="M' + CX + ' 30V270M27 ' + CY + 'H393"/>' + rings + dots + '<circle class="px-cup" cx="' + CX + '" cy="' + CY + '" r="4"/>' + labels + '</svg>' +
      '<div><div class="lg-score"><b class="lg-num">' + avg + '</b><div class="lg-score-bars">' + bars + '</div>' +
      '<span class="lg-meta" style="grid-column:1/-1">' + (cfg.label || "Every review takes a shot at the pin.") + '</span></div></div>';
  };

  /* ----------------------------------------------------------- the tracer
     Lucky.tracer(document.querySelector('.lg-tracer'), { stops: [...same as the hole], tee: 'Tee' })
     Returns { set(value) }: the ball flies the arc to that spot. Pair it with
     a hole bar by calling both from the same number. One per page. */
  Lucky.tracer = function (host, cfg) {
    var stops = cfg.stops || [], max = cfg.max || (stops.length ? stops[stops.length - 1].at : 1);
    var X = function (v) { return 40 + (v / max) * 1120; };
    var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 1200 170'); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet'); svg.setAttribute('aria-hidden', 'true');
    var ticks = '';
    for (var i = 0; i <= 22; i++) { var tx = 40 + i * (1120 / 22); ticks += '<line x1="' + tx + '" x2="' + tx + '" y1="140" y2="' + (i % 2 ? 147 : 152) + '"/>'; }
    var d = 'M40 140', prev = 40, lift = [-60, 40, 108, 120];
    stops.forEach(function (s, k) { var x = X(s.at); d += ' Q ' + ((prev + x) / 2) + ' ' + lift[Math.min(k, 3)] + ' ' + x + ' 140'; prev = x; });
    var flags = stops.map(function (s, k) {
      return '<g class="yd-flag" transform="translate(' + X(s.at) + ' 140)"><line y2="-34"/><path d="M0 -34 L16 -28 L0 -22Z"/><text y="24" text-anchor="' + (k === stops.length - 1 ? 'end' : 'middle') + '"></text></g>';
    }).join('');
    svg.innerHTML = '<g class="yd-ticks">' + ticks + '<line x1="40" x2="1160" y1="140" y2="140"/></g><path class="yd-path" pathLength="1" d="' + d + '"/>' + flags +
      '<text class="yd-tee" x="40" y="164"></text><circle class="yd-ball" cx="40" cy="140" r="6"/>';
    [].slice.call(svg.querySelectorAll('.yd-flag text')).forEach(function (t, k) { t.textContent = stops[k].label || ''; });
    svg.querySelector('.yd-tee').textContent = cfg.tee || '';
    host.appendChild(svg);
    var path = svg.querySelector('.yd-path'), ball = svg.querySelector('.yd-ball'), L = path.getTotalLength(), cur = 0, raf = null;
    function lenAtX(x) { var lo = 0, hi = L; for (var n = 0; n < 22; n++) { var m = (lo + hi) / 2; if (path.getPointAtLength(m).x < x) lo = m; else hi = m; } return lo; }
    function place(len) { cur = len; var p = path.getPointAtLength(len); ball.setAttribute('cx', p.x); ball.setAttribute('cy', p.y); }
    function fly(to) {
      cancelAnimationFrame(raf);
      if (document.hidden || calm()) { place(to); return; }
      var from = cur, t0 = performance.now(), dur = 900 + Math.abs(to - from) * 1.1;
      (function step(now) { var k = Math.min(1, (now - t0) / dur); k = 1 - Math.pow(1 - k, 3); place(from + (to - from) * k); if (k < 1) raf = requestAnimationFrame(step); })(t0);
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { host.classList.add('is-in'); o.disconnect(); } }); }, { threshold: .4 }).observe(host);
    } else host.classList.add('is-in');
    return { set: function (v) { fly(lenAtX(X(Math.min(max, Math.max(0, v))))); } };
  };
})();
