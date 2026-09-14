"""
v7 collection pages: a club collection built to compare, a polo collection
built to browse. Both sit inside the August site's own shell (header, footer,
bag drawer, tokens, type), taken byte for byte from 10-collection-clubs.html
at 8d78d99, so they match the home page Cole approved. Colour comes later.

    python v7/tools/build-collections.py   -> v7/raw/clubs-v7.html, v7/raw/polos-v7.html
    python v7/tools/build.py               -> finishes them into v7/out with the rest

Every price, rating, stock state, size and spec is read from _src/data. A spec
that is not in the data does not appear; nothing is filled in by hand.
"""
import html
import json
import os
import re
import subprocess

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V7, ".."))
DATA = os.path.join(ROOT, "_src", "data")
RAW = os.path.join(V7, "raw")
IMG = os.path.join(V7, "out", "img")
PACKS = os.path.join(ROOT, "v4", "out", "img")
PHOTOS = os.path.join(ROOT, "v4", "img-raw")

esc = lambda s: html.escape(s, quote=True)
J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
CAT = J(DATA, "products.json")
P = {p["id"]: p for p in CAT["products"]}
C = {c["id"]: c for c in CAT["collections"]}
copy = lambda pid: J(DATA, "copy", pid + ".json")
HREF = {"lgw01-gold": "carver-white.html"}
href = lambda pid: HREF.get(pid, f"20-product-{pid}.html")


def git_show(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], cwd=ROOT).decode("utf-8")


def shell(title):
    s = git_show("8d78d99", "10-collection-clubs.html")
    head = s[:s.index("</header>") + len("</header>")]
    foot = s[s.index("<!-- ============ FOOTER ============ -->"):]
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1, flags=re.S)
    return head, foot


def stars(avg, cls="v7-stars"):
    one = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>'
    return (f'<span class="{cls}" style="--pct:{avg / 5 * 100:.1f}%" role="img" aria-label="{avg:.2f} out of 5">'
            f'<span class="bg">{one * 5}</span><span class="fg">{one * 5}</span></span>')


def img_copy(name):
    src = os.path.join(PACKS, name)
    os.makedirs(IMG, exist_ok=True)
    Image.open(src).save(os.path.join(IMG, name), "WEBP", quality=82)
    return "img/" + name


def photo(raw, dest, w, h, focus=(0.5, 0.5)):
    im = Image.open(os.path.join(PHOTOS, raw)).convert("RGB")
    t = w / h
    if im.width / im.height > t:
        nw = round(im.height * t); x = int(min(max(im.width * focus[0] - nw / 2, 0), im.width - nw))
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = round(im.width / t); y = int(min(max(im.height * focus[1] - nh / 2, 0), im.height - nh))
        im = im.crop((0, y, im.width, y + nh))
    im.resize((w, h), Image.LANCZOS).save(os.path.join(IMG, dest), "WEBP", quality=80)
    return "img/" + dest


def find_review(pid, name):
    for s in J(DATA, "reviews", pid + ".json")["sample"]:
        if s["n"] == name:
            return s
    raise SystemExit(f"review {name} not found for {pid}")


# ===================================================================== CLUBS
def sold_out(pid):
    return [k for k, v in P[pid]["variants"].items() if not v["avail"]]


def labels(pid, key):
    for o in P[pid]["options"]:
        if o["key"] == key:
            return [v["label"] for v in o["values"]]
    return []


def stock_line(pid):
    p = P[pid]
    if not p.get("inStock"):
        return '<span class="v7-stock out">Sold out</span>'
    out = sold_out(pid)
    if not out:
        return '<span class="v7-stock">In stock &middot; ships in 1 to 2 days</span>'
    return f'<span class="v7-stock">In stock &middot; {len(out)} of {len(p["variants"])} options sold out</span>'


def club_facts():
    """Every value below is read from products.json and the product copy files."""
    gold, black = P["lgw01-gold"], P["lgw01-black"]
    g_spec = copy("lgw01-gold")["specs"]["grindTables"][0]
    bounces = sorted({int(re.sub(r"\D", "", v)) for v in g_spec["rows"][0]["v"]})
    hands = lambda pid: " & ".join(h.replace(" hand", "") for h in labels(pid, "hand")) + (" hand" if len(labels(pid, "hand")) == 1 else "")
    grinds = lambda pid: sorted({l.split()[-1] for l in labels(pid, "loftgrind")})
    lofts = lambda pid: sorted({int(re.sub(r"\D", "", l.split()[0])) for l in labels(pid, "loftgrind")})

    def kv(pid):
        rows = copy(pid)["specs"]["kvTables"][0]
        head = rows["rows"][0]["v"]
        extra = {r["k"]: r["v"][0] for r in rows["rows"][1:]}
        return rows["cols"], head, extra

    def out_text(pid):
        out = sold_out(pid)
        if not P[pid].get("inStock"):
            return "Sold out"
        if not out:
            return "Everything in stock"
        pretty = [o.replace("RH|", "RH ").replace("LH|", "LH ") for o in out]
        return "In stock. Sold out: " + ", ".join(pretty)

    bl_cols, bl_head, bl_x = kv("lgp01-gold")
    ml_cols, ml_head, ml_x = kv("lgp02-gold")
    hy_cols, hy_head, hy_x = kv("lgh01")
    wedge = {
        "Price": [gold["priceLabel"], black["priceLabel"]],
        "Rating": [f'{gold["rating"]["avg"]} &middot; {gold["rating"]["count"]} reviews', "Shares the Gold's reviews"],
        "Finish": ["Gold", "Black, gold clover and stamp"],
        "Lofts": [f"{len(lofts(x))} lofts, {min(lofts(x))} to {max(lofts(x))}&deg;" for x in ("lgw01-gold", "lgw01-black")],
        "Grinds": [" and ".join(grinds(x)) for x in ("lgw01-gold", "lgw01-black")],
        "Hand": [hands("lgw01-gold"), hands("lgw01-black")],
        "Head": ["Forged 1020 carbon steel"] * 2,
        "Bounce": [f"{bounces[0]} to {bounces[-1]}&deg;, by loft"] * 2,
        "Stock": [out_text("lgw01-gold"), out_text("lgw01-black")],
    }
    putter = {
        "Price": [P["lgp01-gold"]["priceLabel"], P["lgp02-gold"]["priceLabel"]],
        "Rating": [f'{P[x]["rating"]["avg"]} &middot; {P[x]["rating"]["count"]} reviews' for x in ("lgp01-gold", "lgp02-gold")],
        "Head": ["Blade", "Mallet"],
        "Gives you": ["Feel. Tells you exactly where you hit it", "Forgiveness. Off-centre strikes hold their line"],
        "Material": [bl_x["Head material"], ml_x["Head material"]],
        "Head weight": [bl_head[2], ml_head[2]],
        "Loft": [bl_head[0], ml_head[0]],
        "Lie": [bl_head[1], ml_head[1]],
        "Length": [bl_head[3], ml_head[3]],
        "Hand": [hands("lgp01-gold"), hands("lgp02-gold")],
        "Stock": [out_text("lgp01-gold"), out_text("lgp02-gold")],
    }
    hybrid = [("Loft", "19&deg;"), ("Lie", hy_head[0]), ("Head weight", hy_head[1]), ("Length", hy_head[2]),
              ("Head", hy_x["Head material"]), ("Face", hy_x["Face"]), ("Hand", hands("lgh01"))]
    compare = {
        "lgw01-gold": {"Type": "Wedge", "Price": gold["priceLabel"], "Material": "Forged 1020 carbon steel", "Loft": "50 to 60&deg;, six lofts", "Hand": hands("lgw01-gold"), "Rating": f'{gold["rating"]["avg"]} ({gold["rating"]["count"]})', "Stock": out_text("lgw01-gold")},
        "lgw01-black": {"Type": "Wedge", "Price": black["priceLabel"], "Material": "Forged 1020 carbon steel", "Loft": "50 to 60&deg;, six lofts", "Hand": hands("lgw01-black"), "Rating": "Shares the Gold's", "Stock": out_text("lgw01-black")},
        "lgp01-gold": {"Type": "Blade putter", "Price": P["lgp01-gold"]["priceLabel"], "Material": bl_x["Head material"], "Loft": bl_head[0], "Hand": hands("lgp01-gold"), "Rating": f'{P["lgp01-gold"]["rating"]["avg"]} ({P["lgp01-gold"]["rating"]["count"]})', "Stock": out_text("lgp01-gold")},
        "lgp02-gold": {"Type": "Mallet putter", "Price": P["lgp02-gold"]["priceLabel"], "Material": ml_x["Head material"], "Loft": ml_head[0], "Hand": hands("lgp02-gold"), "Rating": f'{P["lgp02-gold"]["rating"]["avg"]} ({P["lgp02-gold"]["rating"]["count"]})', "Stock": out_text("lgp02-gold")},
        "lgh01": {"Type": "Hybrid", "Price": P["lgh01"]["priceLabel"], "Material": "Titanium", "Loft": "19&deg;", "Hand": hands("lgh01"), "Rating": f'{P["lgh01"]["rating"]["avg"]} ({P["lgh01"]["rating"]["count"]})', "Stock": out_text("lgh01")},
    }
    return wedge, putter, hybrid, compare


CARD_LINE = {
    "lgw01-gold": ("Best seller", "Six lofts, two grinds, either hand. The one most golfers start with."),
    "lgw01-black": ("New", "The same forged head, blacked out. K grind, right hand."),
    "lgp01-gold": (None, "A blade that tells you exactly where the putt came off the face."),
    "lgp02-gold": (None, "More head behind the ball, so the ones you miss still hold their line."),
    "lgh01": (None, "Nineteen degrees of titanium for the shot your long irons keep missing."),
}
CHIPS = {
    "lgw01-gold": ["50 to 60&deg;", "K or S grind", "RH &amp; LH"],
    "lgw01-black": ["50 to 60&deg;", "K grind", "RH"],
    "lgp01-gold": ["Blade", "385 g", "35&Prime;"],
    "lgp02-gold": ["Mallet", "365 g", "35&Prime;"],
    "lgh01": ["19&deg;", "Titanium", "RH &amp; LH"],
}


def club_card(pid):
    p = P[pid]
    tag, line = CARD_LINE[pid]
    out = not p.get("inStock")
    if out:
        tag = "Sold out"
    r = p["rating"]
    chips = "".join(f"<li>{c}</li>" for c in CHIPS[pid])
    return f"""<article class="v7-card{' is-out' if out else ''}" data-pid="{pid}">
  <a class="v7-card-ph" href="{href(pid)}">{f'<span class="v7-tag{" out" if out else ""}">{tag}</span>' if tag else ''}<img src="{img_copy(pid + '-pack.webp')}" alt="{esc(p['name'])}" width="1200" height="1500" loading="lazy"></a>
  <div class="v7-card-bd">
    <div class="v7-card-top"><h3><a href="{href(pid)}">{esc(p['name'])}</a></h3><b>{p['priceLabel']}</b></div>
    <a class="v7-rate" href="{href(pid)}#reviews">{stars(r['avg'])}<span>{r['avg']} &middot; {r['count']}</span></a>
    <p>{line}</p>
    <ul class="v7-chips">{chips}</ul>
    {stock_line(pid)}
    <div class="v7-card-act">
      <a class="btn btn-foil btn-sm" href="{href(pid)}"><span>{'See it' if out else 'Shop'}</span><span class="ar">&rarr;</span></a>
    </div>
  </div>
</article>"""


def h2h(title, pids, rows):
    heads = "".join(f'<th scope="col"><a href="{href(pid)}"><img src="img/{pid}-pack.webp" alt="" width="1200" height="1500" loading="lazy"><span>{esc(P[pid]["name"])}</span></a></th>' for pid in pids)
    body = []
    for k, vals in rows.items():
        same = len(set(vals)) == 1
        cells = f'<td colspan="{len(vals)}" class="same">{vals[0]} <em>Same on both</em></td>' if same else "".join(f"<td>{v}</td>" for v in vals)
        body.append(f'<tr class="{"is-same" if same else "is-diff"}"><th scope="row">{k}</th>{cells}</tr>')
    return f"""<div class="v7-h2h">
  <div class="v7-h2h-hd"><h3>{title}</h3><label class="v7-diff"><input type="checkbox" data-diff> Only show differences</label></div>
  <div class="v7-tablewrap"><table><thead><tr><th></th>{heads}</tr></thead><tbody>{''.join(body)}</tbody></table></div>
</div>"""


def build_clubs():
    wedge, putter, hybrid, compare = club_facts()
    bands = {b["label"]: b for b in copy("_collection-clubs")["bands"]}
    avg_n = sum(P[x]["rating"]["count"] for x in ("lgw01-gold", "lgp01-gold", "lgp02-gold", "lgh01"))
    avg = sum(P[x]["rating"]["avg"] * P[x]["rating"]["count"] for x in ("lgw01-gold", "lgp01-gold", "lgp02-gold", "lgh01")) / avg_n
    hy_help = copy("lgh01")["help"]["cards"]
    faqs = [
        ("Which wedge loft should I start with?", copy("lgw01-gold")["helpLoft"]["sub"]),
        ("K grind or S grind?", copy("lgw01-gold")["help"]["sub"]),
        ("Blade or mallet?", copy("lgp01-gold")["help"]["sub"] + " " + copy("lgp01-gold")["help"]["note"]),
        ("What does the hybrid replace?", copy("lgh01")["help"]["sub"] + " " + copy("lgh01")["help"]["note"]),
        ("What if it's not the one?", "Sixty days to decide on any club. Returns need approval and a photo first, and the club has to come back unmarked."),
    ]

    wedge_ph = photo("lucky-carver-gold-address.webp", "cl-wedges.webp", 1200, 1500, (0.5, 0.6))
    putt_ph = photo("lucky-putters-downline.webp", "cl-putters.webp", 1200, 1500, (0.5, 0.55))
    hy_ph = photo("lucky-stryker-hero.webp", "cl-hybrid.webp", 1600, 1000, (0.45, 0.5))

    def band_tile(img, n, unit, q, alt):
        return f"""<div class="v7-band-ph"><img src="{img}" alt="{alt}" loading="lazy"><div><span class="v7-n">{n}<small>{unit}</small></span><span>{q}</span></div></div>"""

    reviews = [("lgw01-gold", "Eric F."), ("lgp02-gold", "Kyle K."), ("lgh01", "LB06")]
    qs = "".join(
        f'<figure class="v7-q">{stars(s["r"])}<blockquote>&ldquo;{esc(" ".join(s["q"].split()))}&rdquo;</blockquote><figcaption><b>{esc(s["n"])}</b> &middot; {esc(P[pid]["name"])} &middot; verified buyer</figcaption></figure>'
        for pid, name in reviews for s in [find_review(pid, name)])

    body = f"""
<nav class="crumb wrap" aria-label="Breadcrumb"><ol><li><a href="home.html">Home</a></li><li><span aria-current="page">Clubs</span></li></ol></nav>

<section class="v7-head wrap">
  <div>
    <p class="eyebrow">The full bag</p>
    <h1 class="disp d-xl">Clubs</h1>
    <p class="body lead">{C['clubs']['lede']}</p>
  </div>
  <ul class="v7-proof">
    <li><b>{len(C['clubs']['products'])}</b><span>clubs</span></li>
    <li><b>{avg:.2f}</b><span>{stars(avg)} {avg_n} reviews</span></li>
    <li><b>60</b><span>days to decide</span></li>
  </ul>
</section>

<div class="v7-bar" id="v7bar"><div class="wrap v7-bar-in">
  <nav class="v7-jump" aria-label="Jump to">
    <a href="#wedges">Wedges <i>2</i></a><a href="#putters">Putters <i>2</i></a><a href="#hybrid">Hybrid <i>1</i></a>
  </nav>
  <span class="v7-bar-note">Every category has a side-by-side under it</span>
</div></div>

<section class="v7-band wrap" id="wedges">
  <header class="v7-band-hd"><div><p class="eyebrow">Inside 100 yards</p><h2 class="disp d-l">Wedges</h2></div><p class="body">{bands['Wedges']['lede'].replace(' The true 02 is coming.', '')}</p></header>
  <div class="v7-band-grid">
    {band_tile(wedge_ph, 100, 'yds', 'Inside a hundred yards', 'Carver 01 Gold at address on the fairway')}
    {club_card('lgw01-gold')}
    {club_card('lgw01-black')}
  </div>
  {h2h('Gold or Black: what actually changes', ['lgw01-gold', 'lgw01-black'], wedge)}
</section>

<section class="v7-band wrap" id="putters">
  <header class="v7-band-hd"><div><p class="eyebrow">On the green</p><h2 class="disp d-l">Putters</h2></div><p class="body">{bands['Putters']['lede']}</p></header>
  <div class="v7-band-grid">
    {band_tile(putt_ph, 8, 'ft', 'The putts you should make', 'Tracer putter behind the ball on the green')}
    {club_card('lgp01-gold')}
    {club_card('lgp02-gold')}
  </div>
  {h2h('Blade or Mallet: what actually changes', ['lgp01-gold', 'lgp02-gold'], putter)}
</section>

<section class="v7-band wrap" id="hybrid">
  <header class="v7-band-hd"><div><p class="eyebrow">The long approach</p><h2 class="disp d-l">Hybrid</h2></div><p class="body">{bands['Hybrid']['lede']}</p></header>
  <div class="v7-band-grid v7-band-grid--one">
    {band_tile(hy_ph, 210, 'yds', 'Still a long way out', 'Stryker hybrid on the course')}
    {club_card('lgh01')}
  </div>
  <div class="v7-hy">
    <dl class="v7-specs">{''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in hybrid)}</dl>
    <div class="v7-replace">{''.join(f'<div><span class="v7-pill">{c["pill"]}</span><h4>{c["name"]}</h4><p>{c["body"]}</p></div>' for c in hy_help)}</div>
  </div>
</section>

<section class="v7-reviews"><div class="wrap">
  <div class="v7-band-hd"><div><p class="eyebrow">Reviews</p><h2 class="disp d-l">{avg:.2f} from {avg_n} golfers</h2></div><p class="body">Real buyers, word for word, one from each part of the bag.</p></div>
  <div class="v7-qs">{qs}</div>
</div></section>

<ul class="v7-trust wrap"><li><b>Sixty days</b> to decide on any club</li><li><b>Ships</b> in 1 to 2 business days</li><li><b>Shop Pay</b> split it at checkout</li></ul>

<section class="v7-faq wrap"><header class="v7-band-hd"><div><p class="eyebrow">Still deciding</p><h2 class="disp d-m">Which one is mine?</h2></div></header>
<div class="v7-faq-list">
{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)}
</div></section>
"""
    head, foot = shell("Clubs · Lucky Golf")
    doc = head + body + foot
    doc = doc.replace("</head>", f"<style>{CSS_COMMON}{CSS_CLUBS}</style>\n</head>", 1).replace("</body>", f"<script>{JS_CLUBS}</script>\n</body>")
    open(os.path.join(RAW, "clubs-v7.html"), "w", encoding="utf-8").write(doc)


# ===================================================================== POLOS
FAMILY = {  # print name -> colour family, read off each product photo
    "polo-gold-dust": "light", "polo-contour": "light", "polo-frost": "light", "polo-marble": "light",
    "polo-swirl": "light", "polo-spot": "light",
    "polo-shadow": "dark", "polo-signature-black": "dark", "polo-nightshade": "dark", "polo-blackout": "dark",
    "polo-gold-carnation": "colour", "polo-cruiser": "colour", "polo-azalea": "colour",
}


def polo_card(pid, i):
    p = P[pid]
    collar = "Classic" if p["family"] == "polo-classic" else "Blade"
    name = p["name"].replace(" Classic Polo", "").replace(" Blade Polo", "")
    sizes = p["options"][0]["values"]
    avail = [s["k"] for s in sizes if p["variants"][s["k"]]["avail"]]
    img = img_copy(pid + "-pack.webp")
    btns = "".join(
        (f'<button type="button" data-add data-sku="{esc(p["variants"][s["k"]]["sku"])}" data-name="{esc(p["name"])}" data-price="{p["priceLabel"]}" data-img="{img}" data-variant="{s["label"]}"><span>{s["label"]}</span></button>'
         if p["variants"][s["k"]]["avail"] else f'<button type="button" disabled aria-label="{s["label"]} sold out"><s>{s["label"]}</s></button>')
        for s in sizes)
    few = len(avail) < len(sizes)
    note = f'Sold out in {", ".join(s["label"] for s in sizes if s["k"] not in avail)}' if few else "Every size in stock"
    return f"""<article class="v7-polo" data-i="{i}" data-collar="{collar.lower()}" data-colour="{FAMILY[pid]}" data-name="{esc(name)}" data-sizes="{' '.join(avail)}">
  <div class="v7-polo-ph">
    <a href="{href(pid)}" tabindex="-1" aria-hidden="true"><img src="{img}" alt="{esc(p['name'])}" width="1200" height="1500" loading="{'eager' if i < 8 else 'lazy'}"></a>
    <button class="v7-qa-open" type="button" aria-label="Quick add {esc(p['name'])}" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></button>
    <div class="v7-qa"><span>Add a size</span><div class="v7-sizes">{btns}</div></div>
  </div>
  <a class="v7-polo-bd" href="{href(pid)}"><span class="nm">{esc(name)}</span><b>{p['priceLabel']}</b><span class="meta">{collar} collar</span><span class="stock{' few' if few else ''}">{note}</span></a>
</article>"""


def build_polos():
    ids = C["polos"]["products"]
    fam = copy("_family-polo-classic")
    cards = [polo_card(pid, i) for i, pid in enumerate(ids)]
    fit_tile = f"""<aside class="v7-fit-tile" data-tile><p class="eyebrow">Every polo, same shirt</p><ul>{''.join(f'<li><b>{x["k"]}</b><span>{x["v"]}</span></li>' for x in fam['four'][1:])}</ul><p class="v7-fit-note">{fam['fitParas'][1]}</p></aside>"""
    cards.insert(4, fit_tile)
    blade = copy("_family-polo-blade")
    faqs = [
        ("How does it fit?", " ".join(fam["fitParas"])),
        ("Classic collar or Blade collar?", " ".join(blade["pieceParas"])),
        ("What is it made of?", " ".join(x["k"] + ": " + x["v"] for x in fam["fabric"])),
        ("What if the size is wrong?", "Apparel returns within 30 days, unworn with the tags on."),
    ]
    counts = {"classic": sum(P[x]["family"] == "polo-classic" for x in ids), "blade": sum(P[x]["family"] == "polo-blade" for x in ids),
              "dark": sum(FAMILY[x] == "dark" for x in ids)}
    tiles = [("collar", "classic", "Classic collar", "Three-button placket", "polo-gold-dust", counts["classic"]),
             ("collar", "blade", "Blade collar", "No buttons, no placket", "polo-swirl", counts["blade"]),
             ("colour", "dark", "Dark prints", "Black and charcoal", "polo-shadow", counts["dark"])]
    style_tiles = "".join(
        f'<button class="v7-style" type="button" data-f="{k}" data-v="{v}" aria-pressed="false"><span class="ph"><img src="img/{img}-pack.webp" alt="" loading="eager"></span><span class="tx"><b>{t}</b><span>{sub} &middot; {n} polos</span></span></button>'
        for k, v, t, sub, img, n in tiles)
    hats = C["hats"]["products"][:4]
    hat_cards = "".join(
        f'<a class="v7-hat" href="{href(h)}"><span class="ph"><img src="{img_copy(h + "-pack.webp")}" alt="{esc(P[h]["name"])}" loading="lazy"></span><span class="nm">{esc(P[h]["name"])}</span><b>{P[h]["priceLabel"]}</b></a>'
        for h in hats)
    sizes = [v["label"] for v in P[ids[0]]["options"][0]["values"]]
    body = f"""
<nav class="crumb wrap" aria-label="Breadcrumb"><ol><li><a href="home.html">Home</a></li><li><span aria-current="page">Polos</span></li></ol></nav>

<section class="v7-head v7-head--tight wrap">
  <div>
    <p class="eyebrow">{C['polos']['eyebrow']}</p>
    <h1 class="disp d-xl">Polos</h1>
    <p class="body lead">{C['polos']['lede']}</p>
  </div>
  <ul class="v7-proof">
    <li><b>{len(ids)}</b><span>prints</span></li>
    <li><b>{P[ids[0]]['priceLabel']}</b><span>every polo, every size</span></li>
    <li><b>{sizes[0]} to {sizes[-1]}</b><span>sizes</span></li>
  </ul>
</section>

<section class="v7-styles wrap" aria-label="Shop by style">{style_tiles}</section>

<div class="v7-bar v7-filters" id="v7bar"><div class="wrap v7-bar-in">
  <div class="v7-fgroup" role="group" aria-label="Collar"><span class="lbl">Collar</span><button type="button" data-f="collar" data-v="" aria-pressed="true">All</button><button type="button" data-f="collar" data-v="classic" aria-pressed="false">Classic</button><button type="button" data-f="collar" data-v="blade" aria-pressed="false">Blade</button></div>
  <div class="v7-fgroup" role="group" aria-label="Colour"><span class="lbl">Colour</span><button type="button" data-f="colour" data-v="" aria-pressed="true">All</button><button type="button" data-f="colour" data-v="light" aria-pressed="false"><i class="sw light"></i>Light</button><button type="button" data-f="colour" data-v="dark" aria-pressed="false"><i class="sw dark"></i>Dark</button><button type="button" data-f="colour" data-v="colour" aria-pressed="false"><i class="sw colour"></i>Colour</button></div>
  <div class="v7-fgroup" role="group" aria-label="In stock in my size"><span class="lbl">My size</span>{''.join(f'<button type="button" data-f="size" data-v="{s}" aria-pressed="false">{s}</button>' for s in sizes)}</div>
  <div class="v7-fright"><span class="v7-count"><b id="v7shown">{len(ids)}</b> of {len(ids)}</span><label class="v7-sort"><span class="sr">Sort</span><select id="v7sort"><option value="featured">Featured</option><option value="az">Name A to Z</option><option value="stock">Most sizes in stock</option></select></label></div>
</div></div>

<section class="wrap v7-pgrid-wrap">
  <div class="v7-pgrid" id="v7grid">{''.join(cards)}</div>
  <p class="v7-empty" id="v7empty" hidden>No polos match. <button type="button" data-f-reset>Clear filters</button></p>
</section>

<section class="v7-faq wrap" style="padding-top:clamp(8px,2vw,24px)"><header class="v7-band-hd"><div><p class="eyebrow">Before you pick</p><h2 class="disp d-m">Fit, fabric and returns</h2></div><p class="body">{fam['closeBody']}</p></header>
<div class="v7-faq-list">{''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)}</div></section>

<section class="v7-hats wrap">
  <header class="v7-band-hd"><div><p class="eyebrow">Finish it off</p><h2 class="disp d-m">Hats</h2></div><a class="btn btn-line btn-sm" href="10-collection-hats.html"><span>All {C['hats']['count']} hats</span><span class="ar">&rarr;</span></a></header>
  <div class="v7-hat-row">{hat_cards}</div>
</section>
"""
    head, foot = shell("Polos · Lucky Golf")
    doc = head + body + foot
    doc = doc.replace("</head>", f"<style>{CSS_COMMON}{CSS_POLOS}</style>\n</head>", 1).replace("</body>", f"<script>{JS_POLOS}</script>\n</body>")
    open(os.path.join(RAW, "polos-v7.html"), "w", encoding="utf-8").write(doc)


# ===================================================================== CSS / JS
CSS_COMMON = r"""
.btn-foil{background-image:var(--lg-foil-tag)}
.v7-polo,.v7-card{min-width:0}
.v7-stars{position:relative;display:inline-block;line-height:0;vertical-align:-2px}
.v7-stars .bg,.v7-stars .fg{display:flex;gap:2px}
.v7-stars svg{width:13px;height:13px;flex:none}
.v7-stars .bg svg{fill:rgba(23,20,15,.16)}
.v7-stars .fg{position:absolute;inset:0 auto 0 0;width:var(--pct);overflow:hidden}
.v7-stars .fg svg{fill:var(--gold)}
.v7-head{display:grid;grid-template-columns:1.3fr 1fr;gap:24px 60px;align-items:end;padding-top:clamp(20px,3vw,40px);padding-bottom:clamp(28px,3.4vw,48px)}
.v7-head h1{margin:0}
.v7-head .lead{margin-top:18px;max-width:52ch}
.v7-proof{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,1fr);border-top:2px solid var(--ink)}
.v7-proof li{padding:16px 12px 0 0;display:flex;flex-direction:column;gap:4px}
.v7-proof b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(1.8rem,3vw,2.6rem);line-height:.9}
.v7-proof span{color:var(--ink-muted);font-size:var(--fs-lg);display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.v7-bar{position:sticky;top:var(--hdr-h,72px);z-index:40;background:rgba(255,255,255,.96);backdrop-filter:blur(8px);border-block:1px solid var(--ink-08)}
.v7-bar-in{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:10px 24px;min-height:62px;padding-block:8px}
.v7-band-hd{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-end;gap:14px 48px;margin-bottom:clamp(20px,2.6vw,36px)}
.v7-band-hd h2{margin:0}
.v7-band-hd .body{max-width:48ch;margin:0}
.v7-pill{display:inline-block;background:var(--ink);color:var(--cream);border-radius:4px;padding:4px 9px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:var(--fs-xs)}
.v7-faq{padding-block:0 clamp(56px,6vw,96px)}
.v7-faq-list{border-top:2px solid var(--ink)}
.v7-faq details{border-bottom:1px solid var(--ink-14)}
.v7-faq summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:16px;min-height:60px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 74;font-weight:800;text-transform:uppercase;font-size:var(--fs-body)}
.v7-faq summary::-webkit-details-marker{display:none}
.v7-faq summary::after{content:'+';font-size:26px;font-weight:400}
.v7-faq details[open] summary::after{content:'\2013'}
.v7-faq details p{margin:0 0 18px;max-width:70ch;color:var(--ink-70);line-height:1.6}
.sr{position:absolute;left:0;top:0;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}
.v7-bar-in{position:relative}
.v7-modal[hidden],.v7-tray[hidden],.v7-empty[hidden]{display:none}
@media (max-width:900px){.v7-head{grid-template-columns:1fr}}
"""

CSS_CLUBS = r"""
.v7-jump{display:flex;gap:8px;flex-wrap:wrap}
.v7-jump a{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;border:1.5px solid var(--ink-14);border-radius:999px;color:var(--ink);text-decoration:none;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 76;font-weight:700;text-transform:uppercase;letter-spacing:.05em;font-size:var(--fs-md)}
.v7-jump a:hover,.v7-jump a.on{border-color:var(--ink);background:var(--ink);color:var(--cream)}
.v7-jump i{font-style:normal;opacity:.6}
.v7-bar-note{color:var(--ink-muted);font-size:var(--fs-lg)}
.v7-band{padding-block:clamp(48px,6vw,96px);border-bottom:1px solid var(--ink-08);scroll-margin-top:140px}
.v7-band-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--gut)}
.v7-band-grid--one{grid-template-columns:2fr 1fr}
.v7-band-ph{position:relative;border-radius:var(--r-card);overflow:hidden;min-height:100%;background:var(--ink)}
.v7-band-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.v7-band-ph::after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(23,20,15,.82) 0%,rgba(23,20,15,.25) 45%,rgba(23,20,15,0) 70%)}
.v7-band-ph>div{position:absolute;left:0;right:0;bottom:0;z-index:1;padding:clamp(18px,2.2vw,30px);color:var(--cream);display:flex;flex-direction:column;gap:6px}
.v7-n{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(3.4rem,6vw,5.6rem);line-height:.82}
.v7-n small{font-size:.34em;margin-left:6px;color:var(--gold-hi)}
.v7-band-ph>div>span:last-child{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 72;font-weight:800;text-transform:uppercase;font-size:var(--fs-lead)}
.v7-card{display:flex;flex-direction:column;border:1px solid var(--ink-08);border-radius:var(--r-card);overflow:hidden;background:var(--white)}
.v7-card-ph{position:relative;display:block;aspect-ratio:4/5;background:#F4F3F0;overflow:hidden}
.v7-card-ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease-out-s)}
.v7-card:hover .v7-card-ph img{transform:scale(1.035)}
.v7-card.is-out .v7-card-ph img{opacity:.6}
.v7-tag{position:absolute;top:12px;left:12px;z-index:1;background:var(--lg-foil-tag);color:var(--ink);border-radius:999px;padding:5px 10px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.1em;font-size:var(--fs-xs)}
.v7-tag.out{background:var(--ink);color:var(--cream)}
.v7-card-bd{padding:18px 18px 20px;display:flex;flex-direction:column;gap:10px;flex:1}
.v7-card-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.v7-card-top h3{margin:0;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:clamp(1.2rem,1.6vw,1.5rem);line-height:1}
.v7-card-top h3 a{color:inherit;text-decoration:none}
.v7-card-top b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 72;font-weight:800;font-size:var(--fs-xl)}
.v7-rate{display:flex;align-items:center;gap:8px;color:var(--ink-muted);font-size:var(--fs-md);text-decoration:none}
.v7-card-bd p{margin:0;color:var(--ink-70);font-size:var(--fs-base);line-height:1.5}
.v7-chips{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px}
.v7-chips li{border:1px solid var(--ink-14);border-radius:4px;padding:4px 8px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 80;font-weight:600;font-size:var(--fs-md)}
.v7-stock{font-size:var(--fs-md);color:var(--green)}
.v7-stock.out{color:var(--ink-muted)}
.v7-card-act{margin-top:auto;padding-top:6px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.v7-cmp{display:inline-flex;align-items:center;gap:8px;cursor:pointer;min-height:44px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:var(--fs-md)}
.v7-cmp input{width:18px;height:18px;accent-color:var(--ink)}
.v7-h2h{margin-top:clamp(24px,3vw,40px)}
.v7-h2h-hd{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px;margin-bottom:12px}
.v7-h2h-hd h3{margin:0;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:800;text-transform:uppercase;font-size:var(--fs-xl)}
.v7-diff{display:inline-flex;gap:8px;align-items:center;font-size:var(--fs-lg);color:var(--ink-70);cursor:pointer}
.v7-diff input{width:17px;height:17px;accent-color:var(--ink)}
.v7-tablewrap{overflow-x:auto;border:1px solid var(--ink-08);border-radius:var(--r-card)}
.v7-h2h table,.v7-modal table{width:100%;border-collapse:collapse;min-width:560px;font-size:var(--fs-base)}
.v7-h2h th,.v7-h2h td,.v7-modal th,.v7-modal td{padding:13px 16px;text-align:left;border-bottom:1px solid var(--ink-08);vertical-align:top}
.v7-h2h tbody tr:last-child>*{border-bottom:0}
.v7-h2h thead th,.v7-modal thead th{background:#F4F3F0;width:40%}
.v7-h2h thead th:first-child,.v7-modal thead th:first-child{width:20%}
.v7-h2h thead a,.v7-modal thead a{display:flex;align-items:center;gap:12px;color:var(--ink);text-decoration:none;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:800;text-transform:uppercase;font-size:var(--fs-body)}
.v7-h2h thead img,.v7-modal thead img{width:52px;height:64px;object-fit:cover;border-radius:6px;background:#fff}
.v7-h2h tbody th,.v7-modal tbody th{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:var(--fs-sm);color:var(--ink-muted)}
.v7-h2h tr.is-diff td{font-weight:600}
.v7-h2h td.same{color:var(--ink-70)}
.v7-h2h td.same em{font-style:normal;margin-left:8px;color:var(--ink-muted);font-size:var(--fs-md)}
.v7-h2h.only-diff tr.is-same{display:none}
.v7-hy{display:grid;grid-template-columns:1fr 1.2fr;gap:var(--gut);margin-top:clamp(24px,3vw,40px)}
.v7-specs{margin:0;display:grid;grid-template-columns:1fr 1fr;border:1px solid var(--ink-08);border-radius:var(--r-card);overflow:hidden}
.v7-specs div{padding:14px 16px;border-bottom:1px solid var(--ink-08)}
.v7-specs div:nth-child(odd){border-right:1px solid var(--ink-08)}
.v7-specs dt{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:var(--fs-sm);color:var(--ink-muted)}
.v7-specs dd{margin:4px 0 0;font-weight:600}
.v7-replace{display:grid;grid-template-columns:1fr 1fr;gap:var(--gut)}
.v7-replace>div{border:1px solid var(--ink-08);border-radius:var(--r-card);padding:20px}
.v7-replace h4{margin:12px 0 6px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:800;text-transform:uppercase;font-size:var(--fs-lead)}
.v7-replace p{margin:0;color:var(--ink-70);font-size:var(--fs-base);line-height:1.5}
.v7-reviews{padding-block:clamp(56px,6vw,96px)}
.v7-qs{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--gut)}
.v7-q{margin:0;border-top:2px solid var(--ink);padding-top:18px}
.v7-q blockquote{margin:10px 0 12px;font-size:var(--fs-body);line-height:1.5}
.v7-q figcaption{font-size:var(--fs-md);color:var(--ink-muted)}
.v7-q figcaption b{color:var(--ink)}
.v7-trust{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:var(--gut);padding-bottom:clamp(56px,6vw,96px);margin:0 auto}
.v7-trust li{border-top:1px solid var(--ink-14);padding-top:14px;color:var(--ink-70)}
.v7-trust b{color:var(--ink);font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 72;font-weight:800;text-transform:uppercase}
.v7-tray{position:fixed;left:0;right:0;bottom:0;z-index:80;background:var(--ink);color:var(--cream);box-shadow:0 -10px 30px rgba(0,0,0,.2)}
.v7-tray-in{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:10px 20px;padding-block:12px}
.v7-tray-items{display:flex;gap:10px;flex-wrap:wrap}
.v7-tray-items span{display:inline-flex;align-items:center;gap:8px;background:rgba(246,242,232,.1);border-radius:6px;padding:4px 10px 4px 4px;font-size:var(--fs-lg)}
.v7-tray-items img{width:34px;height:42px;object-fit:cover;border-radius:4px;background:#fff}
.v7-tray-act{display:flex;gap:8px}
.v7-tray .btn-line{color:var(--cream);border-color:var(--cream-52)}
.v7-modal{position:fixed;inset:0;z-index:120;display:grid;place-items:center;padding:20px}
.v7-modal-bd{position:absolute;inset:0;background:rgba(23,20,15,.6)}
.v7-modal-panel{position:relative;background:var(--white);border-radius:var(--r-card);padding:28px;max-width:1000px;width:100%;max-height:88vh;overflow:auto}
.v7-modal-panel h2{margin:0 0 18px}
.v7-modal thead th{width:auto}
.v7-x{position:absolute;top:10px;right:12px;width:44px;height:44px;border:0;background:none;font-size:28px;cursor:pointer}
@media (max-width:1100px){.v7-band-grid{grid-template-columns:1fr 1fr}.v7-band-grid .v7-band-ph{grid-column:1/-1;aspect-ratio:16/9}.v7-band-grid--one{grid-template-columns:1fr 1fr}.v7-hy{grid-template-columns:1fr}}
@media (max-width:700px){
  .v7-band-grid,.v7-band-grid--one{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .v7-band-grid .v7-band-ph{aspect-ratio:4/3}
  .v7-card-bd{padding:12px}
  .v7-card-bd p,.v7-chips{display:none}
  .v7-card-top{flex-direction:column;gap:4px}
  .v7-card-act{flex-direction:column;align-items:stretch;gap:4px}
  .v7-card-act .btn{justify-content:center}
  .v7-qs,.v7-trust,.v7-replace{grid-template-columns:1fr}
  .v7-bar-note{display:none}
  .v7-specs{grid-template-columns:1fr 1fr}
  .v7-h2h table{min-width:0;font-size:var(--fs-lg)}
  .v7-h2h th,.v7-h2h td{padding:10px 8px}
  .v7-h2h thead th{width:auto!important}
  .v7-h2h thead a{flex-direction:column;align-items:flex-start;gap:6px;font-size:var(--fs-base)}
  .v7-h2h tbody th{width:26%;font-size:var(--fs-xs);letter-spacing:.06em}
  .v7-h2h td.same em{display:block;margin:2px 0 0}
}
"""

CSS_POLOS = r"""
.v7-head--tight{padding-bottom:clamp(20px,2.4vw,32px)}
.v7-styles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--gut);padding-bottom:clamp(20px,2.4vw,32px)}
.v7-style{display:grid;grid-template-columns:96px 1fr;align-items:center;gap:16px;padding:10px 18px 10px 10px;border:1.5px solid var(--ink-08);border-radius:var(--r-card);background:var(--white);cursor:pointer;text-align:left;font:inherit;color:var(--ink);transition:border-color .2s}
.v7-style:hover,.v7-style[aria-pressed="true"]{border-color:var(--ink)}
.v7-style .ph{aspect-ratio:4/5;border-radius:8px;overflow:hidden;background:#F4F3F0}
.v7-style img{width:100%;height:100%;object-fit:cover}
.v7-style b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:var(--fs-xl);line-height:1}
.v7-style .tx>span{color:var(--ink-muted);font-size:var(--fs-lg)}
.v7-filters .v7-bar-in{justify-content:flex-start}
.v7-fgroup{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.v7-fgroup .lbl{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.12em;font-size:var(--fs-xs);color:var(--ink-muted);margin-right:2px}
.v7-fgroup button{display:inline-flex;align-items:center;gap:6px;min-height:40px;min-width:40px;justify-content:center;padding:0 12px;border:1.5px solid var(--ink-14);border-radius:999px;background:var(--white);cursor:pointer;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 80;font-weight:700;font-size:var(--fs-md)}
.v7-fgroup button[aria-pressed="true"]{background:var(--ink);border-color:var(--ink);color:var(--cream)}
.sw{width:12px;height:12px;border-radius:50%;border:1px solid rgba(23,20,15,.25)}
.sw.light{background:#F2F1ED}.sw.dark{background:#1d1d1d}.sw.colour{background:linear-gradient(135deg,#E9C85A 0 33%,#9FB8AC 33% 66%,#C27A93 66%)}
.v7-fright{margin-left:auto;display:flex;align-items:center;gap:14px}
.v7-count{color:var(--ink-muted);font-size:var(--fs-lg)}
.v7-count b{color:var(--ink)}
.v7-sort select{min-height:40px;border:1.5px solid var(--ink-14);border-radius:999px;padding:0 12px;font:inherit;font-size:var(--fs-lg);background:var(--white)}
.v7-pgrid-wrap{padding-block:clamp(20px,2.6vw,36px) clamp(56px,6vw,96px)}
.v7-pgrid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:clamp(22px,2.4vw,36px) var(--gut)}
.v7-polo[hidden],.v7-fit-tile[hidden]{display:none}
.v7-polo-ph{position:relative;aspect-ratio:4/5;background:#F4F3F0;border-radius:var(--r-card);overflow:hidden}
.v7-polo-ph>a{display:block;height:100%}
.v7-polo-ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--ease-out-s)}
.v7-polo:hover .v7-polo-ph img{transform:scale(1.035)}
.v7-qa-open{position:absolute;right:10px;bottom:10px;z-index:2;width:44px;height:44px;border-radius:50%;border:0;background:var(--white);box-shadow:0 2px 10px rgba(0,0,0,.12);display:grid;place-items:center;cursor:pointer}
.v7-qa-open svg{width:20px;height:20px;stroke:var(--ink);stroke-width:2;fill:none}
.v7-qa{position:absolute;left:8px;right:8px;bottom:8px;z-index:3;background:var(--white);border-radius:10px;padding:10px;box-shadow:0 6px 20px rgba(0,0,0,.14);transform:translateY(calc(100% + 12px));transition:transform .28s var(--ease-out-s)}
.v7-qa>span{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:var(--fs-xs);color:var(--ink-muted);margin-bottom:6px}
.v7-sizes{display:grid;grid-template-columns:repeat(6,1fr);gap:4px}
.v7-sizes button{min-height:38px;border:1.5px solid var(--ink-14);border-radius:6px;background:var(--white);cursor:pointer;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 80;font-weight:700;font-size:var(--fs-sm);padding:0}
.v7-sizes button:hover:not(:disabled){background:var(--ink);color:var(--cream);border-color:var(--ink)}
.v7-sizes button:disabled{color:var(--ink-38);background:#F4F3F0;cursor:not-allowed}
.v7-polo:hover .v7-qa,.v7-polo:focus-within .v7-qa,.v7-polo.qa-on .v7-qa{transform:none}
.v7-polo:hover .v7-qa-open,.v7-polo.qa-on .v7-qa-open{opacity:0;pointer-events:none}
.v7-polo-bd{display:grid;grid-template-columns:1fr auto;gap:2px 10px;padding:12px 2px 0;color:var(--ink);text-decoration:none}
.v7-polo-bd .nm{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:clamp(1.05rem,1.3vw,1.25rem);line-height:1.05}
.v7-polo-bd b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 74;font-weight:700}
.v7-polo-bd .meta{grid-column:1/-1;color:var(--ink-muted);font-size:var(--fs-md)}
.v7-polo-bd .stock{grid-column:1/-1;font-size:var(--fs-md);color:var(--green)}
.v7-polo-bd .stock.few{color:var(--ink-muted)}
.v7-fit-tile{background:var(--ink);color:var(--cream);border-radius:var(--r-card);padding:clamp(20px,2vw,28px);display:flex;flex-direction:column;justify-content:center;aspect-ratio:4/5}
.v7-fit-tile .eyebrow{color:var(--gold-hi)}
.v7-fit-tile ul{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:12px}
.v7-fit-tile li b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:var(--fs-xl);line-height:1}
.v7-fit-tile li span{color:var(--cream-70);font-size:var(--fs-lg)}
.v7-fit-note{margin:16px 0 0;color:var(--cream-70);font-size:var(--fs-md);line-height:1.5}
.v7-empty{padding:40px 0;color:var(--ink-70)}
.v7-empty button{border:0;background:none;text-decoration:underline;cursor:pointer;font:inherit}
.v7-fit{display:grid;grid-template-columns:1fr 1.1fr;gap:24px 60px;padding-block:clamp(56px,6vw,96px);border-top:1px solid var(--ink-08)}
.v7-fit h2{margin:0;max-width:16ch}
.v7-fit-copy p{margin:0 0 12px;color:var(--ink-70);font-size:var(--fs-body);line-height:1.6;max-width:56ch}
.v7-fit-small{font-size:var(--fs-lg)!important}
.v7-hats{padding-bottom:clamp(56px,6vw,96px)}
.v7-hat-row{display:grid;grid-template-columns:repeat(4,1fr);gap:var(--gut)}
.v7-hat{color:var(--ink);text-decoration:none;display:grid;grid-template-columns:1fr auto;gap:2px 10px}
.v7-hat .ph{grid-column:1/-1;aspect-ratio:4/5;background:#F4F3F0;border-radius:var(--r-card);overflow:hidden;margin-bottom:10px}
.v7-hat img{width:100%;height:100%;object-fit:cover}
.v7-hat .nm{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 72;font-weight:800;text-transform:uppercase;font-size:var(--fs-base)}
@media (max-width:1100px){.v7-pgrid{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:760px){
  .v7-pgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 10px}
  .v7-filters .v7-bar-in{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}
  .v7-fgroup{flex-wrap:nowrap}
  .v7-fgroup button{white-space:nowrap}
  .v7-fright{margin-left:0}
  .v7-sizes{grid-template-columns:repeat(3,1fr)}
  .v7-styles{grid-template-columns:1fr;gap:8px}
  .v7-style{grid-template-columns:56px 1fr;padding:6px 12px 6px 6px}
  .v7-style b{font-size:var(--fs-body)}
  .v7-hat-row{grid-template-columns:1fr 1fr}
  .v7-fit-tile li b{font-size:var(--fs-body)}
  .v7-fit-tile .v7-fit-note{display:none}
}
"""

JS_CLUBS = r"""
(function(){
  document.addEventListener('change', function(e){
    var d = e.target.closest('[data-diff]');
    if (d) d.closest('.v7-h2h').classList.toggle('only-diff', d.checked);
  });
  var links = document.querySelectorAll('.v7-jump a');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){ es.forEach(function(en){ if (en.isIntersecting) links.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href') === '#' + en.target.id); }); }); }, {rootMargin:'-35% 0px -60% 0px'});
    document.querySelectorAll('.v7-band').forEach(function(sec){ io.observe(sec); });
  }
})();
"""

JS_POLOS = r"""
(function(){
  var grid = document.getElementById('v7grid');
  var cards = [].slice.call(grid.querySelectorAll('.v7-polo'));
  var tile = grid.querySelector('[data-tile]');
  var f = {collar:'', colour:'', size:''}, sort = 'featured';
  function apply(){
    var shown = cards.filter(function(c){
      return (!f.collar || c.dataset.collar === f.collar) && (!f.colour || c.dataset.colour === f.colour) && (!f.size || c.dataset.sizes.split(' ').indexOf(f.size) > -1);
    });
    cards.forEach(function(c){ c.hidden = shown.indexOf(c) < 0; });
    var order = shown.slice().sort(function(a,b){
      if (sort === 'az') return a.dataset.name.localeCompare(b.dataset.name);
      if (sort === 'stock') return b.dataset.sizes.split(' ').length - a.dataset.sizes.split(' ').length || a.dataset.i - b.dataset.i;
      return a.dataset.i - b.dataset.i;
    });
    order.forEach(function(c, i){ grid.appendChild(c); if (i === 3 && tile) grid.appendChild(tile); });
    if (tile) { tile.hidden = order.length < 6; if (order.length <= 3) grid.appendChild(tile); }
    document.getElementById('v7shown').textContent = shown.length;
    document.getElementById('v7empty').hidden = shown.length > 0;
    document.querySelectorAll('[data-f]').forEach(function(b){ b.setAttribute('aria-pressed', String(f[b.dataset.f] === b.dataset.v)); });
  }
  document.addEventListener('click', function(e){
    var b = e.target.closest('[data-f]');
    if (b) { var k = b.dataset.f, tile = b.classList.contains('v7-style'); f[k] = ((k === 'size' || tile) && f[k] === b.dataset.v) ? '' : b.dataset.v; apply(); if (tile) document.getElementById('v7bar').scrollIntoView({behavior:'smooth'}); return; }
    if (e.target.closest('[data-f-reset]')) { f = {collar:'', colour:'', size:''}; apply(); return; }
    var q = e.target.closest('.v7-qa-open');
    if (q) { var card = q.closest('.v7-polo'); var on = !card.classList.contains('qa-on'); document.querySelectorAll('.v7-polo.qa-on').forEach(function(c){ c.classList.remove('qa-on'); }); card.classList.toggle('qa-on', on); q.setAttribute('aria-expanded', String(on)); return; }
    if (!e.target.closest('.v7-qa')) document.querySelectorAll('.v7-polo.qa-on').forEach(function(c){ c.classList.remove('qa-on'); });
  });
  document.getElementById('v7sort').addEventListener('change', function(e){ sort = e.target.value; apply(); });
  apply();
})();
"""


if __name__ == "__main__":
    build_clubs()
    build_polos()
    print("built v7/raw/clubs-v7.html and v7/raw/polos-v7.html")
