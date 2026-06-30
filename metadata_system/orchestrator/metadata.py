from loguru import logger as log
import json





class Metadata:


    def __init__(self, loader):
        
        self.loader = loader



        self.job_cfg = loader.job_cfg

        self.job_name = self.job_cfg['job_name']

        self.system = self.job_cfg['system']

        self.job_type = self.job_cfg['job_type']

        self.sub_jobtype = self.job_cfg['sub_jobtype']

        self.exec_cfg = self.job_cfg['exec']

        self.metadata_cfg = self.job_cfg.get('metadata', {})

        self.dest_cfg = self.job_cfg.get('dest', {})


        log.info("Metadata Loading Completed...")


        log.info("Obj: metadata | Instance Initialized Successfully...")


    def build_job_metadata(self, error_message, rows_processed):

        metadata_dump = {

            "job_name": self.job_name,
            "system": self.system,
            "job_type": self.job_type,
            "sub_jobtype": self.sub_jobtype,
            "error_message": error_message,
            "rows_processed": rows_processed

        }


        json_payload = json.dumps(
            obj=metadata_dump
        )

        if not json_payload:

            raise ValueError(F'JSON Payload is a Required Field: {json_payload}')
        
        return json_payload