from loguru import logger as log
import argparse
from orchestrator.loader import Loader
from orchestrator.validator import Validator
from orchestrator.metadata import Pipeline_Metadata
from orchestrator.logger import Pipeline_Logger
from orchestrator.runner import Runner
from datetime import datetime
import os






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run a Pipeline Defined in a JSON File with a Given Schema.")
    parser.add_argument("--file_path", help="Path to the Pipeline Configuration JSON File.", required=True)
    parser.add_argument("--schema_path", help="Path to the JSON Schema File.", required=True)

    args = parser.parse_args()

    error_message = None

    env = os.getenv('ENV')

    if env == 'DEV':
    
        os.makedirs(name='logs', exist_ok=True)

        now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        file_name = F"logs/orchestrator_logs_{now}.log"

        log.add(file_name,
                level="DEBUG",
                format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
                rotation="1 day",
                retention="3 days",
                compression="zip",
                backtrace=True,
                enqueue=True,
                serialize=True,
                diagnose=True,
                colorize=True
                )

    try:

        loader = Loader(args.file_path, args.schema_path)

        loader.loader_run()


        validator = Validator(loader)

        validator.validator_run()


        pipeline_metadata = Pipeline_Metadata(loader)

        pipeline_metadata.metadata_run()


        loader.loader_run_2()


        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run()

        log.info(F"Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_start_status} | Started At: {pipeline_metadata.pipeline_run_start_time} | Total Jobs: {pipeline_metadata.total_jobs}")
         
        runner = Runner(pipeline_metadata, loader)

        runner.runner_run()

    except Exception as pipeline_error:

        error_message = str(pipeline_error)

        pipeline_metadata.metadata_run_2(status='FAILED', error_message=error_message, successful_job_counts=runner.successful_jobs, failed_job_counts=runner.failed_jobs)

        log.warning(F"Execution of Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_end_status} | error_message: {pipeline_metadata.pipeline_run_error_message} | Ended At: {pipeline_metadata.pipeline_run_end_time} | Failed Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['failed_jobs']}")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()

    else:

        log.info("Pipeline Execution Successful")

        pipeline_metadata.metadata_run_2(status='SUCCESS', error_message=error_message, successful_job_counts=runner.successful_jobs, failed_job_counts=runner.failed_jobs)

        log.info(F"Execution of Pipeline: {pipeline_metadata.pipeline_run_name} | Triggered By: {pipeline_metadata.pipeline_run_triggered_by} | Run ID: {pipeline_metadata.pipeline_run_id} | Status: {pipeline_metadata.pipeline_run_end_status} | Ended At: {pipeline_metadata.pipeline_run_end_time} | Successful Jobs Count: {pipeline_metadata.pipeline_run_end_job_counts['successful_jobs']}")

        pipeline_logger = Pipeline_Logger(loader, pipeline_metadata)

        pipeline_logger.logger_run_2()

