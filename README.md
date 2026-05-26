# Market Analytics Platform

## prod_v1 Release Summary

This repository contains the Market Analytics Platform, a production-ready, versioned ingestion pipeline for cryptocurrency market data. The current release is `prod_v1`, modeled after a SaaS-style rollout where development and production are separated, versioned artifacts are published, and infrastructure is managed declaratively.

## What has been delivered

- A config-driven ingestion pipeline using JSON job definitions
- Schema validation to enforce correct pipeline configuration
- API extraction engine in `pipeline/exec_cmds/api_exec.py`
- Destination engine for Parquet output to Google Cloud Storage in `pipeline/destinations/gcs.py`
- Production orchestration and run tracking in `orchestrator/runner.py`
- Infrastructure setup codified in `terraform/main.tf`
- Production Cloud Run job image tagged `market-job:prod_v1`
- Hourly Cloud Scheduler deployment for production ingestion
- Separate dev and prod configurations, storage, and secrets

## Current production status

- Released production version: `prod_v1`
- Production config file: `configs/coingecko_sources/prod_market_price.json`
- Production destination bucket: `prod-market-analytics-platform-bucket`
- Production Cloud Run job: `prod-market-analytics-platform-run`
- Production scheduler: `prod-market-analytics-platform-scheduler`
- Production secret: `prod-market-analytics-platform-secret`

## Release model

This project uses a SaaS-style versioning pattern:

- `dev_...` resources are used for development/testing
- `prod_...` resources are used for production release
- `prod_v1` is the first production artifact version
- Future releases will follow `prod_v2`, `prod_v3`, etc.

## How the platform is organized

- `orchestrator/runner.py` — main runner, schema validation, run metadata tracking
- `pipeline/exec_cmds/api_exec.py` — API extraction logic
- `pipeline/destinations/gcs.py` — destination persistence logic
- `schemas/api_exec_schema.json` — job configuration schema
- `configs/coingecko_sources/` — environment-specific ingestion jobs
- `terraform/` — infrastructure deployment definitions
- `docs/` — architecture, design, environment, and operational documentation

## How to run locally

```bash
python -m orchestrator.runner --file_path configs/coingecko_sources/dev_market_price.json --schema_path schemas/api_exec_schema.json
```

## Next planned milestones

- Add reliable retry and backoff for API failures
- Add incremental ingestion and delta loads
- Add downstream warehouse integration with BigQuery or dbt
- Add monitoring, alerting, and SLA reporting

## Notes

This release is scoped to ingestion, storage, and run tracking. `prod_v1` represents the first production deployment of the platform with a clear path for future analytics and transformation releases.
