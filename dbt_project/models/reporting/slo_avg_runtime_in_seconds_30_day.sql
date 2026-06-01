WITH metric_calculation AS (
    SELECT pipeline_name,
           EXTRACT(DATE FROM created_at) AS created_at,
           ROUND(AVG(TIMESTAMP_DIFF(end_time, start_time, SECOND)), 2) AS avg_runtime_seconds

    FROM {{ ref('stg_pipeline_runs') }}

    GROUP BY 1, 2
),

boolean_flags AS (
    SELECT pipeline_name,
           created_at,
           avg_runtime_seconds,
           COALESCE(avg_runtime_seconds > 60, TRUE) AS is_slo_threshold_breached

    FROM metric_calculation
),

rolling_30_day_calculation AS (
    SELECT pipeline_name,
           created_at,
           avg_runtime_seconds,
           is_slo_threshold_breached,
           SAFE_DIVIDE(
            COUNTIF(is_slo_threshold_breached = FALSE) OVER(PARTITION BY pipeline_name ORDER BY UNIX_DATE(created_at) RANGE BETWEEN 30 PRECEDING AND CURRENT ROW),
            COUNT(*) OVER(PARTITION BY pipeline_name ORDER BY UNIX_DATE(created_at) RANGE BETWEEN 30 PRECEDING AND CURRENT ROW)
           ) * 100 AS rolling_30_day_slo_percentage
    
    FROM boolean_flags
)

    SELECT pipeline_name,
           created_at,
           avg_runtime_seconds,
           is_slo_threshold_breached,
           rolling_30_day_slo_percentage,
           (rolling_30_day_slo_percentage >= 99.00) AS is_slo_met_for_day
    
    FROM rolling_30_day_calculation

    ORDER BY created_at DESC