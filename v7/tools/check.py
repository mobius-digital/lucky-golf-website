"""
Render every v4 page in real headless Chrome at desktop, tablet and phone
widths and refuse to pass anything the owner should never see.

    python v4/tools/check.py              # all pages, all widths
    python v4/tools/check.py --shots      # also save full-page screenshots to v4/qa/

FAILS on:
  * any <img> that did not load (the v1/v2 review sheets were full of these)
  * a product card showing an image that belongs to another product
  * the page scrolling sideways (v2 on phone)
  * text below WCAG contrast against its real background (4.5:1, 3:1 if large)
  * a JavaScript error

Text laid over a photograph cannot be measured from CSS; those elements are
listed as "on photo" so a person looks at them in the screenshots.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
V4 = os.path.normpath(os.path.join(HERE, ".."))
OUT = os.path.join(V4, "out")
QA = os.path.join(V4, "qa")
PAGES = ["clubs.html", "polos.html"]
WIDTHS = [("desktop", 1440, 900), ("tablet", 834, 1112), ("phone", 390, 844)]

CHROME = next((p for p in (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
) if os.path.exists(p)), None)

PROBE = r"""
<script>
(function(){
  var errors=[];
  window.addEventListener('error',function(e){errors.push(String(e.message||e));});
  function lum(c){var m=c.match(/[\d.]+/g).map(Number);var a=m.slice(0,3).map(function(v){v/=255;return v<=0.03928?v/12.92:Math.pow((v+0.055)/1.055,2.4)});return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2];}
  function parse(c){var m=(c.match(/[\d.]+/g)||[]).map(Number);return {r:m[0],g:m[1],b:m[2],a:m.length>3?m[3]:1};}
  function over(top,bot){return {r:top.r*top.a+bot.r*(1-top.a),g:top.g*top.a+bot.g*(1-top.a),b:top.b*top.a+bot.b*(1-top.a),a:1};}
  function str(c){return 'rgb('+c.r+','+c.g+','+c.b+')';}
  function bgOf(el){
    var stack=[];
    for(var n=el;n&&n.nodeType===1;n=n.parentElement){
      var cs=getComputedStyle(n);
      if(cs.backgroundImage&&cs.backgroundImage!=='none'&&!/gradient/.test(cs.backgroundImage))return {photo:true};
      if(/gradient/.test(cs.backgroundImage)){
        if(n===el||n.matches('.btn,.pill,.tag')){var stops=(cs.backgroundImage.match(/rgba?\([^)]*\)/g)||[]).map(parse);return {stops:stops};}
        return {photo:true};
      }
      var c=parse(cs.backgroundColor);
      if(c.a>0)stack.push(c);
      if(c.a>=1)break;
      // text positioned over a sibling image (hero captions)
      if(n.parentElement&&[].some.call(n.parentElement.children,function(s){return s!==n&&(s.tagName==='IMG'||s.tagName==='PICTURE')&&getComputedStyle(n).position==='absolute';}))return {photo:true};
    }
    var col={r:255,g:255,b:255,a:1};
    for(var i=stack.length-1;i>=0;i--)col=over(stack[i],col);
    return {color:col};
  }
  function run(){
    var res={w:innerWidth,h:document.documentElement.scrollHeight,images:[],mismatch:[],overflow:null,wide:[],contrast:[],onPhoto:[],errors:errors};
    [].forEach.call(document.images,function(im){ if(!(im.complete&&im.naturalWidth>0)) res.images.push(im.getAttribute('src')); });
    [].forEach.call(document.querySelectorAll('[data-pid] img'),function(im){
      var pid=im.closest('[data-pid]').getAttribute('data-pid'); var f=(im.getAttribute('src')||'').split('/').pop();
      if(f.indexOf(pid+'-')!==0) res.mismatch.push(pid+' shows '+f);
    });
    var sw=document.documentElement.scrollWidth; if(sw>innerWidth+1) res.overflow=sw;
    [].forEach.call(document.querySelectorAll('body *'),function(el){
      var r=el.getBoundingClientRect(); if(!r.width||!r.height)return;
      var cs=getComputedStyle(el); if(cs.visibility==='hidden'||cs.display==='none')return;
      var inScroller=false; for(var n=el.parentElement;n;n=n.parentElement){var o=getComputedStyle(n).overflowX; if(o==='auto'||o==='scroll'||o==='hidden'){inScroller=true;break;}}
      if(!inScroller&&(r.right>innerWidth+1||r.left<-1)&&res.wide.length<8) res.wide.push((el.className||el.tagName)+' '+Math.round(r.left)+'..'+Math.round(r.right));
      var own=[].some.call(el.childNodes,function(t){return t.nodeType===3&&t.textContent.trim().length>1;});
      if(!own)return;
      if(cs.opacity==='0')return;
      if((cs.webkitTextFillColor||'').indexOf('rgba(0, 0, 0, 0)')===0||/transparent/.test(cs.webkitTextFillColor||'')){
        var b0=bgOf(el.parentElement); if(b0.photo){res.onPhoto.push('foil: '+el.textContent.trim().slice(0,40));return;}
        var L0=lum(str(b0.color)); var dark=L0<0.2;
        if(!dark&&parseFloat(cs.fontSize)<24) res.contrast.push({t:'foil on light, small: '+el.textContent.trim().slice(0,40),ratio:0,need:3});
        return;
      }
      var b=bgOf(el); if(b.photo){res.onPhoto.push(el.textContent.trim().slice(0,50));return;}
      var fg=parse(cs.color); var bgs=b.stops&&b.stops.length?b.stops:[b.color]; var ratio=99, bg=bgs[0];
      bgs.forEach(function(bc){var f=over(fg,bc);var L1=lum(str(f)),L2=lum(str(bc));var q=(Math.max(L1,L2)+0.05)/(Math.min(L1,L2)+0.05);if(q<ratio){ratio=q;bg=bc;}});
      var size=parseFloat(cs.fontSize),bold=parseInt(cs.fontWeight,10)>=700; var large=size>=24||(size>=18.66&&bold);
      var need=large?3:4.5;
      if(el.closest('.stars'))need=3;  /* rating stars are a graphic next to the number: 1.4.11, 3:1 */
      if(el.closest('button:disabled'))need=0;
      if(ratio<need) res.contrast.push({t:el.textContent.trim().slice(0,50),ratio:Math.round(ratio*100)/100,need:need,fg:cs.color,bg:str(bg)});
    });
    parent.postMessage('QA'+JSON.stringify(res)+'QA','*');
  }
  window.addEventListener('load',function(){
    [].forEach.call(document.images,function(im){im.loading='eager';});
    var waits=[].map.call(document.images,function(im){return im.complete?Promise.resolve():new Promise(function(r){im.onload=im.onerror=r;});});
    Promise.all(waits.concat([document.fonts?document.fonts.ready:Promise.resolve()])).then(function(){setTimeout(run,300);});
  });
})();
</script>
"""


HARNESS = """<!DOCTYPE html><html><body style="margin:0;background:#888">
<iframe id="f" src="{src}" style="border:0;display:block;width:{w}px;height:{h}px"></iframe>
<script>window.addEventListener('message',function(e){{var p=document.createElement('pre');p.textContent=e.data;document.body.appendChild(p);}});</script>
</body></html>"""


def harness(tmp, page, label, w, h):
    path = os.path.join(tmp, f"_h-{label}-{h}-{page}")
    open(path, "w", encoding="utf-8").write(HARNESS.format(src=page, w=w, h=h))
    return "file:///" + path.replace("\\", "/")


def chrome(args, timeout=90):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                           "--no-first-run", "--no-default-browser-check", "--run-all-compositor-stages-before-draw"] + args,
                          capture_output=True, text=True, encoding="utf-8", errors="ignore", timeout=timeout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shots", action="store_true")
    ap.add_argument("pages", nargs="*")
    a = ap.parse_args()
    if not CHROME:
        sys.exit("no Chrome or Edge found")
    pages = a.pages or PAGES
    tmp = tempfile.mkdtemp(prefix="luckyqa-", dir=OUT)
    if a.shots:
        os.makedirs(QA, exist_ok=True)
    bad = 0
    report = {}
    try:
        for page in pages:
            src = open(os.path.join(OUT, page), encoding="utf-8").read()
            probe = src.replace("</body>", PROBE + "</body>")
            probe = probe.replace('href="site.css"', 'href="../site.css"').replace('src="site.js"', 'src="../site.js"')
            probe = re.sub(r'(src|href)="img/', r'\1="../img/', probe)
            qpath = os.path.join(tmp, page)
            open(qpath, "w", encoding="utf-8").write(probe)
            for label, w, h in WIDTHS:
                url = harness(tmp, page, label, w, h)
                r = chrome([f"--window-size={max(w, 600)},{h}", "--virtual-time-budget=20000", "--dump-dom", url])
                m = re.search(r"QA(\{.*?\})QA", r.stdout, re.S)
                if not m:
                    print(f"FAIL {page} @ {label}: probe did not report (page may not have loaded)")
                    bad += 1
                    continue
                res = json.loads(m.group(1).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
                report[f"{page}@{label}"] = res
                problems = []
                if res["images"]:
                    problems.append(f"{len(res['images'])} image(s) failed: {res['images'][:4]}")
                if res["mismatch"]:
                    problems.append(f"wrong product image: {res['mismatch']}")
                if res["overflow"]:
                    problems.append(f"page scrolls sideways ({res['overflow']}px wide at {res['w']}): {res['wide']}")
                if res["contrast"]:
                    problems.append(f"{len(res['contrast'])} contrast failure(s): " + "; ".join(f"'{c['t']}' {c['ratio']}:1" for c in res["contrast"][:6]))
                if res["errors"]:
                    problems.append(f"JS errors: {res['errors']}")
                status = "FAIL" if problems else "pass"
                bad += bool(problems)
                print(f"{status} {page:16} {label:8} {res['w']}px  height {res['h']}px  on-photo text: {len(res['onPhoto'])}")
                for p in problems:
                    print("     - " + p)
                if a.shots:
                    shot = os.path.join(QA, f"{page.replace('.html', '')}-{label}.png")
                    hh = min(res["h"], 16000)
                    chrome([f"--window-size={max(w, 600)},{hh}", "--virtual-time-budget=20000", f"--screenshot={shot}", harness(tmp, page, label, w, hh)], timeout=120)
                    if w < 600:
                        from PIL import Image
                        Image.open(shot).crop((0, 0, w, hh)).save(shot)
        json.dump(report, open(os.path.join(V4, "qa-report.json"), "w", encoding="utf-8"), indent=1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("ALL CLEAR" if not bad else f"{bad} page/width combination(s) failed")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
