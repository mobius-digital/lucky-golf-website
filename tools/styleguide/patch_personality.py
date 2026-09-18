"""Styleguide: a real Personality section (status map + the picked designs),
review proximity in the reviews block, pinstripe noted as retired."""
import io
p = 'C:/Users/wetzl/Lucky Golf/Website/tools/styleguide/template.html'
s = io.open(p, encoding='utf-8').read()
a = s.index('  <!-- YARDAGE -->')
b = s.index('  <section class="lg-band is-photo"')
NEW = io.open('C:/Users/wetzl/Lucky Golf/Website/tools/styleguide/personality.html', encoding='utf-8').read()
s = s[:a] + NEW + s[b:]
s = s.replace('<a href="#s-yardage">Yardage</a>', '<a href="#s-yardage">Personality</a>')
s = s.replace('<div><b class="lg-num">4</b><span>Yardage. Only where a number is real.</span></div>',
              '<div><b class="lg-num">4</b><span>Yardage, the golf instruments. Only where a number is real.</span></div>')
old = "  paint();\n\n  /* Mags on demand */"
assert old in s
s = s.replace(old, "  paint();\n  Lucky.proximity(document.getElementById('sg-prox'), { counts: { 5: 585, 4: 37, 3: 12, 2: 5, 1: 11 }, label: '650 reviews on the Carver 01 Gold' });\n\n  /* Mags on demand */")
s = s.replace("<li>No two dark bands in a row. No dark page outside an event.</li>",
              "<li>No two dark bands in a row. No dark page outside an event. No pinstripe: it's retired.</li>")
io.open(p, 'w', encoding='utf-8').write(s)

b2 = 'C:/Users/wetzl/Lucky Golf/Website/tools/styleguide/build.cjs'
t = io.open(b2, encoding='utf-8').read()
if 'gwp-contour-day.svg' not in t:
    t = t.replace("  'mags-bag-light.webp': 'handoff/img/mags-bag-light.webp',\n",
                  "  'mags-bag-light.webp': 'handoff/img/mags-bag-light.webp',\n  'gwp-contour-day.svg': 'shopify/assets/gwp-contour-day.svg',\n")
    io.open(b2, 'w', encoding='utf-8').write(t)
print('ok')
