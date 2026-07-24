import re
import subprocess

from automation.slurm.job_status import JobStatus


def submit(command: str, cwd: str) -> str:
    """
    Submit a Slurm job.
    """

    result = subprocess.run(
        command.split(),
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout.strip()

    match = re.search(r"Submitted batch job (\d+)", output)

    if match is None:
        raise RuntimeError(
            f"Unable to parse sbatch output:\n{output}"
        )

    return match.group(1)


def status(job_id: str) -> JobStatus:
    """
    Returns the current Slurm status of a job.

    Uses sacct because jobs remain queryable after completion.
    """

    result = subprocess.run(
        [
            "sacct",
            "-j",
            job_id,
            "--format=State",
            "--noheader",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout.strip()

    if output == "":
        return JobStatus.UNKNOWN

    state = output.split()[0].upper()

    mapping = {
        "PENDING": JobStatus.PENDING,
        "CONFIGURING": JobStatus.PENDING,
        "RUNNING": JobStatus.RUNNING,
        "COMPLETED": JobStatus.COMPLETED,
        "FAILED": JobStatus.FAILED,
        "CANCELLED": JobStatus.CANCELLED,
        "TIMEOUT": JobStatus.TIMEOUT,
    }

    return mapping.get(state, JobStatus.UNKNOWN)


def cancel(job_id: str):

    subprocess.run(
        ["scancel", job_id],
        check=True,
    )