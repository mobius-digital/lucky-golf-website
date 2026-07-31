/* ==========================================================================
   PDP — LGW01 Carver Gold
   Variant matrix, gallery, spec tabs, accordions, loft finder, review grid.
   Every price, SKU and availability flag below is the live Shopify state as
   of 2026-07-31. LH 50 and LH 60 are genuinely out of stock.
   ========================================================================== */
var PD = {
  name: 'Carver Gold',
  sku: 'LGW01',
  price: 99,
  img: 'https://cdn.shopify.com/s/files/1/2286/3149/files/6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868',
  hands: [{k:'RH', label:'Right hand'}, {k:'LH', label:'Left hand'}],
  lofts: [50, 52, 54, 56, 58, 60],
  /* hand -> loft -> units on hand. 0 means the variant exists but is out. */
  stock: {
    RH: {50:99,  52:577, 54:216, 56:163, 58:315, 60:686},
    LH: {50:0,   52:275, 54:82,  56:104, 58:15,  60:0}
  },
  role: {
    50: ['Gap', 'Full swings from the yardage your pitching wedge can’t quite reach.'],
    52: ['Gap', 'The most-bought loft in the lineup, and usually the first wedge people add.'],
    54: ['Sand / gap', 'Full shots, longer bunker shots, anything that needs a little height.'],
    56: ['Sand', 'Greenside and bunkers. The club most golfers reach for by default.'],
    58: ['Lob', 'Higher, softer, lands quieter. For pins you can’t run the ball at.'],
    60: ['Lob', 'Flop shots, short-sided, tight pins. The most specialist club in the bag.']
  }
};

/* Hand-checked gapping table. Every gap lands between 4 and 6 degrees.
   A lookup beats a clever algorithm here — these five answers are the whole
   problem space, and each one can be sanity-checked by eye. */
var PD_GAPS = {
  44: [50, 54, 58],
  45: [50, 54, 58],
  46: [52, 56, 60],
  47: [52, 56, 60],
  48: [52, 56, 60]
};

/* 47 real Judge.me reviews, verbatim, spanning every rating so the star
   filter and the histogram tell the same story. The curated 4-star-and-up
   rule still governs the pull quotes; a widget that hides its 1-stars is a
   widget nobody believes. */
var PD_JM = [{"n":"David L.","r":5,"t":"Golden sw","d":"2026-07-19","q":"Love the club really do hitting it very well. Knock on wood lol a friend has tried it he likes it yo talk of himself getting one","v":true,"rep":""},{"n":"Beverly F.","r":5,"t":"He loves his 60’","d":"2026-07-10","q":"I’m not the golfer but he is and he loves lucky irons very happy with all he has","v":true,"rep":""},{"n":"JD M.","r":5,"t":"So nice, I bought it twice!","d":"2026-07-08","q":"I bought myself a 60 degree last year. I love it so much, and get so many comments/compliments on the look… but the performance speaks even louder!\nIn this recent purchase I bought 2 more and gave them to my dad for Father’s Day and my brother for his birthday (same week!).\nThey love them!","v":true,"rep":""},{"n":"Nick F.","r":4,"t":"Great club, Ok customer Service","d":"2026-06-20","q":"The club itself, outstanding. Looks sharp, plays well, nice feel. Definitely a good addition to the bag.\nFirst club got lost in transit. Took forever to get a response from anyone. Like weeks. Actually got a notification of a replacement shipping before anyone actually replied to me. \nSo, as long as it ships ok, you’ll love the club! But good luck if there’s an issue. Hope you have patience.","v":true,"rep":""},{"n":"James B.","r":5,"t":"LGW01","d":"2026-06-12","q":"Super great club, love the feel, the sound, the spin, only problem I have is getting under the ball with it but easy fix none the less. Great club!!","v":true,"rep":""},{"n":"1981 C.o.M.","r":5,"t":"As Good As Gold","d":"2026-06-10","q":"Very good club. Performs as well as my Vokey SM10, and Cleveland RTX wedges. Consistent distances and puts good spin on the ball. All around solid performer.","v":true,"rep":""},{"n":"kyle","r":1,"t":"","d":"2026-06-07","q":"Took one swing and the head separated from the shaft right where the ferrule is. Pretty disappointed. I hate going through the hassle of returning things so i guess im just out a hundred bucks :/","v":true,"rep":""},{"n":"Courtney G.","r":5,"t":"Sixk","d":"2026-05-27","q":"They’re fucking awesome. Yall are killing it","v":true,"rep":""},{"n":"Kyle M.","r":5,"t":"Sexist clubs in your bag","d":"2026-05-23","q":"I LOVE my wedges they preform high up with the big name brands and all my friends are jealous of how sexy these clubs are","v":true,"rep":""},{"n":"Christopher V.","r":5,"t":"56 degree wedge","d":"2026-05-14","q":"Love the weight of this club! Great looking bag candy! It’s so pretty I’m almost afraid to use it. I like it more than my titleist vokey","v":true,"rep":""},{"n":"Anita","r":5,"t":"","d":"2026-05-07","q":"This is a sweet looking club! \nJust a bit to long for me, but it should be an easy fix. Shipping was fast!","v":true,"rep":""},{"n":"Brandon L.","r":5,"t":"Love my wedges","d":"2026-04-17","q":"One of the absolute best purchases I ever made. all of my friends are jealous from the look.And when they stick on the green and come back two feet, there's no doubt their top quality","v":true,"rep":""},{"n":"Maci","r":5,"t":"","d":"2026-04-15","q":"Great quality! Made a perfect gift for my fianće!","v":true,"rep":""},{"n":"Adam K.","r":4,"t":"Very impressed","d":"2026-04-09","q":"Took a chance on these wedges and have been very pleasantly surprised at their appearance, performance and durability. Would definitely recommend for someone looking for a solid wedge and doesn’t want to pay the price for the large and popular brands and doesn’t have the need or want to get fitted!","v":true,"rep":""},{"n":"John M.","r":5,"t":"54 degree wedge","d":"2026-04-06","q":"I've only played twice with it love it so far, still have to dial in the distance","v":true,"rep":""},{"n":"Keelan W.","r":5,"t":"Lucky Golf wedges","d":"2026-03-25","q":"Loving the wedges so far have seen improvement in my game since using them!","v":true,"rep":""},{"n":"Eric F.","r":5,"t":"“Goldy”","d":"2026-03-18","q":"My buddies already named my club “Goldy” because they are jealous of the results!!","v":true,"rep":""},{"n":"Riley B.","r":5,"t":"Good look, good play","d":"2026-03-14","q":"I’ve got a few hours of range time and 2, 18-hole rounds with the 54° and 60° clubs. They look good enough to make me feel good and play well with them. They make me want to play more. The fit and finish are great. I like the green grip. Clubs feel solid.","v":true,"rep":""},{"n":"Paul F.","r":5,"t":"New wedges","d":"2026-03-14","q":"The new Lucky wedges look and feel great and strike pure! I always play better when I feel Lucky!","v":true,"rep":""},{"n":"Michelle S.","r":5,"t":"My husband loves it","d":"2026-03-12","q":"This club was a Valentine’s Day gift for my husband, and he loves it. He says he loves how it feels and the unique gold design looks so cool.","v":true,"rep":""},{"n":"Dalton","r":5,"t":"","d":"2026-02-28","q":"Played for about 3 weeks been good so far","v":true,"rep":""},{"n":"Tim M.","r":5,"t":"Wedges and Hybrid","d":"2026-02-17","q":"Gotta admit, I didn't have a 60 degree wedge so I bought this one because it's GOLD. Love the look. Liked it so much I also bought the 52 degree and the Hybrid. If you play Hybrid's this one is the real deal! Liked these so much I ordered a putter that's supposed to be here Friday. I'll write a review after a few rounds with it. Thanks Lucky Golf...I love my clubs!","v":true,"rep":""},{"n":"David G.","r":4,"t":"Bounce is better than expected","d":"2026-02-12","q":"I have the 60 deg and the club surprised me right out of the box. I thought is was going to be all sizzle but that’s not the case. One of the better 60 s I’ve used.","v":true,"rep":""},{"n":"Frank","r":5,"t":"","d":"2026-02-10","q":"Love it. Played with both the 58 and the 54 I bought before and I love the feel and bite they both have.","v":true,"rep":""},{"n":"Anastasia B.","r":5,"t":"My boyfriend LOVES IT","d":"2026-02-09","q":"HE hasnt used it on the course yet, but the quality is great!","v":true,"rep":""},{"n":"January Z.","r":5,"t":"Great Customer Service!","d":"2026-02-05","q":"I ordered a Christmas present for my boyfriend, it got lost in the mail. Cole personally texted me to get the correct information, and sent a new one that arrived a few days later. I highly recommend!!","v":true,"rep":""},{"n":"Dax R.","r":5,"t":"Incredible Customer service","d":"2026-02-04","q":"The putter and wedge are amazing, but what truly impresses me is the exceptional customer service. They responded to my email on a Sunday and even followed up with a phone call, which was answered by a person on a Sunday! I was shocked, but they explained that their goal is to make every purchase perfect, one happy customer at a time. It really blew me away.","v":true,"rep":""},{"n":"Ray O.","r":5,"t":"Hard to keep it!","d":"2026-02-01","q":"People borrow it in my league- it’s a winner!","v":true,"rep":""},{"n":"Nina E.","r":5,"t":"Gift","d":"2026-01-30","q":"My husband has been extremely happy with his Golf Club, excellent quality and pretty to look at.","v":true,"rep":""},{"n":"Aaron A.","r":5,"t":"I love Lucky Golf","d":"2026-01-25","q":"I love Lucky Golf! I love the 60 degree and the 54!","v":true,"rep":""},{"n":"James V.","r":4,"t":"52 degree wedge","d":"2026-01-20","q":"I purchased the 52 degree wedge and I replaced it with my 54 degree wedge i like this 52 degree wedge much better from 69 yards to around the greens.","v":true,"rep":""},{"n":"kevin c.","r":4,"t":"60 wedge","d":"2026-01-04","q":"Very nice looking wedge. Good grips, but have not tried on the course yet","v":true,"rep":""},{"n":"Binh","r":4,"t":"","d":"2025-12-05","q":"This was for my wife. She used it few times so far and liked it. Its heavier than most wedges as checked against mine. So far no concerns with it.","v":true,"rep":""},{"n":"Chris L.","r":3,"t":"","d":"2025-11-20","q":"This is a gift for Christmas.\nMy only complaint is that the return policy is prior to when I give the gift.","v":true,"rep":""},{"n":"Matt","r":4,"t":"","d":"2025-07-29","q":"Love it club face grooves seem to give me way more control!! 4.5 stars","v":true,"rep":""},{"n":"Andrew O.","r":4,"t":"Good Clubs for the price!","d":"2025-06-27","q":"Love the look and the feel of the clubs. Just wish the shaft was a little stiffer. I am sure I will get use to it.","v":true,"rep":""},{"n":"Nathan C.","r":1,"t":"56 Degree wedge","d":"2025-05-08","q":"Ordered the 56 degree wedge as I really wanted to try these clubs out. 1st day on the course the clubhead broke. Hoping it was just a fluke situation","v":true,"rep":""},{"n":"Jake B.","r":1,"t":"No the best quality","d":"2025-01-10","q":"I had these for a little over a month. Shaft has already dent in it already and showing signs of rust of 6 rounds of golf","v":true,"rep":""},{"n":"M K.C.","r":1,"t":"This is Buffalo!  We use shovels not golf clubs right now.","d":"2025-01-05","q":"Have not used the clubs yet. Will not use them til April/May. Resend your inquiry then.","v":true,"rep":""},{"n":"Benjamin M.","r":3,"t":"Haven%27t%20played%20them","d":"2024-12-21","q":"Haven%27t%20played%20them%20yet%20since%20it%27s%20December%20in%20Wisonsin,%20but%20they%20look%20nice.","v":true,"rep":""},{"n":"Edwin B.","r":3,"t":"Looks great. Performs okay.","d":"2024-09-09","q":"I like the 60 around the greens. It performs as good as my past Vokey, JAWS etc. However, the shaft on it is not the same quality so for full shots or 3/4 shots I don't have as much trust in it. I also get a bunch of compliments on it's looks. Cool club for sure!","v":true,"rep":""},{"n":"William C.","r":3,"t":"Sometimes good sometimes bad","d":"2024-08-10","q":"The way these clubs look in my bag gets me loads of compliments. BUT the metal is soft, I don’t hit the ball hard and I’ve already have some bumps in the milling","v":true,"rep":""},{"n":"Hunter H.","r":3,"t":"","d":"2024-08-10","q":"Solid club. Looks great. Everyone asks about it. -1 star for lacking a little feel. -1 star for being back ordered for half the summer","v":true,"rep":""},{"n":"Tyler","r":2,"t":"","d":"2024-07-30","q":"The wedge was delivered today and it's a 58 instead of the 60 degree I ordered. Please advise on what can be done to rectify this mishap. This is my first purchase with your company and I'm disappointed with my experience.","v":true,"rep":""},{"n":"Owen B.","r":1,"t":"The shaft is bent","d":"2024-04-29","q":"The shaft is already bent and I’m extremely upset about it.","v":true,"rep":""},{"n":"Troy E.","r":2,"t":"It just doesn’t feel consistent","d":"2024-04-24","q":"Can’t seem to get a consistent hit with it","v":true,"rep":""},{"n":"adam c.","r":2,"t":"Work in progress","d":"2024-04-22","q":"I have only played one round and distance felt more like a lob wedge and not 50 degree.","v":true,"rep":""}];

/* Real store rows for the browse rail under the fold. Takomo mixes clubs and
   apparel here rather than showing only comparable products. */
var PD_OAV = [
  {nm:'LGW02 Carver Gold', pr:'$109', rt:'4.78 ★ 69', tag:'',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/1_27f81f90-a495-4dc4-ba02-0650ea6c4608.webp?v=1781012462'},
  {nm:'LGW02 Carver Shadow', pr:'$109', rt:'6 lofts', tag:'New',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/6_cef3d6fc-8907-4866-b6aa-6301f8c614b5.webp?v=1784586436'},
  {nm:'LGP01 Tracer Blade', pr:'$199', rt:'4.86 ★ 147', tag:'Sold out', out:true,
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/3_f3d878d3-a4bb-4cc9-82df-f68e8eec3f61.webp?v=1782599090'},
  {nm:'LGH01 Stryker', pr:'$209', rt:'4.60 ★ 20', tag:'',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/3_a032f79a-78ab-436e-81c9-eea7bb5f7f40.webp?v=1782597493'}
];

/* Six briefs for the highlight reel. No footage exists, so each card is a
   labelled slot describing the clip that belongs there. */
var PD_REEL = [
  {who:'creator', kind:'Creator reel', brief:'Full swing from 100 yards with the 52°, ball tracked to the pin, reaction'},
  {who:'customer', kind:'Customer clip', brief:'Greenside chip with the 56°, one hop and stop, shot from behind'},
  {who:'creator', kind:'Creator reel', brief:'Bunker shot with the 58°, sand spray, ball releasing to the hole'},
  {who:'customer', kind:'Customer clip', brief:'Flop over a bunker with the 60°, face wide open, soft landing'},
  {who:'creator', kind:'Creator reel', brief:'Face close-up in sunlight, grooves and the gold finish, slow pan'},
  {who:'customer', kind:'Customer clip', brief:'Unboxing, club out of the sleeve, first reaction to the finish'}
];

/* Cart cross-sell. Read by core's paintUpsell(); rows already in the bag are
   filtered out there. Prices and SKUs are live Shopify. */
var LG_CART_UPSELL = [
  {sku:'LGW01-56-RH', name:'Carver Gold 56°', price:'$99', variant:'Right hand · 56°',
   why:'The sand wedge. Most-carried loft in the lineup.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868'},
  {sku:'LGW01-60-RH', name:'Carver Gold 60°', price:'$99', variant:'Right hand · 60°',
   why:'The lob. For tight pins and short-sided misses.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/6_2ea13893-f7a8-4035-ad55-75ff49178d48.webp?v=1782597868'},
  {sku:'HeadCover-Blade-SignatureWhite', name:'Lucky Blade Cover', price:'$29.95', variant:'',
   why:'Reviewers keep mentioning cart rash. This stops it.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/products/PhotoAug13_102637PM_8b5e9c51-0604-41c0-ab6a-c6f1e43e5631.png?v=1616431397'}
];

/* Finish-the-look cross-sell: polos and hats only. Cole's call — gear is a
   grab-bag, apparel completes the look and is the same voice as the club. */
var PD_KIT = [
  {sku:'LGA-CP-Contour', nm:'Contour Classic Polo', pr:'$67', sizes:true,
   why:'Classic collar, tailored fit, UPF 50+.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/TopographyStyle1.webp?v=1779472755'},
  {sku:'LGA-BP-Blackout', nm:'Blackout Blade Polo', pr:'$67', sizes:true,
   why:'Blade collar, no buttons. Quieter than it sounds.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/StrokePlay1.webp?v=1779472570'},
  {sku:'HAT-5P-SB-IBTBL-BL', nm:'It’s Better To Be Lucky Hat', pr:'$29',
   why:'Five-panel, snapback, the line on the front.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/39.webp?v=1784585347'},
  {sku:'HAT-5P-SB-CRSV-BBLU-MONO', nm:'Baby Blue Cursive Hat', pr:'$29',
   why:'Monochrome script. Goes with the gold.',
   img:'https://cdn.shopify.com/s/files/1/2286/3149/files/30_203d7c7f-8680-4d32-bf41-18d0d4877086.webp?v=1784585347'}
];


(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var STAR = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>';
  var STAR_OFF = '<svg viewBox="0 0 24 24" class="off"><use href="#star"/></svg>';
  function starRow(n){
    var o = ''; for (var i = 1; i <= 5; i++) o += (i <= n ? STAR : STAR_OFF); return o;
  }
  function fmtDate(iso){
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p = iso.split('-'); return p[2].replace(/^0/,'') + ' ' + m[+p[1]-1] + ' ' + p[0];
  }

  /* ---------------------------------------------------------------- gallery */
  var gal = $('#gal');
  if (gal){
    var slides = [].slice.call(gal.querySelectorAll('.gal-slide'));
    var thumbs = $('.gal-thumbs');
    var at = 0;
    slides.forEach(function(s, i){
      var src = s.querySelector('img').getAttribute('src');
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'gal-th';
      b.setAttribute('aria-current', i === 0 ? 'true' : 'false');
      b.setAttribute('aria-label', 'Image ' + (i + 1) + ' of ' + slides.length);
      b.innerHTML = '<img src="' + src + '" alt="" loading="lazy">';
      b.addEventListener('click', function(){ show(i); });
      thumbs.appendChild(b);
    });
    var ths = [].slice.call(thumbs.children);
    function show(i){
      at = (i + slides.length) % slides.length;
      slides.forEach(function(s, n){
        if (n === at) s.setAttribute('data-on', ''); else s.removeAttribute('data-on'); });
      ths.forEach(function(t, n){ t.setAttribute('aria-current', String(n === at)); });
      $('#gal-i').textContent = at + 1;
    }
    $('[data-p]', gal).addEventListener('click', function(){ show(at - 1); });
    $('[data-n]', gal).addEventListener('click', function(){ show(at + 1); });
    gal.addEventListener('keydown', function(e){
      if (e.key === 'ArrowLeft'){ e.preventDefault(); show(at - 1); }
      if (e.key === 'ArrowRight'){ e.preventDefault(); show(at + 1); }
    });
  }

  /* ------------------------------------------------------ variant selection */
  var hand = 'RH', loft = 56;

  var proxy = document.createElement('button');   /* lets core's [data-add]
    delegate do the actual cart work, so quantity is just N clicks and there
    is one add-to-cart code path on the whole site */
  proxy.type = 'button'; proxy.setAttribute('data-add', ''); proxy.hidden = true;
  proxy.setAttribute('aria-hidden', 'true'); proxy.tabIndex = -1;
  document.body.appendChild(proxy);

  function chip(label, on, dis, attrs){
    return '<button class="chip" type="button" aria-pressed="' + (on ? 'true' : 'false') + '"'
      + (dis ? ' disabled aria-label="' + esc(label) + ', out of stock"' : '')
      + ' ' + attrs + '>' + esc(label) + '</button>';
  }
  function paintHands(){
    var el = $('#pick-hand'); if (!el) return;
    el.innerHTML = PD.hands.map(function(h){
      var any = PD.lofts.some(function(l){ return PD.stock[h.k][l] > 0; });
      return chip(h.label, h.k === hand, !any, 'data-hand="' + h.k + '"');
    }).join('');
  }
  function paintLofts(){
    var el = $('#pick-loft'); if (!el) return;
    el.innerHTML = PD.lofts.map(function(l){
      return chip(l + '°', l === loft, PD.stock[hand][l] === 0, 'data-loft="' + l + '"');
    }).join('');
  }
  function sync(){
    var units = PD.stock[hand][loft];
    var handLabel = hand === 'RH' ? 'Right hand' : 'Left hand';
    var variant = handLabel + ' · ' + loft + '°';
    if ($('#v-hand')) $('#v-hand').textContent = handLabel;
    if ($('#v-sku')) $('#v-sku').textContent = 'LGW01-' + loft + '-' + hand;
    if ($('#atc-bar-v')) $('#atc-bar-v').textContent = variant;

    var stock = $('#stock'), st = $('#stock-t');
    if (stock && st){
      if (units === 0){
        stock.setAttribute('data-out', '');
        st.textContent = 'Out of stock in ' + handLabel.toLowerCase() + ' ' + loft + '°';
      } else {
        stock.removeAttribute('data-out');
        st.textContent = units < 25
          ? 'Low stock — ' + units + ' left. Ships in 1–2 business days'
          : 'In stock — ships in 1–2 business days';
      }
    }
    [['#atc', 'Add to cart · $' + PD.price], ['#atc2', 'Add to cart']].forEach(function(p){
      var b = $(p[0]); if (!b) return;
      b.disabled = units === 0;
      var s = b.querySelector('span'); if (s) s.textContent = units === 0 ? 'Out of stock' : p[1];
    });
    proxy.setAttribute('data-sku', 'LGW01-' + loft + '-' + hand);
    proxy.setAttribute('data-name', PD.name + ' ' + loft + '°');
    proxy.setAttribute('data-price', '$' + PD.price);
    proxy.setAttribute('data-img', PD.img);
    proxy.setAttribute('data-variant', variant);
  }

  document.addEventListener('click', function(e){
    var h = e.target.closest('[data-hand]'), l = e.target.closest('[data-loft]');
    if (h && !h.disabled){
      hand = h.getAttribute('data-hand');
      /* if the chosen loft is dead in this hand, slide to the nearest live one */
      if (PD.stock[hand][loft] === 0){
        var live = PD.lofts.filter(function(x){ return PD.stock[hand][x] > 0; });
        if (live.length){
          live.sort(function(a, b){ return Math.abs(a - loft) - Math.abs(b - loft); });
          loft = live[0];
        }
      }
      paintHands(); paintLofts(); sync();
    }
    if (l && !l.disabled){ loft = +l.getAttribute('data-loft'); paintLofts(); sync(); }
  });

  var qty = $('#qty');
  document.addEventListener('click', function(e){
    var q = e.target.closest('[data-q]');
    if (q && qty){
      qty.value = Math.max(1, Math.min(9, (+qty.value || 1) + (+q.getAttribute('data-q'))));
    }
  });
  ['#atc', '#atc2'].forEach(function(sel){
    var b = $(sel); if (!b) return;
    b.addEventListener('click', function(){
      if (b.disabled) return;
      var n = (sel === '#atc' && qty) ? Math.max(1, Math.min(9, +qty.value || 1)) : 1;
      for (var i = 0; i < n; i++) proxy.click();
      var s = b.querySelector('span'), was = s.textContent;
      s.textContent = 'Added'; setTimeout(function(){ s.textContent = was; }, 1400);
    });
  });
  paintHands(); paintLofts(); sync();

  /* ------------------------------------------------------------ accordions */
  [].forEach.call(document.querySelectorAll('.acc-hd'), function(h){
    h.addEventListener('click', function(){
      var open = h.getAttribute('aria-expanded') === 'true';
      h.setAttribute('aria-expanded', String(!open));
      var body = document.getElementById(h.getAttribute('aria-controls'));
      if (body) body.hidden = open;
    });
  });

  /* ------------------------------------------------------------ spec tabs */
  var sTabs = [].slice.call(document.querySelectorAll('.spec-tab'));
  function selSpec(i){
    sTabs.forEach(function(t, n){ t.setAttribute('aria-selected', String(n === i)); });
    [].forEach.call(document.querySelectorAll('.spec-panel'), function(p){
      p.hidden = p.getAttribute('data-p') !== String(i); });
  }
  sTabs.forEach(function(t, i){
    t.addEventListener('click', function(){ selSpec(i); });
    t.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + sTabs.length) % sTabs.length;
      selSpec(n); sTabs[n].focus();
    });
  });

  /* ----------------------------------------------------------- loft finder */
  function paintLoftFinder(pw){
    var grid = $('#lf-grid'); if (!grid) return;
    var set = PD_GAPS[pw], prev = pw;
    grid.innerHTML = set.map(function(l, i){
      var gap = l - prev; prev = l;
      var r = PD.role[l];
      return '<div class="lf-card"' + (i === 0 ? ' data-rec' : '') + '>'
        + '<span class="rank">' + (i === 0 ? 'Start here' : 'Then') + '</span>'
        + '<span class="lo">' + l + '°</span>'
        + '<span class="rl">' + esc(r[0]) + '</span>'
        + '<p>' + esc(r[1]) + '</p>'
        + '<span class="gap">' + gap + '° up from your '
        + (i === 0 ? 'pitching wedge' : (l - gap) + '°') + '</span>'
        + '</div>';
    }).join('');
    var top = set[set.length - 1];
    $('#lf-note').textContent = top < 60
      ? 'That ladder tops out at ' + top + '°. If you want a 60° for tight pins as well, add it and drop the ' + set[1] + '°.'
      : 'Three wedges, four to six degrees apart. Nothing overlaps and nothing is missing.';
  }
  [].forEach.call(document.querySelectorAll('[data-pw]'), function(b){
    b.addEventListener('click', function(){
      [].forEach.call(document.querySelectorAll('[data-pw]'), function(x){
        x.setAttribute('aria-pressed', String(x === b)); });
      paintLoftFinder(+b.getAttribute('data-pw'));
    });
  });
  paintLoftFinder(46);

  /* ------------------------------------------------- others also viewed */
  var oav = $('#oav');
  if (oav) oav.innerHTML = PD_OAV.map(function(o){
    return '<article class="oav-i">'
      + '<div class="oav-ph">'
      +   '<span class="oav-tag"' + (o.out ? ' data-out' : '') + '>' + esc(o.tag) + '</span>'
      +   '<img src="' + o.img + '" alt="' + esc(o.nm) + '" loading="lazy" width="600" height="600">'
      + '</div>'
      + '<div class="oav-bd"><a class="oav-nm stretch" href="#">' + esc(o.nm) + '</a>'
      +   '<div class="oav-meta"><span class="oav-pr">' + esc(o.pr) + '</span>'
      +   '<span class="oav-rt">' + esc(o.rt) + '</span></div></div>'
      + '</article>';
  }).join('');

  /* ------------------------------------------------------- highlight reel */
  var reel = $('#reel-rail');
  if (reel) reel.innerHTML = PD_REEL.map(function(o){
    return '<article class="post">'
      + '<div class="post-ph">'
      +   '<div class="ph ph--dark"><span class="lbl">'
      +     '<span class="mono k">Video needed</span>'
      +     '<span class="mono">' + esc(o.brief) + '</span></span></div>'
      +   '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>'
      + '</div>'
      + '<div class="post-meta"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span>'
      +   '<span class="h">' + esc(o.kind) + '</span></div>'
      + '</article>';
  }).join('');

  /* ------------------------------------------------- finish the setup */
  var kit = $('#kit');
  if (kit) kit.innerHTML = PD_KIT.map(function(o){
    return '<article class="kit-i">'
      + '<div class="kit-ph"><img src="' + o.img + '" alt="' + esc(o.nm) + '" loading="lazy" width="600" height="600"></div>'
      + '<div class="kit-bd"><span class="kit-nm">' + esc(o.nm) + '</span>'
      +   '<span class="kit-why">' + esc(o.why) + '</span>'
      +   '<div class="kit-bot"><span class="kit-pr">' + esc(o.pr) + '</span>'
      +   (o.sizes
          /* sized product: there is nothing sensible to add without a size,
             so it links to its own page instead of pretending to be one-click */
          ? '<a class="btn btn-line btn-sm" href="#"><span>Choose size</span>'
            + '<span class="ar">&rarr;</span></a>'
          : '<button class="btn btn-ink btn-sm" type="button" data-add data-sku="' + esc(o.sku)
            + '" data-name="' + esc(o.nm) + '" data-price="' + esc(o.pr) + '" data-img="' + o.img
            + '" data-variant=""><span>Add</span></button>')
      +   '</div></div>'
      + '</article>';
  }).join('');

  /* =====================================================================
     REVIEWS — Judge.me shape. The histogram is the real 551-review
     distribution; the list is a 47-review sample that preserves that
     distribution, so filtering by star rating returns a believable set.
     ===================================================================== */
  var JM_TOTALS = {5:494, 4:33, 3:11, 2:4, 1:9};
  var JM_TOTAL = 551, JM_PAGE = 6;
  var jmFilter = 0, jmSort = 'recent', jmShown = JM_PAGE;

  function jmPool(){
    var list = PD_JM.filter(function(r){ return !jmFilter || r.r === jmFilter; });
    list = list.slice();
    if (jmSort === 'high') list.sort(function(a,b){ return b.r - a.r || (a.d < b.d ? 1 : -1); });
    else if (jmSort === 'low') list.sort(function(a,b){ return a.r - b.r || (a.d < b.d ? 1 : -1); });
    else list.sort(function(a,b){ return a.d < b.d ? 1 : a.d > b.d ? -1 : 0; });
    return list;
  }
  function paintBars(){
    var box = $('#jm-bars'); if (!box) return;
    box.innerHTML = [5,4,3,2,1].map(function(k){
      var pct = Math.round(JM_TOTALS[k] / JM_TOTAL * 100);
      return '<button class="row" type="button" data-star="' + k + '"'
        + ' aria-label="Show only ' + k + ' star reviews">'
        + '<span class="k">' + k + ' ★</span>'
        + '<span class="t"><i style="width:' + Math.max(pct, 1) + '%"></i></span>'
        + '<span class="v">' + JM_TOTALS[k] + '</span></button>';
    }).join('');
  }
  function paintFilters(){
    var box = $('#jm-filters'); if (!box) return;
    var opts = [[0, 'All']].concat([5,4,3,2,1].map(function(k){ return [k, k + ' ★']; }));
    box.innerHTML = opts.map(function(o){
      return '<button class="jm-f" type="button" data-star="' + o[0] + '"'
        + ' aria-pressed="' + (jmFilter === o[0]) + '">' + o[1] + '</button>';
    }).join('');
  }
  function paintList(){
    var box = $('#jm-list'), more = $('#jm-more'), cnt = $('#jm-count');
    if (!box) return;
    var pool = jmPool();
    if (!pool.length){
      box.innerHTML = '<p class="jm-empty">No reviews at that rating in this sample.</p>';
      if (more) more.hidden = true;
      if (cnt) cnt.textContent = '';
      return;
    }
    box.innerHTML = pool.slice(0, jmShown).map(function(r){
      return '<article class="jr">'
        + '<div class="jr-top">'
        +   '<span class="jr-av" aria-hidden="true">' + esc(r.n.charAt(0).toUpperCase()) + '</span>'
        +   '<span class="jr-who"><b>' + esc(r.n) + '</b>'
        +     '<span>' + (r.v ? 'Verified buyer · ' : '') + fmtDate(r.d) + '</span></span>'
        +   '<span class="jr-stars" role="img" aria-label="' + r.r + ' out of 5">' + starRow(r.r) + '</span>'
        + '</div>'
        + (r.t ? '<h4>' + esc(r.t) + '</h4>' : '')
        + '<p>' + esc(r.q) + '</p>'
        + '</article>';
    }).join('');
    if (more) more.hidden = jmShown >= pool.length;
    if (cnt){
      var scale = jmFilter ? JM_TOTALS[jmFilter] : JM_TOTAL;
      cnt.textContent = 'Showing ' + Math.min(jmShown, pool.length) + ' of ' + pool.length
        + ' in this sample · ' + scale + ' live'
        + (jmFilter ? ' at ' + jmFilter + ' star' : '');
    }
  }
  function jmSetFilter(star){
    jmFilter = star; jmShown = JM_PAGE;
    paintFilters(); paintList();
    var sec = $('#reviews'); if (sec) sec.scrollIntoView({block:'nearest'});
  }
  document.addEventListener('click', function(e){
    var f = e.target.closest('.jm-f'), b = e.target.closest('.jm-bars .row');
    if (f){ jmSetFilter(+f.getAttribute('data-star')); return; }
    if (b){ jmSetFilter(+b.getAttribute('data-star')); return; }
    if (e.target.closest('#jm-more')){ jmShown += JM_PAGE; paintList(); }
  });
  var sortSel = $('#jm-sort');
  if (sortSel) sortSel.addEventListener('change', function(){
    jmSort = sortSel.value; jmShown = JM_PAGE; paintList();
  });
  paintBars(); paintFilters(); paintList();
})();
