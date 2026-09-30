"""Home page sections (and the general ones Home introduces). Imported by build_sections.py."""
from common import HEAD, BTN, IMG, section, text, textarea, rich, url, img, check, select, rng, product, collection, header, para, plist, number

S = {}

S["lg-hero"] = section("Photo hero", """
{%- liquid
  assign s = section.settings
  assign fd = s.focus_x | append: '% ' | append: s.focus_y | append: '%'
  assign fm = s.focus_mx | append: '% ' | append: s.focus_my | append: '%'
-%}
<section class="lg-hero{% if s.short %} is-short{% endif %}" style="--focus:{{ fd }};--focus-m:{{ fm }}">
  {%- if s.image != blank -%}
    {{ s.image | image_url: width: 2400 | image_tag: class: 'lg-hero-img', alt: s.image.alt, fetchpriority: 'high', loading: 'eager', widths: '750,1100,1500,2000,2400', sizes: '100vw' }}
  {%- elsif request.design_mode -%}<div class="lg-hero-img lg-slot"><small>Hero photo</small>Pick one in the theme editor</div>{%- endif -%}
  <div class="lg-hero-copy"><div class="lg-wrap">
    {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
    {% render 'lg-h', text: s.heading, tag: s.heading_tag, cls: 'lg-d1' %}
    {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
    {%- if s.btn_label != blank -%}<div class="lg-btn-row"><a class="lg-btn" href="{{ s.btn_url }}">{{ s.btn_label }} <span aria-hidden="true">&rarr;</span></a>
      {%- if s.btn2_label != blank %}<a class="lg-btn-line" href="{{ s.btn2_url }}">{{ s.btn2_label }}</a>{% endif -%}</div>{%- endif -%}
  </div></div>
  {%- if s.stamp != blank -%}<div class="hero-stamp lg-label">{{ s.stamp }}<b>{{ s.stamp_b }}</b></div>{%- endif -%}
</section>
""", [
    img("image", "Photo"),
    rng("focus_x", "Focus across (desktop)", 0, 100, 1, 50, "%"), rng("focus_y", "Focus down (desktop)", 0, 100, 1, 50, "%"),
    rng("focus_mx", "Focus across (phone)", 0, 100, 1, 50, "%"), rng("focus_my", "Focus down (phone)", 0, 100, 1, 50, "%"),
    check("short", "Short hero", False),
    text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"),
    select("heading_tag", "Heading level", [("h1", "H1 (one per page)"), ("h2", "H2")], "h1"),
    textarea("lede", "Line under it"),
    text("btn_label", "Button"), url("btn_url", "Button link"),
    text("btn2_label", "Second button"), url("btn2_url", "Second button link"),
    text("stamp", "Corner stamp, top line"), text("stamp_b", "Corner stamp, bold line"),
])

S["lg-trust"] = section("Trust bar", """
{%- assign min = settings.lg_review_min | default: 10 -%}
<div class="lg-cred"><div class="lg-wrap"><div class="cred-in">
  {%- for block in section.blocks -%}
    {%- if block.type == 'rating' -%}
      {%- liquid
        assign n = 0
        assign sum = 0
        for p in block.settings.products
          assign rc = p.metafields.reviews.rating_count.value | default: 0
          assign rv = p.metafields.reviews.rating.value.rating | default: 0
          assign n = n | plus: rc
          assign sum = rv | times: rc | plus: sum
        endfor
      -%}
      {%- if n >= min -%}{%- assign avg = sum | divided_by: n | round: 1 -%}
      {%- assign nf = n -%}{%- if n >= 1000 -%}{%- assign th = n | divided_by: 1000 -%}{%- assign rem = n | modulo: 1000 | prepend: '00' | slice: -3, 3 -%}{%- assign nf = th | append: ',' | append: rem -%}{%- endif -%}
      <a class="cred" href="{{ block.settings.url }}" {{ block.shopify_attributes }}><span class="cred-top lg-stars" aria-hidden="true">{% render 'lg-stars' %}</span><span class="cred-t">{{ block.settings.text | replace: '[avg]', avg | replace: '[count]', nf }}</span></a>
      {%- endif -%}
    {%- else -%}
      <a class="cred" href="{{ block.settings.url }}" {{ block.shopify_attributes }}><span class="cred-top">{% render 'lg-icon', name: block.settings.icon %}</span><span class="cred-t">{{ block.settings.text }}</span></a>
    {%- endif -%}
  {%- endfor -%}
</div></div></div>
""", [], blocks=[
    ("rating", "Review score (live)", [plist("products", "Products whose Judge.me reviews count"), text("text", "Text ([avg] and [count] fill in live)", "[avg] stars from [count] verified reviews"), url("url", "Link")]),
    ("item", "Line with icon", [select("icon", "Icon", [(x, x) for x in ["truck", "rotate-ccw", "badge-check", "credit-card", "shield-check", "package", "hammer", "anvil", "tag", "hand-coins", "message-circle", "star"]], "truck"),
                                text("text", "Text", "Free shipping on $198 and up"), url("url", "Link")]),
], max_blocks=4)

S["lg-cards"] = section("Product cards", """
{%- assign s = section.settings -%}
<section class="lg-sec{% if s.big %} is-wide{% endif %}"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  {%- if s.big -%}
    <div class="cards-big-head">{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: s.heading_tag, cls: 'lg-d2' %}</div>
  {%- else -%}{% render 'lg-sec-head', s: s %}{%- endif -%}
  <div class="{% if s.big %}cards-big{% else %}cards{{ s.cols }}{% endif %}">
    {%- for block in section.blocks -%}
      {%- if block.type == 'card' and block.settings.product != blank -%}
        <div class="lg-card-wrap" {{ block.shopify_attributes }}>
        {%- if s.big -%}{% render 'lg-bigcard', product: block.settings.product, name: block.settings.name, line: block.settings.line, vibe: block.settings.vibe, tag: block.settings.tag, image: block.settings.image, stars: s.stars %}
        {%- else -%}{% render 'lg-card', product: block.settings.product, name: block.settings.name, line: block.settings.line, vibe: block.settings.vibe, tag: block.settings.tag, image: block.settings.image, cut: block.settings.cut, stars: s.stars %}{%- endif -%}
        </div>
      {%- elsif block.type == 'tile' -%}{%- assign b = block.settings -%}
        <a class="ftile" href="{{ b.url }}" {{ block.shopify_attributes }}>{%- if b.image != blank -%}{{ b.image | image_url: width: 900 | image_tag: loading: 'lazy', alt: '', widths: '450,700,900', sizes: '(max-width: 749px) 82vw, 33vw' }}{%- endif -%}
          <div class="ft-in">{%- if b.eyebrow != blank %}<p class="lg-eyebrow">{{ b.eyebrow }}</p>{% endif %}<h3>{{ b.title }}</h3>{%- if b.text != blank %}<p class="ft-p">{{ b.text }}</p>{% endif %}{%- if b.go != blank %}<span class="go">{{ b.go }} &rarr;</span>{% endif %}</div></a>
      {%- endif -%}
    {%- endfor -%}
  </div>
  {%- if s.big and s.link_url != blank %}<div class="cards-big-foot"><a class="lg-btn-line" href="{{ s.link_url }}">{{ s.link_label }} <span aria-hidden="true">&rarr;</span></a></div>{% endif -%}
</div></section>
""", [text("anchor", "Anchor (for #links)", "families"), check("no_top", "No space above", False)] + HEAD + [
    check("big", "Big cards (three across, name on top)", True),
    select("cols", "Small cards per row", [("5", "5"), ("4", "4"), ("3", "3")], "5"), check("stars", "Show stars (only at the review minimum)", False)],
    blocks=[("card", "Product", [product("product", "Product"), text("name", "Name (empty = product's)"), text("line", "Line under it"),
                                 text("vibe", "Vibe tag"), text("tag", "Tag (e.g. Best seller)"),
                                 img("image", "Photo (empty = the product's card cutout)"), check("cut", "Cutout on stone (small cards)", True)]),
            ("tile", "Photo tile", [img("image", "Photo"), text("eyebrow", "Eyebrow"), text("title", "Title"), text("text", "Line"), text("go", "Link text"), url("url", "Link")])])

S["lg-split"] = section("Photo + text", """
{%- assign s = section.settings -%}
<section class="lg-sec{% if s.feat %} feat{% endif %}"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %} style="{% if s.no_top %}padding-top:0;{% endif %}{% if s.rule %}border-top:1px solid var(--lg-rule){% endif %}"><div class="lg-wrap">
  <div class="lg-split{% if s.flip %} is-flip{% endif %}{% if s.text_first %} ed{% endif %}"{% if s.text_first %} style="margin-top:0"{% endif %}>
    {%- capture fig -%}<figure class="lg-frame">{%- if s.image != blank -%}{{ s.image | image_url: width: 1400 | image_tag: loading: 'lazy', alt: s.image.alt, widths: '600,900,1200,1400', sizes: '(max-width: 749px) 100vw, 50vw', style: s.pos }}{%- elsif request.design_mode -%}<span class="lg-slot"><small>Photo</small>Pick one in the theme editor</span>{%- endif -%}</figure>{%- endcapture -%}
    {%- unless s.text_first %}{{ fig }}{% endunless -%}
    <div>
      {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
      {% render 'lg-h', text: s.heading, tag: s.heading_tag, cls: 'lg-d2' %}
      {%- if s.body != blank %}<div class="lg-body">{{ s.body }}</div>{% endif -%}
      {%- if s.btn_label != blank or s.link_label != blank -%}<div class="lg-btn-row">
        {%- if s.btn_label != blank %}<a class="{% if s.btn_gold %}lg-btn{% else %}lg-btn-line{% endif %}" href="{{ s.btn_url }}">{{ s.btn_label }} <span aria-hidden="true">&rarr;</span></a>{% endif -%}
        {%- if s.link_label != blank %}<a class="lg-link" href="{{ s.link_url }}" style="align-self:center">{{ s.link_label }} <span>&rarr;</span></a>{% endif -%}
      </div>{%- endif -%}
      {%- if s.stamp != blank %}<div class="stampline lg-label">{{ s.stamp }}</div>{% endif -%}
    </div>
    {%- if s.text_first %}{{ fig }}{% endif -%}
  </div>
</div></section>
""", [img("image", "Photo"), text("pos", "Photo position (CSS, optional)", "", "e.g. object-position:60% 40%"), check("flip", "Swap sides (is-flip)", False), check("text_first", "Text first, photo second", False),
      text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), select("heading_tag", "Heading level", [("h2", "H2"), ("h3", "H3")], "h2"),
      {"type": "richtext", "id": "body", "label": "Text"},
      text("btn_label", "Button"), url("btn_url", "Button link"), check("btn_gold", "Gold button", False),
      text("link_label", "Text link"), url("link_url", "Text link URL"), text("stamp", "Stamp line under it"),
      text("anchor", "Anchor"), check("no_top", "No space above", True), check("rule", "Line above", False), check("feat", "Wide photo (3:2)", True)])

S["lg-claims"] = section("Numbered claims", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}{% if s.rule %} style="border-top:1px solid var(--lg-rule)"{% endif %}><div class="lg-wrap">
  <div class="why-top">
    <div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div>
    {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
  </div>
  <div class="claims">
    {%- for block in section.blocks -%}<div class="claim" {{ block.shopify_attributes }}><span class="n">{{ forloop.index | prepend: '0' | slice: -2, 2 }}</span><h3 class="lg-d3">{{ block.settings.title }}</h3><p>{{ block.settings.text }}</p></div>{%- endfor -%}
  </div>
  {%- if s.link_label != blank %}<p class="lg-body" style="margin-top:clamp(18px,2.5vw,24px)"><a class="lg-link" href="{{ s.link_url }}">{{ s.link_label }} <span aria-hidden="true">&rarr;</span></a></p>{% endif -%}
</div></section>
""", [text("anchor", "Anchor", "why"), check("rule", "Line above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"),
      textarea("lede", "Line beside it"), text("link_label", "Link under it"), url("link_url", "Link URL")],
    blocks=[("claim", "Claim", [text("title", "Title"), textarea("text", "Text")])], max_blocks=6)

FINDER_CARD = []
for i in (1, 2, 3):
    FINDER_CARD += [header(f"Card {i}"), product(f"p{i}", "Product"), text(f"l{i}", "Line"), img(f"i{i}", "Photo (empty = product's)"), check(f"c{i}", "Cutout on stone", False), text(f"t{i}", "Tag")]

S["lg-finder"] = section("Club finder", """
{%- assign s = section.settings -%}
<section class="lg-sec fnd" id="{{ s.anchor | default: 'finder' }}" data-finder{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  {% render 'lg-sec-head', s: s %}
  <div class="lg-chips" role="tablist" aria-label="{{ s.chips_label | escape }}">
    {%- for block in section.blocks -%}<button class="lg-chip" type="button" role="tab" aria-pressed="{% if forloop.first %}true{% else %}false{% endif %}" data-fp="{{ forloop.index0 }}" {{ block.shopify_attributes }}>{{ block.settings.label }}</button>{%- endfor -%}
  </div>
  {%- for block in section.blocks -%}
  <div class="fnd-panel" data-panel="{{ forloop.index0 }}"{% unless forloop.first %} hidden{% endunless %}><div class="fnd-grid">
    {%- for i in (1..3) -%}{%- assign pk = 'p' | append: i -%}{%- assign p = block.settings[pk] -%}{%- if p != blank -%}
      {%- assign lk = 'l' | append: i -%}{%- assign ik = 'i' | append: i -%}{%- assign ck = 'c' | append: i -%}{%- assign tk = 't' | append: i -%}
      {% render 'lg-card', product: p, line: block.settings[lk], image: block.settings[ik], cut: block.settings[ck], tag: block.settings[tk] %}
    {%- endif -%}{%- endfor -%}
  </div></div>
  {%- endfor -%}
  {%- if s.foot_label != blank %}<div class="fnd-foot"><a class="lg-btn-line lg-btn-sm" href="{{ s.foot_url }}">{{ s.foot_label }} <span aria-hidden="true">&rarr;</span></a></div>{% endif -%}
</div></section>
""", [text("anchor", "Anchor", "finder"), check("no_top", "No space above", True)] + HEAD + [text("chips_label", "Tabs label (for screen readers)", "What to fix"),
      text("foot_label", "Button under it"), url("foot_url", "Button link")],
    blocks=[("tab", "Tab", [text("label", "Tab label", "Around the green")] + FINDER_CARD)], max_blocks=5)

S["lg-pband"] = section("Photo band", """
<div class="lg-pband pband-{{ section.blocks.size }}" aria-label="{{ section.settings.label | escape }}">
  {%- for block in section.blocks -%}<figure class="pb" {{ block.shopify_attributes }}>{%- if block.settings.image != blank -%}{{ block.settings.image | image_url: width: 1000 | image_tag: loading: 'lazy', alt: block.settings.image.alt, widths: '400,700,1000', sizes: '(max-width: 749px) 50vw, 25vw', style: block.settings.pos }}{%- endif -%}</figure>{%- endfor -%}
</div>
""", [text("label", "Label (for screen readers)", "Lucky, out on the course")],
    blocks=[("photo", "Photo", [img("image", "Photo"), text("pos", "Position (CSS, optional)", "", "e.g. object-position:30% 40%")])], max_blocks=4)

REV_CARD = [text("quote", "Quote, word for word from Judge.me"), text("name", "Name as on Judge.me (e.g. Michael P.)"), product("product", "Product")]
S["lg-reviews-band"] = section("Reviews on a photo", """
{%- liquid
  assign s = section.settings
  assign min = settings.lg_review_min | default: 10
  assign n = 0
  assign sum = 0
  for p in s.agg_products
    assign rc = p.metafields.reviews.rating_count.value | default: 0
    assign rv = p.metafields.reviews.rating.value.rating | default: 0
    assign n = n | plus: rc
    assign sum = rv | times: rc | plus: sum
  endfor
  if n > 0
    assign avg = sum | divided_by: n | round: 1
  endif
-%}
<section class="lg-band is-photo" id="{{ s.anchor | default: 'reviews' }}" style="{% if s.bg != blank %}--band-bg:url({{ s.bg | image_url: width: 2000 }});{% endif %}--band-pos:{{ s.bg_pos }}"><div class="lg-wrap">
  {%- if s.pull != blank -%}
  <figure class="pull"><q>&ldquo;{{ s.pull }}&rdquo;</q><figcaption><b>{{ s.pull_name }}</b>{% if s.pull_product != blank %} · {{ s.pull_product.title }}{% endif %}{% if s.pull_stars > 0 %} · {{ s.pull_stars }} stars{% endif %} · verified buyer</figcaption></figure>
  {%- endif -%}
  <div class="proof-hd"><div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div></div>
  {%- if n >= min -%}
  <div class="agg"><b class="lg-num">{{ avg }}</b><div><span class="lg-stars" aria-label="{{ avg }} out of 5">{% render 'lg-stars' %}</span><p class="lg-body" style="margin:6px 0 0">{{ s.agg_line | replace: '[count]', n }}</p></div></div>
  {%- endif -%}
  <div class="rvrail" id="rvrail-{{ section.id }}" role="region" aria-label="Customer reviews" tabindex="0">
    {%- for block in section.blocks -%}{%- assign p = block.settings.product -%}
    <figure class="lg-band-tile rvc" {{ block.shopify_attributes }}><span class="ph">{%- if p != blank -%}{%- assign th = p.metafields.custom.cutout.value | default: p.featured_image -%}{%- if th -%}<span class="th">{{ th | image_url: width: 120 | image_tag: alt: '', loading: 'lazy' }}</span>{%- endif -%}{%- endif -%}<span class="lg-stars" aria-label="5 out of 5">{% render 'lg-stars' %}</span></span><blockquote>&ldquo;{{ block.settings.quote }}&rdquo;</blockquote><figcaption><b>{{ block.settings.name }}</b>{% if p != blank %} · {{ p.title }}{% endif %}</figcaption></figure>
    {%- endfor -%}
  </div>
  <div class="rail-foot">{%- if s.link_label != blank %}<a class="lg-link" href="{{ s.link_url }}">{{ s.link_label }} <span>&rarr;</span></a>{% endif -%}<div class="arrows" data-arrows="rvrail-{{ section.id }}"><button type="button" aria-label="Previous">&lsaquo;</button><button type="button" aria-label="Next">&rsaquo;</button></div></div>
</div></section>
""", [text("anchor", "Anchor", "reviews"), img("bg", "Background photo"), text("bg_pos", "Background position", "center 40%"),
      header("Pull quote"), textarea("pull", "Quote, word for word from Judge.me"), text("pull_name", "Name"), product("pull_product", "Product"), rng("pull_stars", "Stars they gave", 0, 5, 1, 5),
      header("Heading and score"), text("eyebrow", "Eyebrow", "Reviews"), rich("heading", "Heading (italic = gold word)"),
      plist("agg_products", "Products whose Judge.me scores make the average"), text("agg_line", "Line by the score ([count] = number of reviews)", "Stars from verified buyers, across every club."),
      text("link_label", "Link", "Read every review"), url("link_url", "Link URL"),
      para("Tiles are 5-star Judge.me reviews typed in word for word. Never edit or invent a review.")],
    blocks=[("review", "Review tile", REV_CARD)], max_blocks=12)

S["lg-gtiles"] = section("Two photo tiles", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}><div class="lg-wrap">
  {% render 'lg-sec-head', s: s %}
  <div class="gt">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}
    <a class="gtile" href="{{ b.collection.url | default: b.url }}" {{ block.shopify_attributes }}>{%- if b.image != blank -%}{{ b.image | image_url: width: 1400 | image_tag: loading: 'lazy', alt: b.image.alt, widths: '600,900,1400', sizes: '(max-width: 560px) 100vw, 50vw', style: b.pos }}{%- endif -%}<div>
      <span class="ct">{%- if b.count and b.collection != blank -%}{{ b.collection.products_count }} styles{%- else -%}{{ b.kicker }}{%- endif -%}</span>
      <h3 class="lg-d2">{{ b.title | default: b.collection.title }}</h3><p>{{ b.text }}</p><span class="go">{{ b.go }} &rarr;</span></div></a>
    {%- endfor -%}
  </div>
  {%- if s.foot != blank or s.foot_label != blank -%}<div class="gear-foot"><p>{{ s.foot }}</p>{%- if s.foot_label != blank %}<a class="lg-btn-line lg-btn-sm" href="{{ s.foot_url }}">{{ s.foot_label }} <span aria-hidden="true">&rarr;</span></a>{% endif -%}</div>{%- endif -%}
</div></section>
""", [text("anchor", "Anchor", "gear")] + HEAD + [text("foot", "Line under the tiles"), text("foot_label", "Button"), url("foot_url", "Button link")],
    blocks=[("tile", "Tile", [collection("collection", "Collection"), url("url", "Or a link"), img("image", "Photo"), text("pos", "Photo position (CSS, optional)"),
                              check("count", "Show '[n] styles' from the collection", True), text("kicker", "Or a small line"), text("title", "Title (empty = collection's)"),
                              textarea("text", "Text"), text("go", "Link text", "Shop now")])], max_blocks=2)

S["lg-wild"] = section("Community posts", open(__file__.replace("sections_home.py", "wild.liquid"), encoding="utf-8").read(), [text("anchor", "Anchor", "wild"), check("no_top", "No space above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("sub", "Line under it"),
      number("limit", "How many posts", 12), text("btn_label", "Button"), url("btn_url", "Button link"), check("ig", "Show the Instagram button", True),
      para("Posts come from Content > Metaobjects > Community post: a photo or video, the @handle, a caption and the products in it.")])

S["lg-callout"] = section("Callout box", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  <div class="amb">
    <div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}{%- if s.body != blank %}<p class="lg-body">{{ s.body }}</p>{% endif -%}</div>
    {%- if s.btn_label != blank %}<a class="lg-btn-line" href="{{ s.btn_url }}">{{ s.btn_label }} <span aria-hidden="true">&rarr;</span></a>{% endif -%}
  </div>
</div></section>
""", [text("anchor", "Anchor"), check("no_top", "No space above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("body", "Text"),
      text("btn_label", "Button"), url("btn_url", "Button link")])

S["lg-signoff"] = section("Mags sign-off", """
{%- assign s = section.settings -%}
<section class="lg-signoff"><div class="lg-wrap">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d1' %}
  {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
  <div class="lg-btn-row">{%- if s.btn_label != blank %}<a class="lg-btn" href="{{ s.btn_url }}">{{ s.btn_label }}{% if s.btn_arrow %} <span aria-hidden="true">&rarr;</span>{% endif %}</a>{% endif -%}{%- if s.btn2_label != blank %}<a class="lg-btn-line" href="{{ s.btn2_url }}">{{ s.btn2_label }}</a>{% endif -%}</div>
  {%- if s.trust != blank -%}<div class="close-trust">{%- assign ts = s.trust | newline_to_br | split: '<br />' -%}{%- for t in ts -%}{%- assign tt = t | strip -%}{%- if tt != blank %}<span>{{ tt }}</span>{% endif -%}{%- endfor -%}</div>{%- endif -%}
  <div class="lg-signoff-mags" aria-hidden="true">{% render 'lg-mags' %}</div>
</div></section>
""", [text("eyebrow", "Eyebrow", "The last word"), rich("heading", "Heading (italic = gold word)"), text("lede", "Line under it", "It's better to be lucky."),
      text("btn_label", "Gold button"), url("btn_url", "Gold button link"), check("btn_arrow", "Arrow on the gold button", True), text("btn2_label", "Second button"), url("btn2_url", "Second button link"),
      textarea("trust", "Small lines under the buttons (one per line)")])
