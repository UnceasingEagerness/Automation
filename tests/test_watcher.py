from unittest.mock import patch

from automation.core.project import Project
from automation.git.commit import Commit
from automation.state.state_manager import StateManager
from automation.watcher.watcher import Watcher


def create_project():

    return Project(
        name="WATCHER_TEST",
        repo_url="dummy",
        branch="main",
        local_path="/tmp",
        training_command="sbatch train.slurm",
        experiment_dir="experiments/",
        checkpoint_dir="checkpoints/",
        wandb=False,
        telegram=False,
        google_drive=False,
    )


@patch("automation.watcher.watcher.get_new_commits")
def test_first_discovery(mock_commits, tmp_path):

    mock_commits.return_value = [
        Commit("commit1", "main")
    ]

    manager = StateManager(tmp_path)

    watcher = Watcher(manager)

    jobs = watcher.discover(create_project())

    assert len(jobs) == 1

    assert jobs[0].commit == "commit1"

    state = manager.load("WATCHER_TEST")

    assert state.last_seen_commit == "commit1"


@patch("automation.watcher.watcher.get_new_commits")
def test_no_new_commits(mock_commits, tmp_path):

    mock_commits.return_value = []

    manager = StateManager(tmp_path)

    watcher = Watcher(manager)

    jobs = watcher.discover(create_project())

    assert jobs == []


@patch("automation.watcher.watcher.get_new_commits")
def test_multiple_jobs(mock_commits, tmp_path):

    mock_commits.return_value = [
        Commit("sha1", "main"),
        Commit("sha2", "main"),
        Commit("sha3", "main"),
    ]

    manager = StateManager(tmp_path)

    watcher = Watcher(manager)

    jobs = watcher.discover(create_project())

    assert len(jobs) == 3

    assert jobs[0].commit == "sha1"
    assert jobs[1].commit == "sha2"
    assert jobs[2].commit == "sha3"

    state = manager.load("WATCHER_TEST")

    assert state.last_seen_commit == "sha3"