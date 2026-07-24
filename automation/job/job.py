from dataclasses import dataclass, field
from datetime import datetime

from automation.core.project import Project


@dataclass(slots=True)
class Job:
    """
    Represents one training job.

    A Job is immutable with respect to the commit it trains.
    Multiple Jobs may exist for the same Project.
    """

    project: Project

    commit: str

    enqueue_time: datetime = field(default_factory=datetime.now)

    priority: int = 0

    retry_count: int = 0
