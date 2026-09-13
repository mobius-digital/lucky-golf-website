"""
v5 home: the August home page (commit 8d78d99) with three changes Cole asked for
on 2026-09-13: lighter (no flat black bands), imagery first (every empty photo
box becomes a real course photo, big), and the cleaned-up product shots.
Structure, sections and copy stay the August ones.

    python v5/tools/apply-v5-home.py     # edits v5/august/_src, builds, copies to v5/out

Idempotent: it starts from the pristine August files in git every run.
"""
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
V5 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V5, ".."))
AUG = os.path.join(V5, "august")
OUT = os.path.join(V5, "out")
CDN = "https://cdn.shopify.com/s/files/1/2286/3149/files/"

ERR = []


def pristine(rel):
    return subprocess.check_output(["git", "show", "8d78d99:" + rel], cwd=ROOT).decode("utf-8")


def swap(s, old, new, count=1):
    n = s.count(old)
    if n < count or (count == 1 and n != 1):
        ERR.append(f"expected {count} of: {old[:90]!r}, found {n}")
        return s
    return s.replace(old, new)


def between(s, start, end, new):
    i = s.find(start)
    j = s.find(end, i)
    if i < 0 or j < 0:
        ERR.append(f"block not found: {start[:60]!r}")
        return s
    return s[:i] + new + s[j:]


PACK = {
    "lgw01-gold": "img/lgw01-gold-pack.webp", "lgw01-black": "img/lgw01-black-pack.webp",
    "lgp01-gold": "img/lgp01-gold-pack.webp", "lgp02-gold": "img/lgp02-gold-pack.webp",
    "lgh01": "img/lgh01-pack.webp",
}
SHOPIFY_PACK = {
    "6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868": "lgw01-gold",
    "1_27f81f90-a495-4dc4-ba02-0650ea6c4608.webp?v=1781012462": "lgw01-gold",
    "6_cef3d6fc-8907-4866-b6aa-6301f8c614b5.webp?v=1784586436": "lgw01-black",
    "3_f3d878d3-a4bb-4cc9-82df-f68e8eec3f61.webp?v=1782599090": "lgp01-gold",
    "1_b00c01f0-8116-464a-a39c-08a6ebf82b6f.webp?v=1782598133": "lgp02-gold",
    "3_a032f79a-78ab-436e-81c9-eea7bb5f7f40.webp?v=1782597493": "lgh01",
}


def photo(name):
    return CDN + name


def html():
    s = pristine("_src/page-home.html")

    # ---- product shots: the normalised pack shots everywhere a product sits on a tile
    for src, pid in SHOPIFY_PACK.items():
        s = s.replace(CDN + src, PACK[pid])

    # ---- putter feature: cutout on a plinth -> the putter on the green, full bleed.
    # The Blade is sold out, so the button goes to the Mallet that is in stock.
    s = between(s, '<section class="feat sec">', '<section class="why sec"', f"""<section class="feat feat--photo">
  <img class="feat-bg" src="{photo('lucky-putters-downline.webp')}" alt="Lucky Golf Tracer Mallet behind the ball on the green" width="2048" height="1365" loading="lazy" decoding="async">
  <span class="feat-scrim" aria-hidden="true"></span>
  <div class="wrap">
    <div class="feat-copy rv">
      <h2 class="disp d-m">No ping. No buzz. Just <span class="foil on-dark">roll</span></h2>
      <p class="body on-dark">Muted off the face, and it holds the line you picked. The short ones stop feeling like a coin flip.</p>
      <div class="feat-cta">
        <a href="{{{{link:p/lgp02-gold}}}}" class="btn btn-foil"><span>Roll it pure</span><span class="ar">&rarr;</span></a>
        <a href="{{{{link:p/lgp01-gold}}}}" class="btn btn-line-cream"><span>Prefer a blade?</span></a>
      </div>
      <div class="feat-stamp"><span class="stamp">LGP02 &middot; Tracer Mallet &middot; {{{{price:lgp02-gold}}}}</span><span class="ln"></span></div>
    </div>
  </div>
</section>
""")

    # ---- brand band: flat colour -> the course behind it
    s = swap(s, '<section class="bband" aria-label="Lucky Golf">',
             f'<section class="bband bband--photo" aria-label="Lucky Golf">\n  <img class="bband-bg" src="{photo("lucky-stryker-hero.webp")}" alt="" width="2048" height="1365" loading="lazy" decoding="async">')

    # ---- value props collage: the empty photo box becomes a real one
    s = between(s, '<div class="ph ph--dark">\n          <span class="lbl">\n            <span class="mono k">Photo needed</span>', '<img class="home-img" src="https://cdn.shopify.com/s/files/1/2286/3149/files/lucky-bag-glove.webp"',
                f'<img class="home-img" src="{photo("lucky-wedge-face-turf.webp")}" alt="Carver 01 Gold behind a ball on the grass" width="1067" height="1600" loading="lazy" decoding="async">\n        ')

    # ---- in the wild: six empty reel boxes -> six real course photos.
    # These are Lucky's own shoot, not customer posts, so the handles and play
    # buttons go and the heading says what it is.
    wild = [
        ("lucky-blade-hero.webp", "Tracer Blade", "lgp01-gold", "Tracer Blade behind the ball on the green", 1067, 1600),
        ("lucky-carver-black-hero.webp", "Carver 01 Black", "lgw01-black", "Carver 01 Black resting on the grass", 1365, 2048),
        ("lucky-allclubs-swing.webp", "Out of the bunker", "c/clubs", "Golfer splashing out of a bunker", 1366, 2048),
        ("lucky-mallet-hero.webp", "Tracer Mallet", "lgp02-gold", "Tracer Mallet on the fairway", 1968, 2048),
        ("lucky-wedge-two-soles.webp", "Carver 01 Gold", "lgw01-gold", "Two Carver 01 Gold wedges and a ball", 2048, 1365),
        ("lucky-hybrid-crown-turf.webp", "Stryker LGH01", "lgh01", "Stryker hybrid and two wedges on the grass", 1365, 2048),
    ]
    posts = "\n".join(
        f"""      <a class="post post--photo" href="{{{{link:{'p/' + pid if not pid.startswith('c/') else pid}}}}}">
        <div class="post-ph"><img src="{photo(fn)}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"></div>
        <div class="post-meta"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span><span class="h">{cap}</span></div>
      </a>""" for fn, cap, pid, alt, w, h in wild)
    s = between(s, '<div class="rail" role="region" aria-label="Customer and creator posts" tabindex="0">', '<div class="wrap ugc-foot rv">',
                f'<div class="rail" role="region" aria-label="Lucky clubs on the course" tabindex="0">\n{posts}\n  </div>\n  ')
    s = swap(s, 'Lucky golfers in the <span class="foil">wild</span>', 'Out on the <span class="foil">course</span>')
    s = swap(s, '<p class="aside" style="color:var(--ink-muted)">Tag us for a chance to get reposted.</p>',
             '<p class="aside" style="color:var(--ink-muted)">Playing one? Tag us and yours goes here.</p>')

    # ---- first tee spot: that bag photo shows another brand's irons, model name readable
    s = swap(s, 'src="https://cdn.shopify.com/s/files/1/2286/3149/files/lucky-carver-gold-hero.webp?v=1787514597" alt="Lucky Golf Carver 01 Gold wedges in a golf bag, clover mark on the sole" width="2048" height="1639"',
             f'src="{photo("lucky-carver-gold-address.webp")}" alt="Carver 01 Gold at address on the fairway" width="1366" height="2048"')

    # ---- gear: the two empty polo and hat boxes -> the real products
    s = swap(s, """      <article class="gtile">
        <div class="ph ph--dark">
          <span class="lbl"><span class="mono k">Photo needed</span><span class="mono">Portrait &middot; polo on-body, three-quarter crop, clover visible. Room bottom-left.</span></span>
        </div>
        <span class="gtile-scrim" aria-hidden="true"></span>""", """      <article class="gtile gtile--product">
        <img class="home-img" src="img/polo-gold-dust-pack.webp" alt="Gold Dust Classic Polo" width="1200" height="1500" loading="lazy" decoding="async">""")
    s = swap(s, """      <article class="gtile">
        <div class="ph ph--dark">
          <span class="lbl"><span class="mono k">Photo needed</span><span class="mono">Portrait &middot; hat on-body, brim three-quarter, late light. Room bottom-left.</span></span>
        </div>
        <span class="gtile-scrim" aria-hidden="true"></span>""", """      <article class="gtile gtile--product">
        <img class="home-img" src="img/hat-white-gold-classic-pack.webp" alt="White and gold Classic hat" width="1200" height="1500" loading="lazy" decoding="async">""")

    # ---- close: flat ink -> the whole line on the grass
    s = swap(s, '<section class="close">\n  <span class="wm" aria-hidden="true"><svg><use href="#lg-clover-plain"/></svg></span>\n  <span class="halo" aria-hidden="true"></span>',
             f'<section class="close close--photo">\n  <img class="close-bg" src="{photo("lucky-line-together.webp")}" alt="" width="2048" height="878" loading="lazy" decoding="async">')

    # ---- the rating: live Judge.me across the club line (build.py in v4 computes it)
    s = s.replace("4.78 from verified buyers", "4.81 from verified buyers")
    s = s.replace('style="--pct:95.6%" role="img" aria-label="4.78 out of 5"', 'style="--pct:96.2%" role="img" aria-label="4.81 out of 5"')
    s = s.replace("4.78 average from verified buyers on Judge.me", "4.81 average from 875 verified reviews on Judge.me")
    return s


CSS = r"""
/* ==========================================================================
   V5 (2026-09-13) · Cole: "generic, boring, not leaning into the imagery,
   dark heavy". August structure kept. No flat black bands: where August had
   one, there is now a photograph. One colour (green) at the top and bottom
   of the page, white in between, gold as the spice.
   ========================================================================== */
.mq{background:var(--white);border-block:1px solid var(--ink-08)}
.mq::before{display:none}
.mq-set span{color:var(--ink)}
.mq-set .mk{color:var(--green)}

/* product tiles: the cleaned-up shots sit on their own ground, no cream */
.ptile,.ptile .pt-ph,.pt-ph{background:#F4F3F0}
.fnd-c{background:#F4F3F0}
.rv-ph{background:#F4F3F0}

/* putter feature, full bleed */
.feat.feat--photo{position:relative;padding:0;min-height:clamp(520px,62vw,860px);display:flex;align-items:flex-end;
  background:#0f0d09;color:var(--cream);overflow:hidden}
.feat.feat--photo::before{display:none}
.feat-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.feat-scrim{position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(90deg,rgba(15,13,9,.72) 0%,rgba(15,13,9,.38) 38%,rgba(15,13,9,0) 64%),
             linear-gradient(0deg,rgba(15,13,9,.55) 0%,rgba(15,13,9,0) 45%)}
.feat--photo .wrap{position:relative;z-index:1;width:100%;padding-block:clamp(48px,6vw,96px)}
.feat--photo .feat-copy{max-width:560px}
.feat.feat--photo h2{color:var(--cream)}
.feat.feat--photo .on-dark{color:var(--cream-70)}
.feat.feat--photo .feat-stamp{color:var(--cream-70)}
.feat.feat--photo .feat-stamp .ln{background:rgba(246,242,232,.3)}

/* brand band over a photograph, green-tinted so the logo reads */
.bband.bband--photo{background:#0B2E1F;border-block:0}
.bband--photo::before{display:none}
.bband-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42;mix-blend-mode:luminosity}
.bband--photo .wm{display:none}
.bband--photo .wrap{position:relative;z-index:1}
.bband.bband--photo{padding:clamp(96px,11vw,170px) 0}

/* the collage, all real */
.vp-collage img{width:100%;height:100%;object-fit:cover;border-radius:var(--r)}

/* on the course: bigger frames, real photos */
.post.post--photo{flex:0 0 clamp(260px,26vw,380px);color:inherit;text-decoration:none}
.post--photo .post-ph{aspect-ratio:4/5;background:#F4F3F0}
.post--photo .post-ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.post--photo:hover .post-ph img{transform:scale(1.04)}
.post--photo .post-meta .h{color:var(--ink);font-weight:700}

/* first tee: bigger photo */
.spot-img{border-radius:var(--r);width:100%;aspect-ratio:4/5;object-fit:cover}

/* polo and hat tiles: product on its ground, words underneath instead of on a scrim */
.gtile.gtile--product{background:#F4F3F0;flex-direction:column}
.gtile--product > img{position:relative;inset:auto;height:auto;flex:1;min-height:0;object-fit:contain;aspect-ratio:auto;max-height:340px;margin:18px auto 0;width:auto}
.gtile--product .gtile-in{margin-top:0}
.gtile--product .gtile-ct{color:var(--ink-muted)}
.gtile--product .gtile-nm,.gtile--product .gtile-nm a{color:var(--ink)}
.gtile--product .gtile-ln{color:var(--ink-70)}
.gtile--product .btn-line-cream{color:var(--ink);border-color:var(--ink)}

/* close over the line together */
.close.close--photo{background:#0f0d09}
.close--photo::before{display:none}
.close-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 60%}
.close--photo::after{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(15,13,9,.78),rgba(15,13,9,.45));z-index:0}
.close--photo .close-in{z-index:1}
.close--photo .close-in{padding:clamp(120px,13vw,200px) 0}

/* gold buttons: drop the darkest foil stop from under the words (3.64:1 -> 6.9:1) */
.btn-foil{background-image:var(--lg-foil-tag)}

/* footer: the brand green, not black. Deep green, so gold still passes. */
.ftr{background:#0B2E1F}
.ftr::before{opacity:.5}
"""


def main():
    s = html()
    css = pristine("_src/page-home.css") + CSS
    if ERR:
        print("NOT APPLIED\n  " + "\n  ".join(ERR), file=sys.stderr)
        sys.exit(1)
    open(os.path.join(AUG, "_src", "page-home.html"), "w", encoding="utf-8").write(s)
    open(os.path.join(AUG, "_src", "page-home.css"), "w", encoding="utf-8").write(css)
    subprocess.check_call([sys.executable, os.path.join(AUG, "tools", "build.py"), "home"], cwd=AUG, stdout=subprocess.DEVNULL)
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    shutil.copy(os.path.join(AUG, "01-home.html"), os.path.join(OUT, "home.html"))
    for pid in list(PACK) + ["polo-gold-dust", "hat-white-gold-classic"]:
        shutil.copy(os.path.join(ROOT, "v4", "out", "img", pid + "-pack.webp"), os.path.join(OUT, "img"))
    print("v5 home built -> v5/out/home.html")


if __name__ == "__main__":
    main()


def localize():
    """The artifact viewer only serves the page's own files. Every Shopify image
    is downloaded once into v5/out/img (max 1600px), and the page points at it."""
    import re
    import urllib.request
    from PIL import Image
    path = os.path.join(OUT, "home.html")
    s = open(path, encoding="utf-8").read()
    cache = os.path.join(V5, "img-cache")
    os.makedirs(cache, exist_ok=True)
    urls = sorted(set(re.findall(r'https://cdn\.shopify\.com/[^"\'\s)]+', s)))
    for u in urls:
        name = re.sub(r"[^A-Za-z0-9._-]", "_", u.split("?")[0].split("/")[-1])
        base = os.path.splitext(name)[0] + ".webp"
        raw = os.path.join(cache, name)
        if not os.path.exists(raw):
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            open(raw, "wb").write(urllib.request.urlopen(req, timeout=40).read())
        dest = os.path.join(OUT, "img", base)
        if not os.path.exists(dest):
            im = Image.open(raw)
            im = im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB")
            im.thumbnail((1600, 1600))
            im.save(dest, "WEBP", quality=80, method=6)
        s = s.replace(u, "img/" + base)
    open(path, "w", encoding="utf-8").write(s)
    left = re.findall(r'https://cdn\.shopify\.com/', s)
    print(f"localized {len(urls)} images; {len(left)} remote references left")


if __name__ == "__main__":
    localize()
