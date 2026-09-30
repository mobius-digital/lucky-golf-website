"""Content pages (group 70): Our Story, FAQ, Ambassadors, Compare, Contact, Community,
Reviews, 404, Search. Imported by build_sections.py. CSS: theme/css/70-content.css
(built by tools/theme/css_content.py, scoped to each section's wrapper class lgc-*)."""
import json
from common import section, text, textarea, rich, url, img, check, select, rng, product, plist, collection, header, para, number

S = {}

ICONS = [("", "None")] + [(x, x) for x in ["mail", "message-circle", "package", "circle-help", "hand-coins", "send", "star", "badge-check",
                                           "truck", "rotate-ccw", "shield-check", "credit-card", "tag", "hammer", "anvil", "search",
                                           "shopping-bag", "map-pin", "instagram", "tiktok", "youtube"]]
RICHTEXT = lambda id, label: {"type": "richtext", "id": id, "label": label}
INLINE = lambda id, label: {"type": "inline_richtext", "id": id, "label": label}


def sec(name, cls, liquid, settings, blocks=None, max_blocks=None):
    """section() plus a wrapper class on Shopify's section div, so 70-content.css can scope to it."""
    out = section(name, liquid, settings, blocks, max_blocks)
    head, schema = out.split("{% schema %}\n")
    schema = json.loads(schema.split("\n{% endschema %}")[0])
    schema = {"name": schema["name"], "class": cls, **{k: v for k, v in schema.items() if k != "name"}}
    return head + "{% schema %}\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n{% endschema %}\n"


# the rating a product's Judge.me metafields give, gated at the review minimum
RATING = """{%- liquid
  assign min = settings.lg_review_min | default: 10
-%}"""

STARS_N = """<span class="lg-stars" aria-label="{{ n }} out of 5">{%- for i in (1..5) -%}<svg viewBox="0 0 20 20" aria-hidden="true"{% if i > n %} style="opacity:.25"{% endif %}><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6L10 15l-5.4 3 1.2-6L1.3 7.8l6.1-.7z"/></svg>{%- endfor -%}</span>"""

CRUMB = """{%- if s.crumb != blank -%}<nav class="crumb lg-wrap" aria-label="Breadcrumb"><ol><li><a href="{{ routes.root_url }}">Home</a></li><li><span aria-current="page">{{ s.crumb }}</span></li></ol></nav>{%- endif -%}"""

HEAD_BLOCK = """{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}"""

FOCUS = [rng("focus_x", "Focus across (desktop)", 0, 100, 1, 50, "%"), rng("focus_y", "Focus down (desktop)", 0, 100, 1, 50, "%"),
         rng("focus_mx", "Focus across (phone)", 0, 100, 1, 50, "%"), rng("focus_my", "Focus down (phone)", 0, 100, 1, 50, "%")]

# ------------------------------------------------------------------ hero with any buttons + a live review count
S["lg-hero-plus"] = sec("Photo hero, buttons", "lgc-hero", """
{%- liquid
  assign s = section.settings
  assign min = settings.lg_review_min | default: 10
  assign n = 0
  for p in s.count_products
    assign rc = p.metafields.reviews.rating_count.value | default: 0
    assign n = n | plus: rc
  endfor
  assign ey = s.eyebrow
  if ey contains '[count]'
    if n >= min
      assign ey = ey | replace: '[count]', n
    else
      assign ey = s.eyebrow_low
    endif
  endif
  assign fd = s.focus_x | append: '% ' | append: s.focus_y | append: '%'
  assign fm = s.focus_mx | append: '% ' | append: s.focus_my | append: '%'
-%}
<section class="lg-hero{% if s.short %} is-short{% endif %}" style="--focus:{{ fd }};--focus-m:{{ fm }}">
  {%- if s.image != blank -%}
    {{ s.image | image_url: width: 2400 | image_tag: class: 'lg-hero-img', alt: s.image.alt, fetchpriority: 'high', loading: 'eager', widths: '750,1100,1500,2000,2400', sizes: '100vw' }}
  {%- elsif request.design_mode -%}<div class="lg-hero-img lg-slot"><small>Hero photo</small>Pick one in the theme editor</div>{%- endif -%}
  <div class="lg-hero-copy"><div class="lg-wrap">
    {%- if ey != blank %}<p class="lg-eyebrow">{{ ey }}</p>{% endif -%}
    {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}
    {%- if s.lede != blank %}<p class="lg-lede"{% if s.lede_w > 0 %} style="max-width:{{ s.lede_w }}ch"{% endif %}>{{ s.lede }}</p>{% endif -%}
    {%- if section.blocks.size > 0 -%}<div class="lg-btn-row">
      {%- for block in section.blocks -%}{%- assign b = block.settings -%}
      <a class="{% if b.gold %}lg-btn{% else %}lg-btn-line{% endif %}" href="{{ b.url }}"{% if b.new_tab %} target="_blank" rel="noopener"{% endif %} {{ block.shopify_attributes }}>{{ b.label }} {% if b.icon != blank %}{% render 'lg-icon', name: b.icon %}{% else %}<span aria-hidden="true">&rarr;</span>{% endif %}</a>
      {%- endfor -%}</div>{%- endif -%}
  </div></div>
</section>
""", [img("image", "Photo")] + FOCUS + [check("short", "Short hero", True),
      text("eyebrow", "Eyebrow ([count] = live review count)"), text("eyebrow_low", "Eyebrow if the count is under the review minimum"),
      plist("count_products", "Products whose Judge.me counts make [count]", 10),
      rich("heading", "Heading (italic = gold word)"), textarea("lede", "Line under it"), rng("lede_w", "Line width (0 = default)", 0, 80, 2, 0, "ch")],
    blocks=[("button", "Button", [text("label", "Label"), url("url", "Link"), check("gold", "Gold (one per screen)", False),
                                  select("icon", "Icon instead of the arrow", ICONS, ""), check("new_tab", "Open in a new tab", False)])], max_blocks=3)

# ------------------------------------------------------------------ Our story
S["lg-man"] = sec("Manifesto", "lgc-man", """
{%- assign s = section.settings -%}
<section class="lg-sec man-sec"><div class="lg-wrap man">
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d1' %}
  <div>
  {{ s.body | replace: '<p>', '<p class="lg-body">' }}
  {%- if s.close != blank %}<p class="man-close">{{ s.close }}</p>{% endif -%}
  </div>
</div></section>
""", [rich("heading", "Heading (italic = gold word)"), RICHTEXT("body", "Text"), text("close", "Closing line")])

S["lg-parts"] = sec("Three photo parts", "lgc-parts", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  <div class="parts">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}
    <article class="part" {{ block.shopify_attributes }}>
      <figure>{%- if b.image != blank -%}{{ b.image | image_url: width: 1000 | image_tag: loading: 'lazy', alt: b.image.alt, widths: '500,750,1000', sizes: '(max-width: 760px) 100vw, 33vw' }}{%- elsif request.design_mode -%}<span class="lg-slot"><small>Photo</small></span>{%- endif -%}</figure>
      {%- if b.eyebrow != blank %}<p class="lg-eyebrow">{{ b.eyebrow }}</p>{% endif -%}
      {% render 'lg-h', text: b.heading, tag: 'h2', cls: 'lg-d3' %}
      {%- if b.text != blank %}<p>{{ b.text }}</p>{% endif -%}
      {%- if b.link_label != blank %}<a class="lg-link" href="{{ b.link_url }}">{{ b.link_label }} <span aria-hidden="true">&rarr;</span></a>{% endif -%}
    </article>
    {%- endfor -%}
  </div>
</div></section>
""", [check("no_top", "No space above", True)],
    blocks=[("part", "Part", [img("image", "Photo"), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("text", "Text"),
                              text("link_label", "Link"), url("link_url", "Link URL")])], max_blocks=3)

S["lg-photo-band"] = sec("Photo band, words", "lgc-pband", """
{%- assign s = section.settings -%}
<section class="lg-band is-photo" style="{% if s.bg != blank %}--band-bg:url({{ s.bg | image_url: width: 2000 }});{% endif %}--band-pos:{{ s.bg_pos }}"><div class="lg-wrap">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d1' %}
  {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
</div></section>
""", [img("bg", "Background photo"), text("bg_pos", "Background position", "center 50%"), text("eyebrow", "Eyebrow"),
      rich("heading", "Heading (italic = gold word)"), textarea("lede", "Line under it")])

S["lg-timeline"] = sec("Timeline", "lgc-tl", """
{%- assign s = section.settings -%}
<section class="lg-sec"><div class="lg-wrap tl-in">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}
  <div class="tl-hd"><p class="lg-lede">{{ s.lede }}</p><div class="arrows" data-arrows="tl-{{ section.id }}"><button type="button" aria-label="Previous">&lsaquo;</button><button type="button" aria-label="Next">&rsaquo;</button></div></div>
  <ol class="tl" id="tl-{{ section.id }}">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}
    <li{% if b.soon %} data-soon{% endif %} {{ block.shopify_attributes }}><span class="yr">{{ b.year }}</span><div><h3>{{ b.title }}{% if b.soon %} <span class="lg-tag soon">{{ b.soon_label }}</span>{% endif %}</h3><p>{{ b.text }}</p></div></li>
    {%- endfor -%}
  </ol>
</div></section>
""", [text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("lede", "Line under it")],
    blocks=[("moment", "Moment", [text("year", "When"), text("title", "Title"), textarea("text", "Text"),
                                  check("soon", "Still to come (dashed)", False), text("soon_label", "Tag when still to come", "Coming")])], max_blocks=30)

# ------------------------------------------------------------------ a row of cards: link cards, icon cards, numbers, gold-ruled
S["lg-cols"] = sec("Cards in a row", "lgc-cols", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  """ + HEAD_BLOCK + """
  {%- if s.sub != blank %}<p class="lg-body">{{ s.sub }}</p>{% endif -%}
  <div class="cols cols-{{ s.style }}">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}
    {%- case s.style -%}
    {%- when 'links' -%}
      <a class="nx" href="{{ b.url }}" {{ block.shopify_attributes }}><b>{{ b.title }}</b><span>{{ b.text }}</span>{% if b.go != blank %}<span class="go lg-link">{{ b.go }} <span>&rarr;</span></span>{% endif %}</a>
    {%- when 'numbers' -%}
      <div class="num" {{ block.shopify_attributes }}><span class="n">{{ forloop.index | prepend: '0' | slice: -2, 2 }}</span><h3 class="lg-d3">{{ b.title }}</h3><p>{{ b.text }}</p></div>
    {%- when 'rules' -%}
      <div class="rule" {{ block.shopify_attributes }}><b>{{ b.title }}</b><p>{{ b.text }}</p></div>
    {%- else -%}
      {%- if b.url != blank -%}<a class="hcard" href="{{ b.url }}" {{ block.shopify_attributes }}>{%- else -%}<div class="hcard" {{ block.shopify_attributes }}>{%- endif -%}
      {%- if b.icon != blank %}{% render 'lg-icon', name: b.icon %}{% endif -%}<b>{{ b.title }}</b><span>{{ b.text }}</span>
      {%- if b.url != blank -%}</a>{%- else -%}</div>{%- endif -%}
    {%- endcase -%}
    {%- endfor -%}
  </div>
  {%- if s.after != blank or s.after_link_label != blank -%}
  <p class="lg-body after">{{ s.after }}{% if s.after_link_label != blank %}<a class="lg-link" href="{{ s.after_link_url }}">{{ s.after_link_label }} <span aria-hidden="true">&rarr;</span></a>{% endif %}</p>
  {%- endif -%}
</div></section>
""", [text("anchor", "Anchor (for #links)"), check("no_top", "No space above", False),
      select("style", "Look", [("links", "Link cards"), ("icons", "Icon cards"), ("numbers", "Numbered (01, 02, 03)"), ("rules", "Gold rule on top")], "links"),
      text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("sub", "Line under the heading"),
      INLINE("after", "Line under the cards"), text("after_link_label", "Link under the cards"), url("after_link_url", "Link URL")],
    blocks=[("item", "Card", [select("icon", "Icon (icon cards)", ICONS, ""), text("title", "Title"), textarea("text", "Text"),
                              url("url", "Link (link and icon cards)"), text("go", "Link text (link cards)")])], max_blocks=6)

# ------------------------------------------------------------------ Questions (FAQ page and the ambassador FAQ)
S["lg-faq-page"] = sec("Questions", "lgc-faq", """
{%- assign s = section.settings -%}
""" + CRUMB + """
{%- if s.heading != blank -%}
<section class="lg-wrap faq-intro">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}
  {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
</section>
{%- endif -%}
{%- if s.jump -%}
<div class="jump"><nav class="lg-wrap jump-in" aria-label="On this page">
  {%- for block in section.blocks -%}{%- if block.type == 'topic' and block.settings.anchor != blank -%}<a href="#{{ block.settings.anchor }}">{{ block.settings.jump_label | default: block.settings.eyebrow }}</a>{%- endif -%}{%- endfor -%}
  {%- if s.jump_extra_label != blank %}<a href="{{ s.jump_extra_url }}">{{ s.jump_extra_label }}</a>{% endif -%}
</nav></div>
{%- endif -%}
{%- assign open = false -%}{%- assign ti = 0 -%}
{%- for block in section.blocks -%}{%- assign b = block.settings -%}
  {%- if block.type == 'topic' or open == false -%}
    {%- if open %}</div></div></section>{% endif -%}
    <section class="lg-sec blk{% if s.even %} is-even{% endif %}"{% if block.type == 'topic' and b.anchor != blank %} id="{{ b.anchor }}"{% endif %}{% if ti > 0 or s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap blk-in">
      <div>{%- if block.type == 'topic' -%}
        {%- if b.eyebrow != blank %}<p class="lg-eyebrow">{{ b.eyebrow }}</p>{% endif -%}
        {% render 'lg-h', text: b.heading, tag: 'h2', cls: 'lg-d2' %}
        {%- if b.text != blank %}<p class="lg-body">{{ b.text }}</p>{% endif -%}
      {%- endif -%}</div>
      <div class="lg-faq"{% if block.type == 'topic' %} {{ block.shopify_attributes }}{% endif %}>
    {%- assign open = true -%}{%- assign ti = ti | plus: 1 -%}
  {%- endif -%}
  {%- if block.type == 'q' -%}
    <details class="lg-fq"{% if b.open %} open{% endif %} {{ block.shopify_attributes }}><summary>{{ b.question }}</summary><div class="lg-fq-a">{{ b.answer }}</div></details>
  {%- endif -%}
{%- endfor -%}
{%- if open %}</div></div></section>{% endif -%}
{%- if s.jsonld -%}
{%- assign qn = 0 -%}
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
{%- for block in section.blocks -%}{%- if block.type == 'q' and block.settings.question != blank -%}
{%- if qn > 0 %},{% endif %}{"@type":"Question","name":{{ block.settings.question | json }},"acceptedAnswer":{"@type":"Answer","text":{{ block.settings.answer | strip_html | strip | json }}}}
{%- assign qn = qn | plus: 1 -%}
{%- endif -%}{%- endfor -%}
]}
</script>
{%- endif -%}
""", [text("crumb", "Breadcrumb label (empty = none)"), text("eyebrow", "Page eyebrow"), rich("heading", "Page heading, H1 (empty = none)"), textarea("lede", "Line under it"),
      check("jump", "Jump links along the top (sticky)", True), text("jump_extra_label", "Extra jump link"), url("jump_extra_url", "Extra jump link URL"),
      check("even", "Two even columns", False), check("no_top", "No space above the first group", False),
      check("jsonld", "Tell Google these are FAQs (FAQPage)", True),
      para("Add a Group, then its Questions under it. Each group gets its own heading, anchor and jump link.")],
    blocks=[("topic", "Group", [text("anchor", "Anchor (e.g. returns)"), text("jump_label", "Jump link label (empty = eyebrow)"),
                                text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("text", "Line under it")]),
            ("q", "Question", [text("question", "Question"), RICHTEXT("answer", "Answer"), check("open", "Open to start", False)])], max_blocks=50)

# ------------------------------------------------------------------ Ambassadors: what we ask + the apply panel
S["lg-ask"] = sec("Text + panel", "lgc-ask", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap two">
  <div>
    """ + HEAD_BLOCK + """
    {%- if s.body != blank %}<p class="lg-body">{{ s.body }}</p>{% endif -%}
    {%- if section.blocks.size > 0 -%}<ul class="bar-list">
      {%- for block in section.blocks -%}<li {{ block.shopify_attributes }}>{% render 'lg-icon', name: 'badge-check' %}<div>{{ block.settings.text }}</div></li>{%- endfor -%}
    </ul>{%- endif -%}
    {%- if s.after != blank %}<p class="lg-body after">{{ s.after }}</p>{% endif -%}
  </div>
  <div class="apply lg-panel">
    {%- if s.p_eyebrow != blank %}<p class="lg-eyebrow">{{ s.p_eyebrow }}</p>{% endif -%}
    {%- if s.p_title != blank %}<h3 class="lg-d3">{{ s.p_title }}</h3>{% endif -%}
    {%- if s.p_text != blank %}<p>{{ s.p_text }}</p>{% endif -%}
    {%- if s.btn_label != blank %}<a class="lg-btn" href="{{ s.btn_url }}"{% if s.new_tab %} target="_blank" rel="noopener"{% endif %}>{{ s.btn_label }} <span aria-hidden="true">&rarr;</span></a>{% endif -%}
  </div>
</div></section>
""", [check("no_top", "No space above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), textarea("body", "Text"),
      textarea("after", "Line under the list"), header("Panel"), text("p_eyebrow", "Eyebrow"), text("p_title", "Title"), textarea("p_text", "Text"),
      text("btn_label", "Gold button"), url("btn_url", "Button link"), check("new_tab", "Open in a new tab", True)],
    blocks=[("item", "List item", [INLINE("text", "Text")])], max_blocks=8)

# ------------------------------------------------------------------ Compare
S["lg-proof"] = sec("Proof line", "lgc-proof", """
{%- assign s = section.settings -%}""" + RATING + """
{%- liquid
  assign p = s.product
  assign rc = 0
  if p != blank
    assign rc = p.metafields.reviews.rating_count.value | default: 0
    assign rv = p.metafields.reviews.rating.value.rating
  endif
-%}
<section class="lg-sec" style="padding-bottom:0"><div class="lg-wrap"><div class="proof">
  {%- if rc >= min and rv -%}{%- assign n = rv | round -%}<span>""" + STARS_N.replace('aria-label="{{ n }} out of 5"', 'aria-label="{{ rv | round: 1 }} out of 5"') + """{{ s.rating_line | replace: '[rating]', rv | replace: '[count]', rc }}</span>{%- endif -%}
  {%- for block in section.blocks -%}<span {{ block.shopify_attributes }}>{{ block.settings.text }}</span>{%- endfor -%}
</div></div></section>
""", [product("product", "Product whose Judge.me score leads"), text("rating_line", "Score line ([rating], [count])", "[rating] from [count] Carver reviews"),
      para("The score only shows once the product has the review minimum.")],
    blocks=[("item", "Line", [text("text", "Text")])], max_blocks=4)

S["lg-cmp-cards"] = sec("Two product cards", "lgc-pc", """
{%- assign s = section.settings -%}""" + RATING + """
<section class="lg-sec"{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  """ + HEAD_BLOCK + """
  <div class="cards">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}{%- assign p = b.product -%}{%- if p != blank -%}
    {%- liquid
      assign pic = b.image | default: p.metafields.custom.cutout.value | default: p.featured_image
      assign rc = p.metafields.reviews.rating_count.value | default: 0
      assign rv = p.metafields.reviews.rating.value.rating
    -%}
    <article class="pc" {{ block.shopify_attributes }}>
      <a class="pc-ph" href="{{ p.url }}">{%- if b.tag != blank %}<span class="lg-tag">{{ b.tag }}</span>{% endif -%}{%- if pic -%}{{ pic | image_url: width: 900 | image_tag: loading: 'lazy', alt: p.title, widths: '450,700,900', sizes: '(max-width: 560px) 100vw, 430px' }}{%- endif -%}</a>
      <div class="pc-bd">
        <div class="pc-top"><h3><a href="{{ p.url }}">{{ p.title }}</a></h3><b>{{ p.price | money_without_trailing_zeros }}</b></div>
        {%- if rc >= min and rv -%}{%- assign n = rv | round -%}<a class="pc-rate" href="{{ p.url }}#reviews">""" + STARS_N.replace('aria-label="{{ n }} out of 5"', 'aria-label="{{ rv | round: 1 }} out of 5"') + """{{ rv }} · {{ rc }}</a>{%- endif -%}
        {%- if b.line != blank %}<p>{{ b.line }}</p>{% endif -%}
        <a class="lg-btn lg-btn-sm" href="{{ p.url }}">{{ b.btn_label }} <span aria-hidden="true">&rarr;</span></a>
      </div>
    </article>
    {%- endif -%}{%- endfor -%}
  </div>
</div></section>
""", [check("no_top", "No space above", False), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)")],
    blocks=[("card", "Product", [product("product", "Product"), img("image", "Photo (empty = the product's cutout)"), text("tag", "Tag (e.g. Best seller)"),
                                 text("line", "Line"), text("btn_label", "Button", "Pick a loft")])], max_blocks=4)

S["lg-table"] = sec("Side-by-side table", "lgc-table", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.anchor != blank %} id="{{ s.anchor }}"{% endif %}{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  """ + HEAD_BLOCK + """
  {%- if s.sub != blank %}<p class="lg-body">{{ s.sub }}</p>{% endif -%}
  <div class="tablewrap"><table class="lg-table">
    <thead><tr><th scope="col"><span class="sr">{{ s.col0 }}</span></th><th scope="col">{{ s.col_them }}</th><th scope="col">{{ s.col_us }}</th></tr></thead>
    <tbody>
      {%- for block in section.blocks -%}<tr {{ block.shopify_attributes }}><th scope="row">{{ block.settings.label }}</th><td class="them">{{ block.settings.them }}</td><td class="us">{{ block.settings.us }}</td></tr>{%- endfor -%}
    </tbody>
  </table></div>
  {%- if s.after != blank %}<p class="lg-body after">{{ s.after }}</p>{% endif -%}
</div></section>
""", [text("anchor", "Anchor", "breakdown"), check("no_top", "No space above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"),
      textarea("sub", "Line under the heading"), text("col0", "First column (screen readers)", "What we compared"), text("col_them", "Their column", "The big names"),
      text("col_us", "Our column", "Lucky"), textarea("after", "Line under the table")],
    blocks=[("row", "Row", [text("label", "Row"), text("them", "Theirs"), text("us", "Ours")])], max_blocks=16)

S["lg-quotes"] = sec("Review quotes", "lgc-rq", """
{%- assign s = section.settings -%}
<section class="lg-sec"{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap">
  """ + HEAD_BLOCK + """
  <div class="rqs">
    {%- for block in section.blocks -%}{%- assign b = block.settings -%}{%- assign n = b.stars -%}
    <figure class="rq" {{ block.shopify_attributes }}>""" + STARS_N + """<blockquote>&ldquo;{{ b.quote }}&rdquo;</blockquote><figcaption><b>{{ b.name }}</b>{% if b.on != blank %} · {{ b.on }}{% endif %}</figcaption></figure>
    {%- endfor -%}
  </div>
  {%- if s.link_label != blank %}<p class="lg-body after"><a class="lg-link" href="{{ s.link_url }}">{{ s.link_label }} <span aria-hidden="true">&rarr;</span></a></p>{% endif -%}
</div></section>
""", [check("no_top", "No space above", True), text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"),
      text("link_label", "Link under them"), url("link_url", "Link URL"),
      para("Quotes are Judge.me reviews typed in word for word, with the stars they gave. Never edit or invent a review.")],
    blocks=[("quote", "Review", [rng("stars", "Stars they gave", 1, 5, 1, 5), textarea("quote", "Quote, word for word"), text("name", "Name as on Judge.me"),
                                 text("on", "After the name", "Carver, verified buyer")])], max_blocks=6)

# ------------------------------------------------------------------ Contact (Shopify's contact form, so messages reach the store)
S["lg-contact"] = sec("Contact form", "lgc-contact", """
{%- assign s = section.settings -%}
""" + CRUMB + """
<section class="lg-sec" style="padding-top:clamp(16px,2vw,24px)"><div class="lg-wrap wrap2">
  <div>
    {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
    {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}
    {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
    <ul class="ways">
      {%- for block in section.blocks -%}<li {{ block.shopify_attributes }}>{% if block.settings.icon != blank %}{% render 'lg-icon', name: block.settings.icon %}{% endif %}<div><b>{{ block.settings.title }}</b><p>{{ block.settings.text }}</p></div></li>{%- endfor -%}
    </ul>
  </div>
  {%- form 'contact', class: 'form', id: 'contact-form' -%}
    {%- if form.posted_successfully? -%}
      <p class="sent is-on" role="status">{{ s.sent }}</p>
    {%- else -%}
    {%- if form.errors -%}<p class="sent is-on is-err" role="alert">{{ form.errors | default_errors }}</p>{%- endif -%}
    <div class="row two">
      <label><span class="lb">{{ s.l_name }}</span><input name="contact[name]" autocomplete="name" required value="{{ form.name }}"></label>
      <label><span class="lb">{{ s.l_email }}</span><input name="contact[email]" type="email" autocomplete="email" required value="{{ form.email }}"></label>
    </div>
    <div class="row two">
      <label><span class="lb">{{ s.l_order }}</span><input name="contact[Order number]" placeholder="{{ s.p_order }}"></label>
      <label><span class="lb">{{ s.l_topic }}</span><select name="contact[Topic]">
        {%- assign ts = s.topics | newline_to_br | split: '<br />' -%}{%- for t in ts -%}{%- assign tt = t | strip -%}{%- if tt != blank %}<option>{{ tt }}</option>{% endif -%}{%- endfor -%}
      </select></label>
    </div>
    <div class="row"><label><span class="lb">{{ s.l_msg }}</span><textarea name="contact[body]" required>{{ form.body }}</textarea></label></div>
    <button class="lg-btn" type="submit">{{ s.btn }} {% render 'lg-icon', name: 'send' %}</button>
    {%- endif -%}
  {%- endform -%}
</div></section>
""", [text("crumb", "Breadcrumb label (empty = none)", "Contact"), text("eyebrow", "Eyebrow"), rich("heading", "Heading, H1 (italic = gold word)"), textarea("lede", "Line under it"),
      header("The form"), text("l_name", "Name label", "Name"), text("l_email", "Email label", "Email"), text("l_order", "Order label", "Order number"),
      text("p_order", "Order placeholder", "If you have one"), text("l_topic", "Topic label", "What's it about"), textarea("topics", "Topics (one per line)"),
      text("l_msg", "Message label", "Message"), text("btn", "Button", "Send it"), textarea("sent", "After it's sent"),
      para("Messages go to the store's sender email (Settings > Notifications), same as the old contact page.")],
    blocks=[("way", "Way to reach us", [select("icon", "Icon", ICONS, "mail"), text("title", "Title"), INLINE("text", "Text")])], max_blocks=6)

# ------------------------------------------------------------------ Community wall (posts = Content > Metaobjects > Community post)
S["lg-wall"] = sec("Community wall", "lgc-wall", """
{%- comment -%}
  The wall: every Community post, four across, filterable by what's in it (clubs / apparel / gear,
  worked out from the products: tagged "club" = clubs, Apparel or hat = apparel, anything else = gear).
  Tap a post and the shoppable pop-up (lucky-site.js, [data-posts]) opens it.
{%- endcomment -%}
{%- assign s = section.settings -%}
{%- assign posts = shop.metaobjects.community_post.values -%}
<div data-posts>
<div class="bar"><div class="lg-wrap bar-in">
  <div class="fg" role="group" aria-label="{{ s.show_label | escape }}"><span class="lbl">{{ s.show_label }}</span>
    <button type="button" data-k="" aria-pressed="true">{{ s.all_label }}</button>
    <button type="button" data-k="clubs" aria-pressed="false">{{ s.clubs_label }}</button>
    <button type="button" data-k="apparel" aria-pressed="false">{{ s.apparel_label }}</button>
    <button type="button" data-k="gear" aria-pressed="false">{{ s.gear_label }}</button>
  </div>
  <span class="count"><b data-shown>{{ posts.size }}</b> {{ s.count_word }}</span>
</div></div>
<section class="lg-wrap">
  <div class="wall" data-wall data-page="{{ s.page }}">
    {%- for m in posts -%}
      {%- liquid
        assign med = m.media.value
        assign ps = m.products.value
        assign kinds = ''
        assign names = ''
        for p in ps
          assign pt = p.type | downcase
          if p.tags contains 'club'
            assign kinds = kinds | append: ' clubs'
          elsif pt == 'apparel' or pt == 'hat' or pt contains 'polo'
            assign kinds = kinds | append: ' apparel'
          else
            assign kinds = kinds | append: ' gear'
          endif
          if forloop.first
            assign names = p.title
          else
            assign names = names | append: ', ' | append: p.title
          endif
        endfor
        assign alt = m.caption.value | default: m.handle_text.value
      -%}
      <button type="button" class="post" data-post="{{ forloop.index0 }}" data-kinds="{{ kinds | strip }}" aria-label="{{ alt | escape }}{% if names != blank %}. In it: {{ names | escape }}{% endif %}"{% if forloop.index > s.page %} hidden{% endif %}>
        {%- if med.media_type == 'video' -%}{{ med.preview_image | image_url: width: 700 | image_tag: loading: 'lazy', alt: '', widths: '350,500,700', sizes: '(max-width: 640px) 50vw, 25vw' }}<span class="wild-play" aria-hidden="true"></span>
        {%- elsif med -%}{{ med | image_url: width: 700 | image_tag: loading: 'lazy', alt: alt, widths: '350,500,700', sizes: '(max-width: 640px) 50vw, 25vw' }}{%- endif -%}
        <span class="who">{{ m.handle_text.value }}</span>
        {%- if ps.count > 0 %}<span class="bag">{% render 'lg-icon', name: 'shopping-bag' %}{{ ps.count }}</span>{% endif -%}
      </button>
    {%- endfor -%}
  </div>
  <div class="more">
    {%- if s.aside != blank %}<p class="lg-aside">{{ s.aside }}</p>{% endif -%}
    <button class="lg-btn-line lg-btn-sm" type="button" data-more{% if posts.size <= s.page %} hidden{% endif %}>{{ s.more_label }}</button>
  </div>
</section>

{%- for m in posts -%}
  {%- assign med = m.media.value -%}{%- assign ps = m.products.value -%}
  <template data-post-tpl="{{ forloop.index0 }}">
    <div class="pm-media">
      {%- if med.media_type == 'video' -%}{{ med | video_tag: autoplay: true, loop: true, muted: true, controls: true }}
      {%- elsif med -%}{{ med | image_url: width: 1100 | image_tag: alt: m.caption.value, widths: '600,900,1100', sizes: '(max-width: 749px) 100vw, 55vw' }}{%- endif -%}
    </div>
    <div class="pm-info">
      <p class="pm-who">{%- if m.link.value != blank -%}<a href="{{ m.link.value }}" target="_blank" rel="noopener">{{ m.handle_text.value }}</a>{%- else -%}{{ m.handle_text.value }}{%- endif -%}</p>
      {%- if m.caption.value != blank %}<p class="pm-cap">{{ m.caption.value }}</p>{% endif -%}
      {%- if ps.count > 0 -%}
        <p class="lg-label pm-in">{{ s.in_label }}</p>
        <div class="pm-prods">
        {%- for p in ps -%}
          {%- assign pic = p.metafields.custom.cutout.value | default: p.featured_image -%}
          {%- assign v = p.selected_or_first_available_variant -%}
          <form class="pm-prod" data-lg-add action="{{ routes.cart_add_url }}" method="post">
            <a class="pm-ph" href="{{ p.url }}">{%- if pic -%}{{ pic | image_url: width: 200 | image_tag: alt: p.title, loading: 'lazy' }}{%- endif -%}</a>
            <div class="pm-bd">
              <a class="pm-nm" href="{{ p.url }}">{{ p.title }}</a>
              <span class="pm-pr">{{ v.price | money_without_trailing_zeros }}</span>
              {%- if p.has_only_default_variant -%}
                <input type="hidden" name="id" value="{{ v.id }}">
              {%- else -%}
                <label class="sr" for="pw-v-{{ forloop.parentloop.index }}-{{ p.id }}">{{ p.options | join: ' / ' }}</label>
                <select class="lg-input pm-sel" id="pw-v-{{ forloop.parentloop.index }}-{{ p.id }}" name="id">
                  {%- for x in p.variants -%}<option value="{{ x.id }}"{% unless x.available %} disabled{% endunless %}{% if x.id == v.id %} selected{% endif %}>{{ x.title }}{% unless x.available %} (sold out){% endunless %}</option>{%- endfor -%}
                </select>
              {%- endif -%}
            </div>
            {%- if p.available -%}<button class="lg-btn-line lg-btn-sm pm-add" type="submit">Add to bag</button>{%- else -%}<a class="lg-btn-line lg-btn-sm pm-add" href="{{ p.url }}">Sold out</a>{%- endif -%}
          </form>
        {%- endfor -%}
        </div>
      {%- endif -%}
    </div>
  </template>
{%- endfor -%}

<div class="md md-post" hidden role="dialog" aria-modal="true" aria-label="Community post">
  <div class="md-bd" data-md-close></div>
  <div class="md-panel pm">
    <button type="button" class="md-x" data-md-close aria-label="Close">&times;</button>
    <div class="pm-body"></div>
    <div class="pm-nav"><button type="button" data-post-step="-1" aria-label="Previous post">&lsaquo;</button><button type="button" data-post-step="1" aria-label="Next post">&rsaquo;</button></div>
  </div>
</div>
</div>
<script>
(function(){
  var sec = document.currentScript.previousElementSibling, wall = sec.querySelector('[data-wall]'), PAGE = +wall.getAttribute('data-page') || 8, limit = PAGE, kind = '';
  var posts = [].slice.call(wall.querySelectorAll('.post')), more = sec.querySelector('[data-more]'), shown = sec.querySelector('[data-shown]');
  function draw(){ var n = 0;
    posts.forEach(function(p){ var ok = !kind || (' ' + p.getAttribute('data-kinds') + ' ').indexOf(' ' + kind + ' ') > -1; if (ok) n++; p.hidden = !ok || n > limit; });
    shown.textContent = n; more.hidden = n <= limit; }
  sec.addEventListener('click', function(e){
    var k = e.target.closest('[data-k]');
    if (k){ [].forEach.call(sec.querySelectorAll('[data-k]'), function(x){ x.setAttribute('aria-pressed', String(x === k)); }); kind = k.getAttribute('data-k'); limit = PAGE; draw(); return; }
    if (e.target.closest('[data-more]')){ limit += PAGE; draw(); }
  });
  var m = location.hash.match(/^#post-(\\d+)$/); if (m){ limit = Math.max(PAGE, +m[1]); }
  draw();
})();
</script>
""", [text("show_label", "Filter label", "Show"), text("all_label", "Everything", "Everything"), text("clubs_label", "Clubs", "Clubs"),
      text("apparel_label", "Apparel", "Apparel"), text("gear_label", "Gear", "Gear"), text("count_word", "After the count", "posts"),
      number("page", "Posts to start (and per tap)", 8), text("more_label", "Show more button", "Show more"), textarea("aside", "Small line under the wall"),
      text("in_label", "Pop-up: products heading", "What's in the shot"),
      para("Posts come from Content > Metaobjects > Community post: a photo or video, the @handle, a caption, a link and the products in it. Newest first is the order they're listed there.")])

# ------------------------------------------------------------------ All reviews: the live score, a tile per club, then Judge.me's widget
S["lg-reviews-all"] = sec("All reviews", "lgc-rv", """
{%- comment -%}
  All reviews: our live score, star bars and a tile per club, a sticky filter bar, then Judge.me's
  all-reviews list. Judge.me's own header, medals, store-review button and Shop reviews tab are hidden
  (70-content.css); our star bars and chips drive its star filter and sort, the club chips filter the
  reviews on the page by product.
{%- endcomment -%}
{%- liquid
  assign s = section.settings
  assign min = settings.lg_review_min | default: 10
  assign n = 0
  assign sum = 0
  for block in section.blocks
    assign p = block.settings.product
    if p != blank
      assign rc = p.metafields.reviews.rating_count.value | default: 0
      assign rv = p.metafields.reviews.rating.value.rating | default: 0
      assign n = n | plus: rc
      assign sum = rv | times: rc | plus: sum
    endif
  endfor
  if n > 0
    assign avg = sum | divided_by: n | round: 1
  endif
-%}
<div data-rv>
<section class="lg-sec" style="padding-bottom:0"><div class="lg-wrap sum">
  <div class="lg-score">
    {%- if n >= min -%}
    <b>{{ avg }}</b>
    <div><span class="lg-stars" aria-label="{{ avg }} out of 5">{% render 'lg-stars' %}</span><span class="of">{{ s.of_line | replace: '[count]', n }}</span></div>
    {%- endif -%}
    <div class="lg-score-bars" style="grid-column:1/-1" data-bars></div>
  </div>
  <div class="clubs">
    {%- for block in section.blocks -%}{%- assign p = block.settings.product -%}{%- if p != blank -%}
      {%- assign rc = p.metafields.reviews.rating_count.value | default: 0 -%}{%- assign rv = p.metafields.reviews.rating.value.rating | default: 0 -%}
      <button class="ct" type="button" data-ct="{{ forloop.index }}" aria-pressed="false" {{ block.shopify_attributes }}><b>{{ block.settings.label | default: p.title }}</b>
        {%- if rc >= min -%}<span><span class="lg-stars" aria-hidden="true">{% render 'lg-stars' %}</span><em>{{ rv | round: 1 }} · {{ rc }} {{ s.tile_word }}</em></span>{%- endif -%}</button>
    {%- endif -%}{%- endfor -%}
  </div>
</div></section>

<div class="bar"><div class="lg-wrap bar-in">
  <div class="fg" role="group" aria-label="{{ s.club_label | escape }}"><span class="lbl">{{ s.club_label }}</span>
    <button type="button" data-c="0" aria-pressed="true">{{ s.all_label }}</button>
    {%- for block in section.blocks -%}{%- assign p = block.settings.product -%}{%- if p != blank -%}
      {%- capture hs -%}{{ p.handle }}{% for x in block.settings.also %} {{ x.handle }}{% endfor %}{%- endcapture -%}
      {%- assign nm = block.settings.label | default: p.title -%}
      <button type="button" data-c="{{ forloop.index }}" data-handles="{{ hs | strip }}" data-url="{{ p.url }}#reviews" data-name="{{ nm | escape }}" data-count="{{ p.metafields.reviews.rating_count.value | default: 0 }}" aria-pressed="false">{{ nm }}</button>
    {%- endif -%}{%- endfor -%}
  </div>
  <div class="fg" role="group" aria-label="{{ s.stars_label | escape }}"><span class="lbl">{{ s.stars_label }}</span>
    <button type="button" data-s="0" aria-pressed="true">{{ s.all_label }}</button>
    {%- for i in (1..5) -%}{%- assign k = 6 | minus: i -%}<button type="button" data-s="{{ k }}" aria-pressed="false">{{ k }} ★</button>{%- endfor -%}
  </div>
  <div class="fright"><label><span class="sr">{{ s.sort_label }}</span><select data-sort>
    <option value="most-recent">{{ s.sort_recent }}</option><option value="highest-rating">{{ s.sort_high }}</option><option value="lowest-rating">{{ s.sort_low }}</option>
  </select></label></div>
</div></div>

<section class="lg-wrap jm" id="{{ s.anchor | default: 'all-reviews' }}">
  <p class="club-note" data-club-note hidden><span></span> <a class="lg-link" href="#"><em></em> <span aria-hidden="true">&rarr;</span></a></p>
  {% render 'judgeme_all_reviews' %}
</section>
</div>
<script>
(function(){
  var sec = document.currentScript.previousElementSibling, $$ = function(s, r){ return [].slice.call((r || sec).querySelectorAll(s)); };
  var jm = function(){ return sec.querySelector('.jdgm-all-reviews-widget'); };
  var club = null, note = sec.querySelector('[data-club-note]');
  var WORD = {{ s.note_line | json }}, LINK = {{ s.note_link | json }};
  function press(attr, v){ $$('[' + attr + ']').forEach(function(x){ x.setAttribute('aria-pressed', String(x.getAttribute(attr) === String(v))); }); }
  /* the bars: Judge.me's live star split (its hidden histogram) drawn our way; tap one to filter */
  function bars(){
    var box = sec.querySelector('[data-bars]'), w = jm(); if (!w || box.childElementCount) return;
    box.innerHTML = [5, 4, 3, 2, 1].map(function(n){ var r = w.querySelector('.jdgm-histogram__row[data-rating="' + n + '"]'); if (!r) return '';
      var p = r.getAttribute('data-percentage') || 0;
      return '<button class="lg-score-row is-btn" type="button" data-s="' + n + '" aria-pressed="false" aria-label="' + n + ' star reviews"><span>' + n + ' \\u2605</span><i style="--pct:' + p + '%"></i><span>' + p + '%</span></button>'; }).join('');
  }
  function stars(n){
    press('data-s', n); var w = jm(); if (!w) return;
    var t = n ? w.querySelector('.jdgm-histogram__row[data-rating="' + n + '"]') : w.querySelector('.jdgm-histogram__clear-filter');
    if (t) t.click();
  }
  function apply(){
    var w = jm(); if (!w) return;
    var hs = club ? club.getAttribute('data-handles').split(' ') : null;
    $$('.jdgm-all-reviews__body .jdgm-rev', w).forEach(function(r){
      var a = r.querySelector('.jdgm-rev__prod-link'), m = a && (a.getAttribute('href') || '').match(/\\/products\\/([^/?#]+)/);
      var hide = !!hs && !(m && hs.indexOf(m[1]) > -1);
      if (r.hidden !== hide) r.hidden = hide;
    });
  }
  function setClub(i){
    club = i ? sec.querySelector('[data-c="' + i + '"]') : null;
    press('data-c', i || 0); press('data-ct', i || 0);
    if (club){
      note.hidden = false; note.firstElementChild.textContent = WORD.replace('[club]', club.getAttribute('data-name'));
      var a = note.querySelector('a'); a.href = club.getAttribute('data-url');
      a.querySelector('em').textContent = LINK.replace('[club]', club.getAttribute('data-name')).replace('[count]', club.getAttribute('data-count'));
    } else note.hidden = true;
    var wr = document.querySelector('.lg-signoff a[href*="#reviews"]'); if (wr && club) wr.href = club.getAttribute('data-url');
    apply();
  }
  sec.addEventListener('click', function(e){
    var c = e.target.closest('[data-c]'); if (c){ setClub(+c.getAttribute('data-c')); return; }
    var t = e.target.closest('[data-ct]'); if (t){ setClub(t.getAttribute('aria-pressed') === 'true' ? 0 : +t.getAttribute('data-ct')); sec.querySelector('.bar').scrollIntoView({ behavior: 'smooth' }); return; }
    var s = e.target.closest('[data-s]');
    if (s){ var n = +s.getAttribute('data-s'), bar = s.classList.contains('is-btn'); if (bar && s.getAttribute('aria-pressed') === 'true') n = 0;
      stars(n); if (bar) sec.querySelector('.bar').scrollIntoView({ behavior: 'smooth' }); }
  });
  sec.querySelector('[data-sort]').addEventListener('change', function(){
    var w = jm(), d = w && w.querySelector('.jdgm-sort-dropdown'); if (!d) return;
    d.value = this.value; d.dispatchEvent(new Event('change', { bubbles: true }));
  });
  /* Judge.me fills the list after load and on every page / filter: redraw the bars and re-filter */
  new MutationObserver(function(){ bars(); apply(); }).observe(sec.querySelector('.jm'), { childList: true, subtree: true });
  bars();
})();
</script>
""", [text("of_line", "Under the score ([count] = live count)", "out of five, from [count] reviews"), text("tile_word", "After each club's count", "reviews"),
      text("club_label", "Club filter label", "Club"), text("stars_label", "Stars filter label", "Stars"), text("all_label", "All", "All"),
      text("sort_label", "Sort label (screen readers)", "Sort"), text("sort_recent", "Most recent", "Most recent"), text("sort_high", "Highest rating", "Highest rating"), text("sort_low", "Lowest rating", "Lowest rating"),
      text("note_line", "With a club picked ([club])", "Showing the [club] reviews on this page."), text("note_link", "Link to that club's reviews ([club], [count])", "All [count] [club] reviews"),
      text("anchor", "Anchor for the list", "all-reviews"),
      para("Scores are read live from each product's Judge.me metafields and only show at the review minimum. One block per review pool; put the pool's other products (Carver 02 Black with the Gold) under Same pool so the club filter catches them. The list is Judge.me's all-reviews widget; the star bars come from its live split.")],
    blocks=[("club", "Club", [product("product", "Product"), text("label", "Name (empty = product's)"), plist("also", "Same pool (other products)", 5)])], max_blocks=8)

# ------------------------------------------------------------------ 404
S["lg-nf"] = sec("Not found", "lgc-nf", """
{%- assign s = section.settings -%}
<section class="lg-wrap nf">
  {% render 'lg-mags' %}
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow" style="justify-content:center">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}
  {%- if s.lede != blank %}<p class="lg-lede">{{ s.lede }}</p>{% endif -%}
  <div class="btns">
    {%- if s.btn_label != blank %}<a class="lg-btn" href="{{ s.btn_url }}">{{ s.btn_label }}</a>{% endif -%}
    {%- if s.btn2_label != blank %}<a class="lg-btn-line" href="{{ s.btn2_url }}">{{ s.btn2_label }}</a>{% endif -%}
  </div>
  <div class="pop">
    {%- for block in section.blocks -%}{%- assign p = block.settings.product -%}{%- if p != blank -%}
      {%- assign pic = block.settings.image | default: p.metafields.custom.cutout.value | default: p.featured_image -%}
      <a href="{{ p.url }}" {{ block.shopify_attributes }}><span class="ph">{%- if pic -%}{{ pic | image_url: width: 600 | image_tag: loading: 'lazy', alt: p.title, widths: '300,450,600', sizes: '(max-width: 860px) 50vw, 25vw' }}{%- endif -%}</span><span class="nm">{{ block.settings.name | default: p.title }}</span><b>{{ p.price | money_without_trailing_zeros }}</b></a>
    {%- endif -%}{%- endfor -%}
  </div>
</section>
""", [text("eyebrow", "Eyebrow", "404"), rich("heading", "Heading, H1 (italic = gold word)"), textarea("lede", "Line under it"),
      text("btn_label", "Gold button"), url("btn_url", "Gold button link"), text("btn2_label", "Second button"), url("btn2_url", "Second button link")],
    blocks=[("card", "Product", [product("product", "Product"), img("image", "Photo (empty = the product's cutout)"), text("name", "Name (empty = product's)")])], max_blocks=4)

# ------------------------------------------------------------------ Search (real Shopify search; results refresh as you type via the Section Rendering API)
CARD_R = """
          {%- assign pic = r.metafields.custom.cutout.value | default: r.featured_image -%}
          {%- capture kind -%}{%- if r.tags contains 'wedge' -%}Wedge{%- elsif r.tags contains 'putter' -%}Putter{%- elsif r.tags contains 'hybrid' -%}Hybrid{%- elsif r.title contains 'Polo' -%}Polo{%- elsif r.title contains 'Hat' -%}Hat{%- else -%}{{ r.type }}{%- endif -%}{%- endcapture -%}
          <a class="r" href="{{ r.url }}"><span class="ph">{%- if pic -%}{{ pic | image_url: width: 600 | image_tag: loading: 'lazy', alt: r.title, widths: '300,450,600', sizes: '(max-width: 820px) 50vw, 25vw' }}{%- endif -%}</span><span class="nm">{{ r.title }}</span><b>{{ r.price | money_without_trailing_zeros }}</b>{% if kind != blank %}<span class="kind">{{ kind }}</span>{% endif %}</a>"""
S["lg-search"] = sec("Search", "lgc-search", """
{%- assign s = section.settings -%}
<section class="lg-sec" style="padding-bottom:0" data-search-sec="{{ section.id }}"><div class="lg-wrap">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}
  <form class="sbox" role="search" action="{{ routes.search_url }}" method="get" data-search>
    {% render 'lg-icon', name: 'search' %}
    <label class="sr" for="q-{{ section.id }}">{{ s.label }}</label>
    <input id="q-{{ section.id }}" name="q" type="search" value="{{ search.terms | escape }}" placeholder="{{ s.placeholder }}" autocomplete="off">
    <input type="hidden" name="options[prefix]" value="last">
    <button class="lg-btn" type="submit">{{ s.btn }}</button>
  </form>
  {%- if s.sugs != blank -%}
  <div class="sugs" aria-label="{{ s.sugs_label | escape }}">
    {%- assign sg = s.sugs | split: ',' -%}{%- for x in sg -%}{%- assign t = x | strip -%}<a href="{{ routes.search_url }}?q={{ t | url_encode }}&amp;options%5Bprefix%5D=last" data-q="{{ t | escape }}">{{ t }}</a>{%- endfor -%}
  </div>
  {%- endif -%}
  <div data-results>
  {%- if search.performed -%}
    <p class="count" role="status">{{ search.results_count }} {% if search.results_count == 1 %}{{ s.one }}{% else %}{{ s.many }}{% endif %} &ldquo;{{ search.terms | escape }}&rdquo;</p>
    {%- if search.results_count > 0 -%}
    {%- liquid
      assign np = 0
      assign nt = 0
      for r in search.results
        if r.object_type == 'product'
          assign np = np | plus: 1
        else
          assign nt = nt | plus: 1
        endif
      endfor
    -%}
    {%- if np > 0 -%}
    <div class="res">
      {%- for r in search.results -%}{%- if r.object_type == 'product' -%}
""" + CARD_R + """
      {%- endif -%}{%- endfor -%}
    </div>
    {%- endif -%}
    {%- if nt > 0 -%}
    <div class="texts">
      <h2 class="lg-label">{{ s.texts_label }}</h2>
      <ul>
      {%- for r in search.results -%}{%- unless r.object_type == 'product' -%}
        {%- if r.object_type == 'article' -%}{%- assign ex = r.excerpt_or_content -%}{%- else -%}{%- assign ex = r.content -%}{%- endif -%}
        <li><a class="tx" href="{{ r.url }}">
          {%- if r.object_type == 'article' and r.image -%}<span class="tx-ph">{{ r.image | image_url: width: 320 | image_tag: loading: 'lazy', alt: r.title }}</span>{%- endif -%}
          <span class="tx-bd"><span class="kind">{% if r.object_type == 'article' %}{{ s.article_word }}{% else %}{{ s.page_word }}{% endif %}</span><b>{{ r.title }}</b>
          {%- assign ex = ex | strip_html | strip_newlines | truncatewords: 26 -%}{%- if ex != blank %}<span class="ex">{{ ex }}</span>{% endif -%}</span></a></li>
      {%- endunless -%}{%- endfor -%}
      </ul>
    </div>
    {%- endif -%}
    {%- else -%}
    <p class="none">{{ s.none }}</p>
    {%- endif -%}
  {%- else -%}
    {%- if s.start.size > 0 -%}
    <div class="res">
      {%- for r in s.start -%}
""" + CARD_R + """
      {%- endfor -%}
    </div>
    {%- endif -%}
  {%- endif -%}
  </div>
</div></section>
<script>
(function(){
  var sec = document.currentScript.previousElementSibling, f = sec.querySelector('[data-search]'), q = f.querySelector('[name=q]'), box = sec.querySelector('[data-results]'), t, ctl;
  function run(v){
    var p = new URLSearchParams(new FormData(f)); p.set('q', v); p.set('section_id', sec.getAttribute('data-search-sec'));
    if (ctl) ctl.abort(); ctl = window.AbortController ? new AbortController() : null;
    fetch(f.action + '?' + p.toString(), ctl ? { signal: ctl.signal } : {}).then(function(r){ return r.text(); }).then(function(h){
      var d = new DOMParser().parseFromString(h, 'text/html').querySelector('[data-results]'); if (d) box.innerHTML = d.innerHTML;
      p.delete('section_id'); try { history.replaceState(null, '', v ? f.action + '?' + p.toString() : f.action); } catch (e) {}
    }).catch(function(){});
  }
  q.addEventListener('input', function(){ clearTimeout(t); var v = q.value.trim(); t = setTimeout(function(){ run(v); }, 250); });
  sec.addEventListener('click', function(e){ var a = e.target.closest('[data-q]'); if (!a) return; e.preventDefault(); q.value = a.getAttribute('data-q'); run(q.value); });
})();
</script>
""", [text("eyebrow", "Eyebrow", "Search"), rich("heading", "Heading, H1 (italic = gold word)"), text("label", "Field label (screen readers)", "Search Lucky Golf"),
      text("placeholder", "Placeholder"), text("btn", "Button", "Search"), text("sugs", "Quick searches (comma separated)"), text("sugs_label", "Quick searches label (screen readers)", "Common searches"),
      text("one", "After the count (one)", "result for"), text("many", "After the count (many)", "results for"),
      INLINE("none", "When nothing matches"), text("texts_label", "Heading over pages and posts", "Pages and posts"), text("article_word", "Tag on articles", "Article"), text("page_word", "Tag on pages", "Page"),
      plist("start", "Products to show before a search", 24)])
