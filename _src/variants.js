/* ==========================================================================
   Variant-axis engine  —  no DOM, no page state

   Kept out of the page IIFE on purpose. The store needs 0, 1 and 2 axes
   (GAMEPLAN 2a) but only one product page exists to look at, so the rules
   below are verified against the whole catalogue by tools/test-variants.js
   rather than against whatever the open page happens to render.

   A "selection" is one value key per axis, e.g. ['RH','56']. A product with
   no axes has the single variant key '', whose selection is [''].
   ========================================================================== */
(function (root, factory) {
  var api = factory();
  root.LG_VARIANTS = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {

  /* Is any sellable variant reachable with `val` on axis i, holding the axes
     to the LEFT of i at what is already selected?

     Cascading left to right is what makes "Left hand" gray out only when no
     loft at all is available in it, while an individual loft grays out for
     the hand you are actually on. Availability is the `avail` flag and never
     `qty > 0`: Shopify oversells some lines and holds others at zero while
     still selling them, so quantity answers a different question. */
  function offered(pd, sel, i, val) {
    var variants = pd.variants, k, parts, j, ok;
    for (k in variants) {
      if (!variants[k].avail) continue;
      parts = k.split('|');
      if (parts[i] !== val) continue;
      ok = true;
      for (j = 0; j < i; j++) { if (parts[j] !== sel[j]) { ok = false; break; } }
      if (ok) return true;
    }
    return false;
  }

  /* Changing axis `from` can strand the axes to its right on a dead variant.
     Slide each to the nearest offered value by position — on an ordered axis
     (lofts, sizes) that is the neighboring step up or down, which is what
     someone switching hand actually wants. Mutates and returns `sel`. */
  function reconcile(pd, sel, from) {
    var axes = pd.options || [], i, vals, at, best, bestD, n, d;
    for (i = from + 1; i < axes.length; i++) {
      if (offered(pd, sel, i, sel[i])) continue;
      vals = axes[i].values; at = 0; best = null; bestD = Infinity;
      for (n = 0; n < vals.length; n++) { if (vals[n].k === sel[i]) at = n; }
      for (n = 0; n < vals.length; n++) {
        if (!offered(pd, sel, i, vals[n].k)) continue;
        d = Math.abs(n - at);
        if (d < bestD) { bestD = d; best = vals[n].k; }
      }
      if (best !== null) sel[i] = best;
    }
    return sel;
  }

  function selectionFor(pd) { return String(pd['default']).split('|'); }

  function variantFor(pd, sel) { return pd.variants[sel.join('|')]; }

  /* The chosen value's display label on each axis, in axis order. */
  function labels(pd, sel) {
    var axes = pd.options || [], out = [], i, n, vals;
    for (i = 0; i < axes.length; i++) {
      vals = axes[i].values;
      for (n = 0; n < vals.length; n++) { if (vals[n].k === sel[i]) out.push(vals[n].label); }
    }
    return out;
  }

  return {
    offered: offered,
    reconcile: reconcile,
    selectionFor: selectionFor,
    variantFor: variantFor,
    labels: labels
  };
}));
