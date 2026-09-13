---
name: lucky-golf-design
description: Build any Lucky Golf visual surface on-brand - web pages, sections, components, landing pages, email templates, ad creatives, social assets. Trigger whenever the user asks to design, build, mock up, or style anything visual for Lucky Golf, Lucky Wedges, or any Lucky product. Also trigger when reviewing or fixing existing Lucky Golf design work. Contains the complete design system v2 (palette D, white gallery) - tokens, the six devices, type, components, layout, motion - plus the email and ads translations. Voice/copy questions route to lucky-golf-copy; this skill owns how things LOOK.
---

# Lucky Golf Design System v2 (skill)

The living reference is the styleguide page `90-styleguide.html` (unlisted on
the live site) and `_src/core.css`. If they ever disagree with this file, the
CSS wins; update this file to match, never the other way around.

**v2 landed 2026-09-12: palette D, "white gallery", with the groove texture.**
Decided by Cole after 23 revs of the look board. There are no dark bands, no
green masthead and no cream page any more. If a memory or an older doc says
"green header", "ink hero" or "cream band", it is describing v1: ignore it.

## The brand in one line

Gold clubs, honest prices, a magpie called Mags. Premium with attitude,
never templated, never fake, Takomo-level restraint.

## Colour: tokens only

Every component uses a SEMANTIC token from `:root` in `core.css`. A component
that names a hex or a primitive (`--ink`, `--cream`, `--gold`) is a bug.
Palette D values:

| Token | D value | The one job |
|---|---|---|
| `--page` | `#FFFFFF` | the page |
| `--tile` | `#F3F1EC` | cards, photo wells, table fills (a material, never a band) |
| `--text` / `--text-muted` | `#17140F` / 64% | type; muted for body and meta |
| `--rule` / `--rule-08` | ink 14% / 8% | the hairline |
| `--band` / `--on-band` | white / ink | header, reel, footer. White bands get `--band-edge` hairlines |
| `--accent` | `#C29A2B` | gold as a surface: rules, stars, bars, the tag foil |
| `--accent-text` | `#8A6A1C` | gold as TYPE (5.05:1 on white). Never `--accent` as text |
| `--clover` | `#0B5130` | the mark, inside the logo only |
| `--ok` | `#008340` | state green: in stock, added, verified. Never decoration |
| `--foil` / `--foil-text` | the three-stop ramp | the primary button / one display word |
| `--groove-band` | ink 2.8% lines, 6px pitch | the texture on every band |

**Palettes A-F are one attribute:** `<html data-palette="b">`. The styleguide
has the switch. Never fork a component per palette.

Contrast law: floor 4.5 body, 3.0 large. Gold type is `--accent-text` on light
fields and `--accent-on-band` on bands. **Gold on the clover green is banned
as type everywhere.** The foil is display-size only.

## The six devices (carry all six before polishing anything)

1. **Foil** - gold as a material. The primary button and ONE display word per
   page (`<em class="foil">`). Never body size, never a paragraph.
2. **Mark** - Mags the magpie on the bag button (`.bag`), the sign-off
   (`.sign`), the 404 and the empty bag. Stand-in art is `img/mags*.webp`;
   the designer's SVG replaces it in place. Folklore only: "legend has it".
3. **Groove** - 1px lines on a 6px pitch over whole bands (`.band`, `.tick`,
   `.hdr`, `.ftr`). Page sections divide with ONE hairline (`.groove`).
4. **Stamp** - `.lab` / `.eb`: Archivo width 78, weight 600, tracked caps.
5. **Aside** - the charm voice, `.aside` or the sign-off `.sub`. Attitude
   with receipts. Never a flat double statement, never an em dash.
6. **Eyebrow** - `.eb`: a 22px gold rule and a label leads every section. It
   orients; it never restates the headline.

## Type: Archivo, nothing else

- `.disp` = width 62, weight 800, caps, line-height .88. Sizes `.d-xl` (the
  sign-off, one per page), `.d-l` (H1), `.d-m` (sections), `.d-s`, `.d-xs`
  (card titles).
- `.body` 15px muted, max 47ch. `.lab` labels. `.aside` the charm voice.
- Base 15px; 16px on phones. `text-wrap:balance` on display. No em dashes.

## Components (markup in the styleguide; keep the classes)

- **Buttons**: `.btn` foil primary (one per view), `.btn-line` ghost,
  `.btn-sm`. All 44px+ on touch, press scale .975, arrows nudge.
- **Pills and chips**: `.fin .f` two-way pills (finish, hand); `.lg9` the
  nine loft-and-grind chips, multi-select up to three; `.set .s` the 1/2/3
  tiles; `.chip` single-select (facets); `.seg` segmented control.
- **Tiles**: `.tile` photo well (`.cut` for studio cutouts on a multiply
  well), `.tile.slot` the LABELLED SLOT for a photo we do not have (never a
  fake shot, never an unlabelled hole), `.pt2` product card, `.ptile` the
  collection card with `.qadd` quick add and the `.qa` picker, `.kv` copy
  card with a pill, `.q` review card, `.card` link card, `.figs` stat tiles.
- **Bands**: `.band` = white, hairline top and bottom, groove. Only the
  header, the reel and the footer.
- **Mood**: `.mood` + `.mhero` + `.rail`: one full-bleed world per page,
  headline bottom-left over the scrim, numbered callouts on the photo, a
  mixed-ratio rail under it. Every page gets exactly one.
- **Tables**: `.t2` with the `.lofts-row` (big numerals, 2px rule under).
- **Reviews**: `.rv-top` score + `.jm-bars`, three `.q` cards VERBATIM from
  the Judge.me pull (the build refuses a quote it cannot find), then the
  `.jm` list behind "Read all". FABRICATING A REVIEW IS BANNED.
- **Sign-off**: `.sign`: eyebrow, the line with the foil word, the sub, the
  who ("Mags has your 56. Again."), a ghost button, Mags on a 2px line.
- **Sticky bar**: `.stickybar` / `.atc-bar` on phones only, from the buy
  button leaving the screen to the footer arriving.
- **Chrome**: `.tick` trust bar, `.hdr` with mega menu and the mobile
  accordion, `.ftr` with the email capture first and two hairlines, `.cd`
  cart drawer, `.md` modals, `dialog.zoom`.

## Layout

- `.wrap` max 1180px, gutter `--pad`. Sections `var(--sec)` (48 to 64px).
- Page rhythm: trust bar > header > page (white) > one band mid-page (the
  reel) > sign-off > footer. No two bands touch; the page never goes dark.
- Radius: 6px controls, 14px surfaces. Photos never round themselves inside
  a rounded card.
- Rails: `scroll-padding-left` matches the padding or snap eats the gutter.
- Phones: galleries swipe with dots, grids carrying `.msnap` become rails,
  the buy box goes static, every target is 44px.

## Motion: still

The foil slides on hover, the film plays, Gold/Black crossfade. No scroll
reveals, no lifts, no drop shadows. `prefers-reduced-motion` kills all of it.

## Content rules (any surface)

No fabricated reviews, names or numbers; counts round down. Trial wording is
"sixty days to decide / prove us wrong", never "on real grass". No warranty
language. Voice is the `lucky-golf-copy` skill / How We Write v8.

## Email and ads

Designed in Figma, so the full system applies: white page, tile cards, the
foil on one word or the button, Mags to sign off, real photography, real
quotes. Live-coded email parts: 16px ink on white, solid gold fallback
button. Ads: white or ink ground, one condensed-caps headline, foil headline
only when no club is in frame, 4:5 first.

## Workflow

1. Building web: copy component markup from `90-styleguide.html` or the
   page templates in `_src/`, keep the classes, let `core.css` do the work.
2. New page: register in `tools/sitemap.py`, add `_src/page-NAME.html/.css`,
   add its smoke markers to `REQUIRED` in `tools/build.py`, run
   `python tools/build.py` then `--check` and `--links`.
3. Verify before shipping: no console errors, no horizontal overflow at 1440
   and 390, no `{{` left in the output, 44px targets, one foil word.
4. Changed the system? Update `core.css`, the styleguide page and this skill
   in the same commit.
