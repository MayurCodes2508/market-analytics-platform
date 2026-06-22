from loguru import logger as log
from job_executors.exec_cmds.api_exec import ApiExecCommand
from job_executors.destinations.gcs import GCS





class Execution_Command_Factory:


    registry = {
        'ApiExecCommand': ApiExecCommand
    }


    @classmethod
    def get_exec_type(cls, exec_type, *args, **kwargs):

        exec_connector = cls.registry.get(exec_type)

        if not exec_connector:

            raise ValueError(F"Invalid Exec Type: {exec_type}")
        
        return exec_connector(*args, **kwargs)


class Destination_Target_Factory:

    registry = {
        'GCS': GCS
    }


    @classmethod
    def get_dest_type(cls, dest_type, *args, **kwargs):

        if dest_type is None:

            log.info("Dest Not Provided, Skipping...")

            return 

        dest_connect = cls.registry.get(dest_type)

        if not dest_connect:

            raise ValueError(F"Invalid Dest Type: {dest_type}")
        
        return dest_connect(*args, **kwargs )


class Runner:


    def __init__(self, metadata, loader):

        self.metadata = metadata
        self.loader = loader

        self.exec_cfg = self.metadata.exec_cfg
        self.auth_cfg = getattr(self.metadata, 'auth_cfg', {})
        self.dest_cfg = getattr(self.metadata, 'dest_cfg', {})
        self.metadata_cfg = getattr(self.metadata, 'metadata', {})

        self.exec_type = self.metadata.exec_type
        self.job_name = self.metadata.job_name
        self.api_key = getattr(self.loader, 'api_key', None)

        self.dest_type = getattr(self.metadata, 'dest_type', None)
        
    def execute_job(self):

        exec_obj = Execution_Command_Factory.get_exec_type(exec_type=self.exec_type, exec_cfg=self.exec_cfg, job_name=self.job_name, api_key=self.api_key, auth_cfg=self.auth_cfg)

        data, rows_processed = exec_obj.run()


        dest_obj = Destination_Target_Factory.get_dest_type(dest_type=self.dest_type, dest_cfg=self.dest_cfg, metadata_cfg=self.metadata_cfg, job_name=self.job_name, data=data)

        if dest_obj:

            dest_obj.run()

        else:

            log.info("Dest Not Provided, Skipping.....")


    def runner_run(self):

        self.execute_job()