# Lucky Golf design system · v4

**Version 4.0 · 2026-09-18 · Daylight + Twilight, photo-led, Mags the guide.**

This is the one written system. It replaces, and wins over:
`handoff/LUCKY-SYSTEM.md` (v3 Deep Green & Gold), `LUCKY-DESIGN-BRIEF.md` and
the old design skill (v2 white gallery), and `design/YARDAGE-SYSTEM.md`
(the v4 draft, now merged in here).

| File | What it is |
|---|---|
| `shopify/assets/lucky.css` | The system as code. Tokens and every component, all `lg-`. **If this doc and the CSS disagree, the CSS wins** and this doc gets fixed. |
| `shopify/assets/lucky.js` | The behaviour: Mags the guide, the pop-up, the toast, the hole bar, the tracer. |
| `design/styleguide.html` | Every piece, live, in both grounds, desktop and phone. Built by `node tools/styleguide/build.cjs` from the two files above, so it can't drift. |
| The live promo page | The reference build: `shopify/sections/gwp-promo.liquid` + `gwp-promo.css` + `gwp-promo.js`. |

Copy is the `lucky-golf-copy` skill's job. This doc owns how things look and behave.

---

## 1 · The order of importance, on every page

1. **Photography.** Every page opens on a real photo. A photo beat at least every couple of sections.
2. **The voice.** Attitude with receipts.
3. **Mags.** He has a job: getting the shopper to checkout.
4. **Yardage.** Only where a number is real. Seasoning, never the meal.

If a page leans on 3 or 4 because it has no photos, it's the wrong page (Sept 18: the promo felt "too technical" until the photos came back).

## 2 · Grounds

One attribute, `data-ground`, swaps tokens. Components never fork per ground.

| | Daylight (default) | Twilight |
|---|---|---|
| Where | The whole site: home, collections, product pages, story, help, cart, promos | A whole page only for short events (night drop, limited release, Black Friday). Or one band inside a Daylight page. |
| Page | `#FFFFFF` | `#06110B` |
| Type | ink `#17140F` | `#F4F3F0` |
| Gold as type | `#8A6A1C` (any size) · `#A8821C` display only | `#EDD27C` |
| Big numbers (`.lg-num`) | `#C29A2B → #8A6A1C` | `#FFF3C4 → #C29A2B` |
| Glow | never | buttons, open panels, the ball, the bar |
| Floating surface | white | `#0B1911` |

Neither ground works without photos. White alone reads as a wireframe; dark alone feels heavy.

## 3 · Colour

| Token | Value | The one job |
|---|---|---|
| `--lg-page` | `#FFFFFF` | the page, 78 to 88% of a screen |
| `--lg-tile` | `#F4F3F0` | stone: product wells, cards, table fills. A material, never a band |
| `--lg-dark` | `#0B2E1F` | deep green: announcement bar, header, the one band, footer |
| `--lg-night` | `#06110B` | Twilight's page |
| `--lg-ink` | `#17140F` | all type on white; the black Mags |
| `--lg-on-dark` | `#F4F3F0` | type on dark; the light Mags |
| `--lg-gold` | `#C29A2B` | gold as a surface: buttons, rules, flags |
| `--lg-gold-text` | `#8A6A1C` | gold as type on white (5.05:1) |
| `--lg-gold-hi` | `#EDD27C` | gold type on dark. **Never on white** (1.5:1) |
| `--lg-ok` | `#008340` | in stock, verified. **Not "added"** |
| `--lg-clover` | `#0B5130` | inside the logo only. Gold type on it is banned (3.6:1) |

**The foil** (`#C29A2B → #EDD27C`): exactly two places per screen, the primary button and one display word. Never body size, never a field.

**The foil word moves once:** hovering a headline runs a light across its foil word (the same move as the button). Nothing else about it animates.

**The finish's metal (added 2026-09-18, narrowed 2026-09-20):** a finish other than gold may wear its own metal on the product's one display word, **but only on a dark ground**. Tested on the Carver Black page: gunmetal on white has almost no chroma, so it reads as greyed-out type rather than as a finish, and the photography was already saying black three times over. On white, gold stays. Gold is the one accent, it ties the two finishes' pages together, and buttons, stars, prices and links are gold on every page and every ground. `data-metal="black"` / `"silver"` still works, and now only takes effect inside `.lg-band`, `.lg-sign`, `.lg-on-dark` or a Twilight ground.

**Tags say something true** (Sept 19): Best seller, Sold out, In the bag. Not moods. Ink by default; the gold foil tag is for the one thing on a screen we most want noticed.

**The pinstripe is retired** (Sept 18). The Yardage pieces and the photos carry the texture now. A dark band gets one soft gold light from the top corner instead (`--lg-band-light`).

Contrast floor: 4.5:1 body, 3:1 display and graphics. Measure before handing anything back.

## 4 · Type

Archivo only, variable width and weight. Display: width 62, 800, caps, line height .9 (`.lg-d1/d2/d3`). Labels: width 78, 600, tracked caps (`.lg-label`, `.lg-eyebrow`). Body: 17px, ink at 70%, 46 to 62 characters a line. `.lg-aside` is the charm voice. `.lg-num` puts the ground's gold on a real number. No em dashes, no exclamation marks.

## 5 · Shape, space, depth, motion

- Radius: **10px controls** (chips, inputs), **12px buttons**, **18px surfaces** (cards, tiles, photos in the page). Photos never round themselves inside a rounded card.
- Content 1180px wide; sections 64 to 112px apart; every tap target 44px+ on a phone.
- **Shadows only on things that float over the page:** the Mags card, the pop-up, the drawer. Nothing in the page casts one.
- Motion is mostly still. The whole vocabulary: the foil slides on hover, photos ease on hover, the tracer draws once, the hole ball hops when the bag changes, Mags hops when his line changes, the pop-up rises and shrinks into Mags. No scroll reveals, no card lifts. `prefers-reduced-motion` stops all of it.

## 6 · Photography

- Formats: **full bleed** for the hero; **3:2** for bands and frames (the shoot is 3:2); **4:5** only when the frame itself is portrait; **4:5 tiles** for product cutouts on stone.
- **Never a portrait crop of a landscape frame.** It cut "LUCKY" off the hat and the putter head on the promo.
- Cutouts are for choosing (cards, pickers, cart). Photos are for wanting. Apparel is shown worn; clubs on the course.
- A photo we don't have is a **labelled slot** (`.lg-slot`) with the shot brief. Never grey, never stock, never another brand's photo. (The other DSC/1B3A files in Downloads are other brands.)
- Hero crop: `--focus` for desktop, `--focus-m` for phones.

## 7 · Components

All live in the styleguide. Classes to use:

| Piece | Class | Notes |
|---|---|---|
| Buttons | `.lg-btn` (foil) · `.lg-btn-line` (ghost) · `.lg-btn-sm` · `[data-done]` · `[data-busy]` + `.lg-sp` | Done state is ink |
| Chips, tags | `.lg-chips` `.lg-chip[aria-pressed]` `[data-dead]` · `.lg-tag` `-gold` `-ok` | Dead = dashed and struck |
| Swatch | `.lg-swatch` | Pick by picture |
| Chrome | `.lg-tick` `.lg-hdr` `.lg-ftr` (`.lg-ftr-soc`: Instagram, TikTok, YouTube) | Solid deep green. TikTok is its official mark (Simple Icons): Lucide has no TikTok icon |
| Photo hero | `.lg-hero` + `.lg-hero-img` + `.lg-hero-copy` · `.lg-hero.is-short` | Headline bottom-left. Short = a 380 to 480px banner for pages where what's under it is the point (Community, All reviews), the way Takomo runs theirs |
| Photo band | `.lg-pband` (3 × 3:2) | Phones: one wide, two under |
| Frame, split | `.lg-frame` (`.is-tall`) · `.lg-split` (`.is-flip`) | Text beside a photo |
| Band | `.lg-band` · `.lg-band.is-photo` (`--band-bg`) · `.lg-band-tile` | One per Daylight page |
| Cards | `.lg-card` `.lg-card-ph` (`.is-cut`) `.lg-card-bd` `-nm` `-pr` `-ln` | Product on stone, cut off its studio background. A second real photo (the detail shot) may fade in on hover; never on touch, where there is no hover |
| Panel | `.lg-panel` (`.is-open`) | A card that holds controls (a gift) |
| Reviews | `.lg-score` bars · `.lg-quote` · `.lg-stars` | Verbatim only |
| FAQ | `.lg-faq` `.lg-fq` `.lg-fq-a` | Native `<details>` |
| Trust, table, form | `.lg-trust` · `.lg-table` · `.lg-form` `.lg-input` | |
| Sign-off | `.lg-signoff` (Daylight) · `.lg-sign` (dark) | Every page ends on one |
| Mags | `.lg-mags` (with `.is-ink` + `.is-light` images) | Ground picks the art |
| Guide, pop-up, toast | `.lg-guide` · `.lg-pop` · `.lg-toast` | Built by `lucky.js` |
| Yardage | `.lg-hole` · `.lg-tracer` · `.lg-monitor` (launch monitor A) · `.lg-hud` (monitor B) · `.lg-prox` (review proximity A, `Lucky.proximity()`) · `.lg-numbered` · `.lg-ruler` · `.lg-specs` · `.lg-contour` | Real numbers only |

## 8 · Mags

- **Art:** black Mags (`gwp-mags-ink.webp`, `#17130E`) on light; light Mags (`gwp-mags.webp`, `#F5F3E8`) on dark. Never a third colour. Put both images in `.lg-mags`; the ground picks.
- **His job is checkout.** The guide card sits bottom-left (the chat bubble owns bottom-right; on phones he stands above the bottom bars). It always says **one** next step and does it on tap: "the hat's free, tap me and I'll show you where" (scrolls there), then "you're set, tap me to check out" (straight to `/checkout`, skipping the cart page).
- **The pop-up is for promo landing pages only** (the GWP page it was built for). **On a normal page an add to bag opens the cart drawer and nothing else.** No pop-up, no guide card: the shopper asked for the bag, so show them the bag. Where the pop-up does run, it asks the question outright after something good happens: **Check out** (foil) or **Add more / Keep shopping** (ghost). Closing it shrinks it into Mags, who then holds the checkout. Each question once per visit.
- **The guide is one white card** with a thin gold border, Mags and text in ink. Not a green bubble next to a floating bird (tried Sept 18; it read as two things and the green shouted). A card, because it floats over photos and must look tappable.
- **Where else:** the sign-off (on a bare gold line), the empty bag, the 404, the bag button, good-news toasts. **Never on an error.**
- Folklore stays folklore: "Legend has it..."

```js
Lucky.mags = { ink: '…/gwp-mags-ink.webp', light: '…/gwp-mags.webp' };
Lucky.guide.init({ host: document.querySelector('.lg-scope'), avoid: [stickyBar] });
Lucky.guide.say("You're set. Tap me to check out.", '/checkout');
Lucky.pop.open({ title: "The hat's in your bag.", body: '…', once: 'hat',
  primary: { label: 'Check out', href: '/checkout' },
  secondary: { label: 'Add more for the polo', action: '#clubs' } });
```

## 9 · Yardage, the personality layer: where each piece goes

The golf instruments. They replaced the pinstripe. Each one reads a real number the way golf reads it, and only shows up where it has one. Everything picked on Sept 18 is in the system, and the contour map came off the bench the same day. "On the bench" means built and ready but not used on any page; those pieces live in `design/yardage-library.html`.


| Piece | Where | Rule |
|---|---|---|
| Hole bar `.lg-hole` | Cart drawer free-shipping bar; any "spend $X" promo | Flags at the real thresholds |
| Tracer `.lg-tracer` | Promo and launch pages, between the offer and the products | One per page; hidden on phones |
| Section numbers `.lg-numbered` | Long pages: promos, story, guides | Not on short pages |
| Launch monitor A `.lg-monitor` | Product pages: the full readout (lofts, grinds, price, test drive) | Real values only |
| Spec tiles `.lg-specs` | Product pages, the per-loft detail | Manufacturer sheet only |
| HUD strip `.lg-hud` | Product cards, cart lines | |
| Review proximity A `.lg-prox` | Reviews blocks where people COMPARE (collection, product). Not the home page: nothing is being compared there, so the rating, the stars and the quotes do the job | Real Judge.me counts; average rounds down. `Lucky.proximity(el, {counts, nums:false, label})`: `nums:false` hides the per-star counts and the total (a count makes a young brand look smaller than it is), `label` replaces the caption, which defaults to "Every review takes a shot at the pin." The caption stays light and never claims one dot per review: the dots are SCALED (counts divided by `per`), so "every dot is a review" is not true. Only the inner and outer rings are labelled. It flips for a dark band on its own |
| Tick ruler `.lg-ruler` | A divider when a section needs one | Quiet |
| Contour map `.lg-contour` | **In the system (Sept 18).** One per page, behind a quiet section with no photo: the FAQ, "why the price", a spec block, the story timeline | ONE big map: Cole's hand-made base (2026-09-27, `design/img/contour-source.png` -> `lucky-contour-day/tw.webp` via `tools/contour-from-image.py`, lines at 16% ink / 18% cream, zoom 170 to 230%); every use shows a different part (`--cx --cy --cz`, `.is-left`, `.is-flip`, or `Lucky.contours()` picks). Never behind text |
| Loft chart, dot matrix, terrain | Ads, technical pages, the app | Not shopping pages |

## 10 · Page recipes

Bold = photo beat. At most one dark band on a Daylight page; the page always comes back to white; no two dark bands touch.

- **Home:** bar, header · **photo hero** · trust row · the clubs (cards) · **photo band** · why the price (split + frame) · **reviews on a photo** (the one dark beat) · apparel, worn · Mags sign-off · footer.
- **Collection:** header · title and one line · **photo band** (not a big hero: the grid is the point, and the apparel brands we measure ourselves against go straight to it) · filter chips · cards with HUD · compare table (contour behind) · review proximity · sign-off.
- **Product page:** header · **gallery: studio + on course** · buy box (chips, foil Add to bag, stock) · spec tiles · **split: in use** · review proximity + real quotes · FAQ (contour behind) · sign-off · after add: Mags guide to checkout.

**One product template per family.** Wedges, putters and the hybrid come off a single club template driven by data: the option rows are generated from the real variant keys, so a club with one hand shows no hand chooser and the fact goes in the spec table instead. Apparel has its own two (polo, hat). A page per print and per colourway is generated, never hand-built.

**Two rules that catch us out on product pages:**
- **A worn photo on a product page has to be THAT product on a body.** A lifestyle frame of a different colourway reads as a photo of the thing you are about to buy. If we do not have the shot, the page runs its own studio photography and we book the shot, we do not borrow another one.
- **A cross-sell row has to match its link.** "The rest of the look / All apparel" carries apparel only; a wedge in that row sends the eye one way and the link another. Same for "More from the bag / All clubs".
- **Promo / landing:** numbered · **photo hero with the offer** · sticky hole bar · tracer once · product cards · **photo band** · gift panels + a worn frame · **reviews on a photo** · FAQ + frame · sign-off · Mags guide + pop-up. Twilight for a night event.
- **Our story:** numbered · **photo hero** · alternating splits · **photo band** · one dark band (the quote) · timeline (contour behind) · sign-off.
- **Cart / drawer:** hole bar to free shipping · lines with HUD · foil Check out · empty bag = Mags + one line + a ghost button.
- **404:** Mags, one line, two buttons, then four things to buy so a dead link still lands somewhere.
- **Questions / help:** header · sticky jump row · a block per topic (shipping, returns, clubs, apparel, orders) as split + `.lg-faq` · three ways to reach a person · sign-off. Policy answers come from the product reference guide, never from memory.
- **Ambassador:** **photo hero** · what you get (three cards) · what we ask + the application form · **photo band** · FAQ · sign-off.
- **Community:** **short photo hero** (tag us, follow button) · sticky filter chips · even 4:5 grid, @handle and a bag badge with the product count on each post, a post opens with its products · Show more · ambassador sign-off.
- **All reviews:** **short photo hero** · the score (`.lg-score`, bars filter by stars) and one tile per club (live count, filters by club) · sticky filters · the list, club named on each · sign-off.
- **Contact:** ways to reach us beside the form, sign-off. No hours or response times we have not confirmed.
- **Search:** field · common searches · live grid, query in the URL · empty state that points at the clubs.
- **Cart page:** the drawer's content at full width: lines, hole bar, summary, trust row, Mags empty state. It reads the same bag as the drawer, never a second copy of the state.
- **Gear collection:** grouped by job (covers, grips, putter grips, glove) with a jump row, not one long grid. A price that varies by size is shown as a range.

## 11 · Buttons and buying

- **One foil button per screen, on the action we most want there.** On the promo that's the free-gift claim, so club Add to bag is the ghost. On a gold-club product page, Add to bag is the foil.
- "Added" / done is **ink**, never green. Green means in stock or verified.
- **No quantity steppers on club cards.** Golfers buy one of a club/loft; one tap, one club.
- Nothing that floats (Mags, toasts, chat) covers a sticky bar, its message, or a buy button. Toasts go bottom-centre on desktop, top on phones.

## 12 · Content rules (any surface)

No em dashes. No exclamation marks. No invented numbers: every price, spec and count comes from the product guide or the store, counts round down. **No fabricated reviews, names or photos**: reviews are verbatim from Judge.me with the real name. The founder is never named. No competitor named ("the big names"). Banned words: premium, luxury, revolutionary, cheap, tour-proven. No warranty language.

## 13 · Building on Shopify

- **Never switch or publish themes.** Landing-page builders (GemPages, Zipify, Replo) are tied to the live theme. Edit the live theme in place, only with Cole's go-ahead.
- Wrap sections in `.lg-scope` so nothing leaks in or out. The theme's root font is 10px: **px, not rem.**
- Run `npx @shopify/cli theme check` first: a Liquid error makes Shopify silently drop the file.
- The connector can't write the live theme. Push through the admin code editor in Chrome (the Chrome window must be on screen, or keystrokes land on a stale frame), then confirm every file with `checksumMd5` through the Admin API.
- Mags art and photos live in **Content > Files** (`file_url`), not theme assets.

## 14 · Changing the system

Change `lucky.css` / `lucky.js`, run `node tools/styleguide/build.cjs`, update this doc and the `lucky-golf-design` skill, in the same pass.

## 15 · Swapping the contour base map

**Swapped and approved by Cole 2026-09-27:** the site now uses Cole's hand-made map (ChatGPT, dark lines on white). It sits behind the club pages' spec sheet only (the technical spot). Off Home's "Priced honestly" (the bunched band ran behind body text) and off the Our Story timeline (already busy). Each page shows its own patch (seeded by the page address, some mirrored), always from the calm right side of the map (x 45 to 92%), and the lines fade out at the section's top and bottom. At the old 300% zoom the raster lines read about 4px thick, so the zoom is 170 to 230% (340% on phones) and the lines are faint. The generated SVG (`node tools/gen-contour-map.cjs`) stays as the fallback. To swap in a new one:

1. Save it as `design/img/contour-source.png`.
2. `python tools/contour-from-image.py design/img/contour-source.png` makes `shopify/assets/lucky-contour-day.webp` (ink lines) and `-tw.webp` (cream lines) with a see-through background.
3. Point `--lg-contour-day` / `--lg-contour-tw` at the `.webp` files. Rebuild the styleguide. Everything else (a different spot per section) stays the same.
