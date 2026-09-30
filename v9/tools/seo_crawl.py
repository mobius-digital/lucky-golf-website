"""SEO crawl of every live URL: the move's before/after check.

    python v9/tools/seo_crawl.py                       -> v9/migration/seo-baseline.csv
    python v9/tools/seo_crawl.py --theme 1234 --out x  -> the same crawl on a theme preview

Reads v9/migration/url-inventory.txt. Saves, per URL: status, final URL,
title, meta description, H1s, canonical, robots meta, og:title/og:image,
JSON-LD @types, word count, image count and images missing alt.
"""
import argparse, csv, json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
INV = ROOT / "migration" / "url-inventory.txt"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128 Safari/537.36 LuckyMoveCrawl"
FIELDS = ["url", "status", "final_url", "redirects", "title", "title_len", "meta_description", "desc_len",
          "h1_count", "h1", "canonical", "robots", "og_title", "og_image", "jsonld_types", "words",
          "images", "images_no_alt", "bytes", "ms"]


def ld_types(soup):
    out = []
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(s.string or "")
        except Exception:
            out.append("INVALID")
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            d = stack.pop(0)
            if isinstance(d, dict):
                if "@graph" in d:
                    stack.extend(d["@graph"])
                t = d.get("@type")
                if t:
                    out.extend(t if isinstance(t, list) else [t])
    return "|".join(out)


def meta(soup, **attrs):
    tag = soup.find("meta", attrs=attrs)
    return (tag.get("content") or "").strip() if tag else ""


def crawl(url, theme):
    params = {"preview_theme_id": theme} if theme else None
    t0 = time.time()
    for attempt in range(5):
        try:
            r = requests.get(url, params=params, headers={"User-Agent": UA}, timeout=40)
            if r.status_code in (429, 503) and attempt < 4:
                time.sleep(8 * (attempt + 1))
                continue
            break
        except Exception as e:
            if attempt == 4:
                return {"url": url, "status": f"ERR {e.__class__.__name__}"}
            time.sleep(3)
    ms = int((time.time() - t0) * 1000)
    row = {"url": url, "status": r.status_code, "final_url": r.url.split("?")[0],
           "redirects": len(r.history), "bytes": len(r.content), "ms": ms}
    if "html" not in r.headers.get("content-type", ""):
        return row
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")
    title = " ".join(soup.title.get_text(" ").split()) if soup.title else ""
    desc = meta(soup, name="description")
    h1s = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
    can = soup.find("link", rel="canonical")
    imgs = [(i.get("alt") or "").strip() for i in soup.find_all("img")]
    ld = ld_types(soup)
    for s in soup(["script", "style", "noscript", "template", "svg"]):
        s.decompose()
    words = len(re.findall(r"\w+", soup.get_text(" ")))
    row.update(title=title, title_len=len(title), meta_description=desc, desc_len=len(desc),
               h1_count=len(h1s), h1=" || ".join(h1s)[:300], canonical=can.get("href", "") if can else "",
               robots=meta(soup, name="robots"), og_title=meta(soup, property="og:title"),
               og_image=meta(soup, property="og:image"), jsonld_types=ld, words=words,
               images=len(imgs), images_no_alt=sum(1 for i in imgs if not i))
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", help="preview_theme_id to crawl instead of the live theme")
    ap.add_argument("--out", default=str(ROOT / "migration" / "seo-baseline.csv"))
    a = ap.parse_args()
    urls = list(dict.fromkeys(l.strip() for l in INV.read_text(encoding="utf-8").splitlines() if l.startswith("https://")))
    with ThreadPoolExecutor(2) as ex:
        rows = list(ex.map(lambda u: crawl(u, a.theme), urls))
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, FIELDS)
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if str(r.get("status")) != "200"]
    print(f"{len(rows)} URLs -> {a.out}; non-200: {len(bad)}")
    for r in bad:
        print("  ", r["status"], r["url"], "->", r.get("final_url", ""))


if __name__ == "__main__":
    sys.exit(main())
