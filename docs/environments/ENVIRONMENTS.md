# Environments

## Supported environments

The project supports two separate environments:

- `dev`
- `prod`

Each environment uses dedicated configuration, storage, and runtime resources.

## Environment-specific configs

- Dev job config: `configs/coingecko_sources/dev/market_price.json`
- Prod job config: `configs/coingecko_sources/prod/market_price.json`

## Environment differences

- Dev uses `dev-market-analytics-platform-bucket` and `layer = dev`
- Prod uses `prod-market-analytics-platform-bucket` and `layer = staging`
- Dev ingestion runs via `dev-market-analytics-platform-run` using `market-job:latest`
- Dev dbt execution runs via `dev-dbt-project-run` using `dbt-job:latest`
- Dev metadata ingestion is provisioned as `dev-metadata-pipeline`
- Prod ingestion runs via `prod-market-analytics-platform-run` using `market-job:prod_v1`
- Prod dbt execution runs via `prod-dbt-project-run` using `dbt-job:prod_v1`
- Prod metadata ingestion runs via `prod-metadata-pipeline`
- Prod uses Cloud Scheduler for ingestion, dbt, and metadata execution

## Secrets and credentials

- Local development uses `dev.env` for `COINGECKO_API_KEY` and `DB_URL`
- Production is provisioned to use Google Secret Manager via Terraform

## Current status

`prod_v1` is the current production environment release. Dev remains isolated so testing can continue without affecting production resources.
