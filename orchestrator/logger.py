from loguru import logger as log
import psycopg2
from psycopg2.errors import DatabaseError, OperationalError, InterfaceError
from psycopg2.extras import Json




class Pipeline_Logger:


    def __init__(self, loader, metadata):

        self.loader = loader
        self.metadata = metadata

        self.db_url = self.loader.db_url

        self.pipeline_start_metadata_dump = self.metadata.pipeline_start_metadata_dump
        self.pipeline_end_metadata_dump = getattr(self.metadata, 'pipeline_end_metadata_dump', None)
        
    
    def log_pipeline_run_start(self):

        try:

            with psycopg2.connect(self.db_url) as conn:

                    with conn.cursor() as cursor:

                        insert_query = """

                    INSERT INTO pipeline_runs(
                                run_id,
                                pipeline_name,
                                error_message,
                                status,
                                start_time,
                                end_time,
                                created_at,
                                triggered_by,
                                job_counts
                            )

                    VALUES(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) 

                """

                        query_values = (

                            self.pipeline_start_metadata_dump['pipeline_run_id'],
                            self.pipeline_start_metadata_dump.get('pipeline_run_name', None),
                            None,
                            self.pipeline_start_metadata_dump['pipeline_run_status'],
                            self.pipeline_start_metadata_dump.get('pipeline_run_start_time', None),
                            None,
                            self.pipeline_start_metadata_dump.get('pipeline_run_created_at', None),
                            self.pipeline_start_metadata_dump.get('pipeline_run_triggered_by', None),
                            Json(self.pipeline_start_metadata_dump.get('pipeline_run_job_counts', None)),

                        )

                        cursor.execute(insert_query, query_values)

                        log.info("Successfully Inserted Pipeline Run")

        except (OperationalError, InterfaceError):

            log.exception("Network/Connection Error Occured")

        except DatabaseError:

            log.exception("SQL Syntax/DB Constraint Error Occured")

        except Exception:

            log.exception("Unexpected Error Occured")
    

    def log_pipeline_run_end(self):

        try:

            with psycopg2.connect(self.db_url) as conn:
                    
                    with conn.cursor() as cursor:

                        update_query = """

                    UPDATE  pipeline_runs

                    SET status = %s,
                        error_message = %s,
                        end_time = %s,
                        job_counts = %s

                    WHERE run_id = %s

                """

                        query_values = (
                            self.pipeline_end_metadata_dump.get('pipeline_run_status', None),
                            self.pipeline_end_metadata_dump.get('pipeline_run_error_message', None),
                            self.pipeline_end_metadata_dump.get('pipeline_run_end_time', None),
                            Json(self.pipeline_end_metadata_dump.get('pipeline_run_job_counts', None)),
                            self.pipeline_end_metadata_dump.get('pipeline_run_id', None)
                        )

                        cursor.execute(update_query, query_values)

        except (OperationalError, InterfaceError):

            log.exception("Network/Connection Error Occured")

        except DatabaseError:

            log.exception("SQL Syntax/DB Constraint Error Occured")


        except Exception:

            log.exception("Unexpected Error Occured")

    
    def logger_run(self):

        self.log_pipeline_run_start()

    
    def logger_run_2(self):

        self.log_pipeline_run_end()


class Job_Logger:


    def __init__(self, loader, job_metadata):

        self.loader = loader
        self.job_metadata = job_metadata

        self.db_url = self.loader.db_url
        self.job_metadata_dump = self.job_metadata.job_metadata_dump


    def log_job_run_metadata(self):

        try:

            with psycopg2.connect(self.db_url) as conn:
                    
                    with conn.cursor() as cursor:

                        insert_query = """

                    INSERT INTO job_runs(
                                run_id,
                                pipeline_run_id,
                                job_name,
                                system,
                                job_type,
                                sub_jobtype,
                                status,
                                start_time,
                                end_time,
                                created_at,
                                error_message,
                                job_metrics,
                                extra_metadata
                            )

                    VALUES(
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )

                """

                        query_values = (
                            self.job_metadata_dump.get('job_run_id', None),
                            self.job_metadata_dump.get('pipeline_run_id', None),                            
                            self.job_metadata_dump.get('job_name', None),                            
                            self.job_metadata_dump.get('system', None),                        
                            self.job_metadata_dump.get('job_type', None),                        
                            self.job_metadata_dump.get('sub_jobtype', None),                        
                            self.job_metadata_dump.get('job_status', None),                        
                            self.job_metadata_dump.get('start_time', None),                        
                            self.job_metadata_dump.get('end_time', None),                        
                            self.job_metadata_dump.get('created_at', None),                        
                            self.job_metadata_dump.get('error_message', None),                        
                            Json(self.job_metadata_dump.get('job_metrics', None)),                        
                            Json(self.job_metadata_dump.get('extra_metadata', None)),                        
                        )

                        cursor.execute(insert_query, query_values)

        except (OperationalError, InterfaceError):

            log.exception("Network/Connection Error Occured")

        except DatabaseError:

            log.exception("SQL Syntax/DB Constraint Error Occured")

        except Exception:

            log.exception("Unexpected Error Occured")


    def logger_run(self):
        
        self.log_job_run_metadata()