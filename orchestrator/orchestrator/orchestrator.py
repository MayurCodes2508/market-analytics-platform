from loguru import logger as log
import argparse
from orchestrator.loader import Loader
from orchestrator.validator import Validator
from orchestrator.metadata import Pipeline_Metadata
from orchestrator.logger import Pipeline_Logger
from orchestrator.runner import Runner






if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Run a Pipeline Defined in a JSON Pipeline Cfg File with a Given Schema"
    )

    parser.add_argument(
        "--file_path", help="Required File Path to a JSON Pipeline Cfg", required=True
    )

    parser.add_argument(
        "--schema_path", help="Required Schema Path to a JSON Schema Cfg", required=True
    )
        

    error_message = None

    status = "FAILED"
        
    try:

        args = parser.parse_args()

        loader = Loader(args.file_path, args.schema_path)

        loader.loader_run()


        validator = Validator(loader)

        validator.validator_run()


        pipeline_metadata = Pipeline_Metadata(loader)

        pipeline_metadata.metadata_run()


        loader.loader_run_2()


        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run()


        log.info(F"Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_start_status} | Started At: {pipeline_metadata.pipeline_run_start_time} | Total Jobs: {pipeline_metadata.total_jobs}...")
         

        runner = Runner(pipeline_metadata, loader)

        runner.runner_run()

    except Exception as pipeline_error:

        error_message = str(pipeline_error)

        pipeline_metadata.metadata_run_2(status=status, error_message=error_message, successful_job_counts=runner.successful_jobs, failed_job_counts=runner.failed_jobs)

        log.warning(F"Execution of Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_end_status} | error_message: {pipeline_metadata.pipeline_run_error_message} | Ended At: {pipeline_metadata.pipeline_run_end_time} | Successful Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['successful_jobs']} | Failed Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['failed_jobs']}...")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()

    else:

        status = "SUCCESS"

        pipeline_metadata.metadata_run_2(status=status, error_message=error_message, successful_job_counts=runner.successful_jobs, failed_job_counts=runner.failed_jobs)

        log.info(F"Execution of Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_end_status} | Ended At: {pipeline_metadata.pipeline_run_end_time} | Successful Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['successful_jobs']} | Failed Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['failed_jobs']}...")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()

