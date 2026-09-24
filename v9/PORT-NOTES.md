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
