"""Launch day: put every product, collection and page on its new template, create the two new
pages, then (separately) publish the rewritten articles and product copy.

    python tools/theme/launch_day.py            -> writes v9/migration/launch/*.json + prints the plan (dry run)

Nothing here writes to Shopify. Each JSON file is the variables for one connector
graphql_mutation (the mutation text is in the file under "query"). Run them in order,
right AFTER the theme is published (template suffixes that don't exist in the live
theme fall back to the default template, so switching before publish would change the
live site's look page by page).

Order on launch day:
  1. Publish "Lucky v4 (build, unpublished)" (Online Store > Themes).
  2. 01-products.json, 02-collections.json, 03-pages.json, 04-new-pages.json
  3. python tools/theme/publish_articles.py  (then send v9/migration/articles-publish/*.json)
  4. python tools/theme/publish_product_copy.py (then send v9/migration/product-copy/*.json)
  5. Re-crawl: python v9/tools/seo_crawl.py --out v9/migration/seo-after.csv
Rollback: publish the old theme again; template suffixes named club/polo/... then fall back to
the old theme's default templates, so also re-run 01..03 with the "rollback" values in each file.
"""
import json, os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "v9", "migration", "launch")

CLUBS = ["lucky-golf-lgw02-gold", "lucky-golf-lgw02-black", "signature-gold-putters", "limited-edition-mallet-putter", "lucky-striker-hybrid-limited-edition"]
POLOS = ["gold-dust-classic-polo", "shadow-classic-polo", "signature-black-classic-polo", "contour-classic-polo", "marble-classic-polo", "gold-carnation-classic-polo",
         "frost-classic-polo", "swirl-blade-polo", "spot-blade-polo", "blackout-blade-polo", "cruiser-classic-polo", "azalea-classic-polo", "nightshade-classic-polo"]
HATS = ["white-gold-classic-hat", "white-its-better-to-be-lucky-patch-hat", "cream-upside-down-hat", "black-its-better-to-be-lucky-patch-hat", "tan-cursive-hat",
        "black-gold-classic-lucky-hat", "white-black-upside-down-hat", "white-upside-down-hat", "white-cursive-hat", "baby-blue-cursive-hat"]
GEAR = ["lucky-clover-tour-glove", "lucky-putter-head-cover-blade", "copy-of-lucky-golf-clover-grips-green", "lucky-golf-oversized-putter-grip",
        "lucky-golf-clovers-oversized-putter-grip", "lucky-golf-performance-x2-clover-grips-black", "copy-of-lucky-golf-performance-x2-clover-grips-white",
        "lucky-golf-performance-x2-clover-grips-blue", "lucky-golf-performance-x2-clover-grips-pink", "driver-head-cover",
        "stock-putter-grips", "lucky-putter-head-cover-mallet-large"]
CLUB_TPL = {"lucky-golf-lgw02-gold": "club-carver-gold", "lucky-golf-lgw02-black": "club-carver-black", "signature-gold-putters": "club-blade",
            "limited-edition-mallet-putter": "club-mallet", "lucky-striker-hybrid-limited-edition": "club-stryker"}  # own editable templates (2026-09-30)
PRODUCTS = [(h, CLUB_TPL[h]) for h in CLUBS] + [(h, "polo") for h in POLOS] + [(h, "hat") for h in HATS] + [(h, "gear") for h in GEAR] + [("lucky-wedges-gift-card", "giftcard")]
COLLECTIONS = [("polos", "polos"), ("classic-polos", "polos"), ("blade-polos", "polos"), ("hats", "hats"), ("lucky-golf-clubs", "clubs"), ("gear", "gear")]
PAGES = [("about", "story"), ("faq-lucky-wedges", "faq"), ("become-apart-of-the-team", "ambassadors"), ("contact-us", "contact"), ("reviews", "reviews")]
NEW_PAGES = [("compare", "Lucky vs the big names", "compare"), ("community", "Community", "community")]


def dump(name, query, items):
    os.makedirs(OUT, exist_ok=True)
    json.dump({"query": query, "items": items}, open(os.path.join(OUT, name), "w", encoding="utf-8"), indent=2)
    print(f"{name}: {len(items)} changes")


def main():
    dump("01-products.json", "mutation($input: ProductUpdateInput!){ productUpdate(product:$input){ product{ handle templateSuffix } userErrors{ message } } }  # look up id by handle first",
         [{"handle": h, "templateSuffix": t, "rollback": "(the suffix recorded in v9/migration/live-templates.json)"} for h, t in PRODUCTS])
    dump("02-collections.json", "mutation($input: CollectionInput!){ collectionUpdate(input:$input){ collection{ handle templateSuffix } userErrors{ message } } }",
         [{"handle": h, "templateSuffix": t, "rollback": ""} for h, t in COLLECTIONS])
    dump("03-pages.json", "mutation($id: ID!, $page: PageUpdateInput!){ pageUpdate(id:$id, page:$page){ page{ handle templateSuffix } userErrors{ message } } }",
         [{"handle": h, "templateSuffix": t, "rollback": ""} for h, t in PAGES])
    dump("04-new-pages.json", "mutation($page: PageCreateInput!){ pageCreate(page:$page){ page{ handle } userErrors{ message } } }",
         [{"handle": h, "title": title, "templateSuffix": t, "isPublished": True} for h, title, t in NEW_PAGES])


if __name__ == "__main__":
    main()
