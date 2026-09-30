"""Print stagedUploadsCreate input for theme files (paths relative to a root dir).
    python tools/theme/stage_input.py theme [path ...]   (no paths = every file)
Staged names are the path with / -> __ so tools/shopify_stage_put.py can map them back.
"""
import json, os, sys
root = sys.argv[1]
paths = sys.argv[2:] or [os.path.relpath(os.path.join(d, f), root).replace("\\", "/") for d, _, fs in os.walk(root) for f in fs]
paths = [p for p in paths if not p.startswith("css/")]
MT = {"liquid": "text/plain", "json": "application/json", "css": "text/css", "js": "application/javascript", "webp": "image/webp", "svg": "image/svg+xml", "png": "image/png"}
print(json.dumps([{"resource": "FILE", "filename": p.replace("/", "__"), "mimeType": MT.get(p.rsplit(".", 1)[1], "text/plain"), "httpMethod": "PUT"} for p in sorted(paths)], separators=(",", ":")))
print(len(paths), file=sys.stderr)
