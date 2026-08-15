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
- ~~The club collection redesign (§13.3)~~ — **done, see §20.** Four pages from
  a new `clp` template: bands, a comparison with segmented spec bars, a fitting
  CTA on the brand field, story rows and a real review.
- Phases E (Our Story, Trybe), F (support cluster, search, 404) and G (link
  audit + the developer handoff doc). Ten pages remain unbuilt: `story`,
  `trybe`, `reviews`, `returns`, `shipping`, `contact`, `faq`, `search`, `404`
  and `c/sale`.

**§18 is superseded on two counts by §20:** `hybrid-driver` is now `hybrid`,
and the driver and the Patriot are out of every collection rather than merely
pageless.

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

---

## 20. The club collection redesign — §13.3, built 2026-07-31

The largest outstanding item from Cole's first review pass. Takomo's Iron Sets
page (§19a) groups products into labelled bands with a comparison table and a
fitting CTA; ours was one flat filtered grid that ended at the grid.

**Four pages from one new template.** `_src/page-clp.{html,css,js}`, routed by a
`tpl` field on the collection record — `clp` for the club collections, `plp` for
the flat grid that is still the right page for thirteen polos.

```
10-collection-clubs.html    6 products · 3 bands · family router
10-collection-wedges.html   3 · 2 bands (by grind) · 3-way comparison
10-collection-putters.html  2 · 2 bands (blade/mallet) · 2-way comparison
10-collection-hybrid.html   1 · 1 band · no comparison, no router
```

Section order and fields:
`white(head) -> white(bands) -> breath -> cream(router OR comparison) ->
brand(fitting CTA) -> white(story) -> ink(one real review) -> cream(rest of store)`

Green lands mid-page on every club collection now, which is the thing §1 said
was missing from browse pages. No closing CTA, same reason as §11d.

### 20a. The grid is rendered, not painted

The PLP paints its tiles in JS because it has facets, a sort and an in-stock
toggle. A club collection has none of those — bands replace the filter row — so
`build.py` renders the grid into the HTML. A Shopify developer gets markup that
maps onto a Liquid for-loop directly, and the page works with no script at all.

`page-clp.js` exists only to declare `LG_CART_UPSELL`. Quick add rides core.js's
`[data-add]` delegation and the reveal rides its observer, both already running.

### 20b. Every bar is a published number — this is the load-bearing rule

The reference draws forgiveness / distance / workability bars. **We have not
measured any of those and did not invent them.** Every bar on these pages is a
figure from the v1.8 manufacturer spec sheet, prints that figure beside itself,
and states its scale under the module:

| Bar | Scale | Source |
|---|---|---|
| Lofts in production | one segment per loft, 50&deg;&ndash;60&deg; | v1.8 loft lists |
| Bounce across the lofts | 0&deg;&ndash;14&deg;, one segment per 2&deg;, lit as a **range** | v1.8 per-loft tables |
| Head weight | 320&ndash;400 g, one segment per 10 g | v1.8 putter tables |

Segments carry `data-on` individually rather than being one filled width,
because bounce is a range — 8&deg;&ndash;12&deg; lights segments 4 and 5, not 0&ndash;5.

**If you add a bar, add its source with it.** A bar with no number beside it is a
rating, and this project does not publish ratings it cannot cite. Same rule as
the "Needs spec" chips.

The putters page carries **one** bar, deliberately. Loft, lie and length are
identical across both Tracers — head weight is the only figure that differs, and
saying so out loud is a better page than three invented bars.

### 20c. Bands must cover the collection exactly

`build.py` fails if a product in the collection is in no band, in two bands, or
in a band but not in the collection. Without it, adding a club to
`products.json` would quietly leave it off the page — the failure mode a flat
grid does not have, and the reason the flat grid was safe to leave unattended.
Verified by breaking it.

A club collection with no `_src/data/copy/_collection-<id>.json` also fails the
build, same contract as `product_copy`.

### 20d. The character chip is NOT `.pt-tag`

`.clp-tag` sits **under the price**; `.pt-tag` is foil, sits **on the photo**,
and is reserved for genuine news. Cole's rule that a badge on every card is
wallpaper (§9) governs the second one. The first is a different kind of
information — the same descriptor slot filled on every card — so it reads as a
column rather than three competing badges. White on `--brand`, well past 4.5:1.

### 20e. Two discontinued products were still in the store

**This was live.** §15a discontinued the LGD01 driver and the LGP02 Patriot and
deleted their pages, but nothing removed them from the things that point at
products:

- the All Clubs grid rendered both, linking to `#`;
- the driver is 0-axis with one sellable variant, so it rendered **a working
  Quick add** that put a discontinued club in the bag;
- `Hybrid & Driver` was a collection of one hybrid and one dead tile;
- the LGH01 page cross-sold the driver in its browse rail, its bag grid **and**
  a whole comparison column.

Nothing caught it because an unbuilt page resolving to `#` is a normal, counted
state — sixty pages are still to come. **Discontinued is not the same state as
not-built-yet**, and now says so:

- `discon=True` in the overlay. Discontinued products keep their catalogue
  record (the pull is provenance) but leave every collection.
- `cross_sell()` in `build.py` **fails the build** on any copy file pointing at
  one. Verified by putting the driver back into LGH01's browse rail.

Links to discontinued products across the site: **3 -> 0.**

**`hybrid-driver` was renamed to `hybrid`.** v1.8 has no driver section at all,
so a collection named after one held a single hybrid.
`10-collection-hybrid-driver.html` is deleted, not orphaned. When the new driver
lands, add it back and rename.

### 20f. Two things fixed on the way past

- **LGH01's fitting module claimed a 200-220 yd carry**, plus "far better than a
  long iron" and "straighter than a 3-wood". None of that is in the reference
  guide — the carry came off the retired Shopify description — and §15 makes the
  guide the authority. Replaced with loft, lie, head weight, length, shaft and
  face, all v1.8. The module's second option compared the hybrid to the dead
  driver; it now compares two ways of using the same club (instead of a 3-iron,
  instead of a 5-wood), which is what GAMEPLAN §3 always described.
  `rank` and `foot` on a `helpPick` option are now overridable and default to
  today's behavior on every other club page.
- **The "rest of the store" row is generated** from `products.json` for both
  templates, instead of being static markup in one file about to be copied into
  a second. `page-plp.js` no longer removes the current collection from the DOM.

### 20g. A comment cannot contain a link token

`resolve_links()` runs over the whole assembled page **including its CSS**, so a
`{{link:...}}` written illustratively inside a comment fails the build as a
dangling link. It did, twice. Describe the token, do not spell it.

### 20h. Verified

Fresh loads at 1440 and 390, contrast composited through rgba ancestors.

| | 1440 | 390 |
|---|---|---|
| Contrast failures | 0 | 0 |
| Overflow | none | none, `scrollWidth` exactly 390 |
| Band grid | 3-up | 2-up |
| Comparison | 3-up | snap rail at 76% |
| Story rows | 2-col, alternating | 1-col, photo always leads |

Two flagged items are the documented false positives: the `.btn-foil` on the
brand field (the sweep reads `backgroundColor: transparent` and scores ink
against green, when the real field is the gold ramp), and `.stretch`, whose hit
area is a tile-wide `::after` rather than its 367x47 text box. **There is no
`background-clip:text` foil on any of these pages**, so the by-hand foil check
has nothing to catch.

`.clp-cmp-nm` was a 21px link and is now 44px by padding, with the space taken
back off `.clp-cmp-for` so the card reads unchanged.

Also re-checked after the shared-markup changes: the polos PLP still filters,
sorts and counts correctly and its sibling row still drops itself; the LGH01
buy box still opens on $209 with two hand chips.

**Known and NOT fixed**, all pre-existing and shared with the PLP:
- `.qadd` is 38px tall, under the 44px target, on all eleven collection pages.
- Footer links are 16px. Cole's call, unchanged since §11f.
- Inline text links inside a sentence (`.clp-count`, the quote attribution) run
  14-17px. WCAG 2.5.8 exempts inline links, so they are noted, not padded.

### 20i. Still open for Cole

- **The toe-hang contradiction.** §17a and §18c say v1.8 dropped "slight toe
  hang / plumber neck" and that it is out of the copy until it reappears
  somewhere citable. **It is not out of the copy** — `lgp02-gold.json`'s
  blade-or-mallet module still asserts it in the prose and in a fact row. The new
  putters collection page deliberately avoids it and leans on head shape instead,
  so the PDP and the collection page now argue slightly differently. Settle it.
- **Photography.** Eight new labelled briefs across the four pages, two per page.
  Written, specific, and with nothing behind them.
- **`contact` is a stub**, so the fitting CTA's second button resolves to `#` on
  all four pages. Phase F builds it.

### 20j. Build commands, current

```bash
python tools/normalize-products.py   # Shopify raw -> products.json
python tools/build.py                # 50 pages
python tools/build.py --check        # diff against disk
python tools/build.py --links        # 62 declared, 50 built
node   tools/test-variants.js        # variant engine over all 44 products
```

---

## 21. Cole's review of the collection redesign (2026-07-31)

Six notes. All six done, plus four things they turned up.

### 21a. Quick add opens a picker IN the card — it does not go to the page

Cole sent two Primo screenshots: QUICK ADD on the card, and what happens when
you click it — the card fills with **1. CHOOSE SIZE**, a row of size chips and a
**QUICK BUY** button. It adds to the bag from the collection page. Ours linked
to the product page, which was a misreading of the reference.

Now shared in `core.*` (both collection templates paint cards — `page-clp`
server-side, `page-plp` in JS — and a control defined in two page stylesheets is
one that will drift):

```
core.css   .qa .qa-step .qa-lbl .qa-chips .qa-chip .qa-buy .qa-x
core.js    the panel: build, cascade, repaint, close
variants.js  now loaded on collection pages too
```

Three states, and the rule is the same one the cross-sell tiles use:

| Product | Control |
|---|---|
| 0 axes, 1 sellable variant | plain `[data-add]`, real SKU straight to the bag |
| 1+ axes | `[data-qa]` opens the picker |
| sold out | no control at all |

**Clubs take two steps** (Cole's call): *1. Choose hand*, *2. Choose loft*.
Availability comes from `LG_VARIANTS` — the same engine the PDP buy box runs on
and that `test-variants.js` covers over all 44 products. There is deliberately
no second implementation of "is this combination sellable". Verified in the
browser: switching to left hand on the LGW01 greys **50° and 60°**, which are
the two genuinely dead left-hand lofts, and picking 54 resolves to
`LGW01-54-LH`. Grips repaint $9.95 → $11.95 → $14.95 across the grip sizes.

Adding is handed to the existing `[data-add]` delegation: Quick buy carries the
resolved SKU, name, price and variant as data attributes, rewritten on every
selection change. **No new cart code.**

### 21b. Never end-align a flex container that can overflow

The panel was `display:flex; justify-content:flex-end` over the photo well. At
390px the well is 168×168 and a two-axis wedge picker is **320px** of content.
Flex end-alignment puts overflow *above* the scroll origin: "1. Choose hand"
measured at `top:-164px` with `scrollTop` pinned at 0 and `scrollHeight ===
clientHeight`. **On a phone the hand step did not exist and could not be
scrolled to** — and the panel reported "fits".

Fixed twice over: it is a plain block scroll container now, and it mounts on the
whole `.ptile` rather than the photo well, which is 317px tall on a phone
instead of 168. Re-measured: everything reachable, nothing clipped.

### 21c. The wedges page is built around 01 / 02 now — COLE'S PRODUCT DIRECTION

**Read this before editing `_collection-wedges.json`.** The three wedges in the
store today are **all the 01** — different sole grinds and different finishes of
one club. The **02 is a genuinely new club that is coming**, not a re-label of
an LGW02 in stock. Cole chose to make the page official rather than a workaround
("since they will be here soon anyway").

What the 02 will be, per Cole 2026-07-31 — **this is roadmap, not v1.8, and must
not be checked against the reference guide**:

- full-face grooves
- a reshaped head and leading edge, more versatile around the green, more shot shapes
- **cast rather than forged**, specifically so weight can be moved
- progressive weighting through the lofts
- a painted alignment line on the first groove
- more grind options than the 01

It renders as a band with **no product row** — a `.soon` panel, no price, no
loft list, no date, because none of those have been given. **Do not fill them
in from anywhere.** `"coming": false` in the copy file pulls the whole block if
pre-announcing starts costing sales of the wedges that are actually for sale.

The comparison still compares the three 01s (which grind, which finish) and is
now headed *"Pick the sole first. The finish is the easy part."*

### 21d. "Same steel" is banned

Cole, verbatim: *"Anytime that you say same steel I want you to remove that."*
More broadly — **never write copy that flattens the range into one club wearing
different paint.** The 02 has to read as better, not as the same club again.

Three places carried it and all three are gone: the wedges comparison headline,
a wedges story row, and `lgw01-gold.json`'s `specHeadline`, which was still
*"Same steel, same weight, same price. Six lofts."* — §16 note 4 said all five
club spec headlines are *"The numbers"* and that one was missed.

### 21e. No manufacturer tolerances, anywhere

Cole: no `±` deviations. "300 g", never "300 g (±3 g)". **20 figures across 9
copy files**, plus one spec aside on the LGW02 Gold that existed only to state
the tolerance and was deleted outright. Zero `&plusmn;` left in the tree.

### 21f. The homepage club finder had four faults in one section

Cole reported the photos being enormous and the clubs not clickable. Both true,
and two more underneath:

1. **`repeat(auto-fit,minmax(240px,1fr))`** gave a one-card panel a single 1fr
   track, so "The long ones" rendered the Stryker at full page width with a
   photograph to match. Fixed 3 columns now; a tab with one club leaves two
   empty tracks, which is honest — there is one long club.
2. **The cards were `<article>` with no link in them at all.** Now `<a>`.
3. **The prices were hard-coded and stale** — both LGW02s said **$119** against
   a real $109. The finder is driven from `products.json` now via a new
   `_src/data/copy/_page-home.json`.
4. **Text-first cards**, the same fault Cole caught in §13 note 5. Photo leads.

It also had no breakpoints of its own, because auto-fit was doing that job —
2-up at 980 and a `.msnap` rail at 620 now.

### 21g. Radius: an image inside a rounded card must not round itself

Cole on the PDP cross-sell cards: *"the images have way too big of curve, should
these have curve at all and it's not to the edge of the product card itself."*

`.oav-i` carried `--r` (6px, the **control** step) while its own photo carried
`--r-card` (14px, the **surface** step). A 14px curve inside a 6px corner is why
the image read as floating away from the card edge. §13.6's rule is that radius
follows the size of the surface, so:

- the **card** is a surface → `--r-card`;
- the **photo** fills that card edge to edge → **no radius of its own**. The
  card's `overflow:hidden` clips it. This is how `.ptile` has always worked.

**Answer to "should these have curve at all": the card yes, the image no.**

The same fault was one line away: `.gal-stage` — the biggest image well on every
PDP — declared `border-radius` **twice in one rule**, `--r-card` then `--r`, so
the control step won. One declaration now, and it is `--r-card`.

### 21h. Two things the screenshots exposed that Cole did not raise

- **`.pt-rt` was still printing "4.81 ★ 551"** on the PDP cross-sell grids and
  the browse rail. §16 note 2 ruled that a card never shows a review count; it
  landed on the collection grid and the homepage and missed these. 25 rating
  `meta` values removed from 14 copy files, and a **rating in a card meta is now
  a build error** — it is against the rule and it is stale the moment Judge.me
  moves. The variant summary fills the slot instead. **Say the word and this
  reverts.**
- **Disabled chips measured 2.44:1** (`--ink-38` on white). A disabled control
  is formally exempt from the contrast rule, but that is legible enough to look
  like a choice and not quite legible enough to read. Both `.qa-chip[disabled]`
  and `.chip[disabled]` are `--ink-muted` now; the strike-through and the border
  carry "unavailable". This changes the PDP buy box's dead lofts too.

### 21i. A smoke marker must exist in exactly ONE source file

`REQUIRED` listed `"LG_VARIANTS"` to prove the axis engine was bundled. Then
core.js's quick-add started naming `window.LG_VARIANTS` too — so **emptying
`variants.js` entirely still passed the smoke test.** Same class of near-miss as
§12d, from the opposite direction: the marker moved into a file that is always
present.

Both the `club` and `clp` lists now use `function offered(pd, sel, i, val)`,
which exists only in `variants.js`. Verified by emptying it and watching both
fail. **When you add a smoke marker, grep the tree for it first.**

### 21j. Verified

Every changed page swept fresh at 1440 and 390, contrast composited through rgba
ancestors, with a Quick add panel open as well as closed.

| Page | 1440 | 390 |
|---|---|---|
| Home | 0 fails, no overflow | 0 fails, `scrollWidth` 390 |
| Wedges (01 + coming 02) | 0 fails | 0 fails |
| Gear (per-variant pricing) | 0 fails | — |

Driven through the DOM, not eyeballed: the two-axis wedge picker across both
hands, the three-price grip picker, the glove (six of eight combinations dead),
Quick buy landing `LGW01-54-LH` in the bag with the right variant line, the
zero-axis direct add, sold-out cards having no control, and all three finder
tabs returning cards at a constant 419px with live hrefs and catalogue prices.

Build guards verified by breaking each one: band coverage, missing collection
editorial, cross-sell to a discontinued product, a rating in a card meta, the
finder cards losing their link, and the axis engine dropping out of the bundle.

### 21k. Still open for Cole

- **Pre-announcing the 02.** The wedges page now tells a shopper a better wedge
  is coming, on the page where the current ones are for sale. That is Cole's
  call and it is one key to switch off (`"coming": false`).
- **Naming.** A product called *Carver LGW02 Black* sits under a band headed
  *The 01*, because its specs are the 01's. Renaming it in Shopify is what makes
  the page read cleanly.
- The toe-hang line stays in `lgp02-gold.json` per Cole ("if it was in the other
  one then it's fine" — v1.1 carried it). The putters collection page still
  leans on head shape rather than toe hang, so the two argue slightly
  differently; harmless, worth knowing.
- Photography, polo and hat measurements, and the `contact` page are unchanged
  from §20i.

---

## 22. Cole's third pass on the PDPs (2026-07-31)

Six notes. All six done; two of them exposed a third thing each.

### 22a. The size guide is a modal, and it has real numbers at last

Cole supplied the **ATHLETE FIT** chart in inches and centimetres. This was the
longest-standing editorial gap on the site — twelve polo pages had been shipping
a table of em-dashes since §12f.

It is no longer a section on the page. It opens from the **size picker's own
help link**, where the decision is being made:

```
_src/data/copy/_shared-apparel.json   the chart
_src/page-apparel.html                #md-size, using core's generic .md
_src/page-apparel.js                  the unit toggle (new file)
_src/page-apparel.css                 .sg-*
```

**Both unit tables are in the markup and the toggle swaps which is shown.** The
manufacturer publishes inches AND centimetres and they are not exact
conversions of one another — 28.3&Prime; against 72&nbsp;cm is 71.9, 20.5&Prime;
against 52 is 52.1. Computing one from the other would quietly replace supplied
figures with derived ones. **Do not "fix" the rounding.**

The chart's own header says 2XL; the store's size option is XXL. The columns
follow the store so the chart and the picker agree.

### 22b. A third copy layer: `_shared-<template>.json`

The merge order under a product file is now:

```
_shared-<template>.json   true of the template   (new)
_family-<family>.json     true of the family
<product>.json            what is different about THIS product
```

The shared layer exists because the Classic and the Blade share one size chart,
and a 6&times;3&times;2 table copied into two family files is a table that will
drift. `build.py` drops `sizeGuide` from any product with no size axis, which is
how hats inherit the apparel layer without rendering polo measurements.

### 22c. One design section per family, not per design

**22 apparel pages each carried a bespoke headline and two paragraphs about
their own print.** Cole: it should be general and work for any design.

It is one section per family now — Classic, Blade, hat — living in the family
file. What actually differs between colourways is the photograph, not the
garment. `pieceEyebrow` / `pieceHeadline` / `pieceParas` were stripped from **23
product files**; a design that genuinely needs its own paragraph can still set
those keys and override the family.

### 22d. No SKU renders anywhere

Two places did: `#v-sku` under the variant picker, and `.pt-sku` on cross-sell
tiles. Both gone from all three PDP templates, plus the homepage grid and the
club finder. The dead `.pt-sku` rule is out of core.css.

**SKUs are still carried on every variant** — the cart needs them and they are
still never synthesised (§10c). They just never render.

**Consequence worth knowing:** the SKU stamp was the only thing telling the two
Carver Golds apart on a tile — both are `name: "Carver Gold"` at $99 and $109.
Tiles use **`title`** now (Cole's locked full form: family, code, finish), so
they read "Carver LGW01 Gold" and "Carver LGW02 Gold". Applied to the collection
grid, the PLP painter, the homepage grid and the finder.

### 22e. The returns link is in the returns tab

It was its own `.bx-links` line under the trust callouts. It now sits inside the
**Shipping & returns** accordion on all three templates. Gear had no accordion
at all, so it gained one — a policy surface is not the padding §13 note 4 warned
about.

### 22f. The breadcrumb — what was actually wrong, and what I broke fixing it

Measured rather than guessed. The real defect: the current-page item is a
`<span>`, not an `<a>`, so it picked up none of the link sizing — **15.4px tall
against the links' 44px, sitting 14.3px lower than the rest of the trail.** The
page name dropped out of line, which is what reads as clipped. Both now share
one rule.

Also: `.crumb` top padding 18px &rarr; 26px (it is the first thing under a
sticky header), and the trail is `nowrap` with horizontal scroll instead of
wrapping — a four-level trail ending in a long product name wraps on a phone,
and a breadcrumb broken across two lines under a coloured bar looks broken.

**The regression:** the first attempt bled the `<ol>` to the page edge with a
negative `margin-inline` and re-padded it. A nowrap flex row with `overflow-x`
resolves its width from its content once that negative margin is on it — the
`<ol>` came out **1485px in a 1440px viewport and put horizontal overflow on
every PDP.** `min-width:0; max-width:100%` and no bleed is what actually works.
Caught by the sweep, not by eye. **Never bleed a nowrap overflow-x flex row.**

**I could not reproduce a hard clip** at 1440 or 390, scrolled or at rest. The
misalignment above is real and fixed; if it is still cutting off, the window
width and roughly where the page was scrolled would pin it down.

### 22g. The wedges page: gold and black, one tier

Cole: the 01 will be **gold and black only** — not two golds — and today's
LGW02 Gold merges into the 01 as another grind. So the page must not present two
different gold types or two product tiers.

One band, **The 01**, three tiles, differentiated by **finish and grind** rather
than by model. Tags are the grind (`K Grind`, `S Grind`, `K Grind`), which is
what survives the merge. The comparison is headed *"Two finishes. Two soles.
Pick the sole first."*

**When the merge lands in Shopify, delete the LGW02 Gold tile from the band and
the comparison — nothing else on the page has to change.** The `coming` block
for the real 02 (full-face, cast, progressive weighting) is unchanged from §21c.

### 22h. Verified

| | 1440 | 390 |
|---|---|---|
| Polo PDP | 0 contrast fails, no overflow | 0 fails, `scrollWidth` 390 |
| Polo PDP, modal open | 0 fails, all taps &ge;44px | panel 350px, table scrolls in its own container |
| Wedges collection | 0 fails, no overflow | — |

Driven through the DOM: the size modal opening from the picker link, the
inches&rarr;centimetres toggle swapping tables and radio state, focus trapped
and body locked, the returns link resolving inside `.acc-bd`, zero `.pt-sku` /
`#v-sku` on any built page, breadcrumb misalignment at 0px, and the wedges page
carrying no "same steel", no `&plusmn;` and no SKU.

**The size-guide modal is smoke-tested per PAGE, not per template** — it only
exists on a product with a size axis, so `REQUIRED["apparel"]` would fail on
every hat. `smoke()` takes an `extra` list that `build()` derives from the
page's own context. Verified by deleting the modal block and watching it fail.

### 22i. Still open

- The `_family-hat` file lost `fitTitle`/`fitParas` with the size keys — hats
  have no size axis and never rendered them.
- Everything in §21k stands: pre-announcing the 02, the LGW02 Black naming, the
  `contact` stub, photography.

---

## 23. THE 01 — the wedge line collapses into one club (2026-07-31)

**This is the biggest structural change since the templates, and it changes what
the store sells, not just how a page reads. Read it before touching a wedge.**

### 23a. What Cole decided

Lucky sells **one wedge: the 01.** The K-grind gold and the S-grind gold were
two Shopify products at two prices for a difference that is not a difference —
same forged 1020 head, same 300&nbsp;g, same milled and sandblasted face. Grind
is an **option on the 01**, never a tier.

```
Carver 01 Gold    $99    K and S grind    6 lofts    right + left
Carver 01 Black   $109   K grind          6 lofts    right hand today
Carver 02         —      the real one: full-face grooves, cast, progressive
                         weighting, painted first groove. Coming.
```

The $10 is **the blacked-out finish**, which is a genuine extra process. That is
now the only price difference in the wedge line, and the only other one that
will ever be justified is the true 02.

**Cole is deleting the LGW02 in Shopify and folding it into the 01.** This models
that state now, ahead of the store, so the site is not describing a lineup that
is about to stop existing.

### 23b. How the merge works — `merge_grinds()` in normalize-products.py

```
merge:      ["v2-signature-gold-wedge-1"]   fold this product's variants in
grind:      "K" / "S"                       which grind each source is
axisGrind:  True                            Loft -> "Loft & grind"
priceAll:   99                              one price across the product
finishGroup:"carver-01"                     what the gold/black swatch row uses
```

Variant keys gain the grind: `RH|56` becomes `RH|56K` / `RH|56S`. Values sort
**loft ascending, K before S** — `50K, 52K, 52S, 54K, 56K, 56S, 58K, 60K, 60S`,
which is Cole's own ordering.

**Every SKU is still carried verbatim.** `52° S` is the real `LGW02-52-RH`.
Verified in the browser: picking it puts that SKU in the bag at $99 with the
variant line "Right hand · 52° S".

**THIS IS THE ONE PLACE THE OVERLAY OVERRIDES SHOPIFY** rather than only adding
to it — it rewrites variant keys, flattens a price, and removes a product from
`products.json` entirely. It is deliberate and temporary. **When Shopify is
merged: re-pull, delete `merge` / `axisGrind` / `priceAll` and the merged
handle's overlay entry, and the function stops doing anything.**

A single-grind product still gets the combined axis (`axisGrind` without
`merge`), so the Gold and the Black read the same way when you flip finishes.

### 23c. Finish is a swatch row, not an axis

Gold and Black are two Shopify products, exactly like the polo colorways, so
they use the same device — a row of links above the pickers, keyed on
`finishGroup`. Without it the Black is unreachable from the Gold's page.

`.sw` had to move from `page-apparel.css` into `pdp.css` for this. **Fourth time
a component has moved because a page loads core plus ONE page stylesheet**
(`.chip` §11b, the pdp split §12c, `.spec-tbl` §22f, now this).

### 23d. The grind explainer — THE ONLY UNVERIFIED BLOCK ON THE SITE

New section on the club template, `#grinds`, which the buy box's "Which grind?"
link targets. Two cards: K Grind / the all-rounder, S Grind / the shot-maker.

**Cole asked me to draft it and correct it afterwards.** The `facts` rows are
v1.8. The prose — who each grind suits and why — is drafted from the published
bounce plus the standard industry meaning of a K and an S grind, because **the
reference guide publishes the grind NAMES and the per-loft bounce and nothing
whatever about what either does for a player.**

The copy files carry a `_signoff` key saying exactly this, and the section's own
note says it on the page. **Do not treat this block as verified until Cole has
been through it.** It is the only place on the site making a claim that cannot
be traced to a document.

### 23e. Everything that had to move with it

The registry caught all of it — a merged product leaving `products.json` makes
every reference to it a build error:

- `20-product-lgw02-gold.html` deleted; `lgw02-black` renamed to `lgw01-black`,
  so `20-product-lgw02-black.html` is deleted too.
- Mega menu: two wedge tiles now, `01 Gold` (K or S grind) and `01 Black`.
- Homepage: the duplicate gold tile removed from the grid, the finder down to
  two wedge cards, and the hero stamp off "LGW02 · Carver Gold · 52/56/60".
- Footer, All Clubs, the wedges collection, and the LGH01 cross-sells.
- **Spec sheet rebuilt** (Cole asked): the by-loft matrix carries a **Grind
  column** and both v1.8 tables — six K rows and three S rows — and the club
  tab lists both grinds and both lie sets.
- Naming swept: nothing on any built page says LGW02 or "Carver LGW01" any
  more. The only `LGW02` strings left are inside SKUs, which is correct.

### 23f. Also in this pass

- **Carousel callouts are foil now.** `.gal-tag` was a flat `--gold` fill while
  every other emphasis tag ran the ramp. **And a real problem underneath:** ink
  on the ramp's darkest stop `--gold-lo` measures **3.64:1**, a fail at tag
  size, and the contrast sweep cannot see it because it skips gradients. New
  `--lg-foil-tag` drops the shadow stops, so the darkest point is `--gold` at
  6.95:1. `.pt-tag` moved onto it too — it had been failing since Phase 1.
- **Quick add no longer covers the photo.** It was `inset:0`; it is anchored
  bottom now with `max-height:70%`. Measured: **89% of the image still visible
  at 1440, 57% at 390**, with the panel scrolling if the picker is tall.
- **The size guide opened with neither unit selected.** `checked` was a Python
  bool, so it rendered `aria-checked="True"` — CSS attribute matching is
  case-sensitive, so `[aria-checked="true"]` never matched, and it was invalid
  ARIA besides. **Any boolean reaching an attribute VALUE must be a lowercase
  string**; a `{{#section}}` is fine.
- **The size table had no styling at all.** It carried `class="spec-tbl"`, and
  `.spec-tbl` lives in `page-club.css` — which the apparel template does not
  load. Browser-default `<th>` centring and zero padding, which is exactly the
  "weird spacing" Cole saw. `.sg-tbl` is now styled from scratch with a
  `colgroup`: 120px label column, six even 58px size columns.

### 23g. Verified

| | 1440 | 390 |
|---|---|---|
| Carver 01 Gold PDP | 0 contrast fails, no overflow | — |
| Wedges collection | 0 fails, no overflow | — |
| Polo PDP + size modal | 0 fails | panel 350px, table scrolls in its container |
| Quick add | photo 89% visible | photo 57% visible, panel scrolls |

Driven through the DOM: the 9-value Loft & grind picker, `52° S` resolving to
`LGW02-52-RH` at $99 in the cart, left hand correctly killing `50° K` and
`60° K` while every S variant stays live, the gold/black swatch row, the
"Which grind?" link finding `#grinds`, and the size guide opening on Inches
with a filled radio.

`node tools/test-variants.js` passes over all 43 products and 155 variants —
the merged axis included.

### 23h. What Cole still has to do

1. **The Shopify merge itself.** Delete the LGW02 Gold product, move its six
   variants onto the 01 Gold as grind options, and **drop them from $109 to
   $99**. The site already shows that state.
2. **Judge.me.** The 01 Gold page still shows **4.81 / 551** — the base
   product's own real number. The S-grind product's **69 reviews** are not
   folded in, because merging two review sets into a figure no system currently
   reports would be inventing one. After the Shopify merge, migrate the reviews
   and the count becomes 620.
3. **Sign off the grind copy** (§23d).
4. **The 02's specs**, when they exist — no price, no lofts, no date on the page
   until they are real.

---

## 24. Grind copy in Takomo's register, and the 01/02 comparison (2026-07-31)

### 24a. The grind block rewritten

Cole supplied Takomo's F/V grind copy as the model. Their shape: what the sole
is, what the bounce does, who it suits, then **a one-line short version** that
somebody who reads nothing else still reads. Ours now follows it, and the
template gained `.gr-short` for that closing line.

**One accuracy point that has to survive this:** in Vokey's nomenclature a K
grind is the *widest, highest-bounce* sole — but **our K spans 8&ndash;12&deg;
while our S never drops below 10&deg;**, so ours is not simply "the high-bounce
one". The copy describes what we actually publish and keeps the character claims
to what the numbers support. The `_signoff` note in both wedge copy files spells
this out. **Cole still needs to confirm the sole geometry** — is our S actually
narrower, does it have a tapered rear sole — before any of it is verified.

### 24b. The wedge collection compares 01 against 02, not gold against black

Cole: the page's job is the difference between the 01 and the 02. That is the
comparison now. Gold vs black is a *finish* choice and lives on the tiles and in
the buy box, where you are actually picking.

The comparison module gained the ability to describe **a product that does not
exist**: a `coming` column skips the catalogue lookup entirely and renders no
photo, no price, no bars and no buy link, because none of those are real. It
carries the `.soon` marker, a labelled photo brief, and its feature list matched
row-for-row against the 01's:

```
                01                          02  (coming)
Construction    Forged 1020 carbon steel     Cast — for the weighting
Face            Milled grooves, sandblasted  Reshaped head and leading edge
Grooves         Standard face                Full face, heel to toe
Weighting       300 g at every loft          Progressive through the lofts
Grinds          K and S                      More options than the 01
Alignment       None                         Painted first groove
```

Matching the rows is what makes the difference legible — the same six questions
asked of both clubs. The separate `coming` band was removed: one telling of the
02 story, not two.

### 24c. NEXT-PAGES.md

A standalone brief for the ten pages that remain, written to open a fresh
session on: Our Story, Trybe, reviews, the four support pages, search, 404 and
Sale, plus the Phase G developer handoff.

**It answers Cole's question about the policy pages: they do not change,
because they do not exist.** The *content* already does — the real v1.8 policy
is written into the `#md-returns` and `#md-delivery` modals on all 40 product
pages — so building them is lifting and expanding, not writing. The two "Needs
confirming" chips (warranty period, warehouse/duties) are what is missing.

### 24d. Our grind letters are VOKEY'S — and there is a conflict in the numbers

Cole, 2026-07-31: **the K and S are Vokey's nomenclature, not a Lucky scheme.**
He sent Takomo's F/V copy only as a model of tone. That resolves §24a's tension
and corrects a real error in the first draft.

Vokey's meanings, which now govern the copy:

- **K Grind** — the fullest sole with the most camber, the most forgiving of the
  set. Soft turf and sand, steeper attack angles.
- **S Grind** — a narrower sole with heel and trailing-edge relief. A square
  face and a neutral attack, on firm-to-normal turf.

**The first draft called the S "the versatile one, for opening the face". That
is Vokey's M grind, not the S.** Corrected.

**UNRESOLVED, AND COLE NEEDS TO SETTLE IT:** Vokey's K carries the *highest*
bounce of any grind — but our manufacturer sheet gives the **S equal or more
bounce than the K at every shared loft**:

| Loft | K | S |
|---|---|---|
| 52&deg; | 8&deg; | 10&deg; |
| 56&deg; | 12&deg; | 12&deg; |
| 60&deg; | 10&deg; | 12&deg; |

So the copy deliberately describes the **sole shape**, which is what the letter
denotes, and **never claims which grind has more bounce**. The facts rows carry
the real per-loft figures and the spec table below carries them in full. Verified
in the browser: no "more/higher/highest bounce" string appears in the block.

**RESOLVED — Cole 2026-07-31: the spec sheet is true.** The labels are the right
way round and the numbers are real. The apparent contradiction is measured bounce
against **effective** bounce:

> A full, cambered sole puts more of itself on the ground, so it plays every
> degree it measures. A narrow sole with the heel and the trailing edge ground
> away presents less — which is why the S reads higher on paper than the K at the
> same loft and still plays lower through firm turf.

That is standard wedge design, not a Lucky claim, and it is the honest
reconciliation of two facts that are both true. The page **says it out loud** in
`grinds.measured`, set off by a gold rule between the cards and the short
version, and **the spec table's aside repeats it** so the numbers and the prose
can never disagree.

**Anyone editing either one has to edit both.** A customer who reads the table
and not the paragraph concludes the table is a typo.

---

## 25. The Shopify draft, and the support cluster (2026-08-01)

### 25a. Carver 01 Gold exists in Shopify, as a DRAFT

`gid://shopify/Product/9583978905877` · handle `carver-01-gold`
https://admin.shopify.com/store/lucky-wedges/products/9583978905877

Built by duplicating LGW01 Gold (`v1-gold-lucky-golf-wedge`) and correcting the
duplicate. **Neither live product was touched** — Cole archives them himself
after he approves this. Not published to any sales channel
(`resourcePublicationsCount: 0`), not added to a collection by hand.

```
Title    Carver 01 Gold          Status  DRAFT
Price    $99 on all 18 variants
Option1  Hand           Right Hand, Left Hand
Option2  Loft & Grind   50K 52K 52S 54K 56K 56S 58K 60K 60S
```

Option values are in **Cole's ordering** — loft ascending, K before S — set
with `productOptionsReorder` after the variants existed, because
`productVariantsBulkCreate` appends.

**All 18 SKUs were read off the two live products and carried verbatim.** The
twelve K variants came across with the duplicate; the six S variants were
created from LGW02 Gold's real SKUs (`LGW02-52-RH` and friends). Nothing was
synthesised — §10c is why, and 52° S is exactly the case it warns about.

### 25b. The duplicate carried inventory, which the brief did not expect

**`productDuplicate` copies inventory quantities.** The draft holds **2,524
units** across the twelve K variants, and the same stock is still on the live
LGW01 Gold. Nothing can sell — it is an unpublished draft — but **store-wide
inventory totals are inflated until Cole merges.**

Left as-is rather than zeroed: those quantities are carried data, not invented
data, and they make twelve of the eighteen availabilities correct on their own
(including LH 50° K and LH 60° K, which are genuinely dead and stayed dead).

The six S variants are at zero and therefore read unavailable, where the live
LGW02 Gold has all six sellable. **Quantities to move, from the live product:**

| Variant | SKU | Live qty |
|---|---|---|
| RH 52° S | LGW02-52-RH | 38 |
| RH 56° S | LGW02-56-RH | 25 |
| RH 60° S | LGW02-60-RH | 2 |
| LH 52° S | LGW02-52-LH | 94 |
| LH 56° S | LGW02-56-LH | 92 |
| LH 60° S | LGW02-60-LH | 70 |

Tracking and policy match the source on all eighteen: `tracked: true`,
`inventoryPolicy: DENY`, 1.2 lb. So availability behaves the same way once the
stock is there — and `availableForSale` is still not `qty > 0` anywhere else in
the store (§10c).

**Two automated collections picked the draft up** on its copied tags: All
Products (a type rule) and Lucky Golf Clubs (`tag:club`). Not added by hand;
the rules matched. Stripping the tags would keep it out, at the cost of the
tags.

**Nothing in `_src/` changed for this.** The catalogue was NOT re-pulled and
`merge_grinds()` was not touched — the site's merged state is deliberate and
stays until Cole publishes the real product (§23b).

### 25c. The support cluster — four pages, one template

`returns` · `shipping` · `contact` · `faq`, from `_src/page-support.*`.
**53 of 61 pages.** Dead links **678 → 428**; the four that remain are `trybe`
(214), `story` (160), `search` (53) and `reviews` (1).

**Contact is no longer broken.** The "Ask a person" button on all four club
collection pages resolved to `#`; it resolves to `42-contact.html` now.

Editorial is the same two-layer merge the product pages use (§22b):
`_shared-support.json` under `_support-<slug>.json`. The shared layer carries
the four-page list, and **the sibling row on each page is generated from it**
minus itself — a fifth support page needs one entry there and no edits in four
files, the same reason the PLP's row is generated (§11d).

**None of this is new policy.** Returns and Shipping are the `#md-returns` and
`#md-delivery` modals expanded, against Product Reference Guide v1.8's Return
policy section. The modals stay where they are.

### 25d. The FAQ's left-hand answer is generated, not typed

`hand_rows()` in build.py derives it from `products.json`:

```
Carver 01 Gold       Right hand — every loft & grind.
                     Left hand — 52° K, 52° S, 54° K, 56° K, 56° S, 58° K, 60° S.
Carver 01 Black      Right hand — every loft & grind.
Tracer LGP01 Blade   Right hand — sold out at the moment.
Tracer LGP02 Mallet  Right and left hand.
Stryker LGH01        Right and left hand.
```

Left-hand availability is the **most-asked question in the whole review corpus**
— it is in the LGP01 and LGP02 pulls repeatedly, twice at one star. It is also
the answer that goes stale the instant a loft sells out, and "do you make a
left-handed one" is the worst possible question to answer stalely. So it is
derived, like every price and count on the site. It reads `avail`, never
`qty > 0`.

### 25e. `.tbd` had no CSS at all, on 40 pages

`<span class="tbd tbd--light">Needs confirming</span>` has been in the markup
since Phase D — both policy modals and every "Needs spec" row — and **there was
no rule behind it anywhere in the tree.** Every one of those rendered as
ordinary body copy. A gap that looks like prose reads as a statement, which is
the exact opposite of the point.

Now in `core.css`: dashed, Space Mono, `--ink-muted` (5.14:1 on white, 4.94 on
cream). Measured on a live PDP modal at **5.14:1**, 133×22.

It went into core rather than a page stylesheet because the PDP modals and the
support pages both use it, and a page loads core plus exactly ONE page
stylesheet. **Fifth component to move for this reason** — `.chip` (§11b), the
pdp split (§12c), `.spec-tbl` (§22f), `.sw` (§23c), now this.

### 25f. What the two unconfirmed answers do on these pages

Neither was invented. Both carry the modal's own chip, set off by a gold rule:

- **Warranty period, and who pays return shipping when the fault is ours** —
  `40-returns.html#defective`, and again in the FAQ. What v1.8 *does* settle is
  stated: defective gear may be replaced or refunded after inspection, and a
  customized item is returnable if it arrives defective.
- **Warehouse locations, international destinations, duties prepaid or
  collected** — `41-shipping.html#where`, which is a whole section that exists
  to say the question is open.

**A third turned up while writing Contact: staffed hours and a response
target.** There is deliberately no "we reply within N hours" anywhere on the
site — the review corpus contains both a customer emailed back on a Sunday and
one who waited weeks, and a number nobody has committed to internally is worse
than no number. It is the single most useful thing Cole could add to that page.

A fourth, smaller: **the Returns Portal has no URL anywhere**, so Contact and
Returns describe it instead of linking to it.

### 25g. The contact form is markup, and says so before you press it

Real `<form>` fields, shaped for Shopify's contact form. The prototype notice
is a `.tbd` chip **above the fields**, not a message after submit, and the
submit handler stops navigation and repeats it. Verified in the browser: does
not navigate, and **does not thank anyone for a message it never sent**.

### 25h. Two things the sweep caught that eyes did not

- **`.sup-opt`** — the word "optional" on the order-number label — was
  `--ink-38` at 9.9px, **2.44:1**. The same number §21h caught on disabled
  chips. A disabled control is formally exempt from the contrast rule; a form
  label is not. `--ink-muted` now.
- **The email address on Contact** was a 22px hit area, and it is the primary
  control on the page. The FAQ's product links in the hand table were 16px.
  Both are 44px now.

**Still open and NOT fixed here: every footer link is a 16px hit area**, on all
53 pages. It is pre-existing, it is in the shared partial, and changing it
touches the whole site — Cole's call, not a support-cluster edit.

### 25i. The jump nav, and §21b

"On this page" is a nowrap `overflow-x` row on a phone, which is the shape that
put 1485px of overflow on every PDP when it was bled to the page edge (§22f).
It is **not** bled. Verified rather than assumed, because §21b's flex row also
reported "fits" while hiding its first step above the scroll origin:

```
scroll origin 0 · first item visible at origin (left 20)
scrolled to end · last item right 370 == container right 370
page scrollWidth 390 at a 390 viewport
```

### 25j. Verified

Swept at 1440 and 390, contrast composited through rgba ancestors, foil skipped
because the sweep cannot see it (§9).

| Page | 1440 | 390 |
|---|---|---|
| Returns | 0 fails, no overflow | 0 fails, `scrollWidth` 390, jump row reachable |
| Shipping | 0 fails, no overflow | 0 fails, `scrollWidth` 390 |
| Contact | 0 fails, no overflow | 0 fails, `scrollWidth` 390 |
| FAQ | 0 fails, closed AND all 17 open | 0 fails, closed AND all open |
| LGW01 PDP (`.tbd` regression) | chip 5.14:1, no overflow | — |

Driven through the DOM: the deep link into a closed answer on both paths (load
and `hashchange`), a hash matching a group heading, a hash matching nothing
(does not throw), the form's submit interception, and the jump row's scroll
origin and reach.

Build guards verified by breaking each one: the page-support.js marker
(`supOpenFromHash`, by emptying the file), `.tbd` dropping out of core, the FAQ
accordion becoming a `<div>` (fails 43-faq only and lets the other three build
— the per-PAGE `extra` from §22h), a missing editorial file, and a section
losing its `id`.

`--check` reports every one of the 53 pages identical. `test-variants.js` and
`normalize-products.py --check` unchanged.

### 25k. One thing to fix outside the repo

**The `lucky-golf-copy` skill's own example of good returns copy contradicts
the policy.** It reads *"send it back — we'll refund you, and you don't pay
return shipping."* v1.8 says the customer is responsible for return shipping,
and every product page already says so. v1.8 won here, per the skill's own
precedence rule, but that example will produce wrong copy the next time someone
writes an ad from it.

---

## 26. The site is complete, and the copy is re-sourced (2026-08-01)

### 26a. 58 of 61 pages. ZERO dead links.

`678 -> 0`. Every page that can be built is built.

The three not built are all deliberate: **`c/sale`** (blocked — nothing in the
collection carries a `compareAtPrice`, §11e) and the two **discontinued**
products, `lgd01` and `lgp02-patriot`.

Landed this session: the four support pages (§25), Our Story, The Trybe,
Reviews, Search and 404.

### 26b. Three NEW reference documents, and one of them changes the site

Cole supplied four `.docx` files on 2026-08-01. They are extracted into the
repo as markdown beside the existing guide:

```
references-how-we-write-v7.3.md        was v6 in the copy skill
references-culture-v2.md               NEW — golf-culture vocabulary
references-spec-to-benefit-v1.0.md     NEW — what each spec means
references-product-guide-v1.8.md       unchanged, byte-for-byte verified
```

**The Product Reference Guide is identical to the copy already in the repo** —
diffed line by line, no change. The other three are new information.

### 26c. THE GRIND COPY IS NO LONGER UNVERIFIED — and it reversed

This closes the item HANDOFF has carried since §23d as "the only unverified
block on the site".

**Spec-to-Benefit v1.0 defines both grinds directly:**

> **K Grind** — "a wider, flatter sole profile with a standard leading
> edge... the no-surprises wedge... built for the golfer who strikes cleanly
> and plays primarily from standard lies: fairway, rough, fringe."
>
> **S Grind** — "a narrower, more relieved sole with a reshaped leading
> edge... the versatility wedge... tight lies, awkward angles, open-face
> lobs, and bunker shots."

**This REVERSES §24d.** That section recorded that the S is *not* the
open-face versatility grind, reasoning that our letters are Vokey's and that
Vokey's versatility grind is the M. Lucky's own written guide says the S *is*
the versatility grind. A company document about what Lucky's specs mean
outranks an inference from another manufacturer's nomenclature, so the site
now follows the guide.

It also closes §24a's open question — *"is our S actually narrower, does it
have a tapered rear sole"* — in writing: narrower, more relieved, reshaped
leading edge.

What changed on the page, in `lgw01-gold.json` and `lgw01-black.json`:

| | was | now |
|---|---|---|
| K name | The forgiving one | The no-surprises one |
| K for who | Soft turf, and a real divot | Standard lies, and a square setup |
| K sole | Full, with camber | Wider and flatter, standard leading edge |
| S name | The narrower one | The versatile one |
| S for who | Firm turf, and a square face | Tight lies, and an open face |
| S sole | Narrower, heel and trailing-edge relief | Narrower and relieved, reshaped leading edge |

**Note what moved:** the site had given "square face" to the S. The guide gives
"set up square" to the K. That was backwards and is the single most
consequential correction in this pass.

**Every manufacturer number is untouched**, and the measured-vs-effective
bounce reconciliation (§24d) still stands — a narrow, relieved sole carrying
more measured bounce than a wide flat one is exactly what the geometry
predicts, so the new framing makes that paragraph *more* coherent, not less.

`_signoff` in both files records all of this, including how to put the Vokey
reading back if Cole wants it.

### 26d. CLAIMS TO AVOID — audited across all 58 pages, 10 fixes

Spec-to-Benefit v1.0 carries a `CLAIMS TO AVOID` list. Every built page was
scanned against it plus the standing HANDOFF bans. Ten violations, all in our
own copy, all fixed:

| Rule | Where | Fix |
|---|---|---|
| Don't use the word "cheap" | `cover-blade` | "thirty dollars fixes it before it happens" |
| | `cover-driver` | "Thirty dollars, against the most expensive club in the bag" |
| | `grip-putter-clovers`, `grip-putter-green` | "the smallest change that measurably affects putting" |
| | `grip-putter-stock` | "the smallest change you can make to a putter" |
| | `tees-25` | "The least you can spend here" |
| Don't claim "premium" | `lgh01` | "A titanium hybrid at 19 degrees" |
| Don't LEAD with "milled from a single block" | `_collection-clubs` | "both cut from solid stainless so there is nothing inside to rattle" |
| | `_collection-putters` (LGP01) | "Solid 431 stainless... It sits planted behind the ball" |
| | `_collection-putters` (LGP02) | "More head, and the stability that comes with it" |

The spec-table rows that say "Fully CNC-milled from a single block" are
**kept** — the ban is on leading with the process name as a headline, not on
stating it as a spec.

Re-scanned after the fixes: **zero banned claims in our own copy.**

**Two deliberate exceptions, both flagged for Cole rather than changed:**

1. **The Judge.me AI summary on the 01 Gold contains the word "premium"**
   ("Customers praised this premium forged wedge"). It is Judge.me's
   auto-generated text, published verbatim by standing decision (§9B). Ours to
   disable, not to edit.
2. **Competitor names appear on the homepage and the wedges collection** —
   Vokey, Cleveland, Odyssey, Ping, Titleist — every one inside a *verbatim
   customer review*. The rule ("Don't compare to brands by name") governs
   Lucky's claims, not a customer's words. But **choosing** that quote for the
   homepage is arguably making the comparison by proxy, and that is Cole's
   call, not a rule violation to undo unilaterally.

### 26e. How We Write v7.3 — what actually changed from v6

The copy skill still ships v6. v7.3 adds:

- **"The range."** The voice moves between **bold / plainspoken / quiet** —
  "the same person at different volumes". v7 exists specifically so the voice
  "isn't defaulted to quiet by omission".
- **What bold is NOT**: combative us-vs-them framing ("the wedge nobody wanted
  you to find") or wordplay ("new dress code"). Bold in Lucky is "a plain
  statement said with weight".
- **Range within a SET**: four tooltips or six ad variants that all play the
  same shape read templated even when each line is fine.
- **Specs**: not the failure mode. *Stacking* them as proof is. A spec earns
  its place when paired with what it delivers or carrying the line.
- **The fragments rule is now long-form only.** Fragments are the correct shape
  for ads, captions, tooltips and subject lines.
- **Reach vs land**: "playfulness that has to be explained isn't playful".

**Not audited page by page** — that is a subjective register pass across ~58
pages and it needs Cole's eye, not a regex. The site's long-form reads
plainspoken throughout, which v7.3 permits but which is also the "defaulted to
quiet" failure v7 was written to name. Worth a review pass on the homepage and
the collection ledes specifically.

**The `lucky-golf-copy` skill should be updated to v7.3** and given the two new
documents. Its returns-copy example still contradicts v1.8 (§25k).

### 26f. The review widget moved out of pdp.js

`32-reviews.html` needed the histogram, star filter, sort and paging the PDPs
already had. Rather than a second implementation:

```
_src/reviews.js     LG_REVIEWS.mount(root, data, opts)   — the whole widget
core.css            .jm* / .jr* / .jm-p                  — moved from pdp.css
```

**Sixth component to move into core** because a page loads core plus exactly
ONE page stylesheet — `.chip` (§11b), the pdp split (§12c), `.spec-tbl`
(§22f), `.sw` (§23c), `.tbd` (§25e), now this.

The PDP calls `LG_REVIEWS.mount($('#reviews'), PD_REVIEWS)`. Verified in the
browser after the extraction that a product page behaves **identically**: the
real 551 histogram, 1★ filter returning 5 of 9 live, show-more paging 6→12,
sort-by-lowest, and none of the reviews-page-only chrome rendering.

### 26g. The reviews page, and the arithmetic that has to reconcile

Three figures, all derived, none typed:

```
884   clubs-wide on Judge.me — the homepage's number
845   across the five pulls in _src/data/reviews/ — what the filters cover
 39   on the discontinued LGD01 driver
```

`reviews_copy()` reaches 39 **two independent ways** — `clubs_wide - pulled`,
and the sum of rated clubs with no pull in the repo — and **stops the build if
they disagree**. Verified by deleting a set: *"20 reviews are unaccounted
for."* A reviews page whose headline and histogram do not add up is worse than
no page.

The 69 S-grind reviews are their own chip linked to the 01 Gold. They are
**not** summed into the 01's 551 — §23h's rule stands until the Judge.me
migration.

**Known and correct:** filtering the S-grind or LGP01 sets to a low star can
show "No reviews at that rating in this sample". Those two pulls are Judge.me's
*first page*, not distribution-preserving samples, so their samples are
top-heavy while the histogram shows the real spread. The widget says so rather
than pretending.

### 26h. Search

Client-side over the catalogue. The thing that makes it worth having is that
**variant labels are searchable**: "56" finds the wedge, "left hand" finds all
five clubs and covers built in both hands. Neither string is in a product
title. Words are AND-ed, so "left hand wedge" narrows to one.

**SKUs are deliberately NOT searchable** — no SKU renders anywhere (§22d), and
a search that matches a string it will not then show looks broken.

The query lives in `?q=`, so a result page can be linked and reloaded, which is
also what Shopify's search template reads.

### 26i. Verified

Swept at 1440 and 390, contrast composited through rgba ancestors, foil skipped
(§9).

| Page | 1440 | 390 |
|---|---|---|
| Our Story | 0 fails, no overflow | 0 fails, `scrollWidth` 390 |
| The Trybe | 0 fails | 0 fails, roster is the `.msnap` rail |
| Reviews | 0 fails | 0 fails |
| Search | 0 fails | 0 fails, incl. the empty state |
| 404 | 0 fails | 0 fails |
| Putters collection (edited ledes) | 0 fails | — |

Driven through the DOM: the reviews product filter swapping the histogram to
that club's real distribution, the star filter inside a product, the empty
state, paging and sort across the union; six search queries including a
two-word narrowing and a no-match; the roster rail; and field order on both
brand pages (no two dark bands adjacent, brand field once, cream before the
ink footer).

Build guards verified by breaking each one: a real roster name with no
`consent` key, an image slot with no brief, a review set that stops the
figures reconciling, `page-reviews.js` emptied, and `reviews.js` dropped from
the bundle (fails the club pages too).

`--check` reports all 58 identical. `test-variants.js` and
`normalize-products.py --check` unchanged.

### 26j. Still Cole's

1. **Sale** — price the collection or drop it from the nav. The only thing
   between the site and 61 of 61.
2. **The Shopify wedge draft** — move stock onto the six S variants and publish
   (§25a, §25b).
3. **Photography** — every image on Our Story, The Trybe and the collection
   pages is a labelled brief.
4. **The Trybe roster** — five names, five handles, five 4:5 portraits, and the
   program terms.
5. **Four unanswered policy questions**, all chipped on the pages: warranty
   period and who pays return shipping on a defective club; warehouse
   locations and duties; staffed hours and a response target; the Returns
   Portal URL.
6. **The homepage review quotes naming competitors** (§26d).
7. **Update the copy skill to How We Write v7.3** and add the two new guides.
8. **A register pass** against v7.3's "range" section (§26e).

---

## 27. The developer handoff document (2026-08-13)

### 27a. `DEVELOPER-HANDOFF.md` — Round 4 is closed

The last unblocked build task. It existed only as a table inside `NEXT-PAGES.md`
§9; it is its own document now, because it is what ships with the repo.

Fourteen sections: how to run the build, the repo map, the pipeline diagram and
what happens to each half of it in a theme, the page→template map, what each
template is made of, a Mustache→Liquid conversion table, the editorial layer,
the catalogue traps, the design laws, the build guards, what is temporary, what
is still open, a port checklist, and where to read further.

### 27b. The part that is not in §9's brief, and is the most useful thing in it

**Liquid has no merge.** The three-layer editorial contract —
`_shared-<template>.json` under `_family-<family>.json` under `<product>.json`,
shallow and total — is the single hardest thing in this build to reproduce in a
theme, and nothing in NEXT-PAGES §9 mentioned it.

The doc names the mapping (product metafields → `lucky_family` metaobject →
`lucky_template` metaobject) and writes the fallback chain out in Liquid, because
a developer who does not know the layers exist will discover them the way we did:
by finding the same size chart typed into two family files.

### 27c. Two rules that turned out to apply to Liquid as well

- **The scope stack walks outward, and so does Liquid.** `{{ lede }}` inside a
  `{% for %}` resolves to the outer assign exactly as our engine does, so the
  duplicated-headline bug on the refund policy is reproducible in a theme. The
  doc says: reference loop variables explicitly, `{{ sec.lede }}`, never
  `{{ lede }}`.
- **`availableForSale` is `variant.available`, never `variant.inventory_quantity`.**
  The checklist tells the porter to grep for `inventory_quantity` and justify
  every hit.

### 27d. Three counts corrected against the data rather than the prose

NEXT-PAGES §9 and earlier HANDOFF sections carried figures from before the wedge
merge. Recomputed from `products.json` for the doc:

```
club     5 built     (7 records — lgd01 and lgp02-patriot are discontinued)
apparel  23 built
gear     13 built    (§9's brief said 12)
         41 product pages, of 58 built, of 61 declared
```

### 27e. One nuance §9's "no SKU renders anywhere" needed

It is true of every merchandising surface — PDP, tile, buy box, cross-sell rail
— and search deliberately does not match SKUs either. **They do render in the
cart line item and the lightbox buy block**, which is where Shopify's own cart
shows a variant title anyway. Stated that way in the doc rather than as an
absolute a developer would find a counter-example to in five minutes.

### 27f. Verified

`normalize-products.py --check` identical · `build.py --check` **all 58
identical** · `test-variants.js` all invariants hold · `build.py --links` 61
pages, 58 built, 3 declared. No source file changed — this pass is documentation
only.

### 27g. Still Cole's

Unchanged from §26j and `FINISH-LINE.md`. The site side of the checklist now has
one fewer box: the handoff document is written. Everything else on the build
side is blocked on an answer, a photograph or the Shopify merge.

---

## 28. Sale is gone (2026-08-13)

### 28a. Cole: "that was a long time ago"

The `sale` entry is deleted from `COLLECTIONS` in `normalize-products.py`. It had
been the site's only `blocked` collection since Phase B.

Re-verified against the live store before removing it, because the record was
twelve days old:

```
Summer Warehouse Sale (gid://shopify/Collection/486822183189) — 9 members
  6 grip products   ACTIVE    compareAtPrice null or "0.00" on EVERY variant
  3 clover hats     ARCHIVED  sold out, no compare-at
  grip-putter-green ACTIVE    all four variants dead — sold out entirely
```

Nothing changed since §26a. Still not one real was-price anywhere in it.

### 28b. The brief was wrong, and the correction is the useful part

`FINISH-LINE.md` §1a and NEXT-PAGES §8 both said "drop Sale from the nav."
**There was no nav entry.** Zero `{{link:c/sale}}` tokens anywhere in `_src/`,
and `build.py` reported zero links to unbuilt pages — so Sale was a *declared
slug nobody could reach*, not a collection the header was advertising.

That changes what the decision was worth. It was never "the 59th page against a
cleaner nav". It was "do you want a sale section at all", and building one would
have needed compare-at prices **and** a new nav or footer entry, because the page
would have been unreachable the moment it existed.

### 28c. Removing it changes no page's output

`collection_siblings()` already skipped `blocked` collections, so Sale was never
in a sibling row either. **All 58 pages rebuild byte-identical.** The only
observable change is the registry:

```
before   61 pages, 58 built, 3 declared
after    60 pages, 58 built, 2 declared   (the two discontinued products)
```

### 28d. What was kept, and why

- **The `blocked` mechanism stays.** It is how a collection gets a routed slug
  and an explained absence instead of a dangling link, and the next collection
  that is real in Shopify but not ready here will want it.
- **The `members` code path stays**, now documented as unused. It is the general
  facility for a curated rather than family-derived collection.
- **The Shopify collection is untouched.** Removing a slug from our overlay is
  not the same action as deleting a merchandising object in a live store, and
  the second one was not asked for.
- A comment block where the entry was records how to bring Sale back: re-add the
  dict, set genuine compare-at prices, **and add a nav or footer entry.**

### 28e. Verified

`normalize-products.py` 43 products / 155 variants, unchanged · `build.py
--check` **all 58 identical** · `test-variants.js` all invariants hold ·
`--links` 60 pages, 58 built, 2 declared · no `sale` string left in
`products.json`, `_src/` or any built page.

---

## 29. Footer tap targets (2026-08-13)

### 29a. The standing note was half wrong

HANDOFF §25h and `FINISH-LINE.md` both carried "every footer link is a 16px hit
area on all 58 pages". Measured on a built page with the fonts actually loaded:

```
390   44 x 350     already correct — the <=620px rule has done this since Phase 1
1440  16 x 98.7    the real gap, and it is POINTER-only
```

So it was never a tap-target problem. It was a **pointer**-target problem, and
the note had been repeated forward without anyone re-measuring it.

### 29b. What was actually wrong — inline anchors have no vertical hit area

`.ftr ul a` had no `display`, so it was inline: **its hit area is the inline
box, not the line box.** The `<li>` rows were ~27px of line-height with a 9px
grid gap — about 36px of visual pitch — but only 16px of each row was
clickable. Roughly **11px of dead space between every pair of links**, which is
invisible and which no contrast or overflow sweep can see.

16px boxes at a 25px centre-to-centre pitch technically clear WCAG 2.2 SC 2.5.8
through its *spacing* exception, by one pixel. Passing on a technicality is not
the same as being usable.

### 29c. The fix moves the gap INSIDE the target

```css
.ftr ul   { gap:9px -> 1px }
.ftr ul a { + display:flex; align-items:center; min-height:24px }
```

| | before | after |
|---|---|---|
| hit area | 16 &times; 98.7 | **24 &times; 205.7** |
| row pitch | ~36px, 11px of it dead | 25px, all live |
| footer height | 436.2 | **394.7** |

The footer is **41.5px shorter** and every row is fully clickable. The `<=620px`
rule still wins on a phone, so 44px is untouched there.

**The visible consequence, and the reason this needed a decision:** the link
lists are a 25px pitch now instead of ~36px, so the footer columns read tighter.
That is the trade — density for a target that matches what the eye already
thought it was aiming at.

### 29d. Two measurement traps worth keeping

- **Await `document.fonts.ready` before measuring anything.** The first pass
  read the footer at 436.2px pre-font-load and the `.tag` paragraph was wrapping
  to a different number of lines. Every derived comparison would have been
  wrong.
- **Get before/after from the same DOM.** The honest comparison came from
  injecting the OLD rule back into the live page with `!important`, measuring,
  then removing it — not from comparing against a number captured earlier under
  different conditions.

### 29e. Verified

Measured at 1440 and 390 on `01-home.html`, fonts loaded. No two link boxes
overlap in any column, colour is unchanged (`--cream-70`), `display:flex`
confirmed computed, page `scrollWidth` 390 at a 390 viewport.

`normalize-products.py --check` identical · `build.py --check` **all 58
identical** after rebuild · `test-variants.js` all invariants hold · `--links`
60 pages, 58 built, 2 declared.

**All 58 pages changed on disk** — it is core.css, so every page carries it.

---

## 30. The support cluster reaches zero chips (2026-08-13)

Cole answered every open policy question. **All four support pages now carry no
`.tbd` chips at all** — the first time since they were built.

### 30a. Duties: not "collected on delivery", but off the site entirely

> Cole: *"there's no duties, this can just be completely ignored because we ship
> from within the United States… it doesn't even need to be brought up."*

So this was a **deletion**, not an answer. `duties` appeared in five places and
is now in none: `41-shipping.html#where`, the FAQ's `international` answer, and
the delivery modal on **all 40 product pages** (`page-club.html`,
`page-apparel.html` — `page-gear.html` never had it).

**Flagged to Cole and overruled, which is the correct outcome but worth
recording:** shipping *from* the US does not stop a destination country charging
the customer import duty on delivery. The site is now silent on that. His call,
made with the consequence stated.

### 30b. The response target, phrased as an aim

> Cole: *"we try to reply to emails within 24 business hours."*

The copy says **"We aim to answer email within 24 business hours"** — "aim",
because he said "try to", and the Friday-evening case is spelled out the same
way the dispatch section does it. §25f's argument against a committed number is
satisfied: this is a number he has actually committed to.

**Chat has no separate hours.** Same hours as email, Monday to Friday, same
team — so the chat chip became a sentence in the channel body rather than a
second staffed-hours claim.

### 30c. The Returns Portal, and the rule attached to it

```
https://lucky-golf.loopreturns.com/
```

**It is NOT a general "start a return" link, and must never become one.**

> Cole: *"for clubs people are supposed to reach out to support… we need to make
> sure that there's nothing wrong with it before they send it. For apparel they
> can use that return portal 100%."*

So the link is on the **apparel and gear route only**, in exactly two places —
the refund policy's `start` section and Contact's `where` row. Verified: it
appears on no club page anywhere on the site. Both pages carry a note saying why
clubs are the exception, because a reader who sees a portal link and a "contact
support" instruction on the same page will otherwise assume the second is
optional.

**This is the first external link on the entire site**, which is what exposed
§30e.

### 30d. The warranty question, answered as a "depends"

> Cole: *"they have 60 days to try it out, that's our return policy… that may
> change in the future, right now it's 60 days."*

The FAQ's `broken` answer now says there is no lifetime warranty, that sixty
days is the whole of the written policy, and that a fault found afterwards
**depends on what the fault is** — send photos and we will answer, rather than
guess at it on the page. A stated "depends" beats a chip.

**Also fixed here: the chip was stale and contradicting our own refund policy.**
It read "needs confirming: the warranty period on a club, *and who pays return
shipping when the fault is ours*" — but that second half was answered 2026-08-02
and `40-returns.html#defective` already stated it plainly. The FAQ had been
saying "unconfirmed" about something the policy page asserted.

### 30e. EVERY inline prose link on the site was invisible as a link

Adding the portal link surfaced a defect that had shipped with the support
cluster. Measured on `40-returns.html`:

```
link colour    rgba(23,20,15,.70)      <- --ink-70
parent colour  rgba(23,20,15,.70)      <- identical
text-decoration none
```

An `<a>` in body prose inherited the paragraph's colour and carried no
underline. **Colour alone would need 3:1 against the surrounding text plus a
non-colour cue; there was neither.** Every `mailto:support@luckygolf.com` on the
four support pages, and `partners@luckygolf.com` on the Ambassador page, had
been unmarked prose since they were written.

Fixed with an underline — the non-colour cue, it survives the cream and white
fields both, and it avoids adding a second link colour to the palette. The
**gold is the decoration, not the text**, so it carries no contrast obligation
of its own and the text stays `--ink-70`. `.btn` is excluded; a button already
reads as a control.

**The rule is duplicated in `page-support.css` and `page-brand.css` rather than
promoted to core.** Those are the only two stylesheets whose pages carry inline
prose links, and a page loads core plus exactly ONE page stylesheet — promoting
it would have put the rule on 58 pages to serve six. This is the first time that
trade has gone the *other* way from §11b / §12c / §22f / §23c / §25e / §26f.

### 30f. Verified

Swept at 1440 and 390 with `document.fonts.ready` awaited, contrast composited
through rgba ancestors, FAQ accordions forced open.

| | 1440 | 390 |
|---|---|---|
| Refund policy | 0 contrast fails, `scrollWidth` 1425 | 0 fails, `scrollWidth` 390 |
| Portal link | underlined, 1.5px, `--gold` decoration | underlined |

Driven through the DOM: the portal link's computed decoration on returns and
contact, every inline link's parent-colour comparison before and after, and a
grep proving `loopreturns` appears on exactly two pages and no club page.

`normalize-products.py --check` identical · `build.py --check` all 58 identical ·
`test-variants.js` all invariants hold · `--links` 60 pages, 58 built, zero dead
links · **`Needs confirming` count across the four support pages: 7 → 0.**

### 30g. Still Cole's, from this pass

1. **Retire the Shopify FAQ page.** He confirmed it is wrong — no lifetime
   warranty, 60 days on clubs. It still contradicts the site.
2. **The Ambassador roster is being restructured** — see §31 when it lands. He
   does not want five named people; the program is open to anyone meeting the
   criteria, and the criteria and terms are not yet supplied.
3. **Photography**, to be issued as its own brief.

---

## 31. The roster comes off, and the program gets its terms (2026-08-13)

### 31a. Cole's ruling, and the model behind it

The five-slot roster was §3's borrow from Takomo's homepage — and it was
borrowed wrong. Takomo's roster shows **signed influencers** (their ambassador
page gatekeeps at 5k Instagram / 10k TikTok / 1k YouTube); Lucky's program is an
**open door**. Same visual, opposite meaning. Cole, 2026-08-13: anyone meeting
the criteria can be an ambassador; names appear only when there are big, real
ones — a future "Lucky Golf Athletes" idea that stays unannounced (the 02 rule).

Three decisions via question card, plus the analysis he asked for:

1. **The club give stays deliberately unspecified on the page** — "clubs to
   play, details with your acceptance." The specifics travel in the acceptance
   email the way the returns portal travels in the order confirmation. DO NOT
   "fix" the vagueness by inventing a number.
2. **The 10%/AvantLink affiliate block is OFF the page.** He does not want
   commission advertised on the site; the commission test continues on the
   Trybe platform, off-site. (His Grunk Dolfer creator brief — 12% on subtotal,
   free seeding, Partnership Ads — is the in-house model for a future APPAREL
   track, which stays off the page until its terms exist.)
3. **The group chat is real and advertised** — Takomo lists theirs as a
   headline perk, and it is the retention mechanism.

**No commission on clubs is positioning, not thrift.** The homepage sells "no
sponsorships and the middlemen in the price"; a commissioned advocate on the
hero category is a walking counterexample. The test that survives this session:
*if the incentive would embarrass the price story, it does not attach to clubs.*
Apparel carries no price story, so commission there passes the same test.

### 31b. What changed on the two pages

`_brand-trybe.json`: `roster` deleted; the affiliate row became **"What you
get, and what we ask"** (the gives are all Cole's: clubs, group chat, drops and
events, reposts — and "nobody is paid per sale" as brand proof); the stats item
"Small / Five slots" (now false) became **"Unpaid"**; the paid-creator ladder is
one sentence, **earned-not-promised**; the steps' terms chip is gone because the
terms are now on the page. The stale contradiction between "applications open a
few times a year" (stats) and "no application window" (close) is resolved to
"write any time — read in batches", which is what Cole described.

`page-home.html`: the five-card grid is gone; the section is an invitation band
— same `.roster` cream field, same `#trybe` id, because the §7 field order and
the UGC rail's "Join the program" button both depend on the section existing.
Dead `.rost-*` rules removed from `page-home.css`.

`page-brand.html`: the roster block is **dormant, not deleted** — its comment
now says why, and `brand_copy()`'s consent guard still stands for the day real
names exist.

### 31c. A "Trybe" leak the 2026-08-02 sweep missed

`core.js`'s lightbox rendered **"Trybe creator"** as a visible label on UGC
panes — on the homepage, the Ambassador page, and every page with a reel rail.
The 08-02 rule ("the word Trybe comes off the site") was applied to markup and
copy but nobody grepped the JS. Now "Lucky ambassador". The only "Trybe"
strings left in any built page are HTML comments.

### 31d. Verified

Swept at 1440 and 390 with fonts awaited (and re-measured after the
`viewport: 0` trap hit again on a fresh tab — resize EVERY new tab before
trusting a number).

| | 1440 | 390 |
|---|---|---|
| Ambassador page | 0 contrast fails, field order white→INK→cream→white→cream→BRAND→cream, no two darks adjacent | `scrollWidth` 390, partners@ link underlined, 3 steps, 0 chips |
| Homepage #trybe | 0 fails in section, cream between INK and white, 0 roster cards | `scrollWidth` 390, CTA 170×44 |

`--check` all 58 identical after rebuild · `test-variants.js` holds ·
`--links` 60 pages, 58 built · zero `.tbd` chips on the Ambassador page.

### 31e. The shot list shrinks

**26 stills → 22.** The five roster headshots left with the roster; the program
page gained one lifestyle brief (the filming-at-the-range shot moved from the
old affiliate row to the new gives row). `SHOT-LIST.md` and `FINISH-LINE.md`
both updated. Video count unchanged at 36.

### 31f. Still open

The named-roster block waits dormant. The apparel commission track exists only
as the Grunk model plus Cole's intent — off every page until terms exist. The
photography brief for the 22 remaining stills is the next deliverable.

---

## 32. The Ambassador page goes Dartee-shaped (2026-08-13)

### 32a. Cole: follow Dartee's layout, not Takomo's

He sent Dartee's ambassador page as a screenshot: *"I like their layout because
it's so easy to grasp."* He is right about why — **Takomo's page is a pitch you
read; Dartee's is a decision you make.** Their fork ("Which one fits you?", two
cards, first screen) makes every visitor self-sort, and everything below is
sequenced by that choice.

Two things on Dartee's page deliberately did NOT carry over:

- **Their hero leads with commission** ("your own discount code and
  commission", "Earn on Every Sale") — the exact thing §31a took off this page.
- **Their four-tier ladder and stats band** ("300+ crew", "$20K+ paid") run on
  defined tier rewards and real numbers. Lucky has neither; inventing either is
  the roster problem in a different costume.

### 32b. The fork is ONE door, and that was a recommendation Cole asked for

Via question card: inline form YES, two-stage ladder YES, and on the fork he
asked for my thoughts. Recommended and built: **one door with a fast lane** —
Ambassador is open, Creator is by invite, and the application's optional
"links to anything you've made" field is the fast lane ("sometimes on day
one"). Three reasons, recorded so the next session doesn't relitigate:

1. A direct creator door needs a defined offer (store credit? per-project
   rate?) and Cole has not defined one — two doors today means inventing the
   second.
2. Zero members, one review queue. Two application tracks is segmentation
   before there is anything to segment.
3. The links field produces the same outcome as Dartee's creator door without
   a public offer to honour: a strong creator is visible at application time
   and the invite conversation starts immediately.

**If Cole later defines a direct creator deal** (the Grunk Dolfer brief is the
in-house template), card two gains a CTA and the form a branch — one swap.

### 32c. What was built

New template blocks in `page-brand.html`, both gated so Our Story is untouched:

- **`fork`** — two cards: cream Ambassador card (the §31 gives, "No commission.
  No quota. No script.", CTA ↓ to the form) and ink Creator card ("Earned, not
  promised."). The colour contrast IS the information — open vs invited. On the
  ink card the clover bullets flip to `--gold-hi`: green on ink measures ~3.4:1,
  which passes non-text but reads as off (§7's green-on-green lesson, again).
- **`apply`** — the inline application, id `#apply`: name, email, optional
  handle, "how do you play", optional links. Same contract as the contact form
  (§25g): prototype chip ABOVE the fields, submit intercepted, and the
  interception repeats the notice — nobody is thanked for a message that never
  sent. `.br-opt` is `--ink-muted`, never `--ink-38` (§25h's 2.44:1 bug).
- **`steps` reused as the ladder** — no new block. Two numbered stages,
  Ambassador → Creator, in the existing `.br-steps-list` styling.
- **`page-brand.js` is new** (the brand template had no JS until now), and
  `build.py` gained a per-page `extra` for it: `id="amb-apply"` proves the form
  rendered, `function brApplyIntercept` proves the bundle carries the
  interception. Marker verified unique to one source file (§21i).

The gives row died into the fork card; the criteria row ("Golfers, not
audiences") stays as the page's one photo moment, now on white. The close
(`br-fit`) CTA is "Apply now" → `#apply`, and the homepage UGC rail's "Join
the program" deep-links there too — `{{link:trybe#apply}}` resolves through
the registry like everything else.

### 32d. Field order, re-derived

```
white hd → white fork → INK stats → white row → cream ladder → BRAND fit
→ white apply → cream more → INK footer
```

No two dark bands adjacent, brand field once, cream above the footer. The
fork's ink CARD sits inside a white section with padding, so it does not count
as a band and cannot touch the stats band.

### 32e. Verified

1440 and 390, fonts awaited: **0 contrast fails both widths** (the ink card's
badge, bullets and foot included), `scrollWidth` 390 at 390, cards stack
full-width on a phone, inputs 54px, submit 202×55. Driven through the DOM: a
valid submit does NOT navigate and DOES reveal the repeated prototype notice;
`#apply` anchors resolve from the fork card, the close and the homepage.
`--check` all 58 identical after rebuild · `test-variants.js` holds ·
`--links` 60 pages, 58 built, zero dead.

### 32f. The shot list, again

**22 → 21 stills.** The second lifestyle brief (golfer filming at the range)
left with the gives row. The Ambassador page now carries exactly one photo
brief. Video unchanged at 36.

### 32g. Dormant, unchanged

The roster block (§31b) and the apparel-commission track (§31a) both stay off
the page and wait on real terms. The tier ladder can go Dartee-four-wide the
day Cole defines tier rewards — the two-stage version is the honest subset of
it today.

---

## 33. The bar, and the flow (2026-08-13)

Cole, on the Dartee-shaped page: *"add the restrictions like Takomo does to
make it more inclusive"*, and *"is there any way we can make the page flow more
and if people have questions on what they do it's easier to read like
Dartee's?"* Two blocks answer the two halves.

### 33a. The bar — Takomo's device, inverted

Takomo's ambassador page gates on numbers: 5,000 Instagram, 10,000 TikTok,
1,000 YouTube. **The value of that is not the gate, it is the certainty** — you
know before applying whether you fit. That is what Cole wants and it is not in
tension with "inclusive", because the certainty and the threshold are separable.

So `bar` states the bar just as plainly, and the bar is quality-shaped:

```
This is for you if   →  play regularly, merit first, say what's wrong, happy to
                        be tagged, talk golf to people who listen
What we don't ask    →  NO follower count on any platform, no schedule, no
                        script, no exclusivity, no professional gear
What isn't a fit     →  wall-to-wall promo-code feeds, wanting a script or
                        post approval, under 18, free-club hunters
```

**Three columns, not two, and that is the design.** The middle column is the
loudest thing in the section, so the restriction lands beside an explicit list
of what is *not* being asked rather than standing alone. The third column is
marked with a gold top rule and darker heading, but **no red, no cross, no
warning colour** — its bullets keep the clover and run `--ink-muted`. An
explicit bar that looks like a bouncer is the failure mode here.

**⚠️ THE THIRD COLUMN IS DRAFTED, NOT CONFIRMED.** The promo-code exclusion,
the no-script line, **under 18**, and the free-club-hunter line are my drafting
from Cole's stated intent — not quoted terms. The age minimum is real policy
with real consequences. `_signoff` says so and Cole was told directly. The
first two columns are safe: they restate criteria that have been on the page
since it was built.

### 33b. The flow — Dartee's "application to athlete"

`steps` was three abstract stages. It is now **five concrete ones** answering
the question Cole actually named — *what do I do, and what happens next*:

```
1 You apply  →  2 We read it  →  3 Clubs arrive  →  4 You play, and you post
             →  5 Some of you get paid
```

Step 5 is the §32b ladder, kept earned-not-promised. Step 2 promises an answer
but no timeframe, which is the §25f rule about response targets.

### 33c. `.br-steps-list` had to become a timeline

It was `grid-template-columns:repeat(3,1fr)` — it held exactly three steps and
would have gone 3+2 ragged at five. Now the number sits **on top** of its step
with a 2px connector running behind the row, so a sequence reads as a sequence.

**The connector is drawn on the LIST, not per-item**, and clipped to badge
centres — a `::before` on each `li` prints a tail after step five. Getting the
right edge right needed real arithmetic rather than a guess:

```
first centre   19px            (half a 38px badge)
last centre    one column-width minus 19px from the right
column width   (100% - 4 * var(--gut)) / 5
→ right: calc((100% - 4 * var(--gut)) / 5 - 19px)
```

A first attempt used `right:calc(10% + 19px)` and **measured 0px off on the
left and overshot on the right**; the fix measures **0.0px off at both ends**.
A percentage is not a column width when there are gaps.

Under 820px it flips to a **vertical rail** — the connector becomes a left
spine and the number sits beside its step again. Measured: all five badge
centres and the rail land on x=39.

### 33d. Field order, re-derived again

```
white hd → white fork → cream BAR → INK stats → white row → cream ladder
→ BRAND fit → white apply → cream more → INK footer
```

The bar slots between the fork and the stats, so cream separates the white fork
from the ink band. No two darks adjacent, brand field once, cream above the
footer.

### 33e. The duplicate that had to go

The criteria row's three-item list said the same things as the bar's first
column. The row keeps its prose and its photo brief and **lost the list** —
otherwise the page makes the same argument twice within two screens, which is
the §7 "why / value props" mistake in miniature.

### 33f. Verified

1440 and 390, fonts awaited.

| | 1440 | 390 |
|---|---|---|
| Contrast | 0 fails (bar, fork ink card, timeline, form) | 0 fails |
| Timeline | 5 across, connector 0.0px off both badge centres, behind badges | 5 stacked, rail at x=39 aligned to every badge |
| Bar | 3 columns | stacked full-width |
| Overflow | `scrollWidth` 1425 | `scrollWidth` 390 |

**Build guard verified by breaking it:** emptying `page-brand.js` fails the
brand pages on `function brApplyIntercept` and lets the other 56 build — the
per-PAGE `extra` from §22h. Note `page-brand.js` is a NEW untracked file, so
`git checkout` cannot restore it after that test; rewrite it from HANDOFF or
retype it.

`--check` all 58 identical · `test-variants.js` holds · `--links` 60 pages,
58 built, zero dead links.

---

## 34. The money split, and the follower question settled (2026-08-13)

### 34a. Apparel pays, clubs never will

Cole approved apparel commission ON the page, **Dartee-shaped**: *"just say
commission and then you can increase as you go"*, *"just say monthly payout,
don't put whatever the date is"*, *"all of the contractual detail doesn't need
to be on the page... they can learn more after they're accepted."*

New `earn` section, two columns, and the second is the load-bearing one:

```
Apparel — you earn     your own code · commission on what it sells ·
                       rate grows as you do · paid monthly
Clubs — you don't      no code, no commission, no cut, at any level
                       "the one thing on this page we will not change"
```

**NO figures anywhere: no percentage, no cookie window, no payout date, no
network name.** Verified by stripping comments, CSS and JS from the built page
and scanning visible text — "commission" appears six times and is never
quantified. (Those numbers *are* public on the store's own Affiliate
Application page — 10% / 60-day / AvantLink, §33's `_rules` — this page simply
does not repeat them.)

### 34b. "Nobody is paid per sale" became false and had to be rewritten in four places

The blanket claim was true only while nothing paid commission. Apparel paying
made it a lie the moment the `earn` section landed. Every instance is now
**club-specific**:

| | was | now |
|---|---|---|
| lede | "nobody paid per sale" | "nobody ever paid to praise a club" |
| stat | "Unpaid — nobody is paid per sale" | "Unbought — clubs are never commissioned" |
| fork foot | "No commission. No quota. No script." | "No quota. No script. No commission on clubs, ever." |
| fork note | "nobody at either level is paid per sale" | "apparel pays commission and clubs never will, and that split is the whole point" |

**This is the trap to watch on this page.** Adding an earning mechanism
anywhere silently falsifies a global claim made somewhere else. Grep for
"commission", "paid" and "per sale" before touching it.

### 34c. The follower bar — option C, and Cole's reasoning is the good one

I recommended no published minimum; Cole picked **C**, which is stronger than
either extreme, and his stated reason is why: *"I can always transfer back to
like a specific follower account or remove it all entirely in the future."* It
moves in both directions without a rewrite.

```
Joining          open. No threshold on any platform.
Club seeding     limited and competitive. The application decides it.
Everything else  code, commission, chat, drops, reposts — everyone accepted.
```

Takomo publishes 5k IG / 10k TikTok / 1k YT **with an exceptions clause**, so
even their gate is soft. Mirroring it was rejected because a status gate
contradicts the homepage's own no-status-tax argument, and because a published
number has to be enforced against the 900-follower club pro who would be the
best ambassador on the roster.

**The honesty gain matters more than the flexibility.** The previous copy
implied every accepted ambassador got a club, which was never going to be true
at $99–229 a unit. The guaranteed set and the competitive one are now separated
in three places: the fork card (four guarantees, then "a shot at a club to play
— those go out in batches, and there are never enough"), the ladder (**step 3
"You're in"** vs **step 4 "Clubs, when there are clubs"**), and both notes.

### 34d. Two earlier drafts Cole cut

- **The age minimum is gone.** *"The age doesn't matter, so don't add an age
  thing unless Takomo does it"* — they don't.
- **The promo-code bullet was reworded.** It read as though it were about Lucky
  promo codes, which do not exist for clubs. It filters applicants whose *own
  feeds* are wall-to-wall ads, and now says exactly that.

### 34e. Verified

| | 1440 | 390 |
|---|---|---|
| Contrast | 0 fails (fork ink card, bar, earn, timeline, form) | 0 fails |
| Timeline | 5 across, connector 0.0px off both badge centres | 5 stacked, rail x=39 on every badge |
| earn / bar | 2 and 3 columns | both stacked full-width |
| Overflow | `scrollWidth` 1425 | `scrollWidth` 390 |

`--check` all 58 identical · `test-variants.js` holds · `--links` 60 pages, 58
built, zero dead links · no commission figure in visible copy.
