> **Merged into `design/LUCKY-SYSTEM.md` (v4, 2026-09-18).** Kept for history. Build from LUCKY-SYSTEM.md, `shopify/assets/lucky.css` and `design/styleguide.html`.

# Two grounds + Yardage (Lucky system v4 draft)

First used on the free hat / free polo page (Sept 18-25, 2026). It may become
the whole system. The full `lucky.css` update happens in its own chat: this
file is the brief for it.

- Live code: `shopify/assets/gwp-promo.css` (search "GROUNDS + YARDAGE") and the
  tracer in `shopify/assets/gwp-promo.js`
- The page: `shopify/gwp-promo-full-page.html`
- Every option, including the back-burner ones: `design/yardage-library.html`

---

## 1 · Two grounds

| | Daylight | Twilight round |
|---|---|---|
| Page | white `#FFFFFF` | near-black green `#06110B` |
| Type | ink `#17140F` | `#F4F3F0` |
| Use it for | everyday pages: PDPs, collections, story, help | promos, drops, launches, short promos, ads |
| Gold as type | `#A8821C` or darker | `#EDD27C` |
| Big gold numbers | the Twilight gradient one shade deeper: `#C29A2B` to `#8A6A1C` | light gradient `#FFF3C4` to `#C29A2B` |
| Glow | **never** | yes: buttons, the open gift card, the tracer ball, the bar |
| Product tiles | warm `#F4F3F0` | warm `#F1EEE6` (photos always sit on light) |

**Why the Daylight gold is darker.** Gold has to be readable. On white, nothing
lighter than `#A8821C` passes (3.57:1, large text only), and Twilight's
`#EDD27C` would score about 1.5:1. On the dark ground the light gold passes
easily. So it's the same gold idea, lit for each ground.

**Why no glow on Daylight.** A glow is light on a dark surface. On white it
has nothing to glow against and just reads as blur. That's why the review dots'
glow wasn't visible: it was on the white ground. Twilight only.

Built as one attribute (`data-ground="day|twilight"`). Never fork a component
per ground: the ground swaps tokens, the components stay the same.

## 2 · Yardage: the personality layer (replaces the pinstripe)

Instrumentation, never wallpaper. **Every number it shows is real:** prices,
thresholds, lofts, review counts.

| Piece | Where | Rule |
|---|---|---|
| Hole bar | the progress rail | ticks plus flags at the real thresholds ($90 / $140 / $198); the ball rides the fill |
| Tracer | one per page, between offer and product | a real launch-monitor arc built from the real thresholds. The ball flies to where the bag is. Hidden on phones (the rail already does the job there) |
| Ruler | above a section that needs a divider | a tick rule, never a heavy line |
| Contour map | behind at most two flat sections | real contour lines (marching squares on a height field), masked away from the text column |
| Section numbers | the eyebrows | 01, 02, 03... like hole numbers |

Rule: **one moving thing per page** (the tracer ball). Everything else holds
still. `prefers-reduced-motion` and hidden tabs put the ball straight where it lands.

## 3 · Defaults and the back burner

Picked (Sept 18):

| Instrument | Default | Also kept | Back burner, and where it fits |
|---|---|---|---|
| Launch monitor (club specs) | **A · data tiles** | B · HUD strip, for compact spots (cards, the cart) | C · loft chart zoomed to 50-60° (ads, technical pages); D · spec card |
| Reviews | **A · proximity**, lighter star labels | | B · share bar; C · gauge; D · 100-square grid |
| Green map | **A · contour** (live on this page) | B · elevation bands, stepped | C · dot matrix, D · terrain mesh, E · ridgelines: all for the app |

## 4 · Build rules learned the hard way

- **Never use % padding on images.** % padding is measured against the
  container's WIDTH, which crushed the wedge to about 2px on tablet. Use px.
- Photos never sit under a gradient or scrim. The hero tiles are plain.
- Light gold (`#EDD27C`) is never type on white. `--lg-ink-38` is never text (2.4:1).
- A background image can't read CSS variables, so the contour map ships as two
  SVG files, one per ground.
- Twilight cards are opaque (`#0B1911` under the glass) so the contour sits
  behind them, never through them.
- The ground only colours the section it's set on. Header and footer come from
  the theme.

## 5 · For the lucky.css chat

- Move the ground tokens from `.gwp[data-ground]` up to `html[data-ground]`,
  with Daylight as the site default
- Move the Yardage pieces into `lucky.css` as `lg-yd-*` components
- Retire the pinstripe / groove texture where Yardage replaces it
- **Pages built in the other chat will need a pass:** on Daylight they mostly
  keep working. What changes is the texture (groove to Yardage), the gold text
  value, the radius (18px surfaces, 12px buttons) and the section numbers

## 6 · Mags

Mags isn't on this page on purpose. The sign-off block (where Mags lives) was
cut as fat, and this page is a two-day promo that needs to sell clubs fast.
Mags stays on the header bag button. Mags belongs to the brand, Yardage belongs
to the data: Mags signs off and reacts, Yardage measures. Mags now pops up on the "you unlocked it"
message only, never on errors.

---

## 7 · Where everything goes, site-wide (decided Sept 18, after the promo went photo-led)

**The order of importance on any page:** photography first, then the voice, then Mags, then Yardage. Yardage is seasoning, never the meal.

### Grounds
| Ground | Use it for | Never |
|---|---|---|
| **Daylight** (white + gold) | The default for the whole site: home, collections, product pages, story, reviews, help, cart. Also this promo. | Never as a flat page with no photos (it reads as a wireframe) |
| **Twilight** (night green + gold) | Full page only for a short, time-boxed moment: a night drop, a limited-edition launch, Black Friday. As a band inside Daylight pages: the reviews band, any text set over a photo. | Never a whole everyday page |

### Photography (leads every page)
- Every page opens on a full-bleed photo, headline over a scrim.
- A photo band at least every two sections.
- Cutouts are for choosing (cards, pickers, cart); photos are for wanting.
- Apparel is shown worn; clubs are shown on the course.

### Personality, and exactly where it shows up
| Piece | Where | Rule |
|---|---|---|
| Mags | Page sign-offs, empty cart, 404, "you unlocked it" / success messages | Reacts to good news only, never on errors |
| Gold foil | One button + one word per page | Never body text |
| Hole bar (flags + ball) | The cart drawer free-shipping bar, any spend-threshold promo | Only real thresholds |
| Ball-flight tracer | One per page max: promo pages, launch pages | Built from real numbers |
| Section numbers 01/02 | Long pages: promos, story, guides | Not on short pages |
| Launch monitor tiles (A) | Product pages, spec area (loft, bounce, grind) | Real specs only |
| HUD strip (B) | Compact spots: product cards, cart line items | |
| Review proximity dots (A) | Reviews section on product pages, reviews page | Real counts, rounded down in copy |
| Contour map | Back burner. At most one quiet section on a technical page | Never behind text |
| Loft chart (C), dot matrix, terrain, ridgelines | Ads, technical pages, the app | Not on shopping pages |

## 8 · Learned on the promo page (Sept 18, Cole's calls). Build these into the system

The live free-hat/free-polo page (`shopify/sections/gwp-promo.liquid`, `assets/gwp-promo.css`, `assets/gwp-promo.js`) is the reference build. These were decided there and are not written anywhere else:

**Mags has a job: he gets people to checkout.**
- A Mags guide card sits bottom-left (on phones, above the bottom bars; the chat bubble owns bottom-right). It always says ONE next step and does it on tap: "the hat's free, tap me and I'll show you where" (scrolls there), then "you're set, tap me to check out" (straight to /checkout, skipping the cart page).
- After something important happens (a gift claimed), a small clean pop-up asks the question outright: **Check out** (gold foil) or **Add more / Keep shopping** (ghost). Closing it shrinks it into Mags, who then holds the checkout.
- The guide card is ONE white card, thin gold border, Mags + text in ink, soft shadow. Not a green bubble next to a floating bird (tried it; read as two things, and the green shouted on a white page). A card, because it floats over photos and must look tappable. Mags stands on a bare gold line only where the space is fixed and empty (the sign-off).
- Mags art: ink Mags (`gwp-mags-ink.webp`, #17130E = the ink token) on light; light Mags (`gwp-mags.webp`, #F5F3E8 = on-dark) on dark. Never a third colour. On a Twilight page he must switch to light (not automatic yet).
- Every page should end on a Mags sign-off: eyebrow, one display line, a charm sub ("Legend has it..."), a ghost button, Mags on a gold line.

**Buttons.**
- "Added" / done state is **ink**, never green. Green read as a stray colour.
- One gold foil button per screen, on the action we most want: on the promo that's the free gift claim; club "Add to bag" there is the ghost. On a gold-club product page the foil goes on Add to bag.
- No quantity steppers on club cards. Golfers buy one of a club/loft; one tap = one.

**Photos.**
- The shoot is 3:2. Photo bands use 3:2 tiles (three across), never portrait crops of landscape frames (cut off "LUCKY" on the hat and the putter head).
- A photo beside text (FAQ, fit) is 3:2 or 4:5 depending on the frame; check the subject survives the crop at phone and desktop.
- Reviews can sit on a photo band with a dark scrim; the page stays white.

**Floating things.** Anything fixed (Mags, toasts, chat) must never cover the progress bar or its message. Toasts go bottom-centre on desktop, top on phones.

**Pushing to Shopify.** Never switch/publish themes. Edit the live theme in the admin code editor from Chrome (the Chrome window must be on screen or keystrokes land on a stale frame), then confirm every file with `checksumMd5` via the Admin API. Theme root font is 10px: px, not rem. Run `shopify theme check` first; a Liquid error makes Shopify silently drop the file.
