/* ==========================================================================
   v9 · the site layer on top of lucky.js (v4). One bag for every page,
   the drawer with the free-shipping hole bar, Mags taking the shopper to
   checkout after an add, the mega menu, the phone menu, modals and zoom.
   Free shipping is $198 (read live from the store's UpCart tier, 2026-09-18).
   ========================================================================== */
(function(){
  'use strict';
  var FREE = 198;
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var $$ = function(s, r){ return [].slice.call((r || document).querySelectorAll(s)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var money = function(n){ return '$' + (Math.round(n * 100) % 100 ? n.toFixed(2) : Math.round(n)); };

  Lucky.mags = { ink: 'img/mags-ink.webp', light: 'img/mags-light.webp' };

  /* ------------------------------------------------------------ the bag */
  var lines = [];
  try { lines = JSON.parse(sessionStorage.getItem('lg-bag') || '[]') || []; } catch (e) { lines = []; }
  function save(){ try { sessionStorage.setItem('lg-bag', JSON.stringify(lines)); } catch (e) {} }
  function total(){ return lines.reduce(function(a, l){ return a + l.price; }, 0); }

  var sticky = null;
  var subs = [];
  function emit(){ subs.forEach(function(fn){ try { fn(lines, total()); } catch (e) {} }); }
  var Bag = window.LuckyBag = {
    lines: function(){ return lines; },
    total: total,
    /* the cart page listens, so the drawer and the page never disagree */
    onChange: function(fn){ subs.push(fn); fn(lines, total()); },
    remove: function(i){ lines.splice(i, 1); save(); paint(); emit(); },
    add: function(items, opts){
      opts = opts || {};
      items.forEach(function(it){ lines.push(it); });
      save(); paint(); hop(); emit();
      /* An add opens the drawer. Nothing else: Mags popping up belongs to the
         promo landing page, not to a product page. */
      Bag.open();
    },
    open: function(){ var cd = $('#cd'); if (!cd) return; cd.hidden = false; paint(); var x = $('.cd-x', cd); if (x) x.focus({ preventScroll: true }); },
    close: function(){ var cd = $('#cd'); if (cd) cd.hidden = true; }
  };
  function hop(){ var b = $('.bagbtn'); if (!b) return; b.classList.remove('is-hop'); void b.offsetWidth; b.classList.add('is-hop'); }

  var hole = null;
  function paint(){
    $$('.bagbtn .n').forEach(function(n){ n.textContent = lines.length; n.setAttribute('data-n', lines.length); });
    var list = $('#cd-list'); if (!list) return;
    var t = total();
    if (!lines.length){
      list.innerHTML = '<div class="cd-empty"><span class="lg-mags"><img class="is-ink" src="img/mags-ink.webp" alt=""><img class="is-light" src="img/mags-light.webp" alt=""></span>'
        + '<p class="lg-aside" style="margin:0 auto 18px">Nothing in here yet. Mags checked twice.</p>'
        + '<a class="lg-btn-line lg-btn-sm" href="clubs.html">See the clubs</a></div>';
    } else {
      list.innerHTML = lines.map(function(l, i){
        return '<div class="cd-line"><span class="ph"><img src="' + esc(l.img) + '" alt=""></span><span><b>' + esc(l.name) + '</b>'
          + (l.hud && l.hud.length ? '<span class="lg-hud">' + l.hud.map(function(h){ return '<span>' + esc(h) + '</span>'; }).join('') + '</span>' : '')
          + '</span><span class="pr">' + money(l.price) + '<button type="button" class="rm" data-rm="' + i + '">Remove</button></span></div>';
      }).join('');
    }
    var say = $('#cd-say');
    if (say) say.innerHTML = !lines.length ? 'Free shipping at <b>$198</b>.'
      : t >= FREE ? "<b>Shipping's on us.</b>"
      : '<b>' + money(FREE - t) + "</b> more and shipping's on us.";
    if (!hole && $('#cd-hole')) hole = Lucky.hole($('#cd-hole'), { stops: [{ at: FREE, label: 'Free shipping $198' }] });
    if (hole) hole.set(t);
    var s = $('#cd-sub'); if (s) s.textContent = money(t);
    var go = $('#cd-go'); if (go) go.setAttribute('aria-disabled', String(!lines.length));
  }

  document.addEventListener('click', function(e){
    var t;
    if (t = e.target.closest('[data-cart-open]')){ e.preventDefault(); Bag.open(); return; }
    if (t = e.target.closest('[data-cart-close]')){ e.preventDefault(); Bag.close(); return; }
    if (t = e.target.closest('[data-rm]')){ Bag.remove(+t.getAttribute('data-rm')); return; }
    if (t = e.target.closest('#cd-go')){ e.preventDefault(); if (lines.length) Lucky.toast('Checkout is not wired up in this preview.'); return; }
  });

  /* ------------------------------------------------------------ the menus */
  document.addEventListener('click', function(e){
    var b = e.target.closest('.nv > button');
    $$('.nv').forEach(function(n){
      var open = b && n.contains(b) && !n.classList.contains('is-open');
      n.classList.toggle('is-open', !!open); var bt = $('button', n); if (bt) bt.setAttribute('aria-expanded', String(!!open));
    });
    var bu = e.target.closest('.burger');
    if (bu){ var m = $('#mnav'), o = !m.classList.contains('is-open'); m.classList.toggle('is-open', o); bu.setAttribute('aria-expanded', String(o)); }
  });
  $$('.nv').forEach(function(n){
    n.addEventListener('mouseenter', function(){ if (matchMedia('(hover:hover)').matches){ n.classList.add('is-open'); } });
    n.addEventListener('mouseleave', function(){ n.classList.remove('is-open'); });
  });

  /* ------------------------------------------------------------ modals */
  document.addEventListener('click', function(e){
    var o = e.target.closest('[data-md-open]');
    if (o){ e.preventDefault(); var m = document.getElementById(o.getAttribute('data-md-open')); if (m){ m.hidden = false; var x = $('.md-x', m); if (x) x.focus({ preventScroll: true }); }
      if (o.getAttribute('data-md-open') === 'md-shot'){ $('[data-shot-title]').textContent = o.getAttribute('data-title') || 'Shot needed'; $('[data-shot-brief]').textContent = o.getAttribute('data-brief') || ''; }
      return; }
    var c = e.target.closest('[data-md-close]');
    if (c){ var md = c.closest('.md'); if (md) md.hidden = true; }
  });
  document.addEventListener('keydown', function(e){
    if (e.key !== 'Escape') return;
    $$('.md').forEach(function(m){ m.hidden = true; }); Bag.close();
    $$('.nv').forEach(function(n){ n.classList.remove('is-open'); });
  });

  /* zoom */
  var zoom = $('#zoom');
  if (zoom && zoom.showModal){
    document.addEventListener('click', function(e){
      var t = e.target.closest('[data-zoom]');
      if (t){ var im = $('img', zoom); im.src = t.getAttribute('data-zoom'); im.alt = ($('img', t) || {}).alt || ''; zoom.showModal(); return; }
      if (e.target.closest('[data-zoom-close]') || e.target === zoom) zoom.close();
    });
  }

  /* newsletter: no backend in a preview */
  document.addEventListener('submit', function(e){
    var f = e.target.closest('[data-news]'); if (!f) return;
    e.preventDefault(); var i = $('input', f);
    if (!i.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value)){ i.focus(); return; }
    f.outerHTML = '<p class="lg-aside" style="margin:0">Done. You&rsquo;re on the list.</p>';
  });
  /* back-in-stock: any [data-notify] form a page doesn't handle itself */
  document.addEventListener('submit', function(e){
    var f = e.target.closest('[data-notify]'); if (!f || e.defaultPrevented) return;
    e.preventDefault(); var i = $('input', f);
    if (!i.value || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(i.value)){ i.focus(); return; }
    f.outerHTML = '<p class="lg-aside" style="margin:0">Done. You&rsquo;ll get one email when it&rsquo;s back.</p>';
  });

  /* ------------------------------------------------------- preview links */
  var BUILT = window.LG_BUILT || [];
  document.addEventListener('click', function(e){
    var a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
    var h = a.getAttribute('href') || '';
    if (h.charAt(0) === '#' || /^(https?:|mailto:|javascript)/.test(h)) return;
    var page = h.split('#')[0];
    e.preventDefault();
    if (BUILT.indexOf(page) > -1){ try { parent.postMessage({ pvGo: h, side: 'after' }, '*'); } catch (_) {} if (parent === window) location.href = h; return; }
    var t = $('#pv-toast'); if (!t){ t = document.createElement('div'); t.id = 'pv-toast'; document.body.appendChild(t); }
    t.textContent = 'That page is not part of this preview yet.'; t.style.opacity = '1';
    clearTimeout(t._h); t._h = setTimeout(function(){ t.style.opacity = '0'; }, 1800);
  }, true);

  window.LuckySite = { setSticky: function(el){ sticky = el; } };
  paint();

  try { parent.postMessage({ ready: location.pathname.split('/').pop() }, '*'); } catch (_) {}
})();
