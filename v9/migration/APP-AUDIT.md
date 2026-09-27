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
