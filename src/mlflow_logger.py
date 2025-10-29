import mlflow
import json
from datetime import datetime

def log_trends_to_mlflow(file_path="data/trends.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, list):
            latest = data[-1]
        else:
            latest = data

    with mlflow.start_run(run_name="trends_scrape_run"):
        mlflow.log_param("country", latest["meta"]["source"])
        mlflow.log_metric("trend_count", latest["meta"]["count"])
        mlflow.log_param("timestamp", latest["meta"]["scraped_at"])
        mlflow.log_artifact(file_path)
        print("✅ Logged to MLflow")

if __name__ == "__main__":
    mlflow.set_tracking_uri("http://localhost:5000")  # nanti bisa pakai MLflow server
    mlflow.set_experiment("Twitter_Trends_Scraping")
    log_trends_to_mlflow()
