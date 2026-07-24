from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Commit:
    """
    Represents a Git commit discovered by the watcher.
    """

    sha: str

    branch: str
