from loguru import logger as log
import json
import os




class Loader:


    def __init__(self, file_path, schema_path):

        self.file_path = file_path
        self.schema_path = schema_path


    def load_config(self):

        if not self.file_path:

            raise ValueError(F"Invalid 'file_path': {self.file_path}")

        try:
        
            with open(self.file_path, 'r') as f:

                self.job_cfg = json.load(f)

                log.info(f"Successfully Loaded Job Config From Path {self.file_path}")

        except FileNotFoundError:

            log.exception(F"File Not Found Error Occured: {self.file_path}")

            raise

        except json.JSONDecodeError:

            log.exception(F"Parsing Error Occured: {self.file_path}")

            raise

        except Exception:

            log.exception(F"Unexpected Error Occured: {self.file_path}")

            raise


    def load_schema(self):

        if not self.schema_path:

            raise ValueError(F"Invalid 'schema_path': {self.schema}")

        try:

            with open(self.schema_path, 'r') as f:

                self.schema_cfg = json.load(f)

                log.info(f"Successfully Loaded JSON Schema From Path {self.schema_path}")

        except FileNotFoundError:

            log.exception(F"File Not Found Error Occured: {self.schema_path}")

            raise

        except json.JSONDecodeError:

            log.exception(F"Parsing Error Occured: {self.schema_path}")

            raise

        except Exception:

            log.exception(F"Unexpected Error Occured: {self.schema}")

            raise


    def load_auth(self, auth_cfg):

        self.auth_cfg = auth_cfg

                     
        api_key = os.getenv(self.auth_cfg['key_env'])

        if not api_key:

            raise ValueError(f"Invalid 'api_key': {api_key}")
            
        log.info("Successfully Loaded Env Creds")

        return api_key


    def loader_run(self):

        self.load_config()

        self.load_schema()