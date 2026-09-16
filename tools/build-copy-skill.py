"""
Rebuild the lucky-golf-copy skill zip from the reference docs in this repo.

WHY THIS EXISTS
---------------
The skill's four reference docs are copies. The originals live in the repo
root and get edited there (new product specs, a tone-guide revision). Before
this script, keeping the skill in step meant remembering to copy four files
by hand, and the skill silently drifted: it was still shipping How We Write
v6 and Product Guide v1.1 weeks after v8.1 and v1.8 landed.

So: edit the repo doc, run this, upload the zip. One command, no drift.

    python tools/build-copy-skill.py

It also refuses to build a zip that Claude will reject, because that has
already cost a round trip: Windows zips write backslash paths, and the
uploader rejects them with a misleading "must include a SKILL.md" error.
"""
import io
import os
import re
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SKILL = os.path.join(ROOT, ".claude", "skills", "lucky-golf-copy")
OUT = os.path.join(ROOT, "lucky-golf-copy.zip")

# repo doc  ->  name it takes inside the skill
DOCS = {
    "references-how-we-write-v8.1.md": "how-we-write.md",
    "references-product-guide-v1.8.md": "product-reference-guide.md",
    "references-spec-to-benefit-v1.0.md": "spec-to-benefit.md",
    "references-culture-v2.md": "golf-culture.md",
}
# written by hand, has no repo original
SKILL_OWNED = {"prompt-patterns.md"}


def sync():
    """Copy the repo originals over the skill's copies."""
    refs = os.path.join(SKILL, "references")
    os.makedirs(refs, exist_ok=True)
    for src, dst in DOCS.items():
        p = os.path.join(ROOT, src)
        if not os.path.exists(p):
            sys.exit("missing reference doc: %s\n"
                     "If it was renamed (a version bump renames the file), "
                     "update DOCS at the top of this script." % src)
        text = io.open(p, encoding="utf8").read()
        io.open(os.path.join(refs, dst), "w", encoding="utf8",
                newline="\n").write(text)
        ver = next((l.strip() for l in text.splitlines() if "Version" in l), "")
        print("  %-28s <- %-34s %s" % (dst, src, ver[:46]))


def check_skill_md(text):
    """The three things the uploader actually validates."""
    if text.startswith("﻿"):
        sys.exit("SKILL.md starts with a byte-order mark; strip it")
    if not text.startswith("---"):
        sys.exit("SKILL.md must open with the --- frontmatter block")
    fm = text.split("---")[1]
    if "name:" not in fm:
        sys.exit("SKILL.md frontmatter has no name:")
    m = re.search(r"description:(.*)", fm)
    if not m:
        sys.exit("SKILL.md frontmatter has no description:")
    n = len(m.group(1).strip())
    if n > 1024:
        sys.exit("description is %d characters; the limit is 1024" % n)
    return n


def build():
    print("syncing reference docs:")
    sync()

    files = {}
    for dirpath, _, names in os.walk(SKILL):
        for name in names:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, os.path.dirname(SKILL))
            # forward slashes, always: Windows backslash paths in a zip make
            # the uploader report a missing SKILL.md
            files[rel.replace(os.sep, "/")] = open(full, "rb").read()

    key = "lucky-golf-copy/SKILL.md"
    if key not in files:
        sys.exit("no SKILL.md found under %s" % SKILL)
    chars = check_skill_md(files[key].decode("utf8"))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in sorted(files.items()):
            z.writestr(name, data)

    raw = open(OUT, "rb").read()
    assert (b"lucky-golf-copy" + bytes([92])) not in raw, "backslash paths got in"

    print("\nbuilt %s" % os.path.basename(OUT))
    print("  %d files, description %d chars" % (len(files), chars))
    for n in sorted(files):
        print("   ", n)
    print("\nNow upload it: claude.ai -> Settings -> Capabilities -> Skills")


if __name__ == "__main__":
    build()
