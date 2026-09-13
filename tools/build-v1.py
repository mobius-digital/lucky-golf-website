"""The site on the pre-redesign structure (2026-09-12). Cole: "I liked all the
pages a lot better... I just didn't like the color scheme." _v1/ is the
committed site as of 8d78d99 with the palette swapped (ink for green, a
neutral grey for the cream fields and wells). This runs that build and copies
every page over the v2 output EXCEPT the five club product pages, which stay
on the v2 club template Cole liked. Run AFTER tools/build.py."""
import os, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
V1 = os.path.join(ROOT, "_v1")
KEEP_V2 = {"02-pdp-lgw01.html", "20-product-lgw01-black.html", "20-product-lgp01-gold.html",
           "20-product-lgp02-gold.html", "20-product-lgh01.html"}
subprocess.check_call([sys.executable, os.path.join(V1, "tools", "build.py")], cwd=V1,
                      stdout=subprocess.DEVNULL)
n = 0
for f in sorted(os.listdir(V1)):
    if not f.endswith(".html"): continue
    if f not in KEEP_V2:
        # something on this machine (indexer or preview watcher) briefly holds
        # freshly written pages; a copy that fails with EINVAL succeeds a
        # moment later, so retry rather than die
        for attempt in range(20):
            try:
                shutil.copyfile(os.path.join(V1, f), os.path.join(ROOT, f)); break
            except OSError:
                if attempt == 19: raise
                time.sleep(0.5)
        n += 1
    os.remove(os.path.join(V1, f))
print("%d pages from _v1; %d club pages kept on v2" % (n, len(KEEP_V2)))
