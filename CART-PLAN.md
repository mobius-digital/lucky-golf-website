# The cart

Audited against the live store on 2026-09-09. Two carts exist and they are not
the same thing:

- **Live today:** the slide cart on luckygolf.com is the **UpCart** app, not the
  theme. There is no `<cart-drawer>` element on the store at all. Its settings
  live in UpCart's dashboard, not in Shopify and not in this repo.
- **In this repo:** `_src/core.js` renders a prototype drawer backed by
  `localStorage` with no checkout behind it. It exists to prove the interaction
  and the design. **It is not the thing to port.**

---

## What is live right now

| Module | State | Notes |
|---|---|---|
| Free-shipping bar | **on** | One tier, $125, cart total |
| Announcement bar | **on** | Promoting a sold-out product (see below) |
| Upsells | **on** | One item, and it is sold out (see below) |
| Discount code field | on | |
| Trust badges | on | |
| Recommendations | off | |
| Order notes | off | |
| Express pay buttons | **off** | |
| Add-ons / shipping protection | off | |
| Sticky cart button | off | |

**The $125 free-shipping threshold is real.** Verified against the Shopify
delivery profile: there is a `FREE SHIPPING` rate at $0.00 with the condition
`TOTAL_PRICE >= 125.00` on the domestic zone. The bar is not promising something
checkout will not honour, which is the usual failure with these.

It is also well chosen, by accident or not: a $99 wedge alone does not qualify,
a $99 wedge plus a $29 hat is $128 and does. The threshold does the work of
pushing a one-item order to two.

---

## Two things that are broken today

Both point at the same product: **LGP02 Mallet Putter - Patriot**, the
fifty-unit America's 250th run. It is **sold out** (0 inventory,
`availableForSale: false`) and was discontinued by Cole on 2026-07-31.

1. **It is the cart's only upsell.** Every customer who opens the cart is
   offered one product, and nobody can buy it. The upsell slot is earning zero.
2. **The announcement bar advertises it**: *"New America 250 Mallet Putter Now
   Live / Only 50 Made!"* That runs at the moment of checkout, which is the
   worst place to send someone after something that does not exist.

Both are fixed in the UpCart dashboard, not in code.

---

## What the upsell should be

The job of a cart upsell on this store is **not** to sell another club. It is to
close the gap to $125 so the order ships free and the basket grows.

- A wedge is $99. A hat is $29. That is the whole play: **one wedge plus one hat
  clears the threshold.**
- Prefer cheap, high-attach, no-fit-decision items: hats, tees, gloves,
  headcovers, grips. Nothing that needs a loft or a hand chosen in a drawer.
- Never offer something already in the cart. Never offer an out-of-stock
  variant. Check `availableForSale`, not quantity — this store oversells some
  lines and holds others at zero while still selling them.
- Keep it to one or two tiles. A drawer with a grid in it stops being a cart.

---

## What to turn on, in order of expected return

1. **Fix the upsell and the announcement.** Free money, ten minutes, no build.
2. **Express pay buttons** (Shop Pay, Apple Pay, PayPal) in the drawer. The
   single most reliable conversion lever in a cart and currently off.
3. **A second reward tier** above $125 only if the margin supports it. One tier
   that is already met stops motivating; a second gives the bar somewhere to go.
   Needs a decision on what the reward is, and it must be a real Shopify
   discount, not just cart copy.

## What to leave off, and why

- **Order notes.** They invite requests the warehouse cannot honour, and
  modifications void the return window on a club.
- **Recommendations** alongside curated upsells. Two product rails in one drawer
  is noise; pick the curated one.
- **Shipping protection add-on.** It is a fee added to an order from a brand
  whose whole argument is that it does not add fees.

---

## For the theme build

The prototype drawer is a design reference. What has to survive the port:

- The `[data-add]` contract — `data-sku`, `data-name`, `data-price`, `data-img`,
  `data-variant` — is what the buy box, the quick-add panels, the lightbox and
  the upsell rail all speak. Keep the contract, swap what is behind it.
- Availability is `availableForSale`, never `quantity > 0`.
- Every price is per variant.
- A product card never shows a review count.

**Decide early whether the cart stays UpCart or becomes native theme code.**
Building a beautiful theme drawer while UpCart is still installed gives the
store two carts and the app will win. If UpCart stays, the drawer is a
configuration job and the theme should not render one; if it goes, its rewards
bar, upsells and discount field all have to be rebuilt. That choice belongs at
the start of the build, not the end.

> Known trap, already paid for once: UpCart intercepts add-to-cart. It opens by
> putting `.upcartPopupShow` on `<body>`, and exposes
> `window.upcartShouldSkipAddToCart`, `upcartOpenCart`, `upcartCloseCart` and
> `upcartRefreshCart`. Both `fetch` and `XMLHttpRequest` are patched on this
> storefront. If you add to the cart behind its back you must call
> `upcartRefreshCart` or its drawer shows a stale bag.
