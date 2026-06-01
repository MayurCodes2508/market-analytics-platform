WITH metric_calculation AS (
    SELECT pipeline_name,
           created_at,
           TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(IF(status='SUCCESS', end_time, NULL)), MINUTE) AS freshness_minutes
    
    FROM {{ ref('stg_pipeline_runs') }}

    GROUP BY 1, 2
)

    SELECT pipeline_name,
           created_at,
           freshness_minutes,
           COALESCE(freshness_minutes > 90, TRUE) AS is_freshness_anomaly
    
    FROM metric_calculation