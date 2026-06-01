FROM python:3.11-slim

WORKDIR /market_analytics_platform

RUN apt-get update && \
    apt-get purge -y perl perl-modules-* && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "bash", "-c" ]