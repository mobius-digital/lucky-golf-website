# Lucky Golf — the finish line

**58 of 61 pages built. Zero dead links.** Live at
https://mobius-digital.github.io/lucky-golf-website/

This is the plan for closing out the remaining work, ordered so the cheap things
that unblock the most happen first. Nothing below is discovery — every item is
a known, scoped gap.

---

## Round 1 · Fifteen minutes, and it unblocks the most

Three answers. None needs research, all three are decisions or documents that
already exist somewhere.

### 1a. Sale — price it, or drop it

The last unbuilt page. Nine products sit in the Shopify Sale collection — six
grips and three archived hats — and **not one carries a real `compareAtPrice`**.
Every value is `null` or `"0.00"`. Building it today puts six full-price grips
under a heading that says Sale.

Two ways to close it:

- **Price the collection.** Set a genuine compare-at price on the members you
  want discounted, and the page builds with no other change.
- **Drop Sale from the nav.** One line in `normalize-products.py`, and the
  header stops advertising a collection that isn't one.

*(The only product in the whole store with a real was-price is
`stock-putter-grips`, $19.95 from $30.00 — and it is not in the collection.)*

**Unblocks:** the 59th page, or a cleaner nav.

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

| Still open | Where it shows |
|---|---|
| Duties — prepaid at checkout or collected on delivery | `41-shipping.html#where` |
| Staffed hours for chat, and a response target for email | `42-contact.html#when` |
| The Returns Portal's URL | Contact and the refund policy describe it instead of linking |

**On the response target specifically:** there is deliberately no "we reply
within N hours" anywhere on the site. The review corpus contains both a
customer emailed back on a Sunday and one who waited weeks. A number nobody has
committed to internally is worse than no number — so this one is a decision to
make, not a fact to look up.

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

**26 stills and 36 video briefs**, all already written into the copy files and
extracted to **`SHOT-LIST.md`**. That file is handable to a photographer as-is:
every entry names the crop, the light and what has to read in the frame.

The stills are what block pages. The 26 break down as:

- **Our Story** — 4 (a 21:9 hero, a macro of a milled face, a lifestyle shot, and
  a portrait of you working)
- **The Trybe** — 6 (five 4:5 roster portraits plus a lifestyle shot)
- **The four club collections** — 9 landscape 4:3 story shots
- **Product hero panels** — 5 full-bleed portraits
- **The 02** — 1 studio cutout, whenever that club is real

Video is lower priority: every reel slot already renders as a labelled card, and
a page with no footage still reads as finished. Photography does not.

### 3b. The Trybe roster

Five names, five handles, five 4:5 portraits, and **what the program gives and
asks** — discount, commission, product, or some combination.

Nothing on that page invents terms today, and the build will **refuse** a real
name on the roster without a `consent` key. The same five slots sit on the
homepage, so one answer fills both.

---

## Round 4 · One build task left, and it is not blocked

### The developer handoff document

Always the final deliverable, and the reason the build is shaped the way it is.
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

- **Footer links are 16px tap targets** on all 59 pages. Pre-existing, in the
  shared partial, and fixing it touches the whole site.
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

- [ ] Sale priced, or dropped from the nav
- [x] ~~Defective returns — Lucky pays the shipping~~ (answered 2026-08-02)
- [ ] Duties — prepaid at checkout, or collected on delivery
- [ ] Retire or rewrite the Shopify FAQ page (it contradicts the refund policy)
- [ ] Chat hours + email response target
- [ ] Returns Portal URL
- [ ] Product Language Rules sent
- [ ] Stock moved onto the six S-grind variants
- [ ] Draft published
- [ ] Both old wedge products archived
- [ ] Judge.me reviews migrated (01 reads 620)
- [ ] Trybe roster — 5 names, 5 handles, 5 portraits
- [ ] Trybe program terms
- [ ] 26 stills shot (`SHOT-LIST.md`)
- [ ] 36 video clips shot (lower priority)

**Build side**

- [ ] Sale page built, or the slug retired
- [ ] Four policy chips replaced with real answers
- [ ] Catalogue re-pulled, `merge_grinds()` deleted
- [ ] Reviews page: S-grind chip removed, 01 reads 620
- [ ] Product-specific CTAs applied from Product Language Rules
- [ ] Roster names and portraits in, `consent` keys set
- [ ] Photography dropped into the 26 still slots
- [ ] Developer handoff document written
- [ ] Footer tap targets — decided either way
- [ ] Final sweep at 1440 and 390, all pages
- [ ] `python tools/build.py --check` clean
- [ ] `node tools/test-variants.js` passes
- [ ] `python tools/build.py --links` reports 61 of 61, zero dead links

**Then it is finished.**

---

## Starting the next chat

Paste this:

> Continuing Lucky Golf in `C:\Users\wetzl\Lucky Golf\Website`.
> Read `FINISH-LINE.md` first, then `HANDOFF.md` §23–§26.
>
> The site is built and live: 58 of 61 pages, zero dead links, published at
> https://mobius-digital.github.io/lucky-golf-website/ from a public GitHub
> repo (`mobius-digital/lucky-golf-website`, master, GitHub Pages).
>
> `FINISH-LINE.md` has the remaining work as a checklist. Start with
> **Round 4 — the developer handoff document** — it is the one task that is not
> blocked on me.
>
> Answers to Round 1, if I have them by then: [paste here]

**Read in this order, and don't re-derive what's in them:** `FINISH-LINE.md`
(this file) → `HANDOFF.md` §26 (current state) → §23 (the wedge merge) → §25
(the Shopify draft). `GAMEPLAN.md` and `NEXT-PAGES.md` are now history rather
than plan — every page they describe is built.
