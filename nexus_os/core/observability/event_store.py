import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime


class EventStore:
    """
    Event store simples baseado em append-only JSON.
    Em produção isso vira DB / Kafka / S3.
    """

    def __init__(self, path: str = "events"):
        self.base_path = Path(path)
        self.base_path.mkdir(exist_ok=True)

    def persist(self, event: Dict[str, Any]):
        trace_id = event.get("payload", {}).get("trace_id", "unknown")
        timestamp = datetime.utcnow().isoformat()

        file_path = self.base_path / f"{trace_id}.jsonl"

        with file_path.open("a") as f:
            f.write(json.dumps({
                "timestamp": timestamp,
                **event
            }) + "\n")