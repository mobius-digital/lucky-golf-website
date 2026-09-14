"""
v7: "show me the pages I liked" — no redesign, no edits to the pages.

    python v7/tools/build.py      -> v7/out/ (review.html + the pages + img/)

  home.html          01-home.html exactly as committed at 8d78d99 (the August site)
  carver-*.html      02-pdp-lgw01.html exactly as saved at d3be2d9 (the Sept 12
                     Carver 01 page), in the three colour states it went through
                     that day. Only the colour tokens differ between them.

The only things added to each page: images served locally (the review viewer
blocks cdn.shopify.com), links between the two pages rewired, and a guard so
links to pages not in this preview do nothing.
"""
import os
import re
import shutil
import subprocess
import urllib.request

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V7 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V7, ".."))
OUT = os.path.join(V7, "out")
IMG = os.path.join(OUT, "img")
CACHE = os.path.join(ROOT, "v5", "img-cache")

WHITE_CHROME = ("--chrome:#FFFFFF;--on-chrome:#17140F;--on-chrome-m:rgba(23,20,15,.64);--chrome-rule:rgba(23,20,15,.14);"
                "--accent-on-chrome:#8A6A1C;--clover-on-chrome:#0B5130;"
                "--groove-chrome:repeating-linear-gradient(180deg,rgba(23,20,15,.028) 0 1px,rgba(23,20,15,0) 1px 6px);")
WHITE_BANDS = ("--band:#FFFFFF;--on-band:#17140F;--on-band-m:rgba(23,20,15,.64);--band-rule:rgba(23,20,15,.14);--band-edge:1px;"
               "--accent-on-band:#8A6A1C;--clover-on-band:#0B5130;--ok-on-band:#008340;"
               "--groove-band:repeating-linear-gradient(180deg,rgba(23,20,15,.028) 0 1px,rgba(23,20,15,0) 1px 6px);"
               "--slot-stripe-band:repeating-linear-gradient(135deg,rgba(23,20,15,.05) 0 8px,transparent 8px 16px);"
               "--foil-text-band:linear-gradient(178deg,#8A6A1C 0%,#C29A2B 24%,#EDD27C 50%,#C29A2B 76%,#8A6A1C 100%);"
               "--show-on-band-light:block;--show-on-band-dark:none;--tile:#F3F1EC;")

GUARD = """<script>
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href]'); if(!a) return;
  var h=a.getAttribute('href')||'';
  if(h.charAt(0)==='#'||h.indexOf('javascript')===0) return;
  var ok=/^(home|carver-[a-z]+)\\.html/.test(h);
  if(!ok){e.preventDefault();
    var t=document.getElementById('pv-toast');
    if(!t){t=document.createElement('div');t.id='pv-toast';t.style.cssText='position:fixed;left:50%;bottom:22px;transform:translateX(-50%);background:#17140F;color:#fff;font:14px system-ui,sans-serif;padding:12px 16px;border-radius:6px;z-index:99999;box-shadow:0 8px 24px rgba(0,0,0,.25)';document.body.appendChild(t);}
    t.textContent='That page is not part of this preview.';t.style.opacity='1';clearTimeout(t._h);t._h=setTimeout(function(){t.style.opacity='0'},1800);
  } else { e.preventDefault(); try{ parent.postMessage({pvGo:h},'*'); }catch(_){} }
},true);
</script>"""


def git_show(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], cwd=ROOT).decode("utf-8")


def localize(s):
    os.makedirs(CACHE, exist_ok=True)
    for u in sorted(set(re.findall(r'https://cdn\.shopify\.com/[^"\'\s)\\]+', s))):
        name = re.sub(r"[^A-Za-z0-9._-]", "_", u.split("?")[0].split("/")[-1])
        raw = os.path.join(CACHE, name)
        if not os.path.exists(raw):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            open(raw, "wb").write(urllib.request.urlopen(req, timeout=40).read())
        dest = os.path.splitext(name)[0] + ".webp"
        if not os.path.exists(os.path.join(IMG, dest)):
            im = Image.open(raw)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            im.thumbnail((1800, 1800))
            im.save(os.path.join(IMG, dest), "WEBP", quality=82)
        s = s.replace(u, "img/" + dest)
    return s


def finish(s, links):
    for old, new in links.items():
        s = s.replace(f'href="{old}', f'href="{new}')
    s = localize(s)
    return s.replace("</body>", GUARD + "\n</body>")


def main():
    if os.path.exists(OUT):
        for f in os.listdir(OUT):
            if f.endswith(".html") and f != "review.html":
                os.remove(os.path.join(OUT, f))
    os.makedirs(IMG, exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "img")):
        shutil.copy(os.path.join(ROOT, "img", f), IMG)

    home = git_show("8d78d99", "01-home.html")
    open(os.path.join(OUT, "home.html"), "w", encoding="utf-8").write(
        finish(home, {"02-pdp-lgw01.html": "carver-white.html", "01-home.html": "home.html"}))

    carver = git_show("d3be2d9", "02-pdp-lgw01.html")
    states = {
        "white": WHITE_CHROME + WHITE_BANDS,   # palette D as picked: white header, white bands
        "bands": WHITE_CHROME,                 # afternoon: white header, dark bands low on the page
        "saved": "",                           # evening: dark header and dark bands (the saved file)
    }
    for key, tokens in states.items():
        page = carver
        if tokens:
            page = page.replace("</head>", f'<style id="pv-colour">:root{{{tokens}}}</style>\n</head>', 1)
        page = finish(page, {"01-home.html": "home.html", "02-pdp-lgw01.html": f"carver-{key}.html"})
        open(os.path.join(OUT, f"carver-{key}.html"), "w", encoding="utf-8").write(page)
    left = sum(open(os.path.join(OUT, f), encoding="utf-8").read().count("cdn.shopify.com")
               for f in os.listdir(OUT) if f.endswith(".html"))
    print(f"built v7/out: home + 3 carver colour states; {len(os.listdir(IMG))} images; {left} remote image refs left")


if __name__ == "__main__":
    main()
