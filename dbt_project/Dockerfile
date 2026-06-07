FROM python:3.12-slim

WORKDIR /dbt_project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dbt_project.yml packages.yml package-lock.yml ./
RUN dbt deps

COPY . .