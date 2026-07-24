from unittest.mock import patch

from automation.git.commit import Commit
from automation.utils.git_utils import get_new_commits


@patch("automation.utils.git_utils.git_fetch")
@patch("automation.utils.git_utils.get_remote_commit")
def test_first_run_returns_head(mock_remote, mock_fetch):

    mock_remote.return_value = "HEAD_SHA"

    commits = get_new_commits(
        "/tmp",
        "main",
        None,
    )

    assert len(commits) == 1

    assert commits[0] == Commit(
        sha="HEAD_SHA",
        branch="main",
    )


@patch("automation.utils.git_utils.git_fetch")
@patch("automation.utils.git_utils.run_git_command")
def test_no_new_commits(mock_git, mock_fetch):

    mock_git.return_value = ""

    commits = get_new_commits(
        "/tmp",
        "main",
        "old_sha",
    )

    assert commits == []


@patch("automation.utils.git_utils.git_fetch")
@patch("automation.utils.git_utils.run_git_command")
def test_multiple_commits(mock_git, mock_fetch):

    mock_git.return_value = (
        "sha1\n"
        "sha2\n"
        "sha3"
    )

    commits = get_new_commits(
        "/tmp",
        "main",
        "old_sha",
    )

    assert len(commits) == 3

    assert commits[0].sha == "sha1"

    assert commits[1].sha == "sha2"

    assert commits[2].sha == "sha3"


@patch("automation.utils.git_utils.git_fetch")
@patch("automation.utils.git_utils.run_git_command")
def test_branch_saved(mock_git, mock_fetch):

    mock_git.return_value = "abc"

    commits = get_new_commits(
        "/tmp",
        "develop",
        "old_sha",
    )

    assert commits[0].branch == "develop"
