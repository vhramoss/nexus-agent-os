import json
from pathlib import Path
from typing import Any


class ExecutionStore:
    def __init__(self, path: str = "executions.json"):
        self.path = Path(path)

        if not self.path.exists():
            self._write({})

    def _read(self) -> dict:
        with open(self.path) as f:
            return json.load(f)

    def _write(self, data: dict):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def exists(self, execution_id: str) -> bool:
        data = self._read()
        return execution_id in data

    def get(self, execution_id: str) -> dict[str, Any] | None:
        return self._read().get(execution_id)

    def save(self, execution_id: str, record: dict[str, Any]):
        data = self._read()
        data[execution_id] = record
        self._write(data)

    def save_step(self, execution_id: str, step_name: str, data: dict):
        record = self.get(execution_id) or {}

        steps = record.get("steps", {})
        steps[step_name] = data

        record["steps"] = steps

        self.save(execution_id, record)

    def get_steps(self, execution_id: str):
        record = self.get(execution_id)
        if not record:
            return {}

        return record.get("steps", {})
