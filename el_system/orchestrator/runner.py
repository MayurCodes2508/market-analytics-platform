from loguru import logger as log
from job_executors.exec_cmds.registries.exec_cmds import ExecCmdType
from job_executors.dests.registries.dest_targets import DestType


class Runner:
    def __init__(self, loader):

        self.job_cfg = loader.job_cfg

        self.exec_cfg = self.job_cfg['exec']

        self.exec_type = self.exec_cfg["exec_type"]

        self.metadata_cfg = self.job_cfg['metadata']

        self.dest_cfg = self.job_cfg.get('dest', {})

        self.dest_type = self.dest_cfg.get("dest_type", None)

        self.is_dest = True if self.dest_cfg and self.dest_type else False

        log.info("Runner Loading Completed...")

        log.info("Obj: runner | Instance Initialized Successfully...")

    def run_exec_cmd(self):

        exec_cmd = ExecCmdType.get_exec_type(
            exec_type=self.exec_type,
            exec_cfg=self.exec_cfg,
            metadata_cfg=self.metadata_cfg,
        )

        self.data, self.rows_processed = exec_cmd.run()

    def run_dest_target(self):
            
        if not self.is_dest:

            log.info("Dest Not Provided, Skipping...")

            return
        
        dest = DestType.get_dest_type(
            dest_type=self.dest_type,
            dest_cfg=self.dest_cfg,
            metadata_cfg=self.metadata_cfg,
            data=self.data,
        )

        dest.run()


    def runner_run(self):

        self.run_exec_cmd()

        self.run_dest_target()
