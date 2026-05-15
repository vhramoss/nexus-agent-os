def emit_agent_started(agent, goal: str):
    agent.event_bus.publish(
        "agent.started",
        {
            "trace_id": agent.trace_id,
            "component": "agent",
            "status": "started",
            "metadata": {"goal": goal},
        },
    )


def emit_agent_completed(agent):
    agent.event_bus.publish(
        "agent.completed",
        {
            "trace_id": agent.trace_id,
            "component": "agent",
            "status": "completed",
            "metadata": {"status": agent.state.status},
        },
    )