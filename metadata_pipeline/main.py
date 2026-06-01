from loguru import logger
from dotenv import load_dotenv
import os
import psycopg2, psycopg2.extras
from google.cloud import bigquery


def load_env_credentials():

    load_dotenv(dotenv_path="../dev.env")
    db_url = os.getenv("DB_URL")
    logger.info(f"Successfully loaded DB credentials")

    if not db_url:
        raise ValueError (f"DB_URL not found")
    return db_url

def execute_query(db_url):
    
    try:

        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        select_query = """
            SELECT *
            FROM pipeline_runs
            ORDER BY created_at DESC;
        """

        cursor.execute(select_query)

        data = cursor.fetchall()

        cursor.close()
        conn.close()

        logger.info(f"Successfully fetched the data, total_rows: {len(data)}")
        return data
    
    except Exception as e:
        logger.error(f"Error fetching data from the table: {e}")
        raise

def load_data(data):

    try:

        for row in data:
            for key, value in row.items():
                if hasattr(value, "isoformat"):
                    row[key] = value.isoformat()

        big_query_client = bigquery.Client(location='asia-south1')

        table_id = 'instant-medium-491107-t6.dev_metadata.raw_pipeline_runs'

        errors = big_query_client.insert_rows_json(table_id, data)

        if errors:
            logger.error(f"Error inserting data into BigQuery: {errors}")
            raise Exception(errors)
        
        logger.info(f"Successfully loaded the data to BigQuery table: {table_id}")
        
    except Exception as e:
        logger.error(f"Error loading data to table: {e}")
        raise

def handler(request):

    try:

        db_url = load_env_credentials()

        data = execute_query(db_url)

        load_data(data)

        return "OK", 200
    
    except Exception as e:
        logger.error(f"Failed metadata ingestion: {e}")

        return "Failed", 500
    

if __name__ == "__main__":
    handler(None)