# Lucky Golf — the remaining pages  ·  brief for the next session

**Start here, then read `GAMEPLAN.md` and `HANDOFF.md`.** This file is the plan
for the ten pages that do not exist yet. Everything about how the site is built
— the templates, the build system, the copy rules, the traps — is in the other
two, and none of it should be re-derived.

```
python tools/build.py            # 49 pages
python tools/build.py --check    # diff against disk
python tools/build.py --links    # the registry: 61 declared, 49 built
python tools/normalize-products.py --check
node   tools/test-variants.js
```

---

## 1. Where the site stands

**53 of 61 pages.** Home, 8 collection pages, 40 product pages, and the four
support pages. Every sellable product has a page except the two discontinued
clubs.

**The support cluster is built** — see HANDOFF §25. Six pages remain:

| Slug | File | What it is |
|---|---|---|
| `story` | `30-story.html` | Our Story |
| `trybe` | `31-trybe.html` | The Trybe — ambassador program |
| `reviews` | `32-reviews.html` | All reviews, clubs-wide |
| ~~`returns`~~ | `40-returns.html` | **Built 2026-08-01** |
| ~~`shipping`~~ | `41-shipping.html` | **Built 2026-08-01** |
| ~~`contact`~~ | `42-contact.html` | **Built 2026-08-01** |
| ~~`faq`~~ | `43-faq.html` | **Built 2026-08-01** |
| `search` | `50-search.html` | Search results |
| `404` | `51-404.html` | Not found |
| `c/sale` | `10-collection-sale.html` | Sale — **blocked, see §6** |

Every one of them is already declared in `tools/sitemap.py` and already linked
from the footer and the header. The build reported **678 links resolving to
`#`**; the support cluster took it to **428**, and the rest is `trybe` (214),
`story` (160), `search` (53) and `reviews` (1). That number is the to-do list.

---

## 2. Cole's question: do the policy pages change?

**No — they do not exist yet.** There is nothing to change. What exists is the
*content*, already written from Product Reference Guide v1.8 and already
shipping inside modals on all 40 product pages:

- `#md-returns` — the real 60-day club policy, per category
- `#md-delivery` — shipping and dispatch

So building `returns` and `shipping` is **mostly lifting those modals into full
pages and expanding them**, not writing from scratch. The modal stays where it
is — a shopper in a buy box should not have to leave the page — and gains a
"Read the full policy" link into the new page. That link already exists in the
returns tab on all three templates and currently resolves to `#`.

**Two things in the modals still say "Needs confirming"** and want Cole before
the full pages go up:

1. **Warranty period**, and who pays return shipping on a defective item. (The
   general policy — customer pays return shipping — is confirmed and written.)
2. **Warehouse locations, international destinations, and whether duties are
   prepaid or collected.**

**What v1.8 does give you, verbatim and already reflected on the site:**

- 60 days on clubs; 30 on apparel and gear.
- All club returns need **approval and photo verification first**. Unauthorized
  returns are refused.
- **Putters** may be used, and must come back with no face marks, sole wear,
  scratches, dents, chips, bag chatter or grip wear. No regripping, bending,
  cutting.
- **Wedges** — one per order may be opened and tested **on a turf mat**, no
  groove wear. The rest stay factory sealed.
- **Hybrids** must appear completely unused.
- **Apparel** must be unworn, unwashed, tags on. **Without tags, $7 is
  deducted.** No makeup, deodorant, odors, pet hair, stretching, laundering.
- **Gear** must be unused.
- Customized items are final sale.
- Customer pays return shipping. Original shipping is not refunded.
- Refunds only after the item is received and inspected.
- Clubs: `support@luckygolf.com` or website chat. Apparel and gear: the Returns
  Portal.

---

## 3. Our Story (`30-story.html`)

**References:** HANDOFF §19 records what Cole sent for the club collection;
there are two story references noted in GAMEPLAN §5 that were never described.
**Ask Cole to re-send them, or describe them into HANDOFF before building** —
screenshots die at the session boundary and this has cost time once already.

**What is verifiable and can be said without asking anyone:**

- Shopify reports **at least 10,000 customers and 10,000 orders**. "Thousands of
  Lucky golfers" is confirmed copy (HANDOFF §7).
- **884 club reviews** across the line, 4.78 average. That figure is clubs-only
  and belongs inside a review context, not as a boast (§7).
- The price argument — no tour contracts, no middlemen — is **owned by the
  homepage's Why Lucky section** and must not be re-argued here (§7). Our Story
  is about who Lucky is, not why it is cheap.
- Cole personally handles customer problems: there is a real Judge.me review
  (January Z.) describing him texting a customer directly about a lost
  Christmas order. That is a story worth telling and it is verbatim evidence.

**Field order** must alternate ink/white/cream so no two dark bands touch, and
the brand field should land once mid-page — same law as every other page.

**Blocked on:** photography. Every image slot will be a labelled brief.

---

## 4. The Trybe (`31-trybe.html`)

The ambassador program. The homepage already has a **roster section with five
placeholder slots** (HANDOFF §7b G) that feeds this page, and it needs **five
4:5 portraits plus real names and handles**. Names are bracketed, never
invented.

**Needs from Cole before this can be more than a shell:**

- Who the ambassadors actually are — names, handles, headshots.
- What the program gives and what it asks. Discount? Commission? Product?
- How someone applies, and where that form goes.

**Do not invent program terms.** An ambassador page that describes a commission
structure nobody agreed to is worse than a page that says "applications open
soon". If the terms are not available, build the page around the roster and the
brand, with the application as a single clear CTA into `contact`.

---

## 5. Reviews (`32-reviews.html`)

This page exists because the homepage's **"Read all 884 reviews"** has to land
somewhere, and 884 is the clubs-wide count so it cannot point at any single
PDP's review block (HANDOFF §10a).

**The data is already in the repo.** `_src/data/reviews/` holds five real
Judge.me pulls:

| Product | Live | Pulled |
|---|---|---|
| Carver 01 Gold | 551 | 47 |
| Tracer LGP01 Blade | 147 | 22 |
| Carver 01 Gold (S grind, pre-merge) | 69 | 30 |
| Tracer LGP02 Mallet | 58 | **all 58** |
| Stryker LGH01 | 20 | **all 20** |

The review widget on the club template already does filtering, sorting, a
histogram and pagination — **reuse it, do not rebuild it.** This page is that
widget over the union of all five sets, plus a product filter.

**Note:** the 69 S-grind reviews are attached to a Shopify product that is being
merged into the 01 (HANDOFF §23). After the merge and a Judge.me migration the
01's count becomes 620 and the clubs-wide total stays 884.

The widget is deliberately **not** 4-star-and-up. The 4★ floor governs curated
pull quotes only; a widget that hides its 1-stars is a widget nobody believes
(§9).

---

## 6. The support cluster — one template, four pages  ·  **DONE 2026-08-01**

**Built. HANDOFF §25 is the record and supersedes this section.** What follows
is the brief it was built from, kept because it explains the shape.

`returns` · `shipping` · `contact` · `faq`

**Build these as one template**, the way the three PDP templates work. They
share a shape: a title, a lede, a body of sectioned prose, and a "still stuck?"
CTA. Only the body differs.

- **Returns** and **Shipping** — §2 above. The content is written; this is
  lifting and expanding.
- **Contact** — the highest-value of the four, because **the fitting CTA on all
  four club collection pages points at it** and currently goes nowhere. Needs
  the real support channels: `support@luckygolf.com` is confirmed in v1.8;
  website chat is mentioned; anything else needs Cole.
- **FAQ** — write it from the questions the reviews actually ask. There are
  real ones in the pulled data: *"I'm 5'9", is a 35-inch putter right for me?"*
  (James, LGP02) and repeated left-hand availability questions on the LGP01.
  An FAQ built from real customer questions beats an invented one.

**Note the naming trap:** `_src/data/copy/_shared-<template>.json` is the
merge layer under family files (§22b). A support template would use the same
mechanism.

---

## 7. Search and 404

Both are small and both are real pages a Shopify theme needs.

- **Search** — a results template. The catalogue is in `products.json`, so a
  client-side search over 43 products is genuinely useful in this prototype and
  demonstrates the pattern. Include the empty state.
- **404** — the brand's one chance to be funny. Reuse the PLP's empty-state
  shape and the clover mark.

---

## 8. Sale (`c/sale`) — blocked, and has been since Phase B

`c/sale` is declared, routed, and **deliberately not built**. Its nine Shopify
members are six grips plus three archived hats, and **not one carries a real
`compareAtPrice`** — every value is `null` or `"0.00"`. The only product in the
store with a genuine was-price is `stock-putter-grips` ($19.95 from $30.00), and
it is **not in the collection**.

Building it today puts six full-price grips under a heading that says Sale.

**It builds the moment `blocked` comes off the collection in
`normalize-products.py`** — which needs Cole to either price the collection or
drop Sale from the nav. Nothing else is required.

---

## 9. Phase G — the developer handoff document

The last deliverable, and the reason the build is shaped the way it is. It maps
each of our pages onto the Shopify template that will replace it:

| Ours | Shopify |
|---|---|
| `_src/page-home.html` | `templates/index.json` |
| `_src/page-clp.html` | `templates/collection.clubs.json` |
| `_src/page-plp.html` | `templates/collection.json` |
| `_src/page-club.html` | `templates/product.club.json` |
| `_src/page-apparel.html` | `templates/product.apparel.json` |
| `_src/page-gear.html` | `templates/product.gear.json` |

`tools/template.py` was written Mustache-shaped **specifically so `{{#x}}`
maps onto Liquid's `{% for %}` and `{% if %}` legibly** (§12a). Say so in the
doc.

**The handoff doc must carry these, because a developer will otherwise
reintroduce every one:**

- The green-field contrast law (§7). Cream and gold both fail on the brand
  field. This is measured, not aesthetic.
- **Foil is illegal on white** as *type*, and the contrast sweep cannot catch
  it (§9). As a *fill* it is fine, but small text needs `--lg-foil-tag`, not
  the full ramp — ink on `--gold-lo` is 3.64:1 (§23f).
- Radius follows the **size of the surface**, not the type of component (§13.6).
- A product card **never** shows a review count (§16 note 2).
- **No manufacturer tolerances** anywhere (§22e).
- **No SKU renders anywhere** (§22d).
- SKUs are **never synthesised** (§10c). Several are genuinely irregular.
- `availableForSale` is **not** `inventoryQuantity > 0` (§10c).
- Every price is **per variant** (§10c).

---

## 10. What is blocked on Cole, across all ten pages

Ordered by how much it holds up:

1. **Photography.** Every apparel and collection image is a written brief. This
   is the largest gap on the site and it blocks Our Story and Trybe more than
   anything else, because those pages are *made of* photography.
2. **Trybe roster** — five names, five handles, five 4:5 portraits, and the
   program terms.
3. **Our Story references** — Cole sent them; they were never described into
   HANDOFF and the screenshots are gone.
4. **Warranty period** and **warehouse/duties**, the two "Needs confirming"
   chips in the policy modals — now also chips on the returns and shipping
   pages. Two more surfaced building Contact: **staffed hours and a response
   target**, and **the Returns Portal's URL** (§25f).
5. **Sale** — price the collection or drop it from the nav.
6. **The Shopify wedge merge**, and the Judge.me migration behind it (§23h).
7. **Sign-off on the grind copy** — the only unverified block on the site
   (§23d).

---

## 11. Two rules that have each cost a session

**Resize the browser pane before auditing anything.** It reports
`innerWidth: 0` until `resize_window` is called, and every sweep run before
that returns confident nonsense. Sweep at **1440 and 390**, compositing rgba
through ancestors. Known false positives: gradients, decorative SVG, and
`.stretch` (its hit area is a tile-wide `::after`).

**A smoke marker must exist in exactly ONE source file.** `REQUIRED` in
`build.py` is the only thing standing between a silent bundling mistake and a
page that looks right and does nothing — and it has been defeated twice by a
marker string that also appeared somewhere else (§21i). Grep the tree before
adding one, and verify every new guard by breaking it on purpose.
