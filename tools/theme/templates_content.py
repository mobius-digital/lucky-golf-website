"""Content page templates (group 70), filled with the approved v9 copy verbatim
(v9/src/{story,faq,trybe,compare,contact,community,reviews,404,search}.html).
Imported by build_templates.py."""


def im(name):
    return "shopify://shop_images/lg-" + name


def order(d):
    """Give a sections/blocks dict its order key."""
    return list(d.keys())


def blocks(items):
    b = {f"b{i + 1}": x for i, x in enumerate(items)}
    return {"blocks": b, "block_order": order(b)}


def signoff(heading, lede, btn=None, btn_url=None, line=None, line_url=None, arrow=True):
    s = {"eyebrow": "The last word", "heading": heading, "lede": lede}
    if btn and not arrow:
        s["btn_arrow"] = False
    if btn:
        s.update(btn_label=btn, btn_url=btn_url)
    if line:
        s.update(btn2_label=line, btn2_url=line_url)
    return {"type": "lg-signoff", "settings": s}


def page(sections):
    return {"sections": sections, "order": order(sections)}


CARVER, BLACK, BLADE, MALLET, STRYKER = ("lucky-golf-lgw02-gold", "lucky-golf-lgw02-black", "signature-gold-putters",
                                         "limited-edition-mallet-putter", "lucky-striker-hybrid-limited-edition")
CLUBS = "shopify://collections/lucky-golf-clubs"
FAQ, TRYBE, CONTACT, REVIEWS = ("shopify://pages/faq-lucky-wedges", "shopify://pages/become-apart-of-the-team",
                                "shopify://pages/contact-us", "shopify://pages/reviews")
COMPARE = "/pages/compare"
APPLY = "https://creators.luckygolf.com/apply"
QUOTE_LUCKY = "“It's better to be <em>lucky.</em>”"

T = {}

# ------------------------------------------------------------------ Our story  (/pages/about)
T["templates/page.story.json"] = page({
    "hero": {"type": "lg-hero", "settings": {
        "image": im("two-gold-wedges.webp"), "focus_x": 46, "focus_y": 52, "focus_mx": 44, "focus_my": 52,
        "eyebrow": "Our story", "heading": "Golf has a dress code. Ours is <em>gold</em>", "heading_tag": "h1",
        "lede": "Clubs nobody mistakes for anyone else's."}},
    "man": {"type": "lg-man", "settings": {
        "heading": "Luck favors <em>the bold</em>",
        "body": "<p>Golf's the best game there is, and it should feel that way whether it's your first round or your five hundredth. Somewhere along the way it got stiff and way too expensive. We're here to loosen it up.</p>"
                "<p>That starts with clubs that forgive the swings you're still working on, cost what they should, and look like nothing else in the bag.</p>"
                "<p>Nobody here cares about your handicap or whether your polo's tucked in. Show up, swing hard, talk a little trash.</p>"
                "<p>And when the chip drops and somebody asks what you're hitting, tell them it's your lucky wedge. Whether it was luck is your business.</p>",
        "close": "It's better to be lucky."}},
    "parts": {"type": "lg-parts", "settings": {"no_top": True}, **blocks([
        {"type": "part", "settings": {"image": im("lucky-golfer-address.webp"), "eyebrow": "Why we exist",
                                      "heading": "Great clubs got too expensive. We took it <em>personally</em>",
                                      "text": "The big names sponsor a tour pro and add it to your price. We skipped that part, so you get the same materials and none of the markup.",
                                      "link_label": "See the clubs", "link_url": CLUBS}},
        {"type": "part", "settings": {"image": im("lucky-wedge-face-macro.webp"), "eyebrow": "What we do",
                                      "heading": "Same steel as the big names. Different <em>math</em>",
                                      "text": "Every club gets sixty days to make up your mind, and if it doesn't earn its spot in the bag, send it back.",
                                      "link_label": "See the breakdown", "link_url": COMPARE}},
        {"type": "part", "settings": {"image": im("lucky-bag-glove.webp"), "eyebrow": "Our story",
                                      "heading": "We built the clubs we <em>wanted</em>",
                                      "text": "In 2018 we made one gold wedge, built right and priced honestly. It hit.",
                                      "link_label": "Start with the wedge", "link_url": "shopify://products/" + CARVER}}])},
    "gold": {"type": "lg-photo-band", "settings": {
        "bg": im("putt-sunset.webp"), "bg_pos": "center 60%", "eyebrow": "The gold question",
        "heading": "Gold, on <em>purpose.</em>", "lede": "You only get so many Saturdays, and none of them should be spent blending in."}},
    "timeline": {"type": "lg-timeline", "settings": {
        "eyebrow": "2018 to now", "heading": "How a gold wedge turned into all <em>this</em>",
        "lede": "It started with one gold wedge and escalated from there."}, **blocks([
        {"type": "moment", "settings": {"year": y, "title": t, "text": x, "soon": soon}} for y, t, x, soon in [
            ("2018", "The gold wedge", "One wedge, in gold. Lucky starts here.", False),
            ("2019", "The Blade putter", "Fully milled, and quiet off the face. Turns out people wanted more than a wedge.", False),
            ("2020", "Wedges, version two", "The original, refined and re-released. The gold wedge wasn't a fluke.", False),
            ("2023", "The Mallet putter", "Bigger head, fewer excuses on the greens.", False),
            ("2024", "The hybrid", "Titanium with a flex-channel face, for the gap your long irons never covered.", False),
            ("July 2025", "Somebody hit the gas", "Lucky changed hands. Nothing happened to the clubs or the prices. Everything happened to the calendar.", False),
            ("May 2026", "The polos drop", "The clubs got a wardrobe. Same rule: look good, priced fair.", False),
            ("July 2026", "Hats land", "Ten ways to keep the sun off while you take someone's money.", False),
            ("July 2026", "The Patriot putter", "A limited run for America's 250th. Gone when it's gone.", False),
            ("2026", "Nine of us now", "Nine people where there used to be a lot fewer. That's what shipping this much at once actually takes.", False),
            ("Sept 2026", "First accessories drop", "Towels, divot tools, new headcovers. The little stuff, done right.", True),
            ("Late 2026", "KBS shafts", "A name shaft across the line, for everyone who has opinions about shafts.", True),
            ("Late 2026", "Irons and drivers", "The big sticks arrive. Years of asking, answered.", True),
            ("2027", "Just getting started", "Partnerships, and a few drops we're not allowed to describe yet.", True)]])},
    "photos": {"type": "lg-pband", "settings": {"label": "Lucky on the course"}, **blocks([
        {"type": "photo", "settings": {"image": im("from-the-cup.webp")}},
        {"type": "photo", "settings": {"image": im("lucky-bag-glove.webp")}},
        {"type": "photo", "settings": {"image": im("walk-off-green.webp")}}])},
    "next": {"type": "lg-cols", "settings": {"style": "links", "eyebrow": "Keep looking", "heading": "The rest of <em>it</em>"}, **blocks([
        {"type": "item", "settings": {"title": "The clubs", "text": "Every club we make, starting at $99.", "url": CLUBS, "go": "See every club"}},
        {"type": "item", "settings": {"title": "Ambassador program", "text": "Post about Lucky and we put ad money behind your videos. No follower minimum.", "url": TRYBE, "go": "How it works"}},
        {"type": "item", "settings": {"title": "Questions", "text": "Shipping, returns, what happens if the fit's wrong, and how the sixty days work.", "url": FAQ, "go": "Read the answers"}}])},
    "signoff": signoff(QUOTE_LUCKY, "Tell them where you got it.", "See the clubs", CLUBS, arrow=False),
})

# ------------------------------------------------------------------ Questions  (/pages/faq-lucky-wedges)
FAQ_TOPICS = [
    ("shipping", "Shipping", "Out the door in a day or <em>two</em>", "Faster than your buddy pays up on a bet.", [
        ("When does my order ship?", "In one to two business days, and you'll get tracking as soon as the carrier scans it."),
        ("When is shipping free?", "At $198. That's two wedges, if you were looking for an excuse."),
        ("Can I change the address?", "If it hasn't shipped, yes. Email us the order number and the right address and we'll catch it. Once it's with the carrier it's out of our hands.")]),
    ("returns", "Returns", "Sixty days on clubs, thirty on the <em>rest</em>", "Sixty days to make up your mind, with a few conditions so the club can go back on the shelf.", [
        ("How does the sixty-day club return work?", "Start it with us before you send anything back: club returns need approval and a couple of photos first, and the refund goes out after the club is back with us and inspected. Return shipping is on you, and the original shipping fee isn't refunded."),
        ("Can I actually hit it?", "Yes, with one condition per club type. A putter can be rolled during the sixty days and has to come back with no face marks, sole wear, scratches, dents, chips, bag chatter or grip wear. With wedges, one wedge in the set can be opened and tested on a turf mat or another non-abrasive surface, with no groove wear or face marks, and the rest stay factory sealed. Regripping, bending or cutting a club ends the return."),
        ("What about a polo or a hat?", "Thirty days. Apparel comes back unworn and unwashed with the original tags on: no stains, odors, pet hair or stretching. Tags missing costs $7 off the refund. Gear and accessories come back unused inside the same thirty days."),
        ("What can't come back?", "Anything customized is final sale unless it turns up defective. Beyond that: visible wear or damage past the conditions above, modified clubs, anything outside its window, and anything sent back without approval."),
        ("Something arrived damaged.", "Email us a photo the day it lands. Defective items get a replacement or a refund once we've taken a look.")]),
    ("clubs|Clubs", "The clubs", "Which one you actually <em>need</em>", "No salesperson standing over you. Here's the short version.", [
        ("Which wedge should I start with?", "Whatever gap hurts most. If you're carrying a pitching wedge and nothing else, a 56 covers the most ground in one club. If you already have a sand wedge, a 60 gives you the shot over the bunker that a 56 can't hold."),
        ("Gold or black?", "Same wedge underneath. The black runs ten dollars more because of the finish, and it's the quieter one at address. Pick the one you want to look down at."),
        ("Blade or mallet putter?", "It comes down to the ones you miss. The blade feels planted and tells you exactly where you struck it. The mallet spreads its weight out, so the misses stay closer to your line."),
        ("Are these actually as good as the big names?", "Same materials and the same engineering as the big names, without a tour contract or a retail shelf built into the price. You've got sixty days to make up your mind.")]),
    ("apparel", "Apparel", "Sizing and <em>fabric</em>", "", [
        ("How do the polos fit?", "It's an athletic fit, so it sits closer than a boxy golf polo, and the four-way stretch keeps it out of the way of your swing. If you wear a large in a performance polo, a large here's right. Between sizes, size up."),
        ("What are they made of?", "88% polyester and 12% spandex, with four-way stretch. Moisture-wicking, wrinkle-resistant and UPF 50+. Machine wash cold, tumble dry low."),
        ("Classic collar or Blade?", "The Blade drops the buttons and the placket, so there's nothing at your throat to sit crooked by the ninth. Everything under the collar is identical."),
        ("Do the hats come in sizes?", "One size, five-panel snapback, so you set it where you like it. Every one has a moisture-wicking sweatband and laser-cut vents.")]),
    ("orders", "Orders", "After you hit <em>buy</em>", "A confirmation, a tracking number and a box. That's the whole show.", [
        ("Can I change or cancel an order?", "If it hasn't shipped, email us straight away with the order number. Once the carrier has it, treat it as a return."),
        ("Where's my tracking?", "It goes to the email on the order as soon as the label is made. If it isn't there, check the spam folder, then email us and we'll resend it."),
        ("Do you restock sold-out lofts and sizes?", "Yes. Tap the sold-out chip on the product page and we'll email you when that one is back. We don't email you about anything else."),
        ("Do you take returns on a gift?", "Same windows, same conditions, and we'll deal with whoever contacts us. You don't need the buyer standing there.")]),
]


def faq_blocks(topics):
    out = []
    for anchor, eyebrow, heading, text, qs in topics:
        anchor, _, jump = anchor.partition("|")
        out.append({"type": "topic", "settings": {"anchor": anchor, "jump_label": jump, "eyebrow": eyebrow, "heading": heading, "text": text}})
        for i, (q, a) in enumerate(qs):
            out.append({"type": "q", "settings": {"question": q, "answer": f"<p>{a}</p>", "open": i == 0}})
    return blocks(out)


T["templates/page.faq.json"] = page({
    "faq": {"type": "lg-faq-page", "settings": {
        "crumb": "Questions", "eyebrow": "Ask away", "heading": "Questions, answered <em>straight</em>",
        "lede": "Shipping, returns, sizing and what actually happens if a club doesn't earn its spot in the bag. If it isn't here, a person reads the email.",
        "jump": True, "jump_extra_label": "Still stuck", "jump_extra_url": "#contact", "jsonld": True}, **faq_blocks(FAQ_TOPICS)},
    "help": {"type": "lg-cols", "settings": {"anchor": "contact", "no_top": True, "style": "icons", "eyebrow": "Still stuck",
                                             "heading": "Three ways to get a <em>person</em>"}, **blocks([
        {"type": "item", "settings": {"icon": "mail", "title": "Email us", "text": "support@luckygolf.com. A person reads every one.", "url": CONTACT}},
        {"type": "item", "settings": {"icon": "message-circle", "title": "Chat", "text": "Bottom right of any page. Good for a quick sizing or loft question.", "url": CONTACT}},
        {"type": "item", "settings": {"icon": "package", "title": "Start a return", "text": "Apparel and gear go through the returns portal. Clubs need a quick approval first.", "url": CONTACT}}])},
    "signoff": signoff(QUOTE_LUCKY, "Worst case, it comes back. Sixty days on clubs, thirty on apparel.", "See the clubs", CLUBS, arrow=False),
})

# ------------------------------------------------------------------ Ambassador program  (/pages/become-apart-of-the-team)
T["templates/page.ambassadors.json"] = page({
    "hero": {"type": "lg-hero-plus", "settings": {
        "image": im("green-read-fit.webp"), "focus_x": 50, "focus_y": 45, "focus_mx": 46, "focus_my": 48, "short": False,
        "eyebrow": "Ambassador program", "heading": "You post it. We put ad money behind <em>it.</em>",
        "lede": "No follower minimum, no scripts, and nobody gets paid to say a club is good. You post the videos, and we put ad money behind the best ones."}, **blocks([
        {"type": "button", "settings": {"label": "Apply now", "url": APPLY, "gold": True, "new_tab": True}}])},
    "gets": {"type": "lg-cols", "settings": {"style": "icons", "eyebrow": "What you get", "heading": "Three things, and none of them are a <em>discount code</em>"}, **blocks([
        {"type": "item", "settings": {"icon": "hand-coins", "title": "A free wedge, then the bag", "text": "Your first wedge is free when you ask. Post every month and a new club opens up each month."}},
        {"type": "item", "settings": {"icon": "send", "title": "Your videos, run as ads", "text": "We put real ad money behind the best ones, from your handle, and you get a share of what they sell. Your link pays 10% on top."}},
        {"type": "item", "settings": {"icon": "star", "title": "The Clubhouse", "text": "A leaderboard, weekly races anyone can win, and Charms for posting that turn into hats and polos."}}])},
    "ask": {"type": "lg-ask", "settings": {
        "no_top": True, "eyebrow": "What we ask", "heading": "Tell us the truth, including when it's not <em>flattering</em>",
        "body": "We pay for sales, never for reviews. Nobody gets paid to say a club is good.",
        "after": "We read every application and answer either way.",
        "p_eyebrow": "Apply", "p_title": "About two minutes",
        "p_text": "Linking your best posts gets you a faster yes. Ads can only run from Instagram, so that's the handle worth giving us.",
        "btn_label": "Apply now", "btn_url": APPLY, "new_tab": True}, **blocks([
        {"type": "item", "settings": {"text": "Film with your Lucky clubs: range sessions, real rounds, honest reactions."}},
        {"type": "item", "settings": {"text": "Post it as an Instagram Reel and tag @luckygolfofficial. Post it everywhere else too, but the Reel is the one we can run as an ad."}},
        {"type": "item", "settings": {"text": "Say it's a partnership. Every post with our gear gets a clear disclosure, paid or not."}}])},
    "photos": {"type": "lg-pband", "settings": {"label": "Lucky on the course"}, **blocks([
        {"type": "photo", "settings": {"image": im("fit-sunset.webp"), "pos": "object-position:52% center"}},
        {"type": "photo", "settings": {"image": im("swing-black-wedge.webp")}},
        {"type": "photo", "settings": {"image": im("walk-off-green.webp")}}])},
    "faq": {"type": "lg-faq-page", "settings": {"jump": False, "even": True, "jsonld": True}, **faq_blocks([
        ("", "Before you ask", "Stuff people always <em>ask</em>", "", [
            ("How many followers do I need?", "None, on any platform."),
            ("Do I get paid?", "Yes, for sales. When an ad we run from your video sells, you earn a share, and your rate climbs as your ads sell more. Your link pays 10% on anything bought through it."),
            ("Do I have to post?", "To earn, yes. Clubs come from posting every month, and ad money comes from videos we can run. No quota beyond that, and no script."),
            ("Can I work with other brands?", "Yes. We don't ask you to stop."),
            ("Does applying sign me up for anything?", "No. If you're accepted, you'll agree to the terms and privacy policy before anything else happens.")])])},
    "signoff": signoff(QUOTE_LUCKY, "Post it, and we'll put money behind it.", "Apply now", APPLY),
})

# ------------------------------------------------------------------ Lucky vs the big names  (/pages/compare, new)
T["templates/page.compare.json"] = page({
    "hero": {"type": "lg-hero", "settings": {
        "image": im("two-gold-wedges.webp"), "focus_x": 50, "focus_y": 50, "focus_mx": 50, "focus_my": 50,
        "eyebrow": "Lucky vs the big names", "heading": "Why do big-name wedges cost what they <em>do?</em>", "heading_tag": "h1",
        "lede": "Most of it isn't the wedge. It's the tour contract, the shop that stocks it, and everybody in between.",
        "btn_label": "See the clubs", "btn_url": CLUBS, "btn2_label": "See the breakdown ↓", "btn2_url": "#breakdown"}},
    "proof": {"type": "lg-proof", "settings": {"product": CARVER, "rating_line": "[rating] from [count] Carver reviews"}, **blocks([
        {"type": "item", "settings": {"text": "Sixty days on every club"}},
        {"type": "item", "settings": {"text": "Sold direct, no shop markup"}}])},
    "wedge": {"type": "lg-cmp-cards", "settings": {"eyebrow": "The wedge", "heading": "$99 for gold. $109 for <em>black.</em>"}, **blocks([
        {"type": "card", "settings": {"product": CARVER, "image": im("gold-full-cut.webp"), "tag": "Best seller", "line": "Forged, gold, and a face that grabs the ball like it owes it money.", "btn_label": "Pick a loft"}},
        {"type": "card", "settings": {"product": BLACK, "image": im("black-cut.webp"), "line": "The same forged head, blacked out, with the gold clover left on.", "btn_label": "Pick a loft"}}])},
    "table": {"type": "lg-table", "settings": {
        "anchor": "breakdown", "no_top": True, "eyebrow": "The breakdown", "heading": "Their wedge next to <em>ours.</em>",
        "sub": "We're not naming names, because this isn't about one company. It's how the whole shelf is priced.",
        "col0": "What we compared", "col_them": "The big names", "col_us": "Lucky",
        "after": "Look at the head and the face. Those are the parts that hit the ball, and they're not where the markup goes."}, **blocks([
        {"type": "row", "settings": {"label": a, "them": b, "us": c}} for a, b, c in [
            ("One wedge, new", "$170 to $200", "$99 to $109"),
            ("Wedge head", "Carbon steel, cast or forged by model", "Forged 1020 carbon steel"),
            ("Wedge face", "Milled grooves", "CNC-milled grooves and a micro-grooved face"),
            ("Sole grinds", "Several, by model", "K and S on gold, K on black"),
            ("Where you buy it", "Golf shops and online", "Online, direct from us"),
            ("Trying it", "A few swings in the shop", "Sixty days, and you can hit one on a mat")]])},
    "goes": {"type": "lg-cols", "settings": {"style": "numbers", "no_top": True, "eyebrow": "So where does it go", "heading": "Where the extra money <em>goes.</em>",
                                             "after": "We don't have any of those, so none of it got added in the first place. It's not a sale. There's just less in there."}, **blocks([
        {"type": "item", "settings": {"title": "The tour contract", "text": "Somebody's getting paid to have that wedge in the bag on Sunday. That money's in the price you pay."}},
        {"type": "item", "settings": {"title": "The shop", "text": "Floor space, staff and rent, in a building you've got to drive to, and the club's carrying all of it."}},
        {"type": "item", "settings": {"title": "Everybody in between", "text": "A distributor sits between the factory and the shop, and takes a cut on the way past."}}])},
    "net": {"type": "lg-cols", "settings": {"style": "rules", "no_top": True, "eyebrow": "Don't take our word for it", "heading": "Check it <em>yourself.</em>",
                                            "after_link_label": "Read the return policy", "after_link_url": "/policies/refund-policy"}, **blocks([
        {"type": "item", "settings": {"title": "Sixty days on clubs", "text": "Hit one on a mat. Not feeling it? Send it back."}},
        {"type": "item", "settings": {"title": "Ships in 1 to 2 days", "text": "Tracking shows up as soon as the carrier scans it."}},
        {"type": "item", "settings": {"title": "Free shipping at $198", "text": "Two wedges get you there."}}])},
    "quotes": {"type": "lg-quotes", "settings": {"no_top": True, "eyebrow": "From people who switched", "heading": "They switched from the big <em>names.</em>",
                                                 "link_label": "Read every review", "link_url": REVIEWS}, **blocks([
        {"type": "quote", "settings": {"stars": 4, "name": "Adam K.", "on": "Carver, verified buyer",
                                       "quote": "Took a chance on these wedges and have been very pleasantly surprised at their appearance, performance and durability. Would definitely recommend for someone looking for a solid wedge and doesn’t want to pay the price for the large and popular brands and doesn’t have the need or want to get fitted!"}},
        {"type": "quote", "settings": {"stars": 5, "name": "Jason", "on": "Carver, verified buyer", "quote": "Great looks and performance for the price"}},
        {"type": "quote", "settings": {"stars": 5, "name": "Kyle M.", "on": "Carver, verified buyer",
                                       "quote": "I LOVE my wedges they preform high up with the big name brands and all my friends are jealous of how sexy these clubs are"}}])},
    "signoff": signoff(QUOTE_LUCKY, "Spend the difference on green fees.", "See the clubs", CLUBS),
})

# ------------------------------------------------------------------ Contact  (/pages/contact-us)
T["templates/page.contact.json"] = page({
    "contact": {"type": "lg-contact", "settings": {
        "crumb": "Contact", "eyebrow": "Talk to us", "heading": "A person reads <em>these</em>",
        "lede": "Sizing, lofts, where your order is, or the one that got away on 17. Ask whatever you need to ask.",
        "l_name": "Name", "l_email": "Email", "l_order": "Order number", "p_order": "If you have one", "l_topic": "What's it about",
        "topics": "Where my order is\nA return or exchange\nSizing or fit\nWhich club to pick\nSomething arrived damaged\nSomething else",
        "l_msg": "Message", "btn": "Send it", "sent": "Got it. We'll come back to you on the email above, usually the same day."}, **blocks([
        {"type": "way", "settings": {"icon": "mail", "title": "support@luckygolf.com", "text": "Order number in the subject line gets you an answer faster."}},
        {"type": "way", "settings": {"icon": "message-circle", "title": "Chat", "text": "Bottom right of any page. Best for a quick question before you buy."}},
        {"type": "way", "settings": {"icon": "package", "title": "Returns", "text": "Apparel and gear go through the returns portal. Clubs need approval first, so start here and we'll set it up."}},
        {"type": "way", "settings": {"icon": "circle-help", "title": "Already answered", "text": "Shipping times, the 60 days and sizing are all on the <a href=\"/pages/faq-lucky-wedges\">questions page</a>."}}])},
    "signoff": signoff("No phone tree, no ticket <em>number</em>", "Nine of us work here. One of them is a magpie and he's no help at all.",
                       line="Read the questions first →", line_url=FAQ),
})

# ------------------------------------------------------------------ Community  (/pages/community, new)
T["templates/page.community.json"] = page({
    "hero": {"type": "lg-hero-plus", "settings": {
        "image": im("walk-off-green.webp"), "focus_x": 50, "focus_y": 18, "focus_mx": 50, "focus_my": 20, "short": True,
        "eyebrow": "Community", "heading": "Straight off the camera <em>roll</em>", "lede_w": 56,
        "lede": "Real rounds and real bags, from golfers who couldn't keep the shot to themselves. Tag @luckygolfofficial and yours could be next."}, **blocks([
        {"type": "button", "settings": {"label": "Instagram", "url": "https://www.instagram.com/luckygolfofficial/", "icon": "instagram", "new_tab": True}},
        {"type": "button", "settings": {"label": "TikTok", "url": "https://www.tiktok.com/@luckygolfofficial", "icon": "tiktok", "new_tab": True}}])},
    "wall": {"type": "lg-wall", "settings": {"show_label": "Show", "all_label": "Everything", "clubs_label": "Clubs", "apparel_label": "Apparel", "gear_label": "Gear",
                                             "count_word": "posts", "page": 8, "more_label": "Show more",
                                             "aside": "Nothing goes up here until the golfer in it says yes.", "in_label": "What's in the shot"}},
    "signoff": signoff("Posting anyway? Get paid for <em>it</em>",
                       "Ambassadors see their best clips run as ads from their own handle and earn a share of what they bring in. There's no follower minimum.",
                       line="See the ambassador program →", line_url=TRYBE),
})

# ------------------------------------------------------------------ All reviews  (/pages/reviews)
T["templates/page.reviews.json"] = page({
    "hero": {"type": "lg-hero-plus", "settings": {
        "image": im("putt-sunset.webp"), "focus_x": 50, "focus_y": 26, "focus_mx": 42, "focus_my": 30, "short": True,
        "eyebrow": "[count] reviews on the clubs", "eyebrow_low": "Reviews on the clubs", "count_products": [CARVER, BLADE, MALLET, STRYKER],
        "heading": "The raves, and the <em>grumpy</em> ones", "lede_w": 52,
        "lede": "Verified buyers only, pulled straight from Judge.me. Sort by club or by stars, and the low ones haven't gone anywhere."}},
    "all": {"type": "lg-reviews-all", "settings": {"of_line": "out of five, from [count] reviews", "tile_word": "reviews", "anchor": "all-reviews", "club_label": "Club", "stars_label": "Stars", "all_label": "All", "sort_label": "Sort", "sort_recent": "Most recent", "sort_high": "Highest rating", "sort_low": "Lowest rating"}, **blocks([
        {"type": "club", "settings": {"product": CARVER, "label": "Carver 02", "also": [BLACK]}},
        {"type": "club", "settings": {"product": BLADE, "label": "Eclipse Blade"}},
        {"type": "club", "settings": {"product": MALLET, "label": "Eclipse Mallet"}},
        {"type": "club", "settings": {"product": STRYKER, "label": "Stryker"}}])},
    "signoff": signoff("Read <em>enough?</em>",
                       "The clubs are this way.", "See the clubs", "shopify://collections/lucky-golf-clubs", arrow=False),
})

# ------------------------------------------------------------------ 404
T["templates/404.json"] = page({
    "main": {"type": "lg-nf", "settings": {
        "eyebrow": "404", "heading": "This one's in the <em>trees</em>", "lede": "The page isn't here. Take a drop and try one of these.",
        "btn_label": "See the clubs", "btn_url": CLUBS, "btn2_label": "Back to the start", "btn2_url": "/"}, **blocks([
        {"type": "card", "settings": {"product": CARVER, "image": im("gold-full-cut.webp")}},
        {"type": "card", "settings": {"product": MALLET, "image": im("mallet-full-cut.webp")}},
        {"type": "card", "settings": {"product": "azalea-classic-polo", "image": im("polo-azalea-cut.webp")}},
        {"type": "card", "settings": {"product": "white-gold-classic-hat", "image": im("hat-white-gold-classic-cut.webp"), "name": "White & Gold Classic Hat"}}])},
})

# ------------------------------------------------------------------ Search
T["templates/search.json"] = page({
    "main": {"type": "lg-search", "settings": {
        "eyebrow": "Search", "heading": "What are you <em>after?</em>", "label": "Search Lucky Golf",
        "placeholder": "Wedge, 56, mallet, polo, hat", "btn": "Search", "sugs": "wedge, 56, putter, polo, hat, gold", "sugs_label": "Common searches",
        "one": "result for", "many": "results for", "texts_label": "Pages and posts", "article_word": "Article", "page_word": "Page",
        "none": "Nothing matches that. Try the club, the loft or the color, or <a href=\"/collections/lucky-golf-clubs\">see every club</a>.",
        "start": [CARVER, BLACK, BLADE, MALLET, STRYKER, "azalea-classic-polo", "blackout-blade-polo", "gold-dust-classic-polo", "swirl-blade-polo", "white-gold-classic-hat", "black-its-better-to-be-lucky-patch-hat", "cream-upside-down-hat"]}},
    "signoff": signoff("Can't find it? <em>Ask</em>", "Tell us the gap you're trying to cover and we'll tell you which club does it.",
                       line="Talk to a person →", line_url=CONTACT),
})
