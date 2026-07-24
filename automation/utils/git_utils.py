from pathlib import Path
import subprocess
from automation.git.commit import Commit

class GitError(Exception):
    """Raised when a git command fails."""
    pass


def run_git_command(repo_path: str, args: list[str]) -> str:
    """
    Execute a git command inside a repository.

    Parameters
    ----------
    repo_path : str
        Local repository path.
    args : list
        Git arguments.

    Returns
    -------
    str
        stdout of git command.
    """

    result = subprocess.run(
        ["git"] + args,
        cwd=Path(repo_path),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise GitError(result.stderr.strip())

    return result.stdout.strip()


def git_fetch(repo_path: str):
    run_git_command(repo_path, ["fetch"])


def get_local_commit(repo_path: str) -> str:
    return run_git_command(repo_path, ["rev-parse", "HEAD"])


def get_remote_commit(repo_path: str, branch: str) -> str:
    return run_git_command(
        repo_path,
        ["rev-parse", f"origin/{branch}"]
    )


def has_new_commit(repo_path: str, branch: str) -> bool:
    """
    Compare local and remote commits.
    """

    git_fetch(repo_path)

    local = get_local_commit(repo_path)
    remote = get_remote_commit(repo_path, branch)

    return local != remote

def get_new_commits(
    repo_path: str,
    branch: str,
    last_seen_commit: str | None,
) -> list[Commit]:
    """
    Return all commits after `last_seen_commit` in chronological order.

    If last_seen_commit is None, return only the current HEAD.
    """

    git_fetch(repo_path)

    if last_seen_commit is None:

        sha = get_remote_commit(repo_path, branch)

        return [
            Commit(
                sha=sha,
                branch=branch,
            )
        ]

    output = run_git_command(
        repo_path,
        [
            "log",
            "--reverse",
            "--format=%H",
            f"{last_seen_commit}..origin/{branch}",
        ],
    )

    if not output:
        return []

    return [
        Commit(
            sha=sha,
            branch=branch,
        )
        for sha in output.splitlines()
    ]