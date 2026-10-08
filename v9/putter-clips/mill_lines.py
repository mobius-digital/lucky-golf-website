"""mill-lines.html: the Blade face being milled groove by groove (Takomo's 'precision-milled' move, done
for our pattern). Our face is a pyramid knurl = two sets of straight grooves crossing at about +/-45 deg to
the face. Pass 1 cuts every groove in one direction, one after another, each with a bright cutting point
running along it; pass 2 cuts the crossing set and the pyramids appear. The camera starts tight on the
sight line and pulls back; it settles on the real milled photo. Everything drawn in code, no AI video."""
import base64, os
from PIL import Image, ImageFilter
H = os.path.dirname(os.path.abspath(__file__))
m = Image.open(os.path.join(H, '_facemask.png')).convert('L').filter(ImageFilter.MinFilter(17)).filter(ImageFilter.GaussianBlur(2))
rgba=Image.new('RGBA',m.size,(255,255,255,0)); rgba.putalpha(m); rgba.save(os.path.join(H, '_facemask-1920.png'))
b64 = lambda f: base64.b64encode(open(os.path.join(H, f), 'rb').read()).decode()

html = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Milled Face</title>
<style>
:root{--bg:#f4f2ee;--ink:#17140F}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#111;--ink:#f4f3f0}}
:root[data-theme="dark"]{--bg:#111;--ink:#f4f3f0}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,sans-serif}
main{max-width:960px;margin:0 auto;padding:24px 16px}
h1{font-size:20px;margin:0 0 12px}
.stage{position:relative;aspect-ratio:16/9;border-radius:8px;overflow:hidden;background:#0b0d0c}
canvas{display:block;width:100%;height:100%}
button{margin-top:12px;font:inherit;padding:8px 14px;border:1px solid currentColor;background:none;color:inherit;border-radius:6px;cursor:pointer}
</style></head><body><main>
<h1>Fully milled: cut line by line</h1>
<div class="stage"><canvas id="c"></canvas></div>
<button id="replay">Replay</button>
</main>
<script>
(function(){
var IW=1920, IH=1086, SIGHT={x:0.455*IW, y:0.505*IH};
var cv=document.getElementById('c'), ctx=cv.getContext('2d');
function load(src){ return new Promise(function(r){ var i=new Image(); i.onload=function(){ r(i); }; i.src=src; }); }
Promise.all([load('data:image/webp;base64,SMOOTH'), load('data:image/webp;base64,MILLED'), load('data:image/png;base64,MASK')]).then(function(a){
  var smooth=a[0], milled=a[1], mask=a[2];
  // groove layer in image space, persists between frames
  var g=document.createElement('canvas'); g.width=IW; g.height=IH; var gx=g.getContext('2d');
  var mk=document.createElement('canvas'); mk.width=IW; mk.height=IH; var mkx=mk.getContext('2d'); mkx.drawImage(mask,0,0,IW,IH); var MD=mkx.getImageData(0,0,IW,IH).data;
  var onFace=function(x,y){ return MD[(y*IW+x)*4+3]>128; };
  var tmp=document.createElement('canvas'); tmp.width=IW; tmp.height=IH; var tx=tmp.getContext('2d');
  var ar1=document.createElement('canvas'); ar1.width=IW; ar1.height=IH; var a1=ar1.getContext('2d');
  var ar2=document.createElement('canvas'); ar2.width=IW; ar2.height=IH; var a2=ar2.getContext('2d');
  var met=document.createElement('canvas'); met.width=IW; met.height=IH; var mx2=met.getContext('2d');
  // face box from the mask
  var FX0=0, FX1=0.80*IW, FY0=0.36*IH, FY1=0.95*IH;
  var TILT=-10*Math.PI/180, SP=11;                       // groove spacing in px (measured off the photo)
  function grooves(angle){
    var d={x:Math.cos(angle), y:Math.sin(angle)}, n={x:-d.y, y:d.x};
    var cx=(FX0+FX1)/2, cy=(FY0+FY1)/2, R=Math.hypot(FX1-FX0, FY1-FY0)/2+20, list=[];
    // order lines by distance from the sight line so the cut spreads out from it
    for (var k=-Math.ceil(R/SP); k<=Math.ceil(R/SP); k++){
      var ox=cx+n.x*k*SP, oy=cy+n.y*k*SP;
      var dist=Math.abs((ox-SIGHT.x)*n.x+(oy-SIGHT.y)*n.y);
      list.push({a:{x:ox-d.x*R, y:oy-d.y*R}, b:{x:ox+d.x*R, y:oy+d.y*R}, dist:dist, n:n});
    }
    list.sort(function(p,q){ return p.dist-q.dist; });
    return list;
  }
  var P1=grooves(TILT+Math.PI/2), P2=[];   // one pass: cuts across the face, spreading out from the sight line
  var T0=400, PASS=4400, GAP=0, FADE=500, HOLD=1600;
  var LINE=320, STAG1=(PASS-LINE)/P1.length, STAG2=(PASS-LINE)/P2.length;
  var TOTAL=T0+PASS+FADE+HOLD, start=performance.now(), drawn1=[], drawn2=[], AREA=a1;
  function reset(){ start=performance.now(); gx.clearRect(0,0,IW,IH); a1.clearRect(0,0,IW,IH); a2.clearRect(0,0,IW,IH); drawn1=P1.map(function(){return 0;}); drawn2=P2.map(function(){return 0;}); }
  reset(); document.getElementById('replay').onclick=reset;
  function cut(L, f0, f1, heads){
    // draw the groove from f0 to f1 of its length: shadow side, dark core, bright lip
    var ax=L.a.x+(L.b.x-L.a.x)*f0, ay=L.a.y+(L.b.y-L.a.y)*f0, bx=L.a.x+(L.b.x-L.a.x)*f1, by=L.a.y+(L.b.y-L.a.y)*f1;
    gx.lineCap='round';
    AREA.strokeStyle='#fff'; AREA.lineCap='butt'; AREA.lineWidth=SP+1.5; AREA.beginPath(); AREA.moveTo(ax,ay); AREA.lineTo(bx,by); AREA.stroke();
    gx.strokeStyle='rgba(30,18,0,.38)'; gx.lineWidth=2.6; gx.beginPath(); gx.moveTo(ax,ay); gx.lineTo(bx,by); gx.stroke();
    gx.strokeStyle='rgba(255,240,185,.45)'; gx.lineWidth=1.2; gx.beginPath(); gx.moveTo(ax+L.n.x*1.8,ay+L.n.y*1.8); gx.lineTo(bx+L.n.x*1.8,by+L.n.y*1.8); gx.stroke();
    if (f1<1) heads.push({x:bx, y:by});
  }
  function pass(list, drawn, t, stag, heads){
    for (var i=0;i<list.length;i++){
      var f=Math.min(1, Math.max(0, (t-i*stag)/LINE));
      if (f>drawn[i]){ cut(list[i], drawn[i], f, heads); drawn[i]=f; }
      else if (f>0 && f<1) heads.push({x:list[i].a.x+(list[i].b.x-list[i].a.x)*f, y:list[i].a.y+(list[i].b.y-list[i].a.y)*f});
    }
  }
  function frame(now){
    var W=cv.clientWidth, Hh=cv.clientHeight, dpr=Math.min(2, window.devicePixelRatio||1);
    if (cv.width!==Math.round(W*dpr)){ cv.width=Math.round(W*dpr); cv.height=Math.round(Hh*dpr); }
    var t=now-start; if (t>TOTAL){ reset(); t=0; }
    var heads=[];
    if (t>T0){ AREA=a1; pass(P1, drawn1, t-T0, STAG1, heads); }
    
    // masked grooves
    tx.globalCompositeOperation='source-over'; tx.clearRect(0,0,IW,IH); tx.drawImage(g,0,0);
    tx.globalCompositeOperation='destination-in'; tx.drawImage(mask,0,0,IW,IH);
    // camera: tight on the sight line, easing back
    var k=Math.min(1, t/(T0+PASS+FADE)), e=1-Math.pow(1-k,3);
    var zoom=2.8-1.75*e, base=Math.max(cv.width/IW, cv.height/IH)*zoom;
    var fx=SIGHT.x+(IW/2-SIGHT.x)*e*0.7, fy=SIGHT.y+(IH*0.56-SIGHT.y)*e*0.7;
    ctx.setTransform(base,0,0,base, cv.width/2-fx*base, cv.height/2-fy*base);
    ctx.clearRect(-1e4,-1e4,2e4,2e4);
    ctx.drawImage(smooth,0,0,IW,IH);
    function metal(area, alpha){ mx2.globalCompositeOperation='source-over'; mx2.clearRect(0,0,IW,IH); mx2.drawImage(milled,0,0,IW,IH);
      mx2.globalCompositeOperation='destination-in'; mx2.drawImage(area,0,0); mx2.drawImage(mask,0,0,IW,IH);
      ctx.globalAlpha=alpha; ctx.drawImage(met,0,0); ctx.globalAlpha=1; }
    metal(ar1, 1);
    ctx.drawImage(tmp,0,0);
    var tf=t-(T0+PASS); if (tf>0){ ctx.globalAlpha=Math.min(1, tf/FADE); ctx.drawImage(milled,0,0,IW,IH); ctx.globalAlpha=1; }
    // the cutting points: small hot glints, only on the face
    heads.forEach(function(h){
      var mx=Math.round(h.x), my=Math.round(h.y); if (mx<0||my<0||mx>=IW||my>=IH||!onFace(mx,my)) return;
      var r=ctx.createRadialGradient(h.x,h.y,0,h.x,h.y,7); r.addColorStop(0,'rgba(255,252,235,.95)'); r.addColorStop(.35,'rgba(255,214,120,.55)'); r.addColorStop(1,'rgba(255,200,90,0)');
      ctx.fillStyle=r; ctx.beginPath(); ctx.arc(h.x,h.y,7,0,6.283); ctx.fill();
    });
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
});
})();
</script></body></html>"""
html = html.replace('SMOOTH', b64('blade-face-smooth-1920.webp')).replace('MILLED', b64('blade-face-dark-1920.webp')).replace('MASK', b64('_facemask-1920.png'))
open(os.path.join(H, 'mill-lines.html'), 'w', encoding='utf-8').write(html)
print('ok')
