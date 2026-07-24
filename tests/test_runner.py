from datetime import datetime
from unittest.mock import patch

from automation.runner.slurm_runner import SlurmRunner


@patch("automation.slurm.slurm_utils.submit")
def test_runner_start(mock_submit):

    mock_submit.return_value = "12345"

    class DummyProject:
        name = "TEST"
        training_command = "sbatch train.sh"
        local_path = "/tmp"

    class DummyJob:
        project = DummyProject()
        enqueue_time = datetime.now()

    runner = SlurmRunner()

    handle = runner.start(DummyJob())

    assert handle.backend == "slurm"
    assert handle.run_id == "12345"
    assert handle.job_name == "TEST"

    mock_submit.assert_called_once()