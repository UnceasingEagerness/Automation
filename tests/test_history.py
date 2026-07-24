import json
from datetime import datetime, timedelta

from automation.history import HistoryManager


def test_history_directory_created(tmp_path):

    manager = HistoryManager(root=tmp_path)

    assert tmp_path.exists()
    assert tmp_path.is_dir()


def test_record_creates_json(tmp_path):

    manager = HistoryManager(root=tmp_path)

    started = datetime(2026, 1, 1, 10, 0, 0)
    finished = started + timedelta(seconds=120)

    path = manager.record(
        project="MARL",
        commit="abc123",
        branch="main",
        backend="slurm",
        run_id="42",
        status="COMPLETED",
        started=started,
        finished=finished,
    )

    assert path.exists()
    assert path.suffix == ".json"


def test_record_contents(tmp_path):

    manager = HistoryManager(root=tmp_path)

    started = datetime(2026, 1, 1, 10, 0, 0)
    finished = started + timedelta(minutes=5)

    path = manager.record(
        project="MARL",
        commit="deadbeef",
        branch="dev",
        backend="slurm",
        run_id="99",
        status="FAILED",
        started=started,
        finished=finished,
        checkpoint="best.pt",
        artifacts=["metrics.json", "train.log"],
        metadata={"reward": 42},
    )

    with open(path) as f:
        data = json.load(f)

    assert data["project"] == "MARL"
    assert data["commit"] == "deadbeef"
    assert data["branch"] == "dev"
    assert data["backend"] == "slurm"
    assert data["run_id"] == "99"
    assert data["status"] == "FAILED"

    assert data["checkpoint"] == "best.pt"

    assert data["artifacts"] == [
        "metrics.json",
        "train.log",
    ]

    assert data["metadata"] == {
        "reward": 42
    }

    assert data["duration_seconds"] == 300.0


def test_project_directory_created(tmp_path):

    manager = HistoryManager(root=tmp_path)

    manager.record(
        project="Research",
        commit=None,
        branch=None,
        backend=None,
        run_id=None,
        status="COMPLETED",
        started=None,
        finished=None,
    )

    assert (tmp_path / "Research").exists()


def test_list_runs(tmp_path):

    manager = HistoryManager(root=tmp_path)

    for _ in range(3):

        manager.record(
            project="MARL",
            commit=None,
            branch=None,
            backend=None,
            run_id=None,
            status="COMPLETED",
            started=None,
            finished=None,
        )

    runs = manager.list_runs("MARL")

    assert len(runs) == 3

    for run in runs:
        assert run.exists()


def test_latest_returns_last_run(tmp_path):

    manager = HistoryManager(root=tmp_path)

    first = manager.record(
        project="MARL",
        commit="1",
        branch=None,
        backend=None,
        run_id=None,
        status="COMPLETED",
        started=None,
        finished=None,
    )

    second = manager.record(
        project="MARL",
        commit="2",
        branch=None,
        backend=None,
        run_id=None,
        status="FAILED",
        started=None,
        finished=None,
    )

    latest = manager.latest("MARL")

    assert latest == second
    assert latest != first


def test_latest_empty_returns_none(tmp_path):

    manager = HistoryManager(root=tmp_path)

    assert manager.latest("UnknownProject") is None


def test_duration_none_when_missing_times(tmp_path):

    manager = HistoryManager(root=tmp_path)

    path = manager.record(
        project="MARL",
        commit=None,
        branch=None,
        backend=None,
        run_id=None,
        status="COMPLETED",
        started=None,
        finished=None,
    )

    with open(path) as f:
        data = json.load(f)

    assert data["duration_seconds"] is None