from fastapi import APIRouter, HTTPException

from nexus_os.domain.workflow.state_machine import StateMachine
from nexus_os.observability.event_store import event_store
from nexus_os.observability.metrics.builder import build_metrics
from nexus_os.observability.state_rebuilder import StateRebuilder
from nexus_os.state.timeline.builder import build_execution_timeline

router = APIRouter()

machine = StateMachine()
rebuilder = StateRebuilder(machine)


@router.get("/replay/{execution_id}")
def replay(execution_id: str):
    events = event_store.get_events(execution_id)

    if not events:
        raise HTTPException(status_code=404, detail="Execution not found")

    # 🧾 timeline de eventos (debug)
    timeline = build_execution_timeline(events)

    # 🧠 estado reconstruído (core!)
    state = rebuilder.rebuild(events)

    # 📊 métricas
    metrics = build_metrics(events)

    input_data = None
    result_data = None

    for event in events:
        if event["event_type"] == "agent.started" and not input_data:
            input_data = event.get("metadata", {})

        if event["event_type"] == "agent.completed":
            result_data = event.get("metadata", {})

    return {
        "execution_id": execution_id,
        "input": input_data,
        "metrics": metrics,
        "timeline": timeline,
        "state": state,  # 🔥 NOVO
        "result": result_data,
    }
