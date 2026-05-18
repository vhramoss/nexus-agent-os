from nexus_os.core.runtime.dead_letter_queue import DeadLetterQueue


def test_dlq_starts_empty():
    # Arrange
    dlq = DeadLetterQueue()

    # Act
    items = dlq.all()

    # Assert
    assert items == []


def test_dlq_push_adds_record():
    # Arrange
    dlq = DeadLetterQueue()
    record = {"trace_id": "123"}

    # Act
    dlq.push(record)
    items = dlq.all()

    # Assert
    assert len(items) == 1


def test_dlq_preserves_order():
    # Arrange
    dlq = DeadLetterQueue()

    dlq.push({"trace_id": "1"})
    dlq.push({"trace_id": "2"})

    # Act
    items = dlq.all()

    # Assert
    assert items[0]["trace_id"] == "1"
    assert items[1]["trace_id"] == "2"


def test_dlq_push_adds_timestamp():
    # Arrange
    dlq = DeadLetterQueue()
    record = {"trace_id": "123"}

    # Act
    dlq.push(record)
    item = dlq.all()[0]

    # Assert
    assert "dlq_timestamp" in item
