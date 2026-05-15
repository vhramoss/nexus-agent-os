from nexus_os.core.agent_state import AgentState
from nexus_os.core.security.guarded import guarded
from nexus_os.core.security.capabilities import Capability

def tool_agent_node(state: AgentState) -> AgentState:
    
    tracer = state.tracer

    with tracer.span("tool"):
        state.steps.append("Tool agent")

        state.tool_result = {
            "computed_value": len(state.goal),
            "status": "ok",
        }

    return state

tool_agent_node = guarded(tool_agent_node, Capability.CALL_TOOL)