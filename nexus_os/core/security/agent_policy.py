from nexus_os.core.security.capabilities import Capability, CapabilitySet


DEFAULT_AGENT_POLICY = CapabilitySet({
    Capability.READ_MEMORY,
    Capability.WRITE_MEMORY,
    Capability.USE_LLM,
})

PLANNER_POLICY = CapabilitySet({
    Capability.READ_MEMORY,
    Capability.USE_LLM,
})

EXECUTOR_POLICY = CapabilitySet({
    Capability.CALL_TOOL,
})