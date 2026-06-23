import json
from loguru import logger as log
from dotenv import load_dotenv
import os





class Loader:


    def __init__(self, file_path, schema_path):

        self.file_path = file_path
        self.schema_path = schema_path


    def load_pipeline_cfg(self):

        if not self.file_path:

            raise ValueError(F"Invalid 'file_path': {self.file_path}")
        
        try:

            with open(self.file_path, 'r') as f:

                self.pipeline_cfg = json.load(f)

                log.info(F"Pipeline Config Loaded Successfully From Path: {self.file_path}")

        except FileNotFoundError:

            log.exception(F"File not Found Error Occured: {self.file_path}")

            raise

        except json.JSONDecodeError:

            log.exception(F"Parsing Error Occured: {self.file_path}")

            raise

        except Exception:

            log.exception(F"Unexpected Error Occured: {self.file_path}")

            raise
        

    def load_schema_cfg(self):

        if not self.schema_path:

            raise ValueError(F"Invalid 'schema_path': {self.schema_path}")
        
        try:

            with open(self.schema_path, 'r') as f:

                self.schema_cfg = json.load(f)

                log.info(F"Schema Config Loaded Successfully From Path: {self.schema_path}")

        except FileNotFoundError:

            log.exception(F"File Not Found Error Occured: {self.schema_path}")

            raise

        except json.JSONDecodeError:

            log.exception(F"Parsing Error Occured: {self.schema_path}")

            raise

        except Exception:

            log.exception(F"Unexpected Error Occured: {self.schema_path}")

            raise

    
    def load_db_credentials(self):

        load_dotenv(dotenv_path='../dev.env')

        db_url = os.getenv('DB_URL')

        if not db_url:

            raise ValueError(F"Invalid 'db_url': {db_url}")
        
        self.db_url = db_url

        log.info("Successfully Loaded DB Credentials")


    def loader_run(self):

        self.load_pipeline_cfg()

        self.load_schema_cfg()

    
    def loader_run_2(self):

        self.load_db_credentials()