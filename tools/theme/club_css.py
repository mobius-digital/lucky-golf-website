"""Write theme/css/50-club.css: the approved Carver page CSS (v9/src/carver.html) plus what club.html adds,
scoped to the club template (body.lg-t-club), plus the theme-only bits.

    python tools/theme/club_css.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_css import scope_css, ROOT

SRC = os.path.join(ROOT, "v9", "src")


def style(name):
    s = open(os.path.join(SRC, name), encoding="utf-8").read()
    return "\n".join(re.findall(r"<style>(.*?)</style>", s, flags=re.S))


carver = style("carver.html")
club = style("club.html").replace("{{CARVER_CSS}}", "")
THEME = """
/* theme-only */
.gal figure.is-video{cursor:default;background:var(--lg-night)}
.gal figure.is-video video,.gal figure.is-video iframe{display:block;width:100%;height:100%;object-fit:cover;border:0}
/* gallery: five tiles (the cutout wide + four), the rest behind "See all"; the buy box stays in view beside it */
@media (min-width:750px){.gal:not(.is-all) .is-more{display:none}}
.gal-all{width:100%;margin-top:8px}
@media (max-width:749px){.gal-all{display:none}}
.buy{align-self:start}
/* film: the product's own video, or a real photo */
.film-ph{margin:0;border-radius:var(--lg-r-card);overflow:hidden;aspect-ratio:16/9;background:var(--lg-tile);cursor:zoom-in}
.film-ph img{display:block;width:100%;height:100%;object-fit:cover}
.film-v iframe{display:block;width:100%;aspect-ratio:16/9;border:0;border-radius:var(--lg-r-card)}
/* community posts on the dark band */
.club-wild .wild-foot{margin-top:18px}
.film-v video{display:block;width:100%;aspect-ratio:16/9;border-radius:var(--lg-r-card);background:#000}
.buy form.cta{margin:22px 0 0}
/* the old Notify Me app injects its own button into product forms; the theme's Klaviyo button replaces it */
.nm-portal,.restock-alerts-notify-button{display:none!important}
.cta .lg-btn[aria-busy="true"]{opacity:.7}
.lofts:empty{display:none}
.jdgm-widget[hidden]{display:none}
.rail-foot{justify-content:flex-start;flex-wrap:nowrap}
/* the spec sheet's contour runs edge to edge, fading only at the top and bottom (like the approved page) */
@media (min-width:750px){#specs.lg-contour::before{-webkit-mask-image:linear-gradient(180deg,transparent 0,#000 16%,#000 78%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,#000 16%,#000 78%,transparent 100%)}}
"""

def tokens(css):
    """No hard-coded radii, colours or type sizes that duplicate a design token (Cole, 2026-09-27)."""
    # the gold pill "flag" on the set buttons is not in the markup and is not the system tag
    css = re.sub(r"[^{}]*\.set \.fl\{[^}]*\}\n?", "", css)
    css = re.sub(r"border-radius:(?:8|10|12|14|18)px", "border-radius:var(--lg-r-card)", css)
    css = re.sub(r"border-radius:999px", "border-radius:var(--lg-r-tag)", css)
    for a, b in (("#F4F3F0", "var(--lg-on-dark)"), ("#17140F", "var(--lg-ink)"), ("#0B2E1F", "var(--lg-dark)"),
                 ("#C29A2B", "var(--lg-gold)"), ("#EDD27C", "var(--lg-gold-hi)"), ("#06110B", "var(--lg-night)"), ("#0B1911", "var(--lg-night)")):
        css = re.sub(a, b, css, flags=re.I)
    sizes = {"10px": "--lg-fs-xs", "10.5px": "--lg-fs-xs", "11px": "--lg-fs-xs", "12px": "--lg-fs-sm", "13px": "--lg-fs-sm",
             "14px": "--lg-fs-base", "15px": "--lg-fs-base", "16px": "--lg-fs-body", "17px": "--lg-fs-body"}
    css = re.sub(r"font-size:(10\.5px|1[0-7]px)", lambda m: "font-size:var(%s)" % sizes[m.group(1)], css)
    return css


out = ("/* Club product pages (templates/product.club.json). Built by tools/theme/club_css.py from the approved\n"
       "   v9 Carver + club pages: do not edit here. */\n" + tokens(scope_css(carver + "\n" + club + "\n" + THEME, "lg-t-club")) + "\n")
p = os.path.join(ROOT, "theme", "css", "50-club.css")
open(p, "w", encoding="utf-8").write(out)
print(p, len(out))
