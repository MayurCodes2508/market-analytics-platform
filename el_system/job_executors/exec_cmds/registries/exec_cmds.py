from loguru import logger as log
from job_executors.exec_cmds.api_exec import ApiExecCommand


class APIExec:
    @classmethod
    def run(cls, exec_cfg, *args, **kwargs):

        return ApiExecCommand(exec_cfg=exec_cfg)


class ExecCmdType:
    registry = {"ApiExecCmd": APIExec}

    @classmethod
    def get_exec_type(cls, exec_type, *args, **kwargs):

        class_template = cls.registry[exec_type]

        log.info(
            f"Successfully Mapped the Exec Type: {exec_type} with Exec Registry..."
        )

        exec_cmd = class_template.run(*args, **kwargs)

        return exec_cmd
