from loguru import logger as log


class Metadata:
    def __init__(self):

        pass

    def build_job_metadata(self, job_run_id, job_name, status, error_message, rows_processed):

        metadata_dump = {
            "job_run_id": job_run_id,
            "job_name": job_name,
            "system": "el",
            "job_type": None,
            "sub_jobtype": None,
            "status": status,
            "error_message": error_message,
            "rows_processed": rows_processed,
        }

        log.info("Metadata Building Completed...")

        return metadata_dump


    