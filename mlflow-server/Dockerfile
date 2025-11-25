FROM python:3.10-slim

WORKDIR /app

# Install MLflow + B2/S3 support
RUN pip install --no-cache-dir mlflow boto3 s3fs psycopg2-binary

# Railway dynamic port
ENV PORT=5000
EXPOSE 5000

# Backblaze B2 (Railway will inject)
ENV MLFLOW_S3_ENDPOINT_URL=${B2_ENDPOINT}
ENV AWS_ACCESS_KEY_ID=${B2_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${B2_APP_KEY}

# MLflow server
CMD mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root s3://mlops-trends-bucket \
    --host 0.0.0.0 \
    --port $PORT
