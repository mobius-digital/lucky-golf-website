---
name: lucky-golf-design
description: Build any Lucky Golf visual surface on-brand - web pages, sections, components, landing pages, email templates, ad creatives, social assets. Trigger whenever the user asks to design, build, mock up, or style anything visual for Lucky Golf, Lucky Wedges, or any Lucky product. Also trigger when reviewing or fixing existing Lucky Golf design work. Contains the complete design system - colours, the foil, type, components, layout, motion - plus the email and ads translations. Voice/copy questions route to lucky-golf-copy; this skill owns how things LOOK.
---

# Lucky Golf Design System (skill)

The living reference is the styleguide page: `90-styleguide.html` in this repo
(unlisted on the live site). This skill is the distilled, machine-usable
version. If they ever disagree, the styleguide page and `_src/core.css` win;
update this file to match, never the other way around.

## The brand in one line

Gold clubs, honest prices, green clover. Premium with attitude, never
templated, never fake.

## Colour: four colours, one job each

| Colour | Hex | Token | The one job |
|---|---|---|---|
| White | `#FFFFFF` | `--white` | The page. Everything reads here. |
| Ink | `#17140F` | `--ink` | Dark moments inside the page: hero, one band, closing CTA, footer. |
| Green | `#0B5130` | `--brand` | The masthead and the clover. Chrome, never a content band. |
| Gold | `#C29A2B` | `--gold` | The product. Accent, buttons, rules. Ramps into the foil. |

- **Cream `#F6F2E8` (`--cream`) is a material, not a surface**: card/tile
  fills and body text on dark. Never a full-width band.
- **State green `#008340` (`--green`)**: success only (in stock, added,
  verified buyer). Never decoration.
- Alpha steps exist for both ink and cream (`--ink-70/-muted/-38/-14/-08`,
  `--cream-70/-52/-18`). Use them; never invent a new grey.

### Contrast law (measured, current)

- Cream on ink 16.43 / white on green 9.40 / gold on ink 6.95 /
  gold-lo `#8A6A1C` on white 5.05 - all pass.
- **Gold on green = 3.56 = BANNED as type, everywhere, all media.**
  Gold appears on green only as the 2px rule or the clover shape.
- Floor: 4.5 body, 3.0 large text. Verify, do not eyeball.

## The foil (a material, not a colour)

Three stops: `#8A6A1C` low, `#C29A2B` mid, `#EDD27C` high. Light stop in the
MIDDLE is what makes it read as metal. Four ramps, already tokenised:

- `--lg-foil-v` vertical: display type.
- `--lg-foil-h` horizontal: buttons (highlight travels on hover).
- `--lg-foil-v-dark`: display type on ink, brightened.
- `--lg-foil-tag`: small chips/flags; ink text on it is the ONLY legal
  small-text-on-gold.

Rules: on white, foil is one accent word inside an otherwise-ink display
headline, never body-size. Never invent a fourth stop. In email, foil exists
only inside images. In ads, foil headline OR club in frame, not both.

## Type: Archivo, nothing else

Variable font, width axis is the voice switch:

- `.disp` = wdth 62, uppercase, 800, line-height .85. The shout.
  Sizes: `.d-xl` (hero, one per page) > `.d-l` (chapter heads, MAX 3 per
  page) > `.d-m` (section heads) > `.d-s` (card titles).
- `.disp-ed` = wdth 88, sentence case, 700, lh 1.08. For headlines that are
  a thought, not a label.
- `.body` 17px, `--ink-70`, max 47ch. `.aside` = the charm voice.
  `.eyebrow` = small caps label with 22px gold dash, MAX 1 per 3 sections,
  orients never restates. `.stamp`/`.mono` = spec data only.
- Text scale tokens `--fs-xs` through `--fs-xl`: eight steps, never add a
  near-duplicate.
- `text-wrap:balance` on display headlines. No em dashes in any copy, ever.

## Components (markup lives in the styleguide page; keep the classes)

- **Product tile `.ptile`**: cream fill, edge-bleed photo with
  `mix-blend-mode:multiply`, condensed-caps name, sub-20-word hook, plain
  price, one-word corner tag on the tag foil.
- **Review card `.rv-card`**: real Judge.me quote + name + product. Gold
  stars. FABRICATING A REVIEW IS BANNED.
- **Placeholder plates `.ph` / `.ph--dark`**: honest labelled slots for
  photography that does not exist. Solid brand plate + gold keyline + shot
  brief. Never fake the shot, never an unlabelled hole.
- **Buttons**: `.btn-foil` primary (one per view), `.btn-line` secondary
  light, `.btn-line-cream` secondary dark, `.btn-ink` commerce. All press
  (scale .975), arrows nudge, min 44px tall. One label per intent per page.
- **Pull quote**: one per page, 3 lines max, real buyer.
- **Collection/search card**: same `.ptile` + `.qadd` quick-add on the
  photo, bottom right. Sold out = corner tag, no quick add.
- **Compare card `.clp-cmp-i`**: segment bars (`.clp-seg`), never filled
  progress tracks; coming-soon = dashed variant, labelled.
- **PDP gallery/buy box**: `.gal-arw` 44px arrows on the cream stage,
  `.bx-stock` state-green dot, `.btn-add` ink to gold to state-green.
- **Accordion `.sup-q`** (native details, gold cross) and **form fields
  `.sup-fld`** (label above, 44px input, error below, no placeholder-labels).
- **Breadcrumb `.crumb.wrap`**: gold diamond separators, page gutter, side
  scroll on phones.
- **Rating breakdown `.jm-bars`**: rows are filter buttons, gold fills,
  real percentages.
- **Badges**: `.badge-new` state green, `.pt-tag` tag foil, `.clp-tag`
  brand green. One badge per card max.
- **Marquee `.mq`**: the offer on loop, under the hero, one per page; each
  set wider than the widest viewport.
- **Brand band `.bband`**: mid-page punctuation, what buyers praise, never
  the marquee's offer list.
- **Logo**: white on green, gold or cream on ink, brand green on light.
  Never green-on-ink (1.95). Clearspace one clover-width; min 96px wide.
- JS overlays (cart drawer, quick-add picker, lightbox, size guide, mega
  menu, club finder): markup in `_src/partials` and page templates; see
  them live on the site.

## Layout and seams

- Container `.wrap` (max 1560px, fluid `--pad`). Full-bleed moments escape
  one edge at a time, deliberately.
- **Page rhythm, every template**: green masthead > ink hero > white content
  with cream cards > one ink moment > ink closing CTA > ink footer with gold
  rule.
- **Radius law**: 6px small surfaces (buttons/chips/inputs), 14px large
  (cards/tiles/photos). Corner-anchored chips round the inner corner only.
- **Seam rule**: background clover emblems crop ONLY at the viewport edge or
  a colour change, never mid-shape at a same-colour seam. Adjacent white
  sections are one canvas; an emblem may span them
  (`overflow-x:clip; overflow-y:visible` + transparent neighbour).
- **Rails**: every scroll-snap rail needs `scroll-padding-left` matching its
  padding or snap eats the gutter.
- Groove texture (`--groove-dark`/`--groove-light`) is the surface finish on
  every band.

## Motion

- Curves: `--ease-out-s` cubic-bezier(.23,1,.32,1) for enter/react;
  `--ease-io-s` (.77,0,.175,1) for on-screen movement. Never ease-in.
- `.rv` scroll reveal; grids cascade 60ms steps. Cards stay put on hover:
  the photo zoom is the feedback. No lifts, no drop shadows (Cole, A/B
  2026-08-30).
- One ceremony per page: hero load-in (photo settles from 4.5% zoom, copy
  rises .18/.28/.4/.52s).
- `prefers-reduced-motion` kills everything. Non-negotiable.

## Content rules (any surface, any team)

- No fabricated reviews/names/numbers. Counts round DOWN (30,000+ ok).
- Trial wording: "sixty days to decide/prove us wrong". NEVER "on real
  grass"/"on course" near the trial.
- "Tour-quality construction" allowed; "tour-proven" banned.
- No warranty language (there is no warranty; 60-day return is the promise).
- Voice: `lucky-golf-copy` skill / How We Write v8 is the authority.

## Email translation (Klaviyo, designed in Figma)

Emails are DESIGNED IN FIGMA and exported, so the FULL system applies in
designed sections: every colour, the foil, grooves, condensed type. Do not
strip devices because of assumed email-client limits. Design an email as a
short page of the site.

- Structure mirrors the site: green masthead + gold rule, hero, product
  tiles, one review quote, one primary CTA, trust row, ink footer + gold
  rule. Build once as Klaviyo blocks.
- One column, 600px, export at 1200px for retina. Alt text on every image;
  keep the html part under Gmail's 102KB clip.
- LIVE-CODED parts only: body text 16px+ solid `#17140F` on white (alpha
  inverts in dark mode); coded fallback button solid `#C29A2B`, ink text,
  44px min; fallback font Arial bold.
- The legibility laws still travel: never gold type on green, real claims,
  real reviews. Test Gmail/Apple Mail dark mode before a flow ships.

## Ads and organic translation

Pixels, so the full device set returns.

- Grounds: ink or white. Green = frame element (top bar, clover) only.
- One condensed-caps headline per asset; foil headline only when no club is
  in frame (gold never competes with gold).
- Real product photography, gold catching real light. No renders-as-photos.
- Clover crops at the frame edge, never mid-shape on a flat field.
- Claims obey the content rules; ads are not exempt. Real quotes with names.
- Build 4:5 (1080x1350) first; export 1:1 (1080), 9:16 (1080x1920), 16:9.
  Protect the centre 1:1 crop.
- Video: product in frame in the first two seconds, captions in condensed
  caps, end card = ink ground + foil wordmark + one gold CTA.
- Organic: white ground, ink type, one gold accent, clover sign-off; stamp
  device for spec callouts on photos.

## Workflow

1. Building web: copy component markup from `90-styleguide.html` /
   `_src/page-*.html`, keep the classes, let `core.css` do the work.
2. New page: register in `tools/sitemap.py`, add `_src/page-NAME.html/.css`,
   `python tools/build.py`.
3. Verify before shipping: contrast (composite the alphas), overflow at 1440
   and 390, tap targets >= 44px, left-edge gutter alignment, emblem seams.
4. Changed the system? Update: `_src/core.css` comments, the styleguide
   page, this skill, and the shared artifact. Same commit.
