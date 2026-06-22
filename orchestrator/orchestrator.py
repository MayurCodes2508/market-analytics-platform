from loguru import logger as log
import argparse
from loader import Loader
from validator import Validator
from metadata import Pipeline_Metadata
from metadata import Job_Metadata
from logger import Pipeline_Logger
from logger import Job_Logger
from runner import Runner
import psutil




process = psutil.Process()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run a Pipeline Defined in a JSON File with a Given Schema.")
    parser.add_argument("--file_path", help="Path to the Pipeline Configuration JSON File.", required=True)
    parser.add_argument("--schema_path", help="Path to the JSON Schema File.", required=True)

    args = parser.parse_args()

    try:

        loader = Loader(args.file_path, args.schema_path)

        loader.loader_run()


        validator = Validator(loader)

        validator.validator_run()

    except Exception:

        log.exception("Error Loading and Validating")

        raise
    

    pipeline_metadata = Pipeline_Metadata(loader)

    pipeline_metadata.metadata_run()

    loader.loader_run_2()


    pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

    pipeline_logger.logger_run()

    log.info(F"Execution of Pipeline {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_name']}, (Triggered_by: {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_triggered_by']}), Run ID (ID: {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_id']}) Started with Status {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_status']} at {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_start_time']} with Total Jobs: {pipeline_metadata.pipeline_start_metadata_dump['pipeline_run_job_counts']['total_jobs']}")

    # ===============================================================================
    # Pipeline Executions Block:
    # ===============================================================================

    try:

        # ===============================================================================
        # Jobs Executions Block:
        # ===============================================================================

        log.info("All Jobs Executions Started")

        successful_jobs = 0
        failed_jobs = 0

        try:

            for job in pipeline_metadata.run_jobs:

                job_name = job['job_name']

                if not job_name:

                    raise ValueError(F"Invalid 'job_name': {job_name}")
                
                
                runner = Runner(job_name)

                runner.run()

                try:


                    job_metadata = Job_Metadata(runner.operation, job_name, runner.job_run_id, pipeline_metadata.pipeline_run_id)

                    job_metadata.metadata_run_2()


                    job_logger = Job_Logger(loader, job_metadata)

                    job_logger.logger_run()

                    failed_count, successful_count = pipeline_metadata.collect_job_counts(job_metadata.job_metadata_dump.get('job_status', None))
                                                                                                                             

                    successful_jobs += successful_count
                    failed_jobs += failed_count

                except Exception:

                    log.exception("Unexpected Error Occured, Affecting Pipeline/Job Metadata")

        except Exception:

            log.exception("Unexpected Error Occured")

            raise

        # ===============================================================================

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

    # ===============================================================================