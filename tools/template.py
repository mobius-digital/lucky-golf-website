"""
A very small Mustache-shaped template engine — enough for the PDP templates,
and no more.

    {{name}}                 insert a value
    {{#name}} ... {{/name}}  repeat per item if a list; render once if truthy;
                             skip entirely if falsy or absent
    {{^name}} ... {{/name}}  render only if falsy or absent
    {{! note }}              comment, dropped

WHY A TEMPLATE LANGUAGE AT ALL
------------------------------
Phase A made the buy box data-driven but the rest of the PDP was still LGW01's
prose sitting in markup. Forty-four product pages cannot each be a copy of that
file — the point of GAMEPLAN §2b is one template per product *type*, driven by
data, which is also what a Shopify theme does. Mustache's shape was chosen
because `{{#x}}…{{/x}}` maps almost directly onto Liquid's `{% for %}` and
`{% if %}`, so the templates hand over to a Shopify developer legibly.

DELIBERATE LIMITATIONS
----------------------
* **No escaping.** Every value here is authored copy from `_src/data/copy/`,
  written by us, and much of it contains intentional markup (`<em>`, links,
  `&mdash;`). This engine renders trusted content only. It must never be
  pointed at user input.
* **No dotted paths, no filters, no partials.** If a template needs one, the
  data is shaped wrong — flatten it in `build.py` instead. Keeping the engine
  dumb keeps the templates readable.
* Sections consume a **list, a dict, or a bare truthy value**. A dict pushes a
  scope; a list repeats and pushes each item; anything else truthy renders the
  block once without changing scope.

Inside a section, `{{.}}` is the current item — used for plain string lists.
Lookup walks the scope stack outward, so a loop can still reach page-level
values.
"""
import re

TAG = re.compile(r"\{\{([#^/!]?)\s*([^}]*?)\s*\}\}")

_MISSING = object()


class TemplateError(Exception):
    pass


def _lookup(stack, name):
    if name == ".":
        return stack[-1]
    for scope in reversed(stack):
        if isinstance(scope, dict) and name in scope:
            return scope[name]
    return _MISSING


def _truthy(v):
    return not (v is _MISSING or v is None or v is False or v == "" or v == [] or v == {})


def render(text, data, where="<template>"):
    """Render `text` with `data`. Raises TemplateError on an unclosed or
    mismatched section — a silently swallowed block is exactly the kind of
    invisible failure the build is supposed to catch."""
    out = []
    # stack of (kind, name, buffer-index) for open sections
    open_sections = []
    # when skipping, we still have to track nesting depth to find our /close
    pos = 0
    # Render is done by first parsing into a tree; simpler to reason about than
    # a streaming skip counter, and the templates are small.
    tokens = []
    for m in TAG.finditer(text):
        if m.start() > pos:
            tokens.append(("text", text[pos:m.start()]))
        sigil, name = m.group(1), m.group(2)
        if sigil == "!":
            pass
        elif sigil in ("#", "^"):
            tokens.append(("open" if sigil == "#" else "inv", name))
        elif sigil == "/":
            tokens.append(("close", name))
        else:
            tokens.append(("var", name))
        pos = m.end()
    if pos < len(text):
        tokens.append(("text", text[pos:]))

    def parse(i, stop=None):
        """-> (nodes, next index). `stop` is the section name we expect to close."""
        nodes = []
        while i < len(tokens):
            kind, val = tokens[i]
            if kind == "close":
                if val != stop:
                    raise TemplateError("%s: {{/%s}} closes {{#%s}}"
                                        % (where, val, stop or "nothing"))
                return nodes, i + 1
            if kind in ("open", "inv"):
                body, i = parse(i + 1, val)
                nodes.append((kind, val, body))
                continue
            nodes.append((kind, val))
            i += 1
        if stop is not None:
            raise TemplateError("%s: {{#%s}} is never closed" % (where, stop))
        return nodes, i

    tree, _end = parse(0)

    def emit(nodes, stack):
        for node in nodes:
            kind = node[0]
            if kind == "text":
                out.append(node[1])
            elif kind == "var":
                v = _lookup(stack, node[1])
                if v is _MISSING:
                    # Left in place so build.py's unresolved-token check reports
                    # it with the others rather than shipping a blank.
                    out.append("{{%s}}" % node[1])
                elif v is not None and v is not False:
                    out.append(str(v))
            elif kind == "inv":
                if not _truthy(_lookup(stack, node[1])):
                    emit(node[2], stack)
            else:  # open
                v = _lookup(stack, node[1])
                if not _truthy(v):
                    continue
                if isinstance(v, list):
                    for item in v:
                        emit(node[2], stack + [item if isinstance(item, dict) else item])
                elif isinstance(v, dict):
                    emit(node[2], stack + [v])
                else:
                    emit(node[2], stack)

    emit(tree, [data])
    return "".join(out)
