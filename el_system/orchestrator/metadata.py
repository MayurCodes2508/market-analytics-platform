from loguru import logger as log


class Metadata:
    def __init__(self, loader, name):

        self.loader = loader

        self.job_cfg = loader.job_cfg

        self.job_name = name

        self.system = "el"

        self.exec_cfg = self.job_cfg["exec"]

        self.metadata_cfg = self.job_cfg.get("metadata", {})

        self.dest_cfg = self.job_cfg.get("dest", {})

        log.info("Metadata Loading Completed...")

        log.info("Obj: metadata | Instance Initialized Successfully...")

    def build_job_metadata(self, job_run_id, status, error_message, rows_processed):

        metadata_dump = {
            "job_run_id": job_run_id,
            "job_name": self.job_name,
            "system": self.system,
            "job_type": self.job_type,
            "sub_jobtype": self.sub_jobtype,
            "status": status,
            "error_message": error_message,
            "rows_processed": rows_processed,
        }

        return metadata_dump


    