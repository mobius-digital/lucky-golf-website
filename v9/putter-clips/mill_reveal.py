"""Builds mill-reveal.html: the 'fully milled' card animated in code, no AI video.
Two stills of the same head (smooth face / milled face). The milled pattern spreads out from the sight
line in both directions behind a thin bright cutting edge, fine gold chips flick off the edge, and the
camera eases back. Loops. Same code goes into the theme section once Cole approves the look."""
import base64, os
H = os.path.dirname(os.path.abspath(__file__))
b64 = lambda f: base64.b64encode(open(os.path.join(H, f), 'rb').read()).decode()
SMOOTH, MILLED = b64('blade-face-smooth-1920.webp'), b64('blade-face-dark-1920.webp')
MASK = b64('_facemask-soft.png')
COLS = open(os.path.join(H, '_facecols.json')).read()

html = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Milled Face Animation</title>
<style>
:root{--bg:#f4f2ee;--ink:#17140F}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111;--ink:#f4f3f0}}
:root[data-theme="dark"]{--bg:#111;--ink:#f4f3f0}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px}
h1{font-size:20px;margin:0 0 12px}
.mill{position:relative;aspect-ratio:16/9;border-radius:8px;overflow:hidden;background:#0b0d0c}
.mill .cam{position:absolute;inset:0;transform-origin:42% 62%}
.mill img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mill .cut{clip-path:inset(0 58% 0 42%);-webkit-mask:url(data:image/png;base64,MASKB64) center/100% 100%;mask:url(data:image/png;base64,MASKB64) center/100% 100%;mask-mode:luminance}
.mill .edge{position:absolute;top:28%;bottom:4%;width:2px;background:linear-gradient(180deg,transparent,#fff6d6 30%,#fff 55%,#fff6d6 80%,transparent);
  box-shadow:0 0 10px 3px rgba(255,214,120,.55),0 0 28px 8px rgba(255,190,80,.25);mix-blend-mode:screen;opacity:0}
.mill canvas{position:absolute;inset:0;width:100%;height:100%;mix-blend-mode:screen;pointer-events:none}
p{color:color-mix(in srgb,var(--ink) 70%,transparent)}
button{margin-top:12px;font:inherit;padding:8px 14px;border:1px solid currentColor;background:none;color:inherit;border-radius:6px;cursor:pointer}
</style></head><body><main>
<h1>Fully milled: the face gets cut in</h1>
<div class="mill" id="mill">
  <div class="cam">
    <img src="data:image/webp;base64,SMOOTH" alt="">
    <img class="cut" src="data:image/webp;base64,MILLED" alt="Eclipse Blade, milled face">
      </div>
  <canvas id="fx"></canvas>
</div>
<p>No cutter on screen: the pattern spreads out from the sight line behind a bright cutting edge, chips flick off, and the camera eases back. It loops every 7 seconds.</p>
<button id="replay">Replay</button>
</main>
<script>
(function(){
  var box=document.getElementById('mill'), cam=box.querySelector('.cam'), cut=box.querySelector('.cut'),
      COLS=COLSJSON, cv=document.getElementById('fx'), cx=cv.getContext('2d');
  var ORIGIN=0.42, HOLD0=600, RUN=3800, HOLD1=2600, T=HOLD0+RUN+HOLD1, t0=performance.now(), parts=[];
  function size(){ var r=box.getBoundingClientRect(), d=Math.min(2,window.devicePixelRatio||1); cv.width=r.width*d; cv.height=r.height*d; cx.setTransform(d,0,0,d,0,0); }
  size(); addEventListener('resize', size);
  var ease=function(x){ return x<.5 ? 4*x*x*x : 1-Math.pow(-2*x+2,3)/2; };
  function col(x){ var c=COLS[Math.max(0,Math.min(COLS.length-1,Math.floor(x*COLS.length)))]; return c; }
  function edge(x, w, h){ var c=col(x); if(!c) return; var y0=c[0]*h, y1=c[1]*h, g=cx.createLinearGradient(0,y0,0,y1);
    g.addColorStop(0,'rgba(255,240,200,0)'); g.addColorStop(.15,'rgba(255,240,200,.95)'); g.addColorStop(.85,'rgba(255,240,200,.95)'); g.addColorStop(1,'rgba(255,240,200,0)');
    cx.save(); cx.shadowColor='rgba(255,200,90,.9)'; cx.shadowBlur=14; cx.strokeStyle=g; cx.lineWidth=2; cx.beginPath(); cx.moveTo(x*w,y0); cx.lineTo(x*w,y1); cx.stroke(); cx.restore(); }
  function spawn(x, dir, w, h){
    var c=col(x); if(!c) return;
    for (var i=0;i<3;i++) parts.push({x:x*w, y:h*(c[0]+Math.random()*(c[1]-c[0])), vx:dir*(40+Math.random()*120), vy:-30-Math.random()*90,
      life:0, max:.5+Math.random()*.6, r:.6+Math.random()*1.4, hot:Math.random()<.35});
  }
  function frame(now){
    var t=(now-t0)%T, w=box.clientWidth, h=box.clientHeight;
    var p=Math.min(1,Math.max(0,(t-HOLD0)/RUN)), e=ease(p);
    var L=ORIGIN-ORIGIN*e, R=ORIGIN+(1-ORIGIN)*e;            // revealed band [L,R] in 0..1
    cut.style.clipPath='inset(0 '+((1-R)*100)+'% 0 '+(L*100)+'%)';
    var cutting=p>0&&p<1, o=cutting?1:0;
    cam.style.transform='scale('+(1.09-0.09*ease(Math.min(1,t/(HOLD0+RUN+HOLD1*.6))))+')';
    cx.clearRect(0,0,w,h);
    if (cutting){ edge(L,w,h); edge(R,w,h); spawn(L,-1,w,h); spawn(R,1,w,h); }
    var dt=1/60;
    parts=parts.filter(function(q){ q.life+=dt; q.vy+=260*dt; q.x+=q.vx*dt; q.y+=q.vy*dt; return q.life<q.max; });
    parts.forEach(function(q){ var a=1-q.life/q.max; cx.fillStyle=q.hot?'rgba(255,248,220,'+a+')':'rgba(237,200,110,'+a*.9+')';
      cx.beginPath(); cx.arc(q.x,q.y,q.r,0,6.283); cx.fill(); });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  document.getElementById('replay').onclick=function(){ t0=performance.now(); parts=[]; };
})();
</script></body></html>"""
open(os.path.join(H, 'mill-reveal.html'), 'w', encoding='utf-8').write(html.replace('SMOOTH', SMOOTH).replace('MILLED', MILLED).replace('MASKB64', MASK).replace('COLSJSON', COLS))
print('ok')
