"""Club product page sections (templates/product.club.json). Imported by build_sections.py.

One template serves the five clubs. Product data (title, price, variants, stock, media, reviews) is
live Liquid; the per-club words and photos come from the product metafield custom.club_page (json,
built by tools/theme/club_data.py). Section settings hold only what is the same on every club.
"""
import os
from common import section, text, textarea, rich, url, img, check, select, rng, header, para

HERE = os.path.dirname(__file__)
S = {}

C = "{%- assign c = product.metafields.custom.club_page.value -%}\n"
MIN = """{%- liquid
  assign min = settings.lg_review_min | default: 10
  assign rc = product.metafields.reviews.rating_count.value | default: 0
-%}
"""


def load(name):
    return open(os.path.join(HERE, name), encoding="utf-8").read()


def foil(expr):
    return expr + " | replace: '<em>', '<span class=\"lg-foil-word\">' | replace: '</em>', '</span>'"


# ---------------------------------------------------------------- the fold
main = load("club_main.liquid").replace('<script src="{{ \'lg-club.js\' | asset_url }}" defer></script>',
                                         "<script>\n" + load("club.js") + "\n</script>")
S["lg-club-main"] = section("Club: buy box", main, [
    header("Breadcrumb"),
    text("crumb_label", "Crumb", "Clubs"), url("crumb_url", "Crumb link"),
    text("crumb2_label", "Wedges crumb (wedges only)", "Wedges"), url("crumb2_url", "Wedges crumb link"),
    header("Gallery"),
    para("The gallery is the product's own media (Products > the club > Media), led by its card cutout. Five show, the rest behind the button."),
    text("gal_all", "Show-all button ([n] = number of photos)", "See all [n] photos"),
    header("Buy box"),
    para("Every club's own words live on the product (metafield custom.club_page); its photos are the metafields Club page photos, Club photo band, Club spec photo and Finish swatch. Price, hands, lofts and stock are live."),
    text("atc", "Button (if the product has none)", "Put it in the bag"),
    text("in_stock", "In-stock line", "In stock · ships in 1 to 2 days"),
    text("set_hint", "Wedge set hint", "Two or more and shipping's on us"),
    text("set1", "1 wedge line", "Just the one"), text("set2", "2 wedges line", "Gap and sand"), text("set3", "3 wedges line", "Gap, sand and lob"),
    text("returns_link", "Returns link", "Sixty days to make up your mind"), url("returns_url", "Returns page (non-wedges)"),
    text("delivery_link", "Delivery link (wedges)", "When will it get here?"),
    text("ship_link", "Shipping link (non-wedges)", "Free shipping at $198"), url("ship_url", "Shipping page"),
    header("Pop-ups"),
    text("helper_title", "Loft helper title", "Let's find your lofts"),
    textarea("helper_line", "Loft helper line", "Two quick questions. Keep four to six degrees between your wedges and each one gets its own yardage, instead of two of them going the same distance."),
    textarea("notify_line", "Back-in-stock line", "Drop your email. You'll get one message when it's back, and that's it."),
    textarea("write_line", "Write a review line", "Tell other golfers how it plays: the stars, a few words, and a photo if you've got one. Buy it from us and your review gets the verified badge."),
    {"type": "richtext", "id": "returns_body", "label": "Returns pop-up"},
    {"type": "richtext", "id": "delivery_body", "label": "Delivery pop-up"},
], presets=False)

# ---------------------------------------------------------------- the film
S["lg-club-film"] = section("Club: story + film", C + """
{%- if c.story -%}
<section class="lg-sec film" id="film" style="padding-top:0"><div class="lg-wrap">
  <div class="lg-split">
    <div>
      <p class="lg-eyebrow">{{ c.story.eyebrow }}</p>
      <h2 class="lg-d2">{{ """ + foil("c.story.head") + """ }}</h2>
      {%- for p in c.story.body %}<p class="lg-body">{{ p }}</p>{% endfor -%}
      {%- if c.who != blank -%}<div class="whofor"><span class="lg-label">{{ section.settings.who_label }}</span><p>{{ c.who }}</p></div>{%- endif -%}
    </div>
    {%- assign vid = section.settings.video -%}
    {%- if vid == blank -%}{%- for m in product.media -%}{%- if vid == blank -%}{%- if m.media_type == 'video' or m.media_type == 'external_video' -%}{%- assign vid = m -%}{%- endif -%}{%- endif -%}{%- endfor -%}{%- endif -%}
    {%- assign ph = product.featured_image -%}
    {%- if product.media.size > 1 -%}{%- assign ph = product.media[1].preview_image -%}{%- endif -%}
    {%- if vid != blank -%}
      <div class="film-v">{%- if vid.media_type == 'external_video' -%}{{ vid | external_video_tag }}{%- else -%}{{ vid | video_tag: controls: true, playsinline: true, preload: 'metadata', image_size: '1400x' }}{%- endif -%}</div>
    {%- elsif ph != blank -%}
      {%- assign pha = ph.alt | default: product.title -%}
      <figure class="film-ph" data-zoom="{{ ph | image_url: width: 2000 }}">{{ ph | image_url: width: 1400 | image_tag: loading: 'lazy', alt: pha, widths: '700,1000,1400', sizes: '(max-width: 900px) 100vw, 55vw' }}</figure>
    {%- endif -%}
  </div>
</div></section>
{%- endif -%}
""", [text("who_label", "Fit label", "Who it's for"), {"type": "video", "id": "video", "label": "Film for every club", "info": "Empty: the product's own video, else a product photo"}], presets=False)

# ---------------------------------------------------------------- the grinds (wedges)
S["lg-club-grinds"] = section("Club: grinds", C + """
{%- if c.grinds -%}{%- assign gr = c.grinds -%}
<section class="lg-sec" id="grinds"><div class="lg-wrap">
  <div class="hd two">
    <div><p class="lg-eyebrow">{{ gr.eyebrow }}</p><h2 class="lg-d2">{{ gr.head }}</h2></div>
    <p class="lg-body">{{ gr.body }}</p>
  </div>
  <div class="kvs">
    {%- for p in gr.panels -%}
      {%- if p.link -%}{%- assign lp = all_products[p.link[0]] -%}
      <a class="lg-panel" href="{{ lp.url }}" style="text-decoration:none;color:inherit"><span class="lg-tag">{{ p.tag }}</span><h3 class="lg-d3">{{ p.h }}</h3><p>{{ p.p }}</p><span class="lg-link">{{ p.link[1] }} <span>&rarr;</span></span></a>
      {%- else -%}
      <div class="lg-panel"><span class="lg-tag">{{ p.tag }}</span><h3 class="lg-d3">{{ p.h }}</h3><p>{{ p.p }}</p>
        {%- if p.hud -%}<div class="lg-hud">{%- for h in p.hud -%}<span><b>{{ h[0] }}</b>{{ h[1] }}</span>{%- endfor -%}</div>{%- endif -%}</div>
      {%- endif -%}
    {%- endfor -%}
  </div>
</div></section>
{%- endif -%}
""", [], presets=False)

# ---------------------------------------------------------------- in the wild (the one dark band)
S["lg-club-wild"] = section("Club: in the wild", load("club_wild.liquid"), [
    text("eyebrow", "Eyebrow", "Tagged"), text("heading", "Heading", "Caught in the wild"),
    textarea("sub", "Line", "Stuck one close with yours? Tag @luckygolfofficial and you might end up on this page."),
    rng("limit", "Posts to show", 3, 12, 1, 8), text("btn_label", "Button"), url("btn_url", "Button link"),
    para("Posts are Content > Metaobjects > Community post. The ones with this club in them come first.")], presets=False)

# ---------------------------------------------------------------- the finish world (wedges with two finishes)
S["lg-club-world"] = section("Club: finish world", C + """
{%- if c.world != blank -%}{%- assign s = section.settings -%}
<section id="finishes" data-mood="{{ c.world }}" data-metal="{{ c.world }}" style="padding-bottom:var(--lg-sec)">
  <div class="lg-wrap">
    <div class="hd">
      <div><p class="lg-eyebrow">{{ s.eyebrow }}</p>{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div>
      <div class="seg" data-moodseg role="group" aria-label="Finish">
        {%- for b in section.blocks -%}{%- if b.type == 'world' -%}<button class="lg-chip" type="button" data-m="{{ b.settings.key }}" aria-pressed="{% if b.settings.key == c.world %}true{% else %}false{% endif %}" {{ b.shopify_attributes }}>{{ b.settings.label }}</button>{%- endif -%}{%- endfor -%}
      </div>
    </div>
  </div>
  <div class="mhero">
    {%- for b in section.blocks -%}{%- if b.type == 'world' -%}{%- assign w = b.settings -%}
    <div class="mh" data-mh="{{ w.key }}"{% if w.key != c.world %} hidden{% endif %}>
      {%- if w.image != blank -%}{{ w.image | image_url: width: 2400 | image_tag: loading: 'lazy', alt: w.image.alt, widths: '750,1200,1800,2400', sizes: '100vw', style: w.pos }}{%- endif -%}
      {%- for p in section.blocks -%}{%- if p.type == 'point' and p.settings.world == w.key -%}
      <div class="pt{% if p.settings.left %} l{% endif %}" style="left:{{ p.settings.x }}%;top:{{ p.settings.y }}%" {{ p.shopify_attributes }}><i>{{ p.settings.n }}</i><div><b>{{ p.settings.title }}</b>{{ p.settings.text }}</div></div>
      {%- endif -%}{%- endfor -%}
      <div class="cap lg-hero-copy" style="position:absolute;inset:auto 0 0 0"><div class="lg-wrap"><h3 class="lg-d1">{{ w.heading }}</h3>{% if w.body != blank %}<p class="lg-body">{{ w.body }}</p>{% endif %}</div></div>
    </div>
    {%- endif -%}{%- endfor -%}
  </div>
  {%- for b in section.blocks -%}{%- if b.type == 'world' -%}{%- assign wk = b.settings.key -%}
  <div class="rail" data-rail="{{ wk }}"{% if wk != c.world %} hidden{% endif %}>
    {%- for r in section.blocks -%}{%- if r.settings.world == wk -%}
      {%- if r.type == 'photo' and r.settings.image != blank -%}
      <figure class="r{{ r.settings.ratio }}" data-zoom="{{ r.settings.image | image_url: width: 2000 }}" {{ r.shopify_attributes }}>{{ r.settings.image | image_url: width: 900 | image_tag: loading: 'lazy', alt: r.settings.alt, widths: '450,700,900', sizes: '40vw', style: r.settings.pos }}</figure>
      {%- endif -%}
    {%- endif -%}{%- endfor -%}
  </div>
  {%- endif -%}{%- endfor -%}
  <div class="lg-wrap rail-foot">
    <div class="arrows" data-railarrows><button type="button" aria-label="Previous">&lsaquo;</button><button type="button" aria-label="Next">&rsaquo;</button></div>
    {% if s.foot != blank %}<p class="lg-body">{{ s.foot }}</p>{% endif %}
  </div>
</section>
{%- endif -%}
""", [para("Shows only on clubs whose custom.club_page has a \"world\" (the Carver: gold or black). It opens on that finish."),
      text("eyebrow", "Eyebrow", "Two finishes"), text("heading", "Heading (<em>word</em> = gold, <br> = new line)"),
      text("foot", "Line under the rail", "Flip the finish and the whole scene changes with it.")],
    blocks=[("world", "Finish world", [text("key", "Key (gold / black)", "gold"), text("label", "Button", "Gold"), img("image", "Photo"),
                                       text("pos", "Photo position (CSS)", "object-position:50% 50%"), text("heading", "Heading"), textarea("body", "Line")]),
            ("point", "Photo callout", [text("world", "World key", "gold"), text("n", "Number", "1"), rng("x", "Across", 0, 100, 1, 50, "%"),
                                        rng("y", "Down", 0, 100, 1, 50, "%"), check("left", "Label on the left", False), text("title", "Title"), text("text", "Line")]),
            ("photo", "Rail photo", [text("world", "World key", "gold"), img("image", "Photo"), text("alt", "Alt text"),
                                     select("ratio", "Shape", [("23", "2:3"), ("32", "3:2"), ("11", "1:1"), ("45", "4:5")], "32"), text("pos", "Position (CSS, optional)")])],
    presets=False)

# ---------------------------------------------------------------- the spec sheet
S["lg-club-specs"] = section("Club: spec sheet", C + """
{%- if c.spec -%}{%- assign sp = c.spec -%}{%- assign s = section.settings -%}
<section class="lg-sec lg-contour" id="specs" style="border-top:1px solid var(--lg-rule)"><div class="lg-wrap">
  <div class="hd">
    <div><p class="lg-eyebrow">{{ s.eyebrow }}</p><h2 class="lg-d2">{{ sp.head }}</h2>
    <p class="lg-body">{{ sp.line }}</p></div>
  </div>
  <div class="lg-monitor">
    <div class="lg-monitor-hd"><span class="lg-label">{{ sp.mon_label }}</span><span class="lg-label lg-live{% unless product.available %} is-out{% endunless %}"><i></i><span data-mon-stock>{% if product.available %}In stock{% else %}Sold out{% endif %}</span></span></div>
    <div class="lg-monitor-in">
      <div class="lg-monitor-ph">{%- assign mi = product.metafields.custom.club_spec_photo.value | default: product.metafields.custom.cutout.value -%}{%- if mi != blank %}{{ mi | image_url: width: 900 | image_tag: alt: sp.mon_alt, loading: 'lazy', widths: '450,700,900', sizes: '(max-width: 749px) 90vw, 30vw' }}{% endif -%}</div>
      <div class="lg-monitor-tiles">
        {%- for t in sp.tiles -%}
        <div class="lg-mt"><span>{{ t.l }}</span>{%- if t.price -%}<b class="lg-num">{{ product.price | money_without_trailing_zeros }}</b>{%- else -%}<b>{{ t.b }}</b>{%- endif -%}
          {%- if t.vals -%}<div class="lg-vals">{%- for v in t.vals -%}<i>{{ v }}</i>{%- endfor -%}</div>{%- endif -%}
          {%- if t.em != blank %}<em>{{ t.em }}</em>{% endif -%}</div>
        {%- endfor -%}
      </div>
    </div>
  </div>
  {%- if sp.tabs -%}
  <div class="seg specs-tabs" data-spectabs role="tablist"><button class="lg-chip" type="button" data-tab="clubs" aria-pressed="true">Clubs</button><button class="lg-chip" type="button" data-tab="shafts" aria-pressed="false">Shafts</button><button class="lg-chip" type="button" data-tab="grips" aria-pressed="false">Grips</button></div>
  <div data-spectab="clubs">
    <div class="tbar">
      {%- if sp.seg.size > 1 -%}<div class="seg" data-specseg role="group" aria-label="Grind">{%- for g in sp.seg -%}<button class="lg-chip" type="button" data-g="{{ g[0] }}" aria-pressed="{% if forloop.first %}true{% else %}false{% endif %}">{{ g[1] }}</button>{%- endfor -%}</div>
      {%- else -%}<span class="lg-label">{{ sp.seg[0][1] }}</span>{%- endif -%}
      <span class="lg-meta">{{ sp.hands }}</span></div>
    {%- for tb in sp.tables -%}
    <div class="tbl" data-spec="{{ tb.id }}"{% unless forloop.first %} hidden{% endunless %}><table class="lg-table">
      <thead><tr>{%- for h in tb.head -%}<th>{{ h }}</th>{%- endfor -%}</tr></thead>
      <tbody>
      {%- for r in tb.rows -%}<tr>{%- for x in r -%}{%- if forloop.first -%}<th scope="row">{{ x }}</th>{%- else -%}<td>{{ x }}</td>{%- endif -%}{%- endfor -%}</tr>{%- endfor -%}
      <tr><th scope="row">{{ tb.span[0] }}</th><td colspan="{{ tb.head.size | minus: 1 }}">{{ tb.span[1] }}</td></tr>
      </tbody></table></div>
    {%- endfor -%}
    {%- if sp.table_note != blank %}<p class="note">{{ sp.table_note }}</p>{% endif -%}
  </div>
  {%- for k in (1..2) -%}{%- if k == 1 %}{% assign tb = sp.shafts %}{% assign id = 'shafts' %}{% else %}{% assign tb = sp.grips %}{% assign id = 'grips' %}{% endif -%}
  <div data-spectab="{{ id }}" hidden>
    <div class="tbl"><table class="lg-table">
      <thead><tr>{%- for h in tb.head -%}<th>{{ h }}</th>{%- endfor -%}</tr></thead>
      <tbody>{%- for r in tb.rows -%}<tr>{%- for x in r -%}{%- if forloop.first -%}<th scope="row">{{ x }}</th>{%- else -%}<td>{{ x }}</td>{%- endif -%}{%- endfor -%}</tr>{%- endfor -%}</tbody></table></div>
    <p class="note">{{ tb.note }}</p>
  </div>
  {%- endfor -%}
  {%- else -%}
  <div class="tbl" style="margin-top:clamp(18px,2.5vw,26px)"><table class="lg-table">
    <tbody>{%- for r in sp.rows -%}<tr><th scope="row">{{ r[0] }}</th><td>{{ r[1] }}</td></tr>{%- endfor -%}</tbody>
  </table></div>
  {%- if sp.note != blank %}<p class="note">{{ sp.note }}</p>{% endif -%}
  {%- endif -%}
</div></section>
{%- endif -%}
""", [text("eyebrow", "Eyebrow", "The spec sheet")], presets=False)

# ---------------------------------------------------------------- photo beat
S["lg-club-pband"] = section("Club: photo band", C + """
{%- assign band = product.metafields.custom.club_band_photos.value -%}
{%- if band.size > 0 -%}
<div class="lg-pband" aria-label="{{ section.settings.label | escape }}">
  {%- for im in band -%}{%- assign p = c.pband[forloop.index0] -%}{%- assign alt = p[0] | default: im.alt -%}{%- assign pos = p[1] | default: '' -%}
  <figure class="pb">{{ im | image_url: width: 1000 | image_tag: alt: alt, loading: 'lazy', style: pos, widths: '400,700,1000', sizes: '(max-width: 749px) 50vw, 33vw' }}</figure>{%- endfor -%}
</div>
{%- endif -%}
""", [text("label", "Label (for screen readers)", "On the course")], presets=False)

# ---------------------------------------------------------------- reviews: only at 10+
S["lg-club-reviews"] = section("Club: reviews", C + MIN + """
{%- liquid
  assign rv = product.metafields.reviews.rating.value.rating
  assign jd = product.metafields.judgeme.review_widget_data.value
-%}
{%- if rc >= min and rv -%}
<section class="lg-sec" id="reviews"><div class="lg-wrap">
  <div class="rv-top">
    <div><p class="lg-eyebrow">{{ section.settings.eyebrow }}</p><h2 class="lg-d2">{{ rv | round: 1 }} stars from {{ rc }} reviews</h2>
      {%- if c.rv.write %}<button class="lg-btn-line lg-btn-sm" type="button" data-md-open="md-write">Write a review</button>{% endif -%}</div>
    <div id="prox"></div>
  </div>
  {%- if c.quotes.size > 0 -%}
  <div class="qs">
    {%- for q in c.quotes -%}
    <figure class="lg-quote"><span class="lg-stars" aria-label="5 out of 5">{% render 'lg-stars' %}</span>{% if q.t != blank %}<b>{{ q.t }}</b>{% endif %}<blockquote>&ldquo;{{ q.q }}&rdquo;</blockquote><figcaption>{{ q.n }} · <span class="lg-stock">Verified buyer</span></figcaption></figure>
    {%- endfor -%}
  </div>
  {%- endif -%}
  <button class="readall" type="button" data-readall aria-expanded="false" aria-controls="jm"><b>Read every review</b><span>Newest first.</span><i aria-hidden="true">+</i></button>
  <div class="jm" id="jm" hidden>
    <div class="jm-bar"><div class="lg-chips" id="jm-filters" role="group" aria-label="Filter reviews by rating"></div>
      <label><span class="sr">Sort reviews</span><select id="jm-sort"><option value="recent">Most recent</option><option value="high">Highest rating</option><option value="low">Lowest rating</option></select></label></div>
    <p class="jm-count" id="jm-count"></p>
    <div id="jm-list"></div>
    <div class="jdgm-widget jdgm-review-widget" id="judgeme_product_reviews" data-id="{{ product.id }}" data-jdgm-full hidden>{{ product.metafields.judgeme.widget }}</div>
    <div class="jm-more"><button class="lg-btn-line lg-btn-sm" type="button" id="jm-more">Show more reviews</button></div>
  </div>
</div></section>
<script>
window.LG_CLUB_REVIEWS = {
  total: {{ rc }}, nums: {{ c.rv.nums | default: false }},
  totals: { {%- for h in jd.histogram -%}{{ h.rating | json }}: {{ h.frequency | default: 0 }}{% unless forloop.last %},{% endunless %}{%- endfor -%} },
  list: [
    {%- for r in jd.reviews -%}
    { r: {{ r.rating | default: 5 }}, t: {{ r.title | default: '' | json }}, q: {{ r.body | default: '' | json }}, n: {{ r.reviewer_name | default: 'Anonymous' | json }}, v: {{ r.verified_buyer | default: false }}, d: {{ r.created_at | date: '%Y-%m-%d' | json }} }{% unless forloop.last %},{% endunless %}
    {%- endfor -%}
  ]
};
</script>
{%- endif -%}
""", [text("eyebrow", "Eyebrow", "Reviews"),
      para("Shows only at the review minimum (theme settings, 10) from the live Judge.me count. The three quotes come from custom.club_page, verbatim from Judge.me.")],
    presets=False)

# ---------------------------------------------------------------- more from the bag
S["lg-club-more"] = section("Club: more from the bag", C + """
{%- assign s = section.settings -%}
{%- if c.more.size > 0 -%}
<section class="lg-sec more" id="more"><div class="lg-wrap">
  <div class="hd"><div><p class="lg-eyebrow">{{ s.eyebrow }}</p><h2 class="lg-d2">{{ s.heading }}</h2></div>{% if s.link_label != blank %}<a class="lg-link" href="{{ s.link_url }}">{{ s.link_label }} <span>&rarr;</span></a>{% endif %}</div>
  <div class="lg-grid">
    {%- for m in c.more -%}{%- assign mp = all_products[m[0]] -%}
      {%- if mp != blank -%}{% render 'lg-card', product: mp, name: m[1], line: m[2], cut: true, stars: false %}{%- endif -%}
    {%- endfor -%}
  </div>
</div></section>
{%- endif -%}
""", [text("eyebrow", "Eyebrow", "More from the bag"), text("heading", "Heading", "Round out the bag"),
      text("link_label", "Link", "See every club"), url("link_url", "Link URL")], presets=False)

# ---------------------------------------------------------------- the last word
S["lg-club-signoff"] = section("Club: sign-off", C + """
{%- assign s = section.settings -%}
<section class="lg-signoff" id="last"><div class="lg-wrap">
  <p class="lg-eyebrow">{{ s.eyebrow }}</p>
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d1' %}
  {%- if c.sign != blank %}<p class="lg-lede">{{ c.sign }}</p>{% endif -%}
  <a class="lg-btn-line" href="#buy">{% if product.available %}{{ c.signcta | default: s.cta }}{% else %}{{ s.cta_out }}{% endif %} <span aria-hidden="true">&rarr;</span></a>
  <div class="lg-signoff-mags" aria-hidden="true">{% render 'lg-mags' %}</div>
</div></section>
""", [text("eyebrow", "Eyebrow", "The last word"), rich("heading", "Heading (italic = gold word)"),
      text("cta", "Button to the buy box (if the product has none)", "Put it in the bag"),
      text("cta_out", "Button when sold out", "Tell me when it's back")], presets=False)
