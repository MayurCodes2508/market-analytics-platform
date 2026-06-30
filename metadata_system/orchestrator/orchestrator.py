from loguru import logger as log
import argparse
from orchestrator.loader import Loader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner






if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Run a Job Defined in a JSON Job Cfg File with a Given Schema"
    )

    parser.add_argument(
        "--file_path", help="Required File Path to a JSON Job Cfg", required=True
    )

    parser.add_argument(
        "--schema_path", help="Required Schema Path to a JSON Schema Cfg", required=True
    )

    error_message = None

    try:

        log.info("Job Execution Preparations Started...")


        args = parser.parse_args()


        loader = Loader(file_path=args.file_path, schema_path=args.schema_path)

        loader.loader_run()


        validator = Validator(loader=loader)

        validator.validator_run()


        metadata = Metadata(loader=loader)


        log.info(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: RUNNNG...")


        runner = Runner(metadata=metadata)

        runner.runner_run()


    except Exception as job_error:

        error_message = str(job_error)

        job_metadata_dump = metadata.build_job_metadata(error_message=error_message, rows_processed=runner.rows_processed)

        print(F"METADATA_DUMP: {job_metadata_dump}")

        log.error(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: FAILED | Details: {job_error}")

        raise


    else:

        job_metadata_dump = metadata.build_job_metadata(error_message=None, rows_processed=runner.rows_processed)

        print(F"METADATA_DUMP: {job_metadata_dump}")

        log.info(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: SUCCESS...")

