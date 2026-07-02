"""
Fetches live news for the StackWatch dashboard and writes data/news.json.

Runs inside GitHub Actions on a schedule (see .github/workflows/fetch-news.yml).
Uses NewsAPI.org's /v2/everything endpoint. The API key is read from the
NEWS_API_KEY environment variable (set as a GitHub Actions secret) and is
never exposed to the browser.

Get a free key at: https://newsapi.org/register

IMPORTANT: keep these keys and queries in sync with the CATEGORIES object
inside index.html's <script> tag (used as the live-fallback source when
data/news.json isn't available yet).
"""

import json
import os
import time
from datetime import datetime, timezone

import requests

API_KEY = os.environ.get("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

# Edit these to change what each tab tracks. Keep query counts modest —
# see the rate-limit note in README.md before adding more.
CATEGORIES = {
    "sg": [
        "Singapore news",
    ],
    "china": [
        "China technology policy",
        "Huawei",
        "China semiconductor",
    ],
    "politics": [
        "world politics",
        "geopolitics",
    ],
    "usworld": [
        "United States news",
        "world news today",
    ],
    "companies": [
        "startup funding",
    ],
}

ITEMS_PER_CATEGORY = 25


def fetch_query(query: str) -> list[dict]:
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=20)
    resp.raise_for_status()
    payload = resp.json()
    if payload.get("status") != "ok":
        raise RuntimeError(f"API error for '{query}': {payload.get('message')}")
    return payload.get("articles", [])


def build_category(queries: list[str]) -> list[dict]:
    seen_urls = set()
    items = []
    for query in queries:
        try:
            articles = fetch_query(query)
        except Exception as exc:  # noqa: BLE001
            print(f"warning: query '{query}' failed: {exc}")
            continue
        for article in articles:
            url = article.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            items.append({
                "title": article.get("title") or "",
                "source": (article.get("source") or {}).get("name", ""),
                "link": url,
                "pubDate": article.get("publishedAt"),
                "description": article.get("description") or "",
            })
        time.sleep(1)  # be gentle with rate limits
    items.sort(key=lambda a: a.get("pubDate") or "", reverse=True)
    return items[:ITEMS_PER_CATEGORY]


def main() -> None:
    if not API_KEY:
        raise SystemExit("NEWS_API_KEY environment variable is not set")

    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "categories": {},
    }
    for key, queries in CATEGORIES.items():
        print(f"fetching category: {key}")
        output["categories"][key] = build_category(queries)

    os.makedirs("data", exist_ok=True)
    with open("data/news.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("wrote data/news.json")


if __name__ == "__main__":
    main()
