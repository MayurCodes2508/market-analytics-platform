from loguru import logger
import json
import jsonschema_rs
from pathlib import Path
import argparse
from dotenv import load_dotenv
import os
import psycopg2
import uuid
from datetime import datetime, timezone
from pipeline.exec_cmds.api_exec import ApiExecCommand
from pipeline.destinations.gcs import GCS


class Runner:
    def __init__(self, file_path, schema_path):

        self.file_path = file_path
        self.schema_path = schema_path
        logger.info(f"Starting execution of job with config file: {file_path} and schema: {schema_path}")

    def load_config(self):
        
        with open(self.file_path, 'r') as f:
            job_config = json.load(f)
            logger.info(f"Successfully loaded job configuration from {self.file_path}")
            return job_config

    def load_schema(self):

        with open(self.schema_path, 'r') as f:
            schema = json.load(f)
            logger.info(f"Successfully loaded JSON schema from {self.schema_path}")
            return schema

    def validate_config(self, job_config, schema):

        try:

            path_replace = self.schema_path.replace("\\", "/")
            full_uri = Path(self.schema_path).resolve().as_uri()

            validator = jsonschema_rs.validator_for(schema, base_uri=full_uri)

            validator.validate(job_config)
            logger.info(f"Config validation successful")

        except jsonschema_rs.ValidationError as e:
            logger.error(f"Config validation failed: {e}")
            raise

    def load_env_credentials(self, job_config):

            load_dotenv(dotenv_path="../dev.env")
            db_url = os.getenv("DB_URL")

            if not db_url:
                raise ValueError(f"DB_URL not found")

            auth_config = job_config['exec'].get('auth')

            if not auth_config:
                logger.info(f"No auth_config configured for job: {job_config['job_name']}, skipping auth_config")
                return db_url, None
        
            api_key = os.getenv(auth_config['key_env'])

            if not api_key:
                raise ValueError(f"{auth_config['key_env']} not found")
            return db_url, api_key 

    def insert_run_metadata(self, job_config, db_url):

        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            run_id = str(uuid.uuid4())
            now = datetime.now(timezone.utc)

            insert_query = """
                INSERT INTO pipeline_runs (run_id, pipeline_name,  job_name, job_type, rows_processed, error_message, status, start_time, end_time, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (run_id, job_config['pipeline_name'], job_config['job_name'], job_config['job_type'], None, None, 'RUNNING', now, None, now))
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"Inserted run metadata for job {job_config['job_name']} with run ID: {run_id}")
            return run_id
        
        except Exception as e:
            logger.error(f"Error inserting run metadata for job {job_config['job_name']}: {e}")
            raise

    def execute_execcmd(self, job_config, api_key):
        
        exec_cfg = job_config['exec']
        job_name = job_config['job_name']

        if exec_cfg["type"] == "ApiExecCommand":
            return ApiExecCommand(exec_cfg, job_name, api_key)
            
        else:
            raise ValueError(f"Unsupported exec type: {exec_cfg["type"]}")

    def execute_destination(self, job_config, data):

        job_name = job_config['job_name']
        destination_cfg = job_config.get('destination')

        if not destination_cfg:
            logger.info(f"No destination configured for job: {job_name}, skipping destination")
            return None
        
        metadata_cfg = job_config['metadata']
        
        if destination_cfg["type"] == 'GCS':
            return GCS(metadata_cfg, destination_cfg, data)
            
        else:
            raise ValueError(f"Unsupported destination type: {destination_cfg['type']}")

    def update_run_metadata(self, job_config, run_id, status, db_url, total_records, error_message=None,):

        try:
            conn = psycopg2.connect(db_url)
            cursor = conn.cursor()

            now = datetime.now(timezone.utc)

            update_query = """
                UPDATE pipeline_runs
                SET status = %s, rows_processed = %s, error_message = %s, end_time = %s
                WHERE run_id = %s
            """
            cursor.execute(update_query, (status, total_records, error_message, now, run_id))
            conn.commit()
            cursor.close()
            conn.close()
            logger.info(f"Updated run metadata for job {job_config['job_name']} with run ID: {run_id} to status: {status}")
        
        except Exception as e:
            logger.error(f"Error updating run metadata for job {job_config['job_name']} with run ID: {run_id}: {e}")
            raise

    def run(self):
        job_config = self.load_config()

        schema = self.load_schema()

        self.validate_config(job_config=job_config, schema=schema)
        logger.info(f"Job {job_config['job_name']} of type {job_config['job_type']} is ready to run.")

        db_url, api_key = self.load_env_credentials(job_config=job_config)
        logger.info(f"Database credentials loaded successfully for job {job_config['job_name']}")   

        run_id = self.insert_run_metadata(job_config=job_config, db_url=db_url)
        logger.info(f"Job {job_config['job_name']} started with run ID: {run_id}")

        status = "FAILED"
        error_message = None
        total_records = 0
        try:
            execcmd = self.execute_execcmd(job_config=job_config, api_key=api_key)
            logger.info(f"Executing job {job_config['job_name']} with run ID: {run_id}")
            data, total_records = execcmd.run()
            destination = self.execute_destination(job_config=job_config, data=data)
            if destination:
                destination.run()
            logger.info(f"Job {job_config['job_name']} with run ID: {run_id} completed successfully")
            status = "SUCCESS"

        except Exception as e:
            error_message = str(e)
            logger.error(f"Error occurred while executing job {job_config['job_name']} with run ID: {run_id}: {error_message}")
            raise

        finally:
            self.update_run_metadata(job_config=job_config, run_id=run_id, status=status, error_message=error_message, db_url=db_url, total_records=total_records)
            logger.info(f"Job {job_config['job_name']} with run ID: {run_id} finished with status: {status}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a job defined in a JSON file with a given schema.")
    parser.add_argument("--file_path", help="Path to the job configuration JSON file.", required=True)
    parser.add_argument("--schema_path", help="Path to the JSON schema file.", required=True)

    args = parser.parse_args()
    runner = Runner(args.file_path, args.schema_path)
    runner.run()