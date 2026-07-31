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


def apply_context(text, ctx, slug):
    for name, value in ctx.items():
        text = text.replace("{{%s}}" % name, value)
    return text


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

    css = read("core.css") + "\n\n" + read("page-%s.css" % src)
    # Product pages get the variant engine ahead of their own script, which
    # reads it at module scope. Other pages have no buy box and don't need it.
    js = read("variants.js") + "\n\n" if page.kind == "product" else ""
    js += read("page-%s.js" % src, required=False)
    js = js.rstrip("\n") + "\n\n" + read("core.js")

    html = SHELL.format(
        title=page.title,
        css=css,
        symbols=host,
        header=read("partials/header.html"),
        sections=read("page-%s.html" % src),
        footer=read("partials/footer.html"),
        lightbox=read("partials/lightbox.html"),
        cart=read("partials/cart.html"),
        js=js,
    )

    html = apply_context(html, ctx, slug)
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
    "pdp": [
        ".msnap{",
        ".atc-bar{display:flex}",        # mobile sticky add-to-cart
        ".bx-four{grid-template-columns:repeat(2,1fr)",
        ".pd-top{grid-template-columns:1fr",
        ".gal-thumbs{grid-template-columns:repeat(5,1fr)}",
        ".spec-tab{flex:1",
        ".md-panel{",                    # policy modals
        "@media (max-width:760px)",
        'id="pickers"',                  # N-axis buy box mounts here
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
