from nexus_os.core.security.sandbox import enforce
from nexus_os.core.security.capabilities import Capability


def persist_memory(agent):
    state = agent.state

    enforce(state.capabilities, Capability.WRITE_MEMORY)

    record = {
        "agent_id": agent.agent_id,
        "goal": state.goal,
        "steps": state.steps,
        "output": state.llm_output,
        "status": state.status,
    }

    agent.memory_store.save(record)

    if state.llm_output:
        agent.vector_store.add(
            text=state.llm_output,
            metadata={
                "goal": state.goal,
                "agent_id": agent.agent_id,
            },
        )