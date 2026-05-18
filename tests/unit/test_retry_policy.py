import pytest
from nexus_os.core.graph.policies.retry import retry_policy


def test_retry_policy_returns_next_when_no_failure():
    # Arrange
    failed = False
    retries = 0
    max_retries = 3

    # Act
    result = retry_policy(failed, retries, max_retries)

    # Assert
    assert result == "next"

def test_retry_policy_returns_retry_when_failed_and_under_limit():
# Arrange
    failed = True
    retries = 1
    max_retries = 3

    # Act
    result = retry_policy(failed, retries, max_retries)

    # Assert
    assert result == "retry"

def test_retry_policy_returns_fallback_when_retries_exhausted():
    # Arrange
    failed = True
    retries = 3
    max_retries = 3

    # Act
    result = retry_policy(failed, retries, max_retries)

    # Assert
    assert result == "fallback"
