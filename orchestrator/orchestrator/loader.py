import json
from json import JSONDecodeError
from loguru import logger as log
import os





class Loader:


    def __init__(self, file_path, schema_path):

        self.file_path = file_path

        self.schema_path = schema_path

        log.info("JSON Pipeline & Schema Cfg Paths Loading Completed...")


        log.info("Obj: loader | Instance Initialized Successfully...")


    def load_pipeline_cfg(self):
        
        try:

            with open(file=self.file_path, mode='r') as f:

                self.pipeline_cfg = json.load(fp=f)

                log.info("Pipeline Cfg Loading Completed...")

        except FileNotFoundError:

            log.error(F"File Not Found Error: {self.file_path} | Provide a Valid JSON Pipeline Cfg File Path")

            raise

        except JSONDecodeError as e:

            log.error(F"JSON Parsing/Decoding Error: {self.file_path} | Provide a Valid JSON Format | Details: {e}")

            raise

        except UnicodeDecodeError:

            log.error(F"Unicode Decoding Error: {self.file_path} | Expected UTF-8")

            raise

        except Exception:

            log.exception(F"Unknown Error Occured While Loading Pipeline Cfg: {self.file_path}")

            raise
        

    def load_schema_cfg(self):

        try:

            with open(file=self.schema_path, mode='r') as f:

                self.schema_cfg = json.load(fp=f)

                log.info("Schema Cfg Loading Completed...")

        except FileNotFoundError:

            log.error(F"File Not Found Error: {self.schema_path} | Provide a Valid JSON Schema Cfg File Path")

            raise

        except JSONDecodeError as e:

            log.error(F"JSON Parsing/Decoding Error: {self.schema_path} | Provide Valid JSON Format | Details: {e}")

            raise

        except UnicodeDecodeError:

            log.error(F"Unicode Decoding Error: {self.schema_path} | Expected UTF-8")

            raise

        except Exception:

            log.exception(F"Unknown Error Occured While Loading Schema Cfg: {self.schema_path}")

            raise

    
    def load_db_creds(self):

        db_url = os.getenv('NEON_DB_URL')

        if not db_url:

            raise ValueError(F"Invalid or Missing 'db_url': {db_url} | Provide a Valid DB Url")
        
        self.db_url = db_url

        log.info("DB Creds Loading Completed...")


    def loader_run(self):

        self.load_pipeline_cfg()

        self.load_schema_cfg()

    
    def loader_run_2(self):

        self.load_db_creds()