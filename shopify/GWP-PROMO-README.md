# Free hat, free polo · ends Friday, Sept 25

$90 gets the hat. $140 gets the polo too. $198 and shipping's free.

One Shopify section on lucky.css v3.0, dressed in the new look: the **Twilight
round** ground plus the **Yardage** layer (tracer, ruler, contour map, section
numbers). Both are switches in the section settings.

- `gwp-promo-full-page.html`: the page exactly as it ships. **This is the one for
  the design team.** One file, opens offline, real products and photos, working
  (simulated) cart.
- `gwp-system-preview.html`: the same page with a switcher for Daylight /
  Twilight, Yardage on / off, and the three headlines.
- `../design/yardage-library.html`: every instrument option we built, defaults
  and the back-burner ones. System notes: `../design/YARDAGE-SYSTEM.md`.

Both previews are rendered from the section's own schema, template and assets
(`tools/gwp-preview/`, run `node build-system.cjs`), so they can't drift from
what Shopify serves.

**Pushed 2026-09-18 (Cole: "push afterward").** Everything is on Shopify except
the one click that makes it live: publishing the draft theme.

| What | Where | State |
|---|---|---|
| Theme copy with the 8 files | "GWP free hat + polo (draft)", id 171450597653 | unpublished, checksums match local |
| Page | /pages/free-hat-free-polo, template gwp-promo | published (blank on the live theme until the draft is published) |
| Free Hat (Gift) | free-hat-gift: 10 hats, $29, same SKUs, stock mirrored at Ceries OMS | unlisted, Online Store only |
| Free Polo (Gift) | free-polo-gift: 13 x 6 = 78, $67, same SKUs, stock mirrored | unlisted, Online Store only |
| Discount "Free hat with $90+" | automatic Buy X Get Y: $90 from the qualifying collection gets 1 hat 100% off | Sept 18 to 11:59pm CDT Fri Sept 25 |
| Discount "Free hat + polo with $140+" | $140 from the qualifying collection gets up to 2 of hat/polo 100% off (one club over $140 must earn BOTH; Shopify lets each club count toward only one discount) | same dates |
| Collection "GWP qualifying items (internal)" | smart: every product NOT tagged gwp-gift | unpublished |

Preview: https://www.luckygolf.com/pages/free-hat-free-polo?preview_theme_id=171450597653

---

## 1 · Files

| File | Goes in |
|---|---|
| `assets/lucky.css` | `assets/` (skip if the theme already loads it) |
| `assets/gwp-promo.css` | `assets/` |
| `assets/gwp-promo.js` | `assets/` |
| `assets/gwp-contour-day.svg` | `assets/` (the contour map, Daylight colours) |
| `assets/gwp-contour-tw.svg` | `assets/` (the contour map, Twilight colours) |
| `assets/gwp-mags.webp` | `assets/` (Mags, on the unlock message) |
| `sections/gwp-promo.liquid` | `sections/` |
| `templates/page.gwp-promo.json` | `templates/` (pre-filled with the real clubs, reviews and FAQ) |

Then **Online Store > Pages > Add page**, template **gwp-promo**.

### The upload, in order
1. Reconnect the Shopify connector (claude.ai connector settings), or upload by
   hand in **Online Store > Themes > ... > Edit code**. **Duplicate the live theme
   first** and do all of this on the copy.
2. Create the two gift products (section 2), then hide them (section 3)
3. Upload the six assets, the section and the template (table above)
4. Create the page on the **gwp-promo** template
5. In the theme editor on that page: set **Hero hat photo** to the black and gold
   hat, check the two hero clubs, pick the headline
6. Run the checks in section 5 with a real cart, on a phone and a laptop
7. Publish the theme copy (or preview-link it first), then send the link

### Section settings worth knowing
| Setting | Default | What it does |
|---|---|---|
| Ground | Twilight round | Twilight = the dark promo look. Daylight = white, for everyday pages |
| Yardage layer | on | The tracer, ruler, contour map and 01/02 section numbers. Off = the plain page |
| Headline | "$90 gets the hat. $140 gets the fit." | Dollar amounts turn gold on their own |
| Row 1 / Row 2 club | Carver 01 Gold / Stryker | The two "club + gift = price" rows. Price comes from the product |
| Hero hat / polo photo | blank | Blank uses the gift product's first variant photo |

The ground only colours this section. The theme's own header and footer stay as
they are.

---

## 2 · The gift products and the discounts (done)

The gifts are **priced normally** ($29 / $67) and made free by two **automatic
discounts**, not $0 products. A $0 product is free to anyone who finds its link;
this way Shopify itself checks the $90 / $140 at checkout (Cole picked this,
Sept 18). The cart shows the gift at $29 with the discount taking it to $0.

- **Same SKUs as the real hats and polos**, so Ceries OMS ships the real item
- **Stock mirrored** from the real items at Ceries OMS on Sept 18. The two counts
  are separate, so a design could oversell if both sell out at once. Watch the
  low ones (several polo sizes have 1 to 5)
- The qualifying amount counts everything except the gifts, which matches the
  number the page's bar shows
- After Sept 25: the discounts stop on their own. Set both gift products to
  draft, and delete the internal collection if you like

## 3 · Hidden from the store (done)

- Status **Unlisted**: buyable, but not in search, collections or recommendations
- Published to **Online Store only**, so no Google, Facebook or TikTok feeds
- Tagged `gwp-gift` and `hidden`

Check: search the store for "free". Neither should appear.

---

## 4 · What's real on this page, and where it came from

| What | Source | Checked |
|---|---|---|
| Clubs, prices, stock | `luckygolf.com/products.json` | 2026-09-18 |
| Carver 01 Gold $99 · Black $109 · Tracer Mallet $229 · Stryker $209 | same | live |
| Tracer Blade | **left off, sold out** | live |
| Hero rows | Carver 01 Gold (photo 5) and Stryker (photo 5), prices off the product | live |
| Card photos | studio shots picked by measuring for a true-white background | |
| **Free shipping at $198** | live shipping rates: $128 and $166 carts paid $18, a $198 cart was FREE | 2026-09-18 |
| Reviews | Judge.me, verbatim, five stars, verified: Ray O., Jeff C., Arthur V. | |

**`CART-PLAN.md` still says free shipping is at $125. That is stale.** The live
rate and the cart drawer's reward bar are both at $198.

---

## 5 · Check it before sending traffic

1. Empty bag: bar reads "Your bag's empty. $90 gets you a free hat."
2. Add one Carver: hat unlocks, a toast says so
3. Tap a hat, hit **Throw it in**: the page subtotal stays $99; in the cart it shows $29 with "Free hat with $90+" taking it to $0
4. Tap it three more times: still one free hat
5. Bar reads "$41 away from your free polo"
6. Add the Stryker: polo unlocks. Claim it
7. Bar reads "Hat, polo, free shipping. Check out before it ends Friday."
8. Remove the Stryker: the polo comes back out and the page says so
9. Check out: both gifts on the order at $0.00

---

## 6 · How it decides

- Tiers are tested against what the customer pays for, **with the gift lines
  taken out**, so a free hat can't buy a free polo
- The subtotal is read back from `/cart.js` after every change, never counted
  in JavaScript
- Every cart call waits its turn on one queue: that's the double-add guard
- Gifts are only ever **removed** automatically. Adding one is the customer's tap
- The store's cart drawer is UpCart. The page stops it popping open over the
  gift picker, and refreshes it after every change

---

## 7 · Cut from the last version (Cole: "a lot of extra fat")

The tier cards, the "argument" band, the empty photo grid,
how-it-works, and the sign-off with the email box. Each one repeated something
the hero, the sticky bar or the FAQ already says. The trust row came back as
three small lines under the hero button, after Cole asked for "more
trustworthy".

---

## 8 · Live walkthrough, Sept 18 (what was found and fixed)

Tested on the LIVE theme (RIPPLE ... [Checkout+]) with real carts and the real checkout.

- **A single club over $140 charged the hat.** Shopify splits the clubs between the two
  discounts, so a $229 Mallet paid for the polo and left the hat at $29. The $140 discount
  now covers hat + polo together. Checked: Mallet alone checks out at $229 with both FREE.
- **Removing a club in the cart drawer left a paid gift behind.** The page now watches every
  cart request on the page, and `assets/gwp-guard.js` (loaded site-wide from
  `layout/theme.liquid`, one line above `</body>`) does the same on every other page and
  on /cart. It only ever removes a gift the bag no longer qualifies for.
- **Everything rendered at 62% size.** The theme's root font is 10px; lucky.css and
  gwp-promo.css now use px instead of rem.
- **Dark headings on the dark ground, 300-weight body, extra tracking** leaked in from the
  theme. Reset inside `.lg-scope`.
- **The Gorgias chat bubble and the Alia "Try your luck" tab covered Checkout** on phones.
  Lifted above the bars on this page only.

## 9 · After Friday, Sept 25

1. The two discounts end on their own
2. Set Free Hat (Gift) and Free Polo (Gift) to Draft
3. Remove the `gwp-guard.js` script line from `layout/theme.liquid` (line above `</body>`)
4. Optional: delete the empty `assets/gwp-contour-day.svg` and the "GWP free hat + polo
   (draft)" theme
