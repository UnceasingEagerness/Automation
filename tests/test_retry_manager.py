from unittest.mock import MagicMock, patch

from automation.retry import (
    RetryManager,
    RetryPolicy,
)


def test_retry_success():

    scheduler = MagicMock()

    manager = RetryManager(
        scheduler=scheduler,
        policy=RetryPolicy(
            enabled=True,
            max_retries=3,
            initial_backoff=0,
        ),
    )

    with patch("time.sleep"):

        result = manager.retry(
            project="demo",
            reason="FAILED",
            attempts=0,
        )

    assert result is True

    scheduler.enqueue.assert_called_once_with("demo")


def test_retry_limit():

    scheduler = MagicMock()

    manager = RetryManager(
        scheduler=scheduler,
        policy=RetryPolicy(
            enabled=True,
            max_retries=2,
        ),
    )

    result = manager.retry(
        project="demo",
        reason="FAILED",
        attempts=2,
    )

    assert result is False

    scheduler.enqueue.assert_not_called()


def test_retry_disabled():

    scheduler = MagicMock()

    manager = RetryManager(
        scheduler=scheduler,
        policy=RetryPolicy(
            enabled=False,
        ),
    )

    result = manager.retry(
        project="demo",
        reason="FAILED",
        attempts=0,
    )

    assert result is False

    scheduler.enqueue.assert_not_called()


def test_unknown_reason():

    scheduler = MagicMock()

    manager = RetryManager(
        scheduler=scheduler,
    )

    result = manager.retry(
        project="demo",
        reason="UNKNOWN",
        attempts=0,
    )

    assert result is False

    scheduler.enqueue.assert_not_called()