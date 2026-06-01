WITH metric_calculation AS (
    SELECT pipeline_name,
           created_at,
           TIMESTAMP_DIFF(end_time, start_time, SECOND) AS runtime_seconds

    FROM {{ref('stg_pipeline_runs') }}
)

    SELECT pipeline_name,
           created_at,
           runtime_seconds,
           COALESCE(runtime_seconds > 60, TRUE) is_runtime_anomaly,

    FROM metric_calculation