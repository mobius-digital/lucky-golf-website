"""Apparel + collections group (css 60): the collection templates (all, polos, hats, gear, clubs)
and the product templates (polo, hat, gear). Imported by build_sections.py.

Everything a product carries comes from the product: title, description, price, variants, stock,
tags (polo collar), metafields custom.cutout / gallery / detail_photo / color_family / filter_style /
model_sizing / facts / restock_date / sold_out_mode, reviews.rating_count (+ judgeme histogram).
Everything the merchant changes on the page is a setting or a block.
"""
import os
from common import section, text, textarea, rich, url, img, check, select, rng, number, product, plist, collection, header, para

S = {}
HERE = os.path.dirname(__file__)


def liq(name):
    return open(os.path.join(HERE, "liquid_apparel", name), encoding="utf-8").read()


ICONS = [(x, x) for x in ["star", "badge-check", "truck", "credit-card", "rotate-ccw", "shield-check", "package", "hammer",
                          "anvil", "tag", "hand-coins", "message-circle", "mail", "map-pin", "search", "shopping-bag", "circle-help"]]

# ------------------------------------------------------------------ collection head
S["lg-ap-head"] = section("Collection head", liq("head.liquid"), [
    text("crumb", "Breadcrumb name (empty = collection's)"),
    text("eyebrow", "Eyebrow"),
    rich("heading", "Heading (empty = collection's title)"),
    textarea("lede", "Line under it (used when the collection has no description)"),
    check("narrow", "Narrow line (58 characters)", False),
    header("Polos"),
    text("guide_label", "Size guide link (empty = none)"),
    text("count_word", "Count after the number, e.g. polos (empty = none)"),
    header("Numbers on the right"),
    plist("rating_products", "Products whose live rating fills [rating]"),
    para("A number block with [rating] shows the live Judge.me average across the products above."),
], blocks=[("proof", "Number", [text("value", "Number", "60"), text("label", "Line under it", "days to decide"), check("gold", "Gold number", False)])], max_blocks=4)

# ------------------------------------------------------------------ the grid
S["lg-ap-grid"] = section("Collection grid", liq("grid.liquid"), [
    select("card", "Card style", [("item", "Everyday (all products)"), ("polo", "Polo (sizes, hover photo)"), ("hat", "Hat (quick add)")], "item"),
    header("Filters"),
    check("f_kind", "Kind (from product type)", True),
    textarea("kind_map", "Kind names (product type = chip name, one per line)"),
    check("f_stock", "Everything / In stock", True),
    check("f_collar", "Collar (from product tags)", False),
    text("collar_a_tag", "Collar A tag", "Classic Polo"), text("collar_a", "Collar A name", "Classic"),
    text("collar_b_tag", "Collar B tag", "Blade Polo"), text("collar_b", "Collar B name", "Blade"),
    check("f_style", "Style (metafield Filter style)", False),
    check("f_color", "Color (metafield Filter color)", False),
    check("color_dots", "Color dots on the chips", False),
    check("f_size", "My size (in stock in that size)", False),
    text("sizes", "Sizes", "S, M, L, XL, XXL, 3XL"),
    check("sort_stock", "Sort: Most sizes in stock", False),
    check("sort_price", "Sort: Price", True),
    header("Cards"),
    text("drop", "Words to leave off card names (comma separated)"),
    rng("hover_n", "Polo hover photo = product photo #", 1, 10, 1, 3),
    textarea("style_lines", "Hat card line per style (Style = line, one per line)"),
    text("empty", "No-match line", "Nothing matches that."),
    para("Feature tiles: add a Tile block and set which product it follows. Filters move it with the grid."),
], blocks=[("tile", "Feature tile", [number("pos", "Show after product #", 8), img("image", "Photo (empty = ink tile)"), text("eyebrow", "Eyebrow", "Pairs well with"),
                                    text("title", "Headline", "A hat that matches"), textarea("lines", "Bullet lines (one per line)"),
                                    url("url", "Link"), text("cta", "Button text", "Shop hats")])])

# ------------------------------------------------------------------ questions, 2 columns (+ an optional trust row above)
S["lg-ap-faq"] = section("Questions, two columns", liq("faq.liquid"), [
    check("no_top", "No space above", True), check("trust_gap", "Space between trust row and questions", True),
    text("eyebrow", "Eyebrow", "Before you pick"), rich("heading", "Heading"), textarea("body", "Line under it"),
    select("cols", "Columns", [("even", "Even"), ("narrow", "Narrow left")], "even"),
], blocks=[("q", "Question", [text("q", "Question"), {"type": "richtext", "id": "a", "label": "Answer"}]),
           ("trust", "Trust line (above)", [select("icon", "Icon", ICONS, "truck"), text("text", "Text")])])

# ------------------------------------------------------------------ keep browsing + trust strip
S["lg-ap-related"] = section("Keep browsing", liq("related.liquid"), [
    text("label", "Label", "Keep browsing"),
    plist("rating_products", "Products whose live reviews fill [avg] and [count]"),
    para("A trust line with [avg] and [count] shows the live Judge.me average and total across those products."),
], blocks=[("link", "Link", [text("text", "Text"), url("url", "Link")]),
           ("trust", "Trust line", [select("icon", "Icon", ICONS, "truck"), text("text", "Text")])])

# ------------------------------------------------------------------ gear: groups, each a collection
S["lg-ap-gear"] = section("Gear groups", liq("gear.liquid"), [
    textarea("sizes_word", "Button on multi-size cards, by product type (type = text)", "Head Cover = Pick a hand"),
    text("pick", "Button on multi-size cards (default)", "Pick a size"),
], blocks=[("group", "Group", [text("anchor", "Anchor", "covers"), text("jump", "Jump link text", "Head covers"), text("title", "Heading", "Head covers"),
                               textarea("line", "Line under it"), collection("collection", "Collection"),
                               select("meta", "Line under the price", [("stock", "In stock / Sold out"), ("sizes", "One size / More than one size")], "stock")])])

# ------------------------------------------------------------------ clubs: a category band
CARD = [product("product", "Product"), text("name", "Name (empty = product's)"), img("image", "Photo (empty = card cutout)"), text("tag", "Top tag (e.g. Best seller)"),
        text("vibe", "Vibe tag"), textarea("line", "Line"), textarea("hud", "Specs (one per line: value | label)"), text("cta", "Button", "Pick a loft")]
S["lg-ap-clubs-band"] = section("Club category band", liq("clubs_band.liquid"), [
    text("anchor", "Anchor", "wedges"),
    text("eyebrow", "Eyebrow"), rich("heading", "Heading"), textarea("body", "Line beside it"),
    img("photo", "Photo"), text("photo_pos", "Photo position (CSS)", "", "e.g. object-position:35% 40%"),
    select("style", "Card style", [("detail", "Detail card (approved page)"), ("big", "Big card")], "big"),
    header("Compare table"), text("cmp_title", "Table heading"), check("cmp_diff", "Start on 'only what's different'", True),
    text("rating_label", "Rating row label (empty = no row)", "Rating"), text("rating_same", "Rating note when shared", "Shared by both"),
    para("Rating rows are live and only appear at the review minimum."),
], blocks=[("card", "Club card", CARD),
           ("row", "Table row", [text("label", "Row"), text("a", "First club"), text("b", "Second club"), check("same", "Same on both (one cell)", False)]),
           ("spec", "Spec tile", [text("b", "Number"), text("small", "Unit"), text("label", "Label")]),
           ("panel", "Compare panel", [text("tag", "Tag"), text("title", "Title"), textarea("text", "Text")])])

S["lg-ap-jump"] = section("Jump bar", liq("jump.liquid"), [text("label", "Label (for screen readers)", "Jump to a category")],
    blocks=[("link", "Link", [text("text", "Text", "Wedges"), text("anchor", "Anchor of the band", "wedges"), collection("collection", "Count from collection (optional)"),
                              rng("count", "Or this count (0 = none)", 0, 20, 1, 0)])], max_blocks=6)

S["lg-ap-clubs-rev"] = section("Club reviews on a photo", liq("clubs_rev.liquid"), [
    text("anchor", "Anchor", "reviews"), img("bg", "Background photo"), text("bg_pos", "Background position", "center 65%"),
    text("eyebrow", "Eyebrow", "Reviews"), rich("heading", "Heading"), textarea("body", "Line beside it"),
    plist("products", "Products whose live Judge.me stars draw the green"),
    para("Tiles are 5-star Judge.me reviews typed in word for word. Never edit or invent a review."),
], blocks=[("review", "Review", [textarea("quote", "Quote, word for word"), text("name", "Name as on Judge.me"), text("product", "Product name"), rng("stars", "Stars", 1, 5, 1, 5)])], max_blocks=6)

# ------------------------------------------------------------------ product pages
FQ = ("fq", "Fold-out", [text("title", "Title"), {"type": "richtext", "id": "body", "label": "Text"}, check("open", "Open at first", False)])
SPEC = ("spec", "Fact tile", [text("b", "Number"), text("small", "Small part"), text("label", "Label")])
S["lg-ap-polo"] = section("Polo buy box", liq("polo.liquid"), [
    text("crumb_label", "Breadcrumb: collection name", "Polos"), url("crumb_url", "Breadcrumb: collection link"),
    text("drop", "Words to leave off the name (comma separated)", "Classic Polo, Blade Polo"),
    text("collar_a_tag", "Collar A tag", "Classic Polo"), text("collar_a", "Collar A eyebrow", "The Classic"),
    text("collar_b_tag", "Collar B tag", "Blade Polo"), text("collar_b", "Collar B eyebrow", "The Blade"),
    text("eyebrow_tail", "After the collar in the eyebrow", " · Polos"),
    collection("swatches", "Prints: the collection to pick from (same collar only)"),
    rng("swatch_n", "Print swatch = product photo #", 1, 10, 1, 4),
    text("all_prints", "Link under the prints", "See every print side by side"),
    {"type": "richtext", "id": "fitnote", "label": "Fit note under the sizes"},
    text("stock_in", "In stock line", "In stock · ships in 1 to 2 days"),
    text("returns_link", "Returns link", "Thirty days to send it back"), text("delivery_link", "Delivery link", "When will it get here?"),
    header("Returns pop-up"), text("ret_eyebrow", "Eyebrow", "Refund policy"), text("ret_title", "Title", "Thirty days to send it back"), {"type": "richtext", "id": "ret_body", "label": "Text"},
    header("Delivery pop-up"), text("del_eyebrow", "Eyebrow", "Delivery"), text("del_title", "Title", "When it shows up"), text("carriers", "Carriers (comma separated)", "USPS, UPS, FedEx"), {"type": "richtext", "id": "del_body", "label": "Text"},
    para("Photos are the product's own media, in the admin order. The model line under the sizes is the product's 'Model sizing line' metafield; it hides while empty."),
], blocks=[SPEC, FQ])

S["lg-ap-hat"] = section("Hat buy box", liq("hat.liquid"), [
    text("crumb_label", "Breadcrumb: collection name", "Hats"), url("crumb_url", "Breadcrumb: collection link"),
    text("eyebrow", "Eyebrow", "Hat · one size"),
    img("photo1", "Second photo"), text("photo1_label", "Second photo name", "On the green"),
    img("photo2", "Third photo"), text("photo2_label", "Third photo name", "At sunset"),
    text("more_label", "Label above the swatches", "More hats"), collection("swatches", "Swatches: collection"), text("more_link", "Link beside it", "See them all"),
    text("stock_in", "In stock line", "In stock · ships in 1 to 2 days"),
    text("l1", "Link 1", "Thirty days to send it back"), url("l1_url", "Link 1 URL"),
    text("l2", "Link 2", "Free shipping at $198"), url("l2_url", "Link 2 URL"),
], blocks=[("tile", "Fact tile", [text("b", "Big word"), text("label", "Line")])], max_blocks=4)

S["lg-ap-gearp"] = section("Gear buy box", liq("gearp.liquid"), [
    text("crumb_label", "Breadcrumb: collection name", "Gear"), url("crumb_url", "Breadcrumb: collection link"),
    textarea("eyebrows", "Eyebrow by product type (type = eyebrow)"),
    textarea("labels", "Button names (value = shown as, or Type/value = shown as)"),
    img("photo", "Second photo"), img("photo_b", "Second photo for putter gear"),
    text("photo_b_when", "Putter gear = tagged or typed (comma separated)", "putter, Head Cover"),
    text("stock_in", "In stock line", "In stock · ships in 1 to 2 days"), text("stock_out", "Sold out line", "Sold out in this one"),
    text("l1", "Link 1", "Thirty days to send it back"), url("l1_url", "Link 1 URL"),
    text("l2", "Link 2", "Free shipping at $198"), url("l2_url", "Link 2 URL"),
    para("Facts under the button are the product's 'Quick facts' metafield (Label: value per line)."),
])

S["lg-ap-piece"] = section("Product story + photo", liq("piece.liquid"), [
    text("eyebrow", "Eyebrow", "The polo"), rich("heading", "Heading (italic = gold word)"), {"type": "richtext", "id": "body", "label": "Text"},
    text("btn_label", "Button (outline)"), url("btn_url", "Button link"),
    img("image", "Photo (empty = one of the product's own photos)"), rng("media_n", "Which product photo (1 = first)", 1, 10, 1, 4), check("tall", "Tall photo, wide text (polo)", True),
])

S["lg-ap-reviews"] = section("Pooled reviews", liq("reviews.liquid"), [
    collection("pool", "Pool: every product in this collection"),
    text("eyebrow", "Eyebrow", "Reviews"), text("heading", "Heading ([count] = the pool's total)", "[count] reviews"),
    text("line", "Line", "Reviews from every Lucky polo. Same fabric and fit, different print."),
    para("Shows only when the pool has at least the review minimum (Theme settings). Pool the products in Judge.me too (Product groups) so the widget lists every review."),
])

S["lg-ap-more"] = section("Wear it with", liq("more.liquid"), [
    select("layout", "Layout", [("three", "Three across (polo)"), ("four", "Four across (hat, gear)")], "three"),
    text("eyebrow", "Eyebrow", "Wear it with"), rich("heading", "Heading", "Round out the look"),
    text("link_label", "Link on the right", "All apparel"), url("link_url", "Link URL"),
], blocks=[("product", "Product", [product("product", "Product"), text("line", "Line"), img("image", "Photo (empty = card cutout)")]),
           ("others", "More from a collection", [collection("collection", "Collection"), rng("count", "How many", 1, 8, 1, 3)]),
           ("collar", "The other collar", [collection("collection", "Collection"), text("tag", "Tag of this page's collar A", "Classic Polo"),
                                           text("line_a", "Line when showing collar A", "The classic collar, same shirt underneath."),
                                           text("line_b", "Line when showing collar B", "No buttons, nothing at your throat.")])])
