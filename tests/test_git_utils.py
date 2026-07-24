from automation.utils.git_utils import (
    get_local_commit,
    get_remote_commit,
    has_new_commit,
)


REPO = "/home/trizzz/AUV_Project/RLSim/final_marl"


def test_local_commit():

    commit = get_local_commit(REPO)

    assert len(commit) == 40


def test_remote_commit():

    commit = get_remote_commit(REPO, "main")

    assert len(commit) == 40


def test_has_new_commit():

    result = has_new_commit(REPO, "main")

    assert isinstance(result, bool)