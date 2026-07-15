{{
  config(
    tags=['prod'],
    )
}}



SELECT run_id,
       trim(pipeline_name) AS pipeline_name,
       trim(status) AS status,
       start_time,
       end_time,
       created_at,
       trim(triggered_by) AS triggered_by,
       trim(error_message) AS error_message,
       job_counts,
       ingestion_ts

FROM {{ source('metadata', 'raw_pipeline_runs') }}

QUALIFY row_number() OVER(PARTITION BY run_id ORDER BY ingestion_ts) = 1