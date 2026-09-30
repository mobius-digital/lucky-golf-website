"""Pull the newest stagedUploadsCreate result that mentions NAME out of this session's log into OUT,
so reput.py can use it. python tools/theme/staged_from_log.py NAME OUT"""
import json, sys, glob, os
name, out = sys.argv[1], sys.argv[2]
logs = sorted(glob.glob(os.path.expanduser(r"~/.claude/projects/C--Users-wetzl-Lucky-Golf-Website/*.jsonl")), key=os.path.getmtime)
found = None
for line in open(logs[-1], encoding="utf-8"):
    if name not in line or "tool_result" not in line or "stagedTargets" not in line:
        continue
    for c in json.loads(line).get("message", {}).get("content", []):
        if not isinstance(c, dict) or c.get("type") != "tool_result":
            continue
        t = c["content"] if isinstance(c["content"], str) else c["content"][0].get("text", "")
        try:
            d = json.loads(t)
            if any(name in x["resourceUrl"] for x in d["data"]["stagedUploadsCreate"]["stagedTargets"]):
                found = d
        except Exception:
            pass
json.dump(found, open(out, "w"))
print(len(found["data"]["stagedUploadsCreate"]["stagedTargets"]), "targets")
