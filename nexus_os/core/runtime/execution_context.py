import time
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ExecutionContext:
    trace_id: str
    start_time: float = field(default_factory=time.monotonic)
    start_wall_time: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    end_time: float | None = None
    end_wall_time: str | None = None

    attempts: int = 0
    status: str = "started"

    def finish(self, status: str):
        self.end_time = time.monotonic()
        self.end_wall_time = datetime.now(UTC).isoformat()
        self.status = status

    @property
    def duration(self) -> float | None:
        if self.end_time is None:
            return None
        return self.end_time - self.start_time

    def increment_attempts(self):
        self.attempts += 1
