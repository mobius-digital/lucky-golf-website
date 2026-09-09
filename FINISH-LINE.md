# Lucky Golf — the finish line

**58 of 60 pages built. Zero dead links.** Live at
https://mobius-digital.github.io/lucky-golf-website/

**Cole's running order, set 2026-08-13:**

1. **Layouts** — finish every page's structure. *Effectively done; see below.*
2. **Copy revisions** — a SEPARATE chat, page by page, Cole reacting to each.
3. **Photography** — `SHOT-LIST.md`, 51 shots. Last, so nothing is shot for a
   layout that then changes.
4. **The wedge merge** — the Shopify job, whenever he says go.

Photography is deliberately last: shooting 51 images against a layout that is
still moving is the expensive mistake, and the pages read as finished with
labelled briefs in the meantime.

This file is the plan for closing out the remaining work. Nothing below is
discovery — every item is a known, scoped gap.

---

## Round 1 · Fifteen minutes, and it unblocks the most

Three answers. None needs research, all three are decisions or documents that
already exist somewhere.

### 1a. Sale — CLOSED 2026-08-13. Dropped.

Cole: *"That was a long time ago."* The slug is removed from `COLLECTIONS` in
`normalize-products.py`.

Re-verified against the live store before removing it: the Shopify "Summer
Warehouse Sale" collection still holds six grip products plus three **archived**
hats, and **not one variant carries a real `compareAtPrice`** — every value is
`null` or `"0.00"`. One of the six grips is sold out entirely. A page headed
Sale showing six full-price grips is a lie.

**The brief was wrong about one thing:** it said "drop Sale from the nav." There
was no nav entry. Nothing on the site ever linked to Sale — no `{{link:c/sale}}`
token anywhere in `_src/` — so it was a declared slug nobody could reach, not an
advertised collection. Removing it changes **no page's output**; all 58 rebuild
byte-identical. It only stops the registry counting a page that could not exist.

The Shopify collection itself is untouched. **To bring Sale back** for a real
promotion: re-add the dict, set genuine compare-at prices in Shopify, and add a
nav or footer entry — without one the page builds and stays unreachable.

**Registry: 61 pages → 60. Still 58 built, still zero dead links.**

### 1b. The four policy answers

All four currently render as dashed "Needs confirming" chips. The pages are
built around them, so answering turns a chip into a sentence and nothing else
moves.

**ANSWERED 2026-08-02 — three of the four are closed:**

- **Defective items: Lucky pays the return shipping.** Now stated on the refund
  policy page and in the FAQ.
- **The refund policy is the truth, not the FAQ page.** The store's own FAQ page
  claims a lifetime guarantee and says the line is right-hand only — both false.
  That page needs retiring on Shopify; this site follows the refund policy.
- **International: yes, worldwide, rate at checkout.** Was a chip, now an answer.

**ALL CLOSED 2026-08-13. The four support pages now carry ZERO chips.**

| Was open | Answer |
|---|---|
| Duties — prepaid or collected | **Neither. Not relevant, and off the site entirely.** Removed from the shipping page, the FAQ and the delivery modal on all 40 product pages. |
| Chat hours, email response target | **Email: within 24 business hours**, written as an aim rather than a promise. **Chat: no separate hours** — same as email, Monday to Friday, same team. |
| The Returns Portal's URL | **https://lucky-golf.loopreturns.com/** — linked on the APPAREL route only. |
| Warranty after the window | **No lifetime warranty. Sixty days is the whole written policy.** A fault after that is case by case. |

**The portal link has a rule attached to it (Cole, 2026-08-13):** apparel and
gear go to the portal; **clubs go through support first**, so a fault is caught
before the club is in a box. Do not add the portal link to a club route. It
appears exactly twice on the site — the refund policy and Contact — and on no
club page.

**One thing the duties removal buries:** shipping *from* the US does not stop a
destination country charging the customer import duty on delivery. The site now
says nothing about it. Cole's call, made knowingly.

### 1c. The Product Language Rules document — DROPPED 2026-09-09

Cole: *"I don't want to lock certain headlines. I don't know where we're
getting that."* The doc the reference guides pointed at does not exist and the
idea behind it is dead: no CTA or headline is locked to a product. "Fill the
gap" stays on the hybrid because it is good copy for that club, not because a
rulebook assigned it. Write each product's CTA on its merits, same as any
other line. If a future reference doc revives "locked" product language,
this ruling wins.

---

## Round 2 · Shopify — DONE 2026-09-05 except the Judge.me migration

### 2a. The wedge merge — LIVE 2026-09-05

Steps 1–3 happened: the merged **Lucky Golf LGW02 Gold**
(`lucky-golf-lgw02-gold`, Hand × "Loft & Grind", 18 variants) is ACTIVE at
**$99 flat** (Cole confirmed the price 2026-09-09), and both old Gold products
went DRAFT. No double-counting on the storefront.

⚠️ **Step 4 has NOT happened, and it is now urgent: the live merged product has
ZERO Judge.me reviews.** Verified 2026-09-09 via the product's `judgeme`
metafields — "No reviews", count 0. The flagship wedge on luckygolf.com says
"Be the first to write a review".

**But it is not a per-product review migration, and that changes the fix and
the number.** Judge.me on this store pools reviews through **static product
review groups**. The relevant one is **"All Gold Wedges"** (group id `241751`):
27 products, **563 reviews, 4.82**. That pool is where the 551 on the old
product page came from — those reviews were never attached to the product
itself. The merged product is simply **not a member of the group**.

**The fix, one action, Cole's to do by hand:** Judge.me app → Settings →
Product groups → *All Gold Wedges* → Edit → **Add products manually** → search
"LGW02 Gold" → tick *Lucky Golf LGW02 Gold* → **Add**. Then **Refresh all
Groups** (otherwise groups repropagate on a daily ~03:00 schedule).

**Then re-derive the site's numbers from the group, do not assume 620.** 620
was arithmetic for a per-product migration that is not how this store works.
Read the group total after the refresh and rebuild `_page-reviews.json` from
it.

*Why this is not automated — tried and failed 2026-09-09.* The Judge.me admin
is a cross-origin iframe inside Shopify admin, invisible to the accessibility
tree, so it is screenshot-coordinate clicking only. The dialog opens, the
search works and the row ticks, but **the Add button never commits** — verified
by re-reading the group afterwards: still 27 products, 563 reviews, 4.82, and
the storefront badge still 0. About half of all clicks silently fail, and two
strayed onto Shopify's own nav. The group edit page carries a **Delete** button
beside the click target, and deleting that group would destroy the pooling for
563 reviews. Not worth the risk for a 30-second manual task. Nothing was
changed by the attempt.

### 2b. The site side — DONE 2026-09-09

- Catalogue re-pulled (wedges): `shopify-raw.json` now carries the merged
  product; the two old records are gone.
- `merge` / `axisGrind` / `priceAll` and the overlay hack deleted.
  `merge_grinds()` is now `grind_axis()` — only the Black's cosmetic combined
  axis survives, and **nothing in the overlay overrides Shopify any more.**
- The reviews page's S-grind chip **stays until the Judge.me migration lands**,
  by the page's own recorded rule (`_page-reviews.json` `_merge`): summing two
  review sets into a 620 no system reports would be inventing a figure. Flip it
  the day Judge.me reads 620.

---

## Naming — SETTLED 2026-09-09, and the store now matches the site

Cole: *"What do you think and do it."*

**The site keeps "Carver 01 Gold" and "Carver 01 Black". Shopify was renamed to
match.** Both live product titles now read exactly that. Handles are untouched,
so no URL moved and nothing 404s.

**Why this direction and not the other.** "Carver 01" appears **406 times on the
built pages**. Renaming the site to 02 would be a 400-change rewrite of the
flagship product's identity days before handoff. The store title was a leftover
from the merge, changed in one call. Fix the cheap end.

It is also the coherent end. The site's wedge story (Cole, 2026-07-31, locked)
is *one wedge, the 01, in gold or black, with your pick of sole grind* — which
is exactly what the merged product now is: one club, K and S as variants. The
roadmap line "the true 02 is coming" keeps meaning a genuinely new wedge.

⚠️ **The one thing to check, because two of your own rulings disagree.**
2026-07-31: one wedge, *the 01*, grind is a variant. 2026-09-05, on the merge:
*"instead of 01 and 02 it's just 02."* I went with the 01 because the whole site
is built on it and the merged club contains the old 01 head. **If you meant 02
is the name customers see, say so and it flips: two Shopify renames and three
lines in `normalize-products.py`.** Cheap now, expensive after the copy is
reprinted anywhere.

### Two follow-ons this created

- **The rest of the catalogue still carries legacy store titles** ("Lucky Golf
  LGP02 Gold", "Lucky Golf LGH01") while the site says "Tracer LGP02 Mallet",
  "Stryker LGH01". Rename the lot in one sweep at launch so the store is not
  half-renamed. Do not drip-feed it.
- **The live BOGO page's wedge upsell card still shows the old name.** It bakes
  product titles at publish time and `refreshCatalogue()` only self-heals the
  hats. `shopify/build_page.py` is fixed and `shopify/page-body.html` rebuilt,
  but pushing it means replacing the whole 62KB page body by hand, which is a
  corruption risk on a live page for a cosmetic label. **Push it with the next
  deliberate republish**, not bundled into an unrelated batch.

---

## Round 3 · The long poles — other people are involved

### 3a. Photography — the biggest gap on the site

**51 stills**, in `SHOT-LIST.md`, which is handable to a photographer as-is:
every entry names the crop, the light and what has to read in the frame, grouped
into four shoot sessions rather than by page.

**The old count of 21 was wrong.** That file was generated from the copy files
and missed all 23 apparel heroes, the 8 homepage slots and the tees flat-lay.
It is now generated from the 58 built pages, so it cannot drift again.

| Session | Shots | |
|---|---|---|
| A · Course day, the clubs | 14 | 13 shootable; the 02 cutout needs a club that does not exist |
| B · Apparel day, on body | 23 | **unblocks 23 pages at once** — the biggest single win |
| C · Brand + lifestyle | 13 | Our Story, the Ambassador page, 8 homepage slots |
| D · Studio flat-lay | 1 | the tees — the only product with no Shopify photo at all |

Video is lower priority and separate: 5 product films plus 36 short-form reel
briefs. Every reel slot already renders as a labelled card and a page with no
footage still reads as finished. Photography does not.

### 3b. The Ambassador Program — RESTRUCTURED AND CLOSED 2026-08-13

Cole killed the five-slot roster: the program is **open to anyone who meets the
criteria**, and a lineup of five faces said the opposite. The grid is off both
pages, and the terms are now ON the page, all Cole's: clubs to play (specifics
travel in the acceptance email, deliberately), a private group chat, first look
at drops and events, reposts — and **nobody paid per sale, stated as brand
proof**. The 10%/AvantLink affiliate block is off the page at his instruction;
the commission test continues quietly on the Trybe platform, off-site.

A named roster returns only when there are big, real names — the dormant block
in `page-brand.html` still enforces `consent` keys when that day comes.

---

## Round 4 · DONE — `DEVELOPER-HANDOFF.md` (2026-08-13)

### The developer handoff document

**Written. It is `DEVELOPER-HANDOFF.md` at the repo root**, fourteen sections:
how to run the build, the repo map, the pipeline and what happens to each half
of it in a theme, the page→template map, what each template is made of, a
Mustache→Liquid conversion table, **how the three-layer editorial merge has to
be rebuilt in Liquid** (metafields plus metaobjects, with the fallback chain
written out — Liquid has no merge), the catalogue traps, the design laws with
their measured numbers, the build guards, what is temporary and must be deleted
rather than ported, what is still open and who owns it, and a port checklist.

Everything below is what it had to carry, kept here as the record of the brief.

It maps each of our pages onto the Shopify template that replaces it:

| Ours | Shopify |
|---|---|
| `_src/page-home.html` | `templates/index.json` |
| `_src/page-clp.html` | `templates/collection.clubs.json` |
| `_src/page-plp.html` | `templates/collection.json` |
| `_src/page-club.html` | `templates/product.club.json` |
| `_src/page-apparel.html` | `templates/product.apparel.json` |
| `_src/page-gear.html` | `templates/product.gear.json` |
| `_src/page-support.html` | `templates/page.contact.json` and three more |
| `_src/page-brand.html` | `templates/page.json` |
| `_src/page-reviews.html` | `templates/page.reviews.json` |
| `_src/page-search.html` | `templates/search.json` |
| `_src/page-404.html` | `templates/404.json` |

It has to carry the rules a developer will otherwise reintroduce one by one:

- The green-field contrast law — cream and gold both fail on the brand field.
  Measured, not aesthetic.
- **Foil is illegal on white as type**, and the contrast sweep cannot see it.
  Small text on a foil fill needs `--lg-foil-tag`, not the full ramp.
- Radius follows the **size of the surface**, not the type of component.
- A product card **never** shows a review count.
- No manufacturer tolerances. No SKU renders anywhere.
- **SKUs are never synthesised** — several in this store are genuinely irregular.
- `availableForSale` is **not** `inventoryQuantity > 0`.
- Every price is **per variant**.
- `tools/template.py` was written Mustache-shaped specifically so `{{#x}}` maps
  onto Liquid's `{% for %}` and `{% if %}` legibly. Say so.

Currently this exists only as a table inside `NEXT-PAGES.md` §9. It should be
its own document, because it is what ships with the repo.

---

## The bug the sweep caught (fixed 2026-09-09)

**The tees page's Add to cart did nothing, and had not for some time.**

`_src/pdp.js` built the gallery thumbnails with
`s.querySelector('img').getAttribute('src')` on every slide, assuming a slide
is always a photograph. The tees are the one product in the catalogue with **no
Shopify photo at all**, so its only slide is a labelled placeholder with no
`<img>`. That threw a TypeError.

The throw is the point. It happened near the top of the PDP's main IIFE, so
**everything after it never ran** — variant selection, price repainting, and
the `[data-add]` wiring. The page looked completely finished and the button was
inert. Nothing in the build could see it: the HTML was correct, so `--check`,
`--links` and `test-variants.js` all passed. Only loading the page in a browser
and reading the console found it.

Fixed by skipping slides that have no image, with the thumbnail carrying the
**slide index it belongs to** rather than its own position, so a skipped
placeholder cannot put every later thumbnail on the wrong slide. Verified: the
wedge PDP still builds 13 thumbs for 13 slides, indices 0-12 aligned; the tees
page builds none and now wires `TEES-25` correctly.

**Worth knowing for the photo shoot:** this is exactly the failure a page hits
when a product has zero images. Any new product added before its shoot would
have hit it too.

---

## Deferred — real, but not blockers

- ~~**Footer links are 16px tap targets**~~ — **FIXED 2026-08-13.** The note
  overstated it: the phone rule has given them 44px since Phase 1, so the gap
  was only ever the POINTER target on desktop. Measured 16×98.7 with ~11px of
  dead gap between rows; now **24×205.7**, gap moved inside the target. Footer
  is 41.5px shorter and the rows are a 25px pitch instead of ~36px — the one
  visible change, and the reason it needed a decision rather than a patch.
- **The Judge.me AI summary says "premium"** on the 01 Gold — a word the
  Spec-to-Benefit guide bans. It is Judge.me's auto-generated text, published
  verbatim by standing decision. Yours to disable, not to edit.
- **Homepage review quotes name Vokey, Cleveland and Odyssey.** All inside
  verbatim customer reviews, so not Lucky comparing itself by name — but
  *choosing* those quotes is arguably the comparison by proxy.
- **The `lucky-golf-copy` skill still ships How We Write v6**, not v7.3, and its
  returns-copy example ("you don't pay return shipping") contradicts v1.8.

---

## The checklist — done when every box is ticked

**Cole**

- [x] ~~Sale priced, or dropped from the nav~~ — dropped 2026-08-13
- [x] ~~Defective returns — Lucky pays the shipping~~ (answered 2026-08-02)
- [x] ~~Duties~~ — not relevant; removed from the site entirely (2026-08-13)
- [x] ~~Retire or rewrite the Shopify FAQ page~~ — **rewritten and live
      2026-09-09** (page 21570027591, handle `faq-lucky-wedges`, title now
      "FAQ"). Killed: the lifetime guarantee, the Vokey and Cleveland
      comparison, "we only offer right handed", the dead luckywedges.com
      address, the Re:Do upsell and a wrong shaft weight. Now matches the
      refund policy and the hand availability in `products.json`.
- [x] ~~Chat hours + email response target~~ — 24 business hours; chat = email hours, Mon–Fri
- [x] ~~Returns Portal URL~~ — lucky-golf.loopreturns.com, apparel route only
- [x] ~~Product Language Rules sent~~ — dropped 2026-09-09; Cole doesn't want
      locked headlines, the doc never existed
- [x] ~~Stock moved onto the six S-grind variants~~ — synced 2026-09-05
- [x] ~~Draft published~~ — ACTIVE 2026-09-05, $99 flat
- [x] ~~Both old wedge products archived~~ — DRAFT 2026-09-05 (do not republish)
- [ ] **URGENT: add the merged wedge to the "All Gold Wedges" Judge.me group**
      (id 241751) — it shows ZERO reviews on the live site because it is not a
      member. Then Refresh all Groups. See Round 2a
- [x] ~~Trybe roster~~ — roster killed 2026-08-13; open program, no names needed
- [x] ~~Trybe program terms~~ — on the page 2026-08-13, all Cole's
- [ ] 51 stills shot (`SHOT-LIST.md`, 4 sessions — 23 of them unblock every apparel page)
- [ ] 5 product films + 36 reel clips (lower priority)

**Build side**

- [x] ~~Sale page built, or the slug retired~~ — slug retired 2026-08-13
- [x] ~~Four policy chips replaced with real answers~~ — all four support pages at ZERO chips
- [x] ~~Catalogue re-pulled, `merge_grinds()` deleted~~ — 2026-09-09; only the
      Black's cosmetic `grind_axis()` remains
- [ ] Reviews page: S-grind chip removed, count re-derived from the "All Gold
      Wedges" group total (NOT the assumed 620) — BLOCKED on the group fix
      above; flipping early would invent a figure
- [x] ~~Product-specific CTAs applied from Product Language Rules~~ — obsolete;
      no locked product language (Cole, 2026-09-09)
- [x] ~~Roster names and portraits in~~ — obsolete; roster removed, block dormant
- [ ] Photography dropped into the 26 still slots
- [x] ~~Developer handoff document written~~ — `DEVELOPER-HANDOFF.md` (2026-08-13)
- [x] ~~Footer tap targets — decided either way~~ — fixed 2026-08-13, desktop 16px → 24px
- [x] ~~Final sweep at 1440 and 390, all pages~~ — **done 2026-09-09.** All 61
      pages measured in-browser at 1440 and 390 (and the first 21 at 320):
      **zero horizontal overflow anywhere.** The compare table scrolls inside
      its own box as designed. Em dashes in visible copy: **0**. Banned-word
      sweep: 9 hits, all previously accepted (competitor names inside verbatim
      customer reviews, "premium" in the Judge.me auto-summary, styleguide
      specimens). Voice audit exits clean.
      **It also caught a real bug — see below.**
- [ ] `python tools/build.py --check` clean
- [ ] `node tools/test-variants.js` passes
- [ ] `python tools/build.py --links` reports 60 of 60, zero dead links

**Then it is finished.**

---

## Where the copy pass stands (2026-08-18)

The copy chat (HANDOFF §36) has closed out the **homepage** (seven revisions)
and the **Carver 01 Gold PDP** (three revisions, including the Takomo-shaped
description and the three-card spec layout), plus four site-wide rulings: no
em dashes, Space Mono removed (Archivo only), "Free US shipping" off every
page, "never through a middleman" off every product marquee. The nav was
rebuilt (Takomo-style mobile accordion with two-up product cards; the
"Black is right hand" aside deleted from every dropdown).

**Pages still to pass, in order:** Carver 01 Black (template changes landed,
per-product copy did not; ~15 min) → the two putters → the hybrid → the clubs
collection → one polo, one hat (family copy covers the rest) → gear + the
other collections → Our Story, Ambassador, Reviews → the four support pages.

## Starting the next chat

Paste this:

> Continuing Lucky Golf in `C:\Users\wetzl\Lucky Golf\Website`.
> Read `FINISH-LINE.md` first, then `HANDOFF.md` §36 (the copy pass so far)
> and §26 (the state of the site).
>
> This chat is copy revisions, page by page, Cole reacting to each. Layouts
> are locked unless I say otherwise. Start with the **Carver 01 Black**
> (`20-product-lgw01-black.html`): bring its description, spec cards and grind
> handling in line with the Gold (HANDOFF §36c), then move to the **putters**.
> Link me the built page each time so I can react.

**Read in this order, and don't re-derive what's in them:** `FINISH-LINE.md`
(this file) → `HANDOFF.md` §36 (the copy rulings and the PDP shape) → §26
(the state of the site) → §23 / §25 only if the wedge merge comes up.
`GAMEPLAN.md` and `NEXT-PAGES.md` are history rather than plan.
