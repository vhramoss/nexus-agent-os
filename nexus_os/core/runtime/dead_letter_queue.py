from typing import Any, Dict, List
from datetime import datetime

class DeadLetterQueue:

    def __init__(self):
        self.items: List[Dict[str, Any]] = []

    def push(self, record: Dict[str, Any]):
        record["dlq_timestamp"] = datetime.utcnow().isoformat()
        self.items.append(record)

    def all(self) -> List[Dict[str, Any]]:
        return self.items
