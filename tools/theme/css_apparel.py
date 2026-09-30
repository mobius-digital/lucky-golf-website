"""Write theme/css/60-apparel.css: each approved apparel/collection page's own <style>, scoped to
its template body classes, plus the few rules the theme needs on top.

    python tools/theme/css_apparel.py        (then python tools/theme/build_css.py)
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_css import scope_css

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
AFTER = os.path.join(ROOT, "v9", "out", "after")
OUT = os.path.join(ROOT, "theme", "css", "60-apparel.css")

COLL = "lg-t-collection"
ALL = COLL + ":not(.lg-t-polos):not(.lg-t-hats):not(.lg-t-gear):not(.lg-t-clubs)"
PAGES = [  # approved page (built) -> body scope
    ("collection-all", ALL),
    ("polos", COLL + ".lg-t-polos"),
    ("hats", COLL + ".lg-t-hats"),
    ("gear", COLL + ".lg-t-gear"),
    ("clubs", COLL + ".lg-t-clubs"),
    ("polo-azalea", "lg-t-product.lg-t-polo"),
    ("hat-white-gold-classic", "lg-t-product.lg-t-hat"),
    ("gear-grip-clover-black", "lg-t-product.lg-t-gear"),
]

# what the theme needs on top of the approved CSS (Shopify wraps every section in a div,
# so adjacency rules from the static pages need a hand; tags are the flat corner tag)
EXTRA = """
/* shared across the apparel group */
.lg-t-collection .polo-ph > a,.lg-t-collection .hat-ph > a,.lg-t-collection .it-ph > a{display:block;height:100%}
.lg-t-collection .qa form{margin:0}
.lg-t-product.lg-t-polo .buy form,.lg-t-product.lg-t-hat .buy form,.lg-t-product.lg-t-gear .buy form{margin:0}
.ap-desc > :first-child{margin-top:0}
.ap-desc > :last-child{margin-bottom:0}
.lg-t-product.lg-t-hat .buy .lg-btn-line,.lg-t-product.lg-t-gear .buy .lg-btn-line{width:100%;margin-top:18px}
.lg-t-product.lg-t-polo .atc-row .lg-btn-line{flex:1;min-height:58px}
.lg-t-product.lg-t-polo .fitnote p{margin:0}
.lg-t-product.lg-t-polo .sb-sizes button[data-dead]{color:var(--lg-ink-38);border-style:dashed;text-decoration:line-through}
.lg-t-product.lg-t-hat .big img,.lg-t-product.lg-t-gear .big img{display:block}
/* card tags: flat, deep green with gold type, flush in the corner (lead, 2026-09-27) */
.lg-t-collection .it .lg-tag,.lg-t-collection .pc-ph .lg-tag,.lg-t-collection .polo .lg-tag,.lg-t-collection .hat .lg-tag,
.lg-t-product.lg-t-polo .more .lg-card-ph .lg-tag,.lg-t-product.lg-t-hat .more .lg-card-ph .lg-tag,.lg-t-product.lg-t-gear .more .lg-card-ph .lg-tag{position:absolute;left:0;top:0;right:auto;bottom:auto;margin:0;border-radius:0 0 var(--lg-r-tag) 0;
  background:var(--lg-dark);color:var(--lg-on-dark)}
.lg-t-collection .pc-ph .lg-tag.vibe{left:auto;top:auto;right:0;bottom:0;border-radius:var(--lg-r-tag) 0 0 0}
/* product photos are shot on white: multiply them onto the stone tile like the cutouts were */
.lg-t-product.lg-t-polo .gal figure.cut img,.lg-t-product.lg-t-hat .big:not(.is-photo) img,.lg-t-product.lg-t-gear .big:not(.is-photo) img,
.lg-t-product.lg-t-hat .thumbs button:not(.is-photo) img,.lg-t-product.lg-t-gear .thumbs button:not(.is-photo) img{mix-blend-mode:multiply}
.lg-t-product.lg-t-polo .gal figure.cut img{padding:0}
/* every product photo gets a thumbnail, so the row wraps */
.lg-t-product.lg-t-hat .thumbs,.lg-t-product.lg-t-gear .thumbs{flex-wrap:wrap}
.lg-t-product.lg-t-hat .thumbs button,.lg-t-product.lg-t-gear .thumbs button{flex:0 0 76px;max-width:none}
/* clubs: Shopify wraps each band in its own section div */
.lg-t-collection.lg-t-clubs .shopify-section:has(> .band) + .shopify-section > .band{padding-top:0}
.lg-t-collection.lg-t-clubs .row > .lg-card-wrap{min-width:0}
.lg-t-collection.lg-t-clubs .row > .lg-card-wrap .lg-bigcard{flex:1 1 auto;width:100%;height:100%;aspect-ratio:auto;min-height:380px}
"""


def page_css(name):
    h = open(os.path.join(AFTER, name + ".html"), encoding="utf-8").read()
    st = re.findall(r"<style[^>]*>(.*?)</style>", h, flags=re.S)
    return "\n".join(x for x in st if ":root{--lg-contour" not in x[:40])


TOKENS = [  # the approved pages' literal values -> the system tokens (Cole, 2026-09-27)
    ("border-radius:999px", "border-radius:var(--lg-r-btn)"),
    ("border-radius:12px", "border-radius:var(--lg-r-card)"),
    ("border-radius:10px", "border-radius:var(--lg-r-card)"),
    ("border-radius:9px", "border-radius:var(--lg-r)"),
    ("#fff}", "var(--lg-page)}"), ("#fff;", "var(--lg-page);"),
    ("#17140F", "var(--lg-ink)"), ("#1B1B1B", "var(--lg-ink)"), ("#EDEAE3", "var(--lg-tile)"),
    ("#C29A2B", "var(--lg-gold)"), ("#EDD27C", "var(--lg-gold-hi)"), ("#0B2E1F", "var(--lg-dark)"),
]


def tokens(css):
    for a, b in TOKENS:
        css = css.replace(a, b)
    return css


def main():
    parts = ["/* Apparel + collections (group 60). Built by tools/theme/css_apparel.py from the approved v9 pages. */"]
    for page, scope in PAGES:
        parts.append(f"/* ---- {page} -> .{scope} ---- */\n" + scope_css(page_css(page), scope))
    parts.append(EXTRA.strip())
    open(OUT, "w", encoding="utf-8").write(tokens("\n".join(parts)) + "\n")
    print("60-apparel.css", os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
