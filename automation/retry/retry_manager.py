from __future__ import annotations

import time

from .retry_policy import RetryPolicy


class RetryManager:
    """
    Handles retry scheduling.

    This class is backend-independent.
    It simply waits (if required) and
    asks the scheduler to submit again.
    """

    def __init__(
        self,
        scheduler,
        policy: RetryPolicy | None = None,
    ):

        self.scheduler = scheduler

        self.policy = policy or RetryPolicy()

    def retry(
        self,
        project,
        reason: str,
        attempts: int,
    ) -> bool:

        if not self.policy.should_retry(
            reason,
            attempts,
        ):
            return False

        delay = self.policy.next_delay(
            attempts,
        )

        time.sleep(delay)

        self.scheduler.enqueue(project)

        return True