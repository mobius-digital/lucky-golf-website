/* HOME · the finder tabs, the in-the-wild slots, the shot briefs, the zoom.
   Every product fact on the page is a build token; nothing is typed here. */
var LG_POSTS = [
  {kind: 'Creator reel', title: 'The walk in', brief: 'Gold Carver in the bag on a cart path, walking shot, vertical crop'},
  {kind: 'Customer post', title: 'First tee', brief: 'Carver Gold in hand, morning light'},
  {kind: 'Creator post', title: 'The roll', brief: 'Tracer Blade behind the ball on the green, ball rolling out'},
  {kind: 'Customer post', title: 'The bag', brief: 'Full bag setup, gold clubs fanned, overhead'},
  {kind: 'Creator reel', title: 'Off the deck', brief: 'Stryker off the deck, follow-through, mid-flight ball'},
  {kind: 'Customer post', title: 'The polo', brief: 'Classic Polo on course, three-quarter, clover visible'}
];
(function(){
  var $ = function(s){ return document.querySelector(s); };
  var $$ = function(s){ return [].slice.call(document.querySelectorAll(s)); };
  var esc = function(s){ return String(s == null ? '' : s).replace(/[&<>"]/g, function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };

  /* finder tabs */
  var tabs = $$('.fnd-tab');
  function selectTab(i){
    tabs.forEach(function(x, xi){ x.setAttribute('aria-selected', String(xi === i)); x.setAttribute('aria-pressed', String(xi === i)); });
    $$('.fnd-panel').forEach(function(p){ p.hidden = p.getAttribute('data-p') !== String(i); });
  }
  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){ selectTab(i); });
    t.addEventListener('keydown', function(e){
      var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (!d) return;
      e.preventDefault();
      var n = (i + d + tabs.length) % tabs.length;
      selectTab(n); tabs[n].focus();
    });
  });

  /* the clips */
  var clips = $('#clips');
  if (clips) clips.innerHTML = LG_POSTS.map(function(o){
    return '<div class="clip" data-md-open="md-shot" data-title="' + esc(o.title) + '" data-brief="' + esc(o.brief) + '"><small>' + esc(o.kind) + ' needed</small><b>' + esc(o.title) + '</b>' + esc(o.brief) + '</div>';
  }).join('');
  document.addEventListener('click', function(e){
    var c = e.target.closest('[data-cliparrows] button');
    if (c){ var cl = $('#clips'); if (cl) cl.scrollBy({left: (c.getAttribute('aria-label') === 'Next' ? 1 : -1) * cl.clientWidth * .5, behavior: 'smooth'}); }
  });

  /* shot briefs */
  document.addEventListener('click', function(e){
    var t = e.target.closest('[data-md-open="md-shot"]'); if (!t) return;
    if (t.closest('a')) e.preventDefault();
    $('[data-shot-title]').textContent = t.getAttribute('data-title') || 'Shot needed';
    $('[data-shot-brief]').textContent = t.getAttribute('data-brief') || '';
  });

  /* zoom */
  var zoom = $('#zoom');
  if (zoom && zoom.showModal){
    document.addEventListener('click', function(e){
      var t = e.target.closest('[data-zoom]');
      if (t){ var im = zoom.querySelector('img'); im.src = t.getAttribute('data-zoom'); im.alt = (t.querySelector('img') || {}).alt || ''; zoom.showModal(); return; }
      if (e.target.closest('[data-zoom-close]') || e.target === zoom) zoom.close();
    });
  }
})();
