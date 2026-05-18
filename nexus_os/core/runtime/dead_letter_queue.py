from datetime import datetime
from typing import Any


class DeadLetterQueue:
    def __init__(self):
        self.items: list[dict[str, Any]] = []

    def push(self, record: dict[str, Any]):
        record["dlq_timestamp"] = datetime.utcnow().isoformat()
        self.items.append(record)

    def all(self) -> list[dict[str, Any]]:
        return self.items
