import json



class Logger:

    
    def __init__(self):
        
        self.job_name = None
        self.system = None
        self.job_type = None
        self.sub_jobtype = None
        self.error_message = None
        self.rows_processed = None


    def log(self):

        results = {
            'job_name': self.job_name,
            'system': self.system,
            'job_type': self.job_type,
            'sub_jobtype': self.sub_jobtype,
            'error_message': self.error_message,
            'job_metrics': {
                'rows_processed': self.rows_processed
                }
        }

        metadata = json.dumps(results)
        print(F"METADATA_DUMP: {metadata}")