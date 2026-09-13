"""
Build the three v4 review pages from the live catalogue and the approved copy.

    python v4/tools/build.py          # writes v4/out/{home,carver-01,polos}.html
    python v4/tools/check.py          # then render and verify them

Sources (nothing is retyped here that already has a home):
  _src/data/products.json      prices, variants, stock, ratings
  _src/data/copy/*.json        approved editorial lines
  _src/data/reviews/*.json     verbatim Judge.me reviews and live distributions
  v4/out/img/manifest.json     normalised images (tools/normalize-images.py)
  v4/data/price-case.json      big-brand list prices, with sources

The build FAILS on: a product with no normalised image, an image that belongs
to a different product, a review quote that is not found verbatim, and an
em dash anywhere in the output.
"""
import html
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V4, ".."))
DATA = os.path.join(ROOT, "_src", "data")
OUT = os.path.join(V4, "out")

ERR = []


def fail(msg):
    ERR.append(msg)


def jload(*p):
    return json.load(open(os.path.join(*p), encoding="utf-8"))


CAT = jload(DATA, "products.json")
PROD = {p["id"]: p for p in CAT["products"]}
COLL = {c["id"]: c for c in CAT["collections"]}
IMG = jload(OUT, "img", "manifest.json")
CASE = jload(V4, "data", "price-case.json")


def copy(pid):
    p = os.path.join(DATA, "copy", pid + ".json")
    return jload(p) if os.path.exists(p) else {}


def reviews(pid):
    p = os.path.join(DATA, "reviews", pid + ".json")
    return jload(p) if os.path.exists(p) else None


def esc(s):
    return html.escape(s, quote=True)


def money(n):
    return f"${n:,.2f}".replace(".00", "")


def pack(pid):
    e = IMG["products"].get(pid, {})
    src = e.get("pack")
    if not src:
        fail(f"no normalised pack shot for {pid}")
        return ""
    if not os.path.basename(src).startswith(pid + "-"):
        fail(f"{pid} is pointing at {src}, which is another product's image")
    return src


def photo(fn):
    e = IMG["photos"].get(fn)
    if not e:
        fail(f"photo {fn} was not normalised")
        return {"src": "", "w": 1, "h": 1}
    return e


def find_review(pid, name, title=None):
    r = reviews(pid)
    for s in (r or {}).get("sample", []):
        if s["n"] == name and (title is None or s["t"] == title):
            return s
    fail(f"review by {name} ({title}) not found verbatim in reviews/{pid}.json")
    return {"n": name, "t": title or "", "q": "", "r": 5}


# ---------------------------------------------------------------- ratings
def line_rating():
    tot = n = 0
    for pid in ("lgw01-gold", "lgp01-gold", "lgp02-gold", "lgh01"):
        r = reviews(pid)
        for star, c in r["totals"].items():
            tot += int(star) * c
            n += c
    return round(tot / n, 2), n


LINE_AVG, LINE_N = line_rating()
WEDGE = PROD["lgw01-gold"]["rating"]

# ---------------------------------------------------------------- chrome
ICON = {
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.6-3.6"/></svg>',
    "bag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 8h14l-1.2 12.2a1 1 0 0 1-1 .8H7.2a1 1 0 0 1-1-.8L5 8Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
}

# The wordmark is inlined, not <use>d: headless Chrome drew the <use> of these
# symbols blank or clipped, and a logo that can vanish is not a logo.
_SPRITE = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf-8").read()
WORDMARK = re.search(r'<symbol id="lg-lucky"[^>]*>(.*?)</symbol>', _SPRITE, re.S).group(1)

BUILT = {"home": "home.html", "carver": "carver-01.html", "polos": "polos.html"}
SOON = 'href="#" data-soon'


def logo(cls="logo"):
    return f'<a class="{cls}" href="{BUILT["home"]}" aria-label="Lucky Golf, home"><svg viewBox="164.15 237.42 513.48 118.24" fill="currentColor" aria-hidden="true">{WORDMARK}</svg></a>'


def header(current):
    def nav(key, label, href=None):
        cur = ' aria-current="page"' if key == current else ""
        h = f'href="{href}"' if href else SOON
        return f'<a {h}{cur}>{label}</a>'
    links = [nav("clubs", "Clubs"), nav("carver", "Wedges", BUILT["carver"]), nav("polos", "Polos", BUILT["polos"]),
             nav("hats", "Hats"), nav("reviews", "Reviews"), nav("story", "Our story")]
    return f"""
<div class="util"><div class="wrap">
  <span>Sixty-day returns on every club</span>
  <span class="u-opt">Ships in 1 to 2 business days</span>
  <span class="u-rate"><span class="star" aria-hidden="true">&#9733;</span> {LINE_AVG} from {LINE_N} verified reviews</span>
</div></div>
<header class="hdr"><div class="wrap">
  <button class="icon burger" type="button" data-menu aria-expanded="false" aria-controls="drawer" aria-label="Menu">{ICON['menu']}</button>
  {logo()}
  <nav class="nav" aria-label="Main">{''.join(links)}</nav>
  <div class="tools">
    <a class="icon search" {SOON} aria-label="Search">{ICON['search']}</a>
    <a class="icon" {SOON}="Your bag opens here on the real site." aria-label="Bag">{ICON['bag']}<span class="count" id="bagCount" hidden>0</span></a>
  </div>
</div></header>
<div class="drawer" id="drawer" hidden><div class="panel" role="dialog" aria-label="Menu">
  <button class="icon x" type="button" data-close aria-label="Close menu">{ICON['close']}</button>
  {''.join(links)}
</div></div>"""


def footer():
    return f"""
<footer class="ftr on-ink"><div class="wrap">
  <div class="top">
    <div class="brand">{logo()}<p class="blurb">Clubs built to the same standard as the big names, finished in gold, sold direct.</p></div>
    <div><h4>Clubs</h4><ul><li><a href="{BUILT['carver']}">Carver 01 Gold</a></li><li><a href="{BUILT['carver']}?finish=black">Carver 01 Black</a></li><li><a {SOON}>Tracer putters</a></li><li><a {SOON}>Stryker hybrid</a></li></ul></div>
    <div><h4>Apparel</h4><ul><li><a href="{BUILT['polos']}">Polos</a></li><li><a {SOON}>Hats</a></li><li><a {SOON}>Gear</a></li></ul></div>
    <div><h4>Help</h4><ul><li><a {SOON}>Returns</a></li><li><a {SOON}>Shipping</a></li><li><a {SOON}>FAQ</a></li><li><a {SOON}>Contact</a></li></ul></div>
    <div class="news"><h4>First look</h4><p class="blurb" style="margin:0 0 10px">New lofts, restocks and the odd bad idea. One email a month.</p>
      <form class="signup" onsubmit="event.preventDefault()"><label class="sr" for="em">Email</label><input id="em" type="email" placeholder="you@somewhere.com"><button type="submit" data-soon="Sign-up connects on the real site.">Sign me up</button></form></div>
  </div>
  <div class="base"><span>&copy; 2026 Lucky Golf</span><span>It's better to be lucky.</span></div>
</div></footer>"""


def signoff(sub, cta, href):
    return f"""
<section class="sign on-ink"><div class="wrap in">
  <div>
    <span class="label">The last word</span>
    <p class="disp d-xl">It's better<br>to be <em class="foil">lucky.</em></p>
    <p class="lede">{sub}</p>
    <a class="btn" href="{href}">{cta} {ICON['arrow']}</a>
    <p class="who">Sixty days to decide. Ships in 1 to 2 business days.</p>
  </div>
  <img class="mags" src="img/mags-light.webp" alt="Mags the magpie, holding a gold wedge" width="797" height="494" loading="lazy">
</div></section>"""


def page(key, title, desc, body):
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="site.css">
</head>
<body data-page="{key}">
{header(key)}
<main>
{body}
</main>
{footer()}
<script src="site.js"></script>
</body>
</html>
"""
    return doc


def card(pid, line, href=None, tag=None):
    p = PROD[pid]
    out = not p.get("inStock", True)
    h = f'href="{href}"' if href else SOON
    t = '<span class="tag sold">Sold out</span>' if out else (f'<span class="tag">{tag}</span>' if tag else "")
    return f"""<a class="card{' out' if out else ''}" data-pid="{pid}" {h}>{t}<div class="ph"><img src="{pack(pid)}" alt="{esc(p['name'])}" width="1200" height="1500" loading="lazy"></div>
<div class="tx"><span class="nm">{esc(p['name'])}</span><span class="pr">{p['priceLabel']}</span><span class="ln">{line}</span></div></a>"""


def quote(pid, name, title=None, product_name=None):
    s = find_review(pid, name, title)
    body = esc(s["q"]).replace("\n", " ")
    return f"""<figure class="qt" style="margin:0"><span class="stars" aria-label="{s['r']} out of 5 stars">{'&#9733;' * s['r']}{'&#9734;' * (5 - s['r'])}</span>
<h3>{esc(s['t'])}</h3><blockquote style="margin:0"><p>&ldquo;{body}&rdquo;</p></blockquote>
<figcaption class="by"><b>{esc(s['n'])}</b> &middot; {product_name or esc(PROD[pid]['name'])} &middot; <span class="vb">Verified buyer</span></figcaption></figure>"""


# ================================================================ HOME
def build_home():
    hero = photo(jload(V4, "data", "images.json")["photos"]["hero"])
    fin = photo("lucky-wedge-two-soles.webp")
    lines = {
        "lgw01-gold": "The one that makes you stop blaming the swing. Six lofts, two grinds, either hand.",
        "lgw01-black": "Blacked out, with gold on the clover and the loft stamp and nothing else.",
        "lgp01-gold": "Short ones start to feel like a formality. Quiet off the face and planted through the stroke.",
        "lgp02-gold": "Works with the arc your stroke already has instead of asking you to build a new one.",
        "lgh01": "Easier to launch than the long iron it replaces, and the rough does not grab it on the way through.",
    }
    hrefs = {"lgw01-gold": BUILT["carver"], "lgw01-black": BUILT["carver"] + "?finish=black"}
    tags = {"lgw01-gold": "Best seller"}
    cards = "".join(card(pid, lines[pid], hrefs.get(pid), tags.get(pid)) for pid in lines)

    rows = "".join(
        f'<div class="ln"><span class="who">{esc(r["brand"])} {esc(r["model"])}<small>List price, one wedge</small></span><span class="amt">{money(r["price"])}</span></div>'
        for r in CASE["rows"])
    carver = PROD["lgw01-gold"]
    in_stock_putters = sorted(PROD[p]["price"] for p in ("lgp01-gold", "lgp02-gold") if PROD[p].get("inStock"))

    polo_ids = COLL["polos"]["products"]
    hat_ids = COLL["hats"]["products"]

    body = f"""
<section class="hero on-ink">
  <img src="{hero['src']}" alt="The Lucky Golf line together on the grass" width="{hero['w']}" height="{hero['h']}" fetchpriority="high" style="object-position:62% 55%">
  <div class="cap"><div class="wrap">
    <span class="label">It's better to be lucky</span>
    <h1 class="disp d-xl">Get used to the <em class="foil">attention</em></h1>
    <p class="lede">Built to the same standard as the big names, finished in gold, and priced like nobody in the middle is taking a cut. Sixty days to prove us wrong.</p>
    <div class="ctas"><a class="btn" href="#clubs">Shop the clubs {ICON['arrow']}</a><a class="ghost" href="{BUILT['carver']}">See the Carver 01</a></div>
    <div class="rating"><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><span><b>{LINE_AVG}</b> from {LINE_N} verified reviews on Judge.me</span></div>
  </div></div>
</section>

<section class="sec" id="clubs"><div class="wrap">
  <div class="head"><div><span class="label">The line</span><h2 class="disp d-m">Shop the <em class="foil">gold</em> standard</h2></div><a class="link" {SOON}>All clubs</a></div>
  <div class="row five scroll">{cards}</div>
</div></section>

<section class="sec on-ink" id="price"><div class="wrap case">
  <div>
    <div class="head" style="margin-bottom:28px"><div><span class="label">Priced honestly</span><h2 class="disp d-m">Everything you're paying for is the <em class="foil">club</em></h2></div></div>
    <div class="ledger">
      {rows}
      <div class="ln us"><span class="who">Carver 01 Gold<small>Forged 1020, six lofts, two grinds</small></span><span class="amt"><em class="foil">{carver['priceLabel']}</em></span></div>
    </div>
    <p class="src">Big-brand prices are each maker's own US list price for one steel-shaft wedge, checked {CASE['checked']}.</p>
  </div>
  <div class="reasons">
    <div><span class="n">01</span><div><h3>No middlemen</h3><p>We sell direct. The savings are not a sale, they are just the math.</p></div></div>
    <div><span class="n">02</span><div><h3>No tour contracts</h3><p>Nobody is paid to put a Lucky in play on Sunday. That money was never in your price to begin with.</p></div></div>
    <div><span class="n">03</span><div><h3>What is left is the club</h3><p>The forging, the milling, the finish. The parts you actually hit.</p></div></div>
    <div><span class="n">60</span><div><h3>Sixty days to find out</h3><p>Every club gets sixty days from delivery. If it isn't the one, it goes back.</p></div></div>
  </div>
</div></section>

<section class="sec" id="finder"><div class="wrap">
  <div class="head"><div><span class="label">Start here</span><h2 class="disp d-m">Tell us what's costing you <em class="foil">shots</em></h2></div><p class="lede">Most golfers already know the answer to this one. Pick it, and we will point you at the ones worth looking at.</p></div>
  <div class="finder">
    <a class="fx" href="{BUILT['carver']}"><img src="{pack('lgw01-gold')}" alt="" loading="lazy"><span class="big">100<small>yds</small></span><div><p class="q">Inside a hundred yards</p><p>Wedges that stop. Six lofts, two grinds.</p></div><span class="go">Wedges from {money(min(PROD['lgw01-gold']['price'], PROD['lgw01-black']['price']))} {ICON['arrow']}</span></a>
    <a class="fx" {SOON}><img src="{pack('lgp02-gold')}" alt="" loading="lazy"><span class="big">8<small>ft</small></span><div><p class="q">The putts you should make</p><p>A blade and a mallet, milled from stainless.</p></div><span class="go">Putters {money(in_stock_putters[0])} in stock {ICON['arrow']}</span></a>
    <a class="fx" {SOON}><img src="{pack('lgh01')}" alt="" loading="lazy"><span class="big">210<small>yds</small></span><div><p class="q">Still a long way out</p><p>The Stryker. Titanium, nineteen degrees.</p></div><span class="go">Hybrid {PROD['lgh01']['priceLabel']} {ICON['arrow']}</span></a>
  </div>
</div></section>

<section class="split" style="background:var(--tile)">
  <div class="ph"><img src="{fin['src']}" alt="Two Carver 01 Gold wedges and a ball on the grass" width="{fin['w']}" height="{fin['h']}" loading="lazy"></div>
  <div class="tx">
    <span class="label">The finish</span>
    <h2 class="disp d-m">You'll get asked about it on the first tee</h2>
    <p class="body">Somebody in your group is going to ask what you are playing. Gold at address looks like nothing else out there, and it is the first thing the reviews talk about.</p>
    <p class="body">Want it quieter? The blacked-out one does the same job without the conversation.</p>
    <div class="ctas" style="display:flex;gap:12px;flex-wrap:wrap;margin-top:10px"><a class="ghost" href="{BUILT['carver']}">Gold {PROD['lgw01-gold']['priceLabel']}</a><a class="ghost" href="{BUILT['carver']}?finish=black">Black {PROD['lgw01-black']['priceLabel']}</a></div>
  </div>
</section>

<section class="sec" id="reviews"><div class="wrap">
  <div class="rv-top">
    <div><span class="label" style="color:var(--gold-text);display:block;margin-bottom:14px">Reviews</span><h2 class="disp d-m">Thousands of golfers bag <em class="foil">Lucky</em></h2></div>
    <div class="score"><b>{LINE_AVG}</b><div><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><small>{LINE_N} verified reviews on Judge.me, across the club line</small></div></div>
  </div>
  <div class="quotes">
    {quote('lgw01-gold', 'Michael P.')}
    {quote('lgp01-gold', 'Jay S.')}
    {quote('lgh01', 'John L.L.')}
  </div>
  <p style="margin-top:36px"><a class="link" {SOON}>Read every review</a></p>
</div></section>

<section class="sec tight" style="border-top:1px solid var(--line)"><div class="wrap">
  <div class="head"><div><span class="label">Apparel</span><h2 class="disp d-m">Cut to play in</h2></div><a class="link" href="{BUILT['polos']}">All polos</a></div>
  <div class="row four scroll">
    {''.join(card(pid, 'Classic Polo' if PROD[pid]['family']=='polo-classic' else 'Blade Polo', BUILT['polos']) for pid in polo_ids[:3])}
    {card(hat_ids[0], 'Hats, ten styles', None)}
  </div>
</div></section>

{signoff('Golf is luck sometimes. The good bounce, the bad kick, the putt that lips out for no reason. That is the name on the club.', 'Go put one in the bag', '#clubs')}
"""
    return page("home", "Lucky Golf | Gold golf clubs, sold direct", "Forged wedges, milled putters and a titanium hybrid, finished in gold and sold direct.", body)


# ================================================================ CARVER
def lg_label(v):
    return v["label"]


def finish_data(pid, gallery_extra, default_lg, set_defaults):
    p = PROD[pid]
    hands = [v["k"] for v in next(o for o in p["options"] if o["key"] == "hand")["values"]]
    lofts = [{"k": v["k"], "label": lg_label(v)} for v in next(o for o in p["options"] if o["key"] == "loftgrind")["values"]]
    return {
        "name": p["name"], "price": p["price"], "label": p["finish"] + " &middot; " + p["priceLabel"],
        "hands": hands, "lofts": lofts, "defaultLg": default_lg, "setDefaults": set_defaults,
        "variants": {k: {"avail": v["avail"]} for k, v in p["variants"].items()},
    }


def build_carver():
    sel = jload(V4, "data", "images.json")["products"]
    g, b = copy("lgw01-gold"), copy("lgw01-black")
    finishes = {
        "gold": finish_data("lgw01-gold", None, "56K", ["52K", "60K"]),
        "black": finish_data("lgw01-black", None, "56K", ["52K", "60K"]),
    }
    for k in finishes:
        finishes[k]["label"] = finishes[k]["label"].replace("&middot;", "·")

    def gallery(pid, fkey, alt):
        figs = []
        entry = IMG["products"][pid]
        for i, src in enumerate(entry["gallery"]):
            figs.append(f'<figure data-f="{fkey}"><img src="{src}" alt="{esc(alt)}, studio view {i + 1}" width="1600" height="1600" loading="{"eager" if i == 0 else "lazy"}"></figure>')
        for fn in sel[pid].get("photos", []):
            ph = photo(fn)
            figs.append(f'<figure class="wide" data-f="{fkey}"><img src="{ph["src"]}" alt="{esc(alt)} on the course" width="{ph["w"]}" height="{ph["h"]}" loading="lazy"></figure>')
        return "".join(figs)

    gal = gallery("lgw01-gold", "gold", "Carver 01 Gold wedge") + gallery("lgw01-black", "black", "Carver 01 Black wedge")

    def acc(c, fkey):
        return "".join(f'<details data-f="{fkey}"><summary>{a["h"]}</summary><p>{a["b"]}</p></details>' for a in c["accordion"])

    def facts(c, fkey):
        return f'<div class="facts" data-f="{fkey}">' + "".join(f'<div><b>{x["k"]}</b><span>{x["v"]}</span></div>' for x in c["four"]) + "</div>"

    rv = reviews("lgw01-gold")
    tot = rv["total"]
    hist = "".join(
        f'<div><span>{s}&#9733;</span><i><b style="width:{rv["totals"][str(s)] / tot * 100:.1f}%"></b></i><span>{rv["totals"][str(s)]}</span></div>'
        for s in (5, 4, 3, 2, 1))
    # Newest six that say something: 4 stars and up, a real sentence, and a
    # title that is not just the product name Judge.me pre-fills.
    said = [s for s in rv["sample"] if s["r"] >= 4 and len(s["q"]) >= 40 and "LGW" not in s["t"]]
    latest = sorted(said, key=lambda s: s["d"], reverse=True)[:6]
    rcards = "".join(quote("lgw01-gold", s["n"], s["t"], "Carver 01") for s in latest)

    specs = g["specs"]
    tables = []
    for i, t in enumerate(specs["grindTables"]):
        head = "".join(f"<th scope=\"col\">{c}</th>" for c in t["cols"])
        body = "".join(f'<tr><th scope="row">{r["k"]}</th>' + "".join(f"<td>{v}</td>" for v in r["v"]) + "</tr>" for r in t["rows"])
        tables.append((t["label"], f'<div class="tablewrap"><table class="spec"><thead><tr><th scope="col">Loft</th>{head}</tr></thead><tbody>{body}</tbody></table></div>'))
    for t in specs["kvTables"]:
        head = "".join(f"<th scope=\"col\">{c}</th>" for c in t["cols"])
        body = "".join(f'<tr><th scope="row">{r["k"]}</th>' + "".join(f"<td>{v}</td>" for v in r["v"]) + "</tr>" for r in t["rows"])
        tables.append((t["tab"].capitalize(), f'<div class="tablewrap"><table class="spec"><thead><tr><th scope="col"></th>{head}</tr></thead><tbody>{body}</tbody></table></div><p class="tnote">{t["note"]}</p>'))
    tabs = "".join(f'<button type="button" role="tab" id="st{i}" aria-controls="sp{i}" aria-selected="{str(i == 0).lower()}">{lab}</button>' for i, (lab, _) in enumerate(tables))
    panels = "".join(f'<div role="tabpanel" id="sp{i}" aria-labelledby="st{i}"{"" if i == 0 else " hidden"}>{tb}</div>' for i, (_, tb) in enumerate(tables))

    more = "".join(card(m["id"], m["hook"], BUILT["carver"] + "?finish=black" if m["id"] == "lgw01-black" else None) for m in g["more"])
    story_ph = photo("lucky-wedge-sole-turf.webp")
    duo1, duo2 = photo("lucky-wedge-face-turf.webp"), photo("lucky-carver-gold-address.webp")

    pdata = {"defaultFinish": "gold", "finishes": finishes}

    body = f"""
<div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{BUILT['home']}">Home</a> / <a {SOON}>Clubs</a> / <a {SOON}>Wedges</a> / <span aria-current="page">Carver 01</span></nav>
  <div class="pdp">
    <div>
      <div class="gal" id="gal" aria-label="Photos">{gal}</div>
      <div class="dots" id="dots" aria-hidden="true"></div>
    </div>
    <div class="buy">
      <span class="label">The 01 &middot; Wedge</span>
      <h1 class="disp d-l">Carver <em class="foil">01</em></h1>
      <div class="rt"><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><a href="#reviews">{WEDGE['avg']} from {WEDGE['count']} reviews</a></div>
      <p class="quote-line" data-f="gold"><q>{g['quoteLine']}</q> {g['quoteWho']}</p>
      <p class="quote-line" data-f="black" hidden><q>{b['quoteLine']}</q> {b['quoteWho']}</p>
      <p class="price" id="price">{PROD['lgw01-gold']['priceLabel']} <small>Same price, every loft</small></p>
      <p class="pitch" data-f="gold">{g['buyLine']}</p>
      <p class="pitch" data-f="black" hidden>{b['buyLine']}</p>

      <fieldset class="opt"><legend><span class="label">Finish</span><span class="val" id="finVal"></span></legend>
        <div class="chips"><button class="chip" type="button" data-finish-chip="gold"><span class="sw gold"></span>Gold <small>{PROD['lgw01-gold']['priceLabel']}</small></button><button class="chip" type="button" data-finish-chip="black"><span class="sw black"></span>Black <small>{PROD['lgw01-black']['priceLabel']}</small></button></div>
      </fieldset>
      <fieldset class="opt"><legend><span class="label">Hand</span><span class="val" id="handVal"></span></legend>
        <div class="chips"><button class="chip" type="button" data-hand="RH">Right hand</button><button class="chip" type="button" data-hand="LH">Left hand</button></div>
        <p class="tnote" id="handNote" hidden>The Black is right hand only for now. Left hand is coming.</p>
      </fieldset>
      <fieldset class="opt"><legend><span class="label">Loft &amp; grind</span><span class="val" id="lgVal"></span></legend>
        <div class="chips grid3" id="lofts"></div>
        <p class="tnote" id="lgNote" hidden>Struck through means sold out in this hand right now.</p>
      </fieldset>
      <fieldset class="opt set"><legend><span class="label">How many</span></legend>
        <div class="chips grid3"><button class="chip" type="button" data-set="1"><b>1 wedge</b><small>This one</small></button><button class="chip" type="button" data-set="2"><span class="flag">Most carry two</span><b>2 wedges</b><small>Gap and sand</small></button><button class="chip" type="button" data-set="3"><b>3 wedges</b><small>Gap, sand, lob</small></button></div>
      </fieldset>
      <div class="extra" id="extra" hidden></div>

      <button class="btn btn-block" type="button" id="addBtn" data-add><span id="addLabel">Add to bag</span></button>
      <div class="stock"><span><b>In stock</b> &middot; ships in 1 to 2 business days</span><span>Sixty days to decide</span></div>
      {facts(g, 'gold')}{facts(b, 'black').replace('class="facts"', 'class="facts" hidden')}
      <div class="acc">{acc(g, 'gold')}{acc(b, 'black').replace('<details ', '<details hidden ')}</div>
    </div>
  </div>
</div>

<section class="sec" style="background:var(--tile)"><div class="wrap story">
  <div>
    <span class="label" style="color:var(--gold-text)">Forged feel, filthy spin</span>
    <h2 class="disp d-m" style="margin:14px 0 22px" data-f="gold">Rip it back and go <em class="foil">tap it in</em></h2>
    <h2 class="disp d-m" style="margin:14px 0 22px" data-f="black" hidden>All the spin, none of the <em class="foil">shine</em></h2>
    <p class="body" data-f="gold">{g['clubParas'][0]}</p>
    <p class="body" data-f="black" hidden>{b['clubParas'][0]}</p>
  </div>
  <div class="ph"><img src="{story_ph['src']}" alt="Carver 01 Gold behind a ball in a bunker" width="{story_ph['w']}" height="{story_ph['h']}" loading="lazy"></div>
</div></section>

<section class="sec on-ink"><div class="wrap">
  <div class="head"><div><span class="label">Two grinds</span><h2 class="disp d-m">Square it up, or <em class="foil">open it up</em></h2></div><p class="lede">{g['help']['sub']}</p></div>
  <div class="grinds">
    {''.join(f'<div class="grind"><span class="pill">{c["pill"]}</span><h3 class="disp d-s">{c["name"]}</h3><p>{c["body"]}</p><div class="lofts">{c["lofts"]}</div></div>' for c in g['help']['cards'])}
  </div>
  <p class="tnote" style="color:var(--muted-dark)" data-f="black" hidden>The Black comes in the K grind only. The S lives on the Gold.</p>
</div></section>

<section class="sec"><div class="wrap">
  <div class="head"><div><span class="label">LGW01 specs</span><h2 class="disp d-m">The numbers</h2></div><p class="lede">{specs['sub']}</p></div>
  <div data-tabs><div class="tabs" role="tablist" aria-label="Spec tables">{tabs}</div>{panels}</div>
  <p class="tnote">{specs['clubNote']}</p>
</div></section>

<section class="sec" id="reviews" style="border-top:1px solid var(--line)"><div class="wrap">
  <div class="rv-top">
    <div><span class="label" style="color:var(--gold-text);display:block;margin-bottom:14px">Reviews</span><h2 class="disp d-m">What golfers said</h2></div>
    <div style="display:flex;gap:36px;align-items:center;flex-wrap:wrap"><div class="score"><b>{WEDGE['avg']}</b><div><span class="stars" aria-hidden="true">&#9733;&#9733;&#9733;&#9733;&#9733;</span><small>{WEDGE['count']} verified reviews</small></div></div><div class="hist" aria-label="Rating distribution">{hist}</div></div>
  </div>
  <div class="rlist">{rcards}</div>
  <p style="margin-top:36px"><a class="link" {SOON}>Read all {WEDGE['count']} reviews</a></p>
</div></section>

<section class="sec tight"><div class="wrap duo">
  <figure><img src="{duo1['src']}" alt="Carver 01 Gold, face down on the grass" width="{duo1['w']}" height="{duo1['h']}" loading="lazy"></figure>
  <figure><img src="{duo2['src']}" alt="Carver 01 Gold at address on the fairway" width="{duo2['w']}" height="{duo2['h']}" loading="lazy"></figure>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="head"><div><span class="label">More from the bag</span><h2 class="disp d-m">Goes with the 01</h2></div></div>
  <div class="row four scroll">{more}</div>
</div></section>

{signoff(g['signoff']['sub'], 'Pick a loft', '#gal')}

<div class="stickybuy" id="stickybuy" aria-hidden="true"><span class="nm"><span id="sbName">Carver 01 Gold</span><small>Loft and grind chosen above</small></span><button class="btn" type="button" data-add tabindex="-1">Add &middot; <span id="sbPrice"></span></button></div>
<script type="application/json" id="pdata">{json.dumps(pdata)}</script>
"""
    return page("carver", "Carver 01 Wedge | Lucky Golf", "Carver 01: a forged 1020 wedge in gold or black. Six lofts, two grinds.", body)


# ================================================================ POLOS
SWATCH = {
    "polo-gold-dust": ["#F7F6F2", "#E3B23C"], "polo-shadow": ["#2B2B2B", "#555"], "polo-signature-black": ["#111"],
    "polo-contour": ["#F7F7F5"], "polo-marble": ["#F5F4EF", "#E3B23C"], "polo-gold-carnation": ["#F1DE92", "#E3B23C"],
    "polo-frost": ["#F2F3F4"], "polo-cruiser": ["#C9D6CF"], "polo-azalea": ["#4C5A5A", "#D98FA6"],
    "polo-nightshade": ["#1B1B1B", "#EDEDED"], "polo-swirl": ["#F7F7F7"], "polo-spot": ["#E7F1EC"], "polo-blackout": ["#222"],
}


def build_polos():
    c = COLL["polos"]
    cards = []
    for i, pid in enumerate(c["products"]):
        p = PROD[pid]
        collar = "Classic collar" if p["family"] == "polo-classic" else "Blade collar"
        sw = "".join(f'<i style="background:{x}"></i>' for x in SWATCH.get(pid, []))
        cards.append(
            f'<a class="card" data-pid="{pid}" {SOON}="Polo product pages come in the next round." data-fam="{p["family"]}" data-i="{i}" data-name="{esc(p["name"])}">'
            f'<div class="ph"><img src="{pack(pid)}" alt="{esc(p["name"])}" width="1200" height="1500" loading="{"eager" if i < 4 else "lazy"}"></div>'
            f'<div class="tx"><span class="nm">{esc(p["name"].replace(" Classic Polo", "").replace(" Blade Polo", ""))}</span><span class="pr">{p["priceLabel"]}</span><span class="ln">{collar}</span></div></a>')
    facets = "".join(f'<button class="chip" type="button" data-facet="{f["k"]}">{f["label"]}</button>' for f in c["facets"])
    fam = {x: copy("_family-" + x) for x in ("polo-classic", "polo-blade")}
    hats = "".join(card(h, "Five-panel snapback", None) for h in COLL["hats"]["products"][:4])
    body = f"""
<div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{BUILT['home']}">Home</a> / <a {SOON}>Apparel</a> / <span aria-current="page">Polos</span></nav>
  <header class="phead">
    <div><span class="label">{c['eyebrow']}</span><h1 class="disp d-l">Polos</h1><p class="lede">{c['lede']}</p></div>
    <p class="count">{len(c['products'])} prints &middot; {PROD[c['products'][0]]['priceLabel']} each<br>Sizes S to 3XL</p>
  </header>
</div>
<div class="bar"><div class="wrap">
  <div class="chips" role="group" aria-label="Collar"><button class="chip" type="button" data-facet="all">All <span class="muted">&nbsp;<span id="shown"></span></span></button>{facets}</div>
  <label><span class="sr">Sort</span><select id="sort"><option value="featured">Featured</option><option value="az">Name, A to Z</option></select></label>
</div></div>
<div class="wrap">
  <div class="pgrid" id="pgrid">{''.join(cards)}</div>
</div>

<section class="sec tight" style="background:var(--tile)"><div class="wrap">
  <div class="head"><div><span class="label">The polo</span><h2 class="disp d-m">{fam['polo-classic'].get('pieceHeadline', 'Cut to play in')}</h2></div></div>
  <div class="fourup quad" style="margin-top:0">{''.join(f'<div><b>{x["k"]}</b><span>{x["v"]}</span></div>' for x in fam['polo-classic']['four'])}</div>
  <p class="tnote">Blade collar polos swap the three-button placket for a clean collar with no buttons. Same fabric, same fit.</p>
</div></section>

<section class="sec tight"><div class="wrap">
  <div class="head"><div><span class="label">Finish it off</span><h2 class="disp d-m">Hats</h2></div><a class="link" {SOON}>All {COLL['hats']['count']} hats</a></div>
  <div class="row four scroll">{hats}</div>
</div></section>

{signoff('Thirteen prints, and none of them shout. The gold is on the clubs.', 'Back to the polos', '#pgrid')}
"""
    return page("polos", "Polos | Lucky Golf", c["lede"], body)


# ================================================================ main
def main():
    os.makedirs(OUT, exist_ok=True)
    for f in ("site.css", "site.js"):
        shutil.copy(os.path.join(V4, "src", f), os.path.join(OUT, f))
    for f in ("mags-light.webp", "mags.webp"):
        shutil.copy(os.path.join(ROOT, "img", f), os.path.join(OUT, "img", f))
    pages = {"home.html": build_home(), "carver-01.html": build_carver(), "polos.html": build_polos()}
    for name, doc in pages.items():
        if "—" in doc or "&mdash;" in doc:
            fail(f"{name}: em dash in output")
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(doc)
    if ERR:
        print("BUILD FAILED\n  " + "\n  ".join(ERR), file=sys.stderr)
        sys.exit(1)
    print(f"built {', '.join(pages)} | club line {LINE_AVG} from {LINE_N} reviews")


if __name__ == "__main__":
    main()
