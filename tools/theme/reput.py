"""Re-PUT changed theme files to their existing staged URLs (valid 7 days), then
print themeFilesUpsert variables for them.
    python tools/theme/reput.py <staged result json> <root> path [path ...]
"""
import json, sys, requests
from urllib.parse import urlparse, unquote
res, root, paths = sys.argv[1], sys.argv[2], sys.argv[3:]
T = {unquote(urlparse(t["resourceUrl"]).path.rsplit("/", 1)[1]).replace("__", "/"): t for t in json.load(open(res, encoding="utf-8"))["data"]["stagedUploadsCreate"]["stagedTargets"]}
MT = {"liquid": "text/plain", "json": "application/json", "css": "text/css", "js": "application/javascript", "webp": "image/webp"}
files = []
for p in paths:
    t = T[p]
    r = requests.put(t["url"], data=open(root + "/" + p, "rb").read(), headers={"Content-Type": MT[p.rsplit(".", 1)[1]]}, timeout=60)
    assert r.status_code == 200, (p, r.status_code, r.text[:200])
    files.append({"filename": p, "body": {"type": "URL", "value": t["resourceUrl"]}})
print(json.dumps({"files": files}, separators=(",", ":")))
