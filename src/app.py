import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import os


class TrendsScraperIndonesia:
    def __init__(self):
        self.base_url = "https://trends24.in/indonesia/"
        self.headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/91.0.4472.124 Safari/537.36'
            )
        }

    def scrape_trends(self, hour_index=0):
        """Scrape trending topics from trends24.in/indonesia/"""
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            trends_data = {
                "meta": {
                    "source": self.base_url,
                    "scraped_at": datetime.utcnow().isoformat() + "Z",
                    "hour_index": hour_index,
                },
                "trends": [],
            }

            trend_cards = soup.find_all("ol", class_="trend-card__list")

            if not trend_cards or hour_index >= len(trend_cards):
                print(f"⚠ Tidak menemukan tren pada indeks {hour_index}")
                return trends_data

            target_card = trend_cards[hour_index]
            trends_in_card = target_card.find_all("li")

            for trend_item in trends_in_card:
                trend_link = trend_item.find("a")
                if trend_link:
                    trend_name = trend_link.get_text(strip=True)
                    trend_url = trend_link.get("href", "")
                    tweet_volume = trend_item.find("span", class_="tweet-volume")
                    volume = tweet_volume.get_text(strip=True) if tweet_volume else "N/A"

                    trends_data["trends"].append({
                        "trend": trend_name,
                        "url": trend_url,
                        "tweet_volume": volume,
                    })

            trends_data["meta"]["count"] = len(trends_data["trends"])
            trends_data["trends"] = trends_data["trends"][:20]  # limit top 20
            return trends_data

        except Exception as e:
            print(f"❌ Error saat scraping: {e}")
            return {"meta": {"error": str(e)}, "trends": []}


if __name__ == "__main__":
    scraper = TrendsScraperIndonesia()
    data = scraper.scrape_trends(hour_index=0)

    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "trends.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✅ Data tren tersimpan di {output_path}")
