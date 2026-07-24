import json
from pathlib import Path

from automation.state.state import ProjectState


class StateManager:

    def __init__(self, state_dir="state"):

        self.state_dir = Path(state_dir)

        self.state_dir.mkdir(parents=True, exist_ok=True)

    def _state_file(self, project_name: str):

        return self.state_dir / f"{project_name}.json"

    def load(self, project_name: str):

        path = self._state_file(project_name)

        if not path.exists():
            return ProjectState(project_name=project_name)

        with open(path, "r") as f:
            data = json.load(f)

        return ProjectState.from_dict(data)

    def save(self, state: ProjectState):

        path = self._state_file(state.project_name)

        with open(path, "w") as f:
            json.dump(state.to_dict(), f, indent=4)