"""Screenshot the approved v9 page and its Shopify build side by side.

    python tools/theme/compare.py home "/pages/about?view=lucky-home" [--w 1440] [--h 9000]

Writes _ref/compare/<name>-<w>.png (approved left, Shopify right), scaled to 1600px wide.
Uses headless Chrome; the Shopify URL gets the build theme's preview_theme_id.
"""
import argparse, os, subprocess, tempfile
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
THEME = "171555127573"


def shot(url, w, h, out):
    prof = tempfile.mkdtemp()
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}",
                    f"--window-size={w},{h}", "--virtual-time-budget=15000", f"--screenshot={out}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("path")
    ap.add_argument("--w", type=int, default=1440)
    ap.add_argument("--h", type=int, default=9000)
    a = ap.parse_args()
    out = os.path.join(ROOT, "_ref", "compare")
    os.makedirs(out, exist_ok=True)
    left = os.path.join(out, f"{a.page}-v9.png")
    right = os.path.join(out, f"{a.page}-shop.png")
    shot("file:///" + os.path.join(ROOT, "v9", "out", "after", a.page + ".html").replace("\\", "/"), a.w, a.h, left)
    sep = "&" if "?" in a.path else "?"
    shot(f"https://www.luckygolf.com{a.path}{sep}preview_theme_id={THEME}", a.w, a.h, right)
    L, R = Image.open(left), Image.open(right)
    W = L.width + R.width + 20
    c = Image.new("RGB", (W, max(L.height, R.height)), "white")
    c.paste(L, (0, 0))
    c.paste(R, (L.width + 20, 0))
    s = 1600 / W
    c = c.resize((1600, int(c.height * s)))
    final = os.path.join(out, f"{a.page}-{a.w}.png")
    c.save(final)
    # also split into readable slices
    for i in range(0, c.height, 1400):
        c.crop((0, i, 1600, min(c.height, i + 1400))).save(final.replace(".png", f"-{i // 1400}.png"))
    print(final, c.size)


if __name__ == "__main__":
    main()
