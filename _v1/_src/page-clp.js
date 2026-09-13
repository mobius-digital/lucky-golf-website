/* ==========================================================================
   CLUB COLLECTION
   The grid, the bands and the comparison are all rendered by build.py into the
   HTML — there are no facets and no sort on these pages, so there is nothing
   for a script to repaint. Quick add works through core.js's [data-add]
   delegation, and the reveal comes from core.js's observer, both of which are
   already running before this file's only job matters.

   That job: no club ships with a head cover (Product Reference Guide v1.8 says
   so on every club entry), so the drawer offers one. core.js filters out
   anything already in the bag and hides the block when nothing is left.
   ========================================================================== */
var LG_CART_UPSELL = {{UPSELL_JSON}};

/* Option axes and the real variant map for the in-card Quick add picker.
   core.js owns the panel; this only supplies the data. See build.py's
   quick_add_data() — in-stock products with at least one axis only. */
var LG_QUICKADD = {{QUICKADD_JSON}};
