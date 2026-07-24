from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RetryPolicy:
    """
    Defines retry behaviour for failed jobs.
    """

    enabled: bool = True

    max_retries: int = 3

    initial_backoff: int = 30

    exponential: bool = True

    retry_on: set[str] = field(
        default_factory=lambda: {
            "FAILED",
            "TIMEOUT",
            "NODE_FAIL",
            "PREEMPTED",
        }
    )

    def should_retry(
        self,
        reason: str,
        attempts: int,
    ) -> bool:

        if not self.enabled:
            return False

        if attempts >= self.max_retries:
            return False

        return reason in self.retry_on

    def next_delay(
        self,
        attempts: int,
    ) -> int:

        if not self.exponential:
            return self.initial_backoff

        return self.initial_backoff * (2 ** attempts)