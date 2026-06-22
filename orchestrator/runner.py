from google.cloud.run_v2 import JobsClient
from google.api_core.exceptions import GoogleAPIError, NotFound, InvalidArgument
from loguru import logger as log
import uuid




class Runner:


    def __init__(self, job_name):

        self.job_run_name = job_name


    def run_job(self):

        try:

            self.job_run_id = str(uuid.uuid7())

            jobs_client = JobsClient()

            self.base_path = 'projects/instant-medium-491107-t6/locations/asia-south1/jobs'

            log.info(F"Started Execution of Job: {self.job_run_name}, With Run ID: {self.job_run_id}")

            self.operation = jobs_client.run_job(
            name=(F"{self.base_path}/{self.job_run_name}")
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

            log.exception("Unexpected Error Occured")

            raise


    def run(self):

        self.run_job()
