import uuid
from datetime import UTC, datetime

from nexus_os.observability.event_types import Event, EventPayload, Subscriber


class EventBus:
    def __init__(self):
        self.subscribers: dict[str, list[Subscriber]] = {}

    def subscribe(self, event_type: str, callback: Subscriber) -> None:
        self.subscribers.setdefault(event_type, []).append(callback)

    def publish(self, event_type: str, payload: EventPayload) -> None:
        event = self._build_event(event_type, payload)

        # Subscribers específicos
        for callback in self.subscribers.get(event_type, []):
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus] subscriber error: {e}")

        # Subscribers globais (*)
        for callback in self.subscribers.get("*", []):
            try:
                callback(event)
            except Exception as e:
                print(f"[EventBus] subscriber error: {e}")

    def _build_event(self, event_type: str, payload: EventPayload) -> Event:
        return {
            "id": str(uuid.uuid4()),
            "trace_id": payload.get("trace_id") or "unknown",
            "event_type": event_type,
            "timestamp": datetime.now(UTC).isoformat(),
            "component": payload.get("component", "unknown"),
            "status": payload.get("status", "unknown"),
            "metadata": payload.get("metadata", {}),
        }
