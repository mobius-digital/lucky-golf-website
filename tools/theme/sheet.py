"""Contact sheet of build-theme pages: headless screenshots, N per image, for a quick review.
    python tools/theme/sheet.py <name> <w> <h> <path> [<path> ...]
Writes _ref/sheet/<name>.png (pages side by side, each scaled to 480px wide).
"""
import os, subprocess, sys, tempfile
from PIL import Image
C = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
O = os.path.join(ROOT, "_ref", "sheet"); os.makedirs(O, exist_ok=True)
name, w, h, paths = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
ims = []
for i, p in enumerate(paths):
    sep = "&" if "?" in p else "?"
    out = os.path.join(O, f"{name}-{i}.png")
    subprocess.run([C, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={tempfile.mkdtemp()}", f"--window-size={w},{h}",
                    "--virtual-time-budget=14000", "--screenshot=" + out, f"https://www.luckygolf.com{p}{sep}preview_theme_id=171555127573&v=s{i}"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150)
    if not os.path.exists(out):
        print("NO SHOT", p); continue
    im = Image.open(out).convert("RGB"); s = 480 / im.width
    ims.append(im.resize((480, int(im.height * s))))
H = max(i.height for i in ims)
c = Image.new("RGB", (490 * len(ims), H), "white")
for i, im in enumerate(ims):
    c.paste(im, (i * 490, 0))
c.save(os.path.join(O, name + ".png"))
print(os.path.join(O, name + ".png"), c.size)
