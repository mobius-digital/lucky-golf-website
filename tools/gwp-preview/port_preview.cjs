/* Part 4 of the port: the template gets the hero D settings, and the preview
   renderer (build3) emits the SAME markup the section now emits. */
const fs = require('fs');
const ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const H = __dirname;

/* ---------- template JSON ---------- */
const TP = ROOT + '/shopify/templates/page.gwp-promo.json';
const tj = JSON.parse(fs.readFileSync(TP, 'utf8'));
const st = tj.sections.main.settings;
for (const k of ['hero_image', 'hero_product', 'hero_image_index', 'hero_alt', 'hero_shot_brief', 'hero_foil_word', 'promo_end']) delete st[k];
Object.assign(st, {
  ground: 'twilight', yardage: true, tee_label: 'Tee · $0',
  hero_eyebrow: 'This weekend only · Ends Sunday, Sept 20',
  hero_heading: '$90 gets the hat. $140 gets the fit.',
  hero_sub: "The fit's a hat and a polo, both on us, both your pick. Every club here gets you the hat on its own.",
  hero_cta: 'Show me the clubs',
  sum1_product: 'lucky-golf-lgw02-gold', sum1_image_index: 5, sum1_note: 'Any club gets you the hat.', sum_gift1_label: 'Any hat',
  sum2_product: 'lucky-striker-hybrid-limited-edition', sum2_image_index: 5,
  sum2_note: "Over $140 the polo comes too. Over $198, shipping's free.", sum_gift2_label: 'The fit: hat + polo', both_free_tag: 'Both free',
  trust_1: 'Secure checkout', trust_2: 'Sixty days to prove us wrong', trust_3: 'Free shipping over $198'
});
fs.writeFileSync(TP, JSON.stringify(tj, null, 2) + '\n');

/* ---------- build3 ---------- */
const BP = H + '/build3.cjs';
let b = fs.readFileSync(BP, 'utf8');
const rep = (a, c) => { if (!b.includes(a)) throw new Error('missing: ' + a.slice(0, 80)); b = b.replace(a, c); };

rep("const heroImg = P[S.hero_product].images[(S.hero_image_index || 1) - 1];",
`/* hero D, the same maths as the Liquid: the two threshold amounts go gold on their own */
const t1s = short(T1), t2s = short(T2);
let h1 = esc(S.hero_heading).split(t2s).join('<span class="gwp-num">' + t2s + '</span>').split(t1s).join('<span class="gwp-num">' + t1s + '</span>');
if (S.hero_gold_word) h1 = h1.replace(S.hero_gold_word, '<span class="gwp-num">' + S.hero_gold_word + '</span>');
const HATIMG = GIFTS.hat.variants[0].img, POLOIMG = GIFTS.polo.variants[0].img;
const ICON = {
  lock: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="10.5" width="15" height="10" rx="2"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/></svg>',
  back: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 12a9 9 0 1 0 2.6-6.4"/><path d="M3 4v5h5"/></svg>',
  ship: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 7h11v9H2z"/><path d="M13 10h4l3 3v3h-7z"/><circle cx="6.5" cy="18" r="1.8"/><circle cx="17" cy="18" r="1.8"/></svg>'
};
const sumRow = n => {
  const sp = P[S['sum' + n + '_product']]; if (!sp) return '';
  const si = sp.images[(S['sum' + n + '_image_index'] || 1) - 1] || sp.images[0];
  const price = short(Math.min(...sp.variants.map(v => cents(v.price))));
  const gift = '<img src="' + cdn(HATIMG, 500) + '" alt="' + esc(GIFTS.hat.title) + '">' + (n === 2 ? '<img src="' + cdn(POLOIMG, 500) + '" alt="' + esc(GIFTS.polo.title) + '">' : '');
  return \`<div class="gwp-h-sum">
        <figure class="gwp-h-fig"><div class="gwp-h-tile"><img src="\${cdn(si.src, 600)}" alt="\${esc(sp.title)}"><span class="lg-tag">\${price}</span></div><figcaption class="lg-label">\${esc(sp.title)}</figcaption></figure>
        <span class="gwp-h-op" aria-hidden="true">+</span>
        <figure class="gwp-h-fig"><div class="gwp-h-tile\${n === 2 ? ' gwp-h-pair' : ''}">\${gift}<span class="lg-tag lg-tag-gold">\${esc(n === 2 ? S.both_free_tag : S.free_tag)}</span></div><figcaption class="lg-label">\${esc(S['sum_gift' + n + '_label'])}</figcaption></figure>
        <span class="gwp-h-op gwp-h-eq" aria-hidden="true">=</span>
        <div class="gwp-h-res"><b class="gwp-num-d">\${price}</b><span>\${esc(S['sum' + n + '_note'])}</span></div>
      </div>\`;
};`);

b = b.replace(/  <section class="lg-hero gwp-hero">[\s\S]*?<\/section>\n/, `  <section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">\${esc(S.hero_eyebrow)}</p>
      <h1 class="lg-d1 gwp-h-h1">\${h1}</h1>
      <p class="lg-lede gwp-h-lede">\${esc(S.hero_sub)}</p>
      <div class="gwp-h-sums">\${sumRow(1)}\${sumRow(2)}</div>
      <div class="gwp-h-foot">
        <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">\${esc(S.hero_cta)} <span aria-hidden="true">&rarr;</span></a>
        <ul class="gwp-h-trust" role="list">
          <li class="lg-label">\${ICON.lock}\${esc(S.trust_1)}</li><li class="lg-label">\${ICON.back}\${esc(S.trust_2)}</li><li class="lg-label">\${ICON.ship}\${esc(S.trust_3)}</li>
        </ul>
      </div>
    </div>
  </section>
`);
if (!b.includes('gwp-h-hero')) throw new Error('hero not swapped');

rep('<div class="lg-scope gwp" id="gwp" style="--gwp-top:72px"',
    '<div class="lg-scope gwp" id="gwp" data-ground="${S.ground}" data-yardage="${S.yardage ? \'on\' : \'off\'}" style="--gwp-top:72px;--gwp-contour-day:url(gwp-contour-day.svg);--gwp-contour-tw:url(gwp-contour-tw.svg)"');
rep('  <section class="lg-sec" id="gwp-clubs" tabindex="-1">',
    '  ${S.yardage ? `<div class="yd yd-tracer" id="gwp-tracer" data-tee="${esc(S.tee_label)}" aria-hidden="true"><div class="lg-wrap"></div></div>` : \'\'}\n\n  <section class="lg-sec" id="gwp-clubs" tabindex="-1">');
rep('  <section class="lg-sec" id="gwp-gifts" style="padding-top:0">',
    '  ${S.yardage ? \'<div class="yd yd-rule" aria-hidden="true"></div>\' : \'\'}\n  <section class="lg-sec gwp-contour" id="gwp-gifts">');
rep('  <section class="lg-sec"><div class="lg-wrap gwp-faq-wrap">', '  <section class="lg-sec gwp-contour gwp-contour-l"><div class="lg-wrap gwp-faq-wrap">');
rep("for (const f of ['lucky.css', 'gwp-promo.css', 'gwp-promo.js'])", "for (const f of ['lucky.css', 'gwp-promo.css', 'gwp-promo.js', 'gwp-contour-day.svg', 'gwp-contour-tw.svg'])");
fs.writeFileSync(BP, b);
console.log('template + build3 updated');
