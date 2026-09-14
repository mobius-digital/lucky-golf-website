"""
v8: every approved page on one board, plus a colour-system switch that
recolours all of them the same way, and a measured bar of how much of each
colour each page actually shows.

    python v8/tools/build-polo.py     (first: the polo product pages)
    python v8/tools/build.py          -> v8/out/* and v8/out/measure.json

Pages: home (August), carver (Sept 12), clubs + polos collections (v7),
13 polo product pages (v8). Systems are injected as html[data-sys] token
blocks, so "As saved" is always the untouched page.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V8 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V8, ".."))
OUT = os.path.join(V8, "out")
V7OUT = os.path.join(ROOT, "v7", "out")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

spec = importlib.util.spec_from_file_location("v7build", os.path.join(ROOT, "v7", "tools", "build.py"))
v7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v7)
v7.IMG = os.path.join(OUT, "img")

# ----------------------------------------------------------------- the systems
# Shared by all three: white page, ink text, one stone well, gold as the only
# accent (buttons, one word, stars), signal green only for "in stock" and the
# clover inside the logo. What changes is the ONE dark colour and where it goes.
SYSTEMS = {
    "a": {"name": "Ink & Gold", "dark": "#17140F", "header": "dark"},
    "b": {"name": "Deep Green & Gold", "dark": "#0B2E1F", "header": "dark"},
    "c": {"name": "White & Gold", "dark": "#17140F", "header": "white"},
}

ON_DARK = ("--on-brand:#F4F3F0;--on-brand-88:rgba(244,243,240,.88);--on-brand-22:rgba(244,243,240,.22);"
           "--brand-accent:#C29A2B;")
# Gold under dark type: the ramp without its darkest stop, so button text is 6.9:1, not 3.6:1.
FOIL = "linear-gradient(96deg,#C29A2B 0%,#EDD27C 50%,#C29A2B 100%)"
AUG_BASE = ("--cream:#F4F3F0;--white:#FFFFFF;")


def aug_css():
    out = [f"html[data-sys]{{{AUG_BASE}--lg-foil-h:{FOIL};--lg-foil-v:{FOIL}}}"]
    for k, s in SYSTEMS.items():
        d = s["dark"]
        if s["header"] == "dark":
            out.append(f'html[data-sys="{k}"]{{--brand:{d};{ON_DARK}--sys-dark:{d}}}')
        else:
            out.append(f'html[data-sys="{k}"]{{--brand:#FFFFFF;--on-brand:#17140F;--on-brand-88:rgba(23,20,15,.8);'
                       f'--on-brand-22:rgba(23,20,15,.16);--brand-accent:#8A6A1C;'
                       f'--brand-groove:none;--sys-dark:{d}}}')
    out.append("html[data-sys] .close,html[data-sys] .ftr,html[data-sys] .band-ink,html[data-sys] .ph--dark,"
               "html[data-sys] .mq,html[data-sys] .bband,html[data-sys] .v7-fit-tile,html[data-sys] .v7-tray,html[data-sys] .v7-band-ph,html[data-sys] .v7-pill,html[data-sys] .v7-tag.out{background-color:var(--sys-dark)}")
    out.append("html[data-sys] .badge-new,html[data-sys] .mtile .chip,html[data-sys] .jr-av{background:var(--sys-dark)}")
    out.append('html[data-sys="c"] .mq,html[data-sys="c"] .bband{background:#FFFFFF;color:#17140F;border-block:1px solid rgba(23,20,15,.12)}'
               'html[data-sys="c"] .mq-set span{color:#17140F}html[data-sys="c"] .hdr{border-bottom:1px solid rgba(23,20,15,.12)}')
    return "\n".join(out)


def v2_css():
    chrome_dark = lambda d: (f"--chrome:{d};--on-chrome:#F4F3F0;--on-chrome-m:rgba(244,243,240,.68);--chrome-rule:rgba(244,243,240,.18);"
                             f"--accent-on-chrome:#C29A2B;--clover-on-chrome:#C29A2B;")
    band_dark = lambda d: (f"--band:{d};--on-band:#F4F3F0;--on-band-m:rgba(244,243,240,.68);--band-rule:rgba(244,243,240,.18);"
                           f"--band-edge:0;--accent-on-band:#C29A2B;--clover-on-band:#C29A2B;--ok-on-band:#7FB69A;"
                           "--show-on-band-light:none;--show-on-band-dark:block;"
                           "--foil-text-band:linear-gradient(178deg,#C29A2B 0%,#EDD27C 46%,#EDD27C 56%,#C29A2B 100%);")
    out = [f"html[data-sys]{{--page:#FFFFFF;--tile:#F4F3F0;--text:#17140F;--foil:{FOIL}}}",
           "html[data-sys] .stars{color:#9A7619}html[data-sys] .band .stars,html[data-sys] .sign .stars{color:#C29A2B}"]
    for k, s in SYSTEMS.items():
        d = s["dark"]
        if s["header"] == "dark":
            out.append(f'html[data-sys="{k}"]{{{chrome_dark(d)}{band_dark(d)}}}')
        else:
            out.append(f'html[data-sys="{k}"]{{{v7.WHITE_CHROME}{v7.WHITE_BANDS}--tile:#F4F3F0}}'
                       f'html[data-sys="{k}"] .ftr{{{band_dark(d)}}}')
    return "\n".join(out)


LISTENER = """<script>
(function(){
  function set(k){ if(k && k!=='saved') document.documentElement.setAttribute('data-sys',k); else document.documentElement.removeAttribute('data-sys'); }
  var m=/[?&]sys=([a-z]+)/.exec(location.search); if(m) set(m[1]);
  window.addEventListener('message',function(e){ if(e.data && 'sys' in e.data) set(e.data.sys); });
  try{ parent.postMessage({ready:location.pathname.split('/').pop()},'*'); }catch(_){}
})();
</script>"""


# ----------------------------------------------------------------- logo + Mags
_SPRITE = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf-8").read()
SYMBOLS = {m.group(1): (m.group(2), m.group(3)) for m in
           re.finditer(r'<symbol id="(lg-[\w-]+)" viewBox="([^"]+)"[^>]*>(.*?)</symbol>', _SPRITE, re.S)}
WORD_VB = SYMBOLS["lg-lucky"][0]
WORD_W = round(26 * float(WORD_VB.split()[2]) / float(WORD_VB.split()[3]))


def inline_symbols(html):
    """<use href="#lg-..."> draws blank in some browsers (Cole saw the header
    wordmark vanish). Every logo symbol is written into its own svg instead."""
    def sub(m):
        attrs, sid = m.group(1), m.group(2)
        vb, inner = SYMBOLS[sid]
        if "viewBox" not in attrs:
            attrs += f' viewBox="{vb}"'
        return f'<svg{attrs} fill="currentColor" fill-rule="nonzero">{inner}</svg>'
    return re.sub(r'<svg([^>]*)>\s*<use href="#(lg-[\w-]+)"\s*/>\s*</svg>', sub, html)


MAGS = {  # context -> light version (dark grounds), ink version (white grounds)
    "bag": ("img/mags-bag-light.webp", "img/mags-bag-ink.webp", 543, 598),
    "big": ("img/mags-light.webp", "img/mags-ink.webp", 797, 494),
}


def mags_imgs(kind, alt=""):
    light, ink, w, h = MAGS[kind]
    return (f'<img class="mags-light" src="{light}" alt="{alt}" width="{w}" height="{h}" decoding="async">'
            f'<img class="mags-ink" src="{ink}" alt="" width="{w}" height="{h}" decoding="async">')


MAGS_CSS = """
/* Logo on the left, always the LUCKY wordmark. Mags: cream on dark grounds, ink on white. */
.hdr .logo .clv{display:none}
.hdr .logo .word{height:26px;width:""" + str(WORD_W) + """px}
.logo--lucky svg{width:100%;height:100%;display:block}
.cart.has-mags{width:54px;height:54px}
.cart.has-mags img,.bag img{width:48px;height:48px;object-fit:contain}
.mags-ink{display:none!important}
.mags-light{display:block!important}
html[data-sys="c"] .hdr .mags-light,html[data-sys="c"] .sign .mags-light{display:none!important}
html[data-sys="c"] .hdr .mags-ink,html[data-sys="c"] .sign .mags-ink{display:block!important}
"""


def logo_and_mags(html):
    html = inline_symbols(html)
    # v2 header: drop the separate clover (the wordmark already carries it)
    html = re.sub(r'(<a href="home\.html" class="logo"[^>]*>)<svg class="clv".*?</svg>(<svg class="word")',
                  lambda m: m.group(1) + m.group(2).replace('class="word"', f'class="word" width="{WORD_W}" height="26"'), html, count=1, flags=re.S)
    # v2 bag button and sign-off: light + ink, never the green on a dark ground
    html = re.sub(r'<img class="on-light" src="img/mags-bag\.webp"[^>]*>\s*<img class="on-dark" src="img/mags-bag-light\.webp"[^>]*>',
                  mags_imgs("bag"), html)
    html = re.sub(r'<img class="on-light" src="img/mags\.webp"[^>]*>\s*<img class="on-dark" src="img/mags-light\.webp"[^>]*>',
                  mags_imgs("big", "Mags, the magpie, with a gold wedge"), html)
    # August header: Mags on the bag button, like the product pages
    html = re.sub(r'<button type="button" class="cart" data-cart-open aria-label="Open bag">\s*<svg class="icn".*?</svg>',
                  '<button type="button" class="cart has-mags" data-cart-open aria-label="Open bag">' + mags_imgs("bag"), html, count=1, flags=re.S)
    return html.replace("</head>", f"<style id=\"mags\">{MAGS_CSS}</style>\n</head>", 1)


def make_ink_mags():
    """The emblem is drawn in deep green. Ink and White systems have no green,
    so an ink copy is made by recolouring only the green pixels; the gold club
    and the transparent belly stay as they are."""
    import numpy as np
    from PIL import Image
    for f in ("mags", "mags-bag"):
        a = np.array(Image.open(os.path.join(ROOT, "img", f + ".webp")).convert("RGBA")).astype(int)
        r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
        green = (al > 0) & (g > r + 8) & (g >= b) & ((r + g + b) < 330)
        a[green, 0], a[green, 1], a[green, 2] = 23, 20, 15
        Image.fromarray(a.astype("uint8"), "RGBA").save(os.path.join(OUT, "img", f + "-ink.webp"), "WEBP", quality=90)


def inject(html):
    css = aug_css() if "--brand:" in html else v2_css()
    html = logo_and_mags(html)
    html = html.replace("</head>", f'<style id="sys">{css}</style>\n</head>', 1)
    html = html.replace("var ok=/^(home|clubs|polos|carver-[a-z]+)\\.html/.test(h);",
                        "var ok=/^(home|clubs|polos|carver|20-product-polo-[a-z-]+)\\.html/.test(h);")
    html = html.replace('href="carver-white.html', 'href="carver.html').replace('href="02-pdp-lgw01.html', 'href="carver.html')
    html = html.replace('href="10-collection-polos.html', 'href="polos.html').replace('href="01-home.html', 'href="home.html')
    return html.replace("</body>", LISTENER + "\n</body>")


# ----------------------------------------------------------------- measuring
PROBE = r"""<script>
window.addEventListener('load',function(){
 [].forEach.call(document.images,function(i){i.loading='eager'});
 setTimeout(function(){
  var W=document.documentElement.clientWidth,H=document.documentElement.scrollHeight,step=10,c={};
  function rgb(s){var m=(s||'').match(/[\d.]+/g);return m?m.map(Number):null}
  function role(r){
    var P={white:[255,255,255],stone:[244,243,240],cream:[246,242,232],cream2:[236,230,217],ink:[23,20,15],deep:[11,46,31],clover:[11,81,48],gold:[194,154,43]};
    var best='other',bd=1e9;for(var k in P){var p=P[k],d=Math.pow(r[0]-p[0],2)+Math.pow(r[1]-p[1],2)+Math.pow(r[2]-p[2],2);if(d<bd){bd=d;best=k}}
    if(bd>900)return (r[0]+r[1]+r[2])/3>200?'stone':'other';
    return best==='cream2'?'cream':best;
  }
  function cls(x,y){
    var stack=document.elementsFromPoint(x,y);
    for(var i=0;i<stack.length;i++){
      var n=stack[i],t=n.tagName;
      if(t==='IMG'||t==='VIDEO'||t==='PICTURE'||t==='svg'&&n.closest('.mags-big'))return 'photo';
      var cs=getComputedStyle(n),bi=cs.backgroundImage;
      if(bi&&/url\(/.test(bi))return 'photo';
      if(bi&&/gradient/.test(bi)&&/194, 154, 43|237, 210, 124/.test(bi)&&!/repeating/.test(bi))return 'gold';
      var b=rgb(cs.backgroundColor);if(b&&(b.length<4||b[3]>.5)){for(var j=0;j<stack.length;j++){if(stack[j].tagName==='IMG'&&n.contains(stack[j]))return 'photo'}return role(b);}
    }
    return 'white';
  }
  window.scrollTo(0,0);
  for(var y=4;y<H;y+=step){for(var x=4;x<W;x+=step){var k=cls(x,y);c[k]=(c[k]||0)+1}}
  var pre=document.createElement('pre');pre.id='measure';pre.textContent='M'+JSON.stringify(c)+'M';document.body.appendChild(pre);
 },1500);
});
</script>"""


def measure(files):
    res = {}
    tmp = tempfile.mkdtemp(prefix="measure-", dir=OUT)
    try:
        for f in files:
            src = open(os.path.join(OUT, f), encoding="utf-8").read().replace("</body>", PROBE + "</body>")
            src = re.sub(r'(src|href)="img/', r'\1="../img/', src)
            for sys_key in ["saved"] + list(SYSTEMS):
                src_k = src if sys_key == "saved" else src.replace("<html", f'<html data-sys="{sys_key}"', 1)
                p = os.path.join(tmp, f"{sys_key}-{f}")
                open(p, "w", encoding="utf-8").write(src_k)
                r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1440,16000",
                                    "--virtual-time-budget=25000", "--dump-dom", "file:///" + p.replace("\\", "/")],
                                   capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=120)
                m = re.search(r"M(\{.*?\})M", r.stdout)
                if not m:
                    print("no measure", f, sys_key)
                    continue
                c = json.loads(m.group(1))
                tot = sum(c.values()) or 1
                res.setdefault(f, {})[sys_key] = {k: round(v * 100 / tot, 1) for k, v in sorted(c.items(), key=lambda kv: -kv[1])}
                print(f, sys_key, res[f][sys_key])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return res


def main():
    if "--measure-only" in sys.argv:
        m = measure(["home.html", "carver.html", "clubs.html", "polos.html", "20-product-polo-azalea.html"])
        json.dump(m, open(os.path.join(V8, "measure.json"), "w"), indent=1)
        return
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    make_ink_mags()
    for f in os.listdir(os.path.join(V7OUT, "img")):
        shutil.copy(os.path.join(V7OUT, "img", f), os.path.join(OUT, "img"))
    pages = {"home.html": "home.html", "carver.html": "carver-saved.html", "clubs.html": "clubs.html", "polos.html": "polos.html"}
    for dest, src in pages.items():
        html = open(os.path.join(V7OUT, src), encoding="utf-8").read()
        open(os.path.join(OUT, dest), "w", encoding="utf-8").write(inject(html))
    polos = sorted(f for f in os.listdir(os.path.join(V8, "raw")) if f.startswith("polo-"))
    for f in polos:
        html = open(os.path.join(V8, "raw", f), encoding="utf-8").read()
        html = v7.finish(html, {"01-home.html": "home.html", "02-pdp-lgw01.html": "carver.html"})
        open(os.path.join(OUT, "20-product-" + f), "w", encoding="utf-8").write(inject(html))
    left = sum(open(os.path.join(OUT, f), encoding="utf-8").read().count("cdn.shopify.com") for f in os.listdir(OUT) if f.endswith(".html"))
    print(f"pages ready; {left} remote image refs left")
    if "--measure-only" in sys.argv:
        pass
    if "--no-measure" not in sys.argv:
        m = measure(["home.html", "carver.html", "clubs.html", "polos.html", "20-product-polo-azalea.html"])
        json.dump(m, open(os.path.join(V8, "measure.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
