from typing import List, Dict, Any

def build_execution_timeline(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Transforma eventos brutos em uma timeline ordenada e legível.
    """
    timeline = []

    for event in sorted(events, key=lambda e: e["timestamp"]):
        timeline.append({
            "time": event["timestamp"],
            "event": event["event_type"],
            "component": event.get("component"),
            "status": event.get("status"),
            "metadata": event.get("metadata", {}),
        })
    return timeline