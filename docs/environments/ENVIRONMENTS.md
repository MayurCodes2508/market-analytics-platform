# Environments

## Supported environments

The project supports two separate environments:

- `dev`
- `prod`

Each environment uses dedicated configuration, storage, and runtime resources.

## Environment-specific configs

- Dev job config: `configs/coingecko_sources/dev_market_price.json`
- Prod job config: `configs/coingecko_sources/prod_market_price.json`

## Environment differences

- Dev uses `dev-market-analytics-platform-bucket` and `layer = dev`
- Prod uses `prod-market-analytics-platform-bucket` and `layer = staging`
- Prod is deployed with `market-job:prod_v1`
- Dev is expected to use `market-job:latest`

## Secrets and credentials

- Local development uses `dev.env` for `COINGECKO_API_KEY` and `DB_URL`
- Production is provisioned to use Google Secret Manager via Terraform

## Current status

`prod_v1` is the current production environment release. Dev remains isolated so testing can continue without affecting production resources.
