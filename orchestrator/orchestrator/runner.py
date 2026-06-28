from google.cloud.run_v2 import JobsClient
from google.api_core.exceptions import GoogleAPIError, NotFound, InvalidArgument
from loguru import logger as log
from uuid6 import uuid7
from orchestrator.metadata import Job_Metadata
from orchestrator.logger import Job_Logger





class Runner:


    def __init__(self, pipeline_metadata, loader):

        self.pipeline_metadata = pipeline_metadata

        self.loader = loader

        self.jobs = self.pipeline_metadata.run_jobs


    def run_jobs(self):

        log.info("All Jobs Executions Started")

        self.successful_jobs = 0
        self.failed_jobs = 0

        try:

            for job in self.jobs:

                self.job_name = job['job_name']

                if not self.job_name:

                    raise ValueError(F"Invalid 'job_name': {self.job_name}")
                
            
                self.execute_job()

                self.job_run_id = str(uuid7())


                self.job_metadata = Job_Metadata(operation=self.operation, job_name=self.job_name, job_run_id=self.job_run_id, pipeline_run_id=self.pipeline_metadata.pipeline_run_id)

                self.job_metadata.metadata_run()


                self.job_logger = Job_Logger(loader=self.loader, job_metadata=self.job_metadata)

                self.job_logger.logger_run()

                self.failed_count, self.successful_count = self.pipeline_metadata.collect_jobs_count(self.job_metadata.status)

                self.successful_jobs += self.successful_count
                self.failed_jobs += self.failed_count

        except Exception:

            log.exception("Error Occured While Running Jobs")

            raise


    def execute_job(self):

        try:

            jobs_client = JobsClient()

            self.base_path = 'projects/instant-medium-491107-t6/locations/asia-south1/jobs'

            log.info(F"Executing Job: {self.job_name}")

            self.operation = jobs_client.run_job(
            name=(F"{self.base_path}/{self.job_name}")
            )

        except GoogleAPIError:

            log.exception("API Error Occured")

            raise

        except NotFound:

            log.exception(F"Job Not Found Error Occured: {self.job_run_name}")

            raise

        except InvalidArgument:

            log.exception(F"Invalid Argument Error Occured: {self.operation}")

            raise

        except Exception:

            log.exception("Error Occured While Executing Job")

            raise


    def runner_run(self):

        self.run_jobs()
