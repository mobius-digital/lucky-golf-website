"""
ONE-SHOT refactor: split _src-home-template.html into shared + per-page sources.

GAMEPLAN section 2. Run once, verify with `python tools/build.py --check`,
then this script is history — the sources under _src/ become the truth.

Everything here is expressed as 1-based inclusive line ranges into the old
template so the split is mechanical, not retyped. If the rebuild diffs, the
ranges are wrong, not the content.
"""
import os
import io

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "_src")

L = open(os.path.join(ROOT, "_src-home-template.html"), encoding="utf8").read().split("\n")


def cut(a, b):
    """1-based inclusive."""
    return "\n".join(L[a - 1:b])


def write(rel, text):
    path = os.path.join(SRC, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not text.endswith("\n"):
        text += "\n"
    with io.open(path, "w", encoding="utf8", newline="\n") as f:
        f.write(text)
    print("  %-26s %5d lines" % (rel, text.count("\n")))


# --------------------------------------------------------------------------
# CSS.  Block boundaries are the `/* ===` banners; see tools/split-src.py
# history for the full block table.
# --------------------------------------------------------------------------
CORE_CSS = [
    (11, 204),    # tokens, type, layout, focus, buttons, the mark
    (205, 213),   # announcement
    (214, 263),   # header
    (393, 421),   # social rail
    (422, 451),   # review rail + cards
    (452, 519),   # lightbox
    (520, 533),   # labelled placeholder
    (567, 584),   # closing CTA
    (585, 602),   # footer
    (603, 623),   # brand band
    (774, 793),   # marquee
    (794, 854),   # mega menu
    (855, 914),   # cart drawer
    (915, 950),   # mega menu v2
    (951, 984),   # product tiles
    (985, 1021),  # studio cutouts
]

HOME_CSS = [
    (264, 298),   # hero
    (299, 324),   # shop by family
    (325, 348),   # featured — dark event
    (349, 366),   # why lucky
    (367, 374),   # aside moment
    (375, 392),   # social proof
    (534, 545),   # lifestyle break
    (546, 566),   # apparel + gear
    (624, 654),   # value props
    (655, 680),   # club finder
    (681, 695),   # pull quote
    (696, 710),   # the finish
    (711, 727),   # the mindset
    (728, 744),   # the roster
    (745, 773),   # collection tiles
]

# The RESPONSIVE block (1022-1057) mixes both. Split by selector.
CORE_RESPONSIVE = """\
/* ==========================================================================
   RESPONSIVE — shared chrome only. Page-specific breakpoints live in the
   page's own stylesheet.
   ========================================================================== */
@media (max-width:1180px){
  .revs{grid-template-columns:repeat(2,1fr)}
}
@media (max-width:980px){
  .nav{display:none}
  .burger{display:block;margin-left:auto}
  .hdr-act{margin-left:0}
  .ftr-in{grid-template-columns:1fr 1fr}
}
@media (max-width:620px){
  body{font-size:16px}
  .ftr ul{gap:2px}
  .ftr ul a{display:flex;align-items:center;min-height:44px}
  .revs{grid-template-columns:1fr}
  .ftr-in{grid-template-columns:1fr}
  .trust-in{gap:12px}
  .trust .div{display:none}
}
"""

HOME_RESPONSIVE = """\
/* ---------- responsive ---------- */
@media (max-width:1180px){
  .gear{grid-template-columns:1fr 1fr}
}
@media (max-width:980px){
  .fam{grid-template-columns:1fr}
  .feat-in{grid-template-columns:1fr}
  .plinth-wrap{order:-1}
  .why-top{grid-template-columns:1fr}
  .claims{grid-template-columns:1fr}
  .claim{border-right:0;border-bottom:1px solid var(--ink-14);padding-left:0;padding-right:0;padding-bottom:26px}
  .claim:last-child{border-bottom:0}
  .exp-grid{grid-template-columns:1fr}
  .hero-stamp{display:none}
}
@media (max-width:620px){
  .hero-media{height:76vh;height:76dvh}
  .hero-scrim{background:linear-gradient(0deg,rgba(23,20,15,.86) 0%,rgba(23,20,15,.32) 55%,rgba(23,20,15,.1) 100%)}
  .gear{grid-template-columns:1fr}
  .gear .g-hero{grid-column:auto}
}
"""

print("CSS")
write("core.css", "\n".join(cut(a, b) for a, b in CORE_CSS) + "\n\n" + CORE_RESPONSIVE)
write("page-home.css", "\n".join(cut(a, b) for a, b in HOME_CSS) + "\n\n" + HOME_RESPONSIVE)

# --------------------------------------------------------------------------
# Shared markup partials
# --------------------------------------------------------------------------
print("partials")
write("partials/symbols-host.html", cut(1062, 1070))   # the <svg> sprite host
write("partials/header.html", cut(1072, 1162))
write("partials/footer.html", cut(1887, 1937))
write("partials/lightbox.html", cut(2021, 2035))
write("partials/cart.html", cut(2311, 2328))

# --------------------------------------------------------------------------
# Shared JS
# --------------------------------------------------------------------------
CORE_JS = "\n\n".join([
    "/* reveal-on-scroll */\n(function(){\n" + cut(1941, 1955) + "\n})();",
    cut(1977, 1986),   # mobile nav
    cut(1988, 2015),   # rail
    cut(2041, 2172),   # lightbox open/close
    cut(2176, 2307),   # lightbox wiring
    cut(2330, 2491),   # mega menu + cart
])
print("js")
write("core.js", CORE_JS)

HOME_JS = "\n\n".join([
    "/* club finder tabs */\n(function(){\n" + cut(1958, 1974) + "\n})();",
    cut(2037, 2038),   # LG_REVIEWS / LG_POSTS data
])
write("page-home.js", HOME_JS)

# --------------------------------------------------------------------------
# Home page body: its own sections only, in order.
# --------------------------------------------------------------------------
HOME_SECTIONS = [
    (1164, 1185),   # hero
    (1187, 1195),   # marquee
    (1196, 1260),   # shop by family + the breath divider under it
    (1262, 1289),   # featured
    (1291, 1321),   # why lucky
    (1323, 1355),   # club finder
    (1357, 1373),   # brand band
    (1375, 1383),   # pull quote
    (1385, 1521),   # social proof
    (1523, 1606),   # value props
    (1608, 1722),   # social rail
    (1724, 1744),   # the finish
    (1746, 1800),   # roster
    (1802, 1858),   # apparel + gear
    (1860, 1885),   # closing CTA
]
print("page body")
write("page-home.html", "\n\n".join(cut(a, b) for a, b in HOME_SECTIONS))
print("\nDone. Now run:  python tools/build.py --check")
