class Capability:
    READ_MEMORY = "read_memory"
    WRITE_MEMORY = "write_memory"
    CALL_TOOL = "call_tool"
    USE_LLM = "use_llm"
    NETWORK = "network"
    USE_TOOL = "use_tool"


class CapabilitySet:
    def __init__(self, allowed: set[str]):
        self.allowed = allowed

    def allows(self, capability: str) -> bool:
        return capability in self.allowed
