# Tracking baseline (live site, 2026-09-27)

Checked in the in-app browser on www.luckygolf.com (live theme), plus Meta's own
event counts. Re-run the same checks on the preview before Cole's review.

## Where each tool comes from (decides whether a theme swap can break it)

| Tool | Loaded by | Survives a theme swap on its own? |
|---|---|---|
| GA4 `G-8DRJ99ES6W` + Google Ads `AW-790686614` (+ `GT-NS9R3SW`) | Google & YouTube web pixel (Customer events), runs in the top frame | Yes |
| Meta pixel `2196329423966853` | Meta web pixel (Customer events), top frame | Yes |
| Snapchat | web pixel | Yes |
| Pinterest | not installed (no app, nothing fires). Cole 2026-09-27: leave it off | n/a |
| Triple Whale | **three copies:** inline v2.12 + inline v1.9.0 pasted in `theme.liquid`, plus the app embed v2.16 | App embed only carries over (duplicate keeps it). The two inline copies are the double counting; the new theme leaves them out |
| Klaviyo onsite (forms, Active on Site) | app embed | Carries over with the duplicate |
| Alia (popup) | app embed | Carries over |
| Gorgias chat | app embed | Carries over |
| Judge.me | app embed + widgets (tracking.aws.judge.me fired on the hat page) | Embed carries; our sections must render its widgets |
| UpCart | app embed; fires its own journey events and auto-adds Loop's "free-returns-package-protection" via `cart/update.js` | Turned OFF in the new theme; our drawer must add return coverage itself |
| Afterpay messaging | script on every page | Carries (decision pending in APP-AUDIT) |
| AvantLink, Parcel Panel | web pixels | Yes |

## What fired, by step (live)

| Step | Seen |
|---|---|
| Home view | GA4 page_view, Ads page_view/conversion, Meta PageView (fbevents + config loaded), Snapchat page, Triple Whale event ×3 pixels, Klaviyo onsite, Alia, Gorgias |
| Product view (White & Gold Classic Hat) | GA4 `page_view` + `view_item`, Ads `page_view`, Snapchat `/p`, Triple Whale event ×2, Judge.me track event |
| Add to cart (via `/cart/add.js`) | GA4 `add_to_cart`, Ads `add_to_cart` conversion + view-through, Triple Whale event, UpCart trackEvent, Shopify `fec/produce`. Shopify publishes `product_added_to_cart` from `/cart/add.js`, so our drawer must add the same way |
| Begin checkout | Checkout loads (Shopify-hosted, not the theme). Checkout pixels run sandboxed; verify in each tool's test view |

Test cart was emptied afterwards (`/cart/clear`).

## Meta's own counts (Events Manager, 2026-09-03 to 09-27, ~24.5 days, browser + server)

| Event | Count | Per day |
|---|---|---|
| PageView | 134,298 | ~5,480 |
| ViewContent | 74,220 | ~3,030 |
| AddToCart | 4,247 | ~173 |
| InitiateCheckout | 1,171 | ~48 |
| Purchase | 463 | ~19 |
| Search | 370 | ~15 |
| AddPaymentInfo | 237 | ~10 |

Day-7 check after launch: AddToCart per day and the AddToCart : ViewContent ratio (5.7%) should hold.

## Not captured here (needs Cole or a tool that works)

- Triple Whale: checked on the preview by us (one pixel, events arriving), not by Cole.
- Klaviyo Viewed Product / Added to Cart only fire for identified profiles; check the Activity feed of a test profile on the preview.
