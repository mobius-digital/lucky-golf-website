"""Mirror the imagery-led section markup in the preview renderer (build3)."""
import io
p = 'C:/Users/wetzl/Lucky Golf/Website/tools/gwp-preview/build3.cjs'
s = io.open(p, encoding='utf-8').read()
def r(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# image picker values -> the local web copies of the shoot
r("const reviews = BL.filter", """/* image_picker settings point at Shopify Files; the preview maps them to the local shoot copies */
const SHOOT_MAP = { 'gwp-hero-green-read.webp': 'green-read-fit', 'gwp-band-wedges.webp': 'two-gold-wedges', 'gwp-band-hat-mallet.webp': 'black-hat-mallet',
  'gwp-band-putter.webp': 'putter-in-hand', 'gwp-fit-sunset.webp': 'fit-sunset', 'gwp-reviews-hats.webp': 'two-hats-mallet', 'gwp-faq-cup.webp': 'from-the-cup' };
const pic = v => { if (!v) return ''; const f = String(v).split('/').pop(); const n = SHOOT_MAP[f]; if (!n) return '';
  fs.copyFileSync(path.join(ROOT, 'design/img/shoot-0918', n + '.webp'), path.join(OUT, f)); return f; };
const reviews = BL.filter""")

r("""  <section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">${esc(S.hero_eyebrow)}</p>""",
"""  ${pic(S.hero_photo) ? `<section class="gwp-p-hero" style="--focus:${S.hero_focus || '60% 40%'};--focus-m:${S.hero_focus_m || '58% 40%'}">
    <img class="gwp-p-img" src="${pic(S.hero_photo)}" alt="" fetchpriority="high">
    <div class="lg-wrap gwp-p-in">
      <p class="lg-eyebrow gwp-p-eb">${esc(S.hero_eyebrow)}</p>
      <h1 class="lg-d1 gwp-h-h1">${h1}</h1>
      <p class="lg-lede gwp-h-lede">${esc(S.hero_sub)}</p>
      <div class="gwp-h-foot">
        <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">${esc(S.hero_cta)} <span aria-hidden="true">&rarr;</span></a>
        <ul class="gwp-h-trust" role="list">
          <li class="lg-label">${ICON.lock}${esc(S.trust_1)}</li><li class="lg-label">${ICON.back}${esc(S.trust_2)}</li><li class="lg-label">${ICON.ship}${esc(S.trust_3)}</li>
        </ul>
      </div>
    </div>
  </section>` : `<section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">${esc(S.hero_eyebrow)}</p>""")
r("""        </ul>
      </div>
    </div>
  </section>

  <div class="gwp-rail\"""",
"""        </ul>
      </div>
    </div>
  </section>`}

  <div class="gwp-rail\"""")

r("""  ${S.yardage ? '<div class="yd yd-rule" aria-hidden="true"></div>' : ''}
  <section class="lg-sec gwp-contour" id="gwp-gifts"><div class="lg-wrap">""",
"""  ${(S.band_1 || S.band_2 || S.band_3) ? `<section class="gwp-band-ph" aria-label="${esc(S.band_label)}">${[S.band_1, S.band_2, S.band_3].map((b, i) => pic(b) ? `<figure class="gwp-band-f${i === 0 ? ' w2' : ''}"><img src="${pic(b)}" alt="" loading="lazy"></figure>` : '').join('')}</section>` : ''}
  <section class="lg-sec" id="gwp-gifts"><div class="lg-wrap">""")
r("""    <div class="gwp-gift-row">${giftCard('hat', 1, T1, S.gift_hat_title, S.gift_hat_sub)}${giftCard('polo', 2, T2, S.gift_polo_title, S.gift_polo_sub)}</div>""",
"""    <div class="gwp-gifts-grid${pic(S.fit_photo) ? ' has-ph' : ''}">${pic(S.fit_photo) ? `<figure class="gwp-fit-ph"><img src="${pic(S.fit_photo)}" alt="" loading="lazy"><figcaption class="lg-label">${esc(S.fit_caption)}</figcaption></figure>` : ''}
    <div class="gwp-gift-row">${giftCard('hat', 1, T1, S.gift_hat_title, S.gift_hat_sub)}${giftCard('polo', 2, T2, S.gift_polo_title, S.gift_polo_sub)}</div></div>""")
r("""  <section class="lg-band"><div class="lg-wrap">""",
"""  <section class="lg-band${pic(S.reviews_photo) ? ' gwp-rev-ph' : ''}"${pic(S.reviews_photo) ? ` style="--rev-bg:url(${pic(S.reviews_photo)});--rev-pos:${S.reviews_focus || 'center 60%'}"` : ''}><div class="lg-wrap">""")
r("""  <section class="lg-sec gwp-contour"><div class="lg-wrap gwp-faq-wrap">
    <h2 class="lg-d2">${esc(S.faq_heading)}</h2>""",
"""  <section class="lg-sec"><div class="lg-wrap gwp-faq-grid${pic(S.faq_photo) ? ' has-ph' : ''}"><div class="gwp-faq-wrap">
    <h2 class="lg-d2">${esc(S.faq_heading)}</h2>""")
r("""      ${faqs.map(f => `<details class="gwp-fq"><summary><span>${esc(f.q)}</span><span class="mk" aria-hidden="true"></span></summary><div class="gwp-fq-a">${f.a}</div></details>`).join('\\n      ')}
    </div>
  </div></section>""",
"""      ${faqs.map(f => `<details class="gwp-fq"><summary><span>${esc(f.q)}</span><span class="mk" aria-hidden="true"></span></summary><div class="gwp-fq-a">${f.a}</div></details>`).join('\\n      ')}
    </div>
  </div>${pic(S.faq_photo) ? `<figure class="gwp-faq-ph"><img src="${pic(S.faq_photo)}" alt="" loading="lazy"></figure>` : ''}</div></section>""")
io.open(p, 'w', encoding='utf-8').write(s)
print('build3 mirrored')
