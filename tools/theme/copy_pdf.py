"""Every word on the new site, one PDF, for Cole's copy review.

    python tools/theme/copy_pdf.py      -> v9/review-pdfs/Lucky-site-copy.pdf (+ .md next to it)

Reads the build theme's preview (each page on the template it gets at launch), strips the
code, and keeps the words in reading order: headings, labels, body, buttons. The header,
footer, announcement bar and bag drawer are printed once. Product descriptions that change
on launch day come from v9/migration/product-copy/, and the blog rewrites from v9/src/articles/.
Text is shown as written (the site's CSS turns some of it into capitals).
"""
import glob, html, json, os, re
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
import fitz

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "v9", "review-pdfs", "Lucky-site-copy.pdf")
BASE = "https://www.luckygolf.com"
THEME = "171555127573"

PAGES = [
    ("Home", "/", ""),
    ("Clubs (collection)", "/collections/lucky-golf-clubs", "clubs"),
    ("Carver 02 Gold", "/products/lucky-golf-lgw02-gold", "club"),
    ("Carver 02 Black", "/products/lucky-golf-lgw02-black", "club"),
    ("Eclipse Blade", "/products/signature-gold-putters", "club"),
    ("Eclipse Mallet", "/products/limited-edition-mallet-putter", "club"),
    ("Stryker", "/products/lucky-striker-hybrid-limited-edition", "club"),
    ("Polos (collection)", "/collections/polos", "polos"),
    ("Polo page (every polo uses this; its description is in the appendix)", "/products/frost-classic-polo", "polo"),
    ("Hats (collection)", "/collections/hats", "hats"),
    ("Hat page (every hat uses this; its description is in the appendix)", "/products/white-gold-classic-hat", "hat"),
    ("Gear (collection)", "/collections/gear", "gear"),
    ("Gear page (every gear item uses this; its description is in the appendix)", "/products/lucky-clover-tour-glove", "gear"),
    ("Gift card", "/products/lucky-wedges-gift-card", "giftcard"),
    ("All collections", "/collections", ""),
    ("Our story (About)", "/pages/about", "story"),
    ("Lucky vs the big names (new page)", "/pages/about", "compare"),
    ("Community (new page)", "/pages/about", "community"),
    ("Reviews", "/pages/reviews", "reviews"),
    ("FAQ", "/pages/faq-lucky-wedges", "faq"),
    ("Ambassador program", "/pages/become-apart-of-the-team", "ambassadors"),
    ("Contact", "/pages/contact-us", "contact"),
    ("Blog (list)", "/blogs/news", ""),
    ("Cart", "/cart", ""),
    ("Search", "/search?q=wedge", ""),
    ("Page not found (404)", "/this-page-does-not-exist", ""),
]
CHROME = [".lg-tick", ".lg-hdr", ".lg-ftr", ".cd", "#shopify-section-header", "#preview-bar-iframe"]
DROP = ["script", "style", "noscript", "svg", "template", "iframe", "link", "meta", "select", "input", "img", "video", "picture"]
BLOCK = {"h1", "h2", "h3", "h4", "h5", "p", "li", "blockquote", "figcaption", "summary", "dt", "dd", "button", "label", "th", "td", "caption", "legend"}


def session():
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
    s.get(f"{BASE}/?preview_theme_id={THEME}", timeout=60)
    return s


def fetch(s, path, view):
    sep = "&" if "?" in path else "?"
    url = BASE + path + (f"{sep}view={view}" if view else "")
    r = s.get(url, timeout=90)
    if "lucky-site.css" not in r.text:  # preview cookie lost: ask for it again
        r = s.get(url + ("&" if "?" in url else "?") + f"preview_theme_id={THEME}", timeout=90)
    return BeautifulSoup(r.text, "html.parser")


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def kind(el):
    n = el.name
    cls = " ".join(el.get("class", []))
    if n in ("h1", "h2", "h3", "h4", "h5"):
        return n
    if re.search(r"eyebrow|kicker|lg-label|stamp", cls):
        return "label"
    if n == "button" or re.search(r"lg-btn|lg-link|\bgo\b", cls):
        return "button"
    if re.search(r"lg-tag|vibe", cls):
        return "tag"
    return "p"


def blocks(root):
    """Leaf text containers in reading order. A container is emitted whole; its children are skipped."""
    out, seen = [], set()

    def walk(el):
        for c in el.children:
            if not isinstance(c, Tag):
                continue
            if c.name in DROP or c.get("hidden") is not None and c.name != "details":
                continue
            own = "".join(t for t in c.find_all(string=True, recursive=False) if isinstance(t, NavigableString))
            has_block_child = any(isinstance(x, Tag) and (x.name in BLOCK or x.name in ("div", "section", "ul", "ol", "table", "article", "figure", "a")) and clean(x.get_text(" "))
                                  for x in c.children)
            if c.name in BLOCK or c.name == "a" or (clean(own) and not has_block_child):
                t = clean(c.get_text(" "))
                if t and len(t) > 1:
                    k = kind(c)
                    key = (k, t)
                    if not out or out[-1] != key:
                        out.append(key)
                continue
            walk(c)
    walk(root)
    return out


def page_blocks(soup, keep_chrome=False):
    for sel in DROP:
        for x in soup.select(sel):
            x.decompose()
    if keep_chrome:
        parts = []
        for label, sel in [("Announcement bar", ".lg-tick"), ("Header and menu", ".lg-hdr"), ("Bag (cart drawer)", ".cd"), ("Footer", ".lg-ftr")]:
            el = soup.select_one(sel)
            if el:
                parts.append((label, blocks(el)))
        return parts
    for sel in CHROME:
        for x in soup.select(sel):
            x.decompose()
    main = soup.select_one("main") or soup.body
    return blocks(main)


def md_of(title, bl):
    lines = [f"## {title}", ""]
    for k, t in bl:
        if k in ("h1", "h2"):
            lines.append(f"**{t}** ({k.upper()})")
        elif k in ("h3", "h4", "h5"):
            lines.append(f"*{t}*")
        elif k == "label":
            lines.append(f"[label] {t}")
        elif k == "button":
            lines.append(f"[button/link] {t}")
        elif k == "tag":
            lines.append(f"[tag] {t}")
        else:
            lines.append(t)
        lines.append("")
    return "\n".join(lines)


def html_of(title, bl, pid):
    h = [f'<h1 id="{pid}">{html.escape(title)}</h1>']
    for k, t in bl:
        e = html.escape(t)
        if k in ("h1", "h2"):
            h.append(f'<p class="hd">{e} <span class="k">{k.upper()}</span></p>')
        elif k in ("h3", "h4", "h5"):
            h.append(f'<p class="sub">{e}</p>')
        elif k == "label":
            h.append(f'<p class="lb"><span class="k">LABEL</span> {e}</p>')
        elif k == "button":
            h.append(f'<p class="bt"><span class="k">BUTTON / LINK</span> {e}</p>')
        elif k == "tag":
            h.append(f'<p class="lb"><span class="k">TAG</span> {e}</p>')
        else:
            h.append(f"<p>{e}</p>")
    return "\n".join(h)


def article_blocks(path):
    raw = open(path, encoding="utf-8").read()
    head = []
    m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->", raw, re.S)
    if m:
        meta = json.loads(m.group(1))
        head = [("h1", clean(BeautifulSoup(meta.get("h1", meta.get("title", "")), "html.parser").get_text(" ")))]
        if meta.get("lede"):
            head.append(("p", meta["lede"]))
        raw = raw[m.end():]
    soup = BeautifulSoup(raw, "html.parser")
    for sel in DROP:
        for x in soup.select(sel):
            x.decompose()
    for sel in CHROME + ["header", "footer", "nav"]:
        for x in soup.select(sel):
            x.decompose()
    root = soup.select_one("article") or soup.select_one("main") or soup.body or soup
    faq = []
    if m and meta.get("faq"):
        faq = [("h2", "Questions")] + [x for q, a in meta["faq"] for x in (("h3", q), ("p", a))]
    return head + blocks(root) + faq


def main():
    s = session()
    md, hx, toc = ["# Lucky Golf: every word on the new site", "",
                   "Pulled from the build theme preview on 2026-09-27. Each page is on the template it gets at launch. "
                   "Text is shown as written: the site's styling turns some headings and labels into capitals. "
                   "LABEL = the small line above a heading. BUTTON / LINK = anything you tap.", ""], [], []
    home = fetch(s, "/", "")
    for label, bl in page_blocks(home, keep_chrome=True):
        md.append(md_of("Site-wide: " + label, bl)); hx.append(html_of("Site-wide: " + label, bl, f"c{len(toc)}")); toc.append("Site-wide: " + label)
    for title, path, view in PAGES:
        bl = page_blocks(fetch(s, path, view))
        print(f"{title}: {len(bl)} blocks")
        md.append(md_of(title, bl)); hx.append(html_of(title, bl, f"c{len(toc)}")); toc.append(title)
    # product descriptions that change on launch day
    rows = []
    live = {p["handle"]: p for p in json.load(open(os.path.join(ROOT, "v9", "migration", "live-products.json"), encoding="utf-8"))["products"]} \
        if os.path.exists(os.path.join(ROOT, "v9", "migration", "live-products.json")) else {}
    for f in sorted(glob.glob(os.path.join(ROOT, "v9", "migration", "product-copy", "*.json"))):
        h = os.path.basename(f)[:-5]
        v = json.load(open(f, encoding="utf-8"))["variables"]["product"]
        text = clean(BeautifulSoup(v.get("descriptionHtml", ""), "html.parser").get_text(" "))
        name = (live.get(h) or {}).get("title") or h
        rows.append(("h3", name)); rows.append(("p", text))
    md.append(md_of("Appendix A: product descriptions (go live on launch day)", rows)); hx.append(html_of("Appendix A: product descriptions (go live on launch day)", rows, f"c{len(toc)}")); toc.append("Appendix A: product descriptions")
    for f in sorted(glob.glob(os.path.join(ROOT, "v9", "src", "articles", "*.html"))):
        bl = article_blocks(f)
        t = next((x for k, x in bl if k == "h1"), os.path.basename(f)[:-5])
        md.append(md_of("Blog: " + t, bl)); hx.append(html_of("Blog: " + t, bl, f"c{len(toc)}")); toc.append("Blog: " + t)

    open(OUT[:-4] + ".md", "w", encoding="utf-8").write("\n".join(md))
    css = """body{font-family:sans-serif;font-size:10.5pt;line-height:1.45;color:#17140F}
    h1{font-size:17pt;margin:0 0 10pt;padding-top:4pt;border-bottom:1pt solid #999}
    p{margin:0 0 6pt} .hd{font-size:13pt;font-weight:bold;margin-top:10pt} .sub{font-weight:bold;margin-top:6pt}
    .lb{color:#555;font-size:9.5pt} .bt{color:#555;font-size:9.5pt} .k{font-size:7.5pt;color:#8A6A1C;font-weight:bold}
    .cover h1{border:0;font-size:22pt} .toc p{margin:0 0 2pt}"""
    cover = ('<div class="cover"><h1>Lucky Golf: every word on the new site</h1>' + "".join(f"<p>{html.escape(x)}</p>" for x in md[2:3]) +
             '<p class="sub">Contents</p><div class="toc">' + "".join(f"<p>{i + 1}. {html.escape(t)}</p>" for i, t in enumerate(toc)) + "</div></div>")
    doc = f"<html><head><style>{css}</style></head><body>{cover}" + "".join(f'<div style="page-break-before:always">{x}</div>' for x in hx) + "</body></html>"
    story = fitz.Story(html=doc)
    w = fitz.DocumentWriter(OUT)
    rect, where = fitz.paper_rect("letter"), fitz.paper_rect("letter") + (54, 54, -54, -54)
    more = True
    while more:
        dev = w.begin_page(rect)
        more, _ = story.place(where)
        story.draw(dev)
        w.end_page()
    w.close()
    d = fitz.open(OUT)
    print(OUT, d.page_count, "pages")


if __name__ == "__main__":
    main()
