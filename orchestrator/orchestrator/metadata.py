from loguru import logger as log
from uuid6 import uuid7
from datetime import datetime
import os
from google.cloud.run_v2 import ExecutionsClient
from google.api_core.exceptions import GoogleAPIError, NotFound, InvalidArgument
import time
import google.cloud.logging_v2
import json





class Pipeline_Metadata:


    def __init__(self, loader):
        
        self.loader = loader



        self.pipeline_cfg = self.loader.pipeline_cfg

        self.pipeline_run_name = self.pipeline_cfg['pipeline_name']

        self.run_jobs = self.pipeline_cfg['jobs']


        log.info("Pipeline Values Loading Completed...")


        log.info("Obj: pipeline metadata | Instance Initialized Successfully...")


    def create_pipeline_start_metadata(self):
            
        try:

            self.pipeline_run_id = str(uuid7())

            self.now = datetime.now().isoformat()

            self.pipeline_run_start_time = self.now

            self.pipeline_run_start_status = 'RUNNING'

            self.pipeline_run_triggered_by = os.getenv('TRIGGERED_BY', 'manual')

            self.pipeline_run_created_at = self.now

            self.total_jobs = len(self.run_jobs)

            self.pipeline_run_start_job_counts = {

                'total_jobs': self.total_jobs,
                'successful_jobs': None,
                'failed_jobs': None

            }

            self.pipeline_start_metadata_dump = {

                "pipeline_run_id": self.pipeline_run_id,
                "pipeline_run_name": self.pipeline_run_name,
                "pipeline_run_start_time": self.pipeline_run_start_time,
                "pipeline_run_status": self.pipeline_run_start_status,
                "pipeline_run_triggered_by": self.pipeline_run_triggered_by,
                "pipeline_run_created_at": self.pipeline_run_created_at,
                "pipeline_run_job_counts": self.pipeline_run_start_job_counts

            }

            log.info("Pipeline Start Metadata Creation Completed...")

        except Exception:

            log.error("Unexpected Error Occured While Creating Pipeline Start Metadata")

            raise


    def create_pipeline_end_metadata(self, status, error_message, successful_job_counts, failed_job_counts):

        try:

            self.pipeline_run_end_status = status
            self.pipeline_run_error_message = error_message
            self.successful_job_counts = successful_job_counts
            self.failed_job_counts = failed_job_counts
            self.pipeline_run_end_time = datetime.now().isoformat()

            self.pipeline_run_end_job_counts = {

                "total_jobs": self.total_jobs,
                "successful_jobs": self.successful_job_counts,
                "failed_jobs": self.failed_job_counts
            }

            self.pipeline_end_metadata_dump = {

                "pipeline_run_id": self.pipeline_run_id,
                "pipeline_run_status": self.pipeline_run_end_status,
                "pipeline_run_error_message":  self.pipeline_run_error_message,
                "pipeline_run_end_time": self.pipeline_run_end_time,
                "pipeline_run_job_counts": self.pipeline_run_end_job_counts

            }

            log.info("Pipeline End Metadata Creation Completed...")

        except Exception:

            log.error("Unexpected Error Occured While Creating Pipeline End Metadata")

            raise

        
    def collect_jobs_count(self, status):

        try:

            if status == 'FAILED':

                failed_count = 1
                successful_count = 0

            elif status == 'SUCCESS':

                successful_count = 1
                failed_count = 0

            log.info("Jobs Count Collection Completed...")
            
            return failed_count, successful_count
        
        except Exception:

            log.error("Unexpected Error Occured While Collecting Jobs Count")

            raise


    def metadata_run(self):

        self.create_pipeline_start_metadata()

    
    def metadata_run_2(self, *args, **kwargs):

        self.create_pipeline_end_metadata(*args, **kwargs)


class Job_Metadata:


    def __init__(self, operation, job_name, job_run_id, pipeline_run_id):


        self.operation = operation

        self.job_run_name = job_name

        self.job_run_id = job_run_id

        self.pipeline_run_id = pipeline_run_id


    def create_job_metadata(self):

        executions_client = ExecutionsClient()

        try:

            self.execution_name = self.operation.metadata.name

            log.info(F"Job Execution Name: {self.execution_name}")

            for seconds in range(30):

                self.execution = executions_client.get_execution(
                    name=self.execution_name
                )

                if self.execution.completion_time:

                    log.info("Successfully Got Final Job Execution")

                    break

                time.sleep(2)
        
            if not self.execution:

                raise ValueError("Invalid 'execution', Stopping....")

            elif not self.execution.completion_time:

                raise ValueError("Execution Failed to Complete Within Time, Stopping....")


            start_time = self.execution.start_time

            end_time = self.execution.completion_time

            created_at = self.execution.create_time

            cloud_run_job_id = self.execution.uid

            cloud_run_job_name = self.execution.job

            log_uri = self.execution.log_uri

            max_retries = self.execution.template.max_retries

            timeout = self.execution.template.timeout.seconds

            is_retry = bool(self.execution.retried_count)

            for seconds in range(30):

                for condition in self.execution.conditions:

                    if condition.type_ == 'Completed' and condition.state == 4:
 
                        log.info("Job Executed Successfully")

                        self.status = 'SUCCESS'

                        break

                if self.status == 'SUCCESS':

                    break

                time.sleep(2)

            else:

                self.status = 'FAILED' 

                log.warning("Job Execution Failed")

            logging_client = google.cloud.logging_v2.Client()

            exec_name = self.execution_name.rsplit('/', 1)[-1]

            job_filter = F'''

                resource.labels.job_name="{self.job_run_name}"
                resource.labels.location="asia-south1"
                labels."run.googleapis.com/execution_name"="{exec_name}"
                textPayload:"METADATA_DUMP"

                '''

            for entry in logging_client.list_entries(filter_=job_filter):

                log_text = entry.payload

                metadata = log_text.rsplit("METADATA_DUMP: ", 1)[-1]

                job_metadata = json.loads(metadata)

                if job_metadata:

                    break


        except Exception:

            log.exception("Unexpected Error Occured, Affecting Job Metadata")

            raise

        try:

            self.job_metadata_dump = {
                "job_run_id": self.job_run_id,
                "pipeline_run_id": self.pipeline_run_id,
                "job_name": job_metadata.get('job_name', None),
                "system": job_metadata.get('system', None),
                "job_type": job_metadata.get('job_type', None),
                "sub_jobtype": job_metadata.get('sub_jobtype', None),
                "job_status": self.status,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "created_at": created_at.isoformat(),
                "error_message": job_metadata.get('error_message', None),
                "job_metrics": {
                    "rows_processed": job_metadata.get('rows_processed', None)
                },
                "extra_metadata": {
                    "cloud_run_job_id": cloud_run_job_id,
                    "cloud_run_job_name": cloud_run_job_name,
                    "log_uri": log_uri,
                    "max_retries": max_retries,
                    "timeout": timeout,
                    "is_retry": is_retry
                }
            }

            log.info("Job Metadata Created")

        except Exception:

            log.exception("Unexpected Error Occured, Affecting Job Metadata")            

        except GoogleAPIError:

            log.exception("API Error Occured, Affecting Job Metadata")

        except NotFound:

            log.exception("Execution Not Found Error Occured, Affecting Job Metadata")

        except InvalidArgument:

            log.exception("Invalid Argument Error Occured, Affecting Job Metadata")

        except Exception:

            log.exception("Unexpected Error Occured, Affecting Job Metadata")

    
    def metadata_run(self):

        self.create_job_metadata()