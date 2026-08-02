"""
The link registry: every page the site will ever have, and the one place a URL
is written down.

WHY
---
Roughly sixty pages are coming. Hard-coding `href="02-pdp-lgw01.html"` across
them and fixing it later is the expensive version of routing — GAMEPLAN phase A
exists to avoid exactly that. So: every page declares a slug here, every
internal link in `_src/` is written as a token, and `build.py` resolves them.

    {{link:home}}              -> 01-home.html   (-> "" on the homepage itself)
    {{link:home#families}}     -> 01-home.html#families  (-> "#families" on home)
    {{link:p/lgw01-gold}}      -> 02-pdp-lgw01.html
    {{link:c/wedges}}          -> "#"  — declared, not built yet
    {{link:none}}              -> "#"  — deliberately not a link

Three failure modes, all fatal at build time:

  * a token naming a slug that is not declared here      -> dangling link
  * a literal href="#" left in _src/                     -> untracked link
  * any {{...}} still in the output after resolution     -> typo'd token

The middle one is why `{{link:none}}` exists. Modal triggers and JS-driven
controls are real anchors that genuinely go nowhere, and without an explicit
way to say so there is no way to tell them apart from a link someone forgot to
wire up. Saying it out loud costs one token and makes `href="#"` a build error
everywhere else.

Pages that are declared but not yet built resolve to "#" and are counted in the
build report, so the run prints how much of the site is still stubbed rather
than failing until all sixty pages exist.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
PRODUCTS_JSON = os.path.join(ROOT, "_src", "data", "products.json")

with open(PRODUCTS_JSON, encoding="utf8") as f:
    CATALOGUE = json.load(f)

PRODUCTS = CATALOGUE["products"]
COLLECTIONS = CATALOGUE["collections"]


class Page(object):
    """`src` is the _src/page-NAME.* basename for pages build.py assembles;
    declared-but-unbuilt pages leave it None."""

    def __init__(self, slug, file, title, src=None, built=False, kind="page"):
        self.slug, self.file, self.title = slug, file, title
        self.src, self.built, self.kind = src, built, kind

    def __repr__(self):
        return "<Page %s -> %s%s>" % (self.slug, self.file, "" if self.built else " (stub)")


def _pages():
    p = {}

    def add(slug, file, title, src=None, built=False, kind="page"):
        assert slug not in p, "duplicate slug %r" % slug
        p[slug] = Page(slug, file, title, src, built, kind)

    # ---- built ------------------------------------------------------------
    add("home", "01-home.html", "Lucky Golf — Home", src="home", built=True)

    # ---- product pages, one per catalogue entry ---------------------------
    # The slug is p/<products.json id>, so adding a product to the catalogue
    # routes it automatically. LGW01 keeps its existing filename.
    for prod in PRODUCTS:
        add("p/" + prod["id"],
            prod.get("file", "20-product-%s.html" % prod["id"]),
            "%s — Lucky Golf" % prod["title"],
            src=prod["template"] if prod["built"] else None,
            built=prod["built"],
            kind="product")

    # ---- collections (GAMEPLAN phase B) -----------------------------------
    # A collection carrying `blocked` is declared and routed but not built —
    # links to it resolve to "#" like any other stub, and the reason travels in
    # products.json. `tpl` is the template: `clp` for the club collections
    # (bands, comparison, brand copy), `plp` for the flat filtered grid.
    for coll in COLLECTIONS:
        live = not coll.get("blocked")
        add("c/" + coll["id"], "10-collection-%s.html" % coll["id"],
            "%s — Lucky Golf" % coll["name"],
            src=coll.get("tpl", "plp") if live else None,
            built=live, kind="collection")

    # ---- brand, support, utility (phases E and F) -------------------------
    # ---- brand pages (phase E) --------------------------------------------
    # One template, two pages, same argument as the support cluster: they share
    # a shape and differ only in which blocks they carry.
    add("story", "30-story.html", "Our Story — Lucky Golf",
        src="brand", built=True, kind="brand")
    add("trybe", "31-trybe.html", "The Trybe — Lucky Golf",
        src="brand", built=True, kind="brand")
    # Not in GAMEPLAN 4's page list, but the homepage's "Read all 884 reviews"
    # has to land somewhere, and that count is clubs-wide — so it cannot point
    # at any single PDP's review block.
    add("reviews", "32-reviews.html", "Reviews — Lucky Golf",
        src="reviews", built=True)
    # ---- the support cluster (phase F) ------------------------------------
    # Four pages, ONE template, the way the three PDP templates work: they
    # share a shape (title, lede, sectioned prose, a way to reach a person) and
    # differ only in the body. `kind` is what routes build.py at the editorial
    # file, exactly as "product" and "collection" do.
    for slug, file, title in (
        ("returns",  "40-returns.html",  "Returns & the 60-day policy — Lucky Golf"),
        ("shipping", "41-shipping.html", "Shipping — Lucky Golf"),
        ("contact",  "42-contact.html",  "Contact — Lucky Golf"),
        ("faq",      "43-faq.html",      "FAQ — Lucky Golf"),
    ):
        add(slug, file, title, src="support", built=True, kind="support")
    add("search", "50-search.html", "Search — Lucky Golf",
        src="search", built=True)
    add("404", "51-404.html", "Page not found — Lucky Golf",
        src="404", built=True)

    return p


PAGES = _pages()

# Slugs build.py actually assembles this run, in output order.
BUILDABLE = [s for s, pg in PAGES.items() if pg.built]


def product(pid):
    for prod in PRODUCTS:
        if prod["id"] == pid:
            return prod
    raise KeyError("no product %r in products.json" % pid)


def collection(cid):
    for coll in COLLECTIONS:
        if coll["id"] == cid:
            return coll
    raise KeyError("no collection %r in products.json" % cid)
