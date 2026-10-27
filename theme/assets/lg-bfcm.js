/* The Black Friday page (sections/lg-bfcm.liquid): picks the phase from the clock, runs the countdown,
   and applies the mail code for people who came from the postcard QR (or any ?code=X link). */
(function () {
  var cfg = window.LG_BF, page = document.querySelector('[data-bf-page]');
  if (!cfg || !page) return;

  var q = new URLSearchParams(location.search);
  var forced = q.get('bf_phase'); // preview any phase: ?bf_phase=live
  var now = Date.now();
  var phase = 'mail';
  cfg.phases.forEach(function (p) { if (p[1] && now >= Date.parse(p[1])) phase = p[0]; });
  if (forced) phase = forced;
  page.setAttribute('data-phase', phase);
  page.querySelectorAll('[data-bf-show]').forEach(function (el) {
    el.hidden = el.getAttribute('data-bf-show').split(' ').indexOf(phase) < 0;
  });

  // countdown to the end of the deal
  var clock = page.querySelector('[data-bf-clock]'), end = Date.parse(cfg.end);
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    if (!clock || !end) return;
    var t = Math.max(0, Math.floor((end - Date.now()) / 1000));
    clock.querySelector('[data-d]').textContent = Math.floor(t / 86400);
    clock.querySelector('[data-h]').textContent = pad(Math.floor(t % 86400 / 3600));
    clock.querySelector('[data-m]').textContent = pad(Math.floor(t % 3600 / 60));
  }
  tick(); setInterval(tick, 30000);

  // the code: the list phase shows its own code when one is set
  var box = page.querySelector('[data-bf-code]');
  var code = (phase === 'list' && cfg.codes.list) ? cfg.codes.list : cfg.codes.mail;
  if (box) box.querySelector('[data-code-text]').textContent = code;

  var src = (q.get('utm_source') || '').toLowerCase();
  var sources = (cfg.autoSources || '').toLowerCase().split(/[\s,]+/).filter(Boolean);
  var want = q.get('code') || (sources.indexOf(src) > -1 ? code : '');
  var KEY = 'lg_bf_code';
  try { if (!want) want = sessionStorage.getItem(KEY) || ''; } catch (e) {}
  if (!want || (phase !== 'mail' && phase !== 'list')) return;

  // GET /discount/CODE sets the checkout discount cookie; the cart and checkout pick it up from there
  fetch('/discount/' + encodeURIComponent(want), { credentials: 'same-origin', redirect: 'follow' })
    .then(function () {
      try { sessionStorage.setItem(KEY, want); } catch (e) {}
      if (!box) return;
      box.querySelector('[data-code-text]').textContent = want;
      box.querySelector('[data-code-off]').hidden = true;
      box.querySelector('[data-code-on]').hidden = false;
      box.classList.add('is-on');
    })
    .catch(function () {});
})();
