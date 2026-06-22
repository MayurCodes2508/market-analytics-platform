from loguru import logger as log
import jsonschema_rs
from jsonschema_rs import ValidationError
from pathlib import Path





class Validator:


    def __init__(self, loader):

        self.loader = loader

        self.pipeline_cfg = self.loader.pipeline_cfg
        self.schema_cfg = self.loader.schema_cfg

        self.schema_path = self.loader.schema_path


    def schema_validation(self):

        if not self.pipeline_cfg:

            raise ValueError(F"Invalid 'pipeline_cfg': {self.pipeline_cfg}")
        
        if not self.schema_cfg:

            raise ValueError(F"Invalid 'schema_cfg': {self.schema_cfg}")

        try:

            full_uri = Path(self.schema_path).resolve().as_uri()

            validator = jsonschema_rs.validator_for(self.schema_cfg, base_uri=full_uri)

            validator.validate(self.pipeline_cfg)

            log.info(f"Configuration Validated Against Schema {self.schema_path}")

        except ValidationError:

            log.exception(F"Validation Error Occured: {self.schema_path}")

            raise

        except Exception:

            log.exception("Unexpected Error Occured")

            raise


    def validator_run(self):

        self.schema_validation()