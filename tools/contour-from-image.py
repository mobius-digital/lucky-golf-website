"""Turn a contour-map image (e.g. from ChatGPT: dark lines on white) into the
two Lucky contour files, coloured for each ground, with a see-through
background so they sit on any section.

  python tools/contour-from-image.py design/img/contour-source.png

Out: shopify/assets/lucky-contour-day.webp (ink lines, gold index lines kept
gold if the source has colour) and lucky-contour-tw.webp (cream lines).
Then point --lg-contour-day / --lg-contour-tw at the .webp files instead of
the .svg ones. Everything else (the random spot per section) stays the same.
"""
import sys
from PIL import Image, ImageOps

src = sys.argv[1] if len(sys.argv) > 1 else 'design/img/contour-source.png'
OUT = 'shopify/assets/'
im = Image.open(src).convert('RGB')
W = 2400
if im.width != W:
    im = im.resize((W, round(im.height * W / im.width)), Image.LANCZOS)

# line strength = how dark each pixel is against the white paper
grey = ImageOps.autocontrast(ImageOps.grayscale(im), cutoff=1)
ink = ImageOps.invert(grey)                       # lines -> bright
ink = ink.point(lambda v: 0 if v < 18 else min(255, int((v - 18) * 1.25)))  # drop paper grain

def paint(rgb, strength):
    a = ink.point(lambda v: int(v * strength))
    layer = Image.new('RGBA', im.size, rgb + (0,))
    layer.putalpha(a)
    return layer

paint((23, 20, 15), .30).save(OUT + 'lucky-contour-day.webp', 'WEBP', quality=90, method=6)
paint((244, 243, 240), .30).save(OUT + 'lucky-contour-tw.webp', 'WEBP', quality=90, method=6)
print('wrote', OUT + 'lucky-contour-day.webp', 'and -tw.webp', im.size)
