from contextlib import contextmanager
from time import perf_counter
from typing import Dict, Any, Optional
from nexus_os.core.observability.event_bus import EventBus

class Tracer:
    event_bus: EventBus
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
                "component": name,
                "status": "started",
                "metadata": extra or {},
            },
        )

        success = True
        try:
            yield
        except Exception as e:
            success = False

            self.event_bus.publish(
                "node.failed",
                {
                    "trace_id": self.trace_id,
                    "component": name,
                    "status": "failed",
                    "metadata": {"error": str(e)},
                },
            )
            raise
        finally:
            duration = int((perf_counter() - start) * 1000)
            if success:
                self.event_bus.publish(
                    "node.completed",
                    {
                        "trace_id": self.trace_id,
                        "component": name,
                        "status": "completed",
                        "metadata":{"duration_ms": duration},
                    },
                )