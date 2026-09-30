"""Home (templates/index.json) + the header and footer groups, filled with the
approved v9 copy (v9/src/home.html and build.py's NAV/footer). Imported by build_templates.py."""

def im(name):
    return "shopify://shop_images/lg-" + name


CARVER, BLACK, BLADE, MALLET, STRYKER = ("lucky-golf-lgw02-gold", "lucky-golf-lgw02-black", "signature-gold-putters",
                                         "limited-edition-mallet-putter", "lucky-striker-hybrid-limited-edition")

T = {}

T["templates/index.json"] = {
    "sections": {
        "hero": {"type": "lg-hero", "settings": {
            "image": im("two-gold-wedges.webp"), "focus_x": 42, "focus_y": 55, "focus_mx": 38, "focus_my": 55,
            "eyebrow": "It's better to be lucky", "heading": "Get used to the <em>attention</em>", "heading_tag": "h1",
            "lede": "Big-name performance, finished in gold and shipped straight from us to your bag. Honestly, it's a little unfair.",
            "btn_label": "Shop the clubs", "btn_url": "#families",
            "stamp": "Carver 02 · Gold or black", "stamp_b": "Six lofts · K and S grind"}},
        "trust": {"type": "lg-trust", "settings": {}, "blocks": {
            "t1": {"type": "rating", "settings": {"products": [CARVER, BLACK, BLADE, MALLET, STRYKER], "text": "[avg] stars from [count] verified reviews", "url": "/pages/reviews"}},
            "t2": {"type": "item", "settings": {"icon": "truck", "text": "Free shipping on $198 and up", "url": "/pages/faq-lucky-wedges#shipping"}},
            "t3": {"type": "item", "settings": {"icon": "rotate-ccw", "text": "Sixty days to prove us wrong", "url": "/pages/faq-lucky-wedges#returns"}}},
            "block_order": ["t1", "t2", "t3"]},
        "families": {"type": "lg-cards", "settings": {
            "anchor": "families", "eyebrow": "The clubs", "heading": "Pick your <em>club</em>", "heading_tag": "h2",
            "link_label": "See every club", "link_url": "shopify://collections/lucky-golf-clubs", "cols": "5", "big": True}, "blocks": {
            "c1": {"type": "card", "settings": {"product": CARVER, "line": "Forged, spins like crazy, and your buddies will try to borrow it.", "vibe": "Buttery", "tag": "Best seller", "cut": True}},
            "c2": {"type": "card", "settings": {"product": BLACK, "line": "All the spin. None of the spotlight.", "vibe": "Filthy", "cut": True}},
            "c3": {"type": "card", "settings": {"product": BLADE, "line": "Fully milled, and it tells you where you hit it.", "vibe": "Pure", "cut": True}},
            "c4": {"type": "card", "settings": {"product": MALLET, "line": "Big head, soft face, gold all over.", "vibe": "Smooth", "cut": True}},
            "c5": {"type": "card", "settings": {"product": STRYKER, "line": "Gets it up from lies your 4-iron wants no part of.", "vibe": "Flush", "cut": True}}},
            "block_order": ["c1", "c2", "c3", "c4", "c5"]},
        "feat": {"type": "lg-split", "settings": {
            "image": im("black-hat-mallet.webp"), "flip": True, "feat": True, "no_top": True,
            "eyebrow": "On the green", "heading": "Quiet off the face. Loud in the <em>bag.</em>", "heading_tag": "h2",
            "body": "<p>Catch one off the toe and it still holds its line. Fully milled, soft as anything, and gold all over. Four-footers just got a lot less interesting.</p>",
            "btn_label": "See the Mallet", "btn_url": "shopify://products/" + MALLET,
            "link_label": "Prefer a blade?", "link_url": "shopify://products/" + BLADE, "stamp": "Eclipse Mallet · 304 stainless · $229"}},
        "why": {"type": "lg-claims", "settings": {
            "anchor": "why", "rule": True, "eyebrow": "Priced honestly", "heading": "You're paying for the <em>club.</em> That's it.",
            "lede": "",
            "link_label": "See the side by side", "link_url": "/pages/compare"}, "blocks": {
            "k1": {"type": "claim", "settings": {"title": "Sold direct", "text": "No distributor, no store, nobody in the middle taking a cut. It goes from us to your front door."}},
            "k2": {"type": "claim", "settings": {"title": "No tour contracts", "text": "We don't pay anybody to carry our clubs on TV, so you're not paying for it either."}},
            "k3": {"type": "claim", "settings": {"title": "Where the money goes", "text": "Into the forging, the milling and the gold. The stuff you actually swing."}}},
            "block_order": ["k1", "k2", "k3"]},
        "finder": {"type": "lg-finder", "settings": {
            "anchor": "finder", "no_top": True, "eyebrow": "Club finder", "heading": "Where's the round getting away from <em>you?</em>", "heading_tag": "h2",
            "sub": "", "chips_label": "What to fix",
            "foot_label": "See every club", "foot_url": "#families"}, "blocks": {
            "f1": {"type": "tab", "settings": {"label": "Around the green",
                                                "p1": CARVER, "l1": "Pick the K or the S, depending on how you like to chip.",
                                                "p2": BLACK, "l2": "The K grind, blacked out.", "c2": True}},
            "f2": {"type": "tab", "settings": {"label": "On the green",
                                                "p1": MALLET, "l1": "For anybody done handing back four-footers.",
                                                "p2": BLADE, "l2": "Tells you exactly where you hit it, whether you wanted to know or not."}},
            "f3": {"type": "tab", "settings": {"label": "The long ones",
                                                "p1": STRYKER, "l1": "For the long one that has to end up on the green, not near it."}},
            "f4": {"type": "tab", "settings": {"label": "Just the gold one",
                                                "p1": CARVER, "l1": "Six lofts, two grinds, one very shiny wedge.", "c1": True, "t1": "Best seller",
                                                "p2": MALLET, "l2": "Fully milled and gold. Tap-ins deserve a little drama.", "c2": True}}},
            "block_order": ["f1", "f2", "f3", "f4"]},
        "pband": {"type": "lg-pband", "settings": {"label": "Lucky, out on the course"}, "blocks": {
            "b1": {"type": "photo", "settings": {"image": im("swing-black-wedge.webp"), "pos": "object-position:30% 40%"}},
            "b2": {"type": "photo", "settings": {"image": im("putt-sunset.webp"), "pos": "object-position:55% 60%"}},
            "b3": {"type": "photo", "settings": {"image": im("from-the-cup.webp")}},
            "b4": {"type": "photo", "settings": {"image": im("walk-off-green.webp")}}},
            "block_order": ["b1", "b2", "b3", "b4"]},
        "reviews": {"type": "lg-reviews-band", "settings": {
            "anchor": "reviews", "bg": im("putter-in-hand.webp"), "bg_pos": "center 40%",
            "pull": "You don't even have to take it out of the bag and people ask you about it.", "pull_name": "Michael P.", "pull_product": CARVER, "pull_stars": 5,
            "eyebrow": "Reviews", "heading": "Thousands of golfers bag <em>Lucky</em>",
            "agg_products": [CARVER, BLACK, BLADE, MALLET, STRYKER], "agg_line": "Stars from verified buyers, across every club.",
            "link_label": "Read every review", "link_url": "/pages/reviews"}, "blocks": {
            "r1": {"type": "review", "settings": {"quote": "all of my friends are jealous from the look.And when they stick on the green and come back two feet, there's no doubt their top quality", "name": "Brandon L.", "product": CARVER}},
            "r2": {"type": "review", "settings": {"quote": "People borrow it in my league- it’s a winner!", "name": "Ray O.", "product": CARVER}},
            "r3": {"type": "review", "settings": {"quote": "Amazing Putter and looks awesome", "name": "Arthur V.", "product": MALLET}},
            "r4": {"type": "review", "settings": {"quote": "My buddies already named my club “Goldy” because they are jealous of the results!!", "name": "Eric F.", "product": CARVER}},
            "r5": {"type": "review", "settings": {"quote": "Played 2 rounds and love swinging and hitting a fairway shot. Best club in my bag now", "name": "John L.L.", "product": STRYKER}},
            "r6": {"type": "review", "settings": {"quote": "Here is a checklist about the lucky golf LGW02. -Conversation starter ✔️ -shinny✔️ -good looking ✔️ -good feel ✔️ -good for all levels ✔️ These wedges have it all.", "name": "Carter D.", "product": CARVER}}},
            "block_order": ["r1", "r2", "r3", "r4", "r5", "r6"]},
        "gear": {"type": "lg-gtiles", "settings": {
            "anchor": "gear", "eyebrow": "While you're here", "heading": "Dress for the <em>round</em>", "heading_tag": "h2",
            "foot": "Apparel and gear get thirty days to come back, unworn and unused.", "foot_label": "Shop all gear", "foot_url": "shopify://collections/most-popular"}, "blocks": {
            "g1": {"type": "tile", "settings": {"collection": "polos", "image": im("fit-sunset.webp"), "pos": "object-position:52% center", "count": True,
                                                 "title": "Polos", "text": "Stretchy, UPF 50+, and they don't wrinkle in the bag.", "go": "Shop polos"}},
            "g2": {"type": "tile", "settings": {"collection": "hats", "image": im("two-hats-mallet.webp"), "pos": "object-position:45% center", "count": True,
                                                 "title": "Hats", "text": "Five-panel snapbacks, and at least one matches your polo.", "go": "Shop hats"}}},
            "block_order": ["g1", "g2"]},
        "vp": {"type": "lg-split", "settings": {
            "image": im("green-read-fit.webp"), "pos": "object-position:60% 40%", "flip": False, "text_first": True, "feat": False, "no_top": True,
            "eyebrow": "Why it says Lucky", "heading": "Golf takes a little luck. We put it on the club.", "heading_tag": "h3",
            "body": "<p>The cart-path bounce that somehow ends up on the green. The perfect drive that finds a divot. The putt that lips out and then falls anyway. Everybody who plays has a lucky story or two, and a few unlucky ones they'd rather not talk about. We just figured the club should be in on it.</p>"}},
        "wild": {"type": "lg-wild", "settings": {
            "anchor": "wild", "no_top": True, "eyebrow": "See it in play", "heading": "Caught in the <em>wild</em>",
            "sub": "Stuck one close, holed one out, or rattled the flagstick and stayed on the green? Tag @luckygolfofficial and you might end up here.", "limit": 12,
            "btn_label": "See the whole wall", "btn_url": "/pages/community", "ig": True}},
        "trybe": {"type": "lg-callout", "settings": {
            "anchor": "trybe", "no_top": True, "eyebrow": "Ambassador program", "heading": "You post it. We run it.",
            "body": "We put ad money behind the videos that do well. Ask and your first wedge is free, you earn a share of what your ads sell, and there's no follower minimum.",
            "btn_label": "See how it works", "btn_url": "/pages/become-apart-of-the-team"}},
        "close": {"type": "lg-signoff", "settings": {
            "eyebrow": "The last word", "heading": "<em>Bag</em> it.", "lede": "It's better to be lucky.",
            "btn_label": "Find your club", "btn_url": "#families", "btn2_label": "Read our story", "btn2_url": "/pages/about",
            "trust": "Sixty-day returns\nThousands of golfers\n4.8 stars from verified buyers\nShips in 1 to 2 business days"}},
    },
    "order": ["hero", "trust", "families", "feat", "why", "finder", "pband", "reviews", "gear", "vp", "wild", "trybe", "close"],
}

HB, WG, SB, NS, TC = "black-gold-classic-lucky-hat", "white-gold-classic-hat", "signature-black-classic-polo", "nightshade-classic-polo", "tan-cursive-hat"
COMMUNITY = [
    ("swing-black-wedge.webp", [BLACK, HB, SB]), ("two-gold-wedges.webp", [CARVER]), ("fit-sunset.webp", [NS, WG]),
    ("black-hat-mallet.webp", [MALLET, HB]), ("lucky-stryker-in-hand.webp", [STRYKER]), ("gold-wedge-bag.webp", [CARVER]),
    ("two-hats-mallet.webp", [MALLET, HB, TC]), ("green-read-fit.webp", [NS, WG]), ("putter-in-hand.webp", [BLADE]),
    ("lucky-carver-gold-address.webp", [CARVER]), ("lucky-bag-glove.webp", ["lucky-clover-tour-glove"]),
]
def menu_block(label, title, intro, all_url, all_label, photo, cap, cards, all_line=""):
    s = {"label": label, "title": title, "intro": intro, "all_url": all_url, "all_label": all_label, "all_line": all_line, "photo": im(photo), "photo_caption": cap}
    for i, c in enumerate(cards, 1):
        s.update({f"{k}{i}": v for k, v in c.items()})
    return {"type": "menu", "settings": s}


T["sections/header-group.json"] = {
    "type": "header", "name": "Header group",
    "sections": {
        "bar": {"type": "lg-announcement", "blocks": {
            "a1": {"type": "line", "settings": {"text": "<b>Sixty days</b> to prove us wrong", "url": "/pages/faq-lucky-wedges#returns"}},
            "a2": {"type": "line", "settings": {"text": "Ships in 1 to 2 business days", "url": "/pages/faq-lucky-wedges#shipping"}},
            "a3": {"type": "line", "settings": {"text": "Free shipping at $198", "url": "/pages/faq-lucky-wedges#shipping"}}},
            "block_order": ["a1", "a2", "a3"]},
        "header": {"type": "lg-header", "settings": {
            "m_photo": im("walk-off-green.webp"), "m_photo_line": "It's better to be lucky.", "m_photo_url": "/pages/about", "m_links": "lucky-phone-footer"},
            "blocks": {
                "m1": menu_block("Wedges", "Wedges", "Forged, full of spin, and ready to make your short game everybody else's problem.", "shopify://collections/lucky-golf-clubs", "All clubs",
                                 "two-gold-wedges.webp", "Carver 02 Gold, on the fringe",
                                 [{"p": CARVER, "l": "The one they ask about on the next tee.", "t": "Best seller"}, {"p": BLACK, "l": "Same forged head, in the dark."}], "Every club we make"),
                "m2": menu_block("Putters", "Putters", "Fully milled, finished in gold, and ready to take four-footers personally.", "shopify://collections/lucky-golf-clubs", "All clubs",
                                 "from-the-cup.webp", "Eclipse, doing its job",
                                 [{"p": BLADE, "l": "Fully milled, and it tells you where you hit it."}, {"p": MALLET, "l": "Big head, soft face, gold all over."}], "Every club we make"),
                "m3": menu_block("Hybrid", "Hybrid", "Titanium, 19 degrees, and a lot friendlier than the fairway wood you keep leaving in the bag.", "shopify://collections/lucky-golf-clubs", "All clubs",
                                 "lucky-stryker-in-hand.webp", "Stryker, sitting down",
                                 [{"p": STRYKER, "l": "High and easy from the rough."}], "Every club we make"),
                "m4": menu_block("Apparel", "Apparel", "Polos that move when you swing and hats that say it for you.", "shopify://collections/all-products", "Shop all",
                                 "fit-sunset.webp", "Nightshade polo, white hat",
                                 [{"c": "polos", "n": "Polos", "pr": "$67", "l": "Four-way stretch and UPF 50+, loud or quiet.", "i": im("GoldMirage1.webp")},
                                  {"c": "hats", "n": "Hats", "pr": "$29", "l": "The line on the front does the talking.", "i": im("39.webp")},
                                  {"c": "most-popular", "n": "Gear", "pr": "From $9.95", "l": "Covers, gloves, grips. The small stuff.", "i": im("DriverHeadCover1.webp")}], "Polos, hats and gear"),
                "story": {"type": "link", "settings": {"label": "Our Story", "url": "/pages/about"}},
            },
            "block_order": ["m1", "m2", "m3", "m4", "story"]},
    },
    "order": ["bar", "header"],
}

T["sections/footer-group.json"] = {
    "type": "footer", "name": "Footer group",
    "sections": {
        "footer": {"type": "lg-footer", "settings": {}, "blocks": {
            "f1": {"type": "column", "settings": {"title": "Clubs", "menu": "lucky-footer-clubs"}},
            "f2": {"type": "column", "settings": {"title": "Apparel", "menu": "lucky-footer-apparel"}},
            "f3": {"type": "column", "settings": {"title": "Support", "menu": "lucky-footer-support"}}},
            "block_order": ["f1", "f2", "f3"]},
    },
    "order": ["footer"],
}

T["sections/home-group.json"] = {"type": "custom.home", "name": "Home", "sections": T["templates/index.json"]["sections"], "order": T["templates/index.json"]["order"]}
