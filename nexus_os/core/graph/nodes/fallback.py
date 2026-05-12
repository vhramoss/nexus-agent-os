from nexus_os.core.agent_state import AgentState


def fallback_node(state: AgentState) -> AgentState:
    state.steps.append("Global fallback executed")

    state.llm_output = (
        "[GLOBAL FALLBACK]\n"
        "Multi-agent execution failed.\n"
        "Returning safe default response."
    )

    return state