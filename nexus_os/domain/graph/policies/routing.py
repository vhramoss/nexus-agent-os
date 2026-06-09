from nexus_os.core.agent_state import AgentState


def routing_policy(state: AgentState) -> str:
    """
    Decide a rota do grafo com base no estado atual.

    Retorna:
    - "direct": pula o planner e vai direto para o LLM
    - "plan": passa pelo planner/executor
    """

    if state.semantic_recall:
        state.steps.append("Decision: direct execution (semantic recall hit)")
        return "direct"

    state.steps.append("Decision: planning required")
    return "plan"
