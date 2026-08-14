"""
_src/data/shopify-raw.json + the EDITORIAL overlay below  ->  _src/data/products.json

    python tools/normalize-products.py            # write
    python tools/normalize-products.py --check    # diff only, exit 1 if stale

WHY THIS EXISTS
---------------
Shopify is the source of truth for prices, SKUs, options and availability.
It is *not* the source of truth for brand names, families, or which PDP
template a product uses — none of that exists in the store. This script joins
the two so `products.json` can be a single build input, and so re-pulling the
catalogue never clobbers the editorial layer.

RE-PULLING THE CATALOGUE
------------------------
Four Shopify MCP queries produced shopify-raw.json (2026-07-31):

  1. products(first:50, sortKey:PRODUCT_TYPE) { handle title productType status
       totalInventory options{name values} variantsCount{count}
       priceRangeV2{...} featuredMedia{...on MediaImage{image{url}}} }
     ...then the second page via `after: pageInfo.endCursor`.
  2. the same filtered to the club/gear product types, with
       variants(first:20){nodes{sku price availableForSale inventoryQuantity
                                 selectedOptions{name value}}}
  3. the same for `status:active AND product_type:Apparel`
  4. the same for `status:active AND product_type:HAT`, plus
       collections(first:25){nodes{handle title productsCount{count}}}

Paste the results into shopify-raw.json in the shape already there, then run
this script. Excluded from the pull: gift card, the Checkout+ app product,
archived products and the UNLISTED shaft (see raw `_excluded`).

TRAPS THIS SCRIPT ENCODES — each one was found in the real data
--------------------------------------------------------------
* `availableForSale` is NOT `inventoryQuantity > 0`. Several products oversell
  (glove LH Small: qty -3, still sellable) and several sit at qty 0 while still
  purchasable (the black clover grips). Availability drives whether a chip is
  disabled; quantity only drives the "Low stock — N left" line. Keying the buy
  box off quantity would have disabled sellable variants and sold dead ones.
* SKUs are NOT derivable from a pattern. LGW02 Black's 50 and 52 are stamped
  `LGW03-...` (a typo in Shopify) while 54-60 are `LGW02-...`; the mallet cover
  is `HeadCover-Mallet-SignatureWhite-RH` in one hand and
  `Putter-Cover-Mallet-Signature-White-LH` in the other. Every SKU is carried
  verbatim from Shopify. Never synthesise one.
* Price is per-variant, not per-product. Grips run $9.95 / $11.95 / $14.95
  across Standard / Midsize / Jumbo, and the oversized putter grips run
  $19.95 to $26.95. The buy box has to repaint the price on selection.
* A `Title` option with one value is Shopify's "this product has no options"
  sentinel. It becomes zero axes here, not a one-value picker. `Lucky Golf
  Tees` uses the same sentinel with the value "25 Tees" rather than
  "Default Title", so the rule keys off the option NAME plus a single value.
"""
import argparse
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "_src", "data")
RAW = os.path.join(DATA, "shopify-raw.json")
OUT = os.path.join(DATA, "products.json")

IMG_BASE = "https://cdn.shopify.com/s/files/1/2286/3149/"

# --------------------------------------------------------------------------
# Option normalisation. Shopify is inconsistent across product types — wedges
# say "Right Hand", putters and covers say "Right" — so both collapse to one
# key. `k` is the stable key used in variant keys and the DOM; `label` is what
# the chip shows.
# --------------------------------------------------------------------------
OPTION_KEY = {
    "Hand": "hand",
    "Loft": "loft",
    "Size": "size",
    "Grip Size": "gripsize",
}

VALUE_MAP = {
    "hand": {
        "Right Hand": ("RH", "Right hand"), "Right": ("RH", "Right hand"),
        "Left Hand": ("LH", "Left hand"),   "Left":  ("LH", "Left hand"),
    },
    "size": {
        "Small": ("S", "S"), "Medium": ("M", "M"), "Large": ("L", "L"),
        "Extra Large": ("XL", "XL"),
        "XL": ("XL", "XL"), "XXL": ("XXL", "XXL"), "3XL": ("3XL", "3XL"),
    },
    "gripsize": {
        "Standard": ("STD", "Standard"), "Midsize": ("MID", "Midsize"),
        "Jumbo": ("JMB", "Jumbo"), "Lady": ("LDY", "Lady"),
    },
}


def norm_value(key, raw):
    """-> (stable key, display label). Lofts and putter-grip sizes fall through
    to the identity mapping: '56°' -> ('56', '56°'), '2.0' -> ('2.0', '2.0')."""
    m = VALUE_MAP.get(key, {})
    if raw in m:
        return m[raw]
    if key == "loft":
        return (raw.replace("°", ""), raw)
    return (raw, raw)


# --------------------------------------------------------------------------
# EDITORIAL OVERLAY — hand-maintained. Shopify holds none of this.
#
#   id       our slug. Drives the page filename and the {{link:p/<id>}} token,
#            so it is a routing identifier: renaming one moves a URL.
#   tpl      which PDP template renders it — club | apparel | gear (GAMEPLAN 3)
#   fam      family, drives the help-me-choose module and the breadcrumb
#   name     short form for product tiles, where `code` is stamped beside it
#   title    the full name: family, code, finish. Drives the H1, the page
#            <title> and breadcrumbs. Clubs only; apparel and gear fall back
#            to `name`. Locked by Cole 2026-07-31 — do not re-litigate.
#   coll     our collection slug for the breadcrumb (see COLLECTIONS)
#   rating   [average, count] from Judge.me (HANDOFF 5). Absent = no reviews.
#   default  variant key to preselect. LGW01 is pinned to RH|56 because that is
#            what the shipped page selects; everything else takes the first
#            available variant.
#   built    True once a real page exists. The link registry resolves tokens
#            for unbuilt pages to "#" and reports the count.
#   discon   Discontinued. Still in the Shopify pull, deliberately NOT in any
#            collection: a tile for a product with no page is a dead link, and
#            a 0-axis one even rendered a working Quick add. `built` alone was
#            not enough, because "not written yet" and "never again" are
#            different states and only the second should leave the grid.
# --------------------------------------------------------------------------
EDITORIAL = {
    # --- clubs -------------------------------------------------------------
    # THE 01. Everything Lucky sells in a wedge today is this club — the K
    # grind and the S grind are options on it, not tiers (Cole 2026-07-31).
    # `merge` folds another Shopify product's variants in as a second grind;
    # `axisGrind` turns Loft into a combined "Loft & grind" axis (50K, 52K,
    # 52S, ...); `priceAll` puts one price on the whole product, which is the
    # point of the merge. Every SKU is still carried verbatim from Shopify.
    "v1-gold-lucky-golf-wedge": dict(
        id="lgw01-gold", tpl="club", fam="wedge", code="LGW01", name="Carver 01 Gold",
        title="Carver 01 Gold",
        coll="wedges", rating=[4.81, 551], built=True,
        file="02-pdp-lgw01.html",
        finish="Gold", grind="K", finishGroup="carver-01",
        merge=["v2-signature-gold-wedge-1"], axisGrind=True, priceAll=99,
        default="RH|56K"),
    # FOLDED INTO lgw01-gold. Cole 2026-07-31: the S-grind gold was never a
    # different club, only a different grind, and the price gap it carried was
    # for a difference that did not exist. Its six variants become the "S" half
    # of the Gold product's Loft & grind axis, at $99 with their real SKUs.
    # Delete this entry once the merge is done in Shopify and the pull reflects it.
    "v2-signature-gold-wedge-1": dict(
        id="lgw02-gold", tpl="club", fam="wedge", code="LGW01", name="Carver 01 Gold",
        title="Carver 01 Gold", coll="wedges", grind="S",
        merged_into="lgw01-gold"),
    "lucky-golf-lgw02-black": dict(
        id="lgw01-black", tpl="club", fam="wedge", code="LGW01", name="Carver 01 Black",
        title="Carver 01 Black",
        coll="wedges", finish="Black", grind="K", finishGroup="carver-01",
        axisGrind=True, default="RH|56K",
        note="RIGHT HAND ONLY today; left hand is coming (Cole). $109 against the "
             "Gold's $99 — the black finish is a real extra process, which is the "
             "one price difference in the wedge line that stands for something.",
        built=True),
    "signature-gold-putters": dict(
        id="lgp01-gold", tpl="club", fam="putter", code="LGP01", name="Tracer Blade",
        title="Tracer LGP01 Blade",
        coll="putters", rating=[4.86, 147],
        note="Sold out (qty -12, availableForSale false) and right hand only.", built=True),
    "limited-edition-mallet-putter": dict(
        id="lgp02-gold", tpl="club", fam="putter", code="LGP02", name="Tracer Mallet",
        title="Tracer LGP02 Mallet",
        coll="putters", rating=[4.71, 58], built=True),
    "lgp02-mallet-putter-patriot": dict(
        id="lgp02-patriot", tpl="club", fam="putter", code="LGP02", name="Tracer Patriot",
        title="Tracer LGP02 Patriot",
        coll="putters", discon=True,
        note="DISCONTINUED 2026-07-31 (Cole). A fifty-unit run for America's 250th, sold out and being removed from Shopify. Page unbuilt."),
    "lucky-striker-hybrid-limited-edition": dict(
        id="lgh01", tpl="club", fam="hybrid", code="LGH01", name="Stryker",
        title="Stryker LGH01",
        coll="hybrid", rating=[4.60, 20], built=True),
    "lucky-gold-driver-pre-order_": dict(
        id="lgd01", tpl="club", fam="driver", code="LGD01", name="Lucky Driver",
        title="Lucky Driver LGD01",
        coll="hybrid", rating=[4.33, 39], discon=True,
        note="DISCONTINUED 2026-07-31 (Cole). This is an old driver that is being removed from Shopify; a new one is coming and its specs are not in the reference guide yet. Page unbuilt — do not rebuild until the new driver's data lands."),

    # --- apparel: classic polos -------------------------------------------
    "gold-dust-classic-polo":      dict(id="polo-gold-dust",      tpl="apparel", fam="polo-classic", code="LGA-CP", name="Gold Dust Classic Polo",      coll="polos", built=True),
    "shadow-classic-polo":         dict(id="polo-shadow",         tpl="apparel", fam="polo-classic", code="LGA-CP", name="Shadow Classic Polo",         coll="polos", built=True),
    "signature-black-classic-polo":dict(id="polo-signature-black",tpl="apparel", fam="polo-classic", code="LGA-CP", name="Signature Black Classic Polo",coll="polos", built=True),
    "contour-classic-polo":        dict(id="polo-contour",        tpl="apparel", fam="polo-classic", code="LGA-CP", name="Contour Classic Polo",        coll="polos", built=True),
    "marble-classic-polo":         dict(id="polo-marble",         tpl="apparel", fam="polo-classic", code="LGA-CP", name="Marble Classic Polo",         coll="polos", built=True),
    "gold-carnation-classic-polo": dict(id="polo-gold-carnation", tpl="apparel", fam="polo-classic", code="LGA-CP", name="Gold Carnation Classic Polo", coll="polos", built=True),
    "frost-classic-polo":          dict(id="polo-frost",          tpl="apparel", fam="polo-classic", code="LGA-CP", name="Frost Classic Polo",          coll="polos", built=True),
    "cruiser-classic-polo":        dict(id="polo-cruiser",        tpl="apparel", fam="polo-classic", code="LGA-CP", name="Cruiser Classic Polo",        coll="polos", built=True),
    "azalea-classic-polo":         dict(id="polo-azalea",         tpl="apparel", fam="polo-classic", code="LGA-CP", name="Azalea Classic Polo",         coll="polos", built=True),
    "nightshade-classic-polo":     dict(id="polo-nightshade",     tpl="apparel", fam="polo-classic", code="LGA-CP", name="Nightshade Classic Polo",     coll="polos", built=True),

    # --- apparel: blade polos ---------------------------------------------
    "swirl-blade-polo":    dict(id="polo-swirl",    tpl="apparel", fam="polo-blade", code="LGA-BP", name="Swirl Blade Polo",    coll="polos", built=True),
    "spot-blade-polo":     dict(id="polo-spot",     tpl="apparel", fam="polo-blade", code="LGA-BP", name="Spot Blade Polo",     coll="polos", built=True),
    "blackout-blade-polo": dict(id="polo-blackout", tpl="apparel", fam="polo-blade", code="LGA-BP", name="Blackout Blade Polo", coll="polos", built=True),

    # --- hats. Zero axes, so they exercise the 0-axis buy box too. ---------
    "white-gold-classic-hat":                 dict(id="hat-white-gold-classic",  tpl="apparel", fam="hat", code="HAT", name="White | Gold Classic Hat", coll="hats", built=True),
    "white-its-better-to-be-lucky-patch-hat": dict(id="hat-white-ibtbl",         tpl="apparel", fam="hat", code="HAT", name="It's Better To Be Lucky Hat, white", coll="hats", built=True),
    "cream-upside-down-hat":                  dict(id="hat-cream-updown",        tpl="apparel", fam="hat", code="HAT", name="Cream Upside Down Hat",    coll="hats", built=True),
    "black-its-better-to-be-lucky-patch-hat": dict(id="hat-black-ibtbl",         tpl="apparel", fam="hat", code="HAT", name="It's Better To Be Lucky Hat, black", coll="hats", built=True),
    "tan-cursive-hat":                        dict(id="hat-tan-cursive",         tpl="apparel", fam="hat", code="HAT", name="Tan Cursive Hat",          coll="hats", built=True),
    "black-gold-classic-lucky-hat":           dict(id="hat-black-gold-classic",  tpl="apparel", fam="hat", code="HAT", name="Black | Gold Classic Hat", coll="hats", built=True, note="Sold out."),
    "white-black-upside-down-hat":            dict(id="hat-white-black-updown",  tpl="apparel", fam="hat", code="HAT", name="White/Black Upside Down Hat", coll="hats", built=True),
    "white-upside-down-hat":                  dict(id="hat-white-updown",        tpl="apparel", fam="hat", code="HAT", name="White Upside Down Hat",    coll="hats", built=True,
                                               note="59.webp has inverted lettering (HANDOFF 6) and is EXCLUDED from the gallery. The product has ten photos; the other nine are fine and the page leads on 60.webp."),
    "white-cursive-hat":                      dict(id="hat-white-cursive",       tpl="apparel", fam="hat", code="HAT", name="White Cursive Hat",        coll="hats", built=True),
    "baby-blue-cursive-hat":                  dict(id="hat-baby-blue-cursive",   tpl="apparel", fam="hat", code="HAT", name="Baby Blue Cursive Hat",    coll="hats", built=True),

    # --- gear --------------------------------------------------------------
    "lucky-putter-head-cover-blade":        dict(id="cover-blade",   tpl="gear", fam="headcover", code="HC", name="Lucky Blade Cover",  coll="gear", built=True),
    "driver-head-cover":                    dict(id="cover-driver",  tpl="gear", fam="headcover", code="HC", name="Driver Head Cover",  coll="gear", built=True),
    "lucky-putter-head-cover-mallet-large": dict(id="cover-mallet",  tpl="gear", fam="headcover", code="HC", name="Lucky Mallet Cover", coll="gear", built=True),
    "lucky-clover-tour-glove":              dict(id="glove-tour",    tpl="gear", fam="glove",     code="CLG1", name="Lucky Tour Glove", coll="gear", built=True,
                                                 note="Two axes on a $17.95 item — Hand x Size. Only the two left-hand small/medium "
                                                      "variants are sellable, and both are oversold. Nearly every chip renders dead."),
    "copy-of-lucky-golf-clover-grips-green":                dict(id="grip-clover-green",  tpl="gear", fam="grip", code="GRP", name="Tour Performance Clover Grips, green", coll="gear", built=True),
    "lucky-golf-performance-x2-clover-grips-black":         dict(id="grip-clover-black",  tpl="gear", fam="grip", code="GRP", name="Tour Performance Clover Grips, black", coll="gear", built=True),
    "copy-of-lucky-golf-performance-x2-clover-grips-white": dict(id="grip-clover-white",  tpl="gear", fam="grip", code="GRP", name="Tour Performance Clover Grips, white", coll="gear", built=True),
    "lucky-golf-performance-x2-clover-grips-blue":          dict(id="grip-clover-blue",   tpl="gear", fam="grip", code="GRP", name="Tour Performance Clover Grips, blue",  coll="gear", built=True),
    "lucky-golf-performance-x2-clover-grips-pink":          dict(id="grip-clover-pink",   tpl="gear", fam="grip", code="GRP", name="Tour Performance Clover Grips, pink",  coll="gear", built=True,
                                                                note="Lady size only — a one-value axis, which should render as a stated fact, not a picker."),
    "lucky-golf-oversized-putter-grip":                     dict(id="grip-putter-green",  tpl="gear", fam="grip", code="GRP", name="Green Oversized Putter Grip",  coll="gear", built=True, note="Entirely sold out."),
    "lucky-golf-clovers-oversized-putter-grip":             dict(id="grip-putter-clovers",tpl="gear", fam="grip", code="GRP", name="Clovers Oversized Putter Grip",coll="gear", built=True, note="Entirely sold out."),
    "stock-putter-grips":                                   dict(id="grip-putter-stock",  tpl="gear", fam="grip", code="GRP", name="Stock Putter Grip",  coll="gear", built=True),
    "lucky-golf-tees": dict(id="tees-25", tpl="gear", fam="tee", code="TEES", name="Lucky Golf Tees", coll="gear", built=True,
                            note="NO IMAGE IN SHOPIFY. featuredMedia is null — the only product in the store with no photo at all."),
}

# Our collections. `shopify` is the real handle where one exists; Gear and the
# three roll-ups have none, which is HANDOFF 7b item E.
#
# Membership is computed from `fams` — the family assignments above are the
# single source of truth, so a product cannot be in a collection and missing
# from the store's own grouping. `members` overrides that for a collection whose
# contents are curated rather than structural; no collection uses it today (Sale
# was the only one, and it is gone — see below).
#
# `facets` are the filter chips on the PLP: family keys the visitor can narrow
# by. Omitted where there is only one family and a filter row would be noise.
#
# `tpl` picks the template. Club collections run `clp` — bands, a comparison
# with spec bars, a fitting CTA and brand copy under the grid (GAMEPLAN §13.3,
# Takomo's Iron Sets page). Everything else runs the flat filtered grid `plp`,
# which is the right page for thirteen polos and wrong for six clubs.
COLLECTIONS = [
    dict(id="clubs", name="All Clubs", shopify="lucky-golf-clubs", tpl="clp",
         fams=["wedge", "putter", "hybrid", "driver"],
         facets=[("wedge", "Wedges"), ("putter", "Putters"),
                 ("hybrid", "Hybrid"), ("driver", "Driver")],
         eyebrow="The full bag",
         lede="Wedges, putters and a hybrid. The same standard the big names charge "
              "triple for, without the sponsorships and the middlemen in the price."),
    dict(id="wedges", name="Wedges", shopify=None, fams=["wedge"], tpl="clp",
         eyebrow="The scoring clubs",
         lede="The clubs you use most and think about least. Pick the loft you keep "
              "missing and the finish you want to look down at."),
    dict(id="putters", name="Putters", shopify=None, fams=["putter"], tpl="clp",
         eyebrow="On the green",
         lede="Two heads, same loft, same lie, same length. Which one you want comes "
              "down to how much the putter should tell you about a miss."),
    # Was "Hybrid & Driver". The driver is discontinued and the new one's specs
    # are not in the reference guide yet (HANDOFF §15a, §17a), so a collection
    # named after it held one hybrid and one dead tile. Renaming moves the URL —
    # 10-collection-hybrid-driver.html is deleted, not left orphaned.
    dict(id="hybrid", name="Hybrid", shopify=None, fams=["hybrid", "driver"],
         tpl="clp",
         eyebrow="The long approach",
         lede="One club for when the green is still a long way off and the lie isn't "
              "helping. Titanium, nineteen degrees, and easier to hit than the iron "
              "it replaces."),
    dict(id="polos", name="Polos", shopify="polos",
         fams=["polo-classic", "polo-blade"],
         facets=[("polo-classic", "Classic collar"), ("polo-blade", "Blade collar")],
         eyebrow="On the course, and after",
         lede="Cut to play in and comfortable enough to keep on afterwards. Thirteen "
              "patterns, and none of them shout."),
    dict(id="hats", name="Hats", shopify="hats", fams=["hat"],
         eyebrow="Five-panel, snapback",
         lede="Ten of them, in the colours we actually wear. Pick the one that goes "
              "with the rest of what you own."),
    dict(id="gear", name="Gear", shopify=None,
         fams=["headcover", "glove", "grip", "tee"],
         facets=[("headcover", "Head covers"), ("grip", "Grips"),
                 ("glove", "Gloves"), ("tee", "Tees")],
         eyebrow="The rest of it",
         lede="Covers, grips, gloves and tees. The small things that wear out first "
              "and get replaced last."),

    # SALE — REMOVED 2026-08-13 (Cole: "that was a long time ago").
    #
    # It was declared here but never built, and it was the site's only `blocked`
    # collection. Shopify's "Summer Warehouse Sale" holds six grip products plus
    # three ARCHIVED hats, and not one variant carries a real compareAtPrice —
    # every value is null or "0.00", re-verified against the live store on
    # 2026-08-13. A page headed Sale showing six full-price grips is a lie, and
    # the green oversized putter grip in it is sold out entirely.
    #
    # Nothing on the site ever linked to it: there was no {{link:c/sale}} token
    # anywhere in _src/, and `collection_siblings()` already skipped `blocked`
    # collections, so removing the entry changes no page's output. All it does
    # is stop the registry declaring a page nobody could reach.
    #
    # TO BRING IT BACK for a real promotion: re-add a dict here with the members
    # you want, set genuine compareAtPrices in Shopify, and ADD A NAV OR FOOTER
    # ENTRY — without one the page builds and stays unreachable.
    #
    # The `blocked` mechanism itself stays. It is how a collection gets a routed
    # slug and an explained absence instead of a dangling link, and the next
    # collection that is real in Shopify but not ready here will want it.
]


def live_values(options, variants, i):
    """The values on axis i that some sellable variant actually reaches. A
    collection tile promising "6 lofts" when two are dead is a small lie that
    the visitor discovers one click later."""
    out = []
    for v in options[i]["values"]:
        for k, var in variants.items():
            if var["avail"] and k.split("|")[i] == v["k"]:
                out.append(v)
                break
    return out


def axis_summary(options, variants):
    """One short line per axis for the collection tile — what you get to pick.
    Counting is right for lofts (nobody reads six numbers on a tile), naming is
    right for hands and grip sizes, and a range is right for clothing sizes."""
    parts = []
    for i, opt in enumerate(options):
        live = live_values(options, variants, i)
        if not live:
            continue
        labels = [v["label"] for v in live]
        if opt["key"] == "loftgrind":
            lofts = sorted({v["k"][:-1] for v in live}, key=float)
            grinds = sorted({v["k"][-1] for v in live})
            parts.append("%d loft%s · %s grind"
                         % (len(lofts), "" if len(lofts) == 1 else "s",
                            " and ".join(grinds)))
        elif opt["key"] == "hand":
            parts.append("Right & left hand" if len(labels) > 1 else labels[0] + " only")
        elif opt["key"] == "loft":
            parts.append("%d loft%s" % (len(labels), "" if len(labels) == 1 else "s"))
        elif opt["key"] == "size" and len(labels) > 2:
            parts.append("%s–%s" % (labels[0], labels[-1]))
        else:
            parts.append(", ".join(labels))
    return " · ".join(parts)


def money(s):
    """'99.00' -> 99 ; '17.95' -> 17.95. Keeps whole dollars integral so the
    page prints $99 rather than $99.0."""
    f = float(s)
    return int(f) if f == int(f) else f


def fmt_price(n):
    return "$%d" % n if float(n) == int(n) else "$%.2f" % n


def build_product(raw):
    ed = EDITORIAL.get(raw["handle"])
    if not ed:
        sys.exit("no EDITORIAL entry for Shopify handle %r — add one" % raw["handle"])

    # ---- axes. A single-valued `Title` option is Shopify's no-options
    # sentinel, so it produces zero axes rather than a one-chip picker.
    options = []
    axis_src = []           # index into the raw variant `opts` array per axis
    for i, o in enumerate(raw["options"]):
        if o["name"] == "Title" and len(o["values"]) == 1:
            continue
        key = OPTION_KEY.get(o["name"])
        if not key:
            sys.exit("unmapped Shopify option name %r on %s — add it to OPTION_KEY"
                     % (o["name"], raw["handle"]))
        options.append({
            "key": key,
            "name": o["name"],
            "values": [{"k": norm_value(key, v)[0], "label": norm_value(key, v)[1], "sv": v}
                       for v in o["values"]],
        })
        axis_src.append(i)

    # ---- variants, keyed by the normalised axis keys joined with '|'.
    # Zero axes produce the single key ''.
    variants = {}
    for v in raw["variants"]:
        parts = [norm_value(options[n]["key"], v["opts"][src])[0]
                 for n, src in enumerate(axis_src)]
        variants["|".join(parts)] = {
            "sku": v["sku"],                    # verbatim — never synthesised
            "price": money(v["price"]),
            "avail": bool(v["avail"]),          # NOT qty > 0; see the docstring
            "qty": v["qty"],
        }

    prices = sorted(v["price"] for v in variants.values())
    live = [k for k, v in variants.items() if v["avail"]]

    default = ed.get("default")
    # A combined-axis product's variant keys do not exist yet — the grind is
    # appended in merge_grinds() — so its default is validated there instead.
    if default and not ed.get("axisGrind") and default not in variants:
        sys.exit("%s: default %r is not a variant key" % (ed["id"], default))
    if not default:
        default = live[0] if live else sorted(variants)[0]

    p = {
        "id": ed["id"],
        "template": ed["tpl"],
        "family": ed["fam"],
        "collection": ed["coll"],
        "code": ed["code"],
        "name": ed["name"],
        # Cole locked this 2026-07-31: family, then code, then finish for
        # clubs; apparel and gear keep their descriptive names. `name` stays
        # the short form for tiles, where `code` is stamped alongside it.
        "title": ed.get("title", ed["name"]),
        "shopifyHandle": raw["handle"],
        "shopifyTitle": raw["title"],
        "img": (IMG_BASE + raw["img"]) if raw["img"] else None,
        "price": prices[0],
        "priceMax": prices[-1],
        "priceLabel": fmt_price(prices[0]) if prices[0] == prices[-1]
                      else "%s–%s" % (fmt_price(prices[0]), fmt_price(prices[-1])),
        "options": options,
        "variants": variants,
        "default": default,
        "summary": axis_summary(options, variants),
        "inStock": bool(live),
        "built": bool(ed.get("built")),
        "discontinued": bool(ed.get("discon")),
    }
    if ed.get("file"):
        p["file"] = ed["file"]
    if ed.get("rating"):
        p["rating"] = {"avg": ed["rating"][0], "count": ed["rating"][1]}
    if ed.get("note"):
        p["note"] = ed["note"]
    # Finish is a sibling axis expressed as separate products, the way colorways
    # are on the polos: `finishGroup` is what links them into one swatch row.
    for k in ("finish", "grind", "finishGroup"):
        if ed.get(k):
            p[k] = ed[k]
    return p


def merge_grinds(products):
    """Fold a merged product's variants into its target as a second grind, and
    turn the target's Loft axis into a combined "Loft & grind" one.

    WHY THIS EXISTS — Cole, 2026-07-31. Lucky sells one wedge, the 01. The
    K-grind gold and the S-grind gold were two Shopify products at two prices
    for a difference that is not a difference: same 1020 forged head, same
    weight, same face. He is collapsing them in Shopify; this models the
    collapsed state now so the site is not describing a lineup that is about to
    stop existing.

    THIS IS THE ONE PLACE THE OVERLAY OVERRIDES SHOPIFY DATA rather than just
    adding to it, and it is deliberate and temporary:
      * variant keys gain the grind    RH|56  ->  RH|56K / RH|56S
      * `priceAll` flattens the price  the S variants drop $109 -> $99
      * the merged product LEAVES products.json entirely
    Every SKU is still carried verbatim — 56S is the real LGW02-56-RH.

    WHEN SHOPIFY IS MERGED: re-pull, delete `merge`/`axisGrind`/`priceAll` and
    the merged handle's overlay entry, and this function stops doing anything.
    """
    by_handle = {p["shopifyHandle"]: p for p in products}
    drop = set()

    for p in products:
        ed = EDITORIAL[p["shopifyHandle"]]
        if not ed.get("axisGrind"):
            continue

        # A product with one grind still gets the combined axis, so the Gold
        # and the Black read the same way when you flip between finishes.
        sources = [(p, ed.get("grind"))]
        for h in ed.get("merge", []):
            src = by_handle.get(h)
            if src is None:
                sys.exit("%s merges %r, which is not in the pull" % (p["id"], h))
            sources.append((src, EDITORIAL[h].get("grind")))
            drop.add(src["id"])

        loft_i = [i for i, o in enumerate(p["options"]) if o["key"] == "loft"]
        if len(loft_i) != 1:
            sys.exit("%s: axisGrind needs exactly one loft axis" % p["id"])
        loft_i = loft_i[0]

        combined, variants = {}, {}
        for src, grind in sources:
            if not grind:
                sys.exit("%s: every merged product needs a `grind`" % src["id"])
            src_loft = [i for i, o in enumerate(src["options"]) if o["key"] == "loft"][0]
            for key, var in src["variants"].items():
                parts = key.split("|")
                lo = parts[src_loft]
                parts[src_loft] = lo + grind
                combined[lo + grind] = {
                    "k": lo + grind,
                    # Cole's own shorthand: 50K, 52K, 52S. The degree sign and
                    # the space are for the chip; the KEY stays compact.
                    # LITERAL characters, not HTML entities — the buy box runs
                    # every chip label through esc(), so "&deg;" would render
                    # as the four characters "&deg;". norm_value() already uses
                    # a literal degree sign for the plain loft axis.
                    "label": "%s° %s" % (lo, grind),
                    "sv": "%s / %s Grind" % (lo, grind),
                    "loft": float(lo), "grind": grind,
                }
                variants["|".join(parts)] = dict(
                    var, price=ed["priceAll"] if ed.get("priceAll") else var["price"])

        # loft ascending, K before S inside a loft — 50K, 52K, 52S, 54K, ...
        vals = sorted(combined.values(), key=lambda v: (v["loft"], v["grind"]))
        p["options"][loft_i] = {
            "key": "loftgrind", "name": "Loft & grind",
            "values": [{"k": v["k"], "label": v["label"], "sv": v["sv"]} for v in vals],
        }
        p["variants"] = variants
        prices = sorted(v["price"] for v in variants.values())
        p["price"], p["priceMax"] = prices[0], prices[-1]
        p["priceLabel"] = (fmt_price(prices[0]) if prices[0] == prices[-1]
                           else "%s-%s" % (fmt_price(prices[0]), fmt_price(prices[-1])))
        p["summary"] = axis_summary(p["options"], variants)
        live = [k for k, v in variants.items() if v["avail"]]
        p["inStock"] = bool(live)
        if p["default"] not in variants:
            sys.exit("%s: default %r is not a variant key after the merge"
                     % (p["id"], p["default"]))

    return [p for p in products if p["id"] not in drop]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="do not write; exit 1 if products.json is stale")
    a = ap.parse_args()

    raw = json.load(open(RAW, encoding="utf8"))
    products = [build_product(r) for r in raw["products"]]
    products = merge_grinds(products)

    ids = [p["id"] for p in products]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        sys.exit("duplicate product ids: %s" % ", ".join(dupes))

    known = {c["id"] for c in COLLECTIONS}
    for p in products:
        if p["collection"] not in known:
            sys.exit("%s: unknown collection %r" % (p["id"], p["collection"]))

    by_id = {p["id"]: p for p in products}
    colls = []
    for c in COLLECTIONS:
        members = c.get("members")
        if members is None:
            # Discontinued products keep their catalogue record — the pull is
            # provenance and the note explains why they went — but they leave
            # every grid. The driver was still rendering a Quick add.
            members = [p["id"] for p in products
                       if p["family"] in c["fams"] and not p["discontinued"]]
        else:
            unknown = [m for m in members if m not in by_id]
            if unknown:
                sys.exit("collection %s lists unknown products: %s"
                         % (c["id"], ", ".join(unknown)))
        rec = dict(c, products=members, count=len(members))
        rec.pop("members", None)
        rec["tpl"] = c.get("tpl", "plp")
        # A collection that has emptied out should stop being a page rather
        # than ship a heading over nothing. Nothing hits this today; it is here
        # because discontinuing the last member of a family now silently could.
        if not members and not c.get("blocked"):
            sys.exit("collection %s has no members — block it or remove it" % c["id"])

        # Facets that no member actually has would render as chips that filter
        # to nothing, so drop them here rather than in the page.
        present = {by_id[m]["family"] for m in members}
        rec["facets"] = [{"k": k, "label": lab}
                         for k, lab in c.get("facets", []) if k in present]
        colls.append(rec)

    doc = {
        "_": "GENERATED by tools/normalize-products.py — do not hand-edit.",
        "_from": "_src/data/shopify-raw.json + the EDITORIAL overlay in that script",
        "_pulled": raw["_pulled"],
        "collections": colls,
        "products": products,
    }
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"

    if a.check:
        old = open(OUT, encoding="utf8").read() if os.path.exists(OUT) else None
        if old == text:
            print("products.json  identical")
            return 0
        print("products.json  STALE — run: python tools/normalize-products.py")
        return 1

    with io.open(OUT, "w", encoding="utf8", newline="\n") as f:
        f.write(text)

    axes = {}
    for p in products:
        axes[len(p["options"])] = axes.get(len(p["options"]), 0) + 1
    print("products.json  %d products, %d variants" %
          (len(products), sum(len(p["variants"]) for p in products)))
    print("  axes:   " + ", ".join("%d-axis: %d" % (k, axes[k]) for k in sorted(axes)))
    print("  by tpl: " + ", ".join(
        "%s: %d" % (t, sum(1 for p in products if p["template"] == t))
        for t in ("club", "apparel", "gear")))
    print("  built:  %d of %d" % (sum(1 for p in products if p["built"]), len(products)))
    out_of_stock = [p["id"] for p in products if not p["inStock"]]
    if out_of_stock:
        print("  sold out entirely: " + ", ".join(out_of_stock))
    return 0


if __name__ == "__main__":
    sys.exit(main())
