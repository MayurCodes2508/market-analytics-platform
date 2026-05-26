# Warehouse Layer

## Overview

The Warehouse layer represents the planned analytics staging area after ingestion. In `prod_v1`, the architecture prepares for a warehouse layer, even though the current implementation stops at the GCS landing zone.

## Intended workflow

1. Ingest raw Parquet files into GCS
2. Load or transform data into BigQuery
3. Model data across Bronze, Silver, and Gold layers
4. Enable analytics and reporting

## Current state

- `prod_v1` currently writes to a GCS data lake
- `dbt_project/` exists as a placeholder for future warehouse transformations
- The architecture is ready for downstream analytics but does not yet implement full warehouse load logic
