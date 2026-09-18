/* Renders the section the way Liquid would, from REAL store data:
   live-products.json is luckygolf.com/products.json pulled 2026-09-18.
   Real variant ids, real prices, real stock, real CDN photos.
   Copy comes from the section schema + the page template, exactly as shipped.
   The cart is stubbed (a preview must never write to the real store), but it
   prices every line from the real catalogue. */
const fs = require('fs');
const path = require('path');

const ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const SRC = ROOT + '/shopify';
const OUT = __dirname;
const LIVE = JSON.parse(fs.readFileSync(path.join(OUT, 'data', 'live-products.json'), 'utf8')).products;
const P = {}; LIVE.forEach(p => P[p.handle] = p);

const liquid = fs.readFileSync(SRC + '/sections/gwp-promo.liquid', 'utf8');
const schema = JSON.parse(liquid.match(/\{%\s*schema\s*%\}([\s\S]*?)\{%\s*endschema\s*%\}/)[1]);
const tpl = JSON.parse(fs.readFileSync(SRC + '/templates/page.gwp-promo.json', 'utf8')).sections.main;
const S = Object.assign({}, ...schema.settings.filter(x => x.id && x.default !== undefined).map(x => ({[x.id]: x.default})), tpl.settings);
const BL = tpl.block_order.map(k => tpl.blocks[k]);

const T1 = S.tier1_threshold * 100, T2 = S.tier2_threshold * 100, SHIP = S.ship_threshold * 100;
const esc = s => String(s == null ? '' : s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/"/g,'&quot;');
const cdn = (src, w) => src.split('?')[0] + '?width=' + w;
const cents = p => Math.round(parseFloat(p) * 100);
const short = c => '$' + (c % 100 === 0 ? c / 100 : (c / 100).toFixed(2));

/* ---- the clubs, from the blocks, priced and stocked from the live store ---- */
const clubs = BL.filter(b => b.type === 'club').map(b => {
  const p = P[b.settings.product];
  if (!p) throw new Error('no live product ' + b.settings.product);
  return { b, p, variants: p.variants.map(v => ({ id: v.id, opts: [v.option1, v.option2, v.option3].filter(x => x != null), available: v.available, price: cents(v.price) })) };
});

/* ---- the gift products, simulated from the REAL hats and polos ----
   In the store these become "Free Hat (Gift)" and "Free Polo (Gift)": one $0
   variant per design, each with that design's photo as its variant image. */
const hats = LIVE.filter(p => p.product_type === 'HAT');
const polos = LIVE.filter(p => p.product_type === 'Apparel');
let gid = 900000;
const GIFTS = {
  hat: { title: 'Free Hat (Gift)', options: ['Hat'],
    variants: hats.map(h => ({ id: ++gid, opts: [h.title], available: h.variants.some(v => v.available), price: 0, img: h.images[0] && h.images[0].src })) },
  polo: { title: 'Free Polo (Gift)', options: ['Polo', 'Size'],
    variants: polos.flatMap(po => po.variants.map(v => ({ id: ++gid, opts: [po.title, v.option1], available: v.available, price: 0, img: po.images[0] && po.images[0].src }))) }
};

function chipRow(variants, first, attr, names) {
  return '<div class="gwp-opts">' + names.map((name, ax) => {
    const vals = [...new Set(variants.map(v => v.opts[ax]))];
    if (attr === 'data-axis' && vals.length < 2) {
      return `<button type="button" hidden ${attr}="${ax}" data-val="${esc(vals[0])}" aria-pressed="true"></button>`;
    }
    const swatch = attr === 'data-gift-axis' && ax === 0;
    const btns = vals.map((val, i) => {
      const pressed = attr === 'data-axis' ? (first.opts[ax] === val) : (i === 0);
      if (swatch) {
        const img = (variants.find(v => v.opts[ax] === val) || {}).img;
        return `<button type="button" class="gwp-swatch" ${attr}="${ax}" data-val="${esc(val)}" aria-pressed="${pressed}" title="${esc(val)}"><img src="${cdn(img,160)}" width="72" height="72" loading="lazy" alt="${esc(val)}"></button>`;
      }
      return `<button type="button" class="lg-chip" ${attr}="${ax}" data-val="${esc(val)}" aria-pressed="${pressed}">${esc(val)}</button>`;
    }).join('');
    return `<div class="gwp-opt"><span class="lg-label">${esc(name)}</span><div class="gwp-chips${swatch ? ' gwp-swatches' : ''}" role="group" aria-label="${esc(name)}">${btns}</div></div>`;
  }).join('') + '</div>';
}

const cards = clubs.map(({ b, p, variants }) => {
  const fv = variants.find(v => v.available) || variants[0];
  const stock = variants.some(v => v.available);
  const pmin = Math.min(...variants.map(v => v.price));
  const img = p.images[(b.settings.image_index || 1) - 1] || p.images[0];
  const tag = pmin >= T2 ? `<span class="lg-tag lg-tag-gold gwp-unlock">${esc(S.tag_tier2)}</span>`
            : pmin >= T1 ? `<span class="lg-tag gwp-unlock">${esc(S.tag_tier1)}</span>` : '';
  return `<article class="lg-card gwp-card" data-pid="${p.id}"${stock ? '' : ' data-out'}>
  <span class="lg-card-ph gwp-cut"><img src="${cdn(img.src,700)}" width="700" height="700" loading="lazy" alt="${esc(p.title)}">${tag}</span>
  <span class="lg-card-bd"><span class="lg-card-nm">${esc(p.title)}</span><span class="lg-card-pr" data-price>${short(fv.price)}</span>
    <span class="lg-card-ln">${esc(b.settings.line)}</span></span>
  ${chipRow(variants, fv, 'data-axis', p.options.map(o => o.name))}
  <div class="gwp-buy">
    <div class="gwp-qty" role="group" aria-label="How many"><button type="button" data-qty="-1" aria-label="One fewer">&minus;</button><output data-qty-out>1</output><button type="button" data-qty="1" aria-label="One more">+</button></div>
    <button type="button" class="lg-btn lg-btn-line gwp-add" data-add data-variant-id="${fv.id}"${stock ? '' : ' disabled'}><span class="lb">${esc(stock ? S.add_label : S.soldout_label)}</span><span class="gwp-sp" aria-hidden="true"></span></button>
  </div>
</article>`;
}).join('\n');

const giftCard = (slot, tier, th, title, sub) => {
  const g = GIFTS[slot];
  return `<article class="lg-tile gwp-gift" id="gwp-gift-${slot}" tabindex="-1" data-gift="${slot}" data-gift-tier="${tier}" data-threshold="${th}" data-state="locked">
  <div class="gwp-gift-hd"><h3 class="lg-d3">${esc(title)}</h3><span class="lg-tag lg-tag-gold">${esc(S.free_tag)}</span></div>
  <p class="lg-body gwp-gift-sub">${esc(sub)}</p>
  <p class="gwp-lock lg-label" data-lock><svg viewBox="0 0 16 16" aria-hidden="true"><rect x="2.6" y="7" width="10.8" height="7.2" rx="1.4"/><path d="M5 7V4.9a3 3 0 0 1 6 0V7"/></svg><span data-lock-text></span></p>
  ${chipRow(g.variants, g.variants[0], 'data-gift-axis', g.options).replace('class="gwp-opts"', 'class="gwp-opts gwp-gift-opts"')}
  <div class="gwp-pick" data-pick hidden><p class="lg-meta gwp-picked" data-picked></p>
    <button type="button" class="lg-btn gwp-claim" data-claim data-variant-id="${g.variants[0].id}"><span class="lb">${esc(S.claim_label)}</span><span class="gwp-sp" aria-hidden="true"></span></button></div>
</article>`;
};

/* image_picker settings point at Shopify Files; the preview maps them to the local shoot copies */
const SHOOT_MAP = { 'gwp-hero-green-read.webp': 'green-read-fit', 'gwp-band-wedges.webp': 'two-gold-wedges', 'gwp-band-hat-mallet.webp': 'black-hat-mallet',
  'gwp-band-putter.webp': 'putter-in-hand', 'gwp-fit-sunset.webp': 'fit-sunset', 'gwp-reviews-hats.webp': 'two-hats-mallet', 'gwp-faq-cup.webp': 'from-the-cup' };
const pic = v => { if (!v) return ''; const f = String(v).split('/').pop(); const n = SHOOT_MAP[f]; if (!n) return '';
  fs.copyFileSync(path.join(ROOT, 'design/img/shoot-0918', n + '.webp'), path.join(OUT, f)); return f; };
const reviews = BL.filter(b => b.type === 'review').map(b => b.settings);
const faqs = BL.filter(b => b.type === 'faq').map(b => b.settings);
/* hero D, the same maths as the Liquid: the two threshold amounts go gold on their own */
const t1s = short(T1), t2s = short(T2);
let h1 = esc(S.hero_heading).split(t2s).join('<span class="gwp-num">' + t2s + '</span>').split(t1s).join('<span class="gwp-num">' + t1s + '</span>');
if (S.hero_gold_word) h1 = h1.replace(S.hero_gold_word, '<span class="gwp-num">' + S.hero_gold_word + '</span>');
/* stands in for the two hero image pickers */
const HATIMG = P['black-gold-classic-lucky-hat'].images[0].src, POLOIMG = P['gold-dust-classic-polo'].images[0].src;
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
  return `<div class="gwp-h-sum">
        <figure class="gwp-h-fig"><div class="gwp-h-tile"><img src="${cdn(si.src, 600)}" alt="${esc(sp.title)}"><span class="lg-tag">${price}</span></div><figcaption class="lg-label">${esc(sp.title)}</figcaption></figure>
        <span class="gwp-h-op" aria-hidden="true">+</span>
        <figure class="gwp-h-fig"><div class="gwp-h-tile${n === 2 ? ' gwp-h-pair' : ''}">${gift}<span class="lg-tag lg-tag-gold">${esc(n === 2 ? S.both_free_tag : S.free_tag)}</span></div><figcaption class="lg-label">${esc(S['sum_gift' + n + '_label'])}</figcaption></figure>
        <span class="gwp-h-op gwp-h-eq" aria-hidden="true">=</span>
        <div class="gwp-h-res"><b class="gwp-num-d">${price}</b><span>${esc(S['sum' + n + '_note'])}</span></div>
      </div>`;
};
const star = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 2 3 6.6 7 .8-5.2 4.9 1.4 7L12 17.8 5.8 21.3l1.4-7L2 9.4l7-.8z"/></svg>';
const logo = fs.readFileSync(ROOT + '/_src-logo-symbols.svg', 'utf8').match(/<symbol id="lg-lucky"[\s\S]*?<\/symbol>/)[0];

function foil(text, word) {
  const t = String(text), i = word ? t.indexOf(word) : -1;
  return i < 0 ? esc(t) : esc(t.slice(0, i)) + '<span class="lg-foil-word">' + esc(word) + '</span>' + esc(t.slice(i + word.length));
}

const island = JSON.stringify({ moneyFormat: '${{amount}}',
  gifts: Object.fromEntries(Object.entries(GIFTS).map(([k, g]) => [k, { title: g.title, variants: g.variants.map(({img, ...v}) => v) }])),
  products: clubs.map(c => ({ id: c.p.id, variants: c.variants })) });

const attrs = {
  'data-tier1': T1, 'data-tier2': T2, 'data-ship': SHIP,
  'data-gift1-short': S.tier1_short, 'data-gift2-short': S.tier2_short,
  'data-bar-gift1': S.bar_gift_1, 'data-bar-gift2': S.bar_gift_2,
  'data-copy-start': S.bar_start, 'data-copy-away1': S.bar_away_tier1, 'data-copy-away2': S.bar_away_tier2,
  'data-copy-pick': S.bar_pick, 'data-copy-hit1': S.bar_tier1_hit, 'data-copy-ship-away': S.bar_ship_away,
  'data-copy-hit2': S.bar_all_done, 'data-copy-locked': S.gift_locked_template,
  'data-copy-add': S.add_label, 'data-copy-adding': S.adding_label, 'data-copy-added': S.added_label,
  'data-copy-soldout': S.soldout_label, 'data-copy-claim': S.claim_label, 'data-copy-claimed': S.claimed_label,
  'data-copy-gift-lost': S.toast_gift_lost, 'data-copy-gift-won': S.toast_gift_won,
  'data-copy-error': S.toast_error, 'data-copy-soldout-gift': S.toast_gift_soldout
};

/* price table the stub cart charges from: every real variant, and $0 gifts */
const PRICE = {};
clubs.forEach(c => c.variants.forEach(v => PRICE[v.id] = { price: v.price, available: v.available, title: c.p.title }));
LIVE.forEach(p => p.variants.forEach(v => { if (!PRICE[v.id]) PRICE[v.id] = { price: cents(v.price), available: v.available, title: p.title }; }));
Object.values(GIFTS).forEach(g => g.variants.forEach(v => PRICE[v.id] = { price: 0, available: v.available, title: g.title }));

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lucky Golf · Free hat, free polo</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="lucky.css"><link rel="stylesheet" href="gwp-promo.css">
</head><body class="lg">
<svg width="0" height="0" style="position:absolute" aria-hidden="true">${logo}</svg>

<div class="lg-tick"><div class="lg-tick-in">
  <a href="#"><b>Free hat</b> with any club through Friday</a><a href="#">Free shipping over $198</a><a href="#">Sixty days to prove us wrong</a>
</div></div>
<header class="lg-hdr"><div class="lg-hdr-in">
  <a class="lg-logo" href="#" aria-label="Lucky Golf home"><svg viewBox="0 0 513.48 118.24" width="132" height="30" fill="currentColor"><use href="#lg-lucky"/></svg></a>
  <nav class="lg-nav" aria-label="Main"><a href="#">Wedges</a><a href="#">Putters</a><a href="#">Hybrid</a><a href="#">Apparel</a><a href="#">Our Story</a></nav>
  <div class="lg-hdr-act">
    <a href="#" aria-label="Search"><svg viewBox="0 0 24 24" width="21" height="21" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg></a>
    <button type="button" aria-label="Open bag"><img src="../../../../../../../../Users/wetzl/Lucky Golf/Website/img/mags-bag-light.webp" alt="" width="40" height="40" onerror="this.remove()"></button>
  </div>
</div></header>

<script type="application/json" id="gwp-data">${island}</script>
<div class="lg-scope gwp" id="gwp" data-ground="${S.ground}" data-yardage="${S.yardage ? 'on' : 'off'}" style="--gwp-top:72px;--gwp-contour-day:url(gwp-contour-day.svg);--gwp-contour-tw:url(gwp-contour-tw.svg)"
     ${Object.entries(attrs).map(([k, v]) => `${k}="${esc(v)}"`).join('\n     ')}>

  ${pic(S.hero_photo) ? `<section class="gwp-p-hero" style="--focus:${S.hero_focus || '60% 40%'};--focus-m:${S.hero_focus_m || '58% 40%'}">
    <img class="gwp-p-img" src="${pic(S.hero_photo)}" alt="" fetchpriority="high">
    <div class="lg-wrap gwp-p-in">
      <p class="lg-eyebrow gwp-p-eb">${esc(S.hero_eyebrow)}</p>
      <h1 class="lg-d1 gwp-h-h1">${h1}</h1>
      <p class="lg-lede gwp-h-lede">${esc(S.hero_sub)}</p>
      <div class="gwp-h-foot">
        <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">${esc(S.hero_cta)} <span aria-hidden="true">&rarr;</span></a>
        <ul class="gwp-h-trust" role="list">
          <li class="lg-label">${ICON.lock}${esc(S.trust_1)}</li><li class="lg-label">${ICON.back}${esc(S.trust_2)}</li><li class="lg-label">${ICON.ship}${esc(S.trust_3)}</li>
        </ul>
      </div>
    </div>
  </section>` : `<section class="gwp-h-hero">
    <div class="lg-wrap">
      <p class="lg-eyebrow">${esc(S.hero_eyebrow)}</p>
      <h1 class="lg-d1 gwp-h-h1">${h1}</h1>
      <p class="lg-lede gwp-h-lede">${esc(S.hero_sub)}</p>
      <div class="gwp-h-sums">${sumRow(1)}${sumRow(2)}</div>
      <div class="gwp-h-foot">
        <a class="lg-btn" href="#gwp-clubs" data-scroll-to="gwp-clubs">${esc(S.hero_cta)} <span aria-hidden="true">&rarr;</span></a>
        <ul class="gwp-h-trust" role="list">
          <li class="lg-label">${ICON.lock}${esc(S.trust_1)}</li><li class="lg-label">${ICON.back}${esc(S.trust_2)}</li><li class="lg-label">${ICON.ship}${esc(S.trust_3)}</li>
        </ul>
      </div>
    </div>
  </section>`}

  <div class="gwp-rail" id="gwp-rail" data-tier="0"><div class="gwp-rail-in">
    <div class="gwp-rail-copy">
      <div class="gwp-say-row"><p class="gwp-say" id="gwp-say" role="status" aria-live="polite" aria-atomic="true">${esc(S.bar_start)}</p>
        <a class="gwp-rail-pick" id="gwp-pick" href="#gwp-gifts" data-scroll-to="gwp-gifts" hidden>${esc(S.pick_label)} <span aria-hidden="true">&darr;</span></a></div>
      <div class="gwp-track" aria-hidden="true"><span class="gwp-fill" id="gwp-fill"></span><span class="gwp-ball" id="gwp-ball"></span>
        <span class="gwp-node" data-node="1" style="left:${(T1 / SHIP * 100).toFixed(4)}%"><i></i><b>${esc(S.node1_label)}</b></span>
        <span class="gwp-node" data-node="2" style="left:${(T2 / SHIP * 100).toFixed(4)}%"><i></i><b>${esc(S.node2_label)}</b></span>
        <span class="gwp-node" data-node="3" style="left:100%" data-last><i></i><b>${esc(S.node3_label)}</b></span></div>
    </div>
    <div class="gwp-rail-act"><span class="gwp-rail-sum"><span class="l lg-label">${esc(S.bar_subtotal_label)}</span><span class="v" id="gwp-rail-sum">$0.00</span></span>
      <a class="lg-btn lg-btn-line" href="#">${esc(S.checkout_label)}</a></div>
  </div></div>

  ${S.yardage ? `<div class="yd yd-tracer" id="gwp-tracer" data-tee="${esc(S.tee_label)}" aria-hidden="true"><div class="lg-wrap"></div></div>` : ''}

  <section class="lg-sec" id="gwp-clubs" tabindex="-1"><div class="lg-wrap">
    <p class="lg-eyebrow">${esc(S.clubs_eyebrow)}</p>
    <h2 class="lg-d2">${esc(S.clubs_heading)}</h2>
    <p class="lg-aside">${esc(S.clubs_aside)}</p>
    <div class="gwp-clubs">${cards}</div>
  </div></section>

  ${(S.band_1 || S.band_2 || S.band_3) ? `<section class="gwp-band-ph" aria-label="${esc(S.band_label)}">${[S.band_1, S.band_2, S.band_3].map((b, i) => pic(b) ? `<figure class="gwp-band-f${i === 0 ? ' w2' : ''}"><img src="${pic(b)}" alt="" loading="lazy"></figure>` : '').join('')}</section>` : ''}
  <section class="lg-sec" id="gwp-gifts"><div class="lg-wrap">
    <p class="lg-eyebrow">${esc(S.gift_eyebrow)}</p>
    <h2 class="lg-d2">${esc(S.gift_heading)}</h2>
    <p class="lg-body">${esc(S.gift_note)}</p>
    <div class="gwp-gifts-grid${pic(S.fit_photo) ? ' has-ph' : ''}">${pic(S.fit_photo) ? `<figure class="gwp-fit-ph"><img src="${pic(S.fit_photo)}" alt="" loading="lazy"><figcaption class="lg-label">${esc(S.fit_caption)}</figcaption></figure>` : ''}
    <div class="gwp-gift-row">${giftCard('hat', 1, T1, S.gift_hat_title, S.gift_hat_sub)}${giftCard('polo', 2, T2, S.gift_polo_title, S.gift_polo_sub)}</div></div>
  </div></section>

  <section class="lg-band${pic(S.reviews_photo) ? ' gwp-rev-ph' : ''}"${pic(S.reviews_photo) ? ` style="--rev-bg:url(${pic(S.reviews_photo)});--rev-pos:${S.reviews_focus || 'center 60%'}"` : ''}><div class="lg-wrap">
    <p class="lg-eyebrow">${esc(S.rev_eyebrow)}</p>
    <h2 class="lg-d2">${esc(S.rev_heading)}</h2>
    <div class="lg-grid gwp-revs">
      ${reviews.map(r => `<figure class="lg-band-tile gwp-rev"><span class="lg-stars" aria-label="${r.stars} out of 5">${star.repeat(r.stars)}</span>
        <blockquote>${esc(r.quote)}</blockquote>
        <figcaption class="lg-meta">${esc(r.name)} · ${esc(r.club)} ${r.verified ? `<span class="lg-stock">${esc(S.verified_label)}</span>` : ''}</figcaption></figure>`).join('\n      ')}
    </div>
  </div></section>

  <section class="lg-sec"><div class="lg-wrap gwp-faq-grid${pic(S.faq_photo) ? ' has-ph' : ''}"><div class="gwp-faq-wrap">
    <h2 class="lg-d2">${esc(S.faq_heading)}</h2>
    <div class="gwp-faq">
      ${faqs.map(f => `<details class="gwp-fq"><summary><span>${esc(f.q)}</span><span class="mk" aria-hidden="true"></span></summary><div class="gwp-fq-a">${f.a}</div></details>`).join('\n      ')}
    </div>
  </div>${pic(S.faq_photo) ? `<figure class="gwp-faq-ph"><img src="${pic(S.faq_photo)}" alt="" loading="lazy"></figure>` : ''}</div></section>

  <div class="gwp-bar" id="gwp-bar"><div class="gwp-bar-in">
    <span class="gwp-bar-sum"><span class="l lg-label">${esc(S.bar_subtotal_label)}</span><span class="v" id="gwp-bar-sum">$0.00</span></span>
    <span class="gwp-bar-gift" id="gwp-bar-gift" data-none>${esc(S.bar_no_gift)}</span>
    <a class="lg-btn" href="#">${esc(S.checkout_label)}</a>
  </div></div>
  <div class="gwp-toast" id="gwp-toast" hidden role="alert">${S.toast_mags ? '<img class="gwp-toast-mags" src="gwp-mags.webp" alt="" width="64" height="40" hidden>' : ''}<span data-toast-text></span></div>
</div>

<footer class="lg-ftr"><div class="lg-wrap">
  <div class="lg-ftr-in">
    <div><h3>Clubs</h3><ul><li><a href="#">Wedges</a></li><li><a href="#">Putters</a></li><li><a href="#">Hybrid</a></li></ul></div>
    <div><h3>Wear</h3><ul><li><a href="#">Polos</a></li><li><a href="#">Hats</a></li></ul></div>
    <div><h3>Help</h3><ul><li><a href="#">Shipping</a></li><li><a href="#">Returns</a></li><li><a href="#">Contact</a></li></ul></div>
  </div>
  <div class="lg-ftr-base"><span>&copy; 2026 Lucky Golf</span><span>It&rsquo;s better to be lucky.</span></div>
</div></footer>

<script>
(function(){
  var PRICE = ${JSON.stringify(PRICE)};
  var items = [], seq = 0;
  window.__calls = [];
  function body(){ var t = items.reduce(function(a,i){return a+i.line_price;},0);
    return { items: items.slice(), item_count: items.reduce(function(a,i){return a+i.quantity;},0), total_price: t, items_subtotal_price: t }; }
  function json(o, st){ return Promise.resolve(new Response(JSON.stringify(o), {status: st||200, headers:{'Content-Type':'application/json'}})); }
  window.fetch = function(url, opts){
    opts = opts || {}; var p = String(url).replace(/^https?:\\/\\/[^/]+/, '');
    var payload = opts.body ? JSON.parse(opts.body) : null; window.__calls.push({path:p, payload:payload});
    if (p.indexOf('cart.js') > -1) return json(body());
    if (p.indexOf('cart/add.js') > -1) {
      var it = payload.items[0], v = PRICE[it.id];
      if (!v) return json({status:404, description:'Cannot find variant'}, 404);
      if (!v.available) return json({status:422, description:'sold out'}, 422);
      var ex = items.filter(function(l){ return l.variant_id===it.id && JSON.stringify(l.properties||null)===JSON.stringify(it.properties||null); })[0];
      if (ex) { ex.quantity += it.quantity; ex.line_price = ex.quantity*v.price; ex.final_line_price = ex.line_price; }
      else items.push({ key:(++seq)+':k', variant_id:it.id, quantity:it.quantity, price:v.price, line_price:v.price*it.quantity,
        final_line_price:v.price*it.quantity, product_title:v.title, properties:it.properties||null });
      return json({items: payload.items});
    }
    if (p.indexOf('cart/change.js') > -1) {
      var i = items.findIndex(function(l){ return l.key === payload.id; });
      if (i < 0) return json({status:404, description:'line not found'}, 404);
      if (payload.quantity <= 0) items.splice(i,1);
      else { items[i].quantity = payload.quantity; items[i].line_price = items[i].price*payload.quantity; items[i].final_line_price = items[i].line_price; }
      return json(body());
    }
    return json({}, 404);
  };
  window.__cart = function(){ return body(); };
})();
</script>
<script src="gwp-promo.js" defer></script>
</body></html>`;

for (const f of ['lucky.css', 'gwp-promo.css', 'gwp-promo.js', 'gwp-contour-day.svg', 'gwp-contour-tw.svg', 'gwp-mags.webp']) fs.copyFileSync(SRC + '/assets/' + f, path.join(OUT, f));
fs.copyFileSync(ROOT + '/img/mags-bag-light.webp', path.join(OUT, 'mags-bag-light.webp'));
fs.writeFileSync(path.join(OUT, 'index.html'), html.replace('../../../../../../../../Users/wetzl/Lucky Golf/Website/img/mags-bag-light.webp', 'mags-bag-light.webp'));
console.log('wrote index.html ·', clubs.length, 'real clubs ·', GIFTS.hat.variants.length, 'real hats ·', GIFTS.polo.variants.length, 'real polo variants ·', reviews.length, 'real reviews');
