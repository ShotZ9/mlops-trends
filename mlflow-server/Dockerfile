FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow boto3 psycopg2-binary

# MLflow will run on Railway dynamic port
ENV PORT=5000
EXPOSE 5000

# B2 configuration
ENV MLFLOW_S3_ENDPOINT_URL=${B2_ENDPOINT}
ENV AWS_ACCESS_KEY_ID=${B2_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${B2_APP_KEY}

CMD mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root s3://mlflow-artifacts \
    --host 0.0.0.0 \
    --port $PORT
