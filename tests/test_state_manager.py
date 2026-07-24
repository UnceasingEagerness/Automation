import json

from automation.state.state import ProjectState
from automation.state.state_manager import StateManager
from automation.state.status import Status


def test_default_state_creation(tmp_path):

    manager = StateManager(tmp_path)

    state = manager.load("TEST")

    assert state.project_name == "TEST"
    assert state.status == Status.IDLE
    assert state.last_seen_commit is None


def test_save_creates_json(tmp_path):

    manager = StateManager(tmp_path)

    state = ProjectState(project_name="TEST")

    manager.save(state)

    path = tmp_path / "TEST.json"

    assert path.exists()


def test_state_persistence(tmp_path):

    manager = StateManager(tmp_path)

    state = ProjectState(project_name="TEST")

    state.status = Status.RUNNING
    state.last_seen_commit = "abc123"

    manager.save(state)

    loaded = manager.load("TEST")

    assert loaded.status == Status.RUNNING
    assert loaded.last_seen_commit == "abc123"


def test_touch():

    state = ProjectState(project_name="TEST")

    assert state.last_check is None

    state.touch()

    assert state.last_check is not None


def test_state_serialization():

    state = ProjectState(project_name="TEST")

    state.status = Status.QUEUED

    data = state.to_dict()

    restored = ProjectState.from_dict(data)

    assert restored.project_name == "TEST"
    assert restored.status == Status.QUEUED


def test_enum_saved_as_string(tmp_path):

    manager = StateManager(tmp_path)

    state = ProjectState(project_name="TEST")

    state.status = Status.RUNNING

    manager.save(state)

    with open(tmp_path / "TEST.json", "r") as f:
        data = json.load(f)

    assert data["status"] == "running"


def test_enum_loaded_from_string(tmp_path):

    with open(tmp_path / "TEST.json", "w") as f:
        json.dump(
                {
                    "project_name": "TEST",
                    "status": "completed",
                    "last_seen_commit": None,
                    "running_commit": None,
                    "backend": None,
                    "run_id": None,
                    "last_check": None,
                    "last_started": None,
                    "last_finished": None,
                },
                f,
                indent=4,
            )

    manager = StateManager(tmp_path)

    state = manager.load("TEST")

    assert state.status == Status.COMPLETED