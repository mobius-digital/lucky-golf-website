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

/* Nine real Judge.me reviews, 4 star and up, verbatim. Long bodies are cut at
   a sentence boundary and marked. Nothing is paraphrased or invented.
   Deliberately includes one honest 4-star: a page of nothing but 5s reads
   fake, and Cole's rule is a 4-star floor, not a 5-star floor. */
var PD_REVIEWS = [
  {n:'Rick M.', r:5, t:'No wedge like these!', d:'2026-03-09',
   q:'First thing I noticed was the quality. The Lucky Golf wedge feels solid the moment you pick it up. It’s made from forged carbon steel, so the feel off the face is super soft and you actually get good feedback on chips and pitches. The face has CNC-milled grooves, which helps create a lot of spin. Around the greens you can really control it — those little check-ups and one-hop stops are definitely there.'},
  {n:'Dan T.', r:5, t:'A beautiful and amazing club', d:'2023-08-25',
   q:'I purchase the 60 degree wedge in gold finish. I don’t need to talk about the finish as anyone looking at them should know, it’s awesome. The wedge itself is top notch. I have played 10 plus rounds with this club and I love it. I can confidently place the ball within 5ft of where I am aiming with this thing. If I am 75 yards out or closer to the pin this is my go to.'},
  {n:'Max', r:5, t:'Instant Favorite', d:'2026-03-09',
   q:'I’m still early in my golf game, started with a Callaway Edge set, got a LGW01 50º gap and love it. Weight of the club, face mill, grooves, how it rests, the grip — fantastic. Great strike feedback, and the face allows for a lot of control. The spin felt great, and overall this club has been a ton of fun to play.'},
  {n:'Dan B.', r:5, t:'Look Good, Play Good', d:'2024-08-19',
   q:'Not going to lie — the Instagram ads finally got the best of me! And I’m glad they did. I played a round with this club within the week and I have to say, I found myself playing it so much because I just wanted to look at it. My shots around the green were fantastic and my ball spun nicely. I got a ton of compliments on the club, as well.'},
  {n:'Bob M.', r:5, t:'Expectations Met', d:'2025-01-04',
   q:'My Lucky 50 wedge is the second in my bag. My original test was a 54 which fit nicely between my old 60 degree and stock wedge. Playing more golf in retirement I found another gap between the stock wedge and the 54. First time i had a chance to use it at the designated yardage, 5 feet from the hole and a nice birdie made with my Lucky putter.'},
  {n:'Hunter S.', r:5, t:'The Next Scottie Scheffler', d:'2024-05-20',
   q:'The wedges are cool, crisp, and clean and my game shows it. Around the clubhouse I’m getting asked if I am a member of the LIV tour with the solid gold. To their surprise I tell them “No, my guys at Lucky Golf have the hookup.”'},
  {n:'JD M.', r:5, t:'So nice, I bought it twice!', d:'2026-07-08',
   q:'I bought myself a 60 degree last year. I love it so much, and get so many comments/compliments on the look… but the performance speaks even louder! In this recent purchase I bought 2 more and gave them to my dad for Father’s Day and my brother for his birthday (same week!). They love them!'},
  {n:'Dax R.', r:5, t:'Incredible customer service', d:'2026-02-04',
   q:'The putter and wedge are amazing, but what truly impresses me is the exceptional customer service. They responded to my email on a Sunday and even followed up with a phone call, which was answered by a person on a Sunday! I was shocked, but they explained that their goal is to make every purchase perfect, one happy customer at a time.'},
  {n:'Nick F.', r:4, t:'Great club, OK customer service', d:'2026-06-20',
   q:'The club itself, outstanding. Looks sharp, plays well, nice feel. Definitely a good addition to the bag. First club got lost in transit. Took forever to get a response from anyone. So, as long as it ships ok, you’ll love the club! But good luck if there’s an issue.'}
];

(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var STAR = '<svg viewBox="0 0 24 24"><use href="#star"/></svg>';
  var stars = function(n){ var o=''; for(var i=0;i<n;i++) o+=STAR; return o; };

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
        if (live.length) live.sort(function(a, b){
          return Math.abs(a - loft) - Math.abs(b - loft); }), loft = live[0];
      }
      paintHands(); paintLofts(); sync();
    }
    if (l && !l.disabled){ loft = +l.getAttribute('data-loft'); paintLofts(); sync(); }
  });

  /* quantity + add to cart */
  var qty = $('#qty');
  document.addEventListener('click', function(e){
    var q = e.target.closest('[data-q]');
    if (q && qty){
      var v = Math.max(1, Math.min(9, (+qty.value || 1) + (+q.getAttribute('data-q'))));
      qty.value = v;
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
        + '<span class="gap">' + gap + '° up from your ' + (i === 0 ? 'pitching wedge' : (l - gap) + '°') + '</span>'
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

  /* --------------------------------------------------------- review grid */
  var rg = $('#rgrid');
  if (rg) rg.innerHTML = PD_REVIEWS.map(function(r){
    return '<article class="rcard">'
      + '<span class="stars" role="img" aria-label="' + r.r + ' out of 5">' + stars(r.r) + '</span>'
      + '<h4>' + esc(r.t) + '</h4>'
      + '<p>“' + esc(r.q) + '”</p>'
      + '<div class="who"><span class="av" aria-hidden="true">' + esc(r.n.charAt(0)) + '</span>'
      + '<span><b>' + esc(r.n) + '</b><span>Verified buyer · ' + r.d + '</span></span></div>'
      + '</article>';
  }).join('');

  /* ------------------------------------------------------ complete the set */
  var sg = $('#setgrid');
  if (sg) sg.innerHTML = [52, 56, 60].map(function(l){
    var r = PD.role[l];
    return '<div class="setcard">'
      + '<span class="rl">' + esc(r[0]) + ' wedge</span>'
      + '<span class="lo">' + l + '°</span>'
      + '<p>' + esc(r[1]) + '</p>'
      + '<div class="bot"><span class="pr">$' + PD.price + '</span>'
      + '<button class="btn btn-ink btn-sm" type="button" data-add'
      + ' data-sku="LGW01-' + l + '-RH" data-name="' + esc(PD.name) + ' ' + l + '°"'
      + ' data-price="$' + PD.price + '" data-img="' + PD.img + '"'
      + ' data-variant="Right hand · ' + l + '°"><span>Add</span></button></div>'
      + '</div>';
  }).join('');
})();
