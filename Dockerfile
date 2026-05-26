FROM python:3.12-slim

WORKDIR /market_analytics_platform

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "-c"]