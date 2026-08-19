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

### 1c. Send the Product Language Rules document

The fifth reference doc. `references-product-guide-v1.8.md` and the
Spec-to-Benefit guide both point at it, and Golf-Culture Reference v2 names
three CTAs it defines — **"Go get one", "Roll it pure", "Fill the gap"** —
which "stay locked to their products" as recognisable brand markers.

Without the mapping, only "Fill the gap" is in use (on the hybrid), and only
because it also appears independently in Culture v2's Long-game vocabulary.
"Go get one" and "Roll it pure" are unused rather than guessed at.

**Unblocks:** the product-specific CTA layer, and confirmation that "Fill the
gap" is on the right club.

---

## Round 2 · Shopify — about an hour, and it retires a temporary hack

### 2a. Finish the wedge merge

The draft is built and waiting:
https://admin.shopify.com/store/lucky-wedges/products/9583978905877

1. **Move stock onto the six S-grind variants.** They are at zero, so they read
   sold out. From the live LGW02 Gold: RH 52° **38**, RH 56° **25**,
   RH 60° **2**, LH 52° **94**, LH 56° **92**, LH 60° **70**.
2. **Publish the draft.**
3. **Archive `v1-gold-lucky-golf-wedge` and `v2-signature-gold-wedge-1`.**
4. **Migrate the Judge.me reviews** — the S grind's 69 onto the 01, so it reads
   **620** and the clubs-wide total stays 884.

⚠️ **Inventory is double-counted until step 3.** Shopify's duplicate carried the
K-grind quantities across, so the draft holds 2,524 units that also still sit on
the live product. Nothing can sell — it is unpublished — but store-wide
inventory totals are inflated until the old products are archived.

### 2b. Then, on the site side (me)

Once 2a lands, three things get deleted rather than written:

- Re-pull the catalogue.
- Delete `merge` / `axisGrind` / `priceAll` and the merged handle's overlay
  entry from `normalize-products.py`. **`merge_grinds()` is the one place the
  overlay overrides Shopify rather than adding to it** (HANDOFF §23b) and it is
  explicitly temporary. It stops doing anything.
- The reviews page's S-grind chip disappears, and the 01 reads 620.

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
- [ ] Retire or rewrite the Shopify FAQ page (it contradicts the refund policy)
- [x] ~~Chat hours + email response target~~ — 24 business hours; chat = email hours, Mon–Fri
- [x] ~~Returns Portal URL~~ — lucky-golf.loopreturns.com, apparel route only
- [ ] Product Language Rules sent
- [ ] Stock moved onto the six S-grind variants
- [ ] Draft published
- [ ] Both old wedge products archived
- [ ] Judge.me reviews migrated (01 reads 620)
- [x] ~~Trybe roster~~ — roster killed 2026-08-13; open program, no names needed
- [x] ~~Trybe program terms~~ — on the page 2026-08-13, all Cole's
- [ ] 51 stills shot (`SHOT-LIST.md`, 4 sessions — 23 of them unblock every apparel page)
- [ ] 5 product films + 36 reel clips (lower priority)

**Build side**

- [x] ~~Sale page built, or the slug retired~~ — slug retired 2026-08-13
- [x] ~~Four policy chips replaced with real answers~~ — all four support pages at ZERO chips
- [ ] Catalogue re-pulled, `merge_grinds()` deleted
- [ ] Reviews page: S-grind chip removed, 01 reads 620
- [ ] Product-specific CTAs applied from Product Language Rules
- [x] ~~Roster names and portraits in~~ — obsolete; roster removed, block dormant
- [ ] Photography dropped into the 26 still slots
- [x] ~~Developer handoff document written~~ — `DEVELOPER-HANDOFF.md` (2026-08-13)
- [x] ~~Footer tap targets — decided either way~~ — fixed 2026-08-13, desktop 16px → 24px
- [ ] Final sweep at 1440 and 390, all pages
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
