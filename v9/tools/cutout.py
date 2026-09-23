"""Cut a product off its studio background.

Shopify's pack shots sit on a flat sheet with a soft edge. Take the median
colour of the outer frame, keep every pixel far enough from it, feather the
edge a little, crop to what's left. Same method that made the polo cutouts.

    python v9/tools/cutout.py <in.webp> <out.webp> [tolerance]
"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def cut(src, dst, tol=34):
    im = Image.open(src).convert("RGB")
    a = np.asarray(im).astype(np.int16)
    h, w, _ = a.shape
    frame = np.concatenate([
        a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3),
        a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3),
    ])
    bg = np.median(frame, axis=0)
    d = np.sqrt(((a - bg) ** 2).sum(axis=2))
    m = np.clip((d - tol) * 14, 0, 255).astype(np.uint8)
    mask = Image.fromarray(m).filter(ImageFilter.GaussianBlur(1.2))
    out = im.convert("RGBA")
    out.putalpha(mask)
    bb = out.getbbox()
    if bb:
        out = out.crop(bb)
    out.save(dst, quality=90)
    return bg.tolist(), out.size


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    tol = int(sys.argv[3]) if len(sys.argv) > 3 else 34
    print(src, "->", dst, cut(src, dst, tol))
