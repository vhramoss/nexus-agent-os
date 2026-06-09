from datetime import UTC, datetime
from typing import Any


class DeadLetterQueue:
    def __init__(self):
        self.items: list[dict[str, Any]] = []

    def push(self, record: dict[str, Any]):
        enriched = {
            **record,
            "dlq_timestamp": datetime.now(UTC).isoformat(),
        }

        self.items.append(enriched)

    def all(self) -> list[dict[str, Any]]:
        return list(self.items)
