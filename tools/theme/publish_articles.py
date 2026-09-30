"""Prepare the rewritten blog articles (v9/src/articles/<handle>.html) for the live blog
"news" (All Things Lucky). DRY RUN ONLY: this script never writes to Shopify.

    python tools/theme/publish_articles.py

It reads the live snapshot v9/migration/live-articles.json (ids, titles, summaries, images,
bodies; refresh it on launch day with the query below through the Shopify Admin connector),
maps each file to the live article with the same handle, and writes:

  v9/migration/articles-publish/<handle>.json   {"query": ..., "variables": ...} for articleUpdate
  v9/migration/articles-dry-run.md              what each update would change

Launch day (after the theme is live, so article.json renders the new fields):
  1. Refresh the snapshot (connector graphql_query):
       { blogs(first:5){nodes{id handle title articles(first:50){nodes{id handle title isPublished
         publishedAt templateSuffix tags image{url altText} summary body
         seoT:metafield(namespace:"global",key:"title_tag"){value}
         seoD:metafield(namespace:"global",key:"description_tag"){value}
         metafields(first:10){nodes{namespace key type}}}}}} }
     save it to v9/migration/live-articles.json, rerun this script, read the dry-run report.
  2. Send each articles-publish/<handle>.json through the connector's graphql_mutation
     (query + variables as written). Handles, publish dates and published state never change,
     so every URL and its SEO history stays put.
  3. Check one article and the blog index on the live site.

What an update sets: title, body (the rewritten text + its "Quick answers"), summary (the line
under the title on the blog index), the hero image (from Content > Files, lg-<name>.webp) with
alt text, the meta description (global.description_tag), and the article metafields the theme
reads: lucky.h1 (heading with the gold word), lucky.lede, lucky.crumb, lucky.signoff (JSON).
"""
import html, json, os, re

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
SRC = os.path.join(ROOT, "v9", "src", "articles")
SNAP = os.path.join(ROOT, "v9", "migration", "live-articles.json")
OUT_DIR = os.path.join(ROOT, "v9", "migration", "articles-publish")
REPORT = os.path.join(ROOT, "v9", "migration", "articles-dry-run.md")
FILES = "https://cdn.shopify.com/s/files/1/2286/3149/files/lg-"
BLOG = "news"

# v9 preview page -> live store path
LINKS = {
    "carver.html": "/products/lucky-golf-lgw02-gold",
    "black.html": "/products/lucky-golf-lgw02-black",
    "mallet.html": "/products/limited-edition-mallet-putter",
    "blade.html": "/products/signature-gold-putters",
    "stryker.html": "/products/lucky-striker-hybrid-limited-edition",
    "clubs.html": "/collections/lucky-golf-clubs",
    "polos.html": "/collections/polos",
    "hats.html": "/collections/hats",
    "gear.html": "/collections/most-popular",
    "community.html": "/pages/community",
    "compare.html": "/pages/compare",
    "trybe.html": "/pages/become-apart-of-the-team",
    "story.html": "/pages/about",
    "faq.html": "/pages/faq-lucky-wedges",
    "reviews.html": "/pages/reviews",
    "blog.html": "/blogs/" + BLOG,
    "home.html": "/",
}

MUTATION = ("mutation UpdateArticle($id: ID!, $article: ArticleUpdateInput!) { articleUpdate(id: $id, article: $article) "
            "{ article { id handle title isPublished image { url } } userErrors { code field message } } }")


def link(href):
    m = re.match(r"article-(.+)\.html(#.*)?$", href)
    if m:
        return f"/blogs/{BLOG}/{m.group(1)}" + (m.group(2) or "")
    page, _, frag = href.partition("#")
    if page in LINKS:
        return LINKS[page] + ("#" + frag if frag else "")
    return href


def rewrite(body, problems):
    def href(m):
        h = m.group(1)
        new = link(h)
        if new == h and not re.match(r"(https?:|mailto:|#|/)", h):
            problems.append(f"unmapped link {h}")
        return f'href="{new}"'
    body = re.sub(r'href="([^"]+)"', href, body)
    body = re.sub(r'src="img/([^"]+)"', lambda m: f'src="{FILES}{m.group(1)}"', body)
    return body


def load():
    out = []
    for f in sorted(os.listdir(SRC)):
        if not f.endswith(".html"):
            continue
        raw = open(os.path.join(SRC, f), encoding="utf-8").read()
        m = re.match(r"\s*<!--meta\s*(\{.*?\})\s*-->\s*(.*)$", raw, re.S)
        a = json.loads(m.group(1))
        a["handle"], a["body"] = f[:-5], m.group(2).strip()
        out.append(a)
    return out


def text(h):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h or ""))).strip()


def build(a, live, problems):
    body = rewrite(a["body"], problems)
    faq = "".join(f'<details class="lg-fq"{" open" if n == 0 else ""}><summary>{q}</summary><div class="lg-fq-a"><p>{ans}</p></div></details>'
                  for n, (q, ans) in enumerate(a.get("faq", [])))
    if faq:
        body += '\n\n<h2>Quick answers</h2>\n<div class="lg-faq">' + faq + "</div>"
    so = dict(a["signoff"])
    so["href"] = link(so.get("href", ""))
    mf = [
        {"namespace": "lucky", "key": "h1", "type": "single_line_text_field", "value": a["h1"]},
        {"namespace": "lucky", "key": "lede", "type": "multi_line_text_field", "value": a["lede"]},
        {"namespace": "lucky", "key": "crumb", "type": "single_line_text_field", "value": a.get("crumb", a["title"])},
        {"namespace": "lucky", "key": "signoff", "type": "json", "value": json.dumps(so, ensure_ascii=False)},
        {"namespace": "global", "key": "description_tag", "type": "multi_line_text_field", "value": a["sub"]},
    ]
    art = {"title": a["title"], "body": body, "summary": a["sub"],
           "image": {"url": FILES + a["img"], "altText": a.get("alt", "")}, "metafields": mf}
    return {"query": MUTATION, "variables": {"id": live["id"], "article": art}}


def short(s, n=90):
    s = text(s)
    return (s[:n] + "...") if len(s) > n else s


def main():
    snap = json.load(open(SNAP, encoding="utf-8"))
    blog = [b for b in snap["data"]["blogs"]["nodes"] if b["handle"] == BLOG][0]
    live = {x["handle"]: x for x in blog["articles"]["nodes"]}
    os.makedirs(OUT_DIR, exist_ok=True)
    arts = load()
    rows, notes = [], []
    lines = ["# Blog articles: dry run (nothing sent to Shopify)", "",
             f"Blog `{BLOG}` ({blog['title']}): {len(live)} live articles, {len(arts)} rewritten files.",
             "Built by `tools/theme/publish_articles.py` from `v9/migration/live-articles.json`.", "",
             "| File (= live handle) | Live article | Published | Title now -> new | Hero image now -> new | Body words now -> new |",
             "|---|---|---|---|---|---|"]
    for a in arts:
        problems = []
        l = live.get(a["handle"])
        if not l:
            notes.append(f"- `{a['handle']}.html`: NO live article with this handle, skipped.")
            continue
        payload = build(a, l, problems)
        json.dump(payload, open(os.path.join(OUT_DIR, a["handle"] + ".json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
        art = payload["variables"]["article"]
        img_now = (l.get("image") or {}).get("url", "none").split("/")[-1].split("?")[0]
        words_now, words_new = len(text(l.get("body")).split()), len(text(art["body"]).split())
        lines.append(f"| `{a['handle']}` | {l['id'].rsplit('/', 1)[1]} | {'yes' if l['isPublished'] else 'no (draft, stays a draft)'} "
                     f"| {l['title']} -> {a['title']} | {img_now} -> lg-{a['img']} | {words_now} -> {words_new} |")
        detail = [f"### {a['handle']}", "",
                  f"- Summary now: {short(l.get('summary')) or '(empty)'}",
                  f"- Summary new: {a['sub']}",
                  f"- Meta description now: {(l.get('seoD') or {}).get('value') or '(none, Shopify falls back to the body)'}; new: the summary above",
                  f"- Heading on the page: {text(a['h1'])} (gold word from lucky.h1)",
                  f"- Body now starts: {short(l.get('body'))}",
                  f"- Body new starts: {short(art['body'])}",
                  f"- Quick answers added: {len(a.get('faq', []))}; sign-off: {text(a['signoff']['h'])} / {a['signoff']['btn']} -> {link(a['signoff']['href'])}",
                  "- Unchanged: handle, URL, publish date, published state, tags, template, author, comments."]
        if problems:
            detail.append("- CHECK: " + "; ".join(sorted(set(problems))))
        rows.append("\n".join(detail))
    extra = sorted(set(live) - {a["handle"] for a in arts})
    for h in extra:
        notes.append(f"- Live article `{h}` has no rewritten file; left as it is.")
    lines += ["", "Nothing else on the store changes. The theme's article template reads the lucky.* metafields and",
              "falls back to the article title (and skips the lede and sign-off it lacks), so the live articles render fine before and after.", ""]
    if notes:
        lines += ["## Notes", ""] + notes + [""]
    lines += ["## Per article", ""] + rows
    open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{len(rows)} payloads in {os.path.relpath(OUT_DIR, ROOT)}; report {os.path.relpath(REPORT, ROOT)}")


if __name__ == "__main__":
    main()
