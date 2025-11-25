import mlflow
import os

mlflow_uri = os.getenv("MLFLOW_TRACKING_URI", "https://mlflow-production.up.railway.app")

mlflow.set_tracking_uri(mlflow_uri)
mlflow.set_experiment("Twitter_Trends_Scraping")

with mlflow.start_run():
    mlflow.log_param("country", "Indonesia")
    mlflow.log_metric("trend_count", len(open("data/trends.json").read()))
    mlflow.log_artifact("data/trends.json")
