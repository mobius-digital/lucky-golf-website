/* Lucky Golf v4. Small, dependency-free, one file for every page. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- toast: links to pages that are not in this review ---------- */
  var toast = document.createElement("div");
  toast.className = "toast"; toast.setAttribute("role", "status");
  document.body.appendChild(toast);
  var tt;
  function say(msg) {
    toast.textContent = msg; toast.classList.add("on");
    clearTimeout(tt); tt = setTimeout(function () { toast.classList.remove("on"); }, 2600);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-soon]");
    if (!a) return;
    e.preventDefault();
    say(a.getAttribute("data-soon") || "Not part of this review. This page gets the same system once these three are approved.");
  });

  /* ---------- mobile menu ---------- */
  var drawer = $("#drawer");
  $$("[data-menu]").forEach(function (b) {
    b.addEventListener("click", function () {
      var open = drawer.hidden;
      drawer.hidden = !open;
      b.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    });
  });
  if (drawer) drawer.addEventListener("click", function (e) {
    if (e.target === drawer || e.target.closest("[data-close]")) {
      drawer.hidden = true; document.body.style.overflow = "";
    }
  });

  /* ---------- accordion-style tabs (spec tables) ---------- */
  $$("[data-tabs]").forEach(function (root) {
    var btns = $$("[role=tab]", root);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) {
          var on = x === b;
          x.setAttribute("aria-selected", String(on));
          var p = document.getElementById(x.getAttribute("aria-controls"));
          if (p) p.hidden = !on;
        });
      });
    });
  });

  /* ---------- swipe gallery dots ---------- */
  function wireDots(gal, dots) {
    if (!gal || !dots) return;
    dots.innerHTML = "";
    var figs = $$("figure", gal).filter(function (f) { return !f.hidden; });
    figs.forEach(function () { dots.appendChild(document.createElement("i")); });
    function upd() {
      var i = Math.round(gal.scrollLeft / Math.max(1, gal.clientWidth));
      $$("i", dots).forEach(function (d, j) { d.classList.toggle("on", j === i); });
    }
    gal.onscroll = upd; upd();
  }

  /* ---------- product page ---------- */
  var pdataEl = $("#pdata");
  if (pdataEl) {
    var P = JSON.parse(pdataEl.textContent);
    var state = { finish: P.defaultFinish, hand: "RH", lg: null, set: 1, extra: [] };
    var qf = (location.search.match(/[?&]finish=(\w+)/) || [])[1];
    if (qf && P.finishes[qf]) state.finish = qf;
    var money = function (n) { return "$" + (Math.round(n * 100) / 100).toString(); };
    var gal = $("#gal"), dots = $("#dots");

    function fin() { return P.finishes[state.finish]; }
    function avail(hand, lg) { var v = fin().variants[hand + "|" + lg]; return !!(v && v.avail); }

    function render() {
      var f = fin();
      document.documentElement.setAttribute("data-finish", state.finish);
      // finish chips
      $$("[data-finish-chip]").forEach(function (c) { c.setAttribute("aria-pressed", String(c.dataset.finishChip === state.finish)); });
      $("#finVal").textContent = f.label;
      // text swaps
      $$("[data-f]").forEach(function (el) { el.hidden = el.dataset.f !== state.finish; });
      // hands available for this finish
      if (f.hands.indexOf(state.hand) < 0) state.hand = f.hands[0];
      $$("[data-hand]").forEach(function (c) {
        var ok = f.hands.indexOf(c.dataset.hand) >= 0;
        c.hidden = !ok;
        c.setAttribute("aria-pressed", String(c.dataset.hand === state.hand));
      });
      $("#handVal").textContent = state.hand === "RH" ? "Right hand" : "Left hand";
      $("#handNote").hidden = f.hands.length > 1;
      // loft & grind chips
      if (!state.lg || f.lofts.map(function (l) { return l.k; }).indexOf(state.lg) < 0 || !avail(state.hand, state.lg)) {
        var d = f.defaultLg;
        state.lg = avail(state.hand, d) ? d : (f.lofts.filter(function (l) { return avail(state.hand, l.k); })[0] || {}).k;
      }
      var grid = $("#lofts"); grid.innerHTML = "";
      f.lofts.forEach(function (l) {
        var b = document.createElement("button");
        b.type = "button"; b.className = "chip"; b.dataset.lg = l.k;
        var ok = avail(state.hand, l.k);
        b.disabled = !ok;
        b.innerHTML = ok ? l.label : "<s>" + l.label + "</s>";
        b.setAttribute("aria-pressed", String(l.k === state.lg));
        b.setAttribute("aria-label", l.label + (ok ? "" : ", sold out in this hand"));
        b.addEventListener("click", function () { state.lg = l.k; render(); });
        grid.appendChild(b);
      });
      var cur = f.lofts.filter(function (l) { return l.k === state.lg; })[0];
      $("#lgVal").textContent = cur ? cur.label : "";
      var outCount = f.lofts.filter(function (l) { return !avail(state.hand, l.k); }).length;
      $("#lgNote").hidden = outCount === 0;
      // set builder
      $$("[data-set]").forEach(function (c) { c.setAttribute("aria-pressed", String(+c.dataset.set === state.set)); });
      var extra = $("#extra"); extra.innerHTML = "";
      for (var i = 1; i < state.set; i++) {
        var lab = document.createElement("label");
        lab.innerHTML = "<span>Wedge " + (i + 1) + "</span>";
        var sel = document.createElement("select");
        sel.setAttribute("aria-label", "Loft and grind for wedge " + (i + 1));
        f.lofts.forEach(function (l) {
          if (!avail(state.hand, l.k)) return;
          var o = document.createElement("option"); o.value = l.k; o.textContent = l.label; sel.appendChild(o);
        });
        (function (idx, s) {
          var pick = state.extra[idx] || f.setDefaults[idx] || s.options[0].value;
          if (!avail(state.hand, pick)) pick = s.options[0].value;
          s.value = pick; state.extra[idx] = pick;
          s.addEventListener("change", function () { state.extra[idx] = s.value; });
        })(i - 1, sel);
        lab.appendChild(sel); extra.appendChild(lab);
      }
      extra.hidden = state.set === 1;
      // price
      var total = f.price * state.set;
      $("#price").firstChild.nodeValue = money(f.price) + " ";
      $("#addLabel").textContent = "Add to bag · " + money(total);
      $("#sbPrice").textContent = money(total);
      $("#sbName").textContent = f.name;
      // gallery
      $$("figure", gal).forEach(function (fig) { fig.hidden = fig.dataset.f !== state.finish; });
      gal.scrollLeft = 0;
      wireDots(gal, dots);
    }

    $$("[data-finish-chip]").forEach(function (c) { c.addEventListener("click", function () { state.finish = c.dataset.finishChip; state.extra = []; render(); }); });
    $$("[data-hand]").forEach(function (c) { c.addEventListener("click", function () { state.hand = c.dataset.hand; render(); }); });
    $$("[data-set]").forEach(function (c) { c.addEventListener("click", function () { state.set = +c.dataset.set; render(); }); });
    $$("[data-add]").forEach(function (b) {
      b.addEventListener("click", function () {
        var n = +$("#bagCount").textContent + state.set;
        $("#bagCount").textContent = n; $("#bagCount").hidden = false;
        say("Added to bag. This is a review build, so nothing is really in a cart.");
      });
    });
    render();

    // sticky buy bar on phones once the real button scrolls away
    var sb = $("#stickybuy"), real = $("#addBtn");
    if (sb && real && "IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        var e = es[0];
        sb.classList.toggle("on", !e.isIntersecting && e.boundingClientRect.top < 0);
      }).observe(real);
    }
  }

  /* ---------- collection filter + sort ---------- */
  var pgrid = $("#pgrid");
  if (pgrid) {
    var cards = $$(".card", pgrid);
    var facet = "all", sort = "featured";
    function apply() {
      var shown = cards.filter(function (c) { return facet === "all" || c.dataset.fam === facet; });
      cards.forEach(function (c) { c.hidden = shown.indexOf(c) < 0; });
      var ordered = shown.slice().sort(function (a, b) {
        if (sort === "az") return a.dataset.name.localeCompare(b.dataset.name);
        return +a.dataset.i - +b.dataset.i;
      });
      ordered.forEach(function (c) { pgrid.appendChild(c); });
      $("#shown").textContent = shown.length;
      $$("[data-facet]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.facet === facet)); });
    }
    $$("[data-facet]").forEach(function (b) { b.addEventListener("click", function () { facet = b.dataset.facet; apply(); }); });
    var so = $("#sort"); if (so) so.addEventListener("change", function () { sort = so.value; apply(); });
    apply();
  }
})();
