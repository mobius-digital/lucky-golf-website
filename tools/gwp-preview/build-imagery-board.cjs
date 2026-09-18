/* The imagery-led system board: rules, both grounds, the promo page rebuilt
   around real photography (desktop + phone, Daylight + Twilight), and the shot
   list. Output: design/imagery-led-system.html (one file). */
const fs = require('fs'), path = require('path');
const ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const cdn = (f, w) => `https://cdn.shopify.com/s/files/1/2286/3149/files/${f}?width=${w || 1600}`;
const b64 = f => 'data:image/webp;base64,' + fs.readFileSync(path.join(ROOT, 'handoff/img', f)).toString('base64');

const IMG = {
  heroFairway: cdn('11_26414fab-14b8-41ae-8ad7-a801c2f646fb.webp', 2000),   // Carver on the fairway, ball
  overShoulder: cdn('9_e72fa738-81c3-4ee6-9013-c8ca2a153745.webp'),        // Carver over a shoulder
  ballClose: cdn('12_5bea3d04-db05-40df-b68e-c408d3d70b9c.webp'),
  bridge: cdn('10_eb0cd992-4e1f-4285-8b83-8a351d94d640.webp'),
  noParking: cdn('13_e0814fc8-9c00-480c-9771-fe9a8847b5ff.webp'),
  strykerCourse: cdn('11_0464f85e-ccad-487c-bb2a-1c0a5c7b673c.webp'),
  strykerSwing: cdn('12_65f3a9e3-d92c-481b-87b0-85ac2eb90294.webp'),
  malletGreen: cdn('8_a32edd17-2924-472d-8767-0919e47bff83.webp'),
  malletFlag: cdn('Copy_of_LGP02_1.webp'),
  puttersGreen: cdn('2_a3a63c64-3884-4a7c-8adc-f95c92fcd0dd.webp', 2000),
  puttersHand: cdn('PSI-98004-1_bcc3fa37-0dd1-47cc-81ce-5c929821ec59.jpg'),
  hatMacro: cdn('13_b1b79d81-b615-4691-873e-baca22201025.webp'),
  poloDetail: cdn('Blackwhiteflower3.webp'),
  dustDetail: cdn('PaintSplatter3.webp'),
  cutCarver: cdn('6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp', 600),
  cutStryker: cdn('6_f5a07216-0d65-4efc-913f-c5d2d1d9afbe.webp', 600),
  cutMallet: cdn('Copy_of_LGP02.webp', 600),
  cutBlack: cdn('1_870950d7-2758-44d5-be0f-d3bd0f03996b.webp', 600),
  cutHat: cdn('10_96db47c0-e327-4f91-b46b-2f1caced97cf.webp', 600),
  cutPolo: cdn('Classicpolowithlogointhecollar1.webp', 600),
  address: b64('lucky-carver-gold-address.webp'),
  sand: b64('lucky-wedge-sole-turf.webp')
};

const SHOOT_DIR = path.join(ROOT, 'design/img/shoot-0918');
const SHOOT = ['green-read-fit', 'fit-sunset', 'fit-sunset-down', 'swing-black-wedge', 'two-gold-wedges', 'black-hat-mallet',
  'two-hats-mallet', 'gold-wedge-bag', 'putt-sunset', 'from-the-cup', 'putter-in-hand', 'walk-off-green'];
const SHOOT_CSS = SHOOT.map(n => `.s-${n}{background-image:url(data:image/webp;base64,${fs.readFileSync(path.join(SHOOT_DIR, n + '.webp')).toString('base64')})}`).join('\n');
const ph = (n, cls = '', pos = 'center') => `<div class="bgph s-${n} ${cls}" style="background-position:${pos}"></div>`;

/* ---------- one page mock, rendered per ground; container queries make the phone version ---------- */
const slot = (label, brief, cls = '') => `<div class="slot ${cls}"><span class="slot-tag">SHOT NEEDED</span><b>${label}</b><span>${brief}</span></div>`;
const page = () => `
<div class="pg">
  <div class="nav"><b>L&#9827;CKY</b><span>Wedges · Putters · Hybrid · Apparel</span><i>Bag</i></div>

  <section class="hero s-green-read-fit">
    <div class="hero-in">
      <p class="eb">One week only · Ends Friday, Sept 25</p>
      <h1><em>$90</em> gets the hat.<br><em>$140</em> gets the fit.</h1>
      <p class="lede">The fit's a hat and a polo, both on us. Every club here gets you the hat on its own.</p>
      <a class="btn">Show me the clubs →</a>
    </div>
  </section>

  <div class="math">
    <div class="m"><img src="${IMG.cutCarver}" alt=""><span>+</span><img src="${IMG.cutHat}" alt=""><span>=</span><b>$99</b><small>Any club gets the hat</small></div>
    <div class="m"><img src="${IMG.cutStryker}" alt=""><span>+</span><img src="${IMG.cutHat}" alt=""><img src="${IMG.cutPolo}" alt=""><span>=</span><b>$209</b><small>Over $140, the polo too</small></div>
  </div>

  <div class="rail"><span class="say">Your bag's empty. $90 gets you a free hat.</span><div class="track"><i style="left:45%"></i><i style="left:70%"></i><i style="left:100%"></i><span class="ball"></span></div></div>

  <section class="sec">
    <p class="eb">01 · Start here</p><h2>Every one of these gets you a hat</h2>
    <div class="clubs">
      ${[['Carver 01 Gold', '$99', IMG.cutCarver], ['Carver 01 Black', '$109', IMG.cutBlack], ['Tracer Mallet', '$229', IMG.cutMallet], ['Stryker LGH01', '$209', IMG.cutStryker]]
        .map(([t, p, i]) => `<div class="card"><div class="ph"><img src="${i}" alt=""></div><b>${t}</b><span>${p}</span></div>`).join('')}
    </div>
  </section>

  <section class="band">
    <figure class="w2">${ph('two-gold-wedges')}</figure>
    <figure>${ph('black-hat-mallet', '', '30% center')}</figure>
    <figure>${ph('gold-wedge-bag', '', '45% center')}</figure>
  </section>

  <section class="sec fit">
    <figure class="fit-ph">${ph('fit-sunset', '', '52% center')}<figcaption>The fit: hat + polo, both free over $140</figcaption></figure>
    <div class="fit-copy">
      <p class="eb">02 · The free stuff</p><h2>Pick your hat. Then your polo.</h2>
      <p class="body">They unlock as your bag fills up. Take the one you'd actually wear.</p>
      <div class="gifts">
        <div class="gift"><div class="ph"><img src="${IMG.cutHat}" alt=""></div><b>Your hat</b><span>Free at $90</span></div>
        <div class="gift"><div class="ph"><img src="${IMG.cutPolo}" alt=""></div><b>Your polo</b><span>Free at $140</span></div>
      </div>
      <div class="swatch-row"><img src="${IMG.hatMacro}" alt=""><img src="${IMG.poloDetail}" alt=""><img src="${IMG.dustDetail}" alt=""></div>
    </div>
  </section>

  <section class="reviews s-putt-sunset">
    <div class="rv-in">
      <p class="eb">03 · Overheard</p><h2>People keep borrowing them</h2>
      <div class="quotes">
        <figure><blockquote>People borrow it in my league- it's a winner!</blockquote><figcaption>Ray O. · Carver 01 Gold</figcaption></figure>
        <figure><blockquote>This club is MONEY!!' Please make a 3 wood!</blockquote><figcaption>Jeff C. · Stryker</figcaption></figure>
        <figure><blockquote>Amazing Putter and looks awesome</blockquote><figcaption>Arthur V. · Tracer Mallet</figcaption></figure>
      </div>
    </div>
  </section>

  <section class="sec faq">
    <div><p class="eb">04 · Before you ask</p><h2>The fine print, short</h2>
      <p class="q">When does it end? <span>Friday, Sept 25.</span></p><p class="q">Do they stack? <span>Not two hats. Nice try.</span></p></div>
    <figure class="faq-ph">${ph('from-the-cup', '', '40% center')}</figure>
  </section>
</div>`;

const HTML = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Imagery-Led System</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..900&display=swap" rel="stylesheet">
<style>
:root{--ink:#17140F;--page:#FFFFFF;--tile:#F4F3F0;--gold:#C29A2B;--gold-t:#8A6A1C;--green:#0B2E1F;--night:#06110B}
*{box-sizing:border-box}
body{margin:0;background:#EDEBE6;color:var(--ink);font:16px/1.5 Archivo,system-ui,sans-serif}
.doc{max-width:1320px;margin:0 auto;padding:40px 24px 80px}
.doc>h1{font:800 44px/0.95 Archivo;font-variation-settings:'wdth' 62;text-transform:uppercase;margin:0 0 10px}
.doc>p.sub{max-width:70ch;color:#4a463f;margin:0 0 28px;font-size:17px}
.doc h2.h{font:800 28px/1 Archivo;font-variation-settings:'wdth' 62;text-transform:uppercase;margin:56px 0 6px}
.doc p.hs{margin:0 0 20px;color:#555;max-width:72ch}
.rules{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.rule{background:#fff;border-radius:14px;padding:18px}
.rule b{display:block;font:800 18px/1.1 Archivo;font-variation-settings:'wdth' 70;text-transform:uppercase;margin-bottom:6px}
.rule span{color:#555;font-size:15px}
.rule.lead{background:var(--night);color:#F4F3F0}.rule.lead span{color:rgba(244,243,240,.75)}
.grounds{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.gcard{border-radius:16px;overflow:hidden;background:#fff}
.gcard .gh{padding:18px 20px}
.gcard .gh b{font:800 22px/1 Archivo;font-variation-settings:'wdth' 62;text-transform:uppercase}
.gcard .gh p{margin:6px 0 0;font-size:14px;color:#555}
.chips{display:flex;gap:8px;padding:0 20px 16px;flex-wrap:wrap}
.chips span{display:flex;align-items:center;gap:6px;font-size:12px;color:#555}
.chips i{width:22px;height:22px;border-radius:6px;border:1px solid rgba(0,0,0,.1)}
.rhythm{display:grid;gap:4px;padding:0 20px 20px}
.rhythm div{border-radius:6px;font:700 11px/1 Archivo;letter-spacing:.08em;text-transform:uppercase;display:flex;align-items:center;padding:0 10px}
.rhythm .p{height:54px;background-size:cover;background-position:center;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6)}
.rhythm .c{height:30px}
.gcard.tw{background:var(--night);color:#F4F3F0}.gcard.tw .gh p,.gcard.tw .chips span{color:rgba(244,243,240,.7)}
.gcard.day .rhythm .c{background:var(--tile);color:#555}.gcard.tw .rhythm .c{background:#0B1911;color:rgba(244,243,240,.6);border:1px solid rgba(237,210,124,.2)}

/* mock frames */
.frames{display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start}
.frame-l{font:700 12px/1 Archivo;letter-spacing:.1em;text-transform:uppercase;color:#555;margin:0 0 8px}
.shot{width:600px;border-radius:14px;overflow:hidden;box-shadow:0 1px 0 rgba(0,0,0,.06);background:#fff}
.desk{width:1200px;zoom:.5}
.phonewrap{display:flex;gap:16px;margin-top:16px}
.phone{width:390px;border-radius:28px;overflow:hidden;border:8px solid #17140F;zoom:.75}
.mock{container-type:inline-size}
.shot{max-width:100%}
@media (max-width:1100px){.frames,.grounds{grid-template-columns:1fr}.desk{zoom:.3}.shot{width:360px}.rules{grid-template-columns:1fr}}

/* ---- the page mock ---- */
.pg{--bg:#fff;--fg:#17140F;--mut:rgba(23,20,15,.64);--card:#F4F3F0;--line:rgba(23,20,15,.12);--gt:#8A6A1C;
  --num:linear-gradient(180deg,#C29A2B,#B8912A 38%,#8A6A1C 78%,#A8821C);background:var(--bg);color:var(--fg);font-family:Archivo,sans-serif}
.tw .pg{--bg:#06110B;--fg:#F4F3F0;--mut:rgba(244,243,240,.72);--card:#0B1911;--line:rgba(237,210,124,.18);--gt:#EDD27C;
  --num:linear-gradient(180deg,#FFF3C4,#EDD27C 40%,#C29A2B 78%,#EDD27C)}
.pg .nav{display:flex;align-items:center;gap:28px;padding:18px 40px;background:#fff;color:#17140F;border-bottom:1px solid rgba(0,0,0,.08)}
.pg .nav b{font:800 22px Archivo;letter-spacing:.14em;color:#0B5130}.pg .nav span{font-size:13px;color:#555;flex:1}.pg .nav i{font-style:normal;font-size:13px}
.pg .eb{font:600 12px/1 Archivo;letter-spacing:.16em;text-transform:uppercase;color:var(--gt);margin:0 0 12px;display:flex;gap:10px;align-items:center}
.pg .eb::before{content:'';width:22px;height:2px;background:var(--gold)}
.pg h1,.pg h2{font-family:Archivo;font-variation-settings:'wdth' 62;font-weight:800;text-transform:uppercase;line-height:.9;margin:0;color:inherit}
.pg h2{font-size:48px}
.pg em{font-style:normal;background:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent}
.pg .btn{display:inline-block;background:linear-gradient(96deg,#C29A2B,#EDD27C 50%,#C29A2B);color:#17140F;font:700 14px Archivo;letter-spacing:.08em;text-transform:uppercase;padding:16px 26px;border-radius:12px;margin-top:22px}
.pg .body{color:var(--mut);max-width:44ch;font-size:17px;margin:12px 0 0}
.hero{position:relative;min-height:640px;background-size:cover;background-position:center 60%;display:flex;align-items:flex-end}
.hero::before{content:'';position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.72) 0%,rgba(0,0,0,.25) 45%,transparent 70%)}
.hero-in{position:relative;padding:56px 56px;color:#fff}.hero-in .eb{color:#EDD27C}
.hero h1{font-size:92px}.hero h1 em{background:linear-gradient(180deg,#FFF3C4,#EDD27C 40%,#C29A2B 78%,#EDD27C);-webkit-background-clip:text;background-clip:text}
.hero .lede{max-width:40ch;font-size:19px;color:rgba(255,255,255,.88);margin:16px 0 0}
.math{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:22px 40px;border-bottom:1px solid var(--line)}
.math .m{display:flex;align-items:center;gap:10px;background:var(--card);border-radius:14px;padding:10px 16px}
.math img{width:62px;height:62px;object-fit:contain;background:#F1EEE6;border-radius:10px;mix-blend-mode:normal}
.math span{font:800 22px Archivo;color:var(--gold)}.math b{font:800 34px Archivo;font-variation-settings:'wdth' 62;background:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent}
.math small{color:var(--mut);font-size:13px;margin-left:auto;max-width:14ch;text-align:right}
.rail{padding:14px 40px 18px;border-bottom:1px solid var(--line)}
.rail .say{font:700 15px Archivo;font-variation-settings:'wdth' 80}
.track{position:relative;height:8px;border-radius:4px;margin-top:10px;background:repeating-linear-gradient(90deg,var(--line) 0 1px,transparent 1px 2.5%),var(--card)}
.track i{position:absolute;top:-12px;width:2px;height:20px;background:var(--gold)}
.track i::after{content:'';position:absolute;left:2px;top:0;border:5px solid transparent;border-left:9px solid var(--gold);border-right:0}
.track .ball{position:absolute;left:0;top:50%;width:14px;height:14px;border-radius:50%;background:#fff;border:2px solid var(--fg);transform:translate(-50%,-50%)}
.sec{padding:72px 40px}
.clubs{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:28px}
.card .ph,.gift .ph{aspect-ratio:1;background:#F1EEE6;border-radius:16px;display:flex;align-items:center;justify-content:center;overflow:hidden}
.card img,.gift img{width:82%;height:82%;object-fit:contain}
.card b,.gift b{display:block;margin-top:12px;font:800 18px Archivo;font-variation-settings:'wdth' 70;text-transform:uppercase}
.card span,.gift span{color:var(--mut);font-size:15px}
.band{display:grid;grid-template-columns:2fr 1fr 1fr;gap:6px;height:420px}
.band figure{margin:0;overflow:hidden}.band img{width:100%;height:100%;object-fit:cover}
.fit{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.slot{aspect-ratio:4/5;border-radius:18px;border:2px dashed var(--gold);background:repeating-linear-gradient(135deg,transparent 0 14px,rgba(194,154,43,.08) 14px 28px),var(--card);
  display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:10px;padding:36px;color:var(--fg)}
.slot-tag{font:700 11px Archivo;letter-spacing:.14em;background:var(--gold);color:#17140F;padding:5px 9px;border-radius:6px}
.slot b{font:800 30px/1 Archivo;font-variation-settings:'wdth' 62;text-transform:uppercase}.slot span:last-child{color:var(--mut);max-width:34ch}
.gifts{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:24px}
.swatch-row{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:16px}.swatch-row img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}
.reviews{position:relative;background-size:cover;background-position:center;color:#fff}
.reviews::before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,rgba(6,17,11,.88) 0%,rgba(6,17,11,.6) 60%,rgba(6,17,11,.3))}
.rv-in{position:relative;padding:88px 40px}.rv-in .eb{color:#EDD27C}
.quotes{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:28px}
.quotes figure{margin:0;padding:22px;border-radius:16px;background:rgba(6,17,11,.55);border:1px solid rgba(237,210,124,.25);backdrop-filter:blur(6px)}
.quotes blockquote{margin:0;font-size:19px;line-height:1.35}.quotes figcaption{margin-top:12px;font-size:13px;color:rgba(255,255,255,.7)}
.faq{display:grid;grid-template-columns:1.2fr 1fr;gap:48px;align-items:center}
.faq .q{border-top:1px solid var(--line);padding:16px 0;margin:0;font-weight:700;display:flex;justify-content:space-between;gap:12px}.faq .q span{font-weight:400;color:var(--mut)}
.faq-ph{margin:0;border-radius:18px;overflow:hidden;aspect-ratio:4/5}.faq-ph img{width:100%;height:100%;object-fit:cover}

/* phone layout via container query */
@container (max-width:600px){
  .pg .nav{padding:14px 18px}.pg .nav span{display:none}
  .hero{min-height:560px}.hero-in{padding:28px 20px}.hero h1{font-size:46px}.hero .lede{font-size:16px}
  .math{grid-template-columns:1fr;padding:16px 18px}.math img{width:48px;height:48px}.math small{display:none}
  .rail{padding:12px 18px 16px}.sec{padding:48px 18px}.pg h2{font-size:34px}
  .clubs{grid-template-columns:1fr 1fr;gap:12px}
  .band{grid-template-columns:1fr 1fr;height:auto}.band figure{aspect-ratio:1}.band .w2{grid-column:1/-1;aspect-ratio:16/10}
  .fit,.faq{grid-template-columns:1fr;gap:28px}.slot{padding:24px}.slot b{font-size:24px}
  .quotes{grid-template-columns:1fr}.rv-in{padding:56px 18px}
}

.bgph{width:100%;height:100%;background-size:cover}
.hero,.reviews{background-size:cover}
.hero{background-position:62% 40%}
.reviews{background-position:center 60%}
.fit-ph{margin:0;aspect-ratio:4/5;border-radius:18px;overflow:hidden;position:relative}
.fit-ph figcaption{position:absolute;left:16px;bottom:16px;background:rgba(6,17,11,.72);color:#F4F3F0;font:700 12px Archivo;letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;border-radius:8px}
.band figure{height:100%}
@container (max-width:600px){.hero{background-position:58% center}}
${SHOOT_CSS}
/* shot list */
table{width:100%;border-collapse:collapse;background:#fff;border-radius:14px;overflow:hidden}
th,td{text-align:left;padding:12px 14px;border-bottom:1px solid #eee;font-size:14px;vertical-align:top}
th{font:700 11px Archivo;letter-spacing:.1em;text-transform:uppercase;color:#777;background:#fafaf8}
.p1{background:#17140F;color:#EDD27C;font:700 11px Archivo;padding:3px 7px;border-radius:5px;white-space:nowrap}
.p2{background:#EDD27C;color:#17140F;font:700 11px Archivo;padding:3px 7px;border-radius:5px}
.have{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:8px}.have .bgph{height:auto}.have figure{margin:0}.have img{width:100%;aspect-ratio:1;object-fit:cover;border-radius:10px}
.have figcaption{font-size:11px;color:#555;margin-top:4px}
@media (max-width:900px){.have{grid-template-columns:repeat(4,minmax(0,1fr))}}
</style></head><body><div class="doc">
<h1>Imagery leads. Yardage supports.</h1>
<p class="sub">You were right: the promo page drifted into a data sheet. Every image on it is a product cutout, and the Yardage details ended up carrying the personality. This is the fix: same colours, same type, but photography does the talking and the instruments only show up where there's a real number.</p>

<h2 class="h">The rules</h2>
<div class="rules">
  <div class="rule lead"><b>1 · Every page opens on a photo</b><span>A full-bleed shot of the club (or a person) in the real world, headline over it. Never a grid of cutouts first.</span></div>
  <div class="rule"><b>2 · A photo band every two sections</b><span>The page breathes on photography, not on colour. Two content sections in a row, then a band of real shots.</span></div>
  <div class="rule"><b>3 · Cutouts are for choosing</b><span>Studio cutouts live on cards and pickers. Photos are for wanting. Both, never one without the other.</span></div>
  <div class="rule"><b>4 · Yardage only on real numbers</b><span>The progress bar and the tracer. No contour wallpaper, no rulers as decoration.</span></div>
  <div class="rule"><b>5 · Gold is metal first</b><span>The gold should come from the clubs in the photos. The gradient is for prices and one button.</span></div>
  <div class="rule"><b>6 · Real people, our gear</b><span>No competitor logos on anyone. A person in a Nike polo never goes big. That's the biggest gap to shoot.</span></div>
</div>

<h2 class="h">Two grounds, one rhythm</h2>
<p class="hs">The green was too much because nothing broke it up. Same with white: it only reads as a wireframe without photos. With the photo rhythm, either ground works.</p>
<div class="grounds">
  <div class="gcard day"><div class="gh"><b>Daylight · white + gold</b><p>Everyday pages: home, product pages, collections, story.</p></div>
    <div class="chips"><span><i style="background:#fff"></i>Page</span><span><i style="background:#F4F3F0"></i>Tile</span><span><i style="background:#17140F"></i>Ink</span><span><i style="background:#8A6A1C"></i>Gold text</span><span><i style="background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B)"></i>Foil</span></div>
    <div class="rhythm"><div class="p s-green-read-fit" style="background-position:center 35%">Photo hero</div><div class="c">Offer / product</div><div class="c">Product grid</div><div class="p s-two-gold-wedges">Photo band</div><div class="c">Story / pickers</div><div class="p s-putt-sunset">Reviews on a photo</div><div class="c">FAQ</div></div></div>
  <div class="gcard tw"><div class="gh"><b>Twilight round · night green + gold</b><p>Promos, drops, launches. The same rhythm, darker in between.</p></div>
    <div class="chips"><span><i style="background:#06110B"></i>Page</span><span><i style="background:#0B1911"></i>Card</span><span><i style="background:#F4F3F0"></i>Ink</span><span><i style="background:#EDD27C"></i>Gold text</span><span><i style="background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B)"></i>Foil</span></div>
    <div class="rhythm"><div class="p s-green-read-fit" style="background-position:center 35%">Photo hero</div><div class="c">Offer / product</div><div class="c">Product grid</div><div class="p s-two-gold-wedges">Photo band</div><div class="c">Story / pickers</div><div class="p s-putt-sunset">Reviews on a photo</div><div class="c">FAQ</div></div></div>
</div>

<h2 class="h">The promo page, rebuilt around photos</h2>
<p class="hs">Built on the new shoot (interim edit). The hero is the hat, the polo and a gold putter in one frame, which is the whole offer. The fit section finally shows the gifts worn instead of floating on tiles.</p>
<div class="frames">
  <div><p class="frame-l">Daylight · desktop</p><div class="shot mock day"><div class="desk">${page()}</div></div></div>
  <div><p class="frame-l">Twilight · desktop</p><div class="shot mock tw"><div class="desk">${page()}</div></div></div>
</div>
<div class="phonewrap">
  <div><p class="frame-l">Daylight · phone</p><div class="phone mock day">${page()}</div></div>
  <div><p class="frame-l">Twilight · phone</p><div class="phone mock tw">${page()}</div></div>
</div>

<h2 class="h">Photos we have</h2>
<p class="hs">Top row: the new shoot, interim edit. Below: what's already in your store.</p>
<div class="have">
  ${[['Reading the putt · hero', 'green-read-fit'], ['The fit, low sun', 'fit-sunset'], ['Head down, sun', 'fit-sunset-down'], ['Follow-through, black wedge', 'swing-black-wedge'],
     ['Two gold wedges', 'two-gold-wedges'], ['Black hat + mallet', 'black-hat-mallet'], ['Two hats + mallet', 'two-hats-mallet'], ['Gold wedge on the bag', 'gold-wedge-bag'],
     ['Putting at sunset', 'putt-sunset'], ['Out of the cup', 'from-the-cup'], ['Putter in hand', 'putter-in-hand'], ['Walking off', 'walk-off-green']]
    .map(([c, n]) => `<figure><div class="bgph s-${n}" style="aspect-ratio:1;border-radius:10px"></div><figcaption>${c}</figcaption></figure>`).join('')}
  ${[['Carver on the fairway', IMG.heroFairway], ['Over the shoulder', IMG.overShoulder], ['Gold at address', IMG.address], ['Out of the sand', IMG.sand], ['Stryker on course', IMG.strykerCourse], ['Stryker, swing', IMG.strykerSwing], ['Mallet on the green', IMG.malletGreen], ['Mallet, flag', IMG.malletFlag],
     ['Putters on the green', IMG.puttersGreen], ['Putters in hand', IMG.puttersHand], ['No parking', IMG.noParking], ['On the bridge', IMG.bridge], ['Ball close-up', IMG.ballClose], ['Hat detail', IMG.hatMacro], ['Nightshade detail', IMG.poloDetail], ['Gold Dust detail', IMG.dustDetail]]
    .map(([c, s]) => `<figure><img src="${s.includes('cdn.shopify') ? s.replace(/width=\d+/, 'width=400') : s}" alt=""><figcaption>${c}</figcaption></figure>`).join('')}
</div>

<h2 class="h">Photos we need</h2>
<table>
<tr><th>Priority</th><th>Shot</th><th>Where it goes</th><th>Spec</th></tr>
<tr><td><span class="p2">done</span></td><td><b>The fit, worn.</b> Covered by the new shoot (one golfer, two looks). Still want a second person for range.</td><td>Promo hero, fit section, apparel pages, ads</td><td>Final edit from your creative director</td></tr>
<tr><td><span class="p1">1</span></td><td><b>Hats on heads.</b> 3–4 designs, close, over the shoulder on course.</td><td>Hat picker, hat pages, BOGO page</td><td>4:5</td></tr>
<tr><td><span class="p1">1</span></td><td><b>Polos on body.</b> The 13 designs, one each (already on the shot list, Session B).</td><td>Polo picker, 13 polo pages</td><td>4:5, same light for all</td></tr>
<tr><td><span class="p2">2</span></td><td><b>The bundle.</b> Club + hat + polo laid out on a bench or tailgate. "This is what shows up."</td><td>Promo hero alternative, email, ads</td><td>1:1 and 16:9</td></tr>
<tr><td><span class="p2">2</span></td><td><b>The foursome.</b> Friends on the tee, someone borrowing the gold wedge (the review line, acted out).</td><td>Reviews band, home, story</td><td>16:9 wide</td></tr>
<tr><td><span class="p2">2</span></td><td><b>Gold out of the bag.</b> Carver caught in low sun as it comes out on the tee box.</td><td>Carver page hero, home</td><td>4:5 portrait</td></tr>
<tr><td><span class="p2">3</span></td><td><b>Mags in the wild.</b> The bag tag or headcover on a real bag.</td><td>Sign-offs, 404, empty cart</td><td>1:1</td></tr>
</table>
</div></body></html>`;

fs.writeFileSync(ROOT + '/design/imagery-led-system.html', HTML);
const head = HTML.slice(0, HTML.indexOf('<body>'));
for (const g of ['day', 'tw']) {
  fs.writeFileSync(ROOT + `/design/mock-${g}.html`, head + `<body style="margin:0;background:#fff"><div class="mock ${g}">${page()}</div></body></html>`);
}
console.log('wrote design/imagery-led-system.html', Math.round(HTML.length / 1024) + 'KB');
