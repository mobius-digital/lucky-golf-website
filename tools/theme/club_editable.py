"""Make the club pages editable in the theme editor, without changing a pixel.

Each club section reads its words from its own theme-editor settings first and falls back to the
product metafield custom.club_page (so an empty field still renders what it did before). Then each
club gets its own template (product.club-<name>.json) with those settings filled from the metafield,
word for word. Body class: theme.liquid adds lg-t-club to any suffix starting "club-", so the club CSS
still applies.

    python tools/theme/club_editable.py sections   -> patches theme/sections/lg-club-*.liquid (idempotent)
    python tools/theme/club_editable.py templates  -> writes theme/templates/product.club-<name>.json
"""
import json, os, re, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SEC = os.path.join(ROOT, "theme", "sections")
TPL = os.path.join(ROOT, "theme", "templates")
REF = os.path.join(ROOT, "_ref", "club-page")
CLUBS = {"carver-gold": "lucky-golf-lgw02-gold", "carver-black": "lucky-golf-lgw02-black",
         "blade": "signature-gold-putters", "mallet": "limited-edition-mallet-putter",
         "stryker": "lucky-striker-hybrid-limited-edition"}
MARK = "{%- comment -%} editable: theme-editor settings first, club_page fallback {%- endcomment -%}"


def T(i, l, kind="text"):
    return {"type": kind, "id": i, "label": l}


def patch(fname, reps, settings):
    p = os.path.join(SEC, fname)
    s = open(p, encoding="utf-8").read()
    if MARK in s:
        print(fname, "already patched")
        return
    for a, b in reps:
        assert s.count(a) == 1, (fname, a[:80])
        s = s.replace(a, b)
    m = re.search(r"{%\s*schema\s*%}(.*?){%\s*endschema\s*%}", s, re.S)
    sch = json.loads(m.group(1))
    sch.setdefault("settings", [])
    sch["settings"] += [{"type": "header", "content": "This club's words"},
                        {"type": "paragraph", "content": "Leave a field empty to use the product's saved copy."}] + settings
    s = s[:m.start(1)] + "\n" + json.dumps(sch, indent=2, ensure_ascii=False) + "\n" + s[m.end(1):]
    s = MARK + "\n" + s
    open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


def sections():
    # ---- main: eyebrow, H1, review snippet, description, photo tag, button, the three drop-downs
    patch("lg-club-main.liquid", [
        ("  assign atc = c.atc | default: s.atc\n",
         "  assign atc = s.p_atc | default: c.atc | default: s.atc\n"
         "  assign p_eyebrow = s.p_eyebrow | default: c.eyebrow\n"
         "  assign p_h1 = s.p_h1 | default: c.h1 | default: product.title\n"
         "  assign p_lede = s.p_lede | default: c.lede | default: product.description | strip_html\n"
         "  assign p_tag = s.p_tag | default: c.gallery_tag\n"
         "  assign rv0 = s.p_rvl_q | default: c.rvl[0]\n"
         "  assign rv1 = s.p_rvl_n | default: c.rvl[1]\n"
         "  assign rv2 = s.p_rvl_l | default: c.rvl[2]\n"),
        ("{%- if c.gallery_tag != blank %}<span class=\"lg-tag\">{{ c.gallery_tag }}</span>{% endif -%}",
         "{%- if p_tag != blank %}<span class=\"lg-tag\">{{ p_tag }}</span>{% endif -%}"),
        ("{%- if c.eyebrow != blank %}<p class=\"lg-eyebrow\">{{ c.eyebrow }}</p>{% endif -%}",
         "{%- if p_eyebrow != blank %}<p class=\"lg-eyebrow\">{{ p_eyebrow }}</p>{% endif -%}"),
        ("<h1 class=\"lg-d1\">{{ c.h1 | default: product.title | replace:",
         "<h1 class=\"lg-d1\">{{ p_h1 | replace:"),
        ("{%- if c.rvl -%}<a href=\"#reviews\">&ldquo;{{ c.rvl[0] }}&rdquo; {{ c.rvl[1] }} · {{ c.rvl[2] }}</a>",
         "{%- if rv0 != blank -%}<a href=\"#reviews\">&ldquo;{{ rv0 }}&rdquo; {{ rv1 }} · {{ rv2 }}</a>"),
        ("<p class=\"lg-body\">{{ c.lede | default: product.description | strip_html }}</p>",
         "<p class=\"lg-body\">{{ p_lede }}</p>"),
        ("    {%- if c.details.size > 0 -%}\n    <div class=\"lg-faq\">\n      {%- for d in c.details -%}<details class=\"lg-fq\"><summary>{{ d[0] }}</summary><div class=\"lg-fq-a\"><p>{{ d[1] }}</p></div></details>{%- endfor -%}\n    </div>\n    {%- endif -%}",
         "    {%- assign nd = 0 -%}{%- for k in (1..3) -%}{%- assign kt = 'p_d' | append: k | append: '_t' -%}{%- assign dt = s[kt] | default: c.details[forloop.index0][0] -%}{%- if dt != blank %}{% assign nd = nd | plus: 1 %}{% endif -%}{%- endfor -%}\n"
         "    {%- if nd > 0 -%}\n    <div class=\"lg-faq\">\n"
         "      {%- for k in (1..3) -%}{%- assign kt = 'p_d' | append: k | append: '_t' -%}{%- assign kb = 'p_d' | append: k | append: '_b' -%}"
         "{%- assign dt = s[kt] | default: c.details[forloop.index0][0] -%}{%- assign db = s[kb] | default: c.details[forloop.index0][1] -%}"
         "{%- if dt != blank -%}<details class=\"lg-fq\"><summary>{{ dt }}</summary><div class=\"lg-fq-a\"><p>{{ db }}</p></div></details>{%- endif -%}{%- endfor -%}\n"
         "    </div>\n    {%- endif -%}"),
    ], [T("p_eyebrow", "Eyebrow"), T("p_h1", "Title (a word in em tags turns gold)"), T("p_lede", "Description", "textarea"),
        T("p_rvl_q", "Review snippet: quote"), T("p_rvl_n", "Review snippet: name"), T("p_rvl_l", "Review snippet: link text"),
        T("p_tag", "Tag on the first photo"), T("p_atc", "Button label"),
        T("p_d1_t", "Drop-down 1 title"), T("p_d1_b", "Drop-down 1 text", "textarea"),
        T("p_d2_t", "Drop-down 2 title"), T("p_d2_b", "Drop-down 2 text", "textarea"),
        T("p_d3_t", "Drop-down 3 title"), T("p_d3_b", "Drop-down 3 text", "textarea")])

    # ---- film: the "On the course" words and "Who it's for"
    patch("lg-club-film.liquid", [
        ("{%- if c.story -%}", "{%- assign s = section.settings -%}{%- assign p_eyebrow = s.p_eyebrow | default: c.story.eyebrow -%}"
         "{%- assign p_head = s.p_head | default: c.story.head -%}{%- assign p_who = s.p_who | default: c.who -%}\n{%- if c.story or s.p_head != blank -%}"),
        ("<p class=\"lg-eyebrow\">{{ c.story.eyebrow }}</p>", "<p class=\"lg-eyebrow\">{{ p_eyebrow }}</p>"),
        ("<h2 class=\"lg-d2\">{{ c.story.head | replace:", "<h2 class=\"lg-d2\">{{ p_head | replace:"),
        ("{%- for p in c.story.body %}<p class=\"lg-body\">{{ p }}</p>{% endfor -%}",
         "{%- if s.p_body != blank %}<p class=\"lg-body\">{{ s.p_body }}</p>{%- else -%}{%- for p in c.story.body %}<p class=\"lg-body\">{{ p }}</p>{% endfor -%}{%- endif -%}"),
        ("{%- if c.who != blank -%}<div class=\"whofor\"><span class=\"lg-label\">{{ section.settings.who_label }}</span><p>{{ c.who }}</p></div>{%- endif -%}",
         "{%- if p_who != blank -%}<div class=\"whofor\"><span class=\"lg-label\">{{ section.settings.who_label }}</span><p>{{ p_who }}</p></div>{%- endif -%}"),
    ], [T("p_eyebrow", "Eyebrow"), T("p_head", "Heading (a word in em tags turns gold)"), T("p_body", "Text", "textarea"),
        T("p_who", "Who it's for", "textarea")])

    # ---- grinds: heading, line, and each panel's tag, title and text
    patch("lg-club-grinds.liquid", [
        ("{%- if c.grinds -%}{%- assign gr = c.grinds -%}", "{%- assign s = section.settings -%}\n{%- if c.grinds -%}{%- assign gr = c.grinds -%}"),
        ("<p class=\"lg-eyebrow\">{{ gr.eyebrow }}</p><h2 class=\"lg-d2\">{{ gr.head }}</h2></div>\n    <p class=\"lg-body\">{{ gr.body }}</p>",
         "<p class=\"lg-eyebrow\">{{ s.p_eyebrow | default: gr.eyebrow }}</p><h2 class=\"lg-d2\">{{ s.p_head | default: gr.head }}</h2></div>\n    <p class=\"lg-body\">{{ s.p_body | default: gr.body }}</p>"),
        ("    {%- for p in gr.panels -%}\n",
         "    {%- for p in gr.panels -%}{%- assign k = forloop.index -%}{%- assign kt = 'p_g' | append: k | append: '_tag' -%}{%- assign kh = 'p_g' | append: k | append: '_h' -%}{%- assign kp = 'p_g' | append: k | append: '_p' -%}"
         "{%- assign g_tag = s[kt] | default: p.tag -%}{%- assign g_h = s[kh] | default: p.h -%}{%- assign g_p = s[kp] | default: p.p -%}\n"),
        ("<span class=\"lg-tag\">{{ p.tag }}</span><h3 class=\"lg-d3\">{{ p.h }}</h3><p>{{ p.p }}</p><span class=\"lg-link\">",
         "<span class=\"lg-tag\">{{ g_tag }}</span><h3 class=\"lg-d3\">{{ g_h }}</h3><p>{{ g_p }}</p><span class=\"lg-link\">"),
        ("<div class=\"lg-panel\"><span class=\"lg-tag\">{{ p.tag }}</span><h3 class=\"lg-d3\">{{ p.h }}</h3><p>{{ p.p }}</p>\n",
         "<div class=\"lg-panel\"><span class=\"lg-tag\">{{ g_tag }}</span><h3 class=\"lg-d3\">{{ g_h }}</h3><p>{{ g_p }}</p>\n"),
    ], [T("p_eyebrow", "Eyebrow"), T("p_head", "Heading"), T("p_body", "Line"),
        T("p_g1_tag", "Panel 1 tag"), T("p_g1_h", "Panel 1 title"), T("p_g1_p", "Panel 1 text", "textarea"),
        T("p_g2_tag", "Panel 2 tag"), T("p_g2_h", "Panel 2 title"), T("p_g2_p", "Panel 2 text", "textarea")])

    # ---- specs: heading, line, notes (the numbers stay product data)
    patch("lg-club-specs.liquid", [
        ("<h2 class=\"lg-d2\">{{ sp.head }}</h2>\n    <p class=\"lg-body\">{{ sp.line }}</p>",
         "<h2 class=\"lg-d2\">{{ s.p_head | default: sp.head }}</h2>\n    <p class=\"lg-body\">{{ s.p_line | default: sp.line }}</p>"),
        ("{%- if sp.table_note != blank %}<p class=\"note\">{{ sp.table_note }}</p>{% endif -%}",
         "{%- assign tn = s.p_note | default: sp.table_note -%}{%- if tn != blank %}<p class=\"note\">{{ tn }}</p>{% endif -%}"),
        ("  {%- if sp.note != blank %}<p class=\"note\">{{ sp.note }}</p>{% endif -%}",
         "  {%- assign tn = s.p_note | default: sp.note -%}{%- if tn != blank %}<p class=\"note\">{{ tn }}</p>{% endif -%}"),
    ], [T("p_head", "Heading"), T("p_line", "Line", "textarea"), T("p_note", "Note under the table", "textarea")])

    # ---- reviews: the three quotes on the page
    patch("lg-club-reviews.liquid", [
        ("    {%- for q in c.quotes -%}\n",
         "    {%- for q in c.quotes -%}{%- assign k = forloop.index -%}{%- assign kt = 'p_q' | append: k | append: '_t' -%}{%- assign kq = 'p_q' | append: k | append: '_q' -%}{%- assign kn = 'p_q' | append: k | append: '_n' -%}"
         "{%- assign q_t = section.settings[kt] | default: q.t -%}{%- assign q_q = section.settings[kq] | default: q.q -%}{%- assign q_n = section.settings[kn] | default: q.n -%}\n"),
        ("{% if q.t != blank %}<b>{{ q.t }}</b>{% endif %}<blockquote>&ldquo;{{ q.q }}&rdquo;</blockquote><figcaption>{{ q.n }} ·",
         "{% if q_t != blank %}<b>{{ q_t }}</b>{% endif %}<blockquote>&ldquo;{{ q_q }}&rdquo;</blockquote><figcaption>{{ q_n }} ·"),
    ], [x for k in (1, 2, 3) for x in (T(f"p_q{k}_t", f"Quote {k} title"), T(f"p_q{k}_q", f"Quote {k}", "textarea"), T(f"p_q{k}_n", f"Quote {k} name"))])

    # ---- more: the four cards (product, name, line)
    patch("lg-club-more.liquid", [
        ("    {%- for m in c.more -%}{%- assign mp = all_products[m[0]] -%}\n      {%- if mp != blank -%}{% render 'lg-card', product: mp, name: m[1], line: m[2], cut: true, stars: false %}{%- endif -%}",
         "    {%- for m in c.more -%}{%- assign k = forloop.index -%}{%- assign kp = 'p_m' | append: k | append: '_product' -%}{%- assign kn = 'p_m' | append: k | append: '_name' -%}{%- assign kl = 'p_m' | append: k | append: '_line' -%}"
         "{%- assign mp = s[kp] | default: all_products[m[0]] -%}{%- assign m_n = s[kn] | default: m[1] -%}{%- assign m_l = s[kl] | default: m[2] -%}\n"
         "      {%- if mp != blank -%}{% render 'lg-card', product: mp, name: m_n, line: m_l, cut: true, stars: false %}{%- endif -%}"),
    ], [x for k in (1, 2, 3, 4) for x in (T(f"p_m{k}_product", f"Card {k} product", "product"), T(f"p_m{k}_name", f"Card {k} name"), T(f"p_m{k}_line", f"Card {k} line"))])

    # ---- sign-off: the line under the tagline and the button
    patch("lg-club-signoff.liquid", [
        ("{%- if c.sign != blank %}<p class=\"lg-lede\">{{ c.sign }}</p>{% endif -%}",
         "{%- assign p_sign = s.p_sign | default: c.sign -%}{%- if p_sign != blank %}<p class=\"lg-lede\">{{ p_sign }}</p>{% endif -%}"),
        ("{{ c.signcta | default: s.cta }}", "{{ s.p_signcta | default: c.signcta | default: s.cta }}"),
    ], [T("p_sign", "Line under the tagline"), T("p_signcta", "Button label")])

    # ---- photo band: the three photos and their descriptions
    patch("lg-club-pband.liquid", [
        ("{%- assign band = product.metafields.custom.club_band_photos.value -%}\n{%- if band.size > 0 -%}",
         "{%- assign band = product.metafields.custom.club_band_photos.value -%}{%- assign s = section.settings -%}\n{%- if band.size > 0 -%}"),
        ("{%- for im in band -%}{%- assign p = c.pband[forloop.index0] -%}{%- assign alt = p[0] | default: im.alt -%}",
         "{%- for im0 in band -%}{%- assign k = forloop.index -%}{%- assign ki = 'p_img' | append: k -%}{%- assign ka = 'p_alt' | append: k -%}{%- assign im = s[ki] | default: im0 -%}"
         "{%- assign p = c.pband[forloop.index0] -%}{%- assign alt = s[ka] | default: p[0] | default: im.alt -%}"),
    ], [x for k in (1, 2, 3) for x in (T(f"p_img{k}", f"Photo {k}", "image_picker"), T(f"p_alt{k}", f"Photo {k} description"))])


def templates():
    base = json.load(open(os.path.join(TPL, "product.club.json"), encoding="utf-8"))
    for name, handle in CLUBS.items():
        c = json.load(open(os.path.join(REF, handle + ".json"), encoding="utf-8"))
        t = json.loads(json.dumps(base))
        S = t["sections"]
        m = S["main"]["settings"]
        m.update({"p_eyebrow": c.get("eyebrow", ""), "p_h1": c.get("h1", ""), "p_lede": c.get("lede", ""),
                  "p_tag": c.get("gallery_tag", ""), "p_atc": c.get("atc", "")})
        if c.get("rvl"):
            m.update({"p_rvl_q": c["rvl"][0], "p_rvl_n": c["rvl"][1], "p_rvl_l": c["rvl"][2]})
        for i, d in enumerate(c.get("details", [])[:3], 1):
            m[f"p_d{i}_t"], m[f"p_d{i}_b"] = d[0], d[1]
        st = c.get("story", {})
        S["film"]["settings"].update({"p_eyebrow": st.get("eyebrow", ""), "p_head": st.get("head", ""),
                                      "p_body": "\n\n".join(st.get("body", [])), "p_who": c.get("who", "")})
        if len(st.get("body", [])) > 1:
            sys.exit(f"{name}: story body has more than one paragraph; the single text field would merge them")
        gr = c.get("grinds")
        if gr:
            g = {"p_eyebrow": gr["eyebrow"], "p_head": gr["head"], "p_body": gr["body"]}
            for i, p in enumerate(gr["panels"][:2], 1):
                g.update({f"p_g{i}_tag": p["tag"], f"p_g{i}_h": p["h"], f"p_g{i}_p": p["p"]})
            S["grinds"]["settings"].update(g)
        sp = c.get("spec", {})
        S["specs"]["settings"].update({"p_head": sp.get("head", ""), "p_line": sp.get("line", ""),
                                       "p_note": sp.get("table_note") if "table_note" in sp else sp.get("note", "")})
        for i, q in enumerate(c.get("quotes", [])[:3], 1):
            S["reviews"]["settings"].update({f"p_q{i}_t": q.get("t", ""), f"p_q{i}_q": q["q"], f"p_q{i}_n": q["n"]})
        for i, mm in enumerate(c.get("more", [])[:4], 1):
            S["more"]["settings"].update({f"p_m{i}_product": mm[0], f"p_m{i}_name": mm[1], f"p_m{i}_line": mm[2]})
        S["last"]["settings"].update({"p_sign": c.get("sign", ""), "p_signcta": c.get("signcta", "")})
        for i, p in enumerate(c.get("pband", [])[:3], 1):
            S["pband"]["settings"][f"p_alt{i}"] = p[0]
        # empty strings would make Shopify store nothing; drop them so the fallback shows the same thing
        for sec in S.values():
            for k in [k for k, v in sec.get("settings", {}).items() if k.startswith("p_") and v in ("", None)]:
                del sec["settings"][k]
        out = os.path.join(TPL, f"product.club-{name}.json")
        json.dump(t, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(out)


if __name__ == "__main__":
    {"sections": sections, "templates": templates}[sys.argv[1]]()
