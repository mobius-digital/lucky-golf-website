/* the palette switch and the accordion specimen */
(function(){
  var seg = document.querySelector('[data-pal]');
  if (seg) seg.addEventListener('click', function(e){
    var b = e.target.closest('[data-p]'); if (!b) return;
    var p = b.getAttribute('data-p');
    if (p === 'd') document.documentElement.removeAttribute('data-palette');
    else document.documentElement.setAttribute('data-palette', p);
    [].forEach.call(seg.querySelectorAll('[data-p]'), function(x){ x.setAttribute('aria-pressed', String(x === b)); });
  });
  document.addEventListener('click', function(e){
    var h = e.target.closest('.acc-h'); if (!h) return;
    var body = h.nextElementSibling, open = h.getAttribute('aria-expanded') === 'true';
    h.setAttribute('aria-expanded', String(!open)); body.hidden = open;
    var s = h.querySelector('span'); if (s) s.textContent = open ? '+' : '−';
  });
})();
