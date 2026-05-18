from nexus_os.core.agent_state import AgentState
from nexus_os.core.observability.decorators import traced_node
from nexus_os.core.security.capabilities import Capability
from nexus_os.core.security.guarded import guarded


def execute_tool(goal: str) -> dict:
    return {
        "computed_value": len(goal),
        "status": "ok",
    }


@guarded(Capability.USE_TOOL)
@traced_node("tool")
def tool_agent_node(state: AgentState) -> AgentState:
    tracer = state.tracer
    event_bus = tracer.event_bus

    state.steps.append("Tool agent")

    state.tool_result = execute_tool(state.goal)

    event_bus.publish(
        "tool.executed",
        {
            "trace_id": tracer.trace_id,
            "component": "tool",
            "status": "completed",
            "metadata": {
                "goal_length": len(state.goal),
            },
        },
    )

    return state
