# App audit (2026-09-27)

48 apps are installed (Shopify Admin API). The API won't show what each one
costs: prices are in Shopify admin > Settings > Billing > Subscriptions.
Cole's answers from 2026-09-27 are marked.

## Keep: the store runs on these

| App | Why |
|---|---|
| Judge.me Reviews | every review on the site |
| Klaviyo | email, SMS, signup forms, back in stock (Cole: "we use Klaviyo") |
| TripleWhale | attribution |
| Gorgias | chat and helpdesk (the FAQ promises chat) |
| Loop Returns & Exchanges | returns portal + return coverage in the cart |
| Alia | email popups (Cole: yes, in use) |
| Avalara TrustFile + Extractor for Avalara | sales tax |
| QuickBooks Online | accounting |
| Flow, Messaging, Collabs, Marketplace Connect, Order Printer (legacy) | Shopify's own apps, free |

## Cancel after the new site is live

| App | Replaced by |
|---|---|
| Upcart Cart Drawer | our cart drawer (after 7 clean days) |
| Replo Landing Page Builder | the new theme (Cole: "that'll go away once we do this") |
| GemPages Builder | nothing uses it (Cole: no) |
| Essential Announcer | our announcement bar section |
| Notify Me! | Klaviyo back in stock (one fewer app) |

## Ask Cole: in use, or leftover?

| App | What it is | Question |
|---|---|---|
| ShipBob Fulfillment + ShipStation | two fulfillment/shipping tools | which one ships orders? |
| CWILL (Parcel Panel) | order tracking page | still used for tracking? |
| Nitro Upsell & Cross Sell | upsells | still used? |
| Stock Guard | overselling protection | still used? |
| Rivo Loyalty Rewards Referrals | points + referrals | still used? (the site has no points program anywhere) |
| AvantLink Affiliate Marketing | affiliate network | still running? |
| Kickfurther Growth | inventory financing | still active? |
| Amazon MCF and Buy with Prime | Amazon fulfillment / Prime button | still used? |
| Afterpay On-Site Messaging | pay-later messaging | is Afterpay on at checkout? |
| PostPilot | postcards | still sending? |
| Adveronix | ad reporting to sheets | still used? |
| Ryze AI | ad management | still used? |
| Vibe | streaming TV ads | still running? |
| Air | creative asset library | still used? |
| Trybe UGC | creator content | still used, or replaced by Lucky Creators? |
| Fudge Agent | landing page / AI theme editor (Cole: he installed it) | made four dev themes on 2026-09-27; keep or remove? |
| Lovable | AI app builder | still used? |

## Ours (custom apps, free): leave alone

Lucky Wedges, Creator Hub Integration, Ceries OMS, Inventory Sheet, Viktor - Lucky Golf,
Mobius Supply, Lucky Creators, Lucky Golf Showroom, Lucky Golf Ledger,
Shopify Claude Connector App, Shopify ChatGPT MCP App.

## Leftover code with no app behind it (strip in the new theme)

- Ecomrise upsell bundle: app embed still in the theme, app not installed.
- Best Custom Product Options (bcpo): scripts in theme.liquid, app not installed.
- Zipify Pages: renders in theme.liquid, app not installed (Cole: no).

## Decisions and findings (Cole + live check, 2026-09-27)

| App | Decision |
|---|---|
| Notify Me! | **REPLACE with our own** (Cole: why pay $20/mo). New theme does back in stock through Klaviyo and pre-order through a product switch + Shopify Flow (PORT-NOTES). Export its pending waitlist into Klaviyo first, then cancel. Until then note its Klaviyo integration is OFF (`has_contact_integration: false`). |
| ShipBob | not used: uninstall |
| Stock Guard | Cole's old custom app, not used: uninstall |
| Nitro Upsell | not used: uninstall |
| Parcel Panel | ACTIVE: tracking page at /apps/parcelpanel + a web pixel. Keep until we check where shipping emails link; decide after launch |
| Rivo | starting now: keep; new theme needs its app embed + a rewards spot (see MIGRATION-PLAN) |
| AvantLink | ACTIVE web pixel (merchant 1031441). Third-party affiliate network (publishers, deal sites), not the creator program. Keep only if its dashboard shows sales in the last 90 days |
| Kickfurther | keep (financing, not the site) |
| Amazon MCF + Buy with Prime | not used: uninstall (needs inventory at Amazon; revisit only if selling on Amazon) |
| Afterpay On-Site Messaging | its "pay in 4" widget loads on product pages. Check Settings > Payments: if Afterpay isn't a payment method, uninstall (it's advertising something checkout doesn't offer) |
| PostPilot | starting: keep |
| Adveronix | sends ad data into Google Sheets for reporting. Cancel unless someone's report sheet feeds from it |
| Ryze AI | not used: uninstall |
| Vibe, Air, Trybe UGC | in use: keep |
| Lovable | AI landing pages: cancel after the new site is live |


## Checked in Shopify admin before uninstalling (2026-09-27)

Cole approved uninstalling ShipBob, Stock Guard, Nitro, Amazon Buy with Prime and Ryze.
Each app's page showed what it's actually doing, so nothing was uninstalled:

| App | What the admin shows | Call |
|---|---|---|
| ShipBob | edited ORDERS 19 minutes before the check | may be shipping orders: don't uninstall until Cole confirms who fulfills |
| Amazon MCF + Buy with Prime | read products and orders yesterday; pixel connected | may be fulfilling some orders: confirm first |
| Nitro Upsell & Cross Sell | this IS Ecomrise (app proxy /apps/ecomrise); changed the online store yesterday | active: not a leftover. Decide if its upsells stay |
| Ryze AI | SEO app installed 6 days ago; edited products 4 days ago and the online store 6 days ago | someone is using it: ask before removing (it may have rewritten SEO titles) |
| Stock Guard | no activity in 30 days, no billing | safe to uninstall |

Uninstalling deletes the app's data, so Cole clicks Uninstall himself.

Prices seen on the Apps page: Upcart $29.99 / 30 days + usage, Judge.me $15 / 30 days.
Shopify bills (apps + fees) ran $204 to $556 a month in 2026.

Admin alerts seen: "register and collect sales tax in 3 US states" (every two weeks
since July) and "There's an issue with TikTok" (the TikTok channel, Aug 24).

## Cole, 2026-09-27 (after the checks)

- ShipBob: left long ago, a new 3PL ships now. Remove. Amazon MCF: fulfills nothing. Remove.
  Nitro (Ecomrise), Ryze, Stock Guard: remove. Cole clicks Uninstall (it deletes app data).
- Ryze wrote no SEO titles/descriptions: every product's SEO fields are still empty.
- Gift cards now expire after 5 years (set in Settings > Payments > Gift card expiration, 2026-09-27), matching Takomo and the site copy.

## Uninstalled 2026-09-27 (Cole's go-ahead, done in admin)

- Stock Guard, Ryze AI, Nitro Upsell & Cross Sell (Ecomrise), Amazon MCF and Buy with Prime: uninstalled, each confirmed by Shopify's "successfully uninstalled" banner.
- Amazon's own location ("Amazon Fulfillment") held 1 item at 0 stock, so "delete inventory stored at this location" changed nothing.
- ShipBob: UNINSTALLED later the same day (Cole: nothing is at ShipBob). Its location "ShipBobFulfillment-205688" still records on hand (0 available):
  LGW01-50-RH 7, LGW01-52-RH 3, LGW01-54-RH 1, LGW01-56-RH 2, LGW01-58-RH 1, LGW01-60-RH 1,
  LGW02-52-RH 1, LGW02-56-RH 1, LGW02-52-LH 1, LGW02-56-LH 3, LGW02-60-LH 3, LGD01-Right 1 (25 wedges + 1 driver).
  All 26 were 'committed' but no open order was assigned to ShipBob (stale). The uninstall only offered transfer, so they went to a NEW location, "ShipBobFulfillment-205688 (app uninstalled)", which does not fulfill online orders (Ceries stock untouched). It can be deactivated any time.
- The Nitro/Ecomrise app embed and the Amazon pixel are gone from the live theme with the apps; nothing else to strip for them in the move.

## After launch (2026-10-02)

- Afterpay: last Afterpay order was #27169 on 2025-02-07; every order since Aug 2026 is shopify_payments.
  Afterpay isn't at checkout, so the On-Site Messaging app advertises something you can't pick: uninstall.
- Remove now (Cole: "do everything"): GemPages, Essential Announcer, Lovable, Fudge Agent, Adveronix,
  Afterpay On-Site Messaging, AvantLink (Cole: the creator program replaces it; also close the AvantLink
  account itself so it stops billing).
- Later: Upcart (Oct 9), Notify Me (after the waitlist is in Klaviyo), Replo (early Nov, rollback theme uses it).

## Done 2026-10-02 (Cole: "do everything")

- Uninstalled, each confirmed by Shopify's banner or the app list: Afterpay On-Site Messaging, GemPages,
  Fudge Agent, Essential Announcer, Adveronix, Lovable (Lovable sits under Sales channels, not Apps).
- AvantLink KEPT: Cole asked "should it go if we still have people on there?" Removing the pixel
  stops affiliates' sales tracking, so they stop getting paid. 0 of the last ~500 orders
  (Aug 23 to Oct 2) came in through an AvantLink link. Next: check its dashboard for active
  affiliates, move any to Lucky Creators with notice, close the program, then uninstall.
- Notify Me: opening the app asks to GRANT it more access (customer data, orders) before it loads.
  Not granted. Cole decides: approve that once to export the waitlist, or ask their support for a CSV.
- Judge.me: NOT pooled. The current 13 polos and 10 hats have 0 reviews. The existing "All Polos"
  group holds 11 reviews of 5 discontinued shirts at 3.91 avg; pooling would show 3.9 stars from
  different shirts on the new line. "All Hats" has 0 reviews. Wait for real reviews (request emails run).
- Seen on Sales channels: Pinterest shows "Action needed".

## Later 2026-10-02

- Notify Me UNINSTALLED (Cole). It was $9.90/mo, going to $29.90/mo on Nov 13. It didn't appear in the Apps
  list (pending permission request); removed from Settings > Apps > app_installations/app/bestpush.
- Klaviyo has NO live back-in-stock flow (checked the 13 live flows). The site's "Tell me when it's back"
  signups land in Klaviyo but nobody gets emailed until a Back in Stock flow is built and set live.
- Sept 15 bill, app charges through Shopify: Alia 200, Upcart 54.99, Parcel Panel 24.50, Avalara 24,
  Judge.me 15, Essential Announcer 9.99, Notify Me 9.96. The other apps removed (Sept 27 + today) billed $0
  through Shopify; Lovable/Fudge/Replo may bill a card directly.
- Judge.me: hiding a review requires a reason (fake, duplicate, spam, unrelated, legal, inappropriate,
  foreign language, private info, false/misleading). None is true for "old product", so nothing hidden.
  The 11 old-polo reviews sit on deleted products; they show nowhere on the new polo pages.
- Pinterest channel: "Needs attention", pixel Disconnected (it fired nothing before the move either).
- AvantLink: the login page needs Cole's password.

## Later still, 2026-10-02

- Judge.me: all 8 old-polo reviews (discontinued shirts, 1-3 yrs old) set Hidden, reason "Unrelated to the product"
  (Cole's call), 5-star and low alike: Thomas Vysocky, Cindi Murphy, Trisha Dunn, Richard Robinson, Tim Elder,
  jessica rodriguez, Lucky Cruz x2. Their other reviews (wedges, putters, gloves, tees) untouched. The 2 Cody Reid
  reviews come from the Shop app and Judge.me can't hide them. The Marble Classic Polo review (current) stays.
- Pinterest uninstall: blocked by the permission check (irreversible); Cole said "no Pinterest ads yet", not "remove".
- Parcel Panel: KEEP. It syncs every order (activity "1 minute ago"), and /apps/parcelpanel got 205 landing
  sessions in 90 days (199 direct, so from email/SMS app clicks). Shopify's own shipping email links to the
  Shopify order page + the carrier, so the traffic comes from somewhere else (likely Parcel Panel's own emails).
  "Track your order" added back to the footer menus (lucky-footer-support, lucky-phone-footer).
- AvantLink: Cole pasted a password in chat; Claude doesn't type passwords. The tab sits at verify-device.
- Parcel Panel UNINSTALLED 2026-10-02 (Cole: "drop Parcel Panel"), $23/mo + usage. "Track your order" in
  lucky-footer-support, lucky-phone-footer and the old theme's "footer" menu now points to
  https://shopify.com/22863149/account/orders. Redirect /apps/parcelpanel -> same, for links in old emails.
- AvantLink CHECKED (Cole logged in, merchant 31441): ACTIVE. 2026 YTD 202 orders / $27,197.53 sales /
  $3,535.98 total cost (13%), vs Shopify YTD 3,391 orders / $513,114 = ~6% of orders, ~5% of sales.
  42 active affiliates, 10 pending. Top by sales (30d) are coupon/deal sites: savinggain, dealspotr, sovrn,
  DontPayFull, couponology, gearchase, price.com. Balance due $294.84 on 10/10 (auto-pay on).
  My earlier "0 of ~500 orders came through AvantLink" was WRONG: Shopify's landing-page data doesn't show
  AvantLink's tracking. KEEP. Open question: coupon sites often take credit for buyers who were already checking out.
