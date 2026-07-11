from concurrent.futures import ThreadPoolExecutor as tpe
from loguru import logger as log
from uuid6 import uuid7 as uid
import json
from orchestrator.loader import JobCatalog, JobConfigLoader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner


class Orchestrator:
    def __init__(self):

        pass

    def run_concurrent_job(self, fp, job_name):

        try:
            job_run_id = str(uid())

            log.info(f"Job: {job_name} | ID: {job_run_id} | System: el | Created...")

            job_cfg_loader = JobConfigLoader(fp=fp)

            job_cfg_loader.job_cfg_loader_run()
        
        except Exception as load_err:

            dump = {
                "job_run_id": job_run_id,
                "job_name": job_name,
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=load_err),
                "rows_processed": None
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.error(
                f"Job: {job_name} | ID: {job_run_id} | System: el | Job Cfg Loading Failed"
            )

            log.error(f"Details: {str(object=load_err)}")

            return

        
        try:

            validator = Validator(loader=job_cfg_loader)

            validator.validator_run()

        except Exception as valid_err:

            dump = {
                "job_run_id": job_run_id,
                "job_name": job_name,
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=valid_err),
                "rows_processed": None
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.error(
                f"Job Execution: {job_name} | ID: {job_run_id} | System: el | Job Cfg Validation Failed"
            )

            log.error(f"Details: {str(object=valid_err)}")

            return
        

        try:
            metadata = Metadata(loader=job_cfg_loader, name=job_name)

            log.info(
                f"Job Execution: {job_name} | ID: {job_run_id} | System: el | RUNNING..."
            )

        except Exception as meta_err:

            log.error(f"Job Execution: {job_name} | ID: {job_run_id} | System: el | Job Metadata Building Failed")

            log.error(f"Details: {str(object=meta_err)}")


        try:

            runner = Runner(metadata=metadata)

            runner.runner_run()

        except Exception as execution_error:
            error_message = str(execution_error)

            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=job_run_id,
                status="FAILED",
                error_message=error_message,
                rows_processed=getattr(runner, "rows_processed", None),
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.error(
                f"Job Execution: {metadata.job_name} | ID: {job_run_id} | System: el | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype}"
            )

            log.error(f"Details: {error_message}")

        else:
            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=job_run_id,
                status="SUCCESS",
                error_message=None,
                rows_processed=getattr(runner, "rows_processed", None),
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.success(
                f"Job Execution: {metadata.job_name}| ID: {job_run_id} | System: el | Job Type: {metadata.job_type} | Sub JobType: {metadata.sub_jobtype}"
            )


if __name__ == "__main__":

    try:

        job_catalog_loader = JobCatalog()

        job_catalog_loader.job_catalog_run()


    except Exception as load_err:

        log.critical("System: el | Failed to Load Job Catalog, Aborting Job Executions")

        log.error(f"Details: {str(object=load_err)}")

        raise

    
    try:

        orchestrator = Orchestrator()

        with tpe(max_workers=5) as executor:

            paths = [job['path'] for job in job_catalog_loader.jobs]

            names = [job['job_name'] for job in job_catalog_loader.jobs]

            results = list(executor.map(
                orchestrator.run_concurrent_job,
                paths,
                names
            ))

        log.info("All Job Executions Completed...")

    except Exception as strt_err:
        
        for job in job_catalog_loader.jobs:

            dump = {
                "job_run_id": str(object=uid()),
                "job_name": job.get('job_name'),
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=strt_err),
                "rows_processed": None
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")


        log.critical("System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions")

        log.error(f"Details: {str(object=strt_err)}")
        
        raise
