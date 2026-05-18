import pytest

from nexus_os.core.graph.policies.retry import retry_policy


@pytest.mark.parametrize(
    "failed,retries,max_retries,expected",
    [
        (False, 0, 3, "next"),
        (True, 1, 3, "retry"),
        (True, 3, 3, "fallback"),
    ],
)
def test_retry_policy_scenarios(failed, retries, max_retries, expected):
    # Act
    result = retry_policy(failed, retries, max_retries)

    # Assert
    assert result == expected
