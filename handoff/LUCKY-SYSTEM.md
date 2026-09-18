> **RETIRED 2026-09-18. Superseded by `design/LUCKY-SYSTEM.md` (v4).** This v3 pack (Deep Green & Gold) is kept for history. The current code is `shopify/assets/lucky.css` + `lucky.js`; every piece is in `design/styleguide.html`.

# Lucky Golf: the design system, portable

**Version 3.0 · 2026-09-17 · System: Deep Green & Gold**

This supersedes `LUCKY-DESIGN-BRIEF.md` (v2, 2026-09-12), which described a
white-chrome, no-dark-bands version. Where the two disagree, this wins.

You are building something for Lucky Golf: a landing page, a section, an
email, an ad. Two files come with this document:

- **`lucky.css`**: the system as real code. Tokens and every component,
  all prefixed `lg-`. Use it as is. Do not restyle it, do not add colours.
- **`kit.html`**: a working page built only from those classes. Copy its
  markup. If you need a part that is not in it, ask before inventing one.

If a decision you need is not covered here, ask. Do not fill the gap with a
guess, and never fabricate a photo, a review, a name or a number.

---

## The brand in one line

Gold clubs, honest prices, a magpie called Mags. Serious about the clubs,
not that serious about ourselves. Premium with attitude, never templated,
never fake.

The two legs of every Lucky argument, and there is no third:

1. **You are not overpaying.** Same materials and engineering as the big
   names, minus tour contracts and retail rent, sold direct.
2. **You are not blending in.** Gold, on purpose, because golf got too
   serious and we did not.

If a line would sit unchanged on a competitor's site, it is wrong for us.

---

## Colour: one dark, one accent, and a lot of white

| Role | Value | The one job | Roughly how much of a screen |
|---|---|---|---|
| The page | `#FFFFFF` | Everything reads here | 78 to 88% |
| Photography | the shots | The only other big field | 6 to 22% |
| Deep green | `#0B2E1F` | Announcement bar, header, the band low on the page, the sign-off, the footer | 3 to 12% |
| Stone | `#F4F3F0` | Product wells, cards, table fills. A material, never a band | under 5% |
| Ink | `#17140F` | All text on white. Body at 70%, meta at 64% | type only |
| Gold | `#C29A2B` | The only accent: buttons, one word per headline, stars, hairline marks | under 1.5% |
| Gold as type | `#8A6A1C` | Eyebrows and links on white. The only gold you set text in on white | type only |
| Signal green | `#008340` | In stock, added, verified. Never decoration | tiny |
| Clover green | `#0B5130` | The clover inside the logo. Nowhere else | tiny |

Those percentages are measured off the live pages, not aspirational. If your
page is 30% dark green, it is not this system.

**What is gone, on purpose:** cream fields, brown, the old clover-green
masthead, a second green, any third colour. The old palette failed because
cream, green and brown were all fighting. One dark, one accent, white.

**Contrast, measured (not guessed):**

| Pair | Ratio |
|---|---|
| Cream `#F4F3F0` on deep green | 13.3:1 |
| Gold `#C29A2B` on deep green | 5.6:1 |
| Gold as type `#8A6A1C` on white | 5.1:1 |
| Ink on the foil button (darkest stop) | 7.0:1 |
| Stars `#9A7619` on white (a graphic, 3:1 floor) | 4.2:1 |
| **Gold on clover green `#0B5130`, BANNED** | 3.6:1 |

Floor: 4.5:1 for body, 3:1 for display and graphics. Measure it before you
hand anything back.

### The foil
Gold as a material, not a flat fill: `#C29A2B` to `#EDD27C` and back. It
appears in exactly two places per view: **the primary button**, and **one
display word** ("Ours is **gold**", "to be **lucky**"). Never at body size,
never as a background field, never twice in the same headline.

### The pinstripe
1px cream lines at 10%, every 6px, drawn as a tile (a long CSS gradient
rasterises unevenly and the lines look crooked). It goes on **dark feature
bands and the sign-off only**. The announcement bar, the header and the
footer are solid, because they sit over everything and should stay quiet.
The footer gets a soft light from the top edge instead.

---

## Type: Archivo, nothing else

Load the variable font with width and weight axes. Three registers:

- **Display**: width 62, weight 800, uppercase, line height .9. Headlines
  and card names. Balance the line breaks by hand.
- **Labels**: width 78, weight 600, uppercase, tracked .12em to .2em.
  Eyebrows, chips, tags, table heads, trust rows, the announcement bar.
- **Body**: width 100, 17px, ink at 70%, 46 to 62 characters a line.

The eyebrow is a 22px gold rule plus a label. It orients the section; it
never restates the headline. No exclamation marks, no all caps for emphasis
inside a sentence.

---

## The six devices. A page missing them reads generic

1. **Foil** on one word and one button.
2. **Mags**, the magpie, as an emblem: on the bag button and at the
   sign-off. Never a cartoon with a face doing an action. Cream artwork on
   dark grounds, ink artwork on white ones. Folklore stays folklore
   ("legend has it").
3. **The pinstripe** on the dark bands, one hairline between page sections.
4. **The stamp**: condensed caps on chips, tags, tables and trust rows.
5. **The aside**: one line of charm, sentence case. "Nobody needs a gold
   wedge. That is rather the point."
6. **The eyebrow** leading every section.

---

## Layout and rhythm

Content width 1180px. Sections 64 to 112px apart. Radius 6px on controls,
14px on surfaces. Everything tappable is at least 44px on a phone. Photos
never round themselves inside an already rounded card.

Page order that works, and the one a landing page should follow:

```
announcement bar  (solid, three claims, first one gold)
header            (logo LEFT, nav centre, search + Mags bag right, 72px)
hero              (one full-bleed photograph, headline bottom left)
trust row         (four facts, hairline top and bottom)
the offer         (cards on stone, or a two-up with one photo)
ONE dark band     (the argument: why the price is what it is)
proof             (real reviews, a real number, a compare table)
sign-off          (the brand line, the email capture, Mags on a gold rule)
footer            (solid, links, one hairline)
```

No two dark bands touch. The page never goes dark for more than one
section at a time, and it always comes back to white.

**Motion is still.** The foil slides on hover, photos ease on hover. No
scroll reveals, no card lifts, no drop shadows anywhere.

---

## Imagery

Three formats and nothing else: **full bleed** for the hero and the band,
**4:5 frames** for course photography, **4:5 tiles** for product on stone.

Real gold catching real light, never a render. A photograph that does not
exist yet is a **labelled slot** carrying the shot brief (`.lg-slot`), never
a grey box, never a stock photo, never a placeholder from another brand.

---

## How Lucky sounds

Someone talking, not copy. Confident without straining, warm without
trying, sharp without needing to prove it. Simple language any golfer
understands. When something bold gets said, it gets said plainly, because
the size of the claim carries it.

The voice has range: bold, plainspoken, dry. Same person at different
volumes; the piece picks the volume. A hero can be bold. A spec block is
plainspoken. A closer is often quiet.

**The test: attitude with receipts.** Every swagger line has to land on
something real, a product, a price, a thing that happened. "Golf has a
dress code. Ours is gold" works. Attitude with nothing behind it is noise.

**The failure mode to write against** is the flat double-statement: one
plain sentence followed by another plain sentence with nobody home in
between. If a line could open an investor deck, it is not Lucky. If it
sounds like the funniest guy in your foursome telling the truth, it is.

Approved lines, verbatim, for calibration:

- "Golf has a dress code. Ours is gold."
- "Great clubs got too expensive. We took it personally."
- "Same steel as the big names. Different math."
- "Serious about the clubs. Not that serious about ourselves."

### Hard rules, no exceptions

- **No em dashes.** Anywhere, in any copy.
- **No invented numbers.** No price, percentage or multiplier that is not
  in the Product Reference Guide. Counts round down.
- **No fabricated reviews, names or photos.** A review is quoted exactly as
  the customer wrote it, typos and all, with their real name and a verified
  mark, or it does not appear.
- **Trust claims stay vague.** "Thousands of happy golfers" and "sixty days
  to decide" are approved shapes. Counted claims are not.
- **The founder is never named**, and a review that names him cannot be
  quoted.
- **No competitor named.** The phrase is "the big names".
- **Banned words:** premium, luxury, revolutionary, cheap, tour-proven.
  "Tour-quality construction" is allowed. No warranty language.
- **No process vocabulary** in brand copy. A page never narrates how it
  was built.
- Never write a spec from memory. Open the Product Reference Guide.

---

## Using `lucky.css`

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="lucky.css">
<body class="lg">   <!-- or put class="lg-scope" on a wrapper -->
```

The parts, all in `kit.html`:

| Class | What it is |
|---|---|
| `.lg-tick` / `.lg-tick-in` | announcement bar |
| `.lg-hdr` / `.lg-hdr-in` / `.lg-logo` / `.lg-nav` / `.lg-hdr-act` | the header |
| `.lg-hero` + `.lg-hero-copy` | full-bleed photo hero with the scrim |
| `.lg-wrap` / `.lg-sec` | the 1180px measure and section spacing |
| `.lg-d1` `.lg-d2` `.lg-d3` `.lg-foil-word` | display type |
| `.lg-eyebrow` `.lg-lede` `.lg-body` `.lg-meta` `.lg-aside` `.lg-label` `.lg-link` | text |
| `.lg-btn` (foil) `.lg-btn-line` (ghost) `.lg-btn-row` | buttons |
| `.lg-band` `.lg-band-tile` | the dark band and its inner tiles |
| `.lg-grid` `.lg-card` `.lg-tile` `.lg-slot` `.lg-quote` `.lg-stat` | surfaces |
| `.lg-tag` `.lg-tag-gold` `.lg-tag-ok` `.lg-chip` `.lg-stock` `.lg-stars` `.lg-trust` `.lg-table` | small parts |
| `.lg-form` `.lg-input` | email capture |
| `.lg-sign` `.lg-ftr` | sign-off and footer |
| `.lg-on-dark` | put it on anything you build over a dark field |

To test another colour system, change one token: `--lg-dark`. Ink & gold is
`#17140F`; White & gold keeps the bands white and uses `#121212` for the
footer. Deep green is the pick being tested.

---

## Before you hand anything back

1. One foil button and one foil word per view, not five.
2. Any gold type on green? Fix it.
3. Contrast measured, not guessed.
4. Is the page still mostly white, with one dark band?
5. Every card on stone; every missing photo a labelled slot.
6. Every review, name and number real. No em dashes.
7. Would this sit next to the Carver 01 page and read as the same brand?
   If not, start over.
