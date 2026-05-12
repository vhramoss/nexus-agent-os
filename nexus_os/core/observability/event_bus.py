from typing import Callable, Dict, List, Any
from datetime import datetime, timezone
import uuid

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}
    
    def subscribe(self, event_type: str, callback: Callable[[Dict[str, Any]], None]):
        self.subscribers.setdefault(event_type, []).append(callback)

    def publish(self, event_type: str, data: Dict[str, Any]):
        event = {
            "id": str(uuid.uuid4()),
            "type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
        for callback in self.subscribers.get(event_type, []):
            callback(event)