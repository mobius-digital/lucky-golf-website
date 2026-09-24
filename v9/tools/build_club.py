"""The other club pages (Blade, Mallet, Stryker) on the Carver's layout.

Cole, 2026-09-20: "thought they would all look kind of similar to the Carver
02". They do now: club.html injects the Carver's page CSS whole and repeats its
section order (gallery, buy box, film, in the wild, specs with the monitor,
photo band, reviews, more from the bag, sign-off, sticky bar). What a putter
does not have (lofts, grinds, two finishes) is simply not on the page.

Everything factual comes from the data: prices, hands and what is sold out from
_src/data/products.json, ratings and counts from _src/data/reviews.
The words live in v9/src/club-data.json. Imported by build.py.
"""
import json
import os

HAND = {"RH": "Right hand", "LH": "Left hand"}


def carver_css(SRC):
    s = open(os.path.join(SRC, "carver.html"), encoding="utf-8").read()
    return s[s.index("<style>") + 7:s.index("</style>")]


def gallery(items):
    gal = ""
    for src, alt, kind in items:
        cls = "cut" if kind == "cut" else ("wide" if kind == "wide" else "")
        gal += (f'      <figure class="{cls}" data-zoom="img/{src}">'
                f'<img src="img/{src}" alt="{alt}" loading="lazy"></figure>\n')
    return gal, "<i></i>" * len(items)


def options(pd):
    """Chips for anything with more than one value. One value is a spec, not a
    choice, so it goes in the table instead."""
    keys = [k.split("|") for k in pd["variants"]]
    n = len(keys[0])
    names = ["hand", "loft"][:n] if n <= 2 else ["hand"]
    order, groups, start, labels = [], "", {}, {}
    for i, name in enumerate(names):
        vals = []
        for k in keys:
            if k[i] not in vals:
                vals.append(k[i])
        order.append(name)
        start[name] = vals[0]
        for v in vals:
            labels[v] = HAND.get(v, v[:-1] + "° " + v[-1] if name == "loft" else v)
        if len(vals) < 2:
            continue
        chips = ""
        for v in vals:
            dead = all(not pd["variants"][k]["avail"] for k in pd["variants"] if k.split("|")[i] == v)
            chips += (f'<button class="lg-chip" type="button" data-v="{v}"{" data-dead" if dead else ""}'
                      f' aria-label="{labels[v]}">{labels[v]}</button>')
        groups += (f'<div class="row"><span class="lg-label">{"Hand" if name == "hand" else "Loft and grind"} '
                   f'<span class="m" data-pick="{name}"></span></span></div>'
                   f'<div class="lg-chips" data-opt="{name}" role="group" aria-label="{name}">{chips}</div>')
    return order, groups, start, labels


def sticky_opts(pd, order, labels):
    out = ""
    keys = [k.split("|") for k in pd["variants"]]
    for i, name in enumerate(order):
        vals = []
        for k in keys:
            if len(k) > i and k[i] not in vals:
                vals.append(k[i])
        if len(vals) < 2:
            continue
        opts = "".join(f'<option value="{v}">{labels.get(v, v)}</option>' for v in vals)
        out += (f'<label><span class="sr">{name}</span>'
                f'<select class="sb-sel" data-sb-opt="{name}">{opts}</select></label>')
    return out


def reviews_block(c, rv, stars5, live):
    """The Carver's review layout: the chart, three real quotes, read them all.
    Under 10 live reviews there is no section at all (Cole, 2026-09-24)."""
    if not rv or live[0] < 10:
        return '', None
    counts = {int(k): v for k, v in rv["totals"].items()}
    total, avg = live[0], int(live[1] * 10) / 10
    quotes = "".join(
        f'<figure class="lg-quote"><span class="lg-stars" aria-label="5 out of 5">{stars5}</span>'
        f'<blockquote>&ldquo;{q}&rdquo;</blockquote>'
        f'<figcaption>{n} · <span class="lg-stock">Verified buyer</span></figcaption></figure>'
        for n, q in c["quotes"])
    return ('<section class="lg-sec" id="reviews"><div class="lg-wrap">'
            '<div class="rv-top"><div><p class="lg-eyebrow">Reviews</p>'
            f'<h2 class="lg-d2">{avg:.1f} stars from {total} reviews</h2></div>'
            '<div id="prox"></div></div>'
            f'<div class="qs">{quotes}</div>'
            '<button class="readall" type="button" data-readall aria-expanded="false" aria-controls="jm">'
            '<b>Read every review</b><span>Newest first.</span>'
            '<i aria-hidden="true">+</i></button>'
            '<div class="jm" id="jm" hidden>'
            '<div class="jm-bar"><div class="lg-chips" id="jm-filters" role="group" aria-label="Filter reviews by rating"></div>'
            '<label><span class="sr">Sort reviews</span><select id="jm-sort"><option value="recent">Most recent</option>'
            '<option value="high">Highest rating</option><option value="low">Lowest rating</option></select></label></div>'
            '<p class="jm-count" id="jm-count"></p><div id="jm-list"></div>'
            '<div class="jm-more"><button class="lg-btn-line lg-btn-sm" type="button" id="jm-more">Show more reviews</button></div>'
            '</div></div></section>'), counts


def build(SRC, ROOT, fill, esc, js, stars5, key):
    c = json.load(open(os.path.join(SRC, "club-data.json"), encoding="utf-8"))[key]
    products = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))
    pd = [p for p in products["products"] if p["id"] == c["pid"]][0]
    rv = None
    if c.get("reviews"):
        rv = json.load(open(os.path.join(ROOT, "_src", "data", "reviews", c["reviews"] + ".json"), encoding="utf-8"))

    gal, dots = gallery(c["gallery"])
    order, groups, start, labels = options(pd)
    rcf = json.load(open(os.path.join(ROOT, "_src", "data", "review-counts.json"), encoding="utf-8"))
    rvlive = tuple(rcf["counts"].get(pd.get("shopifyHandle", ""), [0, 0]))
    block, prox = reviews_block(c, rv, stars5, rvlive)
    live = any(v["avail"] for v in pd["variants"].values())

    rate = ""
    if rv and rvlive[0] >= rcf["_threshold"]:
        avg = int(rvlive[1] * 10) / 10
        first = c["quotes"][0]
        rate = (f'<div class="rvl"><span class="lg-stars" aria-label="{avg} out of 5">{stars5}</span>'
                f'<a href="#reviews">&ldquo;{esc(first[1][:52].rstrip())}…&rdquo; {esc(first[0])} · read the reviews</a></div>')

    tiles = "".join(f'<div class="lg-mt"><span>{esc(lab)}</span><b>{esc(val)}</b></div>'
                    for val, lab in c["tiles"])
    rows = "".join(f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in c["specs"])
    pband = "".join(f'<figure class="pb"><img src="img/{i}" alt="{esc(a)}" loading="lazy"></figure>'
                    for i, a in c["pband"])
    more = "".join(
        f'<a class="lg-card" href="{h}"><span class="lg-card-ph is-cut"><img src="img/{im}" alt="" loading="lazy"></span>'
        f'<span class="lg-card-bd"><span class="lg-card-nm">{esc(nm)}</span><span class="lg-card-pr">{pr}</span>'
        f'<span class="lg-card-ln">{esc(ln)}</span></span></a>' for h, im, nm, pr, ln in c["more"])

    PD = {"name": c["name"], "price": pd["price"], "img": "img/" + c["gallery"][0][0],
          "variants": pd["variants"], "order": order, "start": start, "labels": labels,
          "atc": c.get("atc", "Put it in the bag")}

    return fill(open(os.path.join(SRC, "club.html"), encoding="utf-8").read(), {
        "CARVER_CSS": carver_css(SRC),
        "NAME": c["name"], "H1": c.get("h1", c["name"]), "PRICE": pd["priceLabel"],
        "METAL": f' data-metal="{c["metal"]}"' if c["metal"] else "",
        "EYEBROW": c["eyebrow"], "LEDE": c["lede"], "GAL": gal, "DOTS": dots, "RVL": rate,
        "OPTS": groups, "ATC": c.get("atc", "Put it in the bag"),
        "STOCK": "In stock · ships in 1 to 2 days" if live else "Sold out",
        "DETAILS": "".join(f'<details class="lg-fq"><summary>{esc(q)}</summary><div class="lg-fq-a"><p>{a}</p></div></details>'
                           for q, a in c["details"]),
        "STORY_EYEBROW": c["story"]["eyebrow"], "STORY_HEAD": c["story"]["head"],
        "STORY_BODY": "".join(f'<p class="lg-body">{p}</p>' for p in c["story"]["body"]),
        "FILM_TITLE": c["film"][0], "FILM_BRIEF": c["film"][1],
        "WHO": c["who"], "SPEC_HEAD": c["spechead"], "SPEC_LINE": c["specline"], "SPEC_NOTE": c["specnote"],
        "MON_LABEL": c["monlabel"], "MON_IMG": c["gallery"][0][0],
        "MON_STOCK": "In stock" if live else "Sold out",
        "MON_TILES": tiles, "SPEC_ROWS": rows, "PBAND": pband,
        "REVIEWS": block, "MORE": more,
        "SIGNLEDE": c["signlede"],
        "SIGNCTA": c.get("signcta", "Back to the top"),
        "STICKYOPTS": sticky_opts(pd, order, labels),
        "PD_JSON": js(PD),
        "REVIEWS_JSON": js({"total": rvlive[0] or rv["total"], "totals": rv["totals"], "sample": rv["sample"]} if rv
                           else {"total": 0, "totals": {}, "sample": []}),
        "REEL_JSON": js(c["reel"])})
