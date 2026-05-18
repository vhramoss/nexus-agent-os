from nexus_os.core.metrics.builder import build_metrics


def test_build_metrics_returns_empty_when_no_events():
    # Arrange
    events = []

    # Act
    metrics = build_metrics(events)

    # Assert
    assert metrics == {}


def test_build_metrics_counts_nodes_and_retries():
    # Arrange
    events = [
        {
            "event_type": "node.completed",
            "timestamp": "2024-01-01T00:00:01",
        },
        {
            "event_type": "node.completed",
            "timestamp": "2024-01-01T00:00:02",
        },
        {
            "event_type": "retry.triggered",
            "timestamp": "2024-01-01T00:00:03",
        },
    ]

    # Act
    metrics = build_metrics(events)

    # Assert
    assert metrics["node_count"] == 2
    assert metrics["retry_count"] == 1


def test_build_metrics_detects_failure():
    # Arrange
    events = [
        {
            "event_type": "fallback.executed",
            "timestamp": "2024-01-01T00:00:01",
        }
    ]

    # Act
    metrics = build_metrics(events)

    # Assert
    assert metrics["failure"] is True
