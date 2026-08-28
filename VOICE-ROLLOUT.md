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

---

## PROGRESS — session 2, 2026-08-25

**Done: groups 1, 2, 3, 4, 6, 8, and the light half of 7.**

First, a repair: **"The approved model" did not exist.** v8.1's changelog
announced it, but the section itself was never written into the body. It has
now been reconstructed from `_brand-story.json`'s `_register`, `_name` and
`_timeline_src` rulings plus this file, and inserted above "The bar". It
quotes seven approved lines verbatim and states the two legs, the
flat-double-statement failure mode, and five hard rules. Check it reads right
before the rest of the re-pass leans on it.

| Group | State | What changed |
|---|---|---|
| 1 Shared | done | `_shared-brand`: all four nav hooks rewritten; **`moreAside` cut** (see below). `_shared-apparel`: grammar only. `_shared-support`: **no change, deliberately** — it was already plainspoken and correct, and group 7 is clarity-first. |
| 2 Home | done | 5 edits in `_src/page-home.html` (the prose is markup, not JSON). |
| 3 Collections | done | 6 edits, incl. **an invented competitor price** (below). |
| 4 Families | done | Only 1 edit needed across 11 files. These were already written in the approved shape: specs paired with outcomes throughout. Biggest-leverage group turned out to need the least. |
| 5 Products | **done** | 43 files. See the continuation block at the end. |
| 6 Brand/Trybe | done | 7 edits. It was defined entirely by negation. |
| 7 Support | part | FAQ self-reference only. The rest reviewed and left alone on purpose. |
| 8 Reviews | done | 1 edit, cross-page repetition. |

### The two real defects found

1. **An invented competitor price was live.** `_collection-putters.json` read
   *"why these two sit at $199 and $229 instead of $400."* Nobody supplied
   $400. Same class of error as the killed "charge triple". Rewritten to make
   the argument with our own real prices and no invented comparison. Swept the
   whole of `_src/` afterwards: it was the only one.
2. **Process vocabulary was rendering on two public pages.** `_shared-brand`'s
   `moreAside` put *"Some photography on this site is still a written brief"*
   on Our Story and the Ambassador page. v8.1 bans exactly this. Cut to `""`;
   the briefs still live in `phK`/`phBrief` where they belong.

### Repetition counts, before -> after
- Trybe "no follower minimum": **5 -> 0** (the fact survives once, as the
  "Open" stat's value, where it belongs).
- "The one-stars are in there": was about to hit **3** across pages. Now 1.
- Homepage closer: "bag" twice in two adjacent lines -> once.

### One judgment call left for Cole
The homepage marquee still runs **"30,000+ orders shipped"** and **"4.78 from
verified buyers"**. The sweep flags these, but `_brand-story.json`'s `_name`
rule says *"keep trust claims VAGUE"* and is scoped **"on this page"** — the
story page. These are verified real figures (34,360 per Shopify Admin) on the
highest-traffic page's conversion band, so stripping them is a commercial
decision, not a voice one. **Left in. Cole decides.** Per-product review
counts on PDPs and the reviews page were left in for the same reason: a review
widget's whole job is the count.

### Layout traps hit while doing this
- A heading rewrite that reads fine can **double a display heading's line
  count**. "Serious clubs. Unserious price" went 2 lines -> 4 in a 392px
  column. Measure `height / lineHeight` before and after every heading edit;
  the replacement ("Gold clubs, honest math") holds at 2.
- The rollout's browser-resize trap is real and `resize_window` fixed it, but
  **screenshots also need the pane actually displayed** or they time out at
  5s. Measure with `javascript_tool` instead; it works either way.

### Also noticed, not touched
`_src-home-template.html` is dead. `tools/split-src.py` is a spent one-shot
("then this script is history"), and the template has not changed since
2026-07-31 while `_src/page-home.html` has. It still carries `884 reviews` and
an em dash, so it will keep tripping any sweep run over `*.html`. Candidate
for deletion, but not in a copy pass.

**Guards at handoff:** `--check` 58 identical, `--links` 0 dangling,
`test-variants.js` all invariants hold, `normalize-products.py --check`
identical. Sweep clean except the counts named above.

**Job 2, the comparison page, is untouched.**

---

## PROGRESS — session 2 continued: group 5 closed

Cole's ruling that unlocked it, verbatim: *"why someone should choose a polo
it's just based off the design that's it it's like people just like the design
so that's the reason why they choose one polo over the another."*

### The polos: it was a proportion failure, not a voice failure

My first read of these pages was wrong and is corrected here. The per-print
lines were ALREADY close to Lucky ("Gold flecked across the shirt like it was
thrown at it", "Gray camo, built out of four-leaf clovers"). The failure was
that each print got **one sentence**, and the page then handed its biggest
editorial block to a fabric essay byte-identical across all thirteen shirts.
A person spoke for one line; a spec sheet took the rest.

Fixed by overriding `pieceHeadline`/`pieceParas` per print on all 13. No
fabric fact lost: the spec table and the fit block are separate. Volume varied
deliberately across the set (Cruiser and Gold Dust loud, Signature Black and
Azalea quiet, Frost dry) because thirteen blocks in one shape would read
templated no matter how good each one is.

### Hats: deliberately NOT given the same treatment

`_family-hat.json`'s `_piece` carries a Cole ruling from 2026-07-31 against
exactly that: *"Every colorway used to carry its own bespoke headline and two
paragraphs, which is 22 pages of copy saying the same thing 22 ways."* It also
sanctions the escape hatch: *"Anything genuinely specific to one design goes
in that product's own file and overrides these keys."*

The distinction that resolves it: **the polos are 13 distinct artworks; the
hats are 4 designs in 10 colorways** (classic mark, script, woven patch,
inverted mark). Bespoke blocks are right for the first and are the July
failure mode for the second. The hats keep the shared block; their per-design
difference already lives in `buyBody`, in the buy box, where the choice is
made.

### Clubs and gear: no rewrite needed, and that is a finding

Read end to end, both were already in the approved voice and needed nothing.
"Forged feel meets filthy spin." "One driver. One spec. No fitting
appointment." "It is a glove: it grips, it wears out, you buy another one."
"You are out of tees, and you have been since March." The clubs already carry
per-product `clubHeadline`/`clubParas`, which is the architecture the polos
were missing.

### Defects closed this session
1. Invented $400 competitor price (`_collection-putters`).
2. Process vocabulary rendering on Our Story and the Ambassador page.
3. **`(HANDOFF §7b F)` visible to customers on 23 polo and hat pages.** An
   internal doc section number in the photo placeholder. Now 0 site-wide.
4. **The buy-box trust row was hardcoded to the polo's fabric line**, so all
   ten hat pages claimed "Four-way stretch, UPF 50+". Neither is a hat spec.
   Now data-driven per family via `buyTerm`.
5. British "colour" in `_family-hat`, on an otherwise US-spelling site.

### Still open for Cole
- **`jmSummary` on `lgw01-gold` contains the banned word "premium."** It is
  Judge.me's auto-generated review summary, labelled on the page as
  "Auto-generated by Judge.me from all 551 reviews". Rewriting attributed
  third-party text would make it a fabrication, so it was left alone. Either
  accept it as third-party wording or drop the summary widget. Cole's call.
- The marquee order/review counts (see the previous block).
- 25 pages still render a photo brief as visible placeholder copy. That is the
  intentional prototype pattern, not a copy defect, but note that the aside
  explaining it was removed from the brand pages, so the pattern is now
  unexplained where a visitor meets it.

**Guards:** `--check` 58 identical, `--links` 0 dangling, `test-variants.js`
holds, `normalize-products.py --check` identical. Sweep clean except the two
items named above.

**Job 2 is now built. See below.**

---

## JOB 2 — the comparison page: BUILT

`33-compare.html`, slug `compare`, title "What you pay for".
Live at `/33-compare.html`.

### The design decision that made it possible without numbers

The three constraints (no competitor named, no invented price or percentage,
no undefendable row) rule out the table Takomo can run, because theirs has
figures in it and we have none we can stand behind. So the page is built on
the **asymmetry of two stacks instead of a table of numbers**:

    THE BIG NAMES            LUCKY
    The club                 The club
    The tour contract
    The shelf
    The middleman

Four rows against one. The empty space under the Lucky column is the argument,
and it needs no figure at all. Measured on the built page: 417px against 201px.
The Lucky column carries the only color difference on the page, a gold top
rule. **Do not "balance" the columns by padding the Lucky side** — that is
noted in the template and the CSS, because it will look like a bug to anyone
who does not know it is the point.

The day Cole supplies real figures they drop into the existing `v` fields and
nothing has to be rebuilt.

### Every number on the page, and where it comes from
`$99` LGW01, `$199` LGP01, `$229` LGP02, `1020` forged carbon steel, `431` and
`304` stainless. All Product Reference Guide v1.8, all ours. Audited on the
built page: those six and nothing else. Competitor-name check: clean.

### The link anchor changed, deliberately
VOICE-ROLLOUT named **"No crazy retail prices"** as the phrase to wrap. That
wording no longer exists: it was replaced in the 2026-08-25 story rewrite. The
link now sits on **"the middlemen, the retail markup"**, which is the claim the
comparison page actually proves (two of its four rows are exactly those).

It is deliberately NOT on "No four-figure price tags", the other candidate.
That phrase makes a claim about what other people charge, and this page carries
no figure that is not ours, so the link would promise proof the page does not
offer. Reasoning is recorded in `_brand-story.json` under `_compare`.

The page was also added to `_shared-brand.pages`, so it appears in "The rest of
it" on Our Story, the Ambassador page and Reviews.

### Wiring, for whoever touches this next
- `_src/data/copy/_page-compare.json` — copy, with `_rules` restating the three constraints
- `_src/page-compare.html` — template
- `_src/page-compare.css` — styles
- `tools/sitemap.py` — `add("compare", "33-compare.html", ..., src="compare", built=True)`
- `tools/build.py` — `compare_copy()`, the `if slug == "compare"` ctx line, and a
  `"compare"` entry in `REQUIRED`
- `_src/data/copy/_brand-story.json` — `trio.cards[1].paras[1]` carries the link

**The smoke markers were tested by breaking one:** changing
`.cmp-col--us{border-top-color:var(--gold)}` to `red` correctly failed the
build with "compare: build is missing required rules". They are real, not
decorative.

### Verified on the built page
Desktop 1425px and mobile 375px: no horizontal scroll, columns stack at 760px.
Contrast, with rgba composited by hand rather than trusting the raw ratio
(the sweep mis-scores rgba): row body 6.4:1, sibling hook 4.9:1, gold tag
5.05:1 at 11.5px. All pass AA.

**Guards:** `--check` **59** identical (58 + the new page), `--links` 0
dangling, `test-variants.js` holds, `normalize-products.py --check` identical.

### What would make this page much stronger
Real figures. The page works as the shape of an argument; it would work far
better as the shape of an argument with numbers in it. See "What I need from
Cole" below.

---

## JOB 2, REBUILT — after actually reading Takomo's page

Cole, 2026-08-25: *"Review Takomo's page first not sure I even see the
direction here."* He was right. The first build was wrong and has been replaced.

### What Takomo's page actually is
`takomogolf.com/pages/takomo-vs-big-brands`, titled **"Why Pay $1,400 for Golf
Irons?"**. It is a **7-row spec table**, not an essay:

| | Traditional manufacturers | Takomo |
|---|---|---|
| Full iron set price | $1,000 – $1,500+ | $579 – $679 |
| Iron material quality | Premium stainless (17-4 / S20C) | *the same sentence again* |
| Manufacturing process | Cast / Forged (varies by model) | *the same sentence again* |
| Shaft options | Steel / graphite, various | KBS, Fujikura, Mitsubishi, True Temper |
| Award recognition | Major industry awards | MyGolfSpy Most Wanted, Golf Monthly Editor's Choice |
| Sales channel | Retail & Online | Online |
| Try before buy | At the local store | Play the 7-iron 30 days |

**Its power is that rows 2 and 3 are word-for-word identical in both columns.**
That is how it proves "same club, different price" without arguing it. It also
puts a competitor PRICE RANGE on the page while naming no brand.

The first Lucky build got three things wrong: it was an essay of four abstract
cost buckets (no detail, which is the thing Cole liked), it had no figure at
all on the big-names side, and it was a brand page rather than a conversion
page. Scrapped.

### What ours is now
Same structure, our content, wedges only (Cole: *"Wedges for now, irons when we
drop them later this year"*). Seven rows, and rows 2 and 3 read identically.

`$170 to $200` against `$99 to $109`. **Cole cleared competitor pricing**
(*"yes Takomo did it that means we can"*). The range is VERIFIED from published
MSRPs on 2026-08-25: Titleist Vokey SM10 $189.99, Cleveland RTX 6 ZipCore
$169.99–$199.99. Deliberately conservative, no brand named on the page.
**Re-check it in a year: MSRPs move.**

### The award row: deliberately absent, and that was a judgement call
Cole asked what should go there. Takomo's strongest row is their MyGolfSpy and
Golf Monthly awards. We have nothing, and an empty cell on our side of a
comparison table reverses the whole page. So the row is **not there**, and the
**Finish** row takes its slot: gold, or blacked out with gold, against chrome,
black or raw. It is the one row the big names cannot match and it is the second
leg of the argument. Put awards back the day there is one.

### Two invariants added to build.py, and both were tested by breaking them
1. A row flagged `same` whose two cells have drifted apart **fails the build**.
   Without it the table still renders, still prints "Identical" in the margin,
   and is now lying.
2. The price row's Lucky side is checked against the catalogue, so it cannot
   drift the way the club finder did ($119 against a real $109).

Proven by mutation: `'Cast steel'` into the Head construction row and
`'$79 to $109'` into the price row both stop the build with a named error.
(The second silently passed at first: the guard read `category`, and the
product record's key is `family`. A guard that cannot fire is worse than no
guard, which is why both get mutation-tested.)

### Verified on the built page
Desktop 1425px: no horizontal scroll. Mobile 375px: **the page does not scroll
sideways; the 600px table scrolls inside its own box.** Contrast, rgba
composited by hand: Lucky cell 17.3:1, "Identical" marker 5.05:1, footnote
6.8:1. All pass AA. No competitor named in visible copy (the only "Takomo"
strings on the page are CSS comments citing it as a design reference).

**Guards:** `--check` 59 identical, `--links` 0 dangling, `test-variants.js`
holds, `normalize-products.py --check` identical, sweep 0 hits.

### Confirmed while I was there
Takomo's "10 Strong" is real: About page, THE TAKOMO TIMELINE, 2023, *"Team
Takomo Grows (10 Strong)"*. Also worth knowing: **Takomo's wedges are $89 and
$99** — they are not the expensive one, they are at our price. And their copy
leans on "premium" and "tour-proven" throughout, both banned for us.

### The real gap this exposed, for the next session
Takomo's timeline mixes product launches with a founder, a team milestone, two
creator signings and two awards. **Ours is twelve entries and eleven of them
are product launches.** Theirs reads like a company growing; ours reads like a
release log. That is why they can be funny and we strain: they have events to
hang jokes on. The three standing asks (team size, press/awards, exact months)
are exactly the entries that would fix it.

---

## Session close: timeline, hat specs, and a correction to the record

**Cole is not the 2018 founder.** His words, 2026-08-25: *"Formed in 2018 I took
over in July 2025 - others were added as we went."* `_brand-story.json`'s
`_story` note was recorded as "Cole's account: founded 2018" and reads as
though he founded it. Corrected in `_ownership`. **Nothing on the live site was
false** — every sentence in the story card says "we", and the company did do
those things in 2018. The rule banning his name from the page happened to
protect us. Do not write "our founder" copy on the strength of the old note.

**Two timeline entries added,** taking product launches from 11-of-12 to
11-of-14:
- `July 2025 — Somebody Hit the Gas`: "Lucky changed hands. Nothing happened to
  the clubs or the prices. Everything happened to the calendar."
- `2026 — Nine of Us Now`: nine people, per Cole.

The first draft of the ownership entry was rejected on Cole's test — *"Did a
person who embodies the Lucky Golf voice write it?"* It was "New Hands on the
Wheel / What changes is the pace": press-release idiom in the title, analyst
voice in the closer. Worth keeping as a specimen of the failure mode: it is
competent, it is accurate, and nobody is home in it.

The July 2025 entry earns its place structurally, not just tonally: the
timeline shows five products in seven years and then six drops in eighteen
months, and until now gave no reason for the change of pace. Deliberately NOT
"Nine Strong" — "10 Strong" is Takomo's exact construction.

**Hat fabric specs: sourced, not invented.** All ten hat pages rendered
"Needs spec" twice. Shopify holds no fabric or care metafields for any hat
(checked via Admin API) and every hat description is the same generic line. The
live storefront does carry it: the product description says "Light, breathable"
and there is a "Moisture-Wicking Fabric" badge which is **hat-specific** — it
does not render on the head-cover page, so it is a product fact and not a
global trust badge. Fabric row filled from that. **The Care row was removed
rather than filled**: nothing about care is published anywhere, and a guessed
wash instruction can wreck a customer's hat. 20 visible "Needs spec" → 0.
Fibre composition remains unknown and only the manufacturer has it.

**The two unbuilt products are correctly flagged — no action needed.**
Investigated and closed: `lgp02-patriot` is the fifty-unit America's 250th run,
sold out, discontinued per Cole 2026-07-31. `lgd01` is the OLD driver, also
discontinued; the new driver Cole says is "coming this fall" is a different
product with no specs in the reference guide yet, and `normalize-products.py`
already says "do not rebuild until the new driver's data lands". The "2
declared, not built" line in the links report is intentional. Note that
`lgd01.json`'s copy describes the old $299 driver and will not transfer.

**The press question is now CLOSED.** The only coverage Cole could find is a VUE
Magazine gift-guide inclusion, and he flagged the doubt himself. Rejected: a
gift guide is lifestyle placement, not equipment validation, and next to
Takomo's MyGolfSpy Most Wanted it loses the comparison it invites. The bar for
that row is an independent test or a golf-media award. The Finish row keeps the
slot. **This is settled, not outstanding.** Remaining:
photography: 29 "Photo needed" slots, the largest being zero on-body apparel or
hat shots across 23 pages. Cole: "Photos I can do later."
