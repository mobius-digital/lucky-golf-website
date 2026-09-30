---
name: lucky-golf-design
description: Build any Lucky Golf visual surface on-brand - web pages, Shopify sections, components, landing pages, email templates, ad creatives, social assets. Trigger whenever the user asks to design, build, mock up, or style anything visual for Lucky Golf, Lucky Wedges, or any Lucky product. Also trigger when reviewing or fixing existing Lucky Golf design work. Contains design system v4 (Daylight + Twilight grounds, photo-led, Mags the checkout guide, the Yardage layer) - where the code lives, the rules, the components, page recipes, and the Shopify build rules. Voice/copy questions route to lucky-golf-copy; this skill owns how things LOOK and BEHAVE.
---

# Lucky Golf design system v4 (skill)

**Read `design/LUCKY-SYSTEM.md` before building anything.** It is the one
written system (v4, 2026-09-18). The code is the source of truth:

- `shopify/assets/lucky.css` : tokens + every component, all `lg-`, px only
- `shopify/assets/lucky.js` : Mags the guide, the pop-up, the toast, the hole bar, the tracer
- `design/styleguide.html` : every piece live, both grounds, desktop + phone
  (rebuild with `node tools/styleguide/build.cjs` after any change)
- The reference build: the live free hat / free polo page
  (`shopify/sections/gwp-promo.liquid`, `gwp-promo.css`, `gwp-promo.js`)

If a doc and the CSS disagree, the CSS wins; fix the doc. Retired, do not
follow: the v2 "white gallery" brief (`LUCKY-DESIGN-BRIEF.md`), v3
`handoff/LUCKY-SYSTEM.md`, `_src/core.css` for new work, and the groove texture
on white bands.

## The system in eight lines

1. **Photos lead.** Every page opens on a real photo; a photo beat at least every couple of sections. Order on any page: photography, voice, Mags, Yardage.
2. **Daylight is the whole site** (white, ink, warm grey tiles #F4F2EE, never cream). **Twilight** (`data-ground="twilight"`, night green) only for short events or one band. Components never fork per ground; tokens swap.
3. **Deep green `#0B2E1F`** carries the bar, header, one band low on the page, and the footer. At most one dark band on a Daylight page.
4. **Gold is the only accent.** Foil on one button and one display word per screen, on the action we most want. A Black or Silver product's own display word takes its finish's metal (`data-metal`); buttons stay gold. Gold type on white is `#8A6A1C`; No gold type or stars on the green: type there is off-white; on dark, gold is only the foil button (Cole 2026-09-27).
5. **Mags has a job: checkout.** Guide card bottom-left (white, gold border, ink), one next step, tap does it; pop-up after good news ("Check out" or "keep going"), which shrinks into Mags. Black Mags on light, light Mags on dark, never a third colour. Never on errors. Every page ends on a Mags sign-off.
6. **Yardage, the personality layer (replaced the pinstripe):** hole bar, tracer (one per page), launch monitor A (product pages), HUD strip, review proximity A (every reviews block), section numbers (long pages), and the contour map (one per page, behind a quiet no-photo section; one big map, a different part every time). The pinstripe is retired.
7. **Shape:** 6px controls, 6px buttons, 8px surfaces (tightened 2026-09-27). Shadows only on things that float. Motion mostly still.
8. **Photos keep their shape** (the shoot is 3:2). Never a portrait crop of a landscape frame. Missing photo = labelled `.lg-slot`, never fake.

## Hard rules

- "Added"/done is **ink**, never green. Green = in stock / verified only.
- No quantity steppers on club cards.
- Nothing floating covers a sticky bar, its message, or a buy button.
- No em dashes, no exclamation marks, no invented numbers, **no fabricated reviews** (verbatim Judge.me or nothing), founder never named, no competitor named.
- Archivo only.

## Workflow

1. **New page or section:** pick the recipe in `LUCKY-SYSTEM.md` §10, copy markup from `design/styleguide.html`, keep the classes, let `lucky.css` do the work. Wrap Shopify sections in `.lg-scope`.
2. **No structure changes to existing pages without Cole seeing it first** (the site board rule). Show, then he decides.
3. **Verify before shipping:** no console errors, no horizontal overflow at 1280 and 375, 44px targets, one foil button per screen, real numbers only, photos not cropped badly.
4. **Shopify:** never switch or publish themes (page builders are tied to the live theme). `theme check` first; push via the admin code editor with Chrome on screen; confirm with `checksumMd5`. px not rem (root font 10px). Files (photos, Mags) go in Content > Files.
5. **Changed the system?** Update `lucky.css`/`lucky.js`, rebuild the styleguide, update `LUCKY-SYSTEM.md` and this skill in the same pass.

## Email and ads

Same system: white page, grey cards, foil on one word or the button, real photography, real quotes, Mags to sign off. Live-coded email: 16px ink on white, solid gold fallback button. Ads: a real photo first, one condensed-caps headline, foil headline only when no club is in frame, 4:5 first.
