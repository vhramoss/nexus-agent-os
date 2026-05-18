import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone


class EventStore:
    def __init__(self, storage_dir: str = "events"):
        self.base_path = Path(storage_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def append(self, event: Dict[str, Any]) -> None:
        trace_id = event.get("trace_id", "unknown")
        timestamp = datetime.now(timezone.utc).isoformat()

        file_path = self.base_path / f"{trace_id}.jsonl"

        with file_path.open("a") as f:
            data = {**event}
            if "timestamp" not in data:
                data["timestamp"] = timestamp

            f.write(json.dumps(data) + "\n")

    def get_events(self, trace_id: str) -> List[Dict[str, Any]]:
        file_path = self.base_path / f"{trace_id}.jsonl"

        if not file_path.exists():
            return []

        events = []

        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                events.append(json.loads(line))

        return events

                
    def persist(self, event: Dict[str, Any]) -> None:
        self.append(event)

    
