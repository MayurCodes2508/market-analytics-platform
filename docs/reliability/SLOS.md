# Service Level Objectives (SLOs)

## Overview

SLOs define the reliability targets for production ingestion in `prod_v1`.

## Current objectives

- **Job success rate**: target 95%+ for hourly production runs
- **Data availability**: ingestion files should be available shortly after run completion
- **Error visibility**: all failures should be captured in run metadata

## Observability

Run tracking stores:

- `run_id`
- `pipeline_name`
- `job_name`
- `job_type`
- `status`
- `rows_processed`
- `error_message`
- `start_time`
- `end_time`
- `created_at`

## Failure handling

- The runner marks a run as `RUNNING` before execution
- On error, the final run status is updated to `FAILED`
- Error messages are persisted for debugging

## Current status

The `prod_v1` release is built on structured run tracking and hourly scheduled execution. Future releases should add alerting and automated SLA reporting.
