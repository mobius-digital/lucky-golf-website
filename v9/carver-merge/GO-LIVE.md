# Carver 02: one product, Gold + Black (2026-10-08)

Preview theme: **Lucky v4.3 (Carver one product + buy box)**, id `171694391573`
(a copy of v4.2, so it carries the putter work too).
Preview: https://www.luckygolf.com/products/lucky-golf-lgw02-gold?preview_theme_id=171694391573

## Already done (live store, safe before the theme switch)

- Product `9583978905877` renamed **Carver 02**; new option **Finish** at position 3 (Gold on the 18 old variants).
- 6 Black variants added: Right Hand × 50–60° K, $109, the **same SKUs** (LGW03-BLK-STOCK-RH-50/52,
  LGW02-BLK-STOCK-RH-54..60), stocked at Ceries OMS with **0** so nothing can double-sell yet.
- Black's 7 photos copied onto Carver 02; the Black variants point at the black cutout.
- Product metafields **Badge** (`custom.badge`) and **Badge in gold foil** (`custom.badge_foil`) created.
- The live v4.1 page still sells Gold exactly as before (it finds variants by Hand + Loft and Gold comes first).

## What's in v4.3

- Buy box: finish cards (Signature Gold / Black +$10, "New" on Black), Right/Left always shown,
  tap lofts to build a set (max 3), bounce on every loft, no How Many, no Your Set table, no FORGED 1020 tag.
- Finish names, tags, photos and the line under the price: Theme editor > Carver page > Club: buy box > Finish blocks.
- Black cards everywhere (home, menu, finder, Clubs page, compare page, collections list) now point at
  Carver 02 with `?finish=Black`, show $109 and the black photo.
- Black taken out of the review totals (it double-counted the shared 663: home said 1,558, real is 895).
- Gallery shows "1 / 21" instead of 21 dots on phones.

## Go-live, in this order, right after v4.3 is published

1. Read the old Black variants' `available` at Ceries OMS (98054963477), per SKU.
2. Set those numbers on the new Black variants (inventorySetQuantities, name `available`).
3. Old Black product `9574093717781` -> **DRAFT** (not delete; keeps its orders).
4. Redirect `/products/lucky-golf-lgw02-black` -> `/products/lucky-golf-lgw02-gold?finish=Black`
   (Shopify only follows it once the old page is gone, which step 3 does).
5. SEO title `Carver 02 Gold Forged Wedge | Lucky Golf` -> `Carver 02 Forged Wedge | Lucky Golf`.
6. Check: preview link loads Black with stock, adds to cart; old Black URL lands on Black.

Rollback: republish v4.1 (171617943829), set old Black back to ACTIVE, delete the redirect,
zero the new Black variants. Nothing else needs undoing.

## Not changed on purpose

- BOGO page: it bakes in Gold variant ids, and those ids did not change. No rebuild needed.
- `sections/home-group.json` is edited locally but not used by any page, so it was not uploaded.
- SKUs: untouched (Cole, 2026-10-08).

## DONE 2026-10-08 (Cole published v4.3, now MAIN)

1. Old Black `9574093717781` -> DRAFT first (so it couldn't sell during the copy).
2. Its Ceries OMS available copied to the new Black variants: 50° 84, 52° 41, 54° 46, 56° 203, 58° 57, 60° 182 (613).
3. Redirect `/products/lucky-golf-lgw02-black` -> `/products/lucky-golf-lgw02-gold?finish=Black` (301, verified).
4. SEO title -> `Carver 02 Forged Wedge | Lucky Golf`.
5. Verified live: redirect lands on Black, $109, 56° picked; /cart/add.js added the Black 56° K at $109 (removed after).

Still open: the Black card name. The connector can't write the live theme, so the name changes in
Theme editor > Products > Carver page > Club: buy box > "Black" finish block > Name.
