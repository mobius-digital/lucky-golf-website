# SEO baseline: what the live pages carry today (crawled 2026-09-27)

Full per-URL data: `seo-baseline.csv` (made by `python v9/tools/seo_crawl.py`).
The inventory lists 111 lines but 14 are repeats; **97 unique URLs**, 96 return 200.

| Type | URLs | No meta description | H1 count not 1 | Structured data |
|---|---|---|---|---|
| Home | 1 | 0 | 3 H1s | Organization + WebSite |
| Products | 43 | 1 | 5 (club pages have **9 H1s**; Stryker has 0) | **Product schema on only 15 of 43** |
| Pages | 23 | 11 | 9 | mostly Organization only |
| Collections | 14 | **14 (all)** | 0 | Organization only |
| Blog + posts | 14 | 0 | 1 | Article on 13 |

- **404 today:** `/collections/non-clubs` (hidden from the store already; not a move problem).
- **Canonicals:** all self-referencing on www. Keep that.
- **Images without alt text:** 1,296 of 2,330 (56%).
- No page sets a robots meta tag (none noindexed).

## The bar the new theme has to clear

Every URL: same status (200), same canonical, a title and description at least
as good, exactly one H1, and structured data at least as rich. The new theme
should beat this easily: one H1 per page, Product schema on all 43 products,
descriptions on all collections, alt text on product images.

## Re-crawl on the preview

`python v9/tools/seo_crawl.py --theme <id> --out v9/migration/seo-preview.csv`.
Note: plain HTTP requests to a preview link get a 302/503 from Shopify
(it wants a preview cookie), so the preview crawl runs through the browser or
with the cookie from the preview bar. Sort that out when the pages are built.
