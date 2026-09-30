# Launch night (updated 2026-09-29)

Everything below the theme is already built and checked on
"Lucky v4 (build, unpublished)" (`171555127573`). Some things are store data the
live site reads too (template choices, product descriptions, blog posts, SEO
fields), so they switch in the minutes right after the theme is published, not before.

## Cole
1. Review the preview on your phone and laptop: https://www.luckygolf.com/?preview_theme_id=171555127573
2. Pick a quiet hour (weekday late night).
3. Online Store > Themes > "Lucky v4 (build, unpublished)" > Publish.
4. Tell the chat "it's live".
5. Online Store > Preferences > Home page meta description (the API can't set it):
   "Forged wedges, milled putters and a titanium hybrid, built to big-name standards, finished in gold and sold direct. Sixty days to try any club."

## The chat, straight after (about 15 minutes, in this order)
1. Template switches: `01-products.json`, `02-collections.json`, `03-pages.json` (run `python tools/theme/launch_day.py` for the plan).
2. Publish the two new pages (already created hidden on 2026-09-29):
   `pageUpdate` isPublished true on `gid://shopify/Page/141815873813` (compare) and `gid://shopify/Page/141815906581` (community). Skip 04-new-pages.json: they exist.
3. Blog: `python tools/theme/publish_articles.py`, then send `v9/migration/articles-publish/*.json`.
4. Product descriptions (polos, hats, glove, grips, covers): `python tools/theme/publish_product_copy.py`, then send `v9/migration/product-copy/*.json`.
5. SEO fields: send the mutation in `05-seo.json` (5 clubs + 4 collections).
6. Hide `/pages/home` (the Replo copy of the old home) and add a 301 from `/pages/home` to `/`.
7. Check: home, a club, add to cart, checkout loads; GA4 Realtime, Meta Events Manager test events, Triple Whale live (fires once).
8. Re-crawl: `python v9/tools/seo_crawl.py --out v9/migration/seo-after.csv` and compare with `seo-baseline.csv`.

## Rollback
Publish the old theme ("RIPPLE-FINAL-Version-Ride-V3.0-THEME [Checkout+]"), then put the
template suffixes back from `v9/migration/live-templates.json`. Keep the old theme 30 days.

## Not blocking launch (do in week 1)
- Speed baseline (Google PageSpeed quota was hit on 2026-09-27).
- Judge.me: product groups so polos and hats pool their reviews; switch on photo review requests.
- Restock dates on sold-out variants.
- Ad team: point the Facebook ads at the real URLs (redirects cover them for now).
- Apps: see the cancel list (after 7 clean days for UpCart).
