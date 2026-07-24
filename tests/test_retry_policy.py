from automation.retry import RetryPolicy


def test_retry_allowed():

    policy = RetryPolicy(
        enabled=True,
        max_retries=3,
    )

    assert policy.should_retry("FAILED", 0)
    assert policy.should_retry("FAILED", 1)
    assert policy.should_retry("FAILED", 2)


def test_retry_limit():

    policy = RetryPolicy(
        enabled=True,
        max_retries=3,
    )

    assert not policy.should_retry(
        "FAILED",
        3,
    )


def test_retry_disabled():

    policy = RetryPolicy(
        enabled=False,
    )

    assert not policy.should_retry(
        "FAILED",
        0,
    )


def test_unknown_reason():

    policy = RetryPolicy()

    assert not policy.should_retry(
        "SOME_RANDOM_ERROR",
        0,
    )


def test_backoff():

    policy = RetryPolicy(
        initial_backoff=30,
        exponential=True,
    )

    assert policy.next_delay(0) == 30
    assert policy.next_delay(1) == 60
    assert policy.next_delay(2) == 120
    assert policy.next_delay(3) == 240


def test_constant_backoff():

    policy = RetryPolicy(
        initial_backoff=15,
        exponential=False,
    )

    assert policy.next_delay(0) == 15
    assert policy.next_delay(1) == 15
    assert policy.next_delay(2) == 15