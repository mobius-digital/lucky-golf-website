# Lucky Golf: the design system, portable

You are designing something visual for Lucky Golf: a page, an email, an ad, a
social asset, a mockup. Someone will tell you what they need built.

**If a file called `90-styleguide.html` is attached alongside this document,
it is the design system as real code: every component, with its CSS.** Copy
its markup and styles directly instead of rebuilding from the descriptions
below. This document then serves as the rules for how to use those pieces.
If only this document is attached, follow it exactly and say clearly that the
output is an approximation of the system, not the system itself.

If a decision you need is not covered here, ask rather than inventing.

---

## The brand in one line

Gold clubs, honest prices, green clover. Premium with attitude, never
templated, never fake.

## Colour: four colours, one job each

| Colour | Hex | The one job |
|---|---|---|
| White | `#FFFFFF` | The page. Everything reads here. |
| Ink | `#17140F` | Dark moments: hero, one mid-page band, closing CTA, footer. |
| Green | `#0B5130` | The masthead and the clover. Chrome, never a content band. |
| Gold | `#C29A2B` | The product. Accent, buttons, rules. |

- **Cream `#F6F2E8` is a material, not a surface**: card and tile fills, and
  body text on dark grounds. Never a full-width background band.
- **State green `#008340`**: success only (in stock, added to cart, verified
  buyer). Never decoration.
- Greys are transparency steps of ink (70%, 62%, 38%, 14%, 8%) or cream
  (70%, 52%, 18%). Never invent a new grey.

### Contrast law

- **Gold type on green is banned everywhere, in every medium** (it measures
  3.56:1). Gold appears on green only as a thin rule or the clover shape.
- Floor: 4.5:1 for body text, 3:1 for large display text. Check it, do not
  eyeball it.

## The gold foil (a material, not a colour)

A three-stop gradient: `#8A6A1C` low, `#C29A2B` mid, `#EDD27C` high, with the
light stop in the MIDDLE. That middle highlight is what makes it read as
metal. Vertical ramp for display type, horizontal for buttons.

Rules:
- On white, foil is ONE accent word inside an otherwise-ink headline. Never
  body-size text.
- Never invent a fourth stop.
- In email, foil exists only inside exported images.
- In ads: foil headline OR a gold club in frame, never both. Gold never
  competes with gold.

## Type: Archivo, nothing else

One variable font. The width axis is the voice switch:

- **Display**: Archivo condensed (width ~62), UPPERCASE, weight 800, line
  height 0.85. One hero-size headline per page, max 3 chapter-size.
- **Editorial headline**: width ~88, sentence case, weight 700, when the
  headline is a thought rather than a label.
- **Body**: 17px, ink at 70%, max 47 characters per line.
- **Eyebrow**: small caps label with a short gold dash before it. Max 1 per
  3 sections. It orients, it never restates the headline.
- Monospace-style condensed caps for spec data only.
- No em dashes in any copy, ever. Balance display headline line breaks.

## Layout rhythm (every page, every surface)

Green masthead → ink hero → white content with cream cards → one ink
mid-page moment → ink closing CTA → ink footer with a gold rule.

- Corner radius: 6px on small things (buttons, chips, inputs), 14px on large
  (cards, tiles, photos). Nothing else.
- The clover emblem crops only at the viewport edge or at a colour change,
  never mid-shape against a same-colour seam.
- Cards do not lift or drop-shadow on hover; the photo zoom is the feedback.
- One primary (foil) button per view. One label per intent per page.

## Content rules (no surface is exempt)

- No fabricated reviews, names, or numbers. Real quotes with real first
  names. Counts round DOWN ("30,000+" is fine).
- Trial wording is "sixty days to decide" or "sixty days to prove us wrong".
  Never "on real grass" or "on course" near the trial.
- "Tour-quality construction" is allowed; "tour-proven" is banned.
- No warranty language. There is no warranty; the 60-day return is the
  promise.
- The words premium, cheap, luxury and revolutionary are banned. Competitors
  are "the big names", never named.

## Email (Klaviyo)

Design it as a short page of the site: green masthead with gold rule, hero,
product tiles, one real review quote, ONE primary CTA, trust row, ink footer
with gold rule. One column, 600px wide, images exported at 1200px for retina.

Live-text parts: body 16px+ solid ink on white; fallback button solid gold
`#C29A2B` with ink text, minimum 44px tall; fallback font Arial bold. Alt
text on every image. Test dark mode in Gmail and Apple Mail.

## Ads and social

- Grounds: ink or white. Green is a frame element only (top bar, clover).
- One condensed-caps headline per asset.
- Real product photography, gold catching real light. Never renders passed
  off as photos.
- Build 4:5 (1080x1350) first, then export 1:1, 9:16, 16:9. Protect the
  centre square crop.
- Video: product in frame within the first two seconds, captions in
  condensed caps, end card is ink ground + foil wordmark + one gold CTA.
- Organic posts: white ground, ink type, one gold accent, clover sign-off.

## Before you hand anything back

1. Any gold type sitting on green? Fix it. This is the most-broken rule.
2. Contrast: 4.5:1 body, 3:1 display, measured not guessed.
3. One foil moment per view, not five.
4. Cream used as a fill, never as a band.
5. Every review, name and number real.
6. Would this look at home next to the Lucky site, or does it look like a
   template with gold on it? If the second, start over.
