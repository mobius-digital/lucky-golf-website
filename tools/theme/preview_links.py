"""Writes theme/snippets/lg-preview-links.liquid: while the build theme is only being PREVIEWED, point
internal links at the new templates (?view=...), since the template suffixes aren't set until launch
night (launch_day.py). Inert once the theme is published (Shopify.theme.role == 'main')."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import launch_day as L

m = {f"/products/{h}": t for h, t in L.PRODUCTS}
m.update({f"/collections/{h}": t for h, t in L.COLLECTIONS})
m.update({f"/pages/{h}": t for h, t in L.PAGES})
m.update({f"/pages/{h}": t for h, _, t in L.NEW_PAGES})
js = """<script>
(function(){
  var S=window.Shopify; if(!S||!S.theme||S.theme.role==='main')return;
  var M=%s;
  function fix(a){
    try{var u=new URL(a.href,location.href)}catch(e){return}
    if(u.hostname.replace(/^www\./,'')!==location.hostname.replace(/^www\./,''))return;
    var p=u.pathname.replace(/\/$/,''),v=M[p];
    if(!v){var k=p.match(/\/products\/[^\/]+$/);v=k&&M[k[0]]}
    if(!v||u.searchParams.has('view'))return;
    if(p==='/pages/compare'||p==='/pages/community')u.pathname='/pages/about';  // hidden until launch night
    u.searchParams.set('view',v); a.href=u.toString();
  }
  function all(){document.querySelectorAll('a[href]').forEach(fix)}
  document.addEventListener('DOMContentLoaded',all); all();
  document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(a)fix(a)},true);
  document.addEventListener('mouseover',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(a)fix(a)},true);
})();
</script>
""" % json.dumps(m, separators=(",", ":"))
open(os.path.join(L.ROOT, "theme", "snippets", "lg-preview-links.liquid"), "w", encoding="utf-8").write(js)
print(len(m), "paths")
