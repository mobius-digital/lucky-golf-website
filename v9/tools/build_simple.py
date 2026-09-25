"""The simple product page: covers, grips, the glove. Imported by build.py.

Options, prices and stock come from _src/data/products.json. The words are in
GEAR_COPY below and say nothing the product data or the Shopify listing does
not already back up: no invented materials, no invented weights.
"""
import json
import os

# a glove is worn on the other hand, so the glove says who each one is for (Cole, 2026-09-25)
GLOVE_HANDS = {"LH": "Left hand (right-handed golfers)", "RH": "Right hand (left-handed golfers)"}
LABELS = {"RH": "Right hand", "LH": "Left hand", "STD": "Standard", "MID": "Midsize", "JMB": "Jumbo",
          "LDY": "Lady", "S": "S", "M": "M", "L": "L", "XL": "XL"}

GEAR_COPY = {   # copy v10, 2026-09-24
    "cover-blade": {
        "eyebrow": "Putter cover · blade",
        "desc": "Cut for a blade head, white with the clover on it. The Eclipse Blade ships without a cover, and this keeps the face off your irons.",
        "facts": [["Fits", "Blade putters"], ["Colour", "White, green clover"]],
        "sign": ("", "Tell them it's your lucky putter cover.")},
    "cover-mallet": {
        "eyebrow": "Putter cover · mallet",
        "desc": "Shaped for a mallet head, white with the clover. The Eclipse Mallet ships without a cover, and a mallet's the one that takes the most bag chatter.",
        "facts": [["Fits", "Mallet putters"], ["Hand", "Right and left"]],
        "sign": ("", "Tell them it's your lucky putter cover.")},
    "cover-driver": {
        "eyebrow": "Head cover · driver",
        "desc": "White with the stripes and the clover. It fits a driver or a fairway wood, and the top of the bag stops looking like a rental.",
        "facts": [["Fits", "Driver and fairway woods"], ["Colour", "White, green stripes"]],
        "sign": ("", "Tell them it's your lucky head cover.")},
    "glove-tour": {
        "eyebrow": "Glove",
        "desc": "The clover on the back of the hand, in four sizes. Pick the size you already wear, and if you're between two, go down: a glove stretches and never shrinks back.",
        "note": "Cabretta leather, with the clover embroidered on the wrist strap.",
        "facts": [["Hands", "Left (for right-handed golfers) and right"], ["Sizes", "S, M, L, XL"]],
        "sign": ("", "Tell them it's your lucky glove.")},
    "grip-clover": {
        "eyebrow": "Club grip",
        "desc": "Tour velvet style, soft and tacky, with the clover on it. Midsize and Jumbo cost a little more because there's more rubber in them.",
        "facts": [["Style", "Tour velvet"], ["Sizes", "Standard, Midsize, Jumbo"]],
        "sign": ("", "Tell them it's your lucky grips.")},
    "grip-clover-pink": {
        "eyebrow": "Club grip",
        "desc": "Tour velvet style, soft and tacky, in pink and the Lady size, which is the same grip in a smaller diameter.",
        "facts": [["Style", "Tour velvet"], ["Size", "Lady"]],
        "sign": ("", "Tell them it's your lucky grips.")},
    "grip-putter-oversized": {
        "eyebrow": "Putter grip · oversized",
        "desc": "An oversized putter grip in four thicknesses. Bigger quiets the hands in the stroke, which is the whole reason people go oversized.",
        "facts": [["Sizes", "1.0, 2.0, 3.0, 5.0"]],
        "sign": ("", "Tell them it's your lucky putter grip.")},
    "grip-putter-stock": {
        "eyebrow": "Putter grip",
        "desc": "The grip that comes on an Eclipse, sold on its own, for when yours has worn smooth and you want it back the way it arrived.",
        "facts": [["Fits", "Eclipse Blade and Mallet"], ["Size", "Stock"]],
        "sign": ("", "Tell them it's your lucky putter grip.")},
}


def copy_for(pid):
    if pid in GEAR_COPY:
        return GEAR_COPY[pid]
    if pid.startswith("grip-clover"):
        return GEAR_COPY["grip-clover"]
    if pid.startswith("grip-putter") and pid != "grip-putter-stock":
        return GEAR_COPY["grip-putter-oversized"]
    return GEAR_COPY["cover-blade"]


STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.6 6.1.7-4.5 4.2 1.2 6L10 15l-5.4 3 1.2-6L1.3 7.8l6.1-.7z"/></svg>'


def rvl(ROOT, p):
    """Stars and the count, only at 10+ live Judge.me reviews (Cole, 2026-09-24)."""
    rc = json.load(open(os.path.join(ROOT, "_src", "data", "review-counts.json"), encoding="utf-8"))
    n, avg = rc["counts"].get(p.get("shopifyHandle", ""), [0, 0])
    if n < rc["_threshold"]:
        return ""
    return (f'<div class="rvl"><span class="lg-stars" aria-label="{avg:.1f} out of 5">{STAR * 5}</span>'
            f'<span>{avg:.2f} · {n} reviews</span></div>')


def build(SRC, ROOT, fill, esc, js, pid):
    import live as livedata
    products = livedata.products()
    p = [x for x in products["products"] if x["id"] == pid][0]
    c = copy_for(pid)
    names = [o["name"] for o in p.get("options", [])]
    keys = [k.split("|") for k in p["variants"]] if names else []
    order, start, labels, opts = [], {}, {}, ""
    for i, nm in enumerate(names):
        key = nm.lower().replace(" ", "")
        vals = []
        for k in keys:
            if k[i] not in vals:
                vals.append(k[i])
        order.append(key)
        # start on the first value that is actually buyable
        live = [v for v in vals if any(p["variants"][kk]["avail"] for kk in p["variants"] if kk.split("|")[i] == v)]
        start[key] = (live or vals)[0]
        for v in vals:
            labels[v] = (GLOVE_HANDS.get(v) if pid == "glove-tour" else None) or LABELS.get(v, v)
        if len(vals) < 2:
            continue
        chips = ""
        for v in vals:
            dead = all(not p["variants"][kk]["avail"] for kk in p["variants"] if kk.split("|")[i] == v)
            chips += (f'<button class="lg-chip" type="button" data-v="{esc(v)}"{" data-dead" if dead else ""}>'
                      f'{esc(labels[v])}</button>')
        opts += (f'<div class="row"><span class="lg-label">{esc(nm)}</span><span class="m" data-pick="{key}"></span></div>'
                 f'<div class="lg-chips" data-opt="{key}" role="group" aria-label="{esc(nm)}">{chips}</div>')

    variants = {("|".join(k.split("|")) if names else ""): {"price": v["price"], "avail": v["avail"]}
                for k, v in p["variants"].items()}
    live_any = any(v["avail"] for v in p["variants"].values())
    img = "gear-" + pid + ".webp"
    others = [x for x in products["products"]
              if x.get("family") in ("headcover", "grip", "glove") and x["id"] != pid
              and any(v["avail"] for v in x["variants"].values())][:4]
    more = "".join(
        f'<a class="lg-card" href="gear-{x["id"]}.html"><span class="lg-card-ph is-cut">'
        f'<img src="img/gear-{x["id"]}.webp" alt="" loading="lazy"></span><span class="lg-card-bd">'
        f'<span class="lg-card-nm">{esc(x["name"])}</span><span class="lg-card-pr">{esc(x["priceLabel"].replace(chr(8211), " to "))}</span></span></a>'
        for x in others)
    facts = "".join(f'<li><span>{esc(a)}</span><b>{esc(b)}</b></li>' for a, b in c["facts"])
    photo, photo_alt = (("putter-in-hand.webp", "A Lucky putter in hand") if "cover" in pid or "putter" in pid
                        else ("lucky-bag-glove.webp", "A Lucky bag and glove"))
    PD = {"name": p["name"], "img": "img/" + img, "variants": variants, "order": order,
          "start": start, "labels": labels, "priceLabel": p["priceLabel"].replace(chr(8211), " to ")}
    return fill(open(os.path.join(SRC, "simple.html"), encoding="utf-8").read(), {
        "RVL": rvl(ROOT, p),
        "NAME": esc(p["name"]), "IMG": img, "PHOTO": photo, "PHOTO_ALT": photo_alt,
        "EYEBROW": c["eyebrow"], "PRICE": esc(PD["priceLabel"]), "DESC": c["desc"] + (f'</p><p class="lg-body">{c["note"]}' if c.get("note") else ""), "OPTS": opts,
        "STOCK": "In stock · ships in 1 to 2 days" if live_any else "Sold out",
        "FACTS": facts, "MOREHEAD": "Round out the bag", "MORE": more,
        "SIGNHEAD": c["sign"][0], "SIGNLEDE": c["sign"][1], "PD_JSON": js(PD)})
