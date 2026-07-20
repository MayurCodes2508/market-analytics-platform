from loguru import logger as log
from subprocess import run as sp, CalledProcessError as cpe
import shlex
from pathlib import Path







class dbtExecCommand:


    def __init__(self, exec_cfg):
        
        self.exec_cfg = exec_cfg

        cmd = exec_cfg['command']

        self.cmd = shlex.split(s=cmd)

        log.info("Obj: dbtexeccmd | Instance Initialization Completed...")

        log.info("Exec Metadata Loading Completed...")


    def run_dbt(self):

        try:

            result = sp(
                ["dbt",
                *self.cmd,
                "--fail-fast",
                "--project-dir", str(Path(__file__).parent.parent.parent / 'dbt/'),
                "--profiles-dir", str(Path(__file__).parent.parent.parent / 'dbt/')],
                text=True,
                check=True,
                capture_output=True
            )

            log.info(result.stdout)

            log.info("Execution of dbt Completed...")

        
        except cpe as e:

            if e.stdout:

                log.error(e.stdout)

            if e.stderr:

                log.error(e.stderr)


    def run(self):

        self.run_dbt()

        data = None

        job_metrics = {
            "total_models":None,
            "successful_models":None,
            "failed_models":None,
            "total_tests":None,
            "successful_tests":None,
            "failed_tests":None
        }

        return data, job_metrics