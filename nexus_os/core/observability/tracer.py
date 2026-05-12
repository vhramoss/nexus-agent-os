from contextlib import contextmanager
from time import perf_counter
from typing import Dict, Any


class Tracer:
    def __init__(self, event_bus, trace_id: str):
        self.event_bus = event_bus
        self.trace_id = trace_id

    @contextmanager
    def span(self, name: str, extra: Dict[str, Any] | None = None):
        start = perf_counter()

        self.event_bus.publish(
            "node.started",
            {
                "trace_id": self.trace_id,
                "node": name,
                "extra": extra or {},
            },
        )

        try:
            yield
        except Exception as e:
            self.event_bus.publish(
                "node.failed",
                {
                    "trace_id": self.trace_id,
                    "node": name,
                    "error": str(e),
                },
            )
            raise
        finally:
            duration = int((perf_counter() - start) * 1000)
            self.event_bus.publish(
                "node.completed",
                {
                    "trace_id": self.trace_id,
                    "node": name,
                    "duration_ms": duration,
                },
            )