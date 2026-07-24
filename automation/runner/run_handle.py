from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class RunHandle:
    """
    Represents one submitted training run.

    Every execution backend (Local, Slurm, Kubernetes, etc.)
    returns one RunHandle.
    """

    backend: str

    run_id: str

    submit_time: datetime

    job_name: str