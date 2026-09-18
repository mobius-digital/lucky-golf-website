/* Six hero options on one page, A = the version Cole already saw, untouched.
   Same headline, same offer, same button in every one, so the only thing being
   compared is how bold the club and the gold get. Real photos off the live
   store, lucky.css tokens only. */
const fs = require('fs'), path = require('path');
const ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const LIVE = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'live-products.json'), 'utf8')).products;
const P = {}; LIVE.forEach(p => P[p.handle] = p);
const img = (h, n, w) => P[h].images[n - 1].src.split('?')[0] + '?width=' + (w || 2000);
const GOLD = 'lucky-golf-lgw02-gold', MALLET = 'limited-edition-mallet-putter', STRYKER = 'lucky-striker-hybrid-limited-edition';
const HAT = P['black-gold-classic-lucky-hat'];
const POLO = P['gold-dust-classic-polo'];

const lucky = fs.readFileSync(ROOT + '/shopify/assets/lucky.css', 'utf8');
const logo = fs.readFileSync(ROOT + '/_src-logo-symbols.svg', 'utf8').match(/<symbol id="lg-lucky"[\s\S]*?<\/symbol>/)[0];
const clover = fs.readFileSync(ROOT + '/_src-logo-symbols.svg', 'utf8').match(/<symbol id="lg-clover-plain"[\s\S]*?<\/symbol>/)[0];

const EB = 'This weekend only';
const H1 = 'Grab a <span class="lg-foil-word">club</span>. The hat\'s on us.';
const LEDE = 'Spend $90 and we\'ll throw in a hat. Get to $140 and there\'s a polo in it for you too.';
const CTA = '<a class="lg-btn" href="#">Show me the clubs <span aria-hidden="true">&rarr;</span></a>';
const END = 'Ends Sunday, Sept 20';

const label = (k, name, note) => `
<div class="ho-label"><div class="lg-wrap"><b>${k}</b><span class="nm">${name}</span><span class="nt">${note}</span></div></div>`;

const html = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lucky Golf · Hero options</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<style>${lucky}</style>
<style>
/* ---- the option labels: not part of any design, just the menu ---- */
.ho-intro{padding:40px 0 34px;border-bottom:1px solid var(--lg-rule)}
.ho-intro .lg-d2{margin-bottom:10px}
.ho-label{position:sticky;top:0;z-index:50;background:var(--lg-ink);color:var(--lg-page)}
.ho-label .lg-wrap{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;padding-block:12px}
.ho-label b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:1.9rem;line-height:1;color:var(--lg-gold)}
.ho-label .nm{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.8rem}
.ho-label .nt{font-size:.9rem;opacity:.72}
.ho-gap{height:56px;background:var(--lg-page)}
.ho-end{display:flex;align-self:center}

/* ---- A · your first version, exactly as sent ---- */
.hA img{object-position:50% 62%}

/* ---- B · split: photo at full colour, copy on a solid panel ---- */
.hB{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);min-height:min(84vh,780px);background:var(--lg-dark)}
.hB-copy{display:flex;flex-direction:column;justify-content:center;padding:clamp(40px,6vw,96px) var(--lg-pad);color:var(--lg-on-dark)}
.hB-copy .lg-lede{color:var(--lg-on-dark-m)}
.hB-ph{position:relative;min-height:420px}
.hB-ph{overflow:hidden}
.hB-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;scale:1.6;transform-origin:12% 92%}
.hB .ho-stamp{position:absolute;left:clamp(16px,3vw,40px);bottom:clamp(16px,3vw,40px)}

/* ---- C · poster: white, one giant gold club, loud type ---- */
.hC{position:relative;overflow:hidden;background:var(--lg-page);min-height:min(84vh,760px);display:flex;align-items:center}
.hC-club{position:absolute;right:-6%;top:50%;translate:0 -50%;width:min(62vw,860px);aspect-ratio:1;pointer-events:none}
.hC-club img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;rotate:-8deg}
.hC .lg-wrap{position:relative;z-index:2;width:100%}
.hC .lg-d1{font-size:clamp(3.2rem,9vw,8.4rem);max-width:9ch;line-height:.86}
.hC .lg-lede{max-width:34ch}
.hC-price{position:absolute;right:clamp(20px,6vw,90px);bottom:clamp(20px,5vw,64px);z-index:3;text-align:right;
  background:var(--lg-page);padding:12px 16px;border-radius:var(--lg-r);rotate:-4deg;border:2px solid var(--lg-ink)}
.hC-price b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2.6rem,5vw,4.4rem);line-height:.9;color:var(--lg-ink)}
.hC-price span{display:block;margin-top:6px}

/* ---- D · the math: the deal as a sum, with the real club and the real hat ---- */
.hD{background:var(--lg-page);padding:clamp(48px,6vw,96px) 0 clamp(40px,5vw,72px)}
.hD-sum{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1.05fr);align-items:center;gap:clamp(10px,2vw,28px);margin-top:clamp(28px,4vw,48px)}
.hD-tile{position:relative;aspect-ratio:1;background:var(--lg-tile);border-radius:var(--lg-r-card);overflow:hidden}
.hD-tile img{width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;padding:6%}
.hD-tile .lg-tag{position:absolute;left:12px;top:12px}
.hD-tile figcaption{position:absolute;left:0;right:0;bottom:12px;text-align:center}
.hD-op{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2.4rem,5vw,4.6rem);line-height:1;color:var(--lg-gold)}
.hD-res{background:var(--lg-dark);color:var(--lg-on-dark);border-radius:var(--lg-r-card);aspect-ratio:1;display:flex;flex-direction:column;justify-content:center;padding:clamp(16px,2.4vw,32px)}
.hD-res b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2.6rem,6vw,5.6rem);line-height:.86;color:var(--lg-gold)}
.hD-res span{margin-top:10px;color:var(--lg-on-dark-m);font-size:var(--lg-fs-base);line-height:1.4}
.hD-row2{margin-top:clamp(14px,2vw,24px)}
.hD-row2 .hD-tile,.hD-row2 .hD-res{aspect-ratio:auto;height:clamp(150px,18vw,230px)}
.hD-pair{display:grid;grid-template-columns:1fr 1fr}
.hD-pair img{padding:8%}
.hD-foot{display:flex;flex-wrap:wrap;align-items:center;gap:14px 24px;margin-top:clamp(24px,3vw,40px)}

/* ---- E · the lineup: every club on the grass, full colour ---- */
.hE{background:var(--lg-page);padding:clamp(48px,6vw,88px) 0 0}
.hE-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:clamp(28px,4vw,44px)}
.hE-strip figure{position:relative;margin:0;aspect-ratio:4/5;overflow:hidden}
.hE-strip img{width:100%;height:100%;object-fit:cover;transition:transform .6s var(--lg-ease)}
.hE-strip figure:first-child img{scale:1.4;transform-origin:25% 70%}
.hE-strip figure:hover img{transform:scale(1.04)}
.hE-strip figcaption{position:absolute;left:0;right:0;bottom:0;padding:40px 16px 14px;color:var(--lg-on-dark);
  background:linear-gradient(transparent,rgba(23,20,15,.72))}
.hE-strip figcaption b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:1.15rem;line-height:1}
.hE-strip figcaption span{display:block;margin-top:4px;color:var(--lg-gold);font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:700;letter-spacing:.1em;text-transform:uppercase;font-size:var(--lg-fs-xs)}
.hE-top{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(20px,4vw,64px);align-items:end}
.hE-top .lg-btn-row{margin-top:0}

/* ---- F · close and bold: the gold face at full size, only a floor of shadow ---- */
.hF{position:relative;isolation:isolate;overflow:hidden;background:#0f0d09}
.hF img{display:block;width:100%;height:min(88vh,880px);min-height:540px;object-fit:cover;object-position:50% 45%}
.hF img{object-position:50% 58%}
.hF::after{content:'';position:absolute;inset:0;z-index:1;pointer-events:none;
  background:linear-gradient(180deg,rgba(23,20,15,.78) 0%,rgba(23,20,15,.42) 30%,rgba(23,20,15,0) 52%)}
.hF .lg-hero-copy{align-items:flex-start;padding-top:clamp(36px,5vw,72px);padding-bottom:0}
.hF .lg-hero-copy .lg-d1{font-size:clamp(3rem,7.4vw,6.6rem)}
.hF-foot{background:var(--lg-page);border-bottom:1px solid var(--lg-rule)}
.hF-foot .lg-wrap{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px 32px;padding-block:24px}
.hF img{height:min(76vh,760px)}
.hF .ho-stamp{position:absolute;right:clamp(16px,4vw,56px);bottom:clamp(20px,4vw,56px);top:auto;z-index:3}

/* the stamp: the system's gold tag, set big and turned, for a bit of attitude */
.ho-stamp{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;rotate:-6deg;
  background-image:var(--lg-foil);color:var(--lg-ink);font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;
  font-weight:800;text-transform:uppercase;letter-spacing:.1em;font-size:.82rem}
.ho-stamp svg{width:16px;height:16px}

@media (max-width:860px){
  .hB{grid-template-columns:1fr}
  .hB-ph{min-height:360px;order:-1}
  .hC{align-items:flex-start;padding-top:40px;min-height:auto;padding-bottom:280px}
  .hC-club{top:auto;bottom:-40px;translate:0 0;right:-14%;width:88vw}
  .hC-price{bottom:24px}
  .hD-sum{grid-template-columns:1fr auto 1fr;row-gap:14px}
  .hD-sum .hD-eq{display:none}
  .hD-res{grid-column:1/-1;aspect-ratio:auto}
  .hE-strip{grid-template-columns:repeat(2,minmax(0,1fr))}
  .hE-top{grid-template-columns:1fr}
}
</style></head><body class="lg">
<svg width="0" height="0" style="position:absolute" aria-hidden="true">${logo}${clover}</svg>

<div class="lg-wrap ho-intro">
  <p class="lg-eyebrow">Hero options</p>
  <h1 class="lg-d2">Pick one. Or mix two.</h1>
  <p class="lg-body">Same headline and offer in all six, so you're only comparing how hard the club and the gold hit. A is the version you already saw. Every photo is a real shot from the store.</p>
</div>

${label('A', 'Your first version', 'Kept exactly as sent. Photo under the green wash.')}
<section class="lg-hero hA">
  <img src="${img(GOLD,1)}" alt="Carver 01 Gold behind the ball">
  <div class="lg-hero-copy"><div class="lg-wrap">
    <p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1><p class="lg-lede">${LEDE}</p>
    <div class="lg-btn-row">${CTA}<span class="lg-label ho-end">${END}</span></div>
  </div></div>
</section>
<div class="ho-gap"></div>

${label('B', 'Split', 'No wash at all. The club gets half the screen at full colour, the words get a solid panel.')}
<section class="hB">
  <div class="hB-copy">
    <p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1><p class="lg-lede">${LEDE}</p>
    <div class="lg-btn-row">${CTA}<span class="lg-label ho-end">${END}</span></div>
  </div>
  <div class="hB-ph"><img src="${img(GOLD,13)}" alt="Carver 01 Gold, face and clover">
    <span class="ho-stamp"><svg viewBox="249.37 127.71 342.59 330.41" fill="currentColor"><use href="#lg-clover-plain"/></svg>Free hat with it</span></div>
</section>
<div class="ho-gap"></div>

${label('C', 'Poster', 'White page, one huge gold Carver crashing in from the side, loud type, the price like a sticker.')}
<section class="hC">
  <div class="hC-club"><img src="${img(GOLD,5,1400)}" alt=""></div>
  <div class="lg-wrap">
    <p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1><p class="lg-lede">${LEDE}</p>
    <div class="lg-btn-row">${CTA}<span class="lg-label ho-end" style="color:var(--lg-ink-64)">${END}</span></div>
  </div>
  <div class="hC-price"><b>$99</b><span class="lg-label" style="color:var(--lg-gold-text)">Carver 01 Gold · hat included</span></div>
</section>
<div class="ho-gap"></div>

${label('D', 'The math', 'The deal as a sum, with the real wedge and the real hat. Receipts first, then the button.')}
<section class="hD"><div class="lg-wrap">
  <p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1>
  <div class="hD-sum">
    <figure class="hD-tile" style="margin:0"><img src="${img(GOLD,5,900)}" alt="Carver 01 Gold"><span class="lg-tag">$99</span><figcaption class="lg-label">Carver 01 Gold</figcaption></figure>
    <span class="hD-op" aria-hidden="true">+</span>
    <figure class="hD-tile" style="margin:0"><img src="${HAT.images[0].src.split('?')[0]}?width=900" alt="Black and gold Lucky hat"><span class="lg-tag lg-tag-gold">Free</span><figcaption class="lg-label">Any hat you like</figcaption></figure>
    <span class="hD-op hD-eq" aria-hidden="true">=</span>
    <div class="hD-res"><b>$99</b><span>Any club gets you the hat.</span></div>
  </div>
  <div class="hD-sum hD-row2">
    <figure class="hD-tile" style="margin:0"><img src="${img(STRYKER,5,900)}" alt="Stryker hybrid"><span class="lg-tag">$209</span><figcaption class="lg-label">Stryker</figcaption></figure>
    <span class="hD-op" aria-hidden="true">+</span>
    <figure class="hD-tile hD-pair" style="margin:0"><img src="${HAT.images[0].src.split('?')[0]}?width=600" alt="Lucky hat"><img src="${POLO.images[0].src.split('?')[0]}?width=600" alt="Gold Dust polo"><span class="lg-tag lg-tag-gold">Both free</span><figcaption class="lg-label">Hat + polo</figcaption></figure>
    <span class="hD-op hD-eq" aria-hidden="true">=</span>
    <div class="hD-res"><b>$209</b><span>Over $140 the polo comes too. Over $198, shipping's free.</span></div>
  </div>
  <div class="hD-foot">${CTA}<span class="lg-label" style="color:var(--lg-ink-64)">${END}</span></div>
</div></section>
<div class="ho-gap"></div>

${label('E', 'The lineup', 'Every club on the grass, full colour, side by side. Sells all four, not just the wedge.')}
<section class="hE">
  <div class="lg-wrap hE-top">
    <div><p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1></div>
    <div><p class="lg-lede" style="margin-top:0">${LEDE}</p><div class="lg-btn-row" style="margin-top:20px">${CTA}</div></div>
  </div>
  <div class="hE-strip">
    <figure><img src="${img(GOLD,13,900)}" alt="Carver 01 Gold"><figcaption><b>Carver 01 Gold</b><span>$99 · free hat</span></figcaption></figure>
    <figure><img src="${img(GOLD,3,900)}" alt="Carver 01 Gold at the ball"><figcaption><b>Two Carvers</b><span>$198 · hat, polo, free shipping</span></figcaption></figure>
    <figure><img src="${img(MALLET,2,900)}" alt="Tracer Mallet"><figcaption><b>Tracer Mallet</b><span>$229 · hat + polo</span></figcaption></figure>
    <figure><img src="${img(STRYKER,1,900)}" alt="Stryker hybrid"><figcaption><b>Stryker</b><span>$209 · hat + polo</span></figcaption></figure>
  </div>
</section>
<div class="ho-gap"></div>

${label('F', 'Close and bold', 'The gold face at full size and full colour. No green, just a shadow at the floor so the words read.')}
<section class="hF">
  <img src="${img(GOLD,3)}" alt="Carver 01 Gold face next to the ball">
  <span class="ho-stamp"><svg viewBox="249.37 127.71 342.59 330.41" fill="currentColor"><use href="#lg-clover-plain"/></svg>Hat's on us</span>
  <div class="lg-hero-copy" style="z-index:2"><div class="lg-wrap">
    <p class="lg-eyebrow">${EB}</p><h1 class="lg-d1">${H1}</h1>
  </div></div>
</section>
<div class="hF-foot"><div class="lg-wrap">
  <p class="lg-lede" style="margin:0">${LEDE}</p>
  <div class="lg-btn-row" style="margin:0">${CTA}<span class="lg-label ho-end" style="color:var(--lg-ink-64)">${END}</span></div>
</div></div>
<div class="ho-gap"></div>
</body></html>`;

const out = path.join(__dirname, 'heroes.html');
fs.writeFileSync(out, html);
fs.writeFileSync(ROOT + '/shopify/gwp-hero-options.html', html);
console.log('wrote hero options', Math.round(html.length / 1024) + 'KB');
