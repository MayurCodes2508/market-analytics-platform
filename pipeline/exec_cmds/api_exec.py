from loguru import logger
import requests

class ApiReadExecCommand:
    def __init__(self, exec_cfg, job_name, api_key=None):

        self.job_name = job_name
        self.api_key = api_key
        self.exec_cfg = exec_cfg
        self.base_url = exec_cfg["base_url"]
        self.path = exec_cfg["path"]

        pagination_config = exec_cfg["pagination"]
        self.pagination_strategy = pagination_config["strategy"]
        self.page_param = pagination_config.get("page_param", "page")

        page_size_config = exec_cfg["page_size"]
        self.page_size_param = page_size_config["param"]
        self.page_size_value = page_size_config["value"]

        if self.job_name.startswith("prod_"):
            self.page_size_value = 250
            
        query_params_config = exec_cfg["query_params"]
        self.vs_currency = query_params_config["vs_currency"]
        self.custom_query_params = {
            k: v for k, v in query_params_config.items() if k != "vs_currency"
        }
   
        auth_config = exec_cfg.get("auth")
        if auth_config:
            self.auth_type = auth_config["type"]
            self.key_env = auth_config["key_env"]
            self.location = auth_config["location"]
            self.name = auth_config["name"]
        else:
            self.auth_type = None
            self.key_env = None
            self.location = None
            self.name = None

    def build_url(self):

        try:
            url = f"{self.base_url}{self.path}"
            logger.info(f"Built URL: {url}")
            return url
        except Exception as e:
            logger.error(f"Error building URL: {e}")
            raise

    def build_headers(self):

        try:
            headers = {}
            if self.api_key:
                if self.location == "header":
                    headers[self.name] = self.api_key
                    logger.info(f"Added API key to headers: {headers}")
                else:
                    logger.warning(f"Unsupported auth location: {self.location}. API key will not be included in headers.")
            return headers
        except Exception as e:
            logger.error(f"Error building headers: {e}")
            raise

    def build_params(self):

        try:
            params = {
                self.page_size_param: self.page_size_value,
                "vs_currency": self.vs_currency
            }

            params.update(self.custom_query_params)
            logger.info(f"Built query params: {params}")
            return params
        except Exception as e:
            logger.error(f"Error building query params: {e}")
            raise

    def make_request(self, url, headers, params):

        logger.info(f"Making request started with: url={url} | headers={headers} | params={params}")
        try:
            response = requests.get(url=url, headers=headers, params=params)
            logger.info(f"Request made: {response}")
            return response
        except Exception as e:
            logger.error(f"Error making request: {e}")
            raise

    def handle_response(self, response):

       try:
           data = response.json()
           logger.info(f"Successfully fetched & stored the data")
           total_records = len(data)
           logger.info(f"total_records fetched: {total_records}")

           if response.status_code != 200:
               raise Exception(
                   f"Request_failed: {response.status_code} - {response.text}"
               )
           return data, total_records
       except Exception as e:
           logger.error(f"Error handling response: {e}")
           raise

    def run(self):
        
        url = self.build_url()

        headers = self.build_headers()

        params = self.build_params()

        response = self.make_request(url=url, headers=headers, params=params)

        data, total_records = self.handle_response(response)
        return data, total_records