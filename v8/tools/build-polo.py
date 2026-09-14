"""
The polo product page, on the same system as the Carver 01 page Cole approved
(design system v2 as saved at d3be2d9). The template is the saved apparel
template with its weak spots fixed:

  * the empty "shot needed" tile      -> real close-up crops of the print and
                                         the collar, cut from the product photo
  * swatches shown twice              -> once, in the buy box, with a link to
                                         the whole collection
  * an empty "No reviews" section     -> not rendered when there are no reviews
  * nothing about fit near the sizes  -> the fit note, verbatim, under the sizes
  * no quick facts                    -> the four facts strip, like the Carver

    python v8/tools/build-polo.py      -> v8/raw/polo-*.html + v8/out/img/*
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V8 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V8, ".."))
SITE = os.path.join(V8, "site")
RAW = os.path.join(V8, "raw")
IMG = os.path.join(V8, "out", "img")
DATA = os.path.join(ROOT, "_src", "data")
PHOTOS = os.path.join(ROOT, "v4", "img-raw")
PACKS = os.path.join(ROOT, "v4", "out", "img")
TILE = (244, 243, 240)

J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
P = {p["id"]: p for p in J(DATA, "products.json")["products"]}
POLOS = [c for c in J(DATA, "products.json")["collections"] if c["id"] == "polos"][0]["products"]


def git_show(path):
    return subprocess.check_output(["git", "show", "d3be2d9:" + path], cwd=ROOT).decode("utf-8")


def swap(s, old, new):
    if old not in s:
        sys.exit("template changed, not found: " + old[:70])
    return s.replace(old, new, 1)


def patch_template():
    t = git_show("_src/page-apparel.html")
    t = swap(t, """      <div class="tile slot" data-md-open="md-shot" data-title="On body" data-brief="{{lifestyleBrief}}"><div><small>Shot needed &middot; on body</small><span>{{lifestyleBrief}}</span></div></div>\n""", "")
    t = swap(t, """{{/swatches}}

    <div id="pickers"></div>""", """{{/swatches}}
    <p class="all-prints"><a href="{{collLink}}">See all the polos side by side &rarr;</a></p>

    <div id="pickers"></div>
    <!--FITNOTE-->""")
    t = swap(t, """<a href="{{link:none}}" data-md-open="md-delivery">Estimate delivery</a></div>""",
             """<a href="{{link:none}}" data-md-open="md-delivery">Estimate delivery</a></div>
    <!--FACTS-->""")
    i = t.index("<!-- ============ MORE COLOURS")
    j = t.index('<div class="wrap"><span class="groove"></span></div>', i)
    t = t[:i] + t[j:]
    t = swap(t, """    <div class="tile tall slot" data-md-open="md-shot" data-title="On body" data-brief="{{lifestyleBrief}}"><div><small>Shot needed &middot; on body &middot; 4:5</small><span>{{lifestyleBrief}}</span></div></div>""",
             """    <!--PIECEIMG-->""")
    i = t.index("<!-- ============ REVIEWS ============ -->")
    j = t.index("<!-- ============ WEAR IT WITH ============ -->")
    t = t[:i] + "{{#rating}}\n" + t[i:j] + "{{/rating}}\n\n" + t[j:]
    open(os.path.join(SITE, "_src", "page-apparel.html"), "w", encoding="utf-8").write(t)

    css = git_show("_src/page-apparel.css") + """
/* v8 · the fixes: crops fill their tiles, fit note, four facts, collection link */
.gal .tile img{width:100%;height:100%;object-fit:cover}
.all-prints{margin:10px 0 0;font-size:var(--fs-md)}
.all-prints a{color:var(--text-70);text-underline-offset:3px}
.fitnote{margin:10px 0 0;padding:12px 14px;background:var(--tile);border-radius:var(--r);font-size:var(--fs-md);line-height:1.45;color:var(--text-70)}
.fitnote b{color:var(--text)}
.facts4{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:1fr 1fr;border-top:1px solid var(--rule)}
.facts4 li{padding:12px 12px 12px 0;border-bottom:1px solid var(--rule)}
.facts4 b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;font-size:var(--fs-sm);letter-spacing:.1em;text-transform:uppercase}
.facts4 span{display:block;margin-top:2px;font-size:var(--fs-md);color:var(--text-muted)}
.piece-img{margin:0;border-radius:var(--r-card);overflow:hidden;aspect-ratio:4/5;background:var(--tile)}
.piece-img img{width:100%;height:100%;object-fit:cover}
.piece-img figcaption{position:relative;margin-top:-40px;padding:0 16px 14px;font-size:var(--fs-sm);letter-spacing:.1em;text-transform:uppercase;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.5)}
"""
    open(os.path.join(SITE, "_src", "page-apparel.css"), "w", encoding="utf-8").write(css)


def crop(src, dest, cx, cy, frac, w, h):
    im = Image.open(src).convert("RGB")
    side = int(min(im.size) * frac)
    ch = int(side * h / w) if h > w else side
    cw = side
    x0 = int(min(max(im.width * cx - cw / 2, 0), im.width - cw))
    y0 = int(min(max(im.height * cy - ch / 2, 0), im.height - ch))
    im.crop((x0, y0, x0 + cw, y0 + ch)).resize((w, h), Image.LANCZOS).save(os.path.join(IMG, dest), "WEBP", quality=82)
    return "img/" + dest


def main_image(pid):
    man = J(PHOTOS, "manifest.json")
    fn = next(k for k, v in man.items() if v["product"] == pid and v["role"] == "main")
    return os.path.join(PHOTOS, fn)


def post(pid):
    p = P[pid]
    fam = J(DATA, "copy", "_family-" + p["family"] + ".json")
    html = open(os.path.join(SITE, "20-product-" + pid + ".html"), encoding="utf-8").read()
    src = main_image(pid)
    Image.open(os.path.join(PACKS, pid + "-pack.webp")).save(os.path.join(IMG, pid + "-pack.webp"), "WEBP", quality=82)
    print_crop = crop(src, pid + "-print.webp", 0.5, 0.6, 0.30, 900, 900)
    collar_crop = crop(src, pid + "-collar.webp", 0.5, 0.26, 0.30, 900, 900)
    piece_crop = crop(src, pid + "-print-tall.webp", 0.5, 0.58, 0.34, 960, 1200)
    name = p["name"]
    gal = (f'<div class="gal" data-gal aria-label="Product images">'
           f'<figure class="tile one" data-zoom="img/{pid}-pack.webp"><img src="img/{pid}-pack.webp" alt="{name}, front" width="1200" height="1500" decoding="async"></figure>'
           f'<figure class="tile" data-zoom="{print_crop}"><img src="{print_crop}" alt="{name}, print close up" width="900" height="900" loading="lazy"></figure>'
           f'<figure class="tile" data-zoom="{collar_crop}"><img src="{collar_crop}" alt="{name}, collar close up" width="900" height="900" loading="lazy"></figure>'
           f'</div>\n    <div class="dots" data-dots aria-hidden="true"><i></i><i></i><i></i></div>')
    html, n = re.subn(r'<div class="gal" data-gal[^>]*>.*?</div>\s*<div class="dots"[^>]*>.*?</div>', gal, html, count=1, flags=re.S)
    if n != 1:
        sys.exit(pid + ": gallery block not found")
    fit = fam["fitParas"]
    note = f'<p class="fitnote"><b>Fit:</b> {fit[1] if p["family"] == "polo-classic" else fit[0]} Between sizes? Size up.</p>'
    facts = '<ul class="facts4">' + "".join(f'<li><b>{x["k"]}</b><span>{x["v"]}</span></li>' for x in fam["four"]) + "</ul>"
    piece = f'<figure class="piece-img"><img src="{piece_crop}" alt="{name}, the print up close" width="960" height="1200" loading="lazy"></figure>'
    for mark, val in (("<!--FITNOTE-->", note), ("<!--FACTS-->", facts), ("<!--PIECEIMG-->", piece)):
        if mark not in html:
            sys.exit(pid + ": marker missing " + mark)
        html = html.replace(mark, val)
    open(os.path.join(RAW, pid + ".html"), "w", encoding="utf-8").write(html)


def main():
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(IMG, exist_ok=True)
    patch_template()
    r = subprocess.run([sys.executable, os.path.join("tools", "build.py"), "apparel"], cwd=SITE, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout[-2000:] + r.stderr[-2000:])
    for pid in POLOS:
        post(pid)
    print(f"built {len(POLOS)} polo product pages into v8/raw")


if __name__ == "__main__":
    main()
