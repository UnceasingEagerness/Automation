from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable


class Uploader(ABC):
    """
    Base class for all artifact uploaders.

    Every uploader receives a directory containing an
    experiment's artifacts and uploads it somewhere.

    Examples
    --------
    Local filesystem
    Google Drive
    Dropbox
    S3
    NAS
    """

    @abstractmethod
    def upload(
        self,
        artifact_dir: Path,
    ) -> str:
        """
        Upload an artifact directory.

        Parameters
        ----------
        artifact_dir
            Directory containing experiment outputs.

        Returns
        -------
        str
            URI/location of uploaded artifacts.
        """
        raise NotImplementedError


class LocalUploader(Uploader):
    """
    Dummy uploader.

    Used for development and testing.

    Simply returns the absolute path.
    """

    def upload(
        self,
        artifact_dir: Path,
    ) -> str:

        artifact_dir = Path(artifact_dir).resolve()

        if not artifact_dir.exists():
            raise FileNotFoundError(artifact_dir)

        return str(artifact_dir)


class CompositeUploader(Uploader):
    """
    Upload to multiple destinations.

    Example
    -------

    Local

        +

    Google Drive

        +

    S3
    """

    def __init__(
        self,
        uploaders: Iterable[Uploader],
    ):

        self.uploaders = list(uploaders)

    def upload(
        self,
        artifact_dir: Path,
    ) -> list[str]:

        results = []

        for uploader in self.uploaders:
            results.append(
                uploader.upload(artifact_dir)
            )

        return results