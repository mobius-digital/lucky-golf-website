"""Helpers for writing Shopify section files from Python: settings, blocks, schema."""
import json


def text(id, label, default=None, info=None):
    d = {"type": "text", "id": id, "label": label}
    if default:
        d["default"] = default
    if info:
        d["info"] = info
    return d


def textarea(id, label, default=None):
    d = {"type": "textarea", "id": id, "label": label}
    if default:
        d["default"] = default
    return d


def rich(id, label, default=None):
    d = {"type": "inline_richtext", "id": id, "label": label, "info": "Select a word and press Italic to make it the gold word."}
    if default:
        d["default"] = default
    return d


def url(id, label):
    return {"type": "url", "id": id, "label": label}


def img(id, label):
    return {"type": "image_picker", "id": id, "label": label}


def check(id, label, default=False):
    return {"type": "checkbox", "id": id, "label": label, "default": default}


def select(id, label, options, default):
    return {"type": "select", "id": id, "label": label, "options": [{"value": v, "label": l} for v, l in options], "default": default}


def rng(id, label, mn, mx, step, default, unit=""):
    d = {"type": "range", "id": id, "label": label, "min": mn, "max": mx, "step": step, "default": default}
    if unit:
        d["unit"] = unit
    return d


def number(id, label, default=None):
    d = {"type": "number", "id": id, "label": label}
    if default is not None:
        d["default"] = default
    return d


def product(id, label):
    return {"type": "product", "id": id, "label": label}


def plist(id, label, limit=20):
    return {"type": "product_list", "id": id, "label": label, "limit": limit}


def collection(id, label):
    return {"type": "collection", "id": id, "label": label}


def header(content):
    return {"type": "header", "content": content}


def para(content):
    return {"type": "paragraph", "content": content}


HEAD = [text("eyebrow", "Eyebrow"), rich("heading", "Heading (italic = gold word)"),
        select("heading_tag", "Heading level", [("h2", "H2"), ("h3", "H3"), ("h1", "H1 (one per page)")], "h2"),
        textarea("sub", "Line under the heading"), text("link_label", "Link on the right"), url("link_url", "Link URL")]
BTN = [text("btn_label", "Button"), url("btn_url", "Button link")]
IMG = [img("image", "Photo")]


def section(name, liquid, settings, blocks=None, max_blocks=None, groups=None, presets=True, tag=None):
    schema = {"name": name, "settings": settings}
    if tag:
        schema["tag"] = tag
    if blocks:
        schema["blocks"] = [{"type": t, "name": n, "settings": s} for t, n, s in blocks]
        if max_blocks:
            schema["max_blocks"] = max_blocks
    if groups:
        schema["enabled_on"] = {"groups": groups}
    elif presets:
        schema["presets"] = [{"name": name}]
    return liquid.strip() + "\n\n{% schema %}\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n{% endschema %}\n"
