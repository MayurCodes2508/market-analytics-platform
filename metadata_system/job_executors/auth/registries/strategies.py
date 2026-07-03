import os
from loguru import logger as log






class DBUrl:


    def __init__(self, auth_cfg):

        self.auth_cfg = auth_cfg

        self.key_env = auth_cfg['key_env']


        log.info("Auth Metadata Loading Completed...")


        log.info("Obj: dburl | Instance Initialized Successfully...")


    def load_db_creds(self):

        secret = os.getenv(key=self.key_env)

        if not secret:

            raise ValueError(F"Invalid or Missing 'secret': {secret}")
        
        self.secret = secret

        log.info("Successfully Loaded the Secret...")


    def run(self):

        self.load_db_creds()



class AuthRegistry:


    registry = {
        'db_url': DBUrl
    }


    @classmethod
    def get_obj(cls, auth_cfg, auth_type):

        class_template = cls.registry[auth_type]

        
        log.info(F"Successfully Mapped the Auth Type: {auth_type} with Auth Registry...")
        

        obj = class_template(auth_cfg=auth_cfg)

        obj.run()

        return obj