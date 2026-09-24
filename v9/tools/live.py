"""Live stock for every page (Cole, 2026-09-24: "pull stock status live from
Shopify on every product card and buy box instead of from saved data").

products.json and polos-data.json were captured weeks ago; their sold-out flags
went stale (the Black & Gold Classic Hat showed sold out with 72 on hand).
_src/data/stock.json is read straight from the Shopify Admin API, one entry per
SKU, and everything that shows stock loads its data through here, so the saved
flags are never trusted. In the theme, availability comes from Liquid live.
"""
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
STOCK = json.load(open(os.path.join(ROOT, "_src", "data", "stock.json"), encoding="utf-8"))["sku"]
MISSING = set()


def products():
    """products.json with every variant's avail and qty replaced by the live value."""
    d = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))
    for p in d["products"]:
        for v in p.get("variants", {}).values():
            s = STOCK.get(v.get("sku"))
            if s is None:
                if v.get("sku"):
                    MISSING.add(v["sku"])
                continue
            v["avail"], v["qty"] = bool(s[0]), s[1]
    return d


def polos(src):
    """polos-data.json with each size's ok flag and the card's stock line recomputed live."""
    d = json.load(open(os.path.join(src, "polos-data.json"), encoding="utf-8"))
    SUFFIX = {"S": "Small", "M": "Medium", "L": "Large"}
    for x in d:
        # sizes that were sold out when the page was captured came with no SKU;
        # rebuild it from the product's own pattern (LGA-CP-Azalea-Large)
        known = next((z["sku"] for z in x["sizes"] if z.get("sku")), None)
        for z in x["sizes"]:
            if not z.get("sku") and known:
                z["sku"] = known.rsplit("-", 1)[0] + "-" + SUFFIX.get(z["size"], z["size"])
            s = STOCK.get(z["sku"])
            if s is None:
                MISSING.add(z["sku"])
                continue
            z["ok"] = bool(s[0])
        out = [z["size"] for z in x["sizes"] if not z["ok"]]
        x["stock"] = "Every size in stock" if not out else ("Sold out" if len(out) == len(x["sizes"])
                                                             else "Sold out in " + ", ".join(out))
    return d
