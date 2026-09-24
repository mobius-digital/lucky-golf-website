"""The simple product page: covers, grips, the glove. Imported by build.py.

Options, prices and stock come from _src/data/products.json. The words are in
GEAR_COPY below and say nothing the product data or the Shopify listing does
not already back up: no invented materials, no invented weights.
"""
import json
import os

LABELS = {"RH": "Right hand", "LH": "Left hand", "STD": "Standard", "MID": "Midsize", "JMB": "Jumbo",
          "LDY": "Lady", "S": "S", "M": "M", "L": "L", "XL": "XL"}

GEAR_COPY = {
    "cover-blade": {
        "eyebrow": "Putter cover · blade",
        "desc": "Cut for a blade head, white with the clover on it. The Eclipse ships without a cover, so this is the thing that stops it rattling around in the bag.",
        "facts": [["Fits", "Blade putters"], ["Colour", "White, green clover"]],
        "sign": ("The putter ships <span class=\"lg-foil-word\">naked</span>", "Twenty-nine ninety-five to keep the face off the irons.")},
    "cover-mallet": {
        "eyebrow": "Putter cover · mallet",
        "desc": "Shaped for a mallet head, in both hands. The Eclipse Mallet comes without a cover, and a mallet is the one that picks up the most bag chatter.",
        "facts": [["Fits", "Mallet putters"], ["Hand", "Right and left"]],
        "sign": ("Keep the gold <span class=\"lg-foil-word\">gold</span>", "A cover is the cheapest insurance on a $229 putter.")},
    "cover-driver": {
        "eyebrow": "Head cover · driver",
        "desc": "White with the stripes and the clover. It fits a driver or a fairway wood, and it makes the top of the bag look like it belongs to somebody.",
        "facts": [["Fits", "Driver and fairway woods"], ["Colour", "White, green stripes"]],
        "sign": ("The top of the bag counts <span class=\"lg-foil-word\">too</span>", "Forty dollars and the driver stops looking like a rental.")},
    "glove-tour": {
        "eyebrow": "Glove",
        "desc": "The clover on the back of the hand, in both hands and four sizes. Pick the size you already wear; if you are between two, go down, because a glove stretches and never shrinks back.",
        "facts": [["Hands", "Left and right"], ["Sizes", "S, M, L, XL"]],
        "sign": ("One glove, one <span class=\"lg-foil-word\">clover</span>", "Seventeen ninety-five, and it matches the hat.")},
    "grip-clover": {
        "eyebrow": "Club grip",
        "desc": "Tour velvet style, soft and tacky, with the clover on it. Midsize and Jumbo cost a little more because there is more rubber in them, which is the only reason.",
        "facts": [["Style", "Tour velvet"], ["Sizes", "Standard, Midsize, Jumbo"]],
        "sign": ("Ten dollars of <span class=\"lg-foil-word\">better</span>", "A fresh grip is the cheapest thing in golf you can actually feel.")},
    "grip-clover-pink": {
        "eyebrow": "Club grip",
        "desc": "Tour velvet style, soft and tacky, in pink, in the Lady size. Same grip as the rest of the range in a smaller diameter.",
        "facts": [["Style", "Tour velvet"], ["Size", "Lady"]],
        "sign": ("Ten dollars of <span class=\"lg-foil-word\">better</span>", "A fresh grip is the cheapest thing in golf you can actually feel.")},
    "grip-putter-oversized": {
        "eyebrow": "Putter grip · oversized",
        "desc": "An oversized putter grip in four thicknesses. Bigger takes the hands out of the stroke, which is the whole reason people go oversized.",
        "facts": [["Sizes", "1.0, 2.0, 3.0, 5.0"], ["Status", "Between runs"]],
        "sign": ("Quiet hands, straight <span class=\"lg-foil-word\">putts</span>", "Sold out right now. Tap the button and we will email you the day it lands.")},
    "grip-putter-stock": {
        "eyebrow": "Putter grip",
        "desc": "The grip that comes on an Eclipse, sold on its own. For when yours has worn smooth and you want it back the way it arrived.",
        "facts": [["Fits", "Eclipse Blade and Mallet"], ["Size", "Stock"]],
        "sign": ("Back the way it <span class=\"lg-foil-word\">arrived</span>", "Nineteen ninety-five for the grip you already know.")},
}


def copy_for(pid):
    if pid in GEAR_COPY:
        return GEAR_COPY[pid]
    if pid.startswith("grip-clover"):
        return GEAR_COPY["grip-clover"]
    if pid.startswith("grip-putter") and pid != "grip-putter-stock":
        return GEAR_COPY["grip-putter-oversized"]
    return GEAR_COPY["cover-blade"]


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
            labels[v] = LABELS.get(v, v)
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
        "NAME": esc(p["name"]), "IMG": img, "PHOTO": photo, "PHOTO_ALT": photo_alt,
        "EYEBROW": c["eyebrow"], "PRICE": esc(PD["priceLabel"]), "DESC": c["desc"], "OPTS": opts,
        "STOCK": "In stock · ships in 1 to 2 days" if live_any else "Sold out",
        "FACTS": facts, "MOREHEAD": "The rest of the <span class=\"lg-foil-word\">small stuff</span>", "MORE": more,
        "SIGNHEAD": c["sign"][0], "SIGNLEDE": c["sign"][1], "PD_JSON": js(PD)})
