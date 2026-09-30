# Conversion baseline (Shopify analytics, last 30 days to 2026-09-27)

| Metric | Value |
|---|---|
| Sessions | 41,053 (mobile 35,678 · desktop 5,037 · tablet 271) |
| Sessions with add to cart | 1,632 (**3.98%**) |
| Sessions reaching checkout | 698 (**1.70%**) |
| Sessions completing checkout | 320 |
| Conversion rate | **0.78%** (mobile 0.78%, desktop 0.79%) |
| Orders | 354 |
| Gross sales | $63,716.82 |
| Discounts | -$12,143.37 |
| Net sales | $50,931.85 |
| Total sales | $55,623.96 |
| **AOV** | **$145.69** |

Checkout completion from reached-checkout: 45.8%. That step is Shopify's, not the
theme's, so it should not move; if it does after launch, look at the cart drawer
(return coverage, GWP lines) before anything else.

## Quietest hours (sessions, 30 days, shop time)

4am 510 · 3am 518 · 1am 529 · 2am 609 · 5am 712 · midnight 794.
Launch window: a weekday between 1am and 5am shop time, or the latest evening
Cole can watch (section 7 wants someone watching the first hour).

## Day-7 and day-30 comparison

Re-run the same ShopifyQL:
- `FROM sessions SHOW sessions, sessions_with_cart_additions, sessions_that_reached_checkout, sessions_that_completed_checkout, conversion_rate SINCE -7d UNTIL today`
- `FROM sales SHOW orders, gross_sales, discounts, net_sales, total_sales, average_order_value SINCE -7d UNTIL today`
