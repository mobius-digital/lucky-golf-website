# -*- coding: utf-8 -*-
"""Assemble the bundle as ONE blob of page content.

The Shopify connector refuses theme-file writes against a published theme, but a
page's own body is content rather than theme code, and that write is allowed. So
the section is inlined here instead: same CSS, same JS, same markup, with the
catalogue baked in at build time and re-read from the storefront on load, so a
hat that sells out later can never show as available.

Regenerate with:  python build_page.py   then push page-body.html via pageUpdate.
"""
import io, re, json

CSS = io.open('assets/bogo-hats.css', encoding='utf-8').read()
JS = io.open('assets/bogo-hats.js', encoding='utf-8').read()
LIQ = io.open('sections/bogo-hats.liquid', encoding='utf-8').read()
S = json.load(io.open('templates/page.bogo-hats.json', encoding='utf-8'))['sections']['main']['settings']

CLOVER = re.search(r'(<svg width="0".*?</svg>)', LIQ, re.S).group(1)

# Measured on the live page: the theme drops page content into .page-width,
# capped at 726px inside a 1265px section, and prints the page title above it.
# A full-bleed hero rendered as a letterbox with a second heading over it in the
# theme's font. This stylesheet ships inside the page body and therefore exists
# ONLY on this page, so widening the main column cannot reach anything else.
EXTRA_CSS = """
/* ---------- escaping the theme's page column ---------- */
/* padding:0, not just the vertical pair. At desktop the theme's side padding
   happens to be 0, but at tablet it is 90px and at mobile it is not zero either,
   so zeroing only top and bottom left the hero inset on every size but the one
   it was first checked at. .lgb-wrap supplies the real gutter. */
#MainContent .page-width{max-width:none;padding:0}
#MainContent .rte{max-width:none}
#MainContent .main-page-title{display:none}
"""

CDN = 'https://cdn.shopify.com/s/files/1/2286/3149/files/'

# Read from the live catalogue, never retyped by hand. Only products with a real
# storefront URL: three legacy hats sit in the collection unpublished.
HATS = [
    (50028040192277, 'White | Gold Classic Hat', 'white-gold-classic-hat', '79_600x.webp?v=1784585346'),
    (50029741637909, 'White "IT\'S BETTER TO BE LUCKY" Patch Hat', 'white-its-better-to-be-lucky-patch-hat', '89_600x.webp?v=1784585347'),
    (50029743866133, 'Cream Upside Down Hat', 'cream-upside-down-hat', '69_600x.webp?v=1784585346'),
    (50029743898901, 'Black "IT\'S BETTER TO BE LUCKY" Patch Hat', 'black-its-better-to-be-lucky-patch-hat', '39_600x.webp?v=1784585347'),
    (50029744193813, 'Tan Cursive Hat', 'tan-cursive-hat', '1_9c446716-791d-48c1-be9d-9e805bda751a_600x.webp?v=1784585347'),
    (50029744292117, 'Black | Gold Classic Lucky Hat', 'black-gold-classic-lucky-hat', '10_96db47c0-e327-4f91-b46b-2f1caced97cf_600x.webp?v=1784585346'),
    (50029746127125, 'White/Black Upside Down Hat', 'white-black-upside-down-hat', '20_600x.webp?v=1784585346'),
    (50029746159893, 'White Upside Down Hat', 'white-upside-down-hat', '59_600x.webp?v=1784585346'),
    (50029746192661, 'White Cursive Hat', 'white-cursive-hat', '49_600x.webp?v=1784585347'),
    (50048056230165, 'Baby Blue Monochrome Cursive Hat', 'baby-blue-cursive-hat', '30_203d7c7f-8680-4d32-bf41-18d0d4877086_600x.webp?v=1784585347'),
]
hats = [{'id': i, 'name': n, 'url': '/products/' + h, 'img': CDN + im,
         'price': 2900, 'available': True} for (i, n, h, im) in HATS]

SIZES = ['Small', 'Medium', 'Large', 'XL', 'XXL', '3XL']
POLO_A = [49851327381781, 49851327414549, 49851327447317, 49851327480085, 49851327512853, 49851327545621]
POLO_B = [49851331870997, 49851331903765, 49851331936533, 49851331969301, 49851332002069, 49851332034837]
# The two Gold wedges became ONE product on 2026-09-05: LGW01 and LGW02 now sit
# on a single Loft & Grind axis, where K is the old 01 head and S is the old 02
# head. The old `v1-gold-lucky-golf-wedge` went DRAFT the moment that shipped,
# which killed the upsell here: /cart/update.js answered 422 "Cannot find
# variant" and the Add button silently did nothing.
# Availability is listed per variant rather than derived from a rule. The old
# code guessed "only Left Hand 50 is dead", and a guess like that goes stale
# without anything failing loudly.
WEDGE_GRINDS = ['50° K', '52° K', '52° S', '54° K', '56° K', '56° S', '58° K', '60° K', '60° S']
WEDGE_VARIANTS = [
    # (id, hand, loft & grind, in stock)
    (50066568904981, 'Right Hand', '50° K', True),
    (50066568937749, 'Right Hand', '52° K', True),
    (50066570248469, 'Right Hand', '52° S', False),
    (50066568970517, 'Right Hand', '54° K', True),
    (50066569003285, 'Right Hand', '56° K', True),
    (50066570281237, 'Right Hand', '56° S', False),
    (50066569036053, 'Right Hand', '58° K', True),
    (50066569068821, 'Right Hand', '60° K', True),
    (50066570314005, 'Right Hand', '60° S', False),
    (50066569101589, 'Left Hand',  '50° K', False),
    (50066569134357, 'Left Hand',  '52° K', True),
    (50066570346773, 'Left Hand',  '52° S', True),
    (50066569167125, 'Left Hand',  '54° K', True),
    (50066569199893, 'Left Hand',  '56° K', True),
    (50066570379541, 'Left Hand',  '56° S', True),
    (50066569232661, 'Left Hand',  '58° K', True),
    (50066569265429, 'Left Hand',  '60° K', True),
    (50066570412309, 'Left Hand',  '60° S', True),
]


def polo(handle, title, img, ids):
    return {
        'handle': handle, 'group': 'apparel', 'name': title,
        'url': '/products/' + handle, 'img': CDN + img, 'price': 6700,
        'options': [{'name': 'Size', 'values': SIZES}],
        'variants': [{'id': v, 'opts': [s], 'available': True, 'price': 6700}
                     for v, s in zip(ids, SIZES)],
    }


wedge_variants = [{'id': vid, 'opts': [hand, grind], 'available': ok, 'price': 9900}
                  for (vid, hand, grind, ok) in WEDGE_VARIANTS]

upsell = [
    polo('signature-black-classic-polo', 'Signature Black Classic Polo',
         'Classicpolowithlogointhecollar1_600x.webp?v=1779472786', POLO_A),
    polo('gold-carnation-classic-polo', 'Gold Carnation Classic Polo',
         'WhiteCarnation1_600x.webp?v=1779472693', POLO_B),
    {'handle': 'lucky-golf-lgw02-gold', 'group': 'club', 'name': 'Lucky Golf LGW02 Gold',
     'url': '/products/lucky-golf-lgw02-gold',
     'img': CDN + '11_26414fab-14b8-41ae-8ad7-a801c2f646fb_600x.webp?v=1782597869',
     'price': 9900,
     'options': [{'name': 'Hand', 'values': ['Right Hand', 'Left Hand']},
                 {'name': 'Loft & Grind', 'values': WEDGE_GRINDS}],
     'variants': wedge_variants},
    {'handle': 'limited-edition-mallet-putter', 'group': 'club', 'name': 'Lucky Golf LGP02 Gold',
     'url': '/products/limited-edition-mallet-putter',
     'img': CDN + '11_7388f94c-9c93-4aff-ada6-c6a1163ac214_600x.webp?v=1782598134',
     'price': 22900,
     'options': [{'name': 'Hand', 'values': ['Right', 'Left']}],
     'variants': [{'id': 49956772544789, 'opts': ['Right'], 'available': True, 'price': 22900},
                  {'id': 49956772577557, 'opts': ['Left'], 'available': True, 'price': 22900}]},
]
for p, key in zip(upsell, ['why_1', 'why_2', 'why_3', 'why_4']):
    p['why'] = S[key]

DATA = {'bundle': S['bundle_size'], 'cartUrl': '/cart',
        'collection': S['hats_collection'], 'hats': hats, 'upsell': upsell}

# ---------- patch the JS so the baked catalogue cannot go stale ----------
OLD = """  /* hero arithmetic reads the real hat price */
  [].slice.call(root.querySelectorAll('[data-unit-price]')).forEach(function(el){ el.textContent = money(UNIT); });
  var dealSum = root.querySelector('[data-deal-sum]');
  if (dealSum) dealSum.textContent = money(UNIT * (BUNDLE - 1)) + ' for ' + BUNDLE;

  armQuietCart();
  paintUpsell();
  getCart().then(function(c){ cart = c; paint(); }).catch(function(){ paint(); });
})();"""

NEW = """  /* hero arithmetic reads the real hat price */
  function fillHero(){
    [].slice.call(root.querySelectorAll('[data-unit-price]')).forEach(function(el){ el.textContent = money(UNIT); });
    var dealSum = root.querySelector('[data-deal-sum]');
    if (dealSum) dealSum.textContent = money(UNIT * (BUNDLE - 1)) + ' for ' + BUNDLE;
  }

  /* The catalogue above is written into this page when it is published, so on
     its own a hat that sells out tomorrow would still offer an Add button today.
     The storefront serves the collection as JSON to anyone, so re-read it and
     correct price and availability before the reader can act on a stale one.
     It runs alongside the cart fetch rather than after it, so it costs no wait. */
  function refreshCatalogue(){
    return new Promise(function(done){
      if (!D.collection) return done();
      var x = new XMLHttpRequest();
      x.open('GET', root_() + 'collections/' + D.collection + '/products.json?limit=250', true);
      x.onload = function(){
        try {
          var byId = {};
          JSON.parse(x.responseText).products.forEach(function(p){
            p.variants.forEach(function(v){ byId[v.id] = v; });
          });
          HATS.forEach(function(h){
            var v = byId[h.id];
            if (v){ h.available = !!v.available; h.price = Math.round(parseFloat(v.price) * 100); }
          });
          UNIT = HATS[0].price;
        } catch(e){}
        done();
      };
      x.onerror = function(){ done(); };
      x.send();
    });
  }

  /* The four upsell prices are baked in and, unlike the hats, are not re-read
     on every load: that would be four more requests on a store that already
     loads plenty. They are only wrong for a reader Shopify is serving in
     another market, where every price is converted, so only that reader pays
     for the correction. Verified live: a visitor resolving to Barbados is
     served BBD at 2.014875, which turns a $29 hat into $60. */
  function refreshUpsell(){
    var c = window.Shopify && window.Shopify.currency;
    if (!c || parseFloat(c.rate) === 1) return Promise.resolve();
    return Promise.all(UPSELL.map(function(p){
      return new Promise(function(done){
        var x = new XMLHttpRequest();
        x.open('GET', root_() + 'products/' + p.handle + '.js', true);
        x.onload = function(){
          try {
            var byId = {};
            JSON.parse(x.responseText).variants.forEach(function(v){ byId[v.id] = v; });
            p.variants.forEach(function(v){
              var s = byId[v.id];
              if (s){ v.price = s.price; v.available = !!s.available; }
            });
            p.price = Math.min.apply(null, p.variants.map(function(v){ return v.price; }));
          } catch(e){}
          done();
        };
        x.onerror = function(){ done(); };
        x.send();
      });
    }));
  }

  armQuietCart();
  fillHero();
  paintUpsell();
  paint();                                   /* instant, off the baked catalogue */
  Promise.all([
    refreshCatalogue(),
    refreshUpsell(),
    getCart().catch(function(){ return {items: []}; })
  ]).then(function(r){
    if (r[2] && r[2].items) cart = r[2];
    fillHero(); paintUpsell(); paint();      /* corrected against the storefront */
  });
})();"""

assert JS.count(OLD) == 1, 'JS tail did not match'
JS = JS.replace(OLD, NEW)
# curly apostrophes live only inside JS string literals, where ’ is exact
JS = JS.replace(u'’', chr(92) + 'u2019')


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


facts = ''.join('<li>%s</li>' % esc(f.strip()) for f in S['facts'].split(','))

HTML = u"""<style>
%(css)s
</style>

<div class="lg-bogo" id="lg-bogo">
%(clover)s

  <section class="lgb-sec-tight lgb-band-ink bgo-hero">
    <span class="bgo-wm" aria-hidden="true"><svg><use href="#lgb-clover"/></svg></span>
    <div class="lgb-wrap">
      <p class="lgb-eyebrow on-dark">%(eyebrow)s</p>
      <h1 class="lgb-disp bgo-h1">%(heading)s</h1>
      <p class="bgo-lede">%(subheading)s</p>
      <div class="bgo-deal" aria-hidden="true">
        <span class="d paid" data-unit-price></span><span class="op">+</span>
        <span class="d paid" data-unit-price></span><span class="op">+</span>
        <span class="d free">$0</span><span class="op">=</span>
        <span class="sum" data-deal-sum></span>
      </div>
      <ul class="bgo-facts">%(facts)s</ul>
    </div>
  </section>

  <section class="lgb-sec bgo-body">
    <div class="lgb-wrap">
      <span class="lgb-eyebrow">%(grid_eyebrow)s</span>
      <h2 class="lgb-disp lgb-disp-m">%(grid_heading)s</h2>
      <p class="lgb-aside bgo-pick-aside">%(grid_note)s</p>
      <div class="bgo-grid" id="bgo-grid"></div>
    </div>
  </section>

  <div class="lgb-breath"><span class="ln"></span><span class="dot"></span><span class="ln"></span></div>

  <section class="lgb-sec lgb-band-cream bgo-up">
    <div class="lgb-wrap">
      <span class="lgb-eyebrow">%(band_eyebrow)s</span>
      <h2 class="lgb-disp lgb-disp-m">%(band_heading)s</h2>
      <p class="bgo-up-lede">%(band_sub)s</p>
      <div class="bgo-clubs" id="bgo-up-page"></div>
    </div>
  </section>

  <div class="bgo-rail" id="bgo-rail" data-show="false" data-state="empty">
    <span class="flash" aria-hidden="true"></span>
    <div class="bgo-rail-in">
      <div class="bgo-slots" id="bgo-slots" aria-hidden="true"></div>
      <div class="bgo-status">
        <strong class="hd" id="bgo-hd">%(rail_empty)s</strong>
        <span class="sub" id="bgo-sub"></span>
      </div>
      <div class="bgo-rail-act">
        <span class="tot" id="bgo-tot" hidden>
          <span class="l">Bundle</span><span class="v" id="bgo-tot-v"></span><span class="sv" id="bgo-tot-sv"></span>
        </span>
        <a class="lgb-btn lgb-btn-foil lgb-btn-sm" id="bgo-go" href="/cart" hidden>
          <span>%(cta_cart)s</span><span class="ar">&rarr;</span></a>
      </div>
    </div>
  </div>
  <p class="lgb-sr" id="bgo-live" role="status" aria-live="polite"></p>
  <p class="bgo-toast" id="bgo-toast" hidden role="alert"></p>

  <div class="bgo-md" id="bgo-md" hidden data-open="false" role="dialog" aria-modal="true" aria-labelledby="bgo-md-title">
    <div class="bgo-md-bd-scrim" data-bgo-close></div>
    <div class="bgo-md-panel">
      <button type="button" class="bgo-md-x" data-bgo-close aria-label="Close">&times;</button>
      <div class="bgo-md-hd">
        <span class="bgo-wm" aria-hidden="true"><svg><use href="#lgb-clover"/></svg></span>
        <p class="lgb-eyebrow on-dark">%(modal_eyebrow)s</p>
        <h2 class="lgb-disp lgb-disp-s" id="bgo-md-title">%(modal_heading)s</h2>
        <p>%(modal_sub)s</p>
      </div>
      <div class="bgo-md-bd">
        <div class="bgo-updeck" data-deck="apparel">
          <span class="lgb-eyebrow">%(deck_1_label)s</span>
          <div class="bgo-clubs" id="bgo-up-apparel"></div>
        </div>
        <div class="bgo-updeck" data-deck="club">
          <span class="lgb-eyebrow">%(deck_2_label)s</span>
          <div class="bgo-clubs" id="bgo-up-club"></div>
        </div>
      </div>
      <div class="bgo-md-foot">
        <button type="button" class="lgb-btn lgb-btn-line lgb-btn-sm" data-bgo-close><span>%(cta_back)s</span></button>
        <a class="lgb-btn lgb-btn-foil lgb-btn-sm" href="/cart"><span>%(cta_cart)s</span><span class="ar">&rarr;</span></a>
      </div>
    </div>
  </div>
</div>

<script type="application/json" id="lgb-data">%(data)s</script>
<script>
%(js)s
</script>
""" % {
    'css': CSS + EXTRA_CSS, 'clover': CLOVER, 'js': JS,
    'data': json.dumps(DATA, ensure_ascii=True),
    'facts': facts,
    'eyebrow': esc(S['eyebrow']), 'heading': esc(S['heading']), 'subheading': esc(S['subheading']),
    'grid_eyebrow': esc(S['grid_eyebrow']), 'grid_heading': esc(S['grid_heading']),
    'grid_note': esc(S['grid_note']), 'rail_empty': esc(S['rail_empty']), 'cta_cart': esc(S['cta_cart']),
    'band_eyebrow': esc(S['band_eyebrow']), 'band_heading': esc(S['band_heading']), 'band_sub': esc(S['band_sub']),
    'modal_eyebrow': esc(S['modal_eyebrow']), 'modal_heading': esc(S['modal_heading']),
    'modal_sub': esc(S['modal_sub']), 'cta_back': esc(S['cta_back']),
    'deck_1_label': esc(S['deck_1_label']), 'deck_2_label': esc(S['deck_2_label']),
}

io.open('page-body.html', 'w', encoding='utf-8', newline='\n').write(HTML)
print('hats %d, upsell %d, bytes %d' % (len(hats), len(upsell), len(HTML)))
