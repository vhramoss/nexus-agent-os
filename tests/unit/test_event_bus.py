from nexus_os.core.observability.event_bus import EventBus


def test_event_bus_calls_subscriber_on_publish():
    # Arrange
    bus = EventBus()
    received = []

    def subscriber(event):
        received.append(event)

    bus.subscribe("test.event", subscriber)

    # Act
    bus.publish("test.event", {"trace_id": "123"})

    # Assert
    assert len(received) == 1


def test_event_bus_calls_global_subscriber():
    # Arrange
    bus = EventBus()
    received = []

    def subscriber(event):
        received.append(event)

    bus.subscribe("*", subscriber)

    # Act
    bus.publish("any.event", {"trace_id": "123"})

    # Assert
    assert len(received) == 1


def test_event_bus_isolates_subscriber_errors():
    # Arrange
    bus = EventBus()
    received = []

    def bad_subscriber(event):
        raise Exception("fail")

    def good_subscriber(event):
        received.append(event)

    bus.subscribe("test.event", bad_subscriber)
    bus.subscribe("test.event", good_subscriber)

    # Act
    bus.publish("test.event", {"trace_id": "123"})

    # Assert
    assert len(received) == 1


def test_event_bus_builds_event_with_expected_keys():
    # Arrange
    bus = EventBus()
    received = []

    def subscriber(event):
        received.append(event)

    bus.subscribe("test.event", subscriber)

    # Act
    bus.publish("test.event", {"trace_id": "123"})

    # Assert
    event = received[0]

    assert "id" in event
    assert "trace_id" in event
    assert "event_type" in event
    assert "timestamp" in event
    assert "component" in event
    assert "status" in event
    assert "metadata" in event
