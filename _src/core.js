/* reveal-on-scroll */
(function(){
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('.rv').forEach(function(n){n.classList.add('in')});
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting){
        var i = Array.prototype.indexOf.call(e.target.parentNode.children, e.target);
        e.target.style.transitionDelay = Math.min(i,4) * 70 + 'ms';
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  },{rootMargin:'0px 0px -12% 0px',threshold:0.08});
  document.querySelectorAll('.rv').forEach(function(n){io.observe(n)});
})();

/* mobile nav */
(function(){
  var b=document.getElementById('burger'), n=document.getElementById('mnav');
  if(!b||!n) return;
  b.addEventListener('click',function(){
    var open = b.getAttribute('aria-expanded')==='true';
    b.setAttribute('aria-expanded', String(!open));
    n.setAttribute('data-open', String(!open));
  });
  /* accordion rows: one open at a time, Takomo-style */
  var hds = n.querySelectorAll('.mn-hd');
  [].forEach.call(hds, function(h){
    h.addEventListener('click', function(){
      var was = h.getAttribute('aria-expanded')==='true';
      [].forEach.call(hds, function(x){
        x.setAttribute('aria-expanded','false');
        var bd = document.getElementById(x.getAttribute('aria-controls')); if (bd) bd.hidden = true;
      });
      if (!was){
        h.setAttribute('aria-expanded','true');
        var mine = document.getElementById(h.getAttribute('aria-controls')); if (mine) mine.hidden = false;
      }
    });
  });
})();

/* social rail */
(function(){
  document.querySelectorAll('[data-rail]').forEach(function(root){
    var rail=root.querySelector('.rail');
    var prev=root.querySelector('[data-rail-prev]');
    var next=root.querySelector('[data-rail-next]');
    if(!rail||!prev||!next) return;
    var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function step(){
      var c=rail.querySelector('.post');
      var gap=parseFloat(getComputedStyle(rail).columnGap)||22;
      return c ? c.getBoundingClientRect().width + gap : 300;
    }
    function update(){
      var max=rail.scrollWidth-rail.clientWidth;
      prev.disabled = rail.scrollLeft <= 4;
      next.disabled = rail.scrollLeft >= max-4;
    }
    function go(dir){
      rail.scrollBy({left:dir*step(), behavior: reduce ? 'auto' : 'smooth'});
    }
    prev.addEventListener('click',function(){go(-1)});
    next.addEventListener('click',function(){go(1)});
    rail.addEventListener('scroll',update,{passive:true});
    window.addEventListener('resize',update);
    update();
  });
})();

(function(){
  var lb = document.getElementById('lb'),
      media = document.getElementById('lb-media'),
      detail = document.getElementById('lb-detail'),
      prev = lb.querySelector('[data-lb-prev]'),
      next = lb.querySelector('[data-lb-next]');
  var mode = 'rv', idx = 0, lastFocus = null;
  var STAR = '<svg><use href="#star"/></svg>';
  var FIVE = STAR + STAR + STAR + STAR + STAR;

  function stars(sc){
    return '<span class="stars" style="--pct:' + (sc / 5 * 100) + '%" role="img" aria-label="' + sc + ' out of 5">'
         + '<span class="s-bg">' + FIVE + '</span><span class="s-fg">' + FIVE + '</span></span>';
  }
  function esc(s){
    var d = document.createElement('div');
    d.textContent = (s == null ? '' : s);
    return d.innerHTML;
  }
  function fmtDate(iso){
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p = String(iso).split('-');
    if (p.length < 3) return esc(iso);
    return p[2].replace(/^0/,'') + ' ' + m[parseInt(p[1],10)-1] + ' ' + p[0];
  }
  function buyBlock(o, label){
    return '<span class="lb-shown">' + label + '</span>'
      + '<div class="lb-buy">'
      +   '<img src="' + o.img + '" alt="">'
      +   '<span class="info"><span class="sku">' + esc(o.sku) + '</span>'
      +     '<span class="nm">' + esc(o.p) + '</span><span class="pr">' + esc(o.price) + '</span></span>'
      +   '<button type="button" class="btn btn-foil btn-sm" data-add data-sku="' + esc(o.sku) + '" data-name="' + esc(o.p) + '" data-price="' + esc(o.price) + '" data-img="' + o.img + '"><span>' + esc(o.cta) + '</span><span class="ar">&rarr;</span></button>'
      + '</div>';
  }
  function clearMedia(){
    var kids = media.children, i;
    for (i = kids.length - 1; i >= 0; i--){
      if (!kids[i].classList.contains('lb-nav')) media.removeChild(kids[i]);
    }
  }
  function render(){
    var list = (mode === 'rv') ? LG_REVIEWS : LG_POSTS;
    var o = list[idx];
    clearMedia();
    if (mode === 'rv'){
      var img = document.createElement('img');
      img.src = o.img; img.alt = o.p;
      media.insertBefore(img, media.firstChild);
      detail.innerHTML =
        '<div class="lb-row">' + stars(o.r)
        + '<span class="lb-vfd"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span><span>Verified buyer</span></span>'
        + '</div>'
        + '<span class="lb-who" id="lb-who">' + esc(o.n) + '</span>'
        + '<p class="lb-meta">' + (o.co ? esc(o.co) + ' &middot; ' : '') + fmtDate(o.d) + '</p>'
        + (o.ttl ? '<h3 class="disp d-s lb-title">' + esc(o.ttl) + '</h3>' : '')
        + '<p class="lb-text">' + esc(o.txt) + '</p>'
        + (o.rep ? '<div class="lb-reply"><span class="who">Reply from Lucky Golf</span><p>' + esc(o.rep) + '</p></div>' : '')
        + buyBlock(o, 'Reviewed product');
    } else {
      var ph = document.createElement('div');
      ph.className = 'ph ph--dark';
      ph.innerHTML = '<span class="lbl"><span class="mono k">Video needed</span>'
        + '<span class="mono">' + esc(o.brief) + '. Full vertical video, sound on. '
        + 'This pane takes the creator&rsquo;s reel or the customer&rsquo;s clip at full length.</span></span>';
      media.insertBefore(ph, media.firstChild);
      detail.innerHTML =
        '<div class="lb-row">'
        + '<span class="lb-vfd"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span><span>'
        + (o.who === 'creator' ? 'Lucky ambassador' : 'Customer post') + '</span></span>'
        + '</div>'
        + '<span class="lb-who" id="lb-who">' + (o.who === 'creator' ? '@[CREATOR HANDLE]' : '@[CUSTOMER HANDLE]') + '</span>'
        + '<p class="lb-meta">' + esc(o.kind) + '</p>'
        + '<p class="lb-text">[POST CAPTION]</p>'
        + buyBlock(o, 'Shown in this post');
    }
    prev.disabled = (idx <= 0);
    next.disabled = (idx >= list.length - 1);
  }
  function openLb(m, i, trigger){
    mode = m; idx = i;
    lastFocus = trigger || document.activeElement;
    render();
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-x').focus();
  }
  function closeLb(){
    lb.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function step(d){
    var list = (mode === 'rv') ? LG_REVIEWS : LG_POSTS;
    var n = idx + d;
    if (n < 0) n = 0;
    if (n > list.length - 1) n = list.length - 1;
    idx = n; render();
  }
  prev.addEventListener('click', function(){ step(-1); });
  next.addEventListener('click', function(){ step(1); });
  var closers = lb.querySelectorAll('[data-lb-close]');
  for (var c = 0; c < closers.length; c++) closers[c].addEventListener('click', closeLb);

  document.addEventListener('keydown', function(e){
    if (lb.hidden) return;
    if (e.key === 'Escape') { closeLb(); return; }
    if (e.key === 'ArrowLeft')  { step(-1); return; }
    if (e.key === 'ArrowRight') { step(1);  return; }
    if (e.key === 'Tab'){
      var f = lb.querySelectorAll('button:not([disabled]), a[href]');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  });

  function wire(sel, attr, m){
    var els = document.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++){
      (function(el){
        var n = parseInt(el.getAttribute(attr), 10);
        el.addEventListener('click', function(){ openLb(m, n, el); });
        el.addEventListener('keydown', function(e){
          if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openLb(m, n, el); }
        });
      })(els[i]);
    }
  }
  wire('[data-rv]', 'data-rv', 'rv');
  wire('[data-po]', 'data-po', 'po');
})();

(function(){
  var lb = document.getElementById('lb'),
      media = document.getElementById('lb-media'),
      detail = document.getElementById('lb-detail'),
      prev = lb.querySelector('[data-lb-prev]'),
      next = lb.querySelector('[data-lb-next]');
  var mode = 'rv', idx = 0, lastFocus = null;
  var STAR = '<svg><use href="#star"/></svg>';
  var FIVE = STAR + STAR + STAR + STAR + STAR;

  function stars(sc){
    return '<span class="stars" style="--pct:' + (sc / 5 * 100) + '%" role="img" aria-label="' + sc + ' out of 5">'
         + '<span class="s-bg">' + FIVE + '</span><span class="s-fg">' + FIVE + '</span></span>';
  }
  function esc(s){
    var d = document.createElement('div');
    d.textContent = (s == null ? '' : s);
    return d.innerHTML;
  }
  function fmtDate(iso){
    var m = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    var p = String(iso).split('-');
    if (p.length < 3) return esc(iso);
    return p[2].replace(/^0/,'') + ' ' + m[parseInt(p[1],10)-1] + ' ' + p[0];
  }
  function buyBlock(o, label){
    return '<span class="lb-shown">' + label + '</span>'
      + '<div class="lb-buy">'
      +   '<img src="' + o.img + '" alt="">'
      +   '<span class="info"><span class="sku">' + esc(o.sku) + '</span>'
      +     '<span class="nm">' + esc(o.p) + '</span><span class="pr">' + esc(o.price) + '</span></span>'
      +   '<a class="btn btn-foil btn-sm" href="' + (o.href || '#') + '"><span>' + esc(o.cta) + '</span><span class="ar">&rarr;</span></a>'
      + '</div>';
  }
  function clearMedia(){
    var kids = media.children, i;
    for (i = kids.length - 1; i >= 0; i--){
      if (!kids[i].classList.contains('lb-nav')) media.removeChild(kids[i]);
    }
  }
  function render(){
    var list = (mode === 'rv') ? LG_REVIEWS : LG_POSTS;
    var o = list[idx];
    clearMedia();
    if (mode === 'rv'){
      var img = document.createElement('img');
      img.src = o.img; img.alt = o.p;
      media.insertBefore(img, media.firstChild);
      detail.innerHTML =
        '<div class="lb-row">' + stars(o.r)
        + '<span class="lb-vfd"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span><span>Verified buyer</span></span>'
        + '</div>'
        + '<span class="lb-who" id="lb-who">' + esc(o.n) + '</span>'
        + '<p class="lb-meta">' + (o.co ? esc(o.co) + ' &middot; ' : '') + fmtDate(o.d) + '</p>'
        + (o.ttl ? '<h3 class="disp d-s lb-title">' + esc(o.ttl) + '</h3>' : '')
        + '<p class="lb-text">' + esc(o.txt) + '</p>'
        + (o.rep ? '<div class="lb-reply"><span class="who">Reply from Lucky Golf</span><p>' + esc(o.rep) + '</p></div>' : '')
        + buyBlock(o, 'Reviewed product');
    } else {
      var ph = document.createElement('div');
      ph.className = 'ph ph--dark';
      ph.innerHTML = '<span class="lbl"><span class="mono k">Video needed</span>'
        + '<span class="mono">' + esc(o.brief) + '. Full vertical video, sound on. '
        + 'This pane takes the creator&rsquo;s reel or the customer&rsquo;s clip at full length.</span></span>';
      media.insertBefore(ph, media.firstChild);
      detail.innerHTML =
        '<div class="lb-row">'
        + '<span class="lb-vfd"><span class="mk"><svg><use href="#lg-clover-plain"/></svg></span><span>'
        + (o.who === 'creator' ? 'Lucky ambassador' : 'Customer post') + '</span></span>'
        + '</div>'
        + '<span class="lb-who" id="lb-who">' + (o.who === 'creator' ? '@[CREATOR HANDLE]' : '@[CUSTOMER HANDLE]') + '</span>'
        + '<p class="lb-meta">' + esc(o.kind) + '</p>'
        + '<p class="lb-text">[POST CAPTION]</p>'
        + buyBlock(o, 'Shown in this post');
    }
    prev.disabled = (idx <= 0);
    next.disabled = (idx >= list.length - 1);
  }
  function openLb(m, i, trigger){
    mode = m; idx = i;
    lastFocus = trigger || document.activeElement;
    render();
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-x').focus();
  }
  function closeLb(){
    lb.hidden = true;
    document.body.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }
  function step(d){
    var list = (mode === 'rv') ? LG_REVIEWS : LG_POSTS;
    var n = idx + d;
    if (n < 0) n = 0;
    if (n > list.length - 1) n = list.length - 1;
    idx = n; render();
  }
  prev.addEventListener('click', function(){ step(-1); });
  next.addEventListener('click', function(){ step(1); });
  var closers = lb.querySelectorAll('[data-lb-close]');
  for (var c = 0; c < closers.length; c++) closers[c].addEventListener('click', closeLb);

  document.addEventListener('keydown', function(e){
    if (lb.hidden) return;
    if (e.key === 'Escape') { closeLb(); return; }
    if (e.key === 'ArrowLeft')  { step(-1); return; }
    if (e.key === 'ArrowRight') { step(1);  return; }
    if (e.key === 'Tab'){
      var f = lb.querySelectorAll('button:not([disabled]), a[href]');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
  });

  function wire(sel, attr, m){
    var els = document.querySelectorAll(sel);
    for (var i = 0; i < els.length; i++){
      (function(el){
        var n = parseInt(el.getAttribute(attr), 10);
        el.addEventListener('click', function(){ openLb(m, n, el); });
        el.addEventListener('keydown', function(e){
          if (e.key === 'Enter' || e.key === ' '){ e.preventDefault(); openLb(m, n, el); }
        });
      })(els[i]);
    }
  }
  wire('[data-rv]', 'data-rv', 'rv');
  wire('[data-po]', 'data-po', 'po');
})();


/* ==========================================================================
   MEGA MENU — hover on pointer, click/Enter + arrow keys for keyboard,
   Escape closes, focus leaving the item closes it.
   ========================================================================== */
(function(){
  var items = Array.prototype.slice.call(document.querySelectorAll('.nav-item'));
  if (!items.length) return;
  var hoverCapable = window.matchMedia('(hover:hover)').matches;
  var closeTimer = null;

  function setOpen(item, open){
    item.setAttribute('data-open', open ? 'true' : 'false');
    var t = item.querySelector('.nav-trigger');
    if (t) t.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function closeAll(except){
    items.forEach(function(i){ if (i !== except) setOpen(i, false); });
  }
  items.forEach(function(item){
    var trigger = item.querySelector('.nav-trigger');
    if (!trigger) return;
    if (hoverCapable){
      item.addEventListener('mouseenter', function(){
        clearTimeout(closeTimer); closeAll(item); setOpen(item, true);
      });
      item.addEventListener('mouseleave', function(){
        closeTimer = setTimeout(function(){ setOpen(item, false); }, 140);
      });
    }
    trigger.addEventListener('click', function(e){
      e.preventDefault();
      var open = item.getAttribute('data-open') === 'true';
      closeAll(item); setOpen(item, !open);
    });
    trigger.addEventListener('keydown', function(e){
      if (e.key === 'ArrowDown'){
        e.preventDefault(); closeAll(item); setOpen(item, true);
        var f = item.querySelector('.mega a,.mega button');
        if (f) f.focus();
      }
    });
    item.addEventListener('focusout', function(e){
      if (!item.contains(e.relatedTarget)) setOpen(item, false);
    });
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape'){
      var open = document.querySelector('.nav-item[data-open="true"]');
      if (open){ setOpen(open, false); var t = open.querySelector('.nav-trigger'); if (t) t.focus(); }
    }
  });
})();

/* ==========================================================================
   CART — front-end only. Line items persist in localStorage; there is no
   real checkout behind the button (see the note in the drawer footer).
   ========================================================================== */
(function(){
  var KEY = 'lg-cart-v1';
  var drawer = document.getElementById('cd');
  var listEl = document.getElementById('cd-list');
  var subEl  = document.getElementById('cd-sub');
  var countEls = document.querySelectorAll('.cart-count');
  var live = document.getElementById('cart-live');
  var lastFocus = null;
  var cart = [];

  try { cart = JSON.parse(localStorage.getItem(KEY)) || []; } catch(e){ cart = []; }
  if (!Array.isArray(cart)) cart = [];

  function save(){ try { localStorage.setItem(KEY, JSON.stringify(cart)); } catch(e){} }
  function money(n){ return '$' + n.toFixed(2).replace(/\.00$/, ''); }
  function priceOf(s){ return parseFloat(String(s).replace(/[^0-9.]/g, '')) || 0; }
  function units(){ return cart.reduce(function(a,i){ return a + i.q; }, 0); }
  function total(){ return cart.reduce(function(a,i){ return a + priceOf(i.price) * i.q; }, 0); }
  function esc(s){ var d = document.createElement('div'); d.textContent = (s==null?'':s); return d.innerHTML; }

  function paintCount(){
    var n = units();
    countEls.forEach(function(el){
      el.setAttribute('data-n', String(n));
      el.textContent = n > 99 ? '99+' : String(n);
    });
  }
  function render(){
    paintCount();
    if (!cart.length){
      listEl.innerHTML = '<div class="cd-empty">'
        + '<span class="mk"><svg><use href="#lg-clover-plain"/></svg></span>'
        + '<p class="aside">Nothing in the bag yet.</p></div>';
    } else {
      listEl.innerHTML = cart.map(function(i, idx){
        return '<div class="ci">'
          + '<img src="' + i.img + '" alt="" width="152" height="152">'
          + '<div class="info">'
          +   '<span class="sku">' + esc(i.sku) + (i.variant ? ' &middot; ' + esc(i.variant) : '') + '</span>'
          +   '<span class="nm">' + esc(i.name) + '</span>'
          +   '<span class="pr">' + esc(i.price) + '</span>'
          +   '<div class="qty" role="group" aria-label="Quantity for ' + esc(i.name) + '">'
          +     '<button type="button" data-dec="' + idx + '" aria-label="Decrease quantity">&minus;</button>'
          +     '<span>' + i.q + '</span>'
          +     '<button type="button" data-inc="' + idx + '" aria-label="Increase quantity">+</button>'
          +   '</div><br>'
          +   '<button type="button" class="ci-rm" data-rm="' + idx + '">Remove</button>'
          + '</div></div>';
      }).join('');
    }
    paintUpsell();
    subEl.textContent = money(total());
  }

  /* Cross-sell inside the drawer. Page supplies LG_CART_UPSELL; anything
     already in the bag is dropped so we never offer what they just added. */
  function paintUpsell(){
    var box = document.getElementById('cd-up'), list = document.getElementById('cd-up-list');
    if (!box || !list) return;
    var pool = (typeof LG_CART_UPSELL !== 'undefined' && LG_CART_UPSELL) ? LG_CART_UPSELL : [];
    var have = {};
    cart.forEach(function(i){ have[i.sku] = 1; });
    var offer = pool.filter(function(o){ return !have[o.sku]; }).slice(0, 3);
    box.hidden = !cart.length || !offer.length;
    if (box.hidden){ list.innerHTML = ''; return; }
    list.innerHTML = offer.map(function(o){
      return '<div class="cu">'
        + '<img src="' + o.img + '" alt="" width="104" height="104">'
        + '<div class="info"><span class="nm">' + esc(o.name) + '</span>'
        +   '<span class="why">' + esc(o.why) + '</span></div>'
        + '<span class="pr">' + esc(o.price) + '</span>'
        + '<button type="button" data-add data-sku="' + esc(o.sku) + '" data-name="' + esc(o.name)
        +   '" data-price="' + esc(o.price) + '" data-img="' + o.img
        +   '" data-variant="' + esc(o.variant || '') + '"><span>Add</span></button>'
        + '</div>';
    }).join('');
  }
  function announce(msg){ if (live) live.textContent = msg; }

  function add(item){
    var key = item.sku + '|' + (item.variant || '');
    var found = null;
    cart.forEach(function(i){ if (i.sku + '|' + (i.variant || '') === key) found = i; });
    if (found) found.q += 1;
    else cart.push({sku:item.sku,name:item.name,price:item.price,img:item.img,variant:item.variant||'',q:1});
    save(); render();
    announce(item.name + ' added to the bag. ' + units() + ' item' + (units()===1?'':'s') + ' in the bag.');
  }
  function open(trigger){
    if (drawer.getAttribute('data-open') === 'true') return;   /* PDP adds N
      times for quantity; opening once is enough and re-focusing N times is not */
    /* a hidden trigger (the PDP's add-to-cart proxy) cannot take focus back,
       so fall through to whatever the user actually clicked */
    lastFocus = (trigger && trigger.offsetParent !== null) ? trigger : document.activeElement;
    drawer.hidden = false;
    requestAnimationFrame(function(){ drawer.setAttribute('data-open','true'); });
    document.body.style.overflow = 'hidden';
    drawer.querySelector('.cd-x').focus();
  }
  function close(){
    drawer.setAttribute('data-open','false');
    document.body.style.overflow = '';
    setTimeout(function(){ drawer.hidden = true; }, 260);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  // add-to-bag buttons anywhere on the page
  document.addEventListener('click', function(e){
    var btn = e.target.closest('[data-add]');
    if (btn){
      e.preventDefault();
      add({sku:btn.getAttribute('data-sku'), name:btn.getAttribute('data-name'),
           price:btn.getAttribute('data-price'), img:btn.getAttribute('data-img'),
           variant:btn.getAttribute('data-variant') || ''});
      var label = btn.querySelector('span') || btn;
      var was = label.textContent;
      btn.setAttribute('data-added','true'); label.textContent = 'Added';
      setTimeout(function(){ btn.removeAttribute('data-added'); label.textContent = was; }, 1400);
      open(btn);          /* show the bag straight away, the way every store does */
      return;
    }
    if (e.target.closest('[data-cart-open]')){ e.preventDefault(); open(e.target.closest('[data-cart-open]')); return; }
    if (e.target.closest('[data-cart-close]')){ close(); return; }
    var dec = e.target.closest('[data-dec]'), inc = e.target.closest('[data-inc]'), rm = e.target.closest('[data-rm]');
    if (dec){ var i = +dec.getAttribute('data-dec'); cart[i].q -= 1; if (cart[i].q < 1) cart.splice(i,1); save(); render(); return; }
    if (inc){ var j = +inc.getAttribute('data-inc'); cart[j].q += 1; save(); render(); return; }
    if (rm){ var k = +rm.getAttribute('data-rm'); var nm = cart[k].name; cart.splice(k,1); save(); render(); announce(nm + ' removed.'); return; }
  });
  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && !drawer.hidden && drawer.getAttribute('data-open') === 'true') close();
  });
  render();
})();

/* MODAL — generic. [data-md-open="id"] opens .md#id, [data-md-close] and Esc
   close it. Focus moves in and returns to the trigger, and Tab is trapped
   while open, same contract as the cart drawer. */
(function(){
  var open = null, lastFocus = null;
  var FOCUSABLE = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';

  function show(id, trigger){
    var md = document.getElementById(id);
    if (!md) return;
    lastFocus = trigger || document.activeElement;
    md.hidden = false;
    requestAnimationFrame(function(){ md.setAttribute('data-open', 'true'); });
    document.body.style.overflow = 'hidden';
    open = md;
    var x = md.querySelector('.md-x');
    if (x) x.focus();
  }
  function hide(){
    if (!open) return;
    var md = open;
    md.setAttribute('data-open', 'false');
    document.body.style.overflow = '';
    setTimeout(function(){ md.hidden = true; }, 240);
    open = null;
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-md-open]');
    if (t){ e.preventDefault(); show(t.getAttribute('data-md-open'), t); return; }
    if (e.target.closest('[data-md-close]')) hide();
  });
  document.addEventListener('keydown', function(e){
    if (!open) return;
    if (e.key === 'Escape'){ hide(); return; }
    if (e.key !== 'Tab') return;
    var f = [].slice.call(open.querySelectorAll(FOCUSABLE)).filter(function(n){
      return n.offsetParent !== null; });
    if (!f.length) return;
    var first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
  });
})();

/* ==========================================================================
   QUICK ADD — the in-card option picker
   Cole, 2026-07-31: Primo's QUICK ADD opens a size picker inside the card and
   adds to the bag from there, rather than sending you to the product page.
   This is that control. Clubs take two steps (hand, then loft); a polo takes
   one; a hat takes none and keeps its plain [data-add] button.

   Runs on any page that declares LG_QUICKADD and loads variants.js — both
   collection templates do, and no other page does, so this is inert elsewhere.

   Availability comes from LG_VARIANTS, the same engine the PDP buy box uses
   and that tools/test-variants.js exercises over all 44 products. There is
   deliberately no second implementation of "is this combination sellable".

   Adding is handed to the existing [data-add] delegation above: the Quick buy
   button carries the resolved SKU, name, price and variant as data attributes
   and they are rewritten on every selection change. No new cart code.
   ========================================================================== */
(function(){
  var DATA = (typeof LG_QUICKADD !== 'undefined' && LG_QUICKADD) ? LG_QUICKADD : null;
  var V = window.LG_VARIANTS;
  if (!DATA || !V) return;

  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  var money = function(n){ return n === Math.round(n) ? '$' + n : '$' + n.toFixed(2); };

  var current = null;   /* the open .qa panel, or null */

  function paint(panel){
    var pd = panel._pd, sel = panel._sel, axes = pd.options || [], h = '', i, n, v, ok;
    for (i = 0; i < axes.length; i++){
      h += '<div class="qa-step"><span class="qa-lbl">' + (i + 1) + '. Choose '
         + esc(axes[i].name.toLowerCase()) + '</span><div class="qa-chips">';
      for (n = 0; n < axes[i].values.length; n++){
        v = axes[i].values[n];
        ok = V.offered(pd, sel, i, v.k);
        h += '<button class="qa-chip" type="button" data-ax="' + i + '" data-v="' + esc(v.k) + '"'
           + (ok ? '' : ' disabled') + ' aria-pressed="' + (sel[i] === v.k) + '">'
           + esc(v.label) + '</button>';
      }
      h += '</div></div>';
    }
    /* price is PER VARIANT — the grips run $9.95 to $14.95 across the three
       grip sizes — so it is read off the resolved variant, never off the card */
    var vr = V.variantFor(pd, sel) || {};
    h += '<button class="qa-buy" type="button" data-add'
       + ' data-sku="' + esc(vr.sku || '') + '"'
       + ' data-name="' + esc(pd.name) + '"'
       + ' data-price="' + esc(money(vr.price)) + '"'
       + ' data-img="' + esc(pd.img || '') + '"'
       + ' data-variant="' + esc(V.labels(pd, sel).join(' \u00b7 ')) + '">'
       + '<span>Quick buy</span><span class="amt">' + esc(money(vr.price)) + '</span></button>'
       + '<button class="qa-x" type="button" aria-label="Close">\u2715</button>';
    panel.innerHTML = h;
  }

  function close(){
    if (!current) return;
    var t = current._trigger;
    current.hidden = true;
    current = null;
    if (t && t.focus) t.focus();
  }

  function openFor(trigger){
    var pid = trigger.getAttribute('data-qa'), pd = DATA[pid];
    if (!pd) return;
    var card = trigger.closest('.ptile');
    if (!card) return;
    close();
    var panel = card.querySelector('.qa');
    if (!panel){
      panel = document.createElement('div');
      panel.className = 'qa';
      /* mounted on the CARD, not the photo well: a two-axis wedge picker is
         320px of content and the well is 168px square on a phone */
      card.appendChild(panel);
    }
    panel._pd = pd;
    panel._trigger = trigger;
    /* start from the product's own default and reconcile, so a card never
       opens on a combination that cannot be bought */
    panel._sel = V.reconcile(pd, V.selectionFor(pd), 0);
    paint(panel);
    panel.hidden = false;
    current = panel;
    var first = panel.querySelector('.qa-chip:not([disabled])');
    if (first) first.focus();
  }

  document.addEventListener('click', function(e){
    var trig = e.target.closest('[data-qa]');
    if (trig){ e.preventDefault(); openFor(trig); return; }

    var chip = e.target.closest('.qa-chip');
    if (chip && current && !chip.disabled){
      var ax = +chip.getAttribute('data-ax');
      current._sel[ax] = chip.getAttribute('data-v');
      /* reconcile FROM this axis: changing hand can strand a loft, and the
         engine slides you to the nearest live one rather than leaving a dead
         selection sitting in the picker */
      current._sel = V.reconcile(current._pd, current._sel, ax);
      paint(current);
      var again = current.querySelector('[data-ax="' + ax + '"][aria-pressed="true"]');
      if (again) again.focus();
      return;
    }
    if (e.target.closest('.qa-x')){ close(); return; }
    /* Quick buy is handled by the [data-add] delegation; let it run, then get
       the panel out of the way so the card is a card again */
    if (e.target.closest('.qa-buy')){ setTimeout(close, 900); return; }
    if (current && !e.target.closest('.qa')) close();
  });

  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape' && current) close();
  });
})();
