# Lucky Golf — site build gameplan

Phase 1 built the homepage. This is the plan for everything else.

**Read `HANDOFF.md` first** — it holds the locked decisions, the contrast law, the
copy rules and the current homepage section table. This file is the *plan*; that
file is the *law*. Don't re-litigate what's in it.

---

## 0. Two things that will save the next session hours

**1. You can read the reference PDFs. Use `tools/render-ref.py`.**
`Read` fails on them (no `pdftoppm` installed) and the pdf-viewer MCP has no
allowed directories. **PyMuPDF is installed**, which is the way in:

```bash
python tools/render-ref.py --list
python tools/render-ref.py "Takomo/Takomo PDP 1" --pages 1-3
```

PNGs land in `_ref/<slug>/` — then just `Read` them. Verified working. A previous
session burned real time concluding the references were unreadable and working
from written descriptions instead. They aren't. Look at them.

**2. Verify in the browser, not by eye.** The Browser pane can't screenshot in
this setup, but `mcp__Claude_Browser__javascript_tool` works and is better anyway.
Every page should be checked with a computed-style contrast sweep, an overflow
check, and a broken-image count before it's called done. That method caught two
shipped-broken contrast bugs and a white-on-white nav regression on the homepage.
Known false positives: `.foil` text (uses `background-clip:text`), anything on a
gradient background, and decorative SVG marks (non-text, 3:1 not 4.5:1).

---

## 1. Where the homepage stands

Done and verified: 16 sections, forest-green brand field, zero contrast failures,
no overflow. Source of truth is `_src-home-template.html` + `_src-logo-symbols.svg`.

Still open on it:

| | Item | Blocked on |
|---|---|---|
| A | **9 photos** — 3 value-props collage, 1 mindset, 1 finish, 3 collection tiles, 5 roster headshots | Photography |
| B | **No "Gear" collection exists in Shopify** — Polos and Hats are real; gear is scattered across Head Covers / Gloves / Grips / an "Accessories" collection whose handle is confusingly `most-popular`. The tile is `href="#"` | Cole |
| C | **Closing CTA is dark-on-dark against the footer** — fix is to make it the brand field. Three-line change now the field is tokenised. Check the foil headline at 3.56:1 on forest | Cole's eyes |
| D | **Roster names/handles are bracketed placeholders** | Cole |
| E | Judge.me photo requests are off — zero reviews have customer photos | Cole |

---

## 2. DONE — the CSS is split

`_src-home-template.html` is retired. Sources are in `_src/`, assembled by
`tools/build.py`. See **HANDOFF §8** for the layout and commands. The homepage
was verified content-identical after the split and re-passes the contrast sweep.

## 3. The reference set maps onto the pages

You have 13 site PDFs. They tell you what matters:

| Reference | Count | Builds |
|---|---|---|
| Takomo PDP 1/2/3, Dartee PDP 1/2 | **5** | **The PDP** — most-referenced by a distance |
| Takomo About Us, Dartee Our Story | 2 | Our Story |
| Takomo Ambassador, Dartee Ambassador | 2 | Trybe |
| Dartee Bundle Builder | 1 | Bundles (optional, see §5) |
| Dartee How it Works | 1 | Fitting / how-we-price explainer |
| Takomo + Dartee Home | 2 | Done |

Also present, not site work but useful voice reference: **17 email PDFs** and
**9 Lucky ad PNGs** in `Ads/` — those are real Lucky creative, so they're the
closest thing to an existing voice benchmark outside the copy skill.

---

## 4. Build order

Ordered by commercial value and by how much each page unlocks the next.

### Page 2 — PDP  ✅ DONE  ·  `02-pdp-lgw01.html`

Built on LGW01 Carver Gold from all five references. Full write-up in
**HANDOFF §9**: what came from Takomo vs Dartee, the section order, the verified
facts, and the five open items (spec gaps, the Judge.me AI summary, the naming
mismatch, no set discount, no lifestyle photography).

Flat pricing was **verified against the live store**, not assumed — §4's
assumption holds.

The component library it establishes for the rest of the site: gallery with
thumbs, variant chips with real out-of-stock states, buy box, pull-quote card,
accordions, tabbed spec table, review hero + histogram + card grid, cross-sell
cards. Page 3 reuses most of it.

### Page 3 — Collection / PLP  ← start here

Wedges, Putters, Hybrid, Polos, Hats, Gear. Reuses the PDP's tile and the
homepage's `.ptile`. Needs filter/sort behaviour and an empty state. Cheap once
the PDP exists.

### Page 4 — Our Story
Pure brand. The "mindset" argument on the homepage is the seed of this page — the
luck-as-a-mindset idea has more room here than it got in a two-column block.

### Page 5 — Trybe
The homepage roster already feeds it. Both references are ambassador-program
pages, so the shape is known: what it is, what you get, who's in it, how to apply.
Unblocks the roster placeholders (D above).

### Page 6 — Support cluster
Returns & 60-day policy, Shipping, Contact, FAQ. **One template, four pages.** All
four are already linked in the footer and all four currently go nowhere.

### Page 7 — Search results + 404
Small, but the header has a search icon that does nothing today.

---

## 5. Worth discussing, not assumed

- **Bundle builder.** Dartee has one and you have a reference for it. Lucky sells
  wedges in lofts — a "build your wedge set" flow is an obvious AOV play. Real
  build cost though; treat as its own project, not a page.
- **How it works / fitting.** The homepage club finder is a mini version. If it
  performs, this becomes the full page it links to.
- **Press bar.** Takomo runs one (GOLF, Golf Monthly, NCG, MyGolfSpy, bunkered,
  SI). We left it off the homepage deliberately — no real coverage, and mocking up
  publication logos would be fabricating endorsements. If Lucky has genuine press,
  it's a quick add.
- **Blog / journal.** Neither reference leans on it. Skip unless SEO asks.

---

## 6. Rebuild + verify

```bash
python -c "t=open('_src-home-template.html',encoding='utf8').read();s=open('_src-logo-symbols.svg',encoding='utf8').read();open('01-home.html','w',encoding='utf8').write(t.replace('{{SYMBOLS}}',s))"
```

`01-home.html` is generated — **never edit it directly.**
`_brand-variants.html` (12-colour switcher) and `_why-options.html` are generated
too; regenerate them whenever the template changes or they'll show stale work.

When string-replacing copy in the template, **assert every replacement**. A silent
no-op shipped old copy to review once this phase because the search string used
`&mdash;` where the file had a literal `—`.

---

## 7. Starting the next chat

Open with roughly:

> Continuing Lucky Golf. Read `GAMEPLAN.md` then `HANDOFF.md` in
> `C:\Users\wetzl\Lucky Golf\Website`. Homepage and PDP are done. Build the
> collection page. Reference PDFs render via `tools/render-ref.py`. Pages build
> with `python tools/build.py` — never edit the `NN-*.html` files directly.

Decisions to have ready:

- **LGW01 spec gaps** — bounce, grind, swing weight, playing length, grip sizes.
  Nine cells on the PDP are marked "Needs spec" (HANDOFF §9A).
- **Judge.me AI summary** — it publishes two negatives verbatim. Leave or turn
  off (HANDOFF §9B).
- **Gear collection** — still doesn't exist in Shopify; the tile is `href="#"`.
- **Closing-CTA fix** — still dark-on-dark against the footer, and it now
  appears on *two* pages rather than one. Three-line change, still needs eyes.
- **Product naming** — rename the Shopify titles to lead with Carver / Tracer /
  Stryker, so the store matches the brand guide and the site (HANDOFF §9C).
