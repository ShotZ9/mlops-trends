from scraper import scrape_trends
import json
import os

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    data = scrape_trends()
    with open("data/trends.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("✅ Data berhasil disimpan ke data/trends.json")
