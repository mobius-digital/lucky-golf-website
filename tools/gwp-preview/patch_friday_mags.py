"""1) The promo runs through Friday Sept 25 (Cole, 2026-09-18), not Sunday.
   2) Mags on the unlock message only (never on errors or the gift-lost note)."""
import io, shutil
ROOT = "C:/Users/wetzl/Lucky Golf/Website/"
def patch(p, pairs):
    s = io.open(ROOT + p, encoding='utf-8').read()
    for a, b in pairs:
        assert a in s, (p, a[:70]); s = s.replace(a, b)
    io.open(ROOT + p, 'w', encoding='utf-8').write(s)

EYE_OLD, EYE_NEW = "This weekend only · Ends Sunday, Sept 20", "One week only · Ends Friday, Sept 25"
DONE_OLD, DONE_NEW = "Hat, polo, free shipping. Go check out before Sunday.", "Hat, polo, free shipping. Check out before it ends Friday."

patch('shopify/sections/gwp-promo.liquid', [
    ("FREE HAT, FREE POLO · ends Sunday", "FREE HAT, FREE POLO · ends Friday, Sept 25"),
    (EYE_OLD, EYE_NEW), (DONE_OLD, DONE_NEW),
    ('  <p class="gwp-toast" id="gwp-toast" hidden role="alert"></p>',
     '''  <div class="gwp-toast" id="gwp-toast" hidden role="alert">
    {%- if s.toast_mags -%}<img class="gwp-toast-mags" src="{{ 'gwp-mags.webp' | asset_url }}" alt="" width="64" height="40" hidden>{%- endif -%}
    <span data-toast-text></span>
  </div>'''),
    ('''    { "type": "text", "id": "toast_gift_won",''',
     '''    { "type": "checkbox", "id": "toast_mags", "label": "Mags on the unlock message", "info": "Needs assets/gwp-mags.webp. Only on unlocks, never on errors.", "default": true },
    { "type": "text", "id": "toast_gift_won",'''),
])
patch('shopify/templates/page.gwp-promo.json', [
    (EYE_OLD, EYE_NEW), (DONE_OLD, DONE_NEW),
    ("<p>Sunday, September 20. After that the hat's $29 again.</p>", "<p>Friday, September 25. After that the hat's $29 again.</p>"),
])
patch('shopify/GWP-PROMO-README.md', [
    ("# Free hat, free polo · ends Sunday, Sept 20", "# Free hat, free polo · ends Friday, Sept 25"),
    (DONE_OLD, DONE_NEW),
    ("| `assets/gwp-contour-tw.svg` | `assets/` (the contour map, Twilight colours) |",
     "| `assets/gwp-contour-tw.svg` | `assets/` (the contour map, Twilight colours) |\n| `assets/gwp-mags.webp` | `assets/` (Mags, on the unlock message) |"),
    ("Upload the five assets", "Upload the six assets"),
])
patch('design/YARDAGE-SYSTEM.md', [("(Sept 18-20, 2026)", "(Sept 18-25, 2026)"), ("one-weekend pages", "short promos"),
    ("Open question: a small\nMags in the \"you unlocked it\" toast.", "Mags now pops up on the \"you unlocked it\"\nmessage only, never on errors.")])
patch('tools/gwp-preview/build3.cjs', [
    ("<a href=\"#\"><b>Free hat</b> with any club this weekend</a>", "<a href=\"#\"><b>Free hat</b> with any club through Friday</a>"),
    ('  <p class="gwp-toast" id="gwp-toast" hidden role="alert"></p>',
     '  <div class="gwp-toast" id="gwp-toast" hidden role="alert">${S.toast_mags ? \'<img class="gwp-toast-mags" src="gwp-mags.webp" alt="" width="64" height="40" hidden>\' : \'\'}<span data-toast-text></span></div>'),
    ("'gwp-contour-day.svg', 'gwp-contour-tw.svg'])", "'gwp-contour-day.svg', 'gwp-contour-tw.svg', 'gwp-mags.webp'])"),
])
patch('tools/gwp-preview/build-system.cjs', [
    ("""  s = s.split('src="mags-bag-light.webp"')""",
     """  s = s.split('src="gwp-mags.webp"').join('src="data:image/webp;base64,' + fs.readFileSync(path.join(H, 'gwp-mags.webp')).toString('base64') + '"');
  s = s.split('src="mags-bag-light.webp"')"""),
])
patch('shopify/assets/gwp-promo.js', [
    ("""  function toast(msg) {
    if (!msg || !toastEl) return;
    toastEl.textContent = msg;""",
     """  var toastText = toastEl && toastEl.querySelector('[data-toast-text]');
  var toastMags = toastEl && toastEl.querySelector('.gwp-toast-mags');
  /* Mags only shows up for good news. An error with a bird on it is a joke
     at the customer's expense. */
  function toast(msg, mags) {
    if (!msg || !toastEl) return;
    (toastText || toastEl).textContent = msg;
    if (toastMags) toastMags.hidden = !mags;
    toastEl.classList.toggle('has-mags', !!(mags && toastMags));"""),
    ("toast(fill(COPY.giftWon, { gift: tier >= 2 ? COPY.g2 : COPY.g1 }));",
     "toast(fill(COPY.giftWon, { gift: tier >= 2 ? COPY.g2 : COPY.g1 }), true);"),
])
patch('shopify/assets/gwp-promo.css', [
    (".gwp-toast[hidden]{display:none}",
     """.gwp-toast[hidden]{display:none}
.gwp-toast.has-mags{display:flex;align-items:center;gap:14px;padding-left:12px}
.gwp-toast-mags{flex:none;width:64px;height:auto;animation:gwp-mags .5s var(--lg-ease) 1}
.gwp-toast-mags[hidden]{display:none}
@keyframes gwp-mags{from{opacity:0;translate:-10px 0}to{opacity:1;translate:0 0}}
@media (prefers-reduced-motion:reduce){.gwp-toast-mags{animation:none}}"""),
])
shutil.copyfile(ROOT + 'img/mags-light.webp', ROOT + 'shopify/assets/gwp-mags.webp')
print('friday + mags done')
