"""The per-product editorial for the club template (templates/product.club.json).

One JSON template serves all five clubs, so everything that differs per club lives
on the product as the metafield custom.club_page (type json). This file builds those
five values from the approved v9 copy (v9/src/club-data.json, v9/tools/build_wedge.py)
so the words stay verbatim.

    python tools/theme/club_data.py            -> writes _ref/club-page/<handle>.json
    python tools/theme/club_data.py --mutation -> also prints metafieldsSet variables per product

Images are Content > Files names ("lg-...webp") or product media file names; the
section resolves them with file_url.
"""
import json, os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "v9", "tools"))
import build_wedge as W  # noqa: E402

C = json.load(open(os.path.join(ROOT, "v9", "src", "club-data.json"), encoding="utf-8"))

IDS = {
    "lucky-golf-lgw02-gold": "gid://shopify/Product/9583978905877",
    "lucky-golf-lgw02-black": "gid://shopify/Product/9574093717781",
    "signature-gold-putters": "gid://shopify/Product/8882491162901",
    "limited-edition-mallet-putter": "gid://shopify/Product/8973333496085",
    "lucky-striker-hybrid-limited-edition": "gid://shopify/Product/9226792304917",
}
SHIP = ("Orders leave Long Beach, California in 1 to 2 business days, and the tracking number shows up as soon as the "
        "carrier scans it. Every club gets sixty days from delivery. Talk to us before anything ships back, because club "
        "returns need our OK and a few photos first. Return shipping's on you.")
HANDLES = {"carver.html": "lucky-golf-lgw02-gold", "black.html": "lucky-golf-lgw02-black", "blade.html": "signature-gold-putters",
           "mallet.html": "limited-edition-mallet-putter", "stryker.html": "lucky-striker-hybrid-limited-edition",
           "hat-white-ibtbl.html": "white-its-better-to-be-lucky-patch-hat"}
GEAR = {"gear-cover-blade.webp": "lucky-putter-head-cover-blade", "gear-cover-mallet.webp": "lucky-putter-head-cover-mallet-large"}
REEL = [{"title": "Full swing from 100", "brief": "Ball tracked to the pin, reaction", "kind": "Creator reel"},
        {"title": "Greenside chip", "brief": "One hop and stop, shot from behind", "kind": "Customer clip"},
        {"title": "Bunker", "brief": "Sand spray, ball releasing to the hole", "kind": "Creator reel"},
        {"title": "The flop", "brief": "Face wide open, soft landing", "kind": "Customer clip"},
        {"title": "Face in sunlight", "brief": "Grooves and finish, slow pan", "kind": "Creator reel"},
        {"title": "Unboxing", "brief": "Out of the sleeve, first reaction", "kind": "Customer clip"}]

# the wedge sheet (carver.html SPEC): bounce, lie, length by grind and loft
SHEET = {"K": {"50": [8, 63, "35.25"], "52": [8, 63, "35.25"], "54": [12, 63, "35.125"], "56": [12, 63, "35.125"],
               "58": [10, 63, "35"], "60": [10, 63, "35"]},
         "S": {"52": [10, 63.5, "35.25"], "56": [12, 64, "35.125"], "60": [12, 64, "35"]}}
HEADLINE = "1020 forged carbon steel · CNC milled grooves and micro grooves over a sandblasted face"


def f(name):
    """v9 image name -> the Files name on the store (lg- prefix unless it is product media)."""
    return name if name[:2].rstrip("_").isdigit() and "_" in name[:4] else "lg-" + name


def sheet_table(g, lofts):
    s = SHEET[g]
    return {"id": g, "head": ["Loft"] + [l + "°" for l in lofts],
            "rows": [["Bounce"] + [f"{s[l][0]}°" for l in lofts],
                     ["Lie"] + [f"{s[l][1]}°" for l in lofts],
                     ["Length"] + [f"{s[l][2]}″" for l in lofts],
                     ["Head weight"] + ["300 g" for _ in lofts]],
            "span": ["Head", HEADLINE]}


def carver(gold):
    g = W.GOLD_GAL if gold else W.BLACK_GAL
    d = {
        "kind": "wedge",
        "eyebrow": "Forged wedge · LGW02", "h1": "Carver <em>02</em>",
        "lede": ("Fair warning: this thing spins, so your first few chips might stop shorter than you're used to. "
                 "It's forged, so it feels buttery off the face, and it's forgiving enough that the mishits still behave. "
                 "The micro-grooves and sandblasted face are doing the work. And yes, it's gold. People will ask."
                 if gold else
                 "Forged in darkness, lives in the shadows, and nobody sees it coming until it checks up by the pin. "
                 "Same forged 1020 steel and micro-grooved face as the gold one, blacked out for the job. It spins like "
                 "crazy, feels soft, and gives away nothing. Your buddies won't clock it until they're paying up on the bet."),
        "rvl": ["So nice, I bought it twice.", "JD M.", "read them all"],
        "finishes": [{"label": "Gold", "handle": "lucky-golf-lgw02-gold", "img": "lg-gold-3q-cut.webp"},
                     {"label": "Black", "handle": "lucky-golf-lgw02-black", "img": "lg-black-full-cut.webp"}],
        "gallery": [[f(s), a, c, t] for s, a, c, t in g],
        "details": [["What it's made of",
                     ("A forged 1020 carbon steel head with CNC-milled grooves on a micro-grooved, sandblasted "
                      "face. The K grind comes in all six lofts and the S in the 52, 56 and 60." if gold else
                      "A forged 1020 carbon steel head with CNC-milled grooves on a micro-grooved, sandblasted "
                      "face, finished in black with gold accents. The K grind comes in all six lofts.")],
                    ["What's in the box", ("One wedge in the loft and grind you picked, on the stock shaft and grip. No headcover. It's a wedge, it'll be fine." if gold else
                                          "One wedge in the loft you picked, on the stock shaft and grip. No headcover, which fits the whole no-witnesses thing.")],
                    ["Shipping and returns", SHIP]],
        "modals": True,
        "story": ({"eyebrow": "On the course", "head": "Inside 100 yards, it's this one.",
                   "body": ["Every golfer has a lucky something: a ball marker, a broken tee they won't throw out, socks that haven't "
                            "been washed since the club championship. None of them has ever gotten you up and down. This one's going to. The micro-grooved, sandblasted face grabs "
                            "the ball and checks it up like it hit a wall, and with six lofts from 50 to 60 there's one for every shot "
                            "inside 100. We make the wedge. The luck's on you."]} if gold else
                  {"eyebrow": "On the course", "head": "Stick it close. Leave no evidence.",
                   "body": ["From 100 yards in, this is the one you want. Six lofts from 50 to 60, and a sandblasted face that still "
                            "grabs when the grass is wet. Your playing partners will describe it later as \"that black thing.\""]}),
        "who": ("Anyone who's ever bladed a chip clean across the green and into the other bunker. So, everyone."
                if gold else "Anyone who likes a square setup and a quiet bag."),
        "film": ["The film", "16:9 product film, 40 to 60 seconds. The club in hand, face detail, then three shots played: full swing from 100, a greenside check-up, a bunker out. Sound on."],
        "film_small": "Film needed · 16:9 · 40 to 60 s",
        "world": "gold" if gold else "black",
        "spec": {"head": "Find your loft.",
                 "line": "On the K grind, bounce runs 8° on the 50 and 52, 12° on the 54 and 56, and 10° on the 58 and 60.",
                 "mon_label": "Carver 02 Gold · LGW02" if gold else "Carver 02 Black · LGW02",
                 "mon_img": "lg-gold-full-cut.webp" if gold else "lg-black-cut.webp",
                 "mon_alt": ("Carver 02 Gold" if gold else "Carver 02 Black") + ", the full head",
                 "tiles": [{"l": "Lofts", "b": "6", "vals": ["50°", "52°", "54°", "56°", "58°", "60°"]},
                           ({"l": "Grinds", "b": "2", "vals": ["K · every loft", "S · 52 56 60"]} if gold else
                            {"l": "Grind", "b": "K", "vals": ["Every loft"]}),
                           {"l": "Price", "price": True},
                           {"l": "Test drive", "b": "60", "em": "days to decide it's a keeper."}],
                 "tabs": True,
                 "seg": ([["K", "K grind · 6 lofts"], ["S", "S grind · 3 lofts"]] if gold else [["K", "K grind · 6 lofts"]]),
                 "hands": "Right and left hand" if gold else "Right hand",
                 "tables": ([sheet_table("K", ["50", "52", "54", "56", "58", "60"]), sheet_table("S", ["52", "56", "60"])]
                            if gold else [sheet_table("K", ["50", "52", "54", "56", "58", "60"])]),
                 "table_note": ("The S has more bounce on paper, but the narrower sole means it plays with less when you open the face."
                                if gold else ""),
                 "shafts": {"head": ["", "Lucky stock steel", "KBS"],
                            "rows": [["Availability", "Stock option, every loft", "Coming soon as an upgrade"], ["Material", "Steel", "Steel"],
                                     ["Flex", "Regular", "To be confirmed"], ["Kick point", "Mid", "To be confirmed"],
                                     ["Raw weight", "110 g", "To be confirmed"], ["Length", "35″", "To be confirmed"]],
                            "note": "The KBS numbers go up here when the upgrade lands."},
                 "grips": {"head": ["", "Lucky stock grip"],
                           "rows": [["Availability", "Stock option, every loft"], ["Material", "Rubber"], ["Size", "Regular"], ["Weight", "55 g"]],
                           "note": "One grip in one size, for now."},
                 "sheet": SHEET, "head_g": "300 g"},
        "pband": [["lg-swing-black-wedge.webp", "Holding the finish with the Carver 02 Black", "object-position:30% 40%"],
                  ["lg-walk-off-green.webp", "Walking off the green in the Lucky hat and polo", ""],
                  ["lg-fit-sunset.webp", "The Nightshade polo and white Lucky hat at sunset", ""]],
        "rv": {"write": True, "nums": True},
        "quotes": [{"t": "So nice, I bought it twice!", "q": "I bought myself a 60 degree last year. I love it so much, and get so many comments/compliments on the look… but the performance speaks even louder!", "n": "JD M."},
                   {"q": "Super great club, love the feel, the sound, the spin, only problem I have is getting under the ball with it but easy fix none the less. Great club!!", "n": "James B."},
                   {"t": "Hard to keep it!", "q": "People borrow it in my league- it’s a winner!", "n": "Ray O."}],
        "more": ([["lucky-golf-lgw02-black", "Carver 02 Black", "Same forged head, in the dark"]] if gold else
                 [["lucky-golf-lgw02-gold", "Carver 02 Gold", "Same forged head, in gold"]])
                + [["limited-edition-mallet-putter", "Eclipse Mallet", "Holds its line when you miss the middle." if gold else "Soft off the face, gold all over"],
                   ["lucky-striker-hybrid-limited-edition", "Stryker", "High and easy from the rough"],
                   ["white-its-better-to-be-lucky-patch-hat", "White It's Better To Be Lucky Hat", "Says it before you do"]],
        "sign": "Tell them it's your lucky wedge." if gold else "Nobody needs to know where you got it.", "signcta": "Pick a loft",
        "atc": "Put it in the bag",
        "reel": REEL,
        "grind_default": "K",
    }
    if gold:
        d["grinds"] = {"eyebrow": "Two grinds", "head": "Pick your grind.",
                       "body": "The difference is all in the sole.",
                       "panels": [{"tag": "K grind", "h": "The one you trust", "p": "Wide, flat sole and a standard leading edge. Set it up square, take your divot, go find your ball. It won't dig and it won't surprise you, which is all you want from a wedge on a Saturday.",
                                   "hud": [["6", "Lofts"], ["50 to 60°", "Range"], ["8 to 12°", "Bounce"]]},
                                  {"tag": "S grind", "h": "Open it up and get fancy", "p": "Narrower sole and a reshaped leading edge, so you can lay it wide open and slide it under a ball sitting on hardpan or in the sand. It's the flop-shot grind. Use responsibly.",
                                   "hud": [["3", "Lofts"], ["52 · 56 · 60°", "Range"], ["10 to 12°", "Bounce"]]}]}
    else:
        d["grinds"] = {"eyebrow": "One grind", "head": "One grind. Every loft.<br>No guesswork.",
                       "body": "The black runs on the K grind in all six lofts. Want to lay the face wide open? The S lives on the gold.",
                       "panels": [{"tag": "K grind", "h": "The one you trust", "p": "Wide, flat sole and a standard leading edge. Set up square, take your divot, and it does the same thing from the fairway or out of the rough.",
                                   "hud": [["6", "Lofts"], ["50 to 60°", "Range"], ["8 to 12°", "Bounce"]]},
                                  {"tag": "S grind", "h": "Open it up and get fancy", "p": "Narrower sole that opens up clean for tight lies and bunkers. Gold only, in the 52, 56 and 60.",
                                   "link": ["lucky-golf-lgw02-gold", "See the gold"]}]}
    return d


def club(key):
    c = C[key]
    q0 = c["quotes"][0]
    return {
        "kind": "club",
        "eyebrow": c["eyebrow"], "h1": c["h1"].replace('<span class="lg-foil-word">', "<em>").replace("</span>", "</em>"),
        "lede": c["lede"],
        "rvl": [q0[1][:52].rstrip() + "…", q0[0], "read the reviews"],
        "gallery": [[f(s), a, ("cut" if k == "cut" else "wide" if k == "wide" else ""), ""] for s, a, k in c["gallery"]],
        "details": c["details"],
        "story": {"eyebrow": c["story"]["eyebrow"], "head": c["story"]["head"].replace('<span class="lg-foil-word">', "<em>").replace("</span>", "</em>"),
                  "body": c["story"]["body"]},
        "who": c["who"], "film": c["film"], "film_small": "Film needed · 16:9 · 40 to 60 s",
        "spec": {"head": c["spechead"], "line": c["specline"], "note": c["specnote"],
                 "mon_label": c["monlabel"], "mon_img": f(c["gallery"][0][0]), "mon_alt": c["name"] + ", the full club",
                 "tiles": [{"l": lab, "b": val} for val, lab in c["tiles"]],
                 "rows": c["specs"]},
        "pband": [[f(i), a, ""] for i, a in c["pband"]],
        "rv": {"write": False, "nums": False},
        "quotes": [{"q": q, "n": n} for n, q in c["quotes"]],
        "more": [[HANDLES.get(h) or GEAR[im], nm, ln] for h, im, nm, pr, ln in c["more"]],
        "sign": c["signlede"],
        # the sold-out "Tell me when it's back" is live in the section, never stored (PORT-NOTES: stock is live)
        # Blade and Stryker (lead, 2026-09-27): "Put it in the bag" to the buy box, the section default
        "signcta": "" if key in ("blade", "stryker") else c.get("signcta", ""),
        "atc": c.get("atc", "Put it in the bag"),
        "reel": c["reel"],
    }


def all_pages():
    return {"lucky-golf-lgw02-gold": carver(True), "lucky-golf-lgw02-black": carver(False),
            "signature-gold-putters": club("blade"), "limited-edition-mallet-putter": club("mallet"),
            "lucky-striker-hybrid-limited-edition": club("stryker")}


# Content > Files ids for every photo the club pages use (queried 2026-09-27)
FID = {
    "4_744b4c6e-a04c-4618-9d58-9a36314000d8.webp": "49046484353301", "11_26414fab-14b8-41ae-8ad7-a801c2f646fb.webp": "49046484549909",
    "lg-black-cut.webp": "49395840057621", "lg-black-full-cut.webp": "49395840090389", "lg-black-hat-mallet.webp": "49395840123157",
    "lg-blade-cut.webp": "49395840155925", "lg-fit-sunset.webp": "49395840188693", "lg-from-the-cup.webp": "49395840221461",
    "lg-gold-3q-cut.webp": "49395840680213", "lg-gold-full-cut.webp": "49395840712981", "lg-gold-wedge-bag.webp": "49395840745749",
    "lg-green-read-fit.webp": "49395840778517", "lg-lgh01-pack.webp": "49395841138965", "lg-lgp01-gold-pack.webp": "49395841171733",
    "lg-lgp02-gold-pack.webp": "49395841204501", "lg-lgw01-black-pack.webp": "49395841237269", "lg-lucky-bag-glove.webp": "49395841270037",
    "lg-lucky-carver-gold-address.webp": "49395841302805", "lg-lucky-golfer-address.webp": "49395841335573",
    "lg-lucky-stryker-in-hand.webp": "49395841368341", "lg-mallet-full-cut.webp": "49395841532181", "lg-putt-sunset.webp": "49395843432725",
    "lg-putter-in-hand.webp": "49395843465493", "lg-stryker-full-cut.webp": "49395843498261", "lg-swing-black-wedge.webp": "49395843531029",
    "lg-two-gold-wedges.webp": "49395843563797", "lg-two-hats-mallet.webp": "49395843596565", "lg-walk-off-green.webp": "49395843629333",
}
gid = lambda n: "gid://shopify/MediaImage/" + FID[n]


def split(h, d):
    """Photos leave the JSON for file metafields (editable in the admin); the JSON keeps only layout by slot."""
    mf = []
    # the buy-box gallery is the product's own media (Cole, 2026-09-27); only its first tile's tag stays here
    tag = d.pop("gallery")[0][3]
    if tag:
        d["gallery_tag"] = tag
    band = [gid(b[0]) for b in d["pband"]]
    d["pband"] = [b[1:] for b in d["pband"]]                 # [alt, css position]
    spec = gid(d["spec"].pop("mon_img"))
    mf += [{"ownerId": IDS[h], "namespace": "custom", "key": "club_band_photos", "type": "list.file_reference", "value": json.dumps(band)},
           {"ownerId": IDS[h], "namespace": "custom", "key": "club_spec_photo", "type": "file_reference", "value": spec}]
    for fi in d.get("finishes", []):
        if fi["handle"] == h:
            mf.append({"ownerId": IDS[h], "namespace": "custom", "key": "club_swatch", "type": "file_reference", "value": gid(fi["img"])})
        fi.pop("img")
    return mf


if __name__ == "__main__":
    out = os.path.join(ROOT, "_ref", "club-page")
    os.makedirs(out, exist_ok=True)
    photos = []
    for h, d in all_pages().items():
        photos += split(h, d)
        s = json.dumps(d, ensure_ascii=False, separators=(",", ":"))
        open(os.path.join(out, h + ".json"), "w", encoding="utf-8").write(s)
        mv = {"metafields": [{"ownerId": IDS[h], "namespace": "custom", "key": "club_page", "type": "json", "value": s}]}
        open(os.path.join(out, h + ".vars.json"), "w", encoding="utf-8").write(json.dumps(mv, ensure_ascii=False))
        print(h, len(s))
    open(os.path.join(out, "photos.vars.json"), "w", encoding="utf-8").write(json.dumps({"metafields": photos}))
    print(len(photos), "photo metafields")
