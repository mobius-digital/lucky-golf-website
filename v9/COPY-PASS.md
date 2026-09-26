# Copy pass: every v9 page against the new copy skill

Added 2026-09-23 at Cole's request. The copy skill (How We Write v10.0 + the
product reference guide) was revamped; every page gets rewritten against it
BEFORE the Shopify port bakes the words into section defaults.

## How each page goes

1. Load the lucky-golf-copy skill fresh for every page (loading it once and
   drifting is the known failure, see memory: lucky-copy-skill-reaudit).
2. Rewrite every visible string: headlines, body, buttons, tags, FAQ answers,
   empty states, alt text. One big moment per page, energy in the body, the
   rest straight. Facts only from the product reference guide.
3. Check: no em dashes, contractions throughout, no invented numbers or
   reviews, product names current (Eclipse, Havoc, Carver 02).
4. Rebuild, audit at 1440 / 834 / 390, republish the board with a
   "Copy v10" note on that row. Cole reacts; fix; mark the row done below.

Templates count once: the polo, hat, gear and club templates get one pass,
then the per-item lines (polos-copy.json, HAT_COPY, build_simple.py) get theirs.

## Order (money pages first)

| # | Page | Status |
|---|------|--------|
| 1 | Carver 02 Gold + Black (one template) | signed off 2026-09-24 |
| 2 | Home | signed off 2026-09-24 |
| 3 | Clubs | signed off 2026-09-24 |
| 4 | Eclipse Blade + Eclipse Mallet (club template) | signed off 2026-09-24 |
| 5 | Stryker | signed off 2026-09-24 |
| 6 | Polos + polo template + 13 print lines | signed off 2026-09-25 (Breezy tiles) |
| 7 | Hats + hat template + 10 hat lines | signed off 2026-09-24 |
| 8 | Gear + gear template + item lines | signed off 2026-09-25 |
| 9 | Cart, drawer, search, 404 | signed off 2026-09-25 |
| 10 | Our story | done 2026-09-25, awaiting Cole |
| 11 | Questions (FAQ) + policy | done 2026-09-25, awaiting Cole |
| 12 | Ambassadors | done 2026-09-25, awaiting Cole |
| 13 | Community + All reviews | done 2026-09-26, awaiting Cole |
| 14 | Gift card + recipient view | done 2026-09-26, awaiting Cole |
| 15 | Collection template | to do |
| 16 | Account, login, order, addresses | to do |
| 17 | Blog + article | to do |

## Where it sits in the plan

Copy pass (this file) runs page by page with Cole's reactions. The Shopify
port's section code can be built alongside it, but a page's section defaults
are only filled in once that page's copy is done here.
