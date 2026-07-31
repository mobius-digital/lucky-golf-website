/* ==========================================================================
   CLUB PDP — what only a wedge, putter, hybrid or driver needs
   The spec table's tabs, the wedge loft ladder and the highlight reel. Every
   other behaviour on this page comes from _src/pdp.js.
   ========================================================================== */
/* What each loft is FOR. Editorial — Shopify has no field for it, and the
   answer is the same for every wedge we sell. */
var PD_ROLE = {
  50: ['Gap', 'Full swings from the yardage your pitching wedge can’t quite reach.'],
  52: ['Gap', 'The most-bought loft in the lineup, and usually the first wedge people add.'],
  54: ['Sand / gap', 'Full shots, longer bunker shots, anything that needs a little height.'],
  56: ['Sand', 'Greenside and bunkers. The club most golfers reach for by default.'],
  58: ['Lob', 'Higher, softer, lands quieter. For pins you can’t run the ball at.'],
  60: ['Lob', 'Flop shots, short-sided, tight pins. The most specialist club in the bag.']
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

(function(){
  var $ = function(s, r){ return (r || document).querySelector(s); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
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
      var r = PD_ROLE[l];
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

})();
