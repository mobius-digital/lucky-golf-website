# Moving the new site into Shopify: the plan

Written 2026-09-27 from a live check of the store (Admin API + the public site).
This is the runbook for the chat that does the move. Read it top to bottom
before touching anything. Companion files:

- `v9/PORT-NOTES.md`: rules the Liquid must keep (reviews at 10+, live stock,
  restock dates, templates not pages, hosted accounts).
- `v9/migration/url-inventory.txt`: every live URL on 2026-09-27 (111).
- `design/LUCKY-SYSTEM.md` + `shopify/assets/lucky.css` / `lucky.js`: the design system.
- The review board (every approved page): https://claude.ai/artifact/XW8JNBLSwuxLXS3ip2i7Lf
- Source for every page: `v9/src/*.html`, builders in `v9/tools/`.

## 0. Rules that never bend

1. **Never edit the live theme.** Build in a copy; publish the copy.
2. **No URL changes.** Product, collection, page and blog handles stay exactly
   as they are. A theme swap doesn't change URLs on Shopify; nothing we do
   during the move should either. Handle changes (like the Carver merge) happen
   on their own day, with 301s.
3. **Every tracking tool keeps firing.** Nothing ships until each one in
   section 3 is verified on the preview.
4. **Cole approves before publish.** He reviews the preview link; publishing
   is his yes, in a low-traffic hour.
5. **The old theme stays** as the one-click rollback for at least 30 days.
6. Report every step as: what happened, how Cole checks it, what he needs to supply.

## 1. What's live today (checked 2026-09-27)

**Theme:** `RIPPLE-FINAL-Version-Ride-V3.0-THEME [Checkout+]`
(`gid://shopify/OnlineStoreTheme/167760331029`), a Dawn-era theme.
Also on the store: four `[Fudge] Dev Theme` copies created 2026-09-27 00:05
(ask Cole what Fudge is doing before building; don't touch them).

**Page builders:** Replo builds the live home (page `home`, "Home - Cole") and
some landing pages; Zipify Pages renders through `header-scripts.zipifypages` /
`page-footer.zipifypages`; GemPages has an app embed (`embed-gp-script-head`).
Cole is handling Replo; the goal is to cancel it once the new theme is live.

**App embeds switched on in the live theme** (config/settings_data.json;
these are per theme, so each must be switched on in the new one):

| App | What it does here | In the new theme |
|---|---|---|
| Judge.me (core) | reviews data, widgets | ON. Our sections read `reviews.rating_count` / `reviews.rating`; the review list uses Judge.me's widget styled to match |
| Klaviyo (onsite) | forms, Active on Site, back-in-stock | ON. Our footer/blog signup forms post to Klaviyo |
| Triple Whale (pixel) | attribution | ON (app embed only, see section 3) |
| Gorgias | live chat bubble | ON ("Chat, bottom right of any page" is promised on the FAQ) |
| Loop Returns (return coverage) | CO+ offer in the cart | ON, and our cart drawer must show it (it lives inside UpCart today) |
| Notify Me | back-in-stock requests | ON unless Klaviyo back-in-stock replaces it; our "Tell me when it's back" must feed one of them |
| Ecomrise upsell bundle | upsells | ask Cole if still used |
| Essential Announcer | announcement bar | OFF: our announcement bar is a section |
| UpCart | cart drawer + $198 tier | OFF at launch: replaced by our drawer. Cancel after 7 clean days |
| Alia | customer app frame (popup) | ask Cole if still used |
| GemPages | page builder | only if a GemPages page is still live |

**Code pasted into `layout/theme.liquid`** (not app embeds; these do NOT carry over
unless we copy them):

- `{% render 'fudge-head-start' %}`: Fudge snippet. Ask Cole.
- `{% render 'replo-head' %}`: keep while any Replo page is live.
- **Two inline Triple Whale pixels** (v2.12 and v1.9.0) on top of the app
  embed: likely double counting. Ship the new theme with the app embed only,
  after confirming with Triple Whale support that the embed is the current method.
- Best Custom Product Options (`obscure-escarpment-2240.herokuapp.com`, bcpo):
  a product-options app. Check whether any live product uses it
  (`product.metafields.bcpo.bcpo_data`). If none, drop it.
- Zipify Pages header/footer renders: keep while any Zipify page is live.
- `gwp-guard.js` (the gift-with-purchase guard from the GWP campaign): carry
  over if a GWP is running at launch.
- A Judge.me color override (`.jdgm-rev-widg{color:white}`): drop, we style it.

**Web pixels (Settings > Customer events)** are theme-independent and survive the
swap on their own: Google & YouTube (GA4 `G-8DRJ99ES6W`, Ads `AW-790686614`),
Meta, Snapchat (Pinterest is not connected; Cole: leave it off). Verify them anyway (section 3).

**Redirects:** 20 exist (old wedge handles, Patriot putter, ambassador `/join/*`
links, a QR code). They're store-level and survive the swap. Don't delete any.

**URLs:** 43 products, 22 pages, 14 blog posts, 15 collections, home
(`v9/migration/url-inventory.txt`). Canonical host is `www.luckygolf.com`.

**SEO today:** home meta description is "Elegantly designed high performance
golf products" (generic). Product SEO titles and descriptions are mostly empty
(Shopify falls back to the product title and description). The home page
carries 2 JSON-LD blocks.

**Customer accounts** are Shopify-hosted (shopify.com/22863149/account). The theme
only links to them. Branding goes in Settings > Checkout > Customize (colors,
logo, font in PORT-NOTES).

## 2. Before building: the baseline (half a day)

So we can prove nothing got worse:

1. **SEO baseline:** crawl all 111 URLs and save for each: status, title, meta
   description, H1, canonical, JSON-LD types, word count →
   `v9/migration/seo-baseline.csv`. Ask Cole for a Search Console export
   (top 100 pages + top 200 queries, last 3 months) and add it.
2. **Tracking baseline:** with the live site, record which events each tool
   sees on: home view, product view, add to cart, begin checkout. Save as
   `v9/migration/pixel-baseline.md`.
3. **Speed baseline:** PageSpeed Insights (mobile) for home, Carver, Polos,
   a hat, the blog → `v9/migration/speed-baseline.md`.
4. **Conversion baseline:** last 30 days conversion rate, AOV, add-to-cart rate
   from Shopify analytics (or Triple Whale).

## 3. Tracking: what must fire, and how we check it

| Tool | Events | How to verify on the preview |
|---|---|---|
| GA4 + Google Ads | page_view, view_item, add_to_cart, begin_checkout, purchase | Tag Assistant on the preview link; Shopify Customer events > test |
| Meta | PageView, ViewContent, AddToCart, InitiateCheckout, Purchase | Meta Pixel Helper; Events Manager test events |
| Snapchat | page view, add to cart, checkout | its browser helper |
| Triple Whale | pageview, add to cart | Triple Whale pixel test; confirm only ONE pixel loads |
| Klaviyo | Active on Site, Viewed Product, Added to Cart | Klaviyo > Activity feed for a test profile |
| Judge.me | widgets render, review requests unchanged | view a product with 10+ reviews |

**The cart drawer is the risk.** Add-to-cart events come from Shopify's cart API.
Our drawer must add with `/cart/add.js` (or the Ajax Cart API / Section Rendering
API), never a custom endpoint, so Shopify publishes `product_added_to_cart` and
every web pixel sees it. Checkout events are unaffected: checkout isn't the theme.

## 4. Building the new theme

1. **Duplicate the live theme** in Online Store > Themes. Rename it
   "Lucky v4 (build, unpublished)". Duplicating keeps `settings_data.json`,
   which keeps the app embeds switched on.
2. **Replace the theme code** with ours, keeping from the old theme:
   `content_for_header`, the `<title>` / meta description logic, the canonical
   tag, the `meta-tags` snippet (Open Graph + Twitter cards), and each pasted
   snippet section 1 says to keep.
3. **Assets:** `lucky.css`, `lucky.js`, the contour SVGs, icons, Mags art.
   Photos go to Shopify Files and render with `image_url` (Shopify serves
   WebP/AVIF at the right width automatically).
4. **Sections, so everything is editable in the theme editor:** header +
   mega menu, announcement bar, footer (socials from theme settings), photo
   hero (+ short), photo band, split, trust row, club cards, reviews on a photo,
   review score + tiles, FAQ, sign-off, feature tile block, keep-browsing strip,
   compare table, community wall, product (club / polo / hat / gear templates),
   collection (with tile blocks), blog, article, cart page, 404, search,
   gift card. Each approved page on the board becomes a JSON template built
   from these.
5. **Metaobjects:** Community posts (media, @handle, link, products).
6. **Cart drawer:** our design, the $198 free-shipping bar (read the threshold
   from a theme setting), Loop return coverage, upsell if Ecomrise stays.
7. **Everything data-driven** per PORT-NOTES: stock, reviews at 10+, restock
   dates, tags true.

## 5. SEO in the new theme (built in, not added later)

- One H1 per page, headings in order.
- Title and meta description from the admin fields (fill the empty ones before
  launch: home, collections, the club products). Use the copy skill for them.
- Canonical on every page; `noindex` on the Replo `home` page once the theme
  home replaces it (or 301 it to `/`).
- JSON-LD: Organization + WebSite (with SearchAction) on home; Product with
  Offer (price, availability, currency) and AggregateRating from the Judge.me
  metafields (only at 10+, matching what's shown); BreadcrumbList; Article on
  blog posts; FAQPage where a page has an FAQ.
- Image alt text from the admin (write it where it's missing).
- Speed: lazy-load below the fold, preload the hero image, no layout shift,
  one CSS file and one JS file. Target: every page at least as fast as its baseline.
- `robots.txt` and the sitemap are Shopify's; don't override them.

## 6. Test on the preview link (before Cole's review)

- Every page on the board, at 1440, 834 and 390: renders, no sideways
  scroll, no console errors, tap targets 40px+.
- Buy every kind of thing: a wedge (loft + hand), a putter, the Stryker, a polo
  (size), a hat, a grip, a gift card (to someone, on a date). Place one real
  order with a 100% discount code made for the test, then cancel/refund it.
- Discounts, the free-shipping bar at $198, GWP if live, gift card redemption.
- Sold-out variant: "Tell me when it's back" reaches Notify Me or Klaviyo.
- Judge.me: stars only at 10+, pooled polos/hats.
- Search, 404, every redirect in the list still redirects.
- Tracking: every row in section 3.
- SEO: re-crawl the 111 URLs on the preview; titles, descriptions, canonicals,
  H1s and JSON-LD at least as good as the baseline.

## 7. Launch day

1. Pick the quietest hour from Shopify analytics (usually weekday late night).
2. Cole publishes the new theme (Online Store > Themes > Publish).
3. First 15 minutes: home, a product, add to cart, checkout page loads,
   tracking in real time (GA4 Realtime, Meta test events, Triple Whale live).
4. First hour: a real order from the team.
5. **Rollback:** if checkout, tracking or add to cart breaks, publish the old
   theme (one click), then fix on the copy.
6. Don't change anything else on launch day: no product merges, no handle
   changes, no app removals.

## 8. After launch

- **Day 1:** Search Console > Pages for new 404s; add 301s for any.
- **Day 7:** tracking compared with the baseline; conversion rate and AOV compared
  with the 30-day baseline. If clean: turn off UpCart and cancel it.
- **Separate day (Carver merge):** merge Carver 02 Gold + Black into one product
  with a Finish option, 301 the old Black handle to the merged product, move
  its Judge.me reviews, archive the old LGW01/LGW02 drafts.
- **Replo / Zipify / GemPages:** once every page they own is rebuilt or
  retired (301 to the closest page), remove their snippets and cancel them.
- **Day 30:** speed, rankings and conversion compared with the baselines, then
  the full SEO audit (keywords, content, internal links, the blog).

## 9. Cole's answers (2026-09-27)

- **Fudge:** Fudge Agent, a landing page / AI theme app Cole installed. The four
  `[Fudge] Dev Theme` copies are its. Leave them; ask before removing the snippet.
- **Ecomrise:** it's installed as "Nitro Upsell & Cross Sell" and was active yesterday. Keep its embed until Cole decides on its upsells.
- **Alia:** yes, email popups. Keep its app embed on.
- **GemPages:** no. **Best Custom Product Options:** no (not installed): drop its code.
- **Back in stock + pre-order:** built into the theme (Klaviyo back in stock + a pre-order switch with Shopify Flow), replacing Notify Me. Move Notify Me's waitlist into Klaviyo before cancelling. PORT-NOTES "Sold out, back in stock and pre-order".
- **Rivo (loyalty + referrals):** starting now. Switch on its app embed in the new theme and give it a spot (footer link + a rewards page); remember accounts are Shopify-hosted.
- **Zipify:** no (not installed): drop its renders. **Replo:** in use until the new site is live.
- **Search Console:** baseline read 2026-09-27 from Cole's second Chrome: `v9/migration/seo-baseline-gsc.md`. **LGD01's page (/products/lucky-gold-driver-pre-order_) gets 12k impressions: 301 it to Havoc before it's drafted.**
- **GWP at launch:** no (it ended Sept 25). Drop `gwp-guard.js` from the new theme.
- **Pinterest:** not connected (no app, nothing fires; Takomo doesn't have it either). Cole: leave it off.
- **Apps:** full audit in `v9/migration/APP-AUDIT.md`. Cancel the replaced ones after launch; Cole answers the "ask" list.

## 9b. The original questions

1. What is Fudge (the `fudge-head-start` snippet and the four dev themes)?
2. Are Ecomrise upsells, Alia, GemPages and the product-options app still in use?
3. Back in stock: Notify Me or Klaviyo?
4. Is a GWP running at launch?
5. Which Replo/Zipify landing pages must stay live after launch?
6. A Search Console export (or access) for the baseline.

## 10. Progress log

**2026-09-27 (move chat, day 1)**
- Section 2 baselines saved in `v9/migration/`: `seo-baseline.csv` + `seo-baseline.md`
  (97 unique URLs; tools `v9/tools/seo_crawl.py`), `pixel-baseline.md`,
  `conversion-baseline.md`. Speed NOT yet captured: Google's free PageSpeed API hit its daily limit;
  re-run `python v9/tools/speed_check.py` tomorrow (writes `speed-baseline.json`).
- Found: Google + Meta + Snapchat are web pixels (survive the swap). Triple Whale
  loads THREE times today (two inline copies in theme.liquid + the app embed).
  Pinterest fires nothing on the storefront.
- **Build theme created:** "Lucky v4 (build, unpublished)",
  `gid://shopify/OnlineStoreTheme/171555127573`, duplicated from the live theme
  via Admin API `themeDuplicate`. theme.liquid, settings_data.json (app embeds)
  and every template are byte-identical to live. Live theme untouched.
  Preview: https://www.luckygolf.com/?preview_theme_id=171555127573
- Next: section 4 step 2, replace the code in the build theme (never the live one).

**2026-09-27 (move chat, build started)**
- Theme source now lives in `theme/` (built by `tools/theme/`: `build_sections.py`, `build_templates.py`,
  `build_css.py`, `gen_snippets.py`; `compare.py` screenshots approved vs Shopify side by side).
  Pushed to the build theme through staged uploads + `themeFilesUpsert` (connector only writes unpublished themes).
- 119 site photos + Mags uploaded to Content > Files as `lg-*.webp`; every photo is a theme-editor picker.
- New layout (`theme.liquid`: one Triple Whale via the embed, JSON-LD, our bag) + `theme.legacy.liquid`
  (old Ride layout minus the 2 inline TW pixels, bcpo, Zipify, GWP guard). Every old JSON template
  now points at the legacy layout, so pages not rebuilt yet look as they do today.
- Built: header + mega menu, announcement bar, footer (menus `lucky-footer-*`, `lucky-phone-footer`),
  real cart drawer (`/cart/add.js`), Home. Home matches the approved page at 1440 and 390.
- Product metafield `custom.cutout` (Card cutout) created and set on the 5 clubs.
- App embeds in the build theme: UpCart, Essential Announcer, Ecomrise, GemPages OFF; rest unchanged.
- **Blocked:** `templates/index.liquid` (Replo home) must be deleted in the build theme before
  `index.json` can go in; the connector refuses file deletes. Home previews at
  `/pages/about?view=lucky-home` until then.
- Open: Loop return coverage was auto-added by UpCart; with UpCart off nothing adds it yet.

**2026-09-27 (evening): every page built on the build theme**
- Built in four groups (rules: `theme/BUILD-NOTES.md`): clubs (`product.club`, one template for all 5,
  copy/photos in `custom.club_*` metafields), apparel + collections (`collection.json/.polos/.hats/.gear/.clubs`,
  `product.polo/.hat/.gear`), content (`page.story/.faq/.ambassadors/.compare/.contact/.community/.reviews`,
  `404`, `search`), commerce (`cart`, `product.giftcard`, `gift_card.liquid`, `blog`, `article`).
- Sweep: all 27 page views return 200 (404 returns 404), no Liquid errors, exactly one H1 each.
- Home: fixed sections in `templates/index.liquid` (settings in settings_data) because Replo's index.liquid
  can't be deleted by the connector; renders at `/` on the preview.
- New data (none visible on the live theme): metafields custom.cutout, club_page/club_photos/..., restock_date,
  sold_out_mode, model_sizing, color_family, filter_style, gallery, detail_photo, facts; article lucky.*;
  metaobject community_post (11 posts); menus lucky-footer-*; smart collection /collections/gear (published).
- Package protection = Loop Checkout+, attached to the bag's `name="checkout"` button (verified: shows $4.19 on a $29 bag).
- App embeds on the build theme: UpCart, Essential Announcer, Ecomrise, GemPages, Notify Me OFF.
- Launch-day steps: `tools/theme/launch_day.py` (template switches + 2 new pages), `publish_articles.py`,
  `publish_product_copy.py` (all dry-run; payloads in v9/migration/). Take a snapshot of current template
  suffixes before running (rollback).
- Still before launch: tracking check on the preview incl. Meta test events; SEO re-crawl of the preview;
  speed baseline (PageSpeed quota); Judge.me product groups for pooled polo/hat reviews; restock dates
  (Carver says "sold out" where the board said "back next month").

**2026-09-27 (night): look fixes + pre-launch checks**
- Design system: tile is warm grey `#F4F2EE` (was cream); no filled boxes behind text (reviews, panels, stats,
  specs, table heads sit on a hairline); no gold type/stars on the green (off-white; gold = the foil button only).
- Copy: Carver price captions removed ("never say a loft costs the same"); polo spec "Same price" -> "Sizes";
  home hero restored to Cole's "Get used to the attention" (the Sept 24 copy pass had swapped it); sign-off "Bag it."
  Cole will run a separate copy review of every page.
- `/collections` (list-collections) moved to the new layout. Page titles no longer carry a line break.
- Rollback snapshot: `v9/migration/live-templates.json` (every current template suffix).
- SEO check of the preview (95 baseline URLs, with each page's launch template): all 200 except the
  2 new pages (created on launch day); one H1 on every rebuilt page; canonicals unchanged; titles and
  descriptions match live (empty descriptions on the collections + reviews are empty live too: copy review).
  `/pages/fathers-day-bag` has a Liquid error on live too (old Replo page, missing image).
- Tracking on the preview (Carver PDP + add to cart): GA4 page_view + view_item (live sends only page_view),
  Google Ads conversion tags, Snapchat, Triple Whale ONCE (live 3x), Klaviyo, Judge.me, Gorgias. Meta loads
  fbevents + config exactly as live does; confirm in Meta Events Manager > Test events on launch day.
- Judge.me: ~0 photo reviews out of 1,555 (Takomo's photo strip is Judge.me's own widget). Cole approved photo
  requests; needs an admin login in the in-app browser to switch on.
- Speed baseline: Google PageSpeed still returns 429 (keyless daily quota) on 2026-09-27 night. Retry tomorrow, or use an API key.
- Copy review export: `python tools/theme/copy_pdf.py` -> `v9/review-pdfs/Lucky-site-copy.pdf` (+ .md), every page
  on its launch template, product descriptions from the launch payloads, blog rewrites. Found and cut 4 more
  price-parity lines (FAQ apparel heading + subline, polos trust item, Our Story hats line).
- FOUND: dead URLs getting paid traffic on the LIVE site now (90 days): /collections/stock-wedges 4,823 sessions
  (Facebook campaigns 120244398434110221 + 120244156505820221, Klaviyo welcome + cart-abandon flows),
  /collections/putters 1,062, /products/lucky-gold-driver-pre-order_ 342; all 404. Redirects proposed to Cole.
- Cole approved the cleanup (2026-09-27). DONE on the live store: 21 old promo/duplicate pages hidden (not deleted)
  + 29 redirects (incl. the dead ad/email URLs stock-wedges, putters, driver pre-order); free hat/polo gift products
  archived. Verified live: each old URL now lands on its target. NOT done: /collections/summer-warehouse-sale
  (connector can't unpublish collections; ~4 visits, harmless). LAUNCH NIGHT: hide /pages/home (Replo copy of the
  old home) and redirect it to /. The ad team should still swap the ad links to the real URLs.
