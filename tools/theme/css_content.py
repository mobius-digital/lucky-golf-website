"""Write theme/css/70-content.css: the content pages' own CSS (Our Story, FAQ, Ambassadors,
Compare, Contact, Community, Reviews, 404, Search), taken from each approved page's <style>
and scoped to the section wrapper class (.lgc-*) that sections_content.py gives each section.

    python tools/theme/css_content.py && python tools/theme/build_css.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from build_css import scope_css

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "theme", "css", "70-content.css")


def tighten(css):
    """Takomo-tight corners (same rule as group 80): no 12-18px radii, no pills."""
    css = re.sub(r"border-radius:(1[0-8])px", "border-radius:var(--lg-r-card)", css)
    return css.replace("border-radius:var(--lg-r)", "border-radius:var(--lg-r)")


CHIP = """{min-height:40px;padding:0 14px;border-radius:var(--lg-r);border:1px solid var(--lg-rule);background:var(--lg-page);color:var(--lg-ink);font-size:var(--lg-fs-sm);cursor:pointer}"""
LBL = """{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;text-transform:uppercase;letter-spacing:.1em;font-size:var(--lg-fs-xs);color:var(--lg-ink-64)}"""
CARD_B = """{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:var(--lg-fs-body);margin-bottom:6px}"""

C = {}

C["lgc-hero"] = """
.lg-hero .lg-btn-line .ic{width:18px;height:18px;stroke-width:1.8}
"""

C["lgc-man"] = """
.man{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:clamp(24px,5vw,80px);align-items:start}
@media (max-width:900px){.man{grid-template-columns:1fr;gap:18px}}
.man .lg-d1{margin:0}
.man .lg-body{margin:0 0 14px;max-width:60ch}
.man-close{margin:clamp(14px,2vw,22px) 0 0;font-weight:800;text-transform:uppercase;font-variation-settings:'wdth' 66;font-size:clamp(20px,2.4vw,26px);letter-spacing:.01em}
"""

C["lgc-parts"] = """
.parts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(20px,3vw,40px)}
@media (max-width:760px){.parts{grid-template-columns:1fr;gap:40px}}
.part{display:flex;flex-direction:column;min-width:0}
.part figure{margin:0 0 18px;border-radius:var(--lg-r-card);overflow:hidden;aspect-ratio:4/3;background:var(--lg-night)}
@media (max-width:760px){.part figure{aspect-ratio:16/9}}
.part img{width:100%;height:100%;object-fit:cover;display:block}
.part h2{margin:6px 0 10px}
.part > p:not(.lg-eyebrow){margin:0 0 14px;color:var(--lg-ink-70)}
.part .lg-link{margin-top:auto;align-self:flex-start}
"""

C["lgc-pband"] = """
.lg-d1{max-width:22ch}
.lg-lede{max-width:56ch}
"""

C["lgc-tl"] = """
.tl-in{position:relative}
.tl-hd{display:flex;align-items:end;justify-content:space-between;gap:20px;margin-top:10px}
.tl-hd .lg-lede{max-width:60ch;margin:0}
@media (max-width:640px){.tl-hd .arrows{display:none}}
.tl{list-style:none;margin:clamp(20px,3vw,32px) 0 0;padding:0 0 10px;display:grid;grid-auto-flow:column;grid-auto-columns:minmax(230px,270px);gap:var(--lg-gut);overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:thin}
.tl > li{scroll-snap-align:start;padding:16px 0 0;border-top:2px solid var(--lg-gold)}
.tl > li[data-soon]{border-top-style:dashed;border-top-color:var(--lg-rule)}
.tl .yr{display:block;margin-bottom:8px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 62;font-weight:800;text-transform:uppercase;letter-spacing:.02em;
  font-size:clamp(15px,1.5vw,19px);line-height:1.1;color:var(--lg-ink-64);padding-top:3px}
.tl li[data-soon] .yr{color:var(--lg-ink-38)}
.tl h3{margin:0 0 6px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:clamp(17px,1.8vw,22px);line-height:1.08}
.tl p{margin:0;color:var(--lg-ink-64);max-width:62ch}
.tl .soon{margin-left:8px;vertical-align:2px}
"""

C["lgc-cols"] = """
.lg-body{max-width:62ch}
.cols{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--lg-gut);margin-top:clamp(20px,3vw,32px)}
@media (max-width:860px){.cols{grid-template-columns:1fr}}
.nx{display:block;padding:clamp(20px,2.4vw,28px);border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);color:inherit;text-decoration:none;background:var(--lg-page)}
.nx:hover{border-color:var(--lg-ink)}
.nx b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:18px;margin-bottom:6px}
.nx span{color:var(--lg-ink-64)}
.nx .go{display:block;margin-top:14px;font-size:var(--lg-fs-sm)}
.hcard{display:block;padding:clamp(20px,2.4vw,28px);border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);color:inherit;text-decoration:none}
a.hcard:hover{border-color:var(--lg-ink)}
.hcard b""" + CARD_B + """
.hcard span{display:block;color:var(--lg-ink-64)}
.hcard .ic{width:22px;height:22px;stroke-width:1.6;margin-bottom:12px;display:block}
@media (max-width:900px){.cols-numbers{grid-template-columns:1fr}}
.num .n{display:block;color:var(--lg-gold-text);font-weight:700;font-size:var(--lg-fs-sm);margin-bottom:10px}
.num h3{margin:0}
.num p{color:var(--lg-ink-70);margin:8px 0 0}
.rule{border-top:2px solid var(--lg-gold);padding-top:14px}
.rule b{display:block;font-size:var(--lg-fs-body);margin-bottom:4px}
.rule p{margin:0;color:var(--lg-ink-70)}
.after{max-width:62ch;margin-top:clamp(18px,2.5vw,24px)}
"""

C["lgc-faq"] = """
.faq-intro{padding-bottom:clamp(20px,3vw,32px)}
.faq-intro .lg-lede{max-width:60ch}
.jump{position:sticky;top:var(--lg-head-h,64px);z-index:22;background:var(--lg-page);border-block:1px solid var(--lg-rule)}
.jump-in{display:flex;gap:8px;overflow:auto;padding-block:10px;scrollbar-width:none}
.jump-in::-webkit-scrollbar{display:none}
.jump a{flex:none;min-height:40px;display:inline-flex;align-items:center;padding:0 14px;border:1px solid var(--lg-rule);border-radius:var(--lg-r);
  color:var(--lg-ink);text-decoration:none;font-size:var(--lg-fs-sm);white-space:nowrap}
.jump a:hover{border-color:var(--lg-ink)}
.blk{scroll-margin-top:calc(var(--lg-head-h,64px) + 64px)}
.blk-in{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.2fr);gap:clamp(24px,4vw,64px);align-items:start}
.blk.is-even .blk-in{grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(28px,5vw,72px)}
@media (max-width:860px){.blk-in,.blk.is-even .blk-in{grid-template-columns:1fr}}
.lg-fq-a > p:first-child{margin-top:0}
"""

C["lgc-ask"] = """
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(28px,5vw,72px);align-items:start}
@media (max-width:900px){.two{grid-template-columns:1fr}}
.bar-list{list-style:none;margin:clamp(18px,2.5vw,26px) 0 0;padding:0;display:grid;gap:12px}
.bar-list li{display:flex;gap:12px;align-items:flex-start}
.bar-list .ic{width:20px;height:20px;stroke-width:1.7;flex:none;margin-top:3px}
.bar-list b{color:var(--lg-ink)}
.after{margin-top:clamp(18px,2.5vw,24px)}
.apply{align-self:start}
.apply .lg-btn{margin-top:16px}
"""

C["lgc-proof"] = """
.proof{display:flex;flex-wrap:wrap;gap:10px 28px;align-items:center;color:var(--lg-ink-70);font-size:var(--lg-fs-sm)}
.proof .lg-stars{margin-right:6px}
"""

C["lgc-pc"] = """
.cards{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--lg-gut);margin-top:clamp(20px,3vw,32px);max-width:860px}
@media (max-width:560px){.cards{grid-template-columns:1fr}}
.pc{display:flex;flex-direction:column;border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);overflow:hidden;background:var(--lg-page)}
.pc-ph{position:relative;display:block;aspect-ratio:4/5;background:var(--lg-tile);overflow:hidden}
.pc-ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;mix-blend-mode:multiply;padding:12px;transition:transform .5s var(--lg-ease)}
.pc:hover .pc-ph img{transform:scale(1.03)}
.pc-ph .lg-tag{position:absolute;left:12px;top:12px;z-index:1}
.pc-bd{display:flex;flex-direction:column;gap:10px;padding:16px 18px 18px;flex:1}
.pc-top{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.pc-top h3{margin:0;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:20px;line-height:1}
.pc-top h3 a{text-decoration:none;color:inherit;display:inline-block;padding:11px 0;margin:-11px 0}
.pc-top b{font-weight:700}
.pc-rate{display:inline-flex;align-items:center;gap:8px;text-decoration:none;color:var(--lg-ink-64);font-size:var(--lg-fs-sm)}
.pc p{margin:0;color:var(--lg-ink-70);font-size:var(--lg-fs-base)}
.pc .lg-btn{margin-top:auto;width:100%}
"""

C["lgc-table"] = """
.lg-body{max-width:62ch}
.tablewrap{overflow-x:auto;border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);margin-top:clamp(20px,3vw,32px)}
.tablewrap table{min-width:620px}
.lg-table th[scope=col]{text-align:left}
.lg-table td.us{color:var(--lg-ink);font-weight:600}
.lg-table td.them{color:var(--lg-ink-64)}
@media (max-width:640px){
.tablewrap table{min-width:0}
.lg-table thead tr,.lg-table tbody tr{display:grid;grid-template-columns:1fr 1fr}
.lg-table thead th:first-child{display:none}
.lg-table tbody th{grid-column:1/-1;padding-bottom:0;border-bottom:0;font-size:var(--lg-fs-xs);text-transform:uppercase;letter-spacing:.1em;color:var(--lg-ink-64)}
}
.after{max-width:62ch;margin-top:clamp(18px,2.5vw,24px)}
"""

C["lgc-rq"] = """
.rqs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:var(--lg-gut);margin-top:clamp(20px,3vw,32px)}
@media (max-width:900px){.rqs{grid-template-columns:1fr}}
.rq{margin:0;border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);padding:22px;display:flex;flex-direction:column;gap:12px;background:var(--lg-page)}
.rq blockquote{margin:0;font-size:var(--lg-fs-body);line-height:1.45;color:var(--lg-ink)}
.rq figcaption{margin-top:auto;color:var(--lg-ink-64);font-size:var(--lg-fs-sm)}
.rq figcaption b{color:var(--lg-ink)}
.after{max-width:62ch;margin-top:clamp(18px,2.5vw,24px)}
"""

C["lgc-contact"] = """
.wrap2{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(28px,5vw,72px);align-items:start}
@media (max-width:900px){.wrap2{grid-template-columns:1fr}}
.ways{list-style:none;margin:clamp(20px,3vw,28px) 0 0;padding:0;display:grid;gap:14px}
.ways li{display:flex;gap:14px;align-items:flex-start;padding-bottom:14px;border-bottom:1px solid var(--lg-rule)}
.ways li:last-child{border-bottom:0}
.ways .ic{width:22px;height:22px;stroke-width:1.6;flex:none;margin-top:2px}
.ways b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:700;text-transform:uppercase;font-size:var(--lg-fs-base)}
.ways p{margin:2px 0 0;color:var(--lg-ink-64)}
.ways p a{color:var(--lg-ink);text-decoration:none;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 76;font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:var(--lg-fs-sm);border-bottom:2px solid var(--lg-gold);padding-bottom:4px}
.form{border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);padding:clamp(20px,3vw,32px)}
.row{display:grid;gap:14px;margin-bottom:14px}
@media (min-width:640px){.row.two{grid-template-columns:1fr 1fr}}
.form label{display:block}
.form .lb{display:block;margin-bottom:6px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 78;font-weight:600;
  text-transform:uppercase;letter-spacing:.08em;font-size:var(--lg-fs-xs);color:var(--lg-ink-64)}
.form input,.form select,.form textarea{width:100%;min-height:48px;border:1px solid var(--lg-rule);border-radius:var(--lg-r);
  background:var(--lg-page);color:var(--lg-ink);padding:12px 14px;font:inherit}
.form textarea{min-height:140px;resize:vertical}
.form .lg-btn .ic{width:18px;height:18px}
.sent{display:none;padding:14px 16px;border-radius:var(--lg-r);background:var(--lg-tile);margin:0}
.sent.is-on{display:block}
.sent.is-err{margin-bottom:14px}
.sent.is-err ul{margin:0;padding-left:18px}
"""

C["lgc-wall"] = """
.bar{position:sticky;top:var(--lg-head-h,64px);z-index:22;background:var(--lg-page);border-bottom:1px solid var(--lg-rule)}
.bar-in{display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;padding-block:12px}
.fg{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.fg .lbl""" + LBL + """
.fg button""" + CHIP + """
.fg button[aria-pressed="true"]{background:var(--lg-ink);color:var(--lg-page);border-color:var(--lg-ink)}
.count{margin-left:auto;font-size:var(--lg-fs-sm);color:var(--lg-ink-64)}
@media (max-width:640px){.bar-in{flex-wrap:nowrap;gap:12px}.fg{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;min-width:0}.fg::-webkit-scrollbar{display:none}.fg button{flex:none}.count{flex:none}}
.wall{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px;padding-block:clamp(16px,2.4vw,28px) 0}
@media (max-width:1100px){.wall{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:640px){.wall{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px}}
.post{position:relative;display:block;width:100%;aspect-ratio:4/5;border:0;padding:0;border-radius:var(--lg-r);overflow:hidden;background:var(--lg-tile);cursor:pointer;color:inherit}
.post[hidden]{display:none}
.post img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s ease}
@media (hover:hover){.post:hover img{transform:scale(1.03)}}
.post::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,color-mix(in srgb,var(--lg-night) 42%,transparent) 0%,transparent 26%,transparent 74%,color-mix(in srgb,var(--lg-night) 38%,transparent) 100%);pointer-events:none}
.post .who{position:absolute;z-index:1;left:10px;top:10px;color:var(--lg-on-dark);font-size:var(--lg-fs-xs);font-weight:600}
.post .bag{position:absolute;z-index:1;right:10px;bottom:10px;display:inline-flex;align-items:center;gap:5px;padding:5px 9px;border-radius:var(--lg-r);background:color-mix(in srgb,var(--lg-surface) 94%,transparent);color:var(--lg-ink);font-size:var(--lg-fs-xs);font-weight:700}
.post .bag .ic{width:14px;height:14px;stroke-width:2}
.more{display:flex;flex-wrap:wrap;gap:12px 24px;align-items:center;justify-content:space-between;padding-block:clamp(20px,3vw,32px) clamp(40px,6vw,72px)}
.more p{margin:0}
.more [hidden]{display:none}
"""

C["lgc-rv"] = """
.sum{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(24px,4vw,64px);align-items:center}
@media (max-width:900px){.sum{grid-template-columns:1fr}}
.sum .lg-score > b{font-size:clamp(56px,7vw,80px)}
.sum .of{display:block;margin-top:8px;font-size:var(--lg-fs-sm);color:var(--lg-ink-64)}
.lg-score-row.is-btn{width:100%;border:0;background:none;padding:6px 0;margin:-6px 0;min-height:40px;cursor:pointer;font:inherit;font-size:var(--lg-fs-sm);color:var(--lg-ink-64);text-align:left}
.lg-score-row.is-btn:hover,.lg-score-row.is-btn[aria-pressed="true"]{color:var(--lg-ink)}
.lg-score-row.is-btn[aria-pressed="true"] i{outline:2px solid var(--lg-ink);outline-offset:2px}
.clubs{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--lg-gut)}
.ct{display:block;width:100%;text-align:left;padding:clamp(16px,2vw,22px);border:1px solid var(--lg-rule);border-radius:var(--lg-r-card);background:var(--lg-page);color:inherit;cursor:pointer;font:inherit}
.ct:hover{border-color:var(--lg-ink)}
.ct[aria-pressed="true"]{border-color:var(--lg-ink);box-shadow:inset 0 0 0 1px var(--lg-ink)}
.ct b{display:block;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 66;font-weight:800;text-transform:uppercase;font-size:18px;line-height:1.1}
.ct > span{display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;margin-top:8px;font-size:var(--lg-fs-sm);color:var(--lg-ink-64)}
.ct em{font-style:normal;white-space:nowrap}
.bar{position:sticky;top:var(--lg-head-h,64px);z-index:22;background:var(--lg-page);border-block:1px solid var(--lg-rule);margin-top:clamp(28px,4vw,48px)}
.bar-in{display:flex;flex-wrap:wrap;align-items:center;gap:10px 22px;padding-block:12px}
.fg{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.fg .lbl""" + LBL + """
.fg button""" + CHIP + """
.fg button[aria-pressed="true"]{background:var(--lg-ink);color:var(--lg-page);border-color:var(--lg-ink)}
.fright{margin-left:auto}
.fright select{min-height:40px;border-radius:var(--lg-r);border:1px solid var(--lg-rule);background:var(--lg-page);color:var(--lg-ink);padding:0 12px;font:inherit;font-size:var(--lg-fs-sm)}
@media (max-width:640px){.bar{position:static}.fg{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;width:100%}.fg::-webkit-scrollbar{display:none}.fg button,.fg .lbl{flex:none}.fright{margin-left:0}}
.jm{padding-top:clamp(8px,1.5vw,16px);padding-bottom:clamp(40px,6vw,72px)}
.club-note{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;margin:16px 0 0;color:var(--lg-ink-64);font-size:var(--lg-fs-sm)}
.club-note[hidden]{display:none}
.club-note em{font-style:normal}
.jdgm-rev[hidden]{display:none!important}
/* Judge.me's widget: only the product reviews list shows; our score, bars and bar above replace its header */
.jdgm-all-reviews__header,.jdgm-subtab,.jdgm-row-actions,.jdgm-shop-reviews__body,.jdgm-medals-wrapper,.jdgm-row-media,.jdgm-widget-actions-wrapper,.jdgm-write-rev-link{display:none!important}
.jdgm-widget{font-family:inherit;color:var(--lg-ink)}
.jdgm-widget .jdgm-star{color:var(--lg-star)!important}
.jdgm-widget .jdgm-paginate__load-more,.jdgm-widget .jdgm-paginate__page{border-radius:var(--lg-r-btn)!important;font-family:'Archivo',sans-serif;font-weight:700;font-size:var(--lg-fs-sm)}
/* each Judge.me review as our card, two across: stars + date, title, words, name · Verified buyer, the club */
.jdgm-all-reviews__body{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));align-items:start;gap:var(--lg-gut);padding-block:clamp(16px,2vw,24px)}
@media (max-width:860px){.jdgm-all-reviews__body{grid-template-columns:1fr}}
.jdgm-widget .jdgm-rev{display:flex!important;flex-direction:column;gap:8px;margin:0!important;padding:20px 0!important;border:0!important;border-top:1px solid var(--lg-rule)!important;border-radius:0;background:none}
.jdgm-widget .jdgm-rev[hidden]{display:none!important}
.jdgm-widget .jdgm-rev .jdgm-rev__header,.jdgm-widget .jdgm-rev .jdgm-rev__content{display:contents}
.jdgm-widget .jdgm-rev .jdgm-rev__br,.jdgm-widget .jdgm-rev .jdgm-rev__icon,.jdgm-widget .jdgm-rev .jdgm-row-extra,.jdgm-widget .jdgm-rev .jdgm-rev__transparency-badge-wrapper,.jdgm-widget .jdgm-rev .jdgm-rev__actions,.jdgm-widget .jdgm-rev .jdgm-rev__custom-form:empty,.jdgm-widget .jdgm-rev .jdgm-rev__buyer-badge-wrapper,.jdgm-widget .jdgm-rev .jdgm-rev__prod-link-prefix{display:none!important}
.jdgm-widget .jdgm-row-rating{order:1;display:flex;justify-content:space-between;align-items:center;gap:12px;margin:0}
.jdgm-widget .jdgm-rev__rating{color:var(--lg-star);letter-spacing:2px}
.jdgm-widget .jdgm-rev__rating .jdgm-star{font-size:14px;padding:0 1px!important}
.jdgm-widget .jdgm-rev__timestamp{color:var(--lg-ink-64);font-size:var(--lg-fs-sm);margin:0!important}
.jdgm-widget .jdgm-rev__title{order:2;display:block;margin:0;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 72;font-weight:700;text-transform:uppercase;font-size:var(--lg-fs-base);color:var(--lg-ink)}
.jdgm-widget .jdgm-rev__title:empty{display:none}
.jdgm-widget .jdgm-rev__body{order:3;margin:0!important;color:var(--lg-ink-70);max-width:64ch}
.jdgm-widget .jdgm-rev__body p{margin:0 0 6px}
.jdgm-widget .jdgm-rev__body p:last-child{margin-bottom:0}
.jdgm-widget .jdgm-rev__custom-form{order:3;margin:0!important}
.jdgm-widget .jdgm-rev__custom-form:not(:has(*)){display:none!important}
.jdgm-widget .jdgm-row-profile{order:4;display:block;margin:0!important;padding-top:4px}
.jdgm-widget .jdgm-rev__author-wrapper{display:inline!important;margin:0!important;width:auto!important;max-width:none!important;white-space:nowrap}
.jdgm-widget .jdgm-row-profile{width:auto!important;max-width:none!important}
.jdgm-widget .jdgm-rev__author{color:var(--lg-ink-64);font-size:var(--lg-fs-sm);font-weight:400}
.jdgm-widget .jdgm-rev[data-verified-buyer="true"] .jdgm-rev__author::after{content:" · Verified buyer"}
.jdgm-widget .jdgm-row-product{order:5;margin:0}
.jdgm-widget .jdgm-rev__prod-link{display:inline-block;padding:2px 8px;border:1px solid var(--lg-rule);border-radius:var(--lg-r);background:var(--lg-page);font-size:var(--lg-fs-xs);font-weight:500;color:var(--lg-ink-64)!important;text-decoration:none}
.jdgm-widget .jdgm-rev__prod-info-wrapper{font-size:var(--lg-fs-xs);color:var(--lg-ink-64)}
.jdgm-widget .jdgm-all-reviews__footer,.jdgm-widget .jdgm-paginate{margin-top:8px}
"""

C["lgc-nf"] = """
.nf{text-align:center;padding:clamp(56px,10vw,140px) 0 clamp(40px,7vw,90px)}
.nf .lg-mags{width:clamp(120px,16vw,180px);margin:0 auto clamp(20px,3vw,28px);display:block}
.nf .lg-lede{max-width:48ch;margin-inline:auto}
.nf .btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:clamp(20px,3vw,28px)}
.pop{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--lg-gut);margin-top:clamp(40px,6vw,80px)}
@media (max-width:860px){.pop{grid-template-columns:repeat(2,minmax(0,1fr))}}
.pop a{display:block;color:inherit;text-decoration:none}
.pop .ph{display:block;aspect-ratio:4/5;border-radius:var(--lg-r-card);overflow:hidden;background:var(--lg-tile)}
.pop .ph img{width:100%;height:100%;object-fit:contain;padding:14px;mix-blend-mode:multiply}
.pop .nm{display:block;margin-top:10px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:700;text-transform:uppercase;font-size:14px}
.pop b{font-weight:600}
"""

C["lgc-search"] = """
.sbox{display:flex;gap:10px;align-items:center;border:1px solid var(--lg-rule);border-radius:var(--lg-r);padding:6px 6px 6px 16px;max-width:680px;margin-top:clamp(18px,2.5vw,26px)}
.sbox .ic{width:20px;height:20px;stroke-width:1.7;flex:none;color:var(--lg-ink-64)}
.sbox input[type=search]{flex:1;min-width:0;min-height:48px;border:0;background:none;color:var(--lg-ink);font:inherit;font-size:var(--lg-fs-body);outline:none}
.sbox button{flex:none}
.sugs{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.sugs a{display:inline-flex;align-items:center;min-height:40px;padding:0 12px;border:1px solid var(--lg-rule);border-radius:var(--lg-r);background:var(--lg-page);color:var(--lg-ink-64);text-decoration:none;font-size:var(--lg-fs-sm)}
.sugs a:hover{color:var(--lg-ink);border-color:var(--lg-ink)}
.res{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:var(--lg-gut);margin-top:clamp(24px,3vw,40px)}
@media (max-width:1100px){.res{grid-template-columns:repeat(3,minmax(0,1fr))}}
@media (max-width:820px){.res{grid-template-columns:repeat(2,minmax(0,1fr))}}
.r{display:block;color:inherit;text-decoration:none}
.r .ph{display:block;aspect-ratio:4/5;border-radius:var(--lg-r-card);overflow:hidden;background:var(--lg-tile)}
.r .ph img{width:100%;height:100%;object-fit:contain;padding:14px;mix-blend-mode:multiply}
.r .nm{display:block;margin-top:10px;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:700;text-transform:uppercase;font-size:14px;line-height:1.15}
.r b{display:block;margin-top:3px;font-weight:600}
.r .kind{display:block;margin-top:2px;color:var(--lg-ink-64);font-size:var(--lg-fs-sm)}
.none{padding:clamp(32px,6vw,72px) 0;text-align:center;color:var(--lg-ink-64)}
.texts{margin-top:clamp(32px,4vw,56px);max-width:860px}
.texts h2{margin:0 0 6px}
.texts ul{list-style:none;margin:0;padding:0}
.texts li{border-top:1px solid var(--lg-rule)}
.tx{display:flex;gap:16px;align-items:flex-start;padding:16px 0;color:inherit;text-decoration:none}
.tx-ph{flex:none;width:120px;aspect-ratio:3/2;border-radius:var(--lg-r);overflow:hidden;background:var(--lg-tile)}
.tx-ph img{width:100%;height:100%;object-fit:cover;display:block}
.tx-bd{display:flex;flex-direction:column;gap:3px;min-width:0}
.tx .kind{color:var(--lg-ink-64);font-size:var(--lg-fs-xs);text-transform:uppercase;letter-spacing:.08em}
.tx b{font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 70;font-weight:700;text-transform:uppercase;font-size:var(--lg-fs-base);color:var(--lg-ink)}
.tx:hover b{text-decoration:underline;text-decoration-color:var(--lg-gold);text-underline-offset:4px}
.tx .ex{color:var(--lg-ink-70);font-size:var(--lg-fs-sm)}
.none a{color:var(--lg-ink);text-decoration:none;font-family:'Archivo',sans-serif;font-variation-settings:'wdth' 76;font-weight:700;text-transform:uppercase;letter-spacing:.06em;font-size:var(--lg-fs-sm);border-bottom:2px solid var(--lg-gold);padding-bottom:4px}
.count{margin-top:clamp(20px,3vw,28px);color:var(--lg-ink-64);font-size:var(--lg-fs-sm)}
.sbox input[type=search]::-webkit-search-cancel-button{cursor:pointer}
"""


def main():
    parts = ["/* Group 70, content pages. Built by tools/theme/css_content.py: do not edit here. */"]
    for cls, css in C.items():
        parts.append(f"/* .{cls} */\n" + scope_css(tighten(css), cls))
    open(OUT, "w", encoding="utf-8").write("\n".join(parts) + "\n")
    print(OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
