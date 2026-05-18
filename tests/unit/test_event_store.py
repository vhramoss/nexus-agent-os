from nexus_os.core.observability.event_store import EventStore


def test_event_store_creates_file(tmp_path):
    # Arrange
    store = EventStore(storage_dir=str(tmp_path))

    event = {
        "trace_id": "123",
        "event_type": "test",
    }

    # Act
    store.append(event)

    # Assert
    files = list(tmp_path.iterdir())
    assert len(files) == 1

def test_event_store_appends_events(tmp_path):
    store = EventStore(storage_dir=str(tmp_path))

    event1 = {"trace_id": "123", "event_type": "test1"}
    event2 = {"trace_id": "123", "event_type": "test2"}

    store.append(event1)
    store.append(event2)

    file = list(tmp_path.iterdir())[0]

    lines = file.read_text().splitlines()

    assert len(lines) == 2

def test_event_store_reads_events(tmp_path):
    store = EventStore(storage_dir=str(tmp_path))

    event = {"trace_id": "123", "event_type": "test"}

    store.append(event)

    events = store.get_events("123")

    assert len(events) == 1
    assert events[0]["event_type"] == "test"

