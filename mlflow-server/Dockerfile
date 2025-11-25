FROM python:3.10-slim

WORKDIR /app

# Install only needed libraries
RUN pip install --no-cache-dir mlflow

# Dynamic port from Railway
ENV PORT=5000
EXPOSE 5000

RUN mkdir -p /app/mlruns && mkdir -p /app/mlartifacts

CMD mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /app/mlartifacts \
    --host 0.0.0.0 \
    --port $PORT
