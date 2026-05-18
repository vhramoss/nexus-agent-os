from nexus_os.core.runtime.supervisor import Supervisor


def test_supervisor_returns_dlq_when_reason_is_timeout():
    # Arrange
    supervisor = Supervisor()

    context = {
        "reason": "timeout",
        "attempts": 0,
    }

    # Act
    result = supervisor.decide(context)

    # Assert
    assert result == "dlq"


def test_supervisor_returns_retry_on_first_exception():
    # Arrange
    supervisor = Supervisor()

    context = {
        "reason": "exception",
        "attempts": 0,
    }

    # Act
    result = supervisor.decide(context)

    # Assert
    assert result == "retry"


def test_supervisor_returns_dlq_after_max_retries():
    # Arrange
    supervisor = Supervisor()

    context = {
        "reason": "exception",
        "attempts": 1,
    }

    # Act
    result = supervisor.decide(context)

    # Assert
    assert result == "dlq"


def test_supervisor_returns_abort_for_unknown_reason():
    # Arrange
    supervisor = Supervisor()

    context = {
        "reason": "unknown",
        "attempts": 0,
    }

    # Act
    result = supervisor.decide(context)

    # Assert
    assert result == "abort"
