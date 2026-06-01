# Architecture Topology

## System topology

The platform is structured as a modular pipeline from configuration to storage and observability:

- Job configuration in JSON
- Schema validation layer
- Execution engine and command dispatch
- Destination persistence to GCS
- Run metadata capture in PostgreSQL
- Metadata ingestion to BigQuery
- Downstream dbt artifacts and analytics layer

## Pipeline stages

### 1. Configuration

Jobs are defined in `configs/coingecko_sources/*.json` and describe:

- source metadata
- API endpoint settings
- pagination and page size
- authentication details
- destination storage settings

### 2. Validation

- Job configs are validated against `schemas/root_schema.json` before execution.

### 3. Execution

The `Runner` loads the validated config and dispatches `ApiExecCommand` to fetch market data.

### 4. Destination

Extraction results are converted to Parquet and written to GCS using the configured path template.

### 5. Metadata pipeline

Run metadata is loaded from PostgreSQL into BigQuery using `metadata_pipeline/main.py`.

### 6. Observability and reporting

A dbt project consumes the loaded run metadata and builds pipeline observability, SLO reporting, and alert monitoring artifacts.

## Deployment topology

- Dev and prod environments are separated with distinct configs and storage
- Production uses a Cloud Run job image tagged `prod_v1`
- Production also includes a Cloud Run dbt job and Cloud Function metadata pipeline
- Production is scheduled hourly via Cloud Scheduler for ingestion, dbt model execution, and metadata ingestion
- Secrets are managed in Google Secret Manager
