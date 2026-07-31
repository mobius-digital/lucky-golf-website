"""
Assemble each page from _src/ into a single-file, dependency-free NN-name.html.

    python tools/build.py            # build every buildable page
    python tools/build.py pdp        # build one, by source name
    python tools/build.py --check    # build to memory, diff against what's on disk
    python tools/build.py --links    # print the link registry and stop

The generated NN-*.html files stay self-contained on purpose — that is what
makes them easy to send and review. Never edit them directly; they are
overwritten. Source of truth is _src/ + _src-logo-symbols.svg, and the product
data in _src/data/products.json.

Page order inside <body>:
    symbol sprite -> header -> page sections -> footer -> lightbox -> cart
CSS order: core.css -> page-NAME.css
JS  order: page-NAME.js (data first, so core can read it) -> core.js

Three things fail the build, all of them silent-in-a-browser problems:
  * a dangling or malformed {{link:...}} token   (see tools/sitemap.py)
  * a literal href="#" left in _src/             (ditto)
  * a missing load-bearing CSS rule              (see REQUIRED, below)
"""
import argparse
import io
import json
import os
import re
import sys

import sitemap
import template

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "_src")

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>

{symbols}

{header}

{sections}

{footer}

{lightbox}

{cart}

<script>
{js}
</script>

</body>
</html>
"""

LINK_TOKEN = re.compile(r"\{\{link:([^}]*)\}\}")
COUNT_TOKEN = re.compile(r"\{\{count:([^}]*)\}\}")
BARE_HASH = re.compile(r"""href=(["'])#\1""")


def read(rel, required=True):
    path = os.path.join(SRC, rel)
    if not os.path.exists(path):
        if required:
            sys.exit("missing source: _src/%s" % rel)
        return ""
    return open(path, encoding="utf8").read().rstrip("\n")


# --------------------------------------------------------------------------
# Links
# --------------------------------------------------------------------------
def resolve_links(text, current_slug, report):
    """Replace every {{link:...}} token. Unknown slugs are collected rather
    than raised so one build reports all of them at once."""

    def sub(m):
        target = m.group(1).strip()
        if target == "none":
            report["none"] += 1
            return "#"
        slug, _, frag = target.partition("#")
        anchor = ("#" + frag) if frag else ""
        page = sitemap.PAGES.get(slug)
        if page is None:
            report["dangling"].add(target)
            return "#UNRESOLVED"
        if not page.built:
            report["stubs"][slug] = report["stubs"].get(slug, 0) + 1
            return "#"
        # A link to the page you are already on: keep just the anchor, so the
        # shared header's #families / #gear work from the homepage and from
        # every other page without either needing to know which it is.
        if slug == current_slug and anchor:
            return anchor
        return page.file + anchor

    return LINK_TOKEN.sub(sub, text)


def resolve_counts(text):
    """{{count:hats}} -> the number of products actually in that collection.

    The shared mega menu advertised "13 styles" of hat when the store has ten
    — three were archived and the hand-typed number stayed behind. Any count
    quoted in copy comes from products.json now, so it cannot drift again."""

    def sub(m):
        cid = m.group(1).strip()
        try:
            return str(sitemap.collection(cid)["count"])
        except KeyError:
            sys.exit("{{count:%s}}: no such collection in products.json" % cid)

    return COUNT_TOKEN.sub(sub, text)


def audit_sources():
    """Every internal link must be a token. A literal href="#" is either a
    forgotten link or a control that only looks like one — `{{link:none}}`
    is how you say you meant the second."""
    bad = []
    for dirpath, _dirs, files in os.walk(SRC):
        for name in sorted(files):
            if not name.endswith((".html", ".js", ".css")):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, ROOT).replace("\\", "/")
            for n, line in enumerate(open(path, encoding="utf8"), 1):
                if BARE_HASH.search(line):
                    bad.append("%s:%d" % (rel, n))
    return bad


# --------------------------------------------------------------------------
# Product pages: catalogue + editorial -> template context
# --------------------------------------------------------------------------
def spec_table(tab):
    """A spec tab is either structured `rows` (key/value, the common case) or
    raw `html` for the irregular ones — the by-loft matrix has merged cells and
    a header row and is not worth a schema."""
    if "html" in tab:
        return tab["html"]
    body = []
    for r in tab.get("rows", []):
        cell = ('<span class="tbd tbd--light">Needs spec</span>'
                if r.get("tbd") else r.get("v", ""))
        body.append('<tr><th scope="row">%s</th><td>%s</td></tr>' % (r["k"], cell))
    return '<table class="spec-tbl"><tbody>%s</tbody></table>' % "".join(body)


def tile_for(pid, extra=None):
    """A cross-sell tile: catalogue facts from products.json, hook and label
    from whichever copy file asked for it. Nothing about price or availability
    is retyped in the editorial layer."""
    p = sitemap.product(pid)
    t = {
        "id": p["id"], "code": p["code"], "name": p["name"], "title": p["title"],
        "img": p["img"], "priceLabel": p["priceLabel"], "summary": p["summary"],
        "inStock": p["inStock"], "href": "{{link:p/%s}}" % pid,
    }
    # Cole's rule: a product card never shows a review count. The variant
    # summary ("Right & left hand", "S–3XL") is what belongs in that slot —
    # it answers a question the shopper actually has at this point.
    if p.get("rating"):
        t["rating"] = p["rating"]
    t["meta"] = p["summary"]
    if extra:
        t.update({k: v for k, v in extra.items() if k != "id"})
    return t


def product_copy(prod):
    """Merge the editorial file with the catalogue record and precompute
    everything the template would otherwise need expressions for. The template
    engine is deliberately dumb (tools/template.py), so the shaping happens
    here where it can be read and tested."""
    path = os.path.join(SRC, "data", "copy", "%s.json" % prod["id"])
    if not os.path.exists(path):
        sys.exit("%s is marked built but has no editorial: _src/data/copy/%s.json"
                 % (prod["id"], prod["id"]))

    # Family defaults, merged UNDER the product's own file. Thirteen polos share
    # one fabric, one fit note, one size guide and one returns line; writing
    # that thirteen times is thirteen chances for it to drift. The product file
    # carries only what is actually different about that product, and any key
    # it does set wins outright — no deep merging, because a half-overridden
    # list is harder to reason about than a repeated one.
    fam_path = os.path.join(SRC, "data", "copy", "_family-%s.json" % prod["family"])
    copy = {}
    if os.path.exists(fam_path):
        copy.update(json.load(open(fam_path, encoding="utf8")))
    copy.update(json.load(open(path, encoding="utf8")))

    coll = sitemap.collection(prod["collection"])
    ctx = {k: v for k, v in copy.items() if not k.startswith("_")}
    ctx.update({
        "title": prod["title"], "name": prod["name"], "code": prod["code"],
        "priceLabel": prod["priceLabel"],
        "collName": coll["name"], "collLink": "{{link:c/%s}}" % coll["id"],
    })
    if prod.get("rating"):
        ctx["rating"] = prod["rating"]

    # The sticky mobile bar's variant line is repainted by JS on every change,
    # but rendering it server-side too means it is never briefly blank — and
    # unlike the old hard-coded "Right hand · 56°" it is right for any product.
    labels = []
    for i, ax in enumerate(prod["options"]):
        want = prod["default"].split("|")[i]
        labels += [v["label"] for v in ax["values"] if v["k"] == want]
    ctx["defaultVariant"] = " &middot; ".join(labels)

    # gallery: [path, alt] pairs -> objects, with `first` driving data-on and
    # the eager load on slide one
    base = copy.get("galleryBase", "")
    shots = []
    for i, g in enumerate(copy.get("gallery", [])):
        shots.append({"src": base + g[0], "alt": g[1], "first": i == 0})
    ctx["gallery"] = shots
    ctx["galleryCount"] = len(shots)

    tabs = []
    for i, tab in enumerate(copy.get("specTabs", [])):
        tabs.append(dict(tab, i=i, selected="true" if i == 0 else "false",
                         hidden=i > 0, tableHtml=spec_table(tab)))
    ctx["specTabs"] = tabs

    ctx["bag"] = [tile_for(row["id"], row) for row in copy.get("bag", [])]

    # ---- sibling colourways ----------------------------------------------
    # Ten Classic Polos are ten separate Shopify products, so without a strip
    # linking them the range is undiscoverable from any one page (GAMEPLAN
    # §3.2). Membership is the product's own family — nothing to maintain.
    fam = [p for p in sitemap.PRODUCTS
           if p["family"] == prod["family"] and p["id"] != prod["id"]]
    if fam:
        # Swatches are the family in catalogue order WITH this product in it,
        # marked. The strip lower down is siblings only; this row is the whole
        # range, because a swatch set with a hole where you are standing reads
        # as a missing colour rather than as the current one.
        whole = [p for p in sitemap.PRODUCTS if p["family"] == prod["family"]]
        ctx["swatches"] = {
            "label": "Colour" if prod["family"].startswith("polo") else "Design",
            "current": prod["name"],
            "items": [{"name": p["title"], "img": p["img"],
                       "soldOut": not p["inStock"],
                       "isThis": p["id"] == prod["id"],
                       "href": "{{link:p/%s}}" % p["id"]} for p in whole],
        }
        ctx["siblings"] = {
            "items": [{"name": p["name"].replace(" Classic Polo", "").replace(" Blade Polo", ""),
                       "title": p["title"], "img": p["img"], "summary": p["summary"],
                       "soldOut": not p["inStock"],
                       "href": "{{link:p/%s}}" % p["id"]}
                      for p in fam],
        }
        ctx["sibTotal"] = len(fam) + 1

    # ---- JSON blocks the page's script reads -----------------------------
    # The browse rail names product ids; price, rating and stock come from the
    # catalogue, so a neighbour going out of stock updates every page that
    # points at it without anyone editing copy.
    rail = []
    for row in copy.get("oav", []):
        row = {"id": row} if isinstance(row, str) else dict(row)
        p = sitemap.product(row["id"])
        tag = row.get("tag", "")
        if not p["inStock"]:
            tag = "Sold out"
        rail.append({
            "nm": p["title"], "pr": p["priceLabel"],
            "rt": ("%s ★ %s" % (p["rating"]["avg"], p["rating"]["count"])
                   if p.get("rating") else p["summary"]),
            "tag": tag, "out": not p["inStock"],
            "href": "{{link:p/%s}}" % p["id"], "img": p["img"],
        })
    ctx["OAV_JSON"] = json.dumps(rail, ensure_ascii=False)
    ctx["REEL_JSON"] = json.dumps(copy.get("reel", []), ensure_ascii=False)
    ctx["UPSELL_JSON"] = json.dumps(copy.get("upsell", []), ensure_ascii=False)

    rpath = os.path.join(SRC, "data", "reviews", "%s.json" % prod["id"])
    if os.path.exists(rpath):
        rev = json.load(open(rpath, encoding="utf8"))
        rev = {k: v for k, v in rev.items() if not k.startswith("_")}
    else:
        # A product with no reviews pulled yet still renders — the widget just
        # has nothing to show. Better than a page that fails to build.
        rev = {"total": 0, "totals": {}, "sample": []}
    ctx["REVIEWS_JSON"] = json.dumps(rev, ensure_ascii=False)
    ctx["reviewSample"] = bool(rev.get("sample"))

    # the comparison module names its sibling products, so the tiles it shows
    # resolve through the catalogue the same way cross-sells do
    if copy.get("helpPick"):
        pick = dict(copy["helpPick"])
        opts = []
        for o in pick.get("options", []):
            row = dict(o)
            if o.get("id") and o["id"] != prod["id"]:
                row["href"] = "{{link:p/%s}}" % o["id"]
            else:
                row["isThis"] = True
                row["href"] = None
            opts.append(row)
        pick["options"] = opts
        ctx["helpPick"] = pick

    return ctx


# --------------------------------------------------------------------------
# Page assembly
# --------------------------------------------------------------------------
def page_context(slug):
    """Per-page values injected into the sources as {{NAME}} tokens.

    This is what makes the PDP data-driven: the whole product record goes in
    as JSON and page-pdp.js builds its buy box from it, so a re-pull of the
    catalogue changes the page without anyone editing markup."""
    page = sitemap.PAGES[slug]
    ctx = {"TITLE": page.title}

    if page.kind == "product":
        prod = sitemap.product(slug.split("/", 1)[1])
        ctx["PRODUCT_JSON"] = json.dumps(prod, ensure_ascii=False, sort_keys=False)
        ctx.update(product_copy(prod))

    if page.kind == "collection":
        coll = sitemap.collection(slug.split("/", 1)[1])
        # Tiles carry only what the grid renders and sorts on. The href is a
        # registry token so these links are audited like any other, even
        # though the tile itself is painted by JS.
        tiles = []
        for pid in coll["products"]:
            p = sitemap.product(pid)
            tile = {
                "id": p["id"], "code": p["code"], "name": p["name"],
                "title": p["title"], "family": p["family"], "img": p["img"],
                "price": p["price"], "priceLabel": p["priceLabel"],
                "summary": p["summary"], "inStock": p["inStock"],
                "href": "{{link:p/%s}}" % p["id"],
            }
            # Quick add, but only where there is genuinely nothing to choose.
            # One sellable variant and no option axes means the button can put
            # the real SKU in the bag; anything else has to go to its own page.
            live = [v for v in p["variants"].values() if v["avail"]]
            if not p["options"] and len(live) == 1:
                tile["addSku"] = live[0]["sku"]
            else:
                axis = p["options"][0]["name"].lower() if p["options"] else "options"
                tile["chooseLabel"] = "Choose %s" % axis
            if p.get("rating"):
                tile["rating"] = p["rating"]
            tiles.append(tile)
        ctx["COLLECTION_JSON"] = json.dumps(
            {"id": coll["id"], "name": coll["name"],
             "facets": coll["facets"], "products": tiles},
            ensure_ascii=False, sort_keys=False)
        ctx["COLL_NAME"] = coll["name"]
        ctx["COLL_EYEBROW"] = coll["eyebrow"]
        ctx["COLL_LEDE"] = coll["lede"]

    return ctx


def build(slug, report):
    page = sitemap.PAGES[slug]
    if not page.built:
        sys.exit("%s is declared but not built — nothing to assemble" % slug)
    src = page.src
    ctx = page_context(slug)

    symbols = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf8").read().rstrip("\n")
    host = read("partials/symbols-host.html")
    if "{{SYMBOLS}}" not in host:
        sys.exit("partials/symbols-host.html lost its {{SYMBOLS}} placeholder")
    host = host.replace("{{SYMBOLS}}", symbols)

    # Product pages: core, then the shared PDP styles, then the template's own.
    # A page only ever loads core plus one page stylesheet, so anything two
    # templates render has to be in pdp.css — the same reason .chip and .crumb
    # had to move into core.
    css = read("core.css")
    if page.kind == "product":
        css += "\n\n" + read("pdp.css")
    css += "\n\n" + read("page-%s.css" % src)

    # Only the page's own sources go through the template engine — core.css and
    # core.js are shared, contain no tokens, and rendering them would be a
    # pointless place for a surprise. {{link:…}} and {{count:…}} are not in the
    # context, so the engine leaves them alone for their own passes below.
    sections = template.render(read("page-%s.html" % src), ctx, "page-%s.html" % src)
    page_js = template.render(read("page-%s.js" % src, required=False), ctx,
                              "page-%s.js" % src)

    # Product pages get the variant engine, then the shared PDP behaviour
    # (gallery, buy box, cross-sell rails, reviews), then whatever is genuinely
    # specific to their template. Other pages have no buy box and need none of
    # it. pdp.js carries the data declarations, so it is rendered too.
    js = ""
    if page.kind == "product":
        js = read("variants.js") + "\n\n"
        js += template.render(read("pdp.js"), ctx, "pdp.js") + "\n\n"
    js += page_js
    js = js.rstrip("\n") + "\n\n" + read("core.js")

    html = SHELL.format(
        title=page.title,
        css=css,
        symbols=host,
        header=read("partials/header.html"),
        sections=sections,
        footer=read("partials/footer.html"),
        lightbox=read("partials/lightbox.html"),
        cart=read("partials/cart.html"),
        js=js,
    )
    html = resolve_counts(html)
    html = resolve_links(html, slug, report)

    leftover = sorted(set(re.findall(r"\{\{[^}\n]{0,60}\}\}", html)))
    if leftover:
        sys.exit("%s: unresolved template tokens: %s" % (slug, ", ".join(leftover)))
    return html


# Cheap smoke test. A regex cleanup once silently deleted a whole responsive
# block from page-pdp.css and the page still built, still passed a desktop
# sweep, and only showed up as a broken phone layout. Anything load-bearing
# enough that its absence is hard to see belongs here.
REQUIRED = {
    "home": [
        ".msnap{",                       # mobile card rails
        "@media (max-width:980px)",
        ".hdr{", ".cd-panel{", ".mq{",
    ],
    "club": [
        ".msnap{",
        ".atc-bar{display:flex}",        # mobile sticky add-to-cart
        ".bx-four{grid-template-columns:repeat(2,1fr)",
        ".pd-top{grid-template-columns:1fr",
        ".gal-thumbs{grid-template-columns:repeat(5,1fr)}",
        ".spec-tab{flex:1",
        ".md-panel{",                    # policy modals
        "@media (max-width:760px)",
        'id="pickers"',                  # N-axis buy box mounts here
        # JS, not CSS. Splitting the shared PDP behaviour into pdp.js briefly
        # dropped it from the bundle entirely: the page still built, --check
        # still said "identical" (it compares output to output), and only the
        # 30KB size drop gave it away. Anything whose absence leaves a page
        # that looks right and does nothing belongs here.
        "function paintPickers",         # pdp.js — the buy box
        "LG_VARIANTS",                   # variants.js — the axis engine
        "function paintLoftFinder",      # page-club.js — the wedge ladder
    ],
    "apparel": [
        'id="pickers"', "function paintPickers", "LG_VARIANTS",
        ".sibs{",                        # the colourway strip — the range dies without it
        ".sz{",                          # size guide replaces the spec table
        "@media (max-width:620px)",
    ],
    "gear": [
        'id="pickers"', "function paintPickers", "LG_VARIANTS",
        ".pd-top{grid-template-columns:1fr",
        "@media (max-width:760px)",
    ],
    "plp": [
        'id="plp-grid"', 'id="plp-empty"',   # grid and its empty state
        ".plp-grid{grid-template-columns:repeat(2,1fr);gap:14px}",  # phone grid
        ".plp-facets:empty{display:none}",   # single-family collections
        ".chip{",                            # promoted to core; PLP depends on it
        "@media (max-width:620px)",
    ],
}


def smoke(src, html):
    missing = [n for n in REQUIRED.get(src, []) if n not in html]
    if missing:
        sys.exit("%s: build is missing required rules:\n  %s"
                 % (src, "\n  ".join(missing)))


def print_registry():
    built = [p for p in sitemap.PAGES.values() if p.built]
    stub = [p for p in sitemap.PAGES.values() if not p.built]
    print("link registry — %d pages, %d built, %d declared\n"
          % (len(sitemap.PAGES), len(built), len(stub)))
    for page in sorted(built, key=lambda p: p.file):
        print("  %-26s %s" % (page.slug, page.file))
    print()
    by_kind = {}
    for page in stub:
        by_kind.setdefault(page.kind, []).append(page)
    for kind in sorted(by_kind):
        pages = by_kind[kind]
        print("  %-10s %d declared, not built" % (kind, len(pages)))
        for page in sorted(pages, key=lambda p: p.slug)[:4]:
            print("       %-23s -> %s" % (page.slug, page.file))
        if len(pages) > 4:
            print("       ... and %d more" % (len(pages) - 4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="*", help="source names (home, pdp); default all")
    ap.add_argument("--check", action="store_true",
                    help="do not write; report whether output differs from disk")
    ap.add_argument("--links", action="store_true",
                    help="print the link registry and exit")
    a = ap.parse_args()

    if a.links:
        print_registry()
        return 0

    bad = audit_sources()
    if bad:
        sys.exit("literal href=\"#\" in source — use {{link:<slug>}}, or "
                 "{{link:none}} if it is deliberately not a link:\n  "
                 + "\n  ".join(bad))

    targets = [(s, sitemap.PAGES[s]) for s in sitemap.BUILDABLE]
    if a.pages:
        wanted = set(a.pages)
        targets = [(s, p) for s, p in targets if p.src in wanted]
        unknown = wanted - {p.src for _s, p in [(s, sitemap.PAGES[s]) for s in sitemap.BUILDABLE]}
        if unknown:
            sys.exit("unknown page(s): %s\nbuildable: %s"
                     % (", ".join(sorted(unknown)),
                        ", ".join(sorted({sitemap.PAGES[s].src for s in sitemap.BUILDABLE}))))

    report = {"dangling": set(), "stubs": {}, "none": 0}
    rc = 0
    for slug, page in targets:
        html = build(slug, report)
        smoke(page.src, html)
        path = os.path.join(ROOT, page.file)

        if a.check:
            old = open(path, encoding="utf8").read() if os.path.exists(path) else None
            if old is None:
                print("%-22s NEW (not on disk)" % page.file)
                rc = 1
            elif old == html:
                print("%-22s identical" % page.file)
            else:
                o, n = old.split("\n"), html.split("\n")
                print("%-22s DIFFERS  (%d lines on disk -> %d rebuilt)"
                      % (page.file, len(o), len(n)))
                shown = 0
                for i in range(max(len(o), len(n))):
                    a_ = o[i] if i < len(o) else "<eof>"
                    b_ = n[i] if i < len(n) else "<eof>"
                    if a_ != b_:
                        print("   line %d\n     disk: %s\n     new : %s"
                              % (i + 1, a_[:150], b_[:150]))
                        shown += 1
                        if shown >= 12:
                            print("   ... (more)")
                            break
                rc = 1
            continue

        with io.open(path, "w", encoding="utf8", newline="\n") as f:
            f.write(html)
        print("%-22s %6.1f KB" % (page.file, len(html.encode("utf8")) / 1024.0))

    if report["dangling"]:
        print("\nDANGLING LINKS — no such slug in tools/sitemap.py:")
        for t in sorted(report["dangling"]):
            print("  {{link:%s}}" % t)
        return 1

    total = sum(report["stubs"].values())
    if total:
        top = sorted(report["stubs"].items(), key=lambda kv: (-kv[1], kv[0]))
        print("\n%d link%s to %d page%s not built yet (resolved to #):"
              % (total, "" if total == 1 else "s",
                 len(report["stubs"]), "" if len(report["stubs"]) == 1 else "s"))
        print("  " + ", ".join("%s x%d" % (s, n) for s, n in top[:8])
              + (", ..." if len(top) > 8 else ""))
    return rc


if __name__ == "__main__":
    sys.exit(main())
