from loguru import logger as log
import json
from json import JSONDecodeError






class Loader:


    def __init__(self, file_path, schema_path):
        
        self.file_path = file_path

        self.schema_path = schema_path


        log.info("JSON Job & Schema Cfg Paths Loading Completed...")


        log.info("Obj: loader | Instance Initialized Successfully...")


    def load_job_cfg(self):

        try:

            with open(file=self.file_path, mode='r') as f:

                self.job_cfg = json.load(fp=f)

                log.info("Job Cfg Loading Completed...")

        except FileNotFoundError:

            log.error(F"File Not Found Error: {self.file_path} | Provide a Valid JSON Job Cfg File Path")

            raise

        except JSONDecodeError as e:

            log.error(F"JSON Parsing/Decoding Error: {self.file_path} | Provide Valid JSON Format | Details: {e}")

            raise

        except UnicodeDecodeError:

            log.error(F"Unicode Decoding Error: {self.file_path} | Expected UTF-8")

            raise

        except Exception:

            log.exception(F"Unknown Error Occured While Loading Job Cfg: {self.file_path}")

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

            log.error(F"Parsing/Decoding Error: {self.schema_path} | Provide Valid JSON Format | Details: {e}")

            raise

        except UnicodeDecodeError:

            log.error(F"Unicode Decoding Error: {self.schema_path} | Expected UTF-8")

            raise

        except Exception:

            log.exception(F"Unknown Error Occured While Loading Schema Cfg: {self.schema_path}")

            raise


    def loader_run(self):

        self.load_job_cfg()

        self.load_schema_cfg()