# Execution Engine

## Overview

The Execution Engine orchestrates pipeline jobs by loading configs, validating them, dispatching execution commands, and tracking run metadata.

## Responsibilities

- Load JSON job configuration
- Load and validate against the JSON schema
- Load environment credentials
- Create and execute the API command
- Create and run the destination persistence layer
- Track run metadata in PostgreSQL

## Implementation

The main runner is in `orchestrator/runner.py`.

### Execution flow

1. `load_config()` reads the job configuration
2. `load_schema()` reads the schema definition
3. `validate_config()` enforces config correctness
4. `load_env_credentials()` loads secrets from an environment file
5. `insert_run_metadata()` records the job start state
6. `execute_execcmd()` creates the `ApiReadExecCommand`
7. `execute_destination()` creates the GCS destination object
8. `update_run_metadata()` writes final status and record counts

## Design

The runner separates orchestration from execution logic. Execution commands are pluggable, enabling future support for additional data sources without changing the core runner.

## Current status

The runner supports `ApiReadExecCommand` in `prod_v1` and writes ingestion metadata to PostgreSQL. It uses `dev.env` locally for secrets, while production is designed to use secret manager values in Terraform.
