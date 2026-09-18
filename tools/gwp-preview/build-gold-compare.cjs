/* Daylight gold: the choices, side by side on the REAL hero with the real CSS.
   Output: design/gold-compare.html (one file, opens offline). */
const fs = require('fs'), path = require('path');
const H = __dirname, ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const base = fs.readFileSync(path.join(H, 'index.html'), 'utf8');
const hero = base.match(/<section class="gwp-h-hero">[\s\S]*?<\/section>/)[0];
const img = f => 'data:image/webp;base64,' + fs.readFileSync(path.join(H, f)).toString('base64');

const V = [
  { k: 'A', t: 'Now: antique gold', ground: 'day', note: 'Darker and sideways-lit. Readable at any size (3.6 to 7.6:1). Reads more bronze than the Twilight gold.',
    num: 'linear-gradient(100deg,#6B4F0E 0%,#A8821C 30%,#7A5C12 52%,#A8821C 76%,#6B4F0E 100%)', eye: '#8A6A1C' },
  { k: 'B', t: 'Same gold as Twilight', ground: 'day', note: 'Exactly the Twilight numbers. On white the pale top half nearly disappears (1.1 to 2.6:1). Fails readability.',
    num: 'linear-gradient(180deg,#FFF3C4 0%,#EDD27C 40%,#C29A2B 78%,#EDD27C 100%)', eye: '#C29A2B' },
  { k: 'C', t: 'Same gold, one shade deeper', ground: 'day', note: 'The Twilight gradient (same direction, same bright band) moved down one step so it starts at the brand gold. Reads as the same gold, still passes for big numbers (2.6 to 5:1).',
    num: 'linear-gradient(180deg,#C29A2B 0%,#B8912A 38%,#8A6A1C 78%,#A8821C 100%)', eye: '#8A6A1C' },
  { k: 'Ref', t: 'Twilight, for comparison', ground: 'twilight', note: 'What the page ships as today.', num: null, eye: null }
];

const cards = V.map(v => `<figure class="cmp">
  <figcaption><b>${v.k}</b> ${v.t}<span>${v.note}</span></figcaption>
  <div class="frame"><div class="lg-scope gwp" data-ground="${v.ground}" data-yardage="on" style="${v.num ? `--num:${v.num};--lg-gold-text:${v.eye};` : ''}">${hero}</div></div>
</figure>`).join('\n');

const css = fs.readFileSync(path.join(H, 'lucky.css'), 'utf8') + fs.readFileSync(path.join(H, 'gwp-promo.css'), 'utf8');
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Daylight gold options</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<style>${css}
body{margin:0;background:#E9E7E1;font-family:Archivo,system-ui;color:#17140F}
.top{padding:28px 24px 8px;max-width:1260px;margin:0 auto}
.top h1{font-size:22px;margin:0 0 6px}.top p{margin:0;color:#555;max-width:70ch;line-height:1.5}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:24px;padding:20px 24px 40px;max-width:1260px;margin:0 auto}
.cmp{margin:0;background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 1px 0 rgba(0,0,0,.06)}
.cmp figcaption{padding:14px 16px;font-size:14px;line-height:1.45;border-bottom:1px solid #eee}
.cmp figcaption b{display:inline-block;min-width:34px;padding:2px 8px;margin-right:6px;border-radius:6px;background:#17140F;color:#F4F3F0;text-align:center}
.cmp figcaption span{display:block;color:#555;margin-top:4px}
.frame{height:470px;overflow:hidden}
.frame>.gwp{width:1200px;zoom:.5;padding-bottom:0!important}
@media (max-width:900px){.grid{grid-template-columns:1fr}.frame>.gwp{zoom:.42}.frame{height:400px}}
</style></head><body>
<div class="top"><h1>Daylight gold: A, B or C?</h1>
<p>The real hero with the real CSS, on Daylight. Only the gold on the headline numbers and the eyebrow changes. The $99 / $209 tiles already use the Twilight gold on both grounds (they sit on green).</p></div>
<div class="grid">${cards}</div></body></html>`;
fs.writeFileSync(ROOT + '/design/gold-compare.html', html);
console.log('gold-compare', Math.round(html.length / 1024) + 'KB');
