Black Friday 2026 sitewide pieces, pushed to the test theme "BF page v2 test (Oct 27)" (171935793429) on 2026-10-29.
These copies are built on the LIVE theme's versions of each file (not the site-v9-board branch copies), so pushing them
changes nothing else on the site. What each does:
- snippets/lg-cs.liquid + config/settings_data.json (cs_*): the Carver sets offer switch now runs Black Friday
  (VIP/LUCKYMAIL from Oct 28, public Nov 27, ends Dec 1), counts every club in the bag, $50 off 2 / $100 off 3+.
- sections/header-group.json: gold "Black Friday" link first in the menu. Bar line comes from cs_bar.
- sections/lg-club-main.liquid: Carver keeps its 1/2/3 tiles; other clubs get the ladder tiles; "Starts Nov 27" note before.
- sections/lg-bf-home.liquid + templates/index.json: Black Friday band on top of the homepage.
- assets/lucky-site.js/.css: bag link says "See the deals"; foil menu link; PDP note styles.
Note: this replaces the Carver sets offer (Oct 26 to 30) on the test theme only.
