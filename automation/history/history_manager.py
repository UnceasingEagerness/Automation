from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime
from pathlib import Path


class HistoryManager:
    """
    Stores immutable records for completed experiments.

    Directory structure:

    history/
        PROJECT_NAME/
            20260724_183012.json
            20260724_204521.json
    """

    def __init__(self, root: str | Path = "history"):

        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _project_dir(self, project_name: str) -> Path:

        directory = self.root / project_name
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    @staticmethod
    def _serialize(value):

        if isinstance(value, datetime):
            return value.isoformat()

        if is_dataclass(value):
            return asdict(value)

        return value

    def record(
        self,
        *,
        project: str,
        commit: str | None,
        branch: str | None,
        backend: str | None,
        run_id: str | None,
        status: str,
        started: datetime | None,
        finished: datetime | None,
        checkpoint: str | None = None,
        artifacts: list[str] | None = None,
        metadata: dict | None = None,
    ) -> Path:

        artifacts = artifacts or []
        metadata = metadata or {}

        duration = None

        if started is not None and finished is not None:
            duration = (finished - started).total_seconds()

        payload = {
            "project": project,
            "commit": commit,
            "branch": branch,
            "backend": backend,
            "run_id": run_id,
            "status": status,
            "started": self._serialize(started),
            "finished": self._serialize(finished),
            "duration_seconds": duration,
            "checkpoint": checkpoint,
            "artifacts": artifacts,
            "metadata": metadata,
        }

        filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"

        path = self._project_dir(project) / filename

        with path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

        return path

    def list_runs(self, project: str):

        directory = self._project_dir(project)

        return sorted(directory.glob("*.json"))

    def latest(self, project: str):

        runs = self.list_runs(project)

        if not runs:
            return None

        return runs[-1]