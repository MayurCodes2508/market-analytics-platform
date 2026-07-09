# Market Analytics Platform

## prod_v1 Release Summary

This repository contains the Market Analytics Platform, a production-ready, versioned ingestion pipeline for cryptocurrency market data. The current release is `prod_v1`, modeled after a SaaS-style rollout where development and production are separated, versioned artifacts are published, and infrastructure is managed declaratively.

## What has been delivered

- A config-driven ingestion pipeline using JSON job definitions
- Schema validation to enforce correct pipeline configuration
- API extraction engine in `el_system/job_executors/exec_cmds/api_exec.py`
- Destination engine for Parquet output to Google Cloud Storage in `el_system/job_executors/dests/gcs.py`
- Production ingestion orchestration in `el_system/orchestrator/orchestrator.py`
- Metadata ingestion orchestration in `metadata_system/orchestrator/orchestrator.py`
- Infrastructure setup codified in `terraform/cloud_run.tf`, `terraform/buckets.tf`, and `terraform/scheduler.tf`
- Artifact Registry repository `market-analytics-platform-repository` for container images
- Production Cloud Run jobs for EL ingestion, dbt execution, pipeline orchestration, and metadata ingestion
- dbt models for pipeline observability and SLO reporting in `dbt_transformations/`
- Separate dev and prod configurations, storage, and secrets managed by Terraform

## Current production status

- Released production version: `prod_v1`
- Production config file: `el_system/configs/job/coingecko_sources/prod/market_price.json`
- Production destination bucket: `prod-market-analytics-platform-bucket`
- Production EL ingestion Cloud Run job: `prod-el-system-run`
- Production dbt Cloud Run job: `prod-dbt-transformations-run`
- Production pipeline orchestration Cloud Run job: `prod-pipeline-run`
- Production metadata ingestion Cloud Run job: `prod-metadata-system-run`
- Production scheduler: `prod-pipeline-run-scheduler`
- Production secrets: `prod-market-analytics-platform-coingecko-api-key-secret` and `prod-market-analytics-platform-neon-db-url-secret`

## Release model

This project uses a SaaS-style versioning pattern:

- `dev_...` resources are used for development/testing
- `prod_...` resources are used for production release
- `prod_v1` is the first production artifact version
- Future releases will follow `prod_v2`, `prod_v3`, etc.

## How the platform is organized

- `el_system/orchestrator/orchestrator.py` — ingestion orchestration, validation, and run lifecycle logging
- `el_system/job_executors/exec_cmds/api_exec.py` — API extraction logic
- `el_system/job_executors/dests/gcs.py` — destination persistence logic
- `metadata_system/orchestrator/orchestrator.py` — metadata ingestion orchestration and BigQuery loading
- `metadata_system/job_executors/dests/bq_dest.py` — BigQuery metadata loader
- `dbt_transformations/` — dbt models for pipeline observability, SLO reporting, and analytics artifacts
- `el_system/schemas/root_schema.json` — ingestion job configuration schema
- `el_system/configs/job/coingecko_sources/` — environment-specific EL ingestion jobs
- `terraform/` — infrastructure deployment definitions
- `docs/` — architecture, design, environment, and operational documentation

## How to run locally

Ensure `dev.env` contains `COINGECKO_API_KEY` and `DB_URL`.

Run the ingestion pipeline locally from the `el_system/` folder:

```bash
cd el_system
python -m orchestrator.orchestrator
```

Run the metadata ingestion pipeline locally from the `metadata_system/` folder:

```bash
cd metadata_system
python -m orchestrator.orchestrator
```

Run dbt observability models locally from the `dbt_transformations/` folder:

```bash
cd dbt_transformations
dbt deps
dbt build --target dev
```

## Next planned milestones

- Add reliable retry and backoff for API failures
- Add incremental ingestion and delta loads
- Expand dbt analytics beyond pipeline observability into broader market analytics
- Strengthen automated SLA reporting

## Notes

This release is scoped to ingestion, storage, run tracking, metadata ingestion, and dbt observability. `prod_v1` represents the first production deployment of the platform with a clear path for broader analytics and warehouse transformation releases.
