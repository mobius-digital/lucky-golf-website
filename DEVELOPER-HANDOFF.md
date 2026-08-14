# Lucky Golf — developer handoff

**For the developer who turns this prototype into a Shopify theme.**

This repo is 58 built pages, zero dead links, published at
https://mobius-digital.github.io/lucky-golf-website/ from
`mobius-digital/lucky-golf-website` (master, GitHub Pages).

Every page is a single self-contained HTML file with its CSS and JS inlined.
That is a delivery format, not an architecture. The architecture is `_src/` plus
`tools/`, and it was shaped from the first commit to hand over to Liquid: three
product templates driven by data, a Mustache-shaped template engine, a link
registry, and a catalogue normalised out of a real Shopify pull.

**Read §8 and §9 before you write any code.** They are the rules that were
learned by measuring, and every one of them will be reintroduced by accident if
nobody says them out loud.

---

## 1. Run it

Python 3, no dependencies. Node only for the variant test.

```bash
python tools/normalize-products.py          # shopify-raw.json -> products.json
python tools/build.py                       # assemble all 58 pages
```

Checks — all three must be clean before anything ships:

```bash
python tools/normalize-products.py --check  # products.json is not stale
python tools/build.py --check               # every page rebuilds byte-identical
node tools/test-variants.js                 # the axis engine, over all 43 products
```

Two more that are worth knowing:

```bash
python tools/build.py --links               # the link registry: 60 pages, 58 built
python tools/build.py club                  # build one template's pages only
```

Current state: **43 products, 155 variants, 60 declared pages, 58 built.**

**Never edit an `NN-*.html` file.** They are build output and are overwritten.
Source of truth is `_src/` plus `_src-logo-symbols.svg`.

---

## 2. What is in the box

```
_src/
  core.css          the design system: tokens, type, bands, buttons, tiles,
                    modals, the cart drawer, the review widget
  core.js           header, mega menu, cart drawer, lightbox, modals, quick add
  variants.js       the variant-axis engine — no DOM, no page state
  reviews.js        LG_REVIEWS.mount(root, data, opts) — the whole review widget
  pdp.js            behaviour shared by all three product templates
  pdp.css           styles shared by all three product templates
  page-<name>.html  one per template — the markup
  page-<name>.css   one per template — a page loads core plus exactly ONE of these
  page-<name>.js    one per template — optional
  partials/         header, footer, cart, lightbox, symbol host
  data/
    shopify-raw.json    the raw pull, pasted verbatim from four Shopify queries
    products.json       GENERATED — do not hand-edit
    copy/               69 editorial JSON files (see §7)
    reviews/            5 Judge.me pulls, verbatim

tools/
  normalize-products.py   raw pull + editorial overlay -> products.json
  sitemap.py              the link registry — the one place a URL is written down
  template.py             the Mustache-shaped engine (140 lines, read it)
  build.py                page assembly, the build guards, the smoke tests
  test-variants.js        the axis engine's invariants over the whole catalogue
  split-src.py            historical — split the old single file into _src/
  render-ref.py           historical — reference screenshots

references-product-guide-v1.8.md      product facts. Outranks everything.
references-how-we-write-v7.3.md       voice
references-culture-v2.md              golf-culture vocabulary
references-spec-to-benefit-v1.0.md    what each spec means, and CLAIMS TO AVOID

HANDOFF.md        the full build log, §1–§26. The why behind every decision.
FINISH-LINE.md    what remains, as a checklist, and who owns each item.
SHOT-LIST.md      26 stills and 36 video briefs, handable to a photographer.
```

`_ref/` holds reference captures of Takomo and Dartee PDPs — the two sites this
one was measured against. `_brand-variants.html`, `_groove-options.html` and
`_why-options.html` are live option-switchers kept for future colour and copy
decisions; they are not part of the site.

---

## 3. The pipeline, and what happens to it in Shopify

```
Shopify Admin ──(4 GraphQL queries)──> _src/data/shopify-raw.json
                                              │
             EDITORIAL overlay (in normalize-products.py)
                                              │
                                              ▼
                                    _src/data/products.json
                                              │
        _src/data/copy/*.json ───────────────>│<─────── _src/page-*.html
                                              │
                                          build.py
                                              │
                                              ▼
                                        NN-*.html
```

**In a theme, the left half of this disappears.** Liquid reads the catalogue
live, so `shopify-raw.json`, `normalize-products.py` and `products.json` all go
away. What does **not** go away is the two things they encode:

1. **The editorial overlay** — `id`, `template`, `family`, `code`, `title`,
   `finish`, `finishGroup`, `rating`, `default`. None of it exists in Shopify
   today. It has to become metafields, or you will hand-maintain it in Liquid.
   See §7.
2. **The traps in §8.** Every one was found in this store's real data. They are
   properties of the catalogue, not of the prototype.

The right half maps almost directly onto a theme: `page-*.html` are sections,
`data/copy/*.json` is the editorial layer, `build.py` is the shaping step that
Liquid does inline.

---

## 4. Page → Shopify template

| Ours | Shopify | Covers |
|---|---|---|
| `_src/page-home.html` | `templates/index.json` | 1 page |
| `_src/page-clp.html` | `templates/collection.clubs.json` | 4 club collections |
| `_src/page-plp.html` | `templates/collection.json` | Polos, Hats, Gear |
| `_src/page-club.html` | `templates/product.club.json` | 5 clubs |
| `_src/page-apparel.html` | `templates/product.apparel.json` | 23 polos and hats |
| `_src/page-gear.html` | `templates/product.gear.json` | 13 gear products |
| `_src/page-support.html` | `templates/page.contact.json` + `page.policy.json` | 4 pages |
| `_src/page-brand.html` | `templates/page.json` | Our Story, Ambassador Program |
| `_src/page-reviews.html` | `templates/page.reviews.json` | 1 page |
| `_src/page-search.html` | `templates/search.json` | 1 page |
| `_src/page-404.html` | `templates/404.json` | 1 page |

**Three templates serve 41 product pages, one serves four support pages, one
serves two brand pages.** That ratio is the point of the whole build: a change
to the buy box is one edit, not forty.

`templates/collection.json` and `collection.clubs.json` are genuinely different
pages, not one page with a flag. The club collections (`clp`) render their grid
server-side in labelled bands with a spec comparison and brand copy under it;
everything else (`plp`) is a flat grid with facet chips repainted in JS. A flat
grid is the right page for thirteen polos and the wrong page for six clubs.

**Routing note:** `10-collection-hybrid.html` was `hybrid-driver` until the
driver was discontinued. Renaming a collection moves its URL — set up the
redirect rather than leaving the old one orphaned. Same for the two
discontinued products, `lgd01` and `lgp02-patriot`, whose pages no longer exist.

---

## 5. What each template is made of

Section order is deliberate and documented in HANDOFF §7 (homepage) and §20
(club collections). The homepage in particular alternates ink / white / cream so
no two dark bands touch, and the brand field lands exactly three times — 0px,
under the hero, and mid-page — which is what makes it read as a spine rather
than an unused palette entry.

**`page-home.html`** — hero, shop-by-family, featured club, Why Lucky (owns the
price objection), club finder (tabbed, keyboard-navigable), brand band, pull
quote, review rail, value props (owns quality and guarantees), UGC rail, the
finish, ambassador roster, apparel & gear, closing CTA.

> Why Lucky and the value props make two different arguments on purpose. Why
> Lucky owns **price** — no middlemen, no tour contracts. Value props own
> **quality and trust** — built properly, sixty days, backed by golfers. They
> were making the same argument twice, which is what made the page feel
> repetitive. Keep them split.

**`page-club.html`** — breadcrumb, gallery + buy box, story, reel rail, loft
finder, comparison, **grind explainer** (`#grinds`), spec tabs, the look,
pull quote, reviews, cross-sell, bag, closing CTA.

**`page-apparel.html`** — colourway swatches + buy box, design section (one per
*family*, not per design), pull quote, reviews, siblings strip, closing CTA.
The size guide is a **modal** hung off the size picker, not a section.

**`page-gear.html`** — the short one. Buy box, one band, reviews, cross-sell.

**`page-clp.html`** — header, banded grid, "start here" router (All Clubs only),
comparison with segmented spec bars, fitting CTA on the brand field, brand
story, testimonial, sibling collections.

**`page-plp.html`** — header, facet chips + grid + empty state, sibling
collections.

**`page-support.html`** — header, contact channels, jump nav ("On this page",
opt-in per page), sectioned prose, FAQ accordion (`<details>`, opens with no
JS), contact form, "still stuck" band, sibling pages.

**`page-brand.html`** — header, stats band, alternating photo/copy rows, pull
quote, roster, steps, fitting CTA, sibling pages.

**`page-reviews.html`** / **`page-search.html`** / **`page-404.html`** — one
body section each, plus the shared widget in the first two.

### The shared partials

`partials/header.html` is a mega menu with four panels — Wedges, Putters,
Hybrid, Apparel & Gear — plus Our Story, search, cart and a mobile drawer. In a
theme this becomes a header section with menu-driven blocks. **The tile counts
in it are `{{count:polos}}` tokens, not typed numbers**, because the menu once
advertised "13 styles" of hat when the store had ten. In Liquid that is
`{{ collections.hats.products_count }}` — resolve it live, do not type it.

`partials/footer.html` names five clubs and four support pages. It is a footer
section with linklist blocks.

---

## 6. Mustache → Liquid

`tools/template.py` is 140 lines and was written Mustache-shaped **specifically
so `{{#x}}…{{/x}}` maps onto `{% for %}` and `{% if %}` legibly.** Read it once;
it is the shortest file in the repo that explains the most.

| Ours | Liquid |
|---|---|
| `{{name}}` | `{{ name }}` |
| `{{#list}}…{{/list}}` | `{% for item in list %}…{% endfor %}` |
| `{{#flag}}…{{/flag}}` | `{% if flag %}…{% endif %}` |
| `{{#obj}}…{{/obj}}` | `{% assign x = obj %}` — pushes a scope |
| `{{^name}}…{{/name}}` | `{% unless name %}…{% endunless %}` |
| `{{.}}` | the loop item itself, for plain string lists |
| `{{! note }}` | `{% comment %}` |
| `{{#first}}` inside a loop | `{% if forloop.first %}` |
| `{{link:p/lgw01-gold}}` | `{{ product.url }}` |
| `{{link:c/wedges}}` | `{{ collection.url }}` |
| `{{link:home}}` | `{{ routes.root_url }}` |
| `{{link:search}}` | `{{ routes.search_url }}` |
| `{{count:hats}}` | `{{ collections.hats.products_count }}` |
| `{{link:none}}` | a real `href="#"` — see below |

Four things about the engine that matter when you port it:

**It does not escape anything.** Every value is authored copy from
`_src/data/copy/`, much of it carrying intentional markup (`<em>`, links,
`&mdash;`). If that copy moves into metafields, use rich-text metafields or
`| metafield_tag`, and never point this pattern at customer input.

**It has no dotted paths, no filters and no partials.** That is deliberate: if a
template needed one, the data was shaped wrong and `build.py` flattened it
instead. All of the shaping is in `product_copy()`, `collection_copy()`,
`support_copy()`, `brand_copy()` and `reviews_copy()` — read those five
functions and you have the whole data contract.

**Lookup walks the scope stack outward, and so does Liquid.** A section with no
`lede` of its own silently inherits the *page's* lede and renders a duplicated
line rather than nothing — that is how the refund policy came out repeating its
own headline. `support_copy()` pins the optional keys to `""` to stop the
lookup. **Liquid has the same trap**, because a bare `{{ lede }}` inside a
`{% for %}` resolves to the outer assign. Reference loop variables explicitly:
`{{ sec.lede }}`, never `{{ lede }}`.

**`{{link:none}}` is not decoration.** A literal `href="#"` anywhere in `_src/`
is a fatal build error, because there is otherwise no way to tell a modal
trigger that genuinely goes nowhere from a link somebody forgot to wire up.
Keep the discipline — a `href="#"` audit in theme-check costs nothing and this
site shipped with three dead cross-sell rows before the guard existed.

---

## 7. The editorial layer, and where it has to live

This is the part with no Shopify equivalent, and the part a theme port most
often gets wrong.

There are **three layers, each overriding the one under it**, merged in
`product_copy()`:

```
_shared-<template>.json    true of every product on this template   (e.g. the polo size chart)
_family-<family>.json      true of every product in this family     (e.g. the Classic Polo design section)
<product>.json             what is actually different about THIS product
```

The merge is **shallow and total** — any key the product file sets wins
outright, no deep merging, because a half-overridden list is harder to reason
about than a repeated one.

Why it exists: thirteen polos share one fabric, one fit note, one size guide and
one returns line. Writing that thirteen times is thirteen chances for it to
drift, and 22 apparel pages each carried a bespoke design section until Cole
ruled that what actually differs between colourways is the photograph, not the
garment.

**Liquid has no merge.** You have to write the fallback chain explicitly. The
shape that works:

```liquid
{%- assign fam = shop.metaobjects.lucky_family[product.metafields.lucky.family] -%}
{%- assign tpl = shop.metaobjects.lucky_template[product.metafields.lucky.template] -%}
{%- assign design = product.metafields.lucky.design
      | default: fam.design | default: tpl.design -%}
```

Recommended mapping:

| Layer | Shopify home |
|---|---|
| `<product>.json` | product metafields, namespace `lucky` |
| `_family-*.json` | metaobject `lucky_family`, referenced by a product metafield |
| `_shared-*.json` | metaobject `lucky_template`, or theme settings |
| `_collection-*.json` | collection metafields |
| `_support-*.json`, `_brand-*.json` | page metafields, or the page body |
| `_page-home.json` | section settings in `index.json` |
| `data/reviews/*.json` | Judge.me's own app blocks (see §11) |

The editorial overlay in `normalize-products.py` — `id`, `tpl`, `fam`, `code`,
`title`, `finish`, `finishGroup`, `rating`, `default`, `built`, `discon` — is
the other half. `tpl` becomes the product template suffix. `fam` becomes a
product metafield and drives the colourway strip, the breadcrumb and the
help-me-choose module. `title` is **Cole's locked full form** — family, code,
finish — and it is what tiles and H1s use; `name` is the short form. Do not
re-litigate those; HANDOFF §22d records what happened when the store had two
products both reading "Carver Gold" on a tile.

`finishGroup` is worth its own note: **Gold and Black are two Shopify products**,
exactly like the polo colourways, and the swatch row keyed on `finishGroup` is
the only thing making the Black reachable from the Gold's page.

---

## 8. Catalogue traps — every one was found in this store's real data

**These are not prototype quirks. They are properties of the Lucky Golf
catalogue and they will bite a theme exactly as hard.**

**`availableForSale` is NOT `inventoryQuantity > 0`.** Several products oversell
— the Tour Glove's LH Small sits at qty **−3** and is still sellable — and
several sit at qty 0 while still purchasable, including the black clover grips.
Availability drives whether a chip is disabled. Quantity only drives the "Low
stock — N left" line. Keying the buy box off quantity would disable sellable
variants and sell dead ones. In Liquid that is `variant.available`, never
`variant.inventory_quantity`.

**SKUs are never synthesised.** Several in this store are genuinely irregular:
LGW02 Black's 50 and 52 are stamped `LGW03-…` (a typo in Shopify) while 54–60
are `LGW02-…`; the mallet cover is `HeadCover-Mallet-SignatureWhite-RH` in one
hand and `Putter-Cover-Mallet-Signature-White-LH` in the other. Every SKU is
carried verbatim. Any pattern you infer is wrong for at least one product.

**No SKU renders on a merchandising surface.** Not on a PDP, not on a tile, not
in the buy box, not in a cross-sell rail, and search deliberately does not match
them — a search that matches a string it will not then show looks broken. They
are carried on every variant because the cart needs them, and they appear only
in the cart line item and the lightbox buy block.

**Price is per variant, not per product.** Grips run $9.95 / $11.95 / $14.95
across Standard / Midsize / Jumbo; the oversized putter grips run $19.95 to
$26.95. The buy box repaints the price on every selection. Six products in the
catalogue have genuinely variable pricing — `test-variants.js` lists them.

**A `Title` option with one value is Shopify's "no options" sentinel.** It
becomes **zero axes**, not a one-value picker. `Lucky Golf Tees` uses the same
sentinel with the value "25 Tees" rather than "Default Title", so the rule keys
off the option *name* plus a single value, not off the value string.

**Shopify's option names are inconsistent across product types.** Wedges say
"Right Hand", putters and covers say "Right". Both collapse to one key in
`OPTION_KEY` / `VALUE_MAP`. You need the same normalisation or your hand picker
renders four values for two hands.

**A product card never shows a review count.** The variant summary — "Right &
left hand · 6 lofts", "S–3XL" — is what belongs in that slot, because it answers
a question a browsing shopper actually has. This is enforced in `build.py`: a
star character in a card meta is a **fatal build error**, because a rating typed
into a copy file is also stale the moment Judge.me moves.

**No manufacturer tolerances anywhere.** No `±` renders on any page.

**Availability summaries are derived, never typed.** "6 lofts" counts the lofts
some sellable variant actually reaches, and the FAQ's left-hand answer is
generated from the catalogue by `hand_rows()`. Left-hand availability is the
most-asked question in the entire review corpus and it goes stale the instant a
loft sells out.

### The variant engine

`_src/variants.js` is 80 lines, has no DOM and no page state, and is verified
against the whole catalogue by `tools/test-variants.js` rather than against
whatever page happens to be open. **Port it as-is.** It powers the PDP buy box,
the in-card Quick add on the collection grids, and search results — three
surfaces, one implementation, because a second copy of "is this combination
sellable" is the last thing this site needs.

Its one non-obvious rule: **availability cascades left to right.** "Left hand"
grays out only when no loft at all is available in it; an individual loft grays
out for the hand you are actually on. Changing an axis slides the axes to its
right to the *nearest offered value by position*, which on an ordered axis
(lofts, sizes) is the neighbouring step — which is what somebody switching hand
actually wants.

---

## 9. Design laws — measured, not aesthetic

### The green-field contrast law

Against `--green #008340`:

| Foreground | Ratio | Verdict |
|---|---|---|
| `--white` #FFFFFF | **4.86:1** | PASS — use for **all** text on green |
| `--cream` #F6F2E8 | 4.35:1 | **FAIL** — never text |
| `--gold` #C29A2B | 1.84:1 | **FAIL at any size** — never gold on green |
| `--gold-hi` #EDD27C | 3.27:1 | non-text only — rules, borders, marks, badges |

The brand field is currently Forest `#0B5130` with base gold as the accent
(3.56:1, passes the 3:1 non-text bar). **Six variables drive the header, the
marquee and the brand band together** — `--brand`, `--on-brand`, `--on-brand-88`,
`--on-brand-22`, `--brand-accent`, `--brand-groove`. Swap those six and the
whole spine changes colour. `_brand-variants.html` is the same page with a live
switcher over twelve candidates and a contrast readout.

**The `.nav a` trap:** the mega panel lives inside `.nav` and sits on white, so
a bare `.nav a` rule paints those tiles white-on-white. It is scoped `.nav > a`,
and `.mega :focus-visible` is reset to base `--gold`. Keep it that way.

### Foil is illegal on white as type, and the contrast sweep cannot see it

The foil ramp bottoms out at `--gold-lo #8A6A1C`, and ink on that measures
**3.64:1** — a fail at the ~9px mono an emphasis tag is set in. **Automated
contrast tooling skips gradient backgrounds entirely**, so nothing catches this
for you.

- Small text on a foil **fill** uses `--lg-foil-tag`, which drops the shadow
  stops so the darkest point is `--gold` at 6.95:1.
- Foil as **type** (background-clip) only ever runs on ink or the brand field.
  The ramp peaks at `--gold-hi`, which is under 2:1 on white.
- On a button the shadow stops sit under no text and the full ramp is fine.

### Radius follows the size of the surface, not the type of component

```
--r       6px    controls — chips, buttons, inputs, selects, small badges
--r-card  14px   surfaces — product tiles, panels, image wells, modals
```

One radius does not fit a 48px chip and a 420px product card: at 4px a card
reads as a rectangle with a chamfer, which is what made the tiles look rigid.
Borders stay 2px.

### Rules versus the groove

The groove is 1px lines on a 6px pitch, so **a 1px structural divider on a
grooved field reads as one more groove line.** Every rule on a grooved section
is 2px and brighter than the groove — `--rule-on-dark` / `--rule-on-light`.
Grooved sections: `.hdr .mq .bband .feat .why .vp .roster .close .ftr`.

### Never bleed a nowrap overflow-x flex row

A nowrap flex row with `overflow-x` resolves its width from its content once a
negative `margin-inline` is on it. The breadcrumb came out **1485px in a 1440px
viewport and put horizontal overflow on every PDP.** `min-width:0; max-width:100%`
and no bleed is what works. The jump nav on the support pages is the same shape
and is deliberately not bled.

### Any boolean reaching an attribute VALUE must be a lowercase string

A Python `True` rendered `aria-checked="True"`, CSS attribute matching is
case-sensitive, `[aria-checked="true"]` never matched, and the size guide opened
with neither unit selected. It was also invalid ARIA. A `{{#section}}` test is
fine; an attribute value is not.

### Full-bleed bands need the next section's top padding back

`.sec` blocks carrying `padding-top:0` assume the section above is the same
colour. Insert a full-bleed colour band and check the section under it.

### Tap targets

44px on touch, **24px minimum on a pointer** (WCAG 2.2 SC 2.5.8). The email
address on Contact was 22px and the FAQ's product links were 16px; both are 44px
now. Footer links were 16×98.7 on desktop with ~11px of dead gap between rows —
they had been 44px on the phone since Phase 1, so the gap was pointer-only. Fixed
2026-08-13 by moving the gap **inside** the target: 24×205.7, a 25px row pitch,
and a footer 41.5px shorter than before.

> The trap worth carrying over: a `display:inline` anchor's hit area is its
> **inline box**, not its line box. Those footer rows looked 36px apart and were
> 16px clickable. Any list of links needs `display:flex` plus a `min-height`, or
> the spacing you see is not the spacing you can click.

### The one-stylesheet constraint, and why six components live in core

**A page loads `core.css` plus exactly ONE `page-*.css`.** Six components have
had to move into core because two templates needed them:

`.chip` · the pdp split · `.spec-tbl` · `.sw` (finish swatches) · `.tbd`
(the "Needs confirming" chip) · the review widget's `.jm*` / `.jr*`.

**In a theme this constraint goes away** — you can load per-section CSS. If you
un-promote any of them, know that they are in core for that reason and not
because they are foundational.

### `.tbd` is the point, not a placeholder style

`<span class="tbd">Needs confirming</span>` renders dashed, Space Mono,
`--ink-muted` (5.14:1 on white, 4.94 on cream). It had **no CSS rule at all**
for a whole phase, which meant every unconfirmed policy detail rendered as
ordinary body copy — **a gap that looks like prose reads as a statement**, which
is the exact opposite of the point. Three policy answers and 57 unpublished
specs are still chipped this way (§12). Keep the device.

---

## 10. Build guards worth keeping

`build.py` fails the build on all of these. Every one was added after something
shipped broken, and **every guard in the repo has been verified by breaking it
on purpose.**

| Guard | What it catches |
|---|---|
| Dangling `{{link:…}}` | a slug that is not in the registry |
| Literal `href="#"` in `_src/` | a link somebody forgot to wire |
| Any `{{…}}` left after resolution | a typo'd token shipping as a blank |
| `REQUIRED` smoke markers | a load-bearing CSS rule or JS function dropped from the bundle |
| A star in a card meta | a hand-typed review count on a tile |
| Cross-sell to a discontinued product | three dead rows shipped this way once |
| A collection member in no band | a club silently missing from its own page |
| Reviews that do not reconcile | a headline and a histogram that disagree |
| A roster name with no `consent` key | a real person published without agreeing |
| An image slot with no brief | a labelled placeholder with no label |
| A support section with no `id` | nothing can link to it |

Two of these deserve porting even though Liquid does not need them:

**The reviews arithmetic.** `reviews_copy()` reaches the same figure two
independent ways — `clubs_wide − pulled`, and the sum of rated clubs with no
pull in the repo — and stops the build if they disagree. A reviews page whose
headline and histogram do not add up is worse than no page.

**The smoke markers.** A regex cleanup once silently deleted a whole responsive
block and the page still built, still passed a desktop sweep, and only showed up
as a broken phone layout. Splitting `pdp.js` out briefly dropped it from the
bundle entirely: the page built, `--check` said "identical" (it compares output
to output), and only a 30KB size drop gave it away.

> **A smoke marker must exist in exactly ONE source file.** This has been
> defeated twice by a marker string that also appeared somewhere else — `"LG_VARIANTS"`
> survived emptying `variants.js` because `core.js` names it too. Grep the tree
> before adding one.

---

## 11. What is temporary, and must be deleted rather than ported

**`merge_grinds()` in `normalize-products.py`.** Lucky sells one wedge, the 01;
the K-grind gold and the S-grind gold were two Shopify products at two prices
for a difference that is not a difference. This function models the merged state
ahead of the store: it rewrites variant keys (`RH|56` → `RH|56K` / `RH|56S`),
flattens the price to $99, and removes the merged product from `products.json`
entirely.

**It is the one place the overlay overrides Shopify rather than only adding to
it.** When the Shopify merge lands — the draft is built and waiting at
`carver-01-gold` — re-pull the catalogue, delete `merge` / `axisGrind` /
`priceAll` and the merged handle's overlay entry, and the function stops doing
anything. Every SKU is already carried verbatim through it: `52° S` is the real
`LGW02-52-RH`.

**Do not port this function.** Port the state it produces.

**The front-end cart.** `core.js` persists line items in `localStorage` under
`lg-cart-v1` and there is no checkout behind the button — the drawer says so.
Replace it wholesale with `/cart/add.js` and section rendering. The `[data-add]`
delegation contract (`data-sku`, `data-name`, `data-price`, `data-img`,
`data-variant`) is what the buy box, the quick-add panels, the lightbox and the
upsell rail all speak; keep the contract and swap what is behind it for a
variant id.

**The contact form.** Real `<form>` fields shaped for Shopify's contact form,
with a prototype notice **above** the fields and a submit handler that stops
navigation. It does not thank anyone for a message it never sent. Wire it to
`{% form 'contact' %}` and delete the notice.

**The review data.** Five verbatim Judge.me pulls in `_src/data/reviews/`. In a
theme these become the Judge.me app blocks. The widget itself
(`LG_REVIEWS.mount`) is worth keeping if you want the same histogram, star
filter, sort and paging on both the PDPs and the all-reviews page — that is why
it was extracted out of `pdp.js` in the first place.

> Two of the five pulls (the S grind and the LGP01) are Judge.me's **first
> page**, not distribution-preserving samples, so filtering them to a low star
> can legitimately show "No reviews at that rating in this sample" while the
> histogram shows the real spread. The widget says so rather than pretending.

---

## 12. What is not finished, and who owns it

Full detail and the checklist are in `FINISH-LINE.md`. In one paragraph each:

**Photography — the largest gap.** 26 stills and 36 video briefs, all written
into the copy files and extracted to `SHOT-LIST.md`, which is handable to a
photographer as-is. Every image slot on Our Story, the Ambassador Program and
the four club collections is currently a *labelled brief* — a `.ph` block that
states the crop, the light and what has to read in the frame. Video is lower
priority: a reel slot renders as a labelled card and a page with no footage
still reads as finished. Photography does not.

**The ambassador roster.** Five names, five handles, five 4:5 portraits, and the
program terms. The build **refuses** a real name on the roster without a
`consent` key.

**Three policy answers**, all rendering as `.tbd` chips across the four support
pages: duties prepaid at checkout or collected on delivery; staffed hours and an
email response target; the Returns Portal's URL. (Defective-item return shipping
was answered on 2026-08-02 — Lucky pays it.) The 57 "Needs spec" chips on the
product pages are the same device: a spec the manufacturer has not published,
shown as a visible gap rather than guessed at.

> On the response target specifically: there is deliberately no "we reply within
> N hours" anywhere on the site. The review corpus contains both a customer
> emailed back on a Sunday and one who waited weeks, and **a number nobody has
> committed to internally is worse than no number.**

**Sale was removed, not built** (2026-08-13). Shopify's "Summer Warehouse Sale"
collection holds six grip products plus three archived hats, and no variant
carries a real `compareAtPrice` — every value is `null` or `"0.00"`. Nothing on
the site ever linked to it, so the slug was dropped from `COLLECTIONS` rather
than built. **The Shopify collection still exists**; if you want a sale section
in the theme, it needs genuine compare-at prices *and* a menu entry, because the
old prototype had neither.

**Two discontinued products**, `lgd01` and `lgp02-patriot`, keep their catalogue
records (the pull is provenance) but are in no collection and have no page.

**One standing conflict worth knowing about:** the store's own Shopify FAQ page
claims a lifetime guarantee and says the wedge line is right-hand only. Both are
false, and both contradict Product Reference Guide v1.8. **This site follows the
refund policy.** That Shopify page needs retiring, not mirroring.

---

## 13. Port checklist

- [ ] Product metafields created for the editorial overlay (`template`,
      `family`, `code`, `title`, `finish`, `finishGroup`, `default`)
- [ ] Metaobjects for the family and template copy layers, with the fallback
      chain written explicitly in Liquid (§7)
- [ ] Three product templates, not one with branches
- [ ] `collection.clubs.json` separate from `collection.json`
- [ ] `variants.js` ported verbatim; `test-variants.js` kept running against the
      live catalogue
- [ ] Availability reads `variant.available` everywhere — grep for
      `inventory_quantity` and justify every hit
- [ ] Price repaints per variant on every selection
- [ ] No SKU on any merchandising surface; no `±` anywhere; no review count on
      any card
- [ ] Contrast: white on green only, foil never as type on white, `--lg-foil-tag`
      under any small text on a foil fill
- [ ] `--r` / `--r-card` applied by surface size, borders 2px, rules on grooved
      fields 2px
- [ ] Tap targets ≥44px, footer included — decide it deliberately
- [ ] Cart swapped to `/cart/add.js`, `[data-add]` contract preserved
- [ ] Contact form wired to `{% form 'contact' %}`, prototype notice deleted
- [ ] `merge_grinds()` state landed in Shopify and the function deleted, not
      ported
- [ ] Redirects for `10-collection-hybrid-driver.html`, `20-product-lgw02-*.html`
      and the two discontinued products
- [ ] `.tbd` device kept for every unanswered policy detail
- [ ] Swept at 1440 and 390, compositing rgba through ancestors, with foil
      checked by hand because tooling cannot see it

---

## 14. Where to read further

`HANDOFF.md` is the build log and the argument behind every decision above —
§7 for the contrast law and the homepage section order, §10 for the routing and
the data layer, §12 for the three PDP templates, §20–§22 for the collection
redesign and the PDP passes, §23–§24 for the wedge merge and the grind copy,
§25–§26 for the support cluster and the reference documents.

`FINISH-LINE.md` is the remaining work as a checklist, split by owner.

The four reference documents are the source of truth for facts and voice, in
this order of precedence: **Product Reference Guide v1.8** outranks everything
on product facts; **Spec-to-Benefit v1.0** governs what a spec is allowed to
claim and carries the CLAIMS TO AVOID list; **How We Write v7.3** governs voice;
**Golf-Culture Reference v2** supplies vocabulary. All 58 pages were audited
against the CLAIMS TO AVOID list — the site currently carries **zero banned
claims in its own copy**, with two flagged exceptions that are somebody else's
words: a Judge.me AI summary containing "premium", and competitor names inside
verbatim customer reviews.
