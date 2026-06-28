from loguru import logger as log
import argparse
from orchestrator.loader import Loader
from orchestrator.validator import Validator
from orchestrator.metadata import Metadata
from orchestrator.runner import Runner




class Orchestrator:


    def run(self):

        self.load_config()

        self.load_schema()

        self.validate_config()

        self.load_metadata()

        self.load_exec_cfg()

        self.load_dest_cfg()

        self.load_env_credentials()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a job defined in a JSON file with a given schema.")
    parser.add_argument("--file_path", help="Path to the job configuration JSON file.", required=True)
    parser.add_argument("--schema_path", help="Path to the JSON schema file.", required=True)

    args = parser.parse_args()

    error_message = None

    try:

        loader = Loader(args.file_path, args.schema_path)

        loader.loader_run()


        validator = Validator(loader)

        validator.validator_run()


        metadata = Metadata(loader)

        metadata.metadata_run()


        log.info(F"Job: {metadata.job_name} | Type: {metadata.job_type} | Sub Type: {metadata.sub_jobtype} | System: {metadata.system} | Status: Ready to Run...")


        runner = Runner(metadata, loader)

        runner.runner_run()



    except Exception as e:

        error_message = str(e)

        metadata.metadata_run_2(runner.rows_processed, error_message)

        log.exception(F"Job: {metadata.job_name} | Type: {metadata.job_type} | Sub Type: {metadata.sub_jobtype} | System: {metadata.system} | Status: Execution Failed | Error_message: {error_message}...")

        raise


    else:

        error_message = None

        metadata.metadata_run_2(runner.rows_processed, error_message)

        log.info(F"Job: {metadata.job_name} | Type: {metadata.job_type} | Sub Type: {metadata.sub_jobtype} | System: {metadata.system} | Status: Execution Successful...")


    finally:

        print(F"METADATA_DUMP: {metadata.metadata_payload}")