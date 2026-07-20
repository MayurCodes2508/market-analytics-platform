from concurrent.futures import ThreadPoolExecutor as tpe
from loguru import logger as log
from uuid6 import uuid7 as uid
import json
from orchestrator.loader import JobCatalog, JobConfigLoader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner
import sys


log.remove()

log.add(
    sink=sys.stdout,
    filter=lambda record: (
        record["level"].name
        in {"INFO", "SUCCESS", "ERROR", "WARNING", "DEBUG", "TRACE"}
    ),
)

log.add(sink=sys.stderr, filter=lambda record: record["level"].name == "CRITICAL")


class Orchestrator:
    def __init__(self):

        pass

    def run_concurrent_job(self, fp, job_name):

        try:
            job_run_id = str(uid())

            log.info(
                f"Job: {job_name} | ID: {job_run_id} | System: metadata | CREATED..."
            )

            job_cfg_loader = JobConfigLoader(fp=fp)

            job_cfg_loader.job_cfg_loader_run()

        except Exception as load_err:
            dump = {
                "job_run_id": job_run_id,
                "job_name": job_name,
                "system": "metadata",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=load_err),
                "job_metrics": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.error(
                f"Job: {job_name} | ID: {job_run_id} | System: metadata | Job Cfg Loading Failed"
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
                "system": "metadata",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=valid_err),
                "job_metri": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

            log.error(
                f"Job Execution: {job_name} | ID: {job_run_id} | System: metadata | Job Cfg Validation Failed"
            )

            log.error(f"Details: {str(object=valid_err)}")

            return

        log.info(
            f"Job Execution: {job_name} | ID: {job_run_id} | System: metadata | RUNNING..."
        )

        try:
            runner = Runner(loader=job_cfg_loader)

            runner.runner_run()

        except Exception as exec_err:
            metadata = Metadata(loader=job_cfg_loader)

            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=job_run_id,
                job_name=job_name,
                status="FAILED",
                error_message=str(object=exec_err),
                job_metrics=getattr(runner, "job_metrics", None)
                if runner
                else None,
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.error(
                f"Job Execution: {job_name} | ID: {job_run_id} | System: metadata | Job Type: {job_metadata_dump['job_type']} | Sub JobType: {job_metadata_dump['sub_jobtype']}"
            )

            log.error(f"Details: {str(object=exec_err)}")

        else:
            metadata = Metadata(loader=job_cfg_loader)

            metadata.get_metadata()

            job_metadata_dump = metadata.build_job_metadata(
                job_run_id=job_run_id,
                job_name=job_name,
                status="SUCCESS",
                error_message=None,
                job_metrics=getattr(runner, "job_metrics", None)
                if runner
                else None,
            )

            log.info(f"METADATA_DUMP: {json.dumps(obj=job_metadata_dump)}")

            log.success(
                f"Job Execution: {job_name} | ID: {job_run_id} | System: metadata | Job Type: {job_metadata_dump['job_type']} | Sub JobType: {job_metadata_dump['sub_jobtype']}"
            )


if __name__ == "__main__":
    try:
        job_catalog_loader = JobCatalog()

        job_catalog_loader.job_catalog_run()

    except Exception as load_err:
        log.critical(
            "System: metadata | Failed to Load Job Catalog, Aborting Job Executions"
        )

        log.error(f"Details: {str(object=load_err)}")

        raise

    try:
        log.info("All Job Executions Started...")

        orchestrator = Orchestrator()

        with tpe(max_workers=5) as executor:
            for job in job_catalog_loader.jobs:
                future = executor.submit(
                    orchestrator.run_concurrent_job, job["path"], job["job_name"]
                )

        log.info("All Job Executions Completed...")

    except Exception as strt_err:
        for job in job_catalog_loader.jobs:
            dump = {
                "job_run_id": str(object=uid()),
                "job_name": job.get("job_name"),
                "system": "metadata",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=strt_err),
                "job_metrics": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

        log.critical(
            "System: metadata | Failed to Start the Thread Pool Executor, Aborting Job Executions"
        )

        log.error(f"Details: {str(object=strt_err)}")

        raise
