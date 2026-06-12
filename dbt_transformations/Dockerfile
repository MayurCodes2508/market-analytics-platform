FROM python:3.12-slim

WORKDIR /dbt_transformations

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY profiles.yml dbt_project.yml packages.yml package-lock.yml ./
RUN dbt deps

COPY . .