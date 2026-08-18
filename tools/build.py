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


def cross_sell(pid, where):
    """Resolve a product another page points at, and refuse a discontinued one.

    Discontinuing the driver and the Patriot (HANDOFF §15a) deleted their pages
    but left three cross-sell rows pointing at them, so the LGH01 page shipped
    with a browse card, a bag tile and a whole comparison column linking to
    href="#". Nothing caught it: an unbuilt page resolving to "#" is a normal,
    counted state for the sixty pages still to come. A DISCONTINUED one is not
    the same thing, and now says so."""
    p = sitemap.product(pid)
    if p.get("discontinued"):
        sys.exit("%s points at %s, which is discontinued — remove the row"
                 % (where, pid))
    return p


def tile_for(pid, extra=None):
    """A cross-sell tile: catalogue facts from products.json, hook and label
    from whichever copy file asked for it. Nothing about price or availability
    is retyped in the editorial layer."""
    p = cross_sell(pid, "a bag/cross-sell row")
    t = {
        "id": p["id"], "code": p["code"], "name": p["name"], "title": p["title"],
        "img": p["img"], "priceLabel": p["priceLabel"], "summary": p["summary"],
        "inStock": p["inStock"], "href": "{{link:p/%s}}" % pid,
    }
    if p.get("rating"):
        t["rating"] = p["rating"]
    if extra:
        t.update({k: v for k, v in extra.items() if k != "id"})
    # Cole's rule (§16 note 2): a product card NEVER shows a review count. The
    # variant summary ("Right & left hand · 6 lofts", "S–3XL") is what belongs
    # in that slot — it answers a question a browsing shopper actually has.
    #
    # The rule was applied to the collection grid and the homepage and missed
    # the PDP cross-sell grids, where copy files were overriding `meta` with a
    # hand-typed "4.81 ★ 551". So the fallback happens AFTER the copy layer,
    # and a star in a meta is now fatal rather than merely wrong: a rating
    # typed into a copy file is also stale the moment Judge.me moves.
    if "★" in t.get("meta", "") or "&#9733;" in t.get("meta", ""):
        sys.exit("%s: a card meta carries a review count (%r). Cards never show "
                 "ratings — drop the key and the variant summary is used."
                 % (pid, t["meta"]))
    t.setdefault("meta", p["summary"])
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
    # Three layers, each overriding the one under it:
    #
    #   _shared-<template>.json   everything that is true of the template
    #   _family-<family>.json     everything that is true of the family
    #   <product>.json            what is actually different about this product
    #
    # The shared layer exists because the polo size chart is identical for the
    # Classic and the Blade, and a 6x3x2 table copied into two family files is a
    # table that will drift. Same for the design section: Cole, 2026-07-31, one
    # section that works for any polo and one that works for any hat.
    copy = {}
    for layer in ("_shared-%s.json" % prod["template"],
                  "_family-%s.json" % prod["family"]):
        lp = os.path.join(SRC, "data", "copy", layer)
        if os.path.exists(lp):
            copy.update(json.load(open(lp, encoding="utf8")))
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

    # The size guide is a modal hung off the size picker (Cole 2026-07-31), so
    # a product with no size axis has nothing to hang it from. Hats inherit the
    # apparel shared layer and must not render a chart of polo measurements.
    if not any(ax["key"] == "size" for ax in prod["options"]):
        ctx.pop("sizeGuide", None)
    elif ctx.get("sizeGuide"):
        g = dict(ctx["sizeGuide"])
        # "true"/"false" as STRINGS. A Python bool renders as "True", and CSS
        # attribute-value matching is case-sensitive — [aria-checked="true"]
        # never matched, so the guide opened with neither unit selected. It is
        # also invalid ARIA. The same trap applies to any boolean that reaches
        # an attribute VALUE rather than a {{#section}}.
        g["units"] = [dict(u, i=i,
                           checked=("true" if i == 0 else "false"),
                           hidden=(i > 0))
                      for i, u in enumerate(g["units"])]
        ctx["sizeGuide"] = g

    tabs = []
    for i, tab in enumerate(copy.get("specTabs", [])):
        tabs.append(dict(tab, i=i, selected="true" if i == 0 else "false",
                         hidden=i > 0, tableHtml=spec_table(tab)))
    ctx["specTabs"] = tabs

    ctx["bag"] = [tile_for(row["id"], row) for row in copy.get("bag", [])]

    # ---- finish swatches (clubs) -----------------------------------------
    # Gold and Black are two Shopify products, exactly like the polo colorways,
    # so the same swatch device links them: pick the finish, then the loft and
    # grind. Cole asked for this explicitly when the wedges collapsed into the
    # 01 — without it the Black is unreachable from the Gold's page.
    if prod.get("finishGroup"):
        grp = [x for x in sitemap.PRODUCTS
               if x.get("finishGroup") == prod["finishGroup"] and x["built"]]
        if len(grp) > 1:
            ctx["finishes"] = {
                "label": "Finish",
                "current": prod.get("finish", ""),
                "items": [{"name": x.get("finish", x["name"]), "img": x["img"],
                           "priceLabel": x["priceLabel"],
                           "soldOut": not x["inStock"],
                           "isThis": x["id"] == prod["id"],
                           "href": "{{link:p/%s}}" % x["id"]} for x in grp],
            }

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
        p = cross_sell(row["id"], "%s oav" % prod["id"])
        tag = row.get("tag", "")
        if not p["inStock"]:
            tag = "Sold out"
        rail.append({
            "nm": p["title"], "pr": p["priceLabel"],
            # Cole's rule from §16 note 2 — never a review count on a card —
            # was applied to .pt-rt and missed the browse rail, which was still
            # printing "4.81 ★ 551" on every club. The variant summary is what
            # belongs in this slot: it answers a question a browsing shopper
            # actually has.
            "rt": p["summary"],
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
                cross_sell(o["id"], "%s helpPick" % prod["id"])
                row["href"] = "{{link:p/%s}}" % o["id"]
                row.setdefault("rank", "The other one")
            else:
                row["isThis"] = True
                row["href"] = None
                row.setdefault("rank", "You're looking at this one")
                row.setdefault("foot", "You're on this page")
            opts.append(row)
        pick["options"] = opts
        ctx["helpPick"] = pick

    return ctx


# --------------------------------------------------------------------------
# Collections
# --------------------------------------------------------------------------
def collection_tile(pid, tag=None):
    """A product tile for a collection grid. Same catalogue facts the PLP
    paints in JS, but shaped for the template to render server-side — the club
    collections have no filters, so there is nothing for a script to repaint
    and the grid can just be in the HTML."""
    p = sitemap.product(pid)
    live = [v for v in p["variants"].values() if v["avail"]]
    t = {
        # `title` on the card, not `name`. The short form is ambiguous now that
        # the SKU stamp is gone (Cole 2026-07-31): LGW01 Gold and LGW02 Gold are
        # BOTH "Carver Gold", and the code stamp was the only thing separating
        # them. `title` is Cole's own locked full form — family, code, finish.
        "id": p["id"], "name": p["title"], "title": p["title"],
        "img": p["img"], "priceLabel": p["priceLabel"],
        "inStock": p["inStock"], "soldOut": not p["inStock"],
        "href": "{{link:p/%s}}" % pid, "tag": tag,
    }
    # Same rule as the PLP and the cross-sell tiles: a real Add only where
    # there is genuinely nothing to choose. Every club has at least a hand.
    if p["inStock"]:
        if not p["options"] and len(live) == 1:
            t["addSku"] = live[0]["sku"]
        else:
            t["chooseLabel"] = "Build it"
    return t


def quick_add_data(pids):
    """The variant data the in-card Quick add picker needs, keyed by product id.

    Primo's QUICK ADD does not go to the product page — it opens a size picker
    inside the card and adds from there (Cole, 2026-07-31). Clubs have a hand
    and often a loft, so ours is two steps rather than one, but it is the same
    control. That means a collection page now needs the real option axes and
    the real variant map, which is exactly what the PDP buy box runs on — so
    the pages load `variants.js` and reuse the engine `test-variants.js`
    already covers, rather than growing a second availability implementation.

    Only in-stock products with at least one axis appear. A zero-axis product
    keeps its plain [data-add] button — there is nothing to pick — and a
    sold-out one gets no control at all."""
    out = {}
    for pid in pids:
        p = sitemap.product(pid)
        if not p["options"] or not p["inStock"]:
            continue
        out[pid] = {
            "name": p["name"], "img": p["img"], "default": p["default"],
            "options": p["options"], "variants": p["variants"],
        }
    return out


def collection_siblings(cid):
    """The other collections, for the "rest of the store" row. Generated from
    products.json rather than typed into each template — it was static markup
    in one page and would have been static markup in two, which is how the
    duplicate .ptile rules in core.css started (HANDOFF §16)."""
    return [{"name": c["name"], "href": "{{link:c/%s}}" % c["id"]}
            for c in sitemap.COLLECTIONS
            if c["id"] != cid and not c.get("blocked")]


# --------------------------------------------------------------------------
# The support cluster — returns, shipping, contact, faq
# --------------------------------------------------------------------------
def hand_rows():
    """Which clubs exist in which hand, generated from the catalogue.

    The FAQ's most-asked question is left-hand availability — it comes up in
    the LGP01 and LGP02 reviews more than any other subject. Typing the answer
    into a copy file would make it wrong the first time a loft sells out, and
    "do you make a left-handed one" is precisely the question you cannot afford
    to answer stalely. So it is derived, like every price and count on the site.

    Availability is `avail`, never `qty > 0` (§10c)."""
    rows = []
    for p in sitemap.PRODUCTS:
        if not p["built"] or p["template"] != "club":
            continue
        axes = p["options"]
        hand = next((ax for ax in axes if ax["key"] == "hand"), None)
        if not hand:
            continue
        other = next((ax for ax in axes if ax["key"] != "hand"), None)

        def live(key):
            return p["variants"].get(key, {}).get("avail")

        # "Right hand and Left hand" is how the labels concatenate and not how
        # anyone says it. Collapse the repeated noun where every label carries
        # it, which is the case for every club in the store.
        def phrase(labels):
            if len(labels) > 1 and all(l.lower().endswith(" hand") for l in labels):
                heads = [l[:-len(" hand")] for l in labels]
                return "%s and %s hand" % (heads[0],
                                           " and ".join(h.lower() for h in heads[1:]))
            return " and ".join(labels)

        if other is None:
            declared = [h["label"] for h in hand["values"]]
            offered = [h["label"] for h in hand["values"] if live(h["k"])]
            if not offered:
                v = "%s: sold out at the moment." % phrase(declared)
            elif len(offered) < len(declared):
                v = "%s only." % phrase(offered)
            else:
                v = "%s." % phrase(offered)
        else:
            # The axis NAME reaches the page as markup, and "Loft & grind"
            # carries a bare ampersand.
            axis = other["name"].lower().replace("&", "&amp;")
            parts = []
            for h in hand["values"]:
                got = [o["label"] for o in other["values"] if live(h["k"] + "|" + o["k"])]
                if not got:
                    parts.append("%s: none right now" % h["label"])
                elif len(got) == len(other["values"]):
                    parts.append("%s: every %s" % (h["label"], axis))
                else:
                    parts.append("%s: %s" % (h["label"], ", ".join(got)))
            v = ". ".join(parts) + "."
        rows.append({"k": '<a href="{{link:p/%s}}">%s</a>' % (p["id"], p["title"]), "v": v})
    if not rows:
        sys.exit("hand_rows(): no built club has a hand axis — the FAQ's "
                 "left-hand answer would render empty")
    return rows


def support_copy(slug):
    """Two layers, the same contract as a product page: `_shared-support.json`
    under `_support-<slug>.json`, page file wins outright (§22b). A support
    page without its editorial fails the build rather than rendering a shell."""
    path = os.path.join(SRC, "data", "copy", "_support-%s.json" % slug)
    if not os.path.exists(path):
        sys.exit("support page %s has no editorial: _src/data/copy/_support-%s.json"
                 % (slug, slug))
    copy = json.load(open(os.path.join(SRC, "data", "copy", "_shared-support.json"),
                          encoding="utf8"))
    copy.update(json.load(open(path, encoding="utf8")))
    ctx = {k: v for k, v in copy.items() if not k.startswith("_")}

    # The sibling row is the other three pages, generated rather than typed
    # into four files — the same reason the PLP's is generated (§11d).
    pages = ctx.pop("pages", [])
    ctx["siblings"] = [{"name": p["name"], "hook": p["hook"],
                        "href": "{{link:%s}}" % p["slug"]}
                       for p in pages if p["slug"] != slug]
    if not ctx["siblings"]:
        sys.exit("support page %s is not listed in _shared-support.json's "
                 "`pages` — its sibling row would be empty" % slug)

    # The template engine walks the scope stack OUTWARD (tools/template.py), so a
    # section with no `lede` of its own silently inherits the PAGE's lede, and a
    # `list` with no `title` inherits the SECTION's title. Both render as a
    # duplicated line rather than as nothing, which is how the refund policy came
    # out repeating its own headline twice. Pin the optional keys to "" so the
    # lookup stops here — "" is falsy, so `{{#lede}}` skips the block.
    for sec in ctx.get("sections", []):
        sec.setdefault("lede", "")
        sec.setdefault("note", "")
        if isinstance(sec.get("list"), dict):
            sec["list"].setdefault("title", "")
        for sub in sec.get("sub", []) or []:
            sub.setdefault("lede", "")

    # Every section is an anchor target: the jump nav points at it, and so can
    # a link from anywhere else on the site.
    for sec in ctx.get("sections", []):
        if not sec.get("id"):
            sys.exit("support page %s has a section with no id (%r) — nothing "
                     "can link to it" % (slug, sec.get("title")))

    # "On this page" is opt-in per page: four sections on Contact do not need
    # one and eight on Returns do. Only a section that names itself appears.
    if ctx.get("jump"):
        items = [{"id": s["id"], "label": s.get("nav") or s["title"]}
                 for s in ctx.get("sections", []) if s.get("nav")]
        if not items:
            sys.exit("support page %s asks for a jump nav but no section "
                     "carries a `nav` label" % slug)
        ctx["jump"] = {"items": items}

    for grp in ctx.get("faq", {}).get("groups", []):
        for item in grp.get("items", []):
            if not item.get("id"):
                sys.exit("support page %s has an FAQ item with no id (%r) — the "
                         "deep link into it cannot exist" % (slug, item.get("q")))
            if item.pop("handRows", False):
                item["rows"] = {"items": hand_rows()}

    return ctx


def search_copy():
    """The whole catalogue, flattened for a client-side search.

    43 products is small enough that searching them in the browser is genuinely
    useful rather than a toy (NEXT-PAGES §7), and it is the same shape a
    Shopify search template fills server-side.

    `terms` is what makes the search worth having: the variant LABELS go in, so
    "56" finds the wedge and "left hand" finds every club built in both hands.
    Those are the two things a golfer actually types, and neither one appears
    in a product title."""
    rows, ids = [], []
    for p in sitemap.PRODUCTS:
        if not p["built"]:
            continue
        coll = sitemap.collection(p["collection"])
        terms = [p["code"], p["family"], coll["name"]]
        for ax in p["options"]:
            terms.append(ax["name"])
            terms += [v["label"] for v in ax["values"]]
        live = [v for v in p["variants"].values() if v["avail"]]
        row = {
            "id": p["id"], "name": p["title"], "title": p["title"],
            "family": p["family"], "collName": coll["name"],
            "img": p["img"], "priceLabel": p["priceLabel"],
            "inStock": p["inStock"], "href": "{{link:p/%s}}" % p["id"],
            # SKUs are deliberately NOT searchable: no SKU renders anywhere on
            # the site (§22d), and a search that matches a string it will not
            # then show is a search that looks broken.
            "terms": sorted({t for t in terms if t}),
        }
        if not p["options"] and len(live) == 1:
            row["addSku"] = live[0]["sku"]
        rows.append(row)
        ids.append(p["id"])
    if not rows:
        sys.exit("search page: no built products to search")
    return {"SEARCH_JSON": json.dumps(rows, ensure_ascii=False),
            "QUICKADD_JSON": json.dumps(quick_add_data(ids), ensure_ascii=False)}


def reviews_copy():
    """The all-clubs reviews page: the five Judge.me pulls, merged, with each
    review tagged with the product it is about.

    The counts here are the fiddliest arithmetic on the site, so all of it is
    derived and then CHECKED rather than typed:

      pulled      the five sets in _src/data/reviews/          845
      catalogue   every club in products.json with a rating    815  (incl. the
                                                                    discontinued
                                                                    LGD01 driver)
      merged      a set whose product has left products.json    69  (the S grind,
                                                                    §23)
      clubsWide   catalogue + merged                           884  <- the
                                                                    homepage's
                                                                    number
      elsewhere   clubsWide - pulled                            39  <- must equal
                                                                    the rated
                                                                    clubs with no
                                                                    review file

    If those two ways of reaching 39 ever disagree, the build stops. A reviews
    page whose headline and histogram do not add up is worse than no page."""
    path = os.path.join(SRC, "data", "copy", "_page-reviews.json")
    copy = json.load(open(path, encoding="utf8"))
    ctx = {k: v for k, v in copy.items() if not k.startswith("_")}

    prod_ids = {p["id"] for p in sitemap.PRODUCTS}
    sets, sample, totals, pulled, merged = [], [], {5:0,4:0,3:0,2:0,1:0}, 0, 0
    for spec in ctx.pop("sets", []):
        rp = os.path.join(SRC, "data", "reviews", "%s.json" % spec["file"])
        if not os.path.exists(rp):
            sys.exit("reviews page names %s, which has no pull in "
                     "_src/data/reviews/" % spec["file"])
        data = json.load(open(rp, encoding="utf8"))
        cross_sell(spec["product"], "the reviews page")
        href = "{{link:p/%s}}" % spec["product"]
        t = {int(k): v for k, v in data["totals"].items()}
        for k in totals:
            totals[k] += t.get(k, 0)
        pulled += data["total"]
        if spec["file"] not in prod_ids:
            merged += data["total"]
        sets.append({"id": spec["file"], "name": spec["name"],
                     "total": data["total"], "totals": t, "href": href})
        for r in data["sample"]:
            row = dict(r)
            row["p"], row["pn"], row["ph"] = spec["file"], spec["name"], href
            sample.append(row)

    catalogue = sum(p["rating"]["count"] for p in sitemap.PRODUCTS
                    if p["template"] == "club" and p.get("rating"))
    clubs_wide = catalogue + merged
    elsewhere = clubs_wide - pulled
    # the same 39 reached the other way: a rated club with no pull in the repo
    unpulled = [p for p in sitemap.PRODUCTS
                if p["template"] == "club" and p.get("rating")
                and not os.path.exists(os.path.join(SRC, "data", "reviews",
                                                    "%s.json" % p["id"]))]
    check = sum(p["rating"]["count"] for p in unpulled)
    if check != elsewhere:
        sys.exit("reviews page: %d reviews are unaccounted for. clubs-wide %d "
                 "minus pulled %d is %d, but the clubs with no pull hold %d (%s)."
                 % (abs(check - elsewhere), clubs_wide, pulled, elsewhere, check,
                    ", ".join(p["id"] for p in unpulled) or "none"))

    avg = sum(k * v for k, v in totals.items()) / float(pulled)
    ctx["REVIEWS_JSON"] = json.dumps(
        {"total": pulled, "totals": totals, "products": sets, "sample": sample},
        ensure_ascii=False)
    ctx["figures"] = {
        "avg": "%.2f" % avg,
        "pulled": pulled,
        "clubsWide": clubs_wide,
        "elsewhere": elsewhere,
        "elsewhereWho": ", ".join(p["title"] for p in unpulled),
        "sampleCount": len(sample),
        "setCount": len(sets),
    }
    return ctx


def brand_copy(slug):
    """Our Story and The Trybe. Two layers, same contract as everywhere else:
    `_shared-brand.json` under `_brand-<slug>.json`, page file wins."""
    path = os.path.join(SRC, "data", "copy", "_brand-%s.json" % slug)
    if not os.path.exists(path):
        sys.exit("brand page %s has no editorial: _src/data/copy/_brand-%s.json"
                 % (slug, slug))
    copy = json.load(open(os.path.join(SRC, "data", "copy", "_shared-brand.json"),
                          encoding="utf8"))
    copy.update(json.load(open(path, encoding="utf8")))
    ctx = {k: v for k, v in copy.items() if not k.startswith("_")}

    pages = ctx.pop("pages", [])
    ctx["siblings"] = [{"name": p["name"], "hook": p["hook"],
                        "href": "{{link:%s}}" % p["slug"]}
                       for p in pages if p["slug"] != slug]
    if not ctx["siblings"]:
        sys.exit("brand page %s is not listed in _shared-brand.json's `pages`"
                 % slug)

    # An ambassador page must never print a name nobody agreed to (NEXT-PAGES
    # §4). Roster names stay bracketed until Cole supplies real ones, and the
    # build says so rather than trusting a copy edit to remember.
    ros = ctx.get("roster")
    if ros:
        for s_ in ros.get("slots", []):
            named = not (s_["name"].startswith("[") and s_["name"].endswith("]"))
            if named and not s_.get("consent"):
                sys.exit("brand page %s: roster slot %r carries a real name with "
                         "no `consent` key. Nobody appears on the roster until "
                         "they have agreed to (NEXT-PAGES §4)." % (slug, s_["name"]))
        if not ros.get("slots"):
            sys.exit("brand page %s has a roster with no slots" % slug)

    # Every photo brief has to actually say what the shot is. A `.ph` with an
    # empty label is a grey box, which is the thing this device exists to
    # avoid — the brief travels with the page (HANDOFF §18b).
    briefs = []
    if ctx.get("hero"):
        briefs.append(("hero", ctx["hero"]))
    for i, r in enumerate(ctx.get("rows", [])):
        briefs.append(("row %d" % i, {"k": r.get("phK"), "brief": r.get("phBrief")}))
    for i, s_ in enumerate((ctx.get("roster") or {}).get("slots", [])):
        briefs.append(("roster %d" % i, s_))
    for where, b in briefs:
        if not (b.get("k") and b.get("brief")):
            sys.exit("brand page %s: the %s image slot has no brief. A labelled "
                     "placeholder with no label is just a grey box." % (slug, where))

    return ctx


def home_copy():
    """The homepage's catalogue-driven sections. Only the club finder today.

    It used to hard-code a name, a price and an image per card, and the prices
    had gone stale — both LGW02s said $119 against a real $109. Anything that
    names a product now resolves through products.json like everywhere else."""
    path = os.path.join(SRC, "data", "copy", "_page-home.json")
    copy = json.load(open(path, encoding="utf8"))
    tabs = []
    for i, tab in enumerate(copy["finder"]["tabs"]):
        cards = []
        for c in tab["cards"]:
            p = cross_sell(c["id"], "the homepage finder")
            cards.append({
                "code": p["code"], "name": p["title"], "ln": c["ln"],
                "priceLabel": p["priceLabel"], "img": p["img"],
                "soldOut": not p["inStock"],
                "href": "{{link:p/%s}}" % p["id"],
            })
        tabs.append({"label": tab["label"], "i": i, "cards": cards,
                     "selected": "true" if i == 0 else "false", "hidden": i > 0})
    return {"finderTabs": tabs}


def collection_copy(coll):
    """The editorial layer for a club collection page: bands, the comparison,
    the brand copy under the grid. Same contract as product_copy — a club
    collection without a file fails the build rather than rendering a page
    with holes in it."""
    cid = coll["id"]
    path = os.path.join(SRC, "data", "copy", "_collection-%s.json" % cid)
    if not os.path.exists(path):
        sys.exit("collection %s uses the clp template but has no editorial: "
                 "_src/data/copy/_collection-%s.json" % (cid, cid))
    copy = json.load(open(path, encoding="utf8"))
    ctx = {k: v for k, v in copy.items() if not k.startswith("_")}

    tags = copy.get("tags", {})

    # ---- bands ------------------------------------------------------------
    # Every member of the collection must sit in exactly one band. Without the
    # check, adding a club to products.json would quietly leave it off the page
    # — the failure mode a flat grid does not have and the reason the flat grid
    # was safe to leave unattended.
    placed, bands = [], []
    for b in copy.get("bands", []):
        placed += b["ids"]
        bands.append({
            "label": b["label"], "lede": b.get("lede", ""),
            "tiles": [collection_tile(pid, tags.get(pid)) for pid in b["ids"]],
        })
    if sorted(placed) != sorted(coll["products"]):
        missing = [p for p in coll["products"] if p not in placed]
        extra = [p for p in placed if p not in coll["products"]]
        sys.exit("collection %s bands do not match membership%s%s"
                 % (cid,
                    ("\n  not in any band: " + ", ".join(missing)) if missing else "",
                    ("\n  banded but not in the collection: " + ", ".join(extra)) if extra else ""))
    if len(placed) != len(set(placed)):
        sys.exit("collection %s lists a product in two bands" % cid)
    ctx["bands"] = bands

    # ---- the comparison ---------------------------------------------------
    # Bars are segmented, and every segment count comes off a REAL published
    # number with the number printed beside it. There is no forgiveness or
    # workability bar, because nobody has measured one — the same rule that
    # makes the spec tables carry "Needs spec" instead of a guess.
    cmp_ = copy.get("compare")
    if cmp_:
        scales = cmp_["scales"]
        items = []
        for row in cmp_["items"]:
            # A column can describe a product that does not exist yet — the
            # wedge page's whole job is the 01 against the 02 (Cole,
            # 2026-07-31) and the 02 is not in Shopify. A `coming` column has
            # no catalogue lookup, no price, no bars and no buy link: it
            # carries its feature list and says it is coming, which is all
            # that is true about it.
            if row.get("coming"):
                items.append({
                    "coming": True, "name": row["name"], "soon": row.get("soon", "Coming"),
                    "photo": row.get("photo", ""),
                    "forWho": row["forWho"], "facts": row["facts"],
                    "note": row.get("note", ""),
                })
                continue
            p = sitemap.product(row["id"])
            bars = []
            for sc in scales:
                b = row["bars"][sc["k"]]
                lo, hi = b.get("from", 0), b["to"]
                bars.append({
                    "label": sc["label"], "display": b["display"],
                    "segs": [{"on": lo <= i < hi} for i in range(sc["segs"])],
                })
            items.append({
                "name": p["title"], "img": p["img"],
                "priceLabel": p["priceLabel"], "soldOut": not p["inStock"],
                "href": "{{link:p/%s}}" % p["id"],
                "forWho": row["forWho"], "bars": bars,
                "facts": row["facts"], "cta": row.get("cta", "See it"),
            })
        ctx["compare"] = dict(cmp_, items=items,
                              scaleNotes=[s["note"] for s in scales if s.get("note")])

    # ---- the family router (All Clubs only) -------------------------------
    if copy.get("router"):
        r = dict(copy["router"])
        r["cards"] = [dict(c, href="{{link:c/%s}}" % c["to"])
                      for c in r["cards"]]
        ctx["router"] = r

    # ---- the testimonial --------------------------------------------------
    # Verbatim Judge.me, and the product it is actually about is named and
    # linked. A quote floating free of the club it praises is the kind of thing
    # that reads as invented even when it is not.
    if copy.get("quote"):
        q = dict(copy["quote"])
        p = sitemap.product(q["id"])
        q["product"] = p["title"]
        q["href"] = "{{link:p/%s}}" % p["id"]
        ctx["quote"] = q

    ctx["siblings"] = collection_siblings(cid)
    ctx["UPSELL_JSON"] = json.dumps(copy.get("upsell", []), ensure_ascii=False)
    ctx["QUICKADD_JSON"] = json.dumps(quick_add_data(coll["products"]),
                                      ensure_ascii=False)
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

    if slug == "home":
        ctx.update(home_copy())

    if page.kind == "support":
        ctx.update(support_copy(slug))

    if page.kind == "brand":
        ctx.update(brand_copy(slug))

    if slug == "reviews":
        ctx.update(reviews_copy())

    if slug == "search":
        ctx.update(search_copy())

    if page.kind == "product":
        prod = sitemap.product(slug.split("/", 1)[1])
        ctx["PRODUCT_JSON"] = json.dumps(prod, ensure_ascii=False, sort_keys=False)
        ctx.update(product_copy(prod))

    if page.kind == "collection":
        coll = sitemap.collection(slug.split("/", 1)[1])
        ctx["COLL_NAME"] = coll["name"]
        ctx["COLL_EYEBROW"] = coll["eyebrow"]
        ctx["COLL_LEDE"] = coll["lede"]
        ctx["COLL_COUNT"] = "%d %s" % (coll["count"],
                                       "club" if coll["count"] == 1 else "clubs")

        # The club collections are a page, not a product list (GAMEPLAN §13.3).
        # They render their grid server-side in bands and have no filters, so
        # none of the PLP's tile-painting or sort-trimming applies.
        if coll["tpl"] == "clp":
            ctx.update(collection_copy(coll))
            return ctx

        # Tiles carry only what the grid renders and sorts on. The href is a
        # registry token so these links are audited like any other, even
        # though the tile itself is painted by JS.
        tiles = []
        for pid in coll["products"]:
            p = sitemap.product(pid)
            tile = {
                "id": p["id"], "code": p["code"], "name": p["title"],
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
                # "Choose hand" was wrong on a wedge, where there is also a loft
                # to pick. Clubs get one honest label; apparel keeps the
                # specific one because size really is the only choice there.
                tile["chooseLabel"] = ("Choose size" if p["template"] == "apparel"
                                       else "Build it")
            if p.get("rating"):
                tile["rating"] = p["rating"]
            tiles.append(tile)
        ctx["COLLECTION_JSON"] = json.dumps(
            {"id": coll["id"], "name": coll["name"],
             "facets": coll["facets"], "products": tiles},
            ensure_ascii=False, sort_keys=False)
        ctx["siblings"] = collection_siblings(coll["id"])
        ctx["QUICKADD_JSON"] = json.dumps(quick_add_data(coll["products"]),
                                          ensure_ascii=False)

    return ctx


def build(slug, report):
    page = sitemap.PAGES[slug]
    if not page.built:
        sys.exit("%s is declared but not built — nothing to assemble" % slug)
    src = page.src
    ctx = page_context(slug)
    # what THIS page must contain, decided from its own context rather than
    # from its template — see smoke(). One template can serve pages that carry
    # genuinely different blocks: the size guide only exists on a product with
    # a size axis, the accordion only on the FAQ, the form only on Contact.
    page.extra_required = []
    if ctx.get("sizeGuide"):
        page.extra_required.append('id="md-size"')
    if ctx.get("faq"):
        page.extra_required.append('<details class="sup-q"')
    if ctx.get("form"):
        page.extra_required.append('id="sup-contact"')
    # The ambassador application (brand template). The id proves the form
    # rendered; the function name proves page-brand.js made the bundle — a
    # form whose submit navigates to nowhere is a page that looks right and
    # does nothing. Marker verified unique to page-brand.js (§21i).
    if ctx.get("apply"):
        page.extra_required += ['id="amb-apply"', 'function brApplyIntercept']

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
        # The review widget is shared with 32-reviews.html, so it is its own
        # file — pdp.js only mounts it. Must load BEFORE pdp.js, which calls
        # LG_REVIEWS.mount() at parse time.
        js += read("reviews.js") + "\n\n"
        js += template.render(read("pdp.js"), ctx, "pdp.js") + "\n\n"
    # Collection pages get the variant engine too: the in-card Quick add picker
    # runs the same cascading-availability rules as the buy box, and a second
    # implementation of "is this combination sellable" is the last thing this
    # site needs. core.js reads LG_QUICKADD and LG_VARIANTS if both are present.
    # The all-clubs reviews page runs the same widget the PDPs do, so it needs
    # the same file — and BEFORE its own script, which calls mount().
    if slug == "reviews":
        js = read("reviews.js") + "\n\n"
    # Search results carry the in-card quick add, which runs on the same axis
    # engine the buy box and the collection grids do — never a second copy of
    # "is this combination sellable" (§21a).
    if slug == "search":
        js = read("variants.js") + "\n\n"
    if page.kind == "collection":
        js = read("variants.js") + "\n\n"
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
        # the club finder: fixed columns (auto-fit blew a one-card panel up to
        # full width) and cards that are actually links
        ".fnd-grid{display:grid;grid-template-columns:repeat(3,1fr)",
        '<a class="fnd-c"',
    ],
    "club": [
        ".msnap{",
        ".atc-bar--on{transform:translateY(0)}",  # mobile sticky add-to-cart, fallback-only since 2026-08-18
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
        # reviews.js, uniquely. It moved out of pdp.js so 32-reviews.html can
        # run the same widget, and a missing bundle leaves the histogram, the
        # star filter and the whole review list silently empty.
        "var LG_REVIEWS = (function(){",
        # NOT "LG_VARIANTS": core.js's quick-add now names it too, so the
        # marker survived emptying variants.js entirely. A smoke marker has to
        # be a string that exists in exactly ONE source file (§12d again).
        "function offered(pd, sel, i, val)",   # variants.js — the axis engine
        "function paintLoftFinder",      # page-club.js — the wedge ladder
    ],
    "apparel": [
        'id="pickers"', "function paintPickers",
        "function offered(pd, sel, i, val)",   # variants.js, uniquely
        ".sibs{",                        # the colourway strip — the range dies without it
        # the size guide is a modal now, not a section. Three parts, and the
        # page looks fine without any of them: the trigger, the panel and the
        # unit toggle that makes two tables into one control.
        # the trigger wiring and the toggle styles, which every apparel page
        # carries. The modal ITSELF is per-page — see smoke()'s `extra`.
        "md: 'md-size'", ".sg-unit{",
        # page-apparel.js. Without it the modal still renders and the unit
        # radios still look like controls — they just do nothing, and the cm
        # table is never reachable. Marker chosen because it exists in that
        # file and nowhere else (§21i).
        "querySelector('.sg-units')",
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
        # the in-card Quick add: engine, data and panel. Without any one of the
        # three the pill still renders and simply does nothing when clicked.
        "function offered(pd, sel, i, val)",   # variants.js, uniquely
        "LG_QUICKADD", ".qa-chip{", "function paint(panel)",
    ],
    "search": [
        'id="se-grid"', 'id="se-empty"', 'id="se-start"',   # results, empty, pre-query
        "function offered(pd, sel, i, val)",   # variants.js, uniquely — quick add
        "LG_QUICKADD", ".qa-chip{", "function paint(panel)",
        ".ptile{",                             # the tile is core's, not a copy
        "@media (max-width:620px)",
    ],
    "404": [
        ".nf-in{", '<section class="nf"',
        "@media (max-width:620px)",
    ],
    "reviews": [
        "var LG_REVIEWS = (function(){",   # reviews.js, uniquely
        "LG_REVIEWS.mount(",               # page-reviews.js — the mount call
        'id="jm-prods"',                   # the club filter, this page only
        ".jm-p{", ".jm{", ".jr{",          # the widget, promoted to core
        '<section class="rv-fit"',
        "@media (max-width:620px)",
    ],
    "brand": [
        # the brand field, once, and never against the ink footer
        '<section class="br-fit"', ".br-fit{",
        ".ph{",                          # the labelled placeholder — core
        ".br-row-in{display:grid",       # the alternating photo/copy rows
        ".tbd{",
        # .msnap is what stops the roster and the row stack becoming six
        # screens on a phone; it lives in core and is a layout-mode switch
        ".msnap{display:grid",
        "@media (max-width:980px)",
        "@media (max-width:620px)",
    ],
    "support": [
        # The brand field, once per page and never against the ink footer —
        # the cream sibling band below it is what keeps two dark bands apart.
        '<section class="sup-still"', ".sup-still{",
        ".sup-quick{",                   # the answer above the fold
        ".sup-rows{",                    # the key/value blocks the policy lives in
        # The FAQ is <details>, so it opens with no JS. This is the one thing
        # native <details> cannot do, and without it a link into a closed
        # answer lands on a collapsed row — a page that looks right and does
        # nothing, which is what this list is for.
        "function supOpenFromHash",      # page-support.js, uniquely
        ".sup-q summary{",
        # .tbd is the whole reason an unconfirmed policy detail is visible as a
        # gap rather than as prose. It lives in core, so this also proves core
        # is bundled ahead of the page stylesheet.
        ".tbd{",
        "@media (max-width:620px)",
    ],
    "clp": [
        # The grid is server-rendered here, so its absence is a blank page
        # rather than a page that looks right and does nothing. The bars are
        # the part with no analogue anywhere else in the site.
        '<section class="sec clp-bands"',
        ".clp-seg{",                         # the segmented spec bar
        ".clp-seg i[data-on]{",              # ...and its lit segment
        ".clp-tag{",                         # the character chip under the price
        ".clp-fit{",                         # the fitting CTA, on the brand field
        ".clp-grid{grid-template-columns:repeat(2,1fr)",   # phone grid
        "@media (max-width:620px)",
        "function offered(pd, sel, i, val)",   # variants.js, uniquely
        "LG_QUICKADD", ".qa-chip{", "function paint(panel)",
    ],
}


def smoke(src, html, extra=()):
    """`extra` is per-PAGE rather than per-template. The size-guide modal only
    exists on a product that has a size axis, so it cannot live in REQUIRED —
    that list runs against every hat as well as every polo."""
    missing = [n for n in list(REQUIRED.get(src, [])) + list(extra) if n not in html]
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
        smoke(page.src, html, getattr(page, "extra_required", ()))
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
