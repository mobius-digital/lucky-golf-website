"""Write theme/sections/*.liquid from every tools/theme/sections_*.py spec module (dict S).

    python tools/theme/build_sections.py
"""
import glob, importlib, os, sys
sys.path.insert(0, os.path.dirname(__file__))
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "theme", "sections")
n = 0
only = sys.argv[1:]  # e.g. "home club": build just those groups
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "sections_*.py"))):
    g = os.path.basename(f)[len("sections_"):-3]
    if only and g not in only:
        continue
    try:
        mod = importlib.import_module(os.path.basename(f)[:-3])
    except Exception as e:
        print("SKIPPED", g, "->", e)
        continue
    for name, body in mod.S.items():
        open(os.path.join(OUT, name + ".liquid"), "w", encoding="utf-8").write(body)
        n += 1
print(n, "sections written")
