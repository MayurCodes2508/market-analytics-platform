from loguru import logger as log
from uuid6 import uuid7 as uid
from subprocess import run as sp, CalledProcessError as spe
import json
import sys
from concurrent.futures import ThreadPoolExecutor as tpe
from el_system.orchestrator.loader import JobCatalog


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

    def run_concurrent_jobs(self, path, job_name):

        try:
            result = sp(
                [
                    sys.executable,
                    "-u",
                    "-m",
                    "el_system.orchestrator.executor",
                    "--job_name",
                    str(object=job_name),
                    "--file_path",
                    str(object=path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            log.info(result.stdout)

        except spe as e:
            if e.stderr:
                log.error(f"{e.stderr}")

            if e.stdout:
                log.error(f"{e.stdout}")


if __name__ == "__main__":
    try:
        job_catalog_loader = JobCatalog()

        job_catalog_loader.job_catalog_run()

    except Exception as load_err:
        log.critical("System: el | Failed to Load Job Catalog, Aborting Job Executions")

        log.error(f"Details: {str(object=load_err)}")

        raise

    try:
        log.info("All Job Executions Started...")

        orchestrator = Orchestrator()

        with tpe(max_workers=5) as executor:
            for job in job_catalog_loader.jobs:
                future = executor.submit(
                    orchestrator.run_concurrent_jobs, job["path"], job["job_name"]
                )

        log.info("All Job Executions Completed...")

    except Exception as strt_err:
        for job in job_catalog_loader.jobs:
            dump = {
                "job_run_id": str(object=uid()),
                "job_name": job.get("job_name"),
                "system": "el",
                "job_type": None,
                "sub_jobtype": None,
                "status": "FAILED",
                "error_message": str(object=strt_err),
                "rows_processed": None,
            }

            log.info(f"METADATA_DUMP: {json.dumps(obj=dump)}")

        log.critical(
            "System: el | Failed to Start the Thread Pool Executor, Aborting Job Executions"
        )

        log.error(f"Details: {str(object=strt_err)}")

        raise
