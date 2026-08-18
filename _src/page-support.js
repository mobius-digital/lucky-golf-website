/* ==========================================================================
   SUPPORT — the only two behaviours these four pages have.

   The FAQ is <details>, so it opens with no JS at all. This file adds the one
   thing native <details> does not do: honour a link into a closed answer.
   Everything else on these pages is a link or a heading.
   ========================================================================== */

/* Deep link into a closed answer. A footer or an email that points at
   43-faq.html#lh-availability has to land on an OPEN question, not on a
   collapsed row the reader then has to find and click. Runs on load and on
   every subsequent hash change. */
function supOpenFromHash(){
  var id = (location.hash || '').slice(1);
  if(!id) return;
  var el;
  try { el = document.getElementById(decodeURIComponent(id)); }
  catch(e){ el = document.getElementById(id); }
  if(!el) return;
  var d = el.closest ? el.closest('details') : null;
  if(d) d.open = true;
  if(el.tagName === 'DETAILS') el.open = true;
  // the browser already scrolled, before the panel had a height
  el.scrollIntoView({block:'start', behavior:'auto'});
}
(function(){
  if(!document.querySelector('.sup-q')) return;
  supOpenFromHash();
  window.addEventListener('hashchange', supOpenFromHash);
})();

/* The contact form is markup for Shopify's {% form 'contact' %}, and this file
   is a single self-contained HTML page with nothing behind it. It says so
   above the fields; this stops the submit so the page cannot navigate away and
   repeats it where the reader is looking. Deliberately NOT a thank-you. */
(function(){
  var f = document.getElementById('sup-contact');
  var out = document.getElementById('sup-form-out');
  if(!f || !out) return;
  f.addEventListener('submit', function(e){
    e.preventDefault();
    out.hidden = false;
    out.textContent = 'Nothing was sent. This prototype has no server behind it. '
      + 'on the live store these fields post to Shopify. Email '
      + 'support@luckygolf.com in the meantime.';
    out.scrollIntoView({block:'nearest', behavior:'smooth'});
  });
})();
