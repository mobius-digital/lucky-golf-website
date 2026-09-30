"""PageSpeed Insights (mobile) for the five baseline pages.

    python v9/tools/speed_check.py                 -> v9/migration/speed-baseline.json
    python v9/tools/speed_check.py --theme 1234    -> the same pages on a theme preview
"""
import argparse, json, sys, time
from pathlib import Path
from urllib.parse import quote

import requests

ROOT = Path(__file__).resolve().parents[1]
PAGES = {
    "Home": "https://www.luckygolf.com/",
    "Carver (LGW02)": "https://www.luckygolf.com/products/lucky-golf-lgw02-gold",
    "Polos": "https://www.luckygolf.com/collections/polos",
    "Hat": "https://www.luckygolf.com/products/white-gold-classic-hat",
    "Blog": "https://www.luckygolf.com/blogs/news",
}
API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def run(url):
    for attempt in range(4):
        r = requests.get(API, params={"url": url, "strategy": "mobile", "category": "performance"}, timeout=180)
        if r.status_code == 200:
            break
        time.sleep(20 * (attempt + 1))
    r.raise_for_status()
    d = r.json()
    lh = d["lighthouseResult"]
    a = lh["audits"]
    field = d.get("loadingExperience", {}).get("metrics", {})
    return {
        "score": round(lh["categories"]["performance"]["score"] * 100),
        "lcp_s": round(a["largest-contentful-paint"]["numericValue"] / 1000, 2),
        "cls": round(a["cumulative-layout-shift"]["numericValue"], 3),
        "tbt_ms": round(a["total-blocking-time"]["numericValue"]),
        "fcp_s": round(a["first-contentful-paint"]["numericValue"] / 1000, 2),
        "si_s": round(a["speed-index"]["numericValue"] / 1000, 2),
        "bytes_kb": round(a["total-byte-weight"]["numericValue"] / 1024),
        "requests": len(a.get("network-requests", {}).get("details", {}).get("items", [])),
        "field_lcp_p75_ms": field.get("LARGEST_CONTENTFUL_PAINT_MS", {}).get("percentile"),
        "field_inp_p75_ms": field.get("INTERACTION_TO_NEXT_PAINT", {}).get("percentile"),
        "field_cls_p75": field.get("CUMULATIVE_LAYOUT_SHIFT_SCORE", {}).get("percentile"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme")
    ap.add_argument("--out", default=str(ROOT / "migration" / "speed-baseline.json"))
    a = ap.parse_args()
    out = {}
    for name, url in PAGES.items():
        u = f"{url}?preview_theme_id={a.theme}" if a.theme else url
        try:
            out[name] = {"url": u, **run(u)}
        except Exception as e:
            out[name] = {"url": u, "error": str(e)[:200]}
        print(name, out[name])
    Path(a.out).write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
