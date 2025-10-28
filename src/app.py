import requests, json, os
from datetime import datetime, timezone

def scrape_trends():
    url = "https://trends24.in/api/trends/indonesia.json"
    resp = requests.get(url)
    trends = []
    if resp.status_code == 200:
        data = resp.json()
        trends = [t["name"] for t in data.get("trends", [])]

    result = {
        "meta": {
            "source": url,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "count": len(trends)
        },
        "trends": trends
    }

    os.makedirs("data", exist_ok=True)
    with open("data/trends.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return result

if __name__ == "__main__":
    print(json.dumps(scrape_trends(), indent=2, ensure_ascii=False))
