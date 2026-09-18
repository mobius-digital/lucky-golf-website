"""Imagery-led promo page (Cole, Sept 18: "whatever you think, do it and push").
Photo hero, a photo band after the clubs, the gifts shown worn, reviews over a
photo, a photo beside the FAQ. Daylight ground. Tracer stays; contour + rulers go.
Every photo is an image_picker setting, so the final edit swaps in without code."""
import io, re
ROOT = 'C:/Users/wetzl/Lucky Golf/Website/'
def rd(p): return io.open(ROOT + p, encoding='utf-8', newline='').read()
def wr(p, s): io.open(ROOT + p, 'w', encoding='utf-8', newline='').write(s)

L = rd('shopify/sections/gwp-promo.liquid')
NL = '\r\n' if '\r\n' in L else '\n'
L = L.replace('\r\n', '\n')
def r(a, b):
    global L
    assert a in L, a[:90]
    L = L.replace(a, b, 1)

# ---------- 1. photo hero (the math hero stays as the fallback when no photo is set)
r("""  <section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">{{ s.hero_eyebrow }}</p>""",
"""  {%- if s.hero_photo != blank -%}
  <!-- ══════════ HERO · the photo leads: the hat, the polo and a gold club in one frame ══════════ -->
  <section class="gwp-p-hero" style="--focus:{{ s.hero_focus | default: '60% 40%' }};--focus-m:{{ s.hero_focus_m | default: '58% 40%' }}">
    {{ s.hero_photo | image_url: width: 2400 | image_tag: widths: '750,1100,1600,2000,2400', sizes: '100vw', loading: 'eager', fetchpriority: 'high', class: 'gwp-p-img', alt: s.hero_photo.alt }}
    <div class="lg-wrap gwp-p-in">
      <p class="lg-eyebrow gwp-p-eb">{{ s.hero_eyebrow }}</p>
      <h1 class="lg-d1 gwp-h-h1">{{ h1 }}</h1>
      <p class="lg-lede gwp-h-lede">{{ s.hero_sub }}</p>
      <div class="gwp-h-foot">
        <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">{{ s.hero_cta }} <span aria-hidden="true">&rarr;</span></a>
        <ul class="gwp-h-trust" role="list">
          {%- if s.trust_1 != blank -%}<li class="lg-label"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>{{ s.trust_1 }}</li>{%- endif -%}
          {%- if s.trust_2 != blank -%}<li class="lg-label"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 1 0 2.6-6.4"/><path d="M3 4v5h5"/></svg>{{ s.trust_2 }}</li>{%- endif -%}
          {%- if s.trust_3 != blank -%}<li class="lg-label"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 7h11v9H2z"/><path d="M13 10h4l3 3v3h-7z"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg>{{ s.trust_3 }}</li>{%- endif -%}
        </ul>
      </div>
    </div>
  </section>
  {%- else -%}
  <section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">{{ s.hero_eyebrow }}</p>""")
r("""      </div>
    </div>
  </section>

  <!-- ══════════ THE RAIL ══════════ -->""",
"""      </div>
    </div>
  </section>
  {%- endif -%}

  <!-- ══════════ THE RAIL ══════════ -->""")

# ---------- 2. photo band after the clubs; rulers and contour out
r("""  <!-- ══════════ THE FREE STUFF ══════════ -->
  {%- if s.yardage -%}<div class="yd yd-rule" aria-hidden="true"></div>{%- endif -%}
  <section class="lg-sec gwp-contour" id="gwp-gifts">""",
"""  <!-- ══════════ PHOTO BAND · the page breathes on photography, not on colour ══════════ -->
  {%- if s.band_1 != blank or s.band_2 != blank or s.band_3 != blank -%}
    <section class="gwp-band-ph" aria-label="{{ s.band_label | escape }}">
      {%- for k in (1..3) -%}
        {%- assign bkey = 'band_' | append: k -%}
        {%- assign bim = s[bkey] -%}
        {%- if bim != blank -%}
          <figure class="gwp-band-f{% if k == 1 %} w2{% endif %}">
            {{ bim | image_url: width: 1600 | image_tag: widths: '600,1000,1600', sizes: '(max-width:749px) 100vw, 50vw', loading: 'lazy', alt: bim.alt }}
          </figure>
        {%- endif -%}
      {%- endfor -%}
    </section>
  {%- endif -%}

  <!-- ══════════ THE FREE STUFF ══════════ -->
  <section class="lg-sec" id="gwp-gifts">""")

# ---------- 3. the gifts, shown worn
r("""      <div class="gwp-gift-row">
        {%- assign gift_slots""",
"""      <div class="gwp-gifts-grid{% if s.fit_photo != blank %} has-ph{% endif %}">
      {%- if s.fit_photo != blank -%}
        <figure class="gwp-fit-ph">
          {{ s.fit_photo | image_url: width: 1400 | image_tag: widths: '600,1000,1400', sizes: '(max-width:749px) 100vw, 40vw', loading: 'lazy', alt: s.fit_photo.alt }}
          {%- if s.fit_caption != blank -%}<figcaption class="lg-label">{{ s.fit_caption }}</figcaption>{%- endif -%}
        </figure>
      {%- endif -%}
      <div class="gwp-gift-row">
        {%- assign gift_slots""")
r("""        {%- endfor -%}
      </div>
    </div>
  </section>

  <!-- ══════════ REVIEWS""",
"""        {%- endfor -%}
      </div>
      </div>
    </div>
  </section>

  <!-- ══════════ REVIEWS""")

# ---------- 4. reviews over a photo
r("""    <section class="lg-band">""",
"""    <section class="lg-band{% if s.reviews_photo != blank %} gwp-rev-ph{% endif %}"{% if s.reviews_photo != blank %} style="--rev-bg:url({{ s.reviews_photo | image_url: width: 2000 }});--rev-pos:{{ s.reviews_focus | default: 'center 60%' }}"{% endif %}>""")

# ---------- 5. FAQ beside a photo
r("""    <section class="lg-sec gwp-contour">
      <div class="lg-wrap gwp-faq-wrap">
        <h2 class="lg-d2">{{ s.faq_heading }}</h2>
        <div class="gwp-faq">""",
"""    <section class="lg-sec">
      <div class="lg-wrap gwp-faq-grid{% if s.faq_photo != blank %} has-ph{% endif %}">
      <div class="gwp-faq-wrap">
        <h2 class="lg-d2">{{ s.faq_heading }}</h2>
        <div class="gwp-faq">""")
r("""          {%- endfor -%}
        </div>
      </div>
    </section>
  {%- endif -%}
""", """          {%- endfor -%}
        </div>
      </div>
      {%- if s.faq_photo != blank -%}
        <figure class="gwp-faq-ph">{{ s.faq_photo | image_url: width: 1200 | image_tag: widths: '600,1200', sizes: '(max-width:749px) 100vw, 40vw', loading: 'lazy', alt: s.faq_photo.alt }}</figure>
      {%- endif -%}
      </div>
    </section>
  {%- endif -%}
""")

# ---------- 6. schema: the photo settings
r("""    { "type": "header", "content": "Hero (the math)" },""",
"""    { "type": "header", "content": "Photos (the page leads with these)" },
    { "type": "image_picker", "id": "hero_photo", "label": "Hero photo", "info": "Full-bleed behind the headline. Blank = the club + gift = price hero instead." },
    { "type": "text", "id": "hero_focus", "label": "Hero photo focus, desktop", "default": "60% 40%", "info": "Where the photo centres: left% top%." },
    { "type": "text", "id": "hero_focus_m", "label": "Hero photo focus, phone", "default": "58% 40%" },
    { "type": "image_picker", "id": "band_1", "label": "Photo band 1 (wide)" },
    { "type": "image_picker", "id": "band_2", "label": "Photo band 2" },
    { "type": "image_picker", "id": "band_3", "label": "Photo band 3" },
    { "type": "text", "id": "band_label", "label": "Photo band label (screen readers)", "default": "On the course" },
    { "type": "image_picker", "id": "fit_photo", "label": "The fit, worn (beside the gift pickers)" },
    { "type": "text", "id": "fit_caption", "label": "Fit photo caption", "default": "The fit: hat + polo, both free over $140" },
    { "type": "image_picker", "id": "reviews_photo", "label": "Photo behind the reviews" },
    { "type": "text", "id": "reviews_focus", "label": "Reviews photo focus", "default": "center 60%" },
    { "type": "image_picker", "id": "faq_photo", "label": "Photo beside the FAQ" },

    { "type": "header", "content": "Hero (the math)" },""")
L = L.replace('\n', NL)
wr('shopify/sections/gwp-promo.liquid', L)

# ---------- CSS
C = rd('shopify/assets/gwp-promo.css').replace('\r\n', '\n')
MARK = '/* ======================= IMAGERY-LED LAYOUT (Sept 18) ======================= */'
if MARK in C: C = C[:C.index(MARK)].rstrip() + '\n'
C += '\n' + MARK + """
/* Photography leads; the instruments only show up where there's a real number.
   All sizes px: the theme's root font is 10px. */

/* hero: full-bleed photo, headline bottom-left over a scrim */
.gwp-p-hero{position:relative;min-height:clamp(560px,78vh,760px);display:flex;align-items:flex-end;overflow:hidden;background:#0B1911;color:#fff}
.gwp-p-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:var(--focus)}
.gwp-p-hero::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(0deg,rgba(6,17,11,.82) 0%,rgba(6,17,11,.45) 38%,rgba(6,17,11,0) 68%),linear-gradient(90deg,rgba(6,17,11,.55) 0%,rgba(6,17,11,0) 55%)}
.gwp-p-in{position:relative;z-index:1;width:100%;padding-block:56px}
.gwp-p-hero .gwp-p-eb{display:inline-flex;background:rgba(6,17,11,.62);-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);color:#EDD27C;padding:8px 12px;border-radius:8px}
.gwp-p-hero .gwp-p-eb::before{display:none}
.gwp-p-hero .gwp-h-h1{color:#fff;max-width:13ch}
.gwp-p-hero .gwp-num{background-image:linear-gradient(180deg,#FFF3C4 0%,#EDD27C 40%,#C29A2B 78%,#EDD27C 100%)}
.gwp-p-hero .gwp-h-lede{color:rgba(255,255,255,.9);max-width:44ch}
.gwp-p-hero .gwp-h-trust li{color:rgba(255,255,255,.82)}
.gwp-p-hero .gwp-h-trust svg{stroke:#EDD27C}
@media (max-width:749px){
  .gwp-p-hero{min-height:620px}
  .gwp-p-img{object-position:var(--focus-m)}
  .gwp-p-in{padding-block:32px}
  .gwp-p-hero::after{background:linear-gradient(0deg,rgba(6,17,11,.9) 0%,rgba(6,17,11,.55) 45%,rgba(6,17,11,.05) 75%)}
}

/* photo band */
.gwp-band-ph{display:grid;grid-template-columns:2fr 1fr 1fr;gap:6px;height:clamp(300px,34vw,460px)}
.gwp-band-f{margin:0;overflow:hidden;min-width:0}
.gwp-band-f img{width:100%;height:100%;object-fit:cover;display:block}
@media (max-width:749px){
  .gwp-band-ph{grid-template-columns:1fr 1fr;height:auto}
  .gwp-band-f{aspect-ratio:1}
  .gwp-band-f.w2{grid-column:1/-1;aspect-ratio:16/10}
}

/* the fit, worn, beside the pickers */
.gwp-gifts-grid.has-ph{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(20px,3vw,40px);align-items:start;margin-top:32px}
.gwp-gifts-grid.has-ph .gwp-gift-row{grid-template-columns:1fr;margin-top:0}
.gwp-fit-ph{margin:0;position:sticky;top:calc(var(--gwp-top) + var(--gwp-rail-h) + 16px);border-radius:var(--rc,18px);overflow:hidden;aspect-ratio:4/5}
.gwp-fit-ph img{width:100%;height:100%;object-fit:cover;display:block}
.gwp-fit-ph figcaption{position:absolute;left:14px;bottom:14px;background:rgba(6,17,11,.72);color:#F4F3F0;padding:8px 12px;border-radius:8px}
@media (max-width:1080px){
  .gwp-gifts-grid.has-ph{grid-template-columns:1fr}
  .gwp-fit-ph{position:relative;top:auto;aspect-ratio:4/3}
}

/* reviews over a photo */
.lg-band.gwp-rev-ph{background-image:var(--rev-bg);background-size:cover;background-position:var(--rev-pos)}
.lg-band.gwp-rev-ph::before{content:'';position:absolute;inset:0;pointer-events:none;background:linear-gradient(90deg,rgba(6,17,11,.84) 0%,rgba(6,17,11,.62) 55%,rgba(6,17,11,.4) 100%)}
.lg-band.gwp-rev-ph>.lg-wrap{position:relative;z-index:1}
.gwp-rev-ph .gwp-rev{background:rgba(6,17,11,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);border:1px solid rgba(237,210,124,.25)}

/* FAQ beside a photo */
.gwp-faq-grid.has-ph{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);gap:clamp(24px,4vw,56px);align-items:center}
.gwp-faq-ph{margin:0;border-radius:var(--rc,18px);overflow:hidden;aspect-ratio:4/5}
.gwp-faq-ph img{width:100%;height:100%;object-fit:cover;display:block}
@media (max-width:749px){ .gwp-faq-grid.has-ph{grid-template-columns:1fr} .gwp-faq-ph{aspect-ratio:4/3} }
"""
C = C.replace('\n', '\r\n')
wr('shopify/assets/gwp-promo.css', C)

# ---------- template: Daylight + the photos (uploaded to Files as these names)
import json
TP = ROOT + 'shopify/templates/page.gwp-promo.json'
tj = json.load(io.open(TP, encoding='utf-8'))
st = tj['sections']['main']['settings']
st.update({
  'ground': 'day',
  'hero_photo': 'shopify://shop_images/gwp-hero-green-read.webp', 'hero_focus': '62% 38%', 'hero_focus_m': '60% 40%',
  'band_1': 'shopify://shop_images/gwp-band-wedges.webp', 'band_2': 'shopify://shop_images/gwp-band-hat-mallet.webp',
  'band_3': 'shopify://shop_images/gwp-band-putter.webp',
  'fit_photo': 'shopify://shop_images/gwp-fit-sunset.webp',
  'reviews_photo': 'shopify://shop_images/gwp-reviews-hats.webp', 'reviews_focus': 'center 70%',
  'faq_photo': 'shopify://shop_images/gwp-faq-cup.webp'})
io.open(TP, 'w', encoding='utf-8', newline='').write(json.dumps(tj, indent=2, ensure_ascii=False).replace('\n', '\r\n') + '\r\n')
print('liquid, css, template patched')
