from loguru import logger as log
import jsonschema_rs
from jsonschema.exceptions import ValidationError, SchemaError
from pathlib import Path





class Validator:


    def __init__(self, loader):

        self.loader = loader

        self.pipeline_cfg = self.loader.pipeline_cfg

        self.schema_cfg = self.loader.schema_cfg

        self.schema_path = self.loader.schema_path


        log.info("Pipeline & Schema Cfg Loading Completed...")


        log.info("Obj: validator | Instance Initialized Successfully...")


    def validate_pipeline_cfg(self):

        try:

            full_uri = Path(self.schema_path).resolve().as_uri()

            validator = jsonschema_rs.validator_for(schema=self.schema_cfg, base_uri=full_uri)

            validator.validate(instance=self.pipeline_cfg)

            log.info("Pipeline Validation Against Given Schema...")

        except ValidationError as e:

            log.error(F"Validation Error: {self.pipeline_cfg} | Provide a Valid Pipeline Cfg | Details: {e}")

            raise

        except SchemaError as e:

            log.error(F"Schema Error: {self.schema_cfg} | Provide a Valid Schema | Details: {e}")

            raise

        except Exception:

            log.exception("Unknown Error Occured While Validating Pipeline Cfg Againt Given Schema")

            raise


    def validator_run(self):

        self.validate_pipeline_cfg()