"""Port the approved design into the real Shopify files so the section is the ONE
source and the preview is rendered from it (no more drift between the two).
  - gwp-promo.css : grounds (Daylight / Twilight), the Yardage layer, hero D, contour
  - gwp-promo.js  : the live tracer (ball flies the real arc to where the bag is)
  - gwp-promo.liquid : hero D + settings, tracer, ruler, contour sections, ground switch
"""
import io, re, os
ROOT = "C:/Users/wetzl/Lucky Golf/Website/"
def load(p): return io.open(ROOT + p, encoding='utf-8').read()
def save(p, s): io.open(ROOT + p, 'w', encoding='utf-8').write(s)

# ======================= CSS =======================
b = load('tools/gwp-preview/build-system.cjs')
css = b[b.index('const CSS = `') + len('const CSS = `'): b.index('/* ===================== the picker (preview only)')]
css = css.replace('.gs-', '.gwp-h-')
css = css.replace('html[data-ground="twilight"] body.lg{background:#06110B;color:#F4F3F0}', '.gwp[data-ground="twilight"]{background:#06110B;color:#F4F3F0}')
css = css.replace('html[data-ground=', '.gwp[data-ground=')
css = re.sub(r'(?<![\w.])\[data-ground=', '.gwp[data-ground=', css)
css = css.replace('[data-yardage="on"] .gwp{counter-reset:yd}', '.gwp[data-yardage="on"]{counter-reset:yd}')
css = css.replace('[data-yardage="on"] .gwp section', '.gwp[data-yardage="on"] section')
css = re.sub(r'(?<![\w.])\[data-yardage=', '.gwp[data-yardage=', css)
# range rings -> the default green map (Contour A), as a real asset
rs, re_ = css.index('/* 4 · range rings'), css.index('/* 5 · hole numbers')
css = css[:rs] + """/* 4 · the green map (Contour A, the default): real contour lines fading in behind a
   flat section. Never behind the type's own column: the mask keeps the left clear. */
.gwp-contour{position:relative;isolation:isolate}
.gwp[data-yardage="on"] .gwp-contour::before{content:'';position:absolute;inset:0;z-index:-1;pointer-events:none;
  background-repeat:no-repeat;background-size:cover;background-position:right center;
  -webkit-mask-image:linear-gradient(90deg,transparent 30%,#000 85%);mask-image:linear-gradient(90deg,transparent 30%,#000 85%)}
.gwp[data-yardage="on"] .gwp-contour-l::before{-webkit-mask-image:linear-gradient(270deg,transparent 30%,#000 85%);mask-image:linear-gradient(270deg,transparent 30%,#000 85%);background-position:left center}
.gwp[data-ground="day"] .gwp-contour::before{background-image:var(--gwp-contour-day)}
.gwp[data-ground="twilight"] .gwp-contour::before{background-image:var(--gwp-contour-tw)}

""" + css[re_:]
css = css.replace('\n.gwp[data-ground="day"] .yd-rings::before{background-image:${rings(\'rgba(23,20,15,.22)\')}}', '')
# glow is a Twilight-only effect: on white it just reads as blur
css += """
/* Glow is Twilight only. On Daylight it just reads as blur. */
.gwp[data-ground="day"] .gwp-fill{box-shadow:none}
.gwp[data-ground="day"] .yd-ball{filter:none}
"""
assert '${' not in css, 'template leftovers in css'
c = load('shopify/assets/gwp-promo.css')
MARK = '/* ======================= GROUNDS + YARDAGE (system v4) ======================= */'
if MARK in c: c = c[:c.index(MARK)]
c = c.rstrip() + '\n\n' + MARK + '\n' + css
save('shopify/assets/gwp-promo.css', c)

# ======================= JS: the live tracer =======================
j = load('shopify/assets/gwp-promo.js')
TRACER = r"""
  /* ------------------------------------------------------------- the tracer
     One shot, drawn the way a launch monitor draws it: carries to the first
     flag, hops to the second, releases to the green. Built from the real
     thresholds, and the ball flies the arc to wherever the bag is. It reads
     the same number the bar does, so the two can never disagree. */
  (function tracer() {
    var host = document.getElementById('gwp-tracer');
    if (!host || !fillEl) return;
    var MAXV = SHIP > T2 ? SHIP : T2, X = function (v) { return 40 + (v / MAXV) * 1120; };
    var stops = [T1, T2].concat(SHIP > T2 ? [SHIP] : []);
    var labels = [].slice.call(root.querySelectorAll('.gwp-node b')).map(function (b) { return b.textContent; });
    var NS = 'http://www.w3.org/2000/svg', svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 1200 170'); svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
    var ticks = '';
    for (var i = 0; i <= 22; i++) { var tx = 40 + i * (1120 / 22); ticks += '<line x1="' + tx + '" x2="' + tx + '" y1="140" y2="' + (i % 2 ? 147 : 152) + '"/>'; }
    var d = 'M40 140', prev = 40, lift = [-60, 40, 108];
    stops.forEach(function (v, k) { var x = X(v); d += ' Q ' + ((prev + x) / 2) + ' ' + lift[k] + ' ' + x + ' 140'; prev = x; });
    var flags = stops.map(function (v, k) {
      return '<g class="yd-flag" transform="translate(' + X(v) + ' 140)"><line y2="-34"/><path d="M0 -34 L16 -28 L0 -22Z"/><text y="24" text-anchor="' + (k === stops.length - 1 ? 'end' : 'middle') + '"></text></g>';
    }).join('');
    svg.innerHTML = '<g class="yd-ticks">' + ticks + '<line x1="40" x2="1160" y1="140" y2="140"/></g>' +
      '<path class="yd-path" pathLength="1" d="' + d + '"/><circle class="yd-apex" cx="' + (40 + X(T1)) / 2 + '" cy="40" r="3.5"/>' + flags +
      '<text class="yd-tee" x="40" y="164"></text><circle class="yd-ball" cx="40" cy="140" r="6"/>';
    [].slice.call(svg.querySelectorAll('.yd-flag text')).forEach(function (t, k) { t.textContent = labels[k] || ''; });
    svg.querySelector('.yd-tee').textContent = host.getAttribute('data-tee') || '';
    var wrap = host.querySelector('.lg-wrap') || host; wrap.appendChild(svg);

    var pathEl = svg.querySelector('.yd-path'), ball = svg.querySelector('.yd-ball'), L = pathEl.getTotalLength(), cur = 0, raf = null;
    function lenAtX(x) { var lo = 0, hi = L; for (var n = 0; n < 22; n++) { var m = (lo + hi) / 2; if (pathEl.getPointAtLength(m).x < x) lo = m; else hi = m; } return lo; }
    function place(len) { cur = len; var p = pathEl.getPointAtLength(len); ball.setAttribute('cx', p.x); ball.setAttribute('cy', p.y); }
    /* A hidden tab gets no animation frames, so the ball would freeze mid-flight.
       If nobody can see it, or they asked for less motion, it just lands. */
    function fly(to) {
      cancelAnimationFrame(raf);
      if (document.hidden || window.matchMedia('(prefers-reduced-motion: reduce)').matches) { place(to); return; }
      var from = cur, t0 = performance.now(), dur = 900 + Math.abs(to - from) * 1.1;
      (function step(now) { var k = Math.min(1, (now - t0) / dur); k = 1 - Math.pow(1 - k, 3); place(from + (to - from) * k); if (k < 1) raf = requestAnimationFrame(step); })(t0);
    }
    function sync() { var pct = parseFloat(fillEl.style.width) || 0; fly(lenAtX(40 + pct / 100 * 1120)); }
    new MutationObserver(sync).observe(fillEl, { attributes: true, attributeFilter: ['style'] });
    sync();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) { es.forEach(function (e) { if (e.isIntersecting) { host.classList.add('is-in'); o.disconnect(); } }); }, { threshold: .4 }).observe(host);
    } else host.classList.add('is-in');
  })();
"""
TMARK = '  /* ------------------------------------------------------------- the tracer'
if TMARK in j:
    j = j[:j.index(TMARK)] + j[j.index('  /* ------------------------------------------------------------------ boot */'):]
j = j.replace('  /* ------------------------------------------------------------------ boot */', TRACER.lstrip('\n') + '\n  /* ------------------------------------------------------------------ boot */', 1)
save('shopify/assets/gwp-promo.js', j)

# ======================= LIQUID =======================
l = load('shopify/sections/gwp-promo.liquid')
hs, he = l.index('  <!-- ══════════ HERO ══════════ -->'), l.index('  <!-- ══════════ THE RAIL ══════════ -->')
HERO = r"""  <!-- ══════════ HERO · the math: club + gift = price ══════════
       The tiles are plain on purpose: nothing sits over the product. The
       threshold amounts in the headline pick up the gold gradient on their
       own, so the headline stays a plain text setting. -->
  {%- liquid
    assign t1s = t1 | money_without_trailing_zeros | strip_html
    assign t2s = t2 | money_without_trailing_zeros | strip_html
  -%}
  {%- capture t1span -%}<span class="gwp-num">{{ t1s }}</span>{%- endcapture -%}
  {%- capture t2span -%}<span class="gwp-num">{{ t2s }}</span>{%- endcapture -%}
  {%- liquid
    assign h1 = s.hero_heading | escape | replace: t2s, t2span | replace: t1s, t1span
    if s.hero_gold_word != blank
      capture gw
        echo '<span class="gwp-num">' | append: s.hero_gold_word | append: '</span>'
      endcapture
      assign h1 = h1 | replace_first: s.hero_gold_word, gw
    endif
    assign hat_img = hat.variants.first.image | default: hat.featured_image
    assign polo_img = polo.variants.first.image | default: polo.featured_image
  -%}
  <section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">{{ s.hero_eyebrow }}</p>
      <h1 class="lg-d1 gwp-h-h1">{{ h1 }}</h1>
      <p class="lg-lede gwp-h-lede">{{ s.hero_sub }}</p>
      <div class="gwp-h-sums">
        {%- for n in (1..2) -%}
          {%- liquid
            if n == 1
              assign sp = s.sum1_product
              assign si = s.sum1_image_index | default: 1 | minus: 1
              assign snote = s.sum1_note
              assign gcap = s.sum_gift1_label
              assign gtag = s.free_tag
            else
              assign sp = s.sum2_product
              assign si = s.sum2_image_index | default: 1 | minus: 1
              assign snote = s.sum2_note
              assign gcap = s.sum_gift2_label
              assign gtag = s.both_free_tag
            endif
          -%}
          {%- if sp != blank -%}
            {%- assign simg = sp.images[si] | default: sp.featured_image -%}
            <div class="gwp-h-sum">
              <figure class="gwp-h-fig">
                <div class="gwp-h-tile">
                  {%- if simg -%}{{ simg | image_url: width: 600 | image_tag: widths: '300,600', sizes: '(max-width:760px) 44vw, 260px', loading: 'eager', alt: sp.title }}{%- endif -%}
                  <span class="lg-tag">{{ sp.price_min | money_without_trailing_zeros }}</span>
                </div>
                <figcaption class="lg-label">{{ sp.title }}</figcaption>
              </figure>
              <span class="gwp-h-op" aria-hidden="true">+</span>
              <figure class="gwp-h-fig">
                <div class="gwp-h-tile{% if n == 2 %} gwp-h-pair{% endif %}">
                  {%- if hat_img -%}{{ hat_img | image_url: width: 500 | image_tag: loading: 'eager', alt: hat.title }}{%- endif -%}
                  {%- if n == 2 and polo_img -%}{{ polo_img | image_url: width: 500 | image_tag: loading: 'eager', alt: polo.title }}{%- endif -%}
                  <span class="lg-tag lg-tag-gold">{{ gtag }}</span>
                </div>
                <figcaption class="lg-label">{{ gcap }}</figcaption>
              </figure>
              <span class="gwp-h-op gwp-h-eq" aria-hidden="true">=</span>
              <div class="gwp-h-res"><b class="gwp-num-d">{{ sp.price_min | money_without_trailing_zeros }}</b><span>{{ snote }}</span></div>
            </div>
          {%- endif -%}
        {%- endfor -%}
      </div>
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

"""
l = l[:hs] + HERO + l[he:]

# root: ground + yardage switches, contour asset urls
l = l.replace('''<div class="lg-scope gwp" id="gwp"
     style="--gwp-top:{{ s.sticky_offset | default: 0 }}px"''',
'''<div class="lg-scope gwp" id="gwp"
     data-ground="{{ s.ground | default: 'twilight' }}" data-yardage="{% if s.yardage %}on{% else %}off{% endif %}"
     style="--gwp-top:{{ s.sticky_offset | default: 0 }}px;--gwp-contour-day:url({{ 'gwp-contour-day.svg' | asset_url }});--gwp-contour-tw:url({{ 'gwp-contour-tw.svg' | asset_url }})"''', 1)
assert 'data-ground=' in l

# tracer after the rail, ruler before the gifts, contour on the flat sections
l = l.replace('  <!-- ══════════ THE CLUBS ══════════ -->',
'''  <!-- ══════════ THE TRACER · the one Yardage moment between offer and clubs ══════════ -->
  {%- if s.yardage -%}
    <div class="yd yd-tracer" id="gwp-tracer" data-tee="{{ s.tee_label | escape }}" aria-hidden="true"><div class="lg-wrap"></div></div>
  {%- endif -%}

  <!-- ══════════ THE CLUBS ══════════ -->''', 1)
l = l.replace('''  <section class="lg-sec" id="gwp-gifts" style="padding-top:0">''',
'''  {%- if s.yardage -%}<div class="yd yd-rule" aria-hidden="true"></div>{%- endif -%}
  <section class="lg-sec gwp-contour" id="gwp-gifts">''', 1)
l = l.replace('''    <section class="lg-sec">
      <div class="lg-wrap gwp-faq-wrap">''', '''    <section class="lg-sec gwp-contour gwp-contour-l">
      <div class="lg-wrap gwp-faq-wrap">''', 1)
assert 'gwp-contour gwp-contour-l' in l and 'id="gwp-tracer"' in l and 'yd-rule' in l

# ---- schema: out with the photo hero, in with ground / yardage / hero D ----
hs2 = l.index('    { "type": "header", "content": "Hero" },')
he2 = l.index('    { "type": "header", "content": "The sticky bar" },')
l = l[:hs2] + '''    { "type": "header", "content": "Look" },
    { "type": "select", "id": "ground", "label": "Ground", "default": "twilight",
      "options": [{ "value": "twilight", "label": "Twilight round (promos, drops)" }, { "value": "day", "label": "Daylight (everyday)" }] },
    { "type": "checkbox", "id": "yardage", "label": "Yardage layer (tracer, ruler, contour, section numbers)", "default": true },
    { "type": "text", "id": "tee_label", "label": "Tracer start label", "default": "Tee · $0" },

    { "type": "header", "content": "Hero (the math)" },
    { "type": "text", "id": "hero_eyebrow", "label": "Eyebrow", "default": "This weekend only · Ends Sunday, Sept 20" },
    { "type": "text", "id": "hero_heading", "label": "Headline", "info": "The two threshold amounts turn gold on their own.", "default": "$90 gets the hat. $140 gets the fit." },
    { "type": "text", "id": "hero_gold_word", "label": "Extra gold word (optional)", "info": "Only for a headline with no dollar amounts in it." },
    { "type": "textarea", "id": "hero_sub", "label": "Subhead", "default": "The fit's a hat and a polo, both on us, both your pick. Every club here gets you the hat on its own." },
    { "type": "text", "id": "hero_cta", "label": "Button", "default": "Show me the clubs" },
    { "type": "product", "id": "sum1_product", "label": "Row 1 club (clears the hat)" },
    { "type": "number", "id": "sum1_image_index", "label": "Row 1 photo (1 = first)", "default": 5 },
    { "type": "text", "id": "sum1_note", "label": "Row 1 note", "default": "Any club gets you the hat." },
    { "type": "text", "id": "sum_gift1_label", "label": "Row 1 gift caption", "default": "Any hat" },
    { "type": "product", "id": "sum2_product", "label": "Row 2 club (clears both)" },
    { "type": "number", "id": "sum2_image_index", "label": "Row 2 photo (1 = first)", "default": 5 },
    { "type": "text", "id": "sum2_note", "label": "Row 2 note", "default": "Over $140 the polo comes too. Over $198, shipping's free." },
    { "type": "text", "id": "sum_gift2_label", "label": "Row 2 gift caption", "default": "The fit: hat + polo" },
    { "type": "text", "id": "both_free_tag", "label": "Row 2 tag", "default": "Both free" },
    { "type": "text", "id": "trust_1", "label": "Trust line 1", "default": "Secure checkout" },
    { "type": "text", "id": "trust_2", "label": "Trust line 2", "default": "Sixty days to prove us wrong" },
    { "type": "text", "id": "trust_3", "label": "Trust line 3", "default": "Free shipping over $198" },

''' + l[he2:]
save('shopify/sections/gwp-promo.liquid', l)
print('ported: css', len(css), 'chars · tracer in js · hero D + switches in liquid')
