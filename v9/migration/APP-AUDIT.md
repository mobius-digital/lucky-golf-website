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
