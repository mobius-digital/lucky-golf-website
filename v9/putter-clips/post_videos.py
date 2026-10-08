"""POST the four putter clips to Shopify's staged video targets (multipart form, fields first, file last).
Reads the newest stagedUploadsCreate result from this session's log (tools/theme/staged_from_log.py)."""
import json, os, subprocess, sys, requests
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
out = os.path.join(HERE, "_staged_videos.json")
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "theme", "staged_from_log.py"), "lg-putter-mallet-3-wings", out], check=True)
targets = json.load(open(out))["data"]["stagedUploadsCreate"]["stagedTargets"]
done = []
for t in targets:
    name = t["resourceUrl"].split("/")[-1].split("?")[0]
    fields = {p["name"]: p["value"] for p in t["parameters"]}
    with open(os.path.join(HERE, name), "rb") as fh:
        r = requests.post(t["url"], data=fields, files={"file": (name, fh, "video/mp4")}, timeout=300)
    print(name, r.status_code, r.text[:120])
    done.append({"originalSource": t["resourceUrl"], "contentType": "VIDEO", "alt": name.replace("lg-putter-", "").replace(".mp4", "")})
print(json.dumps({"files": done}))
