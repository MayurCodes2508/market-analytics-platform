from loguru import logger as log
import json





class Metadata:


    def __init__(self, loader):

        self.loader = loader

        self.job_cfg = loader.job_cfg


    def load_metadata(self):

        job_name = self.job_cfg['job_name']

        if not job_name:

            raise ValueError(F"Invalid 'job_name': {job_name}")
            
        self.job_name = job_name


        system = self.job_cfg.get('system', None)

        if not system:

            log.warning("'system' Not Provided, Affected Metadata")

        self.system = system


        job_type = self.job_cfg['job_type']

        if not job_type:

            raise ValueError(F"Invalid 'job_type': {job_type}")
        
        self.job_type = job_type


        sub_jobtype = self.job_cfg.get('sub_jobtype', None)

        if not sub_jobtype:

            log.warning("'sub_jobtype' Not Provided, Affected Metadata")

        self.sub_jobtype = sub_jobtype


    def load_exec_metadata(self):

        exec_cfg = self.job_cfg['exec']

        if not exec_cfg:

            raise ValueError(F"Invalid 'exec_cfg': {exec_cfg}")
        
        self.exec_cfg = exec_cfg
        
        log.info("Successfully Loaded Exec Cfg")


        exec_type = self.exec_cfg['type']

        if not exec_type:

            raise ValueError(F"Invalid 'exec_type': {exec_type}")
        
        self.exec_type = exec_type


        auth_cfg = self.exec_cfg.get('auth')

        if not auth_cfg:

            log.info("Auth Cfg Not Provided, Skipping...")

            return
        
        self.auth_cfg = auth_cfg

        log.info("Successfully Loaded the Exec Type")
        



    def load_dest_metadata(self):

        if self.job_type == 'ingestion':

            dest_cfg = self.job_cfg['destination']

            if not dest_cfg:

                raise ValueError(F"Invalid 'dest_cfg': {dest_cfg}")
            
            self.dest_cfg = dest_cfg

            log.info("Successfully Loaded Dest Cfg")


            dest_type = self.dest_cfg['type']

            if not dest_type:

                raise ValueError(F"Invalid 'dest_type': {dest_type}")
        
            self.dest_type = dest_type

            log.info("Successfully Loaded the Dest Type")


            metadata = self.job_cfg['metadata']

            if not metadata:

                raise ValueError(F"Invalid 'metadata': {metadata}")
            
            self.metadata = metadata

            log.info("Successfully Loaded Job Metadata")
            
        else:

            dest_cfg = self.job_cfg.get('destination')

            if not dest_cfg:

                log.info("Dest Config Not Provided, Skipping Dest")

                return
            
            self.dest_cfg = dest_cfg

            log.info("Successfully Loaded Dest Cfg")

        
            dest_type = self.dest_cfg['type']

            if not dest_type:

                raise ValueError(F"Invalid 'dest_type': {dest_type}")
        
            self.dest_type = dest_type

            log.info("Successfully Loaded the Dest Type")


            metadata = self.job_cfg['metadata']

            if not metadata:

                raise ValueError(F"Invalid 'metadata': {metadata}")
            
            self.metadata = metadata

            log.info("Successfully Loaded Job Metadata")


    def metadata_dump(self, rows_processed, error_message):

        metadata = {

            'job_name': self.job_name,
            'system': self.system,
            'job_type': self.job_type,
            'sub_jobtype': self.sub_jobtype,
            'rows_processed': rows_processed,
            'error_message': error_message

        }

        self.metadata = json.dumps(metadata)


    def metadata_run(self):

        self.load_metadata()

        self.load_exec_metadata()

        self.load_dest_metadata()

    
    def metadata_run_2(self, *args, **kwargs):

        self.metadata_dump(*args, **kwargs)