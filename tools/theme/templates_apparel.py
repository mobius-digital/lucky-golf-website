"""Apparel + collections templates, filled with the approved v9 copy (v9/src/collection.html,
polos.html, hats.html, gear.html, clubs.html, polo.html, hat.html, simple.html and build.py).
Imported by build_templates.py."""


def im(name):
    return "shopify://shop_images/lg-" + name


def order(d):
    return list(d.keys())


def blocks(*items):
    """[(type, settings), ...] -> ({id: block}, order)"""
    b = {f"b{i + 1}": {"type": t, "settings": s} for i, (t, s) in enumerate(items)}
    return b, list(b.keys())


def sec(type_, settings, *items):
    d = {"type": type_, "settings": settings}
    if items:
        d["blocks"], d["block_order"] = blocks(*items)
    return d


def tpl(sections):
    return {"sections": sections, "order": list(sections.keys())}


def pband(label, *photos):
    return sec("lg-pband", {"label": label}, *[("photo", {"image": im(i), "pos": p}) for i, p in photos])


def signoff(head, lede, btn, href):
    return sec("lg-signoff", {"eyebrow": "The last word", "heading": head, "lede": lede, "btn2_label": btn, "btn2_url": href})


def faq(eyebrow, heading, body, qs, cols="even", no_top=True, trust=()):
    items = [("trust", {"icon": i, "text": t}) for i, t in trust] + [("q", {"q": q, "a": a}) for q, a in qs]
    return sec("lg-ap-faq", {"no_top": no_top, "eyebrow": eyebrow, "heading": heading, "body": body, "cols": cols}, *items)


def related(links, trust, rating=None):
    items = [("link", {"text": t, "url": u}) for t, u in links] + [("trust", {"icon": i, "text": t}) for i, t in trust]
    st = {"label": "Keep browsing"}
    if rating:
        st["rating_products"] = rating
    return sec("lg-ap-related", st, *items)


C = lambda h: "shopify://collections/" + h
P = lambda h: "shopify://products/" + h
CARVER, BLACK, BLADE, MALLET, STRYKER = ("lucky-golf-lgw02-gold", "lucky-golf-lgw02-black", "signature-gold-putters",
                                         "limited-edition-mallet-putter", "lucky-striker-hybrid-limited-edition")
RATED = [CARVER, BLADE, MALLET, STRYKER]   # Black shares Gold's Judge.me pool, so it isn't counted twice
LUCKY = "“It's better to be <em>lucky.</em>”"
FAQ_URL = "/pages/faq-lucky-wedges"

T = {}

# ------------------------------------------------------------------ collection (any; the approved "All products")
T["templates/collection.json"] = tpl({
    "head": sec("lg-ap-head", {"eyebrow": "Everything we make", "narrow": True,
                               "lede": "The whole shop on one page. Sort it, filter it, or just scroll until something gold catches your eye."}),
    "photos": pband("Lucky on the course", ("two-gold-wedges.webp", ""), ("fit-sunset.webp", ""), ("putt-sunset.webp", "")),
    "grid": sec("lg-ap-grid", {"card": "item", "f_kind": True, "f_stock": True, "sort_price": True, "empty": "Nothing matches that.",
                               "kind_map": "Wedges = Wedges\nPutter = Putters\nHybrids = Hybrid\nApparel = Polos\nHAT = Hats\nHead Cover = Covers\nGrip = Grips\nGrips = Grips\nGlove = Gloves"},
                ("tile", {"pos": 7, "eyebrow": "Can't decide?", "title": "Let them pick", "url": P("lucky-wedges-gift-card"), "cta": "Send a gift card"})),
    "related": related([("Clubs", C("lucky-golf-clubs")), ("Polos", C("polos")), ("Hats", C("hats")), ("Gear", C("gear"))],
                       [("star", "[avg] from [count] club reviews"), ("truck", "Free shipping at $198"), ("rotate-ccw", "Sixty days on clubs")], RATED),
    "signoff": signoff("That's the whole <em>shop</em>", "Sixty days to make up your mind on the clubs, thirty on the rest.", "Back to the top ↑", "#grid"),
})

# ------------------------------------------------------------------ polos
POLO_QS = [
    ("How does it fit?", "<p>It's an athletic fit, so it sits closer than a boxy golf polo, and the four-way stretch makes it more forgiving than the cut suggests. If you wear a large in a performance polo, a large here's right. Between sizes, or want room across the chest? Size up.</p>"),
    ("Classic collar or Blade collar?", "<p>The Blade has no buttons and no placket, so there's nothing at your throat. Everything else is the same shirt: athletic fit, 88/12 poly-spandex, four-way stretch and UPF 50+. You're picking a collar and a print.</p>"),
    ("What's it made of?", "<p>88% polyester and 12% spandex, with four-way stretch. It's moisture-wicking, wrinkle-resistant and UPF 50+. Machine wash cold, tumble dry low.</p>"),
    ("What if the size is wrong?", "<p>Send it back within thirty days, unworn with the tags on.</p>"),
]
T["templates/collection.polos.json"] = tpl({
    "head": sec("lg-ap-head", {"eyebrow": "Polos", "heading": "Loud prints, quiet prints, zero boxy <em>ones</em>",
                               "lede": "An athletic cut with four-way stretch, UPF 50+, and nothing tugging at the top of your backswing.",
                               "guide_label": "Size guide", "count_word": "polos"}),
    "photos": pband("The polos, worn", ("fit-sunset.webp", "object-position:52% center"), ("walk-off-green.webp", ""), ("green-read-fit.webp", "object-position:60% 40%")),
    "grid": sec("lg-ap-grid", {"card": "polo", "f_kind": False, "f_stock": False, "f_collar": True, "f_color": True, "color_dots": True,
                               "f_size": True, "sort_stock": True, "sort_price": False, "drop": "Classic Polo, Blade Polo",
                               "empty": "Nothing in that combination."},
                ("tile", {"pos": 8, "image": im("two-hats-mallet.webp"), "eyebrow": "Pairs well with", "title": "A hat that matches", "url": C("hats"), "cta": "Shop hats"})),
    "faq": faq("Before you pick", "Find your size", "Get it wrong and you've got thirty days to send it back, unworn with the tags on.", POLO_QS),
    "related": related([("Hats", C("hats")), ("Gear", C("gear")), ("Clubs", C("lucky-golf-clubs")), ("All products", C("all-products"))],
                       [("truck", "Free shipping at $198"), ("rotate-ccw", "Thirty days to send it back"), ("tag", "Sizes S to 3XL")]),
    "signoff": signoff(LUCKY, "Wear it the day you shoot your best round, or the day you need to look like you did.", "Back to the polos ↑", "#grid"),
})

# ------------------------------------------------------------------ hats
T["templates/collection.hats.json"] = tpl({
    "head": sec("lg-ap-head", {"eyebrow": "Hats", "heading": "Hats that go with every <em>polo.</em>",
                               "lede": "Five-panel snapbacks with a moisture-wicking sweatband and laser-cut vents. $29 each."}),
    "photos": pband("Lucky hats on the course", ("two-hats-mallet.webp", ""), ("fit-sunset.webp", "object-position:52% center"), ("black-hat-mallet.webp", "")),
    "grid": sec("lg-ap-grid", {"card": "hat", "f_kind": False, "f_stock": False, "f_style": True, "f_color": True, "sort_price": False,
                               "style_lines": "Classic = Gold wordmark\nBetter To Be Lucky = The tagline, on a patch\nUpside Down = LUCKY, upside down\nCursive = Script front",
                               "empty": "Nothing in that combination."},
                ("tile", {"pos": 7, "image": im("fit-sunset.webp"), "eyebrow": "Pairs well with", "title": "A polo to match", "url": C("polos"), "cta": "Shop polos"})),
    "faq": faq("Before you pick", "One size, set it where you like", "Every hat here is the same five-panel snapback underneath. The front is the only thing that changes.", [
        ("Will it fit me?", "<p>It's a snapback, so you set it where you want it and it stays there, whether you wear it high or pulled down.</p>"),
        ("What's in it?", "<p>A moisture-wicking sweatband and laser-cut vents, which you'll notice in July when the group ahead is still looking for a ball.</p>"),
        ("What if I don't like it?", "<p>Send it back within thirty days, unworn with the tags on. A hat that's been out on the course can't go back on the shelf, so decide before you play in it.</p>"),
    ], cols="narrow"),
    "related": related([("Polos", C("polos")), ("Gear", C("gear")), ("Clubs", C("lucky-golf-clubs")), ("All products", C("all-products"))],
                       [("truck", "Free shipping at $198"), ("rotate-ccw", "Thirty days to send it back"), ("tag", "One size, $29")]),
    "signoff": signoff(LUCKY, "One for the bag, one for the car.", "Back to the hats ↑", "#grid"),
})

# ------------------------------------------------------------------ gear
T["templates/collection.gear.json"] = tpl({
    "head": sec("lg-ap-head", {"crumb": "Gear", "eyebrow": "Gear", "heading": "Dress the <em>bag.</em>",
                               "lede": "None of it lowers your handicap. All of it makes the bag look like it belongs to somebody who cares."}),
    "photos": pband("Lucky gear on the course", ("lucky-bag-glove.webp", ""), ("two-hats-mallet.webp", ""), ("putter-in-hand.webp", "")),
    "groups": sec("lg-ap-gear", {"pick": "Pick a size", "sizes_word": "Head Cover = Pick a hand"},
                  ("group", {"anchor": "covers", "jump": "Head covers", "title": "Head covers", "line": "Our clubs ship without one, so this is where the putter gets its jacket.", "collection": "head-covers", "meta": "stock"}),
                  ("group", {"anchor": "grips", "jump": "Grips", "title": "Club grips", "line": "A new grip is the easiest change in golf you can actually feel.", "collection": "performance-x2", "meta": "sizes"}),
                  ("group", {"anchor": "putter-grips", "jump": "Putter grips", "title": "Putter grips", "line": "The stock grip, or oversized for hands that get busy over a short one.", "collection": "putter-grips", "meta": "sizes"}),
                  ("group", {"anchor": "glove", "jump": "Glove", "title": "Glove", "line": "The clover on the back of your hand.", "collection": "gloves", "meta": "stock"})),
    "related": related([("Clubs", C("lucky-golf-clubs")), ("Polos", C("polos")), ("Hats", C("hats")), ("All products", C("all-products"))],
                       [("truck", "Free shipping at $198"), ("rotate-ccw", "Thirty days to send it back"), ("package", "Ships in 1 to 2 business days")]),
    "faq": faq("Before you add it", "Get the fit right", "Quick answers, so nothing ends up on the wrong club.", [
        ("Does a club come with a head cover?", "<p>No. Our clubs ship without one, which is why the covers live here.</p>"),
        ("Will the blade cover fit my putter?", "<p>The blade cover's cut for a blade head and the mallet cover for a mallet. Match the shape of the head, not the brand on it.</p>"),
        ("What size grip do I need?", "<p>The clover grips come in Standard, Midsize and Jumbo, and the bigger ones cost a little more. If you know the size you play, pick that. If you don't, Standard is the safe call.</p>"),
        ("Can I send gear back?", "<p>Thirty days, unused. A grip that's been fitted to a club counts as used, so decide before it goes on the shaft.</p>"),
    ], cols="narrow"),
    "signoff": signoff(LUCKY, "Grip it and rip it.", "Back to the gear ↑", "#covers"),
})

# ------------------------------------------------------------------ clubs
HUD = lambda *xs: "\n".join(f"{a} | {b}" for a, b in xs)
T["templates/collection.clubs.json"] = tpl({
    "head": sec("lg-ap-head", {"crumb": "Clubs", "eyebrow": "Clubs", "heading": "Clubs you'll want to show <em>off.</em>",
                               "lede": "Same materials and machining as the big names, a lot more personality, and every one of them gets sixty days to prove itself.",
                               "rating_products": RATED},
                ("proof", {"value": "1 to 2", "label": "days to ship"}), ("proof", {"value": "[rating]", "label": "from verified buyers", "gold": True}),
                ("proof", {"value": "60", "label": "days to decide"})),
    "photos": pband("Lucky clubs on the course", ("two-gold-wedges.webp", ""), ("from-the-cup.webp", ""), ("lucky-stryker-in-hand.webp", "")),
    "jump": sec("lg-ap-jump", {"label": "Jump to a category"},
                ("link", {"text": "Wedges", "anchor": "wedges", "count": 2}), ("link", {"text": "Putters", "anchor": "putters", "count": 2}),
                ("link", {"text": "Hybrid", "anchor": "hybrid", "count": 1})),
    "wedges": sec("lg-ap-clubs-band", {"anchor": "wedges", "eyebrow": "Wedges", "heading": "Pick your color. The spin comes standard.",
                                       "body": "The Carver 02 in gold or black. Pick your loft, then pick your grind.",
                                       "photo": im("swing-black-wedge.webp"), "photo_pos": "object-position:35% 40%", "style": "big",
                                       "cmp_title": "What the extra ten dollars buys you", "cmp_diff": True, "rating_label": "Rating", "rating_same": "Shared by both"},
                  ("card", {"product": CARVER, "name": "Carver 02 Gold", "tag": "Best seller", "vibe": "Buttery", "line": "Six lofts, two grinds, and a whole lot of shine.",
                            "hud": HUD(("50 to 60°", "Lofts"), ("K · S", "Grinds"), ("RH · LH", "Hand")), "cta": "Pick a loft"}),
                  ("card", {"product": BLACK, "name": "Carver 02 Black", "vibe": "Filthy", "line": "All the spin. None of the spotlight. K grind, six lofts.",
                            "hud": HUD(("50 to 60°", "Lofts"), ("K", "Grind"), ("RH · LH", "Hand")), "cta": "Pick a loft"}),
                  ("row", {"label": "Price", "a": "$99", "b": "$109"}),
                  ("row", {"label": "Who it's for", "a": "Square setups, and anyone who opens the face", "b": "Square setups, same thing every time"}),
                  ("row", {"label": "Finish", "a": "Gold", "b": "Black, gold clover and stamp"}),
                  ("row", {"label": "Lofts", "a": "6 lofts, 50 to 60°", "same": True}),
                  ("row", {"label": "Grinds", "a": "K and S", "b": "K"}),
                  ("row", {"label": "Head", "a": "Forged 1020 carbon steel", "same": True}),
                  ("row", {"label": "Bounce", "a": "8 to 12°, by loft", "same": True})),
    "putters": sec("lg-ap-clubs-band", {"anchor": "putters", "eyebrow": "Putters", "heading": "Blade or mallet? Pick your miss.",
                                        "body": "Both are fully milled, both are gold, and both will make your buddies nervous on the green. The difference is how much help you want on the putts you don't middle.",
                                        "photo": im("putt-sunset.webp"), "photo_pos": "object-position:55% 60%", "style": "big",
                                        "cmp_title": "Thirty dollars apart. Here's where it goes", "cmp_diff": True, "rating_label": "Rating", "rating_same": "Shared by both"},
                   ("card", {"product": BLADE, "name": "Eclipse Blade", "vibe": "Pure", "line": "Planted, fully milled, and all feel.",
                             "hud": HUD(("Blade", "Head"), ("3.5°", "Loft"), ("35″", "Length")), "cta": "Put it in the bag"}),
                   ("card", {"product": MALLET, "name": "Eclipse Mallet", "tag": "In the bag", "vibe": "Smooth", "line": "More head behind the ball for the putts you don't hit perfectly.",
                             "hud": HUD(("Mallet", "Head"), ("3.5°", "Loft"), ("35″", "Length")), "cta": "Put it in the bag"}),
                   ("row", {"label": "Price", "a": "$199", "b": "$229"}),
                   ("row", {"label": "Who it's for", "a": "Golfers who want to feel every putt", "b": "Golfers who want the misses to stay on line"}),
                   ("row", {"label": "Head", "a": "Blade", "b": "Mallet"}),
                   ("row", {"label": "Material", "a": "CNC-milled 431 stainless", "b": "CNC-milled 304 stainless"}),
                   ("row", {"label": "Head weight", "a": "385 g", "b": "365 g"}),
                   ("row", {"label": "Loft", "a": "3.5°", "same": True}),
                   ("row", {"label": "Length", "a": "35″", "same": True})),
    "hybrid": sec("lg-ap-clubs-band", {"anchor": "hybrid", "eyebrow": "Hybrid", "heading": "Long approaches, minus the panic",
                                       "body": "A titanium hybrid in one loft and one flex: 19° and stiff.", "photo": im("walk-off-green.webp"), "style": "big",
                                       "rating_label": ""},
                  ("card", {"product": STRYKER, "name": "Stryker", "vibe": "Flush", "line": "Gets it airborne from lies your long iron can't.",
                            "hud": HUD(("19°", "Loft"), ("Titanium", "Head"), ("RH · LH", "Hand")), "cta": "Fill the gap"}),
                  ("spec", {"b": "19", "small": "°", "label": "Loft"}), ("spec", {"b": "59", "small": "°", "label": "Lie"}),
                  ("spec", {"b": "235", "small": "g", "label": "Head"}), ("spec", {"b": "40.5", "small": "in", "label": "Length"}),
                  ("panel", {"tag": "Instead of a 3-iron", "title": "Easier to get airborne", "text": "In the right hands, a 3-iron and a 19° hybrid go about the same distance. In everybody else's, the hybrid actually gets off the ground."}),
                  ("panel", {"tag": "Instead of a 5-wood", "title": "Easier to keep straight", "text": "Covers the same ground as a 5-wood in a shorter, friendlier club. Easier to find the middle, easier to keep out of the trees."})),
    "reviews": sec("lg-ap-clubs-rev", {"anchor": "reviews", "bg": im("two-hats-mallet.webp"), "bg_pos": "center 65%", "eyebrow": "Reviews",
                                       "heading": "Thousands of golfers bag <em>Lucky</em>", "body": "Straight from people who bought one. Typos included.", "products": RATED},
                   ("review", {"quote": "My buddies already named my club “Goldy” because they are jealous of the results!!", "name": "Eric F.", "product": "Carver 02 Gold", "stars": 5}),
                   ("review", {"quote": "Love the look and feel of this putter. Definitely a head turner walking up to the green with your buddies.", "name": "Kyle K.", "product": "Eclipse Mallet", "stars": 5}),
                   ("review", {"quote": "I'm loving my new hybrid. The gold color is stunning and the performance is unmatched. This club has replaced my sorry 3 wood.", "name": "LB06", "product": "Stryker", "stars": 5})),
    "faq": faq("Still deciding", "Which one's mine?", "If it's still a coin flip after this, write to us and a person answers.", [
        ("Which wedge loft should I start with?", "<p>Keep four to six degrees between your wedges and each one gets its own yardage. Tell us your pitching wedge loft and we'll do the math.</p>"),
        ("K grind or S grind?", "<p>The K is the one you set up square and trust from anywhere, in every loft. The S has a narrower sole, so it opens up clean when you like to lay the face open around the green.</p>"),
        ("Blade or mallet?", "<p>It comes down to the ones you miss. The blade feels planted and tells you exactly where you struck it. The mallet spreads its weight out, so the misses stay closer to your line.</p>"),
        ("What does the hybrid replace?", "<p>It slots in where a 3-iron or a 5-wood would go, and the panels above lay out both.</p>"),
        ("What if it's not the one?", "<p>Every club gets sixty days. Talk to us first: club returns need our OK and a few photos, and the club has to come back in brand-new condition.</p>"),
    ], no_top=False, trust=[("rotate-ccw", "Sixty days to decide on any club"), ("truck", "Ships in 1 to 2 business days"), ("credit-card", "Shop Pay splits it at checkout")]),
    "signoff": signoff("Your bag's missing one of <em>these</em>", "It's better to be lucky.", "Back to the top ↑", "#wedges"),
})

# ------------------------------------------------------------------ polo product
T["templates/product.polo.json"] = tpl({
    "main": sec("lg-ap-polo", {
        "crumb_label": "Polos", "crumb_url": C("polos"), "drop": "Classic Polo, Blade Polo",
        "collar_a_tag": "Classic Polo", "collar_a": "The Classic", "collar_b_tag": "Blade Polo", "collar_b": "The Blade", "eyebrow_tail": " · Polos",
        "swatches": "polos", "all_prints": "See every print side by side",
        "fitnote": "<p><strong>Fit:</strong> athletic, with four-way stretch, so it's more forgiving than the cut suggests. If you wear a large in a performance polo, a large here's right. Between sizes, size up.</p>",
        "stock_in": "In stock · ships in 1 to 2 days", "returns_link": "Thirty days to send it back", "delivery_link": "When will it get here?",
        "ret_eyebrow": "Refund policy", "ret_title": "Thirty days to send it back",
        "ret_body": "<p>Apparel comes back within thirty days of delivery, unworn, unwashed and in original condition with all original tags attached.</p><p>No makeup or deodorant marks, odors, pet hair, stretching or laundering. <strong>A return without its tags has $7 deducted from the refund.</strong></p><p>Requests after thirty days aren't accepted. Clubs get sixty days; apparel doesn't.</p><h4>How the refund works</h4><p>Refunds go out once the item's back and inspected. Return shipping's on you, and original shipping isn't refunded.</p>",
        "del_eyebrow": "Delivery", "del_title": "When it shows up", "carriers": "USPS, UPS, FedEx",
        "del_body": "<p>Orders leave the warehouse in one to two business days. Ground delivery takes a few business days after that, and you get a tracking number as soon as the carrier scans it.</p><p>You'll see what shipping costs, and how fast it is, at checkout before you pay. Orders of $198 or more ship free.</p><h4>Where it ships from</h4><p>Long Beach, California.</p>"},
        ("spec", {"b": "88", "small": "/12", "label": "Poly-spandex"}), ("spec", {"b": "50", "small": "+", "label": "UPF"}),
        ("spec", {"b": "S", "small": "–3XL", "label": "Sizes"}), ("spec", {"b": "4", "small": "way", "label": "Stretch"}),
        ("fq", {"title": "Fabric and care", "open": True, "body": "<ul><li><strong>Fabric</strong> 88% polyester, 12% spandex.</li><li><strong>Stretch</strong> Four-way, so it moves the way your swing does.</li><li><strong>Finish</strong> Moisture-wicking, wrinkle-resistant, and UPF 50+, so the back of your neck makes it to the back nine.</li><li><strong>Care</strong> Machine wash cold. Tumble dry low.</li></ul>"}),
        ("fq", {"title": "Shipping and returns", "body": "<p>Orders leave Long Beach, California in 1 to 2 business days, and the tracking number shows up as soon as the carrier scans it.</p><p>Apparel gets thirty days to come back: unworn, unwashed, tags on. Return shipping's on you.</p>"})),
    "piece": sec("lg-ap-piece", {"eyebrow": "The polo", "heading": "Swing in it. Stay out <em>after.</em>", "tall": True,
                                 "body": "<p>Four-way stretch, so the only thing limiting your backswing is your back. It's an athletic fit in 88/12 poly-spandex, it wicks, it's UPF 50+, and it comes out of the bag looking like it didn't spend the morning in one.</p><p>Every print is the same shirt underneath. Pick the one you want your buddies roasting you about.</p>"}),
    "photos": pband("Lucky polos on the course", ("fit-sunset.webp", "object-position:52% center"), ("green-read-fit.webp", "object-position:60% 40%"), ("walk-off-green.webp", "")),
    "reviews": sec("lg-ap-reviews", {"pool": "polos", "eyebrow": "Reviews", "heading": "[count] reviews",
                                     "line": "Reviews from every Lucky polo. Same fabric and fit, different print."}),
    "more": sec("lg-ap-more", {"layout": "three", "eyebrow": "Wear it with", "heading": "Round out the look", "link_label": "All apparel", "link_url": C("polos")},
                ("product", {"product": "black-its-better-to-be-lucky-patch-hat", "line": "Says it before you do."}),
                ("collar", {"collection": "polos", "tag": "Classic Polo", "line_a": "The classic collar, same shirt underneath.", "line_b": "No buttons, nothing at your throat."}),
                ("product", {"product": "cream-upside-down-hat", "line": "Cream rope hat, made for the loud prints."})),
    "signoff": signoff(LUCKY, "Wear it the day you shoot your best round, or the day you need to look like you did.", "Pick a size →", "#sizes"),
})

# ------------------------------------------------------------------ hat product
T["templates/product.hat.json"] = tpl({
    "main": sec("lg-ap-hat", {"crumb_label": "Hats", "crumb_url": C("hats"), "eyebrow": "Hat · one size",
                              "photo1": im("two-hats-mallet.webp"), "photo1_label": "On the green", "photo2": im("fit-sunset.webp"), "photo2_label": "At sunset",
                              "more_label": "More hats", "swatches": "hats", "more_link": "See them all", "stock_in": "In stock · ships in 1 to 2 days",
                              "l1": "Thirty days to send it back", "l1_url": FAQ_URL + "#returns", "l2": "Free shipping at $198", "l2_url": FAQ_URL + "#shipping"},
                ("tile", {"b": "5", "label": "panels, snapback"}), ("tile", {"b": "One", "label": "size, you set it"}),
                ("tile", {"b": "Wicking", "label": "sweatband"}), ("tile", {"b": "Vents", "label": "laser cut"})),
    "piece": sec("lg-ap-piece", {"eyebrow": "The hat", "heading": "Made for the ninth hole in <em>July.</em>", "tall": False, "image": im("black-hat-mallet.webp"),
                                 "body": "<p>Five panels, a snapback, a sweatband that actually wicks, and vents cut right into it, which you'll appreciate on the back nine. Covers the sunburn and the bad hair day. We won't ask which.</p><p>Every hat is the same underneath. Only the front changes.</p>",
                                 "btn_label": "See every hat", "btn_url": C("hats")}),
    "photos": pband("Lucky hats on the course", ("fit-sunset.webp", "object-position:52% center"), ("two-hats-mallet.webp", ""), ("walk-off-green.webp", "")),
    "more": sec("lg-ap-more", {"layout": "four", "eyebrow": "Wear it with", "heading": "Round out the look", "link_label": "All apparel", "link_url": C("polos")},
                ("others", {"collection": "hats", "count": 3}), ("product", {"product": "azalea-classic-polo"})),
    "signoff": signoff(LUCKY, "One for the bag, one for the car.", "Back to the hats →", C("hats")),
})

# ------------------------------------------------------------------ gear product (covers, grips, the glove)
T["templates/product.gear.json"] = tpl({
    "main": sec("lg-ap-gearp", {"crumb_label": "Gear", "crumb_url": C("gear"),
                                "eyebrows": "Head Cover = Head cover\nGrip = Club grip\nGrips = Putter grip\nGlove = Glove",
                                "labels": "Right = Right hand\nLeft = Left hand\nGlove/Left = Left hand (right-handed golfers)\nGlove/Right = Right hand (left-handed golfers)\nSmall = S\nMedium = M\nLarge = L\nExtra Large = XL",
                                "photo": im("lucky-bag-glove.webp"), "photo_b": im("putter-in-hand.webp"), "photo_b_when": "putter, Head Cover",
                                "stock_in": "In stock · ships in 1 to 2 days", "stock_out": "Sold out in this one",
                                "l1": "Thirty days to send it back", "l1_url": FAQ_URL + "#returns", "l2": "Free shipping at $198", "l2_url": FAQ_URL + "#shipping"}),
    "more": sec("lg-ap-more", {"layout": "four", "eyebrow": "Goes with it", "heading": "Round out the bag", "link_label": "See all the gear", "link_url": C("gear")},
                ("others", {"collection": "head-covers", "count": 2}), ("others", {"collection": "gloves", "count": 1}), ("others", {"collection": "performance-x2", "count": 1})),
    "signoff": signoff(LUCKY, "Grip it and rip it.", "Back to the gear →", C("gear")),
})
