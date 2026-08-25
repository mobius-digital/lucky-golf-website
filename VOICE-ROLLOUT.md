# VOICE ROLLOUT — the plan for the next chat

Written 2026-08-25, at the end of the session where Our Story finally landed.
Cole: *"Now this is good. You finally found a voice, personality, etc. That is
consistent across this entire page. How can we use this on every other page."*

**Read first, in this order:**

1. `references-how-we-write-v8.1.md` → the section **"The approved model"**.
   That is the whole brief. It quotes the approved lines verbatim.
2. `_src/data/copy/_brand-story.json` → the finished page. Every `_`-prefixed
   key in it is a ruling from this session, including `_register`, `_name`,
   `_layout` and `_timeline_src`.
3. This file.

**The finished page:** `30-story.html`. Start the dev server and read it before
writing anything.

---

## What actually changed, and why it worked

The failure was never craft. It was **`references-how-we-write` v7.1–7.3**,
which banned "us-vs-them defiance" and named "new dress code" as a non-Lucky
line. Every draft got filtered through that paragraph, and what survives a
"no fight" filter is a flat double-statement. Cole's words: *"I hate whenever
we say a statement and then we say another statement after that."*

v8.0 reversed it. Lucky is allowed to swing at golf's stuffiness and its
prices, on one condition: **every swagger line lands on a receipt** — a real
product, a real price, a thing that happened. Attitude with receipts is Lucky.
Attitude floating free is noise.

**The two legs, and nothing else:**

1. You're not overpaying. Same materials as the big names, minus tour
   contracts and retail markup, sold direct.
2. You're not blending in. Gold, on purpose. Golf got too serious; we didn't.

Takomo's thesis is **access**. Ours is **fun + fair**. If a line could sit on
Takomo's site unchanged, it is wrong for us.

---

## Job 1 — the re-pass, in this order

69 copy files. Do them in dependency order so shared files land before the
pages that inherit from them.

| # | Group | Files | Notes |
|---|---|---|---|
| 1 | Shared | `_shared-brand`, `_shared-apparel`, `_shared-support` | 3 files. Every page inherits these, so a wrong line here repeats site-wide. |
| 2 | Home | `_page-home` | The highest-traffic page and the one that sets the register. Manifesto block belongs here too. |
| 3 | Collections | `_collection-clubs / -wedges / -putters / -hybrid` | 4 files. Ledes and closers. |
| 4 | Families | `_family-wedge / -putter / -hybrid / -driver / -polo-* / -hat / -grip / -glove / -headcover / -tee` | 11 files. These carry the copy every product page inherits — biggest leverage per edit. |
| 5 | Products | 43 files | Mostly inherit from families. Only override where the product has its own argument. |
| 6 | Brand | `_brand-trybe` | Story is done. Trybe still reads in the old register. |
| 7 | Support | `_support-returns / -shipping / -contact / -faq` | Lightest touch. These must stay clear before they are clever. |
| 8 | Reviews | `_page-reviews` | Light. |

**Per file, the loop:**

1. Read it.
2. Rewrite against "The approved model" in v8.1.
3. `python tools/build.py` then `python tools/build.py --check` (58 identical).
4. Run the sweep below.
5. Show Cole the built page link. He reacts; do not present options.

**The sweep** (run AFTER writing, not before — a banned word was reintroduced
in July because it was only run before):

```bash
python tools/build.py && python tools/build.py --check
```

Then grep the built page's *visible* copy (strip `<style>`, `<script>` and
comments first, or the inlined stylesheet's own prose produces false hits) for:
`premium`, `cheap`, `luxury`, `revolutionary`, the founder's name, em dashes,
`this page`, `everything above`, and any order/review count.

**Guards that must stay green:** `build.py --check` (58 identical),
`build.py --links` (0 dangling), `node tools/test-variants.js`,
`normalize-products.py --check`.

---

## Job 2 — the comparison page

Takomo's "What we do" popup contains an underlined phrase, **"No crazy retail
prices"**, which links to a standalone page comparing Takomo against the big
brands. Cole: *"I think that's wonderful... that's where detail comes in and
it's so clean."*

**Build the Lucky version.**

### Wiring

The link lives in the What We Do popup, on the phrase about markup, in
`_src/data/copy/_brand-story.json` → `trio.cards[1].paras`. That paragraph
currently reads:

> "We cut out the middlemen, the retail markup and the hype. No crazy retail
> prices. No buzzword-fueled launches. Just top-shelf gear, delivered straight
> to you."

Wrap **"No crazy retail prices"** in a link to the new page. Note that
`.br-dlg-p a` is already styled (gold underline) in `_src/page-brand.css`.

### The page itself

- **New slug** in `tools/sitemap.py`, new template or a `page-compare.html`.
  Check how `sitemap.PAGES` declares pages before inventing a pattern.
- **`{{link:...}}` token required** — `build.py` exits on a literal `href="#"`.
- Register it in `REQUIRED` in `tools/build.py` with a smoke marker.

### What goes on it

The argument, not a spec war:

1. **The price of a big-name club, broken into parts.** What you actually pay
   for: the club, the tour contract, the shelf space, the middleman.
2. **The same breakdown for Lucky.** The club. That's the row that's short.
3. **What's identical** — materials, engineering, the fact that neither is
   made in a magic factory.
4. **What's different** — how it reaches you.
5. **The 60-day test drive** as the closer: you don't have to believe any of
   this, just try it.

**Do NOT:**
- Name a competitor brand. Say "the big names".
- Invent a price, a percentage, or a multiplier. Cole killed "charge triple"
  earlier for exactly this. If a number is needed, ask him first.
- Fabricate a table row you cannot defend.

---

## Open asks for Cole

- **Exact months** for the timeline. He gave years and said *"I can get you
  exact months later."* Currently: 2018 gold wedge, 2019 blade putter, 2020 v2
  wedges, 2023 mallet, 2024 hybrid, May 2026 polos, July 2026 hats + Patriot
  Putter, Sept 2026 accessories, late 2026 KBS shafts + irons/drivers, 2027
  partnerships.
- **Team size.** Asked twice, never answered. Takomo's "10 Strong" is one of
  their best timeline entries.
- **The square working photo** for the Our Story card 3 (packing an order, real
  workspace, no faces required). It is the last placeholder on that page.
- **Any press or independent test result.** Takomo's strongest paragraph is the
  MyGolfSpy award. We have no equivalent, and the 884 reviews were cut on his
  instruction. This is the one real gap in our version.
- **Prices/percentages** for the comparison page, if he wants real numbers on
  it rather than the shape of the argument.

---

## Traps that already cost time this session

- **The browser pane returns garbage unless you resize it explicitly first.**
  `resize_window` to a real size, then measure. A collapsed viewport reports
  `clientWidth: 0` and every measurement is wrong.
- **`aspect-ratio` loses to the `height` HTML attribute** unless `height:auto`
  is also set.
- **`build.py --check` compares output to output.** It says "identical" even
  when a whole JS bundle has silently vanished. That is what `REQUIRED` smoke
  markers are for; add one for anything whose absence leaves a page that looks
  right and does nothing.
- **PDFs:** the `Read` tool fails on this machine (`pdftoppm` missing). Use
  PyMuPDF (`fitz`), render at ~1.6x, slice vertically into JPEGs, then read
  those.
- **`close` is not brand-only.** The reviews template has a `close` key too;
  the Our Story smoke marker had to be scoped with `src == "brand"`.
