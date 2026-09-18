/* Green map A (Contour), the default, exported as two real SVG files for the
   Shopify theme: one coloured for Daylight, one for Twilight. A background
   image cannot read CSS variables, so the colour is baked into each file.

   v2 (Sept 18): the first cut drew every marching-squares cell as its own
   2-point segment, rounded to whole pixels, on a coarse grid. Stretched to a
   full-width section that read as jagged. Now: a fine grid, the segments are
   stitched into continuous lines, thinned (Douglas-Peucker), then drawn as
   smooth curves (Catmull-Rom to cubic Bezier). Strokes don't scale with the
   stretch (vector-effect), so the lines stay hairlines at any width. */
const fs = require('fs');
const OUT = 'C:/Users/wetzl/Lucky Golf/Website/shopify/assets/';
const VW = 600, VH = 320, GX = 180, GY = 96;
const hills = [[150, 95, 95, 1.0], [400, 210, 120, .85], [505, 70, 70, .55], [255, 265, 80, -.5]];
const hgt = (x, y) => hills.reduce((s, [cx, cy, r, a]) => s + a * Math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * r * r)), 0);
const fx = i => i * VW / GX, fy = j => j * VH / GY, F = [];
for (let j = 0; j <= GY; j++) { F[j] = []; for (let i = 0; i <= GX; i++) F[j][i] = hgt(fx(i), fy(j)); }

function segments(level) {
  const segs = [], lp = (a, b, va, vb) => a + (b - a) * ((level - va) / (vb - va));
  for (let j = 0; j < GY; j++) for (let i = 0; i < GX; i++) {
    const v = [F[j][i], F[j][i + 1], F[j + 1][i + 1], F[j + 1][i]];
    const c = (v[0] > level) | (v[1] > level) << 1 | (v[2] > level) << 2 | (v[3] > level) << 3;
    if (c === 0 || c === 15) continue;
    const x0 = fx(i), x1 = fx(i + 1), y0 = fy(j), y1 = fy(j + 1);
    const T = [lp(x0, x1, v[0], v[1]), y0], R = [x1, lp(y0, y1, v[1], v[2])], B = [lp(x0, x1, v[3], v[2]), y1], L = [x0, lp(y0, y1, v[0], v[3])];
    ({ 1: [[L, T]], 2: [[T, R]], 3: [[L, R]], 4: [[R, B]], 5: [[L, T], [R, B]], 6: [[T, B]], 7: [[L, B]], 8: [[L, B]], 9: [[T, B]], 10: [[T, R], [L, B]], 11: [[R, B]], 12: [[L, R]], 13: [[T, R]], 14: [[L, T]] }[c])
      .forEach(s => segs.push(s));
  }
  return segs;
}

/* stitch 2-point segments into continuous polylines (shared endpoints match exactly) */
function stitch(segs) {
  const key = p => p[0].toFixed(4) + ',' + p[1].toFixed(4), ends = new Map(), used = new Array(segs.length).fill(false);
  segs.forEach((s, n) => s.forEach((p, e) => { const k = key(p); if (!ends.has(k)) ends.set(k, []); ends.get(k).push([n, e]); }));
  const next = (p, from) => (ends.get(key(p)) || []).find(([n]) => !used[n] && n !== from);
  const lines = [];
  segs.forEach((s, n) => {
    if (used[n]) return; used[n] = true;
    const line = [s[0], s[1]];
    for (const dir of [1, -1]) {
      let tip = dir === 1 ? line[line.length - 1] : line[0], hop;
      while ((hop = next(tip, -1))) {
        const [m, e] = hop; used[m] = true; const p = segs[m][1 - e];
        if (dir === 1) line.push(p); else line.unshift(p); tip = p;
      }
    }
    lines.push(line);
  });
  return lines;
}

function dp(pts, tol) {  // Douglas-Peucker
  if (pts.length < 3) return pts;
  const [a, b] = [pts[0], pts[pts.length - 1]], dx = b[0] - a[0], dy = b[1] - a[1], len = Math.hypot(dx, dy) || 1;
  let max = 0, idx = 0;
  for (let i = 1; i < pts.length - 1; i++) { const d = Math.abs(dy * pts[i][0] - dx * pts[i][1] + b[0] * a[1] - b[1] * a[0]) / len; if (d > max) { max = d; idx = i; } }
  if (max <= tol) return [a, b];
  return dp(pts.slice(0, idx + 1), tol).slice(0, -1).concat(dp(pts.slice(idx), tol));
}

const f = n => +n.toFixed(1);
function smooth(pts) {  // Catmull-Rom -> cubic Bezier
  const closed = pts.length > 3 && Math.hypot(pts[0][0] - pts[pts.length - 1][0], pts[0][1] - pts[pts.length - 1][1]) < .01;
  if (closed) pts = pts.slice(0, -1);
  const n = pts.length, P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
  let d = `M${f(pts[0][0])} ${f(pts[0][1])}`;
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    d += `C${f(p1[0] + (p2[0] - p0[0]) / 6)} ${f(p1[1] + (p2[1] - p0[1]) / 6)} ${f(p2[0] - (p3[0] - p1[0]) / 6)} ${f(p2[1] - (p3[1] - p1[1]) / 6)} ${f(p2[0])} ${f(p2[1])}`;
  }
  return closed ? d + 'Z' : d;
}

const contour = level => stitch(segments(level)).map(l => dp(l, .9)).filter(l => l.length > 1).map(smooth).join('');
const LV = [-.4, -.3, -.2, -.1, .05, .15, .25, .35, .45, .55, .65, .75, .85, .95];
const minor = LV.filter((_, i) => i % 2).map(contour).join(''), major = LV.filter((_, i) => !(i % 2)).map(contour).join('');
const svg = (ink, inkOp, gold, goldOp) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${VW} ${VH}" preserveAspectRatio="xMidYMid slice">` +
  `<path fill="none" stroke="${ink}" stroke-opacity="${inkOp}" stroke-width="1" vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" d="${minor}"/>` +
  `<path fill="none" stroke="${gold}" stroke-opacity="${goldOp}" stroke-width="1.25" vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round" d="${major}"/></svg>`;
fs.writeFileSync(OUT + 'gwp-contour-day.svg', svg('#17140F', .13, '#A8821C', .55));
fs.writeFileSync(OUT + 'gwp-contour-tw.svg', svg('#F4F3F0', .14, '#C29A2B', .6));
console.log('contour assets:', ['day', 'tw'].map(k => k + ' ' + Math.round(fs.statSync(OUT + 'gwp-contour-' + k + '.svg').size / 1024) + 'KB').join(', '));
