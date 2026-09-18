/* The previews, rendered from the REAL section (build3 mirrors the Liquid).
   Every style and script comes from shopify/assets: nothing here restyles the
   page, so what the design team sees is what Shopify serves.
     shopify/gwp-promo-full-page.html   the page as it ships (Twilight, Yardage, headline 1)
     shopify/gwp-system-preview.html    the same page with a switcher: ground, yardage, headline */
const fs = require('fs'), path = require('path'), cp = require('child_process');
const H = __dirname, ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
cp.execSync('node build3.cjs', { cwd: H, stdio: 'inherit' });
const base = fs.readFileSync(path.join(H, 'index.html'), 'utf8');

/* headline options still open: 1 is the default in the template */
const HEADS = {
  1: { h: '$90 gets the hat. $140 gets the fit.', l: "The fit's a hat and a polo, both on us, both your pick. Every club here gets you the hat on its own." },
  2: { h: 'The more you bag, the more you <span class="gwp-num">wear</span>.', l: "Spend $90 and the hat's on us. Hit $140 and the polo comes with it. Your pick on both." },
  3: { h: "Hit $90, the hat's yours. Hit $140, grab the polo too.", l: 'Every club on this page clears the first one. The Mallet and the Stryker clear both.' }
};
const gold = s => s.replace(/\$(90|140)(?![\d])/g, '<span class="gwp-num">$$$1</span>');
Object.values(HEADS).forEach(o => { if (!o.h.includes('gwp-num')) o.h = gold(o.h); });

/* one self-contained file: css, js, contour maps and the bag icon inlined */
const svgUri = f => 'url("data:image/svg+xml;base64,' + fs.readFileSync(path.join(H, f)).toString('base64') + '")';
function inline(s) {
  s = s.replace('<link rel="stylesheet" href="lucky.css"><link rel="stylesheet" href="gwp-promo.css">',
    '<style>' + fs.readFileSync(path.join(H, 'lucky.css'), 'utf8') + '</style><style>' + fs.readFileSync(path.join(H, 'gwp-promo.css'), 'utf8') + '</style>');
  s = s.replace('<script src="gwp-promo.js" defer></' + 'script>', '<script>' + fs.readFileSync(path.join(H, 'gwp-promo.js'), 'utf8') + '</' + 'script>');
  s = s.replace('--gwp-contour-day:url(gwp-contour-day.svg)', () => '--gwp-contour-day:' + svgUri('gwp-contour-day.svg').replace(/"/g, "'"))
       .replace('--gwp-contour-tw:url(gwp-contour-tw.svg)', () => '--gwp-contour-tw:' + svgUri('gwp-contour-tw.svg').replace(/"/g, "'"));
  s = s.split('src="gwp-mags.webp"').join('src="data:image/webp;base64,' + fs.readFileSync(path.join(H, 'gwp-mags.webp')).toString('base64') + '"');
  s = s.split('src="mags-bag-light.webp"').join('src="data:image/webp;base64,' + fs.readFileSync(path.join(H, 'mags-bag-light.webp')).toString('base64') + '"');
  if (/href="(lucky|gwp-promo)\.css"|src="gwp-promo\.js"|url\(gwp-contour/.test(s)) throw new Error('asset not inlined');
  return s;
}

/* 1 · the full page, exactly as it ships */
const full = inline(base);
fs.writeFileSync(ROOT + '/shopify/gwp-promo-full-page.html', full);

/* 2 · the same page with the switcher (preview only) */
const FX_CSS = `<style>
.fx{position:fixed;right:14px;top:14px;z-index:9999;display:grid;gap:8px;padding:12px;border-radius:14px;background:rgba(23,20,15,.92);color:#F4F3F0;
  font:600 11px/1.2 Archivo,system-ui;letter-spacing:.1em;text-transform:uppercase;box-shadow:0 18px 40px -16px rgba(0,0,0,.5)}
.fx div{display:flex;align-items:center;gap:6px}.fx span{width:66px;opacity:.6}
.fx button{font:inherit;letter-spacing:inherit;text-transform:inherit;min-height:34px;padding:0 11px;border-radius:8px;border:1px solid rgba(244,243,240,.2);background:none;color:inherit;cursor:pointer}
.fx button[aria-pressed="true"]{background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B);color:#17140F;border-color:transparent}
@media (max-width:760px){.fx{left:8px;right:8px;top:6px;padding:7px;gap:5px;border-radius:10px}.fx span{width:54px;font-size:9px}.fx button{min-height:28px;padding:0 8px;font-size:9px}}
</style>`;
const SWITCH = `<div class="fx" role="group" aria-label="Preview controls">
  <div><span>Ground</span><button data-set="ground:day">Daylight</button><button data-set="ground:twilight">Twilight round</button></div>
  <div><span>Yardage</span><button data-set="yardage:on">On</button><button data-set="yardage:off">Off</button></div>
  <div><span>Headline</span><button data-set="h:1">1</button><button data-set="h:2">2</button><button data-set="h:3">3</button></div>
</div>`;
const SWITCH_JS = `<script>
(function(){
  var HEADS=${JSON.stringify(HEADS)}, G=document.getElementById('gwp'), h='1';
  function get(k){return k==='h'?h:G.getAttribute('data-'+k);}
  function paint(){
    document.querySelector('.gwp-h-h1').innerHTML=HEADS[h].h; document.querySelector('.gwp-h-lede').textContent=HEADS[h].l;
    document.querySelectorAll('[data-set]').forEach(function(b){var kv=b.dataset.set.split(':');b.setAttribute('aria-pressed',get(kv[0])===kv[1]);});
  }
  document.addEventListener('click',function(e){var b=e.target.closest('[data-set]');if(!b)return;var kv=b.dataset.set.split(':');
    if(kv[0]==='h')h=kv[1];else G.setAttribute('data-'+kv[0],kv[1]);paint();});
  paint();
})();
</script>`;
const sys = full.replace('</head>', FX_CSS + '</head>').replace('<body class="lg">', '<body class="lg">\n' + SWITCH).replace('</body>', SWITCH_JS + '\n</body>');
fs.writeFileSync(ROOT + '/shopify/gwp-system-preview.html', sys);
fs.writeFileSync(path.join(H, 'system.html'), base.replace('</head>', FX_CSS + '</head>').replace('<body class="lg">', '<body class="lg">\n' + SWITCH).replace('</body>', SWITCH_JS + '\n</body>'));
console.log('full page', Math.round(full.length / 1024) + 'KB · system preview', Math.round(sys.length / 1024) + 'KB');
