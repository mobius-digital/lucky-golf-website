"""Write theme JSON templates / section groups from every tools/theme/templates_*.py module (dict T).

    python tools/theme/build_templates.py
"""
import glob, importlib, json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
n = 0
only = sys.argv[1:]  # e.g. "home club": build just those groups
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "templates_*.py"))):
    g = os.path.basename(f)[len("templates_"):-3]
    if only and g not in only:
        continue
    try:
        mod = importlib.import_module(os.path.basename(f)[:-3])
    except Exception as e:
        print("SKIPPED", g, "->", e)
        continue
    for path, data in mod.T.items():
        p = os.path.join(ROOT, "theme", path)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        json.dump(data, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        n += 1
print(n, "templates written")
