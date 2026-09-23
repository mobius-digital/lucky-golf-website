"""
v9: the approved pages rebuilt on design system v4 (lucky.css + lucky.js),
with a review board: page switcher, desktop/tablet/phone, Before/After.

    python v9/tools/build.py        -> v9/out/  (index.html = the board)

Before = the approved page on the Lucky Colour System board (v8/out, shown
with ?sys=b, Deep Green & Gold, the system Cole picked).
After  = v9/src/<page>.html on shopify/assets/lucky.css + lucky.js, copied
         untouched, so the board shows the real system code.
Nothing is pushed to Shopify. Prices, stock and reviews come from _src/data.
"""
import json
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
V9 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V9, ".."))
SRC = os.path.join(V9, "src")
OUT = os.path.join(V9, "out")
AFTER = os.path.join(OUT, "after")
BEFORE = os.path.join(OUT, "before")
V8OUT = os.path.join(ROOT, "v8", "out")

# pages in board order; "built" flips on as each one is rebuilt
PAGES = [
    {"key": "carver", "name": "Carver 02", "file": "carver.html", "before": "carver.html", "built": True},
    {"key": "home", "name": "Home", "file": "home.html", "before": "home.html", "built": True},
    {"key": "clubs", "name": "Clubs", "file": "clubs.html", "before": "clubs.html", "built": True},
    {"key": "polos", "name": "Polos", "file": "polos.html", "before": "polos.html", "built": True},
    {"key": "polo", "name": "Polo product", "file": "polo-azalea.html", "before": "20-product-polo-azalea.html", "built": True},
    {"key": "hats", "name": "Hats", "file": "hats.html", "before": None, "built": True},
    {"key": "story", "name": "Our story", "file": "story.html", "before": None, "built": True},
    {"key": "faq", "name": "Questions", "file": "faq.html", "before": None, "built": True},
    {"key": "trybe", "name": "Ambassadors", "file": "trybe.html", "before": None, "built": True},
    {"key": "cart", "name": "Cart", "file": "cart.html", "before": None, "built": True},
    {"key": "search", "name": "Search", "file": "search.html", "before": None, "built": True},
    {"key": "404", "name": "404", "file": "404.html", "before": None, "built": True},
    {"key": "black", "name": "Carver Black", "file": "black.html", "before": None, "built": True},
    {"key": "blade", "name": "Eclipse Blade", "file": "blade.html", "before": None, "built": True},
    {"key": "mallet", "name": "Eclipse Mallet", "file": "mallet.html", "before": None, "built": True},
    {"key": "stryker", "name": "Stryker", "file": "stryker.html", "before": None, "built": True},
    {"key": "gear", "name": "Gear", "file": "gear.html", "before": None, "built": True},
    {"key": "hat", "name": "Hat product", "file": "hat-white-gold-classic.html", "before": None, "built": True},
    {"key": "collection", "name": "Collection (any)", "file": "collection-all.html", "before": None, "built": True},
    {"key": "gearpdp", "name": "Gear product", "file": "gear-grip-clover-black.html", "before": None, "built": True},
    {"key": "community", "name": "Community", "file": "community.html", "before": None, "built": True},
    {"key": "reviews", "name": "All reviews", "file": "reviews.html", "before": None, "built": True},
    {"key": "giftcard", "name": "Gift card", "file": "giftcard.html", "before": None, "built": True},
    {"key": "account", "name": "Account", "file": "account.html", "before": None, "built": True},
    {"key": "policy", "name": "Policy", "file": "policy.html", "before": None, "built": True},
    {"key": "blog", "name": "Blog", "file": "blog.html", "before": None, "built": True},
    {"key": "article", "name": "Article", "file": "article.html", "before": None, "built": True},
]

# ------------------------------------------------------------------ images
IMG_SOURCES = [os.path.join(ROOT, "v9", "src"), os.path.join(ROOT, "design", "img", "shoot-0918"), os.path.join(V8OUT, "img"), os.path.join(ROOT, "design", "sg")]
EXTRA = {"lucky-contour-day.svg": os.path.join(ROOT, "shopify", "assets", "lucky-contour-day.svg"),
         "lucky-contour-tw.svg": os.path.join(ROOT, "shopify", "assets", "lucky-contour-tw.svg")}


def find_img(name):
    if name in EXTRA:
        return EXTRA[name]
    for d in IMG_SOURCES:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise SystemExit(f"missing image: {name}")


# ------------------------------------------------------------------ logo
_SPRITE = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf-8").read()
SYM = {m.group(1): (m.group(2), m.group(3)) for m in
       re.finditer(r'<symbol id="(lg-[\w-]+)" viewBox="([^"]+)"[^>]*>(.*?)</symbol>', _SPRITE, re.S)}


def logo(sid="lg-lucky", label="Lucky Golf"):
    vb, inner = SYM[sid]
    return f'<svg viewBox="{vb}" fill="currentColor" fill-rule="nonzero" role="img" aria-label="{label}">{inner}</svg>'


STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6L10 15l-5.4 3 1.2-6L1.3 7.8l6.1-.7z"/></svg>'
STARS5 = STAR * 5

MAGS = ('<span class="lg-mags"><img class="is-ink" src="img/{a}-ink.webp" alt=""><img class="is-light" src="img/{a}-light.webp" alt=""></span>')

# ------------------------------------------------------------------ chrome
# The menu. One structure feeds desktop (mega panel) and phone/tablet (sheet).
# Lines are Lucky copy (copy skill, 2026-09-18 pass), not spec labels.
NAV = [
    {"label": "Wedges", "title": "Wedges", "all": ("clubs.html#wedges", "All wedges"),
     "intro": "Forged, spin-happy, and priced without a tour contract baked in.",
     "photo": ("two-gold-wedges.webp", "Carver 02 Gold, on the fringe"),
     "items": [("carver.html", "Carver 02 Gold", "$99", "The one they ask about on the next tee.", "6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp"),
               ("black.html", "Carver 02 Black", "$109", "Same forged head, in the dark.", "6_cef3d6fc-8907-4866-b6aa-6301f8c614b5.webp")]},
    {"label": "Putters", "title": "Putters", "all": ("clubs.html#putters", "All putters"),
     "intro": "Fully milled, finished in gold, and priced like nobody's paying for a tour van.",
     "photo": ("from-the-cup.webp", "Eclipse, doing its job"),
     "items": [("blade.html", "Eclipse Blade", "$199", "For the stroke with a little arc in it.", "3_f3d878d3-a4bb-4cc9-82df-f68e8eec3f61.webp"),
               ("mallet.html", "Eclipse Mallet", "$229", "Soft off the face, gold all over.", "1_b00c01f0-8116-464a-a39c-08a6ebf82b6f.webp")]},
    {"label": "Hybrid", "title": "Hybrid", "all": ("clubs.html#hybrid", "See the hybrid"),
     "intro": "Titanium, 19 degrees, and a lot friendlier than the fairway wood you keep leaving in the bag.",
     "photo": ("11_0464f85e-ccad-487c-bb2a-1c0a5c7b673c.webp", "Stryker, sitting down"),
     "items": [("stryker.html", "Stryker", "$209", "High and easy from the rough.", "3_a032f79a-78ab-436e-81c9-eea7bb5f7f40.webp")]},
    {"label": "Apparel", "title": "Apparel", "all": ("polos.html", "Shop apparel"),
     "intro": "Polos that move when you swing and hats that say it for you. Thirty days to send them back, tags on.",
     "photo": ("fit-sunset.webp", "Nightshade polo, white hat"),
     "items": [("polos.html", "Polos", "$67", "Four-way stretch and UPF 50+, loud or quiet.", "GoldMirage1.webp"),
               ("hats.html", "Hats", "$29", "The line on the front does the talking.", "39.webp"),
               ("gear.html", "Gear", "From $9.95", "Covers, gloves, grips. The small stuff.", "DriverHeadCover1.webp")]},
]
SEARCH = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>'


def header():
    nav, mob = [], []
    for i, c in enumerate(NAV):
        cards = "".join(f'<a class="mt" href="{h}"><span class="mt-ph"><img src="img/{im}" alt="" loading="lazy"></span>'
                        f'<span class="mt-row"><span class="mt-nm">{n}</span><span class="mt-pr">{pr}</span></span><span class="mt-sub">{ln}</span></a>'
                        for h, n, pr, ln, im in c["items"])
        ph, cap = c["photo"]
        nav.append(f'<div class="nv"><button type="button" aria-expanded="false" aria-controls="mega-{i}">{c["label"]}</button>'
                   f'<div class="mega" id="mega-{i}"><div class="mega-in">'
                   f'<div class="mega-intro"><p class="lg-d3">{c["title"]}</p><p>{c["intro"]}</p><a class="lg-link" href="{c["all"][0]}">{c["all"][1]} <span>&rarr;</span></a></div>'
                   f'<div class="mega-cards">{cards}</div>'
                   f'<a class="mega-ph" href="{c["all"][0]}"><img src="img/{ph}" alt="" loading="lazy"><span>{cap}</span></a>'
                   f'</div></div></div>')
        mcards = "".join(f'<a class="mn-card" href="{h}"><span class="mn-ph"><img src="img/{im}" alt="" loading="lazy"></span>'
                         f'<span class="mn-row"><span class="mn-nm">{n}</span><span class="mn-pr">{pr}</span></span><span class="mn-sub">{ln}</span></a>'
                         for h, n, pr, ln, im in c["items"])
        mob.append(f'<details{" open" if i == 0 else ""}><summary>{c["label"]}</summary><p class="mn-intro">{c["intro"]}</p>'
                   f'<div class="mn-grid">{mcards}</div><a class="lg-link mn-all" href="{c["all"][0]}">{c["all"][1]} <span>&rarr;</span></a></details>')
    nav.append('<a href="story.html">Our Story</a>')
    mob.append('<a class="mn-link" href="story.html">Our Story <span aria-hidden="true">&rarr;</span></a>'
               '<a class="mn-photo" href="story.html"><img src="img/walk-off-green.webp" alt="" loading="lazy"><span>It\'s better to be lucky.</span></a>'
               '<div class="mn-foot"><a href="faq.html#shipping">Shipping</a><a href="faq.html#returns">Sixty-day returns</a><a href="contact.html">Contact</a><a href="faq.html">FAQ</a></div>')
    return f'''<div class="lg-tick"><div class="lg-tick-in">
  <a href="faq.html#returns"><b>Sixty days</b> to prove us wrong</a><a href="faq.html#shipping">Ships in 1 to 2 business days</a><a href="clubs.html#wedges">Forged, not cast</a>
</div></div>
<header class="lg-hdr">
  <div class="lg-hdr-in" style="position:relative">
    <a class="lg-logo" href="home.html" aria-label="Lucky Golf home">{logo()}</a>
    <nav class="lg-nav" aria-label="Primary">{"".join(nav)}</nav>
    <div class="lg-hdr-act">
      <a class="hdr-search" href="search.html" aria-label="Search">{SEARCH}</a>
      <button type="button" class="bagbtn" data-cart-open aria-label="Open bag">{MAGS.format(a="mags-bag")}<span class="n" data-n="0" aria-hidden="true">0</span></button>
      <button type="button" class="burger" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span><i></i><i></i><i></i></span></button>
    </div>
  </div>
  <nav class="mnav" id="mnav" aria-label="Menu">{"".join(mob)}</nav>
</header>'''


def footer():
    return f'''<footer class="lg-ftr"><div class="lg-wrap">
  <div class="ftr-news">
    <div><span class="lg-label">First look</span><p>New lofts, restocks and the odd bad idea, straight to your inbox.</p></div>
    <form class="lg-form" data-news novalidate><label class="sr" for="news-email">Email</label><input class="lg-input" id="news-email" type="email" placeholder="you@somewhere.com" autocomplete="email" required><button class="lg-btn-line" type="submit">Sign me up</button></form>
  </div>
  <div class="lg-ftr-in">
    <div class="ftr-brand"><a class="lg-logo" href="home.html" aria-label="Lucky Golf home">{logo()}</a><p>Clubs that play like the big names, without the tour contracts and the retail markup in the price.</p></div>
    <div><h3>Clubs</h3><ul><li><a href="carver.html">Carver 02 Gold</a></li><li><a href="black.html">Carver 02 Black</a></li><li><a href="blade.html">Eclipse Blade</a></li><li><a href="mallet.html">Eclipse Mallet</a></li><li><a href="stryker.html">Stryker</a></li></ul></div>
    <div><h3>Apparel</h3><ul><li><a href="polos.html">The Classic Polo</a></li><li><a href="polos.html">The Blade Polo</a></li><li><a href="hats.html">Hats</a></li><li><a href="gear.html">Gear</a></li></ul></div>
    <div><h3>Support</h3><ul><li><a href="faq.html#returns">Sixty-day returns</a></li><li><a href="faq.html#shipping">Shipping</a></li><li><a href="contact.html">Contact</a></li><li><a href="faq.html">FAQ</a></li><li><a href="reviews.html">Reviews</a></li><li><a href="community.html">Community</a></li><li><a href="giftcard.html">Gift cards</a></li><li><a href="story.html">Our Story</a></li></ul></div>
  </div>
  <div class="lg-ftr-base"><span>&copy; 2026 Lucky Golf</span><span>It's better to be lucky.</span></div>
</div></footer>'''


DRAWER = '''<div class="cd" id="cd" hidden role="dialog" aria-modal="true" aria-labelledby="cd-title">
  <div class="cd-bd" data-cart-close></div>
  <div class="cd-panel">
    <div class="cd-hd"><h2 class="lg-d3" id="cd-title">Your bag</h2><button type="button" class="cd-x" data-cart-close aria-label="Close bag">&times;</button></div>
    <div class="cd-ship"><p id="cd-say"></p><div class="lg-hole" id="cd-hole"></div></div>
    <div class="cd-body"><div id="cd-list"></div></div>
    <div class="cd-foot">
      <div class="cd-sub"><span>Subtotal</span><span id="cd-sub">$0</span></div>
      <p class="cd-note">Shipping and tax calculated at checkout</p>
      <a href="#" class="lg-btn lg-btn-block" id="cd-go">Check out <span aria-hidden="true">&rarr;</span></a>
      <p class="cd-mock">Preview only. No live checkout wired up.</p>
    </div>
  </div>
</div>'''

HEAD = '''<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="lucky.css">
<link rel="stylesheet" href="site.css">'''


def scripts():
    built = json.dumps([p["file"] for p in PAGES if p["built"]])
    return f'<script src="lucky.js"></script>\n<script>window.LG_BUILT={built};</script>\n<script src="site.js"></script>'


# ------------------------------------------------------------------ data
def product(pid):
    p = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))
    return [x for x in p["products"] if x["id"] == pid][0]


PRODUCTS = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))


def esc(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def reviews(pid):
    r = json.load(open(os.path.join(ROOT, "_src", "data", "reviews", pid + ".json"), encoding="utf-8"))
    return {"total": r["total"], "totals": r["totals"], "sample": r["sample"]}


REEL = [{"title": "Full swing from 100", "brief": "Ball tracked to the pin, reaction", "kind": "Creator reel"},
        {"title": "Greenside chip", "brief": "One hop and stop, shot from behind", "kind": "Customer clip"},
        {"title": "Bunker", "brief": "Sand spray, ball releasing to the hole", "kind": "Creator reel"},
        {"title": "The flop", "brief": "Face wide open, soft landing", "kind": "Customer clip"},
        {"title": "Face in sunlight", "brief": "Grooves and finish, slow pan", "kind": "Creator reel"},
        {"title": "Unboxing", "brief": "Out of the sleeve, first reaction", "kind": "Customer clip"}]


def js(o):
    return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")


def icon(name):
    """A Lucide icon (lucide-static 0.460.0, ISC), inlined from v9/src/icons."""
    svg = open(os.path.join(SRC, "icons", name + ".svg"), encoding="utf-8").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r'\s+', " ", svg).replace('class="lucide lucide-' + name + '"', 'class="ic" aria-hidden="true"')
    return svg


def fill(tpl, extra):
    tpl = re.sub(r"\{\{ICON:([a-z0-9-]+)\}\}", lambda m: icon(m.group(1)), tpl)
    base = {"HEAD": HEAD, "HEADER": header(), "FOOTER": footer(), "DRAWER": DRAWER, "SCRIPTS": scripts(), "STARS5": STARS5,
            # Cole owes us the handle; until then the button points at the profile page
            "IG": "https://www.instagram.com/luckygolfofficial/"}
    base.update(extra)
    for k, v in base.items():
        tpl = tpl.replace("{{" + k + "}}", v)
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", tpl)
    if left:
        raise SystemExit(f"unfilled tokens: {sorted(set(left))}")
    return tpl


def build_carver(finish="gold", mood=False):
    import build_wedge as bw
    return lambda: bw.build(SRC, fill, js, product, reviews, REEL, STARS5, finish, mood)


def build_home():
    """The in-the-wild rail is the Community wall: same posts, same order.
    Each tile opens that post on the wall (community.html?post=N)."""
    by_id = {p["id"]: p for p in PRODUCTS["products"]}
    wild = ""
    for i, (img, alt, cap, ids) in enumerate(COMMUNITY):
        first = by_id[ids[0]]["name"] + (f" +{len(ids) - 1}" if len(ids) > 1 else "")
        wild += (f'<a class="wild" href="community.html?post={i}"><img src="img/{img}" alt="{esc(alt)}" loading="lazy">'
                 f'<span class="who">@luckygolfofficial</span><span class="tag">{esc(first)}</span></a>')
    return fill(open(os.path.join(SRC, "home.html"), encoding="utf-8").read(), {"WILD": wild})


def build_clubs():
    return fill(open(os.path.join(SRC, "clubs.html"), encoding="utf-8").read(), {})


def polo_pid(x):
    return x["img"].split("/")[-1].replace("-pack.webp", "")


def build_polos():
    """Cards come from the approved page's own data: names, collars, colours,
    per-size SKUs and what is actually sold out. Nothing retyped."""
    P = json.load(open(os.path.join(SRC, "polos-data.json"), encoding="utf-8"))
    styles = [("collar", "classic", "Classic collar", "Three buttons, one placket", "polo-gold-dust-cut.webp"),
              ("collar", "blade", "Blade collar", "No buttons, nothing at your throat", "polo-swirl-cut.webp")]
    st = "".join(
        f'<button class="style" type="button" data-f="{f}" data-v="{v}" aria-pressed="false">'
        f'<span class="ph"><img src="img/{im}" alt="" loading="lazy"></span>'
        f'<span><b>{t}</b><span>{sub} · {sum(1 for x in P if x[f] == v)} polos</span></span></button>'
        for f, v, t, sub, im in styles)
    cards = []
    for i, x in enumerate(P):
        live = [z for z in x["sizes"] if z["ok"]]
        sizes = "".join(
            (f'<button type="button" data-size="{z["size"]}" data-sku="{z["sku"]}">{z["size"]}</button>' if z["ok"]
             else f'<button type="button" disabled aria-label="{z["size"]} sold out">{z["size"]}</button>')
            for z in x["sizes"])
        stock = x["stock"]
        cls = "stock" if stock.startswith("Every") else "stock few"
        cards.append(
            f'<article class="polo" data-collar="{x["collar"]}" data-colour="{x["colour"]}" data-name="{x["name"]}" '
            f'data-i="{i}" data-best="{rank(polo_pid(x))[0]}" data-new="{rank(polo_pid(x))[1]}" '
            f'data-full="{x["full"]}" data-img="{x["img"].replace("-pack", "-cut")}" data-sizes="{" ".join(z["size"] for z in live)}">'
            f'<div class="polo-ph"><a href="{polo_slug(x)}" tabindex="-1" aria-hidden="true">f<img src="{x["img"].replace("-pack", "-cut")}" alt="{x["full"]}" loading="lazy">f<img class="alt" src="{x["img"].replace("-pack", "-collar")}" alt="" loading="lazy"></a>'
            f'<button class="qa-open" type="button" aria-expanded="false" aria-label="Add a size of the {x["name"]}">+</button>'
            f'<div class="qa"><span>Add a size</span><div class="sizes">{sizes}</div></div></div>'
            f'<a class="polo-bd" href="{polo_slug(x)}"><span class="nm">{x["name"]}</span><b>$67</b>'
            f'<span class="meta">{"Blade" if x["collar"] == "blade" else "Classic"} collar</span>'
            f'<span class="{cls}">{stock}</span></a></article>')
    return fill(open(os.path.join(SRC, "polos.html"), encoding="utf-8").read(),
                {"STYLES": st, "CARDS": "".join(cards), "COUNT": str(len(P))})


HAT_STYLES = [("classic", "Classic"), ("ibtbl", "Better To Be Lucky"), ("updown", "Upside Down"), ("cursive", "Cursive")]
HAT_META = {   # style and colour family, read off the product name
    "hat-white-gold-classic": ("classic", "light"),
    "hat-white-ibtbl": ("ibtbl", "light"),
    "hat-cream-updown": ("updown", "light"),
    "hat-black-ibtbl": ("ibtbl", "dark"),
    "hat-tan-cursive": ("cursive", "light"),
    "hat-black-gold-classic": ("classic", "dark"),
    "hat-white-black-updown": ("updown", "light"),
    "hat-white-updown": ("updown", "light"),
    "hat-white-cursive": ("cursive", "light"),
    "hat-baby-blue-cursive": ("cursive", "colour"),
}


SEARCHABLE = [
    # what a shopper would actually type, per product, from the catalogue
    ("carver.html", "Carver 02 Gold", "$99", "Wedge", "gold-full-cut.webp", "wedge carver 02 gold 50 52 54 56 58 60 forged lob sand gap"),
    ("black.html", "Carver 02 Black", "$109", "Wedge", "black-cut.webp", "wedge carver 02 black 50 52 54 56 58 60 forged lob sand gap dark"),
    ("blade.html", "Eclipse Blade", "$199", "Putter", "blade-cut.webp", "putter tracer blade milled arc gold"),
    ("mallet.html", "Eclipse Mallet", "$229", "Putter", "mallet-full-cut.webp", "putter eclipse tracer mallet forgiving straight gold"),
    ("stryker.html", "Stryker", "$209", "Hybrid", "stryker-full-cut.webp", "hybrid stryker titanium 3 4 iron replacement gold"),
    ("polo-azalea.html", "Azalea Classic Polo", "$67", "Polo", "polo-azalea-cut.webp", "polo azalea classic collar floral green apparel shirt"),
    ("polos.html", "Blackout Blade Polo", "$67", "Polo", "polo-blackout-cut.webp", "polo blackout blade collar black apparel shirt"),
    ("polos.html", "Gold Dust Classic Polo", "$67", "Polo", "polo-gold-dust-cut.webp", "polo gold dust classic collar light apparel shirt"),
    ("polos.html", "Swirl Blade Polo", "$67", "Polo", "polo-swirl-cut.webp", "polo swirl blade collar light apparel shirt"),
    ("hats.html", "White | Gold Classic Hat", "$29", "Hat", "hat-white-gold-classic-cut.webp", "hat cap snapback white gold classic rope"),
    ("hats.html", "It's Better To Be Lucky Hat, black", "$29", "Hat", "hat-black-ibtbl-cut.webp", "hat cap snapback black better to be lucky rope"),
    ("hats.html", "Cream Upside Down Hat", "$29", "Hat", "hat-cream-updown-cut.webp", "hat cap snapback cream upside down rope"),
]


def build_search():
    res = "".join(
        f'<a class="r" href="{h}" data-k="{esc((nm + " " + kind + " " + keys).lower())}">'
        f'<span class="ph"><img src="img/{im}" alt="{esc(nm)}" loading="lazy"></span>'
        f'<span class="nm">{esc(nm)}</span><b>{pr}</b><span class="kind">{kind}</span></a>'
        for h, nm, pr, kind, im, keys in SEARCHABLE)
    return fill(open(os.path.join(SRC, "search.html"), encoding="utf-8").read(), {"RESULTS": res})


def build_club(key):
    import build_club as bc
    return lambda: bc.build(SRC, ROOT, fill, esc, js, STARS5, key)


def build_gear_product(pid):
    import build_simple as bs
    return lambda: bs.build(SRC, ROOT, fill, esc, js, pid)


def build_simple(name):
    return lambda: fill(open(os.path.join(SRC, name), encoding="utf-8").read(), {})


GEAR_GROUPS = [
    ("covers", "Head covers", "No club we sell ships with one, so if you want the putter protected in the bag, it starts here.",
     ["cover-blade", "cover-mallet", "cover-driver"]),
    ("grips", "Club grips", "The cheapest change in golf you can actually feel. Five colours, more than one size.",
     ["grip-clover-black", "grip-clover-green", "grip-clover-blue", "grip-clover-white", "grip-clover-pink"]),
    ("putter-grips", "Putter grips", "Oversized, for anyone whose hands get busy over a short one.",
     ["grip-putter-stock", "grip-putter-green", "grip-putter-clovers"]),
    ("glove", "Glove", "One glove, both hands, with the clover on the back of it.",
     ["glove-tour"]),
]


def build_gear():
    """Covers, grips and the glove, with real prices and real stock."""
    by_id = {p["id"]: p for p in PRODUCTS["products"]}
    out = ""
    for anchor, title, line, ids in GEAR_GROUPS:
        cards = ""
        for pid in ids:
            p = by_id[pid]
            v = list(p["variants"].values())[0]
            live = any(x["avail"] for x in p["variants"].values())
            img = f"img/gear-{pid}.webp"
            price = p["priceLabel"].replace("–", " to ")
            meta = ("More than one size" if " to " in price else "One size") if "grip" in pid else (
                "Sold out" if not live else "In stock")
            if not live:
                meta = "Sold out"
            # one variant: add straight from the card. More than one: the card takes
            # you to the page to pick, because adding "a grip" with no size is a guess
            multi = len(p["variants"]) > 1
            if not live:
                btn = '<button type="button" disabled>Sold out</button>'
            elif multi:
                btn = f'<a class="pick" href="gear-{pid}.html">Pick a size</a>' if "cover" not in pid else f'<a class="pick" href="gear-{pid}.html">Pick a hand</a>'
            else:
                btn = f'<button type="button">Add · {p["priceLabel"].split("–")[0]}</button>'
            cards += (f'<article class="it" data-name="{esc(p["name"])}" data-price="{p["price"]}" data-img="{img}" '
                      f'data-best="{rank(pid)[0]}" data-new="{rank(pid)[1]}" '
                      f'data-hud="{"Gear"}"{"" if live else " data-dead"}>'
                      f'<div class="it-ph"><a href="gear-{pid}.html" tabindex="-1" aria-hidden="true"><img src="{img}" alt="{esc(p["name"])}" loading="lazy"></a>'
                      f'<div class="qa">{btn}</div></div>'
                      f'<a class="it-bd" href="gear-{pid}.html"><span class="nm">{esc(p["name"])}</span><b>{price}</b>'
                      f'<span class="meta">{meta}</span></a></article>')
        out += (f'<section class="lg-sec grp" id="{anchor}" style="padding-top:clamp(28px,3vw,44px)"><div class="lg-wrap">'
                f'<div class="hd"><div><h2 class="lg-d2">{title}</h2><p>{line}</p></div></div>'
                f'<div class="grid">{cards}</div></div></section>')
    return fill(open(os.path.join(SRC, "gear.html"), encoding="utf-8").read(), {"GROUPS": out})


HAT_COPY = {
    "hat-white-gold-classic": "White with the wordmark in gold across the front and a rope to match. The one that goes with every polo in the rack, which is why it moves fastest.",
    "hat-white-ibtbl": "The line we put on everything, stitched across a white crown. If somebody asks what it means, you have already won the conversation.",
    "hat-cream-updown": "Cream, with the wordmark flipped. You will see people notice it a beat later than they expect to.",
    "hat-black-ibtbl": "Black, with the line in white. The version for golfers who want the joke without the brightness.",
    "hat-tan-cursive": "Cream with the script across the front and a dark rope. The softest thing we make, and it goes with the loud prints.",
    "hat-black-gold-classic": "Black with the wordmark in gold. Between runs at the moment, and it always goes first.",
    "hat-white-black-updown": "White crown, black brim, wordmark upside down. The most contrast in the row without going to a black hat.",
    "hat-white-updown": "All white, wordmark flipped. Clean from the front, and it keeps the sun off exactly the same.",
    "hat-white-cursive": "White with the script in black. The quietest hat here, and the easiest one to wear off the course.",
    "hat-baby-blue-cursive": "Mint, with the script tonal on the crown. One of one in the row: nothing else we make is this colour.",
}


def build_hat(pid):
    """One page per hat. Price, stock and the name come from the catalogue."""
    def run():
        hats = [p for p in PRODUCTS["products"] if p.get("family") == "hat"]
        me = [p for p in hats if p["id"] == pid][0]
        live = any(v["avail"] for v in me["variants"].values())
        sw = "".join(
            f'<a class="lg-swatch" href="{x["id"]}.html"{" aria-current=\"page\"" if x is me else ""} aria-label="{esc(x["name"])}">'
            f'<img src="img/{x["id"]}-cut.webp" alt="" loading="lazy"></a>' for x in hats)
        others = [x for x in hats if x is not me and any(v["avail"] for v in x["variants"].values())][:3]
        more = "".join(
            f'<a class="lg-card" href="{x["id"]}.html"><span class="lg-card-ph is-cut">'
            f'<img src="img/{x["id"]}-cut.webp" alt="" loading="lazy"></span><span class="lg-card-bd">'
            f'<span class="lg-card-nm">{esc(x["name"])}</span><span class="lg-card-pr">$29</span></span></a>'
            for x in others)
        more += ('<a class="lg-card" href="polo-azalea.html"><span class="lg-card-ph is-cut">'
                 '<img src="img/polo-azalea-cut.webp" alt="" loading="lazy"></span><span class="lg-card-bd">'
                 '<span class="lg-card-nm">Azalea Classic Polo</span><span class="lg-card-pr">$67</span></span></a>')
        return fill(open(os.path.join(SRC, "hat.html"), encoding="utf-8").read(), {
            "NAME": esc(me["name"]), "IMG": pid + "-cut.webp", "DESC": HAT_COPY[pid], "SWATCHES": sw, "MORE": more,
            "ATC": "Put it in the bag" if live else "Tell me when it’s back",
            "STOCK": "In stock · ships in 1 to 2 days" if live else "Sold out · between runs",
            "HAT_JSON": js({"name": me["name"], "img": pid + "-cut.webp", "live": live})})
    return run


ARTICLES = [
    # the real articles on the live blog, newest first (pulled 2026-09-20)
    ("Mastering your putt: the power of a well-crafted putting routine", "mastering-your-putt", "", "", ""),
    ("How to improve your golf game according to the pros", "how-to-improve", "12 May 2023", "art-scorecard.webp",
     "Golf is a challenging game, and also one of the most rewarding. A little practice, a little dedication, and some tips from people who do it for a living."),
    ("The top 10 golf shots you can hit using a wedge", "top-10-wedge-shots", "6 May 2023", "art-daniel-berger.webp",
     "If you want to take your game to the next level, start with the shots inside a hundred yards."),
    ("Are your wedges forged?", "are-your-wedges-forged", "3 May 2023", "art-forged-factory.webp",
     "Picking a wedge puts you in front of a choice nobody explains: forged or cast. It changes the feel, and it changes the price."),
    ("Golf is a mental game", "golf-is-a-mental-game", "27 April 2023", "art-mental-game.webp",
     "Focus, discipline and a confident mindset. The part of the game you cannot buy your way out of."),
    ("Why golf wedges are the most important club in your bag", "most-important-club", "19 November 2022", "art-most-important.webp",
     "You hit more shots inside a hundred yards than anywhere else on the course. Spend accordingly."),
    ("Golf.com proves why a lucky charm is necessary on the course", "lucky-charm", "16 June 2021", "art-lucky-charm.webp",
     "Somebody with a press pass finally said what we have been saying since 2018."),
    ("Why we have the best golf wedges for under $100", "best-under-100", "24 March 2021", "art-under-100.webp",
     "Same steel as the big names, none of the markup. Here is the maths."),
    ("MrShortGame reviews Lucky wedges", "mrshortgame-review", "8 October 2019", "art-mrshortgame.webp",
     "Somebody who tests wedges for a living put ours on camera."),
    ("Use your Lucky wedge to get out of a deep bunker lie", "deep-bunker-lie", "18 March 2019", "", ""),
    ("Using your Lucky wedge from the rough", "from-the-rough", "18 November 2018", "art-rough-tip.webp",
     "Extra weight and balance carry momentum through the shot, which is how you avoid the chili dip."),
    ("The dreaded chili dip", "chili-dip", "9 November 2018", "art-chili-dip.webp",
     "Everybody has hit one. Here is why it happens and the drill that stops it."),
    ("Welcome to Lucky", "welcome-to-lucky", "4 November 2018", "art-welcome.webp",
     "One gold wedge, built right, priced honestly. This is where it starts."),
]


def build_blog():
    """The blog index, built off the fourteen articles actually on the store."""
    lead = ARTICLES[3]   # the forged one is the piece worth leading with
    rest = [a for a in ARTICLES if a is not lead]
    lead_html = (
        f'<a class="lead" href="article.html">'
        f'<figure><img src="img/{lead[3]}" alt="{esc(lead[0])}" width="1024" height="1024"></figure>'
        f'<div><p class="lg-eyebrow">Latest</p><h2 class="lg-d2">{esc(lead[0])}</h2>'
        f'<p class="lg-body">{esc(lead[4])}</p>'
        f'<p class="meta" style="margin-top:14px">{lead[2]} · four minute read</p>'
        f'<span class="lg-link" style="margin-top:10px;display:inline-block">Read it <span>&rarr;</span></span></div></a>')
    posts = ""
    for title, slug, date, img, sub in rest:
        href = "article.html" if slug == "are-your-wedges-forged" else "blog.html"
        pic = (f'<figure><img src="img/{img}" alt="{esc(title)}" loading="lazy"></figure>' if img
               else '<figure><span class="noimg">Lucky</span></figure>')
        posts += (f'<a class="post" href="{href}">{pic}<h3>{esc(title)}</h3>'
                  + (f'<p>{esc(sub)}</p>' if sub else "")
                  + (f'<p class="meta" style="margin-top:10px">{date}</p>' if date else "") + "</a>")
    return fill(open(os.path.join(SRC, "blog.html"), encoding="utf-8").read(), {"LEAD": lead_html, "POSTS": posts})


def build_article():
    more = "".join(
        f'<a class="mp" href="blog.html"><figure><img src="img/{img}" alt="" loading="lazy"></figure>'
        f'<b>{esc(title)}</b></a>'
        for title, slug, date, img, sub in ARTICLES[4:7])
    return fill(open(os.path.join(SRC, "article.html"), encoding="utf-8").read(), {"MORE": more})


COLLECTIONS = {
    "all": {
        "title": "All Products", "eyebrow": "Everything we make",
        "lede": "Five clubs, thirteen polos, ten hats and the small stuff. One page, everything on it.",
        "signhead": "That is the whole <span class=\"lg-foil-word\">shop</span>",
        "signlede": "Sixty days on the clubs, thirty on everything else. Mags owns one of each and paid for none.",
        "families": None},
    "accessories": {
        "title": "Accessories", "eyebrow": "The small stuff",
        "lede": "Covers, grips and a glove. The cheap changes that make the bag feel like yours.",
        "signhead": "Ten dollars of <span class=\"lg-foil-word\">better</span>",
        "signlede": "A fresh grip is the cheapest thing in golf you can actually feel.",
        "families": ("headcover", "grip", "glove")},
}

KIND_LABEL = {"wedge": "Wedges", "putter": "Putters", "hybrid": "Hybrid", "polo-classic": "Polos",
              "polo-blade": "Polos", "hat": "Hats", "headcover": "Covers", "grip": "Grips", "glove": "Gloves"}
KIND_HREF = {"wedge": "clubs.html", "putter": "clubs.html", "hybrid": "clubs.html", "hat": "hats.html",
             "headcover": "gear.html", "grip": "gear.html", "glove": "gear.html"}


# Best-seller rank and age, read off the live store on 2026-09-20 (Shopify
# sortKey BEST_SELLING and CREATED). In the theme these come from Shopify
# itself; here they are baked so the sorts are real and not decoration.
BEST_RANK = {
    "lgp01-gold": 1, "lgp02-gold": 2, "cover-mallet": 3, "glove-tour": 4, "cover-blade": 5,
    "grip-clover-green": 6, "lgh01": 7, "grip-putter-clovers": 8, "cover-driver": 9,
    "grip-clover-white": 10, "lgw01-black": 11, "grip-putter-green": 12, "grip-clover-black": 13,
    "grip-clover-blue": 14, "lgw01-gold": 15, "polo-azalea": 16, "grip-clover-pink": 17,
    "polo-signature-black": 18, "polo-blackout": 19, "polo-gold-carnation": 20, "polo-shadow": 21,
    "grip-putter-stock": 22, "polo-cruiser": 23, "polo-gold-dust": 24, "polo-marble": 25,
    "polo-frost": 26, "polo-contour": 27, "polo-nightshade": 28, "polo-swirl": 29, "polo-spot": 30,
    "hat-white-black-updown": 31, "hat-tan-cursive": 32, "hat-white-gold-classic": 33,
    "hat-black-ibtbl": 34, "hat-baby-blue-cursive": 35, "hat-cream-updown": 36,
    "hat-black-gold-classic": 37, "hat-white-ibtbl": 38, "hat-white-cursive": 39, "hat-white-updown": 40,
}
NEWEST = {   # higher is newer
    "lgw01-gold": 100, "hat-baby-blue-cursive": 99, "hat-white-cursive": 98, "hat-white-updown": 97,
    "hat-white-black-updown": 96, "hat-black-gold-classic": 95, "hat-tan-cursive": 94,
    "hat-black-ibtbl": 93, "hat-cream-updown": 92, "hat-white-ibtbl": 91, "hat-white-gold-classic": 90,
    "lgw01-black": 89, "polo-nightshade": 80, "polo-azalea": 79, "polo-cruiser": 78, "polo-blackout": 77,
    "polo-spot": 76, "polo-swirl": 75, "polo-frost": 74, "polo-gold-carnation": 73, "polo-marble": 72,
    "polo-contour": 71, "polo-signature-black": 70, "polo-shadow": 69, "polo-gold-dust": 68,
    "lgh01": 60, "cover-mallet": 55, "grip-putter-stock": 54, "lgp02-gold": 50, "lgp01-gold": 45,
    "cover-driver": 40, "grip-clover-pink": 35, "grip-clover-blue": 34, "grip-clover-white": 33,
    "grip-clover-black": 32, "grip-putter-clovers": 30, "grip-putter-green": 29,
    "grip-clover-green": 25, "cover-blade": 20, "glove-tour": 15,
}


def rank(pid):
    return BEST_RANK.get(pid, 999), NEWEST.get(pid, 0)


def coll_img(p):
    """Whatever cutout we already made for this product."""
    fam = p.get("family")
    if fam == "hat":
        return p["id"] + "-cut.webp"
    if fam in ("polo-classic", "polo-blade"):
        return p["id"].replace("polo-", "polo-") + "-cut.webp"
    if fam in ("headcover", "grip", "glove"):
        return "gear-" + p["id"] + ".webp"
    return {"lgw01-gold": "gold-full-cut.webp", "lgw01-black": "black-cut.webp", "lgp01-gold": "blade-cut.webp",
            "lgp02-gold": "mallet-full-cut.webp", "lgh01": "stryker-full-cut.webp"}.get(p["id"])


def coll_href(p):
    fam = p.get("family")
    if fam == "hat":
        return p["id"] + ".html"
    if fam in ("polo-classic", "polo-blade"):
        return "polo-" + p["id"].replace("polo-", "") + ".html"
    return {"lgw01-gold": "carver.html", "lgw01-black": "black.html", "lgp01-gold": "blade.html",
            "lgp02-gold": "mallet.html", "lgh01": "stryker.html"}.get(p["id"], KIND_HREF.get(fam, "clubs.html"))


def build_collection(key):
    """Any collection, off the catalogue. Kind chips are generated from what
    is actually in it, so an empty filter can never show up."""
    c = COLLECTIONS[key]
    items = [p for p in PRODUCTS["products"]
             if p.get("built", True) and not p.get("discontinued")
             and coll_img(p) and (c["families"] is None or p.get("family") in c["families"])]

    def run():
        kinds, cards = [], ""
        for i, p in enumerate(items):
            fam = p.get("family")
            label = KIND_LABEL.get(fam, fam)
            if label not in kinds:
                kinds.append(label)
            live = any(v["avail"] for v in p["variants"].values())
            img = coll_img(p)
            tag = '<span class="lg-tag">Sold out</span>' if not live else ""
            cards += (f'<article class="it" data-i="{i}" data-kind="{esc(label)}" data-name="{esc(p["name"])}" '
                      f'data-price="{p["price"]}" data-best="{rank(p["id"])[0]}" data-new="{rank(p["id"])[1]}"'
                      f'{"" if live else " data-dead"}>'
                      f'<a class="it-ph" href="{coll_href(p)}"><img src="img/{img}" alt="{esc(p["name"])}" loading="lazy">{tag}</a>'
                      f'<a class="it-bd" href="{coll_href(p)}"><span class="nm">{esc(p["name"])}</span>'
                      f'<b>{p["priceLabel"].replace(chr(8211), " to ")}</b>'
                      f'<span class="meta">{"In stock" if live else "Sold out"}</span></a></article>')
        chips = '<button type="button" data-f="kind" data-v="" aria-pressed="true">All</button>'
        chips += "".join(f'<button type="button" data-f="kind" data-v="{esc(k)}" aria-pressed="false">{esc(k)}</button>'
                         for k in kinds)
        pband = "".join(f'<figure><img src="img/{i}" alt="{esc(a)}" loading="lazy"></figure>' for i, a in
                        [("two-gold-wedges.webp", "Two gold Carvers on the fringe"),
                         ("fit-sunset.webp", "A Lucky polo and hat at sunset"),
                         ("putt-sunset.webp", "A putt at sunset")])
        return fill(open(os.path.join(SRC, "collection.html"), encoding="utf-8").read(), {
            "TITLE": c["title"], "EYEBROW": c["eyebrow"], "LEDE": c["lede"], "PBAND": pband,
            "KINDS": chips, "CARDS": cards, "COUNT": str(len(items)),
            "SIGNHEAD": c["signhead"], "SIGNLEDE": c["signlede"]})
    return run


REVIEW_CLUBS = [("lgw01-gold", "Carver 02"), ("lgp01-gold", "Eclipse Blade"), ("lgp02-gold", "Eclipse Mallet"), ("lgh01", "Stryker")]


def build_reviews():
    """Every club's reviews in one pool: the real Judge.me counts and samples."""
    totals, sample = {}, []
    for pid, label in REVIEW_CLUBS:
        r = json.load(open(os.path.join(ROOT, "_src", "data", "reviews", pid + ".json"), encoding="utf-8"))
        for k, v in r["totals"].items():
            totals[k] = totals.get(k, 0) + v
        for x in r["sample"]:
            y = dict(x); y["c"] = label; sample.append(y)
    n = sum(totals.values())
    avg = int(sum(int(k) * v for k, v in totals.items()) / n * 10) / 10
    clubs = '<button type="button" data-c="" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-c="{esc(l)}" aria-pressed="false">{esc(l)}</button>' for _, l in REVIEW_CLUBS)
    return fill(open(os.path.join(SRC, "reviews.html"), encoding="utf-8").read(), {
        "REVIEWS_JSON": js({"totals": totals, "sample": sample}), "AVG": f"{avg:.1f}", "CLUBS": clubs})


GIFT_AMOUNTS = [10, 25, 50, 100, 150, 200, 250, 300, 500]   # all nine variants on the store, read 2026-09-23


def build_giftcard():
    chips = "".join(f'<button class="lg-chip" type="button" data-a="{a}" aria-pressed="{str(a == 50).lower()}">${a}</button>'
                    for a in GIFT_AMOUNTS)
    return fill(open(os.path.join(SRC, "giftcard.html"), encoding="utf-8").read(), {"AMOUNTS": chips, "LOGO": logo()})


def build_giftcard_view():
    return fill(open(os.path.join(SRC, "giftcard-view.html"), encoding="utf-8").read(), {"LOGO": logo()})


# The community wall. In the theme each post is a metaobject entry in the
# Shopify admin: media, @handle, link, and a product list. These are OUR OWN
# shoot photos, posted as our own account: no fabricated customers.
COMMUNITY = [
    ("swing-black-wedge.webp", "A swing with the Carver 02 Black", "Black on black, gold on the clover.",
     ["lgw01-black", "hat-black-gold-classic", "polo-signature-black"]),
    ("two-gold-wedges.webp", "Two gold Carvers on the fringe", "The 56 and the 60. Nobody needs both. Everybody buys both.",
     ["lgw01-gold"]),
    ("fit-sunset.webp", "Golden hour in the Nightshade and the white rope hat", "Last light, last hole.",
     ["polo-nightshade", "hat-white-gold-classic"]),
    ("black-hat-mallet.webp", "The Mallet and the black hat on the green", "The Mallet, doing Mallet things.",
     ["lgp02-gold", "hat-black-gold-classic"]),
    ("lucky-stryker-in-hand.webp", "The Stryker in hand", "The gap between the 4 iron and the wood, closed.",
     ["lgh01"]),
    ("gold-wedge-bag.webp", "A gold Carver resting on the bag", "Where it lives between shots.",
     ["lgw01-gold"]),
    ("two-hats-mallet.webp", "Two hats and the Mallet", "Pick a hat. Or don't.",
     ["lgp02-gold", "hat-black-gold-classic", "hat-tan-cursive"]),
    ("green-read-fit.webp", "Reading a putt in the Nightshade", "Reading it twice, hitting it once.",
     ["polo-nightshade", "hat-white-gold-classic"]),
    ("putter-in-hand.webp", "The Eclipse Blade in hand", "Milled from a block. You can feel it.",
     ["lgp01-gold"]),
    ("lucky-carver-gold-address.webp", "The gold Carver at address", "Square it up.",
     ["lgw01-gold"]),
    ("lucky-bag-glove.webp", "The Lucky glove on the bag", "The small stuff counts.",
     ["glove-tour"]),
]
KIND = {"wedge": "clubs", "putter": "clubs", "hybrid": "clubs", "polo-classic": "apparel", "polo-blade": "apparel",
        "hat": "apparel", "glove": "gear", "headcover": "gear", "grip": "gear"}


def build_community():
    by_id = {p["id"]: p for p in PRODUCTS["products"]}
    posts, data = "", []
    for i, (img, alt, cap, ids) in enumerate(COMMUNITY):
        prods = []
        for pid in ids:
            p = by_id[pid]
            live = [v for v in p["variants"].values() if v["avail"]]
            prods.append({"name": p["name"], "img": coll_img(p) if p.get("family") not in ("glove",) else "gear-" + pid + ".webp",
                          "href": coll_href(p) if p.get("family") != "glove" else "gear-" + pid + ".html",
                          "price": p["price"], "priceLabel": p["priceLabel"].replace(chr(8211), " to "),
                          "single": len(p["variants"]) == 1 and bool(live), "live": bool(live),
                          "pick": {"wedge": "Pick a loft", "putter": "Pick a hand", "hybrid": "Pick a hand"}.get(p.get("family"), "Pick a size")})
        kinds = sorted({KIND.get(by_id[pid].get("family"), "gear") for pid in ids})
        tags = "".join(f'<span>{esc(x["name"])}</span>' for x in prods[:2]) + (f'<span>+{len(prods) - 2}</span>' if len(prods) > 2 else "")
        posts += (f'<button class="post" type="button" data-i="{i}" data-kinds="{" ".join(kinds)}" aria-label="{esc(alt)}">'
                  f'<img src="img/{img}" alt="{esc(alt)}" loading="lazy"><span class="who">@luckygolfofficial</span>'
                  f'<span class="tags">{tags}</span></button>')
        data.append({"img": img, "alt": alt, "who": "@luckygolfofficial", "cap": cap, "products": prods})
    return fill(open(os.path.join(SRC, "community.html"), encoding="utf-8").read(),
                {"POSTS": posts, "POSTS_JSON": js(data), "COUNT": str(len(COMMUNITY))})


def build_story():
    return fill(open(os.path.join(SRC, "story.html"), encoding="utf-8").read(), {})


def build_hats():
    """Ten hats, $29, with real stock. Names, prices and what is sold out come
    from _src/data/products.json; the cutouts are in v9/src/cut."""
    hats = [p for p in PRODUCTS["products"] if p.get("family") == "hat"]
    st = ['<button type="button" data-f="style" data-v="" aria-pressed="true">All</button>']
    for key, label in HAT_STYLES:
        st.append(f'<button type="button" data-f="style" data-v="{key}" aria-pressed="false">{label}</button>')
    cards = []
    for i, p in enumerate(hats):
        style, colour = HAT_META[p["id"]]
        v = list(p["variants"].values())[0]
        img = f'img/{p["id"]}-cut.webp'
        name = esc(p["name"])
        dead = "" if v["avail"] else " data-dead"
        btn = ('<button type="button">Add · $29</button>' if v["avail"]
               else '<button type="button" disabled>Sold out</button>')
        meta = "Five-panel snapback" if v["avail"] else "Sold out"
        cards.append(
            f'<article class="hat" data-i="{i}" data-style="{style}" data-colour="{colour}" data-name="{name}" data-img="{img}" '
            f'data-best="{rank(p["id"])[0]}" data-new="{rank(p["id"])[1]}"{dead}>'
            f'<div class="hat-ph"><img src="{img}" alt="{name}" loading="lazy">'
            f'<div class="qa">{btn}</div></div>'
            f'<a class="hat-bd" href="{p["id"]}.html"><span class="nm">{name}</span><b>$29</b>'
            f'<span class="meta">{meta}</span></a></article>')
    return fill(open(os.path.join(SRC, "hats.html"), encoding="utf-8").read(),
                {"STYLES": "".join(st), "CARDS": "".join(cards), "COUNT": str(len(hats))})


POLO_COPY = json.load(open(os.path.join(SRC, "polos-copy.json"), encoding="utf-8"))


def polo_slug(x):
    return "polo-" + x["img"].split("/")[-1].replace("polo-", "").replace("-pack.webp", "") + ".html"


def build_polo(name="Azalea"):
    """One product page per print. Sizes, stock, swatches and the cross-sell
    all come from polos-data.json; the words come from polos-copy.json."""
    def run():
        P = json.load(open(os.path.join(SRC, "polos-data.json"), encoding="utf-8"))
        me = [x for x in P if x["name"] == name][0]
        stem = me["img"].split("/")[-1].replace("-pack.webp", "")
        sw = "".join(
            f'<a class="lg-swatch" href="{polo_slug(x)}"{" aria-current=\"page\"" if x is me else ""} aria-label="{x["name"]}">'
            f'<img src="img/{x["img"].split("/")[-1].replace("-pack", "-print")}" alt="" loading="lazy"></a>'
            for x in P if x["collar"] == me["collar"])
        # the cross-sell points at the other collar, so it is never this shirt
        other = [x for x in P if x["collar"] != me["collar"]][0]
        polo = {"name": me["name"], "full": me["full"], "collar": me["collar"],
                "img": me["img"].replace("-pack", "-cut"), "sizes": me["sizes"]}
        return fill(open(os.path.join(SRC, "polo.html"), encoding="utf-8").read(),
                    {"SWATCHES": sw, "POLO_JSON": js(polo), "NAME": esc(me["name"]), "FULL": esc(me["full"]),
                     "STEM": stem, "COLLAR": "The Blade" if me["collar"] == "blade" else "The Classic",
                     "DESC": POLO_COPY[me["name"]],
                     "OTHER_HREF": polo_slug(other), "OTHER_IMG": other["img"].split("/")[-1].replace("-pack", "-cut"),
                     "OTHER_NAME": esc(other["full"]),
                     "OTHER_LN": "Blade collar, no buttons. The quieter half of the rack." if other["collar"] == "blade"
                                 else "Classic collar, three buttons. The other half of the rack."})
    return run


BUILDERS = {"carver": build_carver("gold"), "home": build_home, "clubs": build_clubs, "polos": build_polos, "polo": build_polo("Azalea"),
            "hats": build_hats, "gear": build_gear, "gearpdp": build_gear_product("grip-clover-black"), "blog": build_blog, "collection": build_collection("all"),
            "account": build_simple("account.html"), "reviews": build_reviews, "community": build_community, "giftcard": build_giftcard,
            "giftcard-view": build_giftcard_view, "order": build_simple("order.html"),
            "addresses": build_simple("addresses.html"), "policy": build_simple("policy.html"),
            "login": build_simple("login.html"),
            "collection-accessories": build_collection("accessories"), "article": build_article, "hat": build_hat("hat-white-gold-classic"), "story": build_story, "search": build_search,
            "faq": build_simple("faq.html"), "trybe": build_simple("trybe.html"),
            "cart": build_simple("cart.html"), "404": build_simple("404.html"),
            "contact": build_simple("contact.html"),
            "black": build_carver("black"),
            "mood": build_carver("black", mood=True), "blade": build_club("blade"),
            "mallet": build_club("mallet"), "stryker": build_club("stryker")}


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(AFTER, "img"))
    # the system, copied untouched
    for f in ("lucky.css", "lucky.js"):
        shutil.copy(os.path.join(ROOT, "shopify", "assets", f), AFTER)
    for f in ("site.css", "site.js"):
        shutil.copy(os.path.join(SRC, f), AFTER)
    used = set()
    extra_pages = [{"key": "contact", "file": "contact.html"},
                   {"key": "collection-accessories", "file": "collection-accessories.html"},
                   {"key": "login", "file": "login.html"},
                   {"key": "order", "file": "order.html"},
                   {"key": "addresses", "file": "addresses.html"},
                   {"key": "giftcard-view", "file": "giftcard-view.html"}]
    for h in [p for p in PRODUCTS["products"] if p.get("family") == "hat"]:
        if h["id"] == "hat-white-gold-classic":
            continue                       # that one is a board row already
        BUILDERS["hat:" + h["id"]] = build_hat(h["id"])
        extra_pages.append({"key": "hat:" + h["id"], "file": h["id"] + ".html"})
    for g in [p for p in PRODUCTS["products"] if p.get("family") in ("headcover", "grip", "glove")]:
        if g["id"] == "grip-clover-black":
            continue
        BUILDERS["gear:" + g["id"]] = build_gear_product(g["id"])
        extra_pages.append({"key": "gear:" + g["id"], "file": "gear-" + g["id"] + ".html"})
    POLOS = json.load(open(os.path.join(SRC, "polos-data.json"), encoding="utf-8"))
    for x in POLOS:
        if x["name"] == "Azalea":
            continue                       # that one is a board row already
        key = "polo:" + x["name"]
        BUILDERS[key] = build_polo(x["name"])
        extra_pages.append({"key": key, "file": polo_slug(x)})
    for p in PAGES + extra_pages:
        if not p.get("built", True):
            continue
        html = BUILDERS[p["key"]]()
        used |= set(re.findall(r'img/([\w.\-]+\.(?:webp|svg|jpg|png))', html))
        open(os.path.join(AFTER, p["file"]), "w", encoding="utf-8").write(html)
    used |= {"mags-ink.webp", "mags-light.webp", "mags-bag-ink.webp", "mags-bag-light.webp", "gold-3q-cut.webp"}
    for name in sorted(used):
        shutil.copy(find_img(name), os.path.join(AFTER, "img", name))
    # before: the approved pages exactly as on the colour board
    shutil.copytree(V8OUT, BEFORE, ignore=shutil.ignore_patterns("review.html"))
    # the board
    tpl = open(os.path.join(SRC, "board.html"), encoding="utf-8").read()
    notes = json.load(open(os.path.join(SRC, "notes.json"), encoding="utf-8"))
    board = tpl.replace("{{PAGES}}", js(PAGES)).replace("{{NOTES}}", js(notes))
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(board)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(OUT) for f in fs)
    print(f"built {[p['key'] for p in PAGES if p['built']]} · {n} files · {size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
