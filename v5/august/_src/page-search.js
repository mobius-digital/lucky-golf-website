/* The whole catalogue, from tools/build.py. Same tile shape the PLP paints. */
var LG_SEARCH = {{SEARCH_JSON}};

/* Quick add needs the real option axes and variant map, exactly as on a
   collection page — a result that cannot be added is a result that sends you
   somewhere else to do it. */
var LG_QUICKADD = {{QUICKADD_JSON}};

(function(){
  var $ = function(s){ return document.querySelector(s); };
  var form = $('#se-form'), input = $('#se-q'), grid = $('#se-grid');
  var count = $('#se-count'), empty = $('#se-empty'), start = $('#se-start');
  if (!form || !grid) return;

  function esc(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

  /* What a query is allowed to match. Deliberately includes variant labels, so
     "56" finds the wedge and "left hand" finds everything built in both hands
     — those are the two things a golfer actually types. */
  function haystack(p){
    if (p._h) return p._h;
    var bits = [p.title, p.name, p.family, p.type, p.collName].concat(p.terms || []);
    p._h = bits.join(' ').toLowerCase();
    return p._h;
  }

  /* Every word has to appear somewhere. AND rather than OR: "left hand wedge"
     should narrow, not return the whole store ranked. */
  function match(p, words){
    var h = haystack(p);
    for (var i = 0; i < words.length; i++) if (h.indexOf(words[i]) === -1) return false;
    return true;
  }

  function tile(p){
    var out = !p.inStock;
    return '<article class="ptile rv"' + (out ? ' data-out' : '') + '>'
      + '<div class="pt-ph">'
      + (p.img
          ? '<img src="' + esc(p.img) + '" alt="' + esc(p.title) + '" loading="lazy"'
            + ' width="800" height="800" decoding="async">'
          : '<div class="ph"><span class="lbl"><span class="mono k">Photo needed</span>'
            + '<span class="mono">' + esc(p.title) + '</span></span></div>')
      + (out ? '<span class="pt-tag">Sold out</span>' : '')
      + '<div class="pt-add">'
      + (out
          ? ''
          : '<button class="qadd" type="button"'
            + (p.addSku
                ? ' data-add data-sku="' + esc(p.addSku) + '"'
                  + ' data-name="' + esc(p.name) + '"'
                  + ' data-price="' + esc(p.priceLabel) + '"'
                  + ' data-img="' + esc(p.img || '') + '" data-variant=""'
                : ' data-qa="' + esc(p.id) + '" aria-haspopup="true"')
            + '><svg viewBox="0 0 24 24" aria-hidden="true">'
            + '<path d="M4 7h16l-1.3 13H5.3z"/><path d="M8.5 7V5.4A3.5 3.5 0 0112 2a3.5 3.5 0 013.5 3.4V7"/>'
            + '</svg><span>Quick add</span></button>')
      + '</div>'
      + '</div>'
      + '<a class="stretch" href="' + esc(p.href) + '"><span class="pt-nm">'
        + esc(p.name) + '</span></a>'
      + '<span class="pt-meta"><span class="pt-pr">' + esc(p.priceLabel) + '</span></span>'
      + '</article>';
  }

  function run(q){
    q = (q || '').trim();
    var words = q.toLowerCase().split(/\s+/).filter(Boolean);

    if (!words.length){
      grid.innerHTML = ''; grid.hidden = true;
      if (empty) empty.hidden = true;
      if (start) start.hidden = false;
      if (count) count.textContent = '';
      return;
    }
    if (start) start.hidden = true;

    var list = LG_SEARCH.filter(function(p){ return match(p, words); });
    grid.innerHTML = list.map(tile).join('');
    grid.hidden = !list.length;
    if (empty){
      empty.hidden = !!list.length;
      var h = document.getElementById('se-empty-h');
      if (h && !list.length) h.textContent = 'Nothing matches “' + q + '”';
    }
    if (count){
      count.textContent = list.length
        ? list.length + (list.length === 1 ? ' result for “' : ' results for “') + q + '”'
        : '';
    }
    /* core.js reveals .rv on scroll and has already made its pass by the time
       these exist, so tiles painted now would stay invisible. */
    grid.querySelectorAll('.rv').forEach(function(n){ n.classList.add('in'); });
  }

  /* The query lives in the URL, so a result page can be linked, shared and
     reloaded — which is the whole difference between a search PAGE and a
     search box. Shopify's own template reads ?q= too. */
  function sync(q, push){
    var u = location.pathname + (q ? '?q=' + encodeURIComponent(q) : '');
    if (push) history.replaceState(null, '', u);
  }

  form.addEventListener('submit', function(e){
    e.preventDefault();
    run(input.value); sync(input.value, true);
  });
  /* live, but only once there is something to go on */
  input.addEventListener('input', function(){
    var v = input.value.trim();
    if (!v.length || v.length >= 2){ run(input.value); sync(input.value, true); }
  });
  document.addEventListener('click', function(e){
    var t = e.target.closest('.se-term');
    if (!t) return;
    input.value = t.getAttribute('data-term');
    run(input.value); sync(input.value, true);
    input.focus();
  });

  var q = (location.search.match(/[?&]q=([^&]*)/) || [])[1];
  if (q){ input.value = decodeURIComponent(q.replace(/\+/g, ' ')); }
  run(input.value);
})();
