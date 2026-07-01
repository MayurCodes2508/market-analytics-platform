from loguru import logger as log
from orchestrator.loader import JobCatalog, JobConfigLoader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner
import time






if __name__ == '__main__':

    job_catalog_loader = JobCatalog()

    job_catalog_loader.job_catalog_run()


    for job in job_catalog_loader.jobs:

        file_path = job['path']

        error_message = None


        try:

            job_cfg_loader = JobConfigLoader(file_path=file_path)

            job_cfg_loader.job_cfg_loader_run()


            log.info("Job Execution Preparations Started...")



            validator = Validator(loader=job_cfg_loader)

            validator.validator_run()


            metadata = Metadata(loader=job_cfg_loader)


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

        time.sleep(5)