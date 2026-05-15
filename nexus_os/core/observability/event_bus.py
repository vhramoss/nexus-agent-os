from typing import Callable, Dict, Any, List
from datetime import datetime, timezone
import uuid


class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        self.subscribers.setdefault(event_type, []).append(callback)

    def publish(self, event_type: str, payload: Dict[str, Any]):
        event = self._build_event(event_type, payload)

        # Subscribers específicos
        for callback in self.subscribers.get(event_type, []):
            callback(event)

        # Subscribers globais (*)
        for callback in self.subscribers.get("*", []):
            callback(event)
    
    def _build_event(self, event_type: str, payload: Dict [str, Any]):
        return {
            "id": str(uuid.uuid4()),
            "trace_id": payload.get("trace_id"),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": payload.get("component","unknown"),
            "status": payload.get("status", "unknown"),
            "metadata": payload.get("metadata",{}),
        }