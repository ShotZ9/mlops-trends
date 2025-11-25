import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timezone
import os
from urllib.parse import quote_plus
import re
from cluster_trends import TrendClusterizer

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
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
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

                    # Extract data-count attribute from tweet-count class
                    tweet_count_span = trend_item.find("span", class_="tweet-count")
                    tweet_count = 0
                    if tweet_count_span and 'data-count' in tweet_count_span.attrs:
                        tweet_count = tweet_count_span['data-count']
                        count_str = tweet_count_span['data-count']
                        if count_str.isdigit():  # Check if the string is a digit
                            tweet_count = int(count_str)  # Convert to integer
                            if tweet_count > 1000000:
                                tweet_count = f"{tweet_count / 1000000:.1f}M"  # Format to millions
                            elif tweet_count > 1000:
                                tweet_count = f"{tweet_count / 1000:.1f}k"  # Format to thousands
                            else:
                                tweet_count = tweet_count  # No formatting needed
                        else:
                            tweet_count = "0"  # Assign a default value if data-count is not found

                    trends_data["trends"].append({
                        "trend": trend_name,
                        "url": trend_url,
                        "data_count": tweet_count  # Using data-count attribute
                    })

            trends_data["meta"]["count"] = len(trends_data["trends"])
            trends_data["trends"] = trends_data["trends"][:20]  # limit top 20
            return trends_data

        except Exception as e:
            print(f"❌ Error saat scraping: {e}")
            return {"meta": {"error": str(e)}, "trends": []}

    def _detail_url(self, keyword):
        # trends24 pakai '+' di depan path-nya
        return f"https://trends24.in/indonesia/?q={quote_plus(keyword)}"

    def _parse_detail(self, html):
        soup = BeautifulSoup(html, "html.parser")
        formatted_html = soup.prettify()
        # Write the formatted HTML to a .txt file
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(formatted_html)

        print("HTML content has been saved to output.txt")

        # Initialize data dictionary
        data = {"trend": None, "url": None, "trending_for_hours": None, "total_tweets": None}

        # Find all trend items
        trend_items = soup.find_all("li", class_="stat-card-item")

        # Iterate through each trend item to extract data
        for item in trend_items:
            # Extract trend name and URL
            trend_link = item.find("a", class_="trend-link")
            if trend_link:
                data["trend"] = trend_link.text.strip()
                data["url"] = trend_link["href"]

            # Extract trending duration
            duration_text = item.text.split("with")[0].split("for")[1].strip()
            if duration_text:
                data["trending_for_hours"] = re.search(r"\d+", duration_text).group()

            # Extract total tweets
            tweets_text = item.text.split("with")[1].strip() if "with" in item.text else None
            if tweets_text:
                # Convert text like '13M' to 13000000
                num = float(re.search(r"[\d.]+", tweets_text).group())
                if "K" in tweets_text.upper():
                    data["total_tweets"] = int(num * 1_000)
                elif "M" in tweets_text.upper():
                    data["total_tweets"] = int(num * 1_000_000)

        return data

if __name__ == "__main__":
    scraper = TrendsScraperIndonesia()
    data = scraper.scrape_trends(hour_index=0)

    os.makedirs("data", exist_ok=True)
    output_path = os.path.join("data", "trends.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    trend_clusty = TrendClusterizer(output_path, "clusty.json")
    trend_clusty.run()

    # print(json.dumps(data, indent=2, ensure_ascii=False))
    print(f"✅ Data tren tersimpan di {output_path}")
