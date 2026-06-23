    except Exception as pipeline_error:

        pipeline_metadata.metadata_run_2(status='FAILED', error_message=str(pipeline_error), successful_job_counts=successful_jobs, failed_job_counts=failed_jobs)

        log.warning(F"Execution of Pipeline {pipeline_metadata.pipeline_run_name}, (Triggered_by: {pipeline_metadata.pipeline_run_triggered_by}), Run ID (ID: {pipeline_metadata.pipeline_run_id}) Ended with Status {pipeline_metadata.pipeline_run_status} Due to {pipeline_metadata.error_message} at {pipeline_metadata.pipeline_run_end_time}")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()

    else:

        log.info("Pipeline Execution Successful")

        pipeline_metadata.metadata_run_2(status='SUCCESS', error_message=None, successful_job_counts=successful_jobs, failed_job_counts=failed_jobs)

        log.info(F"Execution of Pipeline {pipeline_metadata.pipeline_run_name}, (Triggered_by: {pipeline_metadata.pipeline_run_triggered_by}), Run ID (ID: {pipeline_metadata.pipeline_run_id}) Ended with Status {pipeline_metadata.pipeline_run_status} at {pipeline_metadata.pipeline_run_end_time}")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()