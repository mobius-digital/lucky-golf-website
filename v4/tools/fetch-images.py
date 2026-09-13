"""
Pull every product and on-course image the v4 pages can use into v4/img-raw/,
so the review build is self-contained (no Shopify CDN at view time) and the
normaliser has local pixels to work on.

    python v4/tools/fetch-images.py

Writes v4/img-raw/manifest.json: {local filename: {url, product, role, alt}}.
Re-running skips files already on disk.
"""
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V4, ".."))
DATA = os.path.join(ROOT, "_src", "data")
RAW = os.path.join(V4, "img-raw")

CDN = "https://cdn.shopify.com/s/files/1/2286/3149/files/"


def slug(url):
    name = url.split("?")[0].rstrip("/").split("/")[-1]
    return re.sub(r"[^A-Za-z0-9._-]", "_", name)


def main():
    os.makedirs(RAW, exist_ok=True)
    products = json.load(open(os.path.join(DATA, "products.json"), encoding="utf-8"))["products"]
    want = {}  # filename -> meta

    def add(url, product, role, alt=""):
        if not url or not url.startswith("http"):
            return
        fn = slug(url)
        if product:
            fn = f"{product}__{fn}"
        want.setdefault(fn, {"url": url, "product": product, "role": role, "alt": alt})

    for p in products:
        add(p.get("img"), p["id"], "main", p["name"])
        cp = os.path.join(DATA, "copy", p["id"] + ".json")
        if os.path.exists(cp):
            c = json.load(open(cp, encoding="utf-8"))
            base = c.get("galleryBase") or ""
            for i, g in enumerate(c.get("gallery") or []):
                src, alt = (g[0], g[1]) if isinstance(g, list) else (g.get("src"), g.get("alt", ""))
                if src and not src.startswith("http"):
                    src = (base or CDN) + src
                add(src, p["id"], f"gallery{i:02d}", alt)

    # On-course photography referenced anywhere in the current sources.
    blob = ""
    for base, _d, files in os.walk(os.path.join(ROOT, "_src")):
        for f in files:
            if f.endswith((".html", ".json", ".js", ".css")):
                blob += open(os.path.join(base, f), encoding="utf-8", errors="ignore").read()
    for m in set(re.findall(r"https://cdn\.shopify\.com/s/files/1/2286/3149/files/lucky-[a-z0-9-]+\.webp", blob)):
        add(m, None, "photo")

    ok = fail = skip = 0
    for fn, meta in sorted(want.items()):
        dest = os.path.join(RAW, fn)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            skip += 1
            continue
        try:
            req = urllib.request.Request(meta["url"], headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                open(dest, "wb").write(r.read())
            ok += 1
        except Exception as e:  # noqa: BLE001
            meta["error"] = str(e)
            fail += 1
            print("FAIL", fn, e, file=sys.stderr)
    json.dump(want, open(os.path.join(RAW, "manifest.json"), "w", encoding="utf-8"), indent=1)
    print(f"fetched {ok}, already had {skip}, failed {fail}, total {len(want)}")


if __name__ == "__main__":
    main()
