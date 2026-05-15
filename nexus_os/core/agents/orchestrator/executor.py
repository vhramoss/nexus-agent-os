from nexus_os.core.graph.execution_graph import build_execution_graph


def execute_graph(agent):
    graph = build_execution_graph()

    with agent.tracer.span("graph.invoke"):
        graph.invoke(agent.state)

    agent.state.status = "completed"