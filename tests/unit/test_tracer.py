import pytest

from nexus_os.observability.event_bus import EventBus
from nexus_os.observability.tracer import Tracer


def test_tracer_publishes_node_started_and_completed():
    # Arrange
    bus = EventBus()
    events = []

    def capture(event):
        events.append(event)

    bus.subscribe("*", capture)

    tracer = Tracer(event_bus=bus, trace_id="123")

    # Act
    with tracer.span("test-node"):
        pass

    # Assert
    event_types = [e["event_type"] for e in events]

    assert "node.started" in event_types
    assert "node.completed" in event_types


def test_tracer_publishes_node_failed_on_exception():
    # Arrange
    bus = EventBus()
    events = []

    def capture(event):
        events.append(event)

    bus.subscribe("*", capture)

    tracer = Tracer(event_bus=bus, trace_id="123")

    # Act
    with pytest.raises(ValueError):
        with tracer.span("test-node"):
            raise ValueError("error")

    # Assert
    event_types = [e["event_type"] for e in events]

    assert "node.started" in event_types
    assert "node.failed" in event_types


def test_tracer_records_duration_on_completed():
    # Arrange
    bus = EventBus()
    events = []

    def capture(event):
        events.append(event)

    bus.subscribe("*", capture)

    tracer = Tracer(event_bus=bus, trace_id="123")

    # Act
    with tracer.span("test-node"):
        pass

    # Assert
    completed_events = [e for e in events if e["event_type"] == "node.completed"]

    assert len(completed_events) == 1
    assert "duration_ms" in completed_events[0]["metadata"]


def test_tracer_reraises_exception_after_logging():
    # Arrange
    bus = EventBus()
    tracer = Tracer(event_bus=bus, trace_id="123")

    # Act & Assert
    with pytest.raises(RuntimeError):
        with tracer.span("test-node"):
            raise RuntimeError("boom")
