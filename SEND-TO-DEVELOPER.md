# Start here

**The job: turn this prototype into a Shopify theme for luckygolf.com.**

The design, the copy and the page structure are finished and signed off. None of
it is a wireframe or a mockup. Every page in this repo is real, working HTML you
can open in a browser today.

---

## The two links

- **Browse it:** https://mobius-digital.github.io/lucky-golf-website/
- **The code:** https://github.com/mobius-digital/lucky-golf-website

---

## Read these, in this order

1. **`DEVELOPER-HANDOFF.md`** — the whole brief. How the build works, the repo
   map, every page mapped to the Shopify template that replaces it, a
   Mustache-to-Liquid conversion table, the catalogue traps, and the design
   rules with their measured numbers. **Sections 8 and 9 before you write any
   code** — those are rules that were arrived at by measuring, and they get
   reintroduced by accident if nobody says them out loud.
2. **`SHOT-LIST.md`** — the 51 photographs still to shoot, grouped into four
   sessions. See "What isn't done" below.
3. **`FINISH-LINE.md`** — the running state of everything outstanding.

The four `references-*.md` files are the brand's own source of truth for voice
and for product specs. Consult them before writing any customer-facing words or
any number. **Never write a spec from memory.**

Everything else at the root (`HANDOFF.md`, `GAMEPLAN.md`, `NEXT-PAGES.md`,
`VOICE-*.md`) is the build's history. Useful if you want to know why something
is the way it is; not required reading.

---

## Run it

Python 3, no dependencies. Node only for the variant test.

```bash
python tools/normalize-products.py     # Shopify pull + editorial overlay -> products.json
python tools/build.py                  # assemble all 60 pages
```

Four checks. All four must be clean before anything ships:

```bash
python tools/build.py --check          # every page rebuilds byte-identical
python tools/build.py --links          # 62 pages, 60 built, zero dead links
python tools/normalize-products.py --check
node tools/test-variants.js
```

`_src/` and `tools/` are the architecture. The HTML files at the root are build
output, not source. **Never hand-edit them.**

---

## What isn't done

**Photography.** 51 stills, listed in `SHOT-LIST.md` with the crop, the light
and what has to read in each frame. Every unshot slot currently renders as a
labelled brief rather than a broken image, so the pages read as finished
without them. Video is lower priority and separate.

⚠️ **One thing to know when photos land:** a product with *zero* images used to
crash its own page and take the Add to cart button down with it. That is fixed,
and the fix is described in `DEVELOPER-HANDOFF.md` §12. Keep that behaviour when
you port the gallery, because every product is in exactly that state until its
shoot happens.

---

## Things that will bite you if nobody says them

All of these are expanded in `DEVELOPER-HANDOFF.md`. They are here because each
one was a real bug found by measuring, not a preference.

- `availableForSale` is **not** `inventoryQuantity > 0`. Some lines oversell,
  some sit at zero and still sell.
- Every price is **per variant**, not per product.
- **SKUs are never synthesised.** Several in this store are genuinely irregular,
  including a typo that is now load-bearing. Carry them verbatim.
- A product card **never** shows a review count.
- Judge.me review numbers on this store are **group pools**, not per-product
  counts. Read them from the product's `judgeme` metafields.
- Foil is illegal on white as type, and automated contrast checkers cannot see
  it. Small text on a foil fill needs the dedicated token.
- Radius follows the **size of the surface**, not the type of component.
- Some code in `tools/` is explicitly temporary and marked as such. Port the
  state it produces, not the code.

---

## Questions

Anything about scope, priority or brand goes to Cole. Anything in this repo that
looks wrong or contradictory, say so rather than guessing. Several of these
pages exist because an earlier assumption went unchallenged.
