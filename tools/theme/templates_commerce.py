"""Cart, gift card, blog and article templates (group 80), filled with the approved v9 copy
(v9/src/cart.html, giftcard.html, blog.html, article.html). Imported by build_templates.py."""


def im(name):
    return "shopify://shop_images/lg-" + name


T = {}

T["templates/cart.json"] = {
    "sections": {
        "main": {"type": "lg-cart", "settings": {
            "crumb": "Your bag", "eyebrow": "Your bag", "heading": "What you're taking to the <em>course</em>",
            "empty_text": "Nothing in here yet.",
            "empty_btn": "See the clubs", "empty_url": "shopify://collections/lucky-golf-clubs",
            "empty_btn2": "Shop the polos", "empty_url2": "shopify://collections/polos",
            "checkout_label": "Check out",
            "note": "Tax is added at checkout, and nothing's charged until you place the order.",
            "show_note": False}, "blocks": {
            "t1": {"type": "trust", "settings": {"icon": "truck", "title": "Ships in 1 to 2 days", "text": "Tracking shows up as soon as the carrier scans it."}},
            "t2": {"type": "trust", "settings": {"icon": "rotate-ccw", "title": "Sixty days on clubs", "text": "Thirty on apparel, unworn with the tags on."}},
            "t3": {"type": "trust", "settings": {"icon": "shield-check", "title": "Free shipping at $198", "text": "Two wedges get you there."}}},
            "block_order": ["t1", "t2", "t3"]},
        "close": {"type": "lg-signoff", "settings": {
            "eyebrow": "The last word", "heading": "“It's better to be <em>lucky.</em>”",
            "lede": "Worst case, it comes back. Sixty days on clubs, thirty on apparel.",
            "btn2_label": "How returns work →", "btn2_url": "/pages/faq-lucky-wedges#returns"}},
    },
    "order": ["main", "close"],
}

T["templates/product.giftcard.json"] = {
    "sections": {
        "main": {"type": "lg-giftcard", "settings": {
            "crumb": "Gift card", "eyebrow": "Gift card",
            "heading": "For the golfer who swears they don't need <em>anything</em>",
            "body": "Emailed straight away, or on the day you pick. They choose the loft, the size or the print, which is the part you were going to get wrong.",
            "default_amount": 50, "card_left": "Gift card", "card_right": "It's better to be lucky",
            "amount_label": "Amount", "who_label": "Who it's for",
            "me_title": "Me", "me_line": "It comes to my email", "them_title": "Someone else", "them_line": "We email them",
            "name_label": "Their name", "email_label": "Their email", "msg_label": "A note from you",
            "msg_placeholder": "Happy birthday. Go fix that short game.", "date_label": "Send it on",
            "btn_label": "Add to cart",
            "fine": "Good on anything in the store for five years, and it arrives by email, so there's nothing to wrap."}},
        "qa": {"type": "lg-qa", "settings": {"eyebrow": "Before you send it", "heading": "The quick <em>answers</em>"}, "blocks": {
            "q1": {"type": "qa", "settings": {"q": "How does it get to them?", "a": "<p>By email, with your note on it, either straight away or on the date you picked.</p>"}},
            "q2": {"type": "qa", "settings": {"q": "What can they spend it on?", "a": "<p>Anything in the store. If they find something that costs more than the card, they pay the difference at checkout.</p>"}},
            "q3": {"type": "qa", "settings": {"q": "Can they check what's left on it?", "a": "<p>Yes. The email links to their card, with the code and the balance, and whatever they don't spend stays on it for the next order.</p>"}},
            "q4": {"type": "qa", "settings": {"q": "How long is it good for?", "a": "<p>Five years from the day it's sent. It can't be refunded or swapped for cash, so spend it on something gold.</p>"}}},
            "block_order": ["q1", "q2", "q3", "q4"]},
        "picks": {"type": "lg-picks", "settings": {
            "eyebrow": "Or pick it out yourself", "heading": "What they'd buy with it <em>anyway</em>",
            "link_label": "See everything", "link_url": "shopify://collections/all-products"}, "blocks": {
            "p1": {"type": "pick", "settings": {"product": "lucky-golf-lgw02-gold", "image": im("gold-full-cut.webp")}},
            "p2": {"type": "pick", "settings": {"product": "limited-edition-mallet-putter", "image": im("mallet-full-cut.webp")}},
            "p3": {"type": "pick", "settings": {"product": "lucky-striker-hybrid-limited-edition"}},
            "p4": {"type": "pick", "settings": {"product": "white-gold-classic-hat", "image": im("hat-white-gold-classic-cut.webp")}}},
            "block_order": ["p1", "p2", "p3", "p4"]},
        "close": {"type": "lg-article-signoff", "settings": {
            "eyebrow": "The last word", "heading": "Nobody returns a gift <em>card</em>",
            "lede": "It lands in their inbox, whatever they pick ships in one to two business days, and you still get the thanks.",
            "btn_label": "Send one", "btn_url": "#send"}},
    },
    "order": ["main", "qa", "picks", "close"],
}

T["templates/blog.json"] = {
    "sections": {
        "hero": {"type": "lg-hero", "settings": {
            "image": im("gold-wedge-bag.webp"), "focus_x": 50, "focus_y": 50, "focus_mx": 40, "focus_my": 50, "short": True,
            "eyebrow": "All Things Lucky", "heading": "Golf, written by people who <em>play</em> it", "heading_tag": "h1",
            "lede": "The short game, the gear, and the occasional thing that happened on the way to the first tee."}},
        "posts": {"type": "lg-blog", "settings": {"lead": "news/are-your-wedges-forged", "lead_eyebrow": "Latest", "read_label": "Read it"}},
        "news": {"type": "lg-news", "settings": {
            "eyebrow": "First look", "heading": "Get the next one in your <em>inbox</em>",
            "body": "New articles land there first, along with restocks and new lofts. Unsubscribe whenever you like, no hard feelings.",
            "placeholder": "you@somewhere.com", "btn_label": "Sign me up", "source": "Blog", "no_top": True}},
        "close": {"type": "lg-signoff", "settings": {
            "eyebrow": "The last word", "heading": "Reading about golf isn't <em>practice</em>",
            "lede": "Take one idea from here to the range this week, and give it a whole bucket before you decide it doesn't work.",
            "btn2_label": "See the clubs →", "btn2_url": "shopify://collections/lucky-golf-clubs"}},
    },
    "order": ["hero", "posts", "news", "close"],
}

T["templates/article.json"] = {
    "sections": {
        "main": {"type": "lg-article", "settings": {}},
        "more": {"type": "lg-article-more", "settings": {"eyebrow": "Keep reading", "heading": "More from the <em>blog</em>", "link_label": "All articles"}},
        "close": {"type": "lg-article-signoff", "settings": {
            "eyebrow": "The last word", "heading": "It's better to be <em>lucky.</em>",
            "lede": "Sixty days to make up your mind on the clubs, thirty on the rest.",
            "btn_label": "See the clubs", "btn_url": "shopify://collections/lucky-golf-clubs"}},
    },
    "order": ["main", "more", "close"],
}
