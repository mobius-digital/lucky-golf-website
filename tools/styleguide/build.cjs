/* Builds design/styleguide.html from the REAL system files, so the styleguide
   can never drift from what ships:
     shopify/assets/lucky.css + lucky.js  ->  inlined
     tools/styleguide/template.html       ->  the page
     images                               ->  design/sg/
   Run: node tools/styleguide/build.cjs */
const fs = require('fs'), path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const rd = p => fs.readFileSync(path.join(ROOT, p), 'utf8');
const OUT = path.join(ROOT, 'design');
const IMG = path.join(OUT, 'sg');
fs.mkdirSync(IMG, { recursive: true });

const copies = {
  'green-read-fit.webp': 'design/img/shoot-0918/green-read-fit.webp',
  'two-gold-wedges.webp': 'design/img/shoot-0918/two-gold-wedges.webp',
  'black-hat-mallet.webp': 'design/img/shoot-0918/black-hat-mallet.webp',
  'putter-in-hand.webp': 'design/img/shoot-0918/putter-in-hand.webp',
  'fit-sunset.webp': 'design/img/shoot-0918/fit-sunset.webp',
  'two-hats-mallet.webp': 'design/img/shoot-0918/two-hats-mallet.webp',
  'from-the-cup.webp': 'design/img/shoot-0918/from-the-cup.webp',
  'gold-3q-cut.webp': 'img/gold-3q-cut.webp',
  'black-full-cut.webp': 'img/black-full-cut.webp',
  'mallet-full-cut.webp': 'img/mallet-full-cut.webp',
  'stryker-full-cut.webp': 'img/stryker-full-cut.webp',
  'hat-cut.webp': 'img/hat-cut.webp',
  'mags-ink.webp': 'handoff/img/mags-ink.webp',
  'mags-light.webp': 'handoff/img/mags-light.webp',
  'mags-bag-ink.webp': 'handoff/img/mags-bag-ink.webp',
  'mags-bag-light.webp': 'handoff/img/mags-bag-light.webp',
  'lucky-contour-day.svg': 'shopify/assets/lucky-contour-day.svg',
  'lucky-contour-tw.svg': 'shopify/assets/lucky-contour-tw.svg',
};
for (const [to, from] of Object.entries(copies)) fs.copyFileSync(path.join(ROOT, from), path.join(IMG, to));

const star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.6 7 .8-5.2 4.9 1.4 7L12 17.8 5.8 21.3l1.4-7L2 9.4l7-.8z"/></svg>';
const wordmark = rd('handoff/img/lucky-wordmark.svg').replace(/<\?xml[^>]*>/, '').trim();

let html = rd('tools/styleguide/template.html');
const fill = (k, v) => { if (!html.includes(k)) throw new Error('missing ' + k); html = html.split(k).join(v); };
fill('{{LUCKY_CSS}}', rd('shopify/assets/lucky.css'));
fill('{{LUCKY_JS}}', rd('shopify/assets/lucky.js'));
fill('{{WORDMARK}}', wordmark);
fill('{{STARS5}}', star.repeat(5));
if (/\{\{[A-Z0-9_]+\}\}/.test(html)) throw new Error('unfilled placeholder');
if (/—/.test(html.replace(/\/\*[\s\S]*?\*\//g, ''))) console.warn('WARNING: em dash outside a comment');
fs.writeFileSync(path.join(OUT, 'styleguide.html'), html);
console.log('design/styleguide.html', (html.length / 1024).toFixed(0) + 'KB,', Object.keys(copies).length, 'images in design/sg/');
