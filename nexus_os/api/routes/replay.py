from fastapi import APIRouter, HTTPException

from nexus_os.observability.event_store import EventStore
from nexus_os.observability.metrics.builder import build_metrics
from nexus_os.state.timeline.builder import build_execution_timeline

router = APIRouter()
event_store = EventStore()


@router.get("/replay/{trace_id}")
def replay(trace_id: str):
    events = event_store.get_events(trace_id)

    if not events:
        raise HTTPException(status_code=404, detail="Trace not found")

    timeline = build_execution_timeline(events)
    metrics = build_metrics(events)

    input_data = None
    result_data = None

    for event in events:
        if event["event_type"] == "agent.started":
            input_data = event.get("metadata", {})

        if event["event_type"] == "agent.completed":
            result_data = event.get("metadata", {})

    return {
        "trace_id": trace_id,
        "input": input_data,
        "metrics": metrics,
        "timeline": timeline,
        "result": result_data,
    }
