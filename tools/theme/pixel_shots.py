"""Full-height screenshots of every build-theme page at desktop and phone width, for before/after
pixel checks when code changes must not change the look.

    python tools/theme/pixel_shots.py before          -> _ref/pixel/before/<page>-<w>.png
    python tools/theme/pixel_shots.py after           -> _ref/pixel/after/...
    python tools/theme/pixel_shots.py diff            -> prints the % of pixels that differ per page

Pages can take an override path per run: after/<page> uses AFTER_PATHS when set (e.g. a club on its
own template), so the same page is compared across templates.
"""
import os, subprocess, sys, tempfile, concurrent.futures as cf
from PIL import Image, ImageChops

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
THEME = "171555127573"
BASE = "https://www.luckygolf.com"
PAGES = {
    "home": "/",
    "clubs": "/collections/lucky-golf-clubs?view=clubs",
    "carver-gold": "/products/lucky-golf-lgw02-gold?view=club",
    "carver-black": "/products/lucky-golf-lgw02-black?view=club",
    "blade": "/products/signature-gold-putters?view=club",
    "mallet": "/products/limited-edition-mallet-putter?view=club",
    "stryker": "/products/lucky-striker-hybrid-limited-edition?view=club",
    "polos": "/collections/polos?view=polos",
    "polo": "/products/frost-classic-polo?view=polo",
    "hats": "/collections/hats?view=hats",
    "hat": "/products/white-gold-classic-hat?view=hat",
    "gear": "/collections/gear?view=gear",
    "glove": "/products/lucky-clover-tour-glove?view=gear",
    "story": "/pages/about?view=story",
    "faq": "/pages/faq-lucky-wedges?view=faq",
    "reviews": "/pages/reviews?view=reviews",
    "contact": "/pages/contact-us?view=contact",
    "ambassadors": "/pages/become-apart-of-the-team?view=ambassadors",
    "blog": "/blogs/news",
    "cart": "/cart",
    "search": "/search?q=wedge",
    "404": "/pages/this-does-not-exist",
    "giftcard": "/products/lucky-wedges-gift-card?view=giftcard",
}
AFTER_PATHS = {  # the clubs on their own editable templates (2026-09-30)
    "carver-gold": "/products/lucky-golf-lgw02-gold?view=club-carver-gold",
    "carver-black": "/products/lucky-golf-lgw02-black?view=club-carver-black",
    "blade": "/products/signature-gold-putters?view=club-blade",
    "mallet": "/products/limited-edition-mallet-putter?view=club-mallet",
    "stryker": "/products/lucky-striker-hybrid-limited-edition?view=club-stryker",
}
WIDTHS = {1440: 16000, 390: 22000}


def url(path):
    sep = "&" if "?" in path else "?"
    return f"{BASE}{path}{sep}preview_theme_id={THEME}&_fd=0&pb=0"


def shot(name, path, w, h, outdir):
    out = os.path.join(outdir, f"{name}-{w}.png")
    prof = tempfile.mkdtemp()
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio",
                    f"--user-data-dir={prof}", f"--window-size={w},{h}", "--virtual-time-budget=20000",
                    f"--screenshot={out}", url(path)],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    return out


def run(kind):
    outdir = os.path.join(ROOT, "_ref", "pixel", kind)
    os.makedirs(outdir, exist_ok=True)
    only = sys.argv[2:] or list(PAGES)
    jobs = []
    with cf.ThreadPoolExecutor(6) as ex:
        for name in only:
            path = AFTER_PATHS.get(name, PAGES[name]) if kind == "after" else PAGES[name]
            for w, h in WIDTHS.items():
                jobs.append(ex.submit(shot, name, path, w, h, outdir))
        for j in jobs:
            print(j.result())


def diff():
    b, a = (os.path.join(ROOT, "_ref", "pixel", k) for k in ("before", "after"))
    os.makedirs(os.path.join(ROOT, "_ref", "pixel", "diff"), exist_ok=True)
    for f in sorted(os.listdir(a)):
        if not os.path.exists(os.path.join(b, f)):
            continue
        i1 = Image.open(os.path.join(b, f)).convert("RGB")
        i2 = Image.open(os.path.join(a, f)).convert("RGB")
        if i1.size != i2.size:
            print(f"{f}: SIZE {i1.size} vs {i2.size}")
            continue
        d = ImageChops.difference(i1, i2)
        bbox = d.getbbox()
        if not bbox:
            print(f"{f}: identical")
            continue
        px = sum(1 for p in d.convert("L").getdata() if p > 16)
        pct = 100 * px / (i1.size[0] * i1.size[1])
        d.point(lambda v: 255 if v > 16 else 0).save(os.path.join(ROOT, "_ref", "pixel", "diff", f))
        print(f"{f}: {pct:.3f}% differ, box {bbox}")


if __name__ == "__main__":
    k = sys.argv[1]
    diff() if k == "diff" else run(k)
