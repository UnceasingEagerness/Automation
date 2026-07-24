from unittest.mock import patch

from automation.monitor.monitor import Monitor

from automation.state.state_manager import StateManager
from automation.state.status import Status

from automation.slurm.job_status import JobStatus


class DummyProject:
    name = "TEST"


def create_running_state(tmp_path):

    manager = StateManager(tmp_path)

    state = manager.load("TEST")

    state.status = Status.RUNNING

    state.backend = "slurm"

    state.run_id = "12345"

    state.running_commit = "abc123"

    manager.save(state)

    return manager


@patch("automation.slurm.slurm_utils.status")
def test_running_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.RUNNING

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.RUNNING

    assert state.status == Status.RUNNING

    assert state.run_id == "12345"

    assert state.running_commit == "abc123"


@patch("automation.slurm.slurm_utils.status")
def test_pending_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.PENDING

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.RUNNING

    assert state.status == Status.RUNNING


@patch("automation.slurm.slurm_utils.status")
def test_completed_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.COMPLETED

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.COMPLETED

    assert state.status == Status.COMPLETED

    assert state.backend is None

    assert state.run_id is None

    assert state.running_commit is None


@patch("automation.slurm.slurm_utils.status")
def test_failed_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.FAILED

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.FAILED

    assert state.status == Status.FAILED

    assert state.backend is None

    assert state.run_id is None

    assert state.running_commit is None


@patch("automation.slurm.slurm_utils.status")
def test_cancelled_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.CANCELLED

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.FAILED

    assert state.status == Status.FAILED


@patch("automation.slurm.slurm_utils.status")
def test_timeout_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.TIMEOUT

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.FAILED

    assert state.status == Status.FAILED


@patch("automation.slurm.slurm_utils.status")
def test_unknown_job(mock_status, tmp_path):

    mock_status.return_value = JobStatus.UNKNOWN

    manager = create_running_state(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    state = manager.load("TEST")

    assert status == Status.RUNNING

    assert state.status == Status.RUNNING


def test_idle_project(tmp_path):

    manager = StateManager(tmp_path)

    monitor = Monitor(manager)

    status = monitor.poll(DummyProject())

    assert status == Status.IDLE