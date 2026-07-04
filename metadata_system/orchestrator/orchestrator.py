from concurrent.futures import ThreadPoolExecutor as tpe
from loguru import logger as log
import json
from orchestrator.loader import JobCatalog, JobConfigLoader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner
import time




class Orchestrator:


    def __init__(self):

        pass



    def run_concurrent_job(self, file_path, job_name):

        try:

            log.info("Job Execution Preparations Started...")

            job_cfg_loader = JobConfigLoader(file_path=file_path)

            job_cfg_loader.job_cfg_loader_run()


            validator = Validator(loader=job_cfg_loader)

            validator.validator_run()


        except Exception as preparation_error:

            error_message = str(preparation_error)

            dump = {

                "job_name": job_name,
                "system": None,
                "job_type": None,
                "sub_jobtype": None,
                "error_message": error_message,
                "rows_processed": None 
            }

            print(F"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.error(F"Job Execution: {job_name} | Preparations Failed")

            log.error(F"Details: {error_message}")


        runner = None

        try:

            metadata = Metadata(loader=job_cfg_loader)


            log.info(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: RUNNNG...")


            runner = Runner(metadata=metadata)

            runner.runner_run()


        except Exception as execution_error:

            error_message = str(execution_error)

            job_metadata_dump = metadata.build_job_metadata(
                error_message=error_message,
                rows_processed=(
                    runner.rows_processed
                    if runner and hasattr(runner, 'rows_processed')
                    else None
                )
            )

            print(F"METADATA_DUMP: {job_metadata_dump}")

            log.error(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: FAILED")

            log.error(F"Details: {error_message}")


        else:

            job_metadata_dump = metadata.build_job_metadata(
                error_message=None,
                rows_processed=(
                    runner.rows_processed
                    if runner and hasattr(runner, 'rows_processed')
                    else None
                )
            )

            print(F"METADATA_DUMP: {job_metadata_dump}")

            log.info(F"Job Execution: {metadata.job_name} | System: {metadata.system} | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype} | Status: SUCCESS...")


        time.sleep(5)




if __name__ == '__main__':

    try:

        job_catalog_loader = JobCatalog()

        job_catalog_loader.job_catalog_run()

        
        orchestrator = Orchestrator()


        with tpe(max_workers=5) as executor:

            for job in job_catalog_loader.jobs:

                file_path = job['path']

                job_name = job['job_name']


                future = executor.submit(orchestrator.run_concurrent_job, file_path, job_name)

    
    except Exception:

        raise