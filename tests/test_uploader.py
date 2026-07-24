from pathlib import Path

import pytest

from automation.uploader import (
    LocalUploader,
    CompositeUploader,
)


def test_local_uploader_returns_absolute_path(tmp_path):

    uploader = LocalUploader()

    artifact = tmp_path / "run"

    artifact.mkdir()

    result = uploader.upload(artifact)

    assert Path(result).resolve() == artifact.resolve()


def test_local_uploader_missing_directory(tmp_path):

    uploader = LocalUploader()

    missing = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        uploader.upload(missing)


class DummyUploader:

    def __init__(self):

        self.called = False

    def upload(self, artifact_dir):

        self.called = True

        return f"uploaded:{artifact_dir.name}"


def test_composite_uploader():

    uploader1 = DummyUploader()

    uploader2 = DummyUploader()

    composite = CompositeUploader(
        [
            uploader1,
            uploader2,
        ]
    )

    result = composite.upload(
        Path("/tmp/run")
    )

    assert uploader1.called
    assert uploader2.called

    assert result == [
        "uploaded:run",
        "uploaded:run",
    ]