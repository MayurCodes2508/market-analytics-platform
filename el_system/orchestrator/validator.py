from loguru import logger as log
import jsonschema_rs
from jsonschema_rs import ValidationError
from pathlib import Path





class Validator:


    def __init__(self, loader):

        self.loader = loader

        self.schema_path = loader.schema_path

        self.job_cfg = loader.job_cfg
        self.schema_cfg = loader.schema_cfg


    def validate_config(self):

        if not self.job_cfg:

            raise ValueError(F"Invalid 'job_config': {self.job_cfg}")
        
        if not self.schema_cfg:

            raise ValueError(F"Invalid 'schema_config': {self.schema_cfg}")

        try:

            full_uri = Path(self.schema_path).resolve().as_uri()

            validator = jsonschema_rs.validator_for(self.schema_cfg, base_uri=full_uri)

            validator.validate(self.job_cfg)

            log.info(f"Configuration Validated Against Schema {self.schema_path}")

        except ValidationError:

            log.exception(F"Validation Error Occured: {self.schema_path}")

            raise

        except Exception:

            log.exception("Unexpected Error Occured")

            raise

    
    def validator_run(self):

        self.validate_config()
