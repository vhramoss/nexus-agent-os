from nexus_os.core.graph.policies.routing import routing_policy


def test_routing_returns_planner_when_no_semantic_recall():
    # Arrange
    state = type("State", (), {})()
    state.semantic_recall = []
    state.steps = []  # ✅ ESSENCIAL

    # Act
    result = routing_policy(state)

    # Assert
    assert result == "plan"

def test_routing_returns_llm_when_semantic_recall_has_results():
    # Arrange
    state = type("State", (), {})()
    state.semantic_recall = [{"text": "something"}]
    state.steps = []  # ✅ ESSENCIAL

    # Act
    result = routing_policy(state)

    # Assert
    assert result == "direct"