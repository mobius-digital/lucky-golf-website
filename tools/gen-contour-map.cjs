/* The Lucky contour map: ONE big green, drawn once, used everywhere.
   Every use shows a different part of it (position, size, flip), so it never
   looks the same twice (Cole, Sept 18: "variety makes it a good website").

   v3: v2 was four round hills on a coarse grid, and the line thinning turned
   long curves into straight runs ("rigid in some areas"). This one is real
   rolling terrain (layered smooth noise plus a few big undulations, like a
   green with a tier), on a fine grid, stitched, lightly thinned, and drawn as
   centripetal Catmull-Rom curves, which don't kink on uneven point spacing.

   Out: shopify/assets/lucky-contour-day.svg and lucky-contour-tw.svg
   (a background image can't read CSS variables, so the colour is baked in).
   Run: node tools/gen-contour-map.cjs */
const fs = require('fs'), path = require('path');
const OUT = path.resolve(__dirname, '../shopify/assets');
const VW = 2400, VH = 1600, CELL = 5, GX = VW / CELL, GY = VH / CELL;

/* seeded value noise, smoothstep-interpolated */
let seed = 20260918;
const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
const N = 64, lattice = Array.from({ length: N * N }, rnd);
const L = (i, j) => lattice[((j % N + N) % N) * N + ((i % N + N) % N)];
const sm = t => t * t * t * (t * (t * 6 - 15) + 10);
function noise(x, y) {
  const i = Math.floor(x), j = Math.floor(y), u = sm(x - i), v = sm(y - j);
  const a = L(i, j), b = L(i + 1, j), c = L(i, j + 1), d = L(i + 1, j + 1);
  return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
}
const fbm = (x, y) => { let s = 0, amp = 1, f = 1, tot = 0; for (let o = 0; o < 2; o++) { s += amp * noise(x * f, y * f); tot += amp; amp *= .5; f *= 2.03; } return s / tot; };
const hills = [[620, 520, 460, .7], [1650, 1050, 560, .6], [1950, 360, 320, .35], [900, 1300, 400, -.45], [1250, 700, 260, .2]];
const H = (x, y) => fbm(x / 900, y / 900) * 1.0 +
  hills.reduce((s, [cx, cy, r, a]) => s + a * Math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)), 0);

const F = [];
let lo = Infinity, hi = -Infinity;
for (let j = 0; j <= GY; j++) { F[j] = new Float64Array(GX + 1); for (let i = 0; i <= GX; i++) { const h = H(i * CELL, j * CELL); F[j][i] = h; if (h < lo) lo = h; if (h > hi) hi = h; } }

function segments(level) {
  const segs = [], lp = (a, b, va, vb) => a + (b - a) * ((level - va) / (vb - va));
  for (let j = 0; j < GY; j++) for (let i = 0; i < GX; i++) {
    const v0 = F[j][i], v1 = F[j][i + 1], v2 = F[j + 1][i + 1], v3 = F[j + 1][i];
    const c = (v0 > level) | (v1 > level) << 1 | (v2 > level) << 2 | (v3 > level) << 3;
    if (c === 0 || c === 15) continue;
    const x0 = i * CELL, x1 = x0 + CELL, y0 = j * CELL, y1 = y0 + CELL;
    const T = [lp(x0, x1, v0, v1), y0], R = [x1, lp(y0, y1, v1, v2)], B = [lp(x0, x1, v3, v2), y1], Lf = [x0, lp(y0, y1, v0, v3)];
    const m = { 1: [[Lf, T]], 2: [[T, R]], 3: [[Lf, R]], 4: [[R, B]], 5: [[Lf, T], [R, B]], 6: [[T, B]], 7: [[Lf, B]], 8: [[Lf, B]], 9: [[T, B]], 10: [[T, R], [Lf, B]], 11: [[R, B]], 12: [[Lf, R]], 13: [[T, R]], 14: [[Lf, T]] }[c];
    for (const s of m) segs.push(s);
  }
  return segs;
}
function stitch(segs) {
  const key = p => p[0].toFixed(3) + ',' + p[1].toFixed(3), ends = new Map(), used = new Uint8Array(segs.length);
  segs.forEach((s, n) => s.forEach((p, e) => { const k = key(p); let a = ends.get(k); if (!a) ends.set(k, a = []); a.push([n, e]); }));
  const next = p => (ends.get(key(p)) || []).find(([n]) => !used[n]);
  const lines = [];
  for (let n = 0; n < segs.length; n++) {
    if (used[n]) continue; used[n] = 1;
    const line = [segs[n][0], segs[n][1]];
    for (const dir of [1, -1]) {
      let tip = dir === 1 ? line[line.length - 1] : line[0], hop;
      while ((hop = next(tip))) { const [m, e] = hop; used[m] = 1; const p = segs[m][1 - e]; if (dir === 1) line.push(p); else line.unshift(p); tip = p; }
    }
    lines.push(line);
  }
  return lines;
}
function dp(pts, tol) {
  if (pts.length < 3) return pts;
  const keep = new Uint8Array(pts.length); keep[0] = keep[pts.length - 1] = 1;
  const stack = [[0, pts.length - 1]];
  while (stack.length) {
    const [s, e] = stack.pop(), a = pts[s], b = pts[e], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1;
    let max = 0, idx = -1;
    for (let i = s + 1; i < e; i++) { const d = Math.abs(dy * pts[i][0] - dx * pts[i][1] + b[0] * a[1] - b[1] * a[0]) / len; if (d > max) { max = d; idx = i; } }
    if (max > tol) { keep[idx] = 1; stack.push([s, idx], [idx, e]); }
  }
  return pts.filter((_, i) => keep[i]);
}
const f = n => Math.round(n);
/* centripetal Catmull-Rom (alpha .5) -> cubic Bezier: no cusps, no overshoot on uneven spacing */
function smooth(pts) {
  const closed = pts.length > 3 && Math.hypot(pts[0][0] - pts[pts.length - 1][0], pts[0][1] - pts[pts.length - 1][1]) < .01;
  if (closed) pts = pts.slice(0, -1);
  const n = pts.length; if (n < 2) return '';
  const P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
  const dist = (a, b) => Math.max(1e-6, Math.sqrt(Math.hypot(b[0] - a[0], b[1] - a[1])));
  let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    const d1 = dist(p0, p1), d2 = dist(p1, p2), d3 = dist(p2, p3);
    const c1 = [p1[0] + (p2[0] - p0[0]) * d2 / (3 * (d1 + d2)) , p1[1] + (p2[1] - p0[1]) * d2 / (3 * (d1 + d2))];
    const c2 = [p2[0] - (p3[0] - p1[0]) * d2 / (3 * (d2 + d3)), p2[1] - (p3[1] - p1[1]) * d2 / (3 * (d2 + d3))];
    d += `C${f(c1[0])} ${f(c1[1])} ${f(c2[0])} ${f(c2[1])} ${f(p2[0])} ${f(p2[1])}`;
  }
  return closed ? d + 'Z' : d;
}
const COUNT = 16, step = (hi - lo) / (COUNT + 1);
const minor = [], major = [];
for (let k = 1; k <= COUNT; k++) {
  const d = stitch(segments(lo + k * step)).map(l => dp(l, 1.2)).filter(l => l.length > 2).map(smooth).join('');
  (k % 4 === 0 ? major : minor).push(d);
}
const svg = (ink, inkOp, gold, goldOp) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${VW} ${VH}">` +
  `<path fill="none" stroke="${ink}" stroke-opacity="${inkOp}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" d="${minor.join('')}"/>` +
  `<path fill="none" stroke="${gold}" stroke-opacity="${goldOp}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" d="${major.join('')}"/></svg>`;
fs.writeFileSync(path.join(OUT, 'lucky-contour-day.svg'), svg('#17140F', .2, '#A8821C', .6));
fs.writeFileSync(path.join(OUT, 'lucky-contour-tw.svg'), svg('#F4F3F0', .2, '#C29A2B', .65));
console.log('lucky-contour:', ['day', 'tw'].map(k => k + ' ' + Math.round(fs.statSync(path.join(OUT, 'lucky-contour-' + k + '.svg')).size / 1024) + 'KB').join(', '));
