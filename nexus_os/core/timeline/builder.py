from typing import Any


def build_execution_timeline(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Transforma eventos brutos em uma timeline ordenada e legível.
    """
    timeline = []

    for event in sorted(events, key=lambda e: e["timestamp"]):
        timeline.append(
            {
                "time": event["timestamp"],
                "event": event["event_type"],
                "component": event.get("component"),
                "status": event.get("status"),
                "metadata": event.get("metadata", {}),
            }
        )
    return timeline
