# Building the Lucky theme: rules for every builder (read all of it first)

We are porting the approved v9 site (the review board) into a Shopify theme. The live store
must not change. Cole approved every page on the board; the theme must reproduce each page
faithfully, as editable Shopify sections, with live product data.

## Where things are

- Approved pages (the spec): `v9/src/<page>.html` (templates with `{{TOKENS}}`) and the built
  result `v9/out/after/<page>.html` (open these to see the real finished markup/copy).
  Builders that fill tokens: `v9/tools/build.py` (+ `build_club.py`, `build_wedge.py`, `build_simple.py`).
  Page CSS lives in each page's `<style>` block; shared CSS in `v9/src/site.css` + `shopify/assets/lucky.css`.
- Rules the Liquid must keep: `v9/PORT-NOTES.md` (reviews only at 10+ by count, pooled polos/hats,
  live stock, restock dates, templates not pages, hosted accounts, sold-out/notify/pre-order). READ IT.
- Design system: `design/LUCKY-SYSTEM.md`, `shopify/assets/lucky.css` (all `lg-` classes).
- Theme source: `theme/` (layout, sections, snippets, templates, assets, config). Generated:
  - sections from `tools/theme/sections_*.py` (dict `S`, helpers in `tools/theme/common.py`) via `python tools/theme/build_sections.py <yourgroup>` (always pass your group name, e.g. `club`, so you only build your own files)
  - JSON templates from `tools/theme/templates_*.py` (dict `T`) via `python tools/theme/build_templates.py <yourgroup>`
  - `theme/assets/lucky-site.css` via `python tools/theme/build_css.py` (concatenates `theme/css/*.css`)
  - Hand-written Liquid is fine for snippets (`theme/snippets/`) and for sections too big for a spec
    (see `tools/theme/wild.liquid` loaded by `sections_home.py`).
- Existing building blocks (reuse, don't duplicate): snippets `lg-card` (small product card), `lg-bigcard`
  (Takomo-style big card), `lg-h` (heading; italic words become the gold foil word), `lg-sec-head`,
  `lg-stars`, `lg-mags`, `lg-icon` (name: star, badge-check, truck, credit-card, rotate-ccw, shield-check,
  package, hammer, anvil, tag, hand-coins, message-circle, mail, map-pin, send, search, shopping-bag,
  circle-help, instagram, tiktok, youtube), `lg-jsonld`. Sections: lg-hero, lg-trust, lg-cards, lg-split,
  lg-claims, lg-finder, lg-pband, lg-reviews-band, lg-gtiles, lg-wild (community posts), lg-callout, lg-signoff.
- The bag: `window.LuckyBag.add([{id, quantity, properties}])`, or any `<form data-lg-add>` with
  `name="id"` (+ `properties[...]`) adds through Shopify's `/cart/add.js` and opens the drawer.
  Back in stock: `<form data-notify data-variant="{{ variant.id }}">` with an email input (Klaviyo).
  Never build a custom cart endpoint (tracking depends on `/cart/add.js`).

## Hard rules

1. **Never touch the live theme** or product/collection/page handles, prices, or product data.
   The only theme you write is **`gid://shopify/OnlineStoreTheme/171555127573`** ("Lucky v4 (build, unpublished)").
   You may create NEW metafield definitions / metaobjects if a page needs data (say so in your report).
2. Everything a merchant would change is a **section setting or block** (text, photos via `image_picker`,
   products via `product`/`product_list`, collections). Photos already uploaded to Content > Files are
   referenced in JSON templates as `"shopify://shop_images/lg-<name>.webp"` where `<name>` is the file in
   `v9/out/after/img/` (e.g. `lg-two-gold-wedges.webp`). Product media with hash names are on the product itself.
3. **Live data only**: price (`money_without_trailing_zeros`), availability, variants, reviews from
   `product.metafields.reviews.rating_count/rating` (show stars/sections ONLY at `settings.lg_review_min`, 10).
   Card cutout image: `product.metafields.custom.cutout.value` (set on the 5 clubs; fall back to featured_image).
4. **Copy is approved: copy it verbatim** from the v9 page. No em dashes, no exclamation marks, no invented
   numbers, no fabricated reviews (Judge.me verbatim or the Judge.me widget), no competitor names.
5. **Look**: Takomo-tight corners (tokens `--lg-r-card` 8px, `--lg-r-btn` 6px; never hard-code 12-18px radii),
   Archivo only, gold is the only accent, at most one gold foil button per screen, tags are flat
   (no pill "chips" floating on photos). Match the approved page's layout at 1440 / 834 / 390.
6. Section schema `name` ≤ 25 characters (longer names make Shopify silently reject the file).
   `product_list` values: loop them, `.first` comes back blank. Avoid filters inside named arguments.
7. Page CSS goes in **your own** `theme/css/<NN>-<group>.css` (NN = your number below), scoped so it can't
   leak: prefix with the template body class (`body.lg-t-<template suffix>`; e.g. `.lg-t-club`) or a unique
   section class. `from build_css import scope_css` (in tools/theme) can prefix a whole stylesheet for you.
   Page JS: inline `<script>` in your section (vanilla, no libraries), or `{% javascript %}`.
8. Don't edit files owned by another group. Shared files (`lucky-site.js`, `lucky.css`, `theme.liquid`,
   `lg-header`, `lg-footer`, `settings_*`) belong to the lead: ask in your report instead of editing.

## Templates and previewing

Template names (the lead switches products/pages onto them on launch day; until then preview with `?view=`):
- products: `product.club`, `product.polo`, `product.hat`, `product.gear`, `product.giftcard`
- collections: `collection.json` (default), `collection.polos`, `collection.hats`, `collection.clubs`, `collection.gear`
- pages: `page.story`, `page.faq`, `page.ambassadors`, `page.compare`, `page.contact`, `page.community`,
  `page.reviews`; plus `404.json`, `search.json`, `cart.json`, `blog.json`, `article.json`, `gift_card.liquid`
- Preview: `https://www.luckygolf.com/<path>?preview_theme_id=171555127573&view=<suffix>`
  e.g. `/products/lucky-golf-lgw02-gold?preview_theme_id=171555127573&view=club`
- JSON templates for alternates must set `"layout": "theme"` implicitly (omit the key).
- Check side by side: `python tools/theme/compare.py <v9 page name without .html> "<path with ?view=...>"`
  (headless Chrome; writes `_ref/compare/<page>-1440-N.png`; `--w 390` for phone). Iterate until it matches.

## Pushing to the build theme (Shopify Admin connector tools)

1. `python tools/theme/stage_input.py theme <path> [<path>...]` prints `stagedUploadsCreate` input.
2. Call `graphql_mutation` `stagedUploadsCreate(input:$input){stagedTargets{url resourceUrl parameters{name value}}}`.
   Tip: include `parameters{name value}` and ask for many files at once so the result is saved to a
   tool-results FILE instead of flooding your context.
3. `python tools/shopify_stage_put.py <that result file> theme` PUTs the files.
4. `graphql_mutation` `themeFilesUpsert(themeId:"gid://shopify/OnlineStoreTheme/171555127573", files:[{filename, body:{type:URL, value:<resourceUrl>}}])` (max 50 files).
5. **Verify every file** with `theme{files(filenames:[...]){nodes{filename checksumMd5}}}` against local
   `md5sum`. A Liquid/schema error drops the file SILENTLY (userErrors stays empty). Missing = broken.
   Staged URLs stay valid 7 days: re-PUT changed files with `python tools/theme/reput.py <result file> theme <paths>`.
6. If you rebuilt `lucky-site.css`, push it too (every group's css is inside it).

## Report back

What you built (files), what matches, what doesn't yet and why, any data you created, any question for Cole.
