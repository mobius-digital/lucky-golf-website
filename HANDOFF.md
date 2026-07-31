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

### Section order and fields  ·  rev 3

`brand(header) → white(crumb+fold) → brand(marquee) → cream(others also viewed)
→ white(the club) → ink(highlight reel) → white(which loft) → cream(the numbers)
→ brand(THE LOOK) → cream(signature quote) → white(reviews) → breath →
white(rest of the bag) → cream(finish the look) → ink(close+footer)`

**Rev 3, off Cole's second review. The important one is the first item.**

1. **"Where the money went" is gone, and its green now carries the brand
   moment.** Its four facts — forged / milled / sandblasted / weighted by loft —
   were *already* the bullet list in "The club" directly above it. The section
   had no job. The green field survives (Cole wanted the page broken up) but now
   holds **`.look`**: a full-bleed image one side, brand-field copy the other,
   about the gold finish and what it's like to pull the club out of the bag.
   **Do not re-add a construction band. Check the bullets first.**
2. **"Most rounds are decided inside a hundred yards" is gone too.** Its
   pricing argument is one sentence inside the club copy now, with a link to the
   homepage's Why Lucky, which is where the price objection is actually argued.
3. **The highlight reel moved directly under "The club"** — social proof right
   after the pitch, before the sizing and spec detail.
4. **Takomo's description layout copied properly.** The bulleted summary sits
   *inside the left copy column* under the prose, with the video beside both —
   not full-width underneath. That is how the reference does it.
5. **"The rest of the bag" moved to white.** `.ptile` is itself cream, so cream
   tiles on a cream field had no edge. A `.breath` divider separates it from the
   reviews above. **Any section using `.ptile` must be on white.**
6. **"Finish the setup" → "Finish the look"**, and it is polos and hats now, not
   gear. Cards went white so they read on the cream field.
6b. **"Others also viewed" is clubs only** (Cole's call), even though Takomo
   mixes apparel into theirs. The apparel cross-sell has its own section now.
7. New club headline: *"The kind of wedge that makes a short-sided miss feel
   survivable."* Spec headline is *"Same steel, same weight, same price. Six
   lofts."* &mdash; "The numbers" was flagged as weak.

### Shafts — the reference guide is WRONG on this, Cole overrides it

`references/product-reference-guide.md` lists the Carver's shaft as **"KBS Tour,
stiff."** That is not what ships. **Cole confirmed 2026-07-31: every Carver goes
out on the Lucky Golf stock steel shaft today, and KBS becomes a selectable
upgrade soon.**

The spec table's Shaft & grip tab now reads *Shaft, stock* / *Shaft, upgrade
(KBS — coming soon)*, and the "What you get" accordion was corrected too. On any
product fact the reference guide normally wins; this is the documented exception
until the guide is updated. **Update the guide.**

When KBS lands it becomes a **third variant axis in the buy box** alongside hand
and loft — the picker markup and `sync()` already generalise, but `PD.stock`
would need a shaft dimension. `.spec-aside` under the table says as much.

The `.soon` pill is a green marker for shipped-soon items. It is deliberately
*not* the dashed `.tbd` chip: "we haven't published this number" and "this is
coming" are different statements and should not look alike.

### Product-card callouts: one tag, or none

`.pt-tag` was on every club card ("3 lofts", "New", "Right & left"), which makes
it wallpaper — Cole flagged it. A badge on one card in three is a signal; a badge
on all three is decoration. **Only genuine news gets a tag now** (LGW02 Shadow =
"New"), and the same rule applies to `.oav-tag` in the browse rail, where "Sold
out" on the Tracer is real state.

### Sized products cannot have an Add button

The apparel cards were one-click "Add". Polos come in six sizes, so there is
nothing sensible to add — Cole caught it. `PD_KIT` rows now carry `sizes:true`,
which swaps the button for **"Choose size →"** linking to that product's own
page. Hats are single-variant and keep the real Add. **Any future cross-sell
tile has to make this distinction.**

### Buy box: trust row and the two policy modals

The trust row now reads **thousands of satisfied golfers · sixty-day return
window · fast, free US shipping**, and two links open modals the way Takomo
does: **Warranty and returns** under the trust row, and **Estimate delivery
time** on the stock line.

`.md` is a **generic component in core** — `<div class="md" id="x" hidden>` plus
a `[data-md-open="x"]` trigger anywhere. Focus moves in, Tab is trapped, Esc
closes, focus returns to the trigger, body scroll locks. Same contract as the
cart drawer. Other pages should reuse it rather than rolling their own.

Both modals contain a **"Needs confirming"** chip: warranty period and who pays
return shipping in one, warehouse locations and international duties in the
other. Real policy detail, not invented.

### The clover-bullet alignment bug

`.cbul` carries `transform:translateY(2px)`, which suits it sitting beside
display type but reads as misaligned inside a centre-aligned flex row — which is
what Cole spotted. The nudge is now switched off in `.bx-terms`, `.jm-medals`,
`.rvh-badges` and `.md-sec` only; the homepage keeps it. Measured offset from
row centre is now exactly 0px.

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

### Mobile card rails — `.msnap`

Below 620px any grid carrying **`.msnap`** becomes a horizontal snap rail that
bleeds to the page edge. Measured saving: **4 screens on the homepage, 1.5 on
the PDP.** Applied to `.pgrid`, `.rost-grid`, `.coll` (home) and `.oav`,
`.pgrid`, `.kit`, `.lf-grid` (PDP).

Cards sit at **76%** so the next one is always half-visible. That peek is the
only thing telling you it scrolls — do not take it to 100%.

**The `!important` on `grid-template-columns` / `grid-auto-flow` is deliberate
and load-bearing.** Page stylesheets load after core, and several set
`grid-template-columns` on these grids at 980/1180px — those rules also match a
390px phone, and the first attempt shipped two collapsed 4px columns with the
rest overflowing. `.msnap` is a layout *mode*, not a tweak, so it has to win
without every page remembering to scope its own breakpoints.

### `tools/build.py --check` and the smoke test — why they exist

A regex written to delete one dead CSS block ate the **entire PDP responsive
section** instead: the mobile sticky add-to-cart, the single-column fold, the
2-up icon strip, the gallery thumb counts. The page still built. It still passed
a desktop sweep. It only showed as a broken phone layout.

`build.py` now asserts a list of load-bearing selectors is present in each
page's output and **exits non-zero** if any is missing. Verified by deleting one
and watching it fail. When you add something whose absence would be invisible on
desktop, add it to `REQUIRED`.

**Lesson: never regex-delete a CSS block with a lookahead for the next banner.**
The banner styles are not uniform (`/* ===` vs `/* ---`), so the match ran past
the intended end.

### Cart, second pass

- **Panel edge is `--gold`, not ink** (Cole's call). It is the drawer's one
  structural gold line and ties the edge to the foil checkout button.
- **Adding to the bag opens the drawer.** `open()` is now idempotent — the PDP
  calls the add path N times for quantity, and re-focusing N times was wrong.
  It also ignores a hidden trigger: the PDP's add-to-cart proxy cannot take
  focus back, so focus falls through to whatever the user actually clicked.

### Dead CSS, verified but not yet removed

`.fam`, `.gear`, `.revs` (page-home.css) and `.rgrid`, `.dial-grid`, `.rvh*`,
`.rcard`, `.rsum`, `.rv-more`, `.setgrid` (page-pdp.css) appear in no markup —
leftovers from replaced sections. **Left in place deliberately**; deleting CSS
blind is what caused the incident above. Remove them in a dedicated pass, one at
a time, rebuilding between each.

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

---

## 10. Phase A — routing, the N-axis buy box, the data layer

Built 2026-07-31. No new pages; this is the plumbing GAMEPLAN §5 said had to
land before the other sixty.

### 10a. The link registry — `tools/sitemap.py`

Every page the site will ever have is declared in one place. Internal links are
tokens, resolved by `build.py`:

```
{{link:home}}           -> 01-home.html   ({{link:home#families}} -> #families ON home)
{{link:p/lgw01-gold}}   -> 02-pdp-lgw01.html
{{link:c/wedges}}       -> "#"   — declared, not built yet
{{link:none}}           -> "#"   — deliberately not a link
```

**Three things now fail the build**, all verified by breaking them on purpose:

| Fault | Message |
|---|---|
| token naming an undeclared slug | `DANGLING LINKS — no such slug` |
| a literal `href="#"` in `_src/` | names the `file:line` |
| any `{{…}}` left after resolution | `unresolved template tokens` |

`{{link:none}}` exists because of the middle one. Modal triggers and JS-driven
controls are real anchors that genuinely go nowhere; without a way to say so
there is no way to tell them apart from a link someone forgot to wire. Saying
it costs one token and makes `href="#"` a build error everywhere else.

**`{{HOME}}` is retired** — the registry subsumes it. Same behaviour, and now
it works from every page rather than being a homepage special case.

Pages declared but not built resolve to `#` and are **counted, not fatal**, so
the build reports how much of the site is still stubbed instead of failing
until all sixty exist. Right now: **62 pages, 2 built, 86 links stubbed.**
`python tools/build.py --links` prints the whole map.

**One page was added to GAMEPLAN §4's list:** `reviews` (`32-reviews.html`).
The homepage's "Read all 884 reviews" needs a destination, and 884 is the
clubs-wide count, so it cannot point at any single PDP's review block.

**Breadcrumbs now point at collections** (`c/clubs`, `c/wedges`) rather than
`01-home.html#families`. Correct destination, currently stubbed — Phase B
builds them.

### 10b. The product data layer

```
_src/data/shopify-raw.json    verbatim Shopify pull — provenance, do not hand-edit
tools/normalize-products.py   raw + the EDITORIAL overlay (in the script) -> products.json
_src/data/products.json       GENERATED. 44 products, 155 variants
```

Shopify owns prices, SKUs, options and availability. It owns **none** of the
brand names, families or template assignments — so those live in the overlay,
and re-pulling the catalogue never clobbers them. The script's docstring holds
the four queries to re-run.

`build.py` injects the whole product record into the page as `{{PRODUCT_JSON}}`,
so `PD` is no longer hand-typed. Re-pull, re-normalise, rebuild, and the page
reflects the store.

**The real catalogue is 44 sellable products, not 45.** Wedges 3 · putters 3 ·
hybrid 1 · driver 1 · polos 13 · **hats 10** · gear 13. GAMEPLAN §1's table had
hats at 13 and gear at ~11.

### 10c. The N-axis buy box — `_src/variants.js`

`PD` is now
`{options:[{key,name,values:[{k,label,sv}]}], variants:{"RH|56":{sku,price,avail,qty}}}`.
Pickers are generated into `#pickers` from the axes, so **the same markup serves
0, 1 and 2 axes**. Axis distribution across the store: **0-axis 15, 1-axis 25,
2-axis 4** — exactly the spread GAMEPLAN §2a predicted.

The rules live outside the page IIFE with no DOM, because the PDP renders one
product and it is the two-axis one. `node tools/test-variants.js` runs them over
all 44 products and 155 variants, asserting among other things that **choosing
any offered value on any axis lands on a variant that is actually sellable.**

**Two traps the old two-axis version got away with:**

1. **`availableForSale` is not `inventoryQuantity > 0`.** The glove ships at
   qty −3 and is sellable; the black clover grips sit at qty 0 and are
   sellable; LGP01 is at −12 and is not. Availability drives whether a chip is
   disabled; quantity only drives "Low stock — N left", which now requires
   `qty > 0` as well as `< 25`. Keying off quantity would have disabled
   sellable variants and sold dead ones.
2. **Price is per variant.** Grips run $9.95 / $11.95 / $14.95 across
   Standard / Midsize / Jumbo. The price repaints on selection (`#bx-amt`).

**SKUs are never synthesised.** A pattern like `{code}-{loft}-{hand}` looks
right on LGW01 and is wrong on the store: LGW02 Black's 50° and 52° are stamped
`LGW03-BLK-…` while 54–60 are `LGW02-BLK-…`, and the mallet cover is
`HeadCover-Mallet-SignatureWhite-RH` in one hand and
`Putter-Cover-Mallet-Signature-White-LH` in the other. Every SKU is carried
verbatim from Shopify.

Cascading availability is unchanged in behaviour and now stated as a rule: a
value on axis *i* is offered if some sellable variant matches it **and** matches
what is already chosen on the axes to its **left**. That is what greys out
"Left hand" only when no loft at all is available in it, while an individual
loft greys out for the hand you are on. Switching to a hand where your loft is
dead still slides you to the nearest live one.

### 10d. What Phase A did NOT do

GAMEPLAN §2b says "one template + products.json → `build.py` emits a page per
product." The **data layer and the emitter wiring are in** — the registry
declares a page and a filename for all 44, and `PD` comes from data. `build.py`
does **not** yet emit 44 HTML files, because the club template cannot render a
hat. That is Phase C's "prove the three templates", which is where the gameplan
puts it. Flip `built=True` in the overlay as each one lands.

### 10e. Catalogue facts — confirmed by Cole, not open questions

These came out of the pull, Cole has confirmed them, and they are recorded
because the next session needs them — not because anyone is waiting on a
decision. **Don't re-raise these.**

- **Hats are 10, polos are 13.** Three hats are ARCHIVED older versions, which
  is why the `hats` collection still counts 13. Every count quoted in copy is
  now a `{{count:…}}` token off `products.json` (see §11c), so this cannot
  drift again.
- **LGW02 Gold has three lofts (52/56/60), not six. LGW02 Black has six, right
  hand only.** Any "6 lofts" or "right and left hand" copy written about
  either one needs checking against the data first. The wedges mega-panel
  aside currently says "Right and left hand" above all three wedge tiles.

### 10e-2. RESOLVED — club naming, locked by Cole 2026-07-31

**Family, then code, then finish.** This closes §9 open item C.

```
Carver LGW01 Gold     Tracer LGP01 Blade      Stryker LGH01
Carver LGW02 Gold     Tracer LGP02 Mallet     Lucky Driver LGD01
Carver LGW02 Black    Tracer LGP02 Patriot
```

Apparel and gear keep their descriptive names — those codes are SKU prefixes,
not model numbers. `products.json` carries **`title`** (the full name, driving
the H1, page title and breadcrumb) and **`name`** (the short form for tiles,
where `code` is stamped beside it). **Do not re-litigate.**

Dead names, now gone from every built page: "Carver Gold V2", "Carver Shadow",
and the code-first "LGW01 Carver Gold" form — which also lived in image alt
text, the homepage review rail's product labels and the UGC lightbox data.

Two accuracy fixes found in the mega menu while doing it: the wedge tiles
claimed **"K Grind" and "S Grind"** when grind is a "Needs spec" row (§9A), and
the wedges aside said "Right and left hand" above the right-hand-only Black.

### 10e-3. Still open for Cole

- ~~Four names in play for LGW02 Gold~~ — **resolved above.** Historic detail:
  it was "Carver Gold" (mega menu),
  "LGW02 Carver Gold" (PDP browse rail), "Carver Gold V2" (PDP cross-sell),
  "Lucky Golf LGW02 Gold" (Shopify). And LGW02 Black is "Carver Black" in the
  mega menu but "Carver Shadow" in the browse rail. This is §9 open item C and
  it is now blocking: `products.json` had to pick one (`code + name`), and the
  shipped pages still disagree with each other.
- **SKU typo in Shopify:** LGW02 Black 50° and 52° are `LGW03-BLK-STOCK-RH-50/52`.
- **`Lucky Golf Tees` has no image at all** — the only product in the store with
  `featuredMedia: null`.
- **LGW01 inventory drifted** since the last pull: RH 50/54/58 are 98/215/314,
  not 99/216/315. Nothing rendered was wrong; the numbers are just live.
- **The glove is nearly all dead stock** — only left-hand Small and Medium are
  sellable, both oversold. A two-axis picker on a $17.95 item where six of eight
  chips render disabled may not be worth a page.
- **Entirely sold out:** both oversized putter grips, LGP01, the LGP02 Patriot,
  and the Black | Gold Classic hat.
- **Sale collection membership was not pulled.** `summer-warehouse-sale` holds 9
  products; Phase B needs to know which nine before the Sale PLP can be built.
- **Still no Gear collection** in Shopify — confirms §7b E. Gear is 13 products
  spread across Head Covers, Gloves, Grips and `most-popular`.

### 10f. Build commands, current

```bash
python tools/normalize-products.py          # Shopify raw -> products.json
python tools/normalize-products.py --check  # is products.json stale?
python tools/build.py                       # build every buildable page
python tools/build.py --check               # diff against disk
python tools/build.py --links               # print the registry
node   tools/test-variants.js               # variant engine over all 44 products
```

**Adding a page:** declare it in `tools/sitemap.py`, point links at its slug,
set `built=True` and give it a `src` when the sources exist. Until then every
link to it resolves to `#` and shows up in the build report.

---

## 11. Phase B — the collection template

Built 2026-07-31. **Seven collection pages from one template.** Sources are
`_src/page-plp.{html,css,js}`; everything they render comes from the collection
record `build.py` injects, so adding a product to `products.json` puts it on the
right page with no edit to the template.

```
10-collection-clubs.html          8 products · 4 facets · ratings
10-collection-wedges.html         3
10-collection-putters.html        3
10-collection-hybrid-driver.html  2 · 2 facets
10-collection-polos.html         13 · 2 facets
10-collection-hats.html          10
10-collection-gear.html          13 · 4 facets
```

### 11a. What the page does

- **Facet chips** by family, from `collection.facets`. A facet no member has is
  dropped in the normaliser rather than rendered as a chip that filters to
  nothing, and a collection with fewer than two facets renders no filter row at
  all — `.plp-facets:empty` collapses it so the sort control doesn't float.
- **In-stock toggle** and **sort** (featured / price ↑ / price ↓ / best reviewed
  / A–Z). "Best reviewed" is **removed at runtime** where nothing in the
  collection has a rating, rather than left to sort on a field that is null for
  every row. Only clubs have Judge.me ratings.
- **Sold-out products sink to the bottom of every ordering** and grey their
  photo. They are still shown — a collection that hides them looks thinner than
  the range actually is — but nothing sold out leads a grid.
- **Empty state** with a Clear-filters button. It is currently unreachable with
  live stock, so it was verified against a copy of the built page with every
  `inStock` flipped false: grid hides, empty shows, Clear restores.
- **`Lucky Golf Tees` gets a labelled "Photo needed" slot** rather than a broken
  image, because it is the one product in the store with no photo in Shopify.
- Tile hrefs are `{{link:p/…}}` tokens even though the tile is painted by JS, so
  collection links are audited by the registry like any other.

### 11b. Two components had to move to core — and why it matters

**Page stylesheets do not see each other.** `core.css` + `page-NAME.css` is the
whole cascade for a page, so anything a second page type needs has to be in
core. Two things were sitting in `page-pdp.css`:

- **`.chip`** — the PDP's variant picker, now also the PLP's facet filter.
- **`.crumb`** — which the PLP used and therefore rendered as **a numbered list
  in Archivo with 40px of browser-default padding**. It looked deliberate
  enough in a screenshot to miss; the sweep caught it as a 18.5px tap target.

Both are now in `core.css` under their own banners. `.mtile .chip` in core is
dead CSS (no markup uses it), so promoting `.chip` changed nothing there.

**The rule going forward: before styling a new page type, check whether the
class you are reusing is in `core.css` or in the other page's stylesheet.**
This is the same trap as HANDOFF §9's "check class names against core.css
before inventing one", from the other direction.

### 11c. Counts come from data now — `{{count:…}}`

`{{count:hats}}` resolves to that collection's real product count at build time.
The mega menu and the homepage collection tiles both used to hard-code "13
styles" for hats, which stopped being true when three were archived. Four
places now read from `products.json`. A count naming a collection that doesn't
exist fails the build.

### 11d. No closing CTA on a collection page, deliberately

`.close` is an ink field and `.ftr` is ink too — that is the dark-on-dark seam
already open against the homepage and the PDP, and putting it on seven more
pages spreads a known problem. A browse page's job is to get you into a
product, not to re-pitch the brand on the way out, so the PLP ends on the cream
"rest of the store" band. **If the `.close`/`.ftr` seam gets fixed, reconsider.**

### 11e. Sale is declared but NOT built — this needs Cole

`c/sale` is routed and stubbed. Its nine Shopify members are six grips plus
three ARCHIVED hats, and **not one carries a real `compareAtPrice`** — every
value is `null` or `"0.00"`. The only product in the store with a genuine
was-price is `stock-putter-grips` ($19.95 from $30.00), and it is **not in the
collection**. Building the page today would put six full-price grips under a
heading that says Sale.

The membership and the reason are recorded in `products.json`; the page builds
the moment `blocked` comes off the collection in `normalize-products.py`.

### 11f. Verified

Fresh loads at 1440 and 390, contrast composited through rgba ancestors:

| | 1440 | 390 |
|---|---|---|
| Contrast failures | 0 | 0 |
| Overflow | none | none, `scrollWidth` exactly 390 |
| Grid | 4-up | 2-up, toolbar stacks |

Filters, sort, in-stock, clear and the empty state were all driven through the
DOM and checked against expected counts. The PDP was re-checked after the CSS
promotions: chips still 48px/2px/Archivo, crumb still Space Mono flex, buy box
still opens on `LGW01-56-RH` in stock.

**Known and NOT fixed:** footer links are 16px tall, well under the 44px tap
target. This is pre-existing on the homepage and the PDP, not introduced here,
and fixing it changes footer spacing on every page — so it is Cole's call.

### 11g. Build commands, current

```bash
python tools/normalize-products.py   # Shopify raw -> products.json
python tools/build.py                # 9 pages
python tools/build.py --check        # diff against disk
python tools/build.py --links        # the registry: 62 declared, 9 built
node   tools/test-variants.js        # variant engine over all 44 products
```

---

## 12. Phase C — the three PDP templates, proven

Built 2026-07-31. **The PDP stopped being a page and became three templates.**
GAMEPLAN §3 predicted clubs, apparel and gear needed different pages; each is
now real and each is proven on a product that stresses it.

| Template | Proof product | What it stresses |
|---|---|---|
| club | LGP02 Tracer Mallet | 1 axis not 2, blade-or-mallet not the loft ladder, no by-loft matrix |
| apparel | Contour Classic Polo | size is the decision, 9 sibling colourways, no spec table, no reviews at all |
| gear | Lucky Blade Cover | **zero axes** — no pickers render — and five sections instead of fourteen |

Built pages: **12 of 62.** Output length falls the way the gameplan said it
should: club 228 KB, apparel 184 KB, gear 170 KB.

### 12a. The template engine — `tools/template.py`

Mustache-shaped, ~120 lines, deliberately dumb:

```
{{name}}                 insert
{{#name}} … {{/name}}    repeat a list · render once if truthy · skip if falsy
{{^name}} … {{/name}}    the inverse
{{.}}                    the current item, for plain string lists
```

Mustache's shape was chosen because `{{#x}}` maps almost directly onto Liquid's
`{% for %}` / `{% if %}`, so these templates hand over to a Shopify developer
legibly. **No escaping** — every value is authored copy from `_src/data/copy/`,
much of it intentional markup. It renders trusted content only and must never
be pointed at user input. **No dotted paths, no filters, no partials**: if a
template needs one, the data is shaped wrong and `build.py` flattens it instead.
An unclosed or mismatched section raises rather than silently swallowing a block.

`{{link:…}}` and `{{count:…}}` are not in the context, so the engine leaves them
for their own passes. Only the page's own sources are rendered — core.css and
core.js are shared, contain no tokens, and are not a place for a surprise.

### 12b. Where a product page's content lives now

```
_src/data/products.json        catalogue: price, SKUs, axes, stock          (generated)
_src/data/copy/<id>.json       editorial: every sentence on the page        (hand)
_src/data/reviews/<id>.json    verbatim Judge.me                            (pulled)
_src/page-<club|apparel|gear>.html   the template                          (no product named)
```

Nothing is typed twice. A cross-sell row names a product id and `build.py`
resolves price, rating and stock through the catalogue — so a neighbour selling
out updates every page pointing at it. `oav` rows tag themselves "Sold out"
automatically for the same reason.

**LGW01 survived the conversion.** The visible text diff against the
pre-template page was five lines, every one explained: a source line-wrap, the
sticky bar's variant line moving from hard-coded to rendered, and one
deliberate "a wedge was never meant to do" → "a club" in the now-shared modal.

### 12c. Two more things had to be split out of the club page

Same lesson as `.chip` and `.crumb` in §11b, one level up. **A page loads
`core.*` plus its own stylesheet and script and nothing else**, so the apparel
and gear templates could see none of the fold, buy box, rails or review widget.

```
_src/pdp.css   fold · buy box · cross-sell rails · reviews · (shared by all 3)
_src/pdp.js    gallery · N-axis buy box · accordions · rails · review widget
_src/page-club.*      specs · loft ladder · blade-or-mallet · the look · the reel
_src/page-apparel.*   sibling colourways · size guide
_src/page-gear.*      the two-up detail block
```

**This is now a three-strike pattern. Before building a fourth page type, check
whether what you are reusing lives in `core.*`/`pdp.*` or in some other page's
file.** Two club-only rules (`.spec-tab` responsive) leaked into `pdp.css` in
the split — harmless unused selectors, worth tidying in a dedicated pass.

### 12d. The near-miss that changed the smoke test

Splitting `pdp.js` out dropped it from the bundle entirely for one build. The
page **still assembled, still had every CSS rule, and `--check` still said
"identical"** — because `--check` compares output to disk, and the disk had just
been written from the same broken build. Only a 30 KB size drop gave it away.

`REQUIRED` now checks **JS as well as CSS**: `function paintPickers`,
`LG_VARIANTS`, `function paintLoftFinder`. Verified by emptying `pdp.js` and
watching the build exit 1.

**`--check` answers "did the sources change?", never "is the output correct."**
The smoke list is the only thing standing between a silent bundling mistake and
a page that looks right and does nothing.

### 12e. Reviews are real or absent — never borrowed

- **LGP02: all 58 pulled**, both Judge.me widget pages. The computed mean is
  273/58 = 4.7069 → 4.71, which matches the rating Shopify reports, so the
  histogram is exact rather than sampled.
- **Both LGP02 1-star reviews are "no left-handed putter" complaints from 2024.**
  LGP02 has shipped a left-hand variant since (89 in stock), so the product
  answers them — worth knowing before reading the histogram as a quality signal.
- **The polo and the cover have no reviews at all**, so the widget renders an
  empty state saying so rather than borrowing a score from a sibling.
- LGP02 has no Judge.me AI summary, so that block is simply absent — none was
  invented to fill the hole.

### 12f. Editorial gaps recorded rather than filled

- **The polo size table is dashes.** Chest, body length and sleeve are not
  published anywhere verifiable, so they render as em-dashes with a note saying
  why. This is the single most useful thing that could be added to that page —
  wrong size is the most common reason apparel comes back, and a table of
  dashes does not prevent that. Same rule as the clubs' "Needs spec" chips.
- **Apparel lifestyle photography still does not exist.** The polo's one slot
  is a labelled brief. HANDOFF §7b F is now blocking a shipped page, not a
  hypothetical one.
- The blade cover's closure, material and dimensions are three "Needs spec"
  rows — Shopify has no description for it and the reference guide does not
  cover head covers.
- Fabric, fit, weight and care ARE verified, from the copy skill's Product
  Reference Guide. That guide is also explicit that **apparel does not get the
  clubs' value-comparison framing**, so there is no middlemen-and-markups
  argument on the polo page.

### 12g. Adding the remaining 40 pages (Phase D)

1. Write `_src/data/copy/<id>.json`.
2. Pull reviews to `_src/data/reviews/<id>.json` if the product has any.
3. Set `built=True` on that handle in `normalize-products.py`.
4. `python tools/normalize-products.py && python tools/build.py`.

No template edits. The registry already routes all 44, and `product_copy()`
fails the build if a product is marked built without an editorial file.

---

## 13. Cole's review notes, 2026-07-31 (rev after Phase C)

Six notes off the first real look at the built pages. Five are done; one is not.

**1. Mega-menu club photos were clipped.** `.mt-img` sat at `right:-14px;
bottom:-24px` and bled off a tile with `overflow:hidden`, so the LGW01 head was
sliced down its right edge. A wedge shot on the diagonal has no spare margin to
give away. Now fully inside the tile (`right:12px; bottom:12px; 128px`), with
the tile's right padding widened to 156px to match. The hover nudge carries the
movement the bleed was reaching for.

**2. Mega menu drops the family word.** Cole's call: the menu shows the code,
not "Carver" in front of it — `LGW01 Gold`, `LGW02 Gold`, `LGW02 Black`,
`LGP01 Blade`, `LGP02 Mallet`, `LGH01`. The finish stays because two of the
wedges are both LGW02. Page H1s keep the full `Carver LGW01 Gold`.

**3. Club collection pages — NOT DONE.** Cole sent Takomo's Iron Sets page as
the reference: products grouped into labelled bands, a "what's the difference"
comparison table with spec bars, a fitting CTA, then brand story sections. Ours
is one flat filtered grid. This is a real piece of work and it is the largest
outstanding item.

**4. Gear copy was too serious — fixed on the cover.** Takomo's glove page is
dry about what the thing is ("yeah, it's a glove") and then useful. The blade
cover now opens "It's a head cover. It goes on the putter, it stays on the
putter" and keeps the compact spec list. **This is the voice for the remaining
twelve gear pages.**

**5. Product cards were text-first.** They were built text-above-photo from a
misread of Takomo, whose cards lead with the image. Reordered in the MARKUP, not
with CSS `order`, so DOM sequence matches reading order — in all three places
tiles are built (homepage, the PDP cross-sell grids, `page-plp.js`). The tag
chip moved onto the photo.

**6. Radius — there was no standard, and that was the problem.**
`.ptile` had **no border-radius at all**; everything else used a flat 4px, which
on a 420px card reads as a chamfer rather than a corner. Now a two-step scale,
because one radius cannot serve a 48px chip and a 420px card:

```
--r        6px   controls  — chips, buttons, inputs, selects, small badges
--r-card  14px   surfaces  — product tiles, panels, image wells, modals
```

Supersedes the flat 4px locked in §4. Borders stay 2px. **Rule: the radius
follows the size of the surface, not the type of component.**

### 13a. Phase D — family defaults

`_src/data/copy/_family-<family>.json` merges **under** each product's own file.
Thirteen polos share one fabric block, one fit note, one size guide and one
returns line; writing that thirteen times is thirteen chances for it to drift.
A product file carries only what is different about that product, and any key it
sets wins outright — no deep merging, because a half-overridden list is harder
to reason about than a repeated one.

**Nine hat pages built this way.** Each file is a photo, a buy-box line, a
design story and a lifestyle brief. Everything else comes from the family file.

**The tenth hat is deliberately not built.** White Upside Down's only photograph
is `59.webp`, which has inverted lettering (§6). A page whose single image is
wrong is worse than no page. Reshoot, then flip `built=True`.

---

## 14. Phase D complete — 43 of 44 products

Built 2026-07-31. **51 pages.** Every sellable product has a page except one.

| Batch | Count | Notes |
|---|---|---|
| Hats | 9 | 0-axis, shortest pages in the store |
| Polos | 13 | 1 axis (size), sibling strips, no reviews anywhere |
| Gear | 13 | dry voice per §13.4, per-variant pricing on the grips |
| Clubs | 8 | spec tables from each product's own Shopify description |

**Not built: `hat-white-updown`.** Its only photograph (`59.webp`) has inverted
lettering (§6). A page whose single image is wrong is worse than no page.
Reshoot, then flip `built=True` — the copy slot is the only thing missing.

### 14a. Family defaults carried it

`_family-<family>.json` merges **under** each product's own file:

```
_family-wedge  _family-putter  _family-hybrid  _family-driver
_family-polo-classic  _family-polo-blade  _family-hat
_family-headcover  _family-grip  _family-glove  _family-tee
```

A product file is now a photo, a buy-box line, a description and whatever specs
that product actually publishes. Everything shared — marquee, care notes, size
guide, closing CTA, cross-sell — lives once. **The hybrid and the driver each
got a family file despite being one-product families**, because the merge is
keyed on `family` and the build fails without one.

### 14b. Specs came from each product's own Shopify description

The driver and the hybrid publish real numbers and their tables are nearly
complete. **Nothing was carried across between products** — LGW01's 1020 steel
and 300 g head are LGW01's, and the LGW02 tables are mostly marked rows because
Shopify gives that club prose instead of figures. Unverified counts by page:
LGW02 Black 11, driver 6, grips 3 each.

Newly recovered from Shopify descriptions, previously unrecorded here:
- **LGD01:** 10.5&deg; loft, 59&deg; lie, 193 g head, **450cc** (not 460),
  45&Prime; shaft, 61 g graphite, stiff, Runner standard grip.
- **LGH01:** titanium, 19&deg;, 200&ndash;220 yd, stiff graphite, black rubber
  grip, **limited run of 100**.
- **LGP01:** 431 stainless casting, 3.5&deg;, 72&deg; lie, 385 g, 35&Prime;.
- **LGP02 Patriot:** high-MOI mallet, twin navy fangs, soft white face insert,
  red clover, **50 units only**, for America's 250th.

### 14c. Reviews: real, or the page says so

Only LGW01 (47 of 551) and LGP02 (all 58) have review text in the repo. The
other six clubs have **real Judge.me scores but no pulled reviews**, which would
have rendered a star filter and a sort control over an empty list — that reads
as a bug. The club template now gates the filter/list/pagination on
`reviewSample`, and shows the score with a line explaining the widget swap
instead. Apparel and gear have no reviews at all and say so.

**Pulling the remaining six clubs' reviews is the highest-value follow-up**
— the Judge.me widget URL in §5 works without auth, and LGP02's pull took two
requests.

### 14d. Still open

- `hat-white-updown` — blocked on a reshoot.
- **Polo measurements** — 13 pages now carry a table of dashes.
- **Apparel and gear lifestyle photography** — every page has a written brief
  and no image behind it.
- Club collection redesign (§13.3), deferred by Cole to after Phase D.

---

## 15. Spec-sheet corrections and two discontinued products (2026-07-31)

Cole confirmed the **Product Reference Guide is the authority on product facts**
and Shopify is not. Reading it in full rather than grepping it turned up real
errors on pages that had already shipped.

| Club | Was (from Shopify) | Is (from the guide) |
|---|---|---|
| LGP02 | 385 g, "face-balanced", material unstated | **365 g**, **slight toe hang (plumber neck)**, 100% CNC-milled **304 stainless** |
| LGP01 | "431 stainless casting" | **100% CNC-milled** 431 stainless, deep precision-milled face |
| LGH01 | lie/weight/shaft all "Needs spec" | Lie 59&deg;, **235 g**, Lucky Graphite S stiff 40.5&Prime; mid kickpoint, Flex Channel face, Glide Sole, gold face + **gloss black crown**. Not forged, not CNC-milled |
| LGW02 | mostly "Needs spec" | Forged 1020, sandblasted, 300 g, **lie 63.5&deg; at 52&deg; and 64&deg; at 56/60** |

**The worst of these was fitting advice, not a number.** The blade-or-mallet
module said the mallet was face-balanced and sent straight-back-straight-through
strokes to it. The guide says **both Tracers suit an arc** — the blade is for
players who release the head, the mallet has a slight toe hang and adds
forgiveness. The real trade is feel against forgiveness, and the module on both
putter pages now says so.

**Lesson: read the reference guide end to end before writing club copy.** It is
200 lines. Grepping it for the product you are working on misses the fact that
it contradicts Shopify elsewhere.

### 15a. Discontinued — pages removed

- **LGD01 driver.** An old model Cole is deleting from Shopify. A new driver is
  coming and **its specs are not in the guide** (v1.1 has no driver section at
  all). `built=False`, page deleted, reason recorded in the overlay.
- **LGP02 Patriot.** The fifty-unit run for America's 250th, sold out and being
  removed. Same treatment.
- **LGH01 is no longer a limited run.** The "100 units" claim is gone from the
  copy and the marquee.

### 15b. The white hat was an overcorrection

`hat-white-updown` has **ten photographs in Shopify**, not one. §6 flags
`59.webp` specifically; the other nine were never the problem. The page is built
on `60.webp` with 59 excluded and the reason recorded in the copy file so nobody
reinstates it. **42 of 44 products now have pages** — the two gaps are the
discontinued ones.

### 15c. Reviews

LGH01's twenty are pulled — one widget page covers the set, so the histogram is
exact. Its `_note` records the thing the score hides: **every sub-5 review that
discusses play flags the shaft as soft or twisty**, and the club offers one flex.

Still to pull, both straightforward — the widget URL is in §5 and takes the
Shopify product id:

- **LGP01** 147 reviews, id `8882491162901` (5 pages of 30)
- **LGW02 Gold** 69 reviews, id `9282811232533` (3 pages)

### 15d. What the guide does NOT have

- **No driver at all** — so the new driver's specs must come from elsewhere.
- **No polo or hat measurements** — the size tables stay dashes until Cole
  supplies them. This was the one thing hoped for from the guide.
- **No gear section** — head covers, grips, gloves and tees are unspecified,
  which is why those pages carry so many marked rows.

**Cole has offered a fuller MD file. Ask for it — it is the only route to the
new driver and to apparel measurements.**

---

## 16. Cole's second review pass — nine notes (2026-07-31)

### The root cause behind three of them

`core.css` defined **`.ptile .pt-ph` and `.ptile .pt-tag` twice** — once under
PRODUCT TILES and again under STUDIO CUTOUTS. The second block won, so:

- the photo-first margin never applied, leaving **a cream band above every
  product image**;
- the tag inherited `top:0` from one rule and `bottom:0` from the other, which
  **stretched SOLD OUT into a full-height black bar** down the side of the card.

One definition each now. **A component defined in two places is a component
that will drift** — this is the same lesson as `.chip` and `.crumb`, from the
inside of one file rather than across two.

| # | Note | Done |
|---|---|---|
| 1 | Cards look wrong, sold-out looks broken | Duplicate rules collapsed. Chip is 68×25 in a 309px well, not a bar |
| 2 | Never show review counts on cards · empty black callout | `.pt-rt` gone from every tile; an empty tag no longer renders an element |
| 3 | Drop the "it costs $X because we sell direct" para | Removed from all four club pages that carried it |
| 4 | "One length, one weight, both hands" tries too hard | All five club spec headlines are now "The numbers" |
| 5 | Delivery/returns links: underline, own line, no stock count | `.bx-links`, underlined, and the stock line says only when it ships |
| 6 | Colourway swatches in the buy box | Added **above** the size picker — see below |
| 7 | Quick add on the collection grid | Added, with the sized-product rule |
| 8 | Trust row layout | Three even columns instead of a wrapping flex row |
| 9 | Material/care dropdown on apparel | Already there — "Fabric and care", open by default |

### 16a. Where the swatches went, and why

**Above the size picker, inside the buy box.** Colour is the first decision —
you choose which shirt, then what size — and the swatch row is what stops a
thirteen-product range feeling like one product with a dead end.

The swatch set includes **the product you are on**, marked with a gold border.
A swatch row with a hole where you are standing reads as a missing colour
rather than as the current one.

The larger "More colours" section lower down stays. It is doing a different
job: swatches are for deciding, the strip is for browsing at a size where you
can actually see the print.

### 16b. Quick add follows the same rule as the cross-sell tiles

A product with **no option axes and exactly one sellable variant** gets a real
Add button carrying the real SKU. Anything with a choice gets
"Choose hand →" / "Choose size →" to its own page, because there is nothing
sensible to put in a bag without that choice. Sold-out products show the state
instead of a control.

### 16c. Stock quantity is no longer published

The buy box used to print "Low stock — 2 left" under 25 units. That is
inventory data a shopper has no use for and we have no reason to broadcast.
The line now says when it ships and nothing else. `qty` is still in the data
and still drives nothing visible.

---

## 17. Reference Guide v1.8 and Cole's third review pass (2026-07-31)

Cole supplied **Product Reference Guide v1.8** as a .docx. Extracted to
`_src/data/` context via `zipfile` + regex on `word/document.xml` — the Read
tool cannot open .docx, but unzipping it can.

### 17a. What v1.8 settles

- **There is no driver.** v1.8 says Lucky sells across four categories: wedges,
  putters, hybrids, apparel. LGD01 staying discontinued is correct.
- **No headcover ships with any club.** Every club entry says so explicitly.
  That closes the "Headcover: Confirm" chip on all eight club pages.
- **Grinds are published:** LGW01 K Grind, LGW02 Gold **S Grind**, LGW02 Black
  **K Grind**. The mega menu's original "K Grind / S Grind" sub-lines were
  right after all — they were removed as unverifiable in §13 and the guide has
  since confirmed them.
- **LGW02 Black is built on the LGW01 platform** — K Grind, LGW01 lies and
  bounces, six lofts. The LGW02 name signals tier and price, **not** a shared
  platform with LGW02 Gold. The two have different grinds and different specs.
- **LGW02 Black is right- AND left-hand** per the guide, but Shopify lists only
  right hand. The buy box follows Shopify because that is what is buyable;
  **worth confirming which is current.**
- **Full manufacturer spec tables** — per-loft lie, bounce, head weight and
  length for LGW01, LGW02 Gold and LGH01, plus shaft flex, kick point, original
  length/weight and grip weight for every club. Shafts are **Regular flex** on
  wedges and putters, **Stiff** on the hybrid.
- **Polo fabric is 88% polyester / 12% spandex**, plus **wrinkle-resistant** and
  **easy to clean**, which v1.1 did not carry.
- **Hats have a moisture-wicking sweatband and laser-cut ventilation** — the
  first construction facts we have had for them.

**Still no apparel measurements.** Colorways and hat SKUs are explicitly "not
tracked here". The size tables stay dashes.

**v1.8 drops the "slight toe hang / plumber neck" line that v1.1 carried for
LGP02.** It is a pure spec sheet now and toe hang is not in it. Treat the toe
hang claim as unconfirmed until it reappears somewhere.

### 17b. The return policy was wrong in ways that cost money

v1.8 carries the real policy and the modal contradicted it:

| Modal said | Policy says |
|---|---|
| "Play it, take it to the range, hit it out of a bunker" | **One wedge per order** may be opened and tested, **on a turf mat**, and must return with no groove or face wear |
| Implied you just post it back | **All club returns need approval and photo verification first**; unauthorized returns are refused |
| "Needs confirming — who pays return shipping" | **The customer does.** Original shipping is not refunded |
| Nothing about tags | Apparel returned **without tags has $7 deducted** |

All three templates' returns modals are rewritten from the policy. Putters may
be used but must come back unmarked; hybrids must appear completely unused.

### 17c. Cole's notes 1, 2, 4, 5, 6

1. **Price note removed** from every PDP, and the price itself dropped from
   display type to 1.5rem / weight 600 — it was competing with the H1.
2. **"Choose hand" was wrong on a wedge**, which also has a loft to pick.
   Clubs now say **"Build it"**; apparel keeps "Choose size", where size really
   is the only choice.
4. **Collection cards carry name and price only.** SKU stamp and variant
   summary both gone — a browse card is for recognising a product and its
   price.
5. **Quick add moved onto the photograph**, bottom-right, the way Primo does
   it. Under a name and a price it read as page furniture; Cole did not find
   it at all. Below 620px it goes full-width under the image, because the pill
   would otherwise cover a third of a 168px photo.
6. **American spelling.** 106 substitutions across 41 files — colour, centre,
   grey, odour, behaviour, neighbour. `centre-none` and `eyebrow centre` are
   CSS class names and were protected from the sweep.

**Lesson: the copy had drifted British throughout and nobody caught it for four
phases.** Lucky is a US brand selling to US golfers. Check spelling on any new
copy file.

---

## 18. Session close — where everything stands

**50 pages built. 42 of 44 products.** The two gaps are the discontinued driver
and Patriot putter.

### 18a. Resolved this session

- **v1.8 spec tables written in.** Zero "Needs spec" chips remain on any club
  page — the LGW01 alone had nine. Per-loft lie, bounce, head weight and length;
  shaft flex, kick point and grip weight for every club.
- **Grinds restored to the mega menu** now that v1.8 publishes them. They were
  pulled in §13 as unverifiable; the Black is K Grind, not the "blacked-out
  wedge" the menu said before.
- **LGW02 Black: right hand today, left hand coming** (Cole). Carries the
  `.soon` pill rather than a flat "right hand only" — the buy box picks up left
  hand automatically once the variants exist in Shopify.
- **Returns policy rewritten from v1.8** across all three templates.
- **American spelling** — 106 substitutions across 41 files.
- **All five clubs that have reviews now have them.** LGH01 and LGP02 are
  complete sets; LGW01, LGW02 Gold and LGP01 carry the **exact live histogram**
  with a first-page sample, so the bars and the star filter agree with the live
  widget.

| Product | Live | In the page |
|---|---|---|
| LGW01 Carver Gold | 551 | 47 |
| LGP01 Tracer Blade | 147 | 22 |
| LGW02 Carver Gold | 69 | 30 |
| LGP02 Tracer Mallet | 58 | **all 58** |
| LGH01 Stryker | 20 | **all 20** |

LGW02 Black has no reviews and correctly shows none.

### 18b. Outstanding

**Blocked on Cole:**
- **Polo and hat measurements.** v1.8 does not carry them and says colorways
  and hat SKUs are "not tracked here". Twelve polo pages show a table of
  dashes. Cole has said these are coming.
- **Apparel and hat lifestyle photography.** Every one of the 22 apparel pages
  carries a written brief and no image. Still the largest asset gap on the site.
- **The new driver.** v1.8 has no driver section at all.

**Not blocked, not done:**
- **The club collection redesign** (§13.3). Takomo groups irons into labelled
  bands with a comparison table and a fitting CTA; ours is one filtered grid.
  Cole deferred it to after Phase D, and Phase D is done. **This is the next
  build.**
- Phases E (Our Story, Trybe), F (support cluster, search, 404) and G (link
  audit + the developer handoff doc). Ten pages remain unbuilt: `story`,
  `trybe`, `reviews`, `returns`, `shipping`, `contact`, `faq`, `search`, `404`
  and `c/sale`.

### 18c. Two facts to verify when convenient

- v1.8 drops the **"slight toe hang / plumber neck"** line v1.1 carried for the
  LGP02. It is out of the copy until it reappears somewhere citable — but it is
  the detail the blade-vs-mallet advice leans on.
- **LGW02 Gold's 50°, 54° and 58°** are listed as in production. When they land,
  add their manufacturer rows and the by-loft table extends itself.

---

## 19. Visual references Cole sent — described, because the images do not carry

Screenshots die at the session boundary. These are the references behind the
outstanding work, written down so the next session is not guessing.

### 19a. Takomo "Iron Sets" collection page — the model for §13.3

The club collection redesign is measured against this. What their page does that
ours does not:

1. **Products are grouped into labelled bands**, not one flat grid. Three bands,
   each with a small centered heading above a 3-up row:
   *New 2025 models* · *Forged players' irons* · *Whole strikers* (approx).
   Each band is a different tier of the same category.
2. **Every card carries a colored tag chip below it** — a short word in a
   colored pill (their orange), sitting under the price rather than on the
   photo. One per product, naming the character of the club rather than its
   state.
3. **A "WHAT'S THE DIFFERENCE" comparison section** below the grid: three
   products side by side, each with its photo, name, price, and a stack of
   **horizontal segmented spec bars** — forgiveness, distance, workability and
   so on, each drawn as ~10 segments with some filled. Underneath each, a short
   key/value list (handicap range, launch, offset, blade length, top-line
   thickness, sole width). This is the single biggest thing ours lacks.
4. **A "NEED HELP FINDING THE RIGHT CLUB?" CTA** in a colored button under the
   comparison.
5. **Then brand story sections** — a full-bleed photo band with a headline over
   it, then three alternating image/text rows (photo left / copy right, then
   reversed), then a testimonial over a dark course photo, then an email capture.

The page is long and it is a *page*, not a product list. Ours currently ends at
the grid.

### 19b. Primo product cards — the model for the collection tile

Cole sent their polo collection. Their card:

- photo fills the card, no padding above it;
- a **NEW** chip top-right, and a red **SOLD OUT** chip under it when relevant —
  both small, both on the photo;
- a **QUICK ADD** pill bottom-right of the photo with a small bag icon;
- under the photo: **product name and price on one line**, name left, price
  right;
- under that, the **product type in small grey text** ("Classic Polo");
- under that, a **row of small round color swatches** — the colorways available,
  as circles, one of them ringed to show the current selection.

Ours matches most of this now (§16). **Not yet done: the type line and the
round color swatches on the card.** The swatch row exists in the buy box but
not on the collection tile.

### 19c. Primo PDP — the model for the swatch row (§16a, done)

Colors as a grid of square thumbnails above the size picker, split into "Basic
colors" and "Seasonal color", with an unavailable one struck through
diagonally. A fit line ("Tapered-Fit") with an info icon, and a "Size Guide"
link on the same row, right-aligned. A model-height note overlaid on the main
photo: *"Wes is 6'1", weighs 225lbs, and wears Large."*

**That last one is worth stealing** once apparel photography exists — it does
more for sizing confidence than a measurement table, and it costs one line of
copy per product.
