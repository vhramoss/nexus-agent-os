from nexus_os.core.agent_state import AgentState


def reviewer_agent_node(state: AgentState) -> AgentState:
    state.steps.append("Reviewer agent")

    if "error" in (state.analysis or "").lower():
        state.reviewer_failed = True
        state.steps.append("Review failed")
        return state

    state.reviewer_failed = False
    state.steps.append("Review passed")
    return state
