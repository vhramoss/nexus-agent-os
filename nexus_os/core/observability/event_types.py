from typing import Callable, Dict, Any, TypedDict

class Event(TypedDict):
    id: str
    trace_id: str
    event_type: str
    timestamp: str
    component: str
    status: str
    metadata: Dict[str, Any]

Subscriber = Callable[[Event], None]

class EventPayload(TypedDict, total=False):
    trace_id: str
    component: str
    status: str
    metadata: Dict[str, Any]
