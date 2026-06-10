{% docs pipeline_runs_status %}

### Pipeline Run Status

The `status` column indicates the final execution state of a pipeline run.  

| Status   | Description                                                             |
|----------|-------------------------------------------------------------------------|
| SUCCESS  | `The pipeline run completed successfully and rows were processed.`      |
| FAILED   | `The pipeline run terminated with an error.`                            | 

{% enddocs %}

{% docs pipeline_runs_rows_processed %}

### Pipeline Run Rows Processed

The `rows_processed` column records the number of rows delivered by a pipeline run.  

- In **dev**, `valid values range between 0 and 250.`  
- In **prod**, `valid values must equal 250.`  

{% enddocs %}

{% docs pipeline_runs_run_success_rate_slo_breached_for_the_day %}

### Daily SLO Breach Flag

The `is_slo_threshold_for_the_day_breached` column indicates whether the daily run success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                       |
|------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_for_the_day < 0.95`          | `The daily success‑rate target (≥=95%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_for_the_day >= 0.95`         | `The daily success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_run_success_rate_slo_breached_over_30_days %}

### Over 30 Days SLO Breach Flag

The `is_slo_threshold_over_30_days_breached` column indicates whether the over 30 days run success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_over_30_days < 0.99`          | `The over 30 days success‑rate target (≥=99%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_over_30_days >= 0.99`         | `The over 30 days success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_runtime_success_rate_in_seconds_slo_breached_for_the_day %}

### Daily SLO Breach Flag

The `is_slo_threshold_for_the_day_breached` column indicates whether the daily runtime success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                       |
|------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_for_the_day < 0.95`          | `The daily success‑rate target (≥=95%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_for_the_day >= 0.95`         | `The daily success‑rate target was met; SLO not breached.`                    |

{% enddocs %}

{% docs pipeline_runs_runtime_success_rate_in_seconds_slo_breached_over_30_days %}

### Over 30 Days SLO Breach Flag

The `is_slo_threshold_over_30_days_breached` column indicates whether the over 30 days runtime success‑rate SLO was breached.  

| Value | Condition                                  | Meaning                                                                               |
|--------------------------------------------------------------------------------------------------------------------------------------------|
| TRUE  | `success_rate_over_30_days < 0.99`          | `The over 30 days success‑rate target (≥=99%) was missed; SLO considered breached.`  |
| FALSE | `success_rate_over_30_days >= 0.99`         | `The over 30 days success‑rate target was met; SLO not breached.`                    |

{% enddocs %}
