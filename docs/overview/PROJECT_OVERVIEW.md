# Project Overview

## What this platform does

The Market Analytics Platform ingests cryptocurrency market data from the CoinGecko API and stores it as Parquet files in Google Cloud Storage. The system is designed to support versioned production releases, with `prod_v1` as the current production deployment.

## Core capabilities

- Declarative JSON pipeline configuration
- Schema validation before execution
- API extraction via `ApiExecCommand`
- GCS Parquet ingestion layer
- Run metadata tracking in PostgreSQL
- Metadata ingestion pipeline to BigQuery table `instant-medium-491107-t6.prod_metadata.raw_pipeline_runs`
- dbt models for pipeline observability, SLO reporting, and alert monitoring
- Artifact Registry repository `market-analytics-platform-repository` and GitHub Actions Workload Identity pool `github-actions-pool`
- Environment separation for dev and prod
- Infrastructure defined in Terraform

## Current state

- Production release: `prod_v1`
- Production config: `configs/coingecko_sources/prod/market_price.json`
- Production bucket: `prod-market-analytics-platform-bucket`
- Production Cloud Run job: `prod-market-analytics-platform-run`
- Production dbt job: `prod-dbt-project-run`
- Production metadata pipeline: `prod-metadata-pipeline`
- Production scheduler: `prod-market-analytics-platform-scheduler`
- Production dbt scheduler: `prod-dbt-project-scheduler`
- Production metadata scheduler: `prod-metadata-pipeline-scheduler`

## Why this matters

The system is built to support a SaaS-like release model: dev and prod are isolated, jobs are versioned, and the production deployment path is explicit. `prod_v1` is the first full production delivery of this ingestion pipeline.

## How the pipeline is structured

- `configs/` holds environment-specific ingestion definitions
- `schemas/` defines the contract for valid configs
- `orchestrator/runner.py` drives execution and observability
- `pipeline/exec_cmds/` contains source extraction logic
- `pipeline/destinations/` contains storage logic
- `metadata_pipeline/` loads pipeline run metadata into BigQuery
- `dbt_project/` builds observability, SLO reporting, and alert monitoring models
- `terraform/` contains infrastructure provisioning
