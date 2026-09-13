/* Exercise the variant engine against every product in the catalogue.
 *
 *     node tools/test-variants.js
 *
 * The PDP renders exactly one product, and it is the two-axis one. Everything
 * the refactor was for — zero axes, one axis, per-variant pricing, products
 * that are entirely sold out — has no page to be seen on yet, so it gets
 * checked here instead. Exits non-zero on the first broken invariant.
 */
'use strict';
const path = require('path');
const fs = require('fs');

const ROOT = path.join(__dirname, '..');
const V = require(path.join(ROOT, '_src', 'variants.js'));
const CATALOGUE = JSON.parse(
  fs.readFileSync(path.join(ROOT, '_src', 'data', 'products.json'), 'utf8'));

let failures = 0;
function check(cond, what) {
  if (!cond) { console.log('  FAIL  ' + what); failures++; }
}

/* every combination of axis values, in axis order */
function allKeys(pd) {
  const axes = pd.options || [];
  if (!axes.length) return [''];
  return axes.reduce(
    (acc, ax) => acc.flatMap(prefix => ax.values.map(v => prefix.concat(v.k))),
    [[]]).map(parts => parts.join('|'));
}

const seen = { 0: 0, 1: 0, 2: 0 };

for (const pd of CATALOGUE.products) {
  const axes = pd.options || [];
  const label = `${pd.id} (${axes.length}-axis)`;
  seen[axes.length] = (seen[axes.length] || 0) + 1;

  // --- the variant map has to cover the full cross-product of the axes, or
  // --- a chip exists with nothing behind it
  const keys = allKeys(pd);
  const missing = keys.filter(k => !(k in pd.variants));
  check(missing.length === 0,
        `${label}: ${missing.length} option combinations have no variant: ${missing.slice(0, 3)}`);
  const extra = Object.keys(pd.variants).filter(k => !keys.includes(k));
  check(extra.length === 0, `${label}: variants not reachable from the axes: ${extra.slice(0, 3)}`);

  // --- the default has to exist, and has to be sellable whenever anything is
  const sel = V.selectionFor(pd);
  check(sel.length === Math.max(axes.length, 1),
        `${label}: selection width ${sel.length} for ${axes.length} axes`);
  const v0 = V.variantFor(pd, sel);
  check(!!v0, `${label}: default ${JSON.stringify(pd['default'])} resolves to no variant`);
  if (v0 && pd.inStock) check(v0.avail, `${label}: default variant is not sellable but others are`);

  // --- labels: one per axis, all non-empty
  const labels = V.labels(pd, sel);
  check(labels.length === axes.length, `${label}: ${labels.length} labels for ${axes.length} axes`);
  check(labels.every(Boolean), `${label}: blank label among ${JSON.stringify(labels)}`);

  // --- SKUs are carried from Shopify, never synthesised, so every variant
  // --- must actually have one and no two may collide
  const skus = Object.values(pd.variants).map(v => v.sku);
  check(skus.every(s => s && s.length), `${label}: a variant has an empty SKU`);
  check(new Set(skus).size === skus.length, `${label}: duplicate SKUs within the product`);

  // --- the core invariant: after picking any offered value on any axis and
  // --- reconciling, you must land on a variant that is actually sellable.
  // --- This is what stops the buy box offering a dead combination.
  for (let i = 0; i < axes.length; i++) {
    for (const v of axes[i].values) {
      const s = V.selectionFor(pd);
      if (!V.offered(pd, s, i, v.k)) continue;      // chip renders disabled
      s[i] = v.k;
      V.reconcile(pd, s, i);
      const landed = V.variantFor(pd, s);
      check(landed && landed.avail,
            `${label}: choosing ${axes[i].name}=${v.label} lands on ` +
            `${s.join('|')} which is ${landed ? 'out of stock' : 'not a variant'}`);
    }
  }

  // --- a product with nothing sellable must offer nothing, so every chip
  // --- renders dead rather than half the grid looking live
  if (!pd.inStock) {
    for (let i = 0; i < axes.length; i++) {
      const s = V.selectionFor(pd);
      check(axes[i].values.every(v => !V.offered(pd, s, i, v.k)),
            `${label}: sold out, but an axis still offers a value`);
    }
  }
}

// --- the cases the refactor exists for have to be present in the data at all
check(seen[0] > 0, 'no zero-axis product in the catalogue to exercise');
check(seen[1] > 0, 'no one-axis product in the catalogue to exercise');
check(seen[2] > 0, 'no two-axis product in the catalogue to exercise');

// --- per-variant pricing must survive normalisation
const priced = CATALOGUE.products.filter(
  p => new Set(Object.values(p.variants).map(v => v.price)).size > 1);
check(priced.length > 0, 'no product with per-variant pricing — the grips should have it');

console.log(`${CATALOGUE.products.length} products, ` +
            `${CATALOGUE.products.reduce((n, p) => n + Object.keys(p.variants).length, 0)} variants`);
console.log(`  axes: 0-axis ${seen[0]}, 1-axis ${seen[1]}, 2-axis ${seen[2]}`);
console.log(`  per-variant pricing: ${priced.map(p => p.id).join(', ')}`);
console.log(failures ? `\n${failures} FAILURE(S)` : '\nall invariants hold');
process.exit(failures ? 1 : 0);
