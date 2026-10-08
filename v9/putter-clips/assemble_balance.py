"""Cut the Blade 'balanced' film the way Takomo's Lumo clip is cut:
  A   top view, gold -> X-ray, crosshairs lock on the centre of gravity   (+ label)
  A'  X-ray back to gold (A reversed, quick)
  B   camera swings down and around to the low front view
  C   front view -> X-ray, orange shaft line, centre of gravity, the gap  (+ labels)
Labels: tiny caps in Archivo with a thin pointer line that draws in, like Takomo's 'CENTER OF GRAVITY'.
Output: blade-balance.mp4 (1280x720, 30 fps, silent, loops)."""
import os, numpy as np, imageio.v2 as iio
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
W, HH, FPS = 1280, 720, 30
font = ImageFont.truetype(os.path.join(H, 'fonts', 'Archivo.ttf'), 15)
try: font.set_variation_by_name('SemiBold')
except Exception: pass

def frames(name):
    r = iio.get_reader(os.path.join(H, name)); fs = [np.asarray(Image.fromarray(f).resize((W, HH), Image.LANCZOS)) for f in r]; r.close(); return fs

def retime(fs, src_fps, speed, a=0.0, b=None, reverse=False):
    n = len(fs); b = n / src_fps if b is None else b
    dur = (b - a) / speed; out = []
    for i in range(int(round(dur * FPS))):
        t = a + (i / FPS) * speed
        if reverse: t = b - (i / FPS) * speed
        out.append(fs[max(0, min(n - 1, int(round(t * src_fps))))])
    return out

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

def label(img, pt, txt, k, side='right', dx=150, dy=-70):
    """pointer from pt to an elbow, then text. k in 0..1 animates: line draws (0-.6), text fades in (.4-1)."""
    if k <= 0: return img
    im = Image.fromarray(img).convert('RGBA'); ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    x0, y0 = pt[0] * W, pt[1] * HH; x1, y1 = x0 + (dx if side == 'right' else -dx) * 0.55, y0 + dy
    x2 = x1 + (dx if side == 'right' else -dx) * 0.45
    L = ease(k / 0.6); seg1 = min(1, L * 2); seg2 = max(0, L * 2 - 1)
    col = (245, 236, 210, 235)
    d.line([(x0, y0), (x0 + (x1 - x0) * seg1, y0 + (y1 - y0) * seg1)], fill=col, width=1)
    if seg2 > 0: d.line([(x1, y1), (x1 + (x2 - x1) * seg2, y1)], fill=col, width=1)
    d.ellipse([x0 - 2.5, y0 - 2.5, x0 + 2.5, y0 + 2.5], fill=col)
    a = int(255 * ease((k - 0.4) / 0.6))
    if a > 0:
        tw = d.textlength(txt, font=font) + (len(txt) - 1) * 2.2
        tx = x2 + 8 if side == 'right' else x2 - 8 - tw; ty = y1 - 10
        x = tx
        for ch in txt:  # letter-spaced caps
            d.text((x, ty), ch, font=font, fill=(245, 236, 210, a)); x += d.textlength(ch, font=font) + 2.2
    return np.asarray(Image.alpha_composite(im, ov).convert('RGB'))

A, B, C = frames('blade-xray.mp4'), frames('seq-b-swing.mp4'), frames('seq-c-xray.mp4')
SRC = 24
COG_TOP = (0.489, 0.42)                       # crosshair centre, top view (read off blade-xray-end.png)
COG_FRONT, SHAFT = (0.434, 0.606), (0.647, 0.26)   # front view (read off blade-face-xray.png)

out = []
seg = retime(A, SRC, 1.25)                     # A
lab_start = len(seg) - int(1.1 * FPS)
for i, f in enumerate(seg):
    out.append(label(f, COG_TOP, 'CENTER OF GRAVITY', (i - lab_start) / (0.7 * FPS)))
hold = out[-1]; out += [hold] * int(1.0 * FPS)
rev = retime(A, SRC, 2.0, a=3.4, reverse=True)  # A' back to gold, label fades
for i, f in enumerate(rev):
    out.append(label(f, COG_TOP, 'CENTER OF GRAVITY', 1 - i / 6) if i < 6 else f)
out += retime(B, SRC, 1.3)                       # B swing
segc = retime(C, SRC, 1.0)                       # C front X-ray
ls = len(segc) - int(1.2 * FPS)
for i, f in enumerate(segc):
    k = (i - ls) / (0.7 * FPS)
    f = label(f, COG_FRONT, 'CENTER OF GRAVITY', k, side='left', dx=170, dy=60)
    f = label(f, SHAFT, 'SHAFT AXIS', k - 0.35, side='right', dx=130, dy=-40)
    out.append(f)
last = out[-1]; out += [last] * int(1.6 * FPS)

wr = iio.get_writer(os.path.join(H, 'blade-balance.mp4'), fps=FPS, codec='libx264', quality=8, macro_block_size=8, ffmpeg_params=['-pix_fmt', 'yuv420p', '-movflags', '+faststart'])
for f in out: wr.append_data(f)
wr.close()
print('frames', len(out), 'seconds', round(len(out) / FPS, 1))
