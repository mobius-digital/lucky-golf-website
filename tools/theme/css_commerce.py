"""Write theme/css/80-commerce.css: the approved cart, gift card, blog and article pages'
own <style> blocks, each scoped to its section wrapper (.lgc-cart, .lgc-gc, .lgc-blog,
.lgc-art), plus what the theme adds (cart quantity, coverage line, note, article body
from Shopify's editor, pagination).

    python tools/theme/css_commerce.py && python tools/theme/build_css.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_css import scope_css, page_style

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "theme", "css", "80-commerce.css")
PAGES = [("cart.html", "lgc-cart"), ("giftcard.html", "lgc-gc"), ("blog.html", "lgc-blog"), ("article.html", "lgc-art")]


def tighten(css):
    """Takomo-tight corners: the approved pages still carry a few 12-18px radii."""
    css = re.sub(r"border-radius:(1[2-8])px", "border-radius:var(--lg-r-card)", css)
    css = css.replace("border-radius:999px", "border-radius:var(--lg-r)")
    # colours, shadows and gradients the system already names
    for a, b in [
        ("background:linear-gradient(150deg,#0F3A27 0%,#0B2E1F 55%,#06110B 100%)", "background:var(--lg-band-light)"),
        ("background:radial-gradient(70% 90% at 90% 0%,rgba(237,210,124,.22),transparent 60%)", "background:none"),
        ("box-shadow:0 30px 60px -30px rgba(6,17,11,.6)", "box-shadow:var(--lg-float-lg)"),
        ("linear-gradient(178deg,#C29A2B 0%,#EDD27C 46%,#EDD27C 56%,#C29A2B 100%)", "var(--lg-foil-text)"),
        ("rgba(244,243,240,.72)", "var(--lg-on-dark-m)"), ("#F4F3F0", "var(--lg-on-dark)"),
        ("background:#000", "background:var(--lg-night)"), ("color:#fff", "color:var(--lg-on-dark)"),
        ("solid #111", "solid var(--lg-ink)"), ("background:rgba(0,0,0,.6)", "background:var(--lg-dark)"),
    ]:
        css = css.replace(a, b)
    # type sizes that duplicate the scale
    for a, b in [("12px", "var(--lg-fs-sm)"), ("13px", "var(--lg-fs-sm)"), ("14px", "var(--lg-fs-base)"),
                 ("16px", "var(--lg-fs-base)"), ("18px", "var(--lg-fs-body)")]:
        css = css.replace("font-size:" + a, "font-size:" + b)
    return css


EXTRA = """
/* ---- theme additions (group 80) ---- */
.lgc-cart .ln .nm{color:inherit;text-decoration:none}
.lgc-cart .ln .cd-qty{margin-top:10px}
.lgc-cart .ln .pr s{display:block;font-weight:400;color:var(--lg-ink-64);font-size:13px}
.lgc-cart .ln.is-cover{grid-template-columns:minmax(0,1fr) auto;padding:12px 0}
.lgc-cart .ln.is-cover b{font-size:13px}
.lgc-cart .ln.is-cover .cv{display:block;margin-top:2px;font-size:13px;color:var(--lg-ink-64)}
.lgc-cart .ln.is-cover .pr{font-weight:500;font-size:var(--lg-fs-sm)}
@media (max-width:560px){.lgc-cart .ln.is-cover{grid-template-columns:minmax(0,1fr) auto}.lgc-cart .ln.is-cover .pr{grid-column:auto;text-align:right}}
.lgc-cart .ship p:empty{display:none}
.lgc-cart #go[aria-disabled="true"]{opacity:.5}
.lgc-cart .sum form{margin:0}
.lgc-cart .cnote{margin-top:14px;border-top:1px solid var(--lg-rule);padding-top:12px}
.lgc-cart .cnote summary{cursor:pointer;font-size:var(--lg-fs-sm);color:var(--lg-ink-70)}
.lgc-cart .cnote textarea{width:100%;min-height:80px;margin-top:10px;border:1px solid var(--lg-rule);border-radius:var(--lg-r);padding:10px 12px;font:inherit;resize:vertical;background:var(--lg-page);color:var(--lg-ink)}
.lgc-gc .buy form{margin:0}
.lgc-gc .to input:invalid:focus{border-color:var(--lg-ink)}
.lgc-gc .lg-chip[disabled]{opacity:.4;cursor:not-allowed}
.lgc-gc .pick .lg-aside{display:block}
.lgc-blog .pages{padding-bottom:clamp(28px,4vw,52px);display:flex;gap:14px;justify-content:center}
.lgc-blog .pages a,.lgc-blog .pages .current{padding:8px 12px}
.lgc-blog .post figure .noimg{display:grid}
/* article bodies come from Shopify's editor: images, embeds and tables sit in the column */
.lgc-art .rte img{max-width:100%;height:auto;border-radius:var(--lg-r-card)}
.lgc-art .rte iframe{width:100%;height:auto;aspect-ratio:16/9;border:0;border-radius:var(--lg-r-card)}
.lgc-art .rte a:not([class]){color:inherit;text-decoration:underline;text-underline-offset:3px}
.lgc-art .rte h3{margin:24px 0 10px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:700;text-transform:uppercase;font-size:18px}
.lgc-art .rte blockquote{margin:28px 0;padding-left:20px;border-left:3px solid var(--lg-gold)}
.lgc-art .rte .lg-faq{margin-bottom:8px}
.lgc-art .rte .lg-fq-a p{margin:0}
.lgc-art .mp figure:empty{aspect-ratio:3/2}
/* image_tag writes width/height: let the CSS ratios win (3:2 cards), and let the article photo keep its own shape */
.lgc-blog .post img,.lgc-art .mp img{height:auto}
.lgc-art .hero img{height:auto;aspect-ratio:auto;max-height:80vh}
"""


def main():
    parts = ["/* Group 80: cart, gift card, blog, article. Built by tools/theme/css_commerce.py: do not edit here. */"]
    for page, scope in PAGES:
        parts.append(f"/* ---- v9/src/{page} (scoped to .{scope}) ---- */\n" + tighten(scope_css(page_style(page), scope)))
    parts.append(tighten(EXTRA.strip()))
    open(OUT, "w", encoding="utf-8").write("\n".join(parts) + "\n")
    print("80-commerce.css", os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
