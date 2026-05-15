from typing import List, Dict, Any
from datetime import datetime


def build_metrics(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not events:
        return {}

    # ordenar por tempo
    events = sorted(events, key=lambda e: e["timestamp"])

    # tempo total
    start = datetime.fromisoformat(events[0]["timestamp"])
    end = datetime.fromisoformat(events[-1]["timestamp"])

    total_duration_ms = int((end - start).total_seconds() * 1000)

    # contagem de eventos importantes
    node_count = sum(1 for e in events if e["event_type"] == "node.completed")

    retry_count = sum(1 for e in events if e["event_type"] == "retry.triggered")

    failure = any(e["event_type"] == "fallback.executed" for e in events)

    return {
        "total_duration_ms": total_duration_ms,
        "node_count": node_count,
        "retry_count": retry_count,
        "failure": failure,
    }