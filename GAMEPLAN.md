# Lucky Golf — site build gameplan  ·  v2

Phase 1 built the homepage. Phase 2 built the LGW01 PDP and the build system.
This is the plan for turning that into a **complete, clickable site** that can be
handed to a Shopify developer.

**Read `HANDOFF.md` first** — it holds the locked decisions, the contrast law,
the copy rules, the build system and every trap found so far. This file is the
*plan*; that file is the *law*. Don't re-litigate what's in it.

---

## 0. Three things that will save the next session hours

**1. The reference PDFs are readable.** `python tools/render-ref.py --list`,
then `--pages 1-3`. PNGs land in `_ref/`. A session once burned real time
concluding they were unreadable.

**2. Pages are built, never edited.** `python tools/build.py` assembles
`_src/` into the `NN-*.html` files. Never edit those directly. `--check` reports
whether output matches disk. The build has a smoke test that fails if a
load-bearing selector goes missing — it exists because a regex once silently ate
the entire PDP responsive block.

**3. Verify in the browser, and resize it first.** `mcp__Claude_Browser__javascript_tool`
works; screenshots do not. **The pane reports `innerWidth: 0` until you call
`resize_window`** — audits run before that return confident nonsense. Sweep for
contrast (compositing alpha properly), overflow, broken images and tap targets
at 1440 **and** 390. Known false positives: `.foil` (invisible to the sweep —
check by hand), gradients, decorative SVG.

---

## 1. Where things stand

| | Status |
|---|---|
| Homepage | Done. 14 sections, verified. |
| PDP — LGW01 Carver Gold | Done, 4 revisions. The club template. |
| Build system | `_src/` + `tools/build.py`, smoke-tested |
| **Phase A** | **Done 2026-07-31 — see HANDOFF §10** |
| **Phase B — collection pages** | **Done 2026-07-31 — 7 of 8 built, see HANDOFF §11** |
| **Phase C — three PDP templates** | **Done 2026-07-31 — proven on a putter, a polo and a cover, see HANDOFF §12** |
| **Phase D — all product pages** | **Done 2026-07-31 — 42 of 44, see HANDOFF §14 and §18** |
| Everything else | Not started |

**The store: 44 sellable products**, counted from the catalogue pull, not
estimated. Full data in `_src/data/products.json`.

| Type | Count | Variant shape | Price |
|---|---|---|---|
| Wedges | 3 | Hand × Loft | $99–109 |
| Putters | 3 | Hand | $199–229 |
| Hybrid | 1 | Hand | $209 |
| Driver | 1 | none | $299 |
| Classic Polos | 10 | Size | $67 |
| Blade Polos | 3 | Size | $67 |
| Hats | **10** | none | $29 |
| Gear | **13** | mixed | $9.95–40 |

Corrections from the pull: hats are 10 (three are archived) and gear is 13, not
~11. Both counts are now `{{count:…}}` tokens off the data wherever they appear
in copy, so they cannot drift again. Ignore `Free Returns + Package
Protection` — it is a checkout app product, not a page.

---

## 2. Do this before any more pages: templates + data

**We are not hand-writing 45 product pages.** Phase 2's lesson was that the
structural fix belongs *before* the next page, not after the eighth. The same
applies here, twice over.

### 2a. Generalise the buy box to N variant axes

`page-pdp.js` currently hardcodes `hand` and `loft`. The store needs **0, 1 and
2 axes**:

| Axes | Products |
|---|---|
| 2 | Wedges (Hand × Loft), Glove (Hand × Size) |
| 1 | Putters, Hybrid, Mallet Cover (Hand) · Polos (Size) · Grips (Grip Size) |
| 0 | Driver, Hats, Tees, Blade Cover, Driver Cover |

Refactor `PD` to `{options:[{name, values[]}], stock:{"RH|52":n}}` and drive the
pickers from that. A 0-axis product renders no pickers at all.

### 2b. Make pages data-driven

One template + `_src/data/products.json` → `build.py` emits a page per product.
This is exactly what a Shopify template does, so it **also demonstrates the
templating to the developer**. Copy changes happen in one place.

Pull the data from Shopify MCP once and commit the JSON — do not re-query per
build.

---

## 3. How many PDP templates? Three.

**This is the answer to "does apparel need the same thing as clubs".** No.

### Club PDP — built ✅ · proven on a putter
Gallery, buy box, description + video, highlight reel, help-me-choose, spec
table, the look (brand field), quote, reviews, cross-sell.

The **help-me-choose module swaps by family** and is the only real difference
between clubs:

| Family | Module |
|---|---|
| Wedges | "Start with the wedge you already carry" — built |
| Putters | **Blade or mallet** — a real question, and both exist (LGP01 blade, LGP02 mallet) |
| Hybrid | **What it replaces** — 3-iron / 5-wood gapping |
| Driver | None needed |

Putters and the driver have no loft axis, so the spec table shortens and the
loft section is omitted. Otherwise identical.

### Apparel PDP — new template
Genuinely different, for four reasons:

1. **Size is the decision, not spec.** Needs a real size guide with measurements
   and a fit note. There is no spec table.
2. **Colourways are separate Shopify products, not variants.** Ten Classic
   Polos are ten products. The template *must* carry a "more colours" strip
   linking siblings, or the range is undiscoverable.
3. **Fabric and care replace construction.** 88/12 poly-spandex, UPF 50+,
   four-way stretch, machine wash — that is the whole story.
4. **Lifestyle photography carries it**, where clubs are carried by studio
   cutouts. This is the biggest asset gap on the whole site.

Reuses: gallery, buy box shell, reviews, cross-sell, modals, closing CTA.

### Gear PDP — new template, deliberately short
Head covers, grips, gloves, tees. **$9.95–40 impulse items.** A fourteen-section
page for a pack of tees is absurd and would read as padding. Gallery + buy box +
two detail blocks + reviews + cross-sell. Nothing else.

---

## 4. Pages to build

~60 pages from ~8 templates.

| # | Page | Template | Count |
|---|---|---|---|
| 1 | Home | done | 1 |
| 2 | **Collection / PLP** | new | ~8 |
| 3 | Club PDPs | built, needs generalising | 8 |
| 4 | Apparel PDPs | new | 26 |
| 5 | Gear PDPs | new | ~11 |
| 6 | Our Story | new | 1 |
| 7 | Trybe / Ambassador | new | 1 |
| 8 | Support cluster | one template | 4 |
| 9 | Search results, 404 | new | 2 |

**Collections that need to exist:** All Clubs, Wedges, Putters, Hybrid &
Driver, Polos, Hats, Gear, Sale. Note **Gear does not exist in Shopify** — see
HANDOFF §7b E.

**Support cluster:** Returns & the 60-day policy, Shipping, Contact, FAQ. All
four are already linked in the footer and all four currently go nowhere.

---

## 5. Build order — what unlocks what

**Phase A — routing and data. DONE 2026-07-31.** Link registry in
`tools/sitemap.py`, N-axis buy box in `_src/variants.js`, product data layer in
`_src/data/`. 62 pages declared, and the build now fails on a dangling link, a
literal `href="#"`, or an unresolved token — each verified by breaking it.
**HANDOFF §10 is the record.**

Carried into Phase C: §2b's "emit a page per product" has its data layer and
emitter wiring, but `build.py` does not yet write 44 HTML files, because the
club template cannot render a hat. That is Phase C's job anyway.

**Phase B — PLP. DONE 2026-07-31.** One template, `_src/page-plp.*`, and seven
built collection pages with facet filters, sort, an in-stock toggle and an
empty state. **Sale is the eighth and is deliberately not built** — nothing in
that collection carries a `compareAtPrice`, so the page would show six
full-price grips under a Sale heading. HANDOFF §11e has the detail; it builds
the moment the collection is priced.

Also landed here: `.chip` and `.crumb` moved to `core.css` (page stylesheets
don't see each other, and the PLP breadcrumb was rendering as a numbered list),
and `{{count:…}}` so product counts in copy come from the data.

**Phase C — prove the three templates. NEXT.** One putter (1 axis + a different
help-me-choose), one polo (siblings + size guide), one head cover (short form).
If the templates flex here, the remaining 40 pages are data entry.

The club template is already parameterised — `PD` comes from `products.json`
and the buy box handles 0, 1 and 2 axes — so the putter is mostly editorial:
the help-me-choose module swaps to blade-or-mallet and the spec table loses its
loft column. Note **LGP01 Tracer Blade is sold out**, so the putter that proves
the template should probably be LGP02.

**Phase D — generate the rest. NEXT.** The remaining 40 PDPs from data. Per
product: write `_src/data/copy/<id>.json`, pull reviews if it has any, flip
`built=True` in `normalize-products.py`, rebuild. **No template edits** — the
registry already routes all 44 and the build fails if a product is marked built
without an editorial file. HANDOFF §12g is the checklist.

The work is copy, not code. The two things that will slow it down are that most
products have no Shopify description to write from, and that apparel lifestyle
photography still does not exist.

**Phase E — brand pages.** Our Story, then Trybe. Both have two references each.

**Phase F — support cluster, search, 404.**

**Phase G — full link audit + a developer handoff doc** describing which
Shopify template each page maps to.

This is **several sessions, not one.** `HANDOFF.md` and this file are the
continuity mechanism between them.

---

## 6. Open items carried forward

From HANDOFF, still needing Cole:

- **LGW01 spec gaps** — bounce, grind, swing weight, playing length, grip sizes
- **Shaft** — reference guide says KBS, reality is the Lucky stock shaft. **The
  guide needs updating**, or a future session re-introduces the error
- **Judge.me AI summary** — publishes two complaints verbatim; leave or disable
- **Gear collection** doesn't exist in Shopify
- **Closing-CTA fix** — dark-on-dark against the footer, now on both pages
- **Product naming** — Shopify titles should lead with Carver / Tracer / Stryker
- **Warranty and shipping policy detail** — both modals carry "needs confirming"
- **Photography and video** — the largest blocker. Every labelled slot is a
  brief. Apparel lifestyle is the biggest single gap.

---

## 7. Starting the next chat

> Continuing Lucky Golf. Read `GAMEPLAN.md` then `HANDOFF.md` in
> `C:\Users\wetzl\Lucky Golf\Website`. Phases A–D are done: routing, the N-axis
> buy box, the product data layer, seven collection pages, all three PDP
> templates and 42 of 44 product pages. **50 of 62 pages built.** HANDOFF
> §10–§18 have the details and §18 is the current state.
>
> Next is the **club collection redesign** — HANDOFF §13.3. Takomo groups irons
> into labelled bands with a comparison table and a fitting CTA; ours is one
> filtered grid. Cole deferred it until Phase D finished, and it has.

Then Phase E (Our Story, Trybe), F (support cluster, search, 404) and G (link
audit plus the developer handoff doc).
