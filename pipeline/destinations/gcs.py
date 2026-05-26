from loguru import logger
from datetime import datetime, timezone
from google.cloud import storage
import io
import pandas as pd

class Gcs:
    def __init__(self, metadata_cfg, destination_cfg, data):
        
        self.data = data

        self.metadata_cfg = metadata_cfg
        self.source = metadata_cfg['source']
        self.dataset = metadata_cfg['dataset']
        self.entity = metadata_cfg['entity']

        self.destination_cfg = destination_cfg
        self.bucket = destination_cfg['bucket']
        self.layer = destination_cfg['layer']
        self.format = destination_cfg['format']
        self.path_template = destination_cfg['path_template']

    def build_path(self):

        now = datetime.now(timezone.utc)

        try:
            path_context = {
                "layer": self.layer,
                "source": self.source,
                "dataset": self.dataset,
                "entity": self.entity,
                "ingestion_dt": now.strftime("%Y-%m-%d"),
                "ingestion_ts": now.strftime("%Y%m%dT%H%M%SZ"),
                "format": self.format
            }
            formatted_path = self.path_template.format(**path_context)
            logger.info(f"Successfully created and formatted path: {formatted_path}")
            return formatted_path
        except Exception as e:
            logger.error(f"Error creating path_context: {e}") 
            raise 

    def upload_to_gcs(self, path_context, data):

        now = datetime.now(timezone.utc)

        try:
            storage_client = storage.Client()
            bucket = storage_client.bucket(self.bucket)
            blob = bucket.blob(path_context)
            df = pd.DataFrame(data)
            df["ingestion_timestamp"] = now
            logger.info(f"Successfully converted the raw JSON data to Pandas DataFrame and added ingestion metadata(ingestion_timestamp)")
            
            buffer = io.BytesIO()
            df.to_parquet(buffer, index=False, compression='snappy')
            logger.info(f"Successfully converted, compressed to Parquet & finished writing it to RAM buffer")
            buffer.seek(0)

            blob.upload_from_file(buffer, content_type='application/octet-stream')
            logger.info(f"Successfully uploaded the parquet data to GCS")

        except Exception as e:
            logger.error(f"Error Uploading the data to GCS: {e}")
            raise 

    def run(self):

        path_context = self.build_path()

        self.upload_to_gcs(path_context= path_context, data=self.data)