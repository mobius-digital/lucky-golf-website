/* The full page, three "feels" and three headlines, switchable live.
   Builds on build3.cjs (real products, real prices, real photos, working
   cart), swaps the hero for option D (the math), and layers each feel over
   lucky.css as a scoped skin: html[data-feel="light|dark|yard"].
   Gradient stops were measured first:
     on white, nothing lighter than #A8821C (3.57:1, the large-text floor)
     on the dark, #FFF3C4 down to #C29A2B (5.6:1 and up)                   */
const fs = require('fs'), path = require('path'), cp = require('child_process');
const H = __dirname, ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
cp.execSync('node build3.cjs', { cwd: H, stdio: 'inherit' });
let html = fs.readFileSync(path.join(H, 'index.html'), 'utf8');

const LIVE = JSON.parse(fs.readFileSync(path.join(H, 'data', 'live-products.json'), 'utf8')).products;
const P = {}; LIVE.forEach(p => P[p.handle] = p);
const im = (h, n, w) => P[h].images[n - 1].src.split('?')[0] + '?width=' + w;
const HAT = P['black-gold-classic-lucky-hat'].images[0].src.split('?')[0];
const POLO = P['gold-dust-classic-polo'].images[0].src.split('?')[0];

/* ---- the three headlines. Numbers carry the gradient; the tiers are the story ---- */
const HEADS = {
  1: { h: '<span class="gwp-num">$90</span> gets the hat. <span class="gwp-num">$140</span> gets the fit.',
       l: "The fit's a hat and a polo, both on us, both your pick. Every club here gets you the hat on its own." },
  2: { h: 'The more you bag, the more you <span class="gwp-num">wear</span>.',
       l: "Spend $90 and the hat's on us. Hit $140 and the polo comes with it. Your pick on both." },
  3: { h: 'Hit <span class="gwp-num">$90</span>, the hat\'s yours. Hit <span class="gwp-num">$140</span>, grab the polo too.',
       l: 'Every club on this page clears the first one. The Mallet and the Stryker clear both.' }
};

const ICON = {
  lock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>',
  back: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 1 0 2.6-6.4"/><path d="M3 4v5h5"/></svg>',
  ship: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 7h11v9H2z"/><path d="M13 10h4l3 3v3h-7z"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg>'
};

const hero = `<section class="gs-hero" id="gs-hero">
  <div class="lg-wrap">
    <p class="lg-eyebrow">This weekend only · Ends Sunday, Sept 20</p>
    <h1 class="lg-d1 gs-h1" id="gs-h1">${HEADS[1].h}</h1>
    <p class="lg-lede gs-lede" id="gs-lede">${HEADS[1].l}</p>
    <div class="gs-sums">
      <div class="gs-sum">
        <figure class="gs-tile"><img src="${im('lucky-golf-lgw02-gold', 5, 700)}" alt="Carver 01 Gold"><span class="lg-tag">$99</span><figcaption class="lg-label">Carver 01 Gold</figcaption></figure>
        <span class="gs-op" aria-hidden="true">+</span>
        <figure class="gs-tile"><img src="${HAT}?width=600" alt="Lucky hat"><span class="lg-tag lg-tag-gold">Free</span><figcaption class="lg-label">Any hat</figcaption></figure>
        <span class="gs-op gs-eq" aria-hidden="true">=</span>
        <div class="gs-res"><b class="gwp-num-d">$99</b><span>Any club gets you the hat.</span></div>
      </div>
      <div class="gs-sum">
        <figure class="gs-tile"><img src="${im('lucky-striker-hybrid-limited-edition', 5, 700)}" alt="Stryker hybrid"><span class="lg-tag">$209</span><figcaption class="lg-label">Stryker</figcaption></figure>
        <span class="gs-op" aria-hidden="true">+</span>
        <figure class="gs-tile gs-pair"><img src="${HAT}?width=500" alt="Lucky hat"><img src="${POLO}?width=500" alt="Gold Dust polo"><span class="lg-tag lg-tag-gold">Both free</span><figcaption class="lg-label">The fit: hat + polo</figcaption></figure>
        <span class="gs-op gs-eq" aria-hidden="true">=</span>
        <div class="gs-res"><b class="gwp-num-d">$209</b><span>Over $140 the polo comes too. Over $198, shipping's free.</span></div>
      </div>
    </div>
    <div class="gs-foot">
      <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">Show me the clubs <span aria-hidden="true">&rarr;</span></a>
      <ul class="gs-trust" role="list">
        <li class="lg-label">${ICON.lock}Secure checkout</li>
        <li class="lg-label">${ICON.back}Sixty days to prove us wrong</li>
        <li class="lg-label">${ICON.ship}Free shipping over $198</li>
      </ul>
    </div>
  </div>
</section>`;

const before = html.length;
html = html.replace(/<section class="lg-hero gwp-hero">[\s\S]*?<\/section>/, hero);
if (html.length === before) throw new Error('hero not replaced');

const CSS = `
/* ===================== shared: the hero (option D, the math) ===================== */
.gwp-num,.gwp-num-d{-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.gwp-num{background-image:var(--num)}
.gwp-num-d{background-image:var(--num-d)}
.gs-hero{position:relative;overflow:hidden;padding:clamp(36px,5vw,76px) 0 clamp(34px,4vw,60px)}
.gs-hero .lg-wrap{position:relative;z-index:1}
.gs-h1{font-size:clamp(2.5rem,6vw,5.4rem);max-width:17ch}
.gs-lede{max-width:52ch}
.gs-sums{display:grid;gap:clamp(10px,1.4vw,16px);margin-top:clamp(24px,3.4vw,40px)}
.gs-sum{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1.15fr);align-items:stretch;gap:clamp(8px,1.6vw,20px)}
.gs-tile{position:relative;margin:0;height:clamp(150px,16vw,210px);border-radius:var(--rc);overflow:hidden}
.gs-tile img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;padding:9% 9% 16%}
.gs-pair{display:grid;grid-template-columns:1fr 1fr}
.gs-tile .lg-tag{position:absolute;left:12px;top:12px;z-index:2}
.gs-tile figcaption{position:absolute;left:0;right:0;bottom:0;padding:22px 8px 9px;text-align:center;z-index:2;color:#17140F;
  background:linear-gradient(rgba(255,255,255,0),rgba(255,255,255,.92) 62%)}
.gs-op{align-self:center;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2rem,4vw,3.4rem);line-height:1;
  background-image:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.gs-res{border-radius:var(--rc);padding:clamp(16px,2vw,26px);display:flex;flex-direction:column;justify-content:center;min-height:clamp(150px,16vw,210px)}
.gs-res b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2.6rem,5.2vw,4.8rem);line-height:.86;letter-spacing:-.01em}
.gs-res span{margin-top:8px;font-size:var(--lg-fs-base);line-height:1.4}
.gs-foot{display:flex;flex-wrap:wrap;align-items:center;gap:16px 28px;margin-top:clamp(22px,3vw,34px)}
.gs-trust{display:flex;flex-wrap:wrap;gap:8px 20px;list-style:none;margin:0;padding:0}
.gs-trust li{display:flex;align-items:center;gap:8px;color:var(--lg-ink-64)}
.gs-trust svg{width:16px;height:16px;fill:none;stroke:var(--lg-gold-text);stroke-width:1.8}
@media (max-width:760px){
  .gs-sum{grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);row-gap:10px}
  .gs-eq{display:none}
  .gs-res{grid-column:1/-1;min-height:0}
  .gs-tile{height:150px}
}

/* ===================== FEEL 1 · GOLD LIGHT ===================== */
html[data-feel="light"]{--rc:22px;
  --num:linear-gradient(100deg,#6B4F0E 0%,#A8821C 30%,#7A5C12 52%,#A8821C 76%,#6B4F0E 100%);
  --num-d:linear-gradient(180deg,#FFF3C4 0%,#EDD27C 40%,#C29A2B 78%,#EDD27C 100%)}
[data-feel="light"] .gs-hero{background:radial-gradient(55% 80% at 92% 0%,rgba(237,210,124,.26),transparent 62%),radial-gradient(40% 60% at 0% 100%,rgba(11,46,31,.06),transparent 70%),#fff}
[data-feel="light"] .gs-tile{background:radial-gradient(75% 75% at 50% 45%,#fff 0%,#F4F3F0 72%);border:1px solid rgba(23,20,15,.06)}
[data-feel="light"] .gs-res{color:var(--lg-on-dark);background:radial-gradient(120% 110% at 100% 0%,rgba(237,210,124,.30),transparent 55%),linear-gradient(160deg,#124530 0%,#0B2E1F 55%,#061C12 100%)}
[data-feel="light"] .gs-res span{color:var(--lg-on-dark-m)}
[data-feel="light"] .lg-card-ph{border-radius:var(--rc);background:radial-gradient(75% 70% at 50% 45%,#fff 0%,#F2F0EB 75%);border:1px solid rgba(23,20,15,.05)}
[data-feel="light"] .gwp-gift{border-radius:var(--rc);background:linear-gradient(180deg,#F9F8F5,#F1EFEA)}
[data-feel="light"] .gwp-gift[data-state="open"]{border-color:transparent;box-shadow:0 0 0 1px rgba(194,154,43,.6),0 14px 40px -18px rgba(194,154,43,.55)}
[data-feel="light"] .gwp-swatch{border-radius:12px}
[data-feel="light"] .lg-chip,[data-feel="light"] .gwp-qty{border-radius:10px}
[data-feel="light"] .lg-btn{border-radius:12px;box-shadow:inset 0 1px 0 rgba(255,255,255,.55),0 8px 22px -12px rgba(194,154,43,.7)}
[data-feel="light"] .lg-btn-line{border-radius:12px;box-shadow:none}
[data-feel="light"] .gwp-rail{background:rgba(255,255,255,.74);-webkit-backdrop-filter:saturate(1.6) blur(16px);backdrop-filter:saturate(1.6) blur(16px);border-bottom-color:rgba(23,20,15,.07)}
[data-feel="light"] .gwp-track{height:8px;background:rgba(23,20,15,.07)}
[data-feel="light"] .gwp-fill{background-image:linear-gradient(90deg,#C29A2B,#EDD27C 60%,#C29A2B);box-shadow:0 0 14px rgba(237,210,124,.75)}
[data-feel="light"] .gwp-node[data-hit] i{background:#C29A2B;box-shadow:0 0 10px rgba(237,210,124,.9)}
[data-feel="light"] .lg-band{background:radial-gradient(70% 120% at 88% 0%,rgba(237,210,124,.18),transparent 60%),linear-gradient(170deg,#0F3A27,#0B2E1F 55%,#071F15)}
[data-feel="light"] .gwp-rev{border-radius:var(--rc);background:rgba(255,255,255,.045);border-color:rgba(237,210,124,.2)}
[data-feel="light"] .gwp-bar{background:rgba(255,255,255,.8);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}

/* ===================== FEEL 2 · AFTER DARK ===================== */
html[data-feel="dark"]{--rc:20px;
  --num:linear-gradient(180deg,#FFF3C4 0%,#EDD27C 40%,#C29A2B 78%,#EDD27C 100%);--num-d:var(--num);
  --lg-page:#06110B;--lg-ink:#F4F3F0;--lg-ink-70:rgba(244,243,240,.76);--lg-ink-64:rgba(244,243,240,.68);--lg-ink-38:rgba(244,243,240,.42);
  --lg-rule:rgba(244,243,240,.13);--lg-rule-08:rgba(244,243,240,.07);--lg-gold-text:#EDD27C;--lg-ok:#3FBF7F}
html[data-feel="dark"] body.lg{background:#06110B;color:#F4F3F0}
[data-feel="dark"] .gs-hero{background:radial-gradient(50% 75% at 85% 5%,rgba(237,210,124,.20),transparent 62%),radial-gradient(50% 60% at 5% 100%,rgba(63,191,127,.08),transparent 70%),#06110B}
[data-feel="dark"] .gs-tile,[data-feel="dark"] .lg-card-ph,[data-feel="dark"] .gwp-swatch{background:radial-gradient(75% 75% at 50% 42%,#FFFFFF 0%,#E7E3D9 80%)}
[data-feel="dark"] .gs-tile{box-shadow:0 20px 50px -24px rgba(237,210,124,.35)}
[data-feel="dark"] .gs-res{background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02));border:1px solid rgba(237,210,124,.28);color:#F4F3F0}
[data-feel="dark"] .gs-res span{color:rgba(244,243,240,.72)}
[data-feel="dark"] .lg-card-ph{border-radius:var(--rc)}
[data-feel="dark"] .lg-btn{color:#17140F;border-radius:12px;box-shadow:0 0 0 1px rgba(255,243,196,.25),0 10px 30px -10px rgba(237,210,124,.55)}
[data-feel="dark"] .lg-btn-line{color:#F4F3F0;border-color:rgba(244,243,240,.5);box-shadow:none}
[data-feel="dark"] .lg-btn-line:hover{background:#F4F3F0;color:#06110B}
[data-feel="dark"] .lg-tag{background:#F4F3F0;color:#06110B}
[data-feel="dark"] .lg-tag-gold{background-image:var(--lg-foil);color:#17140F}
[data-feel="dark"] .gwp-gift{border-radius:var(--rc);background:linear-gradient(160deg,rgba(255,255,255,.06),rgba(255,255,255,.02));border:1px solid rgba(237,210,124,.16)}
[data-feel="dark"] .gwp-gift[data-state="open"]{border-color:rgba(237,210,124,.7);box-shadow:0 0 40px -12px rgba(237,210,124,.45)}
[data-feel="dark"] .gwp-gift[data-state="locked"] .gwp-gift-hd .lg-tag{background:#F4F3F0;color:#06110B}
[data-feel="dark"] .lg-chip{background:rgba(255,255,255,.03);border-color:rgba(244,243,240,.2);color:#F4F3F0;border-radius:10px}
[data-feel="dark"] .lg-chip[aria-pressed="true"]{background:#F4F3F0;color:#06110B;border-color:#F4F3F0}
[data-feel="dark"] .gwp-swatch{border-radius:12px;border-color:rgba(244,243,240,.18)}
[data-feel="dark"] .gwp-swatch[aria-pressed="true"]{border:2px solid #EDD27C;box-shadow:0 0 18px -4px rgba(237,210,124,.6)}
[data-feel="dark"] .gwp-qty{border-radius:10px}
[data-feel="dark"] .gwp-rail{background:rgba(6,17,11,.72);-webkit-backdrop-filter:blur(16px) saturate(1.4);backdrop-filter:blur(16px) saturate(1.4);border-bottom-color:rgba(237,210,124,.16)}
[data-feel="dark"] .gwp-track{height:8px;background:rgba(244,243,240,.09)}
[data-feel="dark"] .gwp-fill{background-image:linear-gradient(90deg,#C29A2B,#FFF3C4 55%,#EDD27C);box-shadow:0 0 18px rgba(237,210,124,.8)}
[data-feel="dark"] .gwp-node[data-hit] i{background:#EDD27C;box-shadow:0 0 12px rgba(237,210,124,.9)}
[data-feel="dark"] .lg-band{background:radial-gradient(60% 110% at 85% 0%,rgba(237,210,124,.14),transparent 60%),#0A1D14;border-block:1px solid rgba(237,210,124,.12)}
[data-feel="dark"] .gwp-rev{border-radius:var(--rc);background:rgba(255,255,255,.04);border-color:rgba(237,210,124,.2)}
[data-feel="dark"] .gwp-bar{background:rgba(6,17,11,.86);-webkit-backdrop-filter:blur(16px);backdrop-filter:blur(16px)}
[data-feel="dark"] .gwp-toast{background:#0A1D14}

/* ===================== FEEL 3 · YARDAGE ===================== */
html[data-feel="yard"]{--rc:4px;
  --num:linear-gradient(180deg,#A8821C 0%,#7A5C12 60%,#6B4F0E 100%);
  --num-d:linear-gradient(180deg,#FFF3C4 0%,#EDD27C 45%,#C29A2B 100%)}
[data-feel="yard"] .gwp{background-color:#fff;
  background-image:linear-gradient(rgba(23,20,15,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(23,20,15,.05) 1px,transparent 1px);
  background-size:56px 56px;counter-reset:yd}
[data-feel="yard"] .gs-hero{background:transparent}
[data-feel="yard"] .gwp section .lg-eyebrow{counter-increment:yd}
[data-feel="yard"] .gwp section .lg-eyebrow::before{content:counter(yd,decimal-leading-zero);width:auto;height:auto;background:none;
  font-variation-settings:'wdth' 62;font-weight:800;font-size:1.05rem;letter-spacing:0;color:var(--lg-ink);padding-right:10px;border-right:2px solid var(--lg-gold)}
[data-feel="yard"] .gs-tile,[data-feel="yard"] .lg-card-ph{background:#fff;border:1px solid rgba(23,20,15,.18);border-radius:var(--rc)}
[data-feel="yard"] .gs-tile::before,[data-feel="yard"] .lg-card-ph::before{content:'';position:absolute;right:8px;bottom:8px;width:12px;height:12px;
  border-right:2px solid var(--lg-gold);border-bottom:2px solid var(--lg-gold);z-index:2}
[data-feel="yard"] .gs-res{background:#17140F;color:#F4F3F0;border-radius:var(--rc);position:relative}
[data-feel="yard"] .gs-res::after{content:'';position:absolute;left:0;right:0;bottom:0;height:4px;background:repeating-linear-gradient(90deg,#C29A2B 0 10px,transparent 10px 14px)}
[data-feel="yard"] .gs-res span{color:rgba(244,243,240,.72)}
[data-feel="yard"] .gwp-gift{background:#fff;border:1px solid rgba(23,20,15,.18);border-radius:var(--rc)}
[data-feel="yard"] .gwp-gift[data-state="open"]{border:2px solid #C29A2B}
[data-feel="yard"] .lg-chip,[data-feel="yard"] .gwp-qty,[data-feel="yard"] .gwp-swatch,[data-feel="yard"] .lg-btn,[data-feel="yard"] .lg-btn-line{border-radius:2px}
[data-feel="yard"] .lg-tag{border-radius:2px}
[data-feel="yard"] .gwp-rail{background:rgba(255,255,255,.92);border-bottom:2px solid #17140F}
[data-feel="yard"] .gwp-track{height:12px;border-radius:0;background:repeating-linear-gradient(90deg,rgba(23,20,15,.12) 0 10px,transparent 10px 14px)}
[data-feel="yard"] .gwp-fill{border-radius:0;background:repeating-linear-gradient(90deg,#C29A2B 0 10px,transparent 10px 14px);box-shadow:none}
[data-feel="yard"] .gwp-node i{height:20px;width:2px;background:#17140F}
[data-feel="yard"] .lg-band{background-color:#0B2E1F;background-image:linear-gradient(rgba(244,243,240,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(244,243,240,.06) 1px,transparent 1px);background-size:56px 56px}
[data-feel="yard"] .gwp-rev{border-radius:var(--rc)}
[data-feel="yard"] .gwp-fq summary::before{content:'';width:8px;height:8px;background:#C29A2B;flex:none;margin-right:4px}
[data-feel="yard"] .lg-card-nm,[data-feel="yard"] .lg-card-pr{font-variation-settings:'wdth' 62}

/* ===================== the switcher (preview only, not part of the page) ===================== */
.fx{position:fixed;right:14px;top:14px;z-index:9999;display:grid;gap:8px;padding:12px;border-radius:14px;
  background:rgba(23,20,15,.92);color:#F4F3F0;font:600 11px/1.2 Archivo,system-ui;letter-spacing:.1em;text-transform:uppercase;
  box-shadow:0 18px 40px -16px rgba(0,0,0,.5)}
.fx div{display:flex;align-items:center;gap:6px}
.fx span{width:62px;opacity:.6}
.fx button{font:inherit;letter-spacing:inherit;text-transform:inherit;min-height:34px;padding:0 11px;border-radius:8px;border:1px solid rgba(244,243,240,.2);background:none;color:inherit;cursor:pointer}
.fx button[aria-pressed="true"]{background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B);color:#17140F;border-color:transparent}
@media (max-width:760px){.fx{left:8px;right:8px;top:6px;padding:7px;gap:5px;border-radius:10px}.fx span{width:52px;font-size:9px}.fx button{min-height:28px;padding:0 8px;font-size:9px}}
`;

const SWITCH = `<div class="fx" role="group" aria-label="Preview controls">
  <div><span>Feel</span><button data-feel-set="light">Gold light</button><button data-feel-set="dark">After dark</button><button data-feel-set="yard">Yardage</button></div>
  <div><span>Headline</span><button data-h-set="1">1</button><button data-h-set="2">2</button><button data-h-set="3">3</button></div>
</div>`;

const SWITCH_JS = `<script>
(function(){
  var HEADS=${JSON.stringify(HEADS)};
  function set(feel,h){
    feel=feel||document.documentElement.getAttribute('data-feel')||'light';
    h=h||document.documentElement.getAttribute('data-h')||'1';
    document.documentElement.setAttribute('data-feel',feel);
    document.documentElement.setAttribute('data-h',h);
    document.getElementById('gs-h1').innerHTML=HEADS[h].h;
    document.getElementById('gs-lede').textContent=HEADS[h].l;
    document.querySelectorAll('[data-feel-set]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.feelSet===feel)});
    document.querySelectorAll('[data-h-set]').forEach(function(b){b.setAttribute('aria-pressed',b.dataset.hSet===h)});
    try{history.replaceState(null,'','#feel='+feel+'&h='+h)}catch(e){}
  }
  document.addEventListener('click',function(e){
    var f=e.target.closest('[data-feel-set]'); if(f){set(f.dataset.feelSet,null);return;}
    var h=e.target.closest('[data-h-set]'); if(h){set(null,h.dataset.hSet);}
  });
  var m=/feel=(\\w+)&h=(\\d)/.exec(location.hash); set(m?m[1]:'light', m?m[2]:'1');
})();
</script>`;

html = html.replace('<html lang="en">', '<html lang="en" data-feel="light" data-h="1">')
           .replace('</head>', '<style>' + CSS + '</style></head>')
           .replace('<body class="lg">', '<body class="lg">\n' + SWITCH)
           .replace('</body>', SWITCH_JS + '\n</body>')
           .replace('<title>Lucky Golf · Free hat, free polo</title>', '<title>Lucky Golf · Feel options</title>');
fs.writeFileSync(path.join(H, 'feel.html'), html);

/* standalone: every asset inlined, photos straight off the Shopify CDN */
let s = html.replace('<link rel="stylesheet" href="lucky.css"><link rel="stylesheet" href="gwp-promo.css">',
  '<style>' + fs.readFileSync(path.join(H, 'lucky.css'), 'utf8') + '</style><style>' + fs.readFileSync(path.join(H, 'gwp-promo.css'), 'utf8') + '</style>');
s = s.replace('<script src="gwp-promo.js" defer></' + 'script>', '<script>' + fs.readFileSync(path.join(H, 'gwp-promo.js'), 'utf8') + '</' + 'script>');
s = s.split('src="mags-bag-light.webp"').join('src="data:image/webp;base64,' + fs.readFileSync(path.join(H, 'mags-bag-light.webp')).toString('base64') + '"');
if (/href="(lucky|gwp-promo)\.css"|src="gwp-promo\.js"/.test(s)) throw new Error('asset not inlined');
fs.writeFileSync(ROOT + '/shopify/gwp-feel-options.html', s);
console.log('feel options built ·', Math.round(s.length / 1024) + 'KB standalone');
