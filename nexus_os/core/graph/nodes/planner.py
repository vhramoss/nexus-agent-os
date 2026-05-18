from nexus_os.core.agent_state import AgentState
from nexus_os.core.observability.decorators import traced_node


@traced_node("planner")
def planner_agent_node(state: AgentState) -> AgentState:
    tracer = state.tracer
    event_bus = tracer.event_bus

    state.steps.append("Planner agent")

    try:
        if not state.goal:
            raise ValueError("Empty goal")

        state.plan = {
            "steps": [
                f"Analyze goal: {state.goal}",
                "Decompose tasks",
                "Prepare execution plan",
            ]
        }

        state.planner_failed = False

    except Exception:
        state.planner_retries += 1
        state.planner_failed = True

        event_bus.publish(
            "retry.triggered",
            {
                "trace_id": tracer.trace_id,
                "component": "planner",
                "status": "retrying",
                "metadata": {"attempt": state.planner_retries},
            },
        )

        return state

    return state