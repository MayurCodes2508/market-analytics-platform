SELECT run_id,
       TRIM(pipeline_name) AS pipeline_name,
       TRIM(job_name) AS job_name,
       TRIM(job_type) AS job_type,
       rows_processed,
       TRIM(error_message) AS error_message,
       TRIM(status) AS status,
       start_time,
       end_time,
       created_at,
       ingestion_ts
FROM {{ source('metadata', 'raw_pipeline_runs') }}
QUALIFY ROW_NUMBER() OVER(PARTITION BY run_id ORDER BY ingestion_ts DESC) = 1