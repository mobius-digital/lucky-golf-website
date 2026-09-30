"""Generate theme snippets that come from files: the logo SVG and the Lucide icons.
    python tools/theme/gen_snippets.py
"""
import os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
T = os.path.join(ROOT, "theme")
sprite = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf-8").read()
SYM = {m.group(1): (m.group(2), m.group(3)) for m in
       re.finditer(r'<symbol[^>]*id="([^"]+)"[^>]*viewBox="([^"]+)"[^>]*>(.*?)</symbol>', sprite, re.S)}
vb, inner = SYM["lg-lucky"]
inner = re.sub(r"\s+", " ", inner).strip()
open(os.path.join(T, "snippets", "lg-logo.liquid"), "w", encoding="utf-8").write(
    "{%- comment -%} The Lucky wordmark. {% render 'lg-logo' %} {%- endcomment -%}\n"
    f'<svg viewBox="{vb}" fill="currentColor" fill-rule="nonzero" role="img" aria-label="Lucky Golf">{inner}</svg>')
icons = []
for f in sorted(os.listdir(os.path.join(ROOT, "v9", "src", "icons"))):
    name = f[:-4]
    svg = open(os.path.join(ROOT, "v9", "src", "icons", f), encoding="utf-8").read()
    svg = re.sub(r"<!--.*?-->", "", svg, flags=re.S).strip()
    svg = re.sub(r"\s+", " ", svg).replace('class="lucide lucide-' + name + '"', 'class="ic" aria-hidden="true"')
    icons.append(f"{{%- when '{name}' -%}}{svg}")
open(os.path.join(T, "snippets", "lg-icon.liquid"), "w", encoding="utf-8").write(
    "{%- comment -%} A Lucide icon (lucide-static 0.460.0, ISC). {% render 'lg-icon', name: 'star' %} {%- endcomment -%}\n"
    "{%- case name -%}" + "".join(icons) + "{%- endcase -%}")
for a in ["lucky.css", "lucky.js", "lucky-contour-day.webp", "lucky-contour-tw.webp"]:
    shutil.copy(os.path.join(ROOT, "shopify", "assets", a), os.path.join(T, "assets", a))
print("ok", len(icons), "icons")
