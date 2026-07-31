"""
Assemble each page from _src/ into a single-file, dependency-free NN-name.html.

    python tools/build.py            # build every page
    python tools/build.py pdp        # build one
    python tools/build.py --check    # build to memory, diff against what's on disk

The generated NN-*.html files stay self-contained on purpose — that is what
makes them easy to send and review. Never edit them directly; they are
overwritten. Source of truth is _src/ + _src-logo-symbols.svg.

Page order inside <body>:
    symbol sprite -> header -> page sections -> footer -> lightbox -> cart
CSS order: core.css -> page-NAME.css
JS  order: page-NAME.js (data first, so core can read it) -> core.js
"""
import argparse
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
SRC = os.path.join(ROOT, "_src")

# slug -> (output filename, <title>)
PAGES = {
    "home": ("01-home.html", "Lucky Golf — Home"),
    "pdp": ("02-pdp-lgw01.html", "Carver Gold Wedge · LGW01 — Lucky Golf"),
}

# The shared header links to #families / #gear, which only exist on the
# homepage. {{HOME}} resolves to nothing there and to the homepage's filename
# everywhere else, so the nav works from any page.
HOME_FILE = PAGES["home"][0]

SHELL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,100..900;1,62..125,100..900&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
<style>
{css}
</style>
</head>
<body>

{symbols}

{header}

{sections}

{footer}

{lightbox}

{cart}

<script>
{js}
</script>

</body>
</html>
"""


def read(rel, required=True):
    path = os.path.join(SRC, rel)
    if not os.path.exists(path):
        if required:
            sys.exit("missing source: _src/%s" % rel)
        return ""
    return open(path, encoding="utf8").read().rstrip("\n")


def build(slug):
    _out, title = PAGES[slug]
    symbols = open(os.path.join(ROOT, "_src-logo-symbols.svg"), encoding="utf8").read().rstrip("\n")

    host = read("partials/symbols-host.html")
    if "{{SYMBOLS}}" not in host:
        sys.exit("partials/symbols-host.html lost its {{SYMBOLS}} placeholder")
    host = host.replace("{{SYMBOLS}}", symbols)

    css = read("core.css") + "\n\n" + read("page-%s.css" % slug)
    js = read("page-%s.js" % slug, required=False)
    js = (js + "\n\n" if js else "") + read("core.js")

    header = read("partials/header.html").replace("{{HOME}}", "" if slug == "home" else HOME_FILE)

    return SHELL.format(
        title=title,
        css=css,
        symbols=host,
        header=header,
        sections=read("page-%s.html" % slug),
        footer=read("partials/footer.html"),
        lightbox=read("partials/lightbox.html"),
        cart=read("partials/cart.html"),
        js=js,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", nargs="*", help="page slugs; default all")
    ap.add_argument("--check", action="store_true",
                    help="do not write; report whether output differs from disk")
    a = ap.parse_args()

    slugs = a.pages or list(PAGES)
    bad = [s for s in slugs if s not in PAGES]
    if bad:
        sys.exit("unknown page(s): %s\nknown: %s" % (", ".join(bad), ", ".join(PAGES)))

    rc = 0
    for slug in slugs:
        out, _title = PAGES[slug]
        html = build(slug)
        path = os.path.join(ROOT, out)

        if a.check:
            old = open(path, encoding="utf8").read() if os.path.exists(path) else None
            if old is None:
                print("%-22s NEW (not on disk)" % out)
                rc = 1
            elif old == html:
                print("%-22s identical" % out)
            else:
                o, n = old.split("\n"), html.split("\n")
                print("%-22s DIFFERS  (%d lines on disk -> %d rebuilt)" % (out, len(o), len(n)))
                shown = 0
                for i in range(max(len(o), len(n))):
                    a_ = o[i] if i < len(o) else "<eof>"
                    b_ = n[i] if i < len(n) else "<eof>"
                    if a_ != b_:
                        print("   line %d\n     disk: %s\n     new : %s" % (i + 1, a_[:150], b_[:150]))
                        shown += 1
                        if shown >= 12:
                            print("   ... (more)")
                            break
                rc = 1
            continue

        with io.open(path, "w", encoding="utf8", newline="\n") as f:
            f.write(html)
        print("%-22s %6.1f KB" % (out, len(html.encode("utf8")) / 1024.0))

    return rc


if __name__ == "__main__":
    sys.exit(main())
