from enum import Enum


class JobStatus(Enum):
    """
    Canonical SLURM job states used by the monitor.

    Raw sacct/squeue output is mapped into one of these values.
    """

    PENDING = "PENDING"

    RUNNING = "RUNNING"

    COMPLETED = "COMPLETED"

    FAILED = "FAILED"

    CANCELLED = "CANCELLED"

    TIMEOUT = "TIMEOUT"

    UNKNOWN = "UNKNOWN"