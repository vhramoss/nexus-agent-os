from typing import Dict, Any
from nexus_os.core.observability.event_bus import EventBus


class Telemetry:
    def __init__(self, event_bus:EventBus):
        self.event_bus = event_bus

    # ------------------------
    # Agent lifecycle
    # ------------------------

    def agent_started(self, trace_id: str, goal: str) -> None:
        self.event_bus.publish(
            "agent.started",
            {
                "trace_id": trace_id,
                "component": "agent",
                "status": "started",
                "metadata": {"goal": goal},
            },
        )

    def agent_completed(self, trace_id: str, status: str) -> None:
        self.event_bus.publish(
            "agent.completed",
            {
                "trace_id": trace_id,
                "component": "agent",
                "status": "completed",
                "metadata": {"status": status},
            },
        )

    # ------------------------
    # Runtime
    # ------------------------

    def retry(self, trace_id: str, attempt: int) -> None:
        self.event_bus.publish(
            "retry.triggered",
            {
                "trace_id": trace_id,
                "component": "runtime",
                "status": "retrying",
                "metadata": {"attempt": attempt},
            },
        )

    def fallback(self, trace_id: str, reason: str) -> None:
        self.event_bus.publish(
            "fallback.executed",
            {
                "trace_id": trace_id,
                "component": "runtime",
                "status": "fallback",
                "metadata": {"reason": reason},
            },
        )
