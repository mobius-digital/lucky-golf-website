"""
Render reference PDFs to PNGs so they can actually be looked at.

The Read tool cannot open these PDFs directly (no pdftoppm on this machine) and
the pdf-viewer MCP has no allowed directories configured. PyMuPDF IS installed,
so this is the way in. Do not waste time rediscovering that.

Usage, from the Website folder:

    python tools/render-ref.py "Takomo/Takomo PDP 1"
    python tools/render-ref.py "Dartee/Dartee Our Story" --pages 1-3 --scale 2.0
    python tools/render-ref.py --list

Output lands in  _ref/<slug>/page-NN.png  which is gitignored.
Then just Read those PNGs.
"""
import argparse
import os
import re
import sys

REF_ROOT = r"C:\Users\wetzl\Downloads\Good References"
OUT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_ref")


def find_pdfs():
    hits = []
    for base, _dirs, files in os.walk(REF_ROOT):
        for f in files:
            if f.lower().endswith(".pdf"):
                full = os.path.join(base, f)
                hits.append((os.path.relpath(full, REF_ROOT).replace("\\", "/"), full))
    return sorted(hits)


def resolve(name):
    name = name.lower().replace("\\", "/").removesuffix(".pdf")
    cands = [(rel, full) for rel, full in find_pdfs()
             if name in rel.lower().removesuffix(".pdf")]
    if not cands:
        sys.exit("No PDF matching %r.\nRun --list to see what's there." % name)
    if len(cands) > 1:
        exact = [c for c in cands if c[0].lower().removesuffix(".pdf").endswith(name)]
        if len(exact) == 1:
            return exact[0]
        sys.exit("Ambiguous %r, matches:\n  " % name + "\n  ".join(r for r, _ in cands))
    return cands[0]


def parse_pages(spec, n):
    if not spec:
        return list(range(n))
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out += list(range(int(a) - 1, int(b)))
        else:
            out.append(int(part) - 1)
    return [p for p in out if 0 <= p < n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", nargs="?", help="partial path, e.g. 'Takomo/Takomo PDP 1'")
    ap.add_argument("--pages", help="1-based, e.g. '1-3' or '2,5'. Default: all")
    ap.add_argument("--scale", type=float, default=1.6, help="render scale, default 1.6")
    ap.add_argument("--list", action="store_true", help="list available PDFs")
    a = ap.parse_args()

    if a.list or not a.pdf:
        for rel, _ in find_pdfs():
            print(rel)
        return

    import fitz  # PyMuPDF

    rel, full = resolve(a.pdf)
    doc = fitz.open(full)
    slug = re.sub(r"[^a-z0-9]+", "-", rel.removesuffix(".pdf").lower()).strip("-")
    outdir = os.path.normpath(os.path.join(OUT_ROOT, slug))
    os.makedirs(outdir, exist_ok=True)

    pages = parse_pages(a.pages, doc.page_count)
    print("%s -> %d page(s) of %d" % (rel, len(pages), doc.page_count))
    for i in pages:
        pix = doc[i].get_pixmap(matrix=fitz.Matrix(a.scale, a.scale))
        path = os.path.join(outdir, "page-%02d.png" % (i + 1))
        pix.save(path)
        print("  %s  %dx%d  %dKB" % (path, pix.width, pix.height, os.path.getsize(path) // 1024))


if __name__ == "__main__":
    main()
