"""
Home v6: a new home page on the August site's system (header, footer, cart,
tokens, type), built from v6/src and the live catalogue.

    python v6/tools/build-home.py        # -> v6/out/home.html + v6/out/img/
    python v5/tools/check.py ...          # (see v6/tools/check.py)

Every number is computed: ratings from the Judge.me pulls, prices and stock
from products.json, big-brand prices from v4/data/price-case.json. Every
review is looked up verbatim by name; a missing one fails the build.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V6, ".."))
SITE = os.path.join(V6, "site")
OUT = os.path.join(V6, "out")
IMG = os.path.join(OUT, "img")
RAW = os.path.join(ROOT, "v4", "img-raw")
PACKS = os.path.join(ROOT, "v4", "out", "img")
DATA = os.path.join(ROOT, "_src", "data")
AUGUST = "8d78d99"

ERR = []


def jload(*p):
    return json.load(open(os.path.join(*p), encoding="utf-8"))


PROD = {p["id"]: p for p in jload(DATA, "products.json")["products"]}
CASE = jload(ROOT, "v4", "data", "price-case.json")
esc = lambda s: html.escape(s, quote=True)


# ------------------------------------------------------------------ site tree
def fresh_site():
    if not os.path.exists(os.path.join(SITE, "tools", "build.py")):
        os.makedirs(SITE, exist_ok=True)
        tar = os.path.join(V6, "august.tar")
        subprocess.check_call(["git", "archive", "--format=tar", "-o", tar, AUGUST, "_src", "_src-logo-symbols.svg", "tools"], cwd=ROOT)
        subprocess.check_call(["tar", "-xf", tar, "-C", SITE])
        os.remove(tar)
    b = os.path.join(SITE, "tools", "build.py")
    s = open(b, encoding="utf-8").read()
    s = re.sub(r'    "home": \[.*?\n    \],', '    "home": [\n        ".msnap{", ".hdr{", ".cd-panel{", "h6-hero",\n    ],', s, count=1, flags=re.S)
    open(b, "w", encoding="utf-8").write(s)


# ------------------------------------------------------------------ images
def crop_to(src, dest, w, h, focus=(0.5, 0.5)):
    im = Image.open(src).convert("RGB")
    target = w / h
    if im.width / im.height > target:
        nw = round(im.height * target)
        x = int(min(max(im.width * focus[0] - nw / 2, 0), im.width - nw))
        im = im.crop((x, 0, x + nw, im.height))
    else:
        nh = round(im.width / target)
        y = int(min(max(im.height * focus[1] - nh / 2, 0), im.height - nh))
        im = im.crop((0, y, im.width, y + nh))
    im = im.resize((w, h), Image.LANCZOS)
    im.save(os.path.join(IMG, dest), "WEBP", quality=80, method=6)


def raw(name):
    p = os.path.join(RAW, name)
    if not os.path.exists(p):
        ERR.append(f"missing raw image {name}")
    return p


def images():
    os.makedirs(IMG, exist_ok=True)
    cache = os.path.join(ROOT, "v5", "img-cache", "10_7d28d460-d8ba-4e34-823b-4969eedb3eaf.webp")
    crop_to(cache, "hero-address.webp", 1600, 1600, (0.55, 0.5))
    crop_to(raw("lucky-carver-gold-address.webp"), "best-address.webp", 1200, 1500, (0.5, 0.6))
    crop_to(raw("lucky-wedge-face-turf.webp"), "shot-wedges.webp", 1200, 1500, (0.5, 0.6))
    crop_to(raw("lgp02-gold__11_7388f94c-9c93-4aff-ada6-c6a1163ac214.webp"), "shot-putters.webp", 1200, 1500, (0.5, 0.55))
    crop_to(raw("lgh01__11_0464f85e-ccad-487c-bb2a-1c0a5c7b673c.webp"), "shot-hybrid.webp", 1200, 1500, (0.5, 0.5))
    crop_to(raw("lgw01-gold__11_26414fab-14b8-41ae-8ad7-a801c2f646fb.webp"), "finish-gold.webp", 1200, 1500, (0.5, 0.5))
    crop_to(raw("lucky-carver-black-hero.webp"), "finish-black.webp", 1200, 1500, (0.5, 0.55))
    crop_to(raw("lucky-bag-glove.webp"), "gift-bag.webp", 1600, 1067, (0.5, 0.5))
    crop_to(raw("lucky-allclubs-swing.webp"), "brand-bunker.webp", 1600, 1800, (0.5, 0.4))
    for pid in ("lgw01-gold", "lgw01-black", "lgp01-gold", "lgp02-gold", "lgh01",
                "polo-gold-dust", "polo-shadow", "polo-signature-black", "hat-white-gold-classic"):
        shutil.copy(os.path.join(PACKS, pid + "-pack.webp"), IMG)
    shutil.copy(os.path.join(ROOT, "img", "mags.webp"), IMG)


COURSE = [
    ("lucky-golfer-address.webp", "course-1.webp", "At address", "p/lgw01-gold", "Carver 01", "Golfer at address with a Carver 01 wedge", (0.5, 0.45)),
    ("lucky-blade-hero.webp", "course-2.webp", "On the green", "p/lgp01-gold", "Tracer Blade", "Tracer Blade behind a ball on the green", (0.5, 0.6)),
    ("lucky-wedge-sole-turf.webp", "course-3.webp", "In the bunker", "p/lgw01-gold", "Carver 01", "Carver 01 Gold behind a ball in the sand", (0.5, 0.65)),
    ("lucky-putters-downline.webp", "course-4.webp", "Lining it up", "p/lgp02-gold", "Tracer Mallet", "Tracer Mallet behind the ball", (0.5, 0.55)),
    ("lgh01__9_d51d0f8d-1213-4585-b809-af99f594601c.webp", "course-5.webp", "Off the tee box", "p/lgh01", "Stryker", "Stryker hybrid held on the course", (0.5, 0.5)),
    ("lucky-hybrid-crown-turf.webp", "course-6.webp", "The set", "c/clubs", "All clubs", "Stryker hybrid and two Carver wedges on the grass", (0.5, 0.5)),
    ("lgw01-gold__10_eb0cd992-4e1f-4285-8b83-8a351d94d640.webp", "course-7.webp", "Walking in", "p/lgw01-gold", "Carver 01", "Carver 01 Gold held up by a footbridge", (0.5, 0.5)),
    ("lgp01-gold__1_7fbd8d34-2c10-48fc-bcfb-b00b50dfbfab.webp", "course-8.webp", "By the flag", "p/lgp01-gold", "Tracer Blade", "Tracer Blade on the green by the flag", (0.5, 0.55)),
]


# ------------------------------------------------------------------ data
def reviews(pid):
    return jload(DATA, "reviews", pid + ".json")


def line_rating():
    tot = n = 0
    for pid in ("lgw01-gold", "lgp01-gold", "lgp02-gold", "lgh01"):
        for star, c in reviews(pid)["totals"].items():
            tot += int(star) * c
            n += c
    return tot / n, n


def find(pid, name, title=None):
    for s in reviews(pid)["sample"]:
        if s["n"] == name and (title is None or s["t"] == title):
            return s
    ERR.append(f"review {name!r} ({title}) not in reviews/{pid}.json")
    return {"n": name, "t": title or "", "q": "", "r": 5}


def stars(avg, size_label=None):
    pct = f"{avg / 5 * 100:.1f}%"
    svg = "".join('<svg><use href="#star"/></svg>' for _ in range(5))
    return (f'<span class="stars" style="--pct:{pct}" role="img" aria-label="{avg:.2f} out of 5 stars">'
            f'<span class="s-bg">{svg}</span><span class="s-fg">{svg}</span></span>')


def product_rating(pid):
    r = PROD[pid].get("rating")
    return (r["avg"], r["count"]) if r else (None, 0)


LINE = [
    ("lgw01-gold", "Best seller", "gold", "The one that makes you stop blaming the swing. Six lofts, two grinds, either hand."),
    ("lgw01-black", "New", "", "Blacked out, with gold on the clover and the loft stamp and nothing else."),
    ("lgp01-gold", None, "", "Short ones start to feel like a formality. Quiet off the face and planted through the stroke."),
    ("lgp02-gold", None, "", "Works with the arc your stroke already has instead of asking you to build a new one."),
    ("lgh01", None, "", "Easier to launch than the long iron it replaces, and the rough does not grab it on the way through."),
]


def tile(pid, tag=None, tagcls="", line=None, rating=True):
    p = PROD[pid]
    out = not p.get("inStock", True)
    if out:
        tag, tagcls = "Sold out", "out"
    avg, n = product_rating(pid)
    rt = f'<span class="h6-tile-rt">{stars(avg)}<span>{avg:.2f} &middot; {n} reviews</span></span>' if (rating and avg) else ""
    ln = f'<p class="h6-tile-ln">{line}</p>' if line else ""
    tg = f'<span class="h6-tile-tag {tagcls}">{tag}</span>' if tag else ""
    return (f'      <a class="h6-tile{" is-out" if out else ""}" href="{{{{link:p/{pid}}}}}">\n'
            f'        <span class="h6-tile-ph">{tg}<img src="img/{pid}-pack.webp" alt="{esc(p["name"])}" width="1200" height="1500" loading="lazy" decoding="async"></span>\n'
            f'        <span class="h6-tile-bd"><span class="h6-tile-nm">{esc(p["name"])}</span><span class="h6-tile-pr">{{{{price:{pid}}}}}</span>{rt}{ln}</span>\n'
            f'      </a>')


RAIL = [
    ("lgw01-gold", "JD M.", None),
    ("lgp02-gold", "Kyle K.", None),
    ("lgw01-gold", "Tim M.", None),
    ("lgw01-gold", "John L.L.", "Lucky Gold 52*"),
    ("lgh01", "LB06", None),
    ("lgp01-gold", "Jay S.", None),
    ("lgw01-gold", "Michael P.", None),
    ("lgw01-gold", "Conrad R.", None),
]
PNAME = {"lgw01-gold": "Carver 01 Gold", "lgp01-gold": "Tracer Blade", "lgp02-gold": "Tracer Mallet", "lgh01": "Stryker LGH01"}
CTA = {"lgw01-gold": "Go get one", "lgp01-gold": "Roll it pure", "lgp02-gold": "Roll it pure", "lgh01": "Fill the gap"}


def clip(t, n=150):
    t = " ".join(t.split())
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0].rstrip(",.;:!") + "…"


def review_rail():
    cards, data = [], []
    for i, (pid, name, title) in enumerate(RAIL):
        s = find(pid, name, title)
        data.append({"n": s["n"], "r": s["r"], "p": PNAME[pid], "d": s.get("d", ""), "ttl": s["t"], "co": "",
                     "txt": s["q"], "rep": "", "img": f"img/{pid}-pack.webp", "sku": PROD[pid]["code"],
                     "price": PROD[pid]["priceLabel"], "cta": CTA[pid]})
        cards.append(
            f'    <article class="rv-card" data-rv="{i}" tabindex="0" role="button" aria-label="Read the full review from {esc(s["n"])}, {s["r"]} stars, {PNAME[pid]}">\n'
            f'      {stars(s["r"])}\n'
            f'      <span class="rv-ttl">{esc(s["t"]) or "&nbsp;"}</span>\n'
            f'      <p class="rv-q">&ldquo;{esc(clip(s["q"], 190))}&rdquo;</p>\n'
            f'      <div class="h6-rv-by"><img src="img/{pid}-pack.webp" alt="" width="1200" height="1500" loading="lazy" decoding="async"><span><b>{esc(s["n"])}</b><span>{PNAME[pid]} &middot; verified buyer</span></span></div>\n'
            f'    </article>')
    return "\n".join(cards), data


def quote_block(pid, name, title=None, product=None):
    s = find(pid, name, title)
    return (f'<q>{esc(" ".join(s["q"].split()))}</q>'
            f'<figcaption>{esc(s["n"])} &middot; {product or PNAME[pid]} &middot; verified buyer</figcaption>')


def course():
    out = []
    for srcname, dest, cap, link, prod, alt, focus in COURSE:
        crop_to(raw(srcname), dest, 1200, 1500, focus)
        out.append(f'    <a class="h6-photo" href="{{{{link:{link}}}}}"><span class="h6-photo-ph"><img src="img/{dest}" alt="{alt}" width="1200" height="1500" loading="lazy" decoding="async"></span>'
                   f'<span class="h6-photo-cap">{cap}<em>{prod}</em></span></a>')
    return "\n".join(out)


# ------------------------------------------------------------------ assemble
def main():
    fresh_site()
    images()
    avg, n = line_rating()
    wavg, wn = product_rating("lgw01-gold")
    big = min(r["price"] for r in CASE["rows"])
    putters = [p for p in ("lgp01-gold", "lgp02-gold") if PROD[p].get("inStock")]
    if len(putters) == 2:
        putter_price = f"from {{{{price:lgp01-gold}}}}"
    elif putters:
        other = "Blade" if putters[0] == "lgp02-gold" else "Mallet"
        putter_price = f"{{{{price:{putters[0]}}}}} in stock, {other} sold out"
    else:
        putter_price = "sold out for now"
    cards, rv_data = review_rail()

    tokens = {
        "LINE_AVG": f"{avg:.2f}", "LINE_N": f"{n:,}",
        "STARS_LINE": stars(avg), "STARS_WEDGE": stars(wavg),
        "WEDGE_AVG": f"{wavg:.2f}", "WEDGE_N": f"{wn:,}",
        "BIG_PRICE": f"${big:,.0f} and up",
        "BIG_SOURCE": f"Big-brand price is the current US list price for one steel-shaft wedge from three of the biggest wedge makers, checked {CASE['checked']}.",
        "PUTTER_PRICE": putter_price,
        "LINE_TILES": "\n".join(tile(pid, tag, cls, line) for pid, tag, cls, line in LINE),
        "APPAREL_TILES": "\n".join([tile(p, rating=False, line="Classic Polo") for p in ("polo-gold-dust", "polo-shadow", "polo-signature-black")]
                                   + [tile("hat-white-gold-classic", rating=False, line="Five-panel snapback")]),
        "QUOTE_GOLDY": quote_block("lgw01-gold", "Paul F.", "New wedges"),
        "QUOTE_GIFT": quote_block("lgw01-gold", "Michelle S."),
        "PULL_QUOTE": (lambda s: f'<q>{esc(" ".join(s["q"].split()))}</q><cite><b>{esc(s["n"])}</b> &middot; Carver 01 Gold &middot; verified buyer</cite>')(find("lgw01-gold", "Eric F.")),
        "REVIEW_CARDS": cards,
        "COURSE_PHOTOS": course(),
    }
    page = open(os.path.join(V6, "src", "home.html"), encoding="utf-8").read()
    for k, v in tokens.items():
        page = page.replace(f"[[{k}]]", v)
    left = re.findall(r"\[\[[A-Z_]+\]\]", page)
    if left:
        ERR.append(f"unfilled tokens: {sorted(set(left))}")
    js = ("var LG_REVIEWS = " + json.dumps(rv_data, ensure_ascii=False) + ";\nvar LG_POSTS = [];\n")

    if ERR:
        print("BUILD FAILED\n  " + "\n  ".join(ERR), file=sys.stderr)
        sys.exit(1)
    src = os.path.join(SITE, "_src")
    open(os.path.join(src, "page-home.html"), "w", encoding="utf-8").write(page)
    open(os.path.join(src, "page-home.css"), "w", encoding="utf-8").write(open(os.path.join(V6, "src", "home.css"), encoding="utf-8").read())
    open(os.path.join(src, "page-home.js"), "w", encoding="utf-8").write(js)
    r = subprocess.run([sys.executable, os.path.join(SITE, "tools", "build.py"), "home"], cwd=SITE, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout[-3000:], r.stderr[-3000:], file=sys.stderr)
        sys.exit(1)
    doc = open(os.path.join(SITE, "01-home.html"), encoding="utf-8").read()
    if "—" in re.sub(r"<!--.*?-->|/\*.*?\*/", "", doc, flags=re.S):
        print("em dash in visible output", file=sys.stderr)
        sys.exit(1)
    doc = localize(doc).replace("<title>Lucky Golf · Home</title>", "<title>Lucky Golf Home v6</title>")
    open(os.path.join(OUT, "home.html"), "w", encoding="utf-8").write(doc)
    print(f"built v6/out/home.html | line {avg:.2f} from {n} | wedge {wavg} from {wn} | big-brand from ${big}")


def localize(s):
    """The review viewer serves only the page's own files: pull every Shopify
    image in (header menu, cart) into img/."""
    cache = os.path.join(ROOT, "v5", "img-cache")
    os.makedirs(cache, exist_ok=True)
    for u in sorted(set(re.findall(r'https://cdn\.shopify\.com/[^"\'\s)]+', s))):
        name = re.sub(r"[^A-Za-z0-9._-]", "_", u.split("?")[0].split("/")[-1])
        rawp = os.path.join(cache, name)
        if not os.path.exists(rawp):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            open(rawp, "wb").write(urllib.request.urlopen(req, timeout=40).read())
        dest = os.path.splitext(name)[0] + ".webp"
        if not os.path.exists(os.path.join(IMG, dest)):
            im = Image.open(rawp)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            im.thumbnail((1000, 1000))
            im.save(os.path.join(IMG, dest), "WEBP", quality=80)
        s = s.replace(u, "img/" + dest)
    return s


if __name__ == "__main__":
    main()
