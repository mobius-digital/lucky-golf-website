/* ==========================================================================
   APPAREL PDP — the size guide's unit toggle
   Both tables are in the markup and this only swaps which one is shown. The
   manufacturer publishes inches AND centimetres and they are not exact
   conversions of each other, so converting one into the other in JS would
   quietly replace supplied figures with derived ones.
   ========================================================================== */
(function(){
  var group = document.querySelector('.sg-units');
  if (!group) return;
  group.addEventListener('click', function(e){
    var btn = e.target.closest('[data-unit]');
    if (!btn) return;
    var want = btn.getAttribute('data-unit');
    [].forEach.call(group.querySelectorAll('[data-unit]'), function(b){
      b.setAttribute('aria-checked', String(b === btn));
    });
    [].forEach.call(document.querySelectorAll('[data-unit-panel]'), function(p){
      p.hidden = p.getAttribute('data-unit-panel') !== want;
    });
  });
  /* arrow keys move between radios, which is what a radiogroup owes you */
  group.addEventListener('keydown', function(e){
    var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
          : e.key === 'ArrowLeft'  || e.key === 'ArrowUp'   ? -1 : 0;
    if (!d) return;
    var all = [].slice.call(group.querySelectorAll('[data-unit]'));
    var i = all.indexOf(document.activeElement);
    if (i < 0) return;
    e.preventDefault();
    var next = all[(i + d + all.length) % all.length];
    next.focus(); next.click();
  });
})();
