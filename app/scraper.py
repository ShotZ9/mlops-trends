import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_trends():
    """Scrape tren Twitter dari trends24.in/indonesia dan kembalikan dalam format JSON."""
    url = "https://trends24.in/indonesia/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    data = []
    time_blocks = soup.select(".trend-card")

    for block in time_blocks[:3]:  # ambil 3 blok waktu teratas
        time_label = block.select_one(".trend-card__time").get_text(strip=True)
        trends = block.select(".trend-card__list a")

        for rank, trend in enumerate(trends, start=1):
            data.append({
                "timestamp": time_label,
                "rank": rank,
                "text": trend.get_text(strip=True),
                "link": trend["href"]
            })

    result = {
        "meta": {
            "source": url,
            "scraped_at": datetime.utcnow().isoformat() + "Z",
            "count": len(data)
        },
        "trends": data
    }

    return result


if __name__ == "__main__":
    import json
    trends = scrape_trends()
    print(json.dumps(trends, ensure_ascii=False, indent=2))
