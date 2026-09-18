"""Turn the v4 options page into the Yardage LIBRARY: defaults marked, alternates kept.
Changes asked for by Cole (2026-09-18):
  - Loft chart zoomed to the real window (48-62 deg fills the dial), wedge beside it
  - Star labels on the proximity target: thinner, softer, 5-star in gold
  - Glow is Twilight-only (on Daylight it just reads as blur)
  - Green map B rebuilt as a true stepped elevation map (hypsometric bands, no blur)
  - Every option badged DEFAULT / COMPACT / LIBRARY with a 'use it for' line
"""
import io
p = 'build-extras.cjs'
s = io.open(p, encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)

# ---------- C: zoomed loft chart. 48-62 deg spread over a 90 deg sweep ----------
old_c_start = s.index('/* C · protractor')
old_c_end = s.index('const monD')
s = s[:old_c_start] + r'''/* C · loft chart, zoomed: only 48-62 degrees, spread across the whole dial,
   so two degrees of loft is a gap you can actually see. */
const V0 = 48, V1 = 62, PX = 28, PY = 214, PR = 176, rad = d => d * Math.PI / 180;
const th = v => (v - V0) / (V1 - V0) * 90;
const pt = (v, r) => [PX + Math.sin(rad(th(v))) * r, PY - Math.cos(rad(th(v))) * r];
let prot = `<path class="pr-arc" d="M${pt(V0, PR).map(n => n.toFixed(1)).join(' ')}A${PR} ${PR} 0 0 1 ${pt(V1, PR).map(n => n.toFixed(1)).join(' ')}"/>`;
prot += `<path class="pr-band" d="M${PX} ${PY}L${pt(50, PR).map(n => n.toFixed(1)).join(' ')}A${PR} ${PR} 0 0 1 ${pt(60, PR).map(n => n.toFixed(1)).join(' ')}Z"/>`;
for (let v = V0; v <= V1; v += .5) { const major = v % 2 === 0, [a, b] = pt(v, PR), [c, e] = pt(v, PR - (major ? 14 : v % 1 ? 5 : 8));
  prot += `<line class="pr-tk${major ? ' mj' : ''}" x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${e.toFixed(1)}"/>`; }
LOFTS.forEach(l => { const [a, b] = pt(l, PR - 18), [c, d] = pt(l, PR + 26);
  prot += `<line class="pr-spoke" x1="${PX}" y1="${PY}" x2="${a.toFixed(1)}" y2="${b.toFixed(1)}"/><text class="pr-lb" x="${c.toFixed(1)}" y="${(d + 4).toFixed(1)}" text-anchor="middle">${l}°</text>`; });
prot += `<circle class="pr-hub" cx="${PX}" cy="${PY}" r="4.5"/><text class="pr-cap" x="${PX + 8}" y="${PY + 22}">LOFT · DEGREES</text>`;
const monC = `<div class="panel">${hd('Carver 01 Gold · loft chart', live)}<div class="mC">
  <svg class="prot" viewBox="0 0 250 250" aria-label="Six lofts, 50 to 60 degrees">${prot}</svg>
  <div class="mC-r">${ph('mC-ph')}<div class="mini"><div><span class="lb">Lofts</span><b class="n s">6</b></div><div><span class="lb">Price</span><b class="n s">$99</b></div><div><span class="lb">Test drive</span><b class="n s">60 days</b></div></div></div></div></div>`;

''' + s[old_c_end:]

# ---------- green map B: stepped elevation bands, the way real elevation maps do it ----------
rep("let heat = ''; for (let j = 0; j < 20; j++) for (let i = 0; i < 38; i++) { const n = nrm(hgt(i * 16 + 8, j * 16 + 8)); if (n > .34) heat += `<rect x=\"${i * 16}\" y=\"${j * 16}\" width=\"16\" height=\"16\" fill-opacity=\"${((n - .34) * .95).toFixed(2)}\"/>`; }",
    "let heat = ''; for (let j = 0; j < 80; j++) for (let i = 0; i < 150; i++) { const n = nrm(hgt(i * 4 + 2, j * 4 + 2)); const band = Math.floor(n * 8) / 8; if (band > .25) heat += `<rect x=\"${i * 4}\" y=\"${j * 4}\" width=\"4.3\" height=\"4.3\" fill-opacity=\"${((band - .25) * .62).toFixed(3)}\"/>`; }")
rep("`<g class=\"heat\" filter=\"url(#blur)\">${heat}</g><path class=\"ln-hair\" d=\"${cMajor}\"/>`",
    "`<g class=\"heat\">${heat}</g><path class=\"ln-hair\" d=\"${cMajor}\"/><path class=\"ln-hair\" d=\"${cMinor}\"/>`")
rep("['B', 'Heat map', 'A soft elevation glow under hairlines, like a green-reading app.'",
    "['B', 'Elevation bands', 'Stepped bands like a real elevation map. High ground is brighter.'")

# ---------- option header: DEFAULT / COMPACT / LIBRARY badge + where to use it ----------
rep("const opt = (k, name, note, body) => `<div class=\"opt\"><div class=\"opt-hd\"><b>${k}</b><span class=\"nm\">${name}</span><span class=\"nt\">${note}</span></div>${body}</div>`;",
    "const opt = (k, name, note, body, tag = 'LIBRARY', use = '') => `<div class=\"opt\" data-tag=\"${tag}\"><div class=\"opt-hd\"><b>${k}</b><span class=\"nm\">${name}</span><span class=\"tag\">${tag}</span><span class=\"nt\">${note}</span></div>${use ? `<p class=\"use\"><span>Use it for</span> ${use}</p>` : ''}${body}</div>`;")
rep("${opt('A', 'Data tiles', 'Four tiles with the real values as chips.', monA)}",
    "${opt('A', 'Data tiles', 'Four tiles with the real values as chips.', monA, 'DEFAULT', 'Product pages. The full readout.')}")
rep("${opt('B', 'HUD strip', 'One slim readout bar. Takes the least room.', monB)}",
    "${opt('B', 'HUD strip', 'One slim readout bar. Takes the least room.', monB, 'COMPACT', 'Anywhere space is tight: collection cards, sticky bars, emails.')}")
rep("${opt('C', 'Loft chart', 'The six lofts drawn at their true angles.', monC)}",
    "${opt('C', 'Loft chart', 'Zoomed to 48-62 degrees, so every loft gets real room.', monC, 'LIBRARY', 'Ads and technical pages: a wedge launch, a loft guide, a fitting page.')}")
rep("${opt('D', 'Spec card', 'Yardage-book rows with dotted leaders. The most classic.', monD)}",
    "${opt('D', 'Spec card', 'Yardage-book rows with dotted leaders. The most classic.', monD, 'LIBRARY', 'Comparison pages, printed inserts, spec sheets.')}")
rep("${opt('A', 'Proximity', 'A top-down target. Closer to the cup is better.', revA)}",
    "${opt('A', 'Proximity', 'A top-down target. Closer to the cup is better.', revA, 'DEFAULT', 'Every reviews block.')}")
rep("${opt('B', 'Share bar', 'One bar split by the real share of each rating.', revB)}",
    "${opt('B', 'Share bar', 'One bar split by the real share of each rating.', revB, 'LIBRARY', 'Tight spots: a product card, a cart drawer, an email.')}")
rep("${opt('C', 'Gauge', 'A dial filled to 4.82.', revC)}",
    "${opt('C', 'Gauge', 'A dial filled to 4.82.', revC, 'LIBRARY', 'The app, and big-number moments in ads.')}")
rep("${opt('D', 'Grid', '100 squares. Each is one percent of reviews.', revD)}",
    "${opt('D', 'Grid', '100 squares. Each is one percent of reviews.', revD, 'LIBRARY', 'Social posts and ads: reads in one glance.')}")
rep("${MAPS.map(([k, name, note, body]) => opt(k, name, note, `",
    "${MAPS.map(([k, name, note, body]) => opt(k, name, note, `")
rep("<div class=\"map-copy\"><h3 class=\"lg-d3\">Great clubs got too expensive.</h3><p class=\"sub\">A flat text section with the map behind it.</p></div></div>`)).join('\\n    ')}",
    "<div class=\"map-copy\"><h3 class=\"lg-d3\">Great clubs got too expensive.</h3><p class=\"sub\">A flat text section with the map behind it.</p></div></div>`, k === 'A' ? 'DEFAULT' : 'LIBRARY', { A: 'Behind any flat section on the site. Subtle on purpose.', B: 'The app, and course or green content.', C: 'The app. The most digital.', D: 'Launch moments and hero graphics.', E: 'Loading and transition screens, the app.' }[k])).join('\\n    ')}")

# ---------- stars: thinner and softer, 5-star in gold; glow is Twilight only ----------
rep(".rl{font:700 10px Archivo,sans-serif;fill:var(--ink);paint-order:stroke;stroke:var(--panel);stroke-width:5px;stroke-linejoin:round}",
    ".rl{font:500 9.5px Archivo,sans-serif;letter-spacing:.04em;fill:var(--mut);paint-order:stroke;stroke:var(--panel);stroke-width:2.5px;stroke-linejoin:round}.rl.r5{fill:var(--gt);font-weight:600}")
rep("<text class=\"rl\" x=\"${CX}\" y=\"${(CY - r * SY + 3.5).toFixed(1)}\" text-anchor=\"middle\">${5 - i}★</text>",
    "<text class=\"rl${i ? '' : ' r5'}\" x=\"${CX}\" y=\"${(CY - r * SY + 3.5).toFixed(1)}\" text-anchor=\"middle\">${5 - i}★</text>")
rep("--halo:drop-shadow(0 0 3px rgba(194,154,43,.55));", "--halo:none;")

# ---------- CSS for the badges, the use line, the zoomed chart ----------
rep(".opt-hd .nt{font-size:.88rem;color:var(--mut)}",
    """.opt-hd .nt{font-size:.88rem;color:var(--mut);flex-basis:100%}
.opt-hd .tag{font:700 .6rem Archivo,sans-serif;letter-spacing:.14em;padding:4px 8px;border-radius:6px;border:1px solid var(--line);color:var(--mut)}
.opt[data-tag="DEFAULT"] .tag,.opt[data-tag="COMPACT"] .tag{background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B);color:#17140F;border-color:transparent}
.use{margin:-4px 0 10px;font-size:.84rem;color:var(--mut)}.use span{font:600 .6rem Archivo,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--gt);margin-right:6px}
.opt[data-tag="LIBRARY"] .panel{opacity:.94}""")
rep(".pr-arc{fill:none;stroke:var(--line);stroke-width:1}.pr-tk{stroke:var(--mut);stroke-opacity:.6}.pr-spoke{stroke:var(--gold);stroke-width:1.5;filter:var(--halo)}",
    ".pr-arc{fill:none;stroke:var(--line);stroke-width:1}.pr-band{fill:var(--gold);fill-opacity:.08}.pr-tk{stroke:var(--mut);stroke-opacity:.45}.pr-tk.mj{stroke-opacity:.9;stroke-width:1.4}.pr-spoke{stroke:var(--gold);stroke-width:1.6;filter:var(--halo)}.pr-cap{font:600 8px Archivo,sans-serif;letter-spacing:.14em;fill:var(--mut)}")
rep(".pr-shaft{stroke:var(--ink);stroke-width:1.5;stroke-dasharray:3 4}.pr-hub{fill:var(--gold)}.pr-lb{font:600 10px Archivo,sans-serif;fill:var(--mut)}",
    ".pr-hub{fill:var(--gold)}.pr-lb{font:700 11px Archivo,sans-serif;fill:var(--ink)}")
rep(".mC-r{display:grid;gap:16px}", ".mC-r{display:grid;gap:16px}.mC-ph{height:170px;border-radius:12px;overflow:hidden}")

# ---------- title ----------
rep("<p class=\"lg-eyebrow\">Yardage instruments · v4</p><h1 class=\"lg-d2\">Pick one of each.</h1>",
    "<p class=\"lg-eyebrow\">Lucky design library · Yardage</p><h1 class=\"lg-d2\">The instruments.</h1><p class=\"sub\" style=\"max-width:60ch;margin-top:8px\">Gold tags are the defaults. Everything else is kept here on purpose, for the places it fits better. Change one here and it changes everywhere it's used.</p>")
rep("<title>Lucky Golf · Yardage instruments v4</title>", "<title>Lucky Golf · Yardage library</title>")
rep("fs.writeFileSync(ROOT + '/shopify/gwp-yardage-extras.html', html);",
    "fs.writeFileSync(ROOT + '/design/yardage-library.html', html);\nfs.writeFileSync(ROOT + '/shopify/gwp-yardage-extras.html', html);")
io.open(p, 'w', encoding='utf-8').write(s)
print('library patched')
