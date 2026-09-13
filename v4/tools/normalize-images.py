"""
Turn the raw studio frames into a set that sits together: same canvas, same
ground colour, same product size and position. Honest cleanup only: no
retouching, no background generation, no new pixels on the product.

    python v4/tools/normalize-images.py

Reads  v4/img-raw/ + v4/data/images.json + _src/data/products.json
Writes v4/out/img/  and  v4/out/img/manifest.json

How: find the product's bounding box on the white studio sweep (ignoring the
faint shadow), scale it into a fixed box on a fixed canvas, then multiply the
whole frame by the tile colour so the studio white becomes the tile and the
shadow stays a shadow.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.normpath(os.path.join(HERE, ".."))
ROOT = os.path.normpath(os.path.join(V4, ".."))
RAW = os.path.join(V4, "img-raw")
OUT = os.path.join(V4, "out", "img")

TILE = (244, 243, 240)          # --tile in v4 css; keep in step
PACK = (1200, 1500)             # 4:5 card
GALLERY = (1600, 1600)          # 1:1 product page frame
APPAREL = (1200, 1500)
PHOTO_MAX = 2000


def load(fn):
    im = Image.open(os.path.join(RAW, fn))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
        bg.alpha_composite(im)
        im = bg
    return im.convert("RGB")


def bbox(im, thresh=226):
    a = np.asarray(im).min(axis=2)
    mask = a < thresh
    rows = np.where(mask.sum(axis=1) > 3)[0]
    cols = np.where(mask.sum(axis=0) > 3)[0]
    if not len(rows) or not len(cols):
        raise ValueError("no product found")
    return cols[0], rows[0], cols[-1] + 1, rows[-1] + 1


def studio_white(im):
    a = np.asarray(im).min(axis=2)
    k = 24
    edge = np.concatenate([a[:k].ravel(), a[-k:].ravel(), a[:, :k].ravel(), a[:, -k:].ravel()])
    return np.median(edge) >= 244


def cover(im, canvas):
    """Full-bleed crop for detail frames shot on a grey sweep: the sweep is
    part of the photograph, so fill the frame instead of floating the product."""
    W, H = canvas
    try:
        x0, y0, x1, y1 = bbox(im, thresh=200)
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    except ValueError:
        cx, cy = im.width / 2, im.height / 2
    s = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    left = int(min(max(cx * s - W / 2, 0), im.width - W))
    top = int(min(max(cy * s - H / 2, 0), im.height - H))
    return im.crop((left, top, left + W, top + H))


def white_point(im):
    """Studio sweeps come in anywhere from 240 to 255. Lift the sweep to true
    white (a levels move, same as any exposure correction) so every frame
    lands on the tile colour instead of a slightly different grey box."""
    a = np.asarray(im).astype(np.float32)
    m = a.min(axis=2)
    k = 24
    edge = np.concatenate([m[:k].ravel(), m[-k:].ravel(), m[:, :k].ravel(), m[:, -k:].ravel()])
    bg = float(np.median(edge))
    if bg >= 254 or bg < 200:
        return im
    a = (a * (255.0 / bg)).clip(0, 255)
    return Image.fromarray(a.astype(np.uint8))


def place(im, canvas, box_w, box_h, cy=0.5):
    W, H = canvas
    im = white_point(im)
    x0, y0, x1, y1 = bbox(im)
    touches_top = y0 <= 3
    pad = int(0.02 * max(im.size))
    x0, y0 = max(0, x0 - pad), (0 if touches_top else max(0, y0 - pad))
    x1, y1 = min(im.width, x1 + pad), min(im.height, y1 + pad)
    crop = im.crop((x0, y0, x1, y1))
    s = min(box_w * W / crop.width, box_h * H / crop.height)
    crop = crop.resize((max(1, round(crop.width * s)), max(1, round(crop.height * s))), Image.LANCZOS)
    out = Image.new("RGB", canvas, (255, 255, 255))
    x = (W - crop.width) // 2
    y = 0 if touches_top else int(cy * H - crop.height / 2)
    y = max(0, min(H - crop.height, y))
    out.paste(crop, (x, y))
    tile = np.array(TILE, dtype=np.float32) / 255.0
    arr = (np.asarray(out, dtype=np.float32) * tile).clip(0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def save(im, name, q=82):
    im.save(os.path.join(OUT, name), "WEBP", quality=q, method=6)
    return "img/" + name


def main():
    os.makedirs(OUT, exist_ok=True)
    sel = json.load(open(os.path.join(V4, "data", "images.json"), encoding="utf-8"))
    raw = json.load(open(os.path.join(RAW, "manifest.json"), encoding="utf-8"))
    products = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))["products"]
    man = {"products": {}, "photos": {}}
    errors = []

    def own(pid, fn):
        if not fn.startswith(pid + "__"):
            errors.append(f"{pid}: {fn} belongs to another product")
            return False
        if not os.path.exists(os.path.join(RAW, fn)):
            errors.append(f"{pid}: {fn} is not in img-raw")
            return False
        return True

    for pid, s in sel["products"].items():
        entry = {}
        if own(pid, s["pack"]):
            im = load(s["pack"])
            if not studio_white(im):
                errors.append(f"{pid}: pack shot {s['pack']} is not on a white sweep; pick another")
            entry["pack"] = save(place(im, PACK, 0.80, 0.86, cy=0.55), f"{pid}-pack.webp")
        entry["gallery"] = []
        for i, fn in enumerate(s.get("gallery", [])):
            if own(pid, fn):
                im = load(fn)
                framed = place(im, GALLERY, 0.78, 0.84) if studio_white(im) else cover(im, GALLERY)
                entry["gallery"].append(save(framed, f"{pid}-g{i}.webp"))
        man["products"][pid] = entry

    for p in products:
        pid = p["id"]
        if not pid.startswith(("polo-", "hat-")):
            continue
        fn = next((k for k, v in raw.items() if v["product"] == pid and v["role"] == "main"), None)
        if not fn or not own(pid, fn):
            errors.append(f"{pid}: no main image")
            continue
        box = (0.84, 0.74) if pid.startswith("polo-") else (0.86, 0.60)
        man["products"][pid] = {"pack": save(place(load(fn), APPAREL, *box, cy=0.5), f"{pid}-pack.webp")}

    wanted = set(sel["photos"].values())
    for s in sel["products"].values():
        wanted.update(s.get("photos", []))
    for fn in sorted(wanted):
        im = load(fn)
        if im.width > PHOTO_MAX:
            im = im.resize((PHOTO_MAX, round(im.height * PHOTO_MAX / im.width)), Image.LANCZOS)
        man["photos"][fn] = {"src": save(im, fn.replace(".webp", "") + ".webp", q=80), "w": im.width, "h": im.height}

    json.dump(man, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"), indent=1)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)
    n = sum(1 for _ in os.listdir(OUT))
    print(f"ok: {n} files in v4/out/img")


if __name__ == "__main__":
    main()
