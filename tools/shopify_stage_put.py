"""PUT local files to Shopify staged-upload targets.

    python tools/shopify_stage_put.py <stagedUploadsCreate result file> <local dir> [strip-prefix]

The result file is the saved JSON of a stagedUploadsCreate mutation. Each
target's filename (the last path part of resourceUrl) maps to a local file in
<local dir>, after removing strip-prefix (e.g. "lg-" or "theme__"; "__" in a
staged name stands for "/"). Prints resourceUrls as JSON for the next mutation
(fileCreate or themeFilesUpsert), keyed by the local relative path.
"""
import json, mimetypes, os, sys
from urllib.parse import urlparse, unquote

import requests

res, root = sys.argv[1], sys.argv[2]
strip = sys.argv[3] if len(sys.argv) > 3 else ""
d = json.load(open(res, encoding="utf-8"))
targets = d["data"]["stagedUploadsCreate"]["stagedTargets"]
out, bad = {}, []
for t in targets:
    name = unquote(urlparse(t["resourceUrl"]).path.rsplit("/", 1)[1])
    rel = name[len(strip):] if strip and name.startswith(strip) else name
    rel = rel.replace("__", "/")
    path = os.path.join(root, rel)
    ctype = mimetypes.guess_type(rel)[0] or "application/octet-stream"
    if rel.endswith(".webp"):
        ctype = "image/webp"
    if rel.endswith((".liquid", ".json", ".css", ".js", ".svg")):
        ctype = {"liquid": "text/plain", "json": "application/json", "css": "text/css", "js": "application/javascript", "svg": "image/svg+xml"}[rel.rsplit(".", 1)[1]]
    with open(path, "rb") as f:
        r = requests.put(t["url"], data=f.read(), headers={"Content-Type": ctype}, timeout=120)
    if r.status_code != 200:
        bad.append((rel, r.status_code, r.text[:200]))
    out[rel] = t["resourceUrl"]
print(json.dumps(out))
for b in bad:
    print("FAILED", b, file=sys.stderr)
print(f"{len(out) - len(bad)} ok, {len(bad)} failed", file=sys.stderr)
