from datetime import datetime

from automation.job.job import Job
from automation.runner.runner import Runner
from automation.runner.run_handle import RunHandle

import automation.slurm.slurm_utils as slurm


class SlurmRunner(Runner):
    """
    Executes training through Slurm.
    """

    def start(self, job: Job) -> RunHandle:

        job_id = slurm.submit(
            command=job.project.training_command,
            cwd=job.project.local_path,
        )

        return RunHandle(
            backend="slurm",
            run_id=job_id,
            submit_time=datetime.now(),
            job_name=job.project.name,
        )