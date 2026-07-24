from dataclasses import asdict, dataclass
from datetime import datetime

from automation.state.status import Status


@dataclass(slots=True)
class ProjectState:
    """
    Persistent state for one project.

    This state is backend-agnostic.
    """

    project_name: str

    status: Status = Status.IDLE

    last_seen_commit: str | None = None

    running_commit: str | None = None

    backend: str | None = None

    run_id: str | None = None

    last_check: datetime | None = None

    last_started: datetime | None = None

    last_finished: datetime | None = None

    def touch(self):

        self.last_check = datetime.now()

    def to_dict(self):

        data = asdict(self)

        data["status"] = self.status.value

        for field in (
            "last_check",
            "last_started",
            "last_finished",
        ):
            if data[field] is not None:
                data[field] = data[field].isoformat()

        return data

    @classmethod
    def from_dict(cls, data):

        data = data.copy()

        data["status"] = Status(data["status"])

        for field in (
            "last_check",
            "last_started",
            "last_finished",
        ):
            if data.get(field):
                data[field] = datetime.fromisoformat(data[field])

        return cls(**data)