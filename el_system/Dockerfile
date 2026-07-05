FROM python:3.12-slim  

WORKDIR /el_system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .