# LUCKY GOLF: apply this design system to the page you built

**Read this whole file before you change anything.** It contains the exact
stylesheet, the markup for every component, and the rules. You are not
designing a new look. You are moving an existing page onto a system that
already exists, so the page sits next to the rest of the Lucky Golf site and
reads as the same brand.

## What to do

1. **Add the font and the stylesheet.** Put the two blocks in STEP 1 into the
   page. If the project uses Tailwind, styled-components or anything else,
   keep it, but let these classes win for anything visual: colour,
   typography, spacing, buttons, cards, bands, header and footer.
2. **Re-skin the page you already have, section by section**, using the
   markup in STEP 2. Keep the page's existing copy, images, links and
   tracking. Do not rewrite the offer or change what the page says, except
   where STEP 4 says a line breaks a rule.
3. **Delete the old visual CSS** that the new classes replace. Two systems
   fighting is what makes a page look almost right and not right. Do not
   keep a second set of colours, shadows or fonts around "just in case".
4. **Do not add colours, fonts, shadows, gradients, rounded pills or scroll
   animations that are not in this file.** If something you need is missing,
   say so and ask. Do not invent it, and do not substitute a similar colour.
5. **Hand back**: the updated page, a list of anything you removed, and a
   list of anything you could not do because this file did not cover it.

## The three things that go wrong, so check them last

- **The page is too dark.** White is 78 to 88% of a Lucky screen. There is
  ONE dark band in the body of the page, plus the announcement bar, the
  header, the sign-off and the footer. If half your page is deep green, it
  is wrong.
- **Gold is everywhere.** Gold is under 1.5% of the screen. One foil button
  and one foil word per view. Not five.
- **The type is not Archivo at the right widths.** Display is width 62 and
  uppercase. Labels are width 78, tracked caps. Body is width 100. A page
  set in default Archivo at one width reads generic and it is the fastest
  way to lose the brand.

---

# STEP 1: the font and the stylesheet

Put this in `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
```

Save the CSS below as `lucky.css` and link it, or paste it into a global
stylesheet. Put `class="lg"` on `<body>`, or `class="lg-scope"` on the
wrapper that holds the page.

```css
/* ==========================================================================
   LUCKY GOLF - the design system as one stylesheet.
   Version 3.0 · 2026-09-17 · System: DEEP GREEN & GOLD.

   Drop this file in, load Archivo, and build with the classes below. Every
   class is prefixed lg- so it cannot collide with anything already on a page.

   The whole system in one paragraph: the page is white, type is ink, product
   sits on a stone tile, and ONE dark colour (deep green) carries the
   announcement bar, the header, the bands low on the page and the footer.
   Gold is the only accent and it never appears as a large field: buttons,
   one word per headline, stars, hairline marks. Signal green means in stock
   and nothing else. No cream, no brown, no second green.

   Measured on the real pages: white 78 to 88% of the screen, photography 6
   to 22%, deep green 3 to 12%, stone under 5%, gold under 1.5%.

   Fonts (put in <head>):
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">

   To try another system, change ONE value: --lg-dark.
     Deep green & gold  #0B2E1F   (this file, the pick)
     Ink & gold         #17140F
     White & gold       keep the bands white and use #121212 for the footer.
   ========================================================================== */

:root{
  /* ---------------- ground ---------------- */
  --lg-page:#FFFFFF;          /* the page. Most of every screen. */
  --lg-tile:#F4F3F0;          /* stone. Product wells, cards, table fills. A material, never a band. */
  --lg-dark:#0B2E1F;          /* THE one dark. Announcement bar, header, bands, footer. */

  /* ---------------- type on the ground ---------------- */
  --lg-ink:#17140F;           /* all text on white */
  --lg-ink-70:rgba(23,20,15,.70);
  --lg-ink-64:rgba(23,20,15,.64);
  --lg-ink-38:rgba(23,20,15,.38);
  --lg-on-dark:#F4F3F0;       /* text on the dark. 13.2:1 */
  --lg-on-dark-m:rgba(244,243,240,.72);
  --lg-rule:rgba(23,20,15,.14);
  --lg-rule-08:rgba(23,20,15,.08);
  --lg-rule-dark:rgba(244,243,240,.18);

  /* ---------------- accent ---------------- */
  --lg-gold:#C29A2B;          /* gold as a SURFACE: stars, rules, bars, buttons. 5.6:1 on the dark. */
  --lg-gold-hi:#EDD27C;
  --lg-gold-text:#8A6A1C;     /* gold as TYPE on white only. 5.05:1 */
  --lg-ok:#008340;            /* in stock, added, verified. Never decoration. */
  --lg-ok-on-dark:#7FB69A;
  --lg-clover:#0B5130;        /* the clover inside the logo. Nowhere else. */

  /* The foil is a material, not a colour. Ink type on it reads 6.9:1.
     Two places per view: the primary button, and ONE display word. */
  --lg-foil:linear-gradient(96deg,#C29A2B 0%,#EDD27C 50%,#C29A2B 100%);
  --lg-foil-text:linear-gradient(178deg,#C29A2B 0%,#EDD27C 46%,#EDD27C 56%,#C29A2B 100%);

  /* The pinstripe. Dark FEATURE bands only: never the header, bar or footer.
     Drawn as a 6px tile, because long CSS gradients rasterise unevenly. */
  --lg-groove:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='6' height='6'%3E%3Crect width='6' height='1' fill='%23F6F2E8' fill-opacity='.10'/%3E%3C/svg%3E");
  --lg-groove-light:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='6' height='6'%3E%3Crect width='6' height='1' fill='%2317140F' fill-opacity='.03'/%3E%3C/svg%3E");

  /* ---------------- measure ---------------- */
  --lg-wrap:1180px;
  --lg-pad:clamp(20px,4.2vw,68px);
  --lg-gut:clamp(16px,2vw,28px);
  --lg-sec:clamp(64px,7vw,112px);   /* space between page sections */
  --lg-r:6px;                       /* controls */
  --lg-r-card:14px;                 /* surfaces */
  --lg-ease:cubic-bezier(.23,1,.32,1);

  /* ---------------- type scale ---------------- */
  --lg-fs-xs:.72rem;
  --lg-fs-sm:.8rem;
  --lg-fs-base:.95rem;
  --lg-fs-body:1.0625rem;
  --lg-fs-lead:clamp(1.1rem,1.5vw,1.3rem);
}

/* ==========================================================================
   BASE
   ========================================================================== */
.lg-scope,
body.lg{margin:0;background:var(--lg-page);color:var(--lg-ink);
  font-family:'Archivo',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  font-variation-settings:'wdth' 100;font-size:var(--lg-fs-body);line-height:1.55;
  -webkit-font-smoothing:antialiased}
.lg-wrap{max-width:var(--lg-wrap);margin:0 auto;padding:0 var(--lg-pad)}
.lg-sec{padding-block:var(--lg-sec)}
.lg-hr{height:1px;background:var(--lg-rule);border:0;margin:0}
.lg-center{text-align:center}
:where(.lg-scope,body.lg) :focus-visible{outline:2px solid var(--lg-gold);outline-offset:2px}

/* ==========================================================================
   TYPE
   Display is Archivo at width 62, uppercase, 800. Labels at width 78, 600,
   tracked caps. Body is plain 100 width. Nothing else.
   ========================================================================== */
.lg-d1,.lg-d2,.lg-d3{margin:0;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;
  font-weight:800;text-transform:uppercase;line-height:.9;letter-spacing:-.005em;text-wrap:balance}
.lg-d1{font-size:clamp(2.6rem,6.2vw,5.2rem)}
.lg-d2{font-size:clamp(2rem,3.9vw,3.2rem)}
.lg-d3{font-size:clamp(1.25rem,1.8vw,1.6rem);line-height:1}

/* ONE word per headline carries the foil. Never body size. */
.lg-foil-word{background:var(--lg-foil-text);-webkit-background-clip:text;background-clip:text;color:transparent}

/* The eyebrow orients the section. It never restates the headline. */
.lg-eyebrow{display:flex;align-items:center;gap:11px;margin:0 0 16px;color:var(--lg-gold-text);
  font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  text-transform:uppercase;letter-spacing:.2em;font-size:var(--lg-fs-xs)}
.lg-eyebrow::before{content:'';width:22px;height:2px;background:var(--lg-gold);flex:none}
.lg-lede{margin:18px 0 0;max-width:46ch;font-size:var(--lg-fs-lead);line-height:1.5;color:var(--lg-ink-70)}
.lg-body{margin:14px 0 0;max-width:62ch;color:var(--lg-ink-70)}
.lg-meta{color:var(--lg-ink-64);font-size:var(--lg-fs-base)}
/* The aside is the charm voice: one line, sentence case, medium weight. */
.lg-aside{margin:14px 0 0;max-width:44ch;font-size:var(--lg-fs-body);font-weight:500;color:var(--lg-ink)}
.lg-label{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  text-transform:uppercase;letter-spacing:.12em;font-size:var(--lg-fs-xs)}
.lg-link{color:var(--lg-ink);text-decoration:none;font-family:'Archivo',sans-serif;
  font-variation-settings:'wdth' 76;font-weight:700;text-transform:uppercase;letter-spacing:.06em;
  font-size:var(--lg-fs-sm);border-bottom:2px solid var(--lg-gold);padding-bottom:4px;
  display:inline-flex;align-items:center;gap:8px}
.lg-link span{transition:transform .22s var(--lg-ease)}
.lg-link:hover span{transform:translateX(4px)}

/* On a dark ground everything flips to cream, and gold stays gold. Put
   .lg-on-dark on any block you build yourself over a dark field or a photo. */
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy){color:var(--lg-on-dark)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) .lg-eyebrow{color:var(--lg-gold)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) :is(.lg-lede,.lg-body,.lg-meta){color:var(--lg-on-dark-m)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) :is(.lg-link,.lg-aside,.lg-label){color:var(--lg-on-dark)}

/* ==========================================================================
   BUTTONS · one foil button per view, everything else is the ghost.
   44px minimum on a phone, always.
   ========================================================================== */
.lg-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;
  padding:0 26px;border:0;border-radius:var(--lg-r);cursor:pointer;text-decoration:none;
  font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 76;font-weight:700;
  text-transform:uppercase;letter-spacing:.06em;font-size:var(--lg-fs-sm);
  color:var(--lg-ink);background-image:var(--lg-foil);background-size:200% 100%;
  background-position:0 0;transition:background-position .45s var(--lg-ease),transform .12s var(--lg-ease)}
.lg-btn:hover,.lg-btn:focus-visible{background-position:100% 0}
.lg-btn:active{transform:scale(.975)}
.lg-btn[disabled],.lg-btn[aria-disabled="true"]{opacity:.55;cursor:not-allowed}
.lg-btn-line{background:transparent;background-image:none;color:var(--lg-ink);
  border:2px solid var(--lg-ink);min-height:48px}
.lg-btn-line:hover{background:var(--lg-ink);color:var(--lg-page)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) .lg-btn-line{color:var(--lg-on-dark);border-color:var(--lg-on-dark)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) .lg-btn-line:hover{background:var(--lg-on-dark);color:var(--lg-dark)}
.lg-btn-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}

/* ==========================================================================
   CHROME · the announcement bar and the header. Solid colour, no pinstripe,
   because they sit over every page and every photo.
   ========================================================================== */
.lg-tick{background:var(--lg-dark);color:var(--lg-on-dark-m)}
.lg-tick-in{max-width:none;padding:0 var(--lg-pad);min-height:34px;display:flex;align-items:center;
  justify-content:center;gap:28px;white-space:nowrap;overflow-x:auto;scrollbar-width:none;
  font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  font-size:11.5px;letter-spacing:.12em;text-transform:uppercase}
.lg-tick-in::-webkit-scrollbar{display:none}
.lg-tick a{color:inherit;text-decoration:none;display:inline-flex;align-items:center;min-height:34px}
.lg-tick b{color:var(--lg-gold);font-weight:600;margin-right:.35em}

.lg-hdr{position:sticky;top:0;z-index:40;background:var(--lg-dark);color:var(--lg-on-dark);
  border-bottom:1px solid var(--lg-rule-dark)}
.lg-hdr-in{padding:0 var(--lg-pad);height:72px;display:grid;grid-template-columns:1fr auto 1fr;
  grid-template-areas:"l n a";align-items:center;gap:24px}
.lg-logo{grid-area:l;justify-self:start;display:inline-flex;align-items:center;color:var(--lg-on-dark)}
.lg-logo svg,.lg-logo img{display:block;width:132px;height:auto}
.lg-nav{grid-area:n;justify-self:center;display:flex;gap:30px}
.lg-nav a{color:var(--lg-on-dark);text-decoration:none;font-family:'Archivo',sans-serif;
  font-variation-settings:'wdth' 78;font-weight:600;font-size:12.8px;letter-spacing:.06em;
  text-transform:uppercase;display:inline-flex;align-items:center;min-height:44px}
.lg-hdr-act{grid-area:a;justify-self:end;display:flex;align-items:center;gap:6px}
.lg-hdr-act a,.lg-hdr-act button{min-width:44px;min-height:44px;display:grid;place-items:center;
  background:none;border:0;color:var(--lg-on-dark);cursor:pointer}
@media (max-width:980px){
  .lg-hdr-in{grid-template-columns:auto 1fr;grid-template-areas:"l a";height:64px}
  .lg-nav{display:none}
  .lg-tick-in a:nth-child(n+2){display:none}
}

/* ==========================================================================
   BANDS · the dark beats low on the page. These carry the pinstripe.
   Rhythm for a landing page: bar, header, hero photo, white sections,
   ONE band, the sign-off, the footer. No two bands touch.
   ========================================================================== */
.lg-band{position:relative;background-color:var(--lg-dark);background-image:var(--lg-groove);
  color:var(--lg-on-dark);padding-block:var(--lg-sec)}
.lg-band-tile{background:rgba(244,243,240,.06);border:1px solid var(--lg-rule-dark);
  border-radius:var(--lg-r-card);padding:24px}

/* The hero: one full bleed photograph, headline bottom left over the scrim. */
.lg-hero{position:relative;isolation:isolate;background:#0f0d09;overflow:hidden}
.lg-hero img{display:block;width:100%;height:min(86vh,860px);min-height:520px;object-fit:cover}
.lg-hero::after{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(92deg,rgba(11,20,15,.82) 0%,rgba(11,20,15,.52) 38%,rgba(11,20,15,.04) 68%),
             linear-gradient(0deg,rgba(11,20,15,.55) 0%,rgba(11,20,15,0) 42%)}
.lg-hero-copy{position:absolute;inset:0;z-index:2;display:flex;align-items:flex-end;
  padding-bottom:clamp(40px,6vw,96px);color:var(--lg-on-dark)}
.lg-hero-copy .lg-wrap{width:100%}

/* ==========================================================================
   SURFACES · tiles and cards. Product sits on stone, photography sits full.
   ========================================================================== */
.lg-tile{background:var(--lg-tile);border-radius:var(--lg-r-card);overflow:hidden}
.lg-grid{display:grid;gap:var(--lg-gut);align-items:start;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}
.lg-card{display:flex;flex-direction:column;color:var(--lg-ink);text-decoration:none}
.lg-card-ph{position:relative;aspect-ratio:4/5;background:var(--lg-tile);border-radius:var(--lg-r-card);overflow:hidden}
.lg-card-ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s var(--lg-ease)}
.lg-card:hover .lg-card-ph img{transform:scale(1.03)}
.lg-card-bd{padding:14px 2px 0;display:grid;grid-template-columns:1fr auto;gap:4px 12px;align-items:baseline}
.lg-card-nm{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;
  text-transform:uppercase;font-size:clamp(1.05rem,1.3vw,1.25rem);line-height:1}
.lg-card-pr{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 74;font-weight:700}
.lg-card-ln{grid-column:1/-1;margin:2px 0 0;color:var(--lg-ink-70);font-size:var(--lg-fs-base);line-height:1.45}

/* A photograph that does not exist yet is a LABELLED SLOT, never a grey box
   and never a stock photo. Put the shot brief on it. */
.lg-slot{display:grid;place-items:center;text-align:center;padding:24px;aspect-ratio:4/5;
  background:var(--lg-tile) repeating-linear-gradient(135deg,rgba(23,20,15,.05) 0 8px,transparent 8px 16px);
  border:1px dashed var(--lg-rule);border-radius:var(--lg-r-card);color:var(--lg-ink-64);font-size:var(--lg-fs-base)}

/* Review card. Only ever a real review, quoted exactly, with a real name. */
.lg-quote{background:var(--lg-tile);border-radius:var(--lg-r-card);padding:24px;display:flex;
  flex-direction:column;gap:12px}
.lg-quote p{margin:0;font-size:var(--lg-fs-body)}
.lg-quote footer{color:var(--lg-ink-64);font-size:var(--lg-fs-base)}

/* Stat tile: a number that is real, and what it means underneath. */
.lg-stat{background:var(--lg-tile);border-radius:var(--lg-r-card);padding:22px}
.lg-stat b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;
  font-weight:800;font-size:clamp(1.8rem,3vw,2.6rem);line-height:1}
.lg-stat span{display:block;margin-top:6px;color:var(--lg-ink-64);font-size:var(--lg-fs-base)}

/* ==========================================================================
   SMALL PARTS · the stamp. Condensed caps on chips, tags, trust rows, tables.
   ========================================================================== */
.lg-tag{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:5px 11px;
  background:var(--lg-ink);color:var(--lg-page);
  font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;
  text-transform:uppercase;letter-spacing:.1em;font-size:var(--lg-fs-xs)}
.lg-tag-gold{background-image:var(--lg-foil);color:var(--lg-ink)}
.lg-tag-ok{background:var(--lg-ok);color:#fff}
.lg-chip{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:0 16px;
  border:1px solid var(--lg-rule);border-radius:var(--lg-r);background:var(--lg-page);cursor:pointer;
  font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  text-transform:uppercase;letter-spacing:.08em;font-size:var(--lg-fs-xs)}
.lg-chip[aria-pressed="true"],.lg-chip.is-on{background:var(--lg-ink);color:var(--lg-page);border-color:var(--lg-ink)}
.lg-stock{display:inline-flex;align-items:center;gap:8px;color:var(--lg-ok);font-size:var(--lg-fs-base)}
.lg-stock::before{content:'';width:8px;height:8px;border-radius:50%;background:currentColor}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) .lg-stock{color:var(--lg-ok-on-dark)}

/* Stars are a graphic: gold on white needs a darker gold to stay legible. */
.lg-stars{display:inline-flex;gap:2px;color:#9A7619;line-height:0}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr,.lg-hero-copy) .lg-stars{color:var(--lg-gold)}
.lg-stars svg{width:15px;height:15px;fill:currentColor}

.lg-trust{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px 24px;
  padding-block:20px;border-block:1px solid var(--lg-rule)}
.lg-trust span{display:flex;align-items:center;gap:10px;font-family:'Archivo',sans-serif;
  font-variation-settings:'wdth' 80;font-weight:600;text-transform:uppercase;letter-spacing:.08em;
  font-size:var(--lg-fs-sm)}
.lg-trust svg{width:20px;height:20px;flex:none;fill:none;stroke:var(--lg-gold-text);stroke-width:1.7}

/* Compare table: stone fill, hairlines, condensed caps in the head column. */
.lg-table{width:100%;border-collapse:collapse;font-size:var(--lg-fs-base)}
.lg-table th,.lg-table td{text-align:left;padding:14px 16px;border-bottom:1px solid var(--lg-rule-08);vertical-align:top}
.lg-table thead th{background:var(--lg-tile);font-family:'Archivo',sans-serif;
  font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
  font-size:var(--lg-fs-xs)}
.lg-table tbody th{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  text-transform:uppercase;letter-spacing:.08em;font-size:var(--lg-fs-xs);color:var(--lg-ink-64);width:1%;white-space:nowrap}

/* Email capture. One field, one button, the reason to give it. */
.lg-form{display:flex;flex-wrap:wrap;gap:10px;margin-top:20px}
.lg-input{flex:1 1 240px;min-height:52px;padding:0 16px;border:1px solid var(--lg-rule);
  border-radius:var(--lg-r);background:var(--lg-page);color:var(--lg-ink);font:inherit;font-size:var(--lg-fs-base)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr) .lg-input{background:transparent;border-color:var(--lg-rule-dark);color:var(--lg-on-dark)}
:is(.lg-on-dark,.lg-band,.lg-sign,.lg-ftr) .lg-input::placeholder{color:var(--lg-on-dark-m)}

/* ==========================================================================
   THE SIGN-OFF and THE FOOTER
   Mags is the emblem, never a cartoon with a face doing an action. He stands
   on the rule at the sign-off, and rides the bag button in the header.
   Use the cream artwork on dark grounds and the ink artwork on white ones.
   ========================================================================== */
.lg-sign{position:relative;background-color:var(--lg-dark);background-image:var(--lg-groove);
  color:var(--lg-on-dark);padding-block:clamp(56px,6vw,96px);overflow:hidden}
.lg-sign-in{display:grid;grid-template-columns:1.2fr auto;gap:32px;align-items:end}
.lg-sign img{width:clamp(140px,18vw,240px);height:auto;justify-self:end}
.lg-sign hr{margin:22px 0 0;height:2px;background:var(--lg-gold);border:0}
@media (max-width:760px){.lg-sign-in{grid-template-columns:1fr}.lg-sign img{justify-self:start;width:150px}}

.lg-ftr{background:var(--lg-dark);color:var(--lg-on-dark);
  background-image:linear-gradient(180deg,rgba(255,255,255,.05) 0%,rgba(255,255,255,0) 45%);
  padding-block:clamp(40px,4.4vw,64px)}
.lg-ftr-in{display:grid;gap:32px var(--lg-gut);grid-template-columns:repeat(auto-fit,minmax(180px,1fr))}
.lg-ftr h3{margin:0 0 12px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;
  font-weight:600;text-transform:uppercase;letter-spacing:.14em;font-size:var(--lg-fs-xs);color:var(--lg-on-dark-m)}
.lg-ftr ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.lg-ftr a{color:var(--lg-on-dark);text-decoration:none;font-size:var(--lg-fs-base)}
.lg-ftr a:hover{text-decoration:underline;text-underline-offset:4px}
.lg-ftr-base{margin-top:32px;padding-top:20px;border-top:1px solid var(--lg-rule-dark);
  display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between;color:var(--lg-on-dark-m);font-size:var(--lg-fs-base)}

/* ==========================================================================
   MOTION · the system is still. The foil slides on hover, photos ease on
   hover, and that is the whole vocabulary. No scroll reveals, no lifts,
   no drop shadows anywhere.
   ========================================================================== */
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.001ms!important;transition-duration:.001ms!important}
}
```

---

# STEP 2: the markup, component by component

Every class below is in the CSS above. Copy the structure, swap in the
page's own words and images.

### Announcement bar and header

```html
<div class="lg-tick">
  <div class="lg-tick-in">
    <a href="/returns"><b>Sixty days</b> to prove us wrong</a>
    <a href="/shipping">Ships in 1 to 2 business days</a>
    <a href="/wedges">Forged, not cast</a>
  </div>
</div>

<header class="lg-hdr">
  <div class="lg-hdr-in">
    <a class="lg-logo" href="/" aria-label="Lucky Golf home">
      <!-- the LUCKY wordmark, on the LEFT, 132px wide, currentColor -->
      <img src="/lucky-wordmark.svg" alt="Lucky Golf" width="132" height="30">
    </a>
    <nav class="lg-nav" aria-label="Main">
      <a href="/wedges">Wedges</a><a href="/putters">Putters</a>
      <a href="/hybrid">Hybrid</a><a href="/apparel">Apparel</a>
      <a href="/story">Our Story</a>
    </nav>
    <div class="lg-hdr-act">
      <a href="/search" aria-label="Search"><!-- 21px stroke icon --></a>
      <button type="button" aria-label="Open bag">
        <img src="/mags-bag-light.webp" alt="" width="48" height="48">
      </button>
    </div>
  </div>
</header>
```

The header is 72px, solid colour, sticky. Logo left, nav centred, search and
the Mags bag button right. Below 980px the nav hides behind a burger in
`.lg-hdr-act` and the bar shows only its first claim.

### Hero: one full-bleed photograph

```html
<section class="lg-hero">
  <img src="/hero.webp" alt="A gold Lucky wedge behind the ball on fairway grass">
  <div class="lg-hero-copy">
    <div class="lg-wrap">
      <p class="lg-eyebrow">The Carver 01</p>
      <h1 class="lg-d1">Golf has a dress code.<br>Ours is <span class="lg-foil-word">gold.</span></h1>
      <p class="lg-lede">One sentence that says what it is and what it costs.</p>
      <div class="lg-btn-row">
        <a class="lg-btn" href="#buy">Shop the Carver <span aria-hidden="true">&rarr;</span></a>
        <a class="lg-btn lg-btn-line" href="#grinds">See the grinds</a>
      </div>
    </div>
  </div>
</section>
```

Headline bottom left over the scrim. One photo, no slider, no video
background, no text centred in the middle of the image.

### Trust row

```html
<div class="lg-wrap">
  <div class="lg-trust">
    <span><svg viewBox="0 0 24 24"><!-- 20px stroke icon --></svg>Sixty days to decide</span>
    <span>...</span><span>...</span><span>...</span>
  </div>
</div>
```

### A white section with product cards

```html
<section class="lg-sec">
  <div class="lg-wrap">
    <p class="lg-eyebrow">The line</p>
    <h2 class="lg-d2">Four clubs. No <span class="lg-foil-word">filler.</span></h2>
    <p class="lg-body">One or two sentences. Never a wall.</p>

    <div class="lg-grid" style="margin-top:36px">
      <a class="lg-card" href="/carver">
        <span class="lg-card-ph"><img src="/carver.webp" alt="Carver 01 Gold wedge"></span>
        <span class="lg-card-bd">
          <span class="lg-card-nm">Carver 01 Gold</span><span class="lg-card-pr">$99</span>
          <span class="lg-card-ln">One line on what the club is for.</span>
        </span>
      </a>
      <!-- more cards -->
    </div>
  </div>
</section>
```

A card is: photo on stone, name, price, one line. Nothing else goes on it.

### The one dark band (the argument)

```html
<section class="lg-band">
  <div class="lg-wrap">
    <p class="lg-eyebrow">Different math</p>
    <h2 class="lg-d2">Same steel as the big names.<br>A <span class="lg-foil-word">third</span> of the counter price.</h2>
    <p class="lg-lede">Why the price is what it is, in one sentence.</p>
    <div class="lg-grid" style="margin-top:36px">
      <div class="lg-band-tile">
        <p class="lg-label" style="color:var(--lg-gold)">Forged, not cast</p>
        <p class="lg-body" style="margin-top:8px">Two lines, maximum.</p>
      </div>
      <!-- two more -->
    </div>
    <div class="lg-btn-row"><a class="lg-btn" href="#buy">Shop the line</a></div>
  </div>
</section>
```

One band per page. It sits low, after the offer, before the proof.

### Proof: a real review, a real number, a missing photo

```html
<figure class="lg-quote">
  <span class="lg-stars" aria-label="5 out of 5"><svg viewBox="0 0 24 24">...</svg><!-- x5 --></span>
  <p>The review, quoted exactly as the customer wrote it.</p>
  <figcaption class="lg-meta">David L. <span class="lg-tag lg-tag-ok">Verified</span></figcaption>
</figure>

<div class="lg-stat"><b>60 days</b><span>To decide, on your own course.</span></div>

<div class="lg-slot">Photo slot: Carver 01 at address, low angle, morning light.</div>
```

`.lg-slot` is what a photo we do not have yet looks like: a labelled slot
carrying the shot brief. Never a grey box, never a stock photo.

### Small parts

```html
<span class="lg-tag">New</span>
<span class="lg-tag lg-tag-gold">Best seller</span>
<span class="lg-stock">In stock</span>
<button class="lg-chip" type="button" aria-pressed="false">54&deg;</button>
<table class="lg-table">...</table>
```

### Sign-off and footer

```html
<section class="lg-sign">
  <div class="lg-wrap lg-sign-in">
    <div>
      <p class="lg-eyebrow">The last word</p>
      <h2 class="lg-d2">&ldquo;It&rsquo;s better<br>to be <span class="lg-foil-word">lucky.</span>&rdquo;</h2>
      <p class="lg-lede">One line of charm.</p>
      <div class="lg-form">
        <input class="lg-input" type="email" placeholder="you@email.com" autocomplete="email">
        <button class="lg-btn" type="submit">Keep me posted</button>
      </div>
      <hr>
    </div>
    <img src="/mags-light.webp" alt="Mags, the magpie, with a gold wedge">
  </div>
</section>

<footer class="lg-ftr">
  <div class="lg-wrap">
    <div class="lg-ftr-in"><!-- four columns: h3 + ul of links --></div>
    <div class="lg-ftr-base"><span>&copy; 2026 Lucky Golf</span><span>It&rsquo;s better to be lucky.</span></div>
  </div>
</footer>
```

Mags is cream artwork on dark grounds and ink artwork on white ones. If you
do not have the file, leave a labelled slot and say so.

---

# STEP 3: page order

```
announcement bar  (solid, three claims, first one gold)
header            (logo left, nav centre, search and bag right, 72px, solid)
hero              (one full-bleed photograph, headline bottom left)
trust row         (four facts, hairline top and bottom)
the offer         (cards on stone, or a two-up with one photo)
ONE dark band     (the argument: why the price is what it is)
proof             (real reviews, a real number, a compare table)
sign-off          (the brand line, the email capture, Mags on a gold rule)
footer            (solid, links, one hairline)
```

No two dark sections touch. The page always comes back to white.

---

# STEP 4: the rules, the colour maths and the voice

Everything below is the system document. Follow it exactly.

## The brand in one line

Gold clubs, honest prices, a magpie called Mags. Serious about the clubs,
not that serious about ourselves. Premium with attitude, never templated,
never fake.

The two legs of every Lucky argument, and there is no third:

1. **You are not overpaying.** Same materials and engineering as the big
   names, minus tour contracts and retail rent, sold direct.
2. **You are not blending in.** Gold, on purpose, because golf got too
   serious and we did not.

If a line would sit unchanged on a competitor's site, it is wrong for us.

---

### Colour: one dark, one accent, and a lot of white

| Role | Value | The one job | Roughly how much of a screen |
|---|---|---|---|
| The page | `#FFFFFF` | Everything reads here | 78 to 88% |
| Photography | the shots | The only other big field | 6 to 22% |
| Deep green | `#0B2E1F` | Announcement bar, header, the band low on the page, the sign-off, the footer | 3 to 12% |
| Stone | `#F4F3F0` | Product wells, cards, table fills. A material, never a band | under 5% |
| Ink | `#17140F` | All text on white. Body at 70%, meta at 64% | type only |
| Gold | `#C29A2B` | The only accent: buttons, one word per headline, stars, hairline marks | under 1.5% |
| Gold as type | `#8A6A1C` | Eyebrows and links on white. The only gold you set text in on white | type only |
| Signal green | `#008340` | In stock, added, verified. Never decoration | tiny |
| Clover green | `#0B5130` | The clover inside the logo. Nowhere else | tiny |

Those percentages are measured off the live pages, not aspirational. If your
page is 30% dark green, it is not this system.

**What is gone, on purpose:** cream fields, brown, the old clover-green
masthead, a second green, any third colour. The old palette failed because
cream, green and brown were all fighting. One dark, one accent, white.

**Contrast, measured (not guessed):**

| Pair | Ratio |
|---|---|
| Cream `#F4F3F0` on deep green | 13.3:1 |
| Gold `#C29A2B` on deep green | 5.6:1 |
| Gold as type `#8A6A1C` on white | 5.1:1 |
| Ink on the foil button (darkest stop) | 7.0:1 |
| Stars `#9A7619` on white (a graphic, 3:1 floor) | 4.2:1 |
| **Gold on clover green `#0B5130`, BANNED** | 3.6:1 |

Floor: 4.5:1 for body, 3:1 for display and graphics. Measure it before you
hand anything back.

### The foil
Gold as a material, not a flat fill: `#C29A2B` to `#EDD27C` and back. It
appears in exactly two places per view: **the primary button**, and **one
display word** ("Ours is **gold**", "to be **lucky**"). Never at body size,
never as a background field, never twice in the same headline.

### The pinstripe
1px cream lines at 10%, every 6px, drawn as a tile (a long CSS gradient
rasterises unevenly and the lines look crooked). It goes on **dark feature
bands and the sign-off only**. The announcement bar, the header and the
footer are solid, because they sit over everything and should stay quiet.
The footer gets a soft light from the top edge instead.

---

### Type: Archivo, nothing else

Load the variable font with width and weight axes. Three registers:

- **Display**: width 62, weight 800, uppercase, line height .9. Headlines
  and card names. Balance the line breaks by hand.
- **Labels**: width 78, weight 600, uppercase, tracked .12em to .2em.
  Eyebrows, chips, tags, table heads, trust rows, the announcement bar.
- **Body**: width 100, 17px, ink at 70%, 46 to 62 characters a line.

The eyebrow is a 22px gold rule plus a label. It orients the section; it
never restates the headline. No exclamation marks, no all caps for emphasis
inside a sentence.

---

### The six devices. A page missing them reads generic

1. **Foil** on one word and one button.
2. **Mags**, the magpie, as an emblem: on the bag button and at the
   sign-off. Never a cartoon with a face doing an action. Cream artwork on
   dark grounds, ink artwork on white ones. Folklore stays folklore
   ("legend has it").
3. **The pinstripe** on the dark bands, one hairline between page sections.
4. **The stamp**: condensed caps on chips, tags, tables and trust rows.
5. **The aside**: one line of charm, sentence case. "Nobody needs a gold
   wedge. That is rather the point."
6. **The eyebrow** leading every section.

---

### Layout and rhythm

Content width 1180px. Sections 64 to 112px apart. Radius 6px on controls,
14px on surfaces. Everything tappable is at least 44px on a phone. Photos
never round themselves inside an already rounded card.

Page order that works, and the one a landing page should follow:

```
announcement bar  (solid, three claims, first one gold)
header            (logo LEFT, nav centre, search + Mags bag right, 72px)
hero              (one full-bleed photograph, headline bottom left)
trust row         (four facts, hairline top and bottom)
the offer         (cards on stone, or a two-up with one photo)
ONE dark band     (the argument: why the price is what it is)
proof             (real reviews, a real number, a compare table)
sign-off          (the brand line, the email capture, Mags on a gold rule)
footer            (solid, links, one hairline)
```

No two dark bands touch. The page never goes dark for more than one
section at a time, and it always comes back to white.

**Motion is still.** The foil slides on hover, photos ease on hover. No
scroll reveals, no card lifts, no drop shadows anywhere.

---

### Imagery

Three formats and nothing else: **full bleed** for the hero and the band,
**4:5 frames** for course photography, **4:5 tiles** for product on stone.

Real gold catching real light, never a render. A photograph that does not
exist yet is a **labelled slot** carrying the shot brief (`.lg-slot`), never
a grey box, never a stock photo, never a placeholder from another brand.

---

### How Lucky sounds

Someone talking, not copy. Confident without straining, warm without
trying, sharp without needing to prove it. Simple language any golfer
understands. When something bold gets said, it gets said plainly, because
the size of the claim carries it.

The voice has range: bold, plainspoken, dry. Same person at different
volumes; the piece picks the volume. A hero can be bold. A spec block is
plainspoken. A closer is often quiet.

**The test: attitude with receipts.** Every swagger line has to land on
something real, a product, a price, a thing that happened. "Golf has a
dress code. Ours is gold" works. Attitude with nothing behind it is noise.

**The failure mode to write against** is the flat double-statement: one
plain sentence followed by another plain sentence with nobody home in
between. If a line could open an investor deck, it is not Lucky. If it
sounds like the funniest guy in your foursome telling the truth, it is.

Approved lines, verbatim, for calibration:

- "Golf has a dress code. Ours is gold."
- "Great clubs got too expensive. We took it personally."
- "Same steel as the big names. Different math."
- "Serious about the clubs. Not that serious about ourselves."

### Hard rules, no exceptions

- **No em dashes.** Anywhere, in any copy.
- **No invented numbers.** No price, percentage or multiplier that is not
  in the Product Reference Guide. Counts round down.
- **No fabricated reviews, names or photos.** A review is quoted exactly as
  the customer wrote it, typos and all, with their real name and a verified
  mark, or it does not appear.
- **Trust claims stay vague.** "Thousands of happy golfers" and "sixty days
  to decide" are approved shapes. Counted claims are not.
- **The founder is never named**, and a review that names him cannot be
  quoted.
- **No competitor named.** The phrase is "the big names".
- **Banned words:** premium, luxury, revolutionary, cheap, tour-proven.
  "Tour-quality construction" is allowed. No warranty language.
- **No process vocabulary** in brand copy. A page never narrates how it
  was built.
- Never write a spec from memory. Open the Product Reference Guide.

---

### Using `lucky.css`

```html
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="lucky.css">
<body class="lg">   <!-- or put class="lg-scope" on a wrapper -->
```

The parts, all in `kit.html`:

| Class | What it is |
|---|---|
| `.lg-tick` / `.lg-tick-in` | announcement bar |
| `.lg-hdr` / `.lg-hdr-in` / `.lg-logo` / `.lg-nav` / `.lg-hdr-act` | the header |
| `.lg-hero` + `.lg-hero-copy` | full-bleed photo hero with the scrim |
| `.lg-wrap` / `.lg-sec` | the 1180px measure and section spacing |
| `.lg-d1` `.lg-d2` `.lg-d3` `.lg-foil-word` | display type |
| `.lg-eyebrow` `.lg-lede` `.lg-body` `.lg-meta` `.lg-aside` `.lg-label` `.lg-link` | text |
| `.lg-btn` (foil) `.lg-btn-line` (ghost) `.lg-btn-row` | buttons |
| `.lg-band` `.lg-band-tile` | the dark band and its inner tiles |
| `.lg-grid` `.lg-card` `.lg-tile` `.lg-slot` `.lg-quote` `.lg-stat` | surfaces |
| `.lg-tag` `.lg-tag-gold` `.lg-tag-ok` `.lg-chip` `.lg-stock` `.lg-stars` `.lg-trust` `.lg-table` | small parts |
| `.lg-form` `.lg-input` | email capture |
| `.lg-sign` `.lg-ftr` | sign-off and footer |
| `.lg-on-dark` | put it on anything you build over a dark field |

To test another colour system, change one token: `--lg-dark`. Ink & gold is
`#17140F`; White & gold keeps the bands white and uses `#121212` for the
footer. Deep green is the pick being tested.

---

### Before you hand anything back

1. One foil button and one foil word per view, not five.
2. Any gold type on green? Fix it.
3. Contrast measured, not guessed.
4. Is the page still mostly white, with one dark band?
5. Every card on stone; every missing photo a labelled slot.
6. Every review, name and number real. No em dashes.
7. Would this sit next to the Carver 01 page and read as the same brand?
   If not, start over.
