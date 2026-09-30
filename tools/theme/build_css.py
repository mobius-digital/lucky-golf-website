"""Build theme/assets/lucky-site.css: the v9 site layer + each approved page's own
<style>, scoped to that page's template so pages can't leak into each other.

    python tools/theme/build_css.py

The theme's <body> carries lg-t-<template name> and lg-t-<template suffix>, so a
page's rules are prefixed with that class (home -> .lg-t-index, the club
template -> .lg-t-club). Rules the theme itself needs live in theme/css/*.css
and are appended unscoped.
"""
import os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "v9", "src")
OUT = os.path.join(ROOT, "theme", "assets", "lucky-site.css")

# v9 page -> the body class of the template that renders it
# None = unscoped: Home's pieces became the shared sections, so its CSS is global.
PAGES = {
    "home.html": None,
}


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def scope_selectors(sel, scope):
    out = []
    for s in sel.split(","):
        s = s.strip()
        if not s:
            continue
        if s.startswith(":root") or s.startswith("html"):
            out.append(s)
        elif s.startswith("body"):
            out.append(re.sub(r"^body", "body." + scope, s, count=1))
        else:
            out.append("." + scope + " " + s)
    return ",".join(out)


def scope_css(css, scope):
    """Prefix every rule's selectors; recurse into @media/@supports; leave @keyframes/@font-face."""
    css = strip_comments(css)
    out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            out.append(css[i:])
            break
        head = css[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{":
                depth += 1
            elif css[k] == "}":
                depth -= 1
            k += 1
        body = css[j + 1:k - 1]
        if head.startswith("@media") or head.startswith("@supports") or head.startswith("@container"):
            out.append(head + "{" + scope_css(body, scope) + "}")
        elif head.startswith("@"):
            out.append(head + "{" + body + "}")
        else:
            out.append(scope_selectors(head, scope) + "{" + body.strip() + "}")
        i = k
    return "\n".join(out)


COLORS = {"#0B2E1F": "--lg-dark", "#C29A2B": "--lg-gold", "#8A6A1C": "--lg-gold-text", "#EDD27C": "--lg-gold-hi",
          "#17140F": "--lg-ink", "#06110B": "--lg-night"}


def tokenize(css):
    """Every page's hand-copied values become design-system tokens, so a change to lucky.css
    reaches every page (Cole, 2026-09-27: 'standardized to our design system ... instant').
    Radii: 3-4px -> tag, 5-6px -> control, 7-40px -> surface, pills (999px) -> tag. Brand hexes -> tokens
    (a hex that is already a var() fallback is left alone)."""
    def rad(m):
        v = int(m.group(2))
        if v >= 999:
            tok = "--lg-r-tag"
        elif 7 <= v <= 40:
            tok = "--lg-r-card"
        elif 5 <= v <= 6:
            tok = "--lg-r"
        elif 3 <= v <= 4:
            tok = "--lg-r-tag"
        else:
            return m.group(0)
        return m.group(1) + "var(" + tok + ")"
    css = re.sub(r"(border-radius:\s*)(\d+)px(?=\s*[;}!])", rad, css)
    for hexv, tok in COLORS.items():
        css = re.sub(r"(?<![,\w-])" + hexv + r"(?![0-9a-fA-F])", "var(" + tok + ")", css, flags=re.I)
    return css


def page_style(name):
    html = open(os.path.join(SRC, name), encoding="utf-8").read()
    return "\n".join(re.findall(r"<style>(.*?)</style>", html, flags=re.S))


def main():
    site = open(os.path.join(SRC, "site.css"), encoding="utf-8").read()
    # preview-only bits
    site = re.sub(r"/\* ---- preview toast ---- \*/\n#pv-toast\{[^}]*\}\n", "", site)
    site = re.sub(r"\.cd-mock\{[^}]*\}\n", "", site)
    parts = ["/* Lucky theme site layer. Built by tools/theme/build_css.py: do not edit here. */", site]
    for name, scope in PAGES.items():
        css = page_style(name)
        label = "scoped to ." + scope if scope else "shared"
        parts.append(f"/* ---- {name} ({label}) ---- */\n" + (scope_css(css, scope) if scope else strip_comments(css)))
    extra = os.path.join(ROOT, "theme", "css")
    for f in sorted(os.listdir(extra)) if os.path.isdir(extra) else []:
        parts.append(f"/* ---- theme/css/{f} ---- */\n" + open(os.path.join(extra, f), encoding="utf-8").read())
    # fonts go through --lg-font (theme setting "Google Font family"), falling back to Archivo
    open(OUT, "w", encoding="utf-8").write(tokenize("\n".join(parts)).replace("font-family:'Archivo'", "font-family:var(--lg-font,'Archivo')"))
    print("lucky-site.css", os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
