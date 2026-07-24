from abc import ABC, abstractmethod

from automation.job.job import Job
from automation.runner.run_handle import RunHandle


class Runner(ABC):
    """
    Abstract execution backend.
    """

    @abstractmethod
    def start(self, job: Job) -> RunHandle:
        """
        Submit a job.

        Returns
        -------
        RunHandle
            Information required to monitor the run.
        """
        raise NotImplementedError