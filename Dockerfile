FROM python:3.10-slim

WORKDIR /app

# Install dependencies from your project
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MLflow + S3 support (B2 compatible)
RUN pip install --no-cache-dir mlflow boto3 s3fs

# Copy all project files
COPY . .

# Railway dynamic port
ENV PORT=8080
EXPOSE 8080

CMD mlflow server \
    --host 0.0.0.0 \
    --port $PORT \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root s3://mlops-trends-bucket/mlflow \
    --workers 1
