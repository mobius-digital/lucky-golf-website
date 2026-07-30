# Lucky Golf — Phase 1 handoff

Read this first, then `01-home.html`. Everything below is decided unless marked OPEN.

---

## 1. Why Dartee reads "branded" instantly and ours doesn't

Compared frame by frame. It is not craft — it is **where the brand devices sit**.

| | Dartee | Takomo | Lucky (now) |
|---|---|---|---|
| First 100px | Deep green band, pink accent, pinstripes | Black bar, orange accent | Black marquee, gold text |
| Header | Green field, mascot present | White, orange cart | White, small green logo |
| Hero | Brand colour field around the photo | Full-bleed photo | Full-bleed photo |
| First scroll | Mascot again, pink CTA | Orange tags on tiles | Nothing until section 3 |

**The diagnosis: our first 900px is a white page with a photo on it.** Every Lucky device — clover watermark, groove, foil, emphasis tags, mono stamps — starts at the product grid and below. Dartee front-loads. Their header *is* a brand field, not a white bar.

**Fix direction (needs approval — see OPEN A):** put a brand-coloured field in the first 100px. Deep green `#008340` is the only palette colour that can carry a field without competing with gold. Gold is the product; green is the brand. Right now green does almost nothing, which is why the top reads neutral.

## 2. The mascot question

**Keep the clover. It is not the problem.** It has a golfer and a flagstick carved into the negative space — that is genuinely ownable and no other golf brand has it.

**The problem is scale and frequency.** Dartee's alligator appears ~4× at large size and is *illustrative*. Ours appears at 19px in the logo and as a low-opacity watermark that only shows up 3 sections down.

**Recommendation:** keep the clover, use it 3–4× at large scale above the fold, and do NOT commission a new mascot. A second character would fight the clover and the brand guide locks the logo system.

## 3. Section problems, confirmed against Takomo

| Section | What is wrong | Fix |
|---|---|---|
| Marquee | Black band at the very top reads like a utility bar, not brand | Move under the hero; test green field instead of ink |
| Product grid | CTA line and hover border are off-brand; no foil anywhere | Remove the black hover border, add foil hover, restyle the meta line |
| Mega menu | Still not Takomo — theirs is bigger, calmer, more air | Rebuild: fewer tiles, larger, more padding |
| Apparel/gear | Lists **individual products** (specific polos, specific hats) | Must be **collections**: Polos / Hats / Gear, lifestyle photo + name + one line + button |
| Missing | Takomo has a full-bleed brand band (logo + mono taglines) | Add one |
| Missing | Takomo has "THE BEST VALUE IN GOLF" — dark, icon value props, photo collage | Add one |
| Missing | Takomo has "THE ROSTER" — creator headshots on the homepage | Add one, feeds Trybe |

## 4. Locked decisions

- Background **white**; cream is an accent only (tiles, pricing band, cart footer)
- Radius **4px**, borders **2px**
- **Cart drawer only**, never a cart page
- Groove: ink `rgba(246,242,232,.13)` 1px/6px · cream `rgba(23,20,15,.032)` 1px/6px
- Type locked: Archivo (wdth 62 display) + Space Mono. Mono-lowercase asides allowed only when attached to a line above
- Foil ramp: shadow→base→highlight→base→shadow, highlight sweeps right→left on hover
- Tiles use **studio cutouts** + `mix-blend-mode:multiply`; lifestyle photography is for full-bleed sections only
- Reviews: real Judge.me, 4★ floor, brand comparisons allowed
- Flat pricing across lofts (assumed from the Product Reference Guide)

## 5. Data sources that already work

- Shopify MCP → `lucky-wedges.myshopify.com`. Product media via `productByHandle{media}`
- Judge.me public widget (no auth):
  `https://app.judge.me/reviews/reviews_for_widget?url=lucky-wedges.myshopify.com&shop_domain=lucky-wedges.myshopify.com&platform=shopify&per_page=30&page=N&product_id=<id>`
- Ratings: LGW01 4.81/551 · LGW02G 4.78/69 · LGP01 4.86/147 · LGP02 4.71/58 · LGH01 4.60/20 · LGD01 4.33/39. Clubs 4.78 / 884
- **Zero reviews have customer photos** — Judge.me photo requests are off. Turn on.

## 6. Studio cutout URLs (base `https://cdn.shopify.com/s/files/1/2286/3149/files/`)

- LGW01 `6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868`
- LGW02 Gold `1_27f81f90-a495-4dc4-ba02-0650ea6c4608.webp?v=1781012462` (bg slightly warm — try `3_b91d1d46-0aaa-4a41-9473-734a3f79362c.webp?v=1781012462`)
- LGW02 Black `6_cef3d6fc-8907-4866-b6aa-6301f8c614b5.webp?v=1784586436`
- LGP01 `3_f3d878d3-a4bb-4cc9-82df-f68e8eec3f61.webp?v=1782599090`
- LGP02 `1_b00c01f0-8116-464a-a39c-08a6ebf82b6f.webp?v=1782598133`
- LGH01 `3_a032f79a-78ab-436e-81c9-eea7bb5f7f40.webp?v=1782597493`

Known bad asset: `59.webp` (white snapback) has inverted lettering. Do not use.

## 7. OPEN — needs Cole

- **A.** Green field in the header/top band, yes or no
- **B.** Marquee: under the hero on green, or delete it
- **C.** Gear section as collections (Polos / Hats / Gear) — confirm the three
- **D.** Add the three missing Takomo-style sections (brand band, value props, creator roster)

## 8. Build notes

`01-home.html` is generated. Source of truth is
`scratchpad/home_template.html` + `logo_symbols.svg` (spliced at `{{SYMBOLS}}`).
Rebuild: `python -c "t=open('home_template.html',encoding='utf8').read();s=open('logo_symbols.svg',encoding='utf8').read();open(r'01-home.html','w',encoding='utf8').write(t.replace('{{SYMBOLS}}',s))"`

Git history is the rollback path: `git log --oneline`.
