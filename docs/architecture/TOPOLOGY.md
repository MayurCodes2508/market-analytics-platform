# Architecture Topology

## System topology

The platform is structured as a modular pipeline from configuration to storage:

- Job configuration in JSON
- Schema validation layer
- Execution engine and command dispatch
- Destination persistence to GCS
- Data lake landing zone
- Data warehouse planning and dbt transformations
- Analytics layer

## Pipeline stages

### 1. Configuration

Jobs are defined in `configs/coingecko_sources/*.json` and describe:

- source metadata
- API endpoint settings
- pagination and page size
- authentication details
- destination storage settings

### 2. Validation

Job configs are validated against `schemas/api_exec_schema.json` before execution.

### 3. Execution

The `Runner` loads the validated config and dispatches `ApiReadExecCommand` to fetch market data.

### 4. Destination

Extraction results are converted to Parquet and written to GCS using the configured path template.

### 5. Observability

Run metadata is inserted and updated in PostgreSQL to track status, start/end times, and record counts.

## Deployment topology

- Dev and prod environments are separated with distinct configs and storage
- Production uses a Cloud Run job image tagged `prod_v1`
- Production is scheduled hourly via Cloud Scheduler
- Secrets are managed in Google Secret Manager
