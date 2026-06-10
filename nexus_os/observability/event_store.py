import json
from pathlib import Path

from nexus_os.observability.event_types import BaseEvent


class EventStore:
    def __init__(self, storage_dir: str = "events"):
        self.base_path = Path(storage_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def append(self, event: BaseEvent) -> None:
        execution_id = event.execution_id
        file_path = self.base_path / f"{execution_id}.jsonl"

        with file_path.open("a", encoding="utf-8") as f:
            data = event.to_dict()
            f.write(json.dumps(data) + "\n")

    def get_events(self, execution_id: str) -> list[dict]:
        file_path = self.base_path / f"{execution_id}.jsonl"

        if not file_path.exists():
            return []

        events = []

        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                events.append(json.loads(line))

        return events

    def persist(self, event: BaseEvent) -> None:
        self.append(event)
