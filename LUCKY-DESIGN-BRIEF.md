# Lucky Golf: the design system, portable (v2, 2026-09-12)

You are designing something visual for Lucky Golf: a page, an email, an ad, a
social asset, a mockup. Someone will tell you what they need built.

**If a file called `90-styleguide.html` is attached alongside this document,
it is the design system as real code: every component, with its CSS.** Copy
its markup and styles directly instead of rebuilding from the descriptions
below. This document then serves as the rules for how to use those pieces.
If only this document is attached, follow it exactly and say clearly that the
output is an approximation of the system, not the system itself.

If a decision you need is not covered here, ask rather than inventing.

**This is v2: palette D, "white gallery".** Anything that still describes a
green masthead, an ink hero or cream bands is the old system. Ignore it.

---

## The brand in one line

Gold clubs, honest prices, a magpie called Mags. Premium with attitude,
never templated, never fake, and as restrained as the best of the
direct-to-golfer brands.

## Colour: a white page, a tile, a gold accent

| Role | Value | The one job |
|---|---|---|
| The page | `#FFFFFF` | Everything reads here. |
| The tile | `#F3F1EC` | Cards, photo wells, table fills. A material, never a band. |
| Ink | `#17140F` | Type. Body and meta at 64%. |
| The hairline | ink at 14% | Structure. One line between sections, never three. |
| Gold, as a surface | `#C29A2B` | Rules, stars, bars, the tag foil, the button ramp. |
| Gold, as type | `#8A6A1C` | Eyebrows and links. The only gold you set text in on white. |
| The clover green | `#0B5130` | The mark, inside the logo. Nowhere else. |
| State green | `#008340` | In stock, added, verified. Never decoration. |

- **There are no dark bands.** The header, the "in the wild" reel and the
  footer are white bands with a hairline top and bottom and the groove
  texture (1px ink lines at 2.8%, on a 6px pitch). The hero photograph
  carries the only dark beat on a page.
- **Gold type on the clover green is banned in every medium** (3.56:1).
- Floor: 4.5:1 body, 3:1 display. Measure it.

## The foil (a material, not a colour)

Three stops: `#8A6A1C` low, `#C29A2B` mid, `#EDD27C` high, light stop in the
middle so it reads as metal. It lives in exactly two places on a page: the
primary button, and ONE display word ("Carver **01**", "to be **lucky.**").
Never body size. Never a fourth stop. In email, only inside images. In ads,
a foil headline OR a gold club in frame, never both.

## Type: Archivo, nothing else

- **Display**: width 62, uppercase, weight 800, line height .88. One
  sign-off size, one H1, section heads, card titles. Balance the breaks.
- **Labels**: width 78, weight 600, tracked caps. The eyebrow is a 22px gold
  rule plus a label; it orients, it never restates the headline.
- **Body**: 15px, ink at 64%, max 47 characters a line. 16px on phones.
- **The aside**: sentence case, medium weight. Attitude with receipts:
  "Nobody needs a gold wedge. That is rather the point." Never a flat double
  statement. No em dashes, ever.

## The six devices (a page without all six reads as generic)

1. **Foil** on one word and the button.
2. **Mags** the magpie: on the bag button, the sign-off, the 404, the empty
   bag. An emblem, never a cartoon acting with a face. Folklore stays
   folklore: "legend has it".
3. **The groove** on every band; one hairline between page sections.
4. **The stamp**: condensed caps labels on chips, tags, tables, trust rows.
5. **The aside**: the charm voice, one line, under a line above.
6. **The eyebrow** leading every section.

## The parts (all real code in the styleguide)

- **Tiles**: photos sit on the tile with a 14px radius; studio cutouts on a
  multiply well. A photo that does not exist yet is a LABELLED SLOT with the
  shot brief on it. Never fake a shot, never leave an unlabelled hole.
- **Cards**: product card (photo, name, price, one-line hook), copy card
  with a pill (the grinds, blade or mallet), review card (real quote, real
  name, verified), link card, stat tile.
- **Controls**: foil button (one per view), ghost button, two-way pills,
  the nine-chip loft-and-grind grid with multi-select, the 1/2/3 set tiles,
  segmented controls, chips. Everything 44px on a phone.
- **The mood**: one full-bleed world per page, headline bottom-left over the
  scrim, numbered callouts on the photo, a mixed-ratio rail under it.
- **The sign-off**: eyebrow, the brand line with the foil word, the sub, a
  "who" line, Mags standing on a 2px rule.
- **The chrome**: trust bar, header with Mags on the bag, footer with the
  email capture first and two hairlines.

## Layout and motion

- Content width 1180px. Sections 48 to 64px apart. Radius 6px on controls,
  14px on surfaces. Photos never round themselves inside a rounded card.
- Rhythm: trust bar, header, page, one band mid-page, sign-off, footer. No
  two bands touch and the page never goes dark.
- Motion is still: the foil slides on hover, the film plays, Gold and Black
  crossfade. No scroll reveals, no lifts, no drop shadows.

## Content rules (no surface is exempt)

- No fabricated reviews, names or numbers. Counts round DOWN.
- "Sixty days to decide" or "sixty days to prove us wrong". Never "on real
  grass" or "on course" near the trial.
- "Tour-quality construction" is allowed; "tour-proven" is banned. No
  warranty language. Premium, cheap, luxury and revolutionary are banned.
  Competitors are "the big names", never named.

## Email (Klaviyo)

A short page of the site: trust line, the header on white, a hero on the
tile, product cards, one real review, ONE primary button, Mags to sign off,
footer with two hairlines. One column, 600px, images at 1200px for retina.
Live-text parts: 16px ink on white; fallback button solid `#C29A2B` with
ink text, 44px tall; Arial bold fallback. Alt text on everything.

## Ads and social

White or ink ground. One condensed-caps headline. Real gold catching real
light, never a render. 4:5 first, then 1:1, 9:16, 16:9. Video: product in
frame in the first two seconds, captions in condensed caps, end card on ink
with the foil wordmark and one gold button.

## Before you hand anything back

1. Any gold type on green? Fix it.
2. Contrast measured, not guessed.
3. One foil word and one foil button per view, not five.
4. Every card on the tile; every missing photo labelled.
5. Every review, name and number real.
6. Would this sit next to the Carver page and look like the same brand? If
   not, start over.
