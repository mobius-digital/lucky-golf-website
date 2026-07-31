# Lucky Golf — Phase 1 handoff

Read this first, then `01-home.html`. Everything below is decided unless marked OPEN.

---

## 1. Why Dartee reads "branded" instantly and ours doesn't

Compared frame by frame. It is not craft — it is **where the brand devices sit**.

| | Dartee | Takomo | Lucky (now) |
|---|---|---|---|
| First 100px | Deep green band, pink accent, pinstripes | Black bar, orange accent | Black marquee, gold text |
| Header | Green field, mascot present | White, orange cart | White, small green logo |
| Hero | Brand colour field around the photo | Full-bleed photo | Full-bleed photo |
| First scroll | Mascot again, pink CTA | Orange tags on tiles | Nothing until section 3 |

**The diagnosis: our first 900px is a white page with a photo on it.** Every Lucky device — clover watermark, groove, foil, emphasis tags, mono stamps — starts at the product grid and below. Dartee front-loads. Their header *is* a brand field, not a white bar.

**Fix direction (needs approval — see OPEN A):** put a brand-coloured field in the first 100px. Deep green `#008340` is the only palette colour that can carry a field without competing with gold. Gold is the product; green is the brand. Right now green does almost nothing, which is why the top reads neutral.

## 2. The mascot question

**Keep the clover. It is not the problem.** It has a golfer and a flagstick carved into the negative space — that is genuinely ownable and no other golf brand has it.

**The problem is scale and frequency.** Dartee's alligator appears ~4× at large size and is *illustrative*. Ours appears at 19px in the logo and as a low-opacity watermark that only shows up 3 sections down.

**Recommendation:** keep the clover, use it 3–4× at large scale above the fold, and do NOT commission a new mascot. A second character would fight the clover and the brand guide locks the logo system.

## 3. Section problems, confirmed against Takomo

| Section | What is wrong | Fix |
|---|---|---|
| Marquee | Black band at the very top reads like a utility bar, not brand | Move under the hero; test green field instead of ink |
| Product grid | CTA line and hover border are off-brand; no foil anywhere | Remove the black hover border, add foil hover, restyle the meta line |
| Mega menu | Still not Takomo — theirs is bigger, calmer, more air | Rebuild: fewer tiles, larger, more padding |
| Apparel/gear | Lists **individual products** (specific polos, specific hats) | Must be **collections**: Polos / Hats / Gear, lifestyle photo + name + one line + button |
| Missing | Takomo has a full-bleed brand band (logo + mono taglines) | Add one |
| Missing | Takomo has "THE BEST VALUE IN GOLF" — dark, icon value props, photo collage | Add one |
| Missing | Takomo has "THE ROSTER" — creator headshots on the homepage | Add one, feeds Trybe |

## 4. Locked decisions

- Background **white**; cream is an accent only (tiles, pricing band, cart footer)
- Radius **4px**, borders **2px**
- **Cart drawer only**, never a cart page
- Groove: ink `rgba(246,242,232,.13)` 1px/6px · cream `rgba(23,20,15,.032)` 1px/6px
- Type locked: Archivo (wdth 62 display) + Space Mono. Mono-lowercase asides allowed only when attached to a line above
- Foil ramp: shadow→base→highlight→base→shadow, highlight sweeps right→left on hover
- Tiles use **studio cutouts** + `mix-blend-mode:multiply`; lifestyle photography is for full-bleed sections only
- Reviews: real Judge.me, 4★ floor, brand comparisons allowed
- Flat pricing across lofts (assumed from the Product Reference Guide)

## 5. Data sources that already work

- Shopify MCP → `lucky-wedges.myshopify.com`. Product media via `productByHandle{media}`
- Judge.me public widget (no auth):
  `https://app.judge.me/reviews/reviews_for_widget?url=lucky-wedges.myshopify.com&shop_domain=lucky-wedges.myshopify.com&platform=shopify&per_page=30&page=N&product_id=<id>`
- Ratings: LGW01 4.81/551 · LGW02G 4.78/69 · LGP01 4.86/147 · LGP02 4.71/58 · LGH01 4.60/20 · LGD01 4.33/39. Clubs 4.78 / 884
- **Zero reviews have customer photos** — Judge.me photo requests are off. Turn on.

## 6. Studio cutout URLs (base `https://cdn.shopify.com/s/files/1/2286/3149/files/`)

- LGW01 `6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868`
- LGW02 Gold `1_27f81f90-a495-4dc4-ba02-0650ea6c4608.webp?v=1781012462` (bg slightly warm — try `3_b91d1d46-0aaa-4a41-9473-734a3f79362c.webp?v=1781012462`)
- LGW02 Black `6_cef3d6fc-8907-4866-b6aa-6301f8c614b5.webp?v=1784586436`
- LGP01 `3_f3d878d3-a4bb-4cc9-82df-f68e8eec3f61.webp?v=1782599090`
- LGP02 `1_b00c01f0-8116-464a-a39c-08a6ebf82b6f.webp?v=1782598133`
- LGH01 `3_a032f79a-78ab-436e-81c9-eea7bb5f7f40.webp?v=1782597493`

Known bad asset: `59.webp` (white snapback) has inverted lettering. Do not use.

## 7. RESOLVED — A–D are closed, all four are built

- **A. Green header field — YES.** Cole delegated the call; decided via the UI/UX skill.
  `.hdr` is now solid `--green` with a groove, a 2px `--gold-hi` bottom rule, white
  logo/nav/icons. Header is `position:sticky`, so green is now a rail down the whole page.
- **B. Marquee moved under the hero, on green.** No longer the first thing on the page.
- **C. Collections are Polos / Hats / Gear.** Individual-product tiles deleted.
- **D. All three sections built:** brand band (green), value props (ink), Trybe roster (cream).

### Green-field contrast law — measured, do not re-derive

Everything below is against `--green #008340`. This is the single most load-bearing
constraint introduced in rev 3, and two of these would have shipped broken:

| Foreground | Ratio | Verdict |
|---|---|---|
| `--white` #FFFFFF | **4.86:1** | PASS 4.5 — use for ALL text on green |
| `--cream` #F6F2E8 | 4.35:1 | **FAIL** — never use for text on green |
| `--gold` #C29A2B | 1.84:1 | **FAIL at any size** — never put gold on green |
| `--gold-hi` #EDD27C | 3.27:1 | PASS 3:1 non-text only — rules, borders, marks, badges |

Consequences already applied: nav hover underline gold → gold-hi; marquee text
gold-hi → white (it is .72rem, so it needs 4.5); marquee clover marks `--green-br`
→ gold-hi (green-on-green was invisible); cart badge `--green-br` → gold-hi.

**Trap:** `.nav a` cannot be used as a selector — the mega panel lives inside `.nav`
and sits on white, so a bare rule paints those tiles white-on-white. It is scoped
`.nav > a`, and `.mega :focus-visible` is reset to base `--gold`. Keep it that way.

### Rules vs groove — system rule

The groove is 1px lines on a 6px pitch. **A 1px structural divider on a grooved
field reads as one more groove line.** Every rule that sits on a grooved section
is therefore 2px (which is the locked border weight anyway — 1px was violating it)
and brighter than the groove: `--rule-on-dark` / `--rule-on-light`.

Applied to `.vp-item`, `.feat-stamp .ln`, `.ftr`, `.ftr-btm`. Grooved sections are
`.hdr .mq .bband .feat .why .vp .roster .close .ftr` — check this before adding any
divider to one of them.

### Full-bleed bands need the next section's top padding back

`.sec` blocks carrying `style="padding-top:0"` assumed the section above was the
same colour. Once the brand band and value props were inserted, a hard coloured
edge butted straight into the next heading. Both were removed. **If you insert a
full-bleed colour band, check the section under it has top padding.**

### Brand field is tokenised — changing the colour is six variables

`--brand --on-brand --on-brand-88 --on-brand-22 --brand-accent --brand-groove`
drive the header, the marquee and the brand band together. **Current: Forest
`#0B5130`** with base gold `#C29A2B` as the accent (3.56:1 — passes 3:1 non-text).
`_brand-variants.html` is the same page with a live switcher over 12 candidates
and a contrast readout; keep it in sync when the build changes.

### Copy rules learned the hard way

- **Never name a material, alloy or grind in homepage copy.** Spec dumps read as
  a brochure. Construction belongs on the PDP, after the promise.
- **Never single out one product or price in generic brand copy.** "A forged
  wedge for $99" in a section about the whole company reads as though wedges are
  all we sell. Same for "right and left hand" — table stakes, not a selling point.
- **Review counts:** 884 is clubs-only. It is fine *inside* the review block,
  where precision builds trust. It is not a boast. Elsewhere use "hundreds of
  five-star reviews". "Thousands of Lucky golfers" is verified — Shopify reports
  at least 10,000 customers and 10,000 orders.
- Asides are sentence case, not lowercase (ruled 2026-07-30).

### Section jobs — why "why" and "value props" both survive

They were making the same argument twice, which is what made the page feel
repetitive. They are now split by job and must stay that way:

- **Why Lucky (cream)** owns the **price objection** — no middlemen, no tour
  contracts, what's left is the club. No materials, no product names, no prices.
- **Value props (ink)** owns **quality and guarantees** — built properly, the
  whole bag, sixty days, backed by golfers.

### New section order

| # | Section | Field | Job |
|---|---|---|---|
| 1 | Header | brand | Brand field in the first 100px |
| 2 | Hero | photo | — |
| 3 | Marquee | brand | Brand hit #2 |
| 4 | Shop by family | white | Show the line |
| 5 | Featured — Tracer Blade | ink | Deep-dive one club |
| 6 | Why Lucky | cream | **Price objection** |
| 7 | **Club finder** | white | **Help me choose** (tabbed, keyboard-navigable) |
| 8 | Brand band | brand | Brand punctuation |
| 9 | **Pull quote** | cream | **One real review at scale** |
| 10 | Social proof rail | white | The evidence |
| 11 | Value props + mindset | ink | **Quality/trust**, then the brand argument |
| 12 | Seen in the wild | white | Community |
| 13 | **The finish** | ink | **Desire** — replaced the lifestyle break |
| 14 | Trybe roster | cream | Community |
| 15 | Apparel & gear | white | Breadth |
| 16 | Closing CTA | dark | Convert |

Brand colour lands three times — 0px, under the hero, and mid-page — which is what
makes it read as the spine rather than an unused palette entry. Fields alternate
ink/white/cream either side of every section, so no two dark bands touch.

The finder sits *after* the price objection on purpose: answer "why is it this
cheap" before asking anyone to pick. The pull quote leads *into* the review rail —
headline, then evidence — and fixes there being no social proof until 60% down.

## 7b. OPEN — needs Cole

- **E.** There is **no "Gear" collection in Shopify.** Polos (`/collections/polos`, 13)
  and Hats (`/collections/hats`, 13) are real and linked. Gear is split across Head Covers,
  Gloves, Grips and a collection titled "Accessories" whose handle is confusingly
  `most-popular`. The Gear tile is `href="#"` until you create one.
- **F.** Collection tiles currently use **studio product shots**, not lifestyle. §3 asked
  for lifestyle photo + name + one line + button; the copy, name and button are in, the
  photo is the gap. Three lifestyle shots needed (polo on body, hat on body, gear flat-lay).
- **G.** Roster is **five placeholder slots** — no headshot assets exist. Needs five
  4:5 portraits plus real names and handles. Names are bracketed, not invented.
- **H.** Value-props collage is three photo-needed slots (specs are in the markup).
- **I.** Hat tile uses `39.webp` (Black patch hat). Deliberately avoids the known-bad
  `59.webp`, which is the White Upside Down Hat with inverted lettering.

## 8. Build notes — READ THIS, IT CHANGED

The single-file `_src-home-template.html` is **retired**. Sources now live in
`_src/`, and `tools/build.py` assembles each page:

```
_src/core.css          tokens, type, the six devices, buttons, header, footer,
                       marquee, mega menu, cart, product tiles, review cards
_src/core.js           reveal, mobile nav, rail, lightbox, mega menu, cart
_src/partials/         symbols-host · header · footer · lightbox · cart
_src/page-home.{css,html,js}
_src/page-pdp.{css,html,js}
tools/build.py         assembles -> 01-home.html, 02-pdp-lgw01.html
```

```bash
python tools/build.py            # build every page
python tools/build.py pdp        # build one
python tools/build.py --check    # build to memory and diff against disk
```

`01-home.html` and `02-pdp-lgw01.html` are **generated — never edit them
directly.** They stay single-file and dependency-free on purpose, which is what
makes them easy to send for review. The build is reproducible: `--check`
reports `identical` when sources and output agree.

The split was verified content-preserving — every non-blank line of the old
template survives in the rebuilt homepage, and the homepage re-passes the
contrast sweep with zero failures.

**`{{HOME}}`** in `partials/header.html` resolves to `""` on the homepage and
to `01-home.html` everywhere else, so the shared nav's `#families` / `#gear`
anchors work from any page. Add the token to any new homepage-only anchor.

`_src-home-template.html` is kept in the tree only as the provenance record for
that split. Do not edit it; it no longer builds anything.

**Consequence for `_brand-variants.html` and `_why-options.html`:** both were
generated from that retired template, so they are now frozen and will drift from
the live homepage. They are still useful as the record of the colour-switcher
and "why" explorations, but stop treating them as regenerable. If the brand
field needs re-testing, rebuild the switcher over `_src/` instead.

Git history is the rollback path: `git log --oneline`.

---

## 9. Page 2 — the PDP  ·  `02-pdp-lgw01.html`

Built from all five PDP references. Subject is **LGW01 Carver Gold** — the most
reviewed product (4.81 / 551), the most inventory, and the only one whose
variant matrix exercises both option axes.

### What came from where

| Device | Source | Why |
|---|---|---|
| Pull-quote review **above the price** | Dartee | Strongest trust move in either reference, and we have 551 reviews to draw on |
| 4-up icon strip in the buy box | Dartee | Construction summary without a spec dump |
| Accordions | Dartee | Keeps the buy box short |
| Full-bleed brand band, 4 columns | Dartee | Already Lucky's own device — this is where green field #3 lands |
| Curated review **card grid** | Dartee | Takomo's raw Judge.me dump is three pages of ugly |
| Tabbed spec table | Takomo | Wedges deserve the table; nothing else gives you per-loft data |
| Cross-sell twice (under fold + bottom) | both | |

### Section order and fields  ·  rev 2, after Cole's review

`brand(header) → white(crumb+fold) → brand(marquee) → cream(others also viewed)
→ white(the club) → brand(where the money went) → cream(the argument) →
white(which loft) → cream(the numbers) → ink(highlight reel) → cream(signature
quote) → white(reviews) → cream(rest of the bag) → white(finish the setup) →
ink(close+footer)`

**Rev 2 changed five things off Cole's feedback. Do not undo them without asking.**

1. **The fold now hands off the way Takomo's does.** Takomo goes fold → upsell
   rail → product description with a video beside it → bulleted spec summary.
   Rev 1 went straight into the brand argument, which Cole flagged. So:
   *Others also viewed* sits directly under the fold, then *The club* carries
   the description, the video slot and the Takomo-style bullet list.
2. **"Most rounds are decided inside a hundred yards" moved down.** It is good
   copy in the wrong slot — it now sits after the build section and sets up the
   loft picker. Problem, then solution.
3. **The spec table came off the ink field.** It was on ink *with the groove*,
   and 1px lines on a 6px pitch behind small mono figures made it hard to read
   — Cole's exact complaint. Takomo's spec block is light grey with a white
   bordered table and a black header row on the loft matrix. It now matches, on
   cream, with no groove under the table. **The fix was the field, not the
   lines.**
4. **Reviews are now Judge.me's shape, not a curated grid.** Score, histogram,
   AI summary, star filter, sort and paging all work. The signature quote moved
   out into its own `.pull` section above it, which is the homepage's device.
5. **Highlight reel added** (`ink`), six labelled video slots.

`.pull` moved from `page-home.css` into `core.css` — it is a two-page component now.

### Reviews: the sample is deliberately not 4-star-and-up

The widget carries **47 real reviews spanning every rating**, in roughly the
live proportion, so the histogram and the star filter tell the same story.
Filtering to 1★ returns real 1★ reviews.

This is not a reversal of the 4★ floor. The floor governs **curated** moments —
the buy-box pull quote and the signature quote — where we are choosing what to
say. A review *widget* that hides its 1-stars is a widget nobody believes, and
Judge.me would not hide them anyway.

### The video gap is now two sections, not zero

`.club-media` (16:9, beside the description) and the six `.reel` slots are all
labelled briefs, not stand-in photography. Nothing on this page pretends a
still is a video. Briefs are written on each card.

### Verified facts on this page

- **Flat pricing across lofts is confirmed**, not assumed. Every LGW01 loft
  variant is $99 in Shopify; every LGW02 is $109. §4's assumption holds.
- Variant availability is the real Shopify state as of 2026-07-31. **LH 50° and
  LH 60° are genuinely out of stock** and render struck through. Switching hand
  while holding a dead loft slides you to the nearest live one.
- Per-variant stock drives the "Low stock — N left" line (fires under 25).
- All nine review cards are verbatim Judge.me, 4★ and up, including **one
  honest 4★** — a page of nothing but 5s reads fake.
- Specs come from the copy skill's **Product Reference Guide**, which turned out
  to hold real LGW01 data (1020 forged carbon steel, lie 63° all lofts, head
  weight 300g all lofts, KBS Tour stiff). LGW01's Shopify `descriptionHtml` is
  empty — the reference guide is the only source.

### Still open on the PDP

- **A. Spec gaps.** Bounce, grind, swing weight, playing length and grip sizes
  are not published anywhere verifiable. They render as dashed **"Needs spec"**
  chips rather than invented numbers. Nine cells. Fill them and the table is done.
- **B. Judge.me's AI summary is live output, not written copy.** It currently
  ends "…one customer reported the head separating from shaft on first swing,
  and another noted slow customer service response times." It is rendered
  verbatim because that is what the widget will actually emit. Turning it off is
  a Judge.me setting and Cole's call — but decide deliberately, don't be
  surprised by it later.
- **C. Naming mismatch.** Shopify calls the product *"Lucky Golf LGW01 Gold"*;
  the brand guide says lead with the family name, so the page says **"Carver
  Gold"** with `LGW01` as a stamp. The Shopify titles should probably be renamed
  to match.
- **D. No set discount exists.** "Most golfers carry three" is a soft cross-sell
  at full price, per Cole's call. If a bundle rule is ever added in Shopify, the
  section is already shaped to carry tier pricing.
- **E. No lifestyle or UGC on this page.** Both references run one. Blocked on
  the same photography gap as the homepage (§7b F/H).

### Cart drawer — three bugs Cole caught in one screenshot

All fixed in `core.css` / `core.js` / `partials/cart.html`, so both pages get them:

1. **The "black bar" before checkout** was `.cd-foot`'s `border-top: 2px solid
   var(--ink)`. A 2px ink rule on a cream field reads as a black bar, not a
   divider — and the colour change from white body to cream footer is already
   all the separation the eye needs. Now `--ink-14`.
2. **The price looked struck through.** `.ci .pr` and `.qty` were inline
   siblings, so the stepper's 2px border crossed `$99` at mid-height. The price
   is `display:block` now, with 10px of clearance measured.
3. **561px of dead space** between a one-line bag and the footer. Measured, not
   estimated. That space now holds the cross-sell.

**The cart cross-sell** reads a page-level `LG_CART_UPSELL` and filters out
anything already in the bag, so it never offers what was just added. It hides
itself when the bag is empty or nothing is left to offer — which is why the
homepage, which defines no upsell list, shows no block at all. Dead gap is down
to 214px.

### Two laws learned building it

- **Foil is illegal on white.** The ramp peaks at `--gold-hi`, which is under
  2:1 on white; base `--gold` is 2.64:1, so it fails even the 3:1 large-text
  bar. Foil only ever runs on ink or the brand field. The contrast sweep
  **cannot catch this** — it skips `background-clip:text` elements — so it has
  to be checked by hand on every new headline.
- **Check class names against `core.css` before inventing one.** The PDP's
  quantity stepper was originally `.qty`, which is also the cart drawer's
  stepper, so the PDP silently restyled the cart. It is now `.bx-qty`. Page
  stylesheets load after core and will win.
