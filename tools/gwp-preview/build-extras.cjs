/* Yardage instruments v4: options for EVERY category, pick one of each.
     01 Monitor panel  A-D
     02 Review chart   A-D
     03 Green map      A-E
   One gold (#C29A2B) for every graphic on both grounds; only gold TYPE changes per ground.
   Image padding is FIXED px, never %: % padding resolves against the box WIDTH, which
   shrank the wedge to ~2px tall in the stacked layout.
   Real numbers only: Carver facts from the product guide; stars 585/37/12/5/11 (650, 4.82). */
const fs = require('fs'), path = require('path');
const ROOT = 'C:/Users/wetzl/Lucky Golf/Website';
const lucky = fs.readFileSync(ROOT + '/shopify/assets/lucky.css', 'utf8');
const LIVE = JSON.parse(fs.readFileSync(path.join(__dirname, 'data', 'live-products.json'), 'utf8')).products;
const gold = LIVE.find(p => p.handle === 'lucky-golf-lgw02-gold').images[4].src.split('?')[0] + '?width=700';
const LOFTS = [50, 52, 54, 56, 58, 60];
const HIST = [[5, 585], [4, 37], [3, 12], [2, 5], [1, 11]], TOTAL = 650, AVG = 4.82;
const pct = n => n / TOTAL * 100, fmt = n => pct(n) < 10 ? pct(n).toFixed(1) : pct(n).toFixed(0);
const ph = (cls = '') => `<div class="ph ${cls}"><img src="${gold}" alt="Carver 01 Gold" width="700" height="700"></div>`;
const hd = (l, r) => `<div class="p-hd"><span class="lg-label">${l}</span><span class="lg-label">${r}</span></div>`;
const live = '<span class="live"><i></i>In stock</span>';

/* ============================== 01 · MONITOR PANEL ============================== */
const chips = a => `<div class="vals">${a.map(v => `<i>${v}</i>`).join('')}</div>`;
const monA = `<div class="panel">${hd('Carver 01 Gold', live)}<div class="mA">${ph()}<div class="tiles">
  <div class="t"><span class="lb">Lofts</span><b class="n">6</b>${chips(LOFTS.map(l => l + '°'))}</div>
  <div class="t"><span class="lb">Grinds</span><b class="n">2</b>${chips(['K', 'S'])}</div>
  <div class="t"><span class="lb">Price</span><b class="n">$99</b><span class="sub">Pick any loft. Same number.</span></div>
  <div class="t"><span class="lb">Test drive</span><b class="n">60</b><span class="sub">days to prove us wrong.</span></div></div></div></div>`;

const monB = `<div class="panel mB">${ph('sm')}
  <div class="hud"><div><span class="lb">Lofts</span><b class="n">50–60°</b><span class="sub">6 of them</span></div>
  <div><span class="lb">Grinds</span><b class="n">K · S</b><span class="sub">2 soles</span></div>
  <div><span class="lb">Price</span><b class="n">$99</b><span class="sub">any loft</span></div>
  <div><span class="lb">Test drive</span><b class="n">60</b><span class="sub">days</span></div></div></div>`;

/* C · loft chart, zoomed: only 48-62 degrees, spread across the whole dial,
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

const monD = `<div class="panel mD">${ph()}<div class="spec"><p class="lb">Carver 01 Gold · spec card</p>
  <dl><div><dt>Lofts</dt><dd>${LOFTS.map(l => l + '°').join(' · ')}</dd></div><div><dt>Grinds</dt><dd>K · S</dd></div>
  <div><dt>Price</dt><dd class="big">$99</dd></div><div><dt>Test drive</dt><dd>60 days to prove us wrong</dd></div></dl></div></div>`;

/* ============================== 02 · REVIEW CHART ============================== */
/* A · proximity target (v3, refined) */
let seed = 11; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const RR = [46, 72, 94, 112, 128], bands = { 5: [0, 42], 4: [50, 68], 3: [76, 90], 2: [98, 108], 1: [116, 124] }, SX = 1.32, SY = .84, CX = 210, CY = 150;
let dots = '';
HIST.forEach(([st, n]) => { const [r0, r1] = bands[st];
  for (let i = 0; i < Math.max(1, Math.round(n / 10)); i++) { let a; do { a = rnd() * 6.283; } while (Math.abs(a - 4.712) < .42);
    const r = Math.sqrt(r0 * r0 + rnd() * (r1 * r1 - r0 * r0));
    dots += `<circle class="dot" style="--o:${st === 5 ? 1 : st === 4 ? .7 : .42}" cx="${(CX + Math.cos(a) * r * SX).toFixed(1)}" cy="${(CY + Math.sin(a) * r * SY).toFixed(1)}" r="2.1"/>`; } });
const proxSvg = `<svg class="px" viewBox="0 0 420 300" aria-hidden="true"><defs><radialGradient id="pe"><stop offset="0" stop-color="#C29A2B" stop-opacity=".26"/><stop offset="1" stop-color="#C29A2B" stop-opacity="0"/></radialGradient></defs>
  <ellipse cx="${CX}" cy="${CY}" rx="${RR[4] * SX}" ry="${RR[4] * SY}" fill="url(#pe)"/>
  <path class="axis" d="M${CX} ${CY - RR[4] * SY - 12}V${CY + RR[4] * SY + 12}M${CX - RR[4] * SX - 14} ${CY}H${CX + RR[4] * SX + 14}"/>
  ${RR.map((r, i) => `<ellipse class="ring${i ? ' r2' : ''}" cx="${CX}" cy="${CY}" rx="${r * SX}" ry="${r * SY}"/>`).join('')}
  ${dots}<circle class="cup" cx="${CX}" cy="${CY}" r="4"/>
  ${RR.map((r, i) => `<text class="rl${i ? '' : ' r5'}" x="${CX}" y="${(CY - r * SY + 3.5).toFixed(1)}" text-anchor="middle">${5 - i}★</text>`).join('')}</svg>`;
const barsList = `<ul class="bars">${HIST.map(([s, n]) => `<li><span>${s}★</span><i><b style="width:${pct(n).toFixed(1)}%"></b></i><em>${fmt(n)}%</em></li>`).join('')}</ul>`;
const score = `<p class="score"><b class="n">4.82</b><span class="lb">out of 5</span></p>`;
const revA = `<div class="panel">${hd('What golfers gave it', 'Closer to the cup is better')}<div class="rA">${proxSvg}<div class="side">${score}${barsList}</div></div></div>`;

/* B · share bar: one bar, split by real share */
const shareCls = { 5: 'c5', 4: 'c4', 3: 'c3', 2: 'c2', 1: 'c1' };
const revB = `<div class="panel">${hd('What golfers gave it', '')}<div class="rB">
  <div class="rB-top">${score}<p class="big-stat"><b class="n">90%</b><span class="sub">gave it all five stars</span></p></div>
  <div class="share">${HIST.map(([s, n]) => `<i class="${shareCls[s]}" style="flex:${pct(n).toFixed(2)}"></i>`).join('')}</div>
  <ul class="legend">${HIST.map(([s, n]) => `<li><i class="${shareCls[s]}"></i>${s}★ <em>${fmt(n)}%</em></li>`).join('')}</ul></div></div>`;

/* C · gauge: a 240° arc from 0 to 5, filled to 4.82 */
const GA = 240, G0 = -120, gR = 92, gC = [120, 118];
const gp = (v, r) => { const d = rad(G0 + GA * v / 5); return [gC[0] + Math.sin(d) * r, gC[1] - Math.cos(d) * r]; };
const arc = (v0, v1, r) => { const [a, b] = gp(v0, r), [c, d] = gp(v1, r); return `M${a.toFixed(1)} ${b.toFixed(1)}A${r} ${r} 0 ${GA * (v1 - v0) / 5 > 180 ? 1 : 0} 1 ${c.toFixed(1)} ${d.toFixed(1)}`; };
let gT = ''; for (let v = 0; v <= 5; v += .25) { const [a, b] = gp(v, gR + 12), [c, d] = gp(v, gR + (v % 1 ? 17 : 22)); gT += `<line class="g-tk${v % 1 ? '' : ' mj'}" x1="${a.toFixed(1)}" y1="${b.toFixed(1)}" x2="${c.toFixed(1)}" y2="${d.toFixed(1)}"/>`; }
for (let v = 0; v <= 5; v++) { const [a, b] = gp(v, gR + 34); gT += `<text class="g-lb" x="${a.toFixed(1)}" y="${(b + 4).toFixed(1)}" text-anchor="middle">${v}</text>`; }
const gauge = `<svg class="gauge" viewBox="0 0 240 200" aria-label="4.82 out of 5"><path class="g-bg" d="${arc(0, 5, gR)}"/><path class="g-fill" d="${arc(0, AVG, gR)}"/>${gT}
  <circle class="g-dot" cx="${gp(AVG, gR)[0].toFixed(1)}" cy="${gp(AVG, gR)[1].toFixed(1)}" r="5"/>
  <text class="g-num" x="120" y="126" text-anchor="middle">4.82</text><text class="g-cap" x="120" y="148" text-anchor="middle">OUT OF 5</text></svg>`;
const revC = `<div class="panel">${hd('What golfers gave it', '')}<div class="rC">${gauge}<div class="side">${barsList}</div></div></div>`;

/* D · waffle: 100 squares, each one percent of real reviews */
const cells = []; HIST.forEach(([s, n]) => { for (let i = 0; i < Math.round(pct(n)); i++) cells.push(s); });
while (cells.length > 100) cells.pop(); while (cells.length < 100) cells.push(5);
const revD = `<div class="panel">${hd('What golfers gave it', '')}<div class="rD">
  <div class="waffle" aria-label="90 of every 100 reviews are five stars">${cells.map(s => `<i class="${shareCls[s]}"></i>`).join('')}</div>
  <div class="side">${score}<p class="sub rD-note"><b>90 of every 100</b> gave it five stars.</p>
  <ul class="legend">${HIST.map(([s, n]) => `<li><i class="${shareCls[s]}"></i>${s}★ <em>${fmt(n)}%</em></li>`).join('')}</ul></div></div></div>`;

/* ============================== 03 · GREEN MAP (A-E, unchanged maths) ============================== */
const VW = 600, VH = 320;
const hills = [[150, 95, 95, 1.0], [400, 210, 120, .85], [505, 70, 70, .55], [255, 265, 80, -.5]];
const hgt = (x, y) => hills.reduce((s, [cx, cy, r, a]) => s + a * Math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)), 0);
const nrm = h => Math.max(0, Math.min(1, (h + .5) / 1.55));
function contours(GX, GY, levels) {
  const fx = i => i * VW / GX, fy = j => j * VH / GY, F = [];
  for (let j = 0; j <= GY; j++) { F[j] = []; for (let i = 0; i <= GX; i++) F[j][i] = hgt(fx(i), fy(j)); }
  return levels.map(level => { let d = ''; const lp = (a, b, va, vb) => a + (b - a) * ((level - va) / (vb - va));
    for (let j = 0; j < GY; j++) for (let i = 0; i < GX; i++) {
      const v = [F[j][i], F[j][i + 1], F[j + 1][i + 1], F[j + 1][i]];
      const c = (v[0] > level) | (v[1] > level) << 1 | (v[2] > level) << 2 | (v[3] > level) << 3;
      if (c === 0 || c === 15) continue;
      const x0 = fx(i), x1 = fx(i + 1), y0 = fy(j), y1 = fy(j + 1);
      const T = [lp(x0, x1, v[0], v[1]), y0], R = [x1, lp(y0, y1, v[1], v[2])], B = [lp(x0, x1, v[3], v[2]), y1], L = [x0, lp(y0, y1, v[0], v[3])];
      ({ 1: [[L, T]], 2: [[T, R]], 3: [[L, R]], 4: [[R, B]], 5: [[L, T], [R, B]], 6: [[T, B]], 7: [[L, B]], 8: [[L, B]], 9: [[T, B]], 10: [[T, R], [L, B]], 11: [[R, B]], 12: [[L, R]], 13: [[T, R]], 14: [[L, T]] }[c])
        .forEach(([a, b]) => { d += `M${a[0].toFixed(1)} ${a[1].toFixed(1)}L${b[0].toFixed(1)} ${b[1].toFixed(1)}`; });
    } return d; });
}
const C = contours(120, 64, [-.4, -.3, -.2, -.1, .05, .15, .25, .35, .45, .55, .65, .75, .85, .95]);
const cMinor = C.filter((_, i) => i % 2).join(''), cMajor = C.filter((_, i) => !(i % 2)).join('');
/* one path per band (not one rect per cell): same picture, a fraction of the weight */
const BANDS = {}; for (let j = 0; j < 80; j++) { let i = 0; while (i < 150) { const band = Math.floor(nrm(hgt(i * 4 + 2, j * 4 + 2)) * 8); let k = i + 1;
  while (k < 150 && Math.floor(nrm(hgt(k * 4 + 2, j * 4 + 2)) * 8) === band) k++;
  if (band > 2) (BANDS[band] = BANDS[band] || []).push(`M${i * 4} ${j * 4}h${(k - i) * 4}v4.3h-${(k - i) * 4}z`); i = k; } }
let heat = Object.keys(BANDS).map(k => `<path fill-opacity="${((k / 8 - .25) * .62).toFixed(3)}" d="${BANDS[k].join('')}"/>`).join('');
let dm = ''; for (let j = 0; j < 20; j++) for (let i = 0; i < 38; i++) { const x = i * 16 + 8, y = j * 16 + 8, n = nrm(hgt(x, y)); dm += `<circle cx="${x}" cy="${y}" r="${(.7 + n * n * 5.2).toFixed(2)}" fill-opacity="${(.18 + n * .8).toFixed(2)}"/>`; }
const proj = (x, y) => { const t = y / VH, s = .42 + .58 * t; return [VW / 2 + (x - VW / 2) * s * 1.25, 70 + Math.pow(t, 1.25) * 235 - hgt(x, y) * 70 * s]; };
let mesh = '', meshV = '';
for (let j = 0; j <= 26; j++) { mesh += 'M'; for (let i = 0; i <= 60; i++) { const p = proj(i * 10, j * (VH / 26)); mesh += `${p[0].toFixed(1)} ${p[1].toFixed(1)} `; } }
for (let i = 0; i <= 60; i += 2) { meshV += 'M'; for (let j = 0; j <= 26; j++) { const p = proj(i * 10, j * (VH / 26)); meshV += `${p[0].toFixed(1)} ${p[1].toFixed(1)} `; } }
let ridge = ''; for (let j = 2; j <= 30; j++) { const y = j * 10; let d = `M0 ${VH + 10}`; for (let x = 0; x <= VW; x += 6) d += `L${x} ${(y - hgt(x, y) * 46).toFixed(1)}`; ridge += `<path d="${d}L${VW} ${VH + 10}Z"/>`; }
const MAPS = [['A', 'Contour', 'Pure contour lines. The quietest.', `<path class="ln-minor" d="${cMinor}"/><path class="ln-major" d="${cMajor}"/>`],
  ['B', 'Elevation bands', 'Stepped bands like a real elevation map. High ground is brighter.', `<g class="heat">${heat}</g><path class="ln-hair" d="${cMajor}"/><path class="ln-hair" d="${cMinor}"/>`],
  ['C', 'Dot matrix', 'Dot size is elevation. The most digital.', `<g class="dm">${dm}</g>`],
  ['D', 'Terrain mesh', 'The green as a 3D wireframe. The most futuristic.', `<path class="ln-major" d="${mesh}"/><path class="ln-minor" d="${meshV}"/>`],
  ['E', 'Ridgelines', 'Scan lines lifted by the ground, like a radar sweep.', `<g class="ridge">${ridge}</g>`]];

const opt = (k, name, note, body, tag = 'LIBRARY', use = '') => `<div class="opt" data-tag="${tag}"><div class="opt-hd"><b>${k}</b><span class="nm">${name}</span><span class="tag">${tag}</span><span class="nt">${note}</span></div>${use ? `<p class="use"><span>Use it for</span> ${use}</p>` : ''}${body}</div>`;

const html = `<!doctype html><html lang="en" data-g="twilight"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lucky Golf · Yardage library</title>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&display=swap" rel="stylesheet">
<style>${lucky}
*{box-sizing:border-box}
html{--gold:#C29A2B}
html[data-g="day"]{--bg:#fff;--ink:#17140F;--mut:rgba(23,20,15,.62);--line:rgba(23,20,15,.15);--soft:rgba(23,20,15,.07);--gt:#8A6A1C;--panel:#FBFBF9;--halo:none;--num:linear-gradient(100deg,#6B4F0E,#A8821C 40%,#7A5C12 60%,#A8821C)}
html[data-g="twilight"]{--bg:#06110B;--ink:#F4F3F0;--mut:rgba(244,243,240,.64);--line:rgba(244,243,240,.15);--soft:rgba(244,243,240,.07);--gt:#EDD27C;--panel:#0B1911;--halo:drop-shadow(0 0 5px rgba(237,210,124,.95));--num:linear-gradient(180deg,#FFF3C4,#EDD27C 45%,#C29A2B)}
body.lg{background:var(--bg);color:var(--ink);transition:background .3s}
.lg-eyebrow{color:var(--gt)}.lg-d2,.lg-d3{color:var(--ink)}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:16px;padding:32px 0 8px}
.tg{display:flex;gap:6px}.tg button{font:600 11px Archivo,sans-serif;letter-spacing:.1em;text-transform:uppercase;min-height:44px;padding:0 14px;border-radius:9px;border:1px solid var(--line);background:none;color:var(--ink);cursor:pointer}
.tg button[aria-pressed="true"]{background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B);color:#17140F;border-color:transparent}
.cat{padding:34px 0 10px}.cat>h2{margin:0 0 4px;font-variation-settings:'wdth' 62;font-weight:800;text-transform:uppercase;font-size:clamp(1.5rem,2.6vw,2.2rem);color:var(--ink)}
.cat>p{margin:0 0 20px;color:var(--mut)}
.opts{display:grid;gap:26px}.opts.two{grid-template-columns:repeat(2,minmax(0,1fr))}
.opt-hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 12px;margin-bottom:10px}
.opt-hd b{font-variation-settings:'wdth' 62;font-weight:800;font-size:1.8rem;line-height:1;color:var(--gt)}
.opt-hd .nm{font-variation-settings:'wdth' 78;font-weight:700;text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;color:var(--ink)}
.opt-hd .nt{font-size:.88rem;color:var(--mut);flex-basis:100%}
.opt-hd .tag{font:700 .6rem Archivo,sans-serif;letter-spacing:.14em;padding:4px 8px;border-radius:6px;border:1px solid var(--line);color:var(--mut)}
.opt[data-tag="DEFAULT"] .tag,.opt[data-tag="COMPACT"] .tag{background:linear-gradient(96deg,#C29A2B,#EDD27C,#C29A2B);color:#17140F;border-color:transparent}
.use{margin:-4px 0 10px;font-size:.84rem;color:var(--mut)}.use span{font:600 .6rem Archivo,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--gt);margin-right:6px}
.opt[data-tag="LIBRARY"] .panel{opacity:.94}
.panel{position:relative;overflow:hidden;border:1px solid var(--line);border-radius:16px;background:var(--panel)}
.p-hd{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 18px;border-bottom:1px solid var(--line);font-size:.64rem;color:var(--mut)}
.live{display:inline-flex;align-items:center;gap:7px;font:600 .64rem Archivo,sans-serif;letter-spacing:.12em;text-transform:uppercase}.live i{width:7px;height:7px;border-radius:50%;background:#3FBF7F;box-shadow:0 0 8px #3FBF7F}
.lb{display:block;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.14em;font-size:.62rem;color:var(--mut)}
.n{font-variation-settings:'wdth' 62;font-weight:800;font-size:clamp(2rem,3vw,2.9rem);line-height:.95;font-variant-numeric:tabular-nums;background-image:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent;display:inline-block}
.n.s{font-size:clamp(1.3rem,2vw,1.7rem)}
.sub{font-size:.82rem;color:var(--mut);line-height:1.35}
.ph{background:#F4F3F0}.ph img{display:block;width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;padding:14px}
.vals{display:flex;flex-wrap:wrap;gap:5px}.vals i{font-style:normal;font:600 .72rem Archivo,sans-serif;font-variant-numeric:tabular-nums;padding:5px 8px;border:1px solid var(--line);border-radius:6px;color:var(--ink)}
/* monitor A */
.mA{display:grid;grid-template-columns:180px 1fr}.mA .ph{border-right:1px solid var(--line)}
.tiles{display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr}
.t{padding:18px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:8px;position:relative}
.t:last-child{border-right:0}.t::before{content:'';position:absolute;left:18px;top:0;width:22px;height:2px;background:var(--gold)}
.t .vals,.t .sub{margin-top:auto}
/* monitor B */
.mB{display:grid;grid-template-columns:120px 1fr}.mB .ph{border-right:1px solid var(--line)}
.hud{display:grid;grid-template-columns:repeat(4,1fr)}
.hud>div{padding:20px 18px;border-right:1px solid var(--line);display:flex;flex-direction:column;gap:6px;justify-content:center}.hud>div:last-child{border-right:0}
/* monitor C */
.mC{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);align-items:center;gap:10px;padding:18px 22px}
.prot{width:100%;max-width:300px;height:auto}
.pr-arc{fill:none;stroke:var(--line);stroke-width:1}.pr-band{fill:var(--gold);fill-opacity:.08}.pr-tk{stroke:var(--mut);stroke-opacity:.45}.pr-tk.mj{stroke-opacity:.9;stroke-width:1.4}.pr-spoke{stroke:var(--gold);stroke-width:1.6;filter:var(--halo)}.pr-cap{font:600 8px Archivo,sans-serif;letter-spacing:.14em;fill:var(--mut)}
.pr-hub{fill:var(--gold)}.pr-lb{font:700 11px Archivo,sans-serif;fill:var(--ink)}
.mC-r{display:grid;gap:16px}.mC-ph{height:170px;border-radius:12px;overflow:hidden}.mini{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--line);padding-top:14px;gap:10px}
/* monitor D */
.mD{display:grid;grid-template-columns:200px 1fr}.mD .ph{border-right:1px solid var(--line)}
.spec{padding:20px 24px}.spec dl{margin:12px 0 0}
.spec dl>div{display:flex;align-items:baseline;gap:10px;padding:11px 0;border-bottom:1px solid var(--line)}.spec dl>div:last-child{border:0}
.spec dt{flex:none;font:600 .7rem Archivo,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}
.spec dt::after{content:'';display:inline-block;width:40px}
.spec dd{margin:0 0 0 auto;text-align:right;font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}
.spec dd.big{font-variation-settings:'wdth' 62;font-weight:800;font-size:2rem;line-height:1;background-image:var(--num);-webkit-background-clip:text;background-clip:text;color:transparent}
.spec dl>div{background:radial-gradient(circle,var(--line) 1px,transparent 1.5px) 0 70%/6px 6px repeat-x}
.spec dt,.spec dd{background:var(--panel);position:relative}.spec dt{padding-right:8px}.spec dd{padding-left:8px}
/* reviews */
.side{padding:20px 22px;border-left:1px solid var(--line);align-self:stretch;display:flex;flex-direction:column;justify-content:center;gap:14px}
.score{margin:0;display:flex;align-items:baseline;gap:10px}.score .n{font-size:clamp(2.8rem,4.6vw,4rem)}
.bars{list-style:none;margin:0;padding:0;display:grid;gap:7px;font-size:.72rem;color:var(--mut);font-variant-numeric:tabular-nums}
.bars li{display:grid;grid-template-columns:24px 1fr 38px;align-items:center;gap:8px}.bars i{height:4px;border-radius:9px;background:var(--soft);overflow:hidden}.bars b{display:block;height:100%;background:var(--gold)}.bars em{font-style:normal;text-align:right}
.rA,.rC,.rD{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);align-items:center}
.px{width:100%;height:auto;display:block}
.axis{stroke:var(--line);fill:none}.ring{fill:none;stroke:var(--gold);stroke-opacity:.75}.ring.r2{stroke:var(--mut);stroke-opacity:.45;stroke-dasharray:1.5 5}
.rl{font:500 9.5px Archivo,sans-serif;letter-spacing:.04em;fill:var(--mut);paint-order:stroke;stroke:var(--panel);stroke-width:2.5px;stroke-linejoin:round}.rl.r5{fill:var(--gt);font-weight:600}
.dot{fill:var(--gold);fill-opacity:var(--o);filter:var(--halo)}.cup{fill:var(--panel);stroke:var(--ink);stroke-width:1.5}
.c5{background:var(--gold)}.c4{background:color-mix(in srgb,var(--gold) 55%,var(--panel))}.c3,.c2,.c1{background:var(--mut);opacity:.5}.c2{opacity:.38}.c1{opacity:.26}
.rB{padding:22px 24px;display:grid;gap:18px}.rB-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:end;gap:14px}
.big-stat{margin:0;text-align:right}.big-stat .n{font-size:clamp(2rem,3.4vw,2.8rem)}.big-stat .sub{display:block}
.share{display:flex;gap:2px;height:14px;border-radius:4px;overflow:hidden}.share i{display:block;min-width:3px}
.legend{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 16px;font-size:.74rem;color:var(--mut);font-variant-numeric:tabular-nums}
.legend li{display:flex;align-items:center;gap:6px}.legend i{width:10px;height:10px;border-radius:2px}.legend em{font-style:normal;color:var(--ink)}
.gauge{width:100%;max-width:340px;height:auto;display:block;margin:auto;padding:16px}
.g-bg{fill:none;stroke:var(--soft);stroke-width:10;stroke-linecap:round}.g-fill{fill:none;stroke:var(--gold);stroke-width:10;stroke-linecap:round;filter:var(--halo)}
.g-tk{stroke:var(--mut);stroke-opacity:.5}.g-tk.mj{stroke-opacity:.9;stroke-width:1.5}.g-lb{font:600 10px Archivo,sans-serif;fill:var(--mut)}
.g-dot{fill:var(--panel);stroke:var(--gold);stroke-width:3}
.g-num{font:800 44px Archivo,sans-serif;font-variation-settings:'wdth' 62;fill:var(--gt)}.g-cap{font:600 9px Archivo,sans-serif;letter-spacing:.16em;fill:var(--mut)}
.waffle{display:grid;grid-template-columns:repeat(10,1fr);gap:4px;padding:22px;max-width:360px;margin:auto;width:100%}
.waffle i{aspect-ratio:1;border-radius:3px}.rD-note b{color:var(--ink)}
/* green maps */
.p-map{min-height:240px;display:flex;align-items:center}
.gm{position:absolute;inset:0;width:100%;height:100%;-webkit-mask-image:linear-gradient(90deg,transparent 22%,#000 66%);mask-image:linear-gradient(90deg,transparent 22%,#000 66%)}
.ln-minor{fill:none;stroke:var(--ink);stroke-opacity:.13;stroke-width:.8}.ln-major{fill:none;stroke:var(--gold);stroke-opacity:.7;stroke-width:1}.ln-hair{fill:none;stroke:var(--ink);stroke-opacity:.22;stroke-width:.7}
.heat rect,.heat path{fill:var(--gold)}.dm circle{fill:var(--gold)}.ridge path{fill:var(--panel);stroke:var(--gold);stroke-opacity:.6;stroke-width:1}
.map-copy{position:relative;padding:24px;max-width:28ch}.map-copy .lg-d3{font-size:1.3rem}.map-copy .sub{margin:6px 0 0}

/* ============ TABLET 750-1080 ============ */
@media (max-width:1080px){
  .cat-rev .opts.two{grid-template-columns:1fr}
  .tiles{grid-template-columns:1fr 1fr}.t:nth-child(2){border-right:0}.t:nth-child(-n+2){border-bottom:1px solid var(--line)}
  .mA{grid-template-columns:200px 1fr}
  .hud{grid-template-columns:1fr 1fr}.hud>div:nth-child(2){border-right:0}.hud>div:nth-child(-n+2){border-bottom:1px solid var(--line)}
}
/* ============ PHONE 0-749 ============ */
@media (max-width:749px){
  .opts.two{grid-template-columns:1fr}
  .mA,.mB,.mD{grid-template-columns:1fr}
  .mA .ph,.mB .ph,.mD .ph{height:190px;border-right:0;border-bottom:1px solid var(--line)}
  .mB .ph{height:150px}
  .mC{grid-template-columns:1fr}.prot{max-width:240px;margin:auto}
  .mini{grid-template-columns:1fr 1fr 1fr}
  .rA,.rC,.rD{grid-template-columns:1fr}.side{border-left:0;border-top:1px solid var(--line)}
  .spec{padding:18px}.spec dd{font-size:.9rem}
  .p-hd{flex-direction:column;align-items:flex-start;gap:4px}
}
</style></head><body class="lg">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><filter id="blur" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="9"/></filter></defs></svg>
<div class="lg-wrap">
  <div class="top"><div><p class="lg-eyebrow">Lucky design library · Yardage</p><h1 class="lg-d2">The instruments.</h1><p class="sub" style="max-width:60ch;margin-top:8px">Gold tags are the defaults. Everything else is kept here on purpose, for the places it fits better. Change one here and it changes everywhere it's used.</p></div>
    <div class="tg" role="group" aria-label="Ground"><button data-g="day" aria-pressed="false">Daylight</button><button data-g="twilight" aria-pressed="true">Twilight round</button></div></div>

  <section class="cat"><h2>01 · Monitor panel</h2><p>The product facts, read like a launch monitor. For product pages.</p><div class="opts">
    ${opt('A', 'Data tiles', 'Four tiles with the real values as chips.', monA, 'DEFAULT', 'Product pages. The full readout.')}
    ${opt('B', 'HUD strip', 'One slim readout bar. Takes the least room.', monB, 'COMPACT', 'Anywhere space is tight: collection cards, sticky bars, emails.')}
    ${opt('C', 'Loft chart', 'Zoomed to 48-62 degrees, so every loft gets real room.', monC, 'LIBRARY', 'Ads and technical pages: a wedge launch, a loft guide, a fitting page.')}
    ${opt('D', 'Spec card', 'Yardage-book rows with dotted leaders. The most classic.', monD, 'LIBRARY', 'Comparison pages, printed inserts, spec sheets.')}
  </div></section>

  <section class="cat cat-rev"><h2>02 · Review chart</h2><p>Same real reviews, four ways. For the reviews block.</p><div class="opts two">
    ${opt('A', 'Proximity', 'A top-down target. Closer to the cup is better.', revA, 'DEFAULT', 'Every reviews block.')}
    ${opt('B', 'Share bar', 'One bar split by the real share of each rating.', revB, 'LIBRARY', 'Tight spots: a product card, a cart drawer, an email.')}
    ${opt('C', 'Gauge', 'A dial filled to 4.82.', revC, 'LIBRARY', 'The app, and big-number moments in ads.')}
    ${opt('D', 'Grid', '100 squares. Each is one percent of reviews.', revD, 'LIBRARY', 'Social posts and ads: reads in one glance.')}
  </div></section>

  <section class="cat"><h2>03 · Green map</h2><p>Behind flat text sections. Same ground, five ways.</p><div class="opts two">
    ${MAPS.map(([k, name, note, body]) => opt(k, name, note, `<div class="panel p-map"><svg class="gm" viewBox="0 0 ${VW} ${VH}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">${body}</svg><div class="map-copy"><h3 class="lg-d3">Great clubs got too expensive.</h3><p class="sub">A flat text section with the map behind it.</p></div></div>`, k === 'A' ? 'DEFAULT' : 'LIBRARY', { A: 'Behind any flat section on the site. Subtle on purpose.', B: 'The app, and course or green content.', C: 'The app. The most digital.', D: 'Launch moments and hero graphics.', E: 'Loading and transition screens, the app.' }[k])).join('\n    ')}
  </div></section>
</div>
<script>document.addEventListener('click',function(e){var b=e.target.closest('.tg [data-g]');if(!b)return;document.documentElement.setAttribute('data-g',b.dataset.g);document.querySelectorAll('.tg button').forEach(function(x){x.setAttribute('aria-pressed',x===b)})});</script>
</body></html>`;
fs.writeFileSync(path.join(__dirname, 'extras.html'), html);
fs.writeFileSync(ROOT + '/design/yardage-library.html', html);
fs.writeFileSync(ROOT + '/shopify/gwp-yardage-extras.html', html);
console.log('extras v4 built', Math.round(html.length / 1024) + 'KB');
