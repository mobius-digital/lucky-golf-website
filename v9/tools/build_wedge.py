"""Carver 02 Gold and Carver 02 Black: one page, two finishes.

Cole, 2026-09-20: "thought it was the same page as gold just different colour".
It is. Both come off v9/src/carver.html with the product's own data; what
changes is the photography, the price, the grinds that exist in that finish,
and whether there are reviews yet. Imported by build.py.
"""

GOLD_GAL = [
    ("gold-full-cut.webp", "Carver 02 Gold wedge, full club", "cut", "Forged 1020"),
    ("11_26414fab-14b8-41ae-8ad7-a801c2f646fb.webp", "Carver 02 Gold at the ball", "", ""),
    ("two-gold-wedges.webp", "Two Carver 02 Gold wedges on the fringe", "wide", ""),
    ("4_744b4c6e-a04c-4618-9d58-9a36314000d8.webp", "Carver 02 Gold, milled face detail", "cut", ""),
    ("lucky-carver-gold-address.webp", "Carver 02 Gold at address", "", ""),
    ("gold-wedge-bag.webp", "Carver 02 Gold resting on the bag, the Lucky hat behind", "wide", ""),
]
BLACK_GAL = [
    ("black-cut.webp", "Carver 02 Black wedge, full club", "cut", "Forged 1020"),
    ("lgw01-black-pack.webp", "Carver 02 Black, sole and stamps", "cut", ""),
    ("swing-black-wedge.webp", "Holding the finish with the Carver 02 Black", "wide", ""),
    ("black-full-cut.webp", "Carver 02 Black, face on", "cut", ""),
    ("lucky-golfer-address.webp", "Over the ball with the Carver 02 Black", "", ""),
]

GRINDS_BOTH = '''<!-- ============ THE GRINDS ============ -->
<section class="lg-sec" id="grinds"><div class="lg-wrap">
  <div class="hd two">
    <div><p class="lg-eyebrow">Two grinds</p><h2 class="lg-d2">Two grinds.<br>Zero excuses.</h2></div>
    <p class="lg-body">The K is the one you set up square and trust from anywhere, in every loft. The S has a narrower sole, so it opens up without a fight when you want to get fancy around the green.</p>
  </div>
  <div class="kvs">
    <div class="lg-panel"><span class="lg-tag">K grind</span><h3 class="lg-d3">The one you trust</h3><p>Wide, flat sole and a standard leading edge. Set up square, take your divot, and it does the same thing from the fairway or out of the rough.</p><div class="lg-hud"><span><b>6</b>Lofts</span><span><b>50 to 60°</b>Range</span><span><b>8 to 12°</b>Bounce</span></div></div>
    <div class="lg-panel"><span class="lg-tag">S grind</span><h3 class="lg-d3">Open it up and get fancy</h3><p>Narrower, relieved sole and a reshaped leading edge, so the face opens as far as you like. Tight lies, bunkers, and the flop shot your group will talk about either way.</p><div class="lg-hud"><span><b>3</b>Lofts</span><span><b>52 · 56 · 60°</b>Range</span><span><b>10 to 12°</b>Bounce</span></div></div>
  </div>
</div></section>'''

GRINDS_K = '''<!-- ============ THE GRIND ============ -->
<section class="lg-sec" id="grinds"><div class="lg-wrap">
  <div class="hd two">
    <div><p class="lg-eyebrow">One grind</p><h2 class="lg-d2">One grind. Every loft.<br>No guesswork.</h2></div>
    <p class="lg-body">The black runs on the K grind in all six lofts. Set it up square and it does the same thing every time. Want to lay the face wide open? The S lives on the gold.</p>
  </div>
  <div class="kvs">
    <div class="lg-panel"><span class="lg-tag">K grind</span><h3 class="lg-d3">The one you trust</h3><p>Wide, flat sole and a standard leading edge. Set up square, take your divot, and it does the same thing from the fairway or out of the rough.</p><div class="lg-hud"><span><b>6</b>Lofts</span><span><b>50 to 60°</b>Range</span><span><b>8 to 12°</b>Bounce</span></div></div>
    <a class="lg-panel" href="carver.html" style="text-decoration:none;color:inherit"><span class="lg-tag">S grind</span><h3 class="lg-d3">Open it up and get fancy</h3><p>Narrower sole that opens up clean for tight lies and bunkers. Gold only, in the 52, 56 and 60.</p><span class="lg-link">See the gold <span>&rarr;</span></span></a>
  </div>
</div></section>'''

SPEC_K_TABLE = '''    <div class="tbl" data-spec="K"><table class="lg-table">
      <thead><tr><th>Loft</th><th>50°</th><th>52°</th><th>54°</th><th>56°</th><th>58°</th><th>60°</th></tr></thead>
      <tbody>
      <tr><th scope="row">Bounce</th><td>8°</td><td>8°</td><td>12°</td><td>12°</td><td>10°</td><td>10°</td></tr>
      <tr><th scope="row">Lie</th><td>63°</td><td>63°</td><td>63°</td><td>63°</td><td>63°</td><td>63°</td></tr>
      <tr><th scope="row">Length</th><td>35.25&Prime;</td><td>35.25&Prime;</td><td>35.125&Prime;</td><td>35.125&Prime;</td><td>35&Prime;</td><td>35&Prime;</td></tr>
      <tr><th scope="row">Head weight</th><td>300 g</td><td>300 g</td><td>300 g</td><td>300 g</td><td>300 g</td><td>300 g</td></tr>
      <tr><th scope="row">Head</th><td colspan="6">1020 forged carbon steel · CNC milled grooves and micro grooves over a sandblasted face</td></tr>
      </tbody></table></div>'''

SPEC_S_TABLE = '''    <div class="tbl" data-spec="S" hidden><table class="lg-table">
      <thead><tr><th>Loft</th><th>52°</th><th>56°</th><th>60°</th></tr></thead>
      <tbody>
      <tr><th scope="row">Bounce</th><td>10°</td><td>12°</td><td>12°</td></tr>
      <tr><th scope="row">Lie</th><td>63.5°</td><td>64°</td><td>64°</td></tr>
      <tr><th scope="row">Length</th><td>35.25&Prime;</td><td>35.125&Prime;</td><td>35&Prime;</td></tr>
      <tr><th scope="row">Head weight</th><td>300 g</td><td>300 g</td><td>300 g</td></tr>
      <tr><th scope="row">Head</th><td colspan="3">1020 forged carbon steel · CNC milled grooves and micro grooves over a sandblasted face</td></tr>
      </tbody></table></div>
    <p class="note">The S reads more bounce on paper than the K and plays with less, because the narrower sole puts less of itself on the turf.</p>'''

TABS = '''  <div class="seg specs-tabs" data-spectabs role="tablist"><button class="lg-chip" type="button" data-tab="clubs" aria-pressed="true">Clubs</button><button class="lg-chip" type="button" data-tab="shafts" aria-pressed="false">Shafts</button><button class="lg-chip" type="button" data-tab="grips" aria-pressed="false">Grips</button></div>
  <div data-spectab="clubs">
{BAR}
{TABLES}
  </div>
'''

BAR_BOTH = '''    <div class="tbar"><div class="seg" data-specseg role="group" aria-label="Grind"><button class="lg-chip" type="button" data-g="K" aria-pressed="true">K grind · 6 lofts</button><button class="lg-chip" type="button" data-g="S" aria-pressed="false">S grind · 3 lofts</button></div><span class="lg-meta">Right and left hand</span></div>'''
BAR_K = '''    <div class="tbar"><span class="lg-label">K grind · six lofts</span><span class="lg-meta">Right hand</span></div>'''

REVIEWS_GOLD = '''<!-- ============ REVIEWS: review proximity + the real quotes ============ -->
<section class="lg-sec" id="reviews"><div class="lg-wrap">
  <div class="rv-top">
    <div><p class="lg-eyebrow">Reviews</p><h2 class="lg-d2">Straight from the people hitting it</h2>
      <p class="lg-body">Every review takes a shot at the pin.</p>
      <button class="lg-btn-line lg-btn-sm" type="button" data-md-open="md-write">Write a review</button></div>
    <div id="prox"></div>
  </div>
  <div class="qs">
    <figure class="lg-quote"><span class="lg-stars" aria-label="5 out of 5">{{STARS5}}</span><b>So nice, I bought it twice!</b><blockquote>&ldquo;I bought myself a 60 degree last year. I love it so much, and get so many comments/compliments on the look… but the performance speaks even louder!&rdquo;</blockquote><figcaption>JD M. · <span class="lg-stock">Verified buyer</span></figcaption></figure>
    <figure class="lg-quote"><span class="lg-stars" aria-label="5 out of 5">{{STARS5}}</span><b>LGW01</b><blockquote>&ldquo;Super great club, love the feel, the sound, the spin, only problem I have is getting under the ball with it but easy fix none the less. Great club!!&rdquo;</blockquote><figcaption>James B. · <span class="lg-stock">Verified buyer</span></figcaption></figure>
    <figure class="lg-quote"><span class="lg-stars" aria-label="5 out of 5">{{STARS5}}</span><b>Hard to keep it!</b><blockquote>&ldquo;People borrow it in my league- it’s a winner!&rdquo;</blockquote><figcaption>Ray O. · <span class="lg-stock">Verified buyer</span></figcaption></figure>
  </div>
  <button class="readall" type="button" data-readall aria-expanded="false" aria-controls="jm"><b>Read every review</b><span>Newest first, grumpy ones included.</span><i aria-hidden="true">+</i></button>
  <div class="jm" id="jm" hidden>
    <div class="jm-bar"><div class="lg-chips" id="jm-filters" role="group" aria-label="Filter reviews by rating"></div>
      <label><span class="sr">Sort reviews</span><select id="jm-sort"><option value="recent">Most recent</option><option value="high">Highest rating</option><option value="low">Lowest rating</option></select></label></div>
    <p class="jm-count" id="jm-count"></p>
    <div id="jm-list"></div>
    <div class="jm-more"><button class="lg-btn-line lg-btn-sm" type="button" id="jm-more">Show more reviews</button></div>
  </div>
</div></section>'''

REVIEWS_BLACK = REVIEWS_GOLD.replace(
    '<p class="lg-body">Every review takes a shot at the pin.</p>',
    '<p class="lg-body">These reviews cover the Carver 02 in both finishes. Same forged head, same face, different coat.</p>')


CARD_GOLD = '<a class="lg-card" href="carver.html"><span class="lg-card-ph is-cut"><img src="img/gold-full-cut.webp" alt="" loading="lazy"></span><span class="lg-card-bd"><span class="lg-card-nm">Carver 02 Gold</span><span class="lg-card-pr">$99</span><span class="lg-card-ln">Same forged head, in gold</span></span></a>'
CARD_BLACK = '<a class="lg-card" href="black.html"><span class="lg-card-ph is-cut"><img src="img/black-full-cut.webp" alt="" loading="lazy"></span><span class="lg-card-bd"><span class="lg-card-nm">Carver 02 Black</span><span class="lg-card-pr">$109</span><span class="lg-card-ln">Same forged head, in the dark</span></span></a>'


def gallery(items):
    gal = ""
    for src, alt, cls, tag in items:
        gal += (f'      <figure class="{cls}" data-zoom="img/{src}"><img src="img/{src}" alt="{alt}" loading="lazy">'
                + (f'<span class="lg-tag">{tag}</span>' if tag else "") + "</figure>\n")
    return gal, "<i></i>" * len(items)


def build(SRC, fill, js, product, reviews, REEL, stars5, finish, mood=False):
    import os
    gold = finish == "gold"
    pd = product("lgw01-gold" if gold else "lgw01-black")
    keep = {k: pd[k] for k in ("id", "title", "price", "options", "variants", "default")}
    keep["title"] = "Carver 02 Gold" if gold else "Carver 02 Black"
    keep["img"] = "img/gold-full-cut.webp" if gold else "img/black-cut.webp"
    gal, dots = gallery(GOLD_GAL if gold else BLACK_GAL)
    t = {
        # the page keeps gold on white; the metal lives on the dark finish band
        "METAL": "",
        "TITLE": keep["title"],
        "PRICE": pd["priceLabel"],
        "GAL": gal, "DOTS": dots,
        "FIN_G": ' aria-current="page"' if gold else "",
        "FIN_B": "" if gold else ' aria-current="page"',
        "RVL": ('<div class="rvl"><span class="lg-stars" aria-label="4.8 out of 5">{{STARS5}}</span>'
                '<a href="#reviews">&ldquo;So nice, I bought it twice.&rdquo; JD M. · read them all</a></div>'),
        "DESC": ("Fair warning: this thing spins, so your first few chips might stop shorter than you're used to. "
                 "It's forged, so it feels buttery off the face, and it's forgiving enough that the mishits still behave. "
                 "The micro-grooves and sandblasted face are doing the work. And yes, it's gold. People will ask."
                 if gold else
                 # the two approved descriptions, verbatim from How We Write v10 (2026-09-23)
                 "Forged in darkness, lives in the shadows, and nobody sees it coming until it checks up by the pin. "
                 "The black Carver is built for the player who wants consistency and craftsmanship without announcing it "
                 "the second it comes out of the bag. With a forged head and a micro-grooved, sandblasted face, the "
                 "Carver 02 Black delivers serious spin and a consistent feel shot after shot."),
        "DETAILS": ("A forged 1020 carbon steel head with CNC-milled grooves on a micro-grooved, sandblasted "
                    "face, which is the dual-texture face that makes it spin like it does. The K grind comes in all six "
                    "lofts and the S in the 52, 56 and 60."
                    if gold else
                    "The same forged 1020 carbon steel head and dual-texture face as the gold, finished in black with "
                    "gold accents. The K grind, in all six lofts."),
        "FILM_H": "Watch it bite." if gold else "They'll notice when it stops.",
        "FILM_B": ("Chip it off a tight lie or splash it out of the bunker and the "
                   + ("Carver" if gold else "black Carver")
                   + " grabs the ball either way. The micro-grooved, sandblasted face keeps spinning when the "
                   "lie's wet and when you don't find the middle, and the forged 1020 head feels soft and solid "
                   "the whole way through. You'll know how you hit it before you look up."),
        "GRINDS": GRINDS_BOTH if gold else GRINDS_K,
        # mood=True is the demo: the finish world becomes one dark beat, where a
        # finish's own metal finally reads as metal instead of as grey type
        "FINISHES": open(os.path.join(SRC, "finishes-mood.html" if mood else "finishes-white.html"),
                         encoding="utf-8").read(),
        "MOOD": "gold" if gold else "black",
        "SEG_G": "true" if gold else "false", "SEG_B": "false" if gold else "true",
        "MH_G": "" if gold else " hidden", "MH_B": " hidden" if gold else "",
        "MON_LABEL": ("Carver 02 Gold · LGW02" if gold else "Carver 02 Black · LGW02"),
        "MON_IMG": "gold-full-cut.webp" if gold else "black-cut.webp",
        "MON_GRINDS": ('<div class="lg-mt"><span>Grinds</span><b>2</b><div class="lg-vals"><i>K · every loft</i><i>S · 52 56 60</i></div></div>'
                       if gold else
                       '<div class="lg-mt"><span>Grind</span><b>K</b><div class="lg-vals"><i>Every loft</i></div></div>'),
        "SPECTABS": TABS.format(BAR=BAR_BOTH if gold else BAR_K,
                                TABLES=(SPEC_K_TABLE + "\n" + SPEC_S_TABLE) if gold else SPEC_K_TABLE),
        "REVIEWS": REVIEWS_GOLD if gold else REVIEWS_BLACK,
        "OTHER_FIN": CARD_BLACK if gold else CARD_GOLD,
        "SIGN": ("Nobody needs a gold wedge. You'll want one anyway." if gold else
                 "Black on the outside. Gold where it counts."),
        "PD_JSON": js(keep),
        "REVIEWS_JSON": js(reviews("lgw01-gold")),   # one wedge, one pool of reviews
        "REEL_JSON": js(REEL),
    }
    for k in ("RVL", "REVIEWS"):
        t[k] = t[k].replace("{{STARS5}}", stars5)
    return fill(open(os.path.join(SRC, "carver.html"), encoding="utf-8").read(), t)
