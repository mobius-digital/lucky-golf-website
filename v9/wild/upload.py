"""POST each downloaded reel to its Shopify staged video target (targets pulled from the session log)."""
import json, os, re, subprocess, sys

LOG = r"C:\Users\wetzl\.claude\projects\C--Users-wetzl-Lucky-Golf-Website\afab062b-faee-4643-a07f-84c93ce5040c.jsonl"
HERE = os.path.dirname(os.path.abspath(__file__))

found = None
for line in open(LOG, encoding="utf-8"):
    if "lucky-wild-C-8yM2RAro0" not in line or "stagedTargets" not in line:
        continue
    for m in re.finditer(r'\{\\*"data\\*":\{\\*"stagedUploadsCreate.*?userErrors\\*":\[\]\}\}\}', line):
        s = m.group(0)
        while '\\"' in s:
            s = s.encode().decode("unicode_escape")
        try:
            d = json.loads(s)
            if d["data"]["stagedUploadsCreate"]["stagedTargets"][0]["parameters"]:
                found = d
        except Exception:
            pass
targets = found["data"]["stagedUploadsCreate"]["stagedTargets"]
out = {}
for t in targets:
    name = re.search(r"lucky-wild-(.+?)\.mp4", t["resourceUrl"]).group(1)
    args = ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-X", "POST", t["url"]]
    for p in t["parameters"]:
        args += ["-F", f"{p['name']}={p['value']}"]
    args += ["-F", f"file=@{os.path.join(HERE, 'files', name + '.mp4')};type=video/mp4"]
    code = subprocess.run(args, capture_output=True, text=True).stdout
    out[name] = t["resourceUrl"]
    print(name, code)
json.dump(out, open(os.path.join(HERE, "resource_urls.json"), "w"), indent=1)
