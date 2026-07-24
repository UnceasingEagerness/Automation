from datetime import datetime
from unittest.mock import MagicMock

from flax.nnx import state

from automation.core.project import Project
from automation.job.job import Job
from automation.runner.run_handle import RunHandle
from automation.scheduler.scheduler import Scheduler
from automation.state.state_manager import StateManager
from automation.state.status import Status


def create_project(name="TEST"):

    return Project(
        name=name,
        repo_url="dummy",
        branch="main",
        local_path="/tmp",
        training_command="sbatch train.slurm",
        experiment_dir="exp",
        checkpoint_dir="ckpt",
        wandb=False,
        telegram=False,
        google_drive=False,
    )


def create_job(name="TEST"):

    return Job(
        project=create_project(name),
        commit="abc123",
    )


def create_scheduler(tmp_path):

    runner = MagicMock()

    runner.start.return_value = RunHandle(
        backend="slurm",
        run_id="12345",
        submit_time=datetime.now(),
        job_name="TEST",
    )

    manager = StateManager(tmp_path)

    scheduler = Scheduler(
        runner=runner,
        state_manager=manager,
    )

    return scheduler, runner, manager


def test_enqueue_changes_state(tmp_path):

    scheduler, _, manager = create_scheduler(tmp_path)

    scheduler.enqueue(create_job())

    state = manager.load("TEST")

    assert state.status == Status.QUEUED


def test_dispatch_changes_state(tmp_path):

    scheduler, runner, manager = create_scheduler(tmp_path)

    job = create_job()

    scheduler.enqueue(job)

    handle = scheduler.dispatch()

    runner.start.assert_called_once_with(job)

    state = manager.load("TEST")

    assert state.status == Status.RUNNING

    assert state.running_commit == "abc123"

    assert state.backend == "slurm"
    assert state.run_id == "12345"

    assert handle.run_id == "12345"


def test_complete_changes_state(tmp_path):

    scheduler, _, manager = create_scheduler(tmp_path)

    manager.load("TEST")

    scheduler.complete("TEST")

    state = manager.load("TEST")

    assert state.status == Status.COMPLETED


def test_fail_changes_state(tmp_path):

    scheduler, _, manager = create_scheduler(tmp_path)

    manager.load("TEST")

    scheduler.fail("TEST")

    state = manager.load("TEST")

    assert state.status == Status.FAILED


def test_fifo_order(tmp_path):

    scheduler, runner, _ = create_scheduler(tmp_path)

    job1 = create_job("P1")
    job2 = create_job("P2")

    scheduler.enqueue(job1)
    scheduler.enqueue(job2)

    scheduler.dispatch()
    scheduler.dispatch()

    calls = runner.start.call_args_list

    assert len(calls) == 2

    assert calls[0].args[0] == job1

    assert calls[1].args[0] == job2