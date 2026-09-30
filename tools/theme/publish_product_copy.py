"""Prepare the approved v9 product copy for the polos, hats and gear. DRY RUN ONLY: this script
never writes to Shopify.

    python tools/theme/publish_product_copy.py

The new theme reads each product's own description (the print / front / what-it-is line), its
title, and the metafields custom.facts (gear "Quick facts") and custom.model_sizing (the polo
"[Name] is [height] ... wears a [size]." line). The approved copy for those lives in the v9 build:

  polos   v9/src/polos-copy.json                 (keyed by print name)
  hats    HAT_COPY in v9/tools/build.py          (keyed by v9 product id)
  gear    GEAR_COPY in v9/tools/build_simple.py  (desc, optional note, facts)
  titles  _src/data/products.json "name"         (only the gear titles differ from live)
  model   v9/src/polos-data.json "model"         (none filled yet, so none written)

It reads the live snapshot v9/migration/live-products.json (id, handle, title, description;
refresh it on launch day with the query below) and writes:

  v9/migration/product-copy/<handle>.json   {"query": ..., "variables": ...} for productUpdate
  v9/migration/product-copy-dry-run.md      what each update would change

Launch day (after the theme is live, so the new templates render these fields):
  1. Refresh the snapshot (connector graphql_query), save as {"products": [...]} with keys
     id, handle, title, description (descriptionHtml is fine):
       { products(first:50, query:"product_type:Apparel OR product_type:HAT OR product_type:Glove
         OR product_type:Grip OR product_type:Grips OR product_type:'Head Cover'"){ nodes{ id handle
         title description: descriptionHtml } } }
  2. Rerun this script, read the dry-run report, get Cole's OK.
  3. Send each product-copy/<handle>.json through the connector's graphql_mutation.
     Handles never change (productUpdate keeps the handle when only the title changes), so every
     URL and its SEO history stays put.
"""
import ast, html, json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
V9 = os.path.join(ROOT, "v9")
SNAP = os.path.join(V9, "migration", "live-products.json")
OUT_DIR = os.path.join(V9, "migration", "product-copy")
REPORT = os.path.join(V9, "migration", "product-copy-dry-run.md")

sys.path.insert(0, os.path.join(V9, "tools"))
import build_simple  # GEAR_COPY, copy_for (plain dicts, no side effects)

MUTATION = ("mutation($product: ProductUpdateInput!){ productUpdate(product: $product){ "
            "product{ id handle title } userErrors{ field message } } }")


def hat_copy():
    """HAT_COPY straight out of build.py without importing it (build.py builds on import)."""
    src = open(os.path.join(V9, "tools", "build.py"), encoding="utf-8").read()
    for node in ast.parse(src).body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "HAT_COPY" for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit("HAT_COPY not found in v9/tools/build.py")


def para(*lines):
    return "".join(f"<p>{html.escape(x, quote=False)}</p>" for x in lines if x)


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()


def main():
    snap = {p["handle"]: p for p in json.load(open(SNAP, encoding="utf-8"))["products"]}
    catalogue = json.load(open(os.path.join(ROOT, "_src", "data", "products.json"), encoding="utf-8"))["products"]
    polo_copy = json.load(open(os.path.join(V9, "src", "polos-copy.json"), encoding="utf-8"))
    polo_data = {x["full"]: x for x in json.load(open(os.path.join(V9, "src", "polos-data.json"), encoding="utf-8"))}
    hats = hat_copy()
    os.makedirs(OUT_DIR, exist_ok=True)

    rows, missing = [], []
    for p in catalogue:
        h, fam, pid = p.get("shopifyHandle"), p.get("family"), p["id"]
        if fam not in ("polo-classic", "polo-blade", "hat", "headcover", "grip", "glove"):
            continue
        live = snap.get(h)
        if not live:
            missing.append(f"{p['name']} ({h}): not in the live snapshot")
            continue
        title, desc, facts, model = p["name"], "", None, None
        if fam.startswith("polo"):
            short = p["name"].replace(" Classic Polo", "").replace(" Blade Polo", "")
            desc = para(polo_copy.get(short, ""))
            model = (polo_data.get(p["name"]) or {}).get("model") or None
        elif fam == "hat":
            desc = para(hats.get(pid, ""))
        else:
            c = build_simple.copy_for(pid)
            desc = para(c["desc"], c.get("note"))
            facts = [f"{a}: {b}" for a, b in c["facts"]]
        if not text(desc):
            missing.append(f"{p['name']} ({h}): no approved copy found")
            continue

        product = {"id": live["id"]}
        changes = []
        if title != live["title"]:
            product["title"] = title
            changes.append(("Title", live["title"], title))
        if text(desc) != text(live.get("description")):
            product["descriptionHtml"] = desc
            changes.append(("Description", text(live.get("description")), text(desc)))
        mf = []
        if facts:
            mf.append({"namespace": "custom", "key": "facts", "type": "list.single_line_text_field", "value": json.dumps(facts)})
            if facts != (live.get("facts") or []):
                changes.append(("Quick facts", ", ".join(live.get("facts") or []) or "(empty)", " | ".join(facts)))
        if model:
            mf.append({"namespace": "custom", "key": "model_sizing", "type": "single_line_text_field", "value": model})
            if model != live.get("model_sizing"):
                changes.append(("Model line", live.get("model_sizing") or "(empty)", model))
        if mf:
            product["metafields"] = mf
        if len(product) == 1:
            rows.append((p["name"], h, []))
            continue
        json.dump({"query": MUTATION, "variables": {"product": product}},
                  open(os.path.join(OUT_DIR, h + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        rows.append((p["name"], h, changes))

    out = ["# Product copy: dry run", "",
           "Built by `tools/theme/publish_product_copy.py` from the approved v9 copy against the live snapshot "
           "`v9/migration/live-products.json`. Nothing has been sent to Shopify. Payloads are in "
           "`v9/migration/product-copy/<handle>.json` (productUpdate; handles never change).", "",
           f"{sum(1 for r in rows if r[2])} products would change, {sum(1 for r in rows if not r[2])} already match.", ""]
    for name, h, changes in rows:
        out.append(f"## {name}  \n`{h}`")
        if not changes:
            out += ["", "Already matches. No update.", ""]
            continue
        out.append("")
        for what, old, new in changes:
            out += [f"**{what}**", "", f"- now: {old}", f"- new: {new}", ""]
    if missing:
        out += ["## Not prepared", ""] + [f"- {m}" for m in missing] + [""]
    out += ["## Not included", "",
            "- Model sizing lines: `v9/src/polos-data.json` has none yet (they wait on the on-body shoot), so no product gets one.",
            "- Collar, color and style filters and the card cutouts are already set as metafields (2026-09-27).", ""]
    open(REPORT, "w", encoding="utf-8").write("\n".join(out))
    print(REPORT, "|", sum(1 for r in rows if r[2]), "payloads |", len(missing), "not prepared")


if __name__ == "__main__":
    main()
