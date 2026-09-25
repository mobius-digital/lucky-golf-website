# Port notes: rules the Shopify theme has to keep

Decisions made on the review board that the Liquid sections must enforce.
Each one is already how the v9 preview behaves.

## Reviews (Cole, 2026-09-24)

- A product shows its star badge (cards and buy box) and its reviews section
  **only at 10 or more Judge.me reviews**. Under 10: no stars, no section,
  never "1 review" or "0 reviews".
- The test is the **count, never the rating**. Once a product is past 10,
  every review shows, good and bad.
- Counts are read **live** from the product metafields
  `reviews.rating_count` and `reviews.rating` (Judge.me writes them). Never
  type a number into a section setting.
- **Polos pool into one group** (every print, both collars) and **hats pool
  into one group**. The count that gates them is the group total. When the
  polo group shows, label it: "Reviews from every Lucky polo. Same fabric and
  fit, different print."
- Carver 02 Gold and Black already share one pool on Judge.me (661 on
  2026-09-24).
- In the preview the counts live in `_src/data/review-counts.json`, pulled
  from those same metafields; refresh it before publishing the board.

## Polos

- The buy button on apparel says "Add to cart". "Put it in the bag" is for
  clubs only.
- The model-sizing line under the size buttons ("[Name] is [height],
  [weight] and wears a [size].") is a per-product field that stays hidden
  until it's filled in.
- The size guide opens on the size picked in the buy box, with that column
  highlighted.

## Stock (Cole, 2026-09-24)

- Every product card, buy box, size chip and "Sold out" tag reads
  availability live (`variant.available` / `product.available` in Liquid).
  Nothing in a section setting or a metafield may say a product is sold out.
- The preview does the same from `_src/data/stock.json`, pulled per SKU from
  the Shopify Admin API; `v9/tools/live.py` overrides the saved catalogue with
  it and the build prints any SKU it couldn't find. Refresh it before every
  board publish.

## Restock notes (Cole, 2026-09-24)

- Each product gets a **restock date** field (product metafield
  `custom.restock_date`, a date), edited on the product in the Shopify admin,
  not in the theme editor.
- The note only appears on a variant that's sold out. With a date it reads
  "Back in October" (the month of the date); with no date it just says
  "Sold out" and offers "Tell me when it's back".
- Once the date has passed, the note hides itself, so a missed restock never
  keeps promising a month that's gone.
- Shopify Flow (free) sends Cole an email when a variant hits 0 and when a
  restock date passes with the product still at 0, so he knows to update it.

## Collections and product pages are templates (Cole, 2026-09-25)

Adding a product must never mean editing a page. In the theme:

- **One collection template** (Polos, Hats, Gear, All, Accessories and any new
  line such as a winter collection) fills its grid from the Shopify
  collection. Add the product to the collection, or let a smart collection
  rule (product type or tag) add it, and it appears with its image, price,
  sizes and live stock.
- **One product template per kind** (club, polo, hat, gear), each reading
  the product's own title, description, media, variants and metafields.
- **What the preview keeps in hand-made tables becomes product data**, set
  once per product in the Shopify admin:
  - polo and hat print/front lines (`polos-copy.json`, `HAT_COPY`, `GEAR_COPY`) -> the product description
  - filter groups (`HAT_META` style/colour, polo collar/colour) -> product tags or a metafield
  - card cutout -> the product's first image
  - best-selling and newest order (`BEST_RANK`, `NEWEST`) -> Shopify's own sort, nothing to maintain
- **In-grid feature tiles** (the Breezy move: a "Pairs well with" or "Layer
  up" tile dropped into the product grid) are theme-editor blocks on the
  collection section: pick an image, a line, a link and which position in
  the grid it sits at. Turning one off or adding one is a theme-editor change,
  not a code change.
- Tiles: as many as he wants per collection, each with an image, eyebrow,
  headline, optional link and button text, and "show after product #N".
  Each apparel line gets its own collection template (collection.polos,
  collection.hats, and later the winter line), so tiles added to Polos never
  appear on Hats. A new collection just picks a template in the admin.
