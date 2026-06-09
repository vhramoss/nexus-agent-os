from nexus_os.state.timeline.builder import build_execution_timeline


def test_build_timeline_returns_empty_when_no_events():
    # Arrange
    events = []

    # Act
    timeline = build_execution_timeline(events)

    # Assert
    assert timeline == []


def test_build_timeline_returns_non_empty_when_events_exist():
    # Arrange
    events = [
        {
            "event_type": "node.started",
            "timestamp": "2024-01-01T00:00:01",
            "component": "planner",
            "status": "started",
            "metadata": {},
        },
        {
            "event_type": "node.completed",
            "timestamp": "2024-01-01T00:00:02",
            "component": "planner",
            "status": "completed",
            "metadata": {},
        },
    ]

    # Act
    timeline = build_execution_timeline(events)

    # Assert
    assert len(timeline) > 0


def test_build_timeline_contains_expected_keys():
    # Arrange
    events = [
        {
            "event_type": "node.started",
            "timestamp": "2024-01-01T00:00:01",
            "component": "planner",
            "status": "started",
            "metadata": {},
        }
    ]

    # Act
    timeline = build_execution_timeline(events)

    # Assert
    first_item = timeline[0]

    assert "time" in first_item
    assert "event" in first_item
    assert "component" in first_item
    assert "status" in first_item
