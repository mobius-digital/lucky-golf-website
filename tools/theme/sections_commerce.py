"""Cart, gift card and blog sections (group 80: commerce). Imported by build_sections.py.

Page CSS: theme/css/80-commerce.css, written by tools/theme/css_commerce.py from the
approved pages' <style> blocks, each scoped to its section wrapper class (.lgc-cart,
.lgc-gc, .lgc-blog, .lgc-art) so nothing leaks into the header, footer or other pages.
"""
from common import section, text, textarea, rich, url, img, check, select, number, product, header, para

S = {}

ICONS = [(x, x) for x in ["truck", "rotate-ccw", "shield-check", "package", "credit-card", "star", "badge-check", "tag", "hand-coins", "message-circle", "mail"]]

# ---------------------------------------------------------------- the cart page
S["lg-cart"] = section("Cart page", r"""
{%- assign s = section.settings -%}
<div class="lgc-cart">
<nav class="crumb lg-wrap" aria-label="Breadcrumb"><ol><li><a href="{{ routes.root_url }}">Home</a></li><li><span aria-current="page">{{ s.crumb }}</span></li></ol></nav>

<section class="lg-sec" style="padding-top:clamp(16px,2vw,24px)"><div class="lg-wrap">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d1' %}

  <div class="cart" style="margin-top:clamp(24px,3vw,40px)">
    <div>
      <div id="lines" aria-live="polite"></div>
      <div class="empty" id="empty"{% if cart.item_count > 0 %} hidden{% endif %}>
        {% render 'lg-mags' %}
        <p class="lg-lede" style="margin-bottom:20px">{{ s.empty_text }}</p>
        {%- if s.empty_btn != blank %}<a class="lg-btn" href="{{ s.empty_url }}">{{ s.empty_btn }}</a>{% endif -%}
        {%- if s.empty_btn2 != blank %}<a class="lg-btn-line" href="{{ s.empty_url2 }}" style="margin-left:10px">{{ s.empty_btn2 }}</a>{% endif -%}
      </div>
      {%- if section.blocks.size > 0 -%}
      <div class="trust">
        {%- for block in section.blocks -%}<div {{ block.shopify_attributes }}>{% render 'lg-icon', name: block.settings.icon %}<div><b>{{ block.settings.title }}</b><p>{{ block.settings.text }}</p></div></div>{%- endfor -%}
      </div>
      {%- endif -%}
    </div>

    <aside class="sum" aria-label="Order summary">
      <div class="ship"><p id="say"></p><div class="lg-hole" id="hole"></div></div>
      <div class="row"><span>Subtotal</span><span id="sub">{{ cart.total_price | money_without_trailing_zeros }}</span></div>
      <div class="row"><span>Shipping</span><span id="shipline">Calculated at checkout</span></div>
      <div class="row big"><span>Total</span><span id="tot">{{ cart.total_price | money_without_trailing_zeros }}</span></div>
      <form action="{{ routes.cart_url }}" method="post" id="cart-go" novalidate>
      {%- if s.show_note -%}
      <details class="cnote"{% if cart.note != blank %} open{% endif %}><summary>{{ s.note_label }}</summary>
        <label class="sr" for="cart-note">{{ s.note_label }}</label>
        <textarea id="cart-note" name="note" maxlength="500" placeholder="{{ s.note_placeholder | escape }}">{{ cart.note }}</textarea></details>
      {%- endif -%}
      <button class="lg-btn" id="go" type="submit" name="checkout" aria-disabled="{% if cart.item_count == 0 %}true{% else %}false{% endif %}">{{ s.checkout_label }}</button>
      </form>
      {%- if s.note != blank %}<p class="note">{{ s.note }}</p>{% endif -%}
    </aside>
  </div>
</div></section>
</div>

<script type="application/json" id="lgc-cart-data">{{ cart | json }}</script>
<script>
document.addEventListener('DOMContentLoaded', function(){
  var $ = function(s){ return document.querySelector(s); };
  var FREE = +((window.LG || {}).freeShipping) || 198, hole = null, COVER = 'free-returns-package-protection';
  var money = function(c){ var n = c / 100; return '$' + (c % 100 ? n.toFixed(2) : Math.round(n)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var pic = function(u){ return u ? u + (u.indexOf('?') > -1 ? '&' : '?') + 'width=260' : ''; };
  function paint(c){
    var lines = c.items || [], goods = lines.filter(function(l){ return l.handle !== COVER; });
    var t = goods.reduce(function(a, l){ return a + l.final_line_price; }, 0);
    $('#empty').hidden = !!goods.length;
    $('#lines').innerHTML = !goods.length ? '' : goods.concat(lines.filter(function(l){ return l.handle === COVER; })).map(function(l){
      if (l.handle === COVER) return '<div class="ln is-cover"><span><b>' + esc(l.product_title) + '</b><span class="cv">Free returns and lost-package cover</span></span>'
        + '<span class="pr">' + money(l.final_line_price) + '<button type="button" class="rm" data-rm="' + esc(l.key) + '">Remove</button></span></div>';
      var opts = (l.options_with_values || []).filter(function(o){ return o.value !== 'Default Title'; }).map(function(o){ return o.value; });
      var props = l.properties ? Object.keys(l.properties).filter(function(k){ return k.charAt(0) !== '_' && l.properties[k]; }).map(function(k){ return l.properties[k]; }) : [];
      var hud = opts.concat(props);
      return '<div class="ln"><a class="ph" href="' + esc(l.url) + '">' + (l.image ? '<img src="' + esc(pic(l.image)) + '" alt="">' : '') + '</a>'
        + '<span><a class="nm" href="' + esc(l.url) + '"><b>' + esc(l.product_title) + '</b></a>'
        + (hud.length ? '<span class="lg-hud">' + hud.map(function(h){ return '<span>' + esc(h) + '</span>'; }).join('') + '</span>' : '')
        + '<span class="cd-qty"><button type="button" data-qty="' + esc(l.key) + '" data-to="' + (l.quantity - 1) + '" aria-label="One fewer">&minus;</button><span>' + l.quantity + '</span><button type="button" data-qty="' + esc(l.key) + '" data-to="' + (l.quantity + 1) + '" aria-label="One more">+</button></span>'
        + '</span><span class="pr">' + money(l.final_line_price) + (l.original_line_price > l.final_line_price ? '<s>' + money(l.original_line_price) + '</s>' : '')
        + '<button type="button" class="rm" data-rm="' + esc(l.key) + '">Remove</button></span></div>';
    }).join('');
    $('#say').innerHTML = !goods.length ? '' : t >= FREE * 100 ? "<b>Shipping's on us.</b>" : '<b>' + money(FREE * 100 - t) + "</b> more and shipping's on us.";
    $('#shipline').textContent = goods.length && t >= FREE * 100 ? 'Free' : 'Calculated at checkout';
    if (!hole && window.Lucky && Lucky.hole) hole = Lucky.hole($('#hole'), { stops: [{ at: FREE, label: 'Free shipping ' + money(FREE * 100) }] });
    if (hole) hole.set(t / 100);
    $('#sub').textContent = money(c.total_price || 0);
    $('#tot').textContent = money(c.total_price || 0);
    $('#go').setAttribute('aria-disabled', String(!goods.length));
  }
  try { paint(JSON.parse($('#lgc-cart-data').textContent)); } catch (e) {}
  if (window.LuckyBag) LuckyBag.onChange(function(c){ if (c && c.token) paint(c); });
  /* checkout is Shopify's own form (POST /cart, name="checkout"), so apps that hook [name="checkout"] keep working */
  document.addEventListener('submit', function(e){
    if (e.target.id !== 'cart-go' || $('#go').getAttribute('aria-disabled') !== 'true') return;
    e.preventDefault(); var el = $('#empty'); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
});
</script>
""", [
    text("crumb", "Breadcrumb", "Your bag"), text("eyebrow", "Eyebrow", "Your bag"),
    rich("heading", "Heading (italic = gold word)", "What you're taking to the <em>course</em>"),
    header("Empty bag"), text("empty_text", "Line", "Nothing in here yet."),
    text("empty_btn", "Gold button", "See the clubs"), url("empty_url", "Gold button link"),
    text("empty_btn2", "Second button", "Shop the polos"), url("empty_url2", "Second button link"),
    header("Summary"), text("checkout_label", "Checkout button", "Check out"),
    textarea("note", "Line under the button", "Tax is added at checkout, and nothing's charged until you place the order."),
    check("show_note", "Let them leave an order note", False), text("note_label", "Order note label", "Add a note to your order"),
    text("note_placeholder", "Order note placeholder", "Anything we should know?"),
    para("The free-shipping bar reads the threshold in Theme settings. The Loop coverage line shows as a small line, never a card."),
], blocks=[("trust", "Trust item", [select("icon", "Icon", ICONS, "truck"), text("title", "Title"), text("text", "Line")])], max_blocks=3)

# ---------------------------------------------------------------- the gift card
S["lg-giftcard"] = section("Gift card buy box", r"""
{%- liquid
  assign s = section.settings
  assign pick = product.selected_or_first_available_variant
  assign want = s.default_amount | times: 100
  for v in product.variants
    if v.price == want and v.available
      assign pick = v
    endif
  endfor
  if product.selected_variant
    assign pick = product.selected_variant
  endif
  assign amt = pick.price | money_without_trailing_zeros
-%}
<div class="lgc-gc">
<nav class="crumb lg-wrap" aria-label="Breadcrumb"><ol><li><a href="{{ routes.root_url }}">Home</a></li><li><span aria-current="page">{{ s.crumb }}</span></li></ol></nav>

<section class="lg-sec" style="padding-top:clamp(12px,2vw,20px)"><div class="lg-wrap pdp">
  <div class="stage">
    <div class="gc" aria-label="Lucky gift card preview">
      <span class="lg-logo" style="position:relative;z-index:1">{% render 'lg-logo' %}</span>
      <span class="amt" data-card-amt>{{ amt }}</span>
      <span class="ln"><span>{{ s.card_left }}</span><span>{{ s.card_right }}</span></span>
    </div>
  </div>

  <div class="buy" id="send">
    {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
    {%- if s.heading != blank -%}{% render 'lg-h', text: s.heading, tag: 'h1', cls: 'lg-d2' %}{%- else -%}<h1 class="lg-d2">{{ product.title }}</h1>{%- endif -%}
    <p class="price" data-price>{{ amt }}</p>
    {%- if s.body != blank %}<p class="lg-body">{{ s.body }}</p>{% endif -%}

    {%- form 'product', product, id: 'gc-form', novalidate: 'novalidate', data-lg-add: '' -%}
      <input type="hidden" name="id" value="{{ pick.id }}" data-gc-id>
      <div class="row"><span class="lg-label">{{ s.amount_label }}</span></div>
      <div class="lg-chips" data-amts role="group" aria-label="{{ s.amount_label | escape }}">
        {%- for v in product.variants -%}<button class="lg-chip" type="button" data-v="{{ v.id }}" data-a="{{ v.price | money_without_trailing_zeros }}" aria-pressed="{% if v.id == pick.id %}true{% else %}false{% endif %}"{% unless v.available %} disabled{% endunless %}>{{ v.price | money_without_trailing_zeros }}</button>{%- endfor -%}
      </div>

      <div class="row"><span class="lg-label">{{ s.who_label }}</span></div>
      <div class="who" role="group" aria-label="{{ s.who_label | escape }}">
        <button type="button" data-who="me" aria-pressed="false"><b>{{ s.me_title }}</b><span>{{ s.me_line }}</span></button>
        <button type="button" data-who="them" aria-pressed="true"><b>{{ s.them_title }}</b><span>{{ s.them_line }}</span></button>
      </div>
      <div class="to" data-to>
        <input type="hidden" name="properties[__shopify_send_gift_card_to_recipient]" value="on" data-rcp>
        <input type="hidden" name="properties[__shopify_offset]" value="" data-rcp data-offset>
        <label><span class="lb">{{ s.name_label }}</span><input name="properties[Recipient name]" maxlength="255" autocomplete="off" data-rcp></label>
        <label><span class="lb">{{ s.email_label }}</span><input type="email" name="properties[Recipient email]" autocomplete="off" required data-rcp></label>
        <label><span class="lb">{{ s.msg_label }}</span><textarea name="properties[Message]" maxlength="200" placeholder="{{ s.msg_placeholder | escape }}" data-rcp></textarea></label>
        <label><span class="lb">{{ s.date_label }}</span><input type="date" name="properties[Send on]" data-rcp data-send-on></label>
      </div>

      <button class="lg-btn" type="submit" data-atc>{{ s.btn_label }} · {{ amt }}</button>
    {%- endform -%}
    {%- if s.fine != blank %}<p class="fine">{{ s.fine }}</p>{% endif -%}
  </div>
</div></section>
</div>
<script>
document.addEventListener('DOMContentLoaded', function(){
  var f = document.getElementById('gc-form'); if (!f) return;
  var $ = function(s){ return f.closest('.lgc-gc').querySelector(s); };
  var $$ = function(s){ return [].slice.call(f.closest('.lgc-gc').querySelectorAll(s)); };
  var label = {{ section.settings.btn_label | json }};
  var off = $('[data-offset]'); if (off) off.value = new Date().getTimezoneOffset();
  var d = $('[data-send-on]');
  if (d){ var iso = function(t){ return new Date(t - new Date(t).getTimezoneOffset() * 60000).toISOString().slice(0, 10); };
    d.min = iso(Date.now()); d.max = iso(Date.now() + 90 * 864e5); }
  function amt(b){
    $$('[data-amts] button').forEach(function(x){ x.setAttribute('aria-pressed', String(x === b)); });
    $('[data-gc-id]').value = b.getAttribute('data-v');
    $('[data-card-amt]').textContent = b.getAttribute('data-a');
    $('[data-price]').textContent = b.getAttribute('data-a');
    $('[data-atc]').textContent = label + ' · ' + b.getAttribute('data-a');
  }
  f.addEventListener('click', function(e){
    var a = e.target.closest('[data-amts] button'); if (a){ amt(a); return; }
    var w = e.target.closest('[data-who]');
    if (w){ $$('[data-who]').forEach(function(x){ x.setAttribute('aria-pressed', String(x === w)); });
      var me = w.getAttribute('data-who') === 'me';
      $('[data-to]').hidden = me;
      $$('[data-rcp]').forEach(function(i){ i.disabled = me; }); }
  });
  /* the recipient's email is the one thing Shopify needs; check it before the bag does */
  f.addEventListener('submit', function(e){
    var em = f.querySelector('[name="properties[Recipient email]"]');
    if (em && !em.disabled && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em.value)){ e.preventDefault(); e.stopImmediatePropagation(); em.focus(); if (window.Lucky && Lucky.toast) Lucky.toast('Add their email and we will send it to them.'); }
  }, true);
});
</script>
""", [
    text("crumb", "Breadcrumb", "Gift card"), text("eyebrow", "Eyebrow", "Gift card"),
    rich("heading", "Heading (italic = gold word; empty = product title)"),
    textarea("body", "Line under the price"),
    number("default_amount", "Amount picked first ($)", 50),
    text("card_left", "Card, bottom left", "Gift card"), text("card_right", "Card, bottom right", "It's better to be lucky"),
    text("amount_label", "Amount label", "Amount"), text("who_label", "Who label", "Who it's for"),
    text("me_title", "Me: title", "Me"), text("me_line", "Me: line", "It comes to my email"),
    text("them_title", "Someone else: title", "Someone else"), text("them_line", "Someone else: line", "We email them"),
    text("name_label", "Their name label", "Their name"), text("email_label", "Their email label", "Their email"),
    text("msg_label", "Note label", "A note from you"), text("msg_placeholder", "Note placeholder"),
    text("date_label", "Send on label", "Send it on"),
    text("btn_label", "Button", "Add to cart"), textarea("fine", "Small print under the button"),
    para("Amounts are the product's variants. The recipient fields are Shopify's own gift card recipient fields: Shopify emails the card on the date picked (up to 90 days out)."),
])

S["lg-qa"] = section("Answers beside heading", r"""
{%- assign s = section.settings -%}
<div class="lgc-gc"><section class="lg-sec"><div class="lg-wrap qa">
  <div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div>
  <div class="lg-faq">
    {%- for block in section.blocks -%}<details class="lg-fq"{% if forloop.first %} open{% endif %} {{ block.shopify_attributes }}><summary>{{ block.settings.q }}</summary><div class="lg-fq-a">{{ block.settings.a }}</div></details>{%- endfor -%}
  </div>
</div></section></div>
""", [text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)")],
    blocks=[("qa", "Question", [text("q", "Question"), {"type": "richtext", "id": "a", "label": "Answer"}])])

S["lg-picks"] = section("Four product picks", r"""
{%- assign s = section.settings -%}
<div class="lgc-gc"><section class="lg-sec" style="padding-top:0"><div class="lg-wrap">
  <div class="pick-hd">
    <div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div>
    {%- if s.link_label != blank %}<a class="lg-link" href="{{ s.link_url }}">{{ s.link_label }} <span>&rarr;</span></a>{% endif -%}
  </div>
  <div class="pick">
    {%- for block in section.blocks -%}{%- assign p = block.settings.product -%}{%- if p != blank -%}
      {%- liquid
        assign pic = block.settings.image
        if pic == blank
          assign pic = p.metafields.custom.cutout.value
        endif
        if pic == blank
          assign pic = p.featured_image
        endif
        assign nm = block.settings.name | default: p.title
      -%}
      <a href="{{ p.url }}" {{ block.shopify_attributes }}><span class="ph">{%- if pic != blank -%}{{ pic | image_url: width: 600 | image_tag: loading: 'lazy', alt: nm, widths: '300,450,600', sizes: '(max-width: 860px) 45vw, 22vw' }}{%- endif -%}</span>
        <span class="nm">{{ nm }}</span><b>{{ p.price_min | money_without_trailing_zeros }}{% if p.price_varies %} to {{ p.price_max | money_without_trailing_zeros }}{% endif %}</b>{% unless p.available %} <span class="lg-aside">Sold out</span>{% endunless %}</a>
    {%- endif -%}{%- endfor -%}
  </div>
</div></section></div>
""", [text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"), text("link_label", "Link on the right"), url("link_url", "Link URL")],
    blocks=[("pick", "Product", [product("product", "Product"), text("name", "Name (empty = product's)"), img("image", "Photo (empty = the product's cutout)")])], max_blocks=8)

# ---------------------------------------------------------------- the blog
S["lg-blog"] = section("Blog posts", r"""
{%- assign s = section.settings -%}
<div class="lgc-blog"><section class="lg-wrap" style="padding-top:clamp(28px,4vw,48px)">
{%- paginate blog.articles by 24 -%}
  {%- liquid
    assign lead = s.lead
    if lead == blank or lead.handle == blank
      assign lead = blog.articles.first
    endif
    if paginate.current_page > 1
      assign lead = nil
    endif
  -%}
  {%- if lead -%}
  <a class="lead" href="{{ lead.url }}">
    <figure>{%- if lead.image -%}{{ lead.image | image_url: width: 1400 | image_tag: alt: lead.title, widths: '600,900,1200,1400', sizes: '(max-width: 900px) 100vw, 55vw' }}{%- else -%}<span class="noimg">Lucky</span>{%- endif -%}</figure>
    <div>{%- if s.lead_eyebrow != blank %}<p class="lg-eyebrow">{{ s.lead_eyebrow }}</p>{% endif -%}<h2 class="lg-d2">{{ lead.title }}</h2>
      {%- assign ex = lead.excerpt | strip_html | strip -%}{%- if ex != blank %}<p class="lg-body">{{ ex }}</p>{% endif -%}
      {%- if lead.published_at %}<p class="meta" style="margin-top:14px">{{ lead.published_at | date: '%B %-d, %Y' }}</p>{% endif -%}
      <span class="lg-link" style="margin-top:10px;display:inline-block">{{ s.read_label }} <span>&rarr;</span></span></div></a>
  {%- endif -%}
  <div class="grid">
    {%- for a in blog.articles -%}{%- if lead and a.id == lead.id %}{% continue %}{% endif -%}
      <a class="post" href="{{ a.url }}">
        {%- if a.image -%}<figure>{{ a.image | image_url: width: 900 | image_tag: loading: 'lazy', alt: a.title, widths: '450,700,900', sizes: '(max-width: 680px) 100vw, (max-width: 1000px) 50vw, 33vw' }}</figure>{%- else -%}<figure><span class="noimg">Lucky</span></figure>{%- endif -%}
        <h3>{{ a.title }}</h3>
        {%- assign ex = a.excerpt | strip_html | strip -%}{%- if ex != blank %}<p>{{ ex | truncatewords: 30 }}</p>{% endif -%}
        {%- if a.published_at %}<p class="meta" style="margin-top:10px">{{ a.published_at | date: '%B %-d, %Y' }}</p>{% endif -%}
      </a>
    {%- endfor -%}
  </div>
  {%- if paginate.pages > 1 -%}<nav class="pages" aria-label="More articles">{{ paginate | default_pagination: next: 'Older', previous: 'Newer' }}</nav>{%- endif -%}
{%- endpaginate -%}
</section></div>
""", [{"type": "article", "id": "lead", "label": "Article to lead with (empty = newest)"},
      text("lead_eyebrow", "Lead eyebrow", "Latest"), text("read_label", "Read link", "Read it"),
      para("The rest are every article on this blog, newest first. The line under each title is the article's excerpt.")])

S["lg-news"] = section("Newsletter signup", r"""
{%- assign s = section.settings -%}
<div class="lgc-blog"><section class="lg-sec"{% if s.no_top %} style="padding-top:0"{% endif %}><div class="lg-wrap sub">
  <div>
    {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
    {% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}
    {%- if s.body != blank %}<p class="lg-body">{{ s.body }}</p>{% endif -%}
  </div>
  <form class="lg-form" data-news data-source="{{ s.source | escape }}"{% if s.list != blank %} data-list="{{ s.list | escape }}"{% endif %} novalidate>
    <label class="sr" for="news-{{ section.id }}">Email</label>
    <input class="lg-input" id="news-{{ section.id }}" type="email" placeholder="{{ s.placeholder | escape }}" autocomplete="email" required>
    <button class="lg-btn" type="submit">{{ s.btn_label }}</button>
  </form>
</div></section></div>
""", [text("eyebrow", "Eyebrow", "First look"), rich("heading", "Heading (italic = gold word)", "Get the next one in your <em>inbox</em>"),
      textarea("body", "Line under it"), text("placeholder", "Email placeholder", "you@somewhere.com"), text("btn_label", "Button", "Sign me up"),
      text("list", "Klaviyo list ID (empty = the one in Theme settings)"), text("source", "Source name in Klaviyo", "Blog"),
      check("no_top", "No space above", True)])

# ---------------------------------------------------------------- the article
S["lg-article"] = section("Article", r"""
{%- liquid
  assign s = section.settings
  assign h1 = article.metafields.lucky.h1.value | default: article.title
  assign lede = article.metafields.lucky.lede.value
  assign crumb = article.metafields.lucky.crumb.value | default: article.title
-%}
<div class="lgc-art">
<nav class="crumb lg-wrap" aria-label="Breadcrumb"><ol><li><a href="{{ routes.root_url }}">Home</a></li><li><a href="{{ blog.url }}">{{ blog.title }}</a></li><li><span aria-current="page">{{ crumb }}</span></li></ol></nav>

<article class="lg-sec" style="padding-top:clamp(12px,2vw,20px)"><div class="lg-wrap">
  <div class="art">
    {%- if article.published_at %}<p class="meta"><span>{{ article.published_at | date: '%B %-d, %Y' }}</span></p>{% endif %}
    {% render 'lg-h', text: h1, tag: 'h1', cls: 'lg-d1' %}
    {%- if lede != blank %}<p class="lg-lede">{{ lede }}</p>{% endif %}
  </div>
  {%- if article.image -%}
  <figure class="hero">{{ article.image | image_url: width: 2000 | image_tag: alt: article.image.alt, fetchpriority: 'high', loading: 'eager', widths: '750,1100,1500,2000', sizes: '(max-width: 1200px) 100vw, 1200px' }}</figure>
  {%- endif -%}
  <div class="art rte">
    {{ article.content }}
  </div>
</div></article>
</div>
""", [para("Title, date, photo and text come from the article. Optional article metafields (set by tools/theme/publish_articles.py): lucky.h1 (heading with the gold word), lucky.lede, lucky.crumb, lucky.signoff.")])

S["lg-article-more"] = section("More articles", r"""
{%- liquid
  assign s = section.settings
  assign found = false
  assign after = ''
  assign before = ''
  for a in blog.articles
    if a.id == article.id
      assign found = true
      continue
    endif
    if found
      assign after = after | append: a.handle | append: ','
    else
      assign before = before | append: a.handle | append: ','
    endif
  endfor
  assign order = after | append: before | split: ','
  assign shown = 0
-%}
<div class="lgc-art"><section class="lg-sec" style="padding-top:0"><div class="lg-wrap">
  <div style="display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:16px 40px;margin-bottom:clamp(20px,3vw,32px)">
    <div>{%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}{% render 'lg-h', text: s.heading, tag: 'h2', cls: 'lg-d2' %}</div>
    {%- if s.link_label != blank %}<a class="lg-link" href="{{ blog.url }}">{{ s.link_label }} <span>&rarr;</span></a>{% endif -%}
  </div>
  <div class="more">
    {%- for h in order -%}{%- if shown >= 3 %}{% break %}{% endif -%}
      {%- for a in blog.articles -%}{%- if a.handle == h -%}
        <a class="mp" href="{{ a.url }}"><figure>{%- if a.image -%}{{ a.image | image_url: width: 800 | image_tag: loading: 'lazy', alt: '', widths: '400,600,800', sizes: '(max-width: 860px) 100vw, 33vw' }}{%- endif -%}</figure><b>{{ a.title }}</b></a>
        {%- assign shown = shown | plus: 1 -%}
      {%- endif -%}{%- endfor -%}
    {%- endfor -%}
  </div>
</div></section></div>
""", [text("eyebrow", "Eyebrow", "Keep reading"), rich("heading", "Heading (italic = gold word)", "More from the <em>blog</em>"), text("link_label", "Link on the right", "All articles")])

S["lg-article-signoff"] = section("Sign-off, no arrow", r"""
{%- liquid
  assign s = section.settings
  assign so = article.metafields.lucky.signoff.value
  assign h = so.h | default: s.heading
  assign lede = so.lede | default: s.lede
  assign btn = so.btn | default: s.btn_label
  assign href = so.href | default: s.btn_url
-%}
<section class="lg-signoff"><div class="lg-wrap">
  {%- if s.eyebrow != blank %}<p class="lg-eyebrow">{{ s.eyebrow }}</p>{% endif -%}
  {% render 'lg-h', text: h, tag: 'h2', cls: 'lg-d1' %}
  {%- if lede != blank %}<p class="lg-lede">{{ lede }}</p>{% endif -%}
  {%- if btn != blank %}<a class="lg-btn" href="{{ href }}">{{ btn }}</a>{% endif -%}
  <div class="lg-signoff-mags" aria-hidden="true">{% render 'lg-mags' %}</div>
</div></section>
""", [text("eyebrow", "Eyebrow", "The last word"),
      rich("heading", "Heading when the article has none (italic = gold word)", "It's better to be <em>lucky.</em>"),
      text("lede", "Line when the article has none", "Sixty days to make up your mind on the clubs, thirty on the rest."),
      text("btn_label", "Button when the article has none", "See the clubs"), url("btn_url", "Button link"),
      para("Each article can carry its own sign-off in the metafield lucky.signoff (JSON: h, lede, btn, href).")])
