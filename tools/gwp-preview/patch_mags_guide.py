"""Mags becomes the guide (Cole, 2026-09-18):
- a Mags dock in the corner that always says the ONE next step, and does it when tapped:
  hat unlocked -> "tap me, I'll show you" (scrolls to the hat)
  polo unlocked -> same for the polo
  otherwise -> "tap me to check out" (straight to /checkout, no cart page)
- a clean pop-up after a gift is claimed: check out now, or add more / keep shopping.
  Closing it shrinks it into Mags, who then holds the checkout.
The tier-crossing toast is retired; Mags carries the good news now."""
import io
DONE = {'sections/gwp-promo.liquid', 'templates/page.gwp-promo.json'}
ROOT = 'C:/Users/wetzl/Lucky Golf/Website/shopify/'
def edit(rel, pairs):
    p = ROOT + rel
    s = io.open(p, encoding='utf-8', newline='').read()
    if rel in DONE: print('skip', rel); return
    crlf = chr(13) + chr(10) in s
    for a, b in pairs:
        if crlf: a, b = a.replace(chr(10), chr(13) + chr(10)), b.replace(chr(10), chr(13) + chr(10))
        assert s.count(a) == 1, (rel, a[:70], s.count(a))
        s = s.replace(a, b, 1)
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('ok', rel)

COPY = [
    ('mags_hat', 'Mags: free hat is waiting', "Congrats, the hat's free. Tap me and I'll show you where."),
    ('mags_polo', 'Mags: free polo is waiting', "The polo's free now too. Tap me, it's right down here."),
    ('mags_go', 'Mags: ready to check out', "You're set. Tap me to check out."),
    ('pop1_title', 'Pop-up after the hat: title', "The hat's in your bag."),
    ('pop1_body', 'Pop-up after the hat: body', "Check out now, or add {amount} more and the polo's free too."),
    ('pop1_more', 'Pop-up after the hat: second button', "Add more for the polo"),
    ('pop2_title', 'Pop-up after both: title', "Hat and polo. Both free."),
    ('pop2_body', 'Pop-up after both: body', "Check out now, or keep shopping. They'll wait in your bag."),
    ('pop2_more', 'Pop-up after both: second button', "Keep shopping"),
    ('pop_ship', 'Pop-up: free shipping line', "Add {amount} more and shipping's free too."),
    ('pop_checkout', 'Pop-up: checkout button', "Check out"),
]
schema = '    { "type": "header", "content": "Mags, the guide" },\n' + \
    '    { "type": "paragraph", "content": "Mags sits in the corner once a gift is unlocked and always says the one next step. {amount} fills in." },\n' + \
    ''.join('    { "type": "text", "id": "%s", "label": "%s", "default": "%s" },\n' % (k, l, d) for k, l, d in COPY) + '\n'
attrs = ''.join('\n     data-%s="{{ s.%s | escape }}"' % (k.replace('_', '-'), k) for k, _, _ in COPY if k != 'pop_checkout')

MARKUP = """
  <!-- ══════════ MAGS · the guide. Always the one next step; tap and he does it ══════════ -->
  <button type="button" class="gwp-mags" id="gwp-mags" hidden>
    <img src="{{ 'gwp-mags.webp' | file_url }}" alt="" width="84" height="52">
    <span class="gwp-mags-say" data-mags-say aria-live="polite"></span>
  </button>

  <div class="gwp-pop" id="gwp-pop" hidden role="dialog" aria-modal="true" aria-labelledby="gwp-pop-h">
    <div class="gwp-pop-card">
      <button type="button" class="gwp-pop-x" data-pop-close aria-label="Close">&times;</button>
      <img class="gwp-pop-mags" src="{{ 'gwp-mags.webp' | file_url }}" alt="" width="96" height="60">
      <h2 class="lg-d3" id="gwp-pop-h" data-pop-title></h2>
      <p class="lg-body" data-pop-body></p>
      <div class="gwp-pop-act">
        <a class="lg-btn" href="/checkout" data-pop-go>{{ s.pop_checkout }} <span aria-hidden="true">&rarr;</span></a>
        <button type="button" class="lg-btn lg-btn-line" data-pop-more></button>
      </div>
    </div>
  </div>

  <div class="gwp-toast\""""

edit('sections/gwp-promo.liquid', [
    ('''     data-copy-soldout-gift="{{ s.toast_gift_soldout | escape }}">''',
     '''     data-copy-soldout-gift="{{ s.toast_gift_soldout | escape }}"''' + attrs + '>'),
    ('''
  <div class="gwp-toast"''', MARKUP),
    ('''    { "type": "header", "content": "Toasts" },''', schema + '''    { "type": "header", "content": "Toasts" },'''),
])

edit('templates/page.gwp-promo.json', [
    ('''        "sign_cta": "Pick your club"''',
     '''        "sign_cta": "Pick your club",\n''' + ',\n'.join('        "%s": "%s"' % (k, d) for k, _, d in COPY)),
])

JS_GUIDE = r"""
  /* ============================== MAGS, THE GUIDE ============================
     Mags is the one who gets the reader to checkout. He shows up the moment a
     gift unlocks and always says exactly one next step, and tapping him does
     it: take me to the hat, take me to the polo, take me to checkout. After a
     gift is claimed a small pop-up asks the question outright (check out, or
     keep going?); closing it shrinks it into Mags, who then holds the door.
     ======================================================================== */
  var magsEl = document.getElementById('gwp-mags');
  var magsSay = magsEl && magsEl.querySelector('[data-mags-say]');
  var popEl = document.getElementById('gwp-pop');
  var popOpen = false, magsMode = null, magsBooted = false, popSeen = {};
  var lastFocus = null;
  function calm() { return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }
  function hop() {
    if (!magsEl || calm()) return;
    magsEl.classList.remove('is-hop'); void magsEl.offsetWidth; magsEl.classList.add('is-hop');
  }
  function guideMode(tier) {
    var hat = giftLines('hat').length > 0, polo = giftLines('polo').length > 0;
    if (tier < 1) return null;
    if (GIFTS.hat && !hat) return 'hat';
    if (GIFTS.polo && tier >= 2 && !polo) return 'polo';
    return 'checkout';
  }
  function paintMags(tier) {
    if (!magsEl) return;
    var mode = guideMode(tier);
    if (popOpen || !mode) { magsEl.hidden = true; magsMode = mode; return; }
    var txt = mode === 'hat' ? COPY.magsHat : mode === 'polo' ? COPY.magsPolo : COPY.magsGo;
    if (magsSay.textContent !== txt) magsSay.textContent = txt;
    magsEl.setAttribute('data-mode', mode);
    var was = magsEl.hidden;
    magsEl.hidden = false;
    if (magsBooted && (mode !== magsMode || was)) hop();
    magsMode = mode;
  }
  function jumpTo(id) {
    var target = document.getElementById(id);
    if (!target) return;
    var gift = target.hasAttribute('data-gift');
    target.scrollIntoView({ behavior: calm() ? 'auto' : 'smooth', block: gift ? 'center' : 'start' });
    if (gift) cue(target.getAttribute('data-gift'));
    target.focus({ preventScroll: true });
  }

  function openPop(kind) {
    if (!popEl || popSeen[kind]) return;
    popSeen[kind] = true;
    var sub = paidSubtotal();
    var title = kind === 'more' ? COPY.pop1Title : COPY.pop2Title;
    var body = kind === 'more' ? fill(COPY.pop1Body, { amount: moneyShort(Math.max(0, T2 - sub)) }) : COPY.pop2Body;
    if (kind === 'done' && SHIP && sub < SHIP && COPY.popShip) body += ' ' + fill(COPY.popShip, { amount: moneyShort(SHIP - sub) });
    popEl.querySelector('[data-pop-title]').textContent = title;
    popEl.querySelector('[data-pop-body]').textContent = body;
    popEl.querySelector('[data-pop-more]').textContent = kind === 'more' ? COPY.pop1More : COPY.pop2More;
    lastFocus = document.activeElement;
    popOpen = true;
    paint();
    popEl.hidden = false;
    popEl.classList.remove('is-out'); popEl.classList.add('is-in');
    var go = popEl.querySelector('[data-pop-go]');
    if (go) go.focus({ preventScroll: true });
  }
  function closePop(after) {
    if (!popEl || popEl.hidden) return;
    var card = popEl.querySelector('.gwp-pop-card');
    popOpen = false;
    paint();                                   /* Mags comes back first, so the card has somewhere to land */
    var done = function () {
      popEl.hidden = true;
      popEl.classList.remove('is-in', 'is-out');
      card.style.transition = ''; card.style.transform = ''; card.style.opacity = '';
      hop();
      if (after) after();
      else if (magsEl && !magsEl.hidden) magsEl.focus({ preventScroll: true });
      else if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    };
    if (calm() || !magsEl || magsEl.hidden) { done(); return; }
    var a = card.getBoundingClientRect(), b = magsEl.querySelector('img').getBoundingClientRect();
    var dx = (b.left + b.width / 2) - (a.left + a.width / 2), dy = (b.top + b.height / 2) - (a.top + a.height / 2);
    popEl.classList.add('is-out');
    card.style.transition = 'transform .42s cubic-bezier(.5,0,.2,1), opacity .42s ease';
    requestAnimationFrame(function () {
      card.style.transform = 'translate(' + dx + 'px,' + dy + 'px) scale(.12)';
      card.style.opacity = '0';
    });
    setTimeout(done, 440);
  }
  /* After a claim: is there a question worth asking? */
  function maybePop(slot) {
    if (!giftLines(slot).length) return;
    var tier = tierOf(paidSubtotal());
    var hat = giftLines('hat').length > 0, polo = giftLines('polo').length > 0;
    if (hat && (!GIFTS.polo || polo)) openPop('done');
    else if (hat && GIFTS.polo && tier < 2) openPop('more');
  }
  if (popEl) {
    popEl.addEventListener('click', function (e) {
      if (e.target === popEl || e.target.closest('[data-pop-close]')) { e.preventDefault(); closePop(); return; }
      if (e.target.closest('[data-pop-more]')) { e.preventDefault(); closePop(function () { jumpTo('gwp-clubs'); }); }
    });
    popEl.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { e.preventDefault(); closePop(); return; }
      if (e.key !== 'Tab') return;
      var f = [].slice.call(popEl.querySelectorAll('a[href],button'));
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }
"""

edit('assets/gwp-promo.js', [
    ('''    giftSoldOut: root.getAttribute('data-copy-soldout-gift') || ''
  };''', '''    giftSoldOut: root.getAttribute('data-copy-soldout-gift') || '',
    magsHat: root.getAttribute('data-mags-hat') || '',
    magsPolo: root.getAttribute('data-mags-polo') || '',
    magsGo: root.getAttribute('data-mags-go') || '',
    pop1Title: root.getAttribute('data-pop1-title') || '',
    pop1Body: root.getAttribute('data-pop1-body') || '',
    pop1More: root.getAttribute('data-pop1-more') || '',
    pop2Title: root.getAttribute('data-pop2-title') || '',
    pop2Body: root.getAttribute('data-pop2-body') || '',
    pop2More: root.getAttribute('data-pop2-more') || '',
    popShip: root.getAttribute('data-pop-ship') || ''
  };'''),
    # the tier crossing: Mags hops with the news instead of a toast
    ('''  function announceTier(tier) {
    if (lastTier !== null && tier > lastTier) {
      toast(fill(COPY.giftWon, { gift: tier >= 2 ? COPY.g2 : COPY.g1 }), true);
      cue(tier >= 2 ? 'polo' : 'hat');
    }''', '''  function announceTier(tier) {
    if (lastTier !== null && tier > lastTier) {
      if (!magsEl) toast(fill(COPY.giftWon, { gift: tier >= 2 ? COPY.g2 : COPY.g1 }), true);
      cue(tier >= 2 ? 'polo' : 'hat');
    }'''),
    ('''    paintRail(sub, tier);
    paintGifts(sub, tier);
  }''', '''    paintRail(sub, tier);
    paintGifts(sub, tier);
    paintMags(tier);
  }
''' + JS_GUIDE),
    # a claim that landed may earn the question
    ('''        }).then(function (r) {
          busy(btn, false);
          if (refused(r)) {''', '''        }).then(function (r) {
          busy(btn, false);
          var landed = !refused(r);
          if (!landed) {'''),
    ('''          settleCart();
          return getCart().then(function (c2) {
            if (c2.body && c2.body.items) { cart = c2.body; return reconcile(); }
          });
        });''', '''          settleCart();
          return getCart().then(function (c2) {
            if (c2.body && c2.body.items) { cart = c2.body; return reconcile(); }
          }).then(function () { if (landed) maybePop(slot); });
        });'''),
    # tapping Mags does the thing he said
    ('''    var claim = e.target.closest('[data-claim]');
    if (claim && !claim.disabled) { e.preventDefault(); claimGift(claim); return; }
''', '''    var claim = e.target.closest('[data-claim]');
    if (claim && !claim.disabled) { e.preventDefault(); claimGift(claim); return; }

    var mg = e.target.closest('#gwp-mags');
    if (mg) {
      e.preventDefault();
      var mode = mg.getAttribute('data-mode');
      if (mode === 'checkout') goCheckout(base() + 'checkout');
      else if (mode) jumpTo('gwp-gift-' + mode);
      return;
    }
'''),
    ('''    var a = e.target.closest('a[href$="/checkout"]');
    if (!a) return;
    e.preventDefault();
    var go = function () { window.location.href = a.href; };
    queue(function () {
      return getCart().then(function (r) {
        if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      });
    }).then(go, go);
  });''', '''    var a = e.target.closest('a[href$="/checkout"]');
    if (!a) return;
    e.preventDefault();
    goCheckout(a.href);
  });
  function goCheckout(href) {
    var go = function () { window.location.href = href; };
    queue(function () {
      return getCart().then(function (r) {
        if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      });
    }).then(go, go);
  }'''),
    ('''      if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      paint();
    }, paint);
  });
})();''', '''      if (r.body && r.body.items) { cart = r.body; return reconcile(); }
      paint();
    }, paint).then(function () { magsBooted = true; });
  });
})();'''),
])

CSS = """

/* ---------------------------------------------------------------- Mags, the guide
   The dock: Mags + one line, bottom-left (the chat bubble owns bottom-right).
   The pop-up: white card, foil hairline, Mags on top, two buttons. */
.gwp-mags{position:fixed;left:20px;bottom:24px;z-index:90;display:flex;align-items:center;margin:0;padding:0;border:0;background:none;
  cursor:pointer;font:inherit;text-align:left;color:inherit;-webkit-tap-highlight-color:transparent}
.gwp-mags[hidden]{display:none}
.gwp-mags img{position:relative;z-index:1;flex:none;width:84px;height:auto;display:block}
.gwp-mags-say{margin-left:-4px;max-width:260px;padding:11px 15px;background:var(--lg-dark);color:var(--lg-on-dark);
  border:1px solid var(--lg-gold);border-radius:14px;font-size:14.4px;line-height:1.35;transition:border-color .2s}
.gwp-mags:hover .gwp-mags-say{border-color:#EDD27C}
.gwp-mags:focus-visible{outline:none}
.gwp-mags:focus-visible .gwp-mags-say{outline:2px solid var(--lg-gold);outline-offset:3px}
.gwp-mags.is-hop img{animation:gwp-hop .7s var(--lg-ease) 1}
.gwp-mags.is-hop .gwp-mags-say{animation:gwp-say .4s var(--lg-ease) 1}
@keyframes gwp-hop{0%{translate:0 0}30%{translate:0 -16px}55%{translate:0 0}75%{translate:0 -6px}100%{translate:0 0}}
@keyframes gwp-say{from{opacity:0;scale:.94}to{opacity:1;scale:1}}
@media (max-width:749px){
  .gwp-mags{left:10px;bottom:calc(182px + env(safe-area-inset-bottom))}
  .gwp-mags img{width:62px}
  .gwp-mags-say{max-width:calc(100vw - 160px);padding:9px 12px;font-size:13.6px}
}

.gwp-pop{position:fixed;inset:0;z-index:120;display:grid;place-items:center;padding:16px;background:rgba(6,17,11,.46);transition:background .35s}
.gwp-pop[hidden]{display:none}
.gwp-pop.is-out{background:rgba(6,17,11,0)}
.gwp-pop-card{position:relative;width:min(420px,100%);padding:30px 26px 24px;background:var(--lg-page);color:var(--lg-ink);
  border-radius:18px;text-align:center;overflow:hidden}
.gwp-pop-card::before{content:'';position:absolute;left:0;right:0;top:0;height:3px;background:var(--lg-foil)}
.gwp-pop.is-in:not(.is-out) .gwp-pop-card{animation:gwp-pop-in .34s var(--lg-ease) 1}
@keyframes gwp-pop-in{from{opacity:0;translate:0 14px;scale:.96}to{opacity:1;translate:0 0;scale:1}}
.gwp-pop-mags{display:block;width:96px;height:auto;margin:0 auto 12px}
.gwp-pop .lg-d3{margin:0 0 10px;color:var(--lg-ink)}
.gwp-pop .lg-body{margin:0 auto 22px;max-width:34ch;color:var(--lg-ink-64)}
.gwp-pop-act{display:grid;gap:10px}
.gwp-pop-act .lg-btn{width:100%;min-height:50px;justify-content:center}
.gwp-pop-x{position:absolute;top:6px;right:6px;width:44px;height:44px;border:0;background:none;cursor:pointer;
  color:var(--lg-ink-64);font-size:26px;line-height:1;display:grid;place-items:center}
.gwp-pop-x:hover{color:var(--lg-ink)}
@media (prefers-reduced-motion:reduce){
  .gwp-mags.is-hop img,.gwp-mags.is-hop .gwp-mags-say,.gwp-pop.is-in .gwp-pop-card{animation:none}
}
"""
p = ROOT + 'assets/gwp-promo.css'
s = io.open(p, encoding='utf-8', newline='').read()
assert 'Mags, the guide' not in s
io.open(p, 'w', encoding='utf-8', newline='').write(s.rstrip('\n') + CSS)
print('ok css')
